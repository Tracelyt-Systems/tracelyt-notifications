# Webhook Security and SSRF Defense Architecture

This document establishes the security architecture and defensive controls required for dispatching outbound HTTP webhooks to customer-configured destinations.

> **CRITICAL SECURITY BOUNDARY**: Under no circumstances may an untrusted tenant configuration turn `tracelyt-notifications` into an unrestricted HTTP proxy capable of probing, scanning, or attacking internal infrastructure.

---

## 1. Threat Landscape for Outbound Webhooks

When a service makes HTTP requests to arbitrary URLs provided by end-users, it is exposed to:
1. **Server-Side Request Forgery (SSRF)**: Reaching internal microservices (`http://control-plane.internal:8080`), database management ports, or container network endpoints.
2. **Cloud Metadata Exfiltration**: Accessing link-local endpoints (`http://169.254.169.254/latest/meta-data/` on AWS, `metadata.google.internal` on GCP) to steal service account credentials.
3. **DNS Rebinding Attacks**: An attacker configures a domain that resolves to a public IP during initial URL validation, but resolves to `127.0.0.1` when the HTTP connection is established.
4. **Denial of Service (Slowloris / Resource Exhaustion)**: Webhook servers that accept TCP connections but never send data, consume connection pools, or return infinite chunked streams.
5. **Open Redirect Abuse**: A public webhook endpoint returning HTTP 301/302 redirects targeting internal IP addresses.

---

## 2. Multi-Layer SSRF Defense Architecture

```mermaid
graph TD
    A[Tenant Configured Webhook URL] --> B[URL Parser & Protocol Validation]
    B -->|Must be HTTPS only| C[DNS Resolution & IP Validation]
    C -->|Check IP against Blacklist| D{Is IP Public & Routable?}
    D -- No (RFC 1918 / Loopback / Metadata) --> E[Reject Delivery & Flag Suspicious]
    D -- Yes --> F[Pin Socket to Validated IP]
    F --> G[Execute HTTP POST with SNI]
    G -->|Enforce Strict Timeouts & Size Limits| H[Receive Response Header]
    H -->|Redirect Attempt?| I{Follow Redirects?}
    I -- Redirect Detected --> J[Abort Immediately - No Redirects Allowed]
    I -- Final 2xx Response --> K[Record Success Receipt]
```

### 2.1 URL Validation Rules
- **Protocol**: Only `https://` is permitted in production environments (`http://` is allowed exclusively in local development with explicit mock flags).
- **Port**: Restricted to standard HTTPS port `443` or an approved explicit allowlist (e.g., `8443`). Arbitrary low ports (`< 1024`) and internal service ports are strictly forbidden.
- **UserInfo**: URLs containing credentials (e.g., `https://user:pass@example.com`) are rejected.

### 2.2 IP Address Blacklisting
Prior to initiating a TCP handshake, the target hostname must be resolved via DNS, and all resolved IPv4/IPv6 addresses must be validated against the following blacklists:
- **IPv4 Loopback**: `127.0.0.0/8`
- **RFC 1918 Private Ranges**: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16`
- **Link-Local & Cloud Metadata**: `169.254.0.0/16`
- **Broadcast / Reserved**: `0.0.0.0/8`, `224.0.0.0/4`, `240.0.0.0/4`
- **IPv6 Loopback & Link-Local**: `::1/128`, `fe80::/10`, `fc00::/7`
- **IPv4-Mapped IPv6**: `::ffff:0:0/96` (checked against IPv4 rules)

### 2.3 DNS Rebinding Mitigation
To prevent Time-of-Check to Time-of-Use (TOCTOU) DNS rebinding attacks:
1. The DNS resolver resolves the target hostname and validates that the resolved IP address is public.
2. The HTTP client initiates the raw TCP connection directly to the **validated IP address**.
3. During the TLS handshake, the original hostname is passed as the **Server Name Indication (SNI)** and checked against the server's X.509 certificate.
4. The HTTP client **must not** re-resolve DNS during connection retry or redirect phases.

### 2.4 Redirect Handling
- The webhook HTTP client must explicitly configure:
  ```java
  HttpClient.newBuilder()
      .followRedirects(HttpClient.Redirect.NEVER)
      .build();
  ```
- If a target endpoint returns an HTTP 3xx redirect status, the delivery attempt is marked as failed. Automated redirect traversal is strictly prohibited.

---

## 3. Webhook Payload Integrity and Signing (HMAC-SHA256)

To allow receiving systems to verify that a webhook payload genuinely originated from Tracelyt:
1. Every webhook request must include cryptographic signature headers:
   - `X-Tracelyt-Signature-Timestamp`: Unix timestamp (seconds) of dispatch.
   - `X-Tracelyt-Signature`: Hex-encoded HMAC-SHA256 hash computed over `${timestamp}.${raw_payload_body}` using a tenant-specific shared secret.
2. The receiving server can verify the HMAC signature and reject requests where `abs(now - timestamp) > 300` seconds to defend against replay attacks.

---

## 4. Resource Limits & DoS Protection

| Parameter | Enforced Limit | Rationale |
| :--- | :--- | :--- |
| **Connection Timeout** | 2 seconds | Prevents hung sockets during TCP SYN floods. |
| **Response/Read Timeout** | 5 seconds | Guards against slowloris attacks. |
| **Maximum Request Body** | 256 KB | Prevents memory exhaustion on worker nodes. |
| **Maximum Response Body Read**| 4 KB | Tracelyt only inspects status codes and brief error messages; does not download arbitrary files. |

---

## 5. Related Documentation

- [Threat Model](threat-model.md)
- [Deployment Models](../architecture/deployment-models.md)
- [Delivery Reliability](../architecture/delivery-reliability.md)

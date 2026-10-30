# Threat Model

This document outlines the threat modeling analysis for the future `tracelyt-notifications` delivery service, utilizing the STRIDE methodology.

---

## 1. Assets, Boundaries, and Actors

### 1.1 Protected Assets
1. **Provider Credentials**: API keys for external services (SendGrid, Slack, Discord, AWS SES).
2. **Webhook Secrets**: Shared secret keys used for signing outbound HMAC webhook payloads.
3. **Internal Platform Infrastructure**: Private endpoints, control-plane databases, and cloud metadata services (`169.254.169.254`).
4. **Tenant Delivery Data & PII**: Recipient email addresses, channel webhooks, and alert message content.
5. **System Availability & Quotas**: Network bandwidth, provider rate limits, and egress worker thread pools.

### 1.2 Trust Boundaries
- **Boundary 1 (External Webhooks)**: Outbound requests to customer-controlled HTTP servers.
- **Boundary 2 (Public Provider APIs)**: Egress connections to third-party SaaS platforms.
- **Boundary 3 (Internal Tracelyt Core)**: Ingress connections from authenticated internal services (`tracelyt-alerting`, `tracelyt-control-plane`).
- **Boundary 4 (Storage & State)**: Connection to the internal delivery state database.

---

## 2. Threat Analysis Matrix (STRIDE)

| ID | STRIDE Category | Asset / Boundary | Attack Scenario | Impact | Proposed Mitigation | Owning Component | Residual Risk | Status |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **TM-01** | Information Disclosure | Provider Credentials | Provider API keys logged in plaintext during outbound HTTP failure or exception trace. | Severe credential compromise; unauthorized third-party billing. | Strict SLF4J log masking filters; sanitization of HTTP headers and bodies in logging interceptors. | Provider Adapter Layer | Misconfigured third-party logging appenders. | Proposed |
| **TM-02** | Elevation of Privilege | Internal Network | Malicious tenant configures webhook URL targeting cloud metadata (`http://169.254.169.254/latest/meta-data/`) to steal IAM roles. | Complete cloud environment takeover (SSRF). | Enforce private IP filtering, block link-local/RFC 1918 ranges, route egress via dedicated proxy. | Webhook Engine / Egress Proxy | Zero-day bypass in HTTP client parser. | Proposed |
| **TM-03** | Elevation of Privilege | Internal Network | Attacker configures webhook domain with low TTL pointing to public IP, which resolves to `127.0.0.1` upon subsequent connection (DNS Rebinding). | Bypass of initial IP validation; access to internal control plane APIs. | Resolve DNS once, validate IP, and connect directly to the validated IP socket with TLS SNI matching the domain. | Webhook HTTP Client | Complex TLS handshake configurations. | Proposed |
| **TM-04** | Tampering | External Webhook | Tenant webhook endpoint responds with HTTP 302 redirecting to internal service (`http://control-plane.internal:8080/admin`). | Unauthorized internal API invocation via redirect following. | Disable automatic HTTP redirect following in webhook dispatch client (`HttpClient.Redirect.NEVER`). | Webhook Engine | None. | Proposed |
| **TM-05** | Information Disclosure | Tenant Delivery Data | Tenant A queries delivery status endpoint supplying a `notificationId` belonging to Tenant B. | Cross-tenant data leak and notification content exposure. | Cryptographic verification of tenant context against request token; mandatory tenant scoping in state queries. | Intake & API Layer | Logic bug in authorization filter. | Proposed |
| **TM-06** | Denial of Service | System Resources | Malicious or runaway alert rule generates 100,000 notifications per minute, exhausting worker threads and provider budgets. | System starvation; dropped critical alert notifications; high provider cost. | Multi-tier rate limiting (per-tenant, per-project, per-provider); priority queue shedding for non-critical alerts. | Rate Limiter & Queue Engine | Distributed flood exhausting ingress memory. | Proposed |
| **TM-07** | Tampering | Recipient Browser / Client | Alert title contains malicious HTML/JavaScript (`<script>...`) rendered unsanitized in HTML email notifications. | Stored Cross-Site Scripting (XSS) in recipient email client or webmail session. | Context-aware HTML escaping in email template rendering engine; strict Content Security Policy headers. | Template Rendering Engine | Complex markdown rendering engine edge cases. | Proposed |
| **TM-08** | Spoofing | Webhook Receiver | Man-in-the-middle or spoofed server injects fake delivery confirmations to falsify audit logs. | Corrupted delivery history and false compliance claims. | Mandatory TLS 1.2/1.3 for all destinations; certificate validation enabled; HMAC payload signatures. | Webhook Dispatcher | Expired or untrusted root CAs. | Proposed |
| **TM-09** | Repudiation | Delivery State | Operator or tenant claims a critical notification was never delivered or was lost by Tracelyt. | Legal dispute or unresolved SLA failure during critical outage. | Immutable delivery attempt audit logging with provider response IDs and timestamped state transitions. | State Persistence Layer | Database disk exhaustion causing log loss. | Proposed |
| **TM-10** | Denial of Service | External Providers | Rapid retries against rate-limited provider (HTTP 429) result in permanent IP blacklisting by provider. | Platform-wide delivery outage across all tenants using shared provider. | Exponential backoff with full jitter; honoring `Retry-After` headers; circuit breaker integration. | Retry Scheduler & Circuit Breaker | Misconfigured provider returning malformed Retry-After headers. | Proposed |
| **TM-11** | Information Disclosure | Recipient PII | Recipient email addresses and phone numbers retained indefinitely in delivery history tables. | Regulatory non-compliance (GDPR, CCPA) and unauthorized PII exposure in database dumps. | Configurable data retention policies (e.g., 30-day purge); automated PII masking in archival logs. | Data Retention Engine | Backups retaining unmasked records beyond TTL. | Proposed |
| **TM-12** | Tampering | Supply Chain | Malicious dependency update introduces backdoor or credential exfiltration code into build artifact. | Arbitrary code execution during runtime and secret exfiltration. | Dependabot automated scanning; commit SHA pinning for GitHub Actions; dependency review workflow. | CI/CD Pipeline | Zero-day vulnerability in approved dependency. | Implemented |
| **TM-13** | Denial of Service | Egress Network | Slowloris-style attack where customer webhook server accepts TCP connection but transmits zero bytes, hanging worker thread. | Worker thread pool exhaustion; delivery paralysis. | Strict connection timeout (2s) and read/socket timeout (5s); global virtual thread concurrency limits. | Webhook HTTP Client | High connection churn on network interface. | Proposed |
| **TM-14** | Information Disclosure | Provider Metadata | Error response from third-party provider containing sensitive customer data is reflected back in public API responses. | Information disclosure to unprivileged users. | Normalize all errors to RFC 9457 Problem Details; strip raw provider error bodies from client responses. | Error Handling Layer | Incomplete error normalization mapping. | Proposed |

---

## 3. Threat Model Governance

This threat model must be updated whenever:
1. A new notification channel (e.g., SMS, PagerDuty, WhatsApp) is evaluated.
2. Changes are made to outbound network routing or egress proxies.
3. An ADR proposing secondary language runtimes or new persistence engines is accepted.

---

## 4. Related Documentation

- [Security Overview](README.md)
- [Webhook Security & SSRF Protection](webhook-security.md)
- [Secret Management](secret-management.md)
- [Supply Chain Security](supply-chain.md)

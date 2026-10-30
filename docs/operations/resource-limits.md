# Resource Limits, Timeouts, and Quotas

This document defines the operational resource boundaries, network timeouts, and tenant quotas enforced by `tracelyt-notifications`.

---

## 1. Network & Socket Timeouts

To prevent hung threads and slowloris attacks during outbound provider and webhook communication:

| Interaction Type | Connect Timeout | Read / Socket Timeout | Total Request Budget |
| :--- | :--- | :--- | :--- |
| **Transactional Email API (HTTPS)** | 3,000 ms | 5,000 ms | 10,000 ms |
| **Chat Providers (Slack / Discord)**| 2,000 ms | 4,000 ms | 8,000 ms |
| **Tenant Webhooks (Untrusted)** | 2,000 ms | 5,000 ms | 7,000 ms |
| **Internal Database Operations** | 1,000 ms | 3,000 ms | 5,000 ms |

If a provider or webhook endpoint fails to respond within the Total Request Budget, the attempt is aborted with a `TIMEOUT` failure category and scheduled for exponential retry.

---

## 2. Payload and Size Limits

| Data Element | Enforced Limit | Violation Action |
| :--- | :--- | :--- |
| **Intake Request JSON Body** | 512 KB | Rejected with HTTP 413 Content Too Large. |
| **Webhook Outbound Body** | 256 KB | Payload truncated or rejected before dispatch. |
| **Webhook Response Body Read Cap** | 4 KB | Truncated; body read stream terminated. |
| **Email HTML Template Body** | 1 MB | Template compilation rejected. |

---

## 3. Tenant Delivery Quotas (Planned)

To prevent resource monopolization:
- **Default Ingress Rate**: 100 notification requests per minute per tenant.
- **Burst Capacity**: Up to 300 requests in a 10-second burst.
- **Concurrent In-Flight Deliveries**: Maximum 50 concurrent outbound deliveries per tenant.

Requests exceeding quotas receive HTTP 429 Too Many Requests with a `Retry-After` header.

---

## 4. Related Documentation

- [Configuration Policy](configuration.md)
- [Rate Limiting](../architecture/rate-limiting.md)
- [Webhook Security](../security/webhook-security.md)

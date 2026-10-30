# Error Handling Standards and Problem Details

This document defines the error classification taxonomy, HTTP status conventions, and RFC 9457 error response formats for `tracelyt-notifications`.

---

## 1. RFC 9457 Problem Details Standard

All client-facing error responses emitted by HTTP endpoints must conform to [RFC 9457 (Problem Details for HTTP APIs)](https://www.rfc-editor.org/rfc/rfc9457.html) with content type `application/problem+json`:

```json
{
  "type": "https://api.tracelyt.io/errors/invalid-recipient-target",
  "title": "Invalid Recipient Destination",
  "status": 400,
  "detail": "The specified webhook destination URL 'http://127.0.0.1:8080' violates SSRF security policies.",
  "instance": "/api/v1/notifications/req-01928374-1234",
  "code": "ERR_SECURITY_SSRF_BLOCKED",
  "timestamp": "2026-10-30T10:46:15Z"
}
```

---

## 2. Delivery Error Taxonomy

Errors encountered during notification delivery are categorized to determine retry eligibility:

| Category | Description | HTTP Status | Retryable? | Action Taken |
| :--- | :--- | :--- | :--- | :--- |
| `VALIDATION_FAILED` | Request schema violation or missing mandatory fields. | 400 Bad Request | No | Immediate rejection; caller must fix payload. |
| `DESTINATION_REJECTED` | SSRF blocked, invalid email format, or webhook domain unresolvable. | 422 Unprocessable | No | Permanent failure; routed to DLQ. |
| `PROVIDER_RATE_LIMITED` | External provider returned HTTP 429 Too Many Requests. | 429 Too Many Requests | Yes | Exponential backoff respecting `Retry-After`. |
| `PROVIDER_TEMPORARY_ERROR` | External provider returned HTTP 500, 502, 503, or connection timeout. | 503 Service Unavailable | Yes | Exponential backoff with full jitter. |
| `PROVIDER_AUTHENTICATION_ERROR` | Provider API key expired, revoked, or invalid (HTTP 401/403). | 502 Bad Gateway | No | Provider suspended; alerts sent to tenant admin. |
| `CONTENT_TOO_LARGE` | Rendered template or webhook payload exceeds maximum size. | 413 Payload Too Large | No | Permanent failure; routed to DLQ. |

---

## 3. Related Documentation

- [Delivery Reliability](../architecture/delivery-reliability.md)
- [Contract Governance](contract-governance.md)
- [Coding Standards](../development/coding-standards.md)

# Contracts & Cross-Service Schema Governance

This directory documents the boundary integration between `tracelyt-notifications` and the canonical schema repository: [`tracelyt-specs`](https://github.com/Tracelyt-Systems/tracelyt-specs).

---

## Canonical Authority Notice

**The `tracelyt-specs` repository is the sole canonical source of truth for all shared Tracelyt contracts.**

The notification subsystem must **not** independently invent conflicting schemas, ad-hoc JSON formats, or private gRPC definitions for:
- Notification request schemas.
- Notification intent event envelopes dispatched by `tracelyt-alerting`.
- Delivery status schemas (`Accepted`, `Pending`, `Delivered`, `Failed`, `RetryScheduled`).
- Channel destination configurations and provider references.
- RFC 9457 Problem Details error envelopes.
- Tenant and project context propagation (`X-Tracelyt-Tenant-ID`, `X-Tracelyt-Project-ID`).

---

## Planned Shared Contracts

| Contract Domain | Target File in `tracelyt-specs` | Purpose |
|---|---|---|
| **Notification Intent** | `schemas/notifications/notification-intent.v1.json` | Event payload received from `tracelyt-alerting` requesting message delivery. |
| **Notification Request** | `schemas/notifications/notification-request.v1.json` | Direct API request for administrative or transactional notifications. |
| **Delivery Status Event** | `schemas/notifications/delivery-status.v1.json` | Status update event emitted to notify platform components of delivery outcomes. |
| **Error Format** | `schemas/common/problem-details.v1.json` | RFC 9457 sanitized error representation. |

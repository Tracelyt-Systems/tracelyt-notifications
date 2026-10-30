# Multi-Tenant Isolation Architecture

This document describes the multi-tenant isolation model, authorization boundaries, and credential segregation policies for `tracelyt-notifications`.

---

## 1. Multi-Tenancy Principles

In a multi-tenant observability platform, notification delivery involves high-risk shared resources: outbound provider API accounts, delivery state databases, and worker thread pools.

Core isolation principles:
1. **No Implicit Tenant Trust**: A tenant identifier supplied in an intake request body must never be accepted without verification against a trusted, cryptographically signed internal JWT or mTLS peer identity supplied by `tracelyt-alerting` or `tracelyt-control-plane`.
2. **Storage Partitioning**: Every database query, state transition, and delivery attempt record must be explicitly scoped by `tenant_id`. Cross-tenant queries are architecturally impossible at the repository layer.
3. **Dedicated Credential Boundaries**: Tenant A can never invoke a provider configuration, webhook signing secret, or Slack integration configured by Tenant B.
4. **Tenant-Level Fair Queuing**: Runaway alert generation in one tenant must never saturate shared egress worker pools and starve delivery for other tenants.

---

## 2. Tenant Context Propagation

Every notification intake request must supply a standardized contextual envelope:

```json
{
  "tenantId": "tenant-8f19b2a1",
  "projectId": "proj-44b1c900",
  "correlationId": "corr-01928374-1234",
  "sourceService": "tracelyt-alerting"
}
```

- **Validation Gate**: The intake filter checks that the caller possesses valid claims authorizing it to dispatch notifications for `tenantId` and `projectId`.
- **Thread Context / Reactor Context**: Once validated, the `TenantContext` is bound to the execution thread or reactive stream and passed down to the provider adapter layer.

---

## 3. Provider Configuration Segregation

Tracelyt supports two provider ownership tiers:
1. **Platform-Provided (Shared Infrastructure)**:
   - Tracelyt platform operators provision shared email or SMS infrastructure.
   - Tenants share egress accounts subject to strict per-tenant rate-limiting quotas and fair-usage policies.
2. **Bring-Your-Own-Provider (Tenant-Dedicated)**:
   - Tenants configure their own SendGrid API keys, Slack App OAuth tokens, or Discord webhooks in `tracelyt-control-plane`.
   - Credentials are encrypted at rest with tenant-specific encryption keys.
   - Worker processes decrypt tenant credentials on-demand and discard them immediately after request dispatch.

---

## 4. Delivery Status & Audit Access

- **Read Isolation**: APIs exposing delivery status (`/api/v1/notifications/{id}`) must require tenant authentication and enforce:
  ```sql
  SELECT * FROM notification_requests 
  WHERE id = :id AND tenant_id = :authenticatedTenantId;
  ```
- **Audit Trails**: Security audits record all cross-service requests with `tenant_id`, `actor_id`, and `destination_type` for forensic traceability.

---

## 5. Related Documentation

- [Security Overview](README.md)
- [Threat Model](threat-model.md)
- [System Boundaries](../architecture/system-boundaries.md)
- [Rate Limiting](../architecture/rate-limiting.md)

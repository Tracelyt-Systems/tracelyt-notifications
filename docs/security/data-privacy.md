# Data Privacy and PII Minimization

This document outlines the data privacy principles, personally identifiable information (PII) minimization rules, and retention lifecycles for `tracelyt-notifications`.

---

## 1. PII and Sensitive Data Classification

Notification messages inherently touch sensitive communications:
- **Direct PII**: Recipient email addresses, telephone numbers, user display names, Slack user IDs.
- **Indirect PII & Telemetry Context**: Hostnames, IP addresses, stack traces, and database query snippets contained within alert notification bodies.
- **Security Tokens**: Webhook signing secrets and provider bearer tokens.

---

## 2. Data Minimization Principles

1. **Storage Minimization**:
   - `tracelyt-notifications` persists metadata required for delivery orchestration and operational audits, not long-term content archives.
   - Once a notification reaches a terminal state (`DELIVERED` or `FAILED`), full rendered message bodies (HTML/JSON) are scrubbed from storage after a short operational window (e.g., 7 days).
2. **Log Redaction**:
   - Operational logs must mask recipient email addresses: `j***n@example.com`.
   - Webhook query parameters and payload bodies must never be dumped to stdout in production environments.
3. **Metric Anonymization**:
   - High-cardinality PII (e.g., individual email addresses, recipient user IDs, webhook URLs) must **never** be used as Prometheus metric labels.
   - Metrics should aggregate exclusively by `channel`, `provider_type`, `tenant_id`, and `status`.

---

## 3. Retention Schedules & Purging

| Data Category | Retention Period | Purge Mechanism |
| :--- | :--- | :--- |
| **Active Delivery Queue** | Transient (< 24 hours) | Discarded upon terminal state. |
| **Delivery Attempt Logs (Metadata)** | 30 days | Automated rolling partition drop or background reaper job. |
| **Rendered Message Bodies** | 7 days | Scheduled scrubbing job. |
| **Dead-Letter Queue (DLQ)** | 14 days | Operator inspection window; auto-purged on expiration. |

---

## 4. Privacy Regulations (GDPR / CCPA)

- **Right to Erasure (Forgotten)**: When `tracelyt-control-plane` issues a tenant or user deletion event, `tracelyt-notifications` must delete or pseudonymize all associated delivery history records.
- **No Unsubstantiated Compliance Claims**: Tracelyt does not claim certified GDPR or HIPAA compliance in repository documentation without verified third-party legal assessment.

---

## 5. Related Documentation

- [Security Overview](README.md)
- [Storage Strategy](../architecture/storage-strategy.md)
- [Tenant Isolation](tenant-isolation.md)

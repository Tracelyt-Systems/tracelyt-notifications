# Storage Strategy & Persistence Architecture

This document evaluates the persistence backends, storage models, and archival lifecycles planned for `tracelyt-notifications`.

---

## 1. Subsystem Data Categories

The notification engine persists multiple distinct categories of data:

| Data Category | Durability & Consistency Requirement | Retention Lifecycle | Primary Storage Candidate |
|---|---|---|---|
| **Notification Requests & Status** | High (ACID transaction) | 30 to 90 days | Relational Database (PostgreSQL) |
| **Delivery Attempt Logs** | High (Audit & compliance) | 30 days hot, 1 year cold | Relational DB ➔ Object Storage (S3/GCS) |
| **Idempotency Keys** | High write speed, atomic check-and-set | 24-hour TTL | In-Memory KV Cache (Redis) / DB Unique Index |
| **Provider Configurations** | High (Sensitive encrypted metadata) | Persistent | Relational Database (Encrypted at rest) |
| **Dead-Letter Quarantine** | Critical (Requires human inspection) | 180 days | Dedicated Relational Quarantine Table |

---

## 2. Storage Candidate Evaluations

- **PostgreSQL (Recommended Primary Store):** Offers native JSONB indexing for arbitrary provider response headers, `SKIP LOCKED` for queue processing, and row-level tenant isolation.
- **Object Storage (Archival Store):** Completed delivery logs and attempt histories older than 30 days are automatically compressed and offloaded to cheap object storage (S3/GCS/MinIO) for regulatory compliance.
- **Premature Commitment Guard:** No JPA dependencies, database drivers, or connection pools are included in this foundation setup.

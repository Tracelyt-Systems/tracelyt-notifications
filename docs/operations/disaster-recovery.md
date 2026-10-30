# Disaster Recovery and High Availability

This document describes the high-availability topology, failover mechanics, and data recovery procedures for `tracelyt-notifications`.

---

## 1. High-Availability Architecture

To achieve zero downtime for critical alert notifications:
1. **Multi-Node Intake**: Minimum of two intake service instances behind a load balancer.
2. **Stateless Processing**: Worker nodes do not store session state in-memory; all state transitions are committed to a transactional store.
3. **Database High Availability**: PostgreSQL primary with synchronous or semi-synchronous streaming replication to a standby instance in an alternate availability zone.

---

## 2. Recovery Scenarios and Mitigations

### 2.1 Worker Node Crash During Delivery
- **Failure Mode**: A worker JVM crashes after dispatching an email to Amazon SES but before recording `DELIVERED` status in the database.
- **Mitigation**:
  - Unacknowledged jobs are detected by a background lease heartbeat reaper after a timeout (e.g., 2 minutes).
  - The job is reassigned to an active worker.
  - The worker uses the **Idempotency Key** when communicating with the provider, allowing the provider to return the existing delivery receipt without sending a duplicate message.

### 2.2 Primary Provider Outage (e.g., SendGrid Down)
- **Failure Mode**: The primary email provider returns HTTP 500 or times out across all delivery attempts.
- **Mitigation**:
  - Circuit breaker trips to `OPEN` state after error threshold is breached.
  - Delivery engine consults tenant failover configuration.
  - If a secondary provider (e.g., AWS SES) is configured and policy permits, traffic automatically fails over to the backup adapter.

### 2.3 Database Outage (Transactional Outbox Buffering)
- **Failure Mode**: State store becomes temporarily unreachable.
- **Mitigation**:
  - Ingestion buffer or message broker holds incoming notification requests.
  - Workers pause queue polling until database connectivity is restored and health probes return HTTP 200.

---

## 3. RPO and RTO Targets

| Disaster Tier | Recovery Point Objective (RPO) | Recovery Time Objective (RTO) |
| :--- | :--- | :--- |
| **Worker Node Crash** | 0 seconds (Stateless) | < 30 seconds (Automatic lease reclamation) |
| **Primary DB Failover** | < 5 seconds (Replication lag) | < 60 seconds (Automated standby promotion) |
| **Complete Region Outage** | < 1 hour (Offsite backup sync) | < 4 hours (Multi-region infrastructure redeploy) |

---

## 4. Related Documentation

- [Delivery Reliability](../architecture/delivery-reliability.md)
- [Provider Model](../architecture/provider-model.md)
- [Observability](observability.md)

# Event Governance and Delivery Envelopes

This document establishes the event governance policies, envelope conventions, and idempotency standards for asynchronous notification events.

---

## 1. CloudEvents Compliance

All asynchronous notification events dispatched to or from message brokers must adhere to the [CloudEvents v1.0 Specification](https://cloudevents.io/):

```json
{
  "specversion": "1.0",
  "type": "io.tracelyt.notifications.delivery.attempt.completed",
  "source": "https://notifications.tracelyt.io/nodes/worker-01",
  "id": "evt-01928374-5678",
  "time": "2026-10-30T10:46:30Z",
  "datacontenttype": "application/json",
  "tracelyttenantid": "tenant-8f19b2a1",
  "tracelytprojectid": "proj-44b1c900",
  "tracelytcorrelationid": "corr-01928374-1234",
  "data": {
    "notificationId": "notif-01928374-1234",
    "attemptNumber": 1,
    "channel": "EMAIL",
    "provider": "AWS_SES",
    "status": "DELIVERED",
    "providerReceipt": "0100018a-ses-1234",
    "durationMillis": 245
  }
}
```

---

## 2. Event Lifecycle Conventions

1. **`io.tracelyt.notifications.request.accepted`**: Emitted when a notification intent is validated and enqueued.
2. **`io.tracelyt.notifications.delivery.attempt.started`**: Emitted when a worker leases the job and initiates outbound delivery.
3. **`io.tracelyt.notifications.delivery.attempt.completed`**: Emitted upon successful provider delivery.
4. **`io.tracelyt.notifications.delivery.attempt.failed`**: Emitted when an attempt fails (transient or permanent).
5. **`io.tracelyt.notifications.dead_lettered`**: Emitted when a notification exhausts retries and is moved to the DLQ.

---

## 3. Idempotency Key Semantics

- **Format**: `idem-{tenantId}-{sourceEventId}-{timestamp}`
- **Deduplication Window**: Idempotency keys must be indexed with a unique constraint and retained for a minimum of 24 hours.
- If a duplicate event arrives with an identical idempotency key, the intake system acknowledges the request immediately with the existing `notificationId` without triggering duplicate provider dispatch.

---

## 4. Related Documentation

- [Contract Governance](contract-governance.md)
- [Delivery Reliability](../architecture/delivery-reliability.md)
- [Messaging Strategy](../architecture/messaging-strategy.md)

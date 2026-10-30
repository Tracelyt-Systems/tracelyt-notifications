# Subsystem Observability and Telemetry

This document outlines the operational metrics, structured logging, distributed tracing, and self-monitoring architecture for `tracelyt-notifications`.

---

## 1. Observability Principles

As an observability platform component delivering alert notifications:
1. **Self-Monitoring Without Feedback Loops**: If the notification service experiences delivery failures, it must not trigger recursive alert storms that flood itself.
2. **Cardinality Discipline**: Metric labels must strictly avoid unbounded values (no email addresses, webhook URLs, or raw user IDs).
3. **Structured Context**: All log entries must be emitted as JSON with trace correlation IDs and tenant identifiers.

---

## 2. Key Operational Metrics (Prometheus / Micrometer)

| Metric Name | Type | Labels | Description |
| :--- | :--- | :--- | :--- |
| `notifications_received_total` | Counter | `source`, `tenant_id`, `category` | Total notification requests accepted at intake. |
| `notifications_delivered_total` | Counter | `channel`, `provider`, `status` | Successful deliveries confirmed by provider. |
| `notifications_failed_total` | Counter | `channel`, `provider`, `error_category` | Permanent delivery failures routed to DLQ. |
| `notifications_retries_total` | Counter | `channel`, `provider` | Transient delivery retry attempts executed. |
| `notification_delivery_latency_seconds` | Histogram | `channel`, `provider` | End-to-end latency from intake acceptance to provider delivery. |
| `notification_provider_latency_seconds` | Histogram | `provider`, `channel` | Outbound HTTP/network latency to external provider API. |
| `notification_queue_depth` | Gauge | `channel`, `priority` | Current count of queued notifications waiting for dispatch. |
| `notification_dlq_count` | Gauge | `channel`, `tenant_id` | Count of unhandled dead-letter notifications. |
| `notification_rate_limited_total` | Counter | `tenant_id`, `scope` | Ingress or egress rate limit shedding events. |

---

## 3. Structured Logging Architecture

Logs are emitted using SLF4J / Logback with JSON formatting:

```json
{
  "timestamp": "2026-10-30T10:45:00.123Z",
  "level": "INFO",
  "logger": "io.tracelyt.notifications.providers.email.SesAdapter",
  "message": "Notification dispatched successfully to provider",
  "context": {
    "notificationId": "notif-01928374-1234",
    "tenantId": "tenant-8f19b2a1",
    "projectId": "proj-44b1c900",
    "channel": "EMAIL",
    "provider": "AWS_SES",
    "attemptNumber": 1,
    "providerMessageId": "0100018a-ses-1234",
    "traceId": "4bf92f3577b34da6a3ce929d0e0e4736",
    "spanId": "00f067aa0ba902b7"
  }
}
```

---

## 4. Distributed Tracing & W3C TraceContext

- Outbound delivery calls inject standard W3C `traceparent` headers into webhook payloads and supported provider requests.
- Enables end-to-end trace correlation from alert trigger (`tracelyt-alerting`) through notification dispatch to customer webhook receipt.

---

## 5. Health and Readiness Probes

Exposed via Spring Boot Actuator:
- **Liveness Probe**: `GET /actuator/health/liveness` (Returns HTTP 200 if JVM process is responsive).
- **Readiness Probe**: `GET /actuator/health/readiness` (Returns HTTP 200 if state database and queue connections are healthy).

---

## 6. Related Documentation

- [Deployment Readiness](deployment-readiness.md)
- [Configuration Policy](configuration.md)
- [Delivery Reliability](../architecture/delivery-reliability.md)

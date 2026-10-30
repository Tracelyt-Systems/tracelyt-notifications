# Contract Governance and Cross-Service Interoperability

This document defines the schema governance, versioning policies, and cross-service contract lifecycle for `tracelyt-notifications`.

---

## 1. Single Source of Truth: `tracelyt-specs`

To maintain architectural cohesion across the distributed Tracelyt observability platform:
- **Canonical Authority**: All public APIs, inter-service event schemas, and data exchange models must originate from and be formally approved within the [`tracelyt-specs`](../../contracts/README.md) repository.
- **No Local Dialects**: `tracelyt-notifications` must never unilaterally invent conflicting message schemas, event envelopes, or status enumerations.
- **Contract Dependencies**: Future client stubs and schema validators should be generated directly from `tracelyt-specs` Protocol Buffers or JSON Schemas.

---

## 2. Ingress Contract Specification (Planned)

The primary ingress contract defines the notification intent submitted by `tracelyt-alerting`:

```json
{
  "$schema": "https://schemas.tracelyt.io/v1/notification-request.json",
  "id": "notif-01928374-1234",
  "tenantId": "tenant-8f19b2a1",
  "projectId": "proj-44b1c900",
  "sourceService": "tracelyt-alerting",
  "category": "ALERT",
  "severity": "CRITICAL",
  "idempotencyKey": "idem-alert-rule-102-firing-1730282400",
  "recipients": [
    {
      "type": "USER",
      "target": "user-8812"
    },
    {
      "type": "CHANNEL",
      "target": "slack-channel-ops"
    }
  ],
  "content": {
    "title": "High CPU Utilization on node-pool-01",
    "summary": "CPU utilization exceeded 95% for 5 minutes",
    "details": "Triggered by alert rule 'node_cpu_saturation'",
    "metadata": {
      "cluster": "prod-us-east-1",
      "metricValue": 98.4
    }
  },
  "createdTimestamp": "2026-10-30T10:46:00Z"
}
```

---

## 3. Protocol Selection Strategy

| Protocol | Evaluation Status | Target Use Case | Rationale |
| :--- | :--- | :--- | :--- |
| **HTTP/REST (JSON)** | **Initial Baseline** | Intake endpoints, status queries, Actuator probes | Universal debugging, language-neutral, simple firewall traversal. |
| **gRPC / Protobuf** | **Candidate** | High-throughput synchronous inter-service intake | Binary serialization, strongly-typed contracts, HTTP/2 multiplexing. |
| **Kafka / CloudEvents**| **Candidate** | Asynchronous decoupled event intake | Decoupled buffering during incident notification storms. |

---

## 4. Contract Change Process

1. **RFC in `tracelyt-specs`**: Propose new fields or contract modifications in `tracelyt-specs` via an ADR or RFC pull request.
2. **Backward Compatibility Check**: Ensure the change does not break existing consumers (additive changes only; no renaming or removing existing fields without a major version bump).
3. **Approval**: Approval by platform architects.
4. **Adoption**: Bump the `tracelyt-specs` version dependency in `tracelyt-notifications/pom.xml`.

---

## 5. Related Documentation

- [Contracts Index](../../contracts/README.md)
- [Compatibility Policy](compatibility.md)
- [Event Governance](event-governance.md)
- [Error Handling Standards](error-handling.md)

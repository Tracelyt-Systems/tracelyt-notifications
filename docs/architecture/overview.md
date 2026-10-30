# Architecture Overview: Tracelyt Notifications

This document outlines the architectural role, core responsibilities, and system boundaries of `tracelyt-notifications` within the Tracelyt Observability Platform.

---

## 1. Subsystem Identity & Purpose

**Tracelyt Notifications** is the multi-channel notification orchestration and delivery subsystem of the Tracelyt platform.

Its primary responsibility is to provide a reliable, secure, multi-tenant delivery engine that:
1. Ingests approved notification requests and intents from upstream services (such as `tracelyt-alerting` and `tracelyt-control-plane`).
2. Validates recipient references and resolves tenant delivery preferences.
3. Translates generic notification payloads into channel-specific formats (Email, Slack, MS Teams, Discord, Webhooks).
4. Dispatches messages across external provider transports with rate limiting, backoff retries, and dead-letter handling.
5. Emits structured delivery status updates back to the platform for auditability and operational monitoring.

> **Status Notice:** This repository is currently in **Stage 1 (Foundation)**. No actual email dispatchers, Slack/Teams SDK integrations, production webhook clients, database drivers, Kafka/Redis queues, or mock delivery endpoints are implemented.

---

## 2. Core Delivery Boundary Principle

To maintain modularity and avoid monolithic coupling, Tracelyt strictly separates alert lifecycle tracking from notification delivery:

```mermaid
flowchart LR
    subgraph AlertingSubsystem["tracelyt-alerting (Decides WHAT & WHEN)"]
        Eval["Alert Evaluator"] --> State["Incident Lifecycle & Deduplication"]
        State --> Intent["Notification Intent Envelope"]
    end

    subgraph NotificationsSubsystem["tracelyt-notifications (Decides HOW)"]
        Router["Channel Router & Policy"] --> Adapter["Provider Abstraction Layer"]
        Adapter --> Dispatch["Transports (SMTP, Slack, Teams, Webhook)"]
    end

    Intent -->|Dispatched via Queue/API| Router
```

- **`tracelyt-alerting` decides WHAT and WHEN:** Determines whether an alert condition warrants notification, applies suppression/silences, groups alerts into incidents, and emits an idempotent notification intent.
- **`tracelyt-notifications` decides HOW:** Resolves recipient destinations to concrete provider credentials, formats message templates, manages provider API rate limits, handles connection retries, and records delivery receipts.
- **Critical Invariant:** A notification delivery failure (e.g., third-party Slack outage) must **never** alter the underlying alert or incident state in `tracelyt-alerting`.

---

## 3. High-Level Subsystem Flow

```mermaid
sequenceDiagram
    autonumber
    participant Alert as tracelyt-alerting
    participant Intake as Notification Intake
    participant Router as Channel Router
    participant Provider as Provider Adapter
    participant Ext as External Service (Slack/Email/Webhook)
    participant Status as Delivery Status Egress

    Alert->>Intake: 1. Dispatch Notification Intent (Idempotent Event)
    Intake->>Intake: 2. Validate Schema & Verify Idempotency Key
    Intake->>Router: 3. Resolve Destination Channel & Tenant Credential
    Router->>Provider: 4. Format Message Template for Target Channel
    Provider->>Ext: 5. Execute HTTP/SMTP Dispatch (Bounded Timeout)
    alt Dispatch Successful
        Ext-->>Provider: 6. 200 OK / Accepted
        Provider->>Status: 7. Emit DELIVERED Status Event
    else Transient Provider Failure (429 / 5xx)
        Ext-->>Provider: 6. Rate Limited / Timeout
        Provider->>Router: 7. Schedule Exponential Backoff Retry
    end
```

# System Boundaries & Ownership Matrix

This document defines the architectural responsibilities, allowed integrations, and prohibited coupling between `tracelyt-notifications` and the other Tracelyt platform repositories.

---

## 1. Platform Boundary Diagram

```mermaid
flowchart TD
    subgraph Governance["Governance & Configuration"]
        Specs["tracelyt-specs<br><b>(Canonical Shared Contracts)</b>"]
        CP["tracelyt-control-plane<br><b>(Tenants, Users, Preferences, Provider Secrets)</b>"]
    end

    subgraph Producers["Notification Request Producers"]
        Alerting["tracelyt-alerting<br>(Alert & Incident Lifecycle Intents)"]
        AI["tracelyt-ai-investigator<br>(Investigation Summaries)"]
    end

    subgraph NotificationCore["Notification Subsystem (This Repository)"]
        Notif["tracelyt-notifications<br>(Intake Validation, Channel Routing,<br>Template Rendering, Transport Dispatch,<br>Retry Backoff & Rate Limiting)"]
    end

    subgraph ExternalDestinations["External Provider Transports"]
        Email["Email Providers (SES, Resend, SMTP)"]
        Slack["Slack Webhook / Bot API"]
        Teams["Microsoft Teams Webhook / Graph"]
        Discord["Discord Webhooks"]
        Webhooks["Customer HTTP(S) Endpoints"]
    end

    Specs -.->|Contract Governance| Notif
    Specs -.->|Contract Governance| Alerting

    CP -->|1. Tenant Credentials & Notification Routing| Notif
    Alerting -->|2. Emit Idempotent Notification Intent| Notif
    AI -->|2. Emit Approved Summary Intent| Notif

    Notif -->|3. Dispatch Formatted Payload| ExternalDestinations
    Notif -->>|4. Return Delivery Status Event| Specs
```

---

## 2. Ownership Matrix

| Subsystem Repository | Allowed Interaction with Notifications | Prohibited Coupling |
|---|---|---|
| **`tracelyt-alerting`** | Emits idempotent notification intents specifying incident context, severity, and destination references. | Notifications must **not** evaluate alert rules, resolve firing alerts, or manage incident state. Alerting must not execute delivery transports. |
| **`tracelyt-control-plane`** | Manages user profiles, team channel subscriptions, tenant provider credentials, and delivery quotas. | Notifications must **not** become an identity provider, manage organization billing, or issue access tokens. |
| **`tracelyt-specs`** | Canonical source of truth for notification request schemas, intent envelopes, delivery status events, and RFC 9457 error models. | Notifications must **not** invent private unapproved schemas or unpublished gRPC stubs. |
| **`tracelyt-query-engine`** | Queries telemetry metrics, logs, and traces for dashboards. | Notifications must **not** execute direct telemetry queries to construct message bodies. |
| **`tracelyt-ai-investigator`** | Emits approved investigation summaries and root-cause evidence for delivery. | Notifications must **not** execute LLMs, generate AI embeddings, or perform autonomous analysis. |
| **`tracelyt-deploy`** | Manages container packaging, Docker Compose stacks, Helm charts, and Kubernetes deployment topology. | Notifications must **not** duplicate platform-wide deployment manifests or infrastructure code. |

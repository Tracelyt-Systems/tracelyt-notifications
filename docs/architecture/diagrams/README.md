# Architecture Diagrams

This directory contains conceptual visual architecture diagrams for the `tracelyt-notifications` service, rendered using GitHub-compatible [Mermaid](https://mermaid.js.org/) syntax.

> **Status Notice**: All diagrams represent planned architectural designs. No actual notification delivery or infrastructure components are implemented during repository bootstrap.

---

## 1. High-Level Delivery Flow & System Boundaries

```mermaid
sequenceDiagram
    autonumber
    actor AlertService as tracelyt-alerting
    actor ControlPlane as tracelyt-control-plane
    participant Specs as tracelyt-specs (Contract)
    participant Intake as Intake & Validation Engine
    participant Routing as Routing & Preference Resolver
    participant Adapter as Provider Adapter Layer
    participant Provider as External Gateway (SES / Slack / Webhook)
    participant Store as Delivery State Store

    AlertService->>Intake: Dispatch Notification Intent (HTTP/Event)
    Note over AlertService,Intake: Request validated against Specs schema
    Intake->>Store: Persist Request (Status: ACCEPTED)
    Intake->>Routing: Resolve Tenant Preferences
    ControlPlane-->>Routing: Tenant Channel Config & Credentials
    Routing->>Adapter: Dispatch to Provider Adapter
    Adapter->>Store: Update Attempt State (Status: PROCESSING)
    Adapter->>Provider: Outbound Delivery Call (TLS / HMAC Signed)
    alt Successful Handshake / Delivery
        Provider-->>Adapter: 200 OK / Accepted Receipt
        Adapter->>Store: Update Attempt (Status: DELIVERED / PROVIDER_ACCEPTED)
    else Provider Temporary Error (e.g., 429 Rate Limited)
        Provider-->>Adapter: 429 Rate Limit Exceeded
        Adapter->>Store: Schedule Exponential Backoff Retry (Status: RETRY_SCHEDULED)
    else Permanent Rejection
        Provider-->>Adapter: 400 Bad Request / 404 Destination Unknown
        Adapter->>Store: Route to DLQ (Status: FAILED)
    end
```

---

## 2. Trust Boundaries and Isolation Architecture

```mermaid
graph TD
    subgraph UntrustedZone["External & Tenant Environments"]
        WebhookDest["Customer Webhook Endpoint"]
        ExternalAPI["Public Provider APIs (SendGrid, Slack, Discord)"]
        TenantUser["Tenant Admin (Control Plane UI)"]
    end

    subgraph PlatformTrustBoundary["Tracelyt Internal Platform (Private VPC)"]
        Alerts["tracelyt-alerting"]
        Control["tracelyt-control-plane"]
        Intake["Notification Intake API"]
        StateDB[(Delivery History DB)]
    end

    subgraph IsolatedEgressZone["Egress DMZ (SSRF Guarded)"]
        Worker["Notification Worker Engine"]
        SSRFProxy["Hardened Egress Proxy & DNS Validator"]
    end

    Alerts -- Authenticated mTLS --> Intake
    Control -- Authenticated mTLS --> Intake
    Intake --> StateDB
    Intake --> Worker
    Worker --> StateDB
    Worker -- Forward Request --> SSRFProxy
    SSRFProxy -- Block RFC 1918 / Cloud Metadata --> WebhookDest
    SSRFProxy -- Outbound TLS --> ExternalAPI
```

---

## 3. Provider Failover State Machine

```mermaid
stateDiagram-v2
    [*] --> PrimaryProvider: Select Configured Channel
    PrimaryProvider --> Success: Handshake Successful
    PrimaryProvider --> TransientFailure: 5xx / 429 Error
    PrimaryProvider --> PermanentFailure: 4xx Client Error

    TransientFailure --> RetryQueue: Retry Budget Available
    RetryQueue --> PrimaryProvider: Backoff Timer Expired

    TransientFailure --> FallbackEvaluation: Retries Exhausted or Circuit Open
    FallbackEvaluation --> SecondaryProvider: Secondary Configured & Policy Permits
    SecondaryProvider --> Success: Handshake Successful
    SecondaryProvider --> DeadLetterQueue: Secondary Exhausted

    PermanentFailure --> DeadLetterQueue: Mark Unrecoverable
    DeadLetterQueue --> [*]
    Success --> [*]
```

---

## 4. Related Documentation

- [Architecture Overview](../overview.md)
- [System Boundaries](../system-boundaries.md)
- [Delivery Reliability](../delivery-reliability.md)
- [Provider Model](../provider-model.md)
- [Threat Model](../../security/threat-model.md)

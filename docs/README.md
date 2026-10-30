# Tracelyt Notifications Documentation

Welcome to the documentation for **Tracelyt Notifications** (`tracelyt-notifications`), the multi-channel notification orchestration and delivery subsystem of the Tracelyt open-source observability platform.

---

## Documentation Navigation

### 1. Architecture & Design
- [Architecture Overview](architecture/overview.md) — Subsystem role, delivery boundary, and core principles.
- [System Boundaries](architecture/system-boundaries.md) — Ownership matrix across Tracelyt platform repositories.
- [Domain Model](architecture/domain-model.md) — Notification requests, attempts, delivery statuses, and recipient destinations.
- [Notification Lifecycle](architecture/notification-lifecycle.md) — 12-step conceptual delivery workflow.
- [Channel Strategy](architecture/channel-strategy.md) — Evaluation of Email, Slack, Teams, Discord, and Webhooks.
- [Provider Abstraction](architecture/provider-model.md) — Decoupled adapter model, capability negotiation, and failover.
- [Delivery Reliability](architecture/delivery-reliability.md) — At-least-once delivery, idempotency keys, backoff, and dead-lettering.
- [Messaging Strategy](architecture/messaging-strategy.md) — Evaluation of asynchronous queue paradigms (Kafka vs RabbitMQ vs DB).
- [Storage Strategy](architecture/storage-strategy.md) — Delivery history, attempt logs, and archival storage.
- [Rate Limiting & Abuse Prevention](architecture/rate-limiting.md) — Multi-tiered rate caps, burst handling, and storm mitigation.
- [Template Strategy](architecture/template-strategy.md) — Formatting, escaping, HTML injection defense, and localization.
- [Scalability](architecture/scalability.md) — Horizontal worker distribution, queue backpressure, and provider concurrency.
- [Technology Strategy](architecture/technology-strategy.md) — Language and framework evaluation matrix.
- [Language Boundaries](architecture/language-boundaries.md) — Multi-language adoption gates and monorepo boundaries.
- [Deployment Models](architecture/deployment-models.md) — Local, Docker, Kubernetes, and network egress considerations.
- [Architecture Diagrams](architecture/diagrams/README.md) — Visual Mermaid diagrams for delivery flow and trust boundaries.

### 2. Architecture Decision Records (ADRs)
- [ADR Index](decisions/README.md) — Decision log and governance.
- [ADR Template](decisions/adr-template.md) — Standardized format for proposing new decisions.
- [ADR-0001: Adopt Java 21 LTS + Spring Boot Foundation](decisions/0001-adopt-java21-spring-boot-foundation.md) — Initial bootstrap foundation decision.

### 3. Developer Experience
- [Local Setup Guide](development/local-setup.md) — Prerequisites, build commands, and offline validation.
- [Project Structure](development/project-structure.md) — Repository layout and Java package boundaries.
- [Coding Standards](development/coding-standards.md) — Checkstyle rules, line limits, and formatting hygiene.
- [Testing Strategy](development/testing-strategy.md) — Testing pyramid, unit tests, and non-blocking rules.
- [Dependency Management](development/dependency-management.md) — Selection discipline, BOM versioning, and CVE triage.
- [Contribution Workflow](development/contribution-workflow.md) — PR lifecycle and review standards.

### 4. Security & Privacy
- [Security Architecture Overview](security/README.md) — Security posture and design objectives.
- [Threat Model](security/threat-model.md) — STRIDE-aligned threat analysis covering 14 distinct notification risks.
- [Secret Management](security/secret-management.md) — Secure provider credentials, token rotation, and zero-leakage logs.
- [Webhook Security & SSRF Protection](security/webhook-security.md) — Private IP blacklisting, DNS rebinding guards, and TLS verification.
- [Tenant Isolation](security/tenant-isolation.md) — Cryptographic tenant verification and credential isolation.
- [Data Privacy & Minimization](security/data-privacy.md) — PII minimization, sensitive attribute masking, and audit logging.
- [Secure Development Lifecycle](security/secure-development.md) — Secure coding guidelines and vulnerability reporting.
- [Supply Chain Security](security/supply-chain.md) — Pinned GitHub Action SHAs and dependency review.

### 5. Operations & Production Readiness
- [Subsystem Observability](operations/observability.md) — Operational metrics, health probes, and recursive loop prevention.
- [Configuration Policy](operations/configuration.md) — Configuration principles, profiles, and startup validation.
- [Resource Limits & Quotas](operations/resource-limits.md) — Delivery timeouts, payload size caps, and provider budgets.
- [Capacity Planning](operations/capacity-planning.md) — Workload sizing dimensions and benchmarking protocols.
- [Disaster Recovery](operations/disaster-recovery.md) — High-availability topology, outbox buffering, and provider failover.
- [Deployment Readiness](operations/deployment-readiness.md) — Health probes, graceful shutdown, and container JVM tuning.

### 6. Standards & Governance
- [Contract Governance](standards/contract-governance.md) — Canonical authority of `tracelyt-specs` and protocol selection.
- [Compatibility Policy](standards/compatibility.md) — Semantic versioning and deprecation timelines.
- [Error Handling Standards](standards/error-handling.md) — RFC 9457 Problem Details and delivery error taxonomy.
- [Event Governance](standards/event-governance.md) — Standard event envelopes and idempotency keys.
- [Performance Testing](standards/performance-testing.md) — Benchmarking methodology and delivery latency percentiles.

### 7. Roadmap
- [Milestone Roadmap](roadmap/README.md) — Project milestones overview.
- [Architecture Evolution](roadmap/architecture-evolution.md) — 7-stage evolution from foundation to advanced multi-channel delivery.

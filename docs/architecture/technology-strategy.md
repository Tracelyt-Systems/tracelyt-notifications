# Technology Strategy & Decision Matrix

This document defines the evaluation criteria, trade-offs, and adoption status for programming languages, runtimes, and frameworks considered for `tracelyt-notifications`.

---

## 1. Technology Evaluation Matrix

| Technology | Proposed Role | Benefits | Alternatives Considered | Operational & Security Cost | Adoption Criteria | Decision Status |
|---|---|---|---|---|---|---|
| **Java 21 LTS** | Core notification orchestration, provider management, template rendering, and delivery state | Native Virtual Threads (Loom) for blocking I/O HTTP dispatches, unified tooling across Tracelyt services, mature enterprise ecosystem | Go, Rust, Node.js | Moderate JVM memory footprint; robust automated CVE scanning | Baseline foundation | **`initial`** |
| **Spring Boot 3.4.x** | Application configuration, dependency injection, and health probes | Standardized actuator health endpoints, robust configuration binding, production-ready testing harness | Quarkus, Micronaut | Low runtime overhead when stripped of unnecessary starters | Baseline foundation | **`initial`** |
| **Apache Maven** | Reproducible build automation and dependency governance | Predictable BOM resolution, automated Checkstyle integration, vendor-neutral wrapper (`mvnw`) | Gradle | Low; requires strict dependency discipline | Baseline foundation | **`initial`** |
| **Go (Golang)** | High-concurrency webhook egress workers | Sub-millisecond startup, minimal container memory footprint, native goroutines for high-throughput HTTP requests | Java Virtual Threads, Rust | Dual-language maintenance overhead, separate CI and linting toolchains | Worker thread saturation in Java | **`candidate` / `deferred`** |
| **Rust / C++** | Cryptographic payload signing and native network drivers | Zero-cost abstractions, memory safety (Rust) | Java Crypto API | High build complexity, steep learning curve | Profiling evidence demonstrating JVM crypto bottleneck | **`deferred`** |
| **Python** | Specialized integration tooling / template preprocessing | Broad scripting library | Java, Node.js | Runtime GIL constraints, heavy image footprint | Not justified for notification delivery | **`rejected`** |
| **Kafka / Message Broker** | High-throughput asynchronous delivery queues | Partitioned ordering, high event retention | Relational DB outbox, RabbitMQ | Broker cluster operations, partition management | Stage 5/6 scale requirements | **`deferred`** |
| **Redis / Distributed Cache** | Fast idempotency key lookups and rate limit counters | In-memory sub-millisecond atomic increments, native TTLs | Relational database unique indices | Additional stateful service to manage | Multi-node worker scaling | **`deferred`** |

---

## 2. Decision Status Definitions
- **`initial`:** Selected and actively implemented in the current repository scaffold.
- **`candidate`:** Approved architectural candidate for future stages, requiring a formal ADR before implementation.
- **`deferred`:** Documented as a future possibility; barred from current implementation.
- **`rejected`:** Explicitly evaluated and rejected for this subsystem.

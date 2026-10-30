# ADR-0001: Adopt Java 21 LTS and Spring Boot Baseline Foundation

- **Status**: Accepted
- **Date**: 2026-10-30
- **Authors**: Tracelyt Maintainers
- **Deciders**: Maintainer Team

---

## 1. Context and Problem Statement

`tracelyt-notifications` must provide a reliable, maintainable foundation for multi-channel notification intake, state persistence, provider integration, and delivery orchestration.

We need an initial programming language, build toolchain, and application framework that balances developer ergonomics, long-term stability, robust networking libraries, structured concurrency, and operational alignment with the broader Tracelyt platform (such as `tracelyt-control-plane` and `tracelyt-ingestion`).

---

## 2. Decision Drivers

- **Platform Ecosystem Cohesion**: Alignment with established Tracelyt Java platform standards and shared coding conventions.
- **Enterprise Integration & Networking**: Rich, mature ecosystem of HTTP/2, TLS, and enterprise messaging clients.
- **Concurrency Model**: High-concurrency I/O performance via modern virtual threads (Java 21 Project Loom) without complex reactive programming models.
- **Reproducible Build Infrastructure**: Maven Wrapper ensuring hermetic builds across diverse developer operating systems (Linux, macOS, Windows) and CI/CD environments.
- **Security & Dependency Hygiene**: First-class tooling for vulnerability scanning, static analysis (Checkstyle), and CVE mitigation.

---

## 3. Considered Options

1. **Java 21 LTS + Spring Boot 3.4.x + Maven**: Mature enterprise stack with virtual thread support, rich ecosystem, and direct alignment with other Tracelyt control services.
2. **Go (Golang)**: Lightweight binary execution, rapid cold-start times, but requires building custom application lifecycle management, dependency injection, and state machine abstractions from scratch.
3. **Rust**: Exceptional memory safety and predictable resource consumption, but high cognitive overhead and slower velocity during rapid initial architectural iteration.
4. **Node.js / TypeScript**: Strong JSON handling and web API ecosystem, but weak multithreading capabilities and higher supply-chain vulnerability attack surface.

---

## 4. Decision Outcome

Chosen option: **Java 21 LTS with Spring Boot 3.4.x and Maven Wrapper**.

### Positive Consequences
- Immediate compatibility with Java 21 virtual threads (`spring.threads.virtual.enabled=true`), allowing thousands of concurrent outbound provider HTTP connections with standard imperative programming models.
- Minimal scaffolding footprint: only core starters (`spring-boot-starter`, `spring-boot-starter-actuator`, `spring-boot-starter-test`) are included. Zero unnecessary databases or queue drivers.
- Reproducible, zero-installation builds using `./mvnw` (Linux/macOS) and `mvnw.cmd` (Windows).
- Automated static analysis enforced through Checkstyle 10.21.4.

### Negative Consequences / Trade-offs
- JVM base memory consumption is higher than a compiled Go or Rust binary (typically 150–250MB resident set size under moderate load).
- Slightly longer container startup latency compared to Go (mitigated by Spring Boot 3.4 optimizations and JVM container sizing flags).

---

## 5. Security & Compliance Implications

- Enforces TLS 1.3 by default on all outbound provider connections.
- Clean integration with SLF4J/Logback masking patterns to prevent credential leaks.
- Pinned dependency versions via Spring Boot BOM and automated CVE scanning via Dependabot.

---

## 6. Operational Impact

- Standardized `/actuator/health` and `/actuator/info` endpoints for Kubernetes readiness and liveness probes.
- Graceful shutdown enabled by default (`server.shutdown=graceful`) to prevent abrupt connection termination during rolling deployments.

---

## 7. Revisit Conditions

This decision will be re-evaluated if:
- Profiling of high-density edge webhook dispatch demonstrates that JVM memory limits prevent cost-effective scaling on resource-constrained nodes.
- Latency benchmarks demand sub-millisecond dispatch times requiring a specialized native runtime.

# Language Boundaries and Multi-Language Strategy

This document establishes the architectural boundaries, evaluation gates, and governance policies for programming languages within the `tracelyt-notifications` subsystem.

---

## 1. Single-Runtime Principle

For Phase 1 and the initial application baseline, `tracelyt-notifications` adheres to a **single-runtime principle**:
- **Adopted Runtime**: Java 21 (LTS) on the HotSpot JVM with Spring Boot 3.4.x.
- **Rationale**: Keeps operational complexity minimal, simplifies CI/CD pipelines, establishes uniform code review standards, and leverages the mature Java ecosystem for enterprise integration, robust network clients, and structured concurrency.

No secondary runtime (e.g., Go, Rust, Python, Node.js) may be added to the build tree, container images, or deployment manifests without completing the formal Multi-Language Adoption Process documented below.

---

## 2. Language Responsibility Matrix

| Language | Operational Role | Decision Status | Adoption Condition / Pre-requisite |
| :--- | :--- | :--- | :--- |
| **Java 21 LTS** | Primary orchestrator, delivery state machine, provider adapters, REST/gRPC intake APIs, schema validation. | **Initial** | Established in baseline repository. |
| **Go** | Candidate for standalone, ultra-low-latency provider egress workers or lightweight edge webhook dispatchers. | **Deferred** | Workload benchmarks must prove JVM memory overhead or cold-start latency is a critical blocker. |
| **Rust** | Candidate for high-throughput cryptographic verification, secure webhook sandbox execution, or native SSRF-safe HTTP client engine. | **Deferred** | Memory safety or raw cryptographic throughput demands exceed JVM capability. |
| **Python** | Prototyping or AI investigation summarization bindings. | **Rejected** | Tracelyt Notification subsystem does not perform AI reasoning; AI features belong in `tracelyt-ai-investigator`. |
| **C / C++** | Low-level system integration. | **Rejected** | No native kernel or hardware acceleration requirements justify the operational and security liability. |

---

## 3. Multi-Language Adoption Process

Before any additional language or runtime is introduced:

1. **Benchmark Justification**: Maintainers must submit reproducible performance or resource profiling data demonstrating that Java 21 (including Virtual Threads / Project Loom) cannot satisfy the SLA.
2. **Architecture Decision Record (ADR)**: A formal ADR must be submitted detailing:
   - Specific component or service boundary to be implemented in the candidate language.
   - Inter-process communication protocol (e.g., gRPC over HTTP/2, IPC, or asynchronous event bus).
   - Toolchain maintenance cost (compilers, linters, dependency scanners, CI agents).
   - Security scanning capabilities (e.g., Dependabot, SAST coverage).
3. **Operational Impact Assessment**: Evaluation of deployment artifacts, container base image sizes, debugging ergonomics, and maintainer cognitive load.
4. **Approval**: Approval by at least two Tracelyt maintainers.

---

## 4. Inter-Service Communication Boundaries

If a secondary language is adopted in the future (such as a Go-based webhook egress worker):
- **No Shared Memory**: Processes must be isolated; no direct shared memory or FFI across service boundaries.
- **Contract-First Communication**: All inter-service message schemas must be defined in `tracelyt-specs` using Protocol Buffers or JSON Schema.
- **Independent Packaging**: The secondary language component must produce an independent deployable artifact with its own CI validation, Docker container, and health probe definitions.

---

## 5. Related Documentation

- [Technology Strategy](technology-strategy.md)
- [System Boundaries](system-boundaries.md)
- [Contract Governance](../standards/contract-governance.md)

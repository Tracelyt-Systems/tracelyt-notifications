# Architecture Decision Records (ADRs)

This directory documents key architectural decisions made for the `tracelyt-notifications` subsystem. We use the Architecture Decision Record (ADR) process to capture the context, rationale, trade-offs, and consequences of significant technical choices.

---

## ADR Process

1. **Format**: Follow the template defined in [adr-template.md](adr-template.md).
2. **Numbering**: Use four-digit sequential numbering (e.g., `0001-...md`).
3. **Status Workflow**:
   - `Proposed` — Under active review by maintainers.
   - `Accepted` — Approved and adopted as official architecture.
   - `Rejected` — Evaluated and declined.
   - `Superseded` — Replaced by a subsequent ADR (link the successor).
   - `Deprecated` — No longer applicable.

---

## Decision Log

| ID | Title | Status | Date | Primary Driver |
| :--- | :--- | :--- | :--- | :--- |
| [ADR-0001](0001-adopt-java21-spring-boot-foundation.md) | Adopt Java 21 LTS and Spring Boot Baseline Foundation | **Accepted** | 2026-10-30 | Minimal operational complexity, enterprise integration, structured concurrency. |

---

## Related Documentation

- [Technology Strategy](../architecture/technology-strategy.md)
- [Language Boundaries](../architecture/language-boundaries.md)
- [Governance Model](../../GOVERNANCE.md)

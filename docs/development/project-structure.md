# Repository and Project Structure

This document describes the organization, folder layout, and Java package conventions for `tracelyt-notifications`.

---

## 1. Top-Level Directory Layout

```text
tracelyt-notifications/
├── .github/                     # GitHub Actions workflows, templates, CODEOWNERS, Dependabot
│   ├── ISSUE_TEMPLATE/          # Bug report, feature request templates
│   └── workflows/               # CI, documentation, dependency review workflows
├── assets/                      # Repository logos, static branding assets
├── contracts/                   # Shared schema governance and references to tracelyt-specs
├── docs/                        # Comprehensive technical documentation
│   ├── architecture/            # Architectural strategies, lifecycle, and Mermaid diagrams
│   ├── decisions/               # Architecture Decision Records (ADRs)
│   ├── development/             # Developer guides, coding standards, testing policies
│   ├── operations/              # Production readiness, observability, capacity planning
│   ├── roadmap/                 # Subsystem milestones and evolution plan
│   ├── security/                # Threat model, webhook SSRF protection, secret management
│   └── standards/               # API, error handling, compatibility, and event governance
├── src/                         # Production application source code and tests
│   ├── main/java/               # Java 21 production code root
│   ├── main/resources/          # Application configuration (application.yml)
│   ├── test/java/               # Automated unit tests
│   └── test/resources/          # Test configuration (application-test.yml)
├── tools/                       # Developer utility scripts (validate_docs.py)
├── .checkstyle.xml              # Checkstyle 10.21.4 rules definition
├── .editorconfig                # Universal indentation and whitespace formatting rules
├── .gitignore                   # Ignored files (build outputs, IDE caches, secrets)
├── Makefile                     # Standard developer commands (validate, test, build)
├── pom.xml                      # Maven build manifest (Java 21, Spring Boot 3.4.3)
└── README.md                    # Primary repository overview and navigation
```

---

## 2. Java Package Hierarchy (Root: `io.tracelyt.notifications`)

The Java source tree is organized into cohesive modules that enforce strict architectural boundaries:

```text
io.tracelyt.notifications/
├── NotificationsApplication.java  # Spring Boot application bootstrap entrypoint
│
├── intake/                        # [Planned] Ingress controllers, request validation
│   ├── api/                       # REST / gRPC intake endpoints
│   └── validation/                # Request validation logic
│
├── domain/                        # [Planned] Pure domain entities and value objects
│   ├── model/                     # NotificationRequest, Attempt, DeliveryStatus
│   └── policy/                    # Routing, retry, and rate-limiting rules
│
├── providers/                     # [Planned] Provider abstraction layer (SPI)
│   ├── api/                       # NotificationProvider, ProviderCapability interfaces
│   ├── email/                     # Transactional email adapters (SES, Resend)
│   ├── chat/                      # Chat adapters (Slack, Teams, Discord)
│   └── webhook/                   # SSRF-guarded HTTP webhook dispatcher
│
└── persistence/                   # [Planned] Storage abstraction and state transitions
    ├── entity/                    # Database entities
    └── repository/                # Storage interfaces
```

> **Note**: For Phase 1, only the root package and `NotificationsApplication.java` are instantiated. Subpackages will be introduced incrementally alongside approved ADRs and schema contracts.

---

## 3. Configuration Conventions

- **Production Configuration**: `src/main/resources/application.yml` defines baseline production properties (server port `8085`, graceful shutdown, Actuator endpoints).
- **Test Configuration**: `src/test/resources/application-test.yml` isolates testing environments from external network and storage requirements.
- **Environment Overrides**: All operational properties are bindable via standard uppercase environment variables (e.g., `SERVER_PORT=8085`).

---

## 4. Related Documentation

- [Local Setup Guide](local-setup.md)
- [Coding Standards](coding-standards.md)
- [Architecture Overview](../architecture/overview.md)

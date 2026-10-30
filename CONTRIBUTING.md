# Contributing to Tracelyt Notifications

Thank you for your interest in contributing to **Tracelyt Notifications**! This document provides guidelines for contributing to this repository.

---

## 1. Ground Rules & Code of Conduct

All contributors must adhere to our [Code of Conduct](CODE_OF_CONDUCT.md). Please treat all participants with respect and professional empathy.

---

## 2. Scope Boundaries

This repository is currently in **Stage 1 (Foundation)**. Please keep in mind:
- **Architecture and Setup Only:** We do not accept PRs introducing working email dispatchers, Slack/Teams SDK integrations, production webhook clients, database drivers, Kafka/Redis queues, or mock delivery endpoints at this stage.
- **Contract Authority:** Shared API models and event schemas must be reviewed and approved through [`tracelyt-specs`](https://github.com/Tracelyt-Systems/tracelyt-specs).
- **Architecture Decision Records:** Significant architectural or technology changes must be proposed via an ADR in `docs/decisions/` before opening implementation PRs.

---

## 3. Local Development & Quality Gates

Before opening a pull request:
1. Ensure Java 21 LTS is installed.
2. Run style and test verification:
   ```bash
   ./mvnw -B -ntp clean test checkstyle:check
   ```
   *(Windows: `mvnw.cmd -B -ntp clean test checkstyle:check`)*
3. Verify documentation links and secrets:
   ```bash
   python tools/validate_docs.py
   ```
4. PRs must have **0 Checkstyle violations** and 100% passing tests.

---

## 4. Pull Request Process

1. Fork the repository and create a branch named `feat/<name>`, `fix/<name>`, or `docs/<name>`.
2. Follow the [Pull Request Template](.github/PULL_REQUEST_TEMPLATE.md).
3. Ensure commits are descriptive and follow conventional commit syntax (`feat:`, `fix:`, `docs:`, `refactor:`).
4. Review approval from at least one repository maintainer listed in [MAINTAINERS.md](MAINTAINERS.md) is required before merging.

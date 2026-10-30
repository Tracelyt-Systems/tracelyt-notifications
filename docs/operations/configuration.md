# Configuration Policy and Environment Properties

This document describes the configuration principles, configuration hierarchy, and environment variables used by `tracelyt-notifications`.

---

## 1. Configuration Principles

1. **Explicit Defaults**: Every configuration property must have a safe, predictable default documented in `application.yml`.
2. **Environment Override**: All properties must be bindable via standard environment variables following Twelve-Factor App principles.
3. **Fail-Fast Startup**: If critical configuration properties (such as database credentials or key store paths) are invalid, the application must abort startup immediately with a descriptive error message.
4. **No Secrets in Config Files**: Secrets must be injected via secure environment variables or vault mounts, never checked into configuration files.

---

## 2. Configuration Hierarchy

Spring Boot resolves configuration in the following order (highest precedence first):
1. Command-line arguments (`--server.port=8085`).
2. Environment variables (`SERVER_PORT=8085`).
3. External profile-specific configuration (`file:./config/application-prod.yml`).
4. Packaged configuration (`src/main/resources/application.yml`).

---

## 3. Core Environment Variables (Planned Baseline)

| Environment Variable | Property Key | Default Value | Description |
| :--- | :--- | :--- | :--- |
| `SERVER_PORT` | `server.port` | `8085` | HTTP port for REST intake and Actuator probes. |
| `MANAGEMENT_SERVER_PORT` | `management.server.port` | `${server.port}` | Dedicated port for internal health/metrics if split. |
| `SPRING_PROFILES_ACTIVE` | `spring.profiles.active` | `default` | Active Spring profile (`dev`, `prod`, `test`). |
| `TRACELYT_NOTIF_MAX_ATTEMPTS` | `tracelyt.notifications.retry.max-attempts` | `5` | Maximum retry attempts before routing to DLQ. |
| `TRACELYT_NOTIF_BACKOFF_INIT_MS`| `tracelyt.notifications.retry.initial-backoff-ms` | `1000` | Initial backoff duration in milliseconds. |
| `TRACELYT_NOTIF_SSRF_ENFORCE` | `tracelyt.notifications.security.ssrf-protection-enabled` | `true` | Enforces private IP blocking for webhooks. |

---

## 4. Related Documentation

- [Observability](observability.md)
- [Resource Limits](resource-limits.md)
- [Deployment Readiness](deployment-readiness.md)

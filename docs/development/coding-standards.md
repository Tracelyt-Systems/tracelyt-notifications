# Coding Standards and Code Hygiene

This document defines the code quality standards, formatting rules, and static analysis requirements for `tracelyt-notifications`.

---

## 1. Java Coding Standards

`tracelyt-notifications` enforces clean, idiomatic Java 21 conventions verified by Checkstyle 10.21.4.

### 1.1 Formatting Rules
- **Indentation**: 4 spaces per indent level. No tab characters.
- **Line Length**: Maximum 120 characters per line.
- **Encoding**: UTF-8 without byte-order marks (BOM).
- **Line Endings**: Unix-style `LF` (`\n`). Enforced via `.gitattributes`.
- **Braces**: K&R style (opening brace on the same line, closing brace on a new line).

### 1.2 Naming Conventions
- **Packages**: All lowercase alphanumeric characters without underscores (`io.tracelyt.notifications.intake`).
- **Classes & Interfaces**: UpperCamelCase (`NotificationRequest`, `ProviderAdapter`).
- **Methods & Variables**: lowerCamelCase (`deliverNotification`, `attemptCount`).
- **Constants**: UPPER_SNAKE_CASE (`DEFAULT_TIMEOUT_MILLIS`).
- **Type Parameters**: Single uppercase letter (`T`, `R`) or descriptive uppercase identifier (`ENTITY`).

### 1.3 Language Features & Modern Java
- **Records**: Use `record` for immutable data carriers, request/response models, and value objects.
- **Pattern Matching**: Utilize modern `switch` expressions and pattern matching for `instanceof`.
- **Virtual Threads**: Design blocking I/O calls to be virtual-thread-friendly (avoid pinning threads with synchronized blocks on long-running operations; prefer `ReentrantLock`).
- **Null Safety**: Avoid returning `null`; use `Optional<T>` for query results that may be absent. Annotate parameters with `@NonNull` where appropriate.

---

## 2. Checkstyle Enforcement

All Java source files must pass Checkstyle rules defined in `.checkstyle.xml`.

Run Checkstyle verification:
```bash
# Linux / macOS
./mvnw -B -ntp checkstyle:check

# Windows
mvnw.cmd -B -ntp checkstyle:check
```

Checkstyle verifies:
- Unused imports and wildcards (e.g., `import java.util.*;` is forbidden).
- Modifier order according to the Java Language Specification.
- Correct package and class naming.
- Absence of empty catch blocks.
- Proper equals and hashCode contracts.

---

## 3. Logging Standards

- **SLF4J**: Always use SLF4J (`org.slf4j.Logger`) via `LoggerFactory.getLogger(...)` or `@Slf4j`.
- **Structured Logging**: Use parameterized logging instead of string concatenation:
  ```java
  // Correct
  logger.info("Notification request accepted: id={}, tenant={}", requestId, tenantId);

  // Forbidden
  logger.info("Notification request accepted: " + requestId);
  ```
- **Zero Sensitive Data**: Never log passwords, API keys, webhook signing secrets, authorization headers, or full unmasked recipient emails.

---

## 4. Markdown and YAML Standards

- Markdown files should follow CommonMark guidelines.
- YAML files must adhere to 2-space indentation and be verified via `.yamllint`.
- All documentation links must be relative and point to existing files.

---

## 5. Related Documentation

- [Local Setup Guide](local-setup.md)
- [Testing Strategy](testing-strategy.md)
- [Secure Development](../security/secure-development.md)

# Dependency Management and Supply Chain Hygiene

This document outlines the dependency governance policies, version management rules, and vulnerability response workflows for `tracelyt-notifications`.

---

## 1. Minimal Dependency Principle

Every dependency added to `pom.xml` introduces an ongoing maintenance cost, potential attack surface, and upgrade burden.

### 1.1 Criteria for Adding a Dependency
Before proposing a new dependency in a Pull Request, contributors must evaluate:
1. **Critical Need**: Can this functionality be achieved with standard Java 21 APIs (`java.net.http.HttpClient`, `java.util.concurrent`) or existing Spring Boot core modules?
2. **Maintenance Status**: Is the library actively maintained by a reputable organization with a history of timely security patches?
3. **License Compatibility**: Is the license compatible with Apache 2.0 (e.g., Apache 2.0, MIT, BSD-3-Clause)? GPL and AGPL dependencies are strictly forbidden.
4. **Transitive Bloat**: Does the dependency pull in excessive transitive libraries?

### 1.2 Prohibited Dependencies in Phase 1
- Direct vendor provider SDKs (e.g., SendGrid Java SDK, Slack Bolt, Teams SDK). Outbound HTTP integrations will use standard HTTP clients to prevent library lock-in.
- Unnecessary database or cache drivers (JPA, Hibernate, Redis, Kafka) before storage architecture is formally approved.
- AI or LLM framework dependencies.

---

## 2. Dependency Management in Maven

`tracelyt-notifications` uses the Spring Boot Dependencies Bill of Materials (BOM) to curate dependency versions:

```xml
<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.4.3</version>
    <relativePath/>
</parent>
```

- **No Explicit Versions for Managed Dependencies**: Do not hardcode `<version>` tags for dependencies managed by the Spring Boot parent POM.
- **Explicit Version Properties**: Third-party plugins or standalone libraries must define their version in the `<properties>` block of `pom.xml`.

---

## 3. Automated Vulnerability Scanning

- **Dependabot**: `.github/dependabot.yml` is configured to scan Maven and GitHub Actions dependencies weekly.
- **Dependency Review**: `.github/workflows/dependency-review.yml` inspects newly introduced dependencies on Pull Requests for known CVEs.
- **Zero Critical CVE Policy**: Any dependency identified with a Critical or High severity CVE must be upgraded or removed immediately.

---

## 4. Related Documentation

- [Local Setup Guide](local-setup.md)
- [Supply Chain Security](../security/supply-chain.md)
- [Security Policy](../../SECURITY.md)

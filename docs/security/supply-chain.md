# Supply Chain Security Architecture

This document defines the controls, tooling, and verification procedures protecting the software supply chain of `tracelyt-notifications`.

---

## 1. Threat Vectors in the Supply Chain

Modern open-source services face severe supply-chain risks:
- Malicious upstream dependency updates (typosquatting, compromised maintainer credentials).
- Compromised GitHub Actions in CI workflows.
- Compromised build artifacts and untrusted container base images.

---

## 2. Supply Chain Defensive Measures

### 2.1 Full Commit SHA Pinning for GitHub Actions
All GitHub Actions in `.github/workflows/` must be pinned to full 40-character commit SHAs rather than mutable Git tags (`@v4`):

```yaml
# Correct: Immutable commit SHA with human-readable version comment
- name: Set up JDK 21
  uses: actions/setup-java@3a4f6e1af504cf6a31855fa899c6aa5355ba6c12 # v4.7.0

# Forbidden: Mutable branch or tag reference
- name: Set up JDK 21
  uses: actions/setup-java@v4
```

This prevents malicious tag mutability attacks if an upstream action repository is compromised.

### 2.2 Maven Dependency Verification
- **Automated Scanning**: Dependabot checks dependencies weekly against known CVE databases.
- **Minimal Dependencies**: The build configuration relies on Spring Boot BOM to eliminate rogue third-party transients.
- **Reproducible Builds**: Maven Wrapper checksums are validated to ensure hermetic build tooling.

### 2.3 Least Privilege CI Permissions
GitHub Actions workflows must explicitly declare minimal permissions:
```yaml
permissions:
  contents: read
```
Workflows never request broad write permissions unless executing an authorized release pipeline.

---

## 3. Related Documentation

- [Security Overview](README.md)
- [Dependency Management](../development/dependency-management.md)
- [CI Workflow](../../.github/workflows/ci.yml)

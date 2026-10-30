# Secret Management and Credential Handling

This document establishes the security architecture and operational guidelines for managing provider credentials, API keys, and webhook signing secrets in `tracelyt-notifications`.

---

## 1. Principles of Credential Handling

1. **Zero Plaintext Secrets in Code or VCS**: No API keys, passwords, webhook tokens, or certificates may ever be committed to Git.
2. **Secret References Over Raw Values**: Internal notification requests must never pass raw credentials in payload bodies. Requests should reference a `credentialId` or `providerId` owned by `tracelyt-control-plane`.
3. **Envelope Encryption at Rest**: Provider credentials stored in persistent databases must be encrypted using AES-256-GCM with keys managed by external Key Management Systems (AWS KMS, HashiCorp Vault, Azure Key Vault).
4. **Zero-Leakage Logging**: Credentials and authorization tokens must be proactively masked across all log appenders and metric labels.
5. **Least Privilege**: Provider API tokens provisioned by tenants should possess only the minimum scopes necessary to dispatch notifications (e.g., SendGrid `mail.send`, Slack `chat:write:bot`).

---

## 2. In-Memory Handling and Sanitization

When processing outbound delivery requests:
- **Ephemeral Exposure**: Secrets should be resolved immediately prior to the outbound network call and discarded from short-lived scope.
- **Log Sanitizer Interceptors**: HTTP client logging interceptors must scrub:
  - Header: `Authorization`
  - Header: `X-Api-Key`
  - Header: `X-Webhook-Secret`
  - JSON fields matching regex: `(?i)(password|secret|token|apiKey|key)`

---

## 3. Secret Rotation Strategy

- **Graceful Rotation**: The system architecture must accommodate dual-active credentials during rotation windows (e.g., verifying webhook signatures against both current and previous signing keys for a 24-hour transition period).
- **Automated Invalidation**: If an outbound provider call returns HTTP 401 Unauthorized or HTTP 403 Forbidden due to an invalid token, the provider configuration must be flagged as `SUSPENDED_INVALID_CREDENTIALS` to prevent continuous retry storms that alert external security teams.

---

## 4. Local Development Practices

- **No Shared Test Secrets**: Local development must rely on local mock servers (e.g., WireMock or MailHog) or environment variables populated via `.env` files explicitly excluded by `.gitignore`.
- **Pre-commit Hooks**: Enforce secret scanning using tools like `detect-secrets` or Gitleaks prior to local commits.

---

## 5. Related Documentation

- [Security Overview](README.md)
- [Threat Model](threat-model.md)
- [Tenant Isolation](tenant-isolation.md)

# Security Architecture Overview

This directory defines the security posture, threat model, mitigation strategies, and operational controls for `tracelyt-notifications`.

---

## 1. Security Mission

Because the notification delivery subsystem sits at the boundary between internal platform events and external communication gateways (transactional email, chat platforms, and tenant-configured webhooks), it represents a high-value security interface.

Our core security objectives are:
1. **Zero Secret Leakage**: API tokens, webhook secrets, and private keys must never be logged, persisted in plaintext, or exposed in error responses.
2. **Robust SSRF Defense**: Tenant-configured webhook destinations must never be permitted to target internal networks, cloud metadata services, or loopback interfaces.
3. **Strict Multi-Tenant Isolation**: A tenant must never receive or access notifications, templates, or delivery history belonging to another tenant.
4. **Supply Chain Integrity**: Dependencies, build tools, and CI actions must be cryptographically pinned and continuously audited.

---

## 2. Security Documentation Index

- [Threat Model](threat-model.md) — Comprehensive STRIDE-aligned threat analysis covering 14 distinct notification risks.
- [Secret Management](secret-management.md) — Provider token handling, encryption at rest, rotation policies, and log masking.
- [Webhook Security & SSRF Protection](webhook-security.md) — Deep dive into SSRF mitigation, IP blacklisting, DNS rebinding guards, and HMAC signing.
- [Tenant Isolation](tenant-isolation.md) — Multi-tenant data segregation, tenant context propagation, and recipient validation.
- [Data Privacy & Minimization](data-privacy.md) — PII handling, message retention schedules, and GDPR/privacy considerations.
- [Secure Development Lifecycle](secure-development.md) — Security practices during coding, static analysis, and vulnerability disclosure.
- [Supply Chain Security](supply-chain.md) — Dependency scanning, Action commit SHA pinning, and build reproducibility.

---

## 3. Reporting a Vulnerability

If you discover a security vulnerability in `tracelyt-notifications`, please follow our responsible disclosure process detailed in [SECURITY.md](../../SECURITY.md). **Do not report security issues via public GitHub issues.**

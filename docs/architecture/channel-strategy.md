# Multi-Channel Delivery Strategy

This document evaluates the delivery channels, provider integration mechanisms, payload formatting, and transport-specific trade-offs supported by `tracelyt-notifications`.

---

## 1. Channel Comparison Matrix

| Channel | Intended Workload | Primary Transport | Candidate Providers | Security & Compliance Considerations |
|---|---|---|---|---|
| **Email** | Detailed incident reports, daily digests, audit notifications | SMTP / HTTPS REST API | AWS SES, Resend, SendGrid, Postmark | SPF/DKIM/DMARC alignment, HTML injection protection, bounce/complaint handling. |
| **Slack** | Team incident channels, on-call alert rooms, interactive triage | HTTPS (Incoming Webhook / Web API) | Slack Web API | OAuth bot token storage, workspace-scoped rate limits (1 req/sec per webhook). |
| **MS Teams** | Enterprise operations teams, corporate incident triage | HTTPS (Incoming Webhooks / Graph API) | Microsoft Teams Graph API | Office 365 tenant boundary, adaptive card formatting constraints. |
| **Discord** | Community open-source alerts, developer triage | HTTPS (Discord Webhook API) | Discord API | Webhook token rotation, payload rate limits (30 req/min). |
| **Generic Webhooks** | Custom customer automation, PagerDuty, OpsGenie, SIEMs | Outbound HTTPS POST | Custom customer endpoints | **High Risk:** Requires SSRF protection, IP blacklisting, HMAC-SHA256 request signing. |

---

## 2. Channel Deep-Dives

### 2.1 Email
- **Dual-MIME Payloads:** Every email must be rendered with both `text/plain` and sanitized `text/html` bodies.
- **Provider Feedback:** Integrates with provider webhook events to capture hard bounces and spam complaints, automatically flagging invalid email addresses.

### 2.2 Slack
- **Block Kit Formatting:** Formats alert notifications into structured Slack Block Kit layouts, displaying severity colors, metric charts, and direct runbook links.
- **Workspace Credential Scoping:** Bot tokens are encrypted and strictly scoped to tenant workspace IDs.

### 2.3 Microsoft Teams
- **Adaptive Cards:** Uses Microsoft Adaptive Cards for clear rendering across desktop and mobile Teams clients.
- **Modern Integration:** Prioritizes Microsoft Graph and Power Automate webhook workflows over legacy deprecated Office 365 connectors.

### 2.4 Generic Webhooks (Security Critical)
Because generic webhooks make outbound HTTP requests to user-supplied URLs, they represent a significant attack surface:
- **Mandatory HTTPS:** Plain HTTP endpoints are rejected by default.
- **HMAC Signature Header:** All outgoing webhook requests include an `X-Tracelyt-Signature` header computed as `HMAC-SHA256(payload, secret)`, enabling recipient validation.
- **SSRF Defense:** Mandatory private IP blocking and DNS rebinding protections (see [Webhook Security](../security/webhook-security.md)).

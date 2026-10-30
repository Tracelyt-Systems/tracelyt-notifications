# Template & Message Formatting Strategy

This document outlines the templating architecture, multi-channel rendering engines, HTML injection defenses, and localization boundaries for `tracelyt-notifications`.

> **Status Notice:** This document establishes design specifications for template compilation. No templating engines (Thymeleaf, FreeMarker, Handlebars) or frontend editors are implemented in this repository foundation.

---

## 1. Multi-Channel Rendering Targets

Each notification channel requires distinct layout formats derived from the same canonical incident model:

| Channel | Format Target | Primary Constraints |
|---|---|---|
| **Email** | Responsive HTML & Plain Text | Inline CSS styles, table layouts for cross-client Outlook/Gmail compatibility, strict HTML sanitization. |
| **Slack** | Block Kit JSON | Maximum 50 blocks per message, 3,000 characters per text block. |
| **MS Teams** | Adaptive Cards JSON | Version 1.5 schema, action buttons bounded by Teams client width. |
| **Discord** | Embed JSON | Maximum 6,000 total characters per embed structure. |
| **Webhooks** | Normalized JSON Payload | Validated against `tracelyt-specs` OpenAPI schemas. |

---

## 2. Security: HTML & Payload Injection Defense

Because notification templates interpolate user-supplied alert titles, error messages, and telemetry labels, **template engines represent a primary attack vector for Cross-Site Scripting (XSS) and HTML injection in emails**:

1. **Strict Context-Aware Auto-Escaping:** All user-supplied variables (e.g., `{{ incident.summary }}`) must be aggressively HTML-escaped (`<`, `>`, `&`, `"`, `'`) before template compilation.
2. **Prohibited Raw HTML Tags:** User input must never be rendered as raw HTML.
3. **No Dynamic Template Code Execution:** Template engines that allow arbitrary Java code execution (e.g., un-sandboxed Groovy or SpEL) are **strictly prohibited**. Lightweight, logic-less templates (e.g., Handlebars or Mustache) are mandated.
4. **Link Sanitization:** Links embedded in templates (e.g., `{{ runbook_url }}`) must be validated against `http://` and `https://` protocols, rejecting `javascript:` or `data:` URIs.

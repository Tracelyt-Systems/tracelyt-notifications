# Delivery Reliability & Failure Semantics

This document details the reliability guarantees, at-least-once delivery semantics, idempotency models, exponential backoff policies, and dead-letter quarantine rules for `tracelyt-notifications`.

---

## 1. The Reality of At-Least-Once Delivery

In distributed notification systems, **guaranteeing universal "exactly-once" delivery across external third-party systems is mathematically impossible**:
- If a delivery worker sends an HTTP request to Slack, Slack accepts the message and posts it to a channel, but a network blip severs the connection before Slack's HTTP 200 response reaches the worker, the worker cannot know whether the message was delivered.
- If the worker retries, the message may be delivered twice (**at-least-once**).
- If the worker does not retry, the message may be lost (**at-most-once**).

**Tracelyt Standard:** We adopt an **at-least-once delivery model paired with idempotent consumer semantics**:
- We prioritize message durability over accidental drops: critical incident notifications must be delivered even if a rare network disruption causes duplicate delivery.
- Wherever external providers support idempotency tokens (e.g., Stripe, modern email APIs), we pass deterministic idempotency keys to suppress duplicates upstream.

---

## 2. Idempotency Keys & Deduplication

All notification requests require an `idempotency_key` derived deterministically from the source incident:

$$\text{IdempotencyKey} = \text{Hash}(\text{tenant\_id}, \text{source\_event\_id}, \text{destination\_channel})$$

- **Idempotency Window:** Idempotency keys are cached in fast-lookup storage for a sliding TTL window (default: 24 hours).
- **Duplicate Handling:** If a notification request arrives with a key currently marked `PROCESSING` or `DELIVERED`, the request is accepted as an idempotent no-op and returns the recorded status without re-dispatching.

---

## 3. Exponential Backoff with Full Jitter

When transient failures occur (e.g., HTTP 429 or network timeouts), retries are scheduled using truncated exponential backoff with full jitter:

$$t_{\text{sleep}} = \text{random}(0, \min(t_{\text{max}}, t_{\text{base}} \times 2^{\text{attempt}}))$$

- **Base Interval ($t_{\text{base}}$):** 2 seconds.
- **Max Interval ($t_{\text{max}}$):** 300 seconds (5 minutes).
- **Maximum Attempts:** 5 attempts before quarantine.
- **Provider `Retry-After` Precedence:** If the external provider returns an explicit `Retry-After` HTTP header, the backoff scheduler respects the provider's requested delay.

---

## 4. Dead-Letter Queue (DLQ) & Quarantine

If all retry attempts are exhausted or a permanent fatal error occurs (e.g., destination host unreachable, unresolvable DNS, malformed template):
1. The notification transitions to status `DEAD_LETTERED`.
2. The payload, complete attempt history, and provider error codes are moved to a quarantine store.
3. An operational metric (`tracelyt_notifications_dead_lettered_total`) is incremented, alerting platform operators.
4. An administrative API allows operators to inspect, fix destination credentials, and safely replay quarantined notifications.

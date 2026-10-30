# Asynchronous Processing & Messaging Strategy

This document evaluates queueing mechanisms, event brokers, and asynchronous scheduling architectures planned for `tracelyt-notifications`.

> **Status Notice:** No message brokers (Kafka, RabbitMQ, SQS, NATS) or queue worker pools are configured in this foundation repository.

---

## 1. Asynchronous Queue Paradigm Evaluation

| Queue Architecture | Candidates | Strengths for Notification Delivery | Weaknesses & Operational Costs | Initial Recommendation |
|---|---|---|---|---|
| **Transactional DB Queue (Outbox)** | PostgreSQL (`pg_notify` / row leases) | Zero new infrastructure; atomic state mutations; simple self-hosted deployment; perfect for low-to-medium volumes (< 500 msgs/sec). | Write amplification on database tables; polling overhead at scale. | **Primary Candidate for Stages 1–4** |
| **Traditional Message Broker** | RabbitMQ, Redis Streams | Native delayed message exchanges for retry backoff; low operational memory footprint; dead-letter exchanges built-in. | Requires managing stateful broker cluster; separate backup and failover. | Candidate for high-concurrency dedicated workers in Stage 5. |
| **Distributed Event Log** | Apache Kafka, Redpanda | Massive throughput (> 100k msgs/sec); partitioned ordering; long-term event replayability. | High operational complexity; poor fit for delayed message scheduling and individual per-message ACK/NACK retries. | Suboptimal for notification dispatch; reserved for telemetry ingestion pipelines. |

---

## 2. Recommendation: Progressive Queue Evolution

1. **Stage 1–4 (Transactional Outbox Pattern):** Notification requests are persisted directly in a relational outbox table alongside delivery state. Delivery workers claim batches using `SELECT ... FOR UPDATE SKIP LOCKED`. This eliminates dual-write race conditions and keeps self-hosted Tracelyt installations simple.
2. **Stage 5–6 (Dedicated Queue Layer):** If notification volume exceeds database outbox capacity (> 1,000 notifications per second), a dedicated queue broker (such as Redis Streams or RabbitMQ) is introduced via formal ADR.

# Capacity Planning and Workload Sizing

This document outlines the capacity sizing methodology, hardware requirements, and scaling dimensions for `tracelyt-notifications`.

---

## 1. Workload Sizing Dimensions

Notification workload is characterized by:
1. **Intake Throughput**: Incoming notification requests per second (RPS) from `tracelyt-alerting`.
2. **Outbound Dispatch Rate**: Egress HTTP requests dispatched across external provider APIs and webhooks.
3. **Delivery Latency Profile**: Time taken by external third-party APIs to accept or reject requests (typically 150ms – 1,500ms).
4. **Storm Amplification**: Sudden spikes during widespread infrastructure incidents where hundreds of alert rules fire simultaneously.

---

## 2. Capacity Sizing Profiles

| Workload Tier | Intake RPS | Sustained Egress RPS | Recommended JVM Nodes | Recommended Memory / CPU | State DB Size (30-day) |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Small (Self-Hosted)** | 1 – 10 RPS | 10 RPS | 1 Node (Combined) | 1 GB RAM / 1 vCPU | ~20 GB |
| **Medium (Enterprise)** | 50 – 200 RPS | 200 RPS | 2 – 4 Worker Nodes | 2 GB RAM / 2 vCPU per node | ~150 GB |
| **Large (Cloud Multi-Tenant)** | 1,000+ RPS | 1,000+ RPS | 8+ Scaled Workers | 4 GB RAM / 4 vCPU per node | ~1 TB (with partitioning) |

---

## 3. High-Density Concurrency with Java 21 Virtual Threads

Traditional thread-per-request architectures require 1 MB of stack memory per thread, capping concurrent outbound network requests at ~1,000 per GB of memory.

By leveraging **Java 21 Virtual Threads (Project Loom)**:
- A single JVM instance can maintain 10,000+ concurrent in-flight outbound HTTP connections waiting on external provider socket responses.
- Eliminates the need for complex reactive programming (WebFlux) while preserving high I/O density.

---

## 4. Bottlenecks and Scaling Gates

1. **State Store Write Throughput**: High-frequency status updates (`ACCEPTED` -> `PROCESSING` -> `DELIVERED`) require batched writes and efficient indexing.
2. **Provider Rate Limits**: Third-party rate limits (e.g., Slack's 1 message per second per channel) dictate egress queue partitioning rather than raw CPU scaling.

---

## 5. Related Documentation

- [Scalability](../architecture/scalability.md)
- [Resource Limits](resource-limits.md)
- [Deployment Models](../architecture/deployment-models.md)

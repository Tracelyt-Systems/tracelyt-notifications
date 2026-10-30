# Performance Testing and Latency Benchmarking

This document outlines the benchmarking methodology, performance test scenarios, and service level objectives (SLOs) for `tracelyt-notifications`.

---

## 1. Service Level Objectives (SLOs)

| Metric | Target Objective | Measurement Window |
| :--- | :--- | :--- |
| **Intake API Latency (p95)** | < 15 ms | Rolling 5-minute window |
| **Intake API Latency (p99)** | < 50 ms | Rolling 5-minute window |
| **End-to-End Delivery Time (p95)** | < 2,000 ms (excluding provider latency) | Rolling 15-minute window |
| **Delivery Success Rate** | > 99.9% of eligible requests | Monthly availability window |

---

## 2. Benchmark Scenarios

### 2.1 Sustained Intake & Egress
- **Objective**: Verify steady-state CPU and memory utilization under continuous traffic.
- **Load Profile**: Constant 200 RPS across 10 concurrent tenants for 60 minutes.
- **Pass Criteria**: Zero JVM heap leaks; garbage collection pause time (p99) < 20 ms.

### 2.2 Alert Storm Surge
- **Objective**: Verify backpressure and rate-limiting behavior during massive incident storms.
- **Load Profile**: Step increase from 10 RPS to 2,000 RPS over 10 seconds, sustained for 5 minutes.
- **Pass Criteria**: System does not crash or exhaust file descriptors; non-critical requests shed gracefully with HTTP 429; critical alerts delivered in priority order.

### 2.3 Slow / Degraded External Provider
- **Objective**: Verify that slow third-party responses do not exhaust worker thread pools.
- **Tooling**: WireMock configured with synthetic 4,000 ms socket delays.
- **Pass Criteria**: Virtual threads absorb high connection count; intake API remains responsive with latency < 20 ms.

---

## 3. Related Documentation

- [Capacity Planning](../operations/capacity-planning.md)
- [Resource Limits](../operations/resource-limits.md)
- [Testing Strategy](../development/testing-strategy.md)

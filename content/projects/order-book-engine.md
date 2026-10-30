+++
title = "Low-Latency Order Book Engine"
weight = 3
aliases = []
[params]
tags_line = "C++20 · lock-free · EC2"
status = "Sep 2025 – Sep 2026"
+++

**Sep 2025 - Sep 2026**

[GitHub repository](https://github.com/RyanJHamby/order-book-engine)

Minimal, high-performance order book engine in C++ designed to explore the foundations of low-latency trading systems. Includes nanosecond-level order matcher skeleton, lock-free queues, thread-local memory pools, and automated benchmarking on AWS EC2 spot instances.

<div class="achievement">
Built C++20 order matching engine with lock-free SPSC ingestion, thread-local slab pools, and inlined matching. On an isolated EC2 <code>c6i.large</code> core over 1M orders: <span class="metric">P50 0.21 µs, P99.9 3.1–3.2 µs, 1.4–1.8M orders/sec</span>
</div>

<div class="achievement">
Automated EC2 spot benchmarking with cloud-init for reproducible, low-cost latency profiling
</div>

*Latency and throughput figures are from the repo README (EC2 `c6i.large`, isolated core, 3 runs), not a `pow run` capture.*

## Architecture

**Order Matching Core:**
- Minimal memory allocation design for sub-microsecond latency
- Inlined matching logic for CPU cache efficiency
- Lock-free queue skeleton for order ingestion
- Thread-local memory pools to reduce contention

**Benchmarking Pipeline:**
- Simulates 1M+ orders with alternating buy/sell sides
- Measures average microseconds per match
- Reproducible results on local machine or EC2

**Separation of Concerns:**
- Order ingestion (queue) → matching engine → latency measurement
- Decoupled architecture mirrors real exchange pipelines

## Local Development

**Build & Run:**
```bash
cd orderbook-engine
chmod +x scripts/build_and_run_benchmark.sh
./scripts/build_and_run_benchmark.sh
```

This script:
- Cleans and creates fresh build directory
- Configures with CMake and builds with parallel jobs
- Runs validation executable
- Executes latency benchmark → `build/benchmark_results.txt`

**Unit Tests:**
```bash
chmod +x scripts/run_tests.sh
./scripts/run_tests.sh
```

Test coverage:
- Order creation, type validation, comparison operations
- Order addition, matching, stress testing (1000 orders)
- Lock-free queue push/pop operations
- Thread-local memory pool allocation (2000 stress allocations)

## Cloud Benchmarking

**Automated EC2 Spot Execution:**
```bash
chmod +x scripts/run_benchmark.sh
./scripts/run_benchmark.sh
```

Process:
1. Launches EC2 spot instance with specified AMI/instance type
2. Cloud-init installs dependencies (build-essential, cmake, git, perf)
3. Clones repository and executes benchmark
4. Logs results to `/home/ubuntu/benchmark_results.txt`
5. Automatically shuts down instance after completion

Benefits: Repeatable benchmarking at low cost with cloud infrastructure consistency.

## Design Insights

1. **Sub-microsecond latency goal:** Minimal allocations, cache-aware layouts, inlined hot paths
2. **Lock-free architecture:** Eliminates mutex contention in order ingestion pipeline
3. **EC2 spot automation:** Reduces operational overhead while maintaining reproducibility
4. **Optimization roadmap:**
   - SIMD vectorization for price matching
   - NUMA-aware memory allocation for multi-threaded workloads
   - Order cancellations and partial fill simulation
   - Latency spike detection and metrics logging

+++
title = "Projects"
+++

## GPU Flight Recorder

**Sep 2026 - Present**

[📊 View GitHub Repository](https://github.com/RyanJHamby/distributed-gpu-training-flight-recorder)

Finds the straggler in a distributed data-parallel training job and explains why it is slow. One slow rank makes every other rank wait at every collective; the symptom (step time went up) says nothing about the cause. Flight Recorder joins per-rank collective timing from the PyTorch NCCL flight recorder with per-GPU NVML telemetry, names the straggling rank, and ranks likely causes (thermal or power throttle, ECC errors, degraded PCIe/NVLink, GPU contention, host stall) with the evidence behind each.

<div class="achievement">
Go agents stream per-rank events over gRPC to a coordinator that correlates collectives by <code>(process_group, sequence_id)</code>, so no cross-node clock synchronization is needed
</div>

<div class="achievement">
Replaced per-collective thresholds (<span class="metric">0/30</span> detected at 10% jitter) with block-median lag tests: <span class="metric">30/30 detection and attribution across 9 injected fault types, 0 false stragglers</span> in simulation
</div>

**Status:** results so far are from a seeded fault simulator; a budget-capped real-GPU validation run is next, and its results will be published whether or not they match.

---

## Open Source Contributions

- **[vllm-project/vllm#48420](https://github.com/vllm-project/vllm/pull/48420)** (merged): root-caused a `StopIteration` crash in Qwen3-Omni multimodal processing on videos with no audio track when `use_audio_in_video=True`; fixed two follow-on false-positive paths in processor caching and parent/child processor inheritance
- **[firecracker-microvm/firecracker#6032](https://github.com/firecracker-microvm/firecracker/pull/6032)** (merged): fixed a VMM panic on ACPI device restore when `EventFd` creation fails under fd exhaustion
- **[firecracker-microvm/firecracker#6033](https://github.com/firecracker-microvm/firecracker/pull/6033)** (merged, docs): documented a DNS lookup delay caused by an IPv6 resolver stall

---

## FlowState

**Mar 2026**

[📊 View GitHub Repository](https://github.com/RyanJHamby/FlowState)

Rust-accelerated temporal join engine for point-in-time ML feature pipelines: join trades, quotes, and signals without look-ahead bias, in batch or streaming.

<div class="achievement">
Rust as-of join engine with O(n+m) merge-scan kernels, zero-copy Arrow via the PyCapsule interface, and lock-free <code>UnsafeCell</code> writes across Rayon workers
</div>

<div class="achievement">
Streaming incremental join with watermark-based emission, per-symbol state, and configurable lateness tolerance; streaming output verified identical to batch
</div>

<div class="achievement">
<span class="metric">132 Rust tests</span>, including property-based checks of every kernel against reference implementations
</div>

---

## Low-Latency Order Book Engine

**Sep 2025 - Sep 2026**

[📊 View GitHub Repository](https://github.com/RyanJHamby/order-book-engine)

Minimal, high-performance order book engine in C++ designed to explore the foundations of low-latency trading systems. Includes nanosecond-level order matcher skeleton, lock-free queues, thread-local memory pools, and automated benchmarking on AWS EC2 spot instances.

<div class="achievement">
Built C++20 order matching engine with lock-free SPSC ingestion, thread-local slab pools, and inlined matching. On an isolated EC2 <code>c6i.large</code> core over 1M orders: <span class="metric">P50 0.21 µs, P99.9 3.1–3.2 µs, 1.4–1.8M orders/sec</span>
</div>

<div class="achievement">
Automated EC2 spot benchmarking with cloud-init for reproducible, low-cost latency profiling
</div>

### Architecture

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

### Local Development

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

### Cloud Benchmarking

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

### Design Insights

1. **Sub-microsecond latency goal:** Minimal allocations, cache-aware layouts, inlined hot paths
2. **Lock-free architecture:** Eliminates mutex contention in order ingestion pipeline
3. **EC2 spot automation:** Reduces operational overhead while maintaining reproducibility
4. **Optimization roadmap:**
   - SIMD vectorization for price matching
   - NUMA-aware memory allocation for multi-threaded workloads
   - Order cancellations and partial fill simulation
   - Latency spike detection and metrics logging

---

## Quant & Trading Projects

## Intelligent Stock Screener

**Oct 2025 - Dec 2025**

[📊 View GitHub Repository](https://github.com/RyanJHamby/stock-screener)

Fully automated stock screening system scanning 3,800+ US stocks daily using Mark Minervini's Trend Template methodology. Identifies high-conviction buy/sell signals via phase-based trend classification, relative strength momentum, and fundamental quality filters.

<div class="achievement">
Automated daily scans of <span class="metric">3,800+ stocks</span> with <span class="metric">74% API reduction</span> via Git-based fundamental caching and GitHub Actions automation
</div>

<div class="achievement">
Phase-based classification identifying Phase 2 uptrend breakouts passing 7 of 8 Minervini criteria (50>150>200 SMA alignment, relative strength ≥70, volume confirmation)
</div>

<div class="achievement">
Risk-managed position management with <span class="metric">max 10% risk, min 2:1 R:R ratio</span>, automated stop-loss trailing, and tax-aware filtering for long-term positions
</div>

### Core Features

**Phase-Based Trend Classification:**
- Phase 1 (Base): Consolidation after decline
- Phase 2 (Uptrend): Confirmed uptrend with 50>150>200 SMA alignment — **BUY ZONE**
- Phase 3 (Distribution): Topping pattern with weakening momentum
- Phase 4 (Downtrend): Declining trend — **AVOID**

**Volatility Contraction Pattern (VCP):**
- Identifies price consolidation before explosive breakout
- Formula: Range_i = ((High_i - Low_i) / Close_i) × 100
- VCP_Score = (∑ Contractions / Total_Periods) × Trend_Quality
- Example: 13 contractions (6.5% → 5.8% → 7.6% → 6.0%) with 54/100 quality score indicates imminent breakout

**Intelligent Market Regime Filtering:**
- Only generates buy signals when SPY in Phase 1/2 with ≥15% of stocks in Phase 2
- Avoids low-probability trades in declining markets
- Sell signals always generated (can exit any market)

**Smart Caching Strategy:**
- Fundamentals stored in Git repository as JSON with metadata
- Earnings season (6 weeks): refresh if >7 days old
- Normal periods: refresh if >90 days old
- Result: 74% fewer API calls, 15-20 min faster scans

### Sample Output

<details>
<summary style="cursor: pointer; font-weight: bold; padding: 1em; background: #f8f9fa; border-radius: 6px; margin: 1.5em 0;">
📊 View Sample Scan Output (Jan 9, 2026)
</summary>

```
OPTIMIZED FULL MARKET SCAN - ALL US STOCKS
Scan Date: 2026-01-09
Generated: 2026-01-09 14:04:49

SCANNING STATISTICS
Total Universe: 3,819 stocks
Analyzed: 1,188 stocks
Buy Signals: 370 | Sell Signals: 111
Error Rate: 0.26%

SPY Trend: Phase 2 - Uptrend (Bullish)
  • 50 SMA: $678.39 (slope: 0.0563)
  • 200 SMA: $626.72 (slope: 0.0982)
  • Confidence: 85%

Market Breadth (n=1,188):
  • Phase 1 (Base): 560 (47.1%)
  • Phase 2 (Uptrend): 504 (42.4%)
  • Phase 3 (Distribution): 1 (0.1%)
  • Phase 4 (Downtrend): 123 (10.4%)

Market Regime: RISK-ON (Strong)

⭐ BUY #1: WWD | Score: 104.5/110
  Phase: 2 | Entry Quality: Good | R:R: 3.2:1
  Stop Loss: $299.25
  • 11.1% above 50 SMA (strong breakout)
  • Revenue: +16.5% YoY | EPS: +64% YoY
  • Volume confirmation (1.17 ratio)
```

</details>

---

## Covariance-Based Macro Trading System

**Sep 2023 - Present**

[📊 View GitHub Repository](https://github.com/RyanJHamby/macro-factor-decomposition)

Systematic S&P 500 futures trading system powered by eigendecomposition of economic indicator covariance matrices. Decomposes 8×8 macro factor covariance to identify uncertainty regimes and size positions via macro surprise exposure.

<div class="achievement">
Achieved <span class="metric">1.4 Sharpe ratio</span> over 17-year backtest at <span class="metric">12% max drawdown</span> via regime-aware position sizing and macro surprise decomposition
</div>

<div class="achievement">
C++ factor decomposition engine (Eigen 3.4.0) processing 8 FRED indicators + VIX with AWS Lambda daily automation, computing eigendecomposition in <span class="metric">12ms</span>
</div>

<div class="achievement">
End-to-end pipeline: FRED API → monthly frequency alignment (downsampling/Hermite interpolation) → spectral decomposition (Σ = UΛUᵀ) → S3 with <span class="metric">180+ unit tests</span> and 73% alignment with NBER recession dates
</div>

### Core Hypothesis

Markets respond to **unexpected** economic information, not levels. Raw covariance is misleading—it captures expected relationships.

Standard assumption: E[r_t | X_t] = α + βX_t

Reality: Markets react to **surprises: ΔX_t - E_t[ΔX_t]**

Solution: Decompose surprise covariance via PCA to identify 3-4 interpretable macro factors (growth, inflation, policy, volatility) and measure ES exposure across regimes.

### 5-Stage Architecture

1. **Data Acquisition:** FRED API (CPI, GDP, Unemployment, Sentiment, Fed Funds, Treasury yields) + VIX
2. **Temporal Alignment:** Daily → month-end LOCF, Quarterly → Hermite interpolation to monthly
3. **Covariance Estimation:** Σ_ij = (1/(n-1)) ∑_t (X_it - X̄_i)(X_jt - X̄_j)
4. **Spectral Decomposition:** Σ = UΛUᵀ → First 3-4 eigenvalues capture 85-92% variance
5. **Regime Quantification:** Frobenius norm ‖Σ‖_F = √(∑_i,j σ²_ij) maps to regime state

**Regime Classification:**
- **Stable** (‖Σ‖_F < μ - σ): Low uncertainty, tight co-movement
- **Neutral** (μ - σ ≤ ‖Σ‖_F ≤ μ + σ): Moderate uncertainty
- **Elevated** (‖Σ‖_F > μ + σ): High uncertainty, factor decoupling

### Infrastructure

**AWS Stack:**
- EventBridge (cron: daily 12:00 UTC) → Lambda (512MB, 600s) → S3 (versioned, encrypted)
- Lambda execution: ~4.2s average (p95: 8.7s)
- Native C++ binary (662 KB) with Eigen, AWS SDK, curl
- IaC: AWS CDK 2.x (TypeScript, dev/staging/prod)

**Validation:**
- 180+ unit tests: covariance symmetry, eigenvalue ordering, numerical stability
- 5+ year backtests: 73% alignment with NBER recession dates

### Data Inputs

8 economic indicators at mixed frequencies:
- CPI (monthly) - Inflation anchor
- Real GDP (quarterly) - Earnings driver
- Unemployment (monthly) - Labor tightness
- Consumer Sentiment (monthly) - Forward demand
- Fed Funds (monthly) - Discount rate
- 10Y/2Y Treasury (daily) - Yield curve
- VIX (daily) - Realized volatility

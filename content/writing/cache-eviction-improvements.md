+++
title = "Cache Eviction: 30 Years of Improvements"
date = 2025-01-11
draft = false
+++

## Introduction

Cache hierarchies are everywhere—from L1/L2/L3 on your CPU to Redis clusters backing your microservices. But the way we organize and manage these tiers has fundamentally transformed over the past three decades. What started as simple in-memory buffers has evolved into a sophisticated science of eviction policies, write-through strategies, and predictive prefetching.

This post explores why caches are structured the way they are, how eviction strategies have improved, and what the actual data tells us about their effectiveness over time.

## The Cache Problem

At its core, caching solves a fundamental asymmetry: access speeds vary wildly. Reading from memory takes ~100 nanoseconds. Reading from disk takes ~10 milliseconds. That's a 100,000x difference. A cache's job is to minimize trips to slower storage by keeping hot data nearby.

But caches have finite capacity. When full, you must decide what to evict. Get this wrong, and your hit rate craters. Get it right, and you can hide most of the latency penalty.

## Historical Context: Why Hierarchies Exist

Early computers (1980s-early 1990s) had flat memory architectures. A single level of cache—or none at all. As CPU speeds increased while DRAM latency barely budged, the problem became acute. A CPU could execute instructions faster than memory could feed them data.

Intel's solution, pioneered with the i486 (1989), was multi-tier caching:

- **L1 Cache**: Tiny (8-32KB), extremely fast (2-4 cycles), physically close to execution units
- **L2 Cache**: Larger (256KB-1MB), slower (10-20 cycles), shared or per-core
- **L3 Cache**: Larger still (4-16MB), even slower (40-75 cycles), shared across cores

The insight was hierarchical: if you can't fit everything in L1, overflow to L2. If you can't fit in L2, overflow to L3. This architecture minimizes the probability of hitting the slowest tier (main memory).

By the late 1990s, this pattern was so effective that it became the de facto standard for all levels of caching—from CPU caches to database buffers to distributed caches like memcached.

## Eviction Policies: The Core Problem

With multiple tiers, the critical question is: which data stays, which gets evicted?

### Least Recently Used (LRU)

LRU was the dominant policy for decades. The intuition is simple: if you haven't used something recently, you won't need it soon. Remove the least recently accessed item when capacity is exceeded.

```
Access pattern: A, B, C, A, B, D (cache size = 3)

Step 1: [A]
Step 2: [A, B]
Step 3: [A, B, C]
Step 4: [B, C, A]  (A accessed, moves to end)
Step 5: [C, A, B]  (B accessed, moves to end)
Step 6: [A, B, D]  (C evicted, D added)
```

LRU is simple to implement and works reasonably well for temporal locality (programs access recently-used data again soon). However, it has a critical weakness: sequential scans. If you're scanning a large array, you evict the entire cache's contents without using them twice.

### Least Frequently Used (LFU)

LFU tracks how many times each item was accessed, evicting the least-accessed. It captures true "popularity" better than LRU.

The trade-off? It's expensive. Maintaining frequency counters requires additional bookkeeping. More importantly, it's inflexible to access pattern changes. An item accessed 100 times an hour ago is treated the same as an item accessed 100 times just now.

### Variants and Hybrids

By the 2000s, the research community had developed sophisticated variants:

- **Clock**: LRU approximation using a circular buffer and a single "hand" pointer. Much faster than true LRU.
- **W-TinyLFU**: Hybrid combining recency (LRU) and frequency (LFU). Used in Caffeine cache (Java).
- **ARC** (Adaptive Replacement Cache): Learns whether your workload benefits more from recency or frequency, adjusts dynamically.

Modern caches like Redis (v4.0+) support multiple policies, letting you choose based on your access patterns.

## Cache Tier Interactions: A Sequence Diagram

How do these tiers actually work together? Here's a typical read miss cascading through the hierarchy:

```
CPU Core                   L1 Cache              L2 Cache              L3 Cache              Main Memory
    |                          |                     |                     |                      |
    | Read 0x1234 (miss)       |                     |                     |                      |
    |------- req ------------->|                     |                     |                      |
    |                          | Check 0x1234 (miss) |                     |                      |
    |                          |------- req -------->|                     |                      |
    |                          |                     | Check 0x1234 (miss) |                      |
    |                          |                     |------- req -------->|                     |
    |                          |                     |                     | Check 0x1234 (hit)  |
    |                          |                     |                     |<----- data ---------|
    |                          |                     |<----- data ---------|                      |
    |                          |                     | [Evict if full]     |                      |
    |                          |<----- data ---------|                     |                      |
    |                          | [Evict if full]     |                     |                      |
    |<----- data --------------|                     |                     |                      |
    | [Execute with data]      |                     |                     |                      |
```

When the CPU needs data, it checks L1. Missing, it requests L2. Missing there too, L3. Finally main memory. On the way back, the data fills each tier. If a tier is full, an eviction policy determines what gets removed.

The key insight: **lower tiers must have space**. If L1 evicts to L2 but L2 is full, L2 must first evict to L3. This cascading effect is why eviction policy matters—poor choices at one level propagate upward.

## Write-Through vs. Write-Back

How do we handle writes? Two main strategies emerged:

### Write-Through
Every write goes immediately to the next level down:

```
CPU writes to L1 → L1 writes to L2 → L2 writes to L3 → L3 writes to main memory
```

Advantage: Data is always consistent. Disadvantage: Write latency is high (you wait for main memory).

### Write-Back
Write to the cache, mark it as "dirty," and only write down when that cache line is evicted:

```
CPU writes to L1 → L1 marks as dirty (done immediately)
[Later, when L1 needs space]
L1 evicts dirty line → writes to L2
```

Advantage: Write latency is much lower. Disadvantage: Complexity and risk of data loss if the cache fails before writeback.

Modern systems mostly use write-back with careful handling of dirty bits and write-back queues.

## Prefetching: Getting Ahead of Misses

By the 2010s, architectures added speculative prefetching. If you access `A[i]`, the hardware speculatively prefetches `A[i+1]`, `A[i+2]`, etc.

This reduces cache misses for predictable access patterns but adds complexity and can waste cache space on mispredictions.

## Quantifying Improvements: 30 Years of Data

Let me put numbers to this evolution. Here's what the research shows about hit rates:

**L1 Cache Hit Rates (1995 vs. 2025)**
- 1995 (Pentium): ~90% typical hit rate, ~80% worst-case
- 2005 (Core 2): ~92% typical hit rate, ~85% worst-case
- 2015 (Broadwell): ~94% typical hit rate, ~88% worst-case
- 2025 (Sapphire Rapids): ~95% typical hit rate, ~90% worst-case

The improvements are incremental but consistent. Modern CPUs benefit from:
- Smarter prefetching algorithms (now ML-assisted in latest Intel/AMD chips)
- Larger L3 caches relative to working set sizes
- Better eviction policies (Clock approximation vs. naive LRU)

**L3 Cache Eviction Rates (Misses per 1000 Accesses)**

```
Year    LRU (Naive)    Clock    ARC      Optimal
1995    ~150           ~140     N/A      ~120
2000    ~130           ~115     ~110     ~95
2005    ~110           ~95      ~90      ~75
2010    ~95            ~80      ~75      ~60
2015    ~75            ~60      ~55      ~40
2020    ~60            ~45      ~40      ~25
2025    ~50            ~35      ~30      ~18
```

(These are synthetic workload averages; real numbers vary by application.)

Why the steady decline? Several factors:

1. **Better eviction policies**: We moved from naive LRU to adaptive, learning-based policies.
2. **Larger caches**: L3 cache sizes have grown 10x since 1995, making "everything fits" more common.
3. **Prefetching**: Modern hardware prefetches so accurately that cache misses are often hidden.
4. **Compiler improvements**: Compilers now optimize for cache behavior (loop tiling, data layout).

## Distributed Caches: The Pattern Scales

The same principles that work for CPU caches apply to distributed systems. Redis, memcached, and distributed caching layers all use variants of these eviction policies.

When you configure Redis with `maxmemory-policy allkeys-lru`, you're using the same principle: keep recently-accessed data, evict the rest.

The challenge in distributed caching is higher complexity:

- Multiple servers must coordinate eviction
- Network latency means prefetching is less effective
- Workloads are often less predictable

Yet the core insight remains: a well-tuned eviction policy reduces misses, increases throughput, and lowers latency.

## The Practical Takeaway

If you're building a system with caching, here's what 30 years of research tells us:

1. **LRU is good**, but variants like Clock or ARC are better. If your framework supports it, use them.
2. **Understand your access patterns**. Sequential scans need different policies than random access.
3. **Measure hit rates**. You can't optimize what you don't measure. Profile your actual cache behavior.
4. **Prefetching matters**. For predictable workloads, it can reduce eviction pressure by 20-30%.
5. **Size your caches conservatively**. A cache that's 80% full is more stable than one constantly at capacity.

The evolution of caching isn't flashy—no breakthroughs, just steady incremental improvements. But collectively, those improvements mean modern systems need far fewer trips to slow storage than systems from 20 years ago.

That's the power of doing one thing well.

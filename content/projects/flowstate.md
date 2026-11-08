+++
title = "FlowState"
weight = 2
aliases = []
[params]
tags_line = "Rust · Arrow · Rayon"
status = "Mar 2026 – Oct 2026"
+++

**Mar 2026 - Oct 2026**

[GitHub repository](https://github.com/RyanJHamby/FlowState)

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

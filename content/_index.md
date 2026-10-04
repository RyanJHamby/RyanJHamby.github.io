+++
title = "Home"
+++

![Profile Picture](/images/engin.JPG)

I make AI compute fast, efficient, and reliable, from the serving layer down to the hardware and the power behind it.

**New York, NY | Software Engineer II @ AWS**

At AWS I build fault-tolerant, multi-tenant payment and IoT systems. Outside work I build the layer AI runs on: a straggler detector for distributed GPU training, merged fixes in vLLM and Firecracker, a Rust temporal join engine, and a sub-microsecond C++ order book.

[Resume (PDF)](/pdfs/Ryan_Hamby_Resume.pdf) | [LinkedIn](https://www.linkedin.com/in/ryan-j-hamby/) | [GitHub](https://github.com/RyanJHamby) | [ryan.j.hamby@gmail.com](mailto:ryan.j.hamby@gmail.com)

---

## Check out my Personal Tech Blog!

Systems, performance, and the craft of building software. [Read more](/blog)

{{< recent-posts 3 >}}

---

## Featured Projects

<div class="projects-grid">

<div class="project-tile">
<div class="project-tile-header">
<h3>GPU Flight Recorder</h3>
<div class="project-tags">
<span class="project-badge">Go</span>
<span class="project-badge">gRPC</span>
<span class="project-badge performance-badge">NCCL + NVML</span>
</div>
</div>
<div class="project-tile-content">
<p>Finds the straggling rank in distributed GPU training and explains why it is slow, joining PyTorch NCCL collective timings with per-GPU hardware telemetry.</p>
<a href="/projects/#gpu-flight-recorder" class="project-link">Explore →</a>
</div>
</div>

<div class="project-tile">
<div class="project-tile-header">
<h3>vLLM &amp; Firecracker</h3>
<div class="project-tags">
<span class="project-badge">Open Source</span>
<span class="project-badge">Python</span>
<span class="project-badge performance-badge">Rust</span>
</div>
</div>
<div class="project-tile-content">
<p>Merged fixes in vLLM (Qwen3-Omni multimodal crash and processor-cache false positives) and Firecracker (VMM snapshot-restore panic).</p>
<a href="/projects/#open-source-contributions" class="project-link">Explore →</a>
</div>
</div>

<div class="project-tile">
<div class="project-tile-header">
<h3>FlowState</h3>
<div class="project-tags">
<span class="project-badge">Rust</span>
<span class="project-badge">Arrow</span>
<span class="project-badge performance-badge">Rayon</span>
</div>
</div>
<div class="project-tile-content">
<p>Rust as-of join engine with zero-copy Arrow, parallel merge scans, and streaming watermark joins for point-in-time ML features.</p>
<a href="/projects/#flowstate" class="project-link">Explore →</a>
</div>
</div>

<div class="project-tile">
<div class="project-tile-header">
<h3>Order Book Engine</h3>
<div class="project-tags">
<span class="project-badge">C++20</span>
<span class="project-badge">Lock-Free</span>
<span class="project-badge performance-badge">0.21µs P50</span>
</div>
</div>
<div class="project-tile-content">
<p>Order matching engine with slab memory pools and lock-free SPSC ingestion, benchmarked on isolated EC2 cores.</p>
<a href="/projects/#low-latency-order-book-engine" class="project-link">Explore →</a>
</div>
</div>

<div class="project-tile">
<div class="project-tile-header">
<h3>Stock Screener</h3>
<div class="project-tags">
<span class="project-badge">Python</span>
<span class="project-badge">Trading</span>
<span class="project-badge performance-badge">3,800+/day</span>
</div>
</div>
<div class="project-tile-content">
<p>Daily Minervini Trend Template scanner over 3,800+ US stocks, automated with GitHub Actions and Git-based caching.</p>
<a href="/projects/#intelligent-stock-screener" class="project-link">Explore →</a>
</div>
</div>

<div class="project-tile">
<div class="project-tile-header">
<h3>Java4Java</h3>
<div class="project-tags">
<span class="project-badge">Swift</span>
<span class="project-badge">Kotlin</span>
<span class="project-badge performance-badge">Spaced repetition</span>
</div>
</div>
<div class="project-tile-content">
<p>Cross-platform spaced repetition app for algorithm practice on iOS, Android, and macOS.</p>
<a href="/hobby-projects/#java4java--iosandroid-anki-like-leetcode-learning-platform" class="project-link">Explore →</a>
</div>
</div>

</div>

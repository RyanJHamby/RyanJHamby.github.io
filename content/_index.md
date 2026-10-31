+++
title = "Ryan J Hamby"
description = "Software engineer working on AI compute, from the serving layer to the hardware: vLLM and Firecracker contributions, GPU telemetry, Rust and low-latency C++."
+++

I make AI compute fast, efficient, and reliable, from the serving layer down to the hardware and the power behind it.

Software Development Engineer II at AWS, New York. At work: fault-tolerant, multi-tenant payment and IoT systems. Outside work: the layer AI runs on.

<div class="links-line">

[Resume](/pdfs/Ryan_Hamby_Resume.pdf) [GitHub](https://github.com/RyanJHamby) [LinkedIn](https://www.linkedin.com/in/ryan-j-hamby/) [Substack](https://substack.com/@ryanjhamby) [Email](mailto:ryan.j.hamby@gmail.com)

</div>

## Merged upstream

<ul class="work-list">
<li><span class="meta">vLLM · MERGED 2026-08-03</span><strong><a href="https://github.com/vllm-project/vllm/pull/48420">Qwen3-Omni crash on videos with no audio track</a></strong><br>Root-caused a <code>StopIteration</code> in multimodal processing when <code>use_audio_in_video=True</code>; fixed two follow-on false-positive paths in processor caching and class inheritance.</li>
<li><span class="meta">FIRECRACKER · MERGED 2026-07-16</span><strong><a href="https://github.com/firecracker-microvm/firecracker/pull/6032">VMM panic on ACPI device restore</a></strong><br>Fixed a panic when <code>EventFd</code> creation fails under fd exhaustion.</li>
<li><span class="meta">FIRECRACKER · MERGED 2026-07-23 · DOCS</span><strong><a href="https://github.com/firecracker-microvm/firecracker/pull/6033">DNS lookup delay from an IPv6 resolver stall</a></strong><br>Documented the cause of the delay.</li>
<li><span class="meta">vLLM · OPEN, OPENED 2026-09-19</span><strong><a href="https://github.com/vllm-project/vllm/pull/57722">NIXL metrics: registration-expiry and writer-loop-error counters</a></strong><br>Not merged yet.</li>
</ul>

[All open-source work](/projects/#open-source)

## Selected work

<ul class="work-list">
<li><span class="meta">RUST · ARROW · 2026</span><strong><a href="/projects/flowstate/">FlowState</a></strong><br>Rust temporal join engine for point-in-time ML feature pipelines, batch and streaming, with zero-copy Arrow.</li>
<li><span class="meta">GO · GRPC · SIMULATED RESULTS</span><strong><a href="/projects/gpu-flight-recorder/">GPU Flight Recorder</a></strong><br>Names the straggling rank in distributed GPU training by joining NCCL collective timings with per-GPU telemetry. Validated in simulation; no real-hardware results yet.</li>
<li><span class="meta">C++20 · 2025–2026</span><strong><a href="/projects/order-book-engine/">Low-Latency Order Book Engine</a></strong><br>Lock-free SPSC ingestion and thread-local slab pools, benchmarked on EC2.</li>
</ul>

## Writing

{{< recent-posts 3 >}}

[All posts](/writing) · [Subscribe on Substack](https://substack.com/@ryanjhamby)

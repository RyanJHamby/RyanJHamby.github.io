+++
title = "GPU Flight Recorder"
weight = 1
aliases = []
[params]
tags_line = "Go · gRPC · NCCL + NVML"
status = "Mar 2026 · early build"
+++

**Mar 2026**

[GitHub repository](https://github.com/RyanJHamby/distributed-gpu-training-flight-recorder)

Finds the straggler in a distributed data-parallel training job and explains why it is slow. One slow rank makes every other rank wait at every collective; the symptom (step time went up) says nothing about the cause. Flight Recorder joins per-rank collective timing from the PyTorch NCCL flight recorder with per-GPU NVML telemetry, names the straggling rank, and ranks likely causes (thermal or power throttle, ECC errors, degraded PCIe/NVLink, GPU contention, host stall) with the evidence behind each.

<div class="achievement">
Go agents stream per-rank events over gRPC to a coordinator that correlates collectives by <code>(process_group, sequence_id)</code>, so no cross-node clock synchronization is needed
</div>

**Status:** early build. The agent, ring buffer, correlator, attribution engine and gRPC transport exist; there are no validation results yet. Results will be published, with hardware named, once a captured run exists.

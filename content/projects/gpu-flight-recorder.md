+++
title = "GPU Flight Recorder"
weight = 1
aliases = []
[params]
tags_line = "Go · gRPC · NCCL + NVML"
status = "Mar 2026 – Sep 2026 · simulated results only"
+++

**Mar 2026 - Sep 2026**

[GitHub repository](https://github.com/RyanJHamby/distributed-gpu-training-flight-recorder)

Finds the straggler in a distributed data-parallel training job and explains why it is slow. One slow rank makes every other rank wait at every collective; the symptom (step time went up) says nothing about the cause. Flight Recorder joins per-rank collective timing from the PyTorch NCCL flight recorder with per-GPU NVML telemetry, names the straggling rank, and ranks likely causes (thermal or power throttle, ECC errors, degraded PCIe/NVLink, GPU contention, host stall) with the evidence behind each.

<div class="achievement">
Go agents stream per-rank events over gRPC to a coordinator that correlates collectives by <code>(process_group, sequence_id)</code>, so no cross-node clock synchronization is needed
</div>

## Results (synthetic)

Eight ranks, 600 steps, one fault injected on a random rank at the midpoint, 30 seeds per cell, seeded and deterministic. Reproduce with `make sim`; the scorecard is `docs/scorecard.md` in the repository.

| Condition | Detected | Attributed correctly | False stragglers |
|---|---|---|---|
| 9 fault types, 3% op jitter, 30% straggler lag | 30/30 each | 30/30 each | 0 |
| 9 fault types, 10% op jitter, 30% straggler lag | 30/30 each | 30/30 each | 0 |
| Clean runs (both noise levels) | n/a | n/a | 0 |

Sensitivity of thermal-fault detection to straggler lag (3% jitter): 2% lag detected 0/30, 5% lag and above 30/30. A first version that thresholded each collective scored 0/30 at 10% jitter; detection now uses block medians over a fault span.

*These figures are from the repository's own README and scorecard, produced by its seeded simulator, not from a `pow run` capture. They are simulated.* The simulator's noise is independent Gaussian, real clusters are correlated and heavy-tailed, and each attribution rule is tested against a fault the simulator generated to trigger it. The results show the logic is sound, not that it works on hardware.

## Status

Implemented and tested in CI: detection, attribution, transport, agent and CLI, with a containerized demo in which eight agents stream a replayed trace to a coordinator. **Not yet done:** the Python shim has never run against real PyTorch or NVML, the real-GPU harness is drafts, the Kubernetes manifests have never been applied, and there are no real-hardware results. The next step is a budget-capped real-GPU run; a result that disagrees with the synthetic scorecard will be published, not tuned away.

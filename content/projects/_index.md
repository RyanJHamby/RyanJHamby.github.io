+++
outputs = ["HTML"]
description = "Open-source contributions to vLLM and Firecracker, plus systems projects in Rust, C++ and Go."
title = "Projects"
aliases = []
+++

Work that is public and checkable. Figures are quoted only where a repo or a captured run backs them; each page says which.

## Open source

- [vllm-project/vllm#48420](https://github.com/vllm-project/vllm/pull/48420) (merged): root-caused a `StopIteration` crash in Qwen3-Omni multimodal processing on videos with no audio track when `use_audio_in_video=True`; fixed two follow-on false-positive paths in processor caching and parent/child processor inheritance.
- [firecracker-microvm/firecracker#6032](https://github.com/firecracker-microvm/firecracker/pull/6032) (merged): fixed a VMM panic on ACPI device restore when `EventFd` creation fails under fd exhaustion.
- [firecracker-microvm/firecracker#6033](https://github.com/firecracker-microvm/firecracker/pull/6033) (merged, docs): documented a DNS lookup delay caused by an IPv6 resolver stall.
- [vllm-project/vllm#57722](https://github.com/vllm-project/vllm/pull/57722) (open, opened 2026-09-19): NIXL metrics, registration-expiry and writer-loop-error counters. Not merged.

## Systems and tools

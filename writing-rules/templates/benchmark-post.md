---
title: "<Specific, result-bearing title — only measured numbers>"
date: YYYY-MM-DD
type: benchmark
tags: [inference, energy, cost]
run_ids: [<run-id>]
results_commit: <sha>
---

<!-- NOTES (AI fills: TODOs, HUMAN gaps, uncertain classifications, unmet rules) -->

**TL;DR.** <Question in one clause. Answer in one sentence with the key number
[run:]. The main caveat in one sentence.>

**Why this matters.** <1–2 sentences: what this changes for someone running
inference, in $, W, or SLA terms.>

## The question

<What I wanted to know and why the common assumption might be wrong
(cite the assumption [cite:]).>

## What I did  [HUMAN]

<From seed.md only: the setup in plain words, the key decisions I made in
designing the experiment, and why. Full specs go in the Spec block.>

## Results

<The shareable figure first. Caption: finding + hardware + run id + n.>

<2–4 short paragraphs walking through what the figure shows. Every number
tagged. Include the configurations that lost.>

| Config | Metric 1 (p50 / p99) | Metric 2 | Energy/token | Quality | Within SLA? |
|---|---|---|---|---|---|
| ... | [run:] | [run:] | [run:] | [run:] | yes/no |

## What surprised me  [HUMAN]

<From seed.md: the thing I didn't expect, a dead end, or a result that
contradicted my hypothesis.>

## What I'd do with this  [HUMAN]

<My judgment: the setting I'd pick, for whom, and under what constraints.
Clearly labeled as opinion.>

## Limits of this result

- **What I didn't test:** <...>
- **Threats to validity:** <...>
- **Measurement boundary:** <GPU board / node / facility>

## Spec

<details>
<summary>Full benchmark specification</summary>

### Hardware
### Software
### Workload
### Metrics definitions
### Energy method
### Cost inputs
### Statistics
(Every field from EVIDENCE.md §4; `n/a` or `unknown`, never omitted.)

Machine-readable: `results/<run-id>/metadata.json` @ `<sha>`
</details>

## Reproduce

```bash
# exact commands, pinned versions
```

Approximate cost to reproduce: <$ and GPU-hours [est:]>

## What's next

<One or two open questions this result raises.>

## References

[1] ...

---
<Footer from STYLE.md §8>

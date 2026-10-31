# Content backlog

One line per candidate post. A candidate needs **evidence that exists or a plan to produce it**, a pillar from
`CONTENT.md` §2, and a type from §3. If an AI with web access could write 80% of it without you, it does not belong here.
Status values: `blocked` (needs a capture or a decision), `needs-seed` (evidence exists, your account of it does not),
`ready` (seed and claims filled, waiting for CHECKLIST), `published`.

Started 2026-10-30. Only entries backed by something in a repo are listed; add a line when a `pow log` entry or capture
turns into a finding.

| # | Candidate | Pillar / type | Evidence | Status | Next step |
|---|---|---|---|---|---|
| 1 | Cost and energy of serving one model on one rented GPU under a latency SLO | Measure / benchmark (anchor) | `tokenomics-bench`: harness and pre-registration exist; **no hardware runs yet** | blocked | Run the plan on rented hardware within its budget cap; capture with `pow run`. This is the strongest anchor: it already follows the method this system requires |
| 2 | How I retracted my own "1.8x faster than Polars" README claim, and what a fair as-of join comparison needs | Build log / dead end | FlowState journal and README; captures at `fdc202b` and `53084c2`; withdrawn draft in `drafts/flowstate-asof-join` | blocked | Needs the fair harness (FlowState specs `bench-result-equality`, `bench-interleaved-timing`, `bench-env-capture`, `bench-phase-breakdown`) and a server-hardware rerun, then a rewrite |
| 3 | Root cause of the Qwen3-Omni `StopIteration` crash on videos with no audio track | Build log / note | merged vLLM PR #48420 (public) | needs-seed | Write `seed.md`: how you found it, what you ruled out, what surprised you |
| 4 | A VMM panic on ACPI device restore under fd exhaustion | Build log / note | merged Firecracker PR #6032 (public) | needs-seed | Same: your account of the debugging path |
| 5 | A DNS lookup delay from an IPv6 resolver stall in a microVM | Build log / note | merged Firecracker docs PR #6033 | needs-seed | Same; keep to what the PR shows |
| 6 | Latency of a lock-free order book on a cloud instance, with the losing configurations | Measure / benchmark | `OrderBookEngine` README figures (EC2 `c6i.large`) are **not** from a `pow run` capture | blocked | Re-run the benchmark under `pow run`; your README already notes PMU counters are unavailable on that instance size |
| 7 | Straggler detection in distributed training, validated | Measure / benchmark | `GPU Flight Recorder` is implemented with a seeded simulator and scorecard (synthetic); real-GPU runbook is in `bench/README.md`; no real-hardware results | blocked | Needs the budget-capped real-GPU run from `bench/README.md`; publish the result whether or not it matches the synthetic scorecard |

## Cadence (realistic)
- One **anchor** post per quarter, from a pillar-1 or pillar-4 finding with a full Spec block.
- A **note** only when a captured finding exists. Silence is better than a thin post.
- Re-run a published method when versions change and publish the delta; never edit a published number.

## Where ideas come from
`docs/journal.md` entries and `results/` captures in each repo. Review them weekly with the proof-of-work weekly review and
move anything that is a finding into this table.

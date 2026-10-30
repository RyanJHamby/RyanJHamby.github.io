# CONTENT.md — What to publish, and what every post must carry over time

The bet: as AI makes fluent text free, readers (and the AI search tools that
increasingly sit between them and the web) reward what can't be generated:
**primary data, accountable judgment, and a track record.** This file decides
*what* gets written so the rules in STYLE and EVIDENCE have something worth
applying them to.

## 1. What the world will keep valuing (and what it won't)

| Rising in value | Falling in value |
|---|---|
| Original measurements on named hardware, raw data public | Explainers of well-documented concepts |
| Failures, dead ends, and decisions with stated trade-offs | Summaries of other people's posts or papers |
| Reproducible artifacts (benchmarks, datasets, tools) | Opinion without evidence; hot takes |
| Longitudinal series (same method, re-run as hardware/software move) | One-off "I tried X" posts with no follow-up |
| A named person with a dated, corrected public record | Anonymous or ghostwritten content |
| Cross-domain insight (AI infra × power/grid) few people can do | Single-domain content anyone in the field could write |
| Calibrated uncertainty ("in my runs," "I don't know yet") | False confidence |

Rule of thumb: **if an AI with web access could write 80% of the post without
you, don't write it.**

## 2. Content pillars (everything maps to one)

1. **Measure:** benchmarks of cost, energy, latency, and reliability in AI serving.
2. **Power:** where AI compute meets electricity: tariffs, grid constraints,
   interconnection, flexible load.
3. **Operate:** running AI in constrained environments (on-prem, air-gapped,
   power-limited), in general terms that never touch employer specifics.
4. **Build log:** dead ends, design decisions, and OSS contributions.

## 3. Post types

| Type | Template | Cadence | Must contain |
|---|---|---|---|
| Benchmark (anchor) | `templates/benchmark-post.md` | Quarterly | New data, full Spec block, losing configs, one shareable figure |
| Dead end / postmortem | `templates/dead-end.md` | 1–2 per year | What I believed, what happened, what I'd do instead |
| Explainer with a twist | `templates/explainer.md` | Occasional | A concept + my measurement or worked example that tests it |
| Note | `templates/note.md` | Weekly-ish | One finding, one chart, one link to data |

No other post types without updating this file.

## 4. What every post must carry, and why it compounds

These are required now and get more valuable as the archive grows:

- **A stable method version.** Tag each benchmark with `method: vN` (defined
  in the benchmark repo). Readers and future-you can compare posts across years.
- **Links backward.** Each new post links the earlier post it extends, updates,
  or contradicts. The archive should read as one evolving investigation.
- **An "As of" line.** Hardware, software, and prices go stale fast; the date
  tells readers what still holds.
- **One open question at the end.** Seeds the next post and invites replies.
- **The shareable figure.** One chart that survives being screenshotted out
  of context (title states the finding, caption names hardware + run id).
- **A data citation block.** Machine-readable (`CITATION.cff` in the benchmark
  repo; DOI via Zenodo once a dataset matters) so others, and AI search tools,
  can cite the numbers correctly.

## 5. Things that compound if started early

- **A living index page** (`/benchmarks`) listing every result with method
  version, hardware, date, and status (current / superseded).
- **Re-runs.** When new GPUs, vLLM versions, or quantization methods land,
  re-run the same method and publish "what changed." Series beat one-offs.
- **Corrections in public.** A visible changelog is a credibility asset, not
  an embarrassment.
- **Named collaborators.** Credit people who reproduce, critique, or extend
  your work (with permission). Their audiences become yours.

## 6. Keeping it interesting (without hype)

- Lead with a tension: a cost, a contradiction of common assumptions (cited),
  or a result that surprised you.
- Show the losing configurations. Readers trust work that includes what failed.
- Mix scales: a cluster-level estimate next to a single-GPU measurement,
  clearly labeled as each.
- Occasionally go one level down (kernel, power rail, tariff line item) and one
  level up (what this means for a datacenter or the grid).
- Vary formats: a whiteboard video for a hard concept, a calculator for a
  cost model, a note for a quick finding.

## 7. Never publish

- Anything from Hume or any employer without written clearance
- Numbers without a run or a citation behind them
- Takes outside the pillars (politics, drama, general AI hype)
- Content about private individuals without permission
- Content you couldn't defend line-by-line in an interview

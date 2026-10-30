# STYLE.md — Voice, prose, and format

## 1. Voice

- **An engineer explaining to a sharp peer.** Not a marketer, not a professor,
  not a thought leader.
- **First person, singular.** "I measured," "I'd choose." Not "we" unless a
  real team did it.
- **Direct and calm.** State the finding, then the evidence. No hype, no
  outrage, no breathlessness.
- **Calibrated.** Confidence matches evidence. One run is "in my runs," not
  "always."
- **Generous to others' work.** Cite people you build on. Disagree with
  arguments, never people.

## 2. Structure: answer first

Every post opens with, in order:

1. **Title:** specific and result-bearing.
   - Good: "Capping an H100 at 450W cost 3% throughput at fixed p99" (only if measured)
   - Bad: "Exploring GPU Power Efficiency"
2. **One-paragraph TL;DR:** the question, the answer, the main caveat.
   A reader who stops here should still learn something true.
3. **"Why this matters":** one or two sentences in dollars, watts, or SLA
   terms. Who should care and what they'd do differently.

Then the body, per template. Close with what's next or what's open, not a summary.

## 3. Prose rules

- **Short paragraphs** (1–4 sentences). One idea each.
- **Concrete over abstract.** Name the model, the GPU, the flag, the number.
- **Active voice.** "vLLM batches requests," not "requests are batched."
- **Cut throat-clearing.** Delete the first sentence of most paragraphs and see
  if anything is lost.
- **Define a term once,** at first use, in plain words. Then use it consistently.
- **Vary sentence length.** Uniform medium-length sentences read as machine-made.
- **Specific verbs.** "dropped," "stalled," "saturated," not "impacted," "affected."
- **No rhetorical questions** as transitions. State the next point.
- **No lists where prose reasons better.** Use lists for steps, specs, and
  comparisons; use prose for arguments and explanations.
- **End sections on information,** not a moral or a hook.

## 4. Banned phrases (hard filter)

Remove or rewrite on sight:

- delve, tapestry, landscape (figurative), realm, embark, journey (figurative)
- "in today's fast-paced world," "in the ever-evolving world of"
- "it's important to note," "it's worth noting," "notably," "crucially"
- "game-changer," "revolutionize," "unlock," "supercharge," "seamless," "robust" (without a measured meaning)
- "leverage" as a verb, "utilize"
- "Let's dive in," "Let's break it down," "Buckle up"
- "In conclusion," "To sum up," "At the end of the day"
- "It's not just X, it's Y" constructions
- Triplet padding ("fast, efficient, and scalable") unless all three were measured
- Unattributed "studies show," "experts say," "many believe"
- Emoji in body text; exclamation points outside quotes

Also avoid: chains of em dashes, colon-driven "Here's the thing:" reveals, and
closing every section with a one-line zinger.

## 5. Numbers and units

- **SI units, with a space:** `450 W`, `1.2 kWh`, `35 ms`, `80 GB`.
- **Name the statistic:** p50, p99, mean, median. Never a bare "latency."
- **Show spread:** n runs, and a range, std dev, or CI. A single number with no
  spread is a draft, not a result.
- **Relative changes include the base:** "throughput fell 3% (from X to Y tok/s)."
- **Money has a date and source:** "$2.49/GPU-hr (Provider, on-demand, Feb 2027)."
- **Significant figures match precision.** Don't print 4 decimals from a
  noisy measurement.
- **Spell out the metric once:** "time to first token (TTFT)."

## 6. Figures and tables

- **Generated from data by a committed script.** Never hand-typed values in a chart.
- **Every chart has** a title that states the finding, labeled axes with units,
  n per point, error bars or bands, and a caption naming the hardware and run id.
- **One idea per chart.** If it needs a paragraph to decode, split it.
- **The one shareable chart:** each post has one figure that tells the whole
  story on its own (it travels on social and gets screenshotted).
- **Accessible:** colorblind-safe palette; don't rely on color alone; alt text
  that states the finding.
- **Tables for specs and comparisons;** charts for trends and frontiers.

## 7. Code and commands

- Exact commands, copy-pasteable, in fenced blocks with the language tag.
- Pin versions and commits. `pip install vllm==X.Y.Z`, not `pip install vllm`.
- Show the minimal snippet that matters; link the full script at a commit.

## 8. Footer (every post)

```
---
**Reproduce:** <link to repo at pinned commit> · **Raw data:** <link>
**Published:** YYYY-MM-DD · **Last updated:** YYYY-MM-DD · [Changelog](CHANGELOG.md)
**AI disclosure:** <honest one-liner, e.g. "Drafted with AI from my notes and
measured data; experiments, numbers, and conclusions are mine and were
verified by hand.">
**Corrections:** If something here is wrong, email ryan.j.hamby@gmail.com. I fix
errors publicly in the changelog.
```

## 9. Titles and hooks (for audience without clickbait)

- Lead with the surprising result or the sharp question, never a vague topic.
- Numbers in titles only if measured and robust.
- No "You won't believe," "Everything you know about X is wrong."
- First two sentences must make a practitioner want to keep reading: a real
  tension, a cost, or a result that contradicts common assumptions (and cite
  the assumption).

## 10. Length

- Anchor posts: 1,200–2,500 words plus figures. Longer only if every section earns it.
- Notes: 100–400 words, one finding, one chart.
- If cutting 20% loses nothing, cut 20%.

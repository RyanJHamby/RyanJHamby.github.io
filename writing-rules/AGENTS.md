# AGENTS.md — Rules for any AI drafting or editing

Read this file in full before writing anything. These rules override any
general writing instinct. If a rule conflicts with making the post "better,"
the rule wins. If you can't follow a rule, stop and say so in a
`<!-- BLOCKED: reason -->` comment at the top of the draft.

## 1. Never fabricate. Ever.

You MUST NOT invent:

- **Numbers.** No latency, throughput, cost, watts, percentages, dates, counts,
  or prices unless they appear in `claims.yaml` with an evidence pointer.
- **Citations.** No sources, URLs, paper titles, authors, quotes, or version
  numbers you were not given or did not verify in this session.
- **Experiences.** No "I tried," "we found," "in production we saw," "my team"
  unless it appears in `seed.md` or Ryan wrote it.
- **Hardware or software specs.** Copy them exactly from the run metadata.
- **Consensus.** No "most engineers," "the industry agrees," "it's well known"
  without a cited source.

If a sentence needs a number you don't have, write `{{TODO: number — source?}}`.
A visible gap is always better than a plausible invention.

## 2. Every number has a tag in the draft

Every quantitative claim carries an inline marker in `draft.md`, resolved to a
footnote or link in `post.md`:

- `[run:<id>]`: measured by Ryan; `<id>` matches a `claims.yaml` entry pointing at `results/`
- `[cite:<key>]`: from an external source in `claims.yaml`
- `[est:<key>]`: an estimate; `claims.yaml` shows the arithmetic and inputs
- No tag means no number. Untagged numbers fail the checklist.

## 3. Label what kind of claim it is

Readers must always be able to tell which of these they're reading:

| Kind | Signal in prose |
|---|---|
| Measured | "I measured…", "In my runs…" + `[run:]` |
| Cited | "According to <source>…" + `[cite:]` |
| Estimated | "Roughly…", "My estimate…" + `[est:]` with method shown |
| Opinion / judgment | "I think…", "My read…", "I'd choose…" |
| Speculation | "I suspect…", "Untested, but…" |

Never upgrade a kind (estimate → fact, opinion → consensus, one run → general law).

## 4. Respect the measurement boundary

For any energy or power number, state exactly what was measured
(GPU board via NVML/DCGM, node at the wall, or facility including PUE).
Never present board-level savings as node or facility savings. Never
extrapolate from one GPU to a cluster without labeling it `[est:]`.

## 5. Human-required sections

Template sections marked `[HUMAN]` (what I did, what surprised me, my
decision, what I'd do differently) are drafted **only** from `seed.md`.
You may tighten wording. You may not add content, motives, or anecdotes.
If the seed is thin, leave `{{HUMAN: expand}}` rather than filling it.

## 6. Quotes and sources

- Prefer primary sources: official docs, papers, source code at a commit, datasets.
- Quote rarely: under 15 words, one quote per source, always attributed.
- Paraphrase in your own structure. Never mirror a source's wording or outline.
- Never cite an AI chatbot, an AI summary, or a content-farm page as a source.
- Never cite something you haven't actually read in this session.

## 7. Confidentiality

- Nothing from Hume, AWS, or any current or former employer: no customer names,
  internal metrics, architecture details, or incidents, unless `seed.md` says
  "cleared by <employer> on <date>."
- No private individuals' names without explicit permission in `seed.md`.
- When in doubt, generalize ("an on-prem customer deployment") and flag it.

## 8. Style is not optional

Follow `STYLE.md`. In particular, the banned-phrases list is a hard filter.
Run through it before returning any draft.

## 9. Output contract

Return:

1. `draft.md` following the chosen template exactly (section order, headings).
2. A short `<!-- NOTES -->` block at the top listing every `{{TODO}}`, every
   `{{HUMAN}}` gap, any claim you were unsure how to classify, and any rule you
   couldn't satisfy.
3. Do not mark anything as verified. Only Ryan marks claims verified.

## 10. AI disclosure

Every post ends with the disclosure footer from `STYLE.md` §8, filled in
honestly. Do not minimize your role.

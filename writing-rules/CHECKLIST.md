# CHECKLIST.md — Publish gate

Every box checked or the post doesn't ship. Ryan runs this, not the AI.

## Evidence
- [ ] Every number in `post.md` has a tag that resolved to a verified `claims.yaml` entry
- [ ] Every `claims.yaml` entry has `verified_by` and `verified_on` filled
- [ ] Derived numbers recomputed by script (linked), units checked
- [ ] Every citation opened and read; locator, version, and access date present
- [ ] Archive links for web sources that a key number depends on
- [ ] Estimates labeled as estimates, with inputs shown
- [ ] No `{{TODO}}`, `{{HUMAN}}`, or `BLOCKED` markers remain

## Benchmarks (if any)
- [ ] Full Spec block present (EVIDENCE.md §4); no omitted fields
- [ ] `metadata.json` and raw data committed at the linked commit
- [ ] n runs and spread reported; differences exceed run-to-run variance
- [ ] Losing configurations shown, not just the winner
- [ ] Energy measurement boundary stated (if energy reported)
- [ ] Quality and SLA held, or the deviation clearly stated
- [ ] "What I didn't test" and threats to validity written
- [ ] Reproduce commands verified by actually running them from a clean environment

## Craft
- [ ] Title is specific and result-bearing
- [ ] TL;DR works alone and is true
- [ ] "Why this matters" in dollars, watts, or SLA terms
- [ ] `[HUMAN]` sections are genuinely mine: a decision, a surprise, or a dead end
- [ ] At least one thing in this post an AI could not have produced without me
      (my measurement, my failure, my judgment call)
- [ ] One shareable figure that tells the story alone
- [ ] Banned-phrases pass (STYLE.md §4)
- [ ] Read aloud once. Anything that sounds like a press release gets rewritten.
- [ ] Cut pass: removed at least 10% on the final edit

## Safety and integrity
- [ ] No employer-confidential content (or written clearance noted)
- [ ] No private individuals named without permission
- [ ] AI disclosure footer is honest
- [ ] Quotes: under 15 words, one per source, attributed
- [ ] Consistent with resume, site, GitHub profile, and repo READMEs (flag mismatches; don't guess)

## Ship
- [ ] Canonical on ryanjhamby.dev; Substack send; cross-posts link to canonical
- [ ] `CHANGELOG.md` created with the publish date
- [ ] Results repo tagged at the published commit

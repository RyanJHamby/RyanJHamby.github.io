# RyanJHamby.github.io: engineering journal

Dated notes on what I tried, what happened, and why I made each call, including
the dead ends. Entries are appended with `pow log` and `pow run`, so dates match
commit history. Raw outputs for any number quoted in the README live in
[`results/`](../results/).

## 2026-10-30 12:14 EDT (at fcee4d0)

Archived old site to archive/old-blog (pushed). Restructured to Writing/Projects/About; kept all 3 old posts, moved content/blog to content/writing with /blog/ aliases. Added static/CNAME + baseURL for ryanjhamby.dev on branch agent/new-site-structure; deliberately NOT merged to main until domain is verified on GitHub. hugo --minify builds clean; live DNS/HTTPS/email not verified (dashboard steps are Ryan's).

## 2026-10-30 12:44 EDT (at fa7b9ad)

Merged origin/main (AI-compute repositioning, resume PDF) into agent/new-site-structure; conflicts in hugo.toml, about.md, _index.md resolved by keeping main's copy and my structure. This also resolved the home-vs-About positioning mismatch. hugo --minify builds clean.

## 2026-10-30 12:56 EDT (at 2207a79)

Switched public contact from hi@ryanjhamby.dev back to ryan.j.hamby@gmail.com. Reason: most inbound/outbound will be automated agents, so gmail deliverability and consistency with resume/profile README matter more than a vanity address on a new domain with no sending reputation. Domain stays for site/Substack.

## 2026-10-30 13:11 EDT (at b42aa22)

Audited site vs repos. GPU Flight Recorder repo has 7 commits (Mar 24-27 2026), no simulator and no results/, so the 30/30 and 0/30 detection figures were removed; section now says early build. Macro backtest is 17 years per repo README (site said 18), tests 240+ (242 counted), dates per first/last commit. Dropped uncaptured Java4Java metrics (installs, retention, consistency, fill rate). Screener/macro figures kept but labelled README-sourced, not captured. Job title unified to Software Development Engineer II. Resume untouched.

## 2026-10-30 13:16 EDT (at 86d01a4)

Site redesign: replaced two stylesheets (965 + 747 lines) with one system-font stylesheet, one accent, light+dark; removed the localStorage views/likes widget (per-visitor fake social proof); home rewritten around selected work; emoji and light-only inline styles removed. Verified: hugo --minify builds; Chrome screenshots of home, projects at desktop and 390px. Not verified: dark mode rendering (headless could not set the theme), deployed site.

## 2026-10-30 13:22 EDT (at 81cf83d)

Split the 300-line projects page into an index plus one page per project (GPU Flight Recorder, FlowState, order book, screener, macro). Old #anchors on /projects/ now land on the index; only the home page linked to them and was updated. Order book page now says its figures are README-sourced, not captured.

## 2026-10-30 13:31 EDT (at 8d2bf02)

Discoverability pass: descriptions on posts/pages, og:image card, PaperMod publisherType=Person (removed my duplicate JSON-LD after finding PaperMod already emits it), llms.txt, hobby projects reordered with an Earlier section, drillpad page added as draft=true (not built). Not verified: indexing, link previews in LinkedIn/Substack, deployed site.

## 2026-10-30 13:40 EDT (at 3ce1f30)

Deploy of PR #7 failed in CI: I inserted [params.schema] directly after [params], which moved author, description, keywords, defaultTheme and the Show* options under params.schema. Hugo 0.154 (local) tolerated it; CI's latest Hugo (0.169) failed in PaperMod rss.xml (site.Author). My earlier verification only checked og:image and the schema block. Fix: schema table moved after the scalar params. Lesson: after editing TOML, check the keys that used to follow the insertion point, and check the CI build, not only the local one.

## 2026-10-30 14:14 EDT (at 6b038fb)

Drafted the FlowState dead-end post in drafts/flowstate-asof-join (not under content/, so not built). Numbers come from FlowState results/2026-10-30-1412-asof-join-spread @ fdc202b (10 runs, min/max, Apple M4). FlowState is 1.34x Polars' median at 1M rows and 1.44x at 10M, ranges do not overlap, derived by derive.py. HUMAN sections left empty: seed.md has to come from Ryan. Lint passes except the intentional HUMAN/TODO blockers. First draft of mine broke AGENTS.md by stating an expectation not in any seed and an opinion; caught on re-read and removed. Added a predates-the-standard note to the three older posts. Substack embed not done: publication subdomain unknown.

## 2026-10-30 14:17 EDT (at 3cfe872)

FlowState post: added the figure (figure.py from output.log) and verified the reproduce commands from a clean clone at fdc202b. First clean attempt failed because uv picked a free-threaded CPython 3.14.7 that has no Polars 1.38.1 wheel; pinning the regular 3.14.3 fixed it. Clean rerun kept the ordering (Polars slowest run faster than FlowState fastest, both sizes), about 1.5 min end to end. The rerun was not a pow capture, so its timings are not quoted. Installed kernel in the original capture verified byte-identical to the release build, built before the capture; only packaging metadata changed after.

## 2026-10-30 14:19 EDT (at 6dcc001)

FlowState post: Ryan asked me to write the seed. I did not invent beliefs; I assembled seed.md only from text he wrote in the FlowState repo (README at 3c7486a, DESIGN.md 3.2, journal 2026-10-04), with sources per line and the unwritten parts left as gaps. That surfaced the real story: a March README table claimed 1.8x over Polars with no captured run; the reproducible run in October reversed it. DESIGN.md 3.2 still says 'Why we outperform Polars' and conflicts with the README: flagged, not changed. Post TL;DR rewritten around the retracted claim; four HUMAN gaps remain.

## 2026-10-30 14:24 EDT (at 7f70409)

Prepared the FlowState post for publication: build_post.py generates content/writing/flowstate-asof-join from draft.md and claims.yaml (evidence tags become footnotes, 17 of them). Gaps resolved by stating what is not known, not by inventing: 'why Polars is faster' is 'I don't know'; expectation and 'could this work elsewhere' dropped; open question taken from the journal's own unverified suspicion. Dates set to 2026-10-30. claims.yaml verified_by/verified_on still empty and CHECKLIST.md not run, so the PR is a draft PR.

## 2026-10-30 14:50 EDT (at 33bc4e4)

Withdrew the FlowState as-of join post (draft = true) pending a fair rerun: the harness had not shown equal work, the wrapper overhead was inside the timed region, and it ran on a laptop only. The changelog in the post records the withdrawal.

## 2026-10-30 16:42 EDT (at 82aac77)

Set up the writing system in the site repo: copied STYLE, CONTENT, AGENTS, CHECKLIST, templates and lint.py unchanged (baseline commit), then made three edits: AWS and former employers named in the confidentiality rule (Hume-only wording before), gmail in the corrections footer (hi@ before). Added tools/new_post.py (scaffold, tested in a scratch copy: creates the folder, refuses overwrite, rejects bad slugs, lint runs on the fresh template) and writing-rules/backlog.md seeded only from evidence in repos. tokenomics-bench is the strongest anchor: pre-registered, hardware runs not yet performed.

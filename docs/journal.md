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

## 2026-10-30 17:04 EDT (at 9e69d03)

Feed fix: the home RSS feed listed every page (About, Contact, project pages) with 0001 dates because the theme feeds site.RegularPages. Added layouts/index.xml to list only the writing section, newest first, with the home description as the channel description. Verified on a clean build: 3 items, no 0001 dates, XML well-formed. Not verified in a feed reader or W3C validator.

## 2026-10-30 17:20 EDT (at 4d2d06d)

RSS links: post and other non-home pages had no feed discovery link (only the home page did), a stray /projects/index.xml feed was published, and the feed's channel image linked to the PNG. Added a site-wide discovery link (titled with the site name, not the theme's generic 'rss'), turned off the projects feed, pointed the image link at the site. Verified on a clean build; not tested in a feed reader.

## 2026-10-30 17:41 EDT (at e01e922)

CORRECTION of my own error. I audited repos from local clones without running git fetch. The GPU Flight Recorder clone was 23 commits behind origin/main (7 vs 30 commits, last commit 2026-09-21), so I wrongly told Ryan the repo had no simulator, no results and no support for the 30/30 figures, and I rewrote the site page as 'early build, no validation results' and removed the numbers. The real repo has a seeded simulator, a scorecard, a README results table (30/30, 0 false stragglers, explicitly synthetic) and a real-GPU runbook that was never run. The stock-screener clone was 130 commits behind (active through 2026-10-30), so 'Nov 2025 - May 2026' on the site was wrong; now 'Present'. Fixed in this branch: GPU page, home, llms.txt, backlog, screener date. Macro: the cleaned README is on a non-default branch (last commit 2026-05-31) while main ends 2026-03-03; flagged, not changed. Rule going forward: git fetch and compare to origin/main before any audit. The 'Reproduce/withdraw' decisions for the FlowState post did not depend on this.

## 2026-10-31 11:40 EDT (at e01e922)

Added a browser tab icon: RH monogram on the site accent blue (static/favicon.svg, ico, 32px png, full-bleed apple-touch icon). PaperMod already emitted icon links to files that did not exist (favicon-16x16.png, safari-pinned-tab.svg), so I pointed params.assets at the real files instead of adding duplicates; [params.assets] sits after the scalar params. Verified: clean hugo build, one set of icon links in the built home page, preview of the 180px render. Not verified: rendering in Safari/Firefox tabs or iOS home screen, and the deployed site.

## 2026-10-31 11:41 EDT (at e01e922)

Wrote 2 site specs (site-integrity-check, build-post-tool) with strict-xfail tests. Dropped the llms.txt generator spec: PR #15 edits static/llms.txt. Found a real defect while proving the check: /writing/ has two RSS links and a duplicate /writing/index.xml feed; spec makes the agent fix it via hugo.toml section outputs. build-post --publish requires verified claims; draft=true by default.

## 2026-10-31 17:05 EDT (at f7e3e10)

Math rendering and a mobile audit. Math is rendered at build time by Hugo (passthrough + transform.ToMath, KaTeX), so pages ship no JS; the KaTeX stylesheet (katex@0.16.11, jsDelivr) loads only on pages that contain math. Inline is `\( ... \)`, display is `$$ ... $$` or `\[ ... \]`. Single-$ inline is off on purpose: STYLE.md writes prices like $2.49/GPU-hr and they would parse as equations. Verified: clean build of a throwaway test page (1 inline, 2 display equations, no katex-error, price left as text); desktop and 390 px renders checked by eye. Mobile audit: 10 pages at 390 px, none overflow horizontally. My first audit reported overflow on two posts; that was my error (the pages were loaded without their CSS), caught by re-running over HTTP. Not verified: dark mode, Safari/Firefox, iOS, the KaTeX CSS from the CDN on the deployed site, and the Hugo version in CI (latest) rather than local 0.154. Wide equations scroll inside their box with no visual hint.

## 2026-10-31 17:40 EDT (at f7e3e10)

Home page: added a dated "Merged upstream" section (vLLM #48420, Firecracker #6032 and #6033 merged; vLLM #57722 open) and removed the vague "vLLM and Firecracker" line from Selected work. Dates and states come from `gh search prs --author RyanJHamby` on 2026-10-31, not from memory. The open PR was missing from the Projects page and is now listed there, labeled open. Verified: clean build, desktop screenshot. Not verified: mobile layout of the new section, dark mode, deployed site. The merged-PR dates will go stale if a state changes, so re-check the list when a new PR merges.

## 2026-10-31 18:05 EDT (at e2e9bab)

Qwen3-Omni post built as a draft page (draft = true, not in the default build or the feed). Checked the public record before writing: the maintainer's inline review comment (prefers a ValueError over a silent fallback) and the commit authors. f25d0ca (raise in the Qwen3 class) and 2d8f7ee (the false-positive fix) are Ryan's; 7166e20, which added the guard to the shared Qwen2.5-Omni parent class where CI failed, is the maintainer's. My earlier drafts said "my guard", which was wrong; corrected in the text and the figure title. Attribution of work, per Ryan: reproduction, first fix and CI investigation are his; the AI traced the root cause (confirmed by Ryan) and wrote the second fix (reviewed and tested by Ryan). The two opinion sections ("Why it failed", "What I'd do instead") were written by the AI at Ryan's direction and must be read and owned by him before publishing. Not verified: CI failure details and the 6 passing tests (PR thread only), dark mode and mobile of this page, anything on the deployed site.

## 2026-10-31 18:20 EDT (at 8a79aed)

Verification pass on the Qwen3-Omni draft. Rerun from a fresh venv with the post's exact commands (transformers 5.22.1, numpy 2.5.4, torch 2.15.0): same StopIteration at line 249, False succeeds. Re-checked against GitHub: 3 files, 57 additions, 1 deletion; line 247 and the (16, 3, 480, 256) shape; "all 6 pass" is in the author's comment; commit authors and the 7166e20 diff. Found and fixed: one mismatched citation (the PR-body argument cited the commit-sequence claim; added pr_body_fallback). Found and fixed: the figure was 880 px wide and its text rendered at about 5 px on a phone; redrawn as a 440 px stacked figure. Checked: no horizontal overflow at 390 px, dark mode text renders. Not checked: the figure's light background against dark mode, Safari/iOS, the deployed page. Still not verified by anyone: the CI failure details and the 6 passing tests, which come only from the PR thread.

## 2026-10-31 18:40 EDT (at e2e9bab)

Raw LaTeX showed on the macro page ("spectral decomposition (\(\Sigma = U \Lambda U^{\top}\))"). Cause: that line sat inside a raw `<div class="achievement">` block, where Markdown and the math passthrough are not processed. Fix: blank lines after the opening tag and before the closing tag so the content is parsed as Markdown. I missed it in the earlier check, which counted KaTeX nodes (8) but never searched the built pages for leftover raw delimiters. Verified: 9 KaTeX nodes on the page, no katex-error, and no raw `\(`, `\[` or `$$` in any built page; screenshot checked. Not verified: other raw HTML blocks that may later hold math (the same trap applies to any future formula inside a div).

## 2026-10-31 19:00 EDT (at cddc1f1)

Qwen3-Omni post flipped to published (draft = false) in PR #27 at Ryan's request, so merging the PR is the publish step. Checked on a clean build: the post appears on the Writing index, the home Writing list, the RSS feed (4 items) and the sitemap. Replaced the footer link to a CHANGELOG.md that would not exist on the live page with an in-page Changelog section. NOT done by me and still open: Ryan's CHECKLIST sign-off (verified_by / verified_on in claims.yaml are blank, so the claims are unverified by the owner), his read of the two opinion sections written by the AI at his direction, and his own rerun of repro.py. Publishing before those is his call.

## 2026-10-31 19:30 EDT (at ddf36d6)

Share buttons trimmed to LinkedIn, X, Reddit and Hacker News (theme keys: linkedin, twitter, reddit, ycombinator; "hackernews" and "x" are not valid keys and render nothing). Tag display fixed for vLLM, Build log and Qwen3-Omni via term pages (the theme title-cased "vllm" to "Vllm"). Added opt-in GoatCounter: `goatcounter = ""` in hugo.toml params; empty means no script and no footer note; set to a site code it adds the script (skipped under `hugo server`) and a footer line saying page counts are anonymous with no cookies. Verified on clean builds: unset renders neither, set renders both, share targets and tag labels as listed. Not verified: that GoatCounter receives hits (no account exists yet; Ryan creates it), mobile layout of the footer note. Metrics to review weekly are in the chat from 2026-10-31: referrers, subscriber conversion, Search Console queries, a manual inbound log, GitHub signals.

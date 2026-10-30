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

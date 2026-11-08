---
id: site-integrity-check
goal: A single command checks a built copy of the site for the failures that already happened once (non-post or 0001-dated RSS items, missing or duplicate feed links, draft pages leaking into output or sitemap, pages without a description, a dead llms.txt link), and the real site passes it.
acceptance:
  - python -m pytest tests/test_check_site.py --runxfail -q
  - python -m pytest tests/test_check_site.py -q
scope:
  - tools/check_site.py
  - tests/test_check_site.py
  - hugo.toml
  - layouts/index.xml
  - layouts/partials/extend_head.html
non_goals:
  - do not change any assertion in the test file; only delete the `XFAIL` constant and the `@XFAIL` decorator lines (the second acceptance command fails while the strict xfail marker remains and the work is done)
  - do not touch anything under content/, static/ (including static/llms.txt), drafts/, writing-rules/, tools/lint.py or tools/new_post.py
  - do not edit .github/, AGENTS.md or CLAUDE.md, and do not add a CI workflow (the owner wires it in later)
  - no new dependencies: the checker uses only the Python standard library (html.parser, xml.etree, re, tomllib, pathlib)
  - do not fetch URLs; every check reads files on disk
risk_tier: 2
max_runs: 3
autonomy: inherit
status: ready
issue: 18
---

## Why
The site has already shipped, and then fixed by hand, a feed that listed every page with `0001` dates (PRs 12-14) and
pages with no feed discovery link. Nothing checks for these, or for a draft leaking into the build. The FlowState post is
withdrawn with `draft = true`; a stray flip would publish it silently. This spec makes those checks a script.

## What to build: `tools/check_site.py`
`python3 tools/check_site.py <public_dir> --root <repo_root>`, where `<public_dir>` is the output of
`hugo --minify -d <dir>`. Prints one line per problem in the form `FAIL <rule>: <detail>`, then `OK` if there were none.
Exit 0 with no problems, 1 with any, never a traceback for a problem it is meant to detect. Rules (the test asserts the
rule names, so use them exactly):

- `feed-items`: `<public>/index.xml` must have at least one `<item>`, and the set of item `<link>`s must equal the set of
  published posts: every non-draft regular page under `content/writing/` (not `_index.md`), at
  `https://ryanjhamby.dev/writing/<slug>/`. Posts are `<slug>.md` or `<slug>/index.md`. Read `draft` from the front matter,
  which is TOML (`+++`) in every file today; YAML (`---`) support is optional.
- `feed-dates`: no `<pubDate>` contains `0001`.
- `rss-link`: every page Hugo generated has exactly one `<link rel="alternate" type="application/rss+xml">`, and its href
  path is `/index.xml`. Skip redirect pages (`<meta http-equiv=refresh>`: aliases and `page/1/`) and any HTML file whose
  relative path also exists under `<root>/static/` (the swolverine pages). Parse with `html.parser`; minified output has
  unquoted attributes, so do not regex on quotes.
- `description`: the same pages must have a non-empty `<meta name="description" content="...">`.
- `draft-leak`: for every `draft = true` page under `content/`, its URL path (`projects/drillpad`, `writing/flowstate-asof-join`)
  must not exist under `<public>` and must not appear in `sitemap.xml`.
- `llms-link`: `<public>/llms.txt` must exist, and every `https://ryanjhamby.dev/...` URL in it must resolve to a file or a
  directory with `index.html` under `<public>`. External links are ignored.

## Known failure the real site has today (you must fix it)
`/writing/index.html` carries TWO feed links: the site-wide `/index.xml` (from `layouts/partials/extend_head.html`) and the
theme's `/writing/index.xml`, because `hugo.toml` only restricts the `home`, `taxonomy` and `term` outputs. A second feed
file, `/writing/index.xml`, is also built. Fix it by adding `section = ["HTML"]` under `[outputs]` in `hugo.toml` (verified in a
throwaway run to make the real site pass; Hugo 0.154.4 locally, CI uses latest). Do not change what `index.xml` contains.

## Hard facts
- The test builds the real site with `hugo --minify -d <tmp>` once, runs the checker on it, and on broken copies. Hugo must
  be on PATH. A clean build takes about 0.3 s.
- Today's published posts: 3 (`cache-eviction-improvements`, `kubernetes-second-act-ai-backbone`,
  `optical-cables-multicast-performance`). Drafts: `content/projects/drillpad.md`, `content/writing/flowstate-asof-join/`. Derive both
  lists from `content/`; never hardcode them in the script.
- Open PR #15 edits `static/llms.txt` and `content/`; do not touch them. The `llms-link` rule must work with whatever
  `static/llms.txt` contains.
- After the work, `hugo --minify` must still build with no warnings, and the only output change allowed is that
  `writing/index.xml` disappears and `writing/index.html` loses its second feed link.

## Log
- 2026-10-31 draft; throwaway reference run: 11 of 11 tests pass with a ~60-line checker plus the one-line hugo.toml fix, then deleted.
- 2026-10-31 ready, issue #18 (handshake was provisional; repo not yet onboarded with ap init; waiting for the owner's agent-ready label)

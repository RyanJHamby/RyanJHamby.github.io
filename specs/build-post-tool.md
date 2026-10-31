---
id: build-post-tool
goal: tools/build_post.py turns any drafts/<slug>/draft.md plus claims.yaml into a Hugo page bundle, refusing on unresolved markers, unknown tags, a missing description, or (with --publish) unverified claims.
acceptance:
  - python -m pytest tests/test_build_post.py --runxfail -q
  - python -m pytest tests/test_build_post.py -q
scope:
  - tools/build_post.py
  - tests/test_build_post.py
non_goals:
  - do not change any assertion in the test file; only delete the `XFAIL` constant and the `@XFAIL` decorator lines (the second acceptance command fails while the strict xfail marker remains and the work is done)
  - do not touch anything under content/ or drafts/ (leave drafts/flowstate-asof-join/build_post.py where it is; removing it is a later decision)
  - do not edit tools/lint.py, tools/new_post.py or anything in writing-rules/
  - no new dependencies: standard library only, no PyYAML (parse claims.yaml with regex like the existing script)
  - the tool writes only to the output directory it is given; it never writes under content/ itself
risk_tier: 1
max_runs: 3
autonomy: inherit
status: ready
issue: 19
---

## Why
`drafts/flowstate-asof-join/build_post.py` is the only builder and is hardcoded to one post (description, tags and
figure name are literals). Publishing is where a fabricated or unverified number would leave the repo, so the builder's
refusals need tests, not trust. The generalized tool must be a straight move of the existing logic, plus the changes below.

## What to build: `tools/build_post.py`
`python3 tools/build_post.py <draft.md> <claims.yaml> <out_dir> [--publish]`. Start from
`drafts/flowstate-asof-join/build_post.py` (50 lines) and keep its behaviour:
- Evidence tags `[run:key]`, `[cite:key]`, `[est:key]` become footnote references `[^key]` (the whitespace before the tag is
  removed), numbered by first use; each used claim becomes `[^key]: <claim> Source: <evidence>.` at the end. Unused claims
  are not emitted.
- The `<!-- ... -->` NOTES comment is removed, and the ` [HUMAN]` label on headings is removed.
- Refuse (non-zero exit, message on stderr, nothing written) if `{{TODO`, `{{HUMAN` or `BLOCKED` appears outside HTML
  comments. The message contains the word "marker".
- Refuse if a tag's key is not in claims.yaml; the message contains the key.

Changes from the original:
- `description` and `tags` come from the draft's front matter (`description: "..."`, `tags: [a, b]`) instead of literals.
  A missing description is an error whose message contains "description". Output front matter is TOML:
  `title`, `date`, `description`, `tags`, `draft`.
- `draft = true` by default. `--publish` writes `draft = false` AND first requires that every claim actually used in the
  body has non-empty `verified_by` and `verified_on`; otherwise it refuses with a message containing "verified" and the
  offending keys. Unused claims are not checked. (AGENTS.md rule: only Ryan marks claims verified.)
- Copy every `.png`, `.svg` and `.jpg` next to draft.md into the output directory (the original copies only `figure.png`).
  Never copy `seed.md`, `claims.yaml` or the draft.

## Hard facts
- Verified in a throwaway run: running the original logic on a copy of `drafts/flowstate-asof-join` (with a description line
  added) yields a body identical to `content/writing/flowstate-asof-join/index.md` after the front matter. Keep that parity;
  it is the regression check you cannot see in the tests.
- The test fixtures are written into pytest's `tmp_path`; the tests never read `content/` or `drafts/`.
- `claims.yaml` entries look like `- key: x` followed by indented `kind`, `claim`, `evidence`, `verified_by`, `verified_on`
  lines (see `tools/new_post.py` `CLAIMS_HEADER`). `verified_by:` with no value counts as empty.
- Tests run from the repo root: `python -m pytest tests/test_build_post.py`. pytest comes from `requirements-dev.txt`.

## Log
- 2026-10-31 draft; throwaway reference run: 8 of 8 tests pass with a ~35-line generalization, then deleted.
- 2026-10-31 ready, issue #19 (handshake was provisional; repo not yet onboarded with ap init; waiting for the owner's agent-ready label)

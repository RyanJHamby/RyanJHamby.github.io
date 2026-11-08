# Writing system

Rules for any post on ryanjhamby.dev, written by hand or with AI. They override general writing instinct.

| File | Purpose |
|---|---|
| `STYLE.md` | Voice, structure, banned phrases, numbers and figures, footer |
| `CONTENT.md` | What to write, pillars, post types, what every post carries over time |
| `AGENTS.md` | Rules for any AI drafting or editing (never fabricate, tag every number, human sections come from `seed.md`) |
| `CHECKLIST.md` | The publish gate. You run it, not an AI |
| `templates/` | Benchmark, dead-end and note templates, `seed.md`, changelog |
| `backlog.md` | Candidate posts with their evidence and status |
| `../tools/lint.py` | Deterministic pre-publish lint (banned phrases, untagged numbers, markers, disclosure) |
| `../tools/new_post.py` | Scaffold `drafts/<slug>/` from a template |

## Flow
1. Pick an entry from `backlog.md` whose evidence exists.
2. `python3 tools/new_post.py <slug> --type benchmark|dead-end|note`
3. Fill `drafts/<slug>/seed.md` yourself. The `[HUMAN]` sections come only from it.
4. Draft with AI if you like, tagging every number `[run:]`, `[cite:]` or `[est:]` and adding it to `claims.yaml`.
5. `python3 tools/lint.py drafts/<slug>/draft.md drafts/<slug>/claims.yaml` until clean.
6. Run `CHECKLIST.md`; fill `verified_by` and `verified_on` yourself.
7. Build the page (for a post generated from a draft, see `drafts/flowstate-asof-join/build_post.py` as a worked example), merge, then send via Substack with the canonical link.

Nothing under `drafts/` or `writing-rules/` is built by Hugo; only `content/` is published.

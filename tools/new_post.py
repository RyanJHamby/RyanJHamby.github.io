#!/usr/bin/env python3
"""Scaffold a new post folder from the templates.

Usage: python3 tools/new_post.py <slug> --type benchmark|dead-end|note [--root .]

Creates drafts/<slug>/ with draft.md (from the template), an empty seed.md, and a claims.yaml
header. Writes nothing under content/, so nothing is built or published. Refuses to overwrite.
Next steps are printed; the rules live in writing-rules/.
"""
import argparse
import datetime
import re
import sys
from pathlib import Path

TEMPLATES = {"benchmark": "benchmark-post.md", "dead-end": "dead-end.md", "note": "note.md"}
CLAIMS_HEADER = """# Evidence for draft.md. Every tagged number needs an entry here.
# verified_by / verified_on are filled by Ryan only.
# - key: <short_name>
#   kind: run | cite | est
#   claim: "<the exact claim, with units>"
#   evidence: "<results path @ commit, URL + access date, or arithmetic and inputs>"
#   verified_by:
#   verified_on:
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("slug")
    ap.add_argument("--type", required=True, choices=sorted(TEMPLATES))
    ap.add_argument("--root", default=".")
    args = ap.parse_args()
    if not re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", args.slug):
        sys.exit("slug must be lowercase words joined by hyphens")
    root = Path(args.root)
    out = root / "drafts" / args.slug
    if out.exists():
        sys.exit(f"{out} already exists; not overwriting")
    template = root / "writing-rules" / "templates" / TEMPLATES[args.type]
    seed = root / "writing-rules" / "templates" / "seed.md"
    text = template.read_text().replace("YYYY-MM-DD", datetime.date.today().isoformat(), 1)
    out.mkdir(parents=True)
    (out / "draft.md").write_text(text)
    (out / "seed.md").write_text(seed.read_text())
    (out / "claims.yaml").write_text(CLAIMS_HEADER)
    print(f"created {out}/ (draft.md, seed.md, claims.yaml)")
    print("1. Fill seed.md yourself: the [HUMAN] sections come only from it.")
    print("2. Tag every number in draft.md as [run:key], [cite:key] or [est:key]; add each to claims.yaml.")
    print(f"3. python3 tools/lint.py drafts/{args.slug}/draft.md drafts/{args.slug}/claims.yaml")
    print("4. Run writing-rules/CHECKLIST.md. Only you mark claims verified.")
    return 0


if __name__ == "__main__":
    sys.exit(main())

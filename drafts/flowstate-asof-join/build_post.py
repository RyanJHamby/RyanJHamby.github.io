#!/usr/bin/env python3
"""Turn draft.md + claims.yaml into a Hugo page bundle.

Usage: python3 -I build_post.py <draft.md> <claims.yaml> <out_dir>
Evidence tags [run:key] / [cite:key] / [est:key] become footnotes; the NOTES comment and
[HUMAN] heading labels are removed; front matter becomes TOML. Refuses to run if a
{{TODO}}, {{HUMAN}} or BLOCKED marker remains.
"""
import re
import shutil
import sys
from pathlib import Path

draft, claims_path, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])
text = draft.read_text()
if re.search(r"\{\{(TODO|HUMAN)|BLOCKED", re.sub(r"<!--.*?-->", "", text, flags=re.S)):
    sys.exit("unresolved markers remain")
claims = {}
for block in re.split(r"\n(?=- key:)", claims_path.read_text()):
    k = re.match(r"- key: (\S+)", block)
    if not k:
        continue
    c = re.search(r"claim: \"(.*?)\"\n", block, re.S)
    e = re.search(r"evidence: \"(.*?)\"\n", block, re.S)
    claims[k.group(1)] = (c.group(1), e.group(1))
fm, body = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S).groups()
meta = dict(re.findall(r"^(\w+): (.*)$", fm, re.M))
body = re.sub(r"<!--.*?-->\n?", "", body, flags=re.S)
body = re.sub(r"  \[HUMAN\]", "", body)
order = []


def sub(m):
    key = m.group(2)
    if key not in claims:
        sys.exit(f"tag {key} not in claims.yaml")
    if key not in order:
        order.append(key)
    return f"[^{key}]"


body = re.sub(r"\s?\[(run|cite|est):([A-Za-z0-9_\-]+)\]", lambda m: sub(m), body)
notes = "\n".join(f"[^{k}]: {claims[k][0]} Source: {claims[k][1]}." for k in order)
title = meta["title"].strip('"')
desc = "A Rust as-of join I claimed was faster than Polars. A reproducible benchmark showed the opposite, and a rebuild of the March kernel did not bring the lead back."
out.mkdir(parents=True, exist_ok=True)
(out / "index.md").write_text(
    f'+++\ntitle = "{title}"\ndate = {meta["date"]}\ndescription = "{desc}"\ntags = ["rust", "arrow", "performance"]\ndraft = false\n+++\n\n{body.strip()}\n\n{notes}\n')
shutil.copy(draft.parent / "figure.png", out / "figure.png")
print("wrote", out / "index.md", "with", len(order), "footnotes")

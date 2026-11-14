#!/usr/bin/env python3
"""Turn draft.md + claims.yaml into a Hugo page bundle.

Usage: python3 -I build_post.py <draft.md> <claims.yaml> <out_dir> [--publish]

Evidence tags [run:key] / [cite:key] / [est:key] become footnotes; the NOTES comment and
[HUMAN] heading labels are removed; front matter becomes TOML. Refuses to run if a
{{TODO}}, {{HUMAN}} or BLOCKED marker remains outside comments.

Without --publish the page is written with draft = true, so Hugo does not build it.
With --publish it refuses unless every claim the post cites has verified_by and
verified_on filled in (only Ryan fills those), and then writes draft = false.
"""
import re
import shutil
import sys
from pathlib import Path

args = [a for a in sys.argv[1:] if a != "--publish"]
publish = "--publish" in sys.argv[1:]
if len(args) != 3:
    sys.exit(__doc__)
draft, claims_path, out = Path(args[0]), Path(args[1]), Path(args[2])

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
    vb = re.search(r"^  verified_by:[ \t]*(.*)$", block, re.M)
    vo = re.search(r"^  verified_on:[ \t]*(.*)$", block, re.M)
    claims[k.group(1)] = (
        c.group(1), e.group(1), bool(vb and vb.group(1).strip()), bool(vo and vo.group(1).strip()))

fm, body = re.match(r"---\n(.*?)\n---\n(.*)", text, re.S).groups()
meta = dict(re.findall(r"^(\w+): (.*)$", fm, re.M))
for field in ("title", "date", "description", "tags"):
    if field not in meta:
        sys.exit(f"front matter is missing {field}")
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


body = re.sub(r"\s?\[(run|cite|est):([A-Za-z0-9_\-]+)\]", sub, body)
unverified = [k for k in order if not (claims[k][2] and claims[k][3])]
if publish and unverified:
    sys.exit("refusing to publish; these cited claims are not verified by Ryan: " + ", ".join(unverified))

notes = "\n".join(f"[^{k}]: {claims[k][0]}. Source: {claims[k][1]}." for k in order)
tags = ", ".join(f'"{t.strip()}"' for t in meta["tags"].strip("[]").split(","))
title = meta["title"].strip('"')
desc = meta["description"].strip('"').replace('\\"', '"')
draft_flag = "false" if publish else "true"
out.mkdir(parents=True, exist_ok=True)
(out / "index.md").write_text(
    f'+++\ntitle = "{title}"\ndate = {meta["date"]}\ndescription = "{desc}"\ntags = [{tags}]\ndraft = {draft_flag}\n+++\n\n{body.strip()}\n\n{notes}\n')
shutil.copy(draft.parent / "figure.png", out / "figure.png")
print(f"wrote {out / 'index.md'} with {len(order)} footnotes, draft = {draft_flag}; unverified: {len(unverified)}")

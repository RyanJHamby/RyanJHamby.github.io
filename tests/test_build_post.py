"""Spec build-post-tool: tools/build_post.py turns draft.md + claims.yaml into a Hugo page bundle.

All fixtures are written into tmp_path. Nothing under content/ or drafts/ is read or written.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

XFAIL = pytest.mark.xfail(
    strict=True, reason="spec:build-post-tool (remove this marker when implemented)"
)
REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "tools" / "build_post.py"

DRAFT = """---
title: "Fixture post"
date: 2026-10-30
description: "A fixture description."
tags: [rust, arrow]
type: note
---

<!-- NOTES
{{TODO: a marker inside an HTML comment must not block the build}} BLOCKED
-->

## Heading  [HUMAN]

Polars took 9.9 ms [run:a_key] and pandas 80 ms [cite:b_key]. Again [run:a_key].
{extra}
"""

CLAIMS = """# header comment
- key: a_key
  kind: run
  claim: "Polars median 9.9 ms (10 runs)"
  evidence: "results/x/output.log"
  verified_by: {va}
  verified_on: {va_on}
- key: b_key
  kind: cite
  claim: "pandas median 80 ms"
  evidence: "https://example.com, accessed 2026-10-30"
  verified_by: {vb}
  verified_on: {vb_on}
- key: unused_key
  kind: est
  claim: "never referenced"
  evidence: "arithmetic"
  verified_by:
  verified_on:
"""


def make(tmp_path, extra="", draft=None, va="Ryan", vb="Ryan") -> tuple[Path, Path, Path]:
    d = tmp_path / "draft"
    d.mkdir()
    (d / "draft.md").write_text((draft or DRAFT).replace("{extra}", extra))
    (d / "claims.yaml").write_text(
        CLAIMS.format(
            va=va, va_on="2026-10-30" if va else "", vb=vb, vb_on="2026-10-30" if vb else ""
        )
    )
    (d / "figure.png").write_bytes(b"\x89PNG fixture bytes")
    (d / "seed.md").write_text("private seed, must not be copied")
    return d / "draft.md", d / "claims.yaml", tmp_path / "bundle"


def build(draft, claims, out, *flags):
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(draft), str(claims), str(out), *flags],
        capture_output=True,
        text=True,
    )


@XFAIL
def test_builds_bundle_with_footnotes_and_toml_front_matter(tmp_path):
    draft, claims, out = make(tmp_path)
    done = build(draft, claims, out)
    assert done.returncode == 0, done.stdout + done.stderr
    text = (out / "index.md").read_text()
    front, _, body = text.removeprefix("+++\n").partition("\n+++\n")
    assert 'title = "Fixture post"' in front
    assert "date = 2026-10-30" in front
    assert 'description = "A fixture description."' in front
    assert 'tags = ["rust", "arrow"]' in front
    assert "draft = true" in front  # default is a draft; publishing is a separate flag
    assert "NOTES" not in body and "[HUMAN]" not in body and "[run:" not in body and "[cite:" not in body
    assert "9.9 ms[^a_key] and pandas 80 ms[^b_key]. Again[^a_key]." in body
    assert body.count("[^a_key]:") == 1 and body.count("[^b_key]:") == 1
    assert body.index("[^a_key]:") < body.index("[^b_key]:")
    assert "[^a_key]: Polars median 9.9 ms (10 runs) Source: results/x/output.log." in body
    assert "unused_key" not in body
    assert (out / "figure.png").read_bytes() == b"\x89PNG fixture bytes"
    assert not (out / "seed.md").exists() and not (out / "claims.yaml").exists()


@pytest.mark.parametrize("marker", ["{{TODO: finish}}", "{{HUMAN: seed}}", "BLOCKED on a run"])
@XFAIL
def test_refuses_unresolved_marker_in_prose(tmp_path, marker):
    draft, claims, out = make(tmp_path, extra=marker)
    done = build(draft, claims, out)
    assert done.returncode != 0
    assert "marker" in (done.stdout + done.stderr).lower()
    assert not (out / "index.md").exists()


@XFAIL
def test_errors_on_tag_missing_from_claims(tmp_path):
    draft, claims, out = make(tmp_path, extra="Also this [run:ghost_key].")
    done = build(draft, claims, out)
    assert done.returncode != 0
    assert "ghost_key" in (done.stdout + done.stderr)
    assert not (out / "index.md").exists()


@XFAIL
def test_errors_when_description_missing(tmp_path):
    no_desc = DRAFT.replace('description: "A fixture description."\n', "")
    draft, claims, out = make(tmp_path, draft=no_desc)
    done = build(draft, claims, out)
    assert done.returncode != 0
    assert "description" in (done.stdout + done.stderr).lower()
    assert not (out / "index.md").exists()


@XFAIL
def test_publish_requires_every_used_claim_verified(tmp_path):
    draft, claims, out = make(tmp_path, vb="")  # b_key is used and unverified; unused_key is unverified too
    done = build(draft, claims, out, "--publish")
    assert done.returncode != 0
    msg = done.stdout + done.stderr
    assert "verified" in msg.lower() and "b_key" in msg
    assert "unused_key" not in msg and "a_key]" not in msg
    assert not (out / "index.md").exists()


@XFAIL
def test_publish_with_all_used_claims_verified_sets_draft_false(tmp_path):
    draft, claims, out = make(tmp_path)  # a_key and b_key verified; unused_key is not and is not used
    done = build(draft, claims, out, "--publish")
    assert done.returncode == 0, done.stdout + done.stderr
    front = (out / "index.md").read_text().split("\n+++\n")[0]
    assert "draft = false" in front and "draft = true" not in front

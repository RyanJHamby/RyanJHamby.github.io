#!/usr/bin/env python3
"""Collect captured runs and evidence-backed claims from one or more repos into one JSON ledger.

    python3 tools/collect_claims.py [--verified-only] OUT.json REPO_DIR[=GITHUB_SLUG] [REPO_DIR[=GITHUB_SLUG] ...]

--verified-only drops claims Ryan has not marked verified (drafts in progress), as the public build does.

For each repo it reads:
  - results/<run>/{cmd.txt,env.txt,output.log}   (written by `pow run`)
  - **/claims.yaml outside .git and node_modules (the writing system's evidence file)

Standard library only. claims.yaml is parsed with the same narrow regex approach as tools/build_post.py:
top-level `- key:` items with `key: value` string fields.

Runs on macOS/Apple hardware are marked real_host=false: they are fine as sanity checks but are not
the numbers to cite (see the resume rules).
"""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SKIP_DIRS = {".git", "node_modules", "public", "themes", ".venv", "target"}
ENV_FIELDS = ("date", "git", "host-os", "cpu", "memory", "exit_code", "wall_seconds")


def parse_env(text: str) -> dict[str, str]:
    env: dict[str, str] = {}
    for line in text.splitlines():
        m = re.match(r"^([A-Za-z0-9_+.-]+):\s*(.*)$", line)
        if m and m.group(1) in ENV_FIELDS and m.group(1) not in env:
            env[m.group(1)] = m.group(2).strip()
    gpu = re.search(r"NVIDIA\s+([A-Z0-9][\w -]*?)\s{2,}", text)
    if gpu:
        env["gpu"] = "NVIDIA " + gpu.group(1).strip()
    return env


def is_real_host(env: dict[str, str]) -> bool:
    host = env.get("host-os", "") + " " + env.get("cpu", "")
    return not re.search(r"Darwin|Apple", host)


def collect_runs(repo: Path, slug: str | None) -> list[dict]:
    runs = []
    results = repo / "results"
    if not results.is_dir():
        return runs
    for run_dir in sorted(p for p in results.iterdir() if p.is_dir()):
        cmd, env_file, log = (run_dir / n for n in ("cmd.txt", "env.txt", "output.log"))
        if not (cmd.is_file() and env_file.is_file() and log.is_file()):
            continue
        env = parse_env(env_file.read_text(errors="replace"))
        rel = f"results/{run_dir.name}"
        runs.append(
            {
                "id": f"{repo.name}:{run_dir.name}",
                "repo": slug or repo.name,
                "name": run_dir.name,
                "date": env.get("date", ""),
                "commit": env.get("git", ""),
                "hardware": {k: env[k] for k in ("host-os", "cpu", "memory", "gpu") if k in env},
                "real_host": is_real_host(env),
                "exit_code": env.get("exit_code", ""),
                "command": cmd.read_text(errors="replace").strip(),
                "url": f"https://github.com/{slug}/tree/HEAD/{rel}" if slug else rel,
            }
        )
    return runs


def parse_claims_yaml(text: str) -> list[dict[str, str]]:
    items: list[dict[str, str]] = []
    current: dict[str, str] | None = None
    for line in text.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        m = re.match(r"^-\s+key:\s*(.+)$", line)
        if m:
            current = {"key": _unquote(m.group(1))}
            items.append(current)
            continue
        m = re.match(r"^\s+([a-z_]+):\s*(.*)$", line)
        if m and current is not None:
            current[m.group(1)] = _unquote(m.group(2))
    return items


def _unquote(v: str) -> str:
    v = v.strip()
    if len(v) >= 2 and v[0] == v[-1] and v[0] in "\"'":
        v = v[1:-1]
    return v


def collect_claims(repo: Path, slug: str | None) -> list[dict]:
    claims = []
    for path in sorted(repo.rglob("claims.yaml")):
        if SKIP_DIRS & set(path.relative_to(repo).parts):
            continue
        rel = path.relative_to(repo).as_posix()
        for item in parse_claims_yaml(path.read_text(errors="replace")):
            if "claim" not in item:
                continue
            claims.append(
                {
                    "id": f"{repo.name}:{path.parent.name}:{item['key']}",
                    "repo": slug or repo.name,
                    "source": rel,
                    "kind": item.get("kind", ""),
                    "claim": item["claim"],
                    "evidence": item.get("evidence", ""),
                    "verified": bool(item.get("verified_by")) and bool(item.get("verified_on")),
                    "verified_on": item.get("verified_on", ""),
                }
            )
    return claims


def build(repos: list[tuple[Path, str | None]], verified_only: bool = False) -> dict:
    runs: list[dict] = []
    claims: list[dict] = []
    for repo, slug in repos:
        runs += collect_runs(repo, slug)
        claims += collect_claims(repo, slug)
    if verified_only:
        claims = [c for c in claims if c["verified"]]
    return {
        "schema": "ryanjhamby.dev/claims/v1",
        "subject": {"name": "Ryan J Hamby", "url": "https://ryanjhamby.dev/"},
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "note": "Runs marked real_host=false were captured on a laptop and are not the figures to cite.",
        "runs": runs,
        "claims": claims,
    }


def main(argv: list[str]) -> int:
    verified_only = "--verified-only" in argv
    argv = [a for a in argv if a != "--verified-only"]
    if len(argv) < 3:
        print("usage: collect_claims.py [--verified-only] OUT.json REPO_DIR[=SLUG] ...", file=sys.stderr)
        return 2
    out = Path(argv[1])
    repos = []
    for arg in argv[2:]:
        path, _, slug = arg.partition("=")
        p = Path(path)
        if not p.is_dir():
            print(f"not a directory: {path}", file=sys.stderr)
            return 2
        repos.append((p, slug or None))
    data = build(repos, verified_only)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")
    print(f"{out}: {len(data['runs'])} runs, {len(data['claims'])} claims")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))

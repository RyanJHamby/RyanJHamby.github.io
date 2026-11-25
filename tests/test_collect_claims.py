"""tools/collect_claims.py: runs and claims from several repos into one JSON ledger."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "tools" / "collect_claims.py"


def make_run(repo: Path, name: str, host: str, cpu: str, gpu: bool = False) -> None:
    d = repo / "results" / name
    d.mkdir(parents=True)
    (d / "cmd.txt").write_text("./bench --orders 1000000\n")
    env = f"date: 2026-11-01 10:00 EST\ngit: abc1234\nhost-os: {host}\ncpu: {cpu}\nmemory: 4 GB\nexit_code: 0\n"
    if gpu:
        env += "| NVIDIA H100 80GB HBM3          On  |\n"
    (d / "env.txt").write_text(env)
    (d / "output.log").write_text("P50 0.21 us\n")


def run(tmp: Path, *args: str) -> tuple[subprocess.CompletedProcess, dict | None]:
    out = tmp / "claims.json"
    done = subprocess.run([sys.executable, str(SCRIPT), str(out), *args], capture_output=True, text=True)
    return done, (json.loads(out.read_text()) if out.exists() else None)


def test_collects_runs_and_marks_laptop_runs(tmp_path: Path) -> None:
    a = tmp_path / "engine"
    make_run(a, "2026-11-01-1000-ec2", "Linux 6.8 x86_64", "Intel Xeon Platinum 8375C, 2 logical cores")
    make_run(a, "2026-11-01-1100-mac", "Darwin 25.6.0 arm64", "Apple M4, 10 logical cores")
    make_run(a, "2026-11-01-1200-gpu", "Linux 6.8 x86_64", "AMD EPYC", gpu=True)
    (a / "results" / "README.md").write_text("not a run")
    (a / "results" / "incomplete").mkdir()
    done, data = run(tmp_path, f"{a}=RyanJHamby/engine")
    assert done.returncode == 0, done.stderr
    runs = {r["name"]: r for r in data["runs"]}
    assert set(runs) == {"2026-11-01-1000-ec2", "2026-11-01-1100-mac", "2026-11-01-1200-gpu"}
    assert runs["2026-11-01-1000-ec2"]["real_host"] is True
    assert runs["2026-11-01-1100-mac"]["real_host"] is False
    assert runs["2026-11-01-1200-gpu"]["hardware"]["gpu"] == "NVIDIA H100 80GB HBM3"
    assert runs["2026-11-01-1000-ec2"]["url"] == (
        "https://github.com/RyanJHamby/engine/tree/HEAD/results/2026-11-01-1000-ec2"
    )
    assert runs["2026-11-01-1000-ec2"]["command"] == "./bench --orders 1000000"


def test_collects_claims_with_verification_state(tmp_path: Path) -> None:
    site = tmp_path / "site"
    (site / "drafts" / "post").mkdir(parents=True)
    (site / "drafts" / "post" / "claims.yaml").write_text(
        "# comment\n"
        "- key: a\n  kind: run\n  claim: \"One: two\"\n  evidence: \"results/x/output.log\"\n"
        "  verified_by: Ryan Hamby\n  verified_on: 2026-11-13\n"
        "- key: b\n  kind: est\n  claim: Unverified estimate\n  evidence: My own estimate\n"
        "  verified_by:\n  verified_on:\n"
    )
    (site / "node_modules" / "x").mkdir(parents=True)
    (site / "node_modules" / "x" / "claims.yaml").write_text("- key: z\n  claim: ignored\n")
    done, data = run(tmp_path, str(site))
    assert done.returncode == 0, done.stderr
    claims = {c["id"]: c for c in data["claims"]}
    assert set(claims) == {"site:post:a", "site:post:b"}
    assert claims["site:post:a"]["claim"] == "One: two"
    assert claims["site:post:a"]["verified"] is True
    assert claims["site:post:b"]["verified"] is False
    assert claims["site:post:a"]["source"] == "drafts/post/claims.yaml"


def test_rejects_missing_repo(tmp_path: Path) -> None:
    done, data = run(tmp_path, str(tmp_path / "nope"))
    assert done.returncode == 2
    assert data is None


def test_real_repo_runs_are_collected() -> None:
    import importlib.util

    spec = importlib.util.spec_from_file_location("cc", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    data = mod.build([(REPO, "RyanJHamby/RyanJHamby.github.io")])
    assert any(r["name"].endswith("zonevex-repo-stats") for r in data["runs"])
    assert all(r["real_host"] is False for r in data["runs"] if "Darwin" in r["hardware"].get("host-os", ""))


def test_verified_only_drops_unverified(tmp_path: Path) -> None:
    site = tmp_path / "site"
    (site / "drafts" / "p").mkdir(parents=True)
    (site / "drafts" / "p" / "claims.yaml").write_text(
        "- key: a\n  claim: yes\n  verified_by: Ryan Hamby\n  verified_on: 2026-11-13\n"
        "- key: b\n  claim: no\n  verified_by:\n  verified_on:\n"
    )
    done, data = run(tmp_path, "--verified-only", str(site))
    assert done.returncode == 0, done.stderr
    assert [c["claim"] for c in data["claims"]] == ["yes"]

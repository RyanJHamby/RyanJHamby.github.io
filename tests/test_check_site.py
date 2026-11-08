"""Spec site-integrity-check: tools/check_site.py verifies a built Hugo site.

Run from the repo root. Builds the real site once with `hugo --minify`, then runs the checker on it
and on deliberately broken copies. Each broken copy must fail with the matching rule name.
"""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

XFAIL = pytest.mark.xfail(
    strict=True, reason="spec:site-integrity-check (remove this marker when implemented)"
)
REPO = Path(__file__).resolve().parents[1]
SCRIPT = REPO / "tools" / "check_site.py"


@pytest.fixture(scope="module")
def built(tmp_path_factory) -> Path:
    out = tmp_path_factory.mktemp("site") / "public"
    done = subprocess.run(
        ["hugo", "--minify", "-d", str(out)], cwd=REPO, capture_output=True, text=True
    )
    assert done.returncode == 0, done.stdout + done.stderr
    assert (out / "index.xml").is_file()
    return out


def run_check(public: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(SCRIPT), str(public), "--root", str(REPO)],
        capture_output=True,
        text=True,
    )


@pytest.fixture
def copy(built, tmp_path) -> Path:
    dst = tmp_path / "public"
    shutil.copytree(built, dst)
    return dst


def expect_fail(public: Path, rule: str) -> str:
    done = run_check(public)
    out = done.stdout + done.stderr
    assert done.returncode == 1, out
    assert f"FAIL {rule}" in out, out
    return out


@XFAIL
def test_real_site_passes(built):
    done = run_check(built)
    assert done.returncode == 0, done.stdout + done.stderr
    assert "FAIL" not in done.stdout


@XFAIL
def test_feed_with_zero_year_date_fails(copy):
    feed = copy / "index.xml"
    text = feed.read_text()
    assert run_check(copy).returncode == 0
    feed.write_text(re.sub(r"<pubDate>[^<]*</pubDate>", "<pubDate>Mon, 01 Jan 0001 00:00:00 +0000</pubDate>", text, count=1))
    expect_fail(copy, "feed-dates")


@XFAIL
def test_feed_with_a_non_post_item_fails(copy):
    feed = copy / "index.xml"
    assert run_check(copy).returncode == 0
    extra = "<item><title>About</title><link>https://ryanjhamby.dev/about/</link><pubDate>Mon, 02 Jan 2006 15:04:05 +0000</pubDate></item>"
    feed.write_text(feed.read_text().replace("</channel>", extra + "</channel>", 1))
    expect_fail(copy, "feed-items")


@XFAIL
def test_empty_feed_fails(copy):
    feed = copy / "index.xml"
    assert run_check(copy).returncode == 0
    feed.write_text(re.sub(r"<item>.*?</item>", "", feed.read_text(), flags=re.S))
    expect_fail(copy, "feed-items")


@XFAIL
def test_page_without_feed_link_fails(copy):
    page = copy / "projects" / "flowstate" / "index.html"
    assert run_check(copy).returncode == 0
    page.write_text(re.sub(r"<link rel=alternate type=application/rss\+xml[^>]*>", "", page.read_text()))
    out = expect_fail(copy, "rss-link")
    assert "projects/flowstate" in out


@XFAIL
def test_page_with_two_feed_links_fails(copy):
    page = copy / "about" / "index.html"
    assert run_check(copy).returncode == 0
    dup = '<link rel=alternate type=application/rss+xml href=https://ryanjhamby.dev/writing/index.xml title=rss>'
    page.write_text(page.read_text().replace("</head>", dup + "</head>", 1))
    expect_fail(copy, "rss-link")


@XFAIL
def test_draft_page_in_output_or_sitemap_fails(copy):
    # content/projects/drillpad.md and content/writing/flowstate-asof-join are draft = true today.
    assert run_check(copy).returncode == 0
    sm = copy / "sitemap.xml"
    sm.write_text(sm.read_text().replace("</urlset>", "<url><loc>https://ryanjhamby.dev/projects/drillpad/</loc></url></urlset>"))
    out = expect_fail(copy, "draft-leak")
    assert "drillpad" in out


@XFAIL
def test_draft_page_built_to_disk_fails(copy):
    assert run_check(copy).returncode == 0
    page = copy / "writing" / "flowstate-asof-join" / "index.html"
    page.parent.mkdir(parents=True)
    page.write_text("<html><head><meta name=description content=x></head></html>")
    out = expect_fail(copy, "draft-leak")
    assert "flowstate-asof-join" in out


@XFAIL
def test_page_without_description_fails(copy):
    page = copy / "about" / "index.html"
    assert run_check(copy).returncode == 0
    page.write_text(re.sub(r"<meta name=description[^>]*>", "", page.read_text()))
    out = expect_fail(copy, "description")
    assert "about" in out


@XFAIL
def test_missing_llms_txt_fails(copy):
    assert run_check(copy).returncode == 0
    (copy / "llms.txt").unlink()
    expect_fail(copy, "llms-link")


@XFAIL
def test_llms_txt_link_to_unbuilt_page_fails(copy):
    llms = copy / "llms.txt"
    assert run_check(copy).returncode == 0
    llms.write_text(llms.read_text() + "\n- [Gone](https://ryanjhamby.dev/writing/does-not-exist/)\n")
    out = expect_fail(copy, "llms-link")
    assert "does-not-exist" in out

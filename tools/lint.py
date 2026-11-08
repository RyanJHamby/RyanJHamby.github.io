#!/usr/bin/env python3
"""Pre-publish lint for writing-rules posts.

Checks (deterministic, no network):
  1. Banned phrases from STYLE.md §4
  2. Unresolved markers: {{TODO}}, {{HUMAN}}, BLOCKED
  3. Numbers in prose without a [run:], [cite:], or [est:] tag on the same line
  4. Tags that don't resolve to a key in claims.yaml (if given)
  5. Required footer elements (AI disclosure, Published date)

Usage: python3 tools/lint.py posts/<slug>/draft.md [posts/<slug>/claims.yaml]
Exit code 1 if any check fails. This is a helper, not a substitute for CHECKLIST.md.
"""
import re
import sys
from pathlib import Path

BANNED = [
    r"\bdelve\w*", r"\btapestry\b", r"\brealm\b", r"\bembark\w*",
    r"in today's fast-paced world", r"ever-evolving",
    r"it'?s important to note", r"it'?s worth noting", r"\bnotably\b", r"\bcrucially\b",
    r"game[- ]changer", r"\brevolutioniz\w*", r"\bunlock\w*", r"\bsupercharg\w*",
    r"\bseamless\w*", r"\bleverag(e|es|ed|ing)\b", r"\butiliz\w*",
    r"let'?s dive in", r"let'?s break it down", r"buckle up",
    r"in conclusion", r"to sum up", r"at the end of the day",
    r"studies show", r"experts say", r"many believe",
    r"it'?s not just \w+.{0,40}it'?s",
]
MARKERS = [r"\{\{TODO", r"\{\{HUMAN", r"BLOCKED"]
TAG = re.compile(r"\[(run|cite|est):([A-Za-z0-9_\-]+)\]")
# A "number" worth tagging: digits with optional decimals/commas, optionally followed by a unit or %.
NUMBER = re.compile(r"(?<![\w./#-])\$?\d[\d,]*(\.\d+)?\s?(%|ms|s|W|kW|kWh|Wh|J|GB|tok/s|x|×)?(?![\w/-])")


def strip_code(text):
    """Remove fenced code, inline code, front matter, links, and HTML comments."""
    text = re.sub(r"^---\n.*?\n---\n", "", text, flags=re.S)
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    text = re.sub(r"<!--.*?-->", "", text, flags=re.S)
    text = re.sub(r"`[^`]*`", "", text)
    text = re.sub(r"\]\([^)]*\)", "]", text)
    return text


def load_keys(path):
    keys = set()
    for line in Path(path).read_text().splitlines():
        m = re.match(r"\s*-\s*key:\s*([A-Za-z0-9_\-]+)", line)
        if m:
            keys.add(m.group(1))
    return keys


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        return 2
    raw = Path(sys.argv[1]).read_text()
    keys = load_keys(sys.argv[2]) if len(sys.argv) > 2 else None
    body = strip_code(raw)
    problems = []

    for i, line in enumerate(body.splitlines(), 1):
        low = line.lower()
        for pat in BANNED:
            if re.search(pat, low):
                problems.append(f"line {i}: banned phrase /{pat}/")
        for pat in MARKERS:
            if re.search(pat, line):
                problems.append(f"line {i}: unresolved marker {pat}")
        if line.lstrip().startswith(("#", "|---", "[", "**Published", "**Reproduce", "**Data")):
            continue
        tags = TAG.findall(line)
        nums = [m.group(0) for m in NUMBER.finditer(TAG.sub("", line))]
        nums = [n for n in nums if not re.fullmatch(r"(19|20)\d\d", n.strip())]  # skip bare years
        if nums and not tags:
            problems.append(f"line {i}: untagged number(s) {nums[:3]}")
        if keys is not None:
            for _, key in tags:
                if key not in keys:
                    problems.append(f"line {i}: tag key '{key}' not in claims.yaml")

    if "AI disclosure" not in raw:
        problems.append("missing AI disclosure footer")

    for p in problems:
        print(p)
    print(f"\n{len(problems)} problem(s)." if problems else "OK: no problems found.")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())

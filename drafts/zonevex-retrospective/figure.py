#!/usr/bin/env python3
"""Generate the post's one figure from a pow run capture's output.log.

Usage: python3 figure.py <path/to/output.log> <out.png>
Input lines look like "  148 2026-02" (commit count, month), from `git log | sort | uniq -c`.
Months with no commits are drawn as zero. The pause-documentation month (2026-11) is excluded
on purpose: those commits record the pause, they are not product work.
Requires matplotlib==3.11.2 (numpy==2.5.4).
"""
import re
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

LINE = re.compile(r"^\s*(\d+)\s+(\d{4})-(\d{2})\s*$")
counts = {}
for line in open(sys.argv[1]):
    if m := LINE.match(line):
        counts[(int(m.group(2)), int(m.group(3)))] = int(m.group(1))

months = [(2026, mo) for mo in range(2, 11)]  # Feb to Oct 2026
labels = ["Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct"]
values = [counts.get(k, 0) for k in months]

fig, ax = plt.subplots(figsize=(8, 4.6), dpi=200)
bars = ax.bar(labels, values, color="#0072B2", width=0.7)
for bar, v in zip(bars, values):
    ax.text(bar.get_x() + bar.get_width() / 2, v + 6, str(v), ha="center", va="bottom", fontsize=9)
ax.set_title("Zonevex commits: busy February to June, none July to September", fontsize=12, loc="left")
ax.set_ylabel("Commits on main per month (n)")
ax.set_xlabel("2026 (commit author date)")
ax.set_ylim(0, max(values) * 1.15)
ax.spines[["top", "right"]].set_visible(False)
fig.text(
    0.01, 0.005,
    "Data: git log of the private Zonevex repo, run 2026-11-13-1729-zonevex-commits-by-month, "
    "Apple M4, 32 GB. Counts commits, not effort or output.",
    fontsize=7, color="#444444",
)
fig.tight_layout(rect=(0, 0.03, 1, 1))
fig.savefig(sys.argv[2])
print("wrote", sys.argv[2], "values:", dict(zip(labels, values)))

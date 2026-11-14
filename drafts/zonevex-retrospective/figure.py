#!/usr/bin/env python3
"""Generate the post's one figure from outreach.csv.

Usage: python3 figure.py outreach.csv figure.png
Horizontal bars on a linear scale, so the drop from the first bar to the rest is drawn to scale.
The numbers are the author's own figures (claim "outreach"), not a captured run.
Requires matplotlib==3.11.2 (numpy==2.5.4).
"""
import csv
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

rows = [r for r in csv.DictReader(line for line in open(sys.argv[1]) if not line.startswith("#"))]
labels = [r["stage"] for r in rows]
values = [int(r["count"]) for r in rows]

fig, ax = plt.subplots(figsize=(8, 3.8), dpi=200)
y = range(len(rows))
ax.barh(list(y), values, color="#0072B2", height=0.6)
ax.set_yticks(list(y), labels)
ax.invert_yaxis()
ax.set_xlim(0, max(values) * 1.12)
for i, v in enumerate(values):
    ax.text(v + max(values) * 0.012, i, f"{v:,}", va="center", fontsize=11)
ax.set_title("2,454 cold emails: one reply, one call, no paying customers", fontsize=12, loc="left")
ax.set_xlabel("Count (bars to scale)")
ax.spines[["top", "right"]].set_visible(False)
ax.tick_params(axis="y", length=0)
fig.text(0.01, 0.01, "Author's own figures; no export from the email-sending tool is published.", fontsize=7, color="#444444")
fig.tight_layout(rect=(0, 0.04, 1, 1))
fig.savefig(sys.argv[2])
print("wrote", sys.argv[2], dict(zip(labels, values)))

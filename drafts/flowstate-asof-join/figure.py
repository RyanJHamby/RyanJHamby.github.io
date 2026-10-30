#!/usr/bin/env python3
"""Generate the post's one figure from a pow run capture's output.log.

Usage: python3 figure.py <path/to/output.log> <out.png>
Bars are medians of 10 runs; whiskers are the fastest and slowest run.
"""
import re
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

LINE = re.compile(r"^\s+(\w+)\s+([\d.]+) ms\s+\(min ([\d.]+), max ([\d.]+);")
DATASET = re.compile(r"^dataset: ([\d,]+) left")
RUNS = re.compile(r"median of (\d+) runs")

data, cur, n = {}, None, None
for line in open(sys.argv[1]):
    if m := RUNS.search(line):
        n = int(m.group(1))
    if m := DATASET.match(line):
        cur = m.group(1)
        data[cur] = {}
    elif (m := LINE.match(line)) and cur:
        data[cur][m.group(1)] = tuple(float(x) for x in m.groups()[1:])

engines = [("polars", "Polars", "#0072B2"), ("flowstate", "FlowState", "#D55E00"), ("pandas", "pandas", "#999999")]
sizes = list(data)
fig, ax = plt.subplots(figsize=(8, 4.6), dpi=200)
w = 0.26
for i, (key, label, color) in enumerate(engines):
    xs = [j + (i - 1) * w for j in range(len(sizes))]
    med = [data[s][key][0] for s in sizes]
    lo = [data[s][key][0] - data[s][key][1] for s in sizes]
    hi = [data[s][key][2] - data[s][key][0] for s in sizes]
    ax.bar(xs, med, w * 0.92, color=color, label=label, yerr=[lo, hi], capsize=3, ecolor="#222222", error_kw={"lw": 1})
    for x, m in zip(xs, med):
        ax.text(x, m * 1.12, f"{m:.1f}", ha="center", va="bottom", fontsize=8)
ax.set_yscale("log")
ax.set_ylim(top=ax.get_ylim()[1] * 2)
ax.set_xticks(range(len(sizes)), [f"{s} left rows" for s in sizes])
ax.set_ylabel("As-of join time (ms, log scale)")
ax.set_title("FlowState's as-of join was slower than Polars at both sizes", loc="left", fontsize=11, fontweight="bold")
for sp in ("top", "right"):
    ax.spines[sp].set_visible(False)
ax.legend(frameon=False, loc="upper left")
fig.text(0.01, 0.01, f"Median of {n} runs per bar, whiskers = fastest and slowest run. Apple M4, 32 GB, backward join, synthetic data.\n"
         "Run 2026-10-30-1412-asof-join-spread @ fdc202b.", fontsize=7, color="#444444", va="bottom")
fig.tight_layout(rect=(0, 0.07, 1, 1))
fig.savefig(sys.argv[2])

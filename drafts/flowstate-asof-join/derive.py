#!/usr/bin/env python3
"""Derive the ratios quoted in the post from a pow run capture's output.log.

Usage: python3 -I derive.py <path/to/output.log>
Reads: lines like "  polars   9.9 ms   (min 9.3, max 10.9; 1.00x vs polars)".
"""
import re
import sys

LINE = re.compile(r"^\s+(\w+)\s+([\d.]+) ms\s+\(min ([\d.]+), max ([\d.]+);")
DATASET = re.compile(r"^dataset: ([\d,]+) left")

data, cur = {}, None
for line in open(sys.argv[1]):
    m = DATASET.match(line)
    if m:
        cur = m.group(1)
        data[cur] = {}
        continue
    m = LINE.match(line)
    if m and cur:
        data[cur][m.group(1)] = tuple(float(x) for x in m.groups()[1:])

for rows, eng in data.items():
    p, f = eng["polars"], eng["flowstate"]
    print(f"left rows {rows}:")
    print(f"  flowstate/polars median ratio: {f[0] / p[0]:.2f}  (flowstate {f[0]} ms, polars {p[0]} ms)")
    print(f"  ranges overlap: {not (p[2] < f[1] or f[2] < p[1])}  (polars max {p[2]} ms, flowstate min {f[1]} ms)")

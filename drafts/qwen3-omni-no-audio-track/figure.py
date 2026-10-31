#!/usr/bin/env python3
"""Draws figure.svg and figure.png: the call chain behind the false-positive guard.
Narrow and stacked so the text stays readable at phone width (about 340 px).
Every box restates the author's PR #48420 comment of 2026-07-18; nothing is measured.
Usage: python3 figure.py   (needs Google Chrome on macOS for the PNG)"""
import subprocess, pathlib

W = 440
INK, MUTED, BG = "#1d1d1f", "#5a5a5f", "#fbfaf7"
BLUE, ORANGE = "#1d4e89", "#b35900"   # colorblind-safe pair; text labels carry meaning too
parts = []

def text(x, y, s, size=13, weight=400, fill=MUTED):
    parts.append(f'<text x="{x}" y="{y}" font-size="{size}" font-weight="{weight}" fill="{fill}">{s}</text>')

def box(y, title, lines, stroke):
    h = 40 + 20 * len(lines)
    parts.append(f'<rect x="16" y="{y}" width="{W-32}" height="{h}" rx="8" fill="#fff" stroke="{stroke}" stroke-width="2"/>')
    text(30, y + 26, title, 14, 700, INK)
    for i, l in enumerate(lines):
        text(30, y + 50 + i * 20, l)
    return y + h

def arrow(y):
    parts.append(f'<path d="M{W//2} {y} V{y+22}" stroke="{INK}" stroke-width="2" fill="none" marker-end="url(#a)"/>')
    return y + 26

text(16, 30, "The guard failed because the parent", 18, 700, INK)
text(16, 52, "never saw the audio", 18, 700, INK)
text(16, 74, "vLLM PR #48420, _call_hf_processor with", 12)
text(16, 90, "use_audio_in_video=True. Source: the PR comment of 2026-07-18.", 12)

text(16, 124, "Path 1: inheritance", 15, 700, INK)
y = box(136, "Qwen3-Omni processor (child)", ["pops mm_data[&quot;audios&quot;]", "builds mm_data[&quot;audio&quot;]", "calls super()._call_hf_processor(...)"], BLUE)
y = arrow(y)
y = box(y, "Qwen2.5-Omni processor (parent)", ["pops &quot;audios&quot; again: already gone", "so it always sees an empty list", "guard raised, even with real audio"], ORANGE)
text(16, y + 24, "Fix: raise only if mm_data still has videos", 12)
text(16, y + 40, "and no &quot;audio&quot; key was built by a subclass.", 12)

y += 72
text(16, y, "Path 2: cache hit", 15, 700, INK)
y = box(y + 12, "Full processor-cache hit", ["_call_hf_processor gets empty mm_data", "nothing to reprocess; result is cached", "guard read empty input as &quot;no audio&quot;"], ORANGE)
y = arrow(y)
y = box(y, "Both guards (child and parent)", ["raised ValueError on the second call of", "test_audio_in_video_cache_correctness"], ORANGE)
text(16, y + 24, "Fix: skip the check when there are no videos.", 12)
text(16, y + 46, "Both were found while investigating CI failures.", 12)
text(16, y + 62, "Not a measurement.", 12)
H = y + 78

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="-apple-system,Helvetica,Arial,sans-serif" role="img" aria-labelledby="t d">
<title id="t">The guard failed because the parent processor never saw the audio</title>
<desc id="d">Path 1: the Qwen3-Omni processor pops the audios key and calls the Qwen2.5-Omni parent, which pops it again, sees an empty list, and raised even with real audio. Path 2: on a processor-cache hit the input is empty and both guards read that as no audio track.</desc>
<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker></defs>
<rect width="{W}" height="{H}" fill="{BG}"/>
{chr(10).join(parts)}
</svg>'''
here = pathlib.Path(__file__).parent
(here / "figure.svg").write_text(svg)
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
                f"--screenshot={here/'figure.png'}", f"file://{here/'figure.svg'}"], check=True, capture_output=True)
print("wrote figure.svg, figure.png", W, "x", H)

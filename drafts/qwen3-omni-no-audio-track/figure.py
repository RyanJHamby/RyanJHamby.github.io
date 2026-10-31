#!/usr/bin/env python3
"""Draws figure.svg and figure.png: the call chain behind the false-positive guard.
Every box restates the author's PR #48420 comment of 2026-07-18; nothing is measured.
Usage: python3 figure.py   (needs Google Chrome on macOS for the PNG)"""
import subprocess, pathlib

W, H = 880, 470
INK, MUTED, BG = "#1d1d1f", "#5a5a5f", "#fbfaf7"
BLUE, ORANGE = "#1d4e89", "#b35900"   # colorblind-safe pair; text labels carry meaning too

def box(x, y, w, h, title, lines, stroke):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="#fff" stroke="{stroke}" stroke-width="2"/>',
           f'<text x="{x+14}" y="{y+26}" font-size="14" font-weight="700" fill="{INK}">{title}</text>']
    for i, l in enumerate(lines):
        out.append(f'<text x="{x+14}" y="{y+50+i*20}" font-size="13" fill="{MUTED}">{l}</text>')
    return "\n".join(out)

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" font-family="-apple-system,Helvetica,Arial,sans-serif" role="img" aria-labelledby="t d">
<title id="t">My guard failed because the parent processor never saw the audio</title>
<desc id="d">Two boxes: the Qwen3-Omni processor pops the audios key and calls the Qwen2.5-Omni parent, which pops it again and sees nothing, so the guard raised even with real audio. A second path: on a processor-cache hit the input is empty and the guard read that as no audio track.</desc>
<rect width="{W}" height="{H}" fill="{BG}"/>
<text x="24" y="38" font-size="20" font-weight="700" fill="{INK}">My guard failed because the parent never saw the audio</text>
<text x="24" y="62" font-size="13" fill="{MUTED}">vLLM PR #48420, _call_hf_processor with use_audio_in_video=True. Source: the author's PR comment of 2026-07-18.</text>
{box(24, 90, 380, 120, "Qwen3-Omni processor (child)", ["pops mm_data[&quot;audios&quot;]", "builds mm_data[&quot;audio&quot;]", "calls super()._call_hf_processor(...)"], BLUE)}
<path d="M404 150 H476" stroke="{INK}" stroke-width="2" fill="none" marker-end="url(#a)"/>
{box(476, 90, 380, 120, "Qwen2.5-Omni processor (parent)", ["pops &quot;audios&quot; again: already gone", "so it always sees an empty list", "new guard raised, even with real audio"], ORANGE)}
<text x="24" y="246" font-size="15" font-weight="700" fill="{INK}">Path 1: inheritance</text>
<text x="24" y="268" font-size="13" fill="{MUTED}">Fix: raise only if mm_data still has videos and no \"audio\" key was already built by a subclass.</text>
{box(24, 296, 380, 120, "Full processor-cache hit", ["_call_hf_processor receives empty mm_data", "nothing to reprocess; result is cached", "guard read empty input as &quot;no audio track&quot;"], ORANGE)}
<path d="M404 356 H476" stroke="{INK}" stroke-width="2" fill="none" marker-end="url(#a)"/>
{box(476, 296, 380, 120, "Both guards (child and parent)", ["raised ValueError on the second call", "of test_audio_in_video_cache_correctness", "Fix: skip the check when there are no videos"], ORANGE)}
<text x="24" y="448" font-size="13" fill="{MUTED}">Path 2: cache hit. Both were found while investigating CI failures. Not a measurement.</text>
<defs><marker id="a" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto"><path d="M0 0 L10 5 L0 10 z" fill="{INK}"/></marker></defs>
</svg>'''
here = pathlib.Path(__file__).parent
(here / "figure.svg").write_text(svg)
chrome = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
subprocess.run([chrome, "--headless=new", "--disable-gpu", "--hide-scrollbars", f"--window-size={W},{H}",
                f"--screenshot={here/'figure.png'}", f"file://{here/'figure.svg'}"], check=True, capture_output=True)
print("wrote figure.svg, figure.png")

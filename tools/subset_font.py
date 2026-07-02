#!/usr/bin/env python3
"""Regenerate the embedded LXGW WenKai subset for proto-d (cross-machine font BLOCKER fix).
Steps: download LXGWWenKai-Regular.ttf (OFL-1.1, github.com/lxgw/LxgwWenKai), collect every
non-ASCII char used in the HTML, pyftsubset to woff (woff2 if brotli available), base64-embed
into the @font-face 'LXGW WenKai S' rule. Re-run whenever page text adds NEW hanzi —
a missing glyph silently falls back to system 楷体 (per-char), so diff the char count."""
import base64, re, subprocess, sys, os
S = os.path.dirname(os.path.abspath(__file__))
HTML = os.path.join(S, "..", "designs", "visible-faithfulness-g01", "prototypes", "proto-d-multiarticle-hub.html")
TTF = sys.argv[1] if len(sys.argv) > 1 else os.path.join(S, "LXGWWenKai-Regular.ttf")
src = open(HTML, encoding="utf-8").read()
chars = "".join(sorted({c for c in src if ord(c) > 127}))
open(os.path.join(S, "subset_chars.txt"), "w", encoding="utf-8").write(chars)
print(f"{len(chars)} chars")
out = os.path.join(S, "lxgw-subset.woff")
subprocess.run(["pyftsubset", TTF, f"--text-file={os.path.join(S,'subset_chars.txt')}",
                "--flavor=woff", f"--output-file={out}"], check=True)
b64 = base64.b64encode(open(out, "rb").read()).decode()
new = re.sub(r"src:url\(data:font/woff;base64,[^)]*\) format\('woff'\)",
             f"src:url(data:font/woff;base64,{b64}) format('woff')", src, count=1)
assert new != src or b64 in src, "font-face rule not found"
open(HTML, "w", encoding="utf-8").write(new)
print(f"embedded {len(b64)//1024}KB base64; html {os.path.getsize(HTML)//1024}KB")

#!/usr/bin/env python3
"""Generate site/changelog.html from CHANGELOG.md.

Two hand-maintained copies of the same list would drift, so the page is built
from the file. Run before deploying the site: python3 scripts/build_changelog.py
"""

from __future__ import annotations

import html
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "CHANGELOG.md"
OUT = ROOT / "site/changelog.html"

MARK = ('<span class="mark"><i></i><i></i><i></i><i></i></span>')


def inline(text: str) -> str:
    """Escape, then re-apply the inline markdown this changelog actually uses."""
    out = html.escape(text)
    out = re.sub(r"`([^`]+)`", r"<code>\1</code>", out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    return out


def render(md: str) -> str:
    lines = md.split("\n")
    parts: list[str] = []
    i, in_list, in_code = 0, False, False
    buf: list[str] = []

    def close_list():
        nonlocal in_list
        if in_list:
            parts.append("</ul>")
            in_list = False

    def flush_para():
        if buf:
            parts.append("<p>" + inline(" ".join(buf).strip()) + "</p>")
            buf.clear()

    while i < len(lines):
        line = lines[i]

        if line.startswith("```"):
            flush_para(); close_list()
            if not in_code:
                block = []
                i += 1
                while i < len(lines) and not lines[i].startswith("```"):
                    block.append(lines[i]); i += 1
                parts.append('<pre><code>' + html.escape("\n".join(block)) + "</code></pre>")
            i += 1
            continue

        if line.startswith("# "):
            i += 1; continue                       # page supplies its own title
        if line.startswith("## "):
            flush_para(); close_list()
            head = line[3:].strip()
            m = re.match(r"^(\S+)\s*\((.+)\)$", head)
            if m:
                parts.append(f'<h2 id="v{m.group(1)}">{inline(m.group(1))}'
                             f'<span class="date">{inline(m.group(2))}</span></h2>')
            else:
                parts.append(f"<h2>{inline(head)}</h2>")
            i += 1; continue
        if line.startswith("### "):
            flush_para(); close_list()
            parts.append(f'<h3>{inline(line[4:].strip())}</h3>')
            i += 1; continue

        if line.startswith("- "):
            flush_para()
            if not in_list:
                parts.append("<ul>"); in_list = True
            item = [line[2:].strip()]
            while i + 1 < len(lines) and lines[i + 1].startswith("  ") and lines[i + 1].strip():
                i += 1; item.append(lines[i].strip())
            parts.append("<li>" + inline(" ".join(item)) + "</li>")
            i += 1; continue

        if not line.strip():
            flush_para(); close_list()
        else:
            buf.append(line.strip())
        i += 1

    flush_para(); close_list()
    return "\n".join(parts)


PAGE = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Changelog: Evals Coach</title>
<meta name="description" content="What changed in each release of Evals Coach, the evals copilot for AI product managers.">
<meta property="og:title" content="Changelog: Evals Coach">
<meta property="og:description" content="What changed in each release of Evals Coach.">
<meta property="og:type" content="website">
<meta property="og:url" content="https://evalscoach.com/changelog">
<meta property="og:image" content="https://evalscoach.com/og.png">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#FAF5EC">
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=EB+Garamond:ital,wght@0,400;0,500;1,400&family=Figtree:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap">
<style>
:root{
  --cream:#FAF5EC; --surface:#FFFDF8; --surface-2:#F1ECDF; --card:#FFFFFF;
  --line:#E9E3D4; --line-strong:#D7D0BE;
  --ink:#1A1A1A; --ink-2:#57574F; --ink-3:#86857B;
  --lilac:#F0D7FF; --lilac-line:#E2BEFB; --lilac-ink:#5B2E86; --coral:#FF6C4C;
  --display:"EB Garamond", Georgia, serif;
  --body:"Figtree", -apple-system, BlinkMacSystemFont, Helvetica, Arial, sans-serif;
  --mono:"JetBrains Mono", ui-monospace, SFMono-Regular, Menlo, monospace;
  color-scheme: light;
}
*{box-sizing:border-box}
body{margin:0; background:var(--cream); color:var(--ink); font-family:var(--body);
  font-size:17px; line-height:1.6; -webkit-font-smoothing:antialiased}
.wrap{max-width:760px; margin:0 auto; padding:0 24px}
a{color:inherit}
nav{border-bottom:1px solid var(--line); background:var(--cream)}
.nav-in{display:flex; align-items:center; justify-content:space-between; height:66px;
  max-width:1080px; margin:0 auto; padding:0 24px}
.logo{display:flex; align-items:center; gap:10px; font-weight:600; font-size:17px; text-decoration:none}
.mark{display:inline-flex; gap:2.5px; align-items:flex-end; height:20px}
.mark i{width:3.5px; border-radius:2px; background:var(--lilac-ink); display:block}
.mark i:nth-child(1){height:8px} .mark i:nth-child(2){height:16px; background:var(--coral)}
.mark i:nth-child(3){height:11px} .mark i:nth-child(4){height:20px; background:var(--coral)}
.nav-links{display:flex; align-items:center; gap:8px}
.nav-links a{font-size:14.5px; font-weight:500; color:var(--ink-2); text-decoration:none;
  padding:8px 12px; border-radius:9px}
.nav-links a:hover{color:var(--ink); background:var(--surface-2)}
.btn{display:inline-flex; align-items:center; gap:8px; font-weight:600; font-size:14px;
  text-decoration:none; border:1px solid var(--lilac-line); border-radius:12px;
  padding:9px 15px; background:var(--lilac); color:var(--ink)}
header{padding:64px 0 0}
h1{font-family:var(--display); font-weight:400; font-size:clamp(38px,6vw,54px);
  letter-spacing:-.02em; margin:0}
.lede{color:var(--ink-2); font-size:18px; margin:16px 0 0; max-width:62ch}
main{padding:24px 0 72px}
main h2{font-family:var(--display); font-weight:400; font-size:34px; letter-spacing:-.015em;
  margin:56px 0 0; padding-top:28px; border-top:1px solid var(--line);
  display:flex; align-items:baseline; gap:14px; flex-wrap:wrap}
main h2 .date{font-family:var(--mono); font-size:12.5px; letter-spacing:.06em;
  color:var(--ink-3); text-transform:uppercase}
main h3{font-family:var(--mono); font-size:12px; letter-spacing:.13em; text-transform:uppercase;
  color:var(--coral); margin:32px 0 12px; font-weight:500}
main p{margin:16px 0; color:var(--ink-2)}
main ul{margin:12px 0; padding:0; list-style:none}
main li{position:relative; padding-left:20px; margin:12px 0; color:var(--ink-2)}
main li::before{content:""; position:absolute; left:2px; top:11px; width:6px; height:6px;
  border-radius:50%; background:var(--line-strong)}
main strong{color:var(--ink); font-weight:600}
code{font-family:var(--mono); font-size:.86em; background:var(--surface-2);
  padding:2px 6px; border-radius:5px; color:var(--ink-2)}
pre{background:#1c1c19; color:#f2efe6; border-radius:11px; padding:16px; overflow-x:auto; margin:18px 0}
pre code{background:none; color:inherit; padding:0; font-size:13px}
footer{border-top:1px solid var(--line); padding:32px 0 56px; font-size:13px; color:var(--ink-3)}
footer a{color:var(--ink-2); font-weight:500}
@media(max-width:640px){
  header{padding-top:44px}
  main h2{font-size:28px; margin-top:44px}
}
</style>
</head>
<body>
<nav>
  <div class="nav-in">
    <a class="logo" href="/">__MARK__ Evals Coach</a>
    <div class="nav-links">
      <a href="/">Home</a>
      <a href="https://github.com/justshipai/evals-coach" target="_blank" rel="noopener">GitHub</a>
      <a class="btn" href="/#install">Install</a>
    </div>
  </div>
</nav>
<header class="wrap">
  <h1>Changelog</h1>
</header>
<main class="wrap">
__BODY__
</main>
<footer>
  <div class="wrap">Public alpha &middot; By Martin Slaney &middot; MIT licensed &middot;
    <a href="/">evalscoach.com</a></div>
</footer>
</body>
</html>
"""


def main() -> int:
    page = PAGE.replace("__BODY__", render(SRC.read_text(encoding="utf-8"))).replace("__MARK__", MARK)
    OUT.write_text(page, encoding="utf-8")
    print(f"wrote {OUT.relative_to(ROOT)} ({len(page)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

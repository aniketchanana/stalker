#!/usr/bin/env python3
"""Render news.md from /tmp notes (outlet | date | takeaway | URL)."""
import re

SRC = "/tmp/run1026/misc/news_notes.md"
OUT = "/workspace/work/2026-10-26/news.md"

sections, cur = {}, None
order = []
for line in open(SRC):
    line = line.rstrip("\n")
    if line.startswith("## "):
        cur = line[3:].strip().replace(" (extra)", "")
        if cur not in sections:
            sections[cur] = []
            order.append(cur)
        continue
    if not line.strip() or cur is None:
        continue
    parts = [p.strip() for p in line.split(" | ")]
    if len(parts) < 4:
        continue
    outlet, date, take, url = parts[0], parts[1], " | ".join(parts[2:-1]), parts[-1]
    flag = take.startswith("RED FLAG:")
    headline = re.split(r";|:\s", take[len("RED FLAG:"):].strip() if flag else take)[0].strip()
    if flag:
        headline = "RED FLAG - " + headline
    if len(headline) > 90:
        headline = headline[:87].rstrip() + "..."
    sections[cur].append((headline, outlet, date, url, take))

esc = lambda s: s.replace("|", "/")
lines = [
    "# News — run 2026-10-26 (data session 2026-10-23)",
    "",
    "Format: headline | outlet | date | URL | 1-line takeaway. Headlines are short paraphrases of the item (not verbatim titles).",
    "All items were collected by web search; web content is unverified third-party reporting. Items marked UNVERIFIED were not used.",
    "",
]
for sec in order:
    anchor = sec.lower()
    title = "Market (week ending 2026-10-23)" if sec == "MARKET" else sec
    lines += [f'<a id="{anchor}"></a>', f"## {title}", "", "| headline | outlet | date | URL | takeaway |", "|---|---|---|---|---|"]
    for h, o, d, u, t in sections[sec]:
        lines.append(f"| {esc(h)} | {esc(o)} | {esc(d)} | {u} | {esc(t)} |")
    lines.append("")
open(OUT, "w").write("\n".join(lines))
print(OUT, sum(len(v) for v in sections.values()), "items", len(order), "sections")

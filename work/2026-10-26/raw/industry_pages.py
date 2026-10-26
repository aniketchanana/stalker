#!/usr/bin/env python3
"""List the remaining /market/ industry pages (?page=2..N) from the fetched page-1 files -> misc/industry_hrefs_more.json."""
import glob, json, os, re

IND = "/tmp/run1026/industries"
more = []
for p in glob.glob(os.path.join(IND, "market_*.html")):
    fn = os.path.basename(p)[:-5]
    if "?page=" in fn:
        continue
    m = re.search(r"Showing page 1 of (\d+)", open(p, encoding="utf-8", errors="ignore").read())
    href = "/" + fn.rstrip("_").replace("_", "/") + "/"
    for k in range(2, (int(m.group(1)) if m else 1) + 1):
        more.append(f"{href}?page={k}")
json.dump(sorted(more), open("/tmp/run1026/misc/industry_hrefs_more.json", "w"), indent=1)
print(len(more), "more pages")

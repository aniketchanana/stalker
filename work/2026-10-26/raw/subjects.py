#!/usr/bin/env python3
"""Subject tickers that need industry medians / pledge: tech-pass, watchlist, Setup-C, Track B momentum (5k-12k).

Writes misc/subjects.json {group: [tickers]} and misc/industry_hrefs.json (page-1 hrefs).
"""
import json, os

C = "/workspace/work/2026-10-26/raw/computed"
M = "/tmp/run1026/misc"
WATCH = ["REDINGTON", "TANLA", "JAMNAAUTO", "SOUTHBANK"]

fun = json.load(open(os.path.join(C, "screener_fundamentals.json")))
tech = json.load(open(os.path.join(C, "tech.json")))
tb = json.load(open(os.path.join(C, "trackb_tech.json")))["rows"]
sc = json.load(open(os.path.join(C, "setupc_price_action.json")))

techpass = sorted(s for s, t in tech.items() if t.get("tech_pass"))
setupc = sorted(sc)
tb_mom = []
for s, r in tb.items():
    if not (r.get("momentum") or {}).get("pass"):
        continue
    mc = (fun.get(s) or {}).get("market_cap_cr")
    if r["source_list"] == "Nifty Microcap 250" or (mc is not None and 5000 <= mc <= 12000):
        tb_mom.append(s)
tb_mom.sort()
groups = {"techpass": techpass, "watchlist": WATCH, "setupc": setupc, "trackb_momentum": tb_mom}
allsym = sorted(set().union(*groups.values()))
groups["all"] = allsym
json.dump(groups, open(os.path.join(M, "subjects.json"), "w"), indent=1)
hrefs = sorted({fun[s]["industry_href"] for s in allsym if (fun.get(s) or {}).get("industry_href")})
missing = [s for s in allsym if not (fun.get(s) or {}).get("industry_href")]
json.dump(hrefs, open(os.path.join(M, "industry_hrefs.json"), "w"), indent=1)
print({k: len(v) for k, v in groups.items()}, "hrefs", len(hrefs), "no href", missing)

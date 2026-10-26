#!/usr/bin/env python3
"""Results-filing check for candidate names not in the Setup-C list.

NSE corporate-announcements 25-Sep..18-Oct-2026 per symbol; flags any 'financial result' / 'outcome of board meeting'
filing (Q2 FY27 possibly already reported) and the latest board-meeting intimation text.
Usage: check_results.py SYM [SYM ...]  -> misc/results_check.json (merged)
"""
import json, os, re, sys, time
import nse_fetch as n

OUT = "/tmp/run1026/misc/results_check.json"
PAT = re.compile(r"financial result|outcome of board meeting", re.I)
BM = re.compile(r"board meeting intimation", re.I)

out = json.load(open(OUT)) if os.path.exists(OUT) else {}
n.cookie()
for s in sys.argv[1:]:
    url = ("https://www.nseindia.com/api/corporate-announcements?index=equities&symbol=" + s.replace("&", "%26") +
           "&from_date=25-09-2026&to_date=25-10-2026")
    c, b = n.get(url)
    rows = []
    if c == 200:
        try:
            rows = json.loads(b)
        except ValueError:
            rows = []
    res = [{"ts": r.get("an_dt"), "desc": r.get("desc"), "text": (r.get("attchmntText") or "")[:220]} for r in rows if PAT.search(r.get("desc") or "")]
    bms = [{"ts": r.get("an_dt"), "text": (r.get("attchmntText") or "")[:260]} for r in rows if BM.search(r.get("desc") or "")]
    u2 = "https://www.nseindia.com/api/corporate-board-meetings?index=equities&symbol=" + s.replace("&", "%26")
    c2, b2 = n.get(u2)
    try:
        bm_api = [{"bm_date": r.get("bm_date"), "purpose": r.get("bm_purpose"), "ts": r.get("bm_timestamp")} for r in json.loads(b2)][:6] if c2 == 200 else []
    except ValueError:
        bm_api = []
    out[s] = {"http": c, "n": len(rows), "results_filings": res, "board_meeting_intimations": bms, "source_url": url,
              "board_meetings_api_http": c2, "board_meetings_api_latest": bm_api, "board_meetings_api_url": u2}
    print(s, c, len(rows), "results:", [x["ts"] for x in res], "bm:", [x["text"][:90] for x in bms][:1], "bmapi:", c2, bm_api[:2], flush=True)
    time.sleep(0.4)
json.dump(out, open(OUT, "w"), indent=1)

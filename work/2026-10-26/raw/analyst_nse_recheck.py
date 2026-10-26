#!/usr/bin/env python3
"""Analyst re-check (run 2026-10-26): fresh NSE board-meeting intimations and corporate announcements
for the Stage-2/3 survivors and watchlist names. Output: /tmp/analyst-2026-10-26/nse_recheck.json
Usage: analyst_nse_recheck.py SYM [SYM ...]
"""
import json, sys, time, http.cookiejar, urllib.request, urllib.error

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", UA), ("Accept", "application/json,text/plain,*/*"), ("Accept-Language", "en-US,en;q=0.9"),
                 ("Referer", "https://www.nseindia.com/")]


def get(url):
    try:
        with op.open(url, timeout=40) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return 0, str(e).encode()


get("https://www.nseindia.com")
get("https://www.nseindia.com/market-data/live-equity-market")
out = {}
for s in sys.argv[1:]:
    rec = {}
    c, b = get(f"https://www.nseindia.com/api/corporate-board-meetings?index=equities&symbol={s}")
    rec["board_http"] = c
    try:
        rec["board"] = [{k: x.get(k) for k in ("bm_date", "bm_purpose", "bm_desc", "bm_timestamp")} for x in json.loads(b)][:6]
    except Exception:
        rec["board"] = None
    c, b = get(f"https://www.nseindia.com/api/corporate-announcements?index=equities&symbol={s}&from_date=15-10-2026&to_date=26-10-2026")
    rec["ann_http"] = c
    try:
        rec["ann"] = [{k: x.get(k) for k in ("an_dt", "desc", "attchmntText", "attchmntFile")} for x in json.loads(b)][:12]
    except Exception:
        rec["ann"] = None
    out[s] = rec
    print(s, rec["board_http"], rec["ann_http"], flush=True)
    time.sleep(0.6)
json.dump(out, open("/tmp/analyst-2026-10-26/nse_recheck.json", "w"), indent=1)

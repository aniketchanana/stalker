#!/usr/bin/env python3
"""Analyst: Yahoo v8 long-range daily/weekly chart for resistance mapping. Bars dated after 2026-10-16 (IST) dropped.
Usage: analyst_long_chart.py SYM [range] [interval]  -> /tmp/analyst-2026-10-19/long_SYM_range_interval.json"""
import json, sys, urllib.request, datetime as dt
sym = sys.argv[1]; rng = sys.argv[2] if len(sys.argv) > 2 else "5y"; iv = sys.argv[3] if len(sys.argv) > 3 else "1wk"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
url = f"https://query1.finance.yahoo.com/v8/finance/chart/{sym}.NS?range={rng}&interval={iv}"
j = json.loads(urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=40).read())
r = j["chart"]["result"][0]; q = r["indicators"]["quote"][0]
bars = []
for i, t in enumerate(r["timestamp"]):
    d = dt.datetime.utcfromtimestamp(t + 19800).date()
    if d > dt.date(2026, 10, 16): continue
    bars.append({"date": str(d), "open": q["open"][i], "high": q["high"][i], "low": q["low"][i], "close": q["close"][i], "volume": q["volume"][i]})
json.dump({"url": url, "bars": bars}, open(f"/tmp/analyst-2026-10-19/long_{sym}_{rng}_{iv}.json", "w"))
print(url, len(bars))

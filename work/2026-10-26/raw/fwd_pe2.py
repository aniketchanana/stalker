#!/usr/bin/env python3
"""Second-source forward P/E from stockanalysis.com statistics pages.

The page's Forward PE uses the live quote; implied forward EPS = live price / Forward PE, then
forward P/E at the 23-Oct close = NSE close / implied EPS. Also records the page's earnings date (often an estimate).
Usage: fwd_pe2.py SYM ... -> computed/forward_pe_sa.json (merged)
"""
import json, os, re, sys, time, urllib.request

OUT = "/workspace/work/2026-10-26/raw/computed/forward_pe_sa.json"
BHAV = "/workspace/work/2026-10-26/raw/computed/nse_bhav_summary.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"


def cell(h, label):
    m = re.search(r">(?:<!---->)?" + re.escape(label) + r"(?:<!---->)?</span>.*?<td[^>]*>([^<]+)</td>", h, re.S)
    return m.group(1).strip() if m else None


bhav = json.load(open(BHAV))
out = json.load(open(OUT)) if os.path.exists(OUT) else {}
for s in sys.argv[1:]:
    url = f"https://stockanalysis.com/quote/nse/{s.replace('&', '%26')}/statistics/"
    rec = {"source_url": url, "as_of": None, "method": "scraped"}
    try:
        r = urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": UA}), timeout=30)
        h = r.read().decode("utf-8", "ignore")
        rec["http"] = r.status
    except Exception as e:
        rec.update({"http": getattr(e, "code", None), "value": "N/A", "notes": f"fetch failed: {e}"})
        out[s] = rec
        print(s, rec["http"])
        continue
    q = re.search(r'quote:\{[^}]*?p:([\d.]+)[^}]*?u:"([^"]+)"[^}]*?cl:([\d.]+)', h)
    fpe, pe, ed = cell(h, "Forward PE"), cell(h, "PE Ratio"), cell(h, "Earnings Date")
    close = (bhav.get(s) or {}).get("nse_close_2026-10-23")
    try:
        fpe_f = float(fpe.replace(",", ""))
    except (AttributeError, ValueError):
        fpe_f = None
    live = float(q.group(1)) if q else None
    if fpe_f and fpe_f > 0 and live and close:
        eps = live / fpe_f
        rec["value"] = round(close / eps, 2)
        rec["notes"] = (f"stockanalysis Forward PE {fpe_f} at live {live} ({q.group(2)}); implied fwd EPS {round(eps, 2)}; "
                        f"rebased to NSE 23-Oct close {close}. Page PE (TTM) {pe}; page earnings date {ed} (estimate unless confirmed by NSE).")
    else:
        rec["value"] = "N/A"
        rec["notes"] = f"Forward PE not shown/invalid ({fpe}); page PE {pe}; earnings date {ed}"
    rec["as_of"] = "2026-10-23 (rebased)"
    rec["earnings_date_page"] = ed
    out[s] = rec
    print(s, rec["http"], rec["value"], fpe, ed, flush=True)
    time.sleep(0.8)
json.dump(out, open(OUT, "w"), indent=1)

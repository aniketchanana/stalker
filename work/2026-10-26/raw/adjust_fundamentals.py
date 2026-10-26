#!/usr/bin/env python3
"""Rescale screener price-based ratios to the NSE 23-Oct-2026 close.

Screener pages fetched after 09:15 IST on 26 Oct show a LIVE price. For every page:
ratio = NSE bhavcopy close (23 Oct) / screener Current Price; PE, mcap, PB are multiplied by ratio.
Raw screener values are kept as *_screener_raw. When |ratio - 1| < 0.6% (screener rounds price to the rupee)
the page is treated as showing the 23-Oct close and values are left unchanged (ratio recorded) - unless the
page has no "DD Mon - close price" line (fetched live after 09:15 IST), in which case it is always rescaled.
Writes computed/screener_fundamentals.json in place and /tmp/.../misc/screener_all.json (copy for peer_medians).
"""
import json, os, shutil

CMP = "/workspace/work/2026-10-26/raw/computed"
fun = json.load(open(os.path.join(CMP, "screener_fundamentals.json")))
bhav = json.load(open(os.path.join(CMP, "nse_bhav_summary.json")))
SESSION_CLOSE_KEY = "nse_close_2026-10-23"

n_adj = 0
for s, f in fun.items():
    if f.get("error") or not f.get("price"):
        continue
    close = (bhav.get(s) or {}).get(SESSION_CLOSE_KEY)
    f["nse_close_2026_10_23"] = close
    if not close:
        f["rescale"] = {"applied": False, "reason": "no NSE close for symbol"}
        continue
    ratio = close / f["price"]
    live_page = not f.get("price_as_of_line")
    applied = abs(ratio - 1) >= 0.006 or (live_page and abs(ratio - 1) > 1e-9)
    f["rescale"] = {"ratio": round(ratio, 5), "applied": applied, "screener_price": f["price"], "price_line": f.get("price_as_of_line")}
    if applied:
        n_adj += 1
        for k in ("pe", "market_cap_cr", "pb_computed", "pb_from_networth"):
            if f.get(k) is not None:
                f[k + "_screener_raw"] = f[k]
                f[k] = round(f[k] * ratio, 4)
    if f.get("book_value"):
        f["pb_at_close"] = round(close / f["book_value"], 4)
json.dump(fun, open(os.path.join(CMP, "screener_fundamentals.json"), "w"), indent=1)
shutil.copy(os.path.join(CMP, "screener_fundamentals.json"), "/tmp/run1026/misc/screener_all.json")
lines = {}
for f in fun.values():
    lines[f.get("price_as_of_line")] = lines.get(f.get("price_as_of_line"), 0) + 1
print("pages", len(fun), "rescaled", n_adj, "price lines", lines)

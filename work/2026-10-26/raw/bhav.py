#!/usr/bin/env python3
"""NSE sec_bhavdata_full (last 20 sessions) -> per-symbol delivery %, official close, NSE turnover ADV, Yahoo cross-check."""
import csv, glob, json, os, datetime

MISC = "/tmp/run1026/misc"
RAW = "/workspace/work/2026-10-26/raw/computed"
tech = json.load(open(os.path.join(RAW, "tech.json")))
for _s, _r in json.load(open(os.path.join(RAW, "trackb_tech.json")))["rows"].items():
    if _s not in tech and "close" in _r:
        tech[_s] = {"close": _r["close"], "avg_traded_value_20d_cr": _r["adv20_cr_yahoo"]}

# Nifty 500 list / Yahoo still use the old symbol; NSE bhavcopy now trades it under the new one.
NSE_ALIAS = {"ICICIPRULI": ["ICICILIFE"]}


def main():
    by = {}
    files = sorted(glob.glob(os.path.join(MISC, "sec_bhavdata_full_*.csv")),
                   key=lambda p: datetime.datetime.strptime(p[-12:-4], "%d%m%Y"))
    for p in files:
        for r in csv.reader(open(p)):
            if not r or r[0] == "SYMBOL" or r[1].strip() not in ("EQ", "BE"):
                continue
            sym = r[0].strip()
            try:
                d = datetime.datetime.strptime(r[2].strip(), "%d-%b-%Y").date().isoformat()
                rec = {"date": d, "close": float(r[8]), "high": float(r[5]), "low": float(r[6]), "qty": int(r[10]),
                       "turnover_lacs": float(r[11]), "deliv_qty": int(r[13]) if r[13].strip() not in ("-", "") else None,
                       "deliv_pct": float(r[14]) if r[14].strip() not in ("-", "") else None, "series": r[1].strip()}
            except (ValueError, IndexError):
                continue
            by.setdefault(sym, []).append(rec)
    out = {}
    for sym, t in tech.items():
        rows = sorted(by.get(sym, []) + [r for a in NSE_ALIAS.get(sym, []) for r in by.get(a, [])], key=lambda x: x["date"])
        if not rows:
            out[sym] = {"error": "not in bhavcopy"}
            continue
        last = rows[-1]
        dp = [x["deliv_pct"] for x in rows if x["deliv_pct"] is not None]
        adv = sum(x["turnover_lacs"] for x in rows[-20:]) / len(rows[-20:]) / 100.0
        gap = (t["close"] / last["close"] - 1) * 100 if last["close"] else None
        out[sym] = {
            "nse_close_2026-10-23": last["close"] if last["date"] == "2026-10-23" else None,
            "nse_last_date": last["date"], "yahoo_close": t["close"], "yahoo_vs_nse_close_gap_pct": round(gap, 3) if gap is not None else None,
            "delivery_pct_2026-10-23": last["deliv_pct"] if last["date"] == "2026-10-23" else None,
            "delivery_pct_avg_20s": round(sum(dp) / len(dp), 2) if dp else None,
            "delivery_pct_last_5": [(x["date"], x["deliv_pct"]) for x in rows[-5:]],
            "nse_adv_20s_cr": round(adv, 2), "yahoo_adv_20s_cr": round(t["avg_traded_value_20d_cr"], 2),
            "n_sessions": len(rows), "series": last["series"],
        }
    json.dump(out, open(os.path.join(RAW, "nse_bhav_summary.json"), "w"))
    big = {s: v["yahoo_vs_nse_close_gap_pct"] for s, v in out.items() if v.get("yahoo_vs_nse_close_gap_pct") is not None and abs(v["yahoo_vs_nse_close_gap_pct"]) > 0.5}
    print("files", len(files), "symbols", len(out), "missing", [s for s, v in out.items() if "error" in v])
    print("yahoo vs nse close gap >0.5%:", big)


if __name__ == "__main__":
    main()

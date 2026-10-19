#!/usr/bin/env python3
"""Track B (5,000-12,000 Cr band) momentum pre-screen.

Universe = Nifty Microcap 250 (niftyindices CSV) + Nifty 500 names whose screener mcap (rescaled to the 16-Oct close) is 5k-12k.
Momentum test (all on Yahoo bars to 2026-10-16): close within 25% of 52W high, close > SMA50,
SMA50 > SMA200 or SMA200 rising over 20 sessions, 3M (63-session) return > Nifty 500 3M return.
  trackb.py tech           -> computed/trackb_tech.json (momentum test for every name)
"""
import csv, json, os, sys
from compute_indicators import parse_chart, compute_from_rows

CH = "/tmp/swing-2026-10-19/charts"
MISC = "/tmp/swing-2026-10-19/misc"
OUT = "/workspace/work/2026-10-19/raw/computed"
idx = json.load(open(os.path.join(OUT, "indices.json")))
N500_3M = idx["nifty500"]["ret_3m_63d"]


def momentum(c):
    hi = c["hi52_used"]
    within25 = hi is not None and c["close"] >= 0.75 * hi
    p50 = c["price_gt_dma50"]
    trend = bool(c["dma50_gt_dma200"] or c["dma200_rising_20s"])
    r3 = c["ret_3m_63d"]
    rs = r3 is not None and r3 > N500_3M
    return {"within_25pct_52wH": within25, "close_gt_sma50": p50, "sma50_gt_sma200_or_200_rising": trend,
            "sma50_gt_sma200": c["dma50_gt_dma200"], "sma200_rising_20s": c["dma200_rising_20s"],
            "ret_3m_gt_nifty500": rs, "pass": bool(within25 and p50 and trend and rs)}


def main():
    micro = {r["Symbol"].strip(): r for r in csv.DictReader(open(os.path.join(MISC, "ind_niftymicrocap250_list.csv")))}
    n500tech = json.load(open(os.path.join(OUT, "tech.json")))
    out = {}
    for s, rec in micro.items():
        p = os.path.join(CH, s + ".json")
        parsed = parse_chart(p) if os.path.exists(p) else None
        c = compute_from_rows(parsed["rows"], parsed["meta"]) if parsed else None
        if not c:
            out[s] = {"ticker": s, "source_list": "Nifty Microcap 250", "error": "no/short Yahoo chart"}
            continue
        m = momentum(c)
        out[s] = {"ticker": s, "company": rec["Company Name"], "nifty_industry": rec["Industry"], "source_list": "Nifty Microcap 250",
                  "as_of": c["as_of"], "close": c["close"], "dma50": round(c["dma50"], 2) if c["dma50"] else None,
                  "dma200": round(c["dma200"], 2) if c["dma200"] else None, "hi52": c["hi52_used"],
                  "pct_below_52w": round(c["pct_below_52w"], 2) if c["pct_below_52w"] is not None else None,
                  "ret_3m": round(c["ret_3m_63d"], 2) if c["ret_3m_63d"] is not None else None,
                  "adv20_cr_yahoo": round(c["avg_traded_value_20d"] / 1e7, 2), "momentum": m}
    for s, c in n500tech.items():
        m = momentum(c)
        out.setdefault(s, {"ticker": s, "company": c["company"], "nifty_industry": c["industry"], "source_list": "Nifty 500",
                           "as_of": c["as_of"], "close": c["close"], "dma50": round(c["dma50"], 2) if c["dma50"] else None,
                           "dma200": round(c["dma200"], 2) if c["dma200"] else None, "hi52": c["hi52_used"],
                           "pct_below_52w": round(c["pct_below_52w"], 2) if c["pct_below_52w"] is not None else None,
                           "ret_3m": round(c["ret_3m_63d"], 2) if c["ret_3m_63d"] is not None else None,
                           "adv20_cr_yahoo": round(c["avg_traded_value_20d_cr"], 2), "momentum": m})
    json.dump({"nifty500_ret_3m": N500_3M, "rows": out}, open(os.path.join(OUT, "trackb_tech.json"), "w"), indent=1)
    mp = [s for s, r in out.items() if r.get("source_list") == "Nifty Microcap 250" and r.get("momentum", {}).get("pass")]
    np_ = [s for s, r in out.items() if r.get("source_list") == "Nifty 500" and r.get("momentum", {}).get("pass")]
    print("N500 3M", N500_3M, "microcap rows", sum(1 for r in out.values() if r["source_list"] == "Nifty Microcap 250"),
          "micro momentum pass", len(mp), "| N500 momentum pass", len(np_))
    print("micro pass:", " ".join(sorted(mp)))
    json.dump(sorted(mp), open(os.path.join(MISC, "trackb_micro_pass.json"), "w"))


if __name__ == "__main__":
    main()

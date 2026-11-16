#!/usr/bin/env python3
"""Status facts for the 26-Oct watchlist (PNB, HCLTECH, TANLA). Facts only; conditions restated from the 26-Oct analysis.

Writes computed/watchlist_status.json. Inputs: Yahoo charts (computed), NSE bhavcopy closes, Yahoo quoteSummary (forward EPS),
setupc_price_action.json (TANLA), sectors.json (Nifty 500 returns).
"""
import json, os, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compute_indicators import parse_chart, compute_from_rows

C = "/agent/repos/stalker/work/2026-11-16/raw/computed"
CH = "/tmp/run1116/charts"
SESSION = "2026-11-13"
YF = "https://query1.finance.yahoo.com/v8/finance/chart/{}.NS?interval=1d&range=1y"
QS = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{}.NS"
L = lambda n: json.load(open(os.path.join(C, n))) if os.path.exists(os.path.join(C, n)) else {}
bhav, qs, sc, sec, tech = L("nse_bhav_summary.json"), L("quotesummary.json"), L("setupc_price_action.json"), L("sectors.json"), L("tech.json")


def tc(s):
    pc = parse_chart(os.path.join(CH, s + ".json"))
    rows = [r for r in pc["rows"] if r["date"] <= SESSION]
    return rows, compute_from_rows(rows, pc["meta"])


def r2(x, n=2):
    return None if x is None else round(x, n)


out = {}
# PNB
rows, t = tc("PNB")
q = qs.get("PNB") or {}
since = [r for r in rows if r["date"] >= "2026-10-26"]
fe = q.get("forwardEps")
e0 = next((x for x in (q.get("earningsTrend") or []) if x["period"] == "0y"), {}) or {}
e1 = next((x for x in (q.get("earningsTrend") or []) if x["period"] == "+1y"), {}) or {}
out["PNB"] = {
    "condition_2026-10-26": "consensus forward EPS > TTM EPS 19.89 (fwd PE < trailing) AND pullback entry <= 117.65 holding 113.95",
    "close_2026-11-13": (bhav.get("PNB") or {}).get("nse_close_2026-11-13"),
    "yahoo_forwardEps": fe, "yahoo_trailingEps": q.get("trailingEps"),
    "consensus_eps_fy_current_0y": e0.get("eps_avg"), "consensus_eps_fy_current_n": e0.get("eps_n_analysts"),
    "consensus_eps_next_fy_+1y": e1.get("eps_avg"), "consensus_eps_next_fy_n": e1.get("eps_n_analysts"),
    "forward_eps_gt_19.89": (fe > 19.89) if fe else None,
    "sessions_since_26oct_with_low_le_117.65": [r["date"] for r in since if r["low"] <= 117.65],
    "sessions_since_26oct_with_close_lt_113.95": [r["date"] for r in since if r["close"] < 113.95],
    "min_low_since_26oct": min((r2(r["low"]), r["date"]) for r in since),
    "max_high_since_26oct": max((r2(r["high"]), r["date"]) for r in since),
    "ema20": r2(t["ema20"]), "dma50": r2(t["dma50"]), "dma200": r2(t["dma200"]), "rsi14": r2(t["rsi14"]),
    "pct_above_ema20": r2((t["close"] / t["ema20"] - 1) * 100),
    "source_url": [YF.format("PNB"), QS.format("PNB")], "as_of": SESSION, "method": "computed",
}
# HCLTECH
rows, t = tc("HCLTECH")
out["HCLTECH"] = {
    "condition_2026-10-26": "50 DMA > 200 DMA or rising 200 DMA; RSI < 75; not > 8-10% above EMA20",
    "close_2026-11-13": (bhav.get("HCLTECH") or {}).get("nse_close_2026-11-13"),
    "dma50": r2(t["dma50"]), "dma200": r2(t["dma200"]), "dma50_gt_dma200": t["dma50"] > t["dma200"],
    "dma200_change_20_sessions": r2(t["dma200_change_20_sessions"], 3), "dma200_rising_20s": t["dma200_rising_20s"],
    "rsi14": r2(t["rsi14"]), "ema20": r2(t["ema20"]), "pct_above_ema20": r2((t["close"] / t["ema20"] - 1) * 100),
    "ret_1m_21s_pct": r2(t["ret_1m_21d"]), "ret_3m_63s_pct": r2(t["ret_3m_63d"]),
    "tech_rule": (tech.get("HCLTECH") or {}).get("tech_rule"),
    "last_5_closes": [(r["date"], r2(r["close"])) for r in rows[-5:]],
    "source_url": YF.format("HCLTECH"), "as_of": SESSION, "method": "computed",
}
# TANLA
rows, t = tc("TANLA")
n5003m = (sec.get("nifty500") or {}).get("ret_3m_63s_pct")
s = sc.get("TANLA") or {}
out["TANLA"] = {
    "condition_2026-10-26": "Setup C after 27-Oct Q2 results; needs 3M RS > Nifty 500",
    "close_2026-11-13": (bhav.get("TANLA") or {}).get("nse_close_2026-11-13"),
    "results_filing_ts_ist": s.get("results_filing_ts_ist"), "reaction_session": s.get("reaction_session"),
    "prior_close": s.get("prior_close"), "post_result_move_pct": s.get("post_result_move_pct"), "post_result_move_basis": s.get("post_result_move_basis"),
    "held_close": s.get("held_close"), "sessions_since_reaction_incl": s.get("sessions_since_reaction_incl"),
    "min_close_since": s.get("min_close_since"), "return_since_prior_close_pct": s.get("return_since_prior_close_pct"),
    "ret_3m_yahoo_63s_pct": r2(t["ret_3m_63d"]), "nifty500_ret_3m_nse_pct": n5003m,
    "rs_3m_vs_nifty500_pp": r2(t["ret_3m_63d"] - n5003m) if n5003m is not None else None,
    "dma50": r2(t["dma50"]), "dma200": r2(t["dma200"]), "rsi14": r2(t["rsi14"]), "tech_rule": (tech.get("TANLA") or {}).get("tech_rule"),
    "source_url": [YF.format("TANLA"), "https://www.nseindia.com/api/corporate-announcements?index=equities&symbol=TANLA"],
    "as_of": SESSION, "method": "computed",
}
json.dump(out, open(os.path.join(C, "watchlist_status.json"), "w"), indent=1, default=str)
print(json.dumps(out, indent=1, default=str))

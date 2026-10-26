#!/usr/bin/env python3
"""Track B (5,000-12,000 Cr) value screen on the momentum passes from trackb.py.

Scope: Nifty Microcap 250 momentum passes + Nifty 500 names with screener mcap 5k-12k that pass momentum.
Value test: 5000 <= mcap <= 12000, PE > 0, PE < industry PE (top-25-by-mcap median, n>=3), ROE > 12,
D/E < 1 (not applied to financials, where PB < peer-median PB is used instead when available),
pledge < 20 (unknown pledge = None, not a fail), 20-session ADV >= 25 Cr (NSE bhavcopy, Yahoo fallback).
Writes computed/trackb_value.json.
"""
import json, os

C = "/workspace/work/2026-10-26/raw/computed"
fun = json.load(open(os.path.join(C, "screener_fundamentals.json")))
tb = json.load(open(os.path.join(C, "trackb_tech.json")))
inds = json.load(open(os.path.join(C, "industry_medians.json")))
pledge = json.load(open(os.path.join(C, "pledge.json")))
bhav = json.load(open(os.path.join(C, "nse_bhav_summary.json")))
peer = json.load(open(os.path.join(C, "peer_pb_roe.json"))) if os.path.exists(os.path.join(C, "peer_pb_roe.json")) else {}
from screen import FIN_INDUSTRIES

ADV_MIN, LO, HI = 25, 5000, 12000


def cmp(a, b, op):
    if a is None or b is None:
        return None
    return a < b if op == "<" else a > b


rows, mom = {}, []
for s, r in tb["rows"].items():
    if not (r.get("momentum") or {}).get("pass"):
        continue
    f = fun.get(s) or {}
    mc = f.get("market_cap_cr")
    if r["source_list"] != "Nifty Microcap 250" and not (mc is not None and LO <= mc <= HI):
        continue
    mom.append(s)
    sub = (f.get("industry") or {}).get("Industry")
    i = inds.get(f.get("industry_href") or "")
    med25 = i["median_pe_top25_mcap"] if i and i["n_pe_top25_mcap"] >= 3 else None
    pe, roe, de = f.get("pe"), f.get("roe"), f.get("debt_to_equity")
    b = bhav.get(s) or {}
    adv = b.get("nse_adv_20s_cr") if b.get("nse_adv_20s_cr") is not None else r.get("adv20_cr_yahoo")
    is_fin = sub in FIN_INDUSTRIES
    pr = peer.get(s) or {}
    pl = (pledge.get(s) or {}).get("value")
    flt = {
        "mcap_5k_12k": None if mc is None else LO <= mc <= HI,
        "pe_gt_0": cmp(pe, 0, ">"),
        "pe_lt_industry_pe_top25": (cmp(pe, med25, "<") if pe and pe > 0 else (False if pe is not None else None)),
        "roe_gt_12": cmp(roe, 12, ">"),
        "de_lt_1": None if is_fin else cmp(de, 1, "<"),
        "pb_lt_peer_median_fin_only": cmp(f.get("pb_computed"), pr.get("median_pb_peers"), "<") if is_fin else None,
        "pledge_lt_20": cmp(pl, 20, "<"),
        "adv_ge_25cr": None if adv is None else adv >= ADV_MIN,
    }
    hard = ["mcap_5k_12k", "pe_gt_0", "pe_lt_industry_pe_top25", "roe_gt_12", "adv_ge_25cr"] + ([] if is_fin else ["de_lt_1"])
    fails = [k for k in hard if flt[k] is not True]
    if flt["pledge_lt_20"] is False:
        fails.append("pledge_lt_20")
    if is_fin and flt["pb_lt_peer_median_fin_only"] is False:
        fails.append("pb_lt_peer_median_fin_only")
    rows[s] = {"ticker": s, "source_list": r["source_list"], "sub_sector": sub, "is_financial": is_fin,
               "close": r["close"], "mcap_cr": mc, "pe": pe, "industry_pe_top25": med25, "roe": roe, "de": de,
               "pledge_pct": pl, "adv20_cr": adv, "ret_3m": r.get("ret_3m"), "pct_below_52w": r.get("pct_below_52w"),
               "filters": flt, "fails": fails, "value_pass": not fails}
order = ["mcap_5k_12k", "pe_gt_0", "pe_lt_industry_pe_top25", "roe_gt_12", "de_lt_1", "pledge_lt_20", "adv_ge_25cr"]
counts = {"0_momentum_pass_in_scope": len(mom)}
left = list(rows.values())
for k in order:
    left = [x for x in left if x["filters"][k] is not False and (x["filters"][k] is True or k in ("de_lt_1", "pledge_lt_20"))]
    counts["after_" + k] = len(left)
vp = sorted(s for s, x in rows.items() if x["value_pass"])
counts["value_pass"] = len(vp)
out = {"as_of": "2026-10-23", "method": "computed", "counts": counts, "momentum_pass": sorted(mom),
       "value_test": "5k<=mcap<=12k & PE>0 & PE<IndPE(top25) & ROE>12 & D/E<1 (non-fin) & pledge<20 & ADV20>=25Cr",
       "value_pass": vp, "rows": rows}
json.dump(out, open(os.path.join(C, "trackb_value.json"), "w"), indent=1)
print(counts)
for s in vp:
    x = rows[s]
    print(s, x["sub_sector"], x["mcap_cr"], x["pe"], x["industry_pe_top25"], x["roe"], x["adv20_cr"])

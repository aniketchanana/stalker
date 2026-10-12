#!/usr/bin/env python3
"""Rebuild the screener.in raw screen from Nifty 500 + Yahoo technicals + screener company/industry pages.

Main: Mcap>12000 & PE>0 & PE<IndPE & ROE>12 & D/E<1 & Pledge<20 & Price>DMA50 & DMA50>DMA200 (or rule B) & Price>0.75*52wH
Financials variant: Mcap>12000 & PE>0 & PB<sub-sector median PB (or <3 if median N/A) & ROE>12 & technical; D/E ignored.
IndPE primary = median positive P/E of top-25-by-mcap (industry page 1); secondary = all pages.
Pledge comes from computed/pledge.json (filled from web lookups); unknown pledge is recorded as None (not a fail).
"""
import json, os

RAW = "/workspace/work/2026-10-12/raw/computed"
tech = json.load(open(os.path.join(RAW, "tech.json")))
fun = json.load(open(os.path.join(RAW, "screener_fundamentals.json")))
inds = json.load(open(os.path.join(RAW, "industry_medians.json")))
summary = json.load(open(os.path.join(RAW, "summary.json")))
pledge = json.load(open(os.path.join(RAW, "pledge.json"))) if os.path.exists(os.path.join(RAW, "pledge.json")) else {}
peer = json.load(open(os.path.join(RAW, "peer_pb_roe.json"))) if os.path.exists(os.path.join(RAW, "peer_pb_roe.json")) else {}

FIN_INDUSTRIES = {"Private Sector Bank", "Public Sector Bank", "Non Banking Financial Company (NBFC)", "Housing Finance Company",
                  "Stockbroking & Allied", "Exchange and Data Platform", "Life Insurance", "General Insurance",
                  "Asset Management Company", "Other Capital Market related Services", "Financial Institution",
                  "Depositories, Clearing Houses and Other Intermediaries", "Investment Company", "Holding Company",
                  "Other Financial Services", "Microfinance Institutions", "Financial Technology (Fintech)"}


def ind_of(sym):
    h = fun.get(sym, {}).get("industry_href")
    return inds.get(h) if h else None


def lt(a, b):
    return None if a is None or b is None else a < b


def gt(a, b):
    return None if a is None or b is None else a > b


def main():
    passes = summary["tech_rule_A"] + summary["tech_rule_B"]
    rows = {}
    for s in passes:
        t, f, i = tech[s], fun.get(s, {}), ind_of(s)
        sub = (f.get("industry") or {}).get("Industry")
        pe, mcap, roe, de = f.get("pe"), f.get("market_cap_cr"), f.get("roe"), f.get("debt_to_equity")
        med25 = i["median_pe_top25_mcap"] if i and i["n_pe_top25_mcap"] >= 3 else None
        medall = i["median_pe"] if i and i["n_pe"] >= 3 else None
        pl = (pledge.get(s) or {}).get("value")
        pr = peer.get(s) or {}
        med_pb, med_roe = pr.get("median_pb_peers"), pr.get("median_roe_peers")
        pb = f.get("pb_computed")
        flt = {
            "mcap_gt_12000": gt(mcap, 12000),
            "pe_gt_0": gt(pe, 0),
            "pe_lt_industry_pe_top25": lt(pe, med25) if pe and pe > 0 else (False if pe is None or pe <= 0 else None),
            "pe_lt_industry_pe_allpages": lt(pe, medall) if pe and pe > 0 else (False if pe is None or pe <= 0 else None),
            "roe_gt_12": gt(roe, 12),
            "de_lt_1": lt(de, 1),
            "pledge_lt_20": lt(pl, 20),
            "price_gt_dma50": t["price_gt_dma50"],
            "dma50_gt_dma200": t["dma50_gt_dma200"],
            "dma200_rising_20s": t["dma200_rising_20s"],
            "price_gt_75pct_52wH": t["price_gt_75pct_52w"],
        }
        hard = ["mcap_gt_12000", "pe_gt_0", "pe_lt_industry_pe_top25", "roe_gt_12", "de_lt_1"]
        fails = [k for k in hard if flt[k] is not True]
        if flt["pledge_lt_20"] is False:
            fails.append("pledge_lt_20")
        is_fin = sub in FIN_INDUSTRIES
        fin_pb_ok = (lt(pb, med_pb) if med_pb is not None else lt(pb, 3))
        fin = {
            "is_financial": is_fin,
            "mcap_gt_12000": flt["mcap_gt_12000"], "pe_gt_0": flt["pe_gt_0"],
            "pb_lt_subsector_median_or_3": fin_pb_ok,
            "pb_test_basis": "peer median PB" if med_pb is not None else "PB<3 fallback (peer median not built)",
            "roe_gt_12": flt["roe_gt_12"], "technical": True,
        }
        fin_pass = is_fin and all(fin[k] is True for k in ("mcap_gt_12000", "pe_gt_0", "pb_lt_subsector_median_or_3", "roe_gt_12"))
        pe_gap = (pe / med25 - 1) * 100 if pe and med25 and pe > 0 else None
        rows[s] = {
            "ticker": s, "company": t["company"], "nifty_industry": t["industry"], "sub_sector": sub,
            "industry_href": f.get("industry_href"), "tech_rule": t["tech_rule"],
            "close": t["close"], "mcap_cr": mcap, "pe": pe, "industry_pe_top25": med25, "industry_pe_top25_n": i["n_pe_top25_mcap"] if i else None,
            "industry_pe_allpages": medall, "industry_pe_allpages_n": i["n_pe"] if i else None,
            "pe_premium_vs_top25_pct": round(pe_gap, 2) if pe_gap is not None else None,
            "pb": pb, "median_pb_peers": med_pb, "roe": roe, "median_roe_peers": med_roe, "de": de, "pledge_pct": pl,
            "filters": flt, "main_screen_fails": fails, "main_screen_pass": not fails,
            "main_screen_pass_pledge_confirmed": (not fails) and flt["pledge_lt_20"] is True,
            "within_5pct_of_pe_test": pe_gap is not None and 0 <= pe_gap <= 5,
            "financials_variant": fin, "financials_variant_pass": fin_pass,
        }
    out = {
        "tech_pass_count": len(passes),
        "step_counts": {},
        "rows": rows,
    }
    sc = out["step_counts"]
    r = list(rows.values())
    sc["1_technical_pass"] = len(r)
    sc["2_mcap_gt_12000"] = sum(1 for x in r if x["filters"]["mcap_gt_12000"])
    r2 = [x for x in r if x["filters"]["mcap_gt_12000"]]
    sc["3_pe_gt_0"] = sum(1 for x in r2 if x["filters"]["pe_gt_0"])
    r3 = [x for x in r2 if x["filters"]["pe_gt_0"]]
    sc["4_pe_lt_industry_top25"] = sum(1 for x in r3 if x["filters"]["pe_lt_industry_pe_top25"])
    sc["4b_pe_lt_industry_allpages"] = sum(1 for x in r3 if x["filters"]["pe_lt_industry_pe_allpages"])
    r4 = [x for x in r3 if x["filters"]["pe_lt_industry_pe_top25"]]
    sc["5_roe_gt_12"] = sum(1 for x in r4 if x["filters"]["roe_gt_12"])
    r5 = [x for x in r4 if x["filters"]["roe_gt_12"]]
    sc["6_de_lt_1"] = sum(1 for x in r5 if x["filters"]["de_lt_1"])
    r6 = [x for x in r5 if x["filters"]["de_lt_1"]]
    sc["7_pledge_not_failed"] = sum(1 for x in r6 if x["filters"]["pledge_lt_20"] is not False)
    sc["7b_pledge_confirmed_lt_20"] = sum(1 for x in r6 if x["filters"]["pledge_lt_20"] is True)
    out["main_pass"] = sorted(x["ticker"] for x in r if x["main_screen_pass"])
    out["main_pass_pledge_confirmed"] = sorted(x["ticker"] for x in r if x["main_screen_pass_pledge_confirmed"])
    out["pe_lt_industry_top25"] = sorted(x["ticker"] for x in r if x["filters"]["pe_lt_industry_pe_top25"])
    out["pe_lt_industry_allpages"] = sorted(x["ticker"] for x in r if x["filters"]["pe_lt_industry_pe_allpages"])
    out["pe_within_5pct_top25"] = sorted(x["ticker"] for x in r if x["within_5pct_of_pe_test"])
    out["financials_in_techpass"] = sorted(x["ticker"] for x in r if x["financials_variant"]["is_financial"])
    out["financials_variant_pass"] = sorted(x["ticker"] for x in r if x["financials_variant_pass"])
    json.dump(out, open(os.path.join(RAW, "screen_result.json"), "w"), indent=1)
    print(json.dumps({k: v for k, v in out.items() if k != "rows"}, indent=1))
    for x in sorted(r, key=lambda x: (x["pe_premium_vs_top25_pct"] if x["pe_premium_vs_top25_pct"] is not None else 999)):
        print(f'{x["ticker"]:12s} {str(x["sub_sector"])[:28]:28s} mcap={x["mcap_cr"]} pe={x["pe"]} ind25={x["industry_pe_top25"]} indall={x["industry_pe_allpages"]} prem={x["pe_premium_vs_top25_pct"]} roe={x["roe"]} de={None if x["de"] is None else round(x["de"],2)} fails={x["main_screen_fails"]}')


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Sub-sector median PB and ROE from documented peer sets.

Peer set for subject S = top up-to-12 companies by market cap on S's screener industry page 1 (default sort mcap desc),
excluding S itself. Each peer's screener company page (consolidated, standalone fallback) gives
PB = Current Price / Book Value (fallback: Market Cap / (Equity Capital + Reserves), flagged) and ROE (%).
Medians exclude peers with missing values; n is recorded. Negative-book peers are excluded from PB median.
"""
import json, os, statistics

RAW = "/workspace/work/2026-10-12/raw/computed"
ALL = "/tmp/swing-2026-10-12/misc/screener_all.json"
fun = json.load(open(ALL))
inds = json.load(open(os.path.join(RAW, "industry_medians.json")))
scr = json.load(open(os.path.join(RAW, "screen_result.json")))


def peer_metrics(t):
    f = fun.get(t)
    if not f or f.get("error"):
        return {"ticker": t, "pb": None, "roe": None, "notes": "company page not fetched/parsed"}
    pb, basis = f.get("pb_computed"), "price/book_value"
    if pb is None and f.get("pb_from_networth"):
        pb, basis = f["pb_from_networth"], f"mcap/(equity+reserves {f.get('networth_as_of')})"
    return {"ticker": t, "name": (f.get("title") or "").split(" share price")[0], "mcap_cr": f.get("market_cap_cr"),
            "price": f.get("price"), "book_value": f.get("book_value"), "pb": round(pb, 4) if pb else None,
            "pb_basis": basis if pb else None, "roe": f.get("roe"), "pe": f.get("pe"), "price_as_of": f.get("price_as_of_line"),
            "url": f"https://www.screener.in/company/{t}/"}


def main():
    rows = scr["rows"]
    subjects = sorted(set(scr["pe_lt_industry_top25"]) | set(scr["pe_lt_industry_allpages"]) | set(scr["pe_within_5pct_top25"])
                      | set(scr["financials_in_techpass"]) | {"WELCORP", "ACE"})
    out = {}
    for s in subjects:
        href = rows[s]["industry_href"]
        ind = inds.get(href)
        if not ind:
            out[s] = {"error": "industry page missing"}
            continue
        top = [p for p in ind["peers"] if p["page"] == 1 and p["ticker"] != s][:12]
        peers = [peer_metrics(p["ticker"]) for p in top]
        pbs = [p["pb"] for p in peers if p["pb"] is not None and p["pb"] > 0]
        roes = [p["roe"] for p in peers if p["roe"] is not None]
        sf = fun.get(s, {})
        spb = sf.get("pb_computed") or sf.get("pb_from_networth")
        sroe = sf.get("roe")
        mpb = statistics.median(pbs) if pbs else None
        mroe = statistics.median(roes) if roes else None
        out[s] = {
            "subject": s, "industry": ind["title"].replace(" Companies - Screener", ""), "industry_url": ind["url"],
            "peer_rule": "top up-to-12 by mcap on screener industry page 1 (default mcap-desc sort), subject excluded",
            "peers": peers, "n_pb": len(pbs), "n_roe": len(roes),
            "median_pb_peers": round(mpb, 4) if mpb else None, "median_roe_peers": round(mroe, 3) if mroe is not None else None,
            "subject_pb": round(spb, 4) if spb else None, "subject_roe": sroe,
            "pb_premium_vs_median_pct": round((spb / mpb - 1) * 100, 2) if spb and mpb else None,
            "pb_lt_median": (spb < mpb) if spb and mpb else None,
            "roe_gt_median": (sroe > mroe) if sroe is not None and mroe is not None else None,
            "as_of": "screener pages fetched 2026-10-12 IST pre-open; prices = 09 Oct 2026 close line",
        }
        o = out[s]
        print(f"{s:11s} {o['industry'][:30]:30s} PB {o['subject_pb'] and round(o['subject_pb'],2)} vs med {o['median_pb_peers']} (n={o['n_pb']}) prem {o['pb_premium_vs_median_pct']} | ROE {sroe} vs med {o['median_roe_peers']} (n={o['n_roe']})")
    json.dump(out, open(os.path.join(RAW, "peer_pb_roe.json"), "w"), indent=1)


if __name__ == "__main__":
    main()

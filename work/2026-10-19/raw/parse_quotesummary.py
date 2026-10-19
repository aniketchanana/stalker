#!/usr/bin/env python3
"""Yahoo quoteSummary JSON -> compact valuation / consensus / EPS-revision fields."""
import glob, json, os, datetime

QS = "/tmp/swing-2026-10-19/qs"
OUT = "/workspace/work/2026-10-19/raw/computed/quotesummary.json"


def raw(d, *keys):
    for k in keys:
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    if isinstance(d, dict):
        return d.get("raw", d.get("fmt"))
    return d


def ts(x):
    return datetime.datetime.fromtimestamp(x, datetime.timezone.utc).date().isoformat() if isinstance(x, (int, float)) else x


def main():
    out = {}
    for p in sorted(glob.glob(os.path.join(QS, "*.json"))):
        s = os.path.basename(p)[:-5]
        try:
            r = json.load(open(p))["quoteSummary"]["result"][0]
        except Exception as e:
            out[s] = {"error": str(e)}
            continue
        fd, ks, sd, pr = r.get("financialData", {}), r.get("defaultKeyStatistics", {}), r.get("summaryDetail", {}), r.get("price", {})
        rec = (r.get("recommendationTrend") or {}).get("trend") or []
        et = (r.get("earningsTrend") or {}).get("trend") or []
        trends = []
        for t in et:
            trends.append({
                "period": t.get("period"), "endDate": t.get("endDate"),
                "eps_avg": raw(t, "earningsEstimate", "avg"), "eps_n_analysts": raw(t, "earningsEstimate", "numberOfAnalysts"),
                "rev_avg": raw(t, "revenueEstimate", "avg"),
                "epsTrend": {k: raw(t, "epsTrend", k) for k in ("current", "7daysAgo", "30daysAgo", "60daysAgo", "90daysAgo")},
                "epsRevisions": {k: raw(t, "epsRevisions", k) for k in ("upLast7days", "upLast30days", "downLast30days", "downLast90days")},
            })
        # 90-day net revision check on current & next fiscal year rows
        rev_check = []
        for t in trends:
            if t["period"] in ("0y", "+1y", "0q", "+1q"):
                cur, ago = t["epsTrend"].get("current"), t["epsTrend"].get("90daysAgo")
                rev_check.append({"period": t["period"], "endDate": t["endDate"], "current": cur, "90daysAgo": ago,
                                  "chg_pct": round((cur / ago - 1) * 100, 3) if cur and ago else None,
                                  "up30": t["epsRevisions"].get("upLast30days"), "down30": t["epsRevisions"].get("downLast30days"),
                                  "down90": t["epsRevisions"].get("downLast90days")})
        fy = [x for x in rev_check if x["period"] in ("0y", "+1y") and x["chg_pct"] is not None]
        net_down = any(x["chg_pct"] < 0 for x in fy) if fy else None
        out[s] = {
            "price": raw(pr, "regularMarketPrice"), "price_time": ts(raw(pr, "regularMarketTime")),
            "mcap_cr": (raw(pr, "marketCap") or 0) / 1e7 or None,
            "trailingPE": raw(sd, "trailingPE"), "forwardPE": raw(sd, "forwardPE") or raw(ks, "forwardPE"),
            "pb": raw(ks, "priceToBook"), "bookValue": raw(ks, "bookValue"), "trailingEps": raw(ks, "trailingEps"),
            "forwardEps": raw(ks, "forwardEps"), "hi52": raw(sd, "fiftyTwoWeekHigh"), "lo52": raw(sd, "fiftyTwoWeekLow"),
            "dma50_yahoo": raw(sd, "fiftyDayAverage"), "dma200_yahoo": raw(sd, "twoHundredDayAverage"),
            "roe_yahoo": raw(fd, "returnOnEquity"), "de_yahoo": raw(fd, "debtToEquity"),
            "ocf_yahoo": raw(fd, "operatingCashflow"), "ev_ebitda": raw(ks, "enterpriseToEbitda"),
            "target_mean": raw(fd, "targetMeanPrice"), "target_median": raw(fd, "targetMedianPrice"),
            "target_high": raw(fd, "targetHighPrice"), "target_low": raw(fd, "targetLowPrice"),
            "n_analysts": raw(fd, "numberOfAnalystOpinions"), "recommendationKey": raw(fd, "recommendationKey"),
            "recommendationMean": raw(fd, "recommendationMean"),
            "recommendationTrend": rec, "earningsTrend": trends, "eps_revision_check": rev_check,
            "net_downward_fy_eps_revision_90d": net_down,
            "earnings_dates": [ts(raw({"x": x}, "x")) for x in ((r.get("calendarEvents") or {}).get("earnings") or {}).get("earningsDate", [])],
        }
    json.dump(out, open(OUT, "w"), indent=1)
    for s, v in out.items():
        if "error" in v:
            print(s, v)
            continue
        print(s, "px", v["price"], v["price_time"], "tPE", v["trailingPE"] and round(v["trailingPE"], 2), "fPE", v["forwardPE"] and round(v["forwardPE"], 2),
              "PB", v["pb"] and round(v["pb"], 2), "tgt", v["target_mean"], "n", v["n_analysts"], v["recommendationKey"],
              "netdown", v["net_downward_fy_eps_revision_90d"], [(x["period"], x["chg_pct"], x["up30"], x["down30"]) for x in v["eps_revision_check"]], "ed", v["earnings_dates"])


if __name__ == "__main__":
    main()

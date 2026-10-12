#!/usr/bin/env python3
"""Sector 1W/1M/3M returns vs Nifty 500 from NSE ind_close_all_<DDMMYYYY>.csv (official closes).

Session offsets come from the Yahoo ^CRSLDX trading calendar: t=2026-10-09, t-5=2026-10-01, t-21=2026-09-08, t-63=2026-07-10.
"""
import csv, json, os

MISC = "/tmp/swing-2026-10-12/misc"
OUT = "/workspace/work/2026-10-12/raw/computed/sectors.json"
FILES = {"t": "ind_close_09102026.csv", "t5": "ind_close_01102026.csv", "t21": "ind_close_08092026.csv", "t63": "ind_close_10072026.csv"}
DATES = {"t": "2026-10-09", "t5": "2026-10-01", "t21": "2026-09-08", "t63": "2026-07-10"}
SECTORS = ["Nifty Auto", "Nifty Bank", "Nifty Financial Services", "Nifty FMCG", "Nifty IT", "Nifty Media", "Nifty Metal",
           "Nifty Pharma", "Nifty PSU Bank", "Nifty Private Bank", "Nifty Realty", "Nifty Healthcare Index",
           "Nifty Consumer Durables", "Nifty Oil & Gas", "Nifty Chemicals", "Nifty Energy", "Nifty Infrastructure",
           "Nifty Commodities", "Nifty India Consumption", "Nifty PSE", "Nifty CPSE", "Nifty MNC", "Nifty Services Sector",
           "Nifty Capital Markets", "Nifty India Defence", "Nifty Cement", "Nifty Financial Services Ex-Bank",
           "Nifty MidSmall Healthcare", "Nifty MidSmall Financial Services", "Nifty MidSmall IT & Telecom",
           "Nifty Midcap 150", "Nifty Smallcap 250", "Nifty Next 50", "Nifty 50", "Nifty 500", "Nifty India Manufacturing",
           "Nifty Transportation & Logistics", "Nifty India Digital", "Nifty Housing", "Nifty Core Housing", "Nifty Mobility"]


def load(fn):
    out = {}
    for r in csv.DictReader(open(os.path.join(MISC, fn))):
        name = r["Index Name"].strip()
        try:
            out[name.lower()] = {"name": name, "close": float(r["Closing Index Value"]), "date": r["Index Date"],
                                 "pe": r.get("P/E"), "pb": r.get("P/B")}
        except ValueError:
            pass
    return out


def main():
    data = {k: load(v) for k, v in FILES.items()}
    n500 = data["t"]["nifty 500"]["close"]
    rets = {}
    for s in SECTORS:
        k = s.lower()
        if k not in data["t"]:
            rets[s] = {"error": "not in ind_close_all"}
            continue
        row = {"close_2026-10-09": data["t"][k]["close"], "index_date": data["t"][k]["date"],
               "pe": data["t"][k]["pe"], "pb": data["t"][k]["pb"]}
        for lab, key in (("1w_5s", "t5"), ("1m_21s", "t21"), ("3m_63s", "t63")):
            prev = data[key].get(k)
            row[f"ret_{lab}_pct"] = round((data["t"][k]["close"] / prev["close"] - 1) * 100, 3) if prev else None
            row[f"base_{lab}"] = {"date": DATES[key], "close": prev["close"] if prev else None}
        rets[s] = row
    nb = rets["Nifty 500"]
    for s, row in rets.items():
        if "error" in row:
            continue
        for lab in ("1w_5s", "1m_21s", "3m_63s"):
            if row.get(f"ret_{lab}_pct") is not None:
                row[f"rs_{lab}_vs_nifty500_pp"] = round(row[f"ret_{lab}_pct"] - nb[f"ret_{lab}_pct"], 3)
    sect = {s: r for s, r in rets.items() if "error" not in r and s not in ("Nifty 50", "Nifty 500", "Nifty Next 50", "Nifty Midcap 150", "Nifty Smallcap 250")}
    top1m = sorted(sect, key=lambda s: -sect[s]["rs_1m_21s_vs_nifty500_pp"])
    top3m = sorted(sect, key=lambda s: -sect[s]["rs_3m_63s_vs_nifty500_pp"])
    out = {"as_of": "2026-10-09", "source": "https://nsearchives.nseindia.com/content/indices/ind_close_all_<DDMMYYYY>.csv",
           "dates": DATES, "nifty500": nb, "sectors": rets,
           "rank_1m_rs": [(s, sect[s]["rs_1m_21s_vs_nifty500_pp"]) for s in top1m],
           "rank_3m_rs": [(s, sect[s]["rs_3m_63s_vs_nifty500_pp"]) for s in top3m]}
    json.dump(out, open(OUT, "w"), indent=1)
    print("Nifty 500", nb)
    print("1M RS:", out["rank_1m_rs"])
    print("3M RS:", out["rank_3m_rs"])
    print([s for s, r in rets.items() if "error" in r])


if __name__ == "__main__":
    main()

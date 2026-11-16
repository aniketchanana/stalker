#!/usr/bin/env python3
"""Sector 1W/1M/3M returns vs Nifty 500 from NSE ind_close_all_<DDMMYYYY>.csv (official closes).

Bases from the NSE holiday-master calendar: t=2026-11-13; 1W=2026-11-06 (prior Friday, 4 sessions; Balipratipada 10-Nov holiday, Muhurat 8-Nov not counted); 1M=2026-10-13 (calendar month, 21 sessions); 3M=2026-08-13 (calendar 3 months, see sessions count in dates).
"""
import csv, json, os

MISC = "/tmp/run1116/misc"
OUT = "/agent/repos/stalker/work/2026-11-16/raw/computed/sectors.json"
FILES = {"t": "ind_close_13112026.csv", "t5": "ind_close_06112026.csv", "t21": "ind_close_13102026.csv", "t63": "ind_close_13082026.csv"}
DATES = {"t": "2026-11-13", "t5": "2026-11-06", "t21": "2026-10-13", "t63": "2026-08-13"}
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
        row = {"close_2026-11-13": data["t"][k]["close"], "index_date": data["t"][k]["date"],
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
    out = {"as_of": "2026-11-13", "source": "https://nsearchives.nseindia.com/content/indices/ind_close_all_<DDMMYYYY>.csv",
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

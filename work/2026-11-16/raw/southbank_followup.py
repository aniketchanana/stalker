#!/usr/bin/env python3
"""SOUTHBANK open-position facts (19-Oct pick) from official NSE bhavcopies. Facts only, no exit decision.

Sessions: every regular NSE session 19-Oct..13-Nov (bhavcopy); `post` = sessions since the 26-Oct report. Sun 8-Nov Muhurat bhavcopy is reported separately
and not counted as a session. 20-day average volume = mean TTL_TRD_QNTY of the 20 regular sessions before each day.
"""
import csv, glob, json, os, datetime

MISC = "/tmp/run1116/misc"
EXT = "/tmp/run1116/bhav_ext"
OUT = "/agent/repos/stalker/work/2026-11-16/raw/computed/southbank_followup.json"
SYM = "SOUTHBANK"
PLAN = {"fill_date": "2026-10-19", "fill_price": 51.45, "shares": 196, "stop": 48.90, "t1": 56.82, "t2": 58.35,
        "failed_breakout_close_below": 50.68, "volume_spike_tighten_stop_to": 50.65, "time_stop_review": "2026-11-03",
        "time_stop_waiver_close_ge": 54.14, "horizon_end": "2026-11-11"}
URL = "https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{}.csv"


def row(p):
    for r in csv.reader(open(p)):
        if r and r[0].strip() == SYM and r[1].strip() == "EQ":
            d = datetime.datetime.strptime(r[2].strip(), "%d-%b-%Y").date().isoformat()
            return {"date": d, "prev_close": float(r[3]), "open": float(r[4]), "high": float(r[5]), "low": float(r[6]),
                    "close": float(r[8]), "vwap": float(r[9]), "volume": int(r[10]), "turnover_lacs": float(r[11]),
                    "trades": int(r[12]), "deliv_qty": int(r[13]), "deliv_pct": float(r[14]),
                    "source_url": URL.format(os.path.basename(p)[-12:-4])}
    return None


files = glob.glob(os.path.join(MISC, "sec_bhavdata_full_*.csv")) + glob.glob(os.path.join(EXT, "sec_bhavdata_full_*.csv"))
bars = sorted((b for b in (row(p) for p in files) if b), key=lambda b: b["date"])
seen, uniq = set(), []
for b in bars:
    if b["date"] not in seen:
        seen.add(b["date"])
        uniq.append(b)
bars = uniq
for i, b in enumerate(bars):
    prior = bars[max(0, i - 20):i]
    b["avg_vol_20_prior"] = round(sum(x["volume"] for x in prior) / len(prior)) if len(prior) == 20 else None
    b["vol_vs_20d_avg"] = round(b["volume"] / b["avg_vol_20_prior"], 2) if b["avg_vol_20_prior"] else None
    b["change_vs_prev_close_pct"] = round((b["close"] / b["prev_close"] - 1) * 100, 2)
    b["down_day"] = b["close"] < b["prev_close"]

win = [b for b in bars if "2026-10-19" <= b["date"] <= "2026-11-13"]
post = [b for b in win if b["date"] >= "2026-10-26"]


def first(pred, rows):
    for b in rows:
        if pred(b):
            return b["date"]
    return None


two_below = [(a["date"], b["date"]) for a, b in zip(win, win[1:]) if a["close"] < PLAN["failed_breakout_close_below"] and b["close"] < PLAN["failed_breakout_close_below"]]
spikes = [{"date": b["date"], "volume": b["volume"], "avg_vol_20_prior": b["avg_vol_20_prior"], "ratio": b["vol_vs_20d_avg"], "close": b["close"], "prev_close": b["prev_close"]}
          for b in win if b["down_day"] and b["vol_vs_20d_avg"] and b["vol_vs_20d_avg"] >= 2]
spikes_any = [{"date": b["date"], "ratio": b["vol_vs_20d_avg"], "down_day": b["down_day"]} for b in win if b["vol_vs_20d_avg"] and b["vol_vs_20d_avg"] >= 2]
by = {b["date"]: b for b in bars}
mu = row(os.path.join(MISC, "muhurat_bhav_08112026.csv"))
facts = {
    "plan": PLAN,
    "sessions_checked": [b["date"] for b in win],
    "first_session_high_ge_t1_56.82": first(lambda b: b["high"] >= PLAN["t1"], win),
    "first_session_high_ge_t2_58.35": first(lambda b: b["high"] >= PLAN["t2"], win),
    "first_session_close_ge_t1": first(lambda b: b["close"] >= PLAN["t1"], win),
    "first_session_close_ge_t2": first(lambda b: b["close"] >= PLAN["t2"], win),
    "first_session_close_ge_54.14": first(lambda b: b["close"] >= PLAN["time_stop_waiver_close_ge"], win),
    "any_low_le_stop_48.90": [b["date"] for b in win if b["low"] <= PLAN["stop"]],
    "min_low_19oct_13nov": min((b["low"], b["date"]) for b in win),
    "two_consecutive_closes_lt_50.68": two_below,
    "down_days_volume_ge_2x_20d_avg": spikes,
    "all_days_volume_ge_2x_20d_avg": spikes_any,
    "close_2026-11-03": by.get("2026-11-03", {}).get("close"),
    "close_2026-11-11": by.get("2026-11-11", {}).get("close"),
    "close_2026-11-13": by.get("2026-11-13", {}).get("close"),
    "high_max_19oct_13nov": max((b["high"], b["date"]) for b in win),
    "muhurat_2026-11-08_not_counted": mu,
}
json.dump({"as_of": "2026-11-13", "method": "computed", "source": "NSE sec_bhavdata_full bhavcopies (EQ series)", "facts": facts,
           "bars_19oct_13nov": win, "bars_26oct_13nov": [b["date"] for b in post]}, open(OUT, "w"), indent=1)
for b in win:
    print(b["date"], b["open"], b["high"], b["low"], b["close"], b["volume"], b["deliv_pct"], b["vol_vs_20d_avg"], "DOWN" if b["down_day"] else "")
print(json.dumps({k: v for k, v in facts.items() if k not in ("plan", "sessions_checked")}, indent=1, default=str))

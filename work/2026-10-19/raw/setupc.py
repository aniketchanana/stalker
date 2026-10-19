#!/usr/bin/env python3
"""Setup C (post-earnings drift) pre-list: Nifty 500 + Microcap 250 names with a results board meeting 1-18 Oct 2026.

  setupc.py fetch  -> per-symbol NSE corporate-announcements (result-date .. +3 days) to timestamp the results filing
  setupc.py calc   -> computed/setupc_price_action.json
Reaction session = result date if the first results-type filing is before 15:30 IST on a trading day, else next session.
Gap % = reaction-session open / prior close - 1. Held = every close from the reaction session to 16 Oct >= prior close
(the pre-result close, i.e. the gap is not filled on a closing basis); held_low also checks lows.
"""
import csv, datetime, json, os, re, sys, time

MISC = "/tmp/swing-2026-10-19/misc"
ANN = os.path.join(MISC, "ann")
OUT = "/workspace/work/2026-10-19/raw/computed/setupc_price_action.json"
CH = "/tmp/swing-2026-10-19/charts"
RESULT_PAT = re.compile(r"financial result|outcome of board meeting|results", re.I)


def meetings():
    u = {r["Symbol"].strip(): "Nifty 500" for r in csv.DictReader(open(os.path.join(MISC, "ind_nifty500list.csv")))}
    for r in csv.DictReader(open(os.path.join(MISC, "ind_niftymicrocap250_list.csv"))):
        u.setdefault(r["Symbol"].strip(), "Nifty Microcap 250")
    hits = {}
    for x in json.load(open(os.path.join(MISC, "nse_board_past.json"))):
        d = datetime.datetime.strptime(x["bm_date"], "%d-%b-%Y").date()
        if x["bm_symbol"] in u and re.search(r"result", x["bm_desc"] + x["bm_purpose"], re.I) and \
                datetime.date(2026, 10, 1) <= d <= datetime.date(2026, 10, 18):
            h = hits.setdefault(x["bm_symbol"], {"ticker": x["bm_symbol"], "list": u[x["bm_symbol"]], "meeting_dates": set(),
                                                 "company": x.get("sm_name"), "desc": x["bm_desc"][:200]})
            h["meeting_dates"].add(d.isoformat())
    for h in hits.values():
        h["meeting_dates"] = sorted(h["meeting_dates"])
    return hits


def fetch():
    import nse_fetch as n
    os.makedirs(ANN, exist_ok=True)
    n.cookie()
    for s, h in sorted(meetings().items()):
        fp = os.path.join(ANN, s + ".json")
        if os.path.exists(fp):
            continue
        d0 = datetime.date.fromisoformat(h["meeting_dates"][0])
        d1 = min(d0 + datetime.timedelta(days=3), datetime.date(2026, 10, 18))
        url = ("https://www.nseindia.com/api/corporate-announcements?index=equities&symbol=" + s.replace("&", "%26") +
               f"&from_date={d0:%d-%m-%Y}&to_date={d1:%d-%m-%Y}")
        c, b = n.get(url)
        print(s, c, len(b), flush=True)
        if c == 200:
            open(fp, "wb").write(b)
        time.sleep(0.4)


def bars(sym):
    from compute_indicators import parse_chart
    p = os.path.join(CH, sym + ".json")
    return parse_chart(p)["rows"] if os.path.exists(p) else None


def calc():
    out = {}
    for s, h in sorted(meetings().items()):
        anns = []
        fp = os.path.join(ANN, s + ".json")
        if os.path.exists(fp):
            try:
                anns = json.load(open(fp))
            except ValueError:
                anns = []
        res = [a for a in anns if RESULT_PAT.search((a.get("desc") or "") + " " + (a.get("attchmntText") or ""))
               and "intimation" not in (a.get("desc") or "").lower()]
        res.sort(key=lambda a: a.get("sort_date") or "")
        filing = res[0]["sort_date"] if res else None
        rows = bars(s)
        rec = dict(h, results_filing_ts_ist=filing, results_filing_desc=res[0].get("desc") if res else None,
                   results_filing_source="https://www.nseindia.com/api/corporate-announcements?index=equities&symbol=" + s)
        if not rows:
            rec["error"] = "no Yahoo bars"
            out[s] = rec
            continue
        dates = [r["date"] for r in rows]
        if filing:
            fdt = datetime.datetime.fromisoformat(filing)
            fd = fdt.date().isoformat()
            intraday = fd in dates and fdt.time() < datetime.time(15, 30)
            basis = "filing timestamp"
        else:
            fd = h["meeting_dates"][-1]
            intraday = False
            basis = "board-meeting date (no results filing timestamp found; assumed post-market)"
        cand = [i for i, d in enumerate(dates) if (d >= fd if intraday else d > fd)]
        if not cand:
            rec.update(reaction_session=None, notes="results after 16-Oct close; reaction not yet observable (first session 19 Oct)")
            out[s] = rec
            continue
        i = cand[0]
        prev = rows[i - 1]["close"]
        o = rows[i]["open"]
        since = rows[i:]
        rec.update(
            reaction_basis=basis, reaction_session=dates[i], prior_close=round(prev, 2), reaction_open=round(o, 2) if o else None,
            reaction_close=round(rows[i]["close"], 2),
            gap_pct=round((o / prev - 1) * 100, 2) if o else None,
            reaction_day_return_pct=round((rows[i]["close"] / prev - 1) * 100, 2),
            sessions_since_reaction_incl=len(since),
            close_2026_10_16=round(rows[-1]["close"], 2),
            return_since_prior_close_pct=round((rows[-1]["close"] / prev - 1) * 100, 2),
            min_close_since=round(min(r["close"] for r in since), 2), min_low_since=round(min(r["low"] for r in since), 2),
            held_close=all(r["close"] >= prev for r in since), held_low=all(r["low"] >= prev for r in since),
            last_bars=[{k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items() if k != "close_filled_from_meta"}
                       for r in rows[max(0, i - 1):]],
        )
        rec["filing_intraday"] = intraday
        rec["post_result_move_pct"] = rec["reaction_day_return_pct"] if intraday else rec["gap_pct"]
        rec["post_result_move_basis"] = ("reaction-day close vs prior close (results filed intraday, open was pre-result)" if intraday
                                         else "reaction-session open vs prior close (results filed after market)")
        rec["gap_up_held_3plus"] = bool(rec["post_result_move_pct"] is not None and rec["post_result_move_pct"] > 0
                                        and rec["held_close"] and len(since) >= 3)
        out[s] = rec
    json.dump(out, open(OUT, "w"), indent=1)
    for s, r in out.items():
        print(f'{s:11s} {r["list"][:9]} mtg={r["meeting_dates"]} filing={r.get("results_filing_ts_ist")} react={r.get("reaction_session")} '
              f'move={r.get("post_result_move_pct")} gap={r.get("gap_pct")} day={r.get("reaction_day_return_pct")} since={r.get("return_since_prior_close_pct")} '
              f'n={r.get("sessions_since_reaction_incl")} held={r.get("held_close")} G3={r.get("gap_up_held_3plus")}')


if __name__ == "__main__":
    {"fetch": fetch, "calc": calc}[sys.argv[1]]()

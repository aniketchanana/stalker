#!/usr/bin/env python3
"""Assemble data.json for run 2026-10-26 (session 2026-10-23) from fetched/computed artifacts. No invented numbers.

Inputs: raw/computed/*.json (tech, summary, indices, sectors, nse_bhav_summary, screener_fundamentals, industry_medians,
screen_result, peer_pb_roe, pledge, quotesummary, trackb_tech, trackb_value, setupc_price_action) + /tmp/run1026/misc NSE API dumps
+ raw/web_facts.json (web-search facts with URLs: flows, macro, bank metrics, results dates, forward-PE cross-checks).
"""
import csv, datetime, json, os, statistics, sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compute_indicators import parse_chart, compute_from_rows

RAW = "/workspace/work/2026-10-26/raw"
CMP = os.path.join(RAW, "computed")
OUT = "/workspace/work/2026-10-26"
MISC = "/tmp/run1026/misc"
CHARTS = "/tmp/run1026/charts"
SESSION = "2026-10-23"
RUN_DATE = "2026-10-26"
WINDOW_START, WINDOW_END = "2026-10-26", "2026-11-16"


def L(name, base=CMP, default=None):
    p = os.path.join(base, name)
    if not os.path.exists(p):
        return default
    return json.load(open(p))


tech = L("tech.json")
summary = L("summary.json")
indices = L("indices.json")
sectors = L("sectors.json")
bhav = L("nse_bhav_summary.json")
fun = L("screener_fundamentals.json")
inds = L("industry_medians.json", default={})
screen = L("screen_result.json")
peers = L("peer_pb_roe.json", default={})
pledge = L("pledge.json", default={})
qs = L("quotesummary.json", default={})
trackb = L("trackb_tech.json")
trackb_val = L("trackb_value.json", default={})
setupc = L("setupc_price_action.json")
web = L("web_facts.json", RAW, default={})
fiidii = L("nse_fiidii.json", MISC)
asm = L("nse_asm.json", MISC)
gsm = L("nse_gsm.json", MISC)
hol = L("nse_holidays.json", MISC)
bm_future = L("nse_board_future.json", MISC)
bm_past = L("nse_board_past.json", MISC)
bm_2025 = L("nse_board_2025q2.json", MISC)
ca = L("nse_corp_actions.json", MISC)
univ = {r["Symbol"].strip(): r for r in csv.DictReader(open(os.path.join(RAW, "ind_nifty500list.csv")))}
micro = {r["Symbol"].strip(): r for r in csv.DictReader(open(os.path.join(MISC, "ind_niftymicrocap250_list.csv")))}

SCR = "https://www.screener.in/company/{}/consolidated/"
YF = "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval=1d&range=1y"
QSURL = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{}.NS"
BHAV = "https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_23102026.csv"
INDCLOSE = "https://nsearchives.nseindia.com/content/indices/ind_close_all_23102026.csv"
BM_URL = "https://www.nseindia.com/api/corporate-board-meetings?index=equities"
ASM_URL = "https://www.nseindia.com/api/reportASM"
GSM_URL = "https://www.nseindia.com/api/reportGSM"
BAN_URL = "https://nsearchives.nseindia.com/content/fo/fo_secban.csv"
FIIDII_URL = "https://www.nseindia.com/api/fiidiiTradeReact"
HOL_URL = "https://www.nseindia.com/api/holiday-master?type=trading"
ANN_URL = "https://www.nseindia.com/api/corporate-announcements?index=equities&symbol={}"
ADV_MIN, MCAP_B = 25.0, 5000.0


def F(value, source_url, as_of, method, notes=""):
    d = {"value": value, "source_url": source_url, "as_of": as_of, "method": method}
    if notes:
        d["notes"] = notes
    return d


def na(reason, source_url="", as_of=""):
    return F("N/A", source_url, as_of, "unavailable", reason)


def rnd(x, n=4):
    if x is None:
        return None
    try:
        return round(float(x), n)
    except (TypeError, ValueError):
        return x


def gap_pct(a, b):
    if a in (None, 0) or b is None:
        return None
    return round(abs(a - b) / abs(a) * 100, 3)


def d_(s):
    return datetime.datetime.strptime(s, "%d-%b-%Y").date()


# ---------------------------------------------------------------- trading calendar / results window
hol_dates = {d_(h["tradingDate"]) for h in hol.get("CM", [])}
sessions, day = [], datetime.date(2026, 10, 26)
while len(sessions) < 15:
    if day.weekday() < 5 and day not in hol_dates:
        sessions.append(day.isoformat())
    day += datetime.timedelta(days=1)
assert sessions[-1] == WINDOW_END, sessions
results_window = F({"start": WINDOW_START, "end": WINDOW_END, "n_sessions": 15, "sessions": sessions,
                    "count_rule": "26 Oct 2026 = day 1; excludes weekends and NSE trading holidays (Tue 10 Nov Diwali-Balipratipada falls inside and is excluded). "
                                  "Sun 8 Nov (Diwali Laxmi Pujan) Muhurat special session not counted."},
                   HOL_URL, RUN_DATE, "computed")


# ---------------------------------------------------------------- market
def index_block(key, ysym, label):
    t = indices[key]
    url = YF.format(ysym)
    return {
        "label": label,
        "close": F(rnd(t["close"], 2), url, t["as_of"], "computed", "Yahoo daily chart last bar (IST date); bars after 2026-10-23 excluded"),
        "sma20": F(rnd(t["dma20"], 2), url, t["as_of"], "computed"),
        "sma50": F(rnd(t["dma50"], 2), url, t["as_of"], "computed"),
        "sma200": F(rnd(t["dma200"], 2), url, t["as_of"], "computed"),
        "ema20": F(rnd(t["ema20"], 2), url, t["as_of"], "computed"),
        "rsi14": F(rnd(t["rsi14"], 2), url, t["as_of"], "computed", "Wilder RSI(14)"),
        "atr14": F(rnd(t["atr14"], 2), url, t["as_of"], "computed", "Wilder ATR(14)"),
        "dma200_change_20_sessions": F(rnd(t["dma200_change_20_sessions"], 2), url, t["as_of"], "computed"),
        "dma50_change_20_sessions": F(rnd(t["dma50_change_20_sessions"], 2), url, t["as_of"], "computed"),
        "ret_1w_5s_pct": F(rnd(t["ret_1w_5d"], 3), url, t["as_of"], "computed"),
        "ret_1m_21s_pct": F(rnd(t["ret_1m_21d"], 3), url, t["as_of"], "computed"),
        "ret_3m_63s_pct": F(rnd(t["ret_3m_63d"], 3), url, t["as_of"], "computed"),
        "52w_high": F(rnd(t["hi52_used"], 2), url, t["as_of"], "computed", f"series high date {t.get('series_52w_high_date')}"),
        "52w_low": F(rnd(t["series_52w_low"], 2), url, t["as_of"], "computed", f"series low date {t.get('series_52w_low_date')}"),
        "close_vs_sma20": "above" if t["close"] > t["dma20"] else "below",
        "close_vs_sma50": "above" if t["close"] > t["dma50"] else "below",
        "close_vs_sma200": "above" if t["close"] > t["dma200"] else "below",
    }


market = {
    "nifty50": index_block("nifty50", "%5ENSEI", "Nifty 50"),
    "nifty500": index_block("nifty500", "%5ECRSLDX", "Nifty 500 (Yahoo ^CRSLDX)"),
    "india_vix": index_block("india_vix", "%5EINDIAVIX", "India VIX"),
    "nifty_bank": index_block("nifty_bank", "%5ENSEBANK", "Nifty Bank"),
    "nifty_it": index_block("nifty_it", "%5ECNXIT", "Nifty IT"),
    "nifty_pharma": index_block("nifty_pharma", "%5ECNXPHARMA", "Nifty Pharma"),
    "nifty_midcap150": index_block("nifty_midcap150", "NIFTYMIDCAP150.NS", "Nifty Midcap 150"),
}
n500_nse = sectors["nifty500"]
n50_nse = sectors["sectors"].get("Nifty 50") or {}
market["nifty500"]["close"]["notes"] += f"; NSE ind_close_all 23-10-2026 close {n500_nse['close_2026-10-23']}"
market["nifty500"]["official_pe_pb"] = F({"pe": n500_nse["pe"], "pb": n500_nse["pb"]}, INDCLOSE, SESSION, "scraped")
if n50_nse:
    market["nifty50"]["close"]["notes"] += f"; NSE ind_close_all 23-10-2026 close {n50_nse.get('close_2026-10-23')}"
    market["nifty50"]["official_pe_pb"] = F({"pe": n50_nse.get("pe"), "pb": n50_nse.get("pb")}, INDCLOSE, SESSION, "scraped")
vt = summary["vix_trend"]
market["india_vix"]["trend_1m"] = F({"now": rnd(vt["now"], 2), "ago_21_sessions": rnd(vt["ago_21_sessions"], 2), "ago_date": vt["ago_date"],
                                     "change_pct": rnd(vt["change_pct"], 2), "direction": vt["direction"],
                                     "last_10_closes": [[d, rnd(v, 2)] for d, v in vt["last_10_closes"]]},
                                    YF.format("%5EINDIAVIX"), vt["now_date"], "computed")
vixn = sectors["sectors"].get("India VIX") or {}
if vixn:
    market["india_vix"]["close"]["notes"] += f"; NSE ind_close_all 23-10-2026 India VIX {vixn.get('close_2026-10-23')}"
fii = {r["category"]: r for r in fiidii}
market["fii_dii_flows"] = {
    "fii_fpi_net_cr_2026-10-23": F(float(fii["FII/FPI"]["netValue"]), FIIDII_URL, fii["FII/FPI"]["date"], "scraped",
                                   f"NSE provisional cash: buy {fii['FII/FPI']['buyValue']} / sell {fii['FII/FPI']['sellValue']}"),
    "dii_net_cr_2026-10-23": F(float(fii["DII"]["netValue"]), FIIDII_URL, fii["DII"]["date"], "scraped",
                               f"buy {fii['DII']['buyValue']} / sell {fii['DII']['sellValue']}"),
}
for k, v in (web.get("flows") or {}).items():
    market["fii_dii_flows"][k] = v


def fx_block(fname, ysym, note):
    pc = parse_chart(os.path.join(CHARTS, fname))
    rows = [r for r in pc["rows"] if r["date"] <= SESSION]
    c = compute_from_rows(rows, pc["meta"])
    url = YF.format(ysym)
    return {"close": F(rnd(rows[-1]["close"], 3), url, rows[-1]["date"], "computed", note),
            "ret_1w_5s_pct": F(rnd(c["ret_1w_5d"], 2), url, rows[-1]["date"], "computed"),
            "ret_1m_21s_pct": F(rnd(c["ret_1m_21d"], 2), url, rows[-1]["date"], "computed"),
            "ret_3m_63s_pct": F(rnd(c["ret_3m_63d"], 2), url, rows[-1]["date"], "computed"),
            "sma50": F(rnd(c["dma50"], 2), url, rows[-1]["date"], "computed"),
            "sma200": F(rnd(c["dma200"], 2), url, rows[-1]["date"], "computed")}


market["brent_usd"] = fx_block("IDX_BZ_F.json", "BZ%3DF", "Yahoo BZ=F front-month; live 26-Oct bar excluded")
market["usdinr"] = fx_block("IDX_USDINR_X.json", "USDINR%3DX", "Yahoo USDINR=X; live 26-Oct bar excluded")
for k, v in (web.get("market_extra") or {}).items():
    market[k] = v

# ---------------------------------------------------------------- sectors
sec_rows = []
for name, s in sectors["sectors"].items():
    sec_rows.append({"index": name, "close": s.get("close_2026-10-23"), "pe": s.get("pe"), "pb": s.get("pb"),
                     "ret_1w_pct": s.get("ret_1w_5s_pct"), "ret_1m_pct": s.get("ret_1m_21s_pct"), "ret_3m_pct": s.get("ret_3m_63s_pct"),
                     "rs_1w_pp": s.get("rs_1w_5s_vs_nifty500_pp"), "rs_1m_pp": s.get("rs_1m_21s_vs_nifty500_pp"), "rs_3m_pp": s.get("rs_3m_63s_vs_nifty500_pp")})
SECTORAL = [r for r in sec_rows if r["rs_1m_pp"] is not None and r["index"] not in
            ("Nifty 500", "Nifty 50", "India VIX")]
top1 = sorted([r for r in SECTORAL if r["rs_1m_pp"] is not None], key=lambda r: -r["rs_1m_pp"])
top3 = sorted([r for r in SECTORAL if r["rs_3m_pp"] is not None], key=lambda r: -r["rs_3m_pp"])
sectors_out = {
    "value": sec_rows,
    "benchmark": {"nifty500_ret_1w_pct": n500_nse["ret_1w_5s_pct"], "nifty500_ret_1m_pct": n500_nse["ret_1m_21s_pct"],
                  "nifty500_ret_3m_pct": n500_nse["ret_3m_63s_pct"]},
    "base_dates": sectors["dates"],
    "top5_rs_1m": [(r["index"], r["rs_1m_pp"]) for r in top1[:5]],
    "top5_rs_3m": [(r["index"], r["rs_3m_pp"]) for r in top3[:5]],
    "bottom5_rs_1m": [(r["index"], r["rs_1m_pp"]) for r in top1[-5:]],
    "bottom5_rs_3m": [(r["index"], r["rs_3m_pp"]) for r in top3[-5:]],
    "source_url": "https://nsearchives.nseindia.com/content/indices/ind_close_all_<DDMMYYYY>.csv (23102026, 16102026, 23092026, 23072026)",
    "as_of": SESSION, "method": "computed",
    "notes": "Official NSE index closes; 1W base 16-Oct (4 sessions; Dussehra 20-Oct), 1M base 23-Sep (20 sessions, calendar month), 3M base 23-Jul (63 sessions); NSE holiday-master calendar; RS = sector return minus Nifty 500 return (pp). "
             "Rankings cover all sectoral/thematic indices in the file (broad-market indices such as Nifty 50/Next 50/Midcap/Smallcap included in 'value' only if present).",
}

# ---------------------------------------------------------------- breadth
b = summary["breadth"]
breadth = {
    "computed": F({"above_20dma_pct": b["above_20dma_pct"], "above_50dma_pct": b["above_50dma_pct"], "above_200dma_pct": b["above_200dma_pct"],
                   "above_20dma": f"{b['above_20dma_count']}/{b['sample_with_20dma']}", "above_50dma": f"{b['above_50dma_count']}/{b['sample_with_50dma']}",
                   "above_200dma": f"{b['above_200dma_count']}/{b['sample_with_200dma']}",
                   "nifty50_above_50dma_pct": b["nifty50_above_50dma_pct"], "nifty50_above_50dma": b["nifty50_above_50dma"]},
                  "Yahoo v8 chart per Nifty 500 constituent", SESSION, "computed", b["universe"]),
    "published_cross_checks": web.get("breadth_cross_checks", []),
}

# ---------------------------------------------------------------- macro calendar
holidays = [h for h in hol.get("CM", []) if d_(h["tradingDate"]) >= datetime.date(2026, 10, 1)]
macro = dict(web.get("macro") or {})
macro["nse_holidays_from_oct_2026"] = F([{"date": h["tradingDate"], "day": h["weekDay"], "desc": h["description"]} for h in holidays], HOL_URL, RUN_DATE, "scraped",
                                        "Diwali Laxmi Pujan Sun 8 Nov = Muhurat trading (timings to be notified by NSE circular)")
macro["results_window_15_sessions"] = results_window

# ---------------------------------------------------------------- screen
QUERY = ("Market Capitalization > 12000 AND Price to earning < Industry PE AND Price to earning > 0 AND Return on equity > 12 AND "
         "Debt to equity < 1 AND Pledged percentage < 20 AND Current price > DMA 50 AND DMA 50 > DMA 200 AND Current price > High price * 0.75")
rows = screen["rows"]
universe_screen = {
    "query": QUERY,
    "source": "Rebuilt: Nifty 500 constituents (niftyindices CSV) -> Yahoo 1y daily (technicals, computed) -> screener.in company pages (fundamentals; "
              "PE/mcap/PB rescaled to the 23-Oct NSE close where the page showed another price) -> screener.in industry pages (industry PE) -> NSE SHP XBRL (pledge)",
    "as_of": SESSION, "method": "computed",
    "technical_rules": {"A": "close > SMA50 > SMA200 and close > 0.75 x 52wH (literal query)",
                        "B": "close > SMA50, SMA50 <= SMA200 but SMA200 rising over 20 sessions, close > 0.75 x 52wH (secondary, flagged)"},
    "industry_pe_basis": "Primary: median positive P/E of top-25-by-mcap peers on screener industry page 1. Secondary flag: median across all pages.",
    "universe_counts": {"nifty500_constituents": len(univ), "with_yahoo_technicals": summary["computed_count"],
                        "tech_rule_A": summary["tech_rule_A_count"], "tech_rule_B": summary["tech_rule_B_count"], "tech_pass": summary["tech_pass_count"]},
    "step_counts": screen["step_counts"],
    "main_pass": screen["main_pass"],
    "main_pass_pledge_confirmed_lt_20": screen["main_pass_pledge_confirmed"],
    "pe_lt_industry_top25": screen["pe_lt_industry_top25"],
    "pe_lt_industry_allpages": screen["pe_lt_industry_allpages"],
    "pe_within_5pct_top25": screen["pe_within_5pct_top25"],
    "tech_rule_A": summary["tech_rule_A"], "tech_rule_B": summary["tech_rule_B"],
    "rows": {s: {k: (rnd(v) if isinstance(v, float) else v) for k, v in r.items() if k not in ("company",)} for s, r in rows.items()},
    "notes": web.get("screen_notes", ""),
}
universe_screen_fin = {
    "query": "Mcap > 12000 AND PE > 0 AND PB < sub-sector peer median PB (fallback PB < 3 when no peer median) AND ROE > 12 AND technical pass (rule A or B); D/E ignored",
    "as_of": SESSION, "method": "computed",
    "financials_in_techpass": screen["financials_in_techpass"],
    "tickers": screen["financials_variant_pass"], "count": len(screen["financials_variant_pass"]),
    "rows": {s: rows[s]["financials_variant"] | {"pb": rnd(rows[s]["pb"]), "median_pb_peers": rows[s]["median_pb_peers"], "roe": rows[s]["roe"],
                                                 "pass": rows[s]["financials_variant_pass"]} for s in screen["financials_in_techpass"]},
}

# ---------------------------------------------------------------- sub-sector medians
sub_sector_medians = {}
for s, p in peers.items():
    if p.get("error"):
        sub_sector_medians[s] = na(p["error"])
        continue
    href = (fun.get(s) or {}).get("industry_href") or ""
    im = inds.get(href.rstrip("/") + "/") if href else None
    sub_sector_medians[s] = {
        "industry": p["industry"], "industry_url": p["industry_url"], "peer_rule": p["peer_rule"],
        "peers": [{"ticker": x.get("ticker"), "mcap_cr": x.get("mcap_cr"), "pb": x.get("pb"), "pb_basis": x.get("pb_basis"), "roe": x.get("roe"), "pe": x.get("pe")}
                  for x in p["peers"]],
        "median_pb": F(p["median_pb_peers"], p["industry_url"], "screener pages fetched 2026-10-26 (23-Oct close line)", "computed", f"n={p['n_pb']}"),
        "median_roe": F(p["median_roe_peers"], p["industry_url"], "latest reported", "computed", f"n={p['n_roe']}"),
        "median_pe_top25": F(im["median_pe_top25_mcap"] if im else None, p["industry_url"], "industry page fetched 2026-10-26", "computed",
                             f"n={im['n_pe_top25_mcap'] if im else None}"),
        "median_pe_allpages": F(im["median_pe"] if im else None, p["industry_url"], "industry page fetched 2026-10-26", "computed", f"n={im['n_pe'] if im else None}"),
        "subject_pb": p["subject_pb"], "subject_roe": p["subject_roe"], "pb_premium_vs_median_pct": p["pb_premium_vs_median_pct"],
    }

# ---------------------------------------------------------------- surveillance
all_univ = set(univ) | set(micro)
asm_rows = [{"symbol": r["symbol"], "term": term, "stage": r["asmSurvIndicator"], "desc": r["survDesc"], "as_of": r["asmTime"]}
            for term in ("longterm", "shortterm") for r in asm[term]["data"] if r["symbol"] in all_univ]
gsm_rows = [{"symbol": r["symbol"], "stage": r["gsmStage"], "desc": r["survDesc"]} for r in gsm if r["symbol"] in all_univ]
asm_all = {}
for term in ("longterm", "shortterm"):
    for r in asm[term]["data"]:
        asm_all.setdefault(r["symbol"], []).append(f"{term} {r['asmSurvIndicator']}")
gsm_all = {r["symbol"]: r["gsmStage"] for r in gsm}
ban_lines = open(os.path.join(MISC, "fo_secban.csv")).read().splitlines()
ban = [l.split(",")[1].strip() for l in ban_lines[1:] if "," in l]
bulk = list(csv.DictReader(open(os.path.join(MISC, "bulk.csv"))))
surveillance = {
    "asm_nifty500_and_microcap250": F(asm_rows, ASM_URL, RUN_DATE, "scraped", f"full NSE ASM list size {sum(len(asm[t]['data']) for t in ('longterm', 'shortterm'))}"),
    "gsm_nifty500_and_microcap250": F(gsm_rows, GSM_URL, RUN_DATE, "scraped", "none" if not gsm_rows else ""),
    "fo_ban_trade_date_2026-10-26": F(ban, BAN_URL, RUN_DATE, "scraped", ban_lines[0] if ban_lines else ""),
    "bulk_deals_2026-10-23": F([r for r in bulk if (r.get("Symbol") or "").strip() in all_univ], "https://nsearchives.nseindia.com/content/equities/bulk.csv",
                               SESSION, "scraped", f"{len(bulk)} bulk-deal rows on 23 Oct; filtered to Nifty 500 + Microcap 250 names. block.csv: NO RECORDS."),
}

# ---------------------------------------------------------------- corporate calendar (26 Oct - 16 Nov)
def in_window(dt):
    return datetime.date(2026, 10, 26) <= dt <= datetime.date(2026, 11, 16)


cal_items, seen = [], set()
for r in bm_future:
    s = r["bm_symbol"]
    if s not in all_univ:
        continue
    dt = d_(r["bm_date"])
    if not in_window(dt) or (s, dt) in seen:
        continue
    seen.add((s, dt))
    cal_items.append({"date": dt.isoformat(), "symbol": s, "event": (r.get("bm_purpose") or "") + ": " + (r.get("bm_desc") or "")[:200],
                      "source": BM_URL + "&from_date=26-10-2026&to_date=31-12-2026", "method": "scraped"})
for c in ca:
    if c["symbol"] in all_univ:
        cal_items.append({"date": d_(c["exDate"]).isoformat(), "symbol": c["symbol"], "event": f"Ex-date: {c['subject']}",
                          "source": "https://www.nseindia.com/api/corporates-corporateActions", "method": "scraped"})
cal_items += web.get("calendar_items", [])
cal_items.sort(key=lambda x: (x["date"], x["symbol"]))
corp_cal = {"through": WINDOW_END, "window_rule": results_window["value"]["count_rule"], "items": cal_items,
            "notes": "NSE board-meeting API (meeting dates 26 Oct-31 Dec) filtered to Nifty 500 + Microcap 250 and to the 15-session window; plus NSE corporate actions and macro events."}

bm_future_by = {}
for r in bm_future:
    bm_future_by.setdefault(r["bm_symbol"], set()).add(d_(r["bm_date"]))
bm_2025_by = {}
for r in bm_2025:
    if "result" in ((r.get("bm_purpose") or "") + (r.get("bm_desc") or "")).lower():
        bm_2025_by.setdefault(r["bm_symbol"], set()).add(d_(r["bm_date"]))


def results_field(s):
    if s in setupc and setupc[s].get("results_filing_ts_ist"):
        return F({"q2fy27_reported": True, "date": setupc[s]["results_filing_ts_ist"][:10]}, ANN_URL.format(s), RUN_DATE, "scraped",
                 f"Q2 FY27 already reported (filing {setupc[s]['results_filing_ts_ist']} IST). Next quarterly results ~Jan 2027; not within window.")
    fut = sorted(x for x in bm_future_by.get(s, set()) if x >= datetime.date(2026, 10, 26))
    if fut:
        dt = fut[0].isoformat()
        return F({"date": dt, "confirmed": True, "in_15_session_window": dt <= WINDOW_END}, BM_URL, RUN_DATE, "scraped", "NSE board-meeting intimation")
    wf = (web.get("results_dates") or {}).get(s)
    if wf:
        return wf
    ly = sorted(x for x in bm_2025_by.get(s, set()) if datetime.date(2025, 10, 1) <= x <= datetime.date(2025, 11, 30))
    hint = ly[0].isoformat() if ly else None
    return F({"date": "N/A", "confirmed": False, "last_year_q2_date_hint": hint,
              "hint_inside_window_if_same_calendar_date": (hint is not None and hint.replace("2025", "2026") <= WINDOW_END)},
             BM_URL + "&from_date=01-10-2025&to_date=30-11-2025", RUN_DATE, "scraped",
             "No NSE board-meeting intimation for 26 Oct-31 Dec 2026 yet; last year's Q2 date shown as an UNCONFIRMED hint")


# ---------------------------------------------------------------- per-symbol technicals (computed directly from charts)
def pivots(rows, k=3, lookback=60):
    seg = rows[-lookback:]
    hi, lo = [], []
    for i in range(k, len(seg) - k):
        w = seg[i - k:i + k + 1]
        if seg[i]["high"] == max(x["high"] for x in w):
            hi.append({"date": seg[i]["date"], "high": rnd(seg[i]["high"], 2)})
        if seg[i]["low"] == min(x["low"] for x in w):
            lo.append({"date": seg[i]["date"], "low": rnd(seg[i]["low"], 2)})
    return hi, lo


def full_tech(s):
    p = os.path.join(CHARTS, s + ".json")
    if not os.path.exists(p):
        return None, None
    pc = parse_chart(p)
    if not pc:
        return None, None
    rows = pc["rows"]
    c = compute_from_rows(rows, pc["meta"])
    if c:
        ph, pl = pivots(rows)
        c["pivot_highs_60s"], c["pivot_lows_60s"] = ph, pl
        cons = {}
        for wk, n in (("3w", 15), ("4w", 20), ("6w", 30), ("8w", 40)):
            seg = rows[-n:]
            h, l = max(x["high"] for x in seg), min(x["low"] for x in seg)
            cons[wk] = {"sessions": n, "high": rnd(h, 2), "low": rnd(l, 2), "width_pct": rnd((h - l) / l * 100, 2), "from": seg[0]["date"]}
        c["consolidation"] = cons
        c["last_10_candles"] = [{k: (rnd(v, 2) if isinstance(v, float) and k != "volume" else v) for k, v in x.items() if k != "close_filled_from_meta"}
                                for x in rows[-10:]]
    return c, pc["meta"]


# ---------------------------------------------------------------- web extras
BANK = web.get("bank_metrics", {})
CYCL = web.get("cyclicals", {})
FWD2 = web.get("forward_pe_second_source", {})
brent = market["brent_usd"]

# ---------------------------------------------------------------- candidate set
cand_roles = {}


def add(s, role):
    cand_roles.setdefault(s, []).append(role)


for s in screen["main_pass"]:
    add(s, "main_pass")
for s in screen["pe_lt_industry_top25"]:
    if s not in screen["main_pass"]:
        add(s, "pe_lt_industry_fails_other")
for s in screen["pe_within_5pct_top25"]:
    add(s, "near_miss_pe_within_5pct")
for s in screen["financials_variant_pass"]:
    add(s, "financials_variant_pass")
for s in ("REDINGTON", "TANLA", "JAMNAAUTO"):
    add(s, "watchlist_2026-10-19")
add("SOUTHBANK", "followup_pick_2026-10-19")
setupc_list = []
for s, r in setupc.items():
    f = fun.get(s) or {}
    bh = bhav.get(s) or {}
    mc, adv = f.get("market_cap_cr"), bh.get("nse_adv_20s_cr")
    r["mcap_cr"], r["adv20_cr"] = mc, adv
    r["mcap_ge_5000"] = mc is not None and mc >= MCAP_B
    r["adv_ge_25"] = adv is not None and adv >= ADV_MIN
    q = f.get("quarters") or {}
    rev_k = "Sales" if "Sales" in q else ("Revenue" if "Revenue" in q else None)
    yo = {}
    for lab, key in ((rev_k, "revenue"), ("Net Profit", "pat")):
        if lab and lab in q:
            cur, ago = q[lab].get("2026-09-30"), q[lab].get("2025-09-30")
            yo[key + "_q2fy27_cr"], yo[key + "_q2fy26_cr"] = cur, ago
            yo[key + "_yoy_pct"] = rnd((cur / ago - 1) * 100, 2) if cur is not None and ago and ago > 0 else None
    r["yoy_from_screener"] = yo
    r["yoy_source"] = SCR.format(s)
    r["setup_c_eligible"] = bool(r.get("gap_up_held_3plus") and r["mcap_ge_5000"] and r["adv_ge_25"])
    r["setup_c_watch_lt3_sessions"] = bool(r.get("post_result_move_pct") and r["post_result_move_pct"] > 0 and r.get("held_close")
                                           and (r.get("sessions_since_reaction_incl") or 0) < 3 and r["mcap_ge_5000"] and r["adv_ge_25"])
    if r["setup_c_eligible"]:
        add(s, "setup_c_gap_held_3plus")
        setupc_list.append(s)
    elif r["setup_c_watch_lt3_sessions"]:
        add(s, "setup_c_watch_held_lt3_sessions")
for s in (trackb_val.get("value_pass") or []):
    add(s, "track_b_5k_value_pass")

# ---------------------------------------------------------------- candidates
candidates, cross = {}, []
for s, roles in cand_roles.items():
    t, meta = full_tech(s)
    if not t:
        candidates[s] = {"ticker": s, "roles": roles, "error": "no Yahoo chart"}
        continue
    f = fun.get(s) or {}
    q = qs.get(s) or {}
    bh = bhav.get(s) or {}
    row = rows.get(s) or {}
    pr = peers.get(s) or {}
    pl = pledge.get(s) or {}
    close_nse = bh.get("nse_close_2026-10-23")
    close = close_nse or t["close"]
    yurl, surl = YF.format(f"{s}.NS"), SCR.format(s)
    rs = f.get("rescale") or {}
    resc = (f"PE/mcap/PB rescaled x{rs.get('ratio')} (23-Oct close / screener price {rs.get('screener_price')})" if rs.get("applied")
            else f"screener price line '{f.get('price_as_of_line')}' (= 23-Oct close; ratio {rs.get('ratio')})")
    ind = f.get("industry") or {}
    href = f.get("industry_href")
    im = inds.get(href) if href else None
    med25 = row.get("industry_pe_top25") if row else (im["median_pe_top25_mcap"] if im and im["n_pe_top25_mcap"] >= 3 else None)
    medall = row.get("industry_pe_allpages") if row else (im["median_pe"] if im and im["n_pe"] >= 3 else None)
    c = {"ticker": s, "company": univ.get(s, micro.get(s, {})).get("Company Name"), "nifty_industry": univ.get(s, micro.get(s, {})).get("Industry"),
         "index_membership": "Nifty 500" if s in univ else ("Nifty Microcap 250" if s in micro else "other"),
         "roles": roles, "tech_rule": t.get("tech_rule"), "tech_pass": t.get("tech_pass")}
    c["price"] = F(close, BHAV, SESSION, "scraped", f"NSE bhavcopy close {close_nse}; Yahoo close {rnd(t['close'], 2)}; gap {bh.get('yahoo_vs_nse_close_gap_pct')}%")
    c["market_cap_cr"] = F(f.get("market_cap_cr"), surl, SESSION, "scraped", resc)
    c["sub_sector"] = F(ind.get("Industry"), surl, RUN_DATE, "scraped", json.dumps(ind))
    c["PE"] = F(f.get("pe"), surl, SESSION, "scraped", "screener Stock P/E; " + resc)
    c["sub_sector_median_PE"] = F(med25, "https://www.screener.in" + (href or ""), RUN_DATE, "computed",
                                  f"top-25-by-mcap median; all-pages median {medall}; PE premium vs top25 "
                                  f"{rnd((f['pe'] / med25 - 1) * 100, 2) if f.get('pe') and med25 and f['pe'] > 0 else None}%")
    pbv = f.get("pb_computed") or f.get("pb_from_networth")
    c["PB"] = F(rnd(pbv), surl, SESSION, "computed", "price/book value" if f.get("pb_computed") else "mcap/(equity+reserves) fallback")
    if pr and not pr.get("error"):
        c["sub_sector_median_PB"] = F(pr["median_pb_peers"], pr["industry_url"], RUN_DATE, "computed", f"peer median, n={pr['n_pb']}; premium {pr['pb_premium_vs_median_pct']}%")
        c["sub_sector_median_ROE"] = F(pr["median_roe_peers"], pr["industry_url"], "latest reported", "computed", f"peer median, n={pr['n_roe']}")
    else:
        c["sub_sector_median_PB"] = na("no peer set built for this name")
        c["sub_sector_median_ROE"] = na("no peer set built for this name")
    fe = q.get("forwardEps")
    if fe:
        e0 = next((x for x in (q.get("eps_revision_check") or []) if x["period"] == "0y"), None)
        e1 = next((x for x in (q.get("eps_revision_check") or []) if x["period"] == "+1y"), None)
        alt = []
        if e0 and e0.get("current"):
            alt.append(f"P/E on FY27E consensus EPS {e0['current']} = {round(close / e0['current'], 2)}")
        if e1 and e1.get("current"):
            alt.append(f"P/E on FY28E {e1['current']} = {round(close / e1['current'], 2)}")
        note = f"23-Oct close / Yahoo forwardEps {rnd(fe, 3)} (Yahoo forwardPE {rnd(q.get('forwardPE'), 2)} uses live 26-Oct price). " + "; ".join(alt)
        if s in FWD2:
            note += " | second source: " + FWD2[s]["notes"]
        c["forward_PE"] = F(round(close / fe, 3) if fe > 0 else None, QSURL.format(s), SESSION, "computed", note)
        if s in FWD2:
            c["forward_PE_second_source"] = FWD2[s]
    else:
        c["forward_PE"] = na("Yahoo forwardEps unavailable", QSURL.format(s))
    c["ROE"] = F(f.get("roe"), surl, "latest reported", "scraped")
    c["D/E"] = F(rnd(f.get("debt_to_equity")), surl, f.get("debt_to_equity_as_of"), "computed", f.get("debt_to_equity_notes") or "")
    c["TTM_EPS"] = F(f.get("ttm_eps"), surl, "TTM", "scraped", f"Yahoo trailingEps {q.get('trailingEps')}")
    c["operating_cash_flow_cr"] = F(f.get("ocf_latest_annual_cr"), surl, f.get("ocf_as_of"), "scraped", "latest annual Cash from Operating Activity")
    cg = f.get("cagr") or {}
    c["3y_revenue_CAGR_pct"] = F((cg.get("Compounded Sales Growth") or {}).get("3 Years"), surl, "latest", "scraped")
    c["3y_profit_CAGR_pct"] = F((cg.get("Compounded Profit Growth") or {}).get("3 Years"), surl, "latest", "scraped")
    c["quarterly_results"] = F(f.get("quarters"), surl, (f.get("quarter_dates") or [None])[-1], "scraped", "screener quarterly table, last 6 quarters")
    if pl:
        c["promoter_pledge_pct"] = F(pl.get("value"), pl.get("source_url", ""), pl.get("as_of", ""), pl.get("method", "unavailable"),
                                     f"promoter % {pl.get('promoter_pct')}. " + (pl.get("notes") or ""))
    else:
        c["promoter_pledge_pct"] = na("SHP XBRL not fetched for this name")
    c["adv_20d_value_cr"] = F(bh.get("nse_adv_20s_cr"), BHAV, SESSION, "computed", f"NSE bhavcopy 20 sessions (24 Sep-23 Oct); Yahoo ADV {bh.get('yahoo_adv_20s_cr')}")
    c["52w_high"] = F(t["hi52_used"], yurl, SESSION, "computed",
                      f"series high {rnd(t['series_52w_high'], 2)} on {t.get('series_52w_high_date')}; Yahoo meta 52wH {t.get('meta_52w_high')}; "
                      f"screener 52wH {f.get('high_52w_screener')}; {rnd(t.get('pct_below_52w'), 2)}% below")
    for k in ("ema20", "dma20", "dma50", "dma200"):
        c[k] = F(rnd(t[k], 2), yurl, SESSION, "computed")
    c["dma200_slope"] = F({"change_20_sessions": rnd(t["dma200_change_20_sessions"], 3), "slope_pct_per_session": rnd(t["dma200_slope_pct_per_session"], 4),
                           "rising": t["dma200_rising_20s"]}, yurl, SESSION, "computed", "linear-regression slope of last 20 SMA200 values")
    c["rsi14"] = F(rnd(t["rsi14"], 2), yurl, SESSION, "computed", "Wilder")
    c["atr14"] = F(rnd(t["atr14"], 3), yurl, SESSION, "computed", f"Wilder; {rnd(t['atr14_pct'], 2)}% of close")
    c["avg_volume_20d"] = F(round(t["avg_vol_20d"]), yurl, SESSION, "computed")
    c["last_20_bars"] = F(t.get("last_20_bars"), yurl, SESSION, "computed", "OHLCV daily (IST dates) with vol vs 20d avg, EMA20, RSI14")
    c["last_10_candles"] = F(t.get("last_10_candles"), yurl, SESSION, "computed")
    c["swing_pivots_60s"] = F({"highs": t["pivot_highs_60s"], "lows": t["pivot_lows_60s"]}, yurl, SESSION, "computed", "3-bar fractal pivots, last 60 sessions")
    c["consolidation_range"] = F(t["consolidation"], yurl, SESSION, "computed", "high/low of last 15/20/30/40 sessions")
    c["delivery_pct"] = F({"2026-10-23": bh.get("delivery_pct_2026-10-23"), "avg_20s": bh.get("delivery_pct_avg_20s"), "last_5": bh.get("delivery_pct_last_5")},
                          BHAV, SESSION, "computed")
    c["1m_return_pct"] = F(rnd(t["ret_1m_21d"], 2), yurl, SESSION, "computed", "21 sessions")
    c["3m_return_pct"] = F(rnd(t["ret_3m_63d"], 2), yurl, SESSION, "computed", "63 sessions")
    c["next_results_date"] = results_field(s)
    c["corporate_actions"] = F([x for x in cal_items if x["symbol"] == s], "https://www.nseindia.com/api/corporates-corporateActions ; " + BM_URL, RUN_DATE, "scraped")
    if web.get("corporate_actions_web", {}).get(s):
        c["corporate_actions"]["web_announced"] = web["corporate_actions_web"][s]
        c["corporate_actions"]["notes"] = "web_announced = board-approved actions from company filings not yet in the NSE corporate-actions feed"
    st = [f"ASM {x}" for x in asm_all.get(s, [])] + ([f"GSM {gsm_all[s]}"] if s in gsm_all else []) + (["F&O ban (trade date 26-Oct-2026)"] if s in ban else [])
    c["asm_gsm_fo_ban_status"] = F(st or ["none"], ASM_URL + " ; " + GSM_URL + " ; " + BAN_URL, RUN_DATE, "scraped")
    c["fii_holding_last"] = F(f.get("fii_pct"), surl, f.get("fii_as_of"), "scraped", json.dumps(f.get("fii_change")))
    c["dii_holding_last"] = F(f.get("dii_pct"), surl, f.get("dii_as_of"), "scraped", json.dumps(f.get("dii_change")))
    c["promoter_holding_last"] = F(f.get("promoter_pct") if f.get("promoter_pct") is not None else pl.get("promoter_pct"), surl,
                                   f.get("promoter_as_of") or pl.get("as_of"), "scraped")
    c["analyst_ratings"] = F({"n": q.get("n_analysts"), "recommendationKey": q.get("recommendationKey"), "mean": q.get("recommendationMean"),
                              "target_mean": q.get("target_mean"), "target_median": q.get("target_median"), "target_low": q.get("target_low"),
                              "target_high": q.get("target_high"), "trend": q.get("recommendationTrend")},
                             QSURL.format(s), RUN_DATE, "scraped", "Yahoo quoteSummary (live 26 Oct); web ratings in news.md")
    c["eps_revisions"] = F({"by_period": q.get("eps_revision_check"), "net_downward_fy_90d": q.get("net_downward_fy_eps_revision_90d")}, QSURL.format(s), RUN_DATE, "scraped")
    if s in BANK:
        c["bank_metrics"] = BANK[s]
    if s in CYCL:
        c["EV_EBITDA"] = F({"current_yahoo": q.get("ev_ebitda"), "5y_avg": CYCL[s].get("ev_ebitda_5y_avg", "N/A")}, QSURL.format(s), RUN_DATE, "scraped",
                           "Yahoo enterpriseToEbitda (EV at live 26-Oct price). " + CYCL[s].get("ev_note", ""))
        c["commodity_price_trend"] = F({"brent_close": brent["close"]["value"], "brent_1m_pct": brent["ret_1m_21s_pct"]["value"],
                                        "brent_3m_pct": brent["ret_3m_63s_pct"]["value"], "context": CYCL[s].get("context")},
                                       brent["close"]["source_url"], SESSION, "computed")
    if s in setupc:
        c["post_result_price_action"] = F({k: setupc[s].get(k) for k in ("results_filing_ts_ist", "reaction_session", "prior_close", "reaction_open", "reaction_close",
                                                                        "gap_pct", "reaction_day_return_pct", "post_result_move_pct", "post_result_move_basis",
                                                                        "sessions_since_reaction_incl", "min_close_since", "min_low_since", "held_close",
                                                                        "held_low", "gap_up_held_3plus", "return_since_prior_close_pct", "yoy_from_screener")},
                                          ANN_URL.format(s), SESSION, "computed")
    if row:
        c["screen_flags"] = {"filters": row.get("filters"), "main_screen_fails": row.get("main_screen_fails"), "main_screen_pass": row.get("main_screen_pass"),
                             "main_screen_pass_pledge_confirmed": row.get("main_screen_pass_pledge_confirmed"), "within_5pct_of_pe_test": row.get("within_5pct_of_pe_test"),
                             "pe_premium_vs_top25_pct": row.get("pe_premium_vs_top25_pct"), "financials_variant": row.get("financials_variant"),
                             "financials_variant_pass": row.get("financials_variant_pass")}
    elif s in (trackb_val.get("rows") or {}):
        c["screen_flags"] = trackb_val["rows"][s]
    c["news_ref"] = "news.md#" + s.lower()
    candidates[s] = c

    cross.append({"field": "price", "ticker": s, "source_a": "NSE bhavcopy", "source_b": "Yahoo chart close", "values": [close_nse, rnd(t["close"], 2)],
                  "gap_pct": gap_pct(close_nse, t["close"]), "chosen": "NSE"})
    if q.get("trailingEps") and f.get("pe"):
        ype = close / q["trailingEps"]
        g = gap_pct(f["pe"], ype)
        cross.append({"field": "PE", "ticker": s, "source_a": "screener Stock P/E (23-Oct basis)", "source_b": "23-Oct close / Yahoo trailingEps", "values": [f["pe"], rnd(ype, 2)],
                      "gap_pct": g, "chosen": "screener" + (" (gap>3%: EPS basis differs, e.g. latest quarter not yet in Yahoo TTM / standalone vs consolidated)" if g and g > 3 else "")})
    if q.get("bookValue") and pbv:
        ypb = close / q["bookValue"]
        cross.append({"field": "PB", "ticker": s, "source_a": "screener price/BV", "source_b": "23-Oct close / Yahoo bookValue", "values": [rnd(pbv, 3), rnd(ypb, 3)],
                      "gap_pct": gap_pct(pbv, ypb), "chosen": "screener"})
    if q.get("mcap_cr") and q.get("price") and f.get("market_cap_cr"):
        ym = q["mcap_cr"] * close / q["price"]
        cross.append({"field": "market_cap_cr", "ticker": s, "source_a": "screener", "source_b": "Yahoo marketCap rescaled to 23-Oct close", "values": [f["market_cap_cr"], rnd(ym, 1)],
                      "gap_pct": gap_pct(f["market_cap_cr"], ym), "chosen": "screener"})
    if q.get("roe_yahoo") is not None and f.get("roe") is not None:
        cross.append({"field": "ROE", "ticker": s, "source_a": "screener ROE (annual)", "source_b": "Yahoo returnOnEquity (TTM)", "values": [f["roe"], rnd(q["roe_yahoo"] * 100, 2)],
                      "gap_pct": gap_pct(f["roe"], q["roe_yahoo"] * 100), "chosen": "screener (basis differs: annual vs TTM)"})
    if f.get("high_52w_screener"):
        cross.append({"field": "52w_high", "ticker": s, "source_a": "Yahoo (meta/series)", "source_b": "screener High", "values": [t["hi52_used"], f["high_52w_screener"]],
                      "gap_pct": gap_pct(t["hi52_used"], f["high_52w_screener"]), "chosen": "Yahoo (screener rounds; may include intraday spikes differently)"})
    if q.get("dma50_yahoo"):
        cross.append({"field": "dma50", "ticker": s, "source_a": "computed (to 23 Oct)", "source_b": "Yahoo fiftyDayAverage (live 26 Oct)", "values": [rnd(t["dma50"], 2), rnd(q["dma50_yahoo"], 2)],
                      "gap_pct": gap_pct(t["dma50"], q["dma50_yahoo"]), "chosen": "computed"})
    if q.get("dma200_yahoo"):
        cross.append({"field": "dma200", "ticker": s, "source_a": "computed (to 23 Oct)", "source_b": "Yahoo twoHundredDayAverage (live 26 Oct)", "values": [rnd(t["dma200"], 2), rnd(q["dma200_yahoo"], 2)],
                      "gap_pct": gap_pct(t["dma200"], q["dma200_yahoo"]), "chosen": "computed"})

cross.append({"field": "nifty500_close", "ticker": "NIFTY 500", "source_a": "NSE ind_close_all", "source_b": "Yahoo ^CRSLDX",
              "values": [n500_nse["close_2026-10-23"], rnd(indices["nifty500"]["close"], 2)],
              "gap_pct": gap_pct(n500_nse["close_2026-10-23"], indices["nifty500"]["close"]), "chosen": "NSE"})
if n50_nse:
    cross.append({"field": "nifty50_close", "ticker": "NIFTY 50", "source_a": "NSE ind_close_all", "source_b": "Yahoo ^NSEI",
                  "values": [n50_nse.get("close_2026-10-23"), rnd(indices["nifty50"]["close"], 2)],
                  "gap_pct": gap_pct(n50_nse.get("close_2026-10-23"), indices["nifty50"]["close"]), "chosen": "NSE"})
cross.append({"field": "price_all_bhav_names", "ticker": "*", "source_a": "NSE bhavcopy", "source_b": "Yahoo", "values": None,
              "gap_pct": max(abs(v.get("yahoo_vs_nse_close_gap_pct") or 0) for v in bhav.values()), "chosen": "NSE",
              "notes": f"max abs gap across {len(bhav)} Nifty 500 + Microcap 250 names"})
cross += web.get("cross_checks_extra", [])
flagged = [x for x in cross if x.get("gap_pct") and x["gap_pct"] > 3]


def _v(c, k):
    v = (c.get(k) or {}).get("value")
    return v if isinstance(v, (int, float)) else None


for x in flagged:
    c = candidates.get(x["ticker"])
    if not c or not x.get("values") or None in x["values"]:
        continue
    a, b = x["values"][:2]
    thr = {"PE": _v(c, "sub_sector_median_PE"), "PB": _v(c, "sub_sector_median_PB"), "ROE": 12.0,
           "market_cap_cr": 5000.0 if (c.get("market_cap_cr") or {}).get("value", 0) < 12000 else 12000.0}.get(x["field"])
    if thr is None:
        continue
    same = (a < thr) == (b < thr) if x["field"] in ("PE", "PB") else (a > thr) == (b > thr)
    x["screen_impact"] = (f"none: both values on same side of threshold {rnd(thr, 2)}" if same
                          else f"CHANGES OUTCOME vs threshold {rnd(thr, 2)}: source_b would flip this filter")

# ---------------------------------------------------------------- track B and setup C sections
track_b = {
    "purpose": "Pre-fetched 5,000-12,000 Cr band, used ONLY if the analyst's mcap relaxation triggers (Stage 3 survivors < 10 at 12,000 Cr).",
    "universe": "Nifty Microcap 250 (niftyindices CSV) + Nifty 500 names with screener mcap 5,000-12,000 Cr",
    "momentum_test": "close >= 0.75 x 52wH AND close > SMA50 AND (SMA50 > SMA200 OR SMA200 rising 20s) AND 3M return > Nifty 500 3M return "
                     f"({rnd(trackb['nifty500_ret_3m'], 2)}%)",
    "as_of": SESSION, "method": "computed",
    "counts": trackb_val.get("counts"),
    "momentum_pass": trackb_val.get("momentum_pass"),
    "value_test": trackb_val.get("value_test"),
    "value_pass": trackb_val.get("value_pass"),
    "rows": trackb_val.get("rows"),
}
setup_c = {
    "definition": "Nifty 500 / Microcap 250 names with a Q2 FY27 results board meeting 1-25 Oct 2026 (NSE board-meeting API, past dates). "
                  "Results timestamp from NSE corporate-announcements. Reaction session = results day if filed before 15:30 IST, else next session. "
                  "Post-result move = reaction-session open vs prior close (after-market filings) or reaction-day close vs prior close (intraday filings). "
                  "Held = every close since the reaction session >= the pre-result close. Eligible = move > 0, held, >= 3 sessions, mcap >= 5,000 Cr, ADV >= 25 Cr.",
    "as_of": SESSION, "method": "computed",
    "eligible": sorted(setupc_list),
    "watch_held_lt3_sessions": sorted(s for s, r in setupc.items() if r.get("setup_c_watch_lt3_sessions")),
    "reported_after_23oct_close_reaction_pending": sorted(s for s, r in setupc.items() if r.get("reaction_session") is None),
    "rows": {s: {k: v for k, v in r.items() if k != "last_bars"} | {"last_bars": r.get("last_bars")} for s, r in setupc.items()},
    "revenue_pat_yoy_notes": "YoY from screener quarterly table (Sep-2026 vs Sep-2025 columns; consolidated page where available). Company releases in news.md.",
}

track_b["microcap_mcap_ge_12000_belongs_in_track_a"] = sorted(
    s for s in (trackb_val.get("momentum_pass") or []) if s in micro and ((fun.get(s) or {}).get("market_cap_cr") or 0) >= 12000)


# ---------------------------------------------------------------- follow-ups from the 2026-10-19 run
def bhav_ohlc(sym, dates):
    out = []
    for d in dates:
        fn = os.path.join(MISC, "sec_bhavdata_full_%s.csv" % datetime.date.fromisoformat(d).strftime("%d%m%Y"))
        for r in csv.reader(open(fn)):
            if r and r[0].strip() == sym and r[1].strip() == "EQ":
                out.append({"date": d, "prev_close": float(r[3]), "open": float(r[4]), "high": float(r[5]), "low": float(r[6]), "close": float(r[8]),
                            "volume": int(r[10]), "delivery_pct": float(r[14]) if r[14].strip() not in ("-", "") else None,
                            "source_url": "https://nsearchives.nseindia.com/products/content/" + os.path.basename(fn)})
    return out


SB_PLAN = {"entry_low": 50.70, "entry_high": 51.50, "stop": 48.90, "t1": 56.82, "cancel_if_not_filled_by": "2026-10-23"}
sb_bars = bhav_ohlc("SOUTHBANK", ["2026-10-16", "2026-10-19", "2026-10-21", "2026-10-22", "2026-10-23"])
sb_live = [x for x in sb_bars if x["date"] >= "2026-10-19"]
sb_fill = next((x for x in sb_live if x["low"] <= SB_PLAN["entry_high"] and x["high"] >= SB_PLAN["entry_low"]), None)
sb_after = [x for x in sb_live if sb_fill and x["date"] >= sb_fill["date"]]
followups = {
    "SOUTHBANK_pick_2026-10-19": {
        "plan": SB_PLAN,
        "daily_ohlc_nse_bhavcopy": sb_bars,
        "facts": {
            "first_session_range_overlapping_entry_zone": sb_fill["date"] if sb_fill else None,
            "that_session_open": sb_fill["open"] if sb_fill else None,
            "open_inside_entry_zone": bool(sb_fill and SB_PLAN["entry_low"] <= sb_fill["open"] <= SB_PLAN["entry_high"]),
            "min_low_from_fill_session": min(x["low"] for x in sb_after) if sb_after else None,
            "stop_touched": any(x["low"] <= SB_PLAN["stop"] for x in sb_after),
            "max_high_from_fill_session": max(x["high"] for x in sb_after) if sb_after else None,
            "t1_reached": any(x["high"] >= SB_PLAN["t1"] for x in sb_after),
            "close_2026-10-23": sb_live[-1]["close"] if sb_live else None,
            "close_2026-10-23_vs_entry_high_pct": rnd((sb_live[-1]["close"] / SB_PLAN["entry_high"] - 1) * 100, 2) if sb_live else None,
        },
        "as_of": SESSION, "method": "scraped",
        "notes": "Order-fill mechanics not modelled; facts are bhavcopy OHLC comparisons only. 20-Oct NSE holiday (Dussehra).",
    },
    "watchlist_2026-10-19": {s: {"next_results_date": results_field(s),
                                 "close_2026-10-23": (bhav.get(s) or {}).get("nse_close_2026-10-23"),
                                 "q2fy27_results_out": bool(s in setupc and setupc[s].get("results_filing_ts_ist"))}
                             for s in ("REDINGTON", "TANLA", "JAMNAAUTO")},
}

# ---------------------------------------------------------------- regime inputs (no judgement)
regime = {
    "nifty50": {k: market["nifty50"][k] for k in ("close", "ema20", "sma20", "sma50", "sma200", "rsi14", "close_vs_sma20", "close_vs_sma50", "close_vs_sma200",
                                                  "ret_1m_21s_pct", "ret_3m_63s_pct", "dma200_change_20_sessions")},
    "nifty500": {k: market["nifty500"][k] for k in ("close", "sma20", "sma50", "sma200", "rsi14", "close_vs_sma20", "close_vs_sma50", "close_vs_sma200",
                                                    "ret_1m_21s_pct", "ret_3m_63s_pct", "dma200_change_20_sessions")},
    "india_vix": {"close": market["india_vix"]["close"], "trend_1m": market["india_vix"]["trend_1m"]},
    "breadth_pct_nifty500_above_50dma": breadth["computed"]["value"]["above_50dma_pct"],
    "breadth_published": [x["value"].get("above_50dma_pct") for x in breadth["published_cross_checks"]],
    "fii_dii_week": {k: market["fii_dii_flows"][k]["value"] for k in ("fii_net_week_19_23_oct_cr", "dii_net_week_19_23_oct_cr") if k in market["fii_dii_flows"]},
    "top5_rs_1m": sectors_out["top5_rs_1m"], "top5_rs_3m": sectors_out["top5_rs_3m"],
    "as_of": SESSION, "method": "computed", "notes": "Inputs only; regime classification is the analyst's job.",
}

gaps = web.get("gaps", [])

data = {
    "run_date_ist": RUN_DATE,
    "data_as_of_session": SESSION,
    "data_mode": "WEB",
    "mcp_error": "screener / screener-core MCP namespaces are absent from the tool catalog in this environment (GetDynamicTools full catalog lists only cursor, "
                 "Cursor Automation Tools, cursor-cloud, cursor-subscriptions; pattern search 'screener' returned 0 matches). Not authenticated, per run rules.",
    "regime": regime,
    "followups": followups,
    "market": market,
    "sectors": sectors_out,
    "breadth": breadth,
    "macro_calendar": macro,
    "universe_screen": universe_screen,
    "universe_screen_financials": universe_screen_fin,
    "track_b_5k": track_b,
    "setup_c_candidates": setup_c,
    "sub_sector_medians": sub_sector_medians,
    "candidates": candidates,
    "surveillance": surveillance,
    "corporate_calendar_next_15_sessions": corp_cal,
    "results_window": results_window,
    "cross_checks": {"rule": "gap > 3% -> prefer NSE/BSE > screener > others", "items": cross, "flagged_gt_3pct": flagged},
    "gaps": gaps,
}
json.dump(data, open(os.path.join(OUT, "data.json"), "w"), indent=1, default=str)
print("candidates", len(candidates), "cross", len(cross), "flagged", len(flagged), "size", os.path.getsize(os.path.join(OUT, "data.json")))
for s, c in candidates.items():
    if "error" in c:
        print(s, c["error"])
        continue
    print(f"{s:11s} {','.join(c['roles'])[:60]:60s} mcap={c['market_cap_cr']['value']} pe={c['PE']['value']} med={c['sub_sector_median_PE']['value']} "
          f"tech={c['tech_rule']} res={json.dumps(c['next_results_date']['value'])[:70]}")
print("top1", sectors_out["top5_rs_1m"])
print("top3", sectors_out["top5_rs_3m"])

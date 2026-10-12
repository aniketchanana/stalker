#!/usr/bin/env python3
"""Assemble data.json for run 2026-10-12 from fetched/computed artifacts. No invented numbers."""
import json, csv, os, sys, datetime, statistics

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from compute_indicators import parse_chart, compute_from_rows

RAW = "/workspace/work/2026-10-12/raw"
CMP = os.path.join(RAW, "computed")
OUT = "/workspace/work/2026-10-12"
MISC = "/tmp/swing-2026-10-12/misc"
CHARTS = "/tmp/swing-2026-10-12/charts"
SESSION = "2026-10-09"
WINDOW_END = "2026-11-02"


def L(name, base=CMP):
    return json.load(open(os.path.join(base, name)))


tech = L("tech.json", "/tmp/swing-2026-10-12/misc/full") if os.path.exists("/tmp/swing-2026-10-12/misc/full/tech.json") else L("tech.json")
fun = L("screener_fundamentals.json")
summary = L("summary.json")
indices = L("indices.json")
inds = L("industry_medians.json", "/tmp/swing-2026-10-12/misc/full") if os.path.exists("/tmp/swing-2026-10-12/misc/full/industry_medians.json") else L("industry_medians.json")
qs = L("quotesummary.json")
screen = L("screen_result.json")
pledge = L("pledge.json")
peers = L("peer_pb_roe.json")
sectors = L("sectors.json")
bhav = L("nse_bhav_summary.json")
cands = L("candidate_list.json")
bm_range = L("bm_range.json", MISC)
ca = L("ca.json", MISC)
fiidii = L("fiidii.json", MISC)
asm = L("nse_api_reportASM.json", MISC)
gsm = L("nse_api_reportGSM.json", MISC)
hol = L("nse_api_holiday-master_type_trading.json", MISC)
univ = {r["Symbol"].strip(): r for r in csv.DictReader(open(os.path.join(RAW, "ind_nifty500list.csv")))}


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


SCR = "https://www.screener.in/company/{}/consolidated/"
YF = "https://query1.finance.yahoo.com/v8/finance/chart/{}?interval=1d&range=1y"
QSURL = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{}.NS"
BHAV = "https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_09102026.csv"
INDCLOSE = "https://nsearchives.nseindia.com/content/indices/ind_close_all_09102026.csv"
BM_URL = "https://www.nseindia.com/api/corporate-board-meetings?index=equities"
ASM_URL = "https://www.nseindia.com/api/reportASM"
GSM_URL = "https://www.nseindia.com/api/reportGSM"
BAN_URL = "https://nsearchives.nseindia.com/content/fo/fo_secban.csv"
FIIDII_URL = "https://www.nseindia.com/api/fiidiiTradeReact"
HOL_URL = "https://www.nseindia.com/api/holiday-master?type=trading"

# ---------------------------------------------------------------- market
def index_block(key, ysym, label):
    t = indices[key]
    url = YF.format(ysym)
    out = {
        "label": label,
        "close": F(rnd(t["close"], 2), url, t["as_of"], "computed", "Yahoo daily chart last bar (IST date)"),
        "sma20": F(rnd(t["dma20"], 2), url, t["as_of"], "computed"),
        "sma50": F(rnd(t["dma50"], 2), url, t["as_of"], "computed"),
        "sma200": F(rnd(t["dma200"], 2), url, t["as_of"], "computed"),
        "ema20": F(rnd(t["ema20"], 2), url, t["as_of"], "computed"),
        "rsi14": F(rnd(t["rsi14"], 2), url, t["as_of"], "computed", "Wilder RSI(14)"),
        "atr14": F(rnd(t["atr14"], 2), url, t["as_of"], "computed", "Wilder ATR(14)"),
        "dma200_change_20_sessions": F(rnd(t["dma200_change_20_sessions"], 2), url, t["as_of"], "computed"),
        "ret_1w_5s_pct": F(rnd(t["ret_1w_5d"], 3), url, t["as_of"], "computed"),
        "ret_1m_21s_pct": F(rnd(t["ret_1m_21d"], 3), url, t["as_of"], "computed"),
        "ret_3m_63s_pct": F(rnd(t["ret_3m_63d"], 3), url, t["as_of"], "computed"),
        "52w_high": F(rnd(t["hi52_used"], 2), url, t["as_of"], "computed", f"series high date {t.get('series_52w_high_date')}"),
        "52w_low": F(rnd(t["series_52w_low"], 2), url, t["as_of"], "computed", f"series low date {t.get('series_52w_low_date')}"),
        "close_vs_sma20": "above" if t["close"] > t["dma20"] else "below",
        "close_vs_sma50": "above" if t["close"] > t["dma50"] else "below",
        "close_vs_sma200": "above" if t["close"] > t["dma200"] else "below",
    }
    return out


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
market["nifty500"]["close"]["notes"] += f"; NSE ind_close_all 09-10-2026 close {n500_nse['close_2026-10-09']} (match)"
market["nifty500"]["official_pe_pb"] = F({"pe": n500_nse["pe"], "pb": n500_nse["pb"]}, INDCLOSE, "2026-10-09", "scraped")
vt = summary["vix_trend"]
market["india_vix"]["trend_1m"] = F({"now": rnd(vt["now"], 2), "ago_21_sessions": rnd(vt["ago_21_sessions"], 2), "ago_date": vt["ago_date"],
                                     "change_pct": rnd(vt["change_pct"], 2), "direction": vt["direction"],
                                     "last_10_closes": [[d, rnd(v, 2)] for d, v in vt["last_10_closes"]]},
                                    YF.format("%5EINDIAVIX"), vt["now_date"], "computed")
market["india_vix"]["vs_sma20"] = "above" if vt["now"] > indices["india_vix"]["dma20"] else "below"
market["india_vix"]["vs_sma50"] = "above" if vt["now"] > indices["india_vix"]["dma50"] else "below"

fii = {r["category"]: r for r in fiidii}
market["fii_dii_flows"] = {
    "fii_fpi_net_cr": F(float(fii["FII/FPI"]["netValue"]), FIIDII_URL, fii["FII/FPI"]["date"], "scraped",
                        f"buy {fii['FII/FPI']['buyValue']} / sell {fii['FII/FPI']['sellValue']} (NSE provisional, cash)"),
    "dii_net_cr": F(float(fii["DII"]["netValue"]), FIIDII_URL, fii["DII"]["date"], "scraped",
                    f"buy {fii['DII']['buyValue']} / sell {fii['DII']['sellValue']}"),
    "fii_net_2026-10-08_cr": F(-12943.58, "https://www.etnownews.com/markets/stock-market-closing-today-oct-9-sensex-closes-879-pts-higher-nifty-ends-above-22500-top-gainers-and-losers-article", "2026-10-08", "websearch", "ET Now"),
    "week_to_2026-10-09": F({"fii_net_cr": -30294, "dii_net_cr": 30313}, "https://www.kotakneo.com/news/market-news/fii-selling-continues-for-eight-weeks-as-diis-offset-outflows/", "2026-10-09", "websearch", "8th straight week of FII selling (Kotak Neo)"),
    "october_to_date": F({"fii_net_cr": -39779, "dii_net_cr": 40355}, "https://www.kotakneo.com/news/market-news/fii-selling-continues-for-eight-weeks-as-diis-offset-outflows/", "2026-10-09", "websearch",
                         "NDTV Profit cites FPI -44,166 Cr Oct-to-date (NSDL-style, different methodology)"),
}


def brent_block():
    p = os.path.join(CHARTS, "IDX_BZ_F.json")
    pc = parse_chart(p)
    rows = [r for r in pc["rows"] if r["date"] <= SESSION]
    c = compute_from_rows(rows, pc["meta"])
    url = YF.format("BZ%3DF")
    return {
        "close": F(rnd(rows[-1]["close"], 2), url, rows[-1]["date"], "computed", "Yahoo BZ=F front-month; bars after 2026-10-09 excluded"),
        "ret_1m_21s_pct": F(rnd(c["ret_1m_21d"], 2), url, rows[-1]["date"], "computed"),
        "ret_3m_63s_pct": F(rnd(c["ret_3m_63d"], 2), url, rows[-1]["date"], "computed"),
        "sma50": F(rnd(c["dma50"], 2), url, rows[-1]["date"], "computed"),
        "sma200": F(rnd(c["dma200"], 2), url, rows[-1]["date"], "computed"),
    }


market["brent_usd"] = brent_block()
ui = parse_chart(os.path.join(CHARTS, "IDX_USDINR_X.json"))
ui_rows = [r for r in ui["rows"] if r["date"] <= SESSION]
market["usdinr"] = F(rnd(ui_rows[-1]["close"], 3), YF.format("USDINR%3DX"), ui_rows[-1]["date"], "computed", "Yahoo USDINR=X; bars after 2026-10-09 excluded")

# ---------------------------------------------------------------- sectors
sec_rows = []
for name, s in sectors["sectors"].items():
    sec_rows.append({"index": name, "close": s.get("close_2026-10-09"), "pe": s.get("pe"), "pb": s.get("pb"),
                     "ret_1w_pct": s.get("ret_1w_5s_pct"), "ret_1m_pct": s.get("ret_1m_21s_pct"), "ret_3m_pct": s.get("ret_3m_63s_pct"),
                     "rs_1w_pp": s.get("rs_1w_5s_vs_nifty500_pp"), "rs_1m_pp": s.get("rs_1m_21s_vs_nifty500_pp"), "rs_3m_pp": s.get("rs_3m_63s_vs_nifty500_pp")})
valid1 = [r for r in sec_rows if r["rs_1m_pp"] is not None]
valid3 = [r for r in sec_rows if r["rs_3m_pp"] is not None]
top1 = sorted(valid1, key=lambda r: -r["rs_1m_pp"])
top3 = sorted(valid3, key=lambda r: -r["rs_3m_pp"])
sectors_out = {
    "value": sec_rows,
    "benchmark": {"nifty500_ret_1m_pct": n500_nse["ret_1m_21s_pct"], "nifty500_ret_3m_pct": n500_nse["ret_3m_63s_pct"],
                  "nifty500_ret_1w_pct": n500_nse["ret_1w_5s_pct"]},
    "base_dates": sectors["dates"],
    "top5_rs_1m": [(r["index"], r["rs_1m_pp"]) for r in top1[:5]],
    "top5_rs_3m": [(r["index"], r["rs_3m_pp"]) for r in top3[:5]],
    "bottom5_rs_1m": [(r["index"], r["rs_1m_pp"]) for r in top1[-5:]],
    "bottom5_rs_3m": [(r["index"], r["rs_3m_pp"]) for r in top3[-5:]],
    "source_url": "https://nsearchives.nseindia.com/content/indices/ind_close_all_<DDMMYYYY>.csv (09102026, 01102026, 08092026, 10072026)",
    "as_of": SESSION,
    "method": "computed",
    "notes": "Official NSE index closes; 1M = 21 sessions, 3M = 63 sessions; RS = sector return minus Nifty 500 return (pp).",
}

# ---------------------------------------------------------------- breadth
b = summary["breadth"]
breadth = {
    "computed": F({"above_20dma_pct": b["above_20dma_pct"], "above_50dma_pct": b["above_50dma_pct"], "above_200dma_pct": b["above_200dma_pct"],
                   "above_50dma": f"{b['above_50dma_count']}/{b['sample_with_50dma']}", "above_200dma": f"{b['above_200dma_count']}/{b['sample_with_200dma']}",
                   "nifty50_above_50dma_pct": b["nifty50_above_50dma_pct"], "nifty50_above_50dma": b["nifty50_above_50dma"]},
                  "Yahoo v8 chart per Nifty 500 constituent", SESSION, "computed", b["universe"]),
    "published_cross_checks": [
        F({"above_50dma_pct": 18, "above_200dma_pct": 38, "nifty50_above_50dma_pct": 14}, "https://punji.ai/stories/market-breadth", SESSION, "websearch", "Punji"),
        F({"above_50dma_pct": 16.0, "above_200dma_pct": 35.0, "advance_decline": "340/157"}, "https://indexbreadth.com/learn/market-breadth-eod-9-october-2026/", SESSION, "websearch", "IndexBreadth"),
        F({"above_50dma_pct": 20.2, "above_200dma_pct": 43.8, "new_highs": 5, "new_lows": 29}, "https://flashfinance.news/market-breadth/", SESSION, "websearch", "Flash Finance top-500 proxy"),
    ],
}

# ---------------------------------------------------------------- macro calendar
holidays = [h for h in hol.get("CM", []) if datetime.datetime.strptime(h["tradingDate"], "%d-%b-%Y").date() >= datetime.date(2026, 10, 1)]
macro = {
    "rbi": F({"date": "2026-10-07", "decision": "repo +25 bp to 5.50% (SDF 5.25%, MSF 5.75%)", "stance": "calibrated tightening",
              "fy27_gdp_proj_pct": 7.1, "fy27_cpi_proj_pct": 5.2, "vote_on_stance": "4:2 (CNBC-TV18)"},
             "https://www.rbi.org.in/scripts/BS_PressReleaseDisplay.aspx?prid=63742", "2026-10-07", "websearch", "Next MPC date not retrieved (N/A)"),
    "fed": F({"last": "Sep 15-16 FOMC +25 bp to 3.75-4.00%", "next_meeting": "2026-10-27/28", "decision_time": "2026-10-28 14:00 ET (2026-10-28 23:30 IST)", "following": "2026-12-08/09"},
             "https://www.federalreserve.gov/monetarypolicy/fomccalendars.htm", "2026", "websearch", "Sep hike per fedratecalc.com"),
    "india_cpi_sep": F("2026-10-12 16:00 IST", "https://www.kotakneo.com/news/market-news/pre-market-12-october-2026-gift-nifty-hints-at-mild-gap-up-opening/", "2026-10-12", "websearch"),
    "india_wpi_sep": F("2026-10-14 (Wednesday)", "https://www.cnbctv18.com/market/trade-setup-nifty-prediction-october-12-buy-sell-key-levels-triggers-q2-results-banks-midcaps-oil-rupee-yields-rbi-20009196.htm", "2026-10-11", "websearch"),
    "q2fy27_results_season": F({"started": "TCS 2026-10-08", "this_week": "HCLTECH/RBLBANK/ICICIAMC 12 Oct; Wipro/TechM/Persistent/Nestle/JioFin/KVB 15 Oct; HDFCBANK/ICICIBANK/AXISBANK/YESBANK Sat 17 Oct",
                                "statutory_deadline": "2026-11-14 (45 days after quarter end)"},
                               "https://economictimes.indiatimes.com/markets/stocks/earnings/", "2026-10-11", "websearch"),
    "nse_holidays_from_oct_2026": F([{"date": h["tradingDate"], "day": h["weekDay"], "desc": h["description"]} for h in holidays], HOL_URL, "2026-10-12", "scraped",
                                    "Diwali Laxmi Pujan 8 Nov is a Sunday (Muhurat session timing per NSE circular, not retrieved)"),
    "results_window_15_sessions": F({"start": "2026-10-12", "end": WINDOW_END, "count_rule": "12 Oct = day 1; excludes weekends and 20 Oct (Dussehra)",
                                     "sessions": ["2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15", "2026-10-16", "2026-10-19", "2026-10-21", "2026-10-22",
                                                  "2026-10-23", "2026-10-26", "2026-10-27", "2026-10-28", "2026-10-29", "2026-10-30", "2026-11-02"]},
                                    HOL_URL, "2026-10-12", "computed"),
}

# ---------------------------------------------------------------- screen
QUERY = ("Market Capitalization > 12000 AND Price to earning < Industry PE AND Price to earning > 0 AND Return on equity > 12 AND "
         "Debt to equity < 1 AND Pledged percentage < 20 AND Current price > DMA 50 AND DMA 50 > DMA 200 AND Current price > High price * 0.75")
rows = screen["rows"]
universe_screen = {
    "query": QUERY,
    "source": "Rebuilt: Nifty 500 constituents (niftyindices CSV) -> Yahoo 1y daily (technicals, computed) -> screener.in company pages (fundamentals) -> screener.in industry pages (industry PE) -> NSE SHP XBRL (pledge)",
    "as_of": SESSION,
    "method": "computed",
    "technical_rules": {"A": "close > SMA50 > SMA200 and close > 0.75 x 52wH (literal query)",
                        "B": "close > SMA50, SMA50 <= SMA200 but SMA200 rising over 20 sessions, close > 0.75 x 52wH (secondary, flagged)"},
    "industry_pe_basis": "Primary: median positive P/E of top-25-by-mcap peers on screener industry page 1 (same basis as last week). Secondary flag: median across all pages.",
    "step_counts": screen["step_counts"],
    "main_pass": screen["main_pass"],
    "main_pass_pledge_confirmed_lt_20": screen["main_pass_pledge_confirmed"],
    "pe_lt_industry_top25": screen["pe_lt_industry_top25"],
    "pe_lt_industry_allpages": screen["pe_lt_industry_allpages"],
    "pe_within_5pct_top25": screen["pe_within_5pct_top25"],
    "tech_rule_A": summary["tech_rule_A"],
    "tech_rule_B": summary["tech_rule_B"],
    "rows": {s: {k: (rnd(v) if isinstance(v, float) else v) for k, v in r.items() if k not in ("company",)} for s, r in rows.items()},
    "notes": "KPIL fails pledge (24.55%). REDINGTON has no promoter group (pledge N/A, not failed). Bank/NBFC D/E = borrowings/(equity+reserves), excludes deposits. AEGISLOG industry ('Trading - Gas') median PE unavailable (industry page not in fetched set).",
}
universe_screen_fin = {
    "query": "Mcap > 12000 AND PE > 0 AND PB < sub-sector peer median PB (fallback PB < 3 when no peer median) AND ROE > 12 AND technical pass (rule A or B); D/E ignored",
    "as_of": SESSION,
    "method": "computed",
    "financials_in_techpass": screen["financials_in_techpass"],
    "tickers": screen["financials_variant_pass"],
    "count": len(screen["financials_variant_pass"]),
    "rows": {s: rows[s]["financials_variant"] | {"pb": rnd(rows[s]["pb"]), "median_pb_peers": rows[s]["median_pb_peers"], "roe": rows[s]["roe"],
                                                 "pass": rows[s]["financials_variant_pass"]} for s in screen["financials_in_techpass"]},
    "notes": "Peer-median PB (top up-to-12 by mcap from screener industry page) replaced last week's PB<3 proxy. KARURVYSYA (2.33 vs 1.66), CUB (2.16 vs 1.66), MAHABANK (1.79 vs 0.945) fail PB-vs-median.",
}

# ---------------------------------------------------------------- sub-sector medians
ind_by_href = {}
for h, v in inds.items():
    ind_by_href[h.rstrip("/") + "/"] = v
sub_sector_medians = {}
for s, p in peers.items():
    href = (fun.get(s) or {}).get("industry_href") or ""
    im = ind_by_href.get(href.rstrip("/") + "/") if href else None
    sub_sector_medians[s] = {
        "industry": p["industry"],
        "industry_url": p["industry_url"],
        "peer_rule": p["peer_rule"],
        "peers": [{"ticker": x.get("ticker"), "mcap_cr": x.get("mcap_cr"), "pb": x.get("pb"), "pb_basis": x.get("pb_basis"), "roe": x.get("roe")} for x in p["peers"]],
        "median_pb": F(p["median_pb_peers"], p["industry_url"], "2026-10-09/12 (page fetch)", "computed", f"n={p['n_pb']}"),
        "median_roe": F(p["median_roe_peers"], p["industry_url"], "latest reported", "computed", f"n={p['n_roe']}"),
        "median_pe_top25": F(im["median_pe_top25_mcap"] if im else None, p["industry_url"], "2026-10-09/12", "computed", f"n={im['n_pe_top25_mcap'] if im else None}"),
        "median_pe_allpages": F(im["median_pe"] if im else None, p["industry_url"], "2026-10-09/12", "computed", f"n={im['n_pe'] if im else None}"),
        "subject_pb": p["subject_pb"], "subject_roe": p["subject_roe"],
        "pb_premium_vs_median_pct": p["pb_premium_vs_median_pct"],
    }

# ---------------------------------------------------------------- surveillance
asm_rows = []
for term in ("longterm", "shortterm"):
    for r in asm[term]["data"]:
        if r["symbol"] in univ:
            asm_rows.append({"symbol": r["symbol"], "term": term, "stage": r["asmSurvIndicator"], "desc": r["survDesc"], "as_of": r["asmTime"]})
gsm_rows = [{"symbol": r["symbol"], "stage": r["gsmStage"], "desc": r["survDesc"]} for r in gsm if r["symbol"] in univ]
ban = [l.split(",")[1].strip() for l in open(os.path.join(MISC, "fo_secban.csv")).read().splitlines()[1:] if "," in l]
asm_map = {r["symbol"]: r for r in asm_rows}
surveillance = {
    "asm_nifty500": F(asm_rows, ASM_URL, "2026-10-12", "scraped"),
    "gsm_nifty500": F(gsm_rows, GSM_URL, "2026-10-12", "scraped", "none of Nifty 500 on GSM" if not gsm_rows else ""),
    "fo_ban_trade_date_2026-10-12": F(ban, BAN_URL, "2026-10-12", "scraped"),
    "bulk_deals_2026-10-09_techpass": F([], "https://nsearchives.nseindia.com/content/equities/bulk.csv", SESSION, "scraped", "No technical-pass names in 9 Oct bulk deals; block-deal file had no records. Historical deal API blocked."),
}

# ---------------------------------------------------------------- calendar
def d(s):
    return datetime.datetime.strptime(s, "%d-%b-%Y").date()


cal_items = []
seen = set()
for bmr in bm_range:
    s = bmr["bm_symbol"]
    if s not in univ:
        continue
    dt = d(bmr["bm_date"])
    if not (datetime.date(2026, 10, 12) <= dt <= datetime.date(2026, 11, 2)):
        continue
    key = (s, dt)
    if key in seen:
        continue
    seen.add(key)
    cal_items.append({"date": dt.isoformat(), "symbol": s, "event": bmr["bm_desc"][:220], "source": BM_URL, "method": "scraped"})
for c in ca:
    if c["symbol"] in univ:
        cal_items.append({"date": d(c["exDate"]).isoformat(), "symbol": c["symbol"], "event": f"Ex-date: {c['subject']}", "source": "https://www.nseindia.com/api/corporates-corporateActions", "method": "scraped"})
cal_items += [
    {"date": "2026-10-12", "symbol": "MACRO", "event": "India CPI (Sep) 16:00 IST", "source": macro["india_cpi_sep"]["source_url"], "method": "websearch"},
    {"date": "2026-10-14", "symbol": "MACRO", "event": "India WPI (Sep)", "source": macro["india_wpi_sep"]["source_url"], "method": "websearch"},
    {"date": "2026-10-17", "symbol": "HDFCBANK/ICICIBANK/AXISBANK/YESBANK", "event": "Q2 results (Saturday)", "source": "Economic Times earnings tracker", "method": "websearch"},
    {"date": "2026-10-20", "symbol": "HOLIDAY", "event": "NSE closed - Dussehra", "source": HOL_URL, "method": "scraped"},
    {"date": "2026-10-28", "symbol": "MACRO", "event": "FOMC decision 14:00 ET", "source": macro["fed"]["source_url"], "method": "websearch"},
]
cal_items.sort(key=lambda x: (x["date"], x["symbol"]))
corp_cal = {"through": WINDOW_END, "window_rule": macro["results_window_15_sessions"]["value"]["count_rule"],
            "items": cal_items,
            "already_reported_q2fy27_among_candidates": [],
            "notes": "NSE board-meeting API scanned 15 Sep-11 Oct: no candidate has reported Q2 FY27 yet. Only Nifty 500 names included."}

# ---------------------------------------------------------------- candidates
RESULTS_WEB = {
    "CYIENT": ("2026-10-22", "https://bazaarwatch.com/announcement/198987/cyient-ltd-cyient-ltdhas-informed-bse-that-the-meeting-of-the-board-of-directors-of-the-company-is-s", "BSE filing 7 Oct; also NSE BM API"),
    "CUB": ("2026-10-28", "https://www.psuconnect.in/financial/city-union-bank-q2-fy27-results-on-october-28-trading-window-to-reopen-on-october-31", "Filing 9 Oct; NSE BM API agrees; Yahoo shows 2026-11-02 (rejected)"),
    "BHEL": ("2026-10-14", "https://flashfinance.news/stocks/BHEL", "also NSE BM API"),
}
UNCONFIRMED = {
    "PNB": "Not announced; trading window closed from 1 Oct; Yahoo shows 2026-10-15, TipRanks estimate 22 Oct (both unconfirmed)",
    "GESHIP": "Not announced (Livemint/IIFL board-meeting lists; Univest)",
    "PETRONET": "Not announced (last BM 12 Aug for Q1); Yahoo estimate 2026-11-05",
    "ENGINERSIN": "Not announced (last BM 13 Aug for Q1)",
    "KPIL": "Not announced as of 15 Sep (Univest/Trendlyne); Yahoo estimate 2026-10-29",
    "LICHSGFIN": "Not announced (last BM 30 Jul); Yahoo estimate 2026-10-28",
    "PNBHOUSING": "Not announced; statutory deadline 14 Nov",
    "REDINGTON": "Not announced (Q1 BM 29 Jul); Yahoo estimate 2026-11-04",
    "IPCALAB": "Not announced; Yahoo estimate 2026-11-12",
    "AUROPHARMA": "Not announced; Yahoo estimate 2026-11-05",
    "FINCABLES": "Not announced; Yahoo estimate 2026-11-13",
    "SOLARINDS": "Not announced; Yahoo estimate 2026-11-20",
    "SHYAMMETL": "Not announced; no Yahoo date",
    "JYOTICNC": "Not announced; trading window closed for Sep quarter",
    "MAHABANK": "Not found",
    "WELCORP": "Not found",
    "ACE": "Not found",
}

BANK_METRICS = {
    "PNB": {"gnpa_pct": 2.78, "nnpa_pct": 0.28, "car_pct": 18.13, "as_of": "2026-06-30",
            "url": "https://www.etnownews.com/markets/pnb-q1-results-fy-2027-profit-zooms-213-yoy-at-rs-5253-crore-total-income-at-rs-32897-cr-check-quarterly-earning-details-article-155128725",
            "notes": "CET1 14.52%, Tier1 16.03% (Q1 call, AlphaStreet). PCR 97.23% per company vs 90.3% per MOFSL (basis differs, likely incl. technical write-offs). Q2 provisional: advances +14.80% YoY, deposits +9.90%, CD ratio 75.56%."},
    "KARURVYSYA": {"gnpa_pct": 0.74, "nnpa_pct": 0.19, "car_pct": 18.61, "as_of": "2026-06-30",
                   "url": "https://stockanalysis.com/quote/nse/KARURVYSYA/transcripts/",
                   "notes": "Q1 NIM 4.26%; FY27 NIM guide 3.7-3.8%. Q2 provisional: business +17.96%, advances +20.34%, deposits +15.96%."},
    "CUB": {"gnpa_pct": 1.73, "nnpa_pct": 0.61, "car_pct": None, "as_of": "2026-06-30",
            "url": "https://cityunionbank.com/filemanager/Jul26/PressRelease_Standalone_UFR_Q1_FY2026.pdf",
            "notes": "PCR 85% incl TWO / 65% excl; CET-1 20.97% (broker note img.etimg.com); total CRAR not retrieved."},
    "MAHABANK": {"gnpa_pct": 1.45, "nnpa_pct": 0.13, "car_pct": 18.64, "as_of": "2026-06-30",
                 "url": "https://financialfilings.com/filings/bank-of-maharashtra/earnings-release/2026/49238122/",
                 "notes": "Tier I 16.35%, PCR 98.55%, ROE 24.65% (Q1)."},
    "LICHSGFIN": {"gnpa_pct": 2.14, "nnpa_pct": 1.11, "car_pct": 25.48, "as_of": "2026-06-30 (CAR as of 2026-03-31)",
                  "url": "https://cdn.lichousing.com/2026/07/Investor_Update_Q1_FY2027.pdf",
                  "notes": "Stage-3 EAD 2.14%, Stage-3 PCR 48%; NNPA 1.11% from PL Capital note; CAR Mar-26 (Tier I 24.20) - June CAR not disclosed in update."},
    "PNBHOUSING": {"gnpa_pct": 0.95, "nnpa_pct": 0.58, "car_pct": 28.26, "as_of": "2026-06-30",
                   "url": "https://www.pnbhousing.com/malayalam/documents/d/guest/PressRelease_04%20Aug%202026",
                   "notes": "PCR 39.43%; CRAR standalone."},
}

CYCLICAL = {
    "CHENNPETRO": "Brent + diesel cracks: Choice Q2FY27 preview cites record diesel crack ~US$52/bbl; Emkay: GRMs softened QoQ; diesel export tax cut to Rs16/l",
    "MRPL": "Brent + diesel cracks (as CHENNPETRO). Note 30 Sep CHTU fire, run-rate cut at one 60k bpd CDU; Crisil: limited throughput impact",
    "PETRONET": "LNG: Brent proxy only; Emkay cites US$8.4/mmbtu spot LNG marketing margin assumption; MOFSL flags spot LNG US$19-20 risk",
    "GESHIP": "Tanker/dry-bulk freight rates not retrieved (N/A); Brent shown as energy-shipping proxy only",
    "SHYAMMETL": "Steel price series not retrieved (N/A); Livemint: 'buoyant steel market', EV/EBITDA ~10x FY27 Bloomberg consensus",
    "WELCORP": "Steel/line-pipe price series not retrieved (N/A); order book record US$4.7 bn",
}
brent = market["brent_usd"]


def results_field(s):
    nse = sorted({bmr["bm_date"] for bmr in bm_range if bmr["bm_symbol"] == s})
    if nse:
        dt = d(nse[0]).isoformat()
        return F(dt, BM_URL, "2026-10-12", "scraped", f"NSE board meeting (results). In 15-session window: {dt <= WINDOW_END}")
    if s in RESULTS_WEB:
        dt, url, note = RESULTS_WEB[s]
        return F(dt, url, "2026-10-12", "websearch", note)
    note = UNCONFIRMED.get(s, "Not found")
    return F("N/A", "", "2026-10-12", "unavailable", note)


def role(s):
    if s in screen["main_pass_pledge_confirmed"]:
        return "main_pass_pledge_confirmed"
    if s in screen["main_pass"]:
        return "main_pass_pledge_na"
    if s in screen["pe_lt_industry_top25"]:
        return "pe_lt_industry_fails_other"
    if s in screen["pe_within_5pct_top25"]:
        return "near_miss_pe_within_5pct"
    if s in screen["financials_in_techpass"]:
        return "financials_variant_watch"
    return "near_miss_other"


candidates = {}
cross = []
for s in cands:
    t = tech[s]
    f = fun.get(s) or {}
    q = qs.get(s) or {}
    bh = bhav.get(s) or {}
    row = rows.get(s) or {}
    pr = peers.get(s) or {}
    pl = pledge.get(s) or {}
    close = t["close"]
    yurl = YF.format(f"{s}.NS")
    surl = SCR.format(s)
    sym_note = f"screener price line '{f.get('price_as_of_line')}'"

    c = {"ticker": s, "company": t.get("company"), "nifty_industry": t.get("industry"), "role": role(s), "tech_rule": t.get("tech_rule")}
    c["price"] = F(close, BHAV, SESSION, "scraped", f"NSE bhavcopy close {bh.get('nse_close_2026-10-09')}; Yahoo close {bh.get('yahoo_close')}; gap {bh.get('yahoo_vs_nse_close_gap_pct')}%")
    c["market_cap_cr"] = F(f.get("market_cap_cr"), surl, "2026-10-09", "scraped", sym_note)
    c["sub_sector"] = F((f.get("industry") or {}).get("Industry"), surl, "2026-10-09", "scraped", json.dumps(f.get("industry")))
    c["PE"] = F(f.get("pe"), surl, "2026-10-09", "scraped", "screener Stock P/E")
    c["sub_sector_median_PE"] = F(row.get("industry_pe_top25"), "https://www.screener.in" + (f.get("industry_href") or ""), "2026-10-09/12", "computed",
                                  f"top-25-by-mcap median (n={row.get('industry_pe_top25_n')}); all-pages median {row.get('industry_pe_allpages')} (n={row.get('industry_pe_allpages_n')}); premium vs top25 {row.get('pe_premium_vs_top25_pct')}%")
    c["PB"] = F(rnd(f.get("pb_computed") or f.get("pb_from_networth")), surl, "2026-10-09", "computed",
                "price/book value" if f.get("pb_computed") else "mcap/(equity+reserves) fallback")
    if pr:
        c["sub_sector_median_PB"] = F(pr["median_pb_peers"], pr["industry_url"], "2026-10-09/12", "computed", f"peer median, n={pr['n_pb']}; premium {pr['pb_premium_vs_median_pct']}%")
        c["sub_sector_median_ROE"] = F(pr["median_roe_peers"], pr["industry_url"], "latest reported", "computed", f"peer median, n={pr['n_roe']}")
    else:
        c["sub_sector_median_PB"] = na("no peer set built")
        c["sub_sector_median_ROE"] = na("no peer set built")
    fe = q.get("forwardEps")
    if fe:
        fpe = round(close / fe, 3)
        e0 = next((x for x in (q.get("eps_revision_check") or []) if x["period"] == "0y"), None)
        e1 = next((x for x in (q.get("eps_revision_check") or []) if x["period"] == "+1y"), None)
        alt = []
        if e0 and e0.get("current"):
            alt.append(f"P/E on FY27E consensus EPS {e0['current']} = {round(close / e0['current'], 2)}")
        if e1 and e1.get("current"):
            alt.append(f"P/E on FY28E {e1['current']} = {round(close / e1['current'], 2)}")
        c["forward_PE"] = F(fpe, QSURL.format(s), SESSION, "computed",
                            f"9 Oct close / Yahoo forwardEps {fe} (Yahoo forwardPE {rnd(q.get('forwardPE'), 2)} uses live 12 Oct price). " + "; ".join(alt) +
                            ". Independent second-source forward PE not obtained.")
    else:
        c["forward_PE"] = na("Yahoo forwardEps unavailable", QSURL.format(s))
    c["ROE"] = F(f.get("roe"), surl, "latest reported", "scraped")
    c["D/E"] = F(rnd(f.get("debt_to_equity")), surl, f.get("debt_to_equity_as_of"), "computed",
                 (f.get("debt_to_equity_notes") or "") + (" (bank/NBFC: borrowings only, deposits excluded)" if s in screen["financials_in_techpass"] or s in BANK_METRICS else ""))
    c["TTM_EPS"] = F(f.get("ttm_eps"), surl, "TTM", "scraped", f"Yahoo trailingEps {q.get('trailingEps')}")
    c["operating_cash_flow_cr"] = F(f.get("ocf_latest_annual_cr"), surl, f.get("ocf_as_of"), "scraped", "latest annual Cash from Operating Activity")
    cg = f.get("cagr") or {}
    c["3y_revenue_CAGR_pct"] = F((cg.get("Compounded Sales Growth") or {}).get("3 Years"), surl, "latest", "scraped")
    c["3y_profit_CAGR_pct"] = F((cg.get("Compounded Profit Growth") or {}).get("3 Years"), surl, "latest", "scraped")
    c["promoter_pledge_pct"] = F(pl.get("value"), pl.get("source_url", ""), pl.get("as_of", ""), pl.get("method", "unavailable"),
                                 f"promoter % {pl.get('promoter_pct')}. " + (pl.get("notes") or ""))
    c["adv_20d_value_cr"] = F(bh.get("nse_adv_20s_cr"), BHAV, SESSION, "computed", f"NSE bhavcopy 20 sessions; Yahoo ADV {bh.get('yahoo_adv_20s_cr')}")
    c["52w_high"] = F(t["hi52_used"], yurl, SESSION, "computed", f"series high date {t.get('series_52w_high_date')}; screener 52wH {f.get('high_52w_screener')}; {rnd(t.get('pct_below_52w'), 2)}% below")
    c["ema20"] = F(rnd(t["ema20"], 2), yurl, SESSION, "computed")
    c["dma20"] = F(rnd(t["dma20"], 2), yurl, SESSION, "computed")
    c["dma50"] = F(rnd(t["dma50"], 2), yurl, SESSION, "computed")
    c["dma200"] = F(rnd(t["dma200"], 2), yurl, SESSION, "computed")
    c["dma200_slope"] = F({"change_20_sessions": rnd(t["dma200_change_20_sessions"], 3), "slope_pct_per_session": rnd(t["dma200_slope_pct_per_session"], 4),
                           "rising": t["dma200_rising_20s"]}, yurl, SESSION, "computed")
    c["rsi14"] = F(rnd(t["rsi14"], 2), yurl, SESSION, "computed", "Wilder")
    c["atr14"] = F(rnd(t["atr14"], 3), yurl, SESSION, "computed", f"{rnd(t['atr14_pct'], 2)}% of close")
    c["last_20_bars"] = F(t.get("last_20_bars"), yurl, SESSION, "computed", "OHLCV daily (IST dates) with vol vs 20d avg, EMA20, RSI14")
    c["delivery_pct"] = F({"2026-10-09": bh.get("delivery_pct_2026-10-09"), "avg_20s": bh.get("delivery_pct_avg_20s"), "last_5": bh.get("delivery_pct_last_5")},
                          BHAV, SESSION, "computed")
    c["3m_return_pct"] = F(rnd(t["ret_3m_63d"], 2), yurl, SESSION, "computed", "63 sessions")
    c["1m_return_pct"] = F(rnd(t["ret_1m_21d"], 2), yurl, SESSION, "computed", "21 sessions")
    c["next_results_date"] = results_field(s)
    c["corporate_actions"] = F([x for x in cal_items if x["symbol"] == s and x["event"].startswith("Ex-date")], "https://www.nseindia.com/api/corporates-corporateActions", "2026-10-12", "scraped")
    st = []
    if s in asm_map:
        st.append(f"ASM {asm_map[s]['term']} {asm_map[s]['stage']}")
    if s in ban:
        st.append("F&O ban (trade date 12-Oct-2026)")
    c["asm_gsm_fo_ban_status"] = F(st or ["none"], ASM_URL + " ; " + GSM_URL + " ; " + BAN_URL, "2026-10-12", "scraped")
    c["fii_holding_last"] = F(f.get("fii_pct"), surl, f.get("fii_as_of"), "scraped", json.dumps(f.get("fii_change")))
    c["dii_holding_last"] = F(f.get("dii_pct"), surl, f.get("dii_as_of"), "scraped", json.dumps(f.get("dii_change")))
    c["promoter_holding_last"] = F(f.get("promoter_pct") if f.get("promoter_pct") is not None else pl.get("promoter_pct"), surl, f.get("promoter_as_of") or pl.get("as_of"), "scraped")
    c["analyst_ratings"] = F({"n": q.get("n_analysts"), "recommendationKey": q.get("recommendationKey"), "mean": q.get("recommendationMean"),
                              "target_mean": q.get("target_mean"), "target_low": q.get("target_low"), "target_high": q.get("target_high"),
                              "trend": q.get("recommendationTrend")}, QSURL.format(s), "2026-10-12", "scraped")
    c["eps_revisions"] = F({"by_period": q.get("eps_revision_check"), "net_downward_fy_90d": q.get("net_downward_fy_eps_revision_90d")}, QSURL.format(s), "2026-10-12", "scraped",
                           "Yahoo earningsTrend: current vs 90 days ago; up/down counts last 30 days")
    if s in BANK_METRICS:
        bm_ = BANK_METRICS[s]
        c["bank_metrics"] = F({"gnpa_pct": bm_["gnpa_pct"], "nnpa_pct": bm_["nnpa_pct"], "car_pct": bm_["car_pct"]}, bm_["url"], bm_["as_of"], "websearch", bm_["notes"])
    if s in CYCLICAL:
        c["EV_EBITDA"] = F({"current": q.get("ev_ebitda"), "5y_avg": "N/A"}, QSURL.format(s), "2026-10-12", "scraped",
                           "Yahoo enterpriseToEbitda (EV at live 12 Oct price); 5-year average not available from any fetched source")
        c["commodity_price_trend"] = F({"brent_close": brent["close"]["value"], "brent_1m_pct": brent["ret_1m_21s_pct"]["value"], "brent_3m_pct": brent["ret_3m_63s_pct"]["value"],
                                        "context": CYCLICAL[s]}, brent["close"]["source_url"], SESSION, "computed")
    c["screen_flags"] = {"filters": row.get("filters"), "main_screen_fails": row.get("main_screen_fails"), "main_screen_pass": row.get("main_screen_pass"),
                         "main_screen_pass_pledge_confirmed": row.get("main_screen_pass_pledge_confirmed"), "within_5pct_of_pe_test": row.get("within_5pct_of_pe_test"),
                         "pe_premium_vs_top25_pct": row.get("pe_premium_vs_top25_pct"), "financials_variant": row.get("financials_variant"),
                         "financials_variant_pass": row.get("financials_variant_pass")}
    c["news_ref"] = "news.md#" + s.lower()
    candidates[s] = c

    # cross-checks
    nse_c = bh.get("nse_close_2026-10-09")
    cross.append({"field": "price", "ticker": s, "source_a": "NSE bhavcopy", "source_b": "Yahoo chart close", "values": [nse_c, bh.get("yahoo_close")],
                  "gap_pct": gap_pct(nse_c, bh.get("yahoo_close")), "chosen": "NSE"})
    if q.get("trailingEps") and f.get("pe"):
        ype = close / q["trailingEps"]
        g = gap_pct(f["pe"], ype)
        cross.append({"field": "PE", "ticker": s, "source_a": "screener Stock P/E", "source_b": "9 Oct close / Yahoo trailingEps", "values": [f["pe"], rnd(ype, 2)],
                      "gap_pct": g, "chosen": "screener" + (" (gap>3%: EPS basis differs, e.g. standalone vs consolidated / TTM timing)" if g and g > 3 else "")})
    pbv = f.get("pb_computed") or f.get("pb_from_networth")
    if q.get("bookValue") and pbv:
        ypb = close / q["bookValue"]
        g = gap_pct(pbv, ypb)
        cross.append({"field": "PB", "ticker": s, "source_a": "screener price/BV", "source_b": "9 Oct close / Yahoo bookValue", "values": [rnd(pbv, 3), rnd(ypb, 3)],
                      "gap_pct": g, "chosen": "screener"})
    if q.get("mcap_cr") and q.get("price") and f.get("market_cap_cr"):
        ym = q["mcap_cr"] * close / q["price"]
        cross.append({"field": "market_cap_cr", "ticker": s, "source_a": "screener", "source_b": "Yahoo marketCap rescaled to 9 Oct close", "values": [f["market_cap_cr"], rnd(ym, 1)],
                      "gap_pct": gap_pct(f["market_cap_cr"], ym), "chosen": "screener"})
    if f.get("high_52w_screener"):
        cross.append({"field": "52w_high", "ticker": s, "source_a": "Yahoo daily series high", "source_b": "screener High", "values": [t["hi52_used"], f["high_52w_screener"]],
                      "gap_pct": gap_pct(t["hi52_used"], f["high_52w_screener"]), "chosen": "Yahoo series (screener rounds)"})
    if q.get("dma50_yahoo"):
        cross.append({"field": "dma50", "ticker": s, "source_a": "computed (to 9 Oct)", "source_b": "Yahoo fiftyDayAverage (live 12 Oct)", "values": [rnd(t["dma50"], 2), rnd(q["dma50_yahoo"], 2)],
                      "gap_pct": gap_pct(t["dma50"], q["dma50_yahoo"]), "chosen": "computed"})
    if q.get("dma200_yahoo"):
        cross.append({"field": "dma200", "ticker": s, "source_a": "computed (to 9 Oct)", "source_b": "Yahoo twoHundredDayAverage (live 12 Oct)", "values": [rnd(t["dma200"], 2), rnd(q["dma200_yahoo"], 2)],
                      "gap_pct": gap_pct(t["dma200"], q["dma200_yahoo"]), "chosen": "computed"})

cross.append({"field": "nifty500_close", "ticker": "NIFTY 500", "source_a": "NSE ind_close_all", "source_b": "Yahoo ^CRSLDX",
              "values": [n500_nse["close_2026-10-09"], rnd(indices["nifty500"]["close"], 2)], "gap_pct": gap_pct(n500_nse["close_2026-10-09"], indices["nifty500"]["close"]), "chosen": "NSE"})
cross.append({"field": "price_all_nifty500", "ticker": "*", "source_a": "NSE bhavcopy", "source_b": "Yahoo", "values": None,
              "gap_pct": max((v.get("yahoo_vs_nse_close_gap_pct") or 0) for v in bhav.values()), "chosen": "NSE", "notes": f"max abs gap across {len(bhav)} names"})
flagged = [x for x in cross if x.get("gap_pct") and x["gap_pct"] > 3]

gaps = [
    "screener / screener-core MCP namespaces absent; DATA_MODE=WEB (no MCP auth attempted).",
    "Screener raw screen engine not used (login/JS); universe rebuilt from Nifty 500 + Yahoo + screener company/industry pages.",
    "Forward PE: only Yahoo (forwardEps; FY27E/FY28E consensus shown as alternates) - no independent second source.",
    "EV/EBITDA 5-year averages: N/A for all cyclicals. Current EV/EBITDA from Yahoo uses live 12 Oct EV.",
    "Commodity series other than Brent (diesel cracks, steel, freight, spot LNG) not fetched as time series; only cited from broker previews.",
    "Q2 FY27 results dates not announced/not found for: " + ", ".join(sorted(k for k in UNCONFIRMED if k in cands)) + ". Yahoo estimates shown as unconfirmed.",
    "Bank CAR: CUB total CRAR not retrieved (CET-1 20.97% only). LICHSGFIN CAR is Mar-26. All bank/NBFC metrics are Q1 FY27 (30 Jun 2026).",
    "PNB PCR conflicts between company (97.23%) and MOFSL (90.3%) - basis difference; both recorded.",
    "AEGISLOG industry median PE unavailable (industry page not fetched); fails PE test by default.",
    "Pledge as-of mostly 30-Jun-2026 (some 30-Sep-2026) from NSE SHP XBRL; NSE pledge API empty.",
    "NSE historical indices/bulk/block deal APIs blocked (HTML); only latest-day bulk/block files used.",
    "Yahoo quoteSummary fields (targets, forwardPE, trailingPE, 50/200-DMA) are live 12 Oct values; recomputed at 9 Oct close where used.",
    "Yahoo ^NSMIDCP is Nifty Next 50 (relabelled, not used for midcap); sector indices from NSE official closes instead of Yahoo single-bar tickers.",
    "BHEL 'Q2 profit -64%' headline (psuconnect 11 Oct) treated as stale/unverified - results due 14 Oct.",
    "Some older news rows (IPCALAB Livemint/DSIJ, ENGINERSIN OGJ, KPIL HBL) keep only the outlet root URL; full article URL not retained.",
    "Next RBI MPC date and US CPI date not retrieved.",
]

data = {
    "run_date_ist": "2026-10-12",
    "data_as_of_session": SESSION,
    "data_mode": "WEB",
    "mcp_error": "screener / screener-core MCP namespaces absent from the tool catalog in this environment (GetDynamicTools full catalog lists only cursor, Cursor Automation Tools, cursor-cloud, cursor-subscriptions; pattern 'screener' returned 0 matches). Not authenticated, per run rules.",
    "market": market,
    "sectors": sectors_out,
    "breadth": breadth,
    "macro_calendar": macro,
    "universe_screen": universe_screen,
    "universe_screen_financials": universe_screen_fin,
    "sub_sector_medians": sub_sector_medians,
    "candidates": candidates,
    "surveillance": surveillance,
    "corporate_calendar_next_15_sessions": corp_cal,
    "cross_checks": {"rule": "gap > 3% -> prefer NSE/BSE > screener > others", "items": cross, "flagged_gt_3pct": flagged},
    "gaps": gaps,
}
json.dump(data, open(os.path.join(OUT, "data.json"), "w"), indent=1, default=str)
print("candidates", len(candidates), "cross", len(cross), "flagged", len(flagged))
for x in flagged:
    print(x["field"], x["ticker"], x["values"], x["gap_pct"])
print("top1", sectors_out["top5_rs_1m"])
print("top3", sectors_out["top5_rs_3m"])

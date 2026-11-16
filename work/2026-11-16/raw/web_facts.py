#!/usr/bin/env python3
"""Web-search facts (with URLs) -> raw/web_facts.json, consumed by assemble_outputs.py.

Run 2026-11-16 (data session Fri 2026-11-13). Every leaf is {value, source_url, as_of, method, notes}.
Values transcribed from the pages cited (see news.md for the same sources). Nothing here is estimated; unknowns are 'N/A'.
Weekly FII/DII sums are computed from NSE daily provisional figures (Alloqo / ET tables) and checked against published weekly totals.
"""
import json, os

RAW = "/agent/repos/stalker/work/2026-11-16/raw"
FWD_P = os.path.join(RAW, "computed", "forward_pe_sa.json")
FWD = json.load(open(FWD_P)) if os.path.exists(FWD_P) else {}
EXTRA_P = os.path.join(RAW, "web_facts_candidates.json")
EXTRA = json.load(open(EXTRA_P)) if os.path.exists(EXTRA_P) else {}


def F(v, url, asof, method="websearch", notes=""):
    return {"value": v, "source_url": url, "as_of": asof, "method": method, "notes": notes}


ALLOQO = "https://alloqo.com/fii-dii"
ET_FIIDII = "https://economictimes.indiatimes.com/markets/fii-dii-activity/cash-provisional"
FIIDII_W1 = "https://fiianddiidata.com/fii-dii-weekly-report-06-november-2026/"
FIIDII_W2 = "https://fiianddiidata.com/fii-dii-weekly-report-13-november-2026/"
BL_MTD = "https://www.thehindubusinessline.com/markets/nifty-may-open-75-points-higher-experts-flag-consolidation-amid-global-weakness/article71706610.ece"
CNBC_W1 = "https://www.cnbctv18.com/market/fpis-light-up-dalal-street-this-diwali-with-rs-48000-crore-buying-spree-over-5-sessions-20029190.htm"
ET_W1 = "https://economictimes.indiatimes.com/markets/stocks/news/fiis-pump-rs-45960-crore-into-indian-stocks-in-a-week-is-the-tide-finally-turning-for-dalal-street/articleshow/135631663.cms"

DAILY = {  # NSE provisional cash-market net (Rs Cr), FII/FPI and DII
    "2026-10-26": (-1462.49, 2609.57), "2026-10-27": (4240.39, -1250.03), "2026-10-28": (871.83, 643.35),
    "2026-10-29": (-943.60, 1924.41), "2026-10-30": (3598.54, -817.51),
    "2026-11-02": (3114.68, -392.20), "2026-11-03": (6836.81, -3678.85), "2026-11-04": (7284.03, -3712.23),
    "2026-11-05": (14974.68, -10444.54), "2026-11-06": (13749.82, -5968.70), "2026-11-08": (-0.25, -700.31),
    "2026-11-09": (7212.22, -7172.53), "2026-11-11": (12563.33, -8434.53), "2026-11-12": (7830.60, -6331.17),
    "2026-11-13": (5736.55, -2253.58),
}


def wk(a, b, excl=()):
    d = [v for k, v in DAILY.items() if a <= k <= b and k not in excl]
    return round(sum(x[0] for x in d), 2), round(sum(x[1] for x in d), 2)


w0, w1, w2 = wk("2026-10-26", "2026-10-30"), wk("2026-11-02", "2026-11-06"), wk("2026-11-09", "2026-11-13")
mtd = wk("2026-11-01", "2026-11-13")
flows = {
    "daily_fii_dii_net_cr": F({k: {"fii": v[0], "dii": v[1]} for k, v in DAILY.items()}, ALLOQO, "2026-11-13", "scraped",
                              "NSE provisional (Alloqo table; identical to ET cash-provisional table " + ET_FIIDII + "). 13-Nov cross-checked vs NSE api/fiidiiTradeReact."),
    "week_26_30_oct": F({"fii_net_cr": w0[0], "dii_net_cr": w0[1], "sessions": 5}, ALLOQO, "2026-10-30", "computed",
                        "sum of NSE daily provisional; fiianddiidata 6-Nov report quotes prior week FII +6,305 / DII +3,110 Cr (matches)"),
    "week_02_06_nov": F({"fii_net_cr": w1[0], "dii_net_cr": w1[1], "sessions": 5}, FIIDII_W1, "2026-11-06", "computed",
                        "sum of NSE daily provisional; matches fiianddiidata/ET/Business Standard weekly FII +45,960 / DII -24,197 Cr. "
                        "CNBC-TV18 quotes +48,263.07 Cr with different daily values (see cross_checks). Excludes Sun 8-Nov Muhurat (FII -0.25 / DII -700.31)."),
    "week_09_13_nov": F({"fii_net_cr": w2[0], "dii_net_cr": w2[1], "sessions": 4}, FIIDII_W2, "2026-11-13", "computed",
                        "sum of NSE daily provisional (10-Nov holiday); matches fiianddiidata weekly FII +33,342.70 / DII -24,191.81 Cr"),
    "november_mtd_to_13nov": F({"fii_net_cr": mtd[0], "dii_net_cr": mtd[1]}, BL_MTD, "2026-11-13", "computed",
                               "sum of daily provisional incl. Muhurat; BusinessLine quotes FPI Rs 79,301 Cr for Nov to 13th (matches)"),
    "fpi_usd_november": F("over $8 bn into Indian stocks in November so far (Reuters 13-Nov); BS column: $6.43 bn up to 12-Nov (NSDL basis)",
                          "https://www.reuters.com/5f374b32b07b/world/india/rupees-faltering-rally-faces-returning-oil-pressure-surging-us-yields-2026-11-13/", "2026-11-13"),
    "fpi_october_net_cr": F({"Moneycontrol": -34843, "ET": -45162}, "https://www.moneycontrol.com/news/business/markets/three-forces-behind-november-s-market-turnaround-ai-correction-rs-54-000-crore-fii-comeback-and-earnings-resilience-14077031.html",
                            "2026-10-31", notes="bases differ (NSDL vs exchange); ET: " + ET_W1),
    "fii_index_futures_net_short_contracts": F({"~2026-10-23": "~280,000 (BS column)", "2026-11-04": 185979, "2026-11-06": 100416},
                                               FIIDII_W1, "2026-11-06", notes="NSE participant OI via Quantsapp; BS: https://www.business-standard.com/opinion/columns/short-covering-and-foreign-inflows-are-fuelling-indian-stock-market-rebound-126111500739_1.html"),
}

BS_FX = "https://www.business-standard.com/economy/news/rupee-weakens-to-94-25-10-year-bond-yield-rises-as-crude-prices-surge-126111301340_1.html"
BL_GSEC = "https://www.thehindubusinessline.com/money-and-banking/g-sec-yields-harden-as-oct-inflation-breaches-6-mark-us-yields-rise/article71698427.ece"
BS_COL = "https://www.business-standard.com/opinion/columns/short-covering-and-foreign-inflows-are-fuelling-indian-stock-market-rebound-126111500739_1.html"
market_extra = {
    "rally_since_23oct": F("Nifty 50 22,600 (23-Oct) -> 25,144.30 (13-Nov), +11.3% in three weeks; 30-Oct->6-Nov +8.58% (best week since Feb 2021). Drivers per BS column: "
                           "govt hint on reconsidering LTCG for FPIs; unwinding of crowded AI trade in Taiwan/Korea/US; Brent down ~1/5 from ~$113-117 (30-Oct); "
                           "FPI index-futures short covering (net short ~280k contracts near 23-Oct -> ~100k by 6-Nov); Q2 earnings (27/50 Nifty cos beat)",
                           BS_COL, "2026-11-15", notes="Reuters 6-Nov: https://www.reuters.com/5f374b32b07b/world/india/indian-stocks-set-pullback-after-sharp-rally-oil-slide-foreign-inflows-2026-11-06/"),
    "week_9_13_nov_summary": F("Nifty +0.46% w/w to 25,144.30 (Fri -155.05 / -0.61%); Sensex 81,592.45 (+0.7% w/w); Bank Nifty +3.7% w/w; Midcap 100 +2%, Smallcap 100 +2.6%; "
                               "nine-month high above 25,400 intraweek; PSU Bank index +7.5% w/w; Nifty IT -3.2% w/w (Nvidia/AI turmoil)",
                               "https://www.livemint.com/market/stock-market-news/stock-market-outlook-november-16-20-nifty-logs-3-week-winning-streak-first-since-june-rally-ahead-or-a-pause-11794738601982.html",
                               "2026-11-14", notes="sector detail: https://www.thefinancialeconomy.com/nifty-outlook-next-week/ ; BS: https://www.business-standard.com/markets/news/indian-markets-extend-gains-for-3rd-straight-week-despite-nvidia-crisis-126111301616_1.html"),
    "usdinr_reported_close_2026-11-13": F({"Business Standard": 94.25, "BusinessLine": 94.24, "Reuters": 94.24}, BS_FX, "2026-11-13",
                                          notes="prev close 94.04; 6-Nov close 93.91 = strongest since 22-Apr (fiianddiidata); Yahoo USDINR=X 13-Nov bar differs (bar timing)"),
    "india_10y_gsec": F("7.31% (+6 bp d/d) on 13-Nov; 10y auction cut-off 7.3203%; 5y 6.98%; +84 bp over a year", BS_FX, "2026-11-13",
                        notes="SquawkNews 7.3079%; BL: " + BL_GSEC + " ; week to 6-Nov fell 23 bp to 7.19%"),
    "brent_context": F("Brent ~$95.87 on 13-Nov after attacks on Saudi Aramco infrastructure and Hormuz shipping disruption (from ~$92.31 on 12-Nov); peak ~$117.64 on 30-Oct",
                       BS_FX, "2026-11-13", notes="30-Oct high per fiianddiidata/BS: " + FIIDII_W1),
    "dollar_index": F("~103.19 (near 19-month high)", BS_FX, "2026-11-13"),
    "india_cpi_oct": F("6.09% YoY (breached RBI 6% upper tolerance)", BL_GSEC, "2026-11-12",
                       notes="markets expect a 25 bp repo hike to 5.75% on 4-Dec (BL); ET: https://economictimes.indiatimes.com/news/economy/indicators/et-poll-india-growth-seen-at-7-7-in-q2-on-track-for-7-3-in-fy2/articleshow/135864178.cms"),
    "nifty_levels_view": F("support 24,800-24,700, resistance 25,400 (HDFC Securities); support 24,750 (Master Capital)",
                           "https://www.cnbctv18.com/market/nifty-outlook-monday-november-16-index-may-see-near-term-consolidation-after-fridays-fall-key-levels-to-watch-20034415.htm",
                           "2026-11-15", notes="third-party opinion, not a computed level"),
    "gift_nifty_pre_open_2026-11-16": F("25,255 (~+75 pts indication)", BL_MTD, "2026-11-16 pre-open", notes="indication only (not session data)"),
    "brokerage_views": F("Citi end-2027 Nifty target 28,000; HSBC upgraded India to overweight", "https://regalticker.com/nvidia-softbank-ai-reset-india-it-stocks-impact", "2026-11-09",
                         notes="third-party aggregation; not independently verified"),
}

breadth_cross_checks = [
    F({"above_50dma_pct": 56.0, "above_200dma_pct": 46.0, "adv_dec": "157/341", "nifty50_above_50dma_pct": 82.0},
      "https://indexbreadth.com/learn/market-breadth-eod-13-november-2026/", "2026-11-13", "scraped", "Nifty 500 universe; 12-Nov was 60.0% / 49.2%"),
    F({"above_50dma_pct": 59.2, "above_200dma_pct": 55.3, "above_20dma_pct": 80.8, "adv_dec": "170/329"},
      "https://flashfinance.news/market-breadth/", "2026-11-13", "websearch", "Top-500-by-mcap proxy universe (definition differs from Nifty 500)"),
    F({"above_50dma_pct": 50.0, "ten_pct_12_sessions_earlier": True},
      "https://www.businesstoday.in/markets/stocks/story/stock-market-nifty-500-stocks-above-50-day-smas-rise-to-50-from-10-in-12-sessions-566812-2026-11-11",
      "2026-11-11", "websearch", "ICICI Securities via BusinessToday; intraday 11-Nov article (likely 9-Nov close basis)"),
]

RBI_MPC = "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=62422"
MOSPI = "https://www.mospi.gov.in/uploads/documents/releaseCalender/1793948871564-ARC%202026-27%20updated%20till%20October%202026.pdf"
BLS = "https://www.bls.gov/schedule/2026/11_sched.htm"
BEA = "https://www.bea.gov/news/schedule"
FED = "https://www.federalreserve.gov/newsevents/2026-november.htm"
EXP = "https://www.quantsapp.com/expiry-calendar"
macro = {
    "rbi_policy_last": F("7 Oct 2026: repo +25 bp to 5.50%", "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63742", "2026-10-07",
                         notes="BL 13-Nov: market expects +25 bp to 5.75% in December after Oct CPI 6.09%"),
    "rbi_next_mpc": F("2-4 Dec 2026 (decision Fri 4-Dec) - INSIDE the 15-session window (day 14)", RBI_MPC, "2026-03-23", "scraped"),
    "india_gdp_q2fy27": F("Mon 30-Nov-2026 (MoSPI); ET poll median 7.7% (range 6.7-8.0%); Q1 FY27 7.8%", MOSPI, "2026-10",
                          notes="ET: https://economictimes.indiatimes.com/news/economy/indicators/et-poll-india-growth-seen-at-7-7-in-q2-on-track-for-7-3-in-fy2/articleshow/135864178.cms"),
    "india_release_calendar": F({"WPI (Oct)": "2026-11-16", "IIP (Oct)": "2026-11-28", "Q2 GDP": "2026-11-30", "CPI (Nov)": "2026-12-12"}, MOSPI, "2026-10",
                                notes="WPI date per thefinancialeconomy week-ahead (https://www.thefinancialeconomy.com/nifty-outlook-next-week/); IIP 28-Nov is a Saturday (MoSPI dates)"),
    "fo_expiries": F({"Nifty weekly": ["2026-11-17", "2026-12-01", "2026-12-08"], "NSE November monthly (Nifty/BankNifty/FinNifty/MidcapNifty/NiftyNxt50/stock F&O)": "2026-11-23 (Mon; moved from Tue 24-Nov holiday)",
                      "BSE Sensex weekly": ["2026-11-19", "2026-12-03"], "BSE monthly": "2026-11-26", "NSE December monthly": "2026-12-29"},
                     EXP, "2026-11-15", notes="cross-check: https://www.laabh.com/market/fo-expiry-calendar/ ; https://www.potoosresearch.in/news/nifty-monthly-expiry-november-2026/"),
    "us_events": F({"Nvidia Q3 results": "2026-11-17 (US)", "US retail sales (Oct)": "2026-11-17", "FOMC minutes (27-28 Oct meeting)": "2026-11-18 14:00 ET",
                    "US GDP Q3 2nd est + PCE (Oct)": "2026-11-25 08:30 ET", "US Thanksgiving (market holiday)": "2026-11-26",
                    "US JOLTS (Oct)": "2026-12-01", "US payrolls (Nov)": "2026-12-04 08:30 ET", "FOMC decision": "2026-12-09 14:00 ET (outside window)",
                    "US CPI (Nov)": "2026-12-10 (outside window)"},
                   BLS, "2026-11-09", notes="BEA: " + BEA + " ; Fed: " + FED + " ; Nvidia date per https://www.thefinancialeconomy.com/nifty-outlook-next-week/"),
    "nse_holidays_in_window": F("Tue 24-Nov-2026 Prakash Gurpurb Sri Guru Nanak Dev; next: Fri 25-Dec Christmas", "https://nsearchives.nseindia.com/content/circulars/FAOP71777.pdf", "2025-12", "scraped"),
    "ipo_events": F("Mahanadi Coalfields (Coal India subsidiary) Rs 9,500 Cr offer opens Thu 19-Nov", "https://www.thefinancialeconomy.com/nifty-outlook-next-week/", "2026-11-15",
                    notes="single source; not verified on NSE"),
    "geopolitics_oil": F("Iran conflict: de-escalation hopes after US midterms faded late week; fresh attacks on Saudi Aramco infrastructure and Hormuz shipping disruption lifted Brent to ~$95.9",
                         BS_FX, "2026-11-13"),
}

screen_notes = ("Industry PE = median of positive P/E on the screener industry page(s) for the sub-sector; company P/E/mcap/PB taken from screener pages showing the 13-Nov close "
                "(pages fetched after 09:15 IST on 16-Nov show a live price and were rescaled to the 13-Nov NSE close by adjust_fundamentals.py). Pledge from NSE SHP XBRL "
                "(latest filed quarter). Names with no promoter group: pledge N/A (not a fail).")

calendar_items = [
    {"date": "2026-11-16", "symbol": "MACRO", "event": "India WPI (Oct)", "source": "https://www.thefinancialeconomy.com/nifty-outlook-next-week/", "method": "websearch"},
    {"date": "2026-11-17", "symbol": "MACRO", "event": "Nifty weekly expiry; Nvidia results (US, after close -> India reacts 18-Nov); US retail sales", "source": EXP, "method": "websearch"},
    {"date": "2026-11-19", "symbol": "MACRO", "event": "FOMC minutes (18-Nov 14:00 ET) - first Indian session to react; Sensex weekly expiry", "source": FED, "method": "websearch"},
    {"date": "2026-11-23", "symbol": "MACRO", "event": "NSE November monthly F&O expiry (moved from 24-Nov holiday)", "source": EXP, "method": "websearch"},
    {"date": "2026-11-24", "symbol": "MACRO", "event": "NSE holiday (Prakash Gurpurb Sri Guru Nanak Dev) - not a session", "source": "https://nsearchives.nseindia.com/content/circulars/FAOP71777.pdf", "method": "scraped"},
    {"date": "2026-11-26", "symbol": "MACRO", "event": "US GDP Q3 2nd est + Oct PCE (25-Nov 08:30 ET) - first Indian session to react; US Thanksgiving", "source": BEA, "method": "websearch"},
    {"date": "2026-11-30", "symbol": "MACRO", "event": "India Q2 FY27 GDP (MoSPI, evening release; IIP 28-Nov)", "source": MOSPI, "method": "websearch"},
    {"date": "2026-12-01", "symbol": "MACRO", "event": "Nifty weekly expiry", "source": EXP, "method": "websearch"},
    {"date": "2026-12-04", "symbol": "MACRO", "event": "RBI MPC decision (2-4 Dec); US Nov payrolls 08:30 ET (India reacts 7-Dec)", "source": RBI_MPC, "method": "scraped"},
]

cross_checks_extra = [
    {"field": "fii_week_02_06_nov", "ticker": "MACRO", "source_a": "sum NSE daily provisional (Alloqo/ET) +45,960.02", "source_b": "CNBC-TV18 +48,263.07 (different daily values)",
     "values": [w1[0], 48263.07], "gap_pct": round(abs(48263.07 - w1[0]) / w1[0] * 100, 2),
     "chosen": "NSE provisional sum (also matched by fiianddiidata, ET, Business Standard)"},
    {"field": "fii_nov_mtd", "ticker": "MACRO", "source_a": "sum NSE daily provisional", "source_b": "BusinessLine Rs 79,301 Cr", "values": [mtd[0], 79301],
     "gap_pct": round(abs(79301 - mtd[0]) / mtd[0] * 100, 3), "chosen": "NSE provisional sum"},
    {"field": "usdinr_close_2026-11-13", "ticker": "USDINR", "source_a": "Business Standard 94.25", "source_b": "Reuters/BusinessLine 94.24", "values": [94.25, 94.24],
     "gap_pct": 0.01, "chosen": "reported close for level; Yahoo for returns"},
    {"field": "brent_2026-11-13", "ticker": "BZ=F", "source_a": "Yahoo BZ=F close", "source_b": "Business Standard ~95.87", "values": [None, 95.87], "gap_pct": None,
     "chosen": "Yahoo for returns; see market.brent_usd"},
]

gaps = [
    {"item": "EV/EBITDA 5-year average (cyclicals)", "status": "N/A", "reason": "no free source with a 5y EV/EBITDA history found; current Yahoo enterpriseToEbitda only"},
    {"item": "NSE corporate financial-results API", "status": "empty response",
     "reason": "api/corporates-financial-results returned [] again; Q2 filings detected via api/corporate-announcements and the board-meeting API"},
    {"item": "Nifty Midcap/Smallcap index series on Yahoo (^CNXMIDCAP, ^CNXSMALLCAP)", "status": "HTTP 404", "reason": "sector/size RS taken from NSE ind_close_all CSVs instead"},
    {"item": "Bulk deals 30-Oct..13-Nov", "status": "partial",
     "reason": "NSE api/historicalOR/bulk-block-short-deals returns max 70 rows per day (alphabetical, A-D only) for bulk deals; full bulk.csv only for 13-Nov. Block deals complete (10 sessions)."},
    {"item": "NSE 10-Nov bhavcopy URL", "status": "ignored", "reason": "10-Nov was a holiday; the URL returns a byte-identical copy of the 9-Nov file"},
    {"item": "Sun 8-Nov Muhurat session", "status": "not counted",
     "reason": "NSE published a Muhurat bhavcopy (sec_bhavdata_full_08112026.csv) but Yahoo has no 8-Nov bar; excluded from all session counts/indicators, shown separately for SOUTHBANK"},
]
gaps += EXTRA.get("gaps", [])

json.dump({"flows": flows, "corporate_actions_web": EXTRA.get("corporate_actions_web", {}), "market_extra": market_extra, "breadth_cross_checks": breadth_cross_checks,
           "macro": macro, "screen_notes": screen_notes, "calendar_items": calendar_items + EXTRA.get("calendar_items", []),
           "results_dates": EXTRA.get("results_dates", {}), "bank_metrics": EXTRA.get("bank_metrics", {}), "cyclicals": EXTRA.get("cyclicals", {}),
           "forward_pe_second_source": {s: v for s, v in FWD.items() if v.get("value") not in (None, "N/A")},
           "cross_checks_extra": cross_checks_extra + EXTRA.get("cross_checks_extra", []), "gaps": gaps},
          open(os.path.join(RAW, "web_facts.json"), "w"), indent=1)
print("web_facts written; weeks", w0, w1, w2, "mtd", mtd)

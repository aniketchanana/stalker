#!/usr/bin/env python3
"""Web-search facts (with URLs) -> raw/web_facts.json, consumed by assemble_outputs.py.

Every leaf is {value, source_url, as_of, method, notes}. Values transcribed from the pages cited
(see news.md for the same sources). Nothing here is estimated; unknowns are 'N/A'.
"""
import json, os

RAW = "/workspace/work/2026-10-19/raw"
FWD = json.load(open(os.path.join(RAW, "computed", "forward_pe_sa.json")))


def F(v, url, asof, method="websearch", notes=""):
    return {"value": v, "source_url": url, "as_of": asof, "method": method, "notes": notes}


ET_FPI = "https://economictimes.indiatimes.com/markets/stocks/news/fpi-selling-crosses-rs-52000-crore-in-october-as-nifty-defies-foreign-exodus/articleshow/135025955.cms"
TOI_FPI = "https://timesofindia.indiatimes.com/business/india-business/fpis-pull-out-52100cr-from-indian-equities-in-october-so-far/articleshow/135037488.cms"
FTI = "https://fundtrackerindia.com/fii-dii"
MC_FII = "https://www.moneycontrol.com/markets/fii-dii-data/"

flows = {
    "fpi_net_week_12_16_oct_settled_cr": F(-7934, ET_FPI, "2026-10-16", notes="FPIs sold net Rs 7,934 Cr (settled basis) in week 12-16 Oct"),
    "fpi_net_oct_mtd_cr": F(-52100, TOI_FPI, "2026-10-16", notes="CDSL/NSDL depository data, Oct 1-16 (TOI 19 Oct; Fund Tracker India same figure). Sep -35,861; Aug +29,631; Jul +20,200"),
    "dii_net_oct_mtd_cr": F(74729, FTI, "2026-10-16", notes="Fund Tracker India; DII Sep +92,734 Cr"),
    "fpi_net_cy2026_cr": F("outflow > 3.1 lakh Cr", TOI_FPI, "2026-10-16", notes="cumulative 2026 to date"),
    "fii_index_futures_net_2026-10-16_cr": F(1024.71, MC_FII, "2026-10-16", notes="Moneycontrol FII/DII page, provisional"),
    "note": "16-Oct provisional FII buy (+1,165.92 Cr) ended a 15-session FII selling streak (ET 18 Oct).",
}

market_extra = {
    "usdinr_reported_close_2026-10-16": F({"ET": 94.96, "New Indian Express (interbank)": 94.92},
                                          "https://economictimes.indiatimes.com/markets/forex/forex-news/rupee-rises-1-9-in-a-week-closes-below-95-per-dollar/articleshow/134996292.cms",
                                          "2026-10-16", notes="Rupee +1.9% w/w; RBI curbs (OMC dollar demand via RBI window). Yahoo USDINR=X 16-Oct bar 94.52 differs ~0.5% (Yahoo bar timing)."),
    "india_fx_reserves": F("USD 726 bn (-8.578 bn w/w; 6th straight weekly fall)",
                           "https://www.newindianexpress.com/business/2026/Oct/16/rbi-curbs-help-rupee-post-best-week-in-seven-months", "2026-10-09"),
    "brent_context": F("Brent touched $110 (first since May), settled $109.86 (+3.7%) on 16 Oct; >=9 ships attacked near Hormuz since 11 Oct; Hormuz crude flows ~9.4 mb/d (~70% of pre-war)",
                       "https://www.cnbc.com/2026/10/16/oil-price-today-iran-strait-hormuz-ukraine-russia.html", "2026-10-16"),
    "week_summary": F("Nifty +2.77% w/w (+625.7 pts) to 23,146; Sensex +3.11%; second straight weekly gain, IT-led (Nifty IT +11.7% w/w)",
                      "https://timesofindia.indiatimes.com/business/india-business/stock-market-outlook-geopolitical-cues-earnings-foreign-inflows-more-to-keep-dalal-street-busy/articleshow/135025850.cms",
                      "2026-10-16"),
    "gift_nifty_pre_open_2026-10-19": F(23131, "https://www.business-standard.com/markets/news/stocks-to-watch-hdfc-bank-icici-bank-bajaj-fin-dlf-omcs-ntpc-more-126101900059_1.html",
                                        "2026-10-19 07:45 IST", notes="indication only (not session data); flat-to-negative start"),
    "us_10y_yield": F("~5.3% after US Sep CPI 3.7%", ET_FPI, "2026-10-16"),
}

breadth_cross_checks = [
    F({"above_50dma_pct": 21.2, "above_200dma_pct": 37.8, "adv_dec": "258/241", "nifty50_above_50dma_pct": 30, "new_lows_pct": 4.0, "new_highs_pct": 1.6},
      "https://indexbreadth.com/learn/market-breadth-eod-16-october-2026/", "2026-10-16", notes="Nifty 500 universe"),
    F({"above_20dma_pct": 33.2, "above_50dma_pct": 24.0, "above_200dma_pct": 46.0, "adv_dec": "255/244", "new_highs": 8, "new_lows": 13},
      "https://flashfinance.news/market-breadth/", "2026-10-16", notes="Top-500 proxy universe (definition differs from Nifty 500)"),
]

FED = "https://www.federalreserve.gov/newsevents/2026-october.htm"
macro = {
    "rbi_policy_last": F("7 Oct 2026: repo +25 bp to 5.50% (unanimous); SDF 5.25%, MSF 5.75%; stance changed to 'calibrated tightening' (rate cuts off the table near term)",
                         "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63742", "2026-10-07", "websearch"),
    "rbi_next_mpc": F("2026-12-04 10:00 IST (decision)", "https://www.econ-calendar.com/rbi-meeting-dates", "2026", notes="outside the 15-session window"),
    "fomc": F("27-28 Oct 2026; statement 28 Oct 2:00 pm ET (~23:30 IST 28 Oct / reaction in India 29 Oct)", FED, "2026-10"),
    "fomc_hike_odds": F({"Yardeni": "17% odds of 25 bp hike", "Economic Times": ">40% (citing an FPI-flows report)"},
                        "https://www.yardeniquicktakes.com/economic-week-ahead-october-19-23/", "2026-10-18", notes="CONFLICT between sources; ET URL: " + ET_FPI),
    "us_cpi_sep": F("3.7% y/y (core 2.6%); PPI 6.3% y/y", "https://www.yardeniquicktakes.com/economic-week-ahead-october-19-23/", "2026-10-18"),
    "india_cpi_sep": F("5.54% y/y (Aug 4.83%); food 7.74%; released 12 Oct",
                       "https://mospi.gov.in/uploads/latestReleases/latest_release_1791800601071_643518af-5320-4e52-b78c-75c92b83885b_Press_Release_for_the_month_of_September,_2026.pdf", "2026-10-12"),
    "india_release_calendar": F({"IIP (Sep)": "2026-10-28", "CPI (Oct)": "2026-11-12", "Q2 GDP": "2026-11-30"},
                                "https://www.mospi.gov.in/uploads/documents/releaseCalender/1774849665042-ADVANCE_RELEASE_CALENDAR_2026_27_FINAL.pdf", "2026-27"),
    "us_events": F({"US midterm Election Day + JOLTS": "2026-11-03", "US Oct payrolls": "2026-11-06 08:30 ET", "US Oct CPI": "2026-11-10"},
                   "https://squawkflow.com/calendar/election-week-2026", "2026-09", notes="payrolls: https://www.bls.gov/schedule/news_release/empsit.htm"),
    "diwali_muhurat": F("Muhurat trading Sun 8 Nov 2026 (timings to be notified); Balipratipada holiday Tue 10 Nov; Dussehra holiday Tue 20 Oct; Gurpurb Tue 24 Nov",
                        "https://nsearchives.nseindia.com/content/circulars/CMTR71775.pdf", "2025-12-12", "scraped"),
    "q2_season_this_week": F("19 Oct: Bajaj Finance, UltraTech, Hindustan Zinc, Union Bank, IREDA, LTTS, HFCL; later in week: Infosys, Coforge (23 Oct), Crisil, Swiggy. "
                             "Reported 16-17 Oct (reaction 19 Oct): HDFC Bank (standalone PAT +4.7%, GNPA 1.11%), ICICI Bank (standalone PAT +20.1%), Axis Bank (PAT +39.4%)",
                             "https://www.business-standard.com/markets/news/stocks-to-watch-hdfc-bank-icici-bank-bajaj-fin-dlf-omcs-ntpc-more-126101900059_1.html", "2026-10-19"),
    "geopolitics_oil": F("Oil up ~10% last week to a one-month high on Iranian attacks on tankers (Hormuz)",
                         "https://www.ndtv.com/business-news/stock-market-sensex-share-market-nifty-live-updates-today-19-october-us-iran-war-oil-price-12204341", "2026-10-19 07:55 IST"),
}

screen_notes = ("Industry PE = median of positive P/E on screener industry page 1 (top 25 by mcap); industry pages were fetched 19-Oct after 09:15 IST, "
                "so peer P/Es reflect live 19-Oct prices (company P/E/mcap/PB were rescaled to the 16-Oct NSE close). Pledge from NSE SHP XBRL "
                "(latest filed quarter; several are 30-Jun-2026 because the Sep-2026 SHP was not yet filed). Names with no promoter group: pledge N/A (not a fail).")

calendar_items = [
    {"date": "2026-10-28", "symbol": "MACRO", "event": "India IIP (Sep) release", "source": macro["india_release_calendar"]["source_url"], "method": "websearch"},
    {"date": "2026-10-29", "symbol": "MACRO", "event": "FOMC decision (28 Oct 2pm ET = ~23:30 IST); first Indian session to react 29 Oct", "source": FED, "method": "websearch"},
    {"date": "2026-11-03", "symbol": "MACRO", "event": "US midterm elections; US JOLTS", "source": "https://squawkflow.com/calendar/election-week-2026", "method": "websearch"},
    {"date": "2026-11-06", "symbol": "MACRO", "event": "US Oct non-farm payrolls (08:30 ET)", "source": "https://www.bls.gov/schedule/news_release/empsit.htm", "method": "websearch"},
    {"date": "2026-11-08", "symbol": "MACRO", "event": "Diwali Muhurat trading (Sunday; timings to be notified)", "source": "https://nsearchives.nseindia.com/content/circulars/CMTR71775.pdf", "method": "scraped"},
    {"date": "2026-11-02", "symbol": "SHRIPISTON", "event": "Q2 FY27 earnings call 16:00 IST (results board meeting 30 Oct)", "source": "https://www.bseindia.com/xml-data/corpfiling/AttachLive/692158eb-44e5-4a46-aa4b-beda33aed9c7.pdf", "method": "websearch"},
]


def unconf(date_hint, url, notes, in_window):
    return F({"date": "N/A", "confirmed": False, "estimate": date_hint, "estimate_inside_window": in_window}, url, "2026-10-19", "websearch", notes)


SA = "https://stockanalysis.com/quote/nse/{}/statistics/"
results_dates = {
    "REDINGTON": unconf("2026-10-30 (Koyfin/StockAnalysis estimate); ~2026-11-04 (Yahoo)", SA.format("REDINGTON"),
                        "No NSE board-meeting intimation found (NSE board-meeting API 19 Oct-30 Nov; corporate announcements to 18 Oct). Estimates only.", True),
    "COALINDIA": unconf("2026-10-23 (StockAnalysis 'estimated earnings date')", SA.format("COALINDIA"),
                        "No NSE board-meeting intimation in the API pull; trading window closed from 1 Oct (Kalkine). UNCONFIRMED.", True),
    "GESHIP": unconf("2026-11-04 (StockAnalysis estimate)", SA.format("GESHIP"), "No NSE board-meeting intimation yet. UNCONFIRMED.", True),
    "HAL": unconf("2026-11-06 (StockAnalysis estimate)", SA.format("HAL"), "No NSE board-meeting intimation yet. UNCONFIRMED.", True),
    "SUNTV": unconf("2026-11-13 (StockAnalysis estimate)", SA.format("SUNTV"), "No NSE board-meeting intimation yet. UNCONFIRMED.", False),
    "WELCORP": unconf("2026-10-23 (StockAnalysis estimate)", SA.format("WELCORP"), "No NSE board-meeting intimation yet. UNCONFIRMED.", True),
    "MRPL": None,
    "JAMNAAUTO": unconf("2026-11-06 (StockAnalysis estimate); prior-year Q2 board meeting 12 Nov 2025 (Trendlyne); SEBI outer deadline 14 Nov 2026",
                        "https://trendlyne.com/equity/board-meeting/JAMNAAUTO/660/jamna-auto-industries-ltd-board_meeting/",
                        "Trading window closed from 1 Oct until 48h after results; board-meeting date not yet announced. UNCONFIRMED.", True),
    "SUPRIYA": unconf("2026-11-13 (StockAnalysis estimate); prior-year Q2 board meeting 12 Nov 2025", "https://bazaarwatch.com/announcement/150339/supriya-lifescience-limited-trading-window",
                      "Company: board-meeting date 'shall be intimated in due course' (28 Sep filing). UNCONFIRMED.", False),
    "TANLA": unconf("2026-10-23 (StockAnalysis estimate; TipRanks/finanzen listed 15-16 Oct which has passed with no NSE results filing)", SA.format("TANLA"),
                    "NSE corporate announcements 25 Sep-18 Oct: no results filing and no board-meeting intimation. UNCONFIRMED.", True),
}
results_dates = {k: v for k, v in results_dates.items() if v}


def B(gnpa, nnpa, car, url, asof, notes=""):
    return F({"gnpa_pct": gnpa, "nnpa_pct": nnpa, "car_pct": car}, url, asof, "websearch", notes)


bank_metrics = {
    "SOUTHBANK": B({"Q2FY26": 2.93, "Q3FY26": 2.67, "Q4FY26": 1.43, "Q1FY27": 1.38, "Q2FY27": 1.24},
                   {"Q2FY26": 0.56, "Q3FY26": 0.45, "Q4FY26": 0.29, "Q1FY27": 0.26, "Q2FY27": 0.09}, {"Q2FY26": 17.70, "Q2FY27": 19.40},
                   "https://nsearchives.nseindia.com/corporate/SOUTHBANK_15102026152810_SD_STT_INVESTORPRESENTATION_15OCT2026.pdf", "2026-09-30",
                   "RoA 1.08%, RoE 14.00%, CASA 31.55% (-143 bp QoQ)"),
    "CANFINHOME": B({"Q2FY26": 0.94, "Q1FY27": 0.87, "Q2FY27": 0.90}, {"Q1FY27": 0.40, "Q2FY27": 0.42}, {"Q2FY27": 23.34},
                    "https://www.bseindia.com/xml-data/corpfiling/AttachHis/3b7bdf9f-c4d0-4f62-9f90-f95152af735b.pdf", "2026-09-30",
                    "HFC: NIM 3.89% (vs 4.02%); disbursements -6.8% YoY; RoE 17.12%"),
    "KARURVYSYA": B({"Q2FY26": 0.76, "Q1FY27": 0.74, "Q2FY27": 0.69}, {"Q2FY26": 0.19, "Q1FY27": 0.19, "Q2FY27": 0.18},
                    {"Q2FY26": 16.58, "Q1FY27": 18.61, "Q2FY27": 17.97},
                    "https://www.equitybulls.com/news/377029/karur-vysya-bank-reports-q2-fy27-net-profit-growth-of-37-2-yoy-to-78-769-lakh-gr", "2026-09-30",
                    "RoA 2.10%; NIM 4.26%; filing: https://www.bseindia.com/xml-data/corpfiling/AttachLive/85CB5430-7689-4AAB-A8EA-38BBF08D97B7-164609.pdf"),
    "PNB": B({"Q2FY26": 3.45, "Q1FY27": 2.78, "Q2FY27": 2.55}, {"Q2FY26": 0.36, "Q1FY27": 0.28, "Q2FY27": 0.25},
             {"Q2FY26": 17.19, "Q1FY27": 18.13, "Q2FY27": 17.95},
             "https://www.bseindia.com/xml-data/corpfiling/AttachLive/6c942833-673e-48dd-8377-51a5a382ac90.pdf", "2026-09-30",
             "PCR 97.32%; slippage 0.77% (vs 0.71%); provisions only Rs 97 Cr in Q2"),
    "ICICIBANK": B({"Q2FY26": 1.58, "Q1FY27": 1.38, "Q2FY27": 1.20}, {"Q2FY26": 0.39, "Q1FY27": 0.35, "Q2FY27": 0.30}, {"Q2FY27": 16.68},
                   "https://www.icici.bank.in/about-us/news-room/2026/performance-review-quarter-ended-september-30-2026", "2026-09-30",
                   "CET-1 16.01%; PCR 75.0%; NIM 4.18% (-18 bp QoQ)"),
    "CUB": F("N/A (Q2 FY27 results due 28 Oct 2026; latest reported Q1 FY27 not collected)",
             "https://www.psuconnect.in/financial/city-union-bank-q2-fy27-results-on-october-28-trading-window-to-reopen-on-october-31", "2026-10-09"),
    "PNBHOUSING": F({"gnpa_pct": {"Q1FY27": 0.95}, "nnpa_pct": "N/A", "car_pct": "N/A"},
                    "https://www.pnbhousing.com/telugu/documents/d/guest/Earnings%20Call%20Transcript%2007082026", "2026-06-30",
                    notes="Q2 FY27 results due 28 Oct 2026; GNPA from Q1 FY27 earnings call (latest available)"),
}

cyc_ctx = "Brent $109.86 (16 Oct), +4.8% 1M, +23.1% 3M (Yahoo BZ=F, computed); Hormuz disruption (CNBC 16 Oct)"
cyclicals = {
    "COALINDIA": {"context": "Sep offtake +12.5% YoY, e-auction premium 94% (Nuvama, Business Today 5 Oct); H1 production -2.5% YoY. " + cyc_ctx,
                  "ev_ebitda_5y_avg": "N/A", "ev_note": "5-year average EV/EBITDA not found in an accessible source (gap)."},
    "MRPL": {"context": "Refiner: PL Capital FY27E GRM $11.3/bbl normalising to $7.4-7.5 in FY28-29E (Mint 15 Oct). " + cyc_ctx,
             "ev_ebitda_5y_avg": "N/A", "ev_note": "5-year average EV/EBITDA not found (gap)."},
    "GESHIP": {"context": "VLCC rates eased w/e 16 Oct from records (Gulf of Oman-China WS ~776 vs 841; Maritime News/Baltic Exchange); crude tanker order book ~27% of fleet",
               "ev_ebitda_5y_avg": "N/A", "ev_note": "5-year average EV/EBITDA not found (gap)."},
    "WELCORP": {"context": "Steel pipes: record order book $4.7bn; DI pipe margins pressured (CARE 15 Oct). " + cyc_ctx,
                "ev_ebitda_5y_avg": "N/A", "ev_note": "5-year average EV/EBITDA not found (gap)."},
    "PETRONET": {"context": "LNG regas: Qatar force majeure / Hormuz; Dahej utilisation 98% in Jul 2026 via third-party cargoes (ETEnergyworld). " + cyc_ctx,
                 "ev_ebitda_5y_avg": "N/A", "ev_note": "5-year average EV/EBITDA not found (gap)."},
    "JINDALSAW": {"context": cyc_ctx, "ev_ebitda_5y_avg": "N/A", "ev_note": "gap"},
}

forward_pe_second_source = {s: v for s, v in FWD.items() if v.get("value") not in (None, "N/A")}

cross_checks_extra = [
    {"field": "usdinr_close_2026-10-16", "ticker": "USDINR", "source_a": "Yahoo USDINR=X", "source_b": "ET reported close", "values": [94.52, 94.96],
     "gap_pct": 0.47, "chosen": "reported close (ET/NIE) for level; Yahoo for returns"},
    {"field": "fomc_hike_odds", "ticker": "MACRO", "source_a": "Yardeni 17%", "source_b": "ET >40%", "values": [17, 40], "gap_pct": None,
     "chosen": "both recorded (conflict)"},
    {"field": "breadth_above_50dma", "ticker": "NIFTY 500", "source_a": "computed 22.24%", "source_b": "IndexBreadth 21.2% / Flash Finance 24.0%",
     "values": [22.24, 21.2, 24.0], "gap_pct": None, "chosen": "computed (within ~1-2 pp of published)"},
    {"field": "breadth_above_200dma", "ticker": "NIFTY 500", "source_a": "computed 41.34%", "source_b": "IndexBreadth 37.8% / Flash Finance 46.0%",
     "values": [41.34, 37.8, 46.0], "gap_pct": None, "chosen": "computed (published values bracket it; universe definitions differ)"},
]

gaps = [
    {"item": "EV/EBITDA 5-year average (cyclicals COALINDIA, MRPL, GESHIP, WELCORP, PETRONET, JINDALSAW)", "status": "N/A",
     "reason": "no free source with a 5y EV/EBITDA history found; current EV/EBITDA only where screener shows it"},
    {"item": "Results dates not yet intimated to NSE", "status": "unconfirmed",
     "tickers": ["COALINDIA", "GESHIP", "HAL", "REDINGTON", "SUNTV", "WELCORP", "JAMNAAUTO", "SUPRIYA", "TANLA",
                 "AARTIIND", "AUROPHARMA", "ECLERX", "FINCABLES", "JYOTICNC", "SHYAMMETL"],
     "reason": "no board-meeting intimation on NSE as of 19-Oct; StockAnalysis/Koyfin estimates or prior-year Q2 dates recorded as hints only"},
    {"item": "NSE corporate financial-results API", "status": "empty response",
     "reason": "api/corporates-financial-results returned [] for all symbols; Q2 filings detected via api/corporate-announcements instead"},
    {"item": "Industry / peer pages (screener /market/)", "status": "live 19-Oct prices",
     "reason": "fetched after 09:15 IST on 19-Oct; industry median PE and peer PB/ROE medians reflect 19-Oct intraday prices, not 16-Oct close (subject PE/PB rescaled to 16-Oct close)"},
    {"item": "Stale screener quarterly data", "status": "stale",
     "tickers": ["GSPLTRANS", "MONEYVIEW", "AXIOMGAS (2024-06)", "SITINET (2025-09)"],
     "reason": "both consolidated and standalone pages lack the latest quarter; affects peer medians only (none is a candidate)"},
    {"item": "Promoter pledge", "status": "as of 30-Jun-2026 for many names",
     "reason": "Sep-2026 shareholding pattern not yet filed; REDINGTON, SOUTHBANK, BSE, FEDERALBNK have no promoter group -> pledge N/A (not a fail)"},
    {"item": "Forward PE second source", "status": "N/A for SUPRIYA and JAYNECOIND (JAYNECOIND also has no Yahoo forward EPS)",
     "reason": "StockAnalysis page has no forward PE for these"},
    {"item": "CUB bank metrics (GNPA/NNPA/CAR)", "status": "N/A", "reason": "Q2FY27 not yet reported; latest-quarter figures not found on a fetchable page"},
    {"item": "Nifty Midcap/Smallcap index series on Yahoo", "status": "HTTP 404", "reason": "sector/size RS taken from NSE ind_close_all CSVs instead"},
    {"item": "NSDL fortnightly FPI data / tipsheet numbers", "status": "omitted",
     "reason": "figures seen only without a citable URL; FII/DII flows taken from news reports citing NSE provisional data"},
    {"item": "Earnings-call transcripts", "status": "N/A", "reason": "transcript fetch returned an empty document"},
    {"item": "Setup-C reaction for filings on/after 16-Oct 15:30 or on Sat 17-Oct", "status": "pending",
     "tickers": ["AXISBANK", "BAJAJHFL", "CENTRALBK", "DLF", "HDFCBANK", "HSCL", "ICICIBANK", "IDBI", "INDIACEM", "IXIGO",
                 "JINDALSAW", "LTM", "OBEROIRLTY", "PNB", "TEJASNET", "URBANCO", "YESBANK"],
     "reason": "reaction session is 19-Oct (live, excluded)"},
]

corporate_actions_web = {
    "TECHM": [{"action": "1:1 bonus issue recommended by board; interim dividend Rs 15", "announced": "2026-10-15",
               "record_date": "N/A (not yet announced)", "source_url": "https://www.techmahindra.com/insights/press-releases/techmahindra-q2-fy27-results/"}],
    "360ONE": [{"action": "second interim dividend Rs 7.5", "announced": "2026-10-15", "record_date": "2026-10-23",
                "source_url": "https://nsearchives.nseindia.com/corporate/IIFLWAM_15102026163141_BoardMeetingOutcomeSigned.pdf"}],
    "AARTIIND": [{"action": "EGM to approve fund raise up to Rs 1,000 Cr (QIP/private placement/other)", "announced": "2026-10-01",
                  "record_date": "EGM 2026-10-31", "source_url": "https://nsearchives.nseindia.com/corporate/AARTIIND_01102026171448_AARTIIND_Outcome.pdf"}],
}

json.dump({"flows": flows, "corporate_actions_web": corporate_actions_web, "market_extra": market_extra, "breadth_cross_checks": breadth_cross_checks, "macro": macro,
           "screen_notes": screen_notes, "calendar_items": calendar_items, "results_dates": results_dates,
           "bank_metrics": bank_metrics, "cyclicals": cyclicals, "forward_pe_second_source": forward_pe_second_source,
           "cross_checks_extra": cross_checks_extra, "gaps": gaps},
          open(os.path.join(RAW, "web_facts.json"), "w"), indent=1)
print("web_facts written; fwd2", len(forward_pe_second_source), "results_dates", list(results_dates))

#!/usr/bin/env python3
"""Web-search facts (with URLs) -> raw/web_facts.json, consumed by assemble_outputs.py.

Run 2026-10-26 (week ending Fri 2026-10-23). Every leaf is {value, source_url, as_of, method, notes}.
Values transcribed from the pages cited (see news.md for the same sources). Nothing here is estimated; unknowns are 'N/A'.
"""
import json, os

RAW = "/workspace/work/2026-10-26/raw"
FWD_P = os.path.join(RAW, "computed", "forward_pe_sa.json")
FWD = json.load(open(FWD_P)) if os.path.exists(FWD_P) else {}


def F(v, url, asof, method="websearch", notes=""):
    return {"value": v, "source_url": url, "as_of": asof, "method": method, "notes": notes}


CNBC_FLOW = "https://www.cnbctv18.com/market/fiis-pull-out-rs2697-crore-this-week-diis-pump-in-nearly-rs11000-crore-20018283.htm"
FIIDII_WK = "https://fiianddiidata.com/fii-dii-weekly-report-23-october-2026/"
MC_PRO = "https://www.moneycontrol.com/news/business/markets/moneycontrol-pro-market-outlook-investors-brace-for-volatile-week-as-crude-oil-boils-14059581.html"
ET_WEEK = "https://economictimes.indiatimes.com/markets/stocks/news/fiis-dump-indian-stocks-for-10th-straight-week-as-markets-slide-is-the-worst-over-or-more-pain-ahead/articleshow/135165684.cms"
NDTV_FPI = "https://www.ndtvprofit.com/markets/fpi-exodus-overseas-investors-pull-out-rs-48-056-crore-from-equities-in-october-so-far-amid-soaring-crude-oil-prices-12232742"

flows = {
    "fii_net_week_19_23_oct_cr": F(-2697.37, CNBC_FLOW, "2026-10-23", notes="NSE provisional cash-market data, 4-session week (20-Oct holiday); 9th straight week of FII selling"),
    "dii_net_week_19_23_oct_cr": F(10942.19, CNBC_FLOW, "2026-10-23"),
    "daily_fii_dii_net_cr": F({"2026-10-19": {"fii": -1148.6, "dii": 3201.2}, "2026-10-21": {"fii": 1022.3, "dii": 1614.3},
                               "2026-10-22": {"fii": -3458.7, "dii": 2891.3}, "2026-10-23": {"fii": 887.6, "dii": 3235.4}},
                              FIIDII_WK, "2026-10-23", notes="NSE provisional; 23-Oct cross-checked vs NSE api/fiidiiTradeReact (FII +887.65, DII +3,235.36)"),
    "fii_net_oct_mtd_cr_exchange": F(-51466.38, MC_PRO, "2026-10-23", notes="Moneycontrol Pro, FII October cash-market sales to date (exchange provisional)"),
    "fpi_net_oct_mtd_cr_nsdl": F(-48056, NDTV_FPI, "2026-10-23", notes="NSDL depository data (settlement basis) - differs from exchange provisional by design"),
    "note": "ET reported FII -26,970 Cr for the week and -5,14,660 Cr MTD (10x all other outlets) - treated as a typo, not used. URL: " + ET_WEEK,
}

market_extra = {
    "week_summary": F("Nifty -2.36% w/w (-546.15 pts) to 22,600 in a 4-session week (Dussehra holiday 20 Oct); Sensex -2.15%; snapped 2-week rally; "
                      "Bank Nifty -2.8%, Midcap 100 -5.6%, Smallcap 100 -7.3% (ET); 43/50 Nifty stocks fell; IT only gainer (+0.2%)",
                      "https://www.moneycontrol.com/news/photos/business/markets/sensex-nifty-snap-2-week-rally-as-oil-shock-fii-selling-weigh-on-d-street-14058980.html",
                      "2026-10-23", notes="ET: " + ET_WEEK + " ; MC Pro: " + MC_PRO),
    "usdinr_reported_close_2026-10-23": F({"PTI (provisional)": 94.93, "Business Standard (settled)": 94.94},
                                          "https://www.thehindu.com/business/markets/rupee-falls-12-paise-to-close-at-9493-against-us-dollar/article71615832.ece",
                                          "2026-10-23", notes="BS: https://www.business-standard.com/economy/news/govt-bonds-log-worst-losing-streak-in-30-years-as-crude-us-yields-rise-126102301399_1.html ; "
                                                              "Yahoo USDINR=X 23-Oct bar 94.71 (bar timing differs ~0.2%)"),
    "india_fx_reserves": F("USD 721.016 bn as of 16-Oct (-5.011 bn w/w); FCA 591.847 bn; ~$65 bn below the $785.7 bn record over 6 weeks (BS)",
                           "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63855", "2026-10-16"),
    "india_10y_gsec": F("7.47% - 10th straight weekly rise (worst losing streak for bonds in 30 years)",
                        "https://www.business-standard.com/economy/news/govt-bonds-log-worst-losing-streak-in-30-years-as-crude-us-yields-rise-126102301399_1.html", "2026-10-23"),
    "brent_context": F("Brent Dec settled $116.72 (+3.14%) on 23 Oct, highest since 29 Apr, +6% w/w (3rd weekly gain); WTI $103.27; Houthi attacks on Saudi energy sites; "
                       "MC Pro: Brent $109.65 Mon -> $117.45 high Fri",
                       "https://www.investing.com/news/commodities-news/oil-little-changed-as-supply-concern-lingers-amid-houthi-attacks-on-saudi-arabia-4967907",
                       "2026-10-23", notes="Yahoo BZ=F 23-Oct close 116.72 (matches). CNBC: https://www.cnbc.com/2026/10/23/oil-price-brent-wti-iran-war-saudi-arabia.html"),
    "india_vix_reported": F({"NSE allIndices": 16.86, "Moneycontrol Pro": 16.76}, MC_PRO, "2026-10-23", notes="NSE value used (0.6% gap)"),
    "gift_nifty_pre_open_2026-10-26": F(22610, "https://www.businesstoday.in/markets/trending-stocks/story/gift-nifty-up-33-points-infosys-kotak-bank-tmcv-indusind-bank-vedanta-among-top-stocks-in-focus-563529-2026-10-26",
                                        "2026-10-26 pre-open", notes="indication only (not session data)"),
    "nifty_support_view": F("22,200 key support (SBI Securities); Bank Nifty support 53,700-53,800, resistance 54,900-55,000",
                            "https://www.cnbctv18.com/market/nifty-outlook-monday-october-26-22200-key-support-crude-oil-fed-policy-earnings-in-focus-20018821.htm", "2026-10-26",
                            notes="third-party opinion, not a computed level"),
    "us_10y_yield": F("slipped below 5% on 23 Oct; DXY 101.73", "https://www.thehindu.com/business/markets/rupee-falls-12-paise-to-close-at-9493-against-us-dollar/article71615832.ece", "2026-10-23"),
}

breadth_cross_checks = [
    F({"above_50dma_pct": 9.6, "above_200dma_pct": 24.0, "adv_dec": "50/450", "nifty50_above_50dma_pct": 16, "new_lows_pct": 25},
      "https://indexbreadth.com/learn/market-breadth-eod-23-october-2026/", "2026-10-23", notes="Nifty 500 universe"),
    F({"above_50dma_pct": 9.9, "new_52w_lows": 104, "new_52w_highs": 2, "fear_greed": 11},
      "https://aftermarketreport.zerodha.com/p/brutal-selling-grips-broader-markets", "2026-10-23", notes="Zerodha aftermarket report, Nifty 500"),
    F({"above_50dma_pct": 10.2, "above_200dma_pct": 32.9, "adv_dec": "49/451"},
      "https://flashfinance.news/market-breadth/", "2026-10-23", notes="Top-500 proxy universe (definition differs from Nifty 500)"),
]

FED = "https://www.federalreserve.gov/newsevents/2026-october.htm"
BS_WEEK = "https://www.business-standard.com/markets/news/q2-results-us-fed-decision-crude-oil-may-drive-stock-markets-this-week-126102500192_1.html"
macro = {
    "rbi_policy_last": F("7 Oct 2026: repo +25 bp to 5.50% (unanimous); SDF 5.25%, MSF 5.75%; stance 'calibrated tightening'",
                         "https://www.rbi.org.in/Scripts/BS_PressReleaseDisplay.aspx?prid=63742", "2026-10-07"),
    "rbi_next_mpc": F("2026-12-04 (decision)", "https://www.econ-calendar.com/rbi-meeting-dates", "2026", notes="outside the 15-session window"),
    "fomc": F("27-28 Oct 2026; statement 28 Oct 2:00 pm ET (~23:30 IST); first Indian session to react 29 Oct", FED, "2026-10"),
    "fomc_hike_odds": F({"GMT Eight citing CME FedWatch": "70.9% odds of 25 bp hike", "Frenzy Capital FedWatch replica": "hike 8% / hold 92%",
                         "Kryptomagazin FedWatch (ZQX26)": "hike 10% / hold 90%", "Kalshi (via Frenzy)": "7% hike"},
                        "https://www.gmt8press.com/flash/detail/1534460", "2026-10-26",
                        notes="CONFLICT between sources; others: https://www.frenzycap.com/fedwatch , https://terminal.kryptomagazin.cz/en/macro/fedwatch"),
    "india_release_calendar": F({"IIP (Sep)": "2026-10-28", "CPI (Oct)": "2026-11-12", "Q2 GDP": "2026-11-30"},
                                "https://www.mospi.gov.in/uploads/documents/releaseCalender/1774849665042-ADVANCE_RELEASE_CALENDAR_2026_27_FINAL.pdf", "2026-27",
                                notes="IIP 28 Oct also in BS week-ahead: " + BS_WEEK),
    "jio_platforms_listing": F("Jio Platforms listing expected this week (BS week-ahead lists it among key events; exact listing date per BS article)", BS_WEEK, "2026-10-25",
                               notes="date not independently verified on NSE"),
    "us_events": F({"US midterm Election Day + JOLTS": "2026-11-03", "US Oct payrolls": "2026-11-06 08:30 ET", "US Oct CPI": "2026-11-10"},
                   "https://squawkflow.com/calendar/election-week-2026", "2026-09", notes="payrolls: https://www.bls.gov/schedule/news_release/empsit.htm"),
    "diwali_muhurat": F("Muhurat trading Sun 8 Nov 2026 (special session; not counted); Balipratipada holiday Tue 10 Nov; Gurpurb Tue 24 Nov",
                        "https://nsearchives.nseindia.com/content/circulars/CMTR71775.pdf", "2025-12-12", "scraped"),
    "q2_season_this_week": F("This week: TVS Motor, Asian Paints, Trent, Sun Pharma, BEL, IOC, Bank of Baroda, GAIL; 26 Oct: Tata Consumer, Paytm, REC, Mankind, Sona BLW, Nazara, IOB, Bank of Maharashtra. "
                             "Weekend (reaction 26 Oct): Kotak PAT +29.5% (GNPA 1.04%), IndusInd profit Rs 1,176 Cr (GNPA 2.73%), Infosys PAT +6.2% with FY27 cc guidance cut to 1-2%, "
                             "Dr Reddy's PAT -36%, BOI PAT +25.4%, Coforge PAT +56.5%",
                             BS_WEEK, "2026-10-26",
                             notes="weekend results: https://www.moneycontrol.com/news/business/markets/stocks-to-watch-today-infosys-kotak-bank-lupin-kec-international-bank-of-india-coforge-bharat-coking-coal-dcb-bank-netweb-apollo-micro-in-focus-on-26-october-14059620.html/amp"),
    "geopolitics_oil": F("Traders expect US to resume strikes on Iran in coming weeks; US ordered non-essential staff out of Saudi Arabia; Aramco evacuated Dhahran HQ after Houthi attacks",
                         "https://www.cnbc.com/2026/10/23/oil-price-brent-wti-iran-war-saudi-arabia.html", "2026-10-23"),
}

screen_notes = ("Industry PE = median of positive P/E on the screener industry page(s) for the sub-sector; company P/E/mcap/PB taken from screener pages showing the 23-Oct close "
                "(pages showing a live 26-Oct price were rescaled to the 23-Oct NSE close by adjust_fundamentals.py). Pledge from NSE SHP XBRL (latest filed quarter). "
                "Names with no promoter group: pledge N/A (not a fail).")

calendar_items = [
    {"date": "2026-10-28", "symbol": "MACRO", "event": "India IIP (Sep) release", "source": macro["india_release_calendar"]["source_url"], "method": "websearch"},
    {"date": "2026-10-29", "symbol": "MACRO", "event": "FOMC decision (28 Oct 2pm ET = ~23:30 IST); first Indian session to react 29 Oct", "source": FED, "method": "websearch"},
    {"date": "2026-11-03", "symbol": "MACRO", "event": "US midterm elections; US JOLTS", "source": "https://squawkflow.com/calendar/election-week-2026", "method": "websearch"},
    {"date": "2026-11-06", "symbol": "MACRO", "event": "US Oct non-farm payrolls (08:30 ET)", "source": "https://www.bls.gov/schedule/news_release/empsit.htm", "method": "websearch"},
    {"date": "2026-11-08", "symbol": "MACRO", "event": "Diwali Muhurat trading (Sunday special session)", "source": "https://nsearchives.nseindia.com/content/circulars/CMTR71775.pdf", "method": "scraped"},
    {"date": "2026-11-12", "symbol": "MACRO", "event": "India CPI (Oct) release", "source": macro["india_release_calendar"]["source_url"], "method": "websearch"},
    {"date": "2026-10-27", "symbol": "LTTS", "event": "Record date, interim dividend Rs 20", "source": "https://www.ltts.com/press-release/Q2FY27-results", "method": "websearch"},
]


def unconf(estimate, url, notes, prior_year, in_window):
    return F({"date": "N/A", "confirmed": False, "estimate": estimate, "last_year_q2_date_hint": prior_year,
              "probable_inside_window": in_window}, url, "2026-10-25", "websearch", notes)


results_dates = {
    "REDINGTON": unconf("2026-10-30 (stockanalysis estimate, not NSE-confirmed)", "https://stockport.app/results-calendar/redington/",
                        "No NSE board-meeting intimation as of 25 Oct 19:45 IST (Stockport; NSE per-symbol board-meeting API also empty for 26 Oct-31 Dec). "
                        "Q2 dates: 5 Nov 2025, 29 Oct 2024; SEBI deadline 14 Nov. stockanalysis: https://stockanalysis.com/quote/nse/REDINGTON/",
                        "2025-11-05", True),
    "JAMNAAUTO": unconf("N/A", "https://trendlyne.com/equity/board-meeting/JAMNAAUTO/660/jamna-auto-industries-ltd-board_meeting/",
                        "No NSE board-meeting intimation (NSE per-symbol API checked 26 Oct). Prior-year Q2 board meeting 12 Nov 2025; SEBI outer deadline 14 Nov 2026. UNCONFIRMED.",
                        "2025-11-12", True),
}


def B(gnpa, nnpa, car, url, asof, notes=""):
    return F({"gnpa_pct": gnpa, "nnpa_pct": nnpa, "car_pct": car}, url, asof, "websearch", notes)


bank_metrics = {
    "SOUTHBANK": B({"Q2FY26": 2.93, "Q1FY27": 1.38, "Q2FY27": 1.24}, {"Q2FY26": 0.56, "Q1FY27": 0.26, "Q2FY27": 0.09}, {"Q2FY26": 17.70, "Q2FY27": 19.40},
                   "https://nsearchives.nseindia.com/corporate/SOUTHBANK_15102026152810_SD_STT_INVESTORPRESENTATION_15OCT2026.pdf", "2026-09-30",
                   "NIM 3.33%; PCR excl. write-off 92.42%; RoA 1.08%; press release: https://www.bseindia.com/xml-data/corpfiling/AttachLive/430c0778-b124-4b35-84dc-fa670aa1ad32.pdf"),
    "PNB": B({"Q2FY26": 3.45, "Q1FY27": 2.78, "Q2FY27": 2.55}, {"Q2FY26": 0.36, "Q1FY27": 0.28, "Q2FY27": 0.25},
             {"Q2FY26": 17.19, "Q1FY27": 18.13, "Q2FY27": 17.95},
             "https://www.bseindia.com/xml-data/corpfiling/AttachLive/6c942833-673e-48dd-8377-51a5a382ac90.pdf", "2026-09-30",
             "PCR 97.32%; RoA 1.05%; mgmt credit cost guide 0.25-0.30%"),
    "ICICIBANK": B({"Q2FY26": 1.58, "Q1FY27": 1.38, "Q2FY27": 1.20}, {"Q2FY26": 0.39, "Q1FY27": 0.35, "Q2FY27": 0.30}, {"Q2FY27": 16.68},
                   "https://www.icici.bank.in/about-us/news-room/2026/performance-review-quarter-ended-september-30-2026", "2026-09-30",
                   "CET-1 16.01%; PCR 75.0%; NIM 4.18%"),
    "FEDERALBNK": B({"Q2FY27": 1.32}, {"Q2FY27": 0.17}, "N/A",
                    "https://www.cnbctv18.com/market/federal-bank-q2-results-nii-provisions-gross-net-npa-slippages-nim-share-price-move-20013451.htm", "2026-09-30",
                    "NIM 3.32%; CASA 32.0%; PCR 86.8%; CAR not in the cited report"),
    "UNIONBANK": B({"Q1FY27": 2.65, "Q2FY27": 2.42}, {"Q2FY27": 0.42}, "N/A",
                   "https://www.cnbctv18.com/market/union-bank-of-india-q2-results-nii-profit-gross-net-npa-provisions-slippages-share-price-20014870.htm", "2026-09-30",
                   "PCR 95.20%; ECL transition impact ~Rs 5,500 Cr (Rs 1,000 Cr provided); CAR not in the cited report"),
    "KOTAKBANK": B({"Q2FY27": 1.04}, "N/A", "N/A",
                   "https://www.moneycontrol.com/news/business/markets/stocks-to-watch-today-infosys-kotak-bank-lupin-kec-international-bank-of-india-coforge-bharat-coking-coal-dcb-bank-netweb-apollo-micro-in-focus-on-26-october-14059620.html/amp",
                   "2026-09-30", "Results filed Sat 24 Oct; PAT +29.5%; NNPA/CAR not collected"),
}

cyc_ctx = "Brent $116.72 (23 Oct settle, +6% w/w; Reuters); Houthi attacks on Saudi energy sites"
cyclicals = {
    "CHENNPETRO": {"context": "Refiner: Q2 FY27 GRM $20.41/bbl incl. $3.82 inventory gain (core $16.59 per Choice); H1 GRM $14.34; throughput lower on turnaround. " + cyc_ctx,
                   "ev_ebitda_5y_avg": "N/A", "ev_note": "5-year average EV/EBITDA not found in an accessible source (gap)."},
    "GESHIP": {"context": "Tanker/LPG shipping: Q1 FY27 crude-carrier TCE $93,026/day (+175% YoY); 54% of Q2 crude days uncovered (spot exposure); crude tanker orderbook ~27% of fleet (Trade Brains 22 Oct)",
               "ev_ebitda_5y_avg": "N/A", "ev_note": "5-year average EV/EBITDA not found (gap)."},
    "SHYAMMETL": {"context": cyc_ctx, "ev_ebitda_5y_avg": "N/A", "ev_note": "gap"},
    "NUVOCO": {"context": "Cement; Q2 FY27 results filed 22 Oct 18:49 IST", "ev_ebitda_5y_avg": "N/A", "ev_note": "gap"},
}

forward_pe_second_source = {s: v for s, v in FWD.items() if v.get("value") not in (None, "N/A")}

cross_checks_extra = [
    {"field": "usdinr_close_2026-10-23", "ticker": "USDINR", "source_a": "Yahoo USDINR=X", "source_b": "PTI 94.93 / BS 94.94", "values": [94.71, 94.93, 94.94],
     "gap_pct": 0.24, "chosen": "reported close (PTI/BS) for level; Yahoo for returns"},
    {"field": "india_vix_2026-10-23", "ticker": "INDIAVIX", "source_a": "NSE 16.86", "source_b": "Moneycontrol Pro 16.76", "values": [16.86, 16.76], "gap_pct": 0.6, "chosen": "NSE"},
    {"field": "fomc_hike_odds", "ticker": "MACRO", "source_a": "GMT Eight (CME) 70.9%", "source_b": "Frenzy 8% / Kryptomagazin 10% / Kalshi 7%", "values": [70.9, 8, 10, 7],
     "gap_pct": None, "chosen": "both recorded (conflict; unresolved)"},
    {"field": "fii_week_flow", "ticker": "MACRO", "source_a": "CNBC-TV18 -2,697.37 Cr", "source_b": "ET -26,970 Cr", "values": [-2697.37, -26970], "gap_pct": 900,
     "chosen": "CNBC-TV18 (matches sum of NSE daily provisional; ET appears 10x typo)"},
    {"field": "fii_oct_mtd", "ticker": "MACRO", "source_a": "Moneycontrol Pro (exchange) -51,466.38 Cr", "source_b": "NDTV Profit (NSDL) -48,056 Cr", "values": [-51466.38, -48056],
     "gap_pct": 6.6, "chosen": "both recorded (different bases: exchange provisional vs depository settlement)"},
]

gaps = [
    {"item": "EV/EBITDA 5-year average (cyclicals)", "status": "N/A",
     "reason": "no free source with a 5y EV/EBITDA history found; current EV/EBITDA only where screener shows it"},
    {"item": "Results dates not yet intimated to NSE", "status": "unconfirmed",
     "tickers": ["REDINGTON", "JAMNAAUTO", "GESHIP", "CPPLUS", "CUPID", "PTCIL"],
     "reason": "no board-meeting intimation on NSE as of 26-Oct pre-open; prior-year Q2 dates (NSE board-meeting API Oct-Nov 2025) recorded as hints only"},
    {"item": "NSE corporate financial-results API", "status": "empty response",
     "reason": "api/corporates-financial-results returned [] again; Q2 filings detected via api/corporate-announcements and per-symbol api/corporate-board-meetings"},
    {"item": "CAR for FEDERALBNK, UNIONBANK, KOTAKBANK; NNPA for KOTAKBANK", "status": "N/A", "reason": "not stated in the cited reports"},
    {"item": "Nifty Midcap/Smallcap index series on Yahoo", "status": "HTTP 404", "reason": "sector/size RS taken from NSE ind_close_all CSVs instead"},
    {"item": "Bulk deals 23-Oct", "status": "partial", "reason": "NSE bulk.csv fetched; block.csv returned NO RECORDS"},
    {"item": "Setup-C reaction for filings after 23-Oct 15:30 or on Sat/Sun 24-25 Oct", "status": "pending",
     "tickers": ["APOLLO", "AUBANK", "BANKINDIA", "BHARATCOAL", "BPCL", "CASTROLIND", "COFORGE", "CRISIL", "DCBBANK", "DRREDDY", "GAEL", "IDFCFIRSTB",
                 "INDUSINDBK", "INFY", "JKCEMENT", "JKTYRE", "KAJARIACER", "KOTAKBANK", "LUMAXTECH", "MASTEK", "NETWEB", "OFSS", "RAILTEL", "SBFC",
                 "SHAKTIPUMP", "SPLPETRO", "TMCV", "TORNTPHARM", "TRIVENIPT", "UTIAMC"],
     "reason": "reaction session is 26-Oct (live, excluded)"},
    {"item": "GSFC results filing timestamp", "status": "N/A", "reason": "no timestamped filing found in NSE announcements"},
]

corporate_actions_web = {
    "TECHM": [{"action": "1:1 bonus issue recommended by board; interim dividend Rs 15; bonus credit expected by 15 Dec (Zee)", "announced": "2026-10-15",
               "record_date": "N/A (not yet announced)", "source_url": "https://www.techmahindra.com/insights/press-releases/techmahindra-q2-fy27-results/"}],
    "LTTS": [{"action": "interim dividend Rs 20", "announced": "2026-10-20", "record_date": "2026-10-27",
              "source_url": "https://www.ltts.com/press-release/Q2FY27-results"}],
    "CHENNPETRO": [{"action": "interim dividend Rs 25", "announced": "2026-10-22", "record_date": "N/A (see NSE corporate actions)",
                    "source_url": "https://nsearchives.nseindia.com/corporate/CHENNPETRO_22102026133810_Q2_Results.pdf"}],
    "TANLA": [{"action": "board to consider interim dividend with Q2 results", "announced": "2026-10-21", "record_date": "board meeting 2026-10-27",
               "source_url": "https://www.bseindia.com/xml-data/corpfiling/AttachLive/528d710e-32c5-40db-9ceb-753072946d12.pdf"}],
    "SUNTV": [{"action": "board to consider interim dividend with Q2 results", "announced": "2026-10-22", "record_date": "board meeting 2026-10-30",
               "source_url": "https://hk.marketscreener.com/news/sun-tv-network-board-meeting-notice-for-the-quarter-and-half-year-ended-september-30-2026-ce785cdede80f420"}],
}

json.dump({"flows": flows, "corporate_actions_web": corporate_actions_web, "market_extra": market_extra, "breadth_cross_checks": breadth_cross_checks, "macro": macro,
           "screen_notes": screen_notes, "calendar_items": calendar_items, "results_dates": results_dates,
           "bank_metrics": bank_metrics, "cyclicals": cyclicals, "forward_pe_second_source": forward_pe_second_source,
           "cross_checks_extra": cross_checks_extra, "gaps": gaps},
          open(os.path.join(RAW, "web_facts.json"), "w"), indent=1)
print("web_facts written; fwd2", len(forward_pe_second_source), "results_dates", list(results_dates))

# Data sources — run 2026-10-26 (IST), data session Fri 2026-10-23

- **DATA_MODE:** WEB
- **MCP_ERROR (verbatim):** screener / screener-core MCP namespaces are absent from the tool catalog in this environment (GetDynamicTools full catalog lists only cursor, Cursor Automation Tools, cursor-cloud, cursor-subscriptions; pattern search 'screener' returned 0 matches). Not authenticated, per run rules.
- **Session check:** Fri 2026-10-23 is the last completed NSE session.
  - It is the latest bhavcopy (`sec_bhavdata_full_23102026.csv`, HTTP 200) and the latest `ind_close_all_23102026.csv`.
  - It is the last bar in all 499 computed Nifty 500 Yahoo series (`names_last_bar_not_session = []`).
  - Mon 26-Oct is a trading day in the NSE holiday master. Live 26-Oct Yahoo bars (`dt > 2026-10-23`) were dropped in `raw/compute_indicators.py`.
  - Screener pages showing a live price were rescaled to the NSE 23-Oct close (181 pages).
- **Results-season window:** 15 NSE sessions, with Mon 26 Oct as day 1 and Tue 10 Nov (Diwali Balipratipada) excluded. The window ends **Mon 2026-11-16**. The Sun 8 Nov Muhurat session is not counted. Session list: `data.json → results_window`.

## Sources

| Source | URL / endpoint | Used for | HTTP | Notes |
|---|---|---|---|---|
| NSE bhavcopy | nsearchives.nseindia.com/products/content/sec_bhavdata_full_DDMMYYYY.csv (20 sessions, 24 Sep to 23 Oct; 2-Oct and 20-Oct holidays) | Official 23-Oct close, OHLC for follow-ups, delivery %, 20-day ADV (value) | 200 ×20 | Yahoo vs NSE close: no gap > 0.5% after the ICICIPRULI→ICICILIFE alias (see gaps). |
| NSE index closes | nsearchives.nseindia.com/content/indices/ind_close_all_{23102026, 16102026, 23092026, 23072026}.csv (+22092026) | Nifty 50/500 closes and PE/PB, VIX, sector 1W/1M/3M returns, RS vs Nifty 500 | 200 ×5 | 1W base 16-Oct (4 sessions), 1M base 23-Sep (20 sessions), 3M base 23-Jul (63 sessions). |
| NSE APIs (cookie from www.nseindia.com + Referer) | api/holiday-master?type=trading · api/reportASM · api/reportGSM · api/corporate-board-meetings (past 25-09→25-10; future 26-10→31-12; 2025 Q2 01-10-2025→30-11-2025 for date hints; per-symbol `&symbol=X` for results checks) · api/event-calendar · api/corporates-corporateActions · api/fiidiiTradeReact | Holidays, ASM/GSM, results dates, corporate actions, 23-Oct FII/DII provisional (FII +887.65 Cr, DII +3,235.36 Cr) | 200 | The homepage returns 403, but its cookie still works. |
| NSE corporate announcements | api/corporate-announcements?index=equities&symbol=X&from_date=&to_date= | Setup-C filing timestamps (161 board meetings 1–25 Oct) and results checks | 200 | GSFC had no timestamped results filing. |
| NSE financial results API | api/corporates-financial-results?index=equities&period=Quarterly | — | 200 but empty (`[]`) | Gap; replaced by corporate announcements and per-symbol board meetings. |
| nsearchives misc | content/fo/fo_secban.csv · content/equities/bulk.csv · block.csv | F&O ban for trade date 26-Oct (AMBUJACEM, KAYNES, SAIL); 23-Oct bulk deals | 200 | block.csv: NO RECORDS. |
| NSE SHP XBRL | nsearchives.nseindia.com/corporate/xbrl/SHP_*.xml (via api/corporate-share-holdings-master?symbol=) | Promoter pledge % (188 names) | 200 | 181 of 188 are as of 30-Sep-2026. Symbols containing `&` needed URL-encoding (fixed; M&MFIN and J&KBANK re-fetched). |
| niftyindices | ind_nifty500list.csv, ind_niftymicrocap250_list.csv, ind_nifty50list.csv, ind_niftyfinancelist.csv | Universe membership | 200 | Nifty 500 list unchanged vs last week. |
| Yahoo v8 chart | query1.finance.yahoo.com/v8/finance/chart/{SYM}.NS?range=1y&interval=1d | OHLCV; all DMA/EMA/RSI/ATR/pivots/consolidation/breadth computed in Python | 200 (786 chart files) | Windows Chrome UA. 404: ^CNXMIDCAP, ^CNXSMALLCAP (sector RS uses NSE CSVs instead), BAGMANE, DUMMYHEG. |
| Yahoo v10 quoteSummary | query1.finance.yahoo.com/v10/finance/quoteSummary/{SYM}.NS | forwardEps, trailingEps, bookValue, ROE (TTM), EPS revisions, ratings, EV/EBITDA | 200 (62 names fetched, 25 candidates parsed) | Cookie + crumb. Prices are live 26-Oct, so forward PE = 23-Oct close / forwardEps. |
| screener.in company pages | screener.in/company/{SYM}/consolidated/ (standalone fallback) | PE, PB, ROE, D/E, EPS, OCF, 3y CAGRs, quarters, holdings, Q2 YoY for Setup-C | 200 (685 pages: 519 universe + 29 extra Setup-C names + 137 peers) | 14 stale consolidated pages replaced by standalone (incl. TATAELXSI, RAILTEL, JUSTDIAL, AUBANK). ICICIPRULI 404 → page now `ICICILIFE`. Pages fetched after 09:15 IST show live prices and were rescaled (181). 429 backoff, 2 streams. |
| screener.in industry pages | screener.in/market/{IN…}/ (?page=N) | Industry median PE (top 25 by mcap, primary; all pages, secondary), peer PB/ROE medians (top 12 peers) | 200 (211 pages, 83 industries; every page of each industry) | Fetched 26-Oct after 09:15 IST, so peer PEs are live prices (see gaps). |
| stockanalysis.com | stockanalysis.com/quote/nse/{SYM}/statistics/ | Second-source forward PE (25 of 26 names), estimated earnings dates | 200 | Rebased: implied EPS = page price / Forward PE; value = 23-Oct close / implied EPS. Earnings dates are estimates unless NSE confirms. TTML: N/A. |
| Web search (news/macro) | URLs per row in news.md and `data.json` leaves | Weekly FII/DII (CNBC-TV18, fiianddiidata), MTD (Moneycontrol Pro, NDTV/NSDL), USD/INR (PTI, BS), FX reserves (rbi.org.in prid=63855), 10y G-sec, Brent (Reuters), RBI policy (prid=63742), FOMC/MoSPI/BLS calendars, breadth cross-checks (IndexBreadth, Zerodha, Flash Finance), bank metrics, company news | n/a (search) | Third-party, unverified. Conflicts are recorded in `cross_checks`. |

## Method notes

- **Technical screen.** Rule A: Price > DMA50 > DMA200 and Price > 0.75 × 52wH. Rule B: as Rule A but DMA50 may be below DMA200 if DMA200 is rising over 20 sessions. Result: 29 names pass on Rule A and 1 on Rule B (SUNTV), 30 in total.
- **Valuation screen.**
  - Industry PE is the median of positive PEs on screener industry page 1 (top 25 by mcap). The all-pages median is a secondary flag only (IPCALAB passes top-25 at 37.9 but not all-pages at 28.1).
  - Financials variant: PB < peer median PB, ROE > 12, PE > 0, mcap > 12,000, and the technical pass. D/E is ignored.
- **Track B (`track_b_5k`).**
  - Scope: Microcap 250 plus Nifty 500 names at 5,000–12,000 Cr.
  - Momentum test: close ≥ 0.75 × 52wH, close > DMA50, DMA50 > DMA200 or DMA200 rising, and 3M return > Nifty 500 3M return (-6.765%).
  - Value test: as the main screen, plus ADV20 ≥ 25 Cr.
  - Microcap names with mcap ≥ 12,000 are listed in `track_b_5k.microcap_mcap_ge_12000_belongs_in_track_a`.
- **Setup-C.**
  - Reaction session: the results day if filed before 15:30 IST, otherwise the next session.
  - Move: reaction close vs prior close for intraday filings; reaction open vs prior close for after-market filings.
  - Held: every close since the reaction session is ≥ the prior close.
  - Eligible: move > 0, held, ≥ 3 sessions, mcap ≥ 5,000 Cr and ADV ≥ 25 Cr. YoY from screener Sep-26 vs Sep-25 quarter columns.
- **Follow-ups (`data.json → followups`).** SOUTHBANK OHLC for 16/19/21/22/23 Oct from the bhavcopy, with zone/stop/T1 comparisons only. Watchlist results status from the NSE board-meeting API.
- **Cross-checks.**
  - Price checks NSE against Yahoo. PE, PB, mcap and ROE check screener against Yahoo.
  - Gaps above 3% are in `cross_checks.flagged_gt_3pct` (37), each with a `screen_impact` note.
  - Only FEDERALBNK ROE (11.6 vs 13.27 TTM) and STLTECH ROE (1.24 vs 22.92 TTM) would flip a filter under source B. Neither is a main-screen pass.
  - Preference order: NSE/BSE > screener > others.
- **Forward PE.** Primary: 23-Oct close / Yahoo forwardEps. Second source: stockanalysis rebased (see table).

## Gaps (also in `data.json → gaps`)

- **EV/EBITDA 5-year average** is N/A for the cyclicals CHENNPETRO, GESHIP, SHYAMMETL and NUVOCO. No free history source was found.
- **Results dates not intimated to NSE** for REDINGTON, JAMNAAUTO, GESHIP, CPPLUS, CUPID and PTCIL. Only prior-year Q2 dates and estimates are recorded, marked unconfirmed.
- **NSE financial-results API** returned empty again.
- **Industry and peer medians** come from 26-Oct live-price pages. Subject PE/PB were rescaled to the 23-Oct close. Peers outside the bhavcopy summary were not rescaled. A few illiquid peers show older price lines (12 Oct, 14 Oct, 29 Sep, 21–22 Oct).
- **Promoter pledge N/A (no promoter group, not a fail):** COFORGE, CROMPTON, ETERNAL, FEDERALBNK, HDFCBANK, ICICIBANK, IDFCFIRSTB, IXIGO, REDINGTON, SOUTHBANK, SWIGGY, UJJIVANSFB, UTIAMC, YESBANK.
- **Bank CAR** is N/A for FEDERALBNK, UNIONBANK and KOTAKBANK, and KOTAKBANK NNPA is N/A, because the cited reports don't state them.
- **Second-source forward PE** is N/A for TTML.
- **Setup-C reaction pending** for 30 names filed after 23-Oct 15:30 or on 24/25-Oct (incl. KOTAKBANK, CASTROLIND, INFY, COFORGE, CRISIL, INDUSINDBK, DRREDDY, BANKINDIA). Their reaction session is 26-Oct, which is live and excluded.
- **FOMC 28-Oct hike odds conflict:** GMT Eight (CME) 70.9% vs Frenzy 8%, Kryptomagazin 10% and Kalshi 7%. Unresolved; both sides recorded.
- **ET flow figures** (FII -26,970 Cr for the week, -5,14,660 Cr MTD) are 10× every other outlet. Treated as a typo and not used.
- **Jio Platforms listing date:** cited in the BS week-ahead piece but not verified on NSE.
- **ICICIPRULI:** the Nifty 500 CSV and Yahoo still use ICICIPRULI, while the NSE bhavcopy and screener now use ICICILIFE. Aliased in `raw/bhav.py`; screener page saved under ICICIPRULI.

## Files

- `data.json`: all structured data. Leaves are {value, source_url, as_of, method, notes?}. The top-level `regime` and `followups` keys are new this week.
- `news.md`: 109 items across 25 sections (market plus every main/financials pass, Setup-C eligible name, watchlist name and near-miss).
- `data_sources.md`: this file.
- `raw/`: Python scripts plus small JSON/CSV.
  - `raw/web_facts.json` holds the web-sourced facts.
  - `raw/computed/` holds indices, sectors, summary, screen_result, peer_pb_roe, pledge, setupc_price_action, trackb_value and forward_pe_sa.
- **Bulky intermediates kept out of the repo** (copy them back to `raw/computed/` to re-run `assemble_outputs.py`):
  - In `/tmp/run1026/computed/`: tech.json, screener_fundamentals.json, industry_medians.json, quotesummary.json, trackb_tech.json and nse_bhav_summary.json.
  - In `/tmp/run1026/`: raw HTML, charts, XBRL and bhavcopies (charts/, qs/, screener/, industries/, misc/).

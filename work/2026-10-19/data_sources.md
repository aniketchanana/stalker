# Data sources — run 2026-10-19 (IST), data session Fri 2026-10-16

- **DATA_MODE:** WEB
- **MCP_ERROR (verbatim):** screener / screener-core MCP namespaces are absent from the tool catalog in this environment (GetDynamicTools full catalog lists only cursor, Cursor Automation Tools, cursor-cloud, cursor-subscriptions; pattern search '(?i)screener' returned 0 matches). Not authenticated, per run rules.
- **Session check:** Fri 2026-10-16 is the last completed NSE session.
  - It is the latest bhavcopy (`sec_bhavdata_full_16102026.csv`, HTTP 200) and the latest `ind_close_all_16102026.csv`.
  - It is the last bar in all 499 computed Nifty 500 Yahoo series (`names_last_bar_not_session = []`).
  - The NSE holiday master lists Mon 19-Oct as a trading day. Live 19-Oct Yahoo bars (`dt > 2026-10-16`) were dropped in `raw/compute_indicators.py`.
- **Results-season window:** 15 NSE sessions, with 19 Oct as day 1 and Dussehra (Tue 20 Oct) excluded. The window ends **Mon 2026-11-09**. The Sun 8 Nov Muhurat session is not counted. Session list: `data.json → results_window`.

## Sources

| Source | URL / endpoint | Used for | HTTP | Notes |
|---|---|---|---|---|
| NSE bhavcopy | nsearchives.nseindia.com/products/content/sec_bhavdata_full_DDMMYYYY.csv (20 sessions, 18 Sep to 16 Oct) | Official 16-Oct close, delivery %, 20-day ADV (value) | 200 ×20 | Yahoo vs NSE close agree; max gap is in `cross_checks` (`price_all_bhav_names`). |
| NSE index closes | nsearchives.nseindia.com/content/indices/ind_close_all_{16102026, 09102026, 16092026, 17072026}.csv | Nifty 50/500 closes, sector 1W/1M/3M returns, RS vs Nifty 500 | 200 ×4 | 1M base 16-Sep, 3M base 17-Jul. |
| NSE APIs (cookie from www.nseindia.com + Referer) | api/holiday-master?type=trading · api/reportASM · api/reportGSM · api/corporate-board-meetings (past 25-09→18-10, future 19-10→30-11, and 2025 Q2 for date hints) · api/event-calendar · api/corporates-corporateActions · api/fiidiiTradeReact | Holidays, ASM/GSM, results dates, corporate actions, 16-Oct FII/DII provisional | 200 | The homepage itself returns 403, but its cookie still works. |
| NSE corporate announcements | api/corporate-announcements?index=equities&symbol=X&from_date=&to_date= | Setup-C filing timestamps (72 names) and results checks (14 names) | 200 | Only TATACOMM showed a results filing (15-Oct 13:59) among unreported-check names. |
| NSE financial results API | api/corporates-financial-results?index=equities&period=Quarterly | — | 200 but empty (`[]`) | Gap; replaced by corporate-announcements. |
| nsearchives misc | content/fo/fo_secban.csv · content/equities/bulk.csv · block.csv | F&O ban (trade date 19-Oct), bulk/block deals (latest day) | 200 | |
| NSE SHP XBRL | nsearchives.nseindia.com/corporate/xbrl/SHP_*.xml (via api/corporate-share-holdings-master?symbol=) | Promoter pledge % (184 names) | 200 | Many are as of 30-Jun-2026 (Sep SHP not yet filed). Names with no promoter group get N/A, which is not a fail. |
| niftyindices | ind_nifty500list.csv, ind_niftymicrocap250_list.csv, ind_nifty50list.csv, ind_niftyfinancelist.csv | Universe membership | 200 | |
| Yahoo v8 chart | query1.finance.yahoo.com/v8/finance/chart/{SYM}.NS?range=1y&interval=1d | OHLCV; all DMA/EMA/RSI/ATR/pivots/breadth computed in Python | 200 (779/786) | Windows Chrome UA. Failures: ^CNXMIDCAP and ^CNXSMALLCAP (404, so sector RS uses NSE CSVs), BAGMANE, and four NSE DUMMY* placeholder symbols. |
| Yahoo v10 quoteSummary | query1.finance.yahoo.com/v10/finance/quoteSummary/{SYM}.NS | forwardEps, trailingEps, bookValue, ROE (TTM), EPS revisions, ratings | 200 (143 names) | Cookie + crumb. Prices are live for 19-Oct, so forward PE was recomputed as 16-Oct close / forwardEps. |
| screener.in company pages | screener.in/company/{SYM}/consolidated/ (standalone fallback) | PE, PB, ROE, D/E, EPS, OCF, 3y CAGRs, quarters, holdings | 200 (700 pages; one 404 for a DUMMY symbol) | Pages fetched after 09:15 IST show **live** prices and are always rescaled to the NSE 16-Oct close (172 rescaled). Stale consolidated pages were replaced by standalone (e.g. TATAELXSI). Rate-limited (429 backoff). |
| screener.in industry pages | screener.in/market/{IN…}/ (?page=N) | Industry median PE (top 25 by mcap), peer PB/ROE medians (top 12 peers) | 200 (199 pages, 80 industries) | Fetched 19-Oct, so they carry live prices (see gaps). |
| stockanalysis.com | stockanalysis.com/quote/nse/{SYM}/statistics/ | Second-source forward PE (42 names), estimated earnings dates | 200 | Forward PE rebased: implied EPS = live price / Forward PE; value = 16-Oct close / implied EPS. Earnings dates are estimates unless NSE confirms. |
| Web search (news/macro) | URLs per row in news.md and `data.json` leaves | FPI week/MTD (ET, TOI), USD/INR, FX reserves, RBI policy (rbi.org.in prid=63742), MoSPI/Fed/BLS calendars, bank metrics, breadth cross-checks (IndexBreadth, Flash Finance), company news | n/a (search) | Third-party, unverified. Items that conflict are recorded in `cross_checks`. |

## Method notes

- **Technical screen.** Rule A: Price > DMA50 > DMA200 and Price > 0.75 × 52wH. Rule B: as Rule A but DMA50 may be below DMA200 if DMA200 is rising over 20 sessions. Result: 70 names pass on Rule A and 4 on Rule B, 74 in total.
- **Valuation screen.**
  - Industry PE is the median of positive PEs on screener industry page 1 (top 25 by mcap). The all-pages median is recorded as a secondary flag only.
  - Financials variant: PB < peer median, ROE > 12, PE > 0, mcap > 12,000, and the technical pass. D/E is ignored.
- **Track B (`track_b_5k`).**
  - Scope: Microcap 250 plus Nifty 500 names at 5,000–12,000 Cr.
  - Momentum test: close ≥ 0.75 × 52wH, close > DMA50, DMA50 > DMA200 or DMA200 rising, and 3M return > Nifty 500 3M return.
  - Value test: as the main screen, plus ADV20 ≥ 25 Cr.
- **Setup-C.**
  - Reaction session: the results day if filed before 15:30 IST, otherwise the next session.
  - Move: reaction close vs prior close for intraday filings; reaction open vs prior close for after-market filings.
  - Held: every close since the reaction session is ≥ the prior close.
  - Eligible: move > 0, held, ≥ 3 sessions, mcap ≥ 5,000 Cr and ADV ≥ 25 Cr.
- **Cross-checks.**
  - Price checks NSE against Yahoo.
  - PE, PB, mcap and ROE check screener against Yahoo.
  - Gaps above 3% are listed in `cross_checks.flagged_gt_3pct`, each with a `screen_impact` note.
  - Only ELECON ROE and FEDERALBNK ROE would flip a filter under source B. Neither is a main-screen pass.
  - Preference order: NSE/BSE > screener > others.
- **Forward PE.** Primary: 16-Oct close / Yahoo forwardEps. Second source: stockanalysis rebased (see table).

## Gaps (also in `data.json → gaps`)

- **EV/EBITDA 5-year average** is N/A for the cyclicals COALINDIA, MRPL, GESHIP, WELCORP, PETRONET and JINDALSAW. No free history source was found.
- **Results dates not intimated to NSE** for COALINDIA, GESHIP, HAL, REDINGTON, SUNTV, WELCORP, JAMNAAUTO, SUPRIYA, TANLA, AARTIIND, AUROPHARMA, ECLERX, FINCABLES, JYOTICNC and SHYAMMETL. Only estimates or prior-year hints are recorded, marked unconfirmed.
- **NSE financial-results API** returned empty.
- **Industry and peer medians** were computed from 19-Oct live-price pages. Subject PE/PB were rescaled to the 16-Oct close; peer PB was not.
- **Stale screener quarterly data** for GSPLTRANS, MONEYVIEW, AXIOMGAS (2024-06) and SITINET (2025-09). This affects peer medians only.
- **Promoter pledge** is as of 30-Jun-2026 for many names. REDINGTON, SOUTHBANK, BSE and FEDERALBNK have no promoter group, so pledge is N/A.
- **Second-source forward PE** is N/A for SUPRIYA and JAYNECOIND. JAYNECOIND also has no Yahoo forward EPS.
- **CUB bank metrics** (GNPA/NNPA/CAR for the latest quarter) are N/A.
- **NSDL fortnightly FPI data and tipsheet figures** were omitted because no citable URL was found. Weekly and MTD FPI figures come from news citing NSE/NSDL.
- **Earnings-call transcripts:** the fetch returned an empty document.
- **Setup-C reaction pending** for filings on or after 16-Oct 15:30 or on Sat 17-Oct: AXISBANK, BAJAJHFL, CENTRALBK, DLF, HDFCBANK, HSCL, ICICIBANK, IDBI, INDIACEM, IXIGO, JINDALSAW, LTM, OBEROIRLTY, PNB, TEJASNET, URBANCO and YESBANK. Their reaction session is 19-Oct, which is live and excluded.

## Files

- `data.json`: all structured data. Leaves are {value, source_url, as_of, method, notes?}.
- `news.md`: 134 items across 45 sections (market plus every candidate).
- `data_sources.md`: this file.
- `raw/`: Python scripts plus small JSON.
  - `raw/web_facts.json` holds the web-sourced facts.
  - `raw/computed/` holds indices, sectors, summary, screen_result, peer_pb_roe, pledge, setupc_price_action, trackb_value and forward_pe_sa.
- **Bulky intermediates kept out of the repo** (copy them back to `raw/computed/` to re-run `assemble_outputs.py`):
  - In `/tmp/swing-2026-10-19/computed/`: tech.json, screener_fundamentals.json, industry_medians.json, quotesummary.json, trackb_tech.json and nse_bhav_summary.json.
  - In `/tmp/swing-2026-10-19/`: raw HTML, charts, XBRL and bhavcopies (charts/, qs/, screener/, industries/, misc/).

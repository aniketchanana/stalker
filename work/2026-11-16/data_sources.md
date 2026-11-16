# Data sources — run 2026-11-16 (IST), data session Fri 2026-11-13

- **DATA_MODE:** WEB
- **MCP_ERROR (verbatim):** screener / screener-core MCP namespaces are absent from the tool catalog in this environment (GetDynamicTools pattern search 'screener' returned 0 matches on 2026-11-16). Not authenticated, per run rules.
- **Session check:** Fri 2026-11-13 is the last completed NSE session.
  - It is the latest bhavcopy (`sec_bhavdata_full_13112026.csv`, HTTP 200) and the latest `ind_close_all_13112026.csv`.
  - It is the last bar in all computed Nifty 500 Yahoo series. Live 16-Nov Yahoo bars (`dt > 2026-11-13`) were dropped in `raw/compute_indicators.py`.
  - Tue 10-Nov (Diwali Balipratipada) was a holiday; its bhavcopy URL returns a byte-identical copy of the 9-Nov file and is ignored. The Sun 8-Nov Muhurat session is not counted.
  - Screener price lines: 604 of 725 pages show "13 Nov"; 6 illiquid pages show older dates (12/11 Nov, 30/29 Oct); 115 BSE-only peer pages show none. 14 pages whose price differed from the NSE 13-Nov close were rescaled to it.
- **Results-season window:** 15 NSE sessions, Mon 16-Nov = day 1, Tue 24-Nov (Prakash Gurpurb) excluded. The window ends **Mon 2026-12-07**. Session list: `data.json → results_window`.

## Sources

| Source | URL / endpoint | Used for | HTTP | Notes |
|---|---|---|---|---|
| NSE bhavcopy | nsearchives.nseindia.com/products/content/sec_bhavdata_full_DDMMYYYY.csv (20 sessions, 15-Oct to 13-Nov; plus 21 sessions 15-Sep to 14-Oct for SOUTHBANK 20-day averages; plus Muhurat 08-Nov file) | Official 13-Nov close, OHLC for follow-ups, delivery %, 20-day ADV (value) | 200 ×42 | 10-Nov URL = duplicate of 9-Nov (ignored). |
| NSE index closes | nsearchives.nseindia.com/content/indices/ind_close_all_{13112026, 06112026, 13102026, 13082026}.csv (+23102026) | Nifty 50/500 closes and PE/PB, VIX, sector 1W/1M/3M returns, RS vs Nifty 500 | 200 ×5 | 1W base 06-Nov (4 sessions), 1M base 13-Oct, 3M base 13-Aug. |
| NSE APIs (no homepage cookie; Referer header) | api/holiday-master?type=trading · api/reportASM · api/reportGSM · api/corporate-board-meetings (past 19-10→15-11; future 16-11→31-12) · api/event-calendar · api/corporates-corporateActions · api/fiidiiTradeReact | Holidays, ASM/GSM, results dates, corporate actions, 13-Nov FII/DII provisional (FII +5,736.55 Cr, DII -2,253.58 Cr) | 200 | Homepage returns 403; api/* returns 200 without cookies. |
| NSE corporate announcements | api/corporate-announcements?index=equities&symbol=X | Setup-C results filing timestamps (674 names scanned) | 200 | No timestamped results filing found for GRSE, TARC, TATASTEEL, TITAGARH, PARKHOSPS, BAGMANE (see gaps). |
| NSE financial results API | api/corporates-financial-results?index=equities&period=Quarterly | — | 200 but empty (`[]`) | Gap; replaced by corporate announcements and board meetings. |
| NSE deals | content/equities/bulk.csv · block.csv (13-Nov) · api/historicalOR/bulk-block-short-deals?optionType=bulk_deals/block_deals&from=&to= (one call per session 30-Oct→13-Nov; `raw/deals_fetch.py`) | Bulk/block deals | 200 | Block deals complete (72 rows, 10 sessions). Bulk history capped at 70 rows/day (alphabetical) → partial for 30-Oct→12-Nov; 13-Nov bulk.csv complete. |
| nsearchives F&O ban | content/fo/fo_secban.csv | Ban list for trade date 16-Nov | 200 | NIL. |
| NSE SHP XBRL | nsearchives.nseindia.in/corporate/xbrl/SHP_*.xml (via api/corporate-share-holdings-master?symbol=) | Promoter pledge % (300 names) | 200 | 291 of 300 as of 30-Sep-2026; 16 have no promoter group (N/A, not a fail). |
| niftyindices | ind_nifty500list.csv, ind_niftymicrocap250_list.csv, ind_nifty50list.csv, ind_niftyfinancelist.csv | Universe membership | 200 | |
| Yahoo v8 chart | query1.finance.yahoo.com/v8/finance/chart/{SYM}.NS?range=1y&interval=1d | OHLCV; all DMA/EMA/RSI/ATR/breadth computed in Python | 200 (784 chart files) | 404: ^CNXMIDCAP, ^CNXSMALLCAP (sector RS uses NSE CSVs), BAGMANE. Brent (BZ=F), USD/INR, DXY also from v8. |
| Yahoo v10 quoteSummary | query1.finance.yahoo.com/v10/finance/quoteSummary/{SYM}.NS | forwardEps, trailingEps, bookValue, ROE, consensus EPS (earningsEstimate.avg), EPS revisions, ratings, EV/EBITDA | 200 (201 names) | Cookie + crumb. Prices live 16-Nov, so forward PE = 13-Nov NSE close / forwardEps. 7 names return 0.0 placeholders in epsTrend → treated as missing. |
| screener.in company pages | screener.in/company/{SYM}/consolidated/ (standalone fallback) | PE, PB, ROE, D/E, EPS, OCF, 3y CAGRs, quarters, holdings, Q2 YoY for Setup-C | 200 (725 pages: 587 universe/Setup-C + 138 peers) | 429 backoff, 2–3 streams. 115 peer pages are BSE-only (numeric codes): not rescaled. |
| screener.in industry pages | screener.in/market/{IN…}/ (?page=N) | Industry median PE (top 25 by mcap primary; all pages secondary), peer PB/ROE medians (top 12 peers) | 200 (272 pages, 133 industries) | Fetched before the 16-Nov open (13-Nov prices). ADANIENSOL and INDIGO: no industry median. |
| stockanalysis.com | stockanalysis.com/quote/nse/{SYM}/statistics/ | Second-source forward PE (34 of 34 names), estimated earnings dates | 200 | Rebased: implied EPS = page price / Forward PE; value = 13-Nov close / implied EPS. |
| Web search (news/macro) | URLs per row in news.md and `data.json` leaves | Weekly FII/DII (fiianddiidata, Alloqo daily provisional), MTD (BusinessLine), USD/INR, 10y G-sec, Brent context, RBI MPC calendar, MoSPI calendar, bank metrics, company news | n/a (search) | Third-party, unverified. Conflicts recorded in `cross_checks` / `web_facts.json → cross_checks_extra`. |

## Method notes

- **FII/DII weekly.** Sum of NSE daily provisional figures: 26–30 Oct FII +6,304.67 / DII +3,109.79; 2–6 Nov FII +45,960.02 / DII -24,196.52; 9–13 Nov (4 sessions) FII +33,342.70 / DII -24,191.81; Nov MTD FII +79,302.47 / DII -49,088.64 Cr (Muhurat 8-Nov included in MTD). BusinessLine's Rs 79,301 Cr MTD agrees.
- **Technical screen.** Rule A: Price > DMA50 > DMA200 and Price > 0.75 × 52wH. Rule B: as A but DMA50 may be below DMA200 if DMA200 is rising over 20 sessions. Result: 147 (A 134, B 13).
- **Valuation funnel.** tech 147 → mcap > 12,000 Cr 146 → PE > 0 141 → PE < industry median (top 25) 27 (all-pages: 14) → ROE > 12 19 → D/E < 1 17 → pledge not failed 17 → pledge confirmed < 20 17.
  - Financials variant: PB < peer median PB, ROE > 12, PE > 0, mcap > 12,000, technical pass; D/E ignored. 4 pass.
  - Near-miss list: PE within 5% above the top-25 industry median (9 names).
- **Track B (`track_b_5k`).** Microcap 250 + Nifty 500 names at 5,000–12,000 Cr. Momentum: close ≥ 0.75 × 52wH, close > DMA50, DMA50 > DMA200 or DMA200 rising, 3M return > Nifty 500 3M (0.26%) → 55. Value test as the main screen plus ADV20 ≥ 25 Cr → 4.
- **Setup-C.** Reaction session = results day if filed before 15:30 IST, else next session. Move = reaction close vs prior close (intraday filing) or reaction open vs prior close (after-market). Held = every close since the reaction session ≥ prior close. Eligible = move > 0, held, ≥ 3 sessions, mcap ≥ 5,000 Cr, ADV ≥ 25 Cr → 134 of 674 scanned; 11 held with < 3 sessions; 38 pending (reaction 16-Nov). YoY from screener Sep-26 vs Sep-25 quarter columns.
- **Follow-ups (`data.json → followups`).** SOUTHBANK OHLC 19-Oct→13-Nov from the bhavcopy, with stop/T1/T2 comparisons only (Muhurat bar shown separately). Watchlist (PNB, HCLTECH, TANLA): condition facts from Yahoo charts, NSE closes, quoteSummary consensus and Setup-C data.
- **Cross-checks.** NSE vs Yahoo price; screener vs Yahoo PE/PB/mcap/ROE. 137 gaps > 3% in `cross_checks.flagged_gt_3pct`, each with a `screen_impact` note. Source B would flip a filter for GLENMARK (PE), HCLTECH (PE), SUNPHARMA (PE), PVRINOX (PE), AIIL (ROE), ZENTEC, ASAHIINDIA, GAIL, KRBL (ROE), ACE (PE), ASTERDM (PB). Preference order: NSE/BSE > screener > others.
- **Forward PE.** Primary: 13-Nov close / Yahoo forwardEps. Second source: stockanalysis rebased.

## Gaps (also in `data.json → gaps`)

- **EV/EBITDA 5-year average** N/A for cyclicals (ADANIPOWER, MRPL, GESHIP, PETRONET, GAIL, SHYAMMETL, NUVOCO).
- **Setup-C reaction pending** for 38 names filed after the 13-Nov close (incl. ABB, EICHERMOT, TMPV, ASHOKLEY, KAYNES, PATANJALI, INOXWIND, GODREJIND, JUBLPHARMA, FIRSTCRY). Reaction session 16-Nov is live and excluded.
- **Setup-C filing timestamp not found** for GRSE, TARC, TATASTEEL, TITAGARH, PARKHOSPS, BAGMANE: reaction assumed as the session after the board meeting. BAGMANE has no Yahoo bars.
- **Saturday 7-Nov results** (FINCABLES, TATASTEEL): first traded in the uncounted Muhurat session, so the 9-Nov open-vs-6-Nov-close move includes the Muhurat move (FINCABLES +20% upper circuit on 8-Nov, then -5% on 9-Nov per ET).
- **Peer PB/ROE medians** fetched only for main/near-miss/financials/watchlist/Track-B-financial subjects (138 peer pages). Other subjects use already-fetched peers; n is recorded per subject. 115 BSE-only peer pages are not rescaled.
- **Industry median** missing for ADANIENSOL and INDIGO.
- **Bulk deals 30-Oct→12-Nov** partial (70-row API cap); block deals complete.
- **NSE financial-results API** returned empty again.
- **Promoter pledge N/A (no promoter group, not a fail):** BSE, COFORGE, CUB, DELHIVERY, ETERNAL, FEDERALBNK, ICICIBANK, INDGN, ITC, KTKBANK, LT, MCX, NORTHARC, PAYTM, SOUTHBANK, TMB.
- **Bank metrics:** LICHSGFIN (HFC, Stage 3 only) and AIIL (investment NBFC) have NNPA/CAR N/A.
- **Conflicts recorded:** SOUTHBANK CAR 19.40% (ICICI Direct / call) vs MarketsMojo 15.95%; ZYDUSLIFE filing 12:19 (NSE, used) vs 19:34 (Strota); GLENMARK revenue YoY -29.8% (company) vs +78.7% (MOFSL table, different base); ADANIPOWER pledge: third-party 1.81% vs NSE XBRL value in `data.json`.
- **Yahoo epsTrend 0.0 placeholders** for 7 names (incl. PNB): revision % N/A for those periods; consensus EPS taken from earningsEstimate.avg.

## Files

- `data.json`: all structured data (compact JSON, 5.5 MB). Leaves are {value, source_url, as_of, method, notes?}. Same top-level keys as the 26-Oct run.
- `news.md`: 122 items across 33 sections (market, SOUTHBANK, watchlist, main/financials passes and top Setup-C names).
- `data_sources.md`: this file.
- `raw/`: Python scripts plus small JSON.
  - `raw/web_facts.json` (built from `raw/web_facts_candidates.json`) holds the web-sourced facts.
  - `raw/computed/` holds the small computed JSONs (indices, sectors, summary, screen_result, pledge, trackb_value, forward_pe_sa, watchlist_status, southbank_followup).
- **Bulky intermediates kept out of the repo** (copy back to `raw/computed/` to re-run `assemble_outputs.py`):
  - In `/tmp/run1116/computed/`: the large computed JSONs (see `raw/computed/MOVED.txt`).
  - In `/tmp/run1116/`: raw HTML, charts, XBRL, PDFs and bhavcopies (charts/, qs/, screener/, industries/, bhav_ext/, pdf/, misc/).

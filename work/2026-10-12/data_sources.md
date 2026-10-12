# Data sources — run 2026-10-12 (IST), data session Fri 2026-10-09

- **DATA_MODE:** WEB
- **MCP_ERROR:** screener / screener-core MCP namespaces are absent from the tool catalog in this environment. The GetDynamicTools full catalog lists only cursor, Cursor Automation Tools, cursor-cloud and cursor-subscriptions, and the pattern 'screener' returned 0 matches. No MCP was authenticated, per run rules.
- **Session check:** 2026-10-09 was a trading day. It is the last bar in the NSE bhavcopy and in all 499 Yahoo series; the next session is 2026-10-12, where Yahoo's live bars were excluded.
- **Results-season window:** 15 NSE trading days counted from 12 Oct (day 1), excluding Dussehra on 20 Oct, ending **Mon 2026-11-02**.

## Sources that worked

| Source | URL / endpoint | Used for | HTTP | Notes |
|---|---|---|---|---|
| Yahoo v8 chart | query1.finance.yahoo.com/v8/finance/chart/{SYM}.NS?range=1y&interval=1d | OHLCV for 499 Nifty 500 names plus indices, Brent and USDINR; all technicals computed in Python | 200 (528/532) | Needs a Windows Chrome UA; a Linux UA got 429. IST date = ts + 19800. 404s: ^CNXSMALLCAP, ^CNXMIDCAP, BAGMANE.NS, DUMMYHEG.NS (not in the universe calc). |
| Yahoo v10 quoteSummary | query1.finance.yahoo.com/v10/finance/quoteSummary/{SYM}.NS | forwardEps, trailingEps, bookValue, analyst targets and trend, earningsTrend (EPS revisions), EV/EBITDA, earnings dates | 200 (27 names) | Needs cookie + crumb (fc.yahoo.com, then /v1/test/getcrumb). Prices are LIVE for 12 Oct, so forward PE was recomputed at the 9 Oct close. |
| NSE bhavcopy | nsearchives.nseindia.com/products/content/sec_bhavdata_full_DDMMYYYY.csv (20 sessions, 10 Sep to 9 Oct) | Official close, delivery %, 20-day ADV | 200 | Yahoo vs NSE close: max gap 0.0% across all 499 names. |
| NSE index closes | nsearchives.nseindia.com/content/indices/ind_close_all_DDMMYYYY.csv (09102026, 01102026, 08092026, 10072026) | Sector 1W/1M/3M returns, RS vs Nifty 500, official index PE/PB | 200 | Nifty 500 close 21,866.65 matches Yahoo ^CRSLDX. |
| NSE APIs (cookie from www.nseindia.com + Referer) | api/reportASM, api/reportGSM, api/holiday-master?type=trading, api/corporate-board-meetings?index=equities&from_date=&to_date=, api/event-calendar, api/corporates-corporateActions, api/fiidiiTradeReact, api/allIndices, api/corporate-share-holdings-master?symbol= | Surveillance, holidays, board meetings, corporate actions, FII/DII, pledge (SHP XBRL) | 200 | Only previousClose was used from allIndices, since it is a live 12 Oct snapshot. |
| NSE SHP XBRL | nsearchives.nseindia.com/corporate/xbrl/SHP_*.xml | Promoter pledge % = NumberOfSharesEncumberedUnderPledged / NumberOfShares (ShareholdingOfPromoterAndPromoterGroup_ContextI) | 200 (72 files) | Mostly as of 30-Jun-2026; some 30-Sep-2026. |
| NSE F&O ban | nsearchives.nseindia.com/content/fo/fo_secban.csv | Ban for trade date 12-Oct-2026 | 200 | AMBUJACEM, BANDHANBNK, LICHSGFIN. |
| NSE bulk / block | nsearchives.nseindia.com/content/equities/bulk.csv, block.csv | Latest day (9 Oct) deals | 200 | No technical-pass names; block file empty. |
| screener.in company pages | www.screener.in/company/{SYM}/consolidated/ (standalone fallback) | Mcap, PE, BV, ROE, ROCE, CAGRs, OCF, borrowings/equity (D/E), shareholding | 200 (391/393) | Consolidated pages that were empty shells were re-fetched as standalone: CASTROLIND, CUB, KARURVYSYA, LGEINDIA, TEGA. GVT&D and M&MFIN gave 404 because of HTML escaping; re-fetched with %26. |
| screener.in industry pages | www.screener.in/market/INxx/.../ (all pages, 25 rows/page, mcap-desc) | Industry PE (top-25 median = primary; all-pages = secondary); peer sets for PB/ROE medians | 200 (134 pages, 44 industries) | Page-2+ filenames needed `rstrip("_")`. |
| Web search (cursor WebSearch) | see news.md | News, breadth cross-checks, RBI/Fed calendar, results dates, bank asset quality and CAR, pledge cross-check | n/a | Treated as unverified third-party content. |

## Sources that failed or were blocked (max 2 attempts each)

| Source | Result | Substitution |
|---|---|---|
| screener / screener-core MCP | Namespace absent | WEB mode: screener HTML pages |
| NSE api/quote-equity, NSE homepage HTML | 403 | Bhavcopy for price and delivery; cookie still obtained for the other APIs |
| NSE indicesHistory / historical bulk- and block-deal APIs | HTML block page | ind_close_all CSVs; latest-day bulk.csv / block.csv only |
| NSE pledge API | Empty response | SHP XBRL via corporate-share-holdings-master |
| NSE ASM_LT.csv / GSM.csv archives | 404 | api/reportASM and api/reportGSM (200) |
| fundtrackerindia.com via curl | 403 (Cloudflare) | Read via WebFetch/WebSearch snippet (REDINGTON MF data only) |
| Yahoo sector tickers (Auto, Metal, FMCG, Energy, Realty, Media, PSU Bank, etc.) | Single bar only | NSE ind_close_all for sector returns |
| Yahoo ^NSMIDCP | Returns Nifty Next 50 (68,166.7) | Relabelled; Midcap from NIFTYMIDCAP150.NS and NSE CSV |

## Method notes

- **Indicators:** SMA, EMA20, Wilder RSI14, Wilder ATR14, and the 200-DMA 20-session change and slope, all computed from Yahoo daily bars up to 2026-10-09.
- **Technical rules:**
  - Rule A is the literal query: close > SMA50 > SMA200 and close > 0.75 × 52-week high.
  - Rule B also passes names with SMA50 ≤ SMA200 if the 200-DMA is rising over 20 sessions. These are flagged.
- **Breadth:** % of the 499 Nifty 500 names above their 20/50/200-DMA. Cross-checked against Punji, IndexBreadth and Flash Finance.
- **Industry PE:** median of positive PE values. Primary = top 25 by mcap (page 1). Secondary = all pages.
- **Sub-sector PB/ROE medians (new):** peers are the top 12 by mcap on screener industry page 1, excluding the subject. PB = price ÷ book value, or mcap ÷ (equity + reserves) when Book Value is blank. Peer lists, n and medians are in data.json `sub_sector_medians`.
- **Financials variant:** PB < peer-median PB (fallback PB < 3), ROE > 12, PE > 0, mcap > 12,000, technical pass. D/E ignored. For banks, D/E is borrowings ÷ equity and excludes deposits.
- **Forward PE:** 9 Oct close ÷ Yahoo forwardEps. PE on FY27E and FY28E consensus EPS is shown as an alternate. No independent second source.
- **Cross-checks:** price (NSE vs Yahoo), PE, PB, mcap, 52-week high, DMA50/200. Gaps above 3%: PE for CYIENT, MRPL, REDINGTON and IPCALAB (EPS basis differs), and CYIENT mcap. Screener is kept for these because NSE has no value for them.

## Files

- `data.json`: all structured fields as {value, source_url, as_of, method, notes}.
- `news.md`: news tables per candidate plus market news.
- `raw/*.py`: fetch_yahoo, compute_indicators, fetch_screener, parse_screener, parse_industries, pledge_xbrl, peer_medians, screen, sectors, bhav, parse_quotesummary, assemble_outputs, build_news.
- `raw/computed/*.json`: small computed artifacts. `tech.json` has no bars (bars are in data.json candidates). `industry_medians.json` keeps page-1 peers only.
- `raw/news_notes_source.md`: raw news notes.
- Not committed (in /tmp/swing-2026-10-12/): charts, screener HTML, industry HTML, quoteSummary JSON, bhavcopies, XBRL, full tech/industry JSON.

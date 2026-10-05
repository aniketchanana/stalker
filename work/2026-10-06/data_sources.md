# Data sources log — 2026-10-06 swing research (WEB mode)

DATA_MODE: WEB  
MCP_ERROR: screener / screener-core MCP namespaces absent from available dynamic tools; GetDynamicTools pattern 'screener' returned no matches.

Run date (IST): **2026-10-06** (Tuesday)  
Last completed NSE session used: **2026-10-05** (Monday) — confirmed trading day, not a holiday.  
Oct 2 2026 (Gandhi Jayanti) appears as a null/holiday bar on Yahoo; skipped in indicator math.

## Last session confirmation

| Source | HTTP | Value | As-of on page/API |
|---|---|---|---|
| Yahoo `^NSEI` chart + `regularMarketPrice` | 200 | Nifty 50 **22555.75** | last daily bar 2026-10-05 (IST tz) |
| The Hindu BusinessLine | 200 (search/fetch) | 22,555.75 (+133.80, +0.60%) | 05 Oct 2026 close / updated 16:48 |
| India Today | search | same 22,555.75 | 05 Oct 2026 15:55 IST |
| Bajaj Broking closing bell | fetch | same; Bank Nifty +0.48% | 05 Oct 2026 |
| Yahoo `^CRSLDX` | 200 | Nifty 500 **21971.6** | 2026-10-05 |
| Team Genus sectoral watch | search snippet | NIFTY 500 21971.6 | 05 Oct 2026 16:00:00 |
| Yahoo `^INDIAVIX` | 200 | **14.775** | 2026-10-05 |
| HDFC Sky | search | VIX 14.71 (prior 14.46) | 05 Oct 2026 — 0.44% below Yahoo |

## MCP / screener tools

- Catalog namespaces: `cursor`, `Cursor Automation Tools`, `cursor-cloud`, `cursor-subscriptions` only.
- `GetDynamicTools` pattern `screener` returned no matches. **Did not authenticate MCP.**
- Screener.in **raw screen URL**: fetched via WebFetch — login/register wall, **no result table**. Query could not be run on-site.

## What worked

| Source | HTTP | Used for |
|---|---|---|
| Yahoo v8 chart `query1.finance.yahoo.com` 1d/1y | 200 | OHLCV + computed EMA20/SMA20/50/200, Wilder RSI14/ATR14, 21d/63d returns, 20d ADV, last-20 volume. Last bar `close` often null — filled from `regularMarketPrice` + day high/low. |
| Yahoo `^NSEI` `^CRSLDX` `^INDIAVIX` `^NSEBANK` `^CNXIT` `^CNXPHARMA` `^NSEMDCP50` | 200 with ~252 bars | Index technicals (Nifty 500 via **^CRSLDX**) |
| Yahoo single-name `{SYM}.NS` for 499/501 Nifty 500 | 200 | Breadth proxy + technical screen |
| Yahoo quoteSummary v10 + crumb cookie | 200 after crumb | PE/PB/forward PE/52w high/mcap cross-check. Crumb from `/v1/test/getcrumb` after `fc.yahoo.com` (fc itself 404 but sets cookies). |
| niftyindices.com `ind_nifty500list.csv` | 200 | 501 rows (Company, Industry, Symbol, Series, ISIN). Also 200 from nsearchives + archives mirrors (same file). |
| niftyindices `ind_nifty50list.csv`, `ind_niftybanklist.csv` | 200 | Nifty 50 / Bank lists |
| nsearchives `ind_niftyfinancelist.csv` | 200 | Nifty Financial Services constituents |
| screener.in `/company/{SYM}/consolidated/` | 200 (~140–250 KB HTML) | Top ratios, P&L/BS/CF, CAGRs, SHP, industry path, upcoming result dates |
| screener.in `/company/{SYM}/` standalone | 200 | CUB, CASTROLIND, PAGEIND, SCHNEIDER, LGEINDIA, ENRIN (consolidated top-ratios were empty JS shells) |
| screener.in `/market/...` industry pages | 200 (51 industries) | Peer CMP/PE/mcap tables → **documented median PE** |
| nsearchives `fo_secban.csv` | 200 | F&O ban for trade date **06-Oct-2026**: AMBUJACEM, BANDHANBNK, SAIL |
| Flash Finance sectors + FII/DII pages | 200 (WebFetch) | Sector 1M/3M as of 2026-10-05; FII/DII 5 Oct |
| Trendlyne shareholding pages | 200 (WebFetch/search) | Promoter pledge Jun 2026 |
| Exchange circulars aggregators | search | Incremental ASM/GSM circulars (not full lists) |

## What failed (max 2 attempts then moved on)

| Source | HTTP / result | Fallback |
|---|---|---|
| NSE homepage + cookie handshake | **403** (AKA_A2 only) | No `quote-equity` / `allIndices` / delivery |
| NSE ASM report CSVs (several URL guesses) | **404** HTML | Incremental circulars only |
| NSE GSM CSVs | **404** | Sep 4 2026 circular additions only |
| Yahoo `NIFTY_500.NS` `^CNX500` | 404 / empty | **^CRSLDX** used |
| Yahoo `NIFTY_BANK.NS` `NIFTY_IT.NS` `^CNXFINANCE` `^CNXMIDCAP` `^CNXSMALLCAP` | 404 | Use `^NSEBANK` `^CNXIT`; finance 1M/3M from Flash Finance |
| Yahoo `^CNXAUTO` `^CNXMETAL` `^CNXFMCG` `^CNXENERGY` `^CNXREALTY` `^CNXINFRA` `^CNXMEDIA` `^CNXPSUBANK` `^CNXCONSUM` `^CNXCMDT` `^CNXSERVICE` `^CNXFIN` `NIFTY_MID_SELECT.NS` | 200 but **n=1 bar** (latest close only) | 1M/3M from Flash Finance 5 Oct table |
| Yahoo v7 quote | **401** | chart + quoteSummary |
| Yahoo quoteSummary without crumb | **401** Invalid Crumb | cookie+crumb retry succeeded |
| Tickertape `api.tickertape.in` | 401/404 | unused |
| Trendlyne equity HTML guessed path | 404 | specific shareholding URLs worked |
| Screener raw screen | login wall | rebuilt screen |
| Screener company peers table | JS placeholder “Loading peers table” | industry `/market/` pages instead |
| WebFetch niftyindices CSV URL | 500 | curl 200 |
| craytheon.com sector page | Cloudflare challenge | Flash Finance + Yahoo |

## Proxy substitutions (do not treat as official)

1. **Nifty 500 level/history:** Yahoo `^CRSLDX` (CNX 500 / Nifty 500). Cross-checked last close vs Team Genus.
2. **Breadth:** Official published figure is ICICI Direct **16% of NSE500 above 50-DMA as of week ending 1 Oct** (Nifty 22,422). **Computed proxy 5 Oct:** 95/499 = **19.04%** of Nifty 500 constituents with a 50-DMA from Yahoo. Nifty 50 proxy: **4/50** (ADANIPORTS, COALINDIA, DRREDDY, KOTAKBANK).
3. **Industry PE:** Median of **positive P/E cells** on screener industry pages (peer list stored in `raw/computed/industry_medians.json`). Not Screener’s unpublished “Industry PE” widget. AEGISLOG industry n_pe=1 — excluded from pass.
4. **D/E:** Latest annual `Borrowings / (Equity Capital + Reserves)` from screener balance sheet (not Yahoo’s percent D/E, which is noted as cross-check).
5. **Sector 1M/3M vs Nifty 500:** Yahoo 21d/63d for Bank/IT/Pharma; Flash Finance for other official NSE sector indices (as-of 2026-10-05). Nifty 500 1M **−5.3878%**, 3M **−6.2403%** (Yahoo 21d/63d).
6. **Private-bank sector PB:** Official median N/A. Documented sample median **1.913** from 8 parsed bank pages (list in `data.json` `universe_screen_financials`).
7. **Last Yahoo daily close null:** filled from `regularMarketPrice` (matches exchange print for Nifty/VIX/names checked).

## Screen reconstruction (because MCP screen unavailable)

1. Download Nifty 500 CSV (501 names).
2. Yahoo 1y daily → require close > SMA50 > SMA200 and close > 0.75 × 52w high → **80** names.
3. Screener company pages for those 80 + sanity/extra banks (**91** HTML files).
4. Industry median PE from 51 industry pages.
5. Pledge from Trendlyne/Smart-investing (Jun 2026 SHP unless noted).
6. Primary pass with confirmed pledge < 20: **WELCORP, CHENNPETRO, REDINGTON, GESHIP, SCI, PETRONET, IPCALAB, EMCURE, ABSLAMC** (9). KPIL would pass except pledge **24.55%**.

## Deep-dive coverage

18 names in `data.json` `candidates` (9 primary + CUB bank + near-misses/quality).  
Sanity: RELIANCE, TCS, HDFCBANK (none pass the primary screen).

Fields filled from fetch/compute for deep dives: price, mcap, sector, PE, industry median PE, PB, forward PE, ROE, D/E, TTM EPS, OCF, 3y CAGRs, pledge (where found), ADV, 52w high, EMA20/50/200/slope, RSI, ATR, last-20 volume, 3m return, FII/DII, some result dates, CUB GNPA/NNPA/CAR.  
**N/A:** delivery %, full ASM/GSM membership, 5y EV/EBITDA, industry median PB/ROE, live consensus counts (except two broker notes), bulk/block deals.

## Intermediate artifacts (not required outputs)

`/workspace/work/2026-10-06/raw/` — Yahoo charts, screener HTML, industry HTML, quoteSummary JSON, CSVs.  
`/workspace/work/2026-10-06/raw/computed/` — `tech.json`, `indices.json`, `summary.json`, `screener_fundamentals.json`, `industry_medians.json`, `quotesummary.json`, `screen_result.json`.

## Required outputs

1. `/workspace/work/2026-10-06/data.json`
2. `/workspace/work/2026-10-06/news.md`
3. `/workspace/work/2026-10-06/data_sources.md` (this file)

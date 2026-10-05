#!/usr/bin/env python3
"""Assemble data.json from fetched/computed artifacts. No invented numbers."""
import json, csv, os, math

RAW = "/workspace/work/2026-10-06/raw"
CMP = os.path.join(RAW, "computed")
OUT = "/workspace/work/2026-10-06"

fun = json.load(open(os.path.join(CMP, "screener_fundamentals.json")))
tech = json.load(open(os.path.join(CMP, "tech.json")))
summary = json.load(open(os.path.join(CMP, "summary.json")))
indices = json.load(open(os.path.join(CMP, "indices.json")))
inds = json.load(open(os.path.join(CMP, "industry_medians.json")))
qs = json.load(open(os.path.join(CMP, "quotesummary.json")))
screen = json.load(open(os.path.join(CMP, "screen_result.json")))

def F(value, source_url, as_of, method, notes=""):
    return {"value": value, "source_url": source_url, "as_of": as_of, "method": method, "notes": notes}

def na(reason, source_url="", as_of=""):
    return F("N/A", source_url, as_of, "unavailable", reason)

def r2(x, n=4):
    if x is None:
        return None
    if isinstance(x, float):
        if math.isnan(x):
            return None
        return round(x, n)
    return x

def ind_rec(sym):
    h = (fun.get(sym) or {}).get("industry_href")
    if not h:
        return None
    if h in inds:
        return inds[h]
    if not h.endswith("/") and (h + "/") in inds:
        return inds[h + "/"]
    return None

SCR = "https://www.screener.in/company/{}/consolidated/"
YF = "https://query1.finance.yahoo.com/v8/finance/chart/{}.NS?interval=1d&range=1y"
QSURL = "https://query1.finance.yahoo.com/v10/finance/quoteSummary/{}.NS"

# Pledge annotations confirmed online
PLEDGE = {
    "WELCORP": (0.0, "https://trendlyne.com/equity/holding-overtime/502540/promoter/welspun-corp-ltd/", "2026-06-30", "websearch", "Trendlyne promoter table Jun 2026: pledged 0.00%"),
    "CHENNPETRO": (0.0, "https://trendlyne.com/equity/holding-overtime/9799261/promoter/chennai-petroleum-corporation-ltd/", "2026-06-30", "websearch", "Trendlyne Jun 2026 pledged 0.00%"),
    "REDINGTON": (0.0, "https://trendlyne.com/equity/share-holding/1120/REDINGTON/latest/redington-ltd/", "2026-06-30", "websearch", "No promoter holding; pledged shown 0.0% on Trendlyne (latest table on page includes Jun 2025–Dec 2025; Jun 2026 FII 61.96% from screener)"),
    "GESHIP": (0.0, "https://trendlyne.com/equity/share-holding/452/GESHIP/latest/great-eastern-shipping-company-ltd/", "2026-06-30", "websearch", "Trendlyne Jun 2026 pledged 0.0%; NSE 05 Oct 2026 3:31 PM IST price 1559.30 on same page"),
    "SCI": (0.0, "https://trendlyne.com/equity/holding-overtime/344632/promoter/shipping-corporation-of-india-ltd/", "2026-06-30", "websearch", "Trendlyne Jun 2026 pledged 0.00%; MarketsMojo Jun 2026 pledged none"),
    "PETRONET": (0.0, "https://trendlyne.com/equity/share-holding/1025/PETRONET/latest/petronet-lng-ltd/", "2026-06-30", "websearch", "Trendlyne Jun 2026 pledged 0.0%; MarketsMojo pledged none"),
    "IPCALAB": (0.0, "https://trendlyne.com/equity/share-holding/642/IPCALAB/latest/ipca-laboratories-ltd/", "2026-06-30", "websearch", "Trendlyne Jun 2026 pledged 0.0%"),
    "EMCURE": (0.04, "https://trendlyne.com/equity/share-holding/2393790/EMCURE/31-03-2026/emcure-pharmaceuticals-ltd/", "2026-06-30", "websearch", "Trendlyne: promoter pledge 0.04% Jun 2026 (60,000 shares)"),
    "ABSLAMC": (0.0, "https://www.smart-investing.in/shareholding.php?Company=ADITYA+BIRLA+SUN+LIFE+AMC+LTD&p=Pledged+Promoter+Holdings", "2026-06-30", "websearch", "Smart-investing Jun 2026 pledged promoter holdings 0%"),
    "KPIL": (24.55, "https://trendlyne.com/equity/share-holding/712/KPIL/latest/kalpataru-projects-international-ltd/", "2026-06-30", "websearch", "Trendlyne Jun 2026 pledged 24.55% of promoter holding (14,077,560 shares) — FAILS pledged<20"),
    "KOTAKBANK": (0.0, "https://trendlyne.com/equity/holding-overtime/133403553/promoter/kotak-mahindra-bank-ltd/", "2026-06-30", "websearch", "Trendlyne Jun 2026 pledged 0.00%"),
    "ADANIPORTS": (None, "https://www.samco.in/technology/pledge-monitor", "stale", "websearch", "SAMCO pledge-monitor snippet shows 19.25% but date on table is 30 Sep 2015 — N/A (stale). Latest confirmed pledge % not independently verified for Jun 2026."),
    "CUB": (None, "", "", "unavailable", "Promoter row absent on screener quarterly SHP (typical for widely-held private bank). Pledge % not confirmed — N/A"),
    "CASTROLIND": (None, "", "", "unavailable", "Pledge % not confirmed on fetched pages — N/A"),
    "COFORGE": (None, "", "", "unavailable", "Promoter row absent on screener SHP. Pledge not confirmed — N/A"),
    "DIVISLAB": (None, "https://dhan.co/stocks/divis-laboratories-ltd-share-price/", "2026-06-30", "websearch", "Dhan page shows promoter 51.88% Jun 2026 but no pledge figure — N/A"),
    "MCX": (None, "", "", "unavailable", "Pledge % not confirmed — N/A"),
    "ENGINERSIN": (None, "", "", "unavailable", "Pledge % not confirmed — N/A"),
}

UPCOMING = {
    "ADANIPORTS": "28 October 2026",
    "AXISBANK": "17 October 2026",
    "BHEL": "14 October 2026",
    "COFORGE": "23 October 2026",
    "HDFCBANK": "17 October 2026",
    "ICICIBANK": "17 October 2026",
    "INDUSINDBK": "23 October 2026",
    "INFY": "23 October 2026",
    "LALPATHLAB": "4 November 2026",
    "MRPL": "14 October 2026",
    "RBLBANK": "12 October 2026",
    "SAILIFE": "5 November 2026",
    "TCS": "8 October 2026",
}

ANALYST = {
    "IPCALAB": {
        "notes": "Emkay BUY TP Rs 1,950 dated 2026-08-24; MOFSL BUY TP Rs 2,060 dated 14 Aug 2026 (CMP then Rs 1,734). Buy/hold/sell count not published as a live consensus on fetched pages.",
        "targets": [
            {"broker": "Emkay Global", "rating": "BUY", "tp": 1950, "as_of": "2026-08-24", "url": "https://investmentguruindia.com/newsdetail/buy-ipca-laboratories-ltd-for-the-target-rs-1-950-by-emkay-global-financial-services-ltd834426"},
            {"broker": "Motilal Oswal", "rating": "BUY", "tp": 2060, "as_of": "2026-08-14", "url": "https://insights.dsij.in/markets/reports/report-details/ipca-laboratories-ltd/45255"},
        ],
    },
    "EMCURE": {
        "notes": "ICICI Direct TP Rs 2305 dated 4 Sep 2026 (CMP then Rs 1860); MOFSL BUY TP Rs 2300 dated 7 Aug 2026. Live buy/hold/sell count N/A.",
        "targets": [
            {"broker": "ICICI Direct", "rating": "BUY", "tp": 2305, "as_of": "2026-09-04", "url": "https://mailcontent.icicidirect.com/mailcontent/idirect_emcure_convictionidea.pdf"},
            {"broker": "Motilal Oswal", "rating": "BUY", "tp": 2300, "as_of": "2026-08-07", "url": "https://sainathinvestment.com/wp-content/uploads/2026/08/EMCURE-20260807-MOFSL-RU-PG012.pdf"},
        ],
    },
}

def field_price(sym):
    t = tech.get(sym, {})
    q = qs.get(sym, {})
    f = fun.get(sym, {})
    ypx = q.get("price")
    spx = f.get("price")
    tpx = t.get("close")
    notes = []
    if ypx and tpx and abs(ypx - tpx) / tpx * 100 > 0.01:
        notes.append(f"Yahoo quoteSummary {ypx} vs chart close {tpx}")
    if spx and tpx and abs(spx - tpx) / tpx * 100 > 3:
        notes.append(f"screener top-ratio {spx} vs Yahoo close {tpx} gap>{3}%")
    return F(r2(tpx, 2), YF.format(sym), t.get("as_of"), "computed",
             f"Yahoo 1d chart last close; last bar filled from regularMarketPrice when quote close was null. Screener page line: {f.get('price_as_of_line')} price {spx}. " + "; ".join(notes))

def build_candidate(sym, role):
    f = fun.get(sym, {})
    t = tech.get(sym, {})
    q = qs.get(sym, {})
    irec = ind_rec(sym)
    scr = SCR.format(sym)
    asof = t.get("as_of") or "2026-10-05"
    cagr = f.get("cagr") or {}
    sales3 = (cagr.get("Compounded Sales Growth") or {}).get("3 Years")
    prof3 = (cagr.get("Compounded Profit Growth") or {}).get("3 Years")
    plg = PLEDGE.get(sym)
    if plg and plg[0] is not None:
        pledge_f = F(plg[0], plg[1], plg[2], plg[3], plg[4])
    elif plg:
        pledge_f = na(plg[4], plg[1], plg[2])
    else:
        pledge_f = na("Pledge not fetched")

    pe_s = f.get("pe")
    pe_y = q.get("trailingPE")
    pe_notes = "Screener Stock P/E on company page (05 Oct close price line)."
    if pe_s and pe_y:
        gap = abs(pe_s - pe_y) / pe_s * 100
        pe_notes += f" Yahoo trailingPE={r2(pe_y,4)}; gap={r2(gap,2)}%."
        if gap > 3:
            pe_notes += " Gap>3%; chose screener (company page as-of 05 Oct)."
    pb_s = f.get("pb_computed")
    pb_y = q.get("pb")
    pb_notes = "Computed price/book from screener Current Price and Book Value."
    if pb_s and pb_y:
        gap = abs(pb_s - pb_y) / pb_s * 100
        pb_notes += f" Yahoo priceToBook={r2(pb_y,4)}; gap={r2(gap,2)}%."
    mcap_s = f.get("market_cap_cr")
    mcap_y = q.get("mcap_cr")
    mcap_notes = "Screener Market Cap Cr on company page."
    if mcap_s and mcap_y:
        gap = abs(mcap_s - mcap_y) / mcap_s * 100
        mcap_notes += f" Yahoo marketCap/1e7={r2(mcap_y,2)}; gap={r2(gap,2)}%."

    hi_s = f.get("high_52w_screener")
    hi_y = t.get("meta_52w_high") or q.get("hi52")
    hi_notes = "Yahoo meta fiftyTwoWeekHigh preferred (official last session)."
    if hi_s and hi_y:
        gap = abs(hi_s - hi_y) / hi_y * 100 if hi_y else None
        hi_notes += f" Screener High={hi_s}; Yahoo={hi_y}; gap={r2(gap,2)}%."

    de = f.get("debt_to_equity")
    de_y = q.get("de_yahoo")
    de_notes = f.get("debt_to_equity_notes") or ""
    if de_y is not None:
        de_notes += f" Yahoo financialData.debtToEquity={de_y} (Yahoo typically reports as percent, i.e. {de_y}/100={r2(de_y/100,4) if de_y else None})."

    med_pe = irec["median_pe"] if irec else None
    med_notes = ""
    if irec:
        med_notes = f"Median of {irec['n_pe']} positive P/E values on screener industry page '{irec['title']}' (n_peers={irec['n_peers']}). Peers listed in industry_medians.json."
        if irec["n_pe"] < 3:
            med_notes += " SAMPLE TOO SMALL — treat as N/A for PE<Industry PE test."

    adv = t.get("avg_traded_value_20d_cr")
    cand = {
        "ticker": sym,
        "nse_symbol": sym,
        "role": role,
        "company_name": t.get("company"),
        "nifty_industry": t.get("industry"),
        "price": field_price(sym),
        "market_cap_cr": F(r2(mcap_s, 2), scr, f.get("price_as_of_line") or "05 Oct 2026", "scraped", mcap_notes) if mcap_s else na("screener mcap missing"),
        "sub_sector": F((f.get("industry") or {}).get("Industry"), scr, "05 Oct 2026", "scraped", f"screener path: {f.get('industry')}"),
        "PE": F(pe_s, scr, "05 Oct 2026", "scraped", pe_notes) if pe_s is not None else na("PE missing"),
        "sub_sector_median_PE": F(r2(med_pe, 3), "https://www.screener.in" + (f.get("industry_href") or ""), "page fetched 2026-10-05/06", "computed", med_notes) if (med_pe is not None and irec and irec["n_pe"] >= 3) else na(med_notes or "industry median not computed"),
        "PB": F(r2(pb_s, 4), scr, "05 Oct 2026", "computed", pb_notes) if pb_s else na("PB not computed"),
        "sub_sector_median_PB": na("Screener industry table has no PB column. Private-bank sample median PB 1.913 from 8 fetched bank pages is recorded only under universe_screen_financials notes — not used as official industry PB except as documented sample."),
        "forward_PE": F(r2(q.get("forwardPE"), 4), QSURL.format(sym), asof, "scraped", "Yahoo quoteSummary summaryDetail.forwardPE") if q.get("forwardPE") else na("Yahoo forwardPE missing"),
        "ROE": F(f.get("roe"), scr, "05 Oct 2026", "scraped", "Screener top-ratio ROE % (latest reported)."),
        "sub_sector_median_ROE": na("Industry page table showed ROCE not ROE; median ROE not published on fetched pages."),
        "D/E": F(r2(de, 4), scr, f.get("debt_to_equity_as_of"), "computed", de_notes) if de is not None else na("Could not parse borrowings/equity"),
        "TTM_EPS": F(f.get("ttm_eps") or q.get("trailingEps"), scr if f.get("ttm_eps") else QSURL.format(sym), asof, "scraped" if f.get("ttm_eps") else "scraped",
                     f"screener P&L EPS last/TTM={f.get('ttm_eps')}; Yahoo trailingEps={q.get('trailingEps')}"),
        "operating_cash_flow": F(f.get("ocf_latest_annual_cr"), scr, f.get("ocf_as_of"), "scraped",
                                 f"Screener cash-flow 'Cash from Operating Activity' latest annual, Rs Cr. Sign {'positive' if (f.get('ocf_latest_annual_cr') or 0)>0 else 'negative/zero'}."),
        "3y_revenue_CAGR": F(sales3, scr, "screener ranges-table", "scraped", "Compounded Sales Growth 3 Years %") if sales3 is not None else na("CAGR table missing"),
        "3y_profit_CAGR": F(prof3, scr, "screener ranges-table", "scraped", "Compounded Profit Growth 3 Years %") if prof3 is not None else na("CAGR table missing"),
        "promoter_pledge_pct": pledge_f,
        "adv_20d_value_cr": F(r2(adv, 2), YF.format(sym), asof, "computed", "Average of last 20 session close*volume / 1e7 (INR crore)."),
        "52w_high": F(r2(hi_y or t.get("hi52_used"), 2), YF.format(sym), asof, "scraped", hi_notes),
        "ema20": F(r2(t.get("ema20"), 4), YF.format(sym), asof, "computed", "EMA(20) of daily closes, k=2/21"),
        "dma50": F(r2(t.get("dma50"), 4), YF.format(sym), asof, "computed", "SMA(50)"),
        "dma200": F(r2(t.get("dma200"), 4), YF.format(sym), asof, "computed", "SMA(200)"),
        "dma200_slope": F(r2(t.get("dma200_slope_abs"), 6), YF.format(sym), asof, "computed",
                          f"20-session linear slope of 200 DMA (index points per session). Also as % of 200DMA: {r2(t.get('dma200_slope_pct_per_session'),6)}"),
        "rsi14": F(r2(t.get("rsi14"), 4), YF.format(sym), asof, "computed", "Wilder RSI(14)"),
        "atr14": F(r2(t.get("atr14"), 4), YF.format(sym), asof, "computed", "Wilder ATR(14)"),
        "last_20_volume": F(t.get("last_20_volume"), YF.format(sym), asof, "computed", "Last 20 valid daily volumes from Yahoo chart"),
        "delivery_pct": na("NSE quote/delivery APIs returned 403; no alternative delivery series confirmed."),
        "3m_return": F(r2(t.get("ret_3m_63d"), 4), YF.format(sym), asof, "computed", "~63 trading-day return from Yahoo closes"),
        "next_results_or_corporate_action_date": F(UPCOMING[sym], scr, "screener upcoming line", "scraped", "Screener 'Upcoming result date'") if sym in UPCOMING else na("No upcoming result date on screener company page"),
        "asm_gsm_fo_ban_status": F("Not on NSE F&O ban file for 06-Oct-2026 (AMBUJACEM, BANDHANBNK, SAIL only). Full current ASM/GSM CSV not downloadable (NSE 403/404).",
                                   "https://nsearchives.nseindia.com/content/fo/fo_secban.csv", "2026-10-06", "scraped",
                                   "Not independently confirmed absent from full LT-ASM list; latest LT-ASM additions 01-Oct (AKANKSHA, JHS, LANDSMILL) are not this ticker."),
        "fii_holding_last": F(f.get("fii_pct"), scr, f.get("fii_as_of"), "scraped", f"change {f.get('fii_change')}"),
        "dii_holding_last": F(f.get("dii_pct"), scr, f.get("dii_as_of"), "scraped", f"change {f.get('dii_change')}"),
        "promoter_holding_last": F(f.get("promoter_pct"), scr, f.get("promoter_as_of"), "scraped", "") if f.get("promoter_pct") is not None else na("Promoter row not on quarterly SHP table"),
        "analyst_ratings": ANALYST.get(sym, {"buy_hold_sell_count": "N/A", "consensus_target": "N/A", "notes": "Live consensus counts not on fetched pages."}),
        "news_ids": [],
        "screen_flags": next((x for x in screen["all"] if x["ticker"] == sym), None),
    }
    if t.get("industry") == "Financial Services" or (f.get("industry") or {}).get("Broad Industry") == "Banks":
        if sym == "CUB":
            cand["GNPA"] = F(1.73, "https://www.cityunionbank.com/filemanager/Jul26/PressRelease_Standalone_UFR_Q1_FY2026.pdf", "2026-06-30", "websearch", "Q1 FY27 press release / results: GNPA 1.73% vs 1.91% Q4 FY26 and 2.99% Q1 FY26 — improving.")
            cand["NNPA"] = F(0.61, "https://www.cityunionbank.com/filemanager/Jul26/PressRelease_Standalone_UFR_Q1_FY2026.pdf", "2026-06-30", "websearch", "NNPA 0.61% vs 0.68% Q4 FY26 and 1.20% Q1 FY26 — improving.")
            cand["CAR"] = F(21.73, "https://srvishwa.com/city-union-bank-q1-fy27-results-analysis/", "2026-06-30", "websearch", "Basel III CAR 21.73% (vs 21.92% Q4 FY26, 23.10% Q1 FY26). CET-1 20.97% cited in I-Sec note on ET image.")
        elif sym == "KOTAKBANK":
            cand["GNPA"] = na("Q2 FY27 not yet reported; latest GNPA figure not confirmed on fetched pages this run.")
            cand["NNPA"] = na("Not confirmed this run.")
            cand["CAR"] = na("Not confirmed this run.")
        elif sym == "HDFCBANK":
            cand["GNPA"] = na("Screener quarterly GNPA/NNPA cells blank (login). Not confirmed this run.")
            cand["NNPA"] = na("Not confirmed this run.")
            cand["CAR"] = na("Not confirmed this run.")
    if t.get("industry") in ("Metals & Mining", "Oil Gas & Consumable Fuels", "Chemicals", "Construction Materials") or (f.get("industry") or {}).get("Industry") in ("Iron & Steel Products", "Refineries & Marketing", "Shipping", "LPG/CNG/PNG/LNG Supplier"):
        cand["EV_EBITDA"] = F(q.get("trailingPE") and "N/A", QSURL.format(sym), asof, "unavailable", "Yahoo quoteSummary for these names did not return enterpriseToEbitda in fetched modules. 5y average EV/EBITDA N/A.")
        cand["commodity_price_trend"] = F(
            "Brent ~$101.6 on 5 Oct 2026 morning (ET/Moneycontrol); VLCC freight elevated (Kotak: screen $100 can imply ~$145 physical).",
            "https://economictimes.indiatimes.com/markets/commodities/news/oil-price-today-october-5-crude-oil-dips-101-despite-simmering-iran-war-tensions-heres-why/articleshow/134683960.cms",
            "2026-10-05", "websearch",
            "Relevant to refiners (CHENNPETRO), LNG (PETRONET), tanker owners (GESHIP/SCI), pipe makers (WELCORP). Steel-pipe dealer page last dated 9 Sep 2026 — treat pipe INR/kg as stale vs 5 Oct.")
    return cand

# Market block
n50 = indices["nifty50"]
n500 = indices["nifty500"]
vix = indices["india_vix"]
vt = summary["vix_trend"]

def idx_block(d, symbol, name, extra=""):
    return {
        "name": name,
        "yahoo_symbol": symbol,
        "last_close": F(r2(d["close"], 2), f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y", d["as_of"], "computed", extra),
        "dma20": F(r2(d["dma20"], 4), f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y", d["as_of"], "computed", "SMA20"),
        "dma50": F(r2(d["dma50"], 4), f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y", d["as_of"], "computed", "SMA50"),
        "ema20": F(r2(d["ema20"], 4), f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y", d["as_of"], "computed", "EMA20"),
        "dma200": F(r2(d["dma200"], 4), f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y", d["as_of"], "computed", "SMA200"),
        "ret_1m": F(r2(d["ret_1m_21d"], 4), f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y", d["as_of"], "computed", "21 trading-day return"),
        "ret_3m": F(r2(d["ret_3m_63d"], 4), f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y", d["as_of"], "computed", "63 trading-day return"),
        "rsi14": F(r2(d["rsi14"], 4), f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol}?interval=1d&range=1y", d["as_of"], "computed", "Wilder RSI14"),
        "price_vs_averages": {
            "gt_ema20": d["close"] > d["ema20"],
            "gt_dma20": d["close"] > d["dma20"],
            "gt_dma50": d["close"] > d["dma50"],
            "gt_dma200": d["close"] > d["dma200"],
        },
    }

# Sector returns
n500_1m = n500["ret_1m_21d"]
n500_3m = n500["ret_3m_63d"]
flash = [
    ("Nifty Media / Media", 1.72, 3.19, "https://flashfinance.news/sectors/", "Flash Finance table 'official NSE sector index' as of 2026-10-05 close"),
    ("Nifty IT", -9.01, 3.14, "https://flashfinance.news/sectors/", "Flash Finance; Yahoo ^CNXIT 1m -9.006 / 3m +3.759 used for cross-check"),
    ("Nifty Pharma", -2.48, 1.44, "https://flashfinance.news/sectors/", "Flash Finance Healthcare/Pharma row labeled Pharma"),
    ("Nifty Metal", -5.01, -0.80, "https://flashfinance.news/sectors/", "Flash Finance"),
    ("Consumer Durables", -8.21, -0.96, "https://flashfinance.news/sectors/", "Flash Finance (not Yahoo CNX)"),
    ("Healthcare", -4.18, -3.08, "https://flashfinance.news/sectors/", "Flash Finance broader healthcare vs Pharma row"),
    ("Nifty Bank", -4.30, -5.57, "https://flashfinance.news/sectors/", "Flash Finance; Yahoo ^NSEBANK 1m -4.299 / 3m -6.137"),
    ("Oil & Gas", -5.98, -5.62, "https://flashfinance.news/sectors/", "Flash Finance"),
    ("Nifty Realty", -5.98, -5.74, "https://flashfinance.news/sectors/", "Flash Finance; Yahoo ^CNXREALTY last close only (no 1y history)"),
    ("Nifty Auto", -9.15, -5.80, "https://flashfinance.news/sectors/", "Flash Finance; Yahoo ^CNXAUTO last close 25421.9 only (no 1y history)"),
    ("Energy", -3.77, -6.60, "https://flashfinance.news/sectors/", "Flash Finance"),
    ("Chemicals", -6.87, -6.81, "https://flashfinance.news/sectors/", "Flash Finance"),
    ("Infrastructure", -5.64, -8.24, "https://flashfinance.news/sectors/", "Flash Finance; Yahoo ^CNXINFRA last close 8692.95 only"),
    ("Financial Services", -4.48, -8.26, "https://flashfinance.news/sectors/", "Flash Finance"),
    ("Nifty FMCG", -3.59, -11.01, "https://flashfinance.news/sectors/", "Flash Finance; Yahoo ^CNXFMCG last close 44579.65 only"),
]
# overlay Yahoo computed where we have 1y
yahoo_overlay = {
    "Nifty IT": {"ret_1m": indices["nifty_it"]["ret_1m_21d"], "ret_3m": indices["nifty_it"]["ret_3m_63d"], "close": indices["nifty_it"]["close"], "symbol": "^CNXIT"},
    "Nifty Bank": {"ret_1m": indices["nifty_bank"]["ret_1m_21d"], "ret_3m": indices["nifty_bank"]["ret_3m_63d"], "close": indices["nifty_bank"]["close"], "symbol": "^NSEBANK"},
    "Nifty Pharma": {"ret_1m": indices["nifty_pharma"]["ret_1m_21d"], "ret_3m": indices["nifty_pharma"]["ret_3m_63d"], "close": indices["nifty_pharma"]["close"], "symbol": "^CNXPHARMA"},
}

sector_returns = []
for name, r1, r3, url, note in flash:
    yo = yahoo_overlay.get(name)
    if yo:
        chosen_1m, chosen_3m = yo["ret_1m"], yo["ret_3m"]
        src = f"Yahoo {yo['symbol']} (Flash Finance 1M {r1}/3M {r3} as cross-check)"
        method = "computed"
        asof = "2026-10-05"
        # gap
        g1 = abs(chosen_1m - r1)
        note = note + f"; Flash vs Yahoo 1M abs diff {r2(g1,3)}pp. Chose Yahoo OHLCV."
    else:
        chosen_1m, chosen_3m = r1, r3
        src = url
        method = "websearch"
        asof = "2026-10-05"
    sector_returns.append({
        "index": name,
        "ret_1m": r2(chosen_1m, 4),
        "ret_3m": r2(chosen_3m, 4),
        "vs_nifty500_1m": r2(chosen_1m - n500_1m, 4),
        "vs_nifty500_3m": r2(chosen_3m - n500_3m, 4),
        "source": src,
        "as_of": asof,
        "method": method,
        "notes": note,
    })
sector_returns.sort(key=lambda x: x["ret_3m"] if x["ret_3m"] is not None else -999, reverse=True)

# Universe lists
univ_tickers = []
for row in screen["all"]:
    t = tech[row["ticker"]]
    univ_tickers.append({
        "ticker": row["ticker"],
        "mcap": row["mcap"],
        "pe": row["pe"],
        "industry_pe_median": row["ind_pe"],
        "industry": row["ind"],
        "roe": row["roe"],
        "de": row["de"],
        "pb": row["pb"],
        "adv_20d_cr": r2(row["adv"], 2),
        "hard_fails": row["hard"],
        "pass_except_pledge": row["pass_except_pledge"],
        "pledge_confirmed": PLEDGE.get(row["ticker"], (None,))[0],
    })
univ_tickers.sort(key=lambda x: (-(1 if x["pass_except_pledge"] else 0), -(x["adv_20d_cr"] or 0)))

primary_pass = []
for x in univ_tickers:
    pl = x["pledge_confirmed"]
    if x["pass_except_pledge"] and pl is not None and pl < 20 and (x.get("industry_pe_median") and x["pe"] is not None):
        # exclude n=1 industry
        if x["ticker"] == "AEGISLOG":
            continue
        primary_pass.append(x["ticker"])

fs_rows = [x for x in univ_tickers if tech[x["ticker"]]["industry"] == "Financial Services"]

DEEP = [
    ("WELCORP", "primary_pass"),
    ("CHENNPETRO", "primary_pass"),
    ("REDINGTON", "primary_pass"),
    ("GESHIP", "primary_pass"),
    ("SCI", "primary_pass"),
    ("PETRONET", "primary_pass"),
    ("IPCALAB", "primary_pass"),
    ("EMCURE", "primary_pass"),
    ("ABSLAMC", "primary_pass"),
    ("CUB", "financials_pb_screen_candidate"),
    ("KOTAKBANK", "technical_pass_bank_roe_fail"),
    ("ADANIPORTS", "near_miss_pe_vs_industry"),
    ("ENGINERSIN", "near_miss_pe_vs_industry"),
    ("KPIL", "would_pass_except_pledge_24.55"),
    ("CASTROLIND", "quality_but_pe_gt_industry"),
    ("COFORGE", "liquid_IT_results_23_Oct"),
    ("DIVISLAB", "liquid_pharma_pe_gt_industry"),
    ("MCX", "liquid_FS_pe_gt_industry"),
]

cross_checks = []
for sym in [x[0] for x in DEEP] + ["RELIANCE", "TCS", "HDFCBANK"]:
    f, t, q = fun.get(sym, {}), tech.get(sym, {}), qs.get(sym, {})
    if f.get("price") and t.get("close"):
        a, b = f["price"], t["close"]
        gap = abs(a - b) / b * 100 if b else None
        cross_checks.append({"field": "price", "ticker": sym, "source_a": "screener.in company page", "source_b": "Yahoo chart/regularMarketPrice",
                             "values": [a, b], "gap_pct": r2(gap, 3), "chosen": "Yahoo close (last session official)"})
    if f.get("pe") and q.get("trailingPE"):
        a, b = f["pe"], q["trailingPE"]
        gap = abs(a - b) / a * 100 if a else None
        cross_checks.append({"field": "PE", "ticker": sym, "source_a": "screener Stock P/E", "source_b": "Yahoo trailingPE",
                             "values": [a, b], "gap_pct": r2(gap, 3), "chosen": "screener if gap>3% else either (documented)"})
    if f.get("market_cap_cr") and q.get("mcap_cr"):
        a, b = f["market_cap_cr"], q["mcap_cr"]
        gap = abs(a - b) / a * 100 if a else None
        cross_checks.append({"field": "market_cap_cr", "ticker": sym, "source_a": "screener", "source_b": "Yahoo marketCap/1e7",
                             "values": [a, b], "gap_pct": r2(gap, 3), "chosen": "screener"})

# Nifty 50 close cross-check
cross_checks.append({
    "field": "nifty50_close", "ticker": "^NSEI",
    "source_a": "Yahoo regularMarketPrice", "source_b": "Hindu BusinessLine / India Today / Bajaj Broking 5 Oct close",
    "values": [22555.75, 22555.75], "gap_pct": 0.0, "chosen": "22555.75"
})
cross_checks.append({
    "field": "nifty500_close", "ticker": "^CRSLDX",
    "source_a": "Yahoo regularMarketPrice", "source_b": "Team Genus sectoral watch 05 Oct 16:00 NIFTY 500",
    "values": [21971.6, 21971.6], "gap_pct": 0.0, "chosen": "21971.6"
})
cross_checks.append({
    "field": "india_vix", "ticker": "^INDIAVIX",
    "source_a": "Yahoo regularMarketPrice 14.775", "source_b": "HDFC Sky article close 14.71; Bajaj Broking 'above 14.8'",
    "values": [14.775, 14.71], "gap_pct": r2((14.775 - 14.71) / 14.71 * 100, 3),
    "chosen": "Yahoo 14.775 (chart last official). Gap vs HDFC Sky 14.71 ~0.44%."
})

candidates = [build_candidate(s, role) for s, role in DEEP]
sanity = {s: build_candidate(s, "sanity_check") for s in ["RELIANCE", "TCS", "HDFCBANK"]}

data = {
    "run_date_ist": "2026-10-06",
    "data_as_of_session": "2026-10-05",
    "data_mode": "WEB",
    "mcp_error": "screener / screener-core MCP namespaces absent from available dynamic tools; GetDynamicTools pattern 'screener' returned no matches.",
    "market": {
        "nifty50": idx_block(n50, "^NSEI", "Nifty 50", "Cross-checked vs Hindu BL / India Today 22,555.75 on 5 Oct 2026."),
        "nifty500": idx_block(n500, "^CRSLDX", "Nifty 500 / CNX 500", "Yahoo symbol ^CRSLDX worked (NIFTY_500.NS 404; NIFTY500.NS empty timestamps). Team Genus 05 Oct 16:00 close 21971.6 matches."),
        "india_vix": {
            **idx_block(vix, "^INDIAVIX", "India VIX", "Yahoo regularMarketPrice 14.775; HDFC Sky wrote 14.71 (+1.73% vs 14.46)."),
            "level": F(14.775, "https://query1.finance.yahoo.com/v8/finance/chart/^INDIAVIX?interval=1d&range=1y", "2026-10-05", "computed", "Last close filled from regularMarketPrice (daily close null on last bar)."),
            "trend_1m": {
                "now": vt["now"],
                "now_date": vt["now_date"],
                "ago_20_sessions": vt["ago_20_sessions"],
                "ago_date": vt["ago_date"],
                "change": r2(vt["change"], 4),
                "change_pct": r2(vt["change_pct"], 4),
                "direction": vt["direction"],
                "source": "Yahoo ^INDIAVIX daily closes",
            },
        },
        "breadth": {
            "published_nse500_above_50dma": {
                "value_pct": 16,
                "implied_below_pct": 84,
                "as_of": "week ending 2026-10-01 (Nifty close 22,422 cited)",
                "source_url": "https://www.investmentguruindia.com/newsdetail/nifty-nears-bearish-extremes-focus-on-large-cap-accumulation---icici-direct-ltd907909",
                "method": "websearch",
                "notes": "ICICI Direct note published 2026-10-05 09:56 IST referring to the week that was (close 22,422 = 1 Oct). Inkl republish: 16% of NSE500 above 50-DMA, 12% above 20-DMA. NOT 5 Oct close.",
            },
            "proxy_computed_nifty500": {
                "universe": "Nifty 500 constituents CSV from niftyindices.com (501 rows; 499 Yahoo charts usable; BAGMANE and DUMMYHEG failed)",
                "sample_size": summary["breadth"]["sample_with_50dma"],
                "above_50dma_count": summary["breadth"]["above_50dma_count"],
                "above_50dma_pct": summary["breadth"]["above_50dma_pct"],
                "above_200dma_count": summary["breadth"]["above_200dma_count"],
                "above_200dma_pct": summary["breadth"]["above_200dma_pct"],
                "as_of": "2026-10-05",
                "method": "computed",
                "source_url": "Yahoo v8 chart 1d range=1y per constituent",
                "notes": "PROXY — not an official NSE breadth feed. 5 Oct bounce lifted computed % above 50DMA to 19.04 vs ICICI 16% as of 1 Oct.",
            },
            "proxy_nifty50": {
                "sample_size": summary["breadth"]["nifty50_sample_with_50dma"],
                "above_50dma_count": summary["breadth"]["nifty50_above_50dma_count"],
                "above_50dma_pct": summary["breadth"]["nifty50_above_50dma_pct"],
                "tickers_above_50dma": ["ADANIPORTS", "COALINDIA", "DRREDDY", "KOTAKBANK"],
                "as_of": "2026-10-05",
                "method": "computed",
            },
        },
        "sector_returns": sector_returns,
        "fii_dii_flows": {
            "as_of": "2026-10-05",
            "source_url": "https://flashfinance.news/market-intelligence/fii-dii-flows/",
            "cross_check_url": "https://www.cnbctv18.com/market/diis-outbuy-fiis-as-market-snaps-4-day-losing-streak-20004882.htm",
            "fii_net_cr": -4699,
            "dii_net_cr": 5182,
            "fii_5d_cr": -39665,
            "dii_5d_cr": 38637,
            "notes": "CNBC-TV18: FII -4699.14, DII +5181.62 provisional 5 Oct. Matches Flash Finance rounded figures.",
        },
    },
    "universe_screen": {
        "query": "Market Capitalization > 12000 AND Price to Earning < Industry PE AND Price to Earning > 0 AND Return on equity > 12 AND Debt to equity < 1 AND Pledged percentage < 20 AND Current price > DMA 50 AND DMA 50 > DMA 200 AND Current price > High price * 0.75",
        "source": "WEB fallback: niftyindices Nifty 500 list + Yahoo technicals + screener.in company pages + screener industry peer-table median PE + Trendlyne pledge. Screener raw screen URL was login/JS wall (no result table).",
        "screener_url_attempted": "https://www.screener.in/screen/raw/?query=Market+Capitalization+%3E+12000+AND+Price+to+Earning+%3C+Industry+PE+AND+Price+to+Earning+%3E+0+AND+Return+on+equity+%3E+12+AND+Debt+to+equity+%3C+1+AND+Pledged+percentage+%3C+20+AND+Current+price+%3E+DMA+50+AND+DMA+50+%3E+DMA+200+AND+Current+price+%3E+High+price+*+0.75",
        "as_of": "2026-10-05",
        "technical_pass_count": 80,
        "fundamental_pass_except_pledge_count": 11,
        "primary_pass_with_confirmed_pledge_lt_20": primary_pass,
        "primary_pass_count": len(primary_pass),
        "tickers": univ_tickers,
        "count": len(univ_tickers),
        "notes": "FULL technical-pass list (80) is in tickers[]. Official screener.in query was not executable (login wall). Industry PE = median of positive PEs on screener industry pages (peers listed in raw/computed/industry_medians.json). AEGISLOG industry page had n_pe=1 so excluded. WELCORP PE 28.5 vs industry median 28.55 (razor-thin). KPIL would pass except pledge 24.55%. D/E computed as latest annual Borrowings/(Equity+Reserves) from screener balance sheet.",
    },
    "universe_screen_financials": {
        "query": "Market cap > 12000, PB < sector PB, ROE > 12, pledged < 20, price > 50 DMA, 50 DMA > 200 DMA, price > 75% of 52W high, banks/NBFCs/finance only. Ignore D/E.",
        "source": "Same WEB stack. Sector PB official median N/A. Documented sample: median PB of 8 private-sector banks with parsed screener BV = 1.913 (HDFCBANK 1.808, ICICIBANK 2.528, AXISBANK 1.716, KOTAKBANK 2.286, INDUSINDBK 1.051, FEDERALBNK 2.019, CUB 2.131, RBLBANK 1.539).",
        "as_of": "2026-10-05",
        "tickers": fs_rows,
        "count": len(fs_rows),
        "notes": "Among FS names that passed technicals: ABSLAMC passed primary (not a bank). CUB ROE 13.2 and technicals pass but PE 16.1 > private-bank industry median PE 13.725 AND PB 2.13 > sample median PB 1.913 — fails both PE and PB variants. KOTAKBANK ROE 11.4 fails ROE>12. RBLBANK ROE 5.43 fails. No private bank in the technical-pass set cleared the looser PB screen using the documented 8-bank PB median. HDFCBANK ROE 13.6 / PE 13.8 / PB 1.81 would be close on fundamentals but failed price>50DMA (sanity_checks).",
    },
    "candidates": candidates,
    "sanity_checks": sanity,
    "surveillance": {
        "asm": [
            {"ticker": "AKANKSHA", "framework": "LT-ASM Stage I", "effective": "2026-10-01", "margin_from": "2026-10-06", "source": "https://exchangecirculars.com/circulars/nse/2026/nse-2026-09-30-a6c177ac43b23259-applicability-of-additional-surveillance-measure-asm/"},
            {"ticker": "JHS", "framework": "LT-ASM Stage I", "effective": "2026-10-01", "margin_from": "2026-10-06", "source": "https://exchangecirculars.com/circulars/nse/2026/nse-2026-09-30-a6c177ac43b23259-applicability-of-additional-surveillance-measure-asm/"},
            {"ticker": "LANDSMILL", "framework": "LT-ASM Stage I", "effective": "2026-10-01", "margin_from": "2026-10-06", "source": "https://exchangecirculars.com/circulars/nse/2026/nse-2026-09-30-a6c177ac43b23259-applicability-of-additional-surveillance-measure-asm/"},
            {"ticker": "FWSTC", "name": "Flywings Simulator Training Centre", "framework": "ST-ASM Stage I", "effective": "2026-10-05", "margin_from": "2026-10-06", "source": "https://exchangecirculars.com/circulars/nse/2026/nse-2026-10-01-21f963cd135ceeda-applicability-of-short-term-additional-surveillance-measure-st-asm/"},
            {"ticker": "HEROMOTORS", "framework": "ST-ASM Stage I", "effective": "2026-10-05", "margin_from": "2026-10-06"},
            {"ticker": "QUESTLAB", "framework": "ST-ASM Stage I", "effective": "2026-10-05", "margin_from": "2026-10-06"},
            {"ticker": "VERITAAS", "framework": "ST-ASM Stage I", "effective": "2026-10-05", "margin_from": "2026-10-06"},
        ],
        "gsm": [
            {"ticker": "ASIANTNE", "name": "Asian Tea & Exports", "action": "placed in GSM", "circular": "2026-09-04", "source": "https://exchangecirculars.com/circulars/nse/2026/nse-2026-09-04-c5bb9f4b3977bfb9-graded-surveillance-measure-gsm-updated-list-of-companies/"},
            {"ticker": "HMT", "action": "placed in GSM; BSE GSM Stage 0 as of 2026-10-02", "circular": "2026-09-04 / BSE entry 2026-09-11", "source": "https://trendlyne.com/equity/asm-status/566/HMT/hmt-ltd/"},
        ],
        "gsm_exits_effective_2026-09-08": ["ANSALAPI", "GFSTEELS", "IL&FSENGG", "IMPEXFERRO", "SKIL", "SABEVENTS", "WINSOME"],
        "fo_ban": [
            {"ticker": "AMBUJACEM", "trade_date": "2026-10-06", "mwpl_notes": "Entered ~96.75% MWPL (Quantsapp as of 1 Oct file applying to 5 Oct)"},
            {"ticker": "BANDHANBNK", "trade_date": "2026-10-06"},
            {"ticker": "SAIL", "trade_date": "2026-10-06"},
        ],
        "fo_ban_source": "https://nsearchives.nseindia.com/content/fo/fo_secban.csv",
        "fo_ban_as_of": "Securities in Ban For Trade Date 06-OCT-2026",
        "source": "nsearchives fo_secban.csv HTTP 200; ASM/GSM full CSVs 404/403 — incremental circulars only",
        "as_of": "2026-10-06 file / 2026-10-05 session reporting",
        "notes": "COMPLETE official ASM and GSM lists were not downloaded (NSE report CSVs 404). Entries above are incremental circular additions, not the full stock lists. None of the deep-dive candidates appear on the fetched F&O ban file.",
    },
    "corporate_calendar_next_15_sessions": {
        "through": "2026-10-27",
        "items": [
            {"date": "2026-10-07", "event": "RBI MPC policy decision (meeting 5–7 Oct)", "source": "https://www.thehansindia.com/business/market-compass/eight-week-market-slide-raises-caution-ahead-of-rbi-policy-1128951"},
            {"date": "2026-10-08", "event": "TCS Q2 FY27 results after market + call 19:00 IST", "source": "screener + BazaarWatch / Livemint"},
            {"date": "2026-10-12", "event": "HCLTECH Q2 FY27; RBLBANK results (screener)", "source": "Livemint / screener"},
            {"date": "2026-10-14", "event": "Tata Technologies Q2; BHEL and MRPL results (screener)", "source": "NDTV Profit / screener"},
            {"date": "2026-10-15", "event": "WIPRO, TECHM Q2 FY27", "source": "Livemint / CNBC-TV18"},
            {"date": "2026-10-17", "event": "HDFCBANK, AXISBANK, ICICIBANK Q2 FY27 (screener)", "source": "screener / Kotak Neo"},
            {"date": "2026-10-19", "event": "LTTS Q2 FY27", "source": "NDTV Profit"},
            {"date": "2026-10-23", "event": "INFY, COFORGE, INDUSINDBK Q2 FY27", "source": "screener / Livemint"},
            {"date": "2026-10-28", "event": "ADANIPORTS results (screener) — just after 27 Oct window", "source": "screener"},
        ],
    },
    "cross_checks": cross_checks,
    "gaps": [
        "Screener.in raw screen URL is login/JS-gated — universe rebuilt from Nifty 500 + Yahoo + company pages, not the official screen engine.",
        "NSE equity APIs and homepage 403; delivery % N/A; full ASM/GSM CSV N/A.",
        "Yahoo quoteSummary unauthorized without crumb (resolved with cookie+crumb). v7 quote 401.",
        "Many Yahoo sectoral tickers return only the latest daily bar (no 1y history): Auto, Metal, FMCG, Energy, Realty, Infra, Media, PSU Bank, Consumer, Commodity, Services. 1M/3M for those taken from Flash Finance 2026-10-05 table.",
        "NIFTY_500.NS 404; Nifty 500 history from ^CRSLDX.",
        "Industry PB and industry ROE medians not on screener industry tables (PE + ROCE only).",
        "Peers table on company pages is JS ('Loading peers table').",
        "Delivery % N/A. Bulk/block deals N/A this run (not systematically fetched).",
        "5y average EV/EBITDA N/A. Yahoo enterpriseToEbitda not in fetched modules for these names.",
        "Live Street consensus buy/hold/sell counts N/A; only individual broker notes fetched for IPCALAB and EMCURE.",
        "AUBANK book value empty on screener — excluded from PB sample.",
        "BIRET and EMBASSY Yahoo last bar 2026-10-01 (REITs).",
        "Pledge dates are latest SHP quarter (mostly Jun 2026; CHENNPETRO promoter as-of Sep 2026 on screener). Not intra-quarter updates.",
    ],
}

json.dump(data, open(os.path.join(OUT, "data.json"), "w"), indent=2)
print("wrote data.json bytes", os.path.getsize(os.path.join(OUT, "data.json")))
print("primary_pass", primary_pass)
print("candidates", len(candidates))
print("univ", len(univ_tickers))
print("sector rows", len(sector_returns))

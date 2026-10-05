#!/usr/bin/env python3
"""Compute technicals from Yahoo 1d charts. No invented values."""
import csv, json, math, os, glob, datetime
from statistics import median

RAW = "/workspace/work/2026-10-06/raw"
CHARTS = os.path.join(RAW, "charts")
OUT = os.path.join(RAW, "computed")
os.makedirs(OUT, exist_ok=True)

def ema(values, span):
    k = 2.0 / (span + 1.0)
    e = values[0]
    out = [e]
    for v in values[1:]:
        e = v * k + e * (1 - k)
        out.append(e)
    return out

def sma(values, n):
    out = [None] * len(values)
    s = 0.0
    for i, v in enumerate(values):
        s += v
        if i >= n:
            s -= values[i - n]
        if i >= n - 1:
            out[i] = s / n
    return out

def wilder_rsi(closes, n=14):
    if len(closes) < n + 1:
        return [None] * len(closes)
    out = [None] * len(closes)
    gains = []
    losses = []
    for i in range(1, len(closes)):
        d = closes[i] - closes[i - 1]
        gains.append(max(d, 0.0))
        losses.append(max(-d, 0.0))
    avg_g = sum(gains[:n]) / n
    avg_l = sum(losses[:n]) / n
    # RSI at index n (after n deltas, which is close index n)
    if avg_l == 0:
        out[n] = 100.0
    else:
        rs = avg_g / avg_l
        out[n] = 100.0 - (100.0 / (1.0 + rs))
    for i in range(n, len(gains)):
        avg_g = (avg_g * (n - 1) + gains[i]) / n
        avg_l = (avg_l * (n - 1) + losses[i]) / n
        if avg_l == 0:
            out[i + 1] = 100.0
        else:
            rs = avg_g / avg_l
            out[i + 1] = 100.0 - (100.0 / (1.0 + rs))
    return out

def wilder_atr(highs, lows, closes, n=14):
    if len(closes) < n + 1:
        return [None] * len(closes)
    trs = [None]
    for i in range(1, len(closes)):
        tr = max(highs[i] - lows[i], abs(highs[i] - closes[i - 1]), abs(lows[i] - closes[i - 1]))
        trs.append(tr)
    out = [None] * len(closes)
    # first ATR at index n
    out[n] = sum(trs[1 : n + 1]) / n
    for i in range(n + 1, len(closes)):
        out[i] = (out[i - 1] * (n - 1) + trs[i]) / n
    return out

def lin_slope(ys):
    n = len(ys)
    if n < 2:
        return None
    xs = list(range(n))
    mx = (n - 1) / 2.0
    my = sum(ys) / n
    num = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    den = sum((x - mx) ** 2 for x in xs)
    if den == 0:
        return None
    return num / den

def parse_chart(path, fill_last_from_meta=True):
    d = json.load(open(path))
    r = (d.get("chart") or {}).get("result")
    if not r:
        return None
    r = r[0]
    meta = r.get("meta") or {}
    ts = r.get("timestamp") or []
    q = (r.get("indicators") or {}).get("quote") or [{}]
    q = q[0]
    opens, highs, lows, closes, vols = q.get("open") or [], q.get("high") or [], q.get("low") or [], q.get("close") or [], q.get("volume") or []
    rows = []
    for i, t in enumerate(ts):
        o = opens[i] if i < len(opens) else None
        h = highs[i] if i < len(highs) else None
        l = lows[i] if i < len(lows) else None
        c = closes[i] if i < len(closes) else None
        v = vols[i] if i < len(vols) else None
        # skip empty holiday bars
        if c is None and h is None:
            continue
        if c is None and fill_last_from_meta and i == len(ts) - 1:
            c = meta.get("regularMarketPrice")
            if h is None:
                h = meta.get("regularMarketDayHigh") or c
            if l is None:
                l = meta.get("regularMarketDayLow") or c
            if o is None:
                o = c
            if v is None:
                v = meta.get("regularMarketVolume") or 0
        if c is None:
            continue
        dt = datetime.datetime.fromtimestamp(t, datetime.timezone.utc).date().isoformat()
        rows.append({
            "date": dt,
            "open": o,
            "high": h if h is not None else c,
            "low": l if l is not None else c,
            "close": float(c),
            "volume": float(v or 0),
        })
    if not rows:
        return None
    return {"meta": meta, "rows": rows}

def compute_from_rows(rows, meta=None):
    closes = [x["close"] for x in rows]
    highs = [x["high"] for x in rows]
    lows = [x["low"] for x in rows]
    vols = [x["volume"] for x in rows]
    n = len(closes)
    if n < 30:
        return None
    ema20 = ema(closes, 20)
    sma20 = sma(closes, 20)
    sma50 = sma(closes, 50)
    sma200 = sma(closes, 200) if n >= 200 else [None] * n
    rsi = wilder_rsi(closes, 14)
    atr = wilder_atr(highs, lows, closes, 14)
    last = n - 1
    dma200_vals = [x for x in sma200 if x is not None]
    slope = None
    slope_pct = None
    if len(dma200_vals) >= 20:
        last20 = dma200_vals[-20:]
        slope = lin_slope(last20)
        if slope is not None and last20[-1]:
            slope_pct = (slope / last20[-1]) * 100.0  # pts per session as % of 200DMA
    # 52w high from series (1y chart) and meta
    series_high = max(highs)
    meta_high = None
    if meta:
        meta_high = meta.get("fiftyTwoWeekHigh")
    hi52 = meta_high if meta_high else series_high
    last_c = closes[last]
    pct_below_52w = None
    if hi52:
        pct_below_52w = (hi52 - last_c) / hi52 * 100.0
    # returns
    def ret(days):
        if n <= days:
            return None
        prev = closes[last - days]
        if not prev:
            return None
        return (last_c / prev - 1.0) * 100.0
    # 20d avg volume and traded value
    last20 = rows[-20:]
    avg_vol20 = sum(x["volume"] for x in last20) / len(last20)
    avg_val20 = sum(x["close"] * x["volume"] for x in last20) / len(last20)
    last20_vol = [x["volume"] for x in last20]
    return {
        "as_of": rows[last]["date"],
        "n_bars": n,
        "close": last_c,
        "ema20": ema20[last],
        "dma20": sma20[last],
        "dma50": sma50[last],
        "dma200": sma200[last],
        "dma200_slope_abs": slope,
        "dma200_slope_pct_per_session": slope_pct,
        "rsi14": rsi[last],
        "atr14": atr[last],
        "ret_1m_21d": ret(21),
        "ret_1m_20d": ret(20),
        "ret_3m_63d": ret(63),
        "series_52w_high": series_high,
        "meta_52w_high": meta_high,
        "hi52_used": hi52,
        "pct_below_52w": pct_below_52w,
        "avg_vol_20d": avg_vol20,
        "avg_traded_value_20d": avg_val20,
        "last_20_volume": last20_vol,
        "price_gt_dma50": (sma50[last] is not None) and (last_c > sma50[last]),
        "dma50_gt_dma200": (sma50[last] is not None and sma200[last] is not None) and (sma50[last] > sma200[last]),
        "price_gt_75pct_52w": (hi52 is not None) and (last_c > hi52 * 0.75),
    }

def load_universe():
    rows = list(csv.DictReader(open(os.path.join(RAW, "csv_www.niftyindices.com_ind_nifty500list.csv"))))
    return {r["Symbol"].strip(): r for r in rows}

def main():
    univ = load_universe()
    tech = {}
    missing = []
    for sym, rec in univ.items():
        path = os.path.join(CHARTS, f"{sym}.json")
        if not os.path.exists(path):
            missing.append(sym)
            continue
        parsed = parse_chart(path)
        if not parsed:
            missing.append(sym)
            continue
        c = compute_from_rows(parsed["rows"], parsed["meta"])
        if not c:
            missing.append(sym)
            continue
        c["ticker"] = sym
        c["company"] = rec.get("Company Name")
        c["industry"] = rec.get("Industry")
        c["yahoo_symbol"] = parsed["meta"].get("symbol")
        c["yahoo_rmp"] = parsed["meta"].get("regularMarketPrice")
        tech[sym] = c

    # indices
    indices = {}
    for label, fname, ysym in [
        ("nifty50", os.path.join(RAW, "yf_NSEI.json"), "^NSEI"),
        ("nifty500", os.path.join(RAW, "yf_CRSLDX.json"), "^CRSLDX"),
        ("india_vix", os.path.join(RAW, "yf_INDIAVIX.json"), "^INDIAVIX"),
        ("nifty_bank", os.path.join(RAW, "yf_NSEBANK.json"), "^NSEBANK"),
        ("nifty_it", os.path.join(RAW, "yf_CNXIT.json"), "^CNXIT"),
        ("nifty_pharma", os.path.join(RAW, "yf_CNXPHARMA.json"), "^CNXPHARMA"),
        ("nifty_midcap50", os.path.join(RAW, "yf_NSEMDCP50.json"), "^NSEMDCP50"),
    ]:
        parsed = parse_chart(fname)
        if not parsed:
            indices[label] = {"error": "parse_failed", "file": fname}
            continue
        c = compute_from_rows(parsed["rows"], parsed["meta"])
        if c:
            c["yahoo_symbol"] = parsed["meta"].get("symbol")
            c["yahoo_rmp"] = parsed["meta"].get("regularMarketPrice")
            c["yahoo_name"] = parsed["meta"].get("shortName") or parsed["meta"].get("longName")
        indices[label] = c

    # VIX 20-session trend
    vix_parsed = parse_chart(os.path.join(RAW, "yf_INDIAVIX.json"))
    vix_trend = None
    if vix_parsed and len(vix_parsed["rows"]) >= 21:
        now = vix_parsed["rows"][-1]["close"]
        ago = vix_parsed["rows"][-21]["close"]
        vix_trend = {
            "now": now,
            "now_date": vix_parsed["rows"][-1]["date"],
            "ago_20_sessions": ago,
            "ago_date": vix_parsed["rows"][-21]["date"],
            "change": now - ago,
            "change_pct": (now / ago - 1) * 100 if ago else None,
            "direction": "up" if now > ago else ("down" if now < ago else "flat"),
        }

    # breadth
    n50 = set(r["Symbol"].strip() for r in csv.DictReader(open(os.path.join(RAW, "csv_www.niftyindices.com_ind_nifty50list.csv"))))
    above50_all = [s for s, c in tech.items() if c.get("dma50") is not None and c["close"] > c["dma50"]]
    below50_all = [s for s, c in tech.items() if c.get("dma50") is not None and c["close"] <= c["dma50"]]
    have50 = [s for s, c in tech.items() if c.get("dma50") is not None]
    above50_n50 = [s for s in n50 if s in tech and tech[s].get("dma50") is not None and tech[s]["close"] > tech[s]["dma50"]]
    have50_n50 = [s for s in n50 if s in tech and tech[s].get("dma50") is not None]
    above200_all = [s for s, c in tech.items() if c.get("dma200") is not None and c["close"] > c["dma200"]]
    have200 = [s for s, c in tech.items() if c.get("dma200") is not None]

    # technical screen (price > 50DMA > 200DMA, price > 75% of 52w)
    tech_pass = []
    for s, c in tech.items():
        if c.get("price_gt_dma50") and c.get("dma50_gt_dma200") and c.get("price_gt_75pct_52w"):
            tech_pass.append(s)

    banks_nbfc_ind = {"Financial Services"}
    tech_pass_fs = [s for s in tech_pass if tech.get(s, {}).get("industry") == "Financial Services"]

    summary = {
        "computed_count": len(tech),
        "missing_or_short": missing,
        "session_dates": sorted({c["as_of"] for c in tech.values()}),
        "breadth": {
            "universe": "Nifty 500 constituents from niftyindices CSV (501 rows)",
            "sample_with_50dma": len(have50),
            "above_50dma_count": len(above50_all),
            "above_50dma_pct": round(100.0 * len(above50_all) / len(have50), 2) if have50 else None,
            "above_200dma_count": len(above200_all),
            "above_200dma_pct": round(100.0 * len(above200_all) / len(have200), 2) if have200 else None,
            "nifty50_sample_with_50dma": len(have50_n50),
            "nifty50_above_50dma_count": len(above50_n50),
            "nifty50_above_50dma_pct": round(100.0 * len(above50_n50) / len(have50_n50), 2) if have50_n50 else None,
            "above_50dma_tickers": sorted(above50_all),
        },
        "vix_trend": vix_trend,
        "tech_pass_count": len(tech_pass),
        "tech_pass": sorted(tech_pass),
        "tech_pass_financial_services": sorted(tech_pass_fs),
    }
    # compact tech dump
    compact = {}
    for s, c in tech.items():
        compact[s] = {k: c[k] for k in c if k != "last_20_volume"}
        compact[s]["last_20_volume"] = c["last_20_volume"]
        compact[s]["avg_traded_value_20d_cr"] = (c["avg_traded_value_20d"] / 1e7) if c.get("avg_traded_value_20d") is not None else None

    json.dump(indices, open(os.path.join(OUT, "indices.json"), "w"), indent=2)
    json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), indent=2)
    json.dump(compact, open(os.path.join(OUT, "tech.json"), "w"), indent=2)
    print("computed", len(tech), "missing", len(missing))
    print("session dates", summary["session_dates"])
    print("breadth N500 above 50DMA", summary["breadth"]["above_50dma_count"], "/", summary["breadth"]["sample_with_50dma"], summary["breadth"]["above_50dma_pct"], "%")
    print("breadth N50 above 50DMA", summary["breadth"]["nifty50_above_50dma_count"], "/", summary["breadth"]["nifty50_sample_with_50dma"])
    print("tech pass", len(tech_pass))
    print("vix", vix_trend)
    for lab in ["nifty50", "nifty500", "india_vix", "nifty_bank", "nifty_it"]:
        ix = indices.get(lab) or {}
        print(lab, "close", ix.get("close"), "as_of", ix.get("as_of"), "dma20", ix.get("dma20"), "dma50", ix.get("dma50"), "ema20", ix.get("ema20"), "dma200", ix.get("dma200"), "1m", ix.get("ret_1m_21d"), "3m", ix.get("ret_3m_63d"))

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Compute technicals from Yahoo 1d charts. No invented values."""
import csv, json, math, os, glob, datetime
from statistics import median

RAW = "/workspace/work/2026-10-19/raw"
CHARTS = "/tmp/swing-2026-10-19/charts"
OUT = os.path.join(RAW, "computed")
SESSION = "2026-10-16"
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
        filled = False
        if c is None and fill_last_from_meta and i == len(ts) - 1:
            filled = True
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
        dt = datetime.datetime.fromtimestamp(t + 19800, datetime.timezone.utc).date().isoformat()
        if dt > SESSION:
            continue
        rows.append({
            "date": dt,
            "open": o,
            "high": h if h is not None else c,
            "low": l if l is not None else c,
            "close": float(c),
            "volume": float(v or 0),
            "close_filled_from_meta": filled,
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
    slope = slope_pct = slope_diff20 = None
    if len(dma200_vals) >= 21:
        last20 = dma200_vals[-20:]
        slope = lin_slope(last20)
        if slope is not None and last20[-1]:
            slope_pct = (slope / last20[-1]) * 100.0
        slope_diff20 = dma200_vals[-1] - dma200_vals[-21]
    dma50_vals = [x for x in sma50 if x is not None]
    dma50_diff20 = dma50_vals[-1] - dma50_vals[-21] if len(dma50_vals) >= 21 else None
    i_hi = max(range(n), key=lambda i: highs[i])
    series_high = highs[i_hi]
    series_high_date = rows[i_hi]["date"]
    i_lo = min(range(n), key=lambda i: lows[i])
    meta_high = meta.get("fiftyTwoWeekHigh") if meta else None
    hi52 = meta_high if meta_high else series_high
    last_c = closes[last]
    pct_below_52w = (hi52 - last_c) / hi52 * 100.0 if hi52 else None

    def ret(days):
        if n <= days or not closes[last - days]:
            return None
        return (last_c / closes[last - days] - 1.0) * 100.0

    last20 = rows[-20:]
    avg_vol20 = sum(x["volume"] for x in last20) / len(last20)
    avg_val20 = sum(x["close"] * x["volume"] for x in last20) / len(last20)
    p50 = sma50[last] is not None and last_c > sma50[last]
    s50_200 = sma50[last] is not None and sma200[last] is not None and sma50[last] > sma200[last]
    p75 = hi52 is not None and last_c > hi52 * 0.75
    rising200 = slope_diff20 is not None and slope_diff20 > 0
    rule_a = bool(p50 and s50_200 and p75)
    rule_b = bool(p50 and rising200 and p75 and not s50_200)
    bars = []
    for k, x in enumerate(rows[-20:]):
        j = n - 20 + k
        bars.append({"date": x["date"], "open": r(x["open"]), "high": r(x["high"]), "low": r(x["low"]), "close": r(x["close"]),
                     "volume": int(x["volume"]), "vol_vs_20d_avg": r(x["volume"] / avg_vol20 if avg_vol20 else None, 3),
                     "ema20": r(ema20[j]), "rsi14": r(rsi[j]), "close_filled_from_meta": x.get("close_filled_from_meta", False)})
    return {
        "as_of": rows[last]["date"],
        "n_bars": n,
        "close": last_c,
        "prev_close": closes[last - 1],
        "ema20": ema20[last],
        "dma20": sma20[last],
        "dma50": sma50[last],
        "dma200": sma200[last],
        "dma200_slope_abs": slope,
        "dma200_slope_pct_per_session": slope_pct,
        "dma200_change_20_sessions": slope_diff20,
        "dma50_change_20_sessions": dma50_diff20,
        "rsi14": rsi[last],
        "atr14": atr[last],
        "atr14_pct": atr[last] / last_c * 100 if atr[last] else None,
        "ret_1w_5d": ret(5),
        "ret_1m_21d": ret(21),
        "ret_1m_20d": ret(20),
        "ret_3m_63d": ret(63),
        "ret_6m_126d": ret(126),
        "series_52w_high": series_high,
        "series_52w_high_date": series_high_date,
        "series_52w_low": lows[i_lo],
        "series_52w_low_date": rows[i_lo]["date"],
        "meta_52w_high": meta_high,
        "meta_52w_low": meta.get("fiftyTwoWeekLow") if meta else None,
        "hi52_used": hi52,
        "pct_below_52w": pct_below_52w,
        "avg_vol_20d": avg_vol20,
        "avg_traded_value_20d": avg_val20,
        "last_close_filled_from_meta": rows[last].get("close_filled_from_meta", False),
        "price_gt_dma50": p50,
        "dma50_gt_dma200": s50_200,
        "dma200_rising_20s": rising200,
        "price_gt_75pct_52w": p75,
        "tech_rule_A_close_gt_50_gt_200_and_75pct52wH": rule_a,
        "tech_rule_B_close_gt_50_rising200_and_75pct52wH_only": rule_b,
        "tech_pass": rule_a or rule_b,
        "tech_rule": "A" if rule_a else ("B" if rule_b else None),
        "last_20_bars": bars,
    }


def r(x, n=2):
    return None if x is None else round(float(x), n)


def load_csv(name):
    return list(csv.DictReader(open(os.path.join(RAW, name))))


INDEX_FILES = [
    ("nifty50", "IDX_NSEI.json"), ("nifty500", "IDX_CRSLDX.json"), ("india_vix", "IDX_INDIAVIX.json"),
    ("nifty_bank", "IDX_NSEBANK.json"), ("nifty_it", "IDX_CNXIT.json"), ("nifty_pharma", "IDX_CNXPHARMA.json"),
    ("nifty_midcap50", "IDX_NSEMDCP50.json"), ("nifty_midcap150", "IDX_NIFTYMIDCAP150.NS.json"),
    ("nifty_midcap_nsmidcp", "IDX_NSMIDCP.json"), ("brent_BZ=F", "IDX_BZ_F.json"), ("usdinr", "IDX_USDINR_X.json"),
]


def main():
    univ = {r_["Symbol"].strip(): r_ for r_ in load_csv("ind_nifty500list.csv")}
    n50 = {r_["Symbol"].strip() for r_ in load_csv("ind_nifty50list.csv")}
    tech, missing = {}, []
    for sym, rec in univ.items():
        path = os.path.join(CHARTS, f"{sym}.json")
        parsed = parse_chart(path) if os.path.exists(path) else None
        c = compute_from_rows(parsed["rows"], parsed["meta"]) if parsed else None
        if not c:
            missing.append(sym)
            continue
        c.update(ticker=sym, company=rec.get("Company Name"), industry=rec.get("Industry"),
                 yahoo_symbol=parsed["meta"].get("symbol"), yahoo_rmp=parsed["meta"].get("regularMarketPrice"),
                 yahoo_rmt=parsed["meta"].get("regularMarketTime"), in_nifty50=sym in n50)
        c["avg_traded_value_20d_cr"] = c["avg_traded_value_20d"] / 1e7
        tech[sym] = c

    indices = {}
    for label, fname in INDEX_FILES:
        parsed = parse_chart(os.path.join(CHARTS, fname))
        c = compute_from_rows(parsed["rows"], parsed["meta"]) if parsed else None
        if not c:
            indices[label] = {"error": "parse_failed_or_short", "file": fname}
            continue
        c.update(yahoo_symbol=parsed["meta"].get("symbol"), yahoo_rmp=parsed["meta"].get("regularMarketPrice"),
                 yahoo_name=parsed["meta"].get("shortName") or parsed["meta"].get("longName"))
        for k in ("close", "ema20", "dma20", "dma50", "dma200"):
            pass
        indices[label] = c
    single_bar = {}
    for fn in sorted(glob.glob(os.path.join(CHARTS, "IDX_*.json"))):
        p = parse_chart(fn)
        if p and len(p["rows"]) < 30:
            single_bar[os.path.basename(fn)] = {"n_bars": len(p["rows"]), "last": p["rows"][-1], "symbol": p["meta"].get("symbol")}

    vix_trend = None
    vp = parse_chart(os.path.join(CHARTS, "IDX_INDIAVIX.json"))
    if vp and len(vp["rows"]) >= 22:
        rows = vp["rows"]
        now, ago = rows[-1]["close"], rows[-22]["close"]
        vix_trend = {"now": now, "now_date": rows[-1]["date"], "ago_21_sessions": ago, "ago_date": rows[-22]["date"],
                     "change": now - ago, "change_pct": (now / ago - 1) * 100 if ago else None,
                     "direction": "up" if now > ago else ("down" if now < ago else "flat"),
                     "last_10_closes": [(x["date"], x["close"]) for x in rows[-10:]]}

    have50 = [s for s, c in tech.items() if c.get("dma50") is not None]
    above50 = [s for s in have50 if tech[s]["close"] > tech[s]["dma50"]]
    have200 = [s for s, c in tech.items() if c.get("dma200") is not None]
    above200 = [s for s in have200 if tech[s]["close"] > tech[s]["dma200"]]
    have20 = [s for s, c in tech.items() if c.get("dma20") is not None]
    above20 = [s for s in have20 if tech[s]["close"] > tech[s]["dma20"]]
    n50_have = [s for s in n50 if s in tech and tech[s].get("dma50") is not None]
    n50_above = [s for s in n50_have if tech[s]["close"] > tech[s]["dma50"]]
    rule_a = sorted(s for s, c in tech.items() if c["tech_rule"] == "A")
    rule_b = sorted(s for s, c in tech.items() if c["tech_rule"] == "B")
    off_session = sorted(s for s, c in tech.items() if c["as_of"] != SESSION)

    summary = {
        "session": SESSION,
        "computed_count": len(tech),
        "missing_or_short": missing,
        "names_last_bar_not_session": off_session,
        "session_dates": sorted({c["as_of"] for c in tech.values()}),
        "breadth": {
            "universe": f"Nifty 500 constituents (niftyindices CSV, {len(univ)} rows)",
            "sample_with_50dma": len(have50), "above_50dma_count": len(above50),
            "above_50dma_pct": round(100.0 * len(above50) / len(have50), 2) if have50 else None,
            "sample_with_20dma": len(have20), "above_20dma_count": len(above20),
            "above_20dma_pct": round(100.0 * len(above20) / len(have20), 2) if have20 else None,
            "sample_with_200dma": len(have200), "above_200dma_count": len(above200),
            "above_200dma_pct": round(100.0 * len(above200) / len(have200), 2) if have200 else None,
            "nifty50_sample_with_50dma": len(n50_have), "nifty50_above_50dma_count": len(n50_above),
            "nifty50_above_50dma_pct": round(100.0 * len(n50_above) / len(n50_have), 2) if n50_have else None,
            "nifty50_above_50dma": sorted(n50_above),
        },
        "vix_trend": vix_trend,
        "tech_rule_A_count": len(rule_a), "tech_rule_A": rule_a,
        "tech_rule_B_count": len(rule_b), "tech_rule_B": rule_b,
        "tech_pass_count": len(rule_a) + len(rule_b),
        "single_bar_indices": single_bar,
    }
    compact = {}
    for s, c in tech.items():
        d = {k: (round(v, 4) if isinstance(v, float) else v) for k, v in c.items() if k != "last_20_bars"}
        if c["tech_pass"]:
            d["last_20_bars"] = c["last_20_bars"]
        compact[s] = d
    full_bars = {s: c["last_20_bars"] for s, c in tech.items()}
    json.dump(indices, open(os.path.join(OUT, "indices.json"), "w"), indent=1)
    json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), indent=1)
    json.dump(compact, open(os.path.join(OUT, "tech.json"), "w"))
    json.dump(full_bars, open("/tmp/swing-2026-10-19/misc/all_last20_bars.json", "w"))
    b = summary["breadth"]
    print("computed", len(tech), "missing", missing, "off-session", off_session)
    print("breadth >50", b["above_50dma_count"], "/", b["sample_with_50dma"], b["above_50dma_pct"], "% | >20", b["above_20dma_pct"], "| >200", b["above_200dma_pct"], "| N50", b["nifty50_above_50dma_count"], "/", b["nifty50_sample_with_50dma"])
    print("rule A", len(rule_a), "rule B", len(rule_b))
    print("vix", vix_trend)
    for lab, ix in indices.items():
        print(lab, {k: (round(ix[k], 2) if isinstance(ix.get(k), float) else ix.get(k)) for k in ("as_of", "close", "ema20", "dma20", "dma50", "dma200", "rsi14", "ret_1m_21d", "ret_3m_63d", "last_close_filled_from_meta")})


if __name__ == "__main__":
    main()

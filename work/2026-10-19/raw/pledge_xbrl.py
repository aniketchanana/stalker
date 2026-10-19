#!/usr/bin/env python3
"""Promoter pledge % from the latest NSE shareholding-pattern XBRL filing.

pledge % of promoter holding = NumberOfSharesEncumberedUnderPledged / NumberOfShares  (context ShareholdingOfPromoterAndPromoterGroup)
Source list: https://www.nseindia.com/api/corporate-share-holdings-master?index=equities&symbol=SYM
Writes computed/pledge.json  {SYM: {value, as_of, source_url, method, notes}}
"""
import http.cookiejar, json, os, re, sys, time, urllib.request, datetime

TMP = "/tmp/swing-2026-10-19/misc/shp"
OUT = "/workspace/work/2026-10-19/raw/computed/pledge.json"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", UA), ("Accept", "application/json,text/html,*/*"), ("Referer", "https://www.nseindia.com/")]
CTX = "ShareholdingOfPromoterAndPromoterGroup_ContextI"


def get(url):
    try:
        with op.open(url, timeout=40) as r:
            return r.status, r.read()
    except urllib.error.HTTPError as e:
        return e.code, b""
    except Exception as e:
        return 0, str(e).encode()


def val(x, tag, ctx):
    m = re.search(r'<[^>]*:%s\b[^>]*contextRef="%s"[^>]*>([^<]*)<' % (tag, ctx), x)
    return float(m.group(1)) if m and m.group(1).strip() else None


def main(syms):
    os.makedirs(TMP, exist_ok=True)
    out = json.load(open(OUT)) if os.path.exists(OUT) else {}
    get("https://www.nseindia.com/")
    for s in syms:
        code, body = get(f"https://www.nseindia.com/api/corporate-share-holdings-master?index=equities&symbol={s}")
        try:
            recs = json.loads(body)
        except Exception:
            out[s] = {"value": None, "notes": f"NSE shareholding master HTTP {code}, unparseable", "method": "unavailable"}
            continue
        if not recs:
            out[s] = {"value": None, "notes": "NSE shareholding master empty", "method": "unavailable"}
            continue
        recs.sort(key=lambda r: datetime.datetime.strptime(r["date"], "%d-%b-%Y"), reverse=True)
        r = recs[0]
        xp = os.path.join(TMP, f"{s}.xml")
        c2, xb = get(r["xbrl"])
        open(xp, "wb").write(xb)
        x = xb.decode("utf-8", "ignore")
        tot = val(x, "NumberOfShares", CTX)
        pl = val(x, "NumberOfSharesEncumberedUnderPledged", CTX)
        enc = val(x, "NumberOfSharesEncumbered", CTX)
        promo_pct = r.get("pr_and_prgrp")
        if tot in (None, 0):
            v = None
            note = f"No promoter-group shares in XBRL (promoter % on NSE master={promo_pct}); pledge not applicable"
        else:
            v = round((pl or 0) / tot * 100, 2)
            note = (f"Pledged {int(pl or 0)} of {int(tot)} promoter shares; total encumbered {int(enc or 0)} "
                    f"({round((enc or 0) / tot * 100, 2)}%). Promoter % of equity {promo_pct}. Filed {r.get('submissionDate')}.")
        out[s] = {"value": v, "as_of": r["date"], "source_url": r["xbrl"], "method": "scraped",
                  "promoter_pct": promo_pct, "notes": note, "xbrl_http": c2}
        print(s, r["date"], v, note[:120], flush=True)
        time.sleep(0.6)
    json.dump(out, open(OUT, "w"), indent=1)


if __name__ == "__main__":
    args = sys.argv[1:]
    if len(args) == 1 and os.path.exists(args[0]):
        args = json.load(open(args[0]))
    main(args)

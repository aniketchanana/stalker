#!/usr/bin/env python3
"""Fetch Yahoo v8 1d/1y charts (indices + Nifty 500 names) and quoteSummary for candidates.

Usage:
  fetch_yahoo.py charts            # indices + all Nifty 500 names
  fetch_yahoo.py qs SYM1 SYM2 ...   # quoteSummary (cookie + crumb)
Raw responses go to /tmp/swing-2026-10-19/{charts,qs}. Never invents data.
"""
import csv, json, os, sys, time, urllib.parse, http.cookiejar, urllib.request, urllib.error
from concurrent.futures import ThreadPoolExecutor

TMP = "/tmp/swing-2026-10-19"
CH = os.path.join(TMP, "charts")
QS = os.path.join(TMP, "qs")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
LOG = os.path.join(TMP, "misc", "yahoo_fetch_log.json")

cj = http.cookiejar.CookieJar()
opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
opener.addheaders = [("User-Agent", UA), ("Accept", "application/json,text/html,*/*"), ("Accept-Language", "en-US,en;q=0.9")]

INDICES = ["^NSEI", "^CRSLDX", "^INDIAVIX", "^NSEBANK", "^CNXIT", "^CNXPHARMA", "^NSEMDCP50", "^CNXAUTO", "^CNXMETAL",
           "^CNXFMCG", "^CNXENERGY", "^CNXREALTY", "^CNXINFRA", "^CNXMEDIA", "^CNXPSUBANK", "^CNXCONSUM", "^CNXCMDT",
           "^CNXSERVICE", "^CNXFIN", "NIFTY_FIN_SERVICE.NS", "^CNXSC", "^CNXPSE", "^CNXMNC", "NIFTY_HEALTHCARE.NS",
           "^CNXSMALLCAP", "^CNXMIDCAP", "NIFTYMIDCAP150.NS", "NIFTY_MIDCAP_100.NS", "^NSMIDCP", "BZ=F", "USDINR=X"]


def get(url, tries=4):
    last = None
    for i in range(tries):
        try:
            with opener.open(url, timeout=30) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            last = (e.code, e.read())
            if e.code == 429:
                time.sleep(4 * (2 ** i))
                continue
            return last
        except Exception as e:  # network
            last = (0, str(e).encode())
            time.sleep(2 * (2 ** i))
    return last


def chart(sym, fname):
    url = f"https://query1.finance.yahoo.com/v8/finance/chart/{urllib.parse.quote(sym)}?interval=1d&range=1y"
    code, body = get(url)
    with open(os.path.join(CH, fname), "wb") as f:
        f.write(body or b"")
    return sym, code, len(body or b"")


def run_charts():
    os.makedirs(CH, exist_ok=True)
    get("https://fc.yahoo.com")
    log = {}
    for s in INDICES:
        sym, code, n = chart(s, "IDX_" + s.replace("^", "").replace("=", "_") + ".json")
        log[s] = code
        time.sleep(0.3)
    rows = list(csv.DictReader(open(os.path.join(TMP, "misc", "ind_nifty500list.csv"))))
    syms = [r["Symbol"].strip() for r in rows]
    with ThreadPoolExecutor(max_workers=4) as ex:
        for sym, code, n in ex.map(lambda s: chart(s + ".NS", s + ".json"), syms):
            log[sym] = code
    json.dump(log, open(LOG, "w"), indent=1)
    bad = {k: v for k, v in log.items() if v != 200}
    print("fetched", len(log), "non-200:", bad)


def run_qs(syms):
    os.makedirs(QS, exist_ok=True)
    get("https://fc.yahoo.com")
    code, crumb = get("https://query1.finance.yahoo.com/v1/test/getcrumb")
    crumb = crumb.decode().strip()
    print("crumb", code, crumb)
    mods = "financialData,defaultKeyStatistics,summaryDetail,recommendationTrend,earningsTrend,price,calendarEvents"
    for s in syms:
        y = s if (s.startswith("^") or s.endswith(".NS")) else s + ".NS"
        url = f"https://query1.finance.yahoo.com/v10/finance/quoteSummary/{urllib.parse.quote(y)}?modules={mods}&crumb={urllib.parse.quote(crumb)}"
        code, body = get(url)
        with open(os.path.join(QS, s + ".json"), "wb") as f:
            f.write(body or b"")
        print(s, code, len(body or b""))
        time.sleep(0.5)


def run_list(csvpath):
    os.makedirs(CH, exist_ok=True)
    get("https://fc.yahoo.com")
    syms = [r["Symbol"].strip() for r in csv.DictReader(open(csvpath))]
    syms = [s for s in syms if not os.path.exists(os.path.join(CH, s + ".json"))]
    log = {}
    with ThreadPoolExecutor(max_workers=4) as ex:
        for sym, code, n in ex.map(lambda s: chart(s + ".NS", s + ".json"), syms):
            log[sym] = code
    print("fetched", len(log), "non-200:", {k: v for k, v in log.items() if v != 200})


if __name__ == "__main__":
    if sys.argv[1] == "charts":
        run_charts()
    elif sys.argv[1] == "list":
        run_list(sys.argv[2])
    else:
        run_qs(sys.argv[2:])

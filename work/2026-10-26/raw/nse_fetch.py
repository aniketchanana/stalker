#!/usr/bin/env python3
"""NSE archives + cookie-gated APIs for the 2026-10-26 run (session 2026-10-23).

  nse_fetch.py archives   -> bhavcopies (last 20 sessions), ind_close_all (t, t-5, t-21, t-63), fo_secban, bulk, block
  nse_fetch.py apis       -> holiday master, ASM, GSM, board meetings (past + future), event calendar, corp actions, FII/DII
  nse_fetch.py shp SYM .. -> corporate-share-holdings-master per symbol + latest SHP XBRL
Everything lands in /tmp/run1026/misc (shp/ for XBRL). Logs HTTP codes to misc/nse_fetch_log.json.
"""
import json, os, sys, time, http.cookiejar, urllib.request, urllib.error, urllib.parse

MISC = "/tmp/run1026/misc"
SHP = os.path.join(MISC, "shp")
LOG = os.path.join(MISC, "nse_fetch_log.json")
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
SESSIONS = ['2026-09-24', '2026-09-25', '2026-09-28', '2026-09-29', '2026-09-30', '2026-10-01', '2026-10-05', '2026-10-06', '2026-10-07', '2026-10-08', '2026-10-09', '2026-10-12', '2026-10-13', '2026-10-14', '2026-10-15', '2026-10-16', '2026-10-19', '2026-10-21', '2026-10-22', '2026-10-23']
IDX_DATES = {"t": "2026-10-23", "t1w": "2026-10-16", "t1m": "2026-09-23", "t3m": "2026-07-23", "t21": "2026-09-22", "t63": "2026-07-23"}

cj = http.cookiejar.CookieJar()
op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
op.addheaders = [("User-Agent", UA), ("Accept", "application/json,text/plain,text/csv,*/*"), ("Accept-Language", "en-US,en;q=0.9"),
                 ("Referer", "https://www.nseindia.com/")]
log = json.load(open(LOG)) if os.path.exists(LOG) else {}


def get(url, tries=2):
    last = (0, b"")
    for i in range(tries):
        try:
            with op.open(url, timeout=40) as r:
                return r.status, r.read()
        except urllib.error.HTTPError as e:
            last = (e.code, e.read() or b"")
            if e.code in (404, 403):
                return last
        except Exception as e:
            last = (0, str(e).encode())
        time.sleep(3 * (i + 1))
    return last


def save(url, fn):
    code, body = get(url)
    log[url] = {"code": code, "bytes": len(body), "file": fn}
    if code == 200 and body:
        open(os.path.join(MISC, fn), "wb").write(body)
    print(code, len(body), fn, flush=True)
    time.sleep(0.4)
    return code, body


def ddmmyyyy(iso):
    y, m, d = iso.split("-")
    return d + m + y


def archives():
    for s in SESSIONS:
        k = ddmmyyyy(s)
        fn = f"sec_bhavdata_full_{k}.csv"
        if not os.path.exists(os.path.join(MISC, fn)):
            save(f"https://nsearchives.nseindia.com/products/content/sec_bhavdata_full_{k}.csv", fn)
    for lab, s in IDX_DATES.items():
        k = ddmmyyyy(s)
        save(f"https://nsearchives.nseindia.com/content/indices/ind_close_all_{k}.csv", f"ind_close_{k}.csv")
    save("https://nsearchives.nseindia.com/content/fo/fo_secban.csv", "fo_secban.csv")
    save("https://nsearchives.nseindia.com/content/equities/bulk.csv", "bulk.csv")
    save("https://nsearchives.nseindia.com/content/equities/block.csv", "block.csv")


def cookie():
    c, _ = get("https://www.nseindia.com")
    print("homepage", c, [x.name for x in cj])
    get("https://www.nseindia.com/market-data/live-equity-market")


def apis():
    cookie()
    base = "https://www.nseindia.com/api/"
    jobs = [
        ("holiday-master?type=trading", "nse_holidays.json"),
        ("reportASM", "nse_asm.json"),
        ("reportGSM", "nse_gsm.json"),
        ("corporate-board-meetings?index=equities&from_date=26-10-2026&to_date=31-12-2026", "nse_board_future.json"),
        ("corporate-board-meetings?index=equities&from_date=25-09-2026&to_date=25-10-2026", "nse_board_past.json"),
        ("event-calendar", "nse_event_calendar.json"),
        ("corporate-board-meetings?index=equities&from_date=01-10-2025&to_date=30-11-2025", "nse_board_2025q2.json"),
        ("corporates-corporateActions?index=equities&from_date=26-10-2026&to_date=30-11-2026", "nse_corp_actions.json"),
        ("fiidiiTradeReact", "nse_fiidii.json"),
        ("corporates-financial-results?index=equities&period=Quarterly&from_date=01-10-2026&to_date=25-10-2026", "nse_fin_results.json"),
    ]
    for path, fn in jobs:
        save(base + path, fn)
    json.dump(log, open(LOG, "w"), indent=1)


def shp(syms):
    os.makedirs(SHP, exist_ok=True)
    cookie()
    for s in syms:
        code, body = get("https://www.nseindia.com/api/corporate-share-holdings-master?index=equities&symbol=" + urllib.parse.quote(s))
        log["shp_master_" + s] = code
        if code != 200:
            print(s, "master", code, flush=True)
            continue
        try:
            rows = json.loads(body)
        except ValueError:
            print(s, "bad json", flush=True)
            continue
        open(os.path.join(SHP, s + "_master.json"), "wb").write(body)
        rows = [r for r in rows if r.get("xbrl")]
        rows.sort(key=lambda r: time.strptime(r.get("date", "01-JAN-1900"), "%d-%b-%Y"), reverse=True)
        if not rows:
            print(s, "no xbrl rows", flush=True)
            continue
        r = rows[0]
        c2, x = get(r["xbrl"])
        if c2 == 200:
            open(os.path.join(SHP, s + ".xml"), "wb").write(x)
            json.dump({"date": r.get("date"), "xbrl": r["xbrl"], "submissionDate": r.get("submissionDate") or r.get("broadcastDate")},
                      open(os.path.join(SHP, s + "_meta.json"), "w"))
        print(s, r.get("date"), c2, len(x), flush=True)
        time.sleep(0.4)
    json.dump(log, open(LOG, "w"), indent=1)


if __name__ == "__main__":
    {"archives": lambda: archives(), "apis": lambda: apis(), "shp": lambda: shp(sys.argv[2:])}[sys.argv[1]]()
    json.dump(log, open(LOG, "w"), indent=1)

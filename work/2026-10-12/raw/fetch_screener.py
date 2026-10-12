#!/usr/bin/env python3
"""Polite screener.in fetcher (company pages + /market/ industry pages).

  fetch_screener.py company SYM ...   -> /tmp/swing-2026-10-12/screener/SYM.html (consolidated, standalone fallback)
  fetch_screener.py market /market/... -> /tmp/swing-2026-10-12/industries/<href with _>.html
Skips files already on disk. ~1.1 s between requests, exponential backoff on 429.
"""
import os, re, sys, time, json, urllib.request, urllib.error

TMP = "/tmp/swing-2026-10-12"
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
LOG = os.path.join(TMP, "misc", "screener_fetch_log.json")


def get(url, tries=5):
    for i in range(tries):
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": "text/html", "Accept-Language": "en-US,en;q=0.9"})
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.status, r.read().decode("utf-8", "ignore")
        except urllib.error.HTTPError as e:
            if e.code == 429:
                time.sleep(10 * (2 ** i))
                continue
            return e.code, ""
        except Exception:
            time.sleep(5 * (2 ** i))
    return 429, ""


def has_ratios(html):
    i = html.find('id="top-ratios"')
    if i < 0:
        return False
    chunk = html[i:i + 4000]
    return bool(re.search(r'Book Value.{0,400}?class="number">\s*[\d,.]+', chunk, re.S))


def load_log():
    return json.load(open(LOG)) if os.path.exists(LOG) else {}


def company(syms):
    os.makedirs(os.path.join(TMP, "screener"), exist_ok=True)
    log = load_log()
    for s in syms:
        out = os.path.join(TMP, "screener", s + ".html")
        if os.path.exists(out) and os.path.getsize(out) > 20000:
            continue
        url = f"https://www.screener.in/company/{s}/consolidated/"
        code, html = get(url)
        variant = "consolidated"
        time.sleep(1.1)
        if code != 200 or not has_ratios(html):
            url2 = f"https://www.screener.in/company/{s}/"
            code2, html2 = get(url2)
            time.sleep(1.1)
            if code2 == 200 and html2:
                code, html, url, variant = code2, html2, url2, "standalone"
        log[s] = {"code": code, "url": url, "variant": variant, "bytes": len(html)}
        if html:
            open(out, "w").write(html)
        print(s, code, variant, len(html), flush=True)
    json.dump(log, open(LOG, "w"), indent=1)


def market(hrefs):
    os.makedirs(os.path.join(TMP, "industries"), exist_ok=True)
    log = load_log()
    for h in hrefs:
        fn = h.strip("/").replace("/", "_") + ".html"
        out = os.path.join(TMP, "industries", fn)
        if os.path.exists(out) and os.path.getsize(out) > 5000:
            continue
        code, html = get("https://www.screener.in" + h)
        time.sleep(1.1)
        log[h] = {"code": code, "bytes": len(html)}
        if html:
            open(out, "w").write(html)
        print(h, code, len(html), flush=True)
    json.dump(log, open(LOG, "w"), indent=1)


if __name__ == "__main__":
    args = sys.argv[2:]
    if len(args) == 1 and os.path.exists(args[0]):
        args = json.load(open(args[0]))
    (company if sys.argv[1] == "company" else market)(args)

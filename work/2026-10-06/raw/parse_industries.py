#!/usr/bin/env python3
import os, re, json, glob, statistics, html as htmllib

INDIR = "/workspace/work/2026-10-06/raw/industries"
OUT = "/workspace/work/2026-10-06/raw/computed/industry_medians.json"

def clean(s):
    return re.sub(r"\s+", " ", htmllib.unescape(s or "")).strip()

def fnum(s):
    t = clean(s).replace(",", "").replace("%", "")
    if t in ("", "-", "—"):
        return None
    try:
        return float(t)
    except ValueError:
        return None

def parse_industry(path):
    html = open(path, encoding="utf-8", errors="ignore").read()
    title = None
    m = re.search(r"<title>([^<]+)</title>", html)
    if m:
        title = clean(m.group(1))
    peers = []
    for tr in re.findall(r'<tr data-row-company-id="[^"]+">(.*?)</tr>', html, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(tds) < 5:
            continue
        aname = re.search(r"<a href=\"(/company/([^/]+)/[^\"]*)\"[^>]*>([^<]+)</a>", tds[1])
        if not aname:
            continue
        ticker = aname.group(2)
        name = clean(aname.group(3))
        # columns: sno, company, CMP, P/E, Mar Cap, ...
        cmp_ = fnum(re.sub("<[^>]+>", "", tds[2]))
        pe = fnum(re.sub("<[^>]+>", "", tds[3]))
        mcap = fnum(re.sub("<[^>]+>", "", tds[4]))
        peers.append({"ticker": ticker, "name": name, "cmp": cmp_, "pe": pe, "mcap_cr": mcap})
    pes = [p["pe"] for p in peers if p["pe"] is not None and p["pe"] > 0]
    med = statistics.median(pes) if pes else None
    return {
        "title": title,
        "file": os.path.basename(path),
        "n_peers": len(peers),
        "n_pe": len(pes),
        "median_pe": med,
        "min_pe": min(pes) if pes else None,
        "max_pe": max(pes) if pes else None,
        "peers": peers,
    }

def main():
    hrefs = json.load(open("/tmp/ind_hrefs.json"))
    out = {}
    by_href = {}
    for path in glob.glob(os.path.join(INDIR, "*.html")):
        rec = parse_industry(path)
        # reconstruct href from filename _market_IN.. -> /market/IN..
        fn = rec["file"].replace(".html", "")
        href = fn.replace("_", "/")
        if not href.startswith("/"):
            href = "/" + href
        # filenames were /market/... with / -> _
        # '/market/IN06/...' became '_market_IN06_...'
        href = fn
        if href.startswith("_market_"):
            href = "/" + href[1:].replace("_", "/")
            # careful: IN060101 should stay... we replaced ALL _ with /
            # original: /market/IN06/IN0601/IN060101/IN060101001/
            # fn: _market_IN06_IN0601_IN060101_IN060101001_
            # after: /market/IN06/IN0601/IN060101/IN060101001/
            pass
        rec["href"] = href
        by_href[href] = rec
        out[href] = rec
        print(f"{rec['median_pe']} n={rec['n_pe']}/{rec['n_peers']} {rec['title']}")
    json.dump(out, open(OUT, "w"), indent=2)
    print("wrote", OUT, "industries", len(out))

if __name__ == "__main__":
    main()

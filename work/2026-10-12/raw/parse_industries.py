#!/usr/bin/env python3
"""Screener /market/ industry pages (all pages, default sort = market cap desc) -> peer tables + median PE.

Primary median = median of all positive P/E cells across every page of the industry.
Also records median of the top-25-by-mcap page-1 subset (last week's method) for comparison.
"""
import os, re, json, glob, statistics, html as htmllib

INDIR = "/tmp/swing-2026-10-12/industries"
OUT = "/workspace/work/2026-10-12/raw/computed/industry_medians.json"


def clean(s):
    return re.sub(r"\s+", " ", htmllib.unescape(s or "")).strip()


def fnum(s):
    t = clean(re.sub("<[^>]+>", "", s or "")).replace(",", "").replace("%", "")
    if t in ("", "-", "—"):
        return None
    try:
        return float(t)
    except ValueError:
        return None


def parse_page(html):
    peers = []
    for tr in re.findall(r'<tr data-row-company-id="[^"]+">(.*?)</tr>', html, re.S):
        tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
        if len(tds) < 11:
            continue
        a = re.search(r"<a href=\"(/company/([^/]+)/[^\"]*)\"[^>]*>([^<]+)</a>", tds[1])
        if not a:
            continue
        peers.append({"ticker": a.group(2), "href": a.group(1), "name": clean(a.group(3)), "cmp": fnum(tds[2]),
                      "pe": fnum(tds[3]), "mcap_cr": fnum(tds[4]), "roce": fnum(tds[10])})
    return peers


def med(xs):
    return statistics.median(xs) if xs else None


def main():
    groups = {}
    for path in glob.glob(os.path.join(INDIR, "market_*.html")):
        fn = os.path.basename(path)[:-5]
        base, _, q = fn.partition("?page=")
        base = base.rstrip("_")
        page = int(q) if q else 1
        groups.setdefault(base, {})[page] = path
    out = {}
    for base, pages in groups.items():
        href = "/" + base.replace("_", "/") + "/"
        html1 = open(pages[1], encoding="utf-8", errors="ignore").read()
        title = clean(re.search(r"<title>([^<]+)</title>", html1).group(1)) if "<title>" in html1 else None
        m = re.search(r"Showing page 1 of (\d+)", html1)
        n_pages_site = int(m.group(1)) if m else 1
        peers = []
        for p in sorted(pages):
            for row in parse_page(open(pages[p], encoding="utf-8", errors="ignore").read()):
                row["page"] = p
                peers.append(row)
        pes = [x["pe"] for x in peers if x["pe"] is not None and x["pe"] > 0]
        top25 = [x for x in peers if x["page"] == 1]
        pes25 = [x["pe"] for x in top25 if x["pe"] is not None and x["pe"] > 0]
        roces = [x["roce"] for x in peers if x["roce"] is not None]
        out[href] = {
            "title": title, "href": href, "url": "https://www.screener.in" + href,
            "pages_site": n_pages_site, "pages_fetched": len(pages),
            "n_peers": len(peers), "n_pe": len(pes), "median_pe": med(pes),
            "n_pe_top25_mcap": len(pes25), "median_pe_top25_mcap": med(pes25),
            "median_roce": med(roces), "n_roce": len(roces),
            "peers": peers,
        }
        print(f"{title}: med_pe_all={out[href]['median_pe']} n={len(pes)}/{len(peers)} pages {len(pages)}/{n_pages_site} | top25 med={out[href]['median_pe_top25_mcap']} n={len(pes25)}")
    json.dump(out, open(OUT, "w"), indent=1)
    print("wrote", OUT, len(out))


if __name__ == "__main__":
    main()

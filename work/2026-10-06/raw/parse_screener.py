#!/usr/bin/env python3
"""Parse screener.in company HTML. Never invent values."""
import os, re, json, glob, html as htmllib
from html.parser import HTMLParser

INDIR = "/workspace/work/2026-10-06/raw/screener"
OUT = "/workspace/work/2026-10-06/raw/computed/screener_fundamentals.json"

def clean_text(s):
    s = htmllib.unescape(s or "")
    s = re.sub(r"\s+", " ", s).strip()
    return s

def parse_num(s):
    if s is None:
        return None
    t = clean_text(str(s))
    if t in ("", "-", "—", "NA", "N/A", "nan"):
        return None
    neg = False
    if t.startswith("(") and t.endswith(")"):
        neg = True
        t = t[1:-1]
    t = t.replace(",", "").replace("%", "").replace("₹", "").replace("Cr.", "").replace("Cr", "").strip()
    if t.endswith("%"):
        t = t[:-1]
    try:
        v = float(t)
        return -v if neg else v
    except ValueError:
        return None

class TableParser:
    def __init__(self, html):
        self.html = html

    def top_ratios(self):
        m = re.search(r'<ul id="top-ratios".*?</ul>', self.html, re.S)
        if not m:
            return {}
        out = {}
        for li in re.findall(r"<li[^>]*>(.*?)</li>", m.group(0), re.S):
            nm = re.search(r'class="name"[^>]*>\s*([^<]+)', li)
            if not nm:
                continue
            name = clean_text(nm.group(1))
            nums = re.findall(r'class="number"[^>]*>\s*([^<]+)', li)
            nums = [clean_text(x) for x in nums]
            if name == "High / Low" and len(nums) >= 2:
                out["high_52w_screener"] = parse_num(nums[0])
                out["low_52w_screener"] = parse_num(nums[1])
                out["high_low_raw"] = " / ".join(nums)
            elif nums:
                out[name] = parse_num(nums[0])
                out[name + "_raw"] = nums[0]
            else:
                val = re.search(r'class="nowrap value"[^>]*>(.*?)</span>', li, re.S)
                out[name + "_raw"] = clean_text(re.sub("<[^>]+>", " ", val.group(1))) if val else None
        return out

    def section_table(self, section_id):
        """Return {row_label: {date: value}} for first data-table in section."""
        idx = self.html.find(f'id="{section_id}"')
        if idx < 0:
            return None, []
        chunk = self.html[idx: idx + 80000]
        tm = re.search(r"<table class=\"data-table[^\"]*\"[^>]*>(.*?)</table>", chunk, re.S)
        if not tm:
            return None, []
        table = tm.group(1)
        # headers
        thead = re.search(r"<thead>(.*?)</thead>", table, re.S)
        dates = []
        if thead:
            # data-date-key preferred
            dates = re.findall(r'data-date-key="([^"]+)"', thead.group(1))
            if not dates:
                dates = [clean_text(x) for x in re.findall(r"<th[^>]*>(.*?)</th>", thead.group(1), re.S)]
                dates = [re.sub("<[^>]+>", " ", d) for d in dates]
                dates = [clean_text(d) for d in dates]
                if dates and dates[0] == "":
                    dates = dates[1:]
        body = re.search(r"<tbody>(.*?)</tbody>", table, re.S)
        rows = {}
        if not body:
            return rows, dates
        for tr in re.findall(r"<tr[^>]*>(.*?)</tr>", body.group(1), re.S):
            tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
            if not tds:
                continue
            label = clean_text(re.sub(r"<button[^>]*>", " ", tds[0]))
            label = clean_text(re.sub(r"<[^>]+>", " ", label))
            label = label.replace("+", "").strip()
            vals = []
            for td in tds[1:]:
                txt = clean_text(re.sub(r"<[^>]+>", " ", td))
                vals.append(parse_num(txt) if txt not in ("",) else None)
            # map to dates
            dmap = {}
            for i, v in enumerate(vals):
                key = dates[i] if i < len(dates) else str(i)
                dmap[key] = v
            rows[label] = dmap
        return rows, dates

    def ranges(self):
        out = {}
        for m in re.finditer(r'<table class="ranges-table">(.*?)</table>', self.html, re.S):
            block = m.group(1)
            th = re.search(r"<th[^>]*>(.*?)</th>", block, re.S)
            title = clean_text(re.sub("<[^>]+>", " ", th.group(1))) if th else None
            pairs = {}
            for tr in re.findall(r"<tr>(.*?)</tr>", block, re.S):
                tds = re.findall(r"<td[^>]*>(.*?)</td>", tr, re.S)
                if len(tds) >= 2:
                    k = clean_text(re.sub("<[^>]+>", " ", tds[0])).rstrip(":")
                    v = clean_text(re.sub("<[^>]+>", " ", tds[1]))
                    pairs[k] = parse_num(v)
                    pairs[k + "_raw"] = v
            if title:
                out[title] = pairs
        return out

    def industry_path(self):
        # last industry link in peers sub
        m = re.search(r'id="peers".{0,4000}?title="Industry"[^>]*>\s*([^<]+)', self.html, re.S)
        names = {}
        for title, name in re.findall(r'title="(Broad Sector|Sector|Broad Industry|Industry)"[^>]*>\s*([^<]+)', self.html):
            names[title] = clean_text(name)
        hrefs = re.findall(r'<a href="(/market/[^"]+)"[^>]*title="Industry"', self.html)
        return names, hrefs[-1] if hrefs else None

    def upcoming(self):
        m = re.search(r"Upcoming result date:\s*([^<\n]+)", self.html, re.I)
        if m:
            return clean_text(m.group(1))
        m = re.search(r"result date[^<]{0,40}(\d{1,2}\s+\w+\s+20\d{2})", self.html, re.I)
        return clean_text(m.group(1)) if m else None

    def as_of_price_line(self):
        # e.g. 05 Oct - close price
        m = re.search(r'(\d{1,2}\s+\w+)\s*-\s*close price', self.html, re.I)
        return clean_text(m.group(1)) if m else None

    def pledged(self):
        # sometimes in top ratios as Promoter holding / pledged
        m = re.search(r'Pledged[^<]{0,80}class="number"[^>]*>\s*([^<]+)', self.html, re.I)
        if m:
            return parse_num(m.group(1))
        m = re.search(r'Pledged percentage.{0,200}?class="number"[^>]*>\s*([^<]+)', self.html, re.S | re.I)
        if m:
            return parse_num(m.group(1))
        # shareholding pledged row
        if re.search(r">Pledged<", self.html):
            idx = self.html.find(">Pledged<")
            chunk = self.html[idx: idx + 2000]
            nums = re.findall(r"<td[^>]*>\s*([0-9.,]+)\s*%?", chunk)
            if nums:
                return parse_num(nums[-1])
        return None


def last_val(dmap):
    if not dmap:
        return None, None
    # prefer ISO dates
    items = list(dmap.items())
    # skip TTM if we want annual? keep both
    return items[-1][0], items[-1][1]


def parse_file(path):
    html = open(path, encoding="utf-8", errors="ignore").read()
    if "Key Insights" not in html and "top-ratios" not in html:
        return {"error": "not_a_company_page", "size": len(html)}
    P = TableParser(html)
    top = P.top_ratios()
    pl, pl_dates = P.section_table("profit-loss")
    bs, bs_dates = P.section_table("balance-sheet")
    cf, cf_dates = P.section_table("cash-flow")
    q, q_dates = P.section_table("quarters")
    shp, shp_dates = P.section_table("shareholding")
    if shp is None or not shp:
        # quarterly-shp
        idx = html.find('id="quarterly-shp"')
        if idx >= 0:
            # reuse by injecting
            P2 = TableParser(html[idx-50:])
            # fake id
            html2 = 'id="shareholding"' + html[idx:]
            P2 = TableParser(html2)
            shp, shp_dates = P2.section_table("shareholding")
    ranges = P.ranges()
    ind_names, ind_href = P.industry_path()
    # D/E from balance sheet
    de = None
    de_asof = None
    de_notes = None
    if bs:
        # find equity + reserves and borrowings
        eq = None
        res = None
        bor = None
        eq_k = res_k = bor_k = None
        for lab, dmap in bs.items():
            l = lab.lower()
            if l.startswith("equity capital") or l == "equity capital":
                eq_k, eq = last_val(dmap)
            elif l.startswith("reserves"):
                res_k, res = last_val(dmap)
            elif "borrow" in l:
                bor_k, bor = last_val(dmap)
        if eq is not None and res is not None and bor is not None:
            den = eq + res
            if den:
                de = bor / den
                de_asof = bor_k
                de_notes = f"computed Borrowings({bor})/(Equity Capital {eq}+Reserves {res}) as of {bor_k}"
    # OCF
    ocf = ocf_asof = None
    if cf:
        for lab, dmap in cf.items():
            if "operating" in lab.lower():
                ocf_asof, ocf = last_val(dmap)
                break
    # TTM EPS from P&L
    ttm_eps = None
    if pl:
        for lab, dmap in pl.items():
            if lab.lower().startswith("eps"):
                # TTM column if present
                if "TTM" in dmap and dmap["TTM"] is not None:
                    ttm_eps = dmap["TTM"]
                else:
                    _, ttm_eps = last_val(dmap)
    # shareholding last
    def last_pct(key_substrs):
        if not shp:
            return None, None
        for lab, dmap in shp.items():
            l = lab.lower()
            if any(s in l for s in key_substrs):
                k, v = last_val(dmap)
                return v, k
        return None, None
    fii, fii_d = last_pct(["fii"])
    dii, dii_d = last_pct(["dii"])
    promo, promo_d = last_pct(["promoter"])
    # FII change last two
    fii_chg = None
    if shp:
        for lab, dmap in shp.items():
            if "fii" in lab.lower():
                items = [(k, v) for k, v in dmap.items() if v is not None]
                if len(items) >= 2:
                    fii_chg = {"from": items[-2], "to": items[-1], "delta_pp": items[-1][1] - items[-2][1]}
                break
    dii_chg = None
    if shp:
        for lab, dmap in shp.items():
            if "dii" in lab.lower():
                items = [(k, v) for k, v in dmap.items() if v is not None]
                if len(items) >= 2:
                    dii_chg = {"from": items[-2], "to": items[-1], "delta_pp": items[-1][1] - items[-2][1]}
                break
    title = None
    mt = re.search(r"<title>([^<]+)</title>", html)
    if mt:
        title = clean_text(mt.group(1))
    pb = None
    price = top.get("Current Price")
    bv = top.get("Book Value")
    if price and bv:
        pb = price / bv
    mcap = top.get("Market Cap")
    pe = top.get("Stock P/E")
    roe = top.get("ROE")
    return {
        "title": title,
        "price_as_of_line": P.as_of_price_line(),
        "upcoming_result_date": P.upcoming(),
        "top_ratios": {k: v for k, v in top.items() if not k.endswith("_raw") or True},
        "market_cap_cr": mcap,
        "price": price,
        "pe": pe,
        "book_value": bv,
        "pb_computed": pb,
        "roe": roe,
        "roce": top.get("ROCE"),
        "high_52w_screener": top.get("high_52w_screener"),
        "low_52w_screener": top.get("low_52w_screener"),
        "industry": ind_names,
        "industry_href": ind_href,
        "cagr": ranges,
        "debt_to_equity": de,
        "debt_to_equity_as_of": de_asof,
        "debt_to_equity_notes": de_notes,
        "ocf_latest_annual_cr": ocf,
        "ocf_as_of": ocf_asof,
        "ttm_eps": ttm_eps,
        "pledged_pct": P.pledged(),
        "promoter_pct": promo,
        "promoter_as_of": promo_d,
        "fii_pct": fii,
        "fii_as_of": fii_d,
        "fii_change": fii_chg,
        "dii_pct": dii,
        "dii_as_of": dii_d,
        "dii_change": dii_chg,
        "pl_labels": list(pl.keys())[:8] if pl else [],
        "bs_labels": list(bs.keys())[:10] if bs else [],
        "cf_labels": list(cf.keys())[:8] if cf else [],
        "shp_labels": list(shp.keys()) if shp else [],
    }


def main():
    out = {}
    for p in sorted(glob.glob(os.path.join(INDIR, "*.html"))):
        sym = os.path.basename(p).replace(".html", "")
        try:
            out[sym] = parse_file(p)
        except Exception as e:
            out[sym] = {"error": str(e)}
    json.dump(out, open(OUT, "w"), indent=2)
    print("parsed", len(out))
    # sanity
    for s in ["RELIANCE", "HDFCBANK", "TCS", "KOTAKBANK", "DIVISLAB", "PAYTM"]:
        d = out.get(s, {})
        print(s, "mcap", d.get("market_cap_cr"), "pe", d.get("pe"), "roe", d.get("roe"), "pb", d.get("pb_computed"),
              "de", d.get("debt_to_equity"), "ocf", d.get("ocf_latest_annual_cr"), "pledge", d.get("pledged_pct"),
              "ind", d.get("industry"), "res", d.get("upcoming_result_date"), "asof", d.get("price_as_of_line"),
              "3ysales", (d.get("cagr") or {}).get("Compounded Sales Growth", {}).get("3 Years"),
              "err", d.get("error"))

if __name__ == "__main__":
    main()

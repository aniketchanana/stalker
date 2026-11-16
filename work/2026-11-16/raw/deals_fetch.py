#!/usr/bin/env python3
"""NSE bulk/block deal history, one request per session -> misc/hist_{bulk,block}_deals.json.

Bulk deals are capped by the API at 70 rows per day (alphabetical), so history before the latest session is partial.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(__file__))
from nse_fetch import get, cookie

MISC = "/tmp/run1116/misc"
URL = "https://www.nseindia.com/api/historicalOR/bulk-block-short-deals?optionType={opt}&from={d}&to={d}"
DAYS = ["30-10-2026", "02-11-2026", "03-11-2026", "04-11-2026", "05-11-2026", "06-11-2026",
        "09-11-2026", "11-11-2026", "12-11-2026", "13-11-2026"]


def main():
    cookie()
    for opt, fn in (("bulk_deals", "hist_bulk_deals.json"), ("block_deals", "hist_block_deals.json")):
        rows = []
        for d in DAYS:
            code, body = get(URL.format(opt=opt, d=d))
            try:
                data = json.loads(body).get("data") or []
            except Exception:
                data = []
            print(opt, d, code, len(data), flush=True)
            rows += data
        json.dump(rows, open(os.path.join(MISC, fn), "w"))


if __name__ == "__main__":
    main()

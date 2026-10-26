"""Analyst Stage 1 (run 2026-10-26): tradability + results-window screen for Track A (>= 12k) and Track B (5k-12k).
Inputs: data.json and the data agent's /tmp/run1026 intermediates. Output: /tmp/analyst-2026-10-26/stage1.json"""
import json, os, datetime as dt
B = '/tmp/run1026'
OUT = '/tmp/analyst-2026-10-26'
os.makedirs(OUT, exist_ok=True)
d = json.load(open('/workspace/work/2026-10-26/data.json'))
rows = d['universe_screen']['rows']
tb = d['track_b_5k']['rows']
bh = json.load(open(f'{B}/computed/nse_bhav_summary.json'))
fut = json.load(open(f'{B}/misc/nse_board_future.json'))
past = json.load(open(f'{B}/misc/nse_board_past.json'))
q25 = json.load(open(f'{B}/misc/nse_board_2025q2.json'))
asm = json.load(open(f'{B}/misc/nse_asm.json'))
gsm = {x['symbol'] for x in json.load(open(f'{B}/misc/nse_gsm.json'))}
asmset = {x['symbol']: term + ' ' + x['asmSurvIndicator'] for term in asm for x in asm[term]['data']}
ban = set(l.split(',')[1].strip() for l in open(f'{B}/misc/fo_secban.csv').read().splitlines()[1:] if ',' in l)
W0, W1 = dt.date(2026, 10, 26), dt.date(2026, 11, 16)
PW0, PW1 = dt.date(2025, 10, 26), dt.date(2025, 11, 16)
P = lambda s: dt.datetime.strptime(s, '%d-%b-%Y').date()


def index(lst, results_only=False):
    m = {}
    for x in lst:
        try:
            dd = P(x['bm_date'])
        except Exception:
            continue
        txt = (x.get('bm_purpose') or '') + ' ' + (x.get('bm_desc') or '')
        if results_only and 'esult' not in txt:
            continue
        m.setdefault(x['bm_symbol'], set()).add((dd, (x.get('bm_purpose') or '')[:30]))
    return m


bm = index(fut)
rep = {t: {a for a, _ in v if a >= dt.date(2026, 9, 25)} for t, v in index(past, True).items()}
prior = {t: sorted(a for a, _ in v if dt.date(2025, 9, 25) <= a <= dt.date(2025, 11, 20)) for t, v in index(q25, True).items()}

uni = {}
for t, r in rows.items():
    uni[t] = dict(track='A' if r['mcap_cr'] >= 12000 else 'B', src='N500 tech-pass', mcap=r['mcap_cr'], pledge=r['pledge_pct'])
for t, r in tb.items():
    if t in uni:
        continue
    uni[t] = dict(track='A' if r['mcap_cr'] >= 12000 else 'B', src=r['source_list'] + ' momentum-pass', mcap=r['mcap_cr'], pledge=r['pledge_pct'])
out = {}
for t in sorted(uni):
    u = uni[t]; rs = []
    adv = bh.get(t, {}).get('nse_adv_20s_cr')
    if adv is None:
        adv = (tb.get(t) or {}).get('adv20_cr')
    if adv is None or adv < 25: rs.append(f'ADV {adv}')
    if t in asmset: rs.append('ASM ' + asmset[t])
    if t in gsm: rs.append('GSM')
    if t in ban: rs.append('F&O ban')
    if u['pledge'] is not None and u['pledge'] > 20: rs.append(f"pledge {u['pledge']}")
    inw = sorted(x for x in bm.get(t, []) if W0 <= x[0] <= W1)
    if inw: rs.append('event ' + '; '.join(f'{a:%d-%b} {b}' for a, b in inw))
    reported = sorted(rep.get(t, []))
    pr = prior.get(t, [])
    probable = None
    if not reported and not any('esult' in b or 'Financial' in b for _, b in inw):
        if any(PW0 <= x <= PW1 for x in pr):
            probable = 'prior-year Q2 inside window'
        elif pr and all(x < PW0 for x in pr):
            probable = 'prior-year Q2 already past, nothing filed (overdue)'
    if probable: rs.append('PROBABLE results: ' + probable + ' (' + ','.join(f'{x:%d-%b-%y}' for x in pr) + ')')
    out[t] = dict(u, adv=adv, reasons=rs, reported=[str(x) for x in reported], prior=[str(x) for x in pr],
                  after=[f'{a:%d-%b} {b}' for a, b in sorted(bm.get(t, [])) if a > W1][:2])
    print(f"{u['track']} {t:11s} mc {u['mcap']:>9} adv {adv} | {'PASS' if not rs else 'FAIL ' + ' | '.join(rs)} | rep {out[t]['reported']} | after {out[t]['after']}")
for tr in 'AB':
    print(tr, sum(1 for v in out.values() if v['track'] == tr), 'pass', sorted(t for t, v in out.items() if v['track'] == tr and not v['reasons']))
json.dump(out, open(f'{OUT}/stage1.json', 'w'), indent=1)

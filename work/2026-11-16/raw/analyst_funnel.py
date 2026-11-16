"""Analyst funnel (run 2026-11-16): Stage 1 (tradability + window), Stage 2 (relative value + value-trap filters)
and Stage 3 (momentum) for every universe name: Nifty 500 tech-pass, Microcap-250 momentum-pass, all Setup-C
eligible names (any mcap >= 5k), and Track B (5k-12k). Inputs: data.json + the data agent's /tmp/run1116
intermediates. Output: /tmp/analyst-2026-11-16/funnel.json (+ printed tables)."""
import csv, json, os, sys, datetime as dt
from statistics import median

sys.path.insert(0, os.path.dirname(__file__))
from compute_indicators import parse_chart, compute_from_rows

W = '/agent/repos/stalker/work/2026-11-16'
B = '/tmp/run1116'
OUT = '/tmp/analyst-2026-11-16'
os.makedirs(OUT, exist_ok=True)
d = json.load(open(f'{W}/data.json'))
tech = json.load(open(f'{B}/computed/tech.json'))
scr = json.load(open(f'{B}/computed/screener_fundamentals.json'))
bh = json.load(open(f'{B}/computed/nse_bhav_summary.json'))
qs = json.load(open(f'{B}/computed/quotesummary.json'))
imed = json.load(open(f'{B}/computed/industry_medians.json'))
peer = json.load(open(f'{B}/computed/peer_pb_roe.json'))
spa = json.load(open(f'{B}/computed/setupc_price_action.json'))
pledge = json.load(open(f'{W}/raw/computed/pledge.json'))
sa = json.load(open(f'{W}/raw/computed/forward_pe_sa.json'))
fut = json.load(open(f'{B}/misc/nse_board_future.json'))
q25 = json.load(open(f'{B}/misc/nse_board_2025q2.json'))
ca = json.load(open(f'{B}/misc/nse_corp_actions.json'))
asm = json.load(open(f'{B}/misc/nse_asm.json'))
gsm = {x['symbol'] for x in json.load(open(f'{B}/misc/nse_gsm.json'))}
asmset = {x['symbol']: x['survCode'] for term in asm for x in asm[term]['data']}
ban = set(l.split(',')[1].strip() for l in open(f'{B}/misc/fo_secban.csv').read().splitlines()[1:] if ',' in l)
N500_3M = d['regime']['nifty500']['ret_3m_63s_pct']['value']
SC = d['setup_c_candidates']
pending = set(SC['reported_after_13nov_close_reaction_pending'])
lt3 = set(SC['watch_held_lt3_sessions'])
eligC = set(SC['eligible'])
W0, W1 = dt.date(2026, 11, 16), dt.date(2026, 12, 7)
P = lambda s: dt.datetime.strptime(s, '%d-%b-%Y').date()
micro = {r['Symbol'].strip() for r in csv.DictReader(open(f'{W}/raw/ind_niftymicrocap250_list.csv'))}
n500 = {r['Symbol'].strip() for r in csv.DictReader(open(f'{W}/raw/ind_nifty500list.csv'))}
fin_ind = {r['Symbol'].strip() for r in csv.DictReader(open(f'{W}/raw/ind_niftyfinancelist.csv'))}

events = {}
for x in fut:
    try:
        a = P(x['bm_date'])
    except Exception:
        continue
    if W0 <= a <= W1:
        events.setdefault(x['bm_symbol'], set()).add(f"{a:%d-%b} board: {x['bm_purpose'][:30]}")
for x in ca:
    try:
        a = P(x['exDate'])
    except Exception:
        continue
    if W0 <= a <= W1:
        events.setdefault(x['symbol'], set()).add(f"{a:%d-%b} ex: {x['subject'][:45]}")


# analyst NSE re-query (raw/analyst_nse_recheck.py, 16-Nov): EGMs / postal ballots are not in the board-meeting feed
events.setdefault('IIFL', set()).add('04-Dec EGM: approve Rs 6,414 Cr preferential issue (Blackstone CCPS + promoter warrants)')


def tech_of(t):
    if t in tech:
        return tech[t]
    p = f'{B}/charts/{t}.json'
    if not os.path.exists(p):
        return None
    pc = parse_chart(p)
    return compute_from_rows(pc['rows'], pc['meta']) if pc else None


# industry -> peer PB / ROE medians pooled from any subject on the same screener industry page
ind_peers = {}
for s, v in peer.items():
    href = (scr.get(s) or {}).get('industry_href')
    for p_ in v.get('peers', []):
        ind_peers.setdefault(href, {})[p_['ticker']] = p_


def peer_meds(t):
    v = peer.get(t)
    if v and v.get('peers'):
        ps = [p_ for p_ in v['peers'] if p_['ticker'] != t]
        src = f'subject peers n={len(ps)}'
    else:
        href = (scr.get(t) or {}).get('industry_href')
        ps = [p_ for k, p_ in ind_peers.get(href, {}).items() if k != t]
        src = f'pooled industry peers n={len(ps)}'
    pbs = [p_['pb'] for p_ in ps if p_.get('pb') not in (None, 0)]
    roes = [p_['roe'] for p_ in ps if p_.get('roe') is not None]
    return (median(pbs) if len(pbs) >= 3 else None, median(roes) if len(roes) >= 3 else None, src)


def is_fin(t):
    s = scr.get(t) or {}
    ind = s.get('industry') or {}
    return t in fin_ind or ind.get('Broad Sector') == 'Financial Services' or ind.get('Sector') == 'Financial Services'


# ---------------- universe ----------------
uni = {}
for t, c in tech.items():
    if c.get('tech_pass'):
        uni[t] = {'src': 'N500 tech-pass'}
for t, r in d['track_b_5k']['rows'].items():
    uni.setdefault(t, {'src': r['source_list'] + ' momentum-pass'})
for t in SC['eligible']:
    uni.setdefault(t, {'src': 'Setup-C eligible only'})
    uni[t]['setupC'] = True
for t in d['track_b_5k']['microcap_mcap_ge_12000_belongs_in_track_a']:
    uni.setdefault(t, {'src': 'Microcap>=12k'})

rows = {}
for t, u in sorted(uni.items()):
    s = scr.get(t) or {}
    tc = tech_of(t)
    mc = s.get('market_cap_cr')
    if mc is None and t in d['track_b_5k']['rows']:
        mc = d['track_b_5k']['rows'][t]['mcap_cr']
    track = 'A' if (mc or 0) >= 12000 else ('B' if (mc or 0) >= 5000 else 'X')
    r = dict(t=t, src=u['src'], setupC=t in eligC, track=track, mcap=mc, fin=is_fin(t),
             sub=(s.get('industry') or {}).get('Industry'), close=bh.get(t, {}).get('nse_close_2026-11-13') or (tc or {}).get('close'))
    # ---- Stage 1
    s1 = []
    adv = bh.get(t, {}).get('nse_adv_20s_cr')
    if track == 'X':
        s1.append(f'mcap {mc} < 5,000')
    if adv is None or adv < 25:
        s1.append(f'ADV {adv}')
    if t in asmset:
        s1.append('ASM ' + asmset[t])
    if t in gsm:
        s1.append('GSM')
    if t in ban:
        s1.append('F&O ban')
    pl = (pledge.get(t) or {}).get('value')
    if pl is None:
        pl = s.get('pledged_pct')
    if pl is not None and pl > 20:
        s1.append(f'pledge {pl}')
    if t in pending:
        s1.append('results filed after 13-Nov close; first reaction 16-Nov (inside window)')
    filed = (spa.get(t) or {}).get('results_filing_ts_ist')
    if not filed and s and s.get('quarter_dates') and s['quarter_dates'][-1] != '2026-09-30':
        pr = sorted({x['bm_date'] for x in q25 if x['bm_symbol'] == t and 'esult' in (x.get('bm_purpose') or '')})
        s1.append('PROBABLE results in window: no Sep-26 quarter on screener, no NSE results filing found; prior-year meeting ' + (', '.join(pr) or 'N/A'))
    ev = sorted(events.get(t, []))
    major = [e for e in ev if 'Dividend' not in e]
    if major:
        s1.append('event in window: ' + '; '.join(major))
    r.update(adv=adv, pledge=pl, events=ev, s1=s1)
    # ---- Stage 2
    s2 = []
    pe, pb, roe, de = s.get('pe'), s.get('pb_at_close') or s.get('pb_computed'), s.get('roe'), s.get('debt_to_equity')
    im = imed.get(s.get('industry_href')) or {}
    mpe = im.get('median_pe_top25_mcap')
    mpb, mroe, psrc = peer_meds(t)
    q = qs.get(t) or {}
    fe = q.get('forwardEps')
    fpe = (r['close'] / fe) if (fe and fe > 0 and r['close']) else None
    fpe2 = (sa.get(t) or {}).get('value') if isinstance(sa.get(t), dict) else None
    fpe2 = fpe2 if isinstance(fpe2, (int, float)) else None
    eps = s.get('ttm_eps')
    ocf = s.get('ocf_latest_annual_cr')
    cg = s.get('cagr') or {}
    rc = (cg.get('Compounded Sales Growth') or {}).get('3 Years')
    pc = (cg.get('Compounded Profit Growth') or {}).get('3 Years')
    # net = mean of the FY0 / FY+1 90-day % changes; if neither has a value, FY up30 vs down30 counts
    fy = [x for x in (q.get('eps_revision_check') or []) if x.get('period') in ('0y', '+1y')]
    chg = [x['chg_pct'] for x in fy if isinstance(x.get('chg_pct'), (int, float))]
    if chg:
        rev = sum(chg) / len(chg) < 0
    else:
        up = sum(x.get('up30') or 0 for x in fy); dn = sum(x.get('down30') or 0 for x in fy)
        rev = dn > up if (up or dn) else None
    r['rev_detail'] = [(x['period'], x.get('chg_pct'), x.get('up30'), x.get('down30')) for x in fy]
    r.update(pe=pe, mpe=mpe, pb=pb, mpb=mpb, roe=roe, mroe=mroe, peer_src=psrc, de=de, fpe=fpe, fpe2=fpe2, eps=eps, ocf=ocf,
             rc=rc, pc=pc, down_rev=rev, pe_prem=(pe / mpe - 1) * 100 if pe and mpe else None,
             pb_prem=(pb / mpb - 1) * 100 if pb and mpb else None)
    if pe is None or pe <= 0:
        s2.append(f'PE {pe} (n/m)')
    elif mpe is None:
        s2.append('sub-sector PE median N/A')
    elif pe >= mpe:
        s2.append(f"PE {pe} >= {mpe:.2f} ({r['pe_prem']:+.2f}%)")
    if pb is None or mpb is None:
        s2.append('PB or peer PB median N/A')
    elif pb >= mpb:
        allow = roe is not None and mroe is not None and roe > mroe and pb <= mpb * 1.10
        if not allow:
            s2.append(f"PB {pb:.3f} vs {mpb:.3f} ({r['pb_prem']:+.2f}%)" + ('' if roe is None or mroe is None or roe > mroe else f'; ROE {roe} <= {mroe}'))
    if fpe is None and fpe2 is None:
        s2.append('fwd PE N/A')
    else:
        f_ = fpe if fpe is not None else fpe2
        if f_ >= 20:
            s2.append(f'fwd PE {f_:.2f} >= 20')
        if pe and f_ >= pe:
            s2.append(f'fwd PE {f_:.2f} >= trailing {pe}')
    if eps is not None and eps <= 0:
        s2.append(f'TTM EPS {eps}')
    if not r['fin'] and ocf is not None and ocf <= 0:
        s2.append(f'OCF {ocf}')
    if rc is not None and rc <= 0:
        s2.append(f'3y rev CAGR {rc}%')
    if pc is not None and pc <= 0:
        s2.append(f'3y profit CAGR {pc}%')
    if roe is not None and roe < 12 and (mroe is None or roe < mroe):
        s2.append(f'ROE {roe}')
    if not r['fin'] and de is not None and de >= 1:
        s2.append(f'D/E {de:.2f}')
    if rev:
        s2.append('net downward FY EPS revisions 90d ' + ', '.join(f'{p} {c}%' for p, c, u, dn in r['rev_detail'] if c is not None))
    r['s2'] = s2
    # ---- Stage 3
    s3 = []
    if tc:
        hi = tc['hi52_used']; c = r['close'] or tc['close']
        pbh = (1 - c / hi) * 100
        r.update(pct_below=pbh, d50=tc['dma50'], d200=tc['dma200'], d200chg=tc['dma200_change_20_sessions'], rsi=tc['rsi14'],
                 e20=tc['ema20'], atr=tc['atr14'], r3=tc['ret_3m_63d'], r1=tc['ret_1m_21d'])
        if pbh > 25:
            s3.append(f'{pbh:.2f}% below 52wH')
        if tc['dma50'] is None or c <= tc['dma50']:
            s3.append(f"close {c} <= 50DMA {tc['dma50']}")
        if tc['dma200'] is not None and tc['dma50'] is not None and tc['dma50'] <= tc['dma200'] and not ((tc['dma200_change_20_sessions'] or 0) > 0):
            s3.append('50DMA <= 200DMA and 200DMA falling')
        if tc['ret_3m_63d'] is None or tc['ret_3m_63d'] <= N500_3M:
            s3.append(f"3M {tc['ret_3m_63d'] if tc['ret_3m_63d'] is None else round(tc['ret_3m_63d'], 2)}% <= N500 {N500_3M:.2f}%")
    else:
        s3.append('no chart')
    r['s3'] = s3
    rows[t] = r

json.dump(rows, open(f'{OUT}/funnel.json', 'w'), indent=1, default=str)


def cnt(f):
    return sum(1 for r in rows.values() if f(r))


for tr in 'AB':
    T = [r for r in rows.values() if r['track'] == tr]
    s1 = [r for r in T if not r['s1']]
    s2 = [r for r in s1 if not r['s2']]
    s3 = [r for r in s2 if not r['s3']]
    print(f'Track {tr}: start {len(T)} -> S1 {len(s1)} -> S2 {len(s2)} -> S3 {len(s3)}: {[r["t"] for r in s3]}')
    print('   S2 pass:', [r['t'] for r in s2])
X = [r for r in rows.values() if r['track'] == 'X']
print('mcap<5k in universe:', len(X), [r['t'] for r in X][:30])
C = [r for r in rows.values() if r['setupC']]
print('Setup-C eligible', len(C), 'S2 value pass (ignoring S1):', [r['t'] for r in C if not r['s2']], cnt(lambda r: r['setupC'] and not r['s2']))
print('Setup-C S1 pass', cnt(lambda r: r['setupC'] and not r['s1']), 'S1+S2', [r['t'] for r in C if not r['s1'] and not r['s2']])
print('Setup-C S2+S3 (ignoring S1):', [r['t'] for r in C if not r['s2'] and not r['s3']])

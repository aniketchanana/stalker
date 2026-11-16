"""Analyst arithmetic (run 2026-11-16). Every %, R:R, share count, exposure, P&L and score total quoted in analysis.md
is printed here. Inputs: data.json, /tmp/analyst-2026-11-16/funnel.json (from analyst_funnel.py)."""
import json, math

W = '/agent/repos/stalker/work/2026-11-16'
d = json.load(open(f'{W}/data.json'))
F = json.load(open('/tmp/analyst-2026-11-16/funnel.json'))
qs = json.load(open('/tmp/run1116/computed/quotesummary.json'))
N500_3M = d['regime']['nifty500']['ret_3m_63s_pct']['value']
N500_1M = d['regime']['nifty500']['ret_1m_21s_pct']['value']


def pct(a, b):
    return (a / b - 1) * 100


def rr(e, s, t):
    return (t - e) / (e - s)


def plan(name, e, s, t1, t2):
    risk = e - s
    sh = math.floor(500 / risk)
    print(f"  {name}: entry {e:.2f} stop {s:.2f} ({risk / e * 100:.2f}%) T1 {t1:.2f} R:R {rr(e, s, t1):.2f} T2 {t2:.2f} R:R2 {rr(e, s, t2):.2f} "
          f"shares {sh} exposure {sh * e:,.2f} risk {sh * risk:.2f} maxE(RR2 to T1) {(t1 + 2 * s) / 3:.2f}")
    return sh


print('== Regime')
m = d['market']
for k in ['nifty50', 'nifty500', 'nifty_bank', 'nifty_it', 'nifty_pharma', 'india_vix']:
    c = m[k]['close']['value']
    print(k, c, *[f"{s} {m[k][s]['value']} ({pct(c, m[k][s]['value']):+.2f}%)" for s in ['ema20', 'sma20', 'sma50', 'sma200']],
          'rsi', m[k]['rsi14']['value'], '1M', m[k]['ret_1m_21s_pct']['value'], '3M', m[k]['ret_3m_63s_pct']['value'],
          '52wH', m[k]['52w_high']['value'], f"below 52wH {(1 - c / m[k]['52w_high']['value']) * 100:.2f}%",
          '200chg', m[k]['dma200_change_20_sessions']['value'], '50chg', m[k]['dma50_change_20_sessions']['value'])
v = m['india_vix']['trend_1m']['value']
print('VIX 1M', v['ago_21_sessions'], '->', v['now'], f"{v['change_pct']}%", 'peak 11-Nov 17.56 -> 15.50', f"{pct(15.5, 17.56):.2f}%")
fl = d['regime']['fii_dii_weeks']
print('FII/DII weeks', fl)

print('== SOUTHBANK settlement')
E, S, T1, T2, SH = 51.45, 48.90, 56.82, 58.35, 196
bars = d['followups']['SOUTHBANK_open_position_pick_2026-10-19']['daily_ohlc_nse_bhavcopy_19oct_13nov']
b29 = [b for b in bars if b['date'] == '2026-10-29'][0]
b09 = [b for b in bars if b['date'] == '2026-11-09'][0]
print('29-Oct open', b29['open'], '< T1', b29['open'] < T1, 'high', b29['high'], '| 9-Nov open', b09['open'], '< T2', b09['open'] < T2, 'high', b09['high'])
sess = [b['date'] for b in bars]
print('session index after fill: 29-Oct =', sess.index('2026-10-29'), '| 3-Nov =', sess.index('2026-11-03'), '| 9-Nov =', sess.index('2026-11-09'), '| 11-Nov =', sess.index('2026-11-11'))
for lab, px in [('T1 full (primary)', T1), ('T2 full (ref)', T2), ('horizon close 11-Nov (ref)', 60.46), ('13-Nov close (ref)', 61.86)]:
    pnl = (px - E) * SH
    print(f"  {lab}: exit {px} P&L {pnl:,.2f} ({pct(px, E):.2f}%) R {(px - E) / (E - S):.2f} proceeds {px * SH:,.2f}")
half = SH // 2
pnl_split = (T1 - E) * half + (T2 - E) * (SH - half)
print(f"  split ref {half} @T1 + {SH - half} @T2: P&L {pnl_split:,.2f} ({pnl_split / (E * SH) * 100:.2f}%) R {pnl_split / ((E - S) * SH):.2f}")
print(f"  exposure {E * SH:,.2f} risk {(E - S) * SH:.2f}; capital after primary settlement {50000 + (T1 - E) * SH:,.2f}")
print(f"  T1-hit day high 57.28 vs T1: {pct(57.28, T1):+.2f}%; muhurat high 58.64 >= T2 {58.64 >= T2}, open 58.25 < T2 {58.25 < T2}")

print('== Stage-3 survivors and near misses')
for t in ['HCLTECH', 'LICHSGFIN', 'SOUTHBANK', 'IIFL', 'DCBBANK', 'TANLA', 'UNIONBANK', 'PNB']:
    r = F[t]
    q = qs.get(t, {})
    print(f"  {t}: PE {r['pe']} vs {r['mpe']:.2f} ({r['pe_prem']:+.2f}%) PB {r['pb']:.3f} vs {r['mpb']:.3f} ({r['pb_prem']:+.2f}%) "
          f"fwd {r['fpe']:.2f}/{r['fpe2']} ROE {r['roe']}/{r['mroe']} | close {r['close']} vsE20 {pct(r['close'], r['e20']):+.2f}% "
          f"RSI {r['rsi']:.2f} below52 {r['pct_below']:.2f}% 3M {r['r3']:.2f} RS3M {r['r3'] - N500_3M:+.2f} 1M {r['r1']:.2f} RS1M {r['r1'] - N500_1M:+.2f} "
          f"ATR {r['atr']:.3f} d50 {r['d50']:.2f} d200 {r['d200']:.2f} chg {r['d200chg']:.2f} | TP {q.get('target_mean')} ({pct(q['target_mean'], r['close']):+.2f}%)")
print(f"  HCLTECH Yahoo PE {1378 / 67.59:.2f} vs median 19.87 -> flips; fwd EPS 80.10137 -> {1378 / 80.10137:.2f}")
print(f"  UNIONBANK fwd PE {203 / 28.76739:.4f} vs trailing 7.04 ({pct(203 / 28.76739, 7.04):+.2f}%); fwd EPS needed > {203 / 7.04:.3f} (+{pct(203 / 7.04, 28.76739):.2f}%)")
print(f"  PNB fwd PE {142.81 / 18.51918:.2f} vs 7.18; fwd EPS needed > {142.81 / 7.18:.2f} (+{pct(142.81 / 7.18, 18.51918):.2f}%)")
print(f"  LICHSGFIN Q2 rev {pct(7194, 7179):+.2f}% PAT {pct(1507, 1349):+.2f}%; since prior close {pct(585.1, 493.7):+.2f}%; R:R to 598.2 from 585.1 with 1.5xATR stop {rr(585.1, 585.1 - 1.5 * 17.59, 598.2):.2f}")
print(f"  SOUTHBANK R:R from 61.86 to 62.57 with 1.5xATR stop: {rr(61.86, 61.86 - 1.5 * 1.966, 62.57):.2f}")
print(f"  IIFL 11-Nov {pct(666.25, 627.0):+.2f}%, gave back to 641.1 ({pct(641.1, 666.25):+.2f}%), base width 512.7->637.5 {pct(637.5, 512.7):.2f}%; CCPS conversion 602 vs close {pct(602, 641.1):+.2f}%; raise/mcap {6414 / 27376 * 100:.2f}%")
print(f"  DCBBANK vs EMA20 {pct(233.01, 207.226):+.2f}%; TANLA vs EMA20 {pct(732.9, 632.839):+.2f}%")

print('== HCLTECH hypothetical Setup A (not a pick)')
plan('HCLTECH trigger', 1397.00, 1362.00, 1469.00, 1574.00)
print(f"  stop 1362 = {(1397 - 1362) / 38.733:.2f} ATR; 1.5xATR stop {1397 - 1.5 * 38.733:.2f} -> R:R {rr(1397, 1397 - 1.5 * 38.733, 1469):.2f}")

print('== Watchlist indicative plans')
plan('SOUTHBANK re-entry A', 57.70, 55.30, 62.57, 64.10)
plan('LICHSGFIN A', 547.00, 522.00, 598.20, 646.50)
plan('UNIONBANK A', 191.00, 184.20, 205.25, 216.85)
print(f"  UNIONBANK base 23-Oct..6-Nov {177.3}-{188.9} width {pct(188.9, 177.3):.2f}%; T2 = 205.25 + 11.60 = {205.25 + 11.6:.2f}")
print(f"  SOUTHBANK base 23-Oct..6-Nov 51.70-57.90 height {57.90 - 51.70:.2f}; T2 = 57.90 + 6.20 = {57.90 + 6.2:.2f}")

print('== Scores')
S = {'HCLTECH': (9, 12, 7, 8, 4), 'LICHSGFIN': (22, 9, 15, 5, 7), 'SOUTHBANK': (21, 12, 18, 3, 10), 'IIFL': (21, 8, 12, 4, 10),
     'DCBBANK': (20, 9, 17, 3, 9), 'TANLA': (20, 10, 14, 2, 5), 'UNIONBANK': (15, 12, 18, 6, 10)}
for t, c in S.items():
    print(f"  {t}: {' / '.join(map(str, c))} = {sum(c)}")
print('== Sector ranks')
sec = [x for x in d['sectors']['value'] if x['index'] not in ('Nifty 50', 'Nifty 500', 'Nifty Next 50', 'Nifty Midcap 150', 'Nifty Smallcap 250')]
r1 = [x['index'] for x in sorted(sec, key=lambda x: -x['rs_1m_pp'])]
r3 = [x['index'] for x in sorted(sec, key=lambda x: -x['rs_3m_pp'])]
for nm in ['Nifty PSU Bank', 'Nifty Private Bank', 'Nifty IT', 'Nifty Housing', 'Nifty Financial Services Ex-Bank', 'Nifty MidSmall IT & Telecom', 'Nifty Pharma', 'Nifty Capital Markets']:
    x = [y for y in sec if y['index'] == nm][0]
    print(f"  {nm}: 1M {x['rs_1m_pp']:+.2f} rank {r1.index(nm) + 1}/{len(sec)} | 3M {x['rs_3m_pp']:+.2f} rank {r3.index(nm) + 1}")

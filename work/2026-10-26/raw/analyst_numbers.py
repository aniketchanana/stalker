"""Analyst number checks (run 2026-10-26): regime deltas, sector ranks, SOUTHBANK follow-up P&L / session count,
watchlist status and near-miss arithmetic. Prints only; every figure quoted in analysis.md comes from here or data.json."""
import json, math, datetime as dt
d = json.load(open('/workspace/work/2026-10-26/data.json'))
m = d['market']
for k in ['nifty50', 'nifty500', 'nifty_bank', 'india_vix']:
    c = m[k]['close']['value']
    print(k, c, *[f"{s} {m[k][s]['value']} ({(c / m[k][s]['value'] - 1) * 100:+.2f}%)" for s in ['sma20', 'sma50', 'sma200']])
sec = [x for x in d['sectors']['value'] if x['index'] not in ('Nifty 50', 'Nifty 500', 'Nifty Next 50', 'Nifty Midcap 150', 'Nifty Smallcap 250')]
r1 = sorted(sec, key=lambda x: -x['rs_1m_pp']); r3 = sorted(sec, key=lambda x: -x['rs_3m_pp'])
print('n sectors', len(sec))
print('top5 1M', [(x['index'], x['rs_1m_pp']) for x in r1[:5]]); print('top5 3M', [(x['index'], x['rs_3m_pp']) for x in r3[:5]])
print('bot5 1M', [(x['index'], x['rs_1m_pp']) for x in r1[-5:]]); print('bot5 3M', [(x['index'], x['rs_3m_pp']) for x in r3[-5:]])
for nm in ['Nifty Private Bank', 'Nifty Bank', 'Nifty PSU Bank', 'Nifty Financial Services', 'Nifty IT', 'Nifty Oil & Gas', 'Nifty Media', 'Nifty Pharma']:
    x = [y for y in sec if y['index'] == nm][0]
    print(nm, '1M', x['rs_1m_pp'], 'rank', [y['index'] for y in r1].index(nm) + 1, '| 3M', x['rs_3m_pp'], 'rank', [y['index'] for y in r3].index(nm) + 1)

# SOUTHBANK follow-up
f = d['followups']['SOUTHBANK_pick_2026-10-19']
bars = f['daily_ohlc_nse_bhavcopy']
E, S, T1, T2, SH = 51.45, 48.90, 56.82, 58.35, 196
after = [b for b in bars if b['date'] >= '2026-10-19']
lo = min(b['low'] for b in after); hi = max(b['high'] for b in after); c = after[-1]['close']
print('fill 19-Oct open', after[0]['open'], 'zone 50.70-51.50; 19-Oct close', after[0]['close'], '>= 50.68')
print('low since fill', lo, 'high', hi, 'stop hit', lo <= S, 'T1 hit', hi >= T1)
print('MTM', round((c - E) * SH, 2), f'{(c / E - 1) * 100:.2f}%', 'exposure at entry', round(E * SH, 2), 'value at close', round(c * SH, 2))
print('best close', max(b['close'] for b in after), 'MTM best close', round((max(b['close'] for b in after) - E) * SH, 2), 'MTM at high', round((hi - E) * SH, 2))
print('pct of T1 distance reached at high', round((hi - E) / (T1 - E) * 100, 1), '1R level', E + (E - S), 'closes >= 1R', [b['date'] for b in after if b['close'] >= E + (E - S)])
print('closes >= halfway 54.14', [(b['date'], b['close']) for b in after if b['close'] >= 54.14])
print('23-Oct day ret', round((52.57 / 55.75 - 1) * 100, 2), 'R open', round((c - E) / (E - S), 2), 'R')
hol = json.load(open('/tmp/run1026/misc/calendar.json'))['hol']
sess = []; dd = dt.date(2026, 10, 20)
while len(sess) < 12:
    if dd.weekday() < 5 and str(dd) not in hol:
        sess.append(str(dd))
    dd += dt.timedelta(days=1)
print('sessions after 19-Oct fill', list(enumerate(sess, 1)))
print('remaining risk to stop', round((c - S) * SH, 2), 'stop dist from close %', round((c - S) / c * 100, 2))
print('breakeven 51.45 vs close in ATR', round((c - E) / 2.034, 2))
sb = d['candidates']['SOUTHBANK']
for k in ['ema20', 'dma20', 'dma50', 'dma200', 'rsi14', 'atr14', 'avg_volume_20d', '52w_high', '1m_return_pct', '3m_return_pct']:
    print('SB', k, sb[k]['value'])
print('SB delivery', sb['delivery_pct']['value'])
print('23-Oct vol / 20d avg', round(27651195 / sb['avg_volume_20d']['value'], 2), '2x avg', 2 * sb['avg_volume_20d']['value'])
print('SB 3M RS', round(sb['3m_return_pct']['value'] + 6.765, 2), '1M RS (21s vs N500 21s -5.995)', round(sb['1m_return_pct']['value'] + 5.995, 2))
print('SB % below 52wH', round((1 - 52.57 / 56.25) * 100, 2), 'vs ema20', round((52.57 / sb['ema20']['value'] - 1) * 100, 2))
print('SB PE prem', round((8.68 / 12.425 - 1) * 100, 2), 'PB prem', round((1.141 / 1.4583 - 1) * 100, 2))

# near-miss arithmetic
pnb = d['candidates']['PNB']
print('PNB fwd vs trailing', 6.5, 6.6, 6.05, round((6.5 / 6.05 - 1) * 100, 2), 'PB prem', round((0.8571 / 0.8878 - 1) * 100, 2), 'PE prem', round((6.05 / 6.885 - 1) * 100, 2))
print('PNB vs ema20', round((120.37 / 117.51 - 1) * 100, 2), '3M RS', round(9.28 + 6.765, 2))
print('UNIONBANK PB prem', round((0.9466 / 0.8571 - 1) * 100, 2), 'PE prem', round((6.1965 / 6.885 - 1) * 100, 2), 'fwd', 6.215, 'vs', 6.1965)
print('HCLTECH PE prem', round((20.3 / 22.03 - 1) * 100, 2), 'PB prem', round((5.0786 / 4.7408 - 1) * 100, 2), 'vs ema20', round((1422.2 / 1318.6 - 1) * 100, 2))
print('CHENNPETRO PE prem', round((3.85 / 14.99 - 1) * 100, 2), 'PB prem', round((1.6166 / 1.3629 - 1) * 100, 2))
print('PCJEWELLER PE prem', round((19.7 / 22.67 - 1) * 100, 2), 'peer ROE median (TITAN 37.7, KALYANKJIL 24.8, SKYGOLD 28.9, THANGAMAYL 28.1, BLUESTONE 1.11)', sorted([37.7, 24.8, 28.9, 28.1, 1.11])[2])
print('JUSTDIAL PE prem', round((11.8495 / 13.85 - 1) * 100, 2), 'Q2 PAT yoy', round((108 / 119 - 1) * 100, 2))
for t in ['REDINGTON', 'TANLA', 'JAMNAAUTO']:
    c_ = d['candidates'][t]
    px = c_['price']['value']
    print(t, px, 'd50', c_['dma50']['value'], 'd200', c_['dma200']['value'], 'rsi', c_['rsi14']['value'], '3M', c_['3m_return_pct']['value'], 'mcap', c_['market_cap_cr']['value'],
          'lows', [(b['date'], b['low'], b['close']) for b in c_['last_10_candles']['value'][-6:]])

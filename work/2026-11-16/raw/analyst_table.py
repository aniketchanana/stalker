"""Analyst appendix generator (run 2026-11-16): Stage 1/2/3 rejection lists per track, and the Setup-C value test
on all 134 data-agent 'eligible' names, from /tmp/analyst-2026-11-16/funnel.json. Writes /tmp/analyst-2026-11-16/appendix.md."""
import json, collections

R = json.load(open('/tmp/analyst-2026-11-16/funnel.json'))
out = []
P = out.append


def f(x, n=2):
    return 'N/A' if x is None else f'{x:.{n}f}'


def s1key(x):
    for k, lab in [('ADV', 'ADV < ₹25 Cr'), ('ASM', 'ASM'), ('GSM', 'GSM'), ('pledge', 'Pledge > 20%'),
                   ('results filed after', 'Results filed after the 13-Nov close (first reaction 16-Nov, inside the window)'),
                   ('PROBABLE', 'Results probable in window (no Sep-26 filing; not intimated)'), ('event', 'Major corporate action in window')]:
        if x.startswith(k):
            return lab
    return x


def s2group(s):
    has = lambda p: any(x.startswith(p) for x in s)
    if has('PE ') or has('sub-sector'):
        return '1. PE ≥ sub-sector median (or PE n/m)'
    if has('PB'):
        return '2. PB test (PB ≥ peer median beyond the ROE allowance, or peer median N/A)'
    if has('fwd PE N/A'):
        return '3a. Forward PE N/A (data gap; every such name also fails Stage 3)'
    if has('fwd PE'):
        return '3. Forward PE ≥ 20 or ≥ trailing PE'
    return '4. Value-trap filter'


for tr, title in [('A', 'Track A (≥ ₹12,000 Cr)'), ('B', 'Track B (₹5,000–12,000 Cr, relaxation run)')]:
    T = {t: r for t, r in R.items() if r['track'] == tr}
    P(f'### {title}: start {len(T)}')
    src = collections.Counter(r['src'] for r in T.values())
    P('Universe sources: ' + '; '.join(f'{k} {v}' for k, v in sorted(src.items())) + '.')
    P('')
    fails = {t: r for t, r in T.items() if r['s1']}
    P(f'**Stage 1 rejections ({len(fails)}; {len(T) - len(fails)} survive).** A name can carry more than one reason.')
    P('')
    grp = collections.defaultdict(list)
    for t, r in sorted(fails.items()):
        for x in r['s1']:
            k = s1key(x)
            detail = x.split(' ', 1)[1] if k in ('ADV < ₹25 Cr', 'Pledge > 20%') else (x.split(' ', 1)[1] if k == 'ASM' else '')
            if k.startswith('Major'):
                detail = x.replace('event in window: ', '')
            if k.startswith('Results probable'):
                detail = x.split('prior-year meeting ')[-1]
                detail = 'prior-year ' + detail
            grp[k].append(f'{t}' + (f' ({detail})' if detail else ''))
    for k in sorted(grp):
        P(f'- **{k}** ({len(grp[k])}): ' + ', '.join(grp[k]) + '.')
    P('')
    S1 = {t: r for t, r in T.items() if not r['s1']}
    g2 = collections.defaultdict(list)
    for t, r in sorted(S1.items()):
        if r['s2']:
            g2[s2group(r['s2'])].append((t, r))
    P(f'**Stage 2 ({len(S1)} → {sum(1 for r in S1.values() if not r["s2"])}).** First binding test, in the order PE → PB → forward PE → value-trap filters.')
    P('')
    for k in sorted(g2):
        items = g2[k]
        if k.startswith('1.'):
            txt = ', '.join(f"{t} {('n/m' if r['pe_prem'] is None else format(r['pe_prem'], '+.1f') + '%')}" for t, r in items)
        elif k.startswith('2.'):
            txt = ', '.join(f"{t} ({'peer PB N/A' if r['pb_prem'] is None else ('peer PB median ' + format(r['mpb'], '.3f') + ' ≤ 0, not meaningful' if r['mpb'] <= 0 else 'PB ' + format(r['pb_prem'], '+.1f') + '%')})" for t, r in items)
        elif k.startswith('3.'):
            txt = ', '.join(f"{t} ({f(r['fpe'] if r['fpe'] is not None else r['fpe2'])} vs trailing {r['pe']})" for t, r in items)
        elif k.startswith('3a'):
            txt = ', '.join(t for t, r in items)
        else:
            txt = '; '.join(f"{t} ({', '.join(r['s2'])})" for t, r in items)
        P(f'- **{k}** ({len(items)}): {txt}.')
    S2 = [t for t, r in S1.items() if not r['s2']]
    P(f'- **Pass ({len(S2)}):** ' + ', '.join(S2) + '.')
    P('')
    P('**Stage 3:** ' + '; '.join(f"{t} {'passes' if not R[t]['s3'] else 'fails: ' + ', '.join(R[t]['s3'])}" for t in S2) + '.')
    P('')

C = {t: r for t, r in R.items() if r['setupC']}
P(f'### Setup-C value test on all {len(C)} data-agent "eligible" names')
P(f"Track A {sum(1 for r in C.values() if r['track'] == 'A')}, Track B {sum(1 for r in C.values() if r['track'] == 'B')}. "
  f"Stage 1 (ignoring the waived results window): {sum(1 for r in C.values() if not r['s1'])} pass; fails: "
  + ', '.join(f"{t} ({'; '.join(r['s1'])})" for t, r in sorted(C.items()) if r['s1']) + '.')
P('')
g = collections.defaultdict(list)
for t, r in sorted(C.items()):
    g[s2group(r['s2']) if r['s2'] else 'Pass'].append(t)
for k in sorted(g):
    P(f'- **{k}** ({len(g[k])}): ' + ', '.join(g[k]) + '.')
P('')
P(f"Stage 3 on the full 134 (for reference): {sum(1 for r in C.values() if not r['s3'])} pass. Stage 2 ∩ Stage 3: "
  + ', '.join(t for t, r in sorted(C.items()) if not r['s2'] and not r['s3']) + '.')
open('/tmp/analyst-2026-11-16/appendix.md', 'w').write('\n'.join(out) + '\n')
print('\n'.join(out))

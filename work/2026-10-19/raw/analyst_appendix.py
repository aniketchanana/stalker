import json
d=json.load(open('/workspace/work/2026-10-19/data.json'))
rows=d['universe_screen']['rows']; tb=d['track_b_5k']['rows']
s1=json.load(open('/tmp/analyst-2026-10-19/stage1.json')); s1b=json.load(open('/tmp/analyst-2026-10-19/stage1b.json'))
pr=json.load(open('/tmp/analyst-2026-10-19/prior.json'))
def fmt(x): return 'N/A' if x is None else (f'{x:+.1f}%')
A=[];B=[]
for t,v in s1.items():
    if v['reasons']: continue
    if pr[t][1] or (pr[t][0].startswith('prior 17-Oct')): continue
    A.append(t)
for t,(g,r) in s1b.items():
    if r: continue
    if pr[t][1] or pr[t][0].startswith('prior 17-Oct'): continue
    (A if g=='A_ext' else B).append(t)
print('A',len(A),sorted(A)); print('B',len(B),sorted(B))
print('--- probable (prior-year) exclusions')
for t,v in pr.items():
    if v[1] or v[0].startswith('prior 17-Oct'): print(t, v[0])
print('--- A stage2 PE')
for t in sorted(A):
    r=rows.get(t) or tb.get(t)
    pe=r['pe']; ind=r['industry_pe_top25']
    prem=None if (pe is None or ind is None) else (pe/ind-1)*100
    print(t, pe, ind, fmt(prem))
print('--- B stage2 PE')
for t in sorted(B):
    r=tb[t]; pe=r['pe']; ind=r['industry_pe_top25']
    prem=None if (pe is None or ind is None) else (pe/ind-1)*100
    print(t, pe, ind, fmt(prem), 'roe',r['roe'])

import json,datetime as dt
q=json.load(open('/tmp/swing-2026-10-19/misc/nse_board_2025q2.json'))
past=json.load(open('/tmp/swing-2026-10-19/misc/nse_board_past.json'))
s1=json.load(open('/tmp/analyst-2026-10-19/stage1.json'))
s1b=json.load(open('/tmp/analyst-2026-10-19/stage1b.json'))
P=lambda s: dt.datetime.strptime(s,'%d-%b-%Y').date()
prior={}
for x in q:
    if 'Financial Results' in (x.get('bm_purpose') or ''):
        try: dd=P(x['bm_date'])
        except: continue
        if dt.date(2025,9,25)<=dd<=dt.date(2025,11,20):
            prior.setdefault(x['bm_symbol'],set()).add(dd)
rep={}  # already reported Q2 FY27 in 2026 (past file)
for x in past:
    if 'Financial Results' in (x.get('bm_purpose') or ''):
        try: dd=P(x['bm_date'])
        except: continue
        if dd>=dt.date(2026,9,25): rep.setdefault(x['bm_symbol'],set()).add(dd)
print('prior-range in file', min(min(v) for v in prior.values()), max(max(v) for v in prior.values()))
surv=[t for t,v in s1.items() if not v['reasons']]+[t for t,(g,r) in s1b.items() if not r]
out={}
for t in surv:
    if t in rep: out[t]=('reported '+','.join(f'{x:%d-%b}' for x in sorted(rep[t])),False); continue
    p=sorted(prior.get(t,[]))
    inw=any(dt.date(2025,10,19)<=x<=dt.date(2025,11,9) for x in p)
    out[t]=('prior '+','.join(f'{x:%d-%b-%y}' for x in p) if p else 'prior N/A', inw)
for t,v in out.items(): print(f'{t:11s} {v[0]:30s} {"PROBABLE-IN-WINDOW" if v[1] else ""}')
json.dump(out,open('/tmp/analyst-2026-10-19/prior.json','w'),indent=1)

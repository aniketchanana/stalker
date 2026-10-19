import json,datetime as dt
d=json.load(open('/workspace/work/2026-10-19/data.json'))
rows=d['universe_screen']['rows']
bh=json.load(open('/tmp/swing-2026-10-19/computed/nse_bhav_summary.json'))
fut=json.load(open('/tmp/swing-2026-10-19/misc/nse_board_future.json'))
past=json.load(open('/tmp/swing-2026-10-19/misc/nse_board_past.json'))
asm=json.load(open('/tmp/swing-2026-10-19/misc/nse_asm.json'))
asmset={}
for term in asm:
    for x in asm[term]['data']: asmset[x['symbol']]=term+' '+x['asmSurvIndicator']
ban=set(d['surveillance']['fo_ban_trade_date_2026-10-19']['value'])
ca=json.load(open('/tmp/swing-2026-10-19/misc/nse_corp_actions.json'))
W0,W1=dt.date(2026,10,19),dt.date(2026,11,9)
def P(s): return dt.datetime.strptime(s,'%d-%b-%Y').date()
bm={}
for x in fut:
    try: dd=P(x['bm_date'])
    except: continue
    bm.setdefault(x['bm_symbol'],set()).add((dd,x['bm_purpose'][:40]))
pastbm={}
for x in past:
    try: dd=P(x['bm_date'])
    except: continue
    pastbm.setdefault(x['bm_symbol'],set()).add((dd,x['bm_purpose'][:30]))
out={}
for t in sorted(rows):
    r=rows[t]; reasons=[]
    adv=bh.get(t,{}).get('nse_adv_20s_cr')
    if adv is None or adv<25: reasons.append(f'ADV {adv}')
    if t in asmset: reasons.append('ASM '+asmset[t])
    if t in ban: reasons.append('F&O ban')
    pl=r.get('pledge_pct')
    if pl is not None and pl>20: reasons.append(f'pledge {pl}')
    if r['mcap_cr']<12000: reasons.append('mcap')
    inw=sorted([x for x in bm.get(t,[]) if W0<=x[0]<=W1])
    if inw: reasons.append('event '+'; '.join(f'{a:%d-%b} {b}' for a,b in inw))
    post=sorted([x for x in bm.get(t,[]) if x[0]>W1])
    pst=sorted(pastbm.get(t,[]))
    out[t]=dict(adv=adv,reasons=reasons,after=[f'{a:%d-%b} {b}' for a,b in post][:2],past=[f'{a:%d-%b} {b}' for a,b in pst][-2:])
    print(f"{t:11s} adv {adv} | {'PASS' if not reasons else 'FAIL '+' | '.join(reasons)} | after {out[t]['after']} | past {out[t]['past']}")
json.dump(out,open('/tmp/analyst-2026-10-19/stage1.json','w'),indent=1)
print(sum(1 for v in out.values() if not v['reasons']))

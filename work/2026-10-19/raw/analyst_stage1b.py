import json,datetime as dt
d=json.load(open('/workspace/work/2026-10-19/data.json'))
tb=d['track_b_5k']['rows']
bh=json.load(open('/tmp/swing-2026-10-19/computed/nse_bhav_summary.json'))
fut=json.load(open('/tmp/swing-2026-10-19/misc/nse_board_future.json'))
asm=json.load(open('/tmp/swing-2026-10-19/misc/nse_asm.json'))
asmset={}
for term in asm:
    for x in asm[term]['data']: asmset[x['symbol']]=term+' '+x['asmSurvIndicator']
ban=set(d['surveillance']['fo_ban_trade_date_2026-10-19']['value'])
W0,W1=dt.date(2026,10,19),dt.date(2026,11,9)
P=lambda s: dt.datetime.strptime(s,'%d-%b-%Y').date()
bm={}
for x in fut:
    try: dd=P(x['bm_date'])
    except: continue
    bm.setdefault(x['bm_symbol'],set()).add(dd)
res={}
for grp,cond in [('A_ext',lambda m:m>=12000),('B',lambda m:5000<=m<12000)]:
    print('==',grp)
    n=0
    for t,r in sorted(tb.items()):
        if not cond(r['mcap_cr']): continue
        n+=1
        rs=[]
        adv=r['adv20_cr']
        if adv is None or adv<25: rs.append(f'ADV {adv}')
        if t in asmset: rs.append('ASM '+asmset[t])
        if t in ban: rs.append('ban')
        if r['pledge_pct'] is not None and r['pledge_pct']>20: rs.append(f"pledge {r['pledge_pct']}")
        inw=sorted(x for x in bm.get(t,[]) if W0<=x<=W1)
        if inw: rs.append('results '+','.join(f'{x:%d-%b}' for x in inw))
        aft=sorted(x for x in bm.get(t,[]) if x>W1)
        res[t]=(grp,rs)
        print(f"{t:11s} mc {r['mcap_cr']} {'PASS' if not rs else 'FAIL '+' | '.join(rs)} {('after '+str(aft[0])) if aft else ''}")
    print(grp,n, sum(1 for t,(g,rs) in res.items() if g==grp and not rs))
json.dump(res,open('/tmp/analyst-2026-10-19/stage1b.json','w'),indent=1)

import json, math
d=json.load(open('/workspace/work/2026-10-19/data.json'))
m=d['market']
for k in ['nifty50','nifty500']:
    c=m[k]['close']['value']
    for s in ['sma20','sma50','sma200']:
        print(k,s,m[k][s]['value'], f"{(c/m[k][s]['value']-1)*100:+.2f}%")
sec=[x for x in d['sectors']['value'] if x['index'] not in ('Nifty 50','Nifty 500','Nifty Next 50','Nifty Midcap 150','Nifty Smallcap 250')]
r1=sorted(sec,key=lambda x:-x['rs_1m_pp']); r3=sorted(sec,key=lambda x:-x['rs_3m_pp'])
for nm in ['Nifty Private Bank','Nifty Bank','Nifty Financial Services','Nifty Auto','Nifty IT','Nifty MidSmall IT & Telecom']:
    print(nm,'1M rank',[x['index'] for x in r1].index(nm)+1,'/',len(sec),'3M rank',[x['index'] for x in r3].index(nm)+1)
# trade plan
E,S=51.45,48.90
T1=50.68+(50.68-44.54); T2=50.68+(50.68-43.01)
risk=E-S; sh=math.floor(500/risk)
print('T1',round(T1,2),'T2',round(T2,2),'risk',round(risk,2),'stop%',round(risk/E*100,2),'RR1',round((T1-E)/risk,2),'RR2',round((T2-E)/risk,2),'shares',sh,'exp',round(sh*E,2),'riskRs',round(sh*risk,2))
print('max entry for RR2', round((T1+2*S)/3,2), 'halfway', round((E+T1)/2,2))
print('base width', round((50.68-44.54)/44.54*100,2), 'broad', round((50.68-43.01)/43.01*100,2))
print('vs ema20', round((E/48.48-1)*100,2), 'atr1.5', round(E-1.5*1.699,2), '2x', round(E-2*1.699,2))
print('2x avg vol', 2*19786427)
# low end of zone
E2=50.70; print('zone low RR', round((T1-E2)/(E2-S),2), math.floor(500/(E2-S)))
# JAMNAAUTO indicative
E,S,T=134.5,127.4,148.9; print('JAMNA RR',round((T-E)/(E-S),2), math.floor(500/(E-S)), round(math.floor(500/(E-S))*E,1), round((E-S)/E*100,2), '152.6/154 RR', round((154-E)/(E-S),2))
# REDINGTON indicative
S=376.0; T=419.5; Emax=(T+2*S)/3; print('RED maxE',round(Emax,2)); E=390.5; print(round((T-E)/(E-S),2), math.floor(500/(E-S)), round(math.floor(500/(E-S))*E,1), round((E-S)/E*100,2))
print('SOUTHBANK 1M RS', 13.85+1.163, '3M RS', 15.36+4.569)
print('JAMNA 3M RS', 6.91+4.569, 'TANLA', -4.26+4.569, 'REDINGTON', 39.43+4.569)
print('pct below 52wH SB', round((1-51.45/52.5)*100,2))

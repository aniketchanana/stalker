import json
d=json.load(open('/workspace/work/2026-10-19/data.json'))
C=d['candidates']
def v(c,k):
    x=c.get(k)
    if isinstance(x,dict) and 'value' in x: return x['value']
    return x
rows=[]
for t,c in C.items():
    nr=v(c,'next_results_date')
    rev=v(c,'eps_revisions')
    rows.append(dict(t=t,roles=','.join(c.get('roles',[])),sub=v(c,'sub_sector'),px=v(c,'price'),mcap=v(c,'market_cap_cr'),adv=v(c,'adv_20d_value_cr'),
      nr=(nr.get('date'),nr.get('confirmed'),nr.get('in_15_session_window')) if isinstance(nr,dict) else nr,
      sv=v(c,'asm_gsm_fo_ban_status'),pl=v(c,'promoter_pledge_pct'),
      pe=v(c,'PE'),mpe=v(c,'sub_sector_median_PE'),pb=v(c,'PB'),mpb=v(c,'sub_sector_median_PB'),roe=v(c,'ROE'),mroe=v(c,'sub_sector_median_ROE'),
      fpe=v(c,'forward_PE'),fpe2=v(c,'forward_PE_second_source'),de=v(c,'D/E'),ocf=v(c,'operating_cash_flow_cr'),eps=v(c,'TTM_EPS'),
      rc=v(c,'3y_revenue_CAGR_pct'),pc=v(c,'3y_profit_CAGR_pct'),
      h52=v(c,'52w_high'),e20=v(c,'ema20'),d50=v(c,'dma50'),d200=v(c,'dma200'),r200=(v(c,'dma200_slope') or {}).get('rising'),rsi=v(c,'rsi14'),atr=v(c,'atr14'),r3=v(c,'3m_return_pct')))
for r in rows:
    fp2=r['fpe2'] if not isinstance(r['fpe2'],dict) else r['fpe2'].get('value')
    print(f"{r['t']:11s}|{r['roles'][:22]:22s}|{str(r['sub'])[:24]:24s}|px {r['px']}|mc {r['mcap']}|adv {r['adv']}|res {r['nr']}|sv {r['sv']}|pl {r['pl']}")
    print(f"            PE {r['pe']} vs {r['mpe']} | PB {r['pb']} vs {r['mpb']} | ROE {r['roe']} vs {r['mroe']} | fPE {r['fpe']} / {fp2} | DE {r['de']} OCF {r['ocf']} EPS {r['eps']} CAGR {r['rc']}/{r['pc']}")
    try: pbh=(1-r['px']/r['h52'])*100
    except: pbh=None
    print(f"            52wH {r['h52']} ({pbh if pbh is None else round(pbh,2)}%) e20 {r['e20']} d50 {r['d50']} d200 {r['d200']} rising {r['r200']} rsi {r['rsi']} atr {r['atr']} 3M {r['r3']}")

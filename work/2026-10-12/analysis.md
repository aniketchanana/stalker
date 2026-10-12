# Weekly swing research — NSE — run 2026-10-12 (IST)

**DATA_MODE:** WEB (screener / screener-core MCP absent).
**Prices / indicators as-of:** last completed NSE session **Fri 2026-10-09**. Results-season exclusion window: 15 sessions, **12 Oct – Mon 2 Nov 2026** (20 Oct Dussehra excluded).
**Capital:** ₹50,000 | risk/trade ₹500 (1%) | max 5 names | total exposure cap ₹50,000 | horizon 1–3 weeks.

# No qualifying trade this week

Cash is the position. The regime is **RISK-OFF**, which caps the book at 2 ideas. Two tracks were screened: the Nifty 500 at the ₹12,000 Cr floor, and the Nifty Microcap 250 at the ₹5,000 Cr floor. The relaxation was triggered because Stage 3 had fewer than 10 survivors. Across both tracks, only **REDINGTON** and **JAMNAAUTO** pass relative value, quality and momentum together. Neither is tradeable as of the 9 Oct close:

- **REDINGTON** is pulling back toward its 50 DMA, but there is no reversal candle and RSI is still falling (Setup A not triggered).
- **JAMNAAUTO** has a marginal Setup B breakout. Its reward to the nearest resistance is **0.74:1** (1.34:1 even to the 154 high), short of the 2:1 minimum.

No ticker is eligible for a score ≥ 65 as a pick.

```yaml
SUMMARY:
  regime: RISK-OFF
  data_mode: WEB
  data_as_of: "2026-10-09"
  run_date_ist: "2026-10-12"
  mcap_floor_relaxed: true          # Stage 3 < 10 at Rs12,000 Cr; Track B = Nifty Microcap 250 at >= Rs5,000 Cr
  funnel:                           # Track A (Nifty 500 tech-pass, >=12k) + Track B (Microcap 250 momentum-pass, >=5k)
    start: 126                      # 73 + 53
    stage1: 75                      # 47 + 28
    stage2: 2                       # REDINGTON (A) + JAMNAAUTO (B)
    stage3: 2
    stage4: 1                       # JAMNAAUTO (Setup B, marginal)
    final: 0
  picks: []
  total_exposure: 0
  near_misses_scored:               # NOT picks - each fails a hard gate
    - {ticker: REDINGTON, score: 66.5, eligible: false, gate_failed: "Stage 4 - Setup A not triggered (no reversal, RSI falling)"}
    - {ticker: JAMNAAUTO, score: 62, eligible: false, gate_failed: "Stage 6 - R:R to T1 148.9 = 0.74 (< 2)"}
  watchlist: [REDINGTON, SOUTHBANK, JAMNAAUTO]
  incomplete: false
```

---

## 1. Market regime

**RISK-OFF.** Nifty 50 **22,520.45** is below SMA20 22,972.44 (−1.97%), SMA50 23,726.47 (−5.08%) and SMA200 24,271.24 (−7.21%), with RSI14 36.5. Its 52w low of 22,179.9 was printed on **8 Oct**. Nifty 500 **21,866.65** is below SMA20 22,402.45 (−2.39%), SMA50 23,055.70 (−5.16%) and SMA200 22,916.66 (−4.58%). Nifty 500 returns: 1M **−5.364%**, 3M **−6.346%**. The +0.44% weekly gain only snapped an 8-week losing streak.

**VIX / breadth / flows.** India VIX **14.38** vs SMA20 12.94 / SMA50 12.06; 1M **+28.05%** (11.23 on 8 Sep), peak 15.28 on 8 Oct. Breadth: **17.84%** (89/499) of Nifty 500 above 50 DMA, 19.44% above 20 DMA, 38.37% above 200 DMA, Nifty 50 14% (7/50). Cross-checks: Punji 18%, IndexBreadth 16.0%, Flash Finance 20.2%. FII cash flow was **−₹3,568.9 Cr** on 9 Oct, **−₹30,294 Cr** for the week (8th straight week) and **−₹39,779 Cr** October-to-date. DIIs bought **+₹30,313 Cr** for the week. RBI **hiked repo 25 bp to 5.50%** on 7 Oct. Brent **$104.72**, USDINR **96.82**. Fed decision 28 Oct.

**Leading sectors (RS vs Nifty 500, pp, 1M / 3M).** Media **+6.19 / +11.00**, IT **+0.99 / +8.36**, Pharma **+1.95 / +7.47**, Private Bank **+4.45 / +3.28**, PSU Bank **+1.96 / +2.50**. Favour these for any long. Laggards: Auto 1M **−5.13**, Defence −4.56, Realty −4.51 / −8.00, Metal −3.42, Cement 3M −6.57. RISK-OFF caps the book at **2 ideas**; this week the correct count is **0**.

---

## 2. Funnel

**Why two tracks.** At the ₹12,000 Cr floor, only **1** name (REDINGTON) survived Stage 3, fewer than 10, so the method's mcap relaxation to **₹5,000 Cr** applies.

- Within the Nifty 500 the relaxation adds **0** names: all 73 technical-pass names already exceed ₹12,000 Cr, so every ₹5,000–12,000 Cr Nifty 500 name had already failed the momentum rules.
- The data agent did not cover the ₹5,000–12,000 Cr band outside the Nifty 500. I fetched it myself: the **Nifty Microcap 250** list, Yahoo charts for all 250, screener pages for 44 names plus 11 peers, and 17 industry pages (details in the last section).
- In Track B, the Stage 3 momentum test was applied first for efficiency. Every Track B survivor is re-checked against all stages.

| Stage | Left | Tickers | What dropped |
|---|---:|---|---|
| 0 regime | — | RISK-OFF | Book capped at 2; cash preferred |
| Start | **126** | A: 73 Nifty 500 technical-pass (data.json `universe_screen`); B: 53 Microcap 250 names passing Stage 3 momentum | B: 197 of 250 failed momentum (4 charts 404) |
| **1 tradability** | **75** (A 47 + B 28) | Appendix A | **A (−26):** ADV < ₹25 Cr: ASAHIINDIA 12.07, KPIL 24.13. Pledge > 20%: KPIL 24.55%, NUVAMA 62.8%. ASM: CUPID, HFCL, MTARTECH, SANSERA, STLTECH, WELCORP. F&O ban 12 Oct: LICHSGFIN. Results within window: RBLBANK 12 Oct, BHEL 14, MRPL 14, KARURVYSYA 15, PERSISTENT 15, URBANCO 16, CHENNPETRO 22, CYIENT 22, COFORGE 23, STLTECH 23, CASTROLIND 24, KOTAKBANK 24, RADICO 27, ADANIPORTS 28, CUB 28, APARINDS 29, NAVINFLUOR 30. **B (−25):** ADV < ₹25 Cr: CEIGALL 13.80, GODREJAGRO 14.09, HERITGFOOD 23.57, IIFLCAPS 21.39, MBAPL 13.91, SGMART 18.54, SPLPETRO 23.17, THELEELA 21.11, VMART 6.96. ASM (full NSE list, 199 entries): AVALON, CENTUM, PAISALO, PCJEWELLER, SHILPAMED, SHREEJISPG, SIGMAADV, SKYGOLD, SUNFLAG. Results within window: AEROFLEX 14 Oct, **SOUTHBANK 15 Oct**, WESTLIFE 23, AARTIPHARM 28, INDGN 29, GNFC 2 Nov. Pledge: **STAR 38.1%** (also last year's Q2 was 31 Oct 2025, so Q2 FY27 is probably inside the window). |
| **2 relative value + quality** | **2** | **REDINGTON**, **JAMNAAUTO** | A: 39 fail PE < sub-sector median or have no usable median (appendix B). Of the 8 PE-cheap names, 7 fail a hard test (appendix C). B: 27 of 28 fail (appendix D). |
| **3 momentum** | **2** | REDINGTON, JAMNAAUTO | — (both within 25% of 52w high, above 50 DMA, 50 DMA > 200 DMA, 3M > −6.346%) |
| **4 swing setup** | **1** | JAMNAAUTO (Setup B, marginal) | **REDINGTON:** pullback on falling volume, but RSI is falling (49.70 → 45.96) and the 9 Oct candle is bearish (O 388.10, C 380.00, near its low of 377.95). No reversal yet, so Setup A is not triggered. |
| **Final (score ≥ 65, stop ≤ 8%, R:R ≥ 2)** | **0** | **No qualifying trade** | **JAMNAAUTO:** entry 142.67, logical stop 134.2 (5.94%). T1 = 148.9 (Aug-2026 swing high) gives R:R **0.74**; even T1 = 154.0 (7 Oct high) gives **1.34**. To reach 2:1, entry would have to be ≤ 140.8, which is back inside the base (below 141.75) and would invalidate the breakout. Rejected. |

**Filters not silently loosened.** The smallest relaxations that would re-open research (not applied):

1. A ±2% tolerance on the PE-vs-median test would admit **PNBHOUSING** (PE 13.0 vs 12.85, +1.17%; PB 1.57 vs 1.88; ROE 12.7%). Its results date is unconfirmed and it has no Stage-4 setup. Its 9 Oct close of 1158.0 is 2.7% above EMA20 1127.17, RSI 56.9.
2. Letting a regas business justify a negative 3y revenue CAGR would admit **PETRONET**. Its 6 Oct breakout above ~293 failed (close back at 288.50 on 8 Oct), and R:R to 299.6 from 291.5 is **0.81**.

Neither relaxation produces a legal book.

---

## 3. Shortlist table

No ticker qualifies (score ≥ 65 **and** all hard gates). Empty by design.

| Ticker | Sub-sector | Mcap (₹Cr) | PE prem vs sub-sector | PB prem vs sub-sector | Fwd PE | % below 52W high | 3M RS vs Nifty 500 | Setup (A/B/C) | Score |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| — | — | — | — | — | — | — | — | — | — |

**Closest scored near-misses (NOT picks; each fails a hard gate).** Scores are shown for reference only.

| Ticker | Sub-sector | Mcap (₹Cr) | PE prem | PB prem | Fwd PE | % below 52W high | 3M RS (pp) | Setup | Score | Gate failed |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|
| REDINGTON | Trading & Distributors | 29,707 | −48.2% (16.5 vs 31.84, n=20) | −39.5% (2.92 vs 4.83, n=12) | 12.43 | 9.42% | +41.87 | none (A forming) | 66.5 | Stage 4 |
| JAMNAAUTO | Auto Components & Equipments | 5,707 | −51.0% (23.65 vs 48.22, n=25) | −38.9% (4.97 vs 8.14, n=11) | 18.53 | 7.36% | +10.82 | B (marginal) | 62 | Stage 6 R:R |

**Score breakdown** (Relative value 25 / Quality 15 / Momentum & RS 20 / Setup & R:R 25 / Catalysts 15):

- **REDINGTON:** 25 / 10 / 18.5 / 4 / 9.
  - Quality lost points on OCF of ₹231 Cr vs roughly ₹1,701 Cr TTM PAT (OCF/PAT 0.14) and a 5% 3y profit CAGR.
  - Momentum: sector is neutral (no direct sector index).
  - Setup: partial only.
  - Catalysts: 5/5 Buy, mean TP 438.8 (+15.5%); ownership mixed; no event in 1–3 weeks.
- **JAMNAAUTO:** 22 / 13 / 15 / 9 / 3.
  - Momentum: Auto is a bottom-5 sector on 1M RS (0 points for sector).
  - Setup: marginal B, R:R 0.74.
  - Catalysts: n=1 analyst; FII −0.24 pp and DII −0.92 pp (Mar→Jun 2026).

---

## 4. Final picks

**None.** Do not allocate the ₹50,000 this week. Reasons:

- RISK-OFF tape: breadth 17.8% above 50 DMA, VIX 1M +28%, eight straight weeks of FII selling, RBI hiking.
- Q2 results begin in earnest (HDFC Bank, ICICI Bank and Axis Bank on 17 Oct).
- The only two fully cheap-and-sound names have no legal entry today.

---

## 5. Watchlist (3 near-misses)

None of these are orders. Each lists the exact additional conditions required.

### REDINGTON (Trading & Distributors): closest to Setup A

- **As-of 9 Oct:**
  - Price: close **380.00**; EMA20 393.49 (−3.43%); DMA50 **370.43**, rising (+49.58 over 20 sessions); DMA200 279.49, rising; RSI14 45.96; ATR14 15.458.
  - Highs and returns: 52w high **419.5** (23 Sep; 9.42% below); 3M +35.52% vs −6.35%.
  - Valuation and quality: PE 16.5 vs 31.84; PB 2.92 vs 4.83; fwd PE 12.43 (< 20 and < trailing); ROE 16.9% vs 13.405%; D/E 0.28; 3y sales/profit CAGR 15%/5%; pledge N/A (no promoter group).
  - Liquidity: ADV ₹225.53 Cr; delivery 35.2% on 9 Oct vs 43.29% 20-day average.
  - Analysts: 5/5 Buy, TP 438.8 (380–505).
- **Bars:** swing low 371.20 (16 Sep). 8 Oct C 388.00 (−4.6%) and 9 Oct C 380.00 came on falling volume (0.53× and 0.51× the 20-day average). That is a clean, quiet pullback, but it is unconfirmed.
- **Would qualify only if all of the following hold:**
  1. Q2 FY27 results date is confirmed **after 2 Nov**. Prior Q2 dates: 5 Nov 2025, 29 Oct 2024, 6 Nov 2023; TipRanks estimates 10 Nov 2026. A board-meeting intimation dated on or before 2 Nov removes the name.
  2. A bullish reversal close prints, by **23 Oct**: a close above the prior session's high, or a bullish engulfing candle. The session low must hold **≥ 371.20**, RSI14 must turn up while in 40–55, and reversal-day volume should be ≥ 1.0× the 20-day average (5.66 mn shares).
  3. The reversal close is **≤ 385.5**, which is what makes R:R ≥ 2 to T1 **419.5** with stop **368.5** (below 371.20 and the 50 DMA).
- **Indicative plan if all conditions trigger:**
  - Entry 385.5, stop 368.5 (4.41%), T1 419.5, T2 467.8 (measured move: base 371.2–419.5 + 48.3).
  - Size: 29 shares, ₹11,180 exposure.
- **Kill levels:** a close below 368.5, or no trigger by 23 Oct.

### SOUTHBANK (Private Sector Bank; relaxed-universe, mcap ₹12,555 Cr): post-results Setup C candidate

- **Excluded this week:** results on **15 Oct** (Stage 1).
- **As-of 9 Oct:**
  - Price: close **47.91**; EMA20 47.31; DMA50 46.53; DMA200 42.77, rising; RSI14 53.80; ATR14 1.534.
  - Highs and returns: 52w high **50.68** (25 Sep); 3M +4.58% (RS +10.93 pp); sector Private Bank 1M RS +4.45 pp.
  - Valuation: PE 8.32 at the 9 Oct close vs 13.96 (−40%); PB **1.06** vs 1.66 (−36%); fwd PE **6.82** (< trailing).
  - Quality: ROE 13.5% vs 11.5%. Q1 FY27: GNPA **1.38%** (3.15% a year earlier), NNPA **0.26%** (0.68%), CRAR **19.62%**, PAT +17.3%, NII +23%.
  - Ownership: FII +1.18 pp, DII +1.49 pp (Mar→Jun 2026).
  - Analysts: 3 Buy / 3 Hold; mean TP **47.0, below the price**.
- **Bars:** 24 Sep breakout on 4.0× volume. Pullback to EMA20 with a bullish 9 Oct candle (L 46.15, C 47.91, H 48.24).
- **Today's geometry fails.** With stop 45.85 (below the 46.15 low), R:R to 50.68 is **1.34**. Pre-results, it would need entry ≤ 47.4 (R:R 2.12), but the 15 Oct event blocks it.
- **Would qualify (Setup C) only if all of:**
  1. Q2 FY27 results on 15 Oct show YoY growth in both NII/total income and PAT, with GNPA/NNPA no worse than 1.38%/0.26%.
  2. A gap-up opens on 16 Oct above the 15 Oct high.
  3. Closes stay above the gap level on 16, 19 and 21 Oct.
  4. On 21 Oct, the stop below the gap-day low is ≤ 8% and R:R to the nearest resistance is ≥ 2. If it breaks out above 50.68, use a measured-move T1.

### JAMNAAUTO (Auto Components; relaxed-universe, mcap ₹5,707 Cr): Setup B failed R:R; watching for Setup A at the 50 DMA

- **As-of 9 Oct:**
  - Price: close **142.67**; base 122.40–141.75 (14 Sep–5 Oct, 15.8% wide); breakout closes 144.21 (6 Oct, 1.56× volume) and 151.77 (7 Oct, 3.13× volume, high **154.0**); then 147.95 and 142.67 on fading volume.
  - Indicators: EMA20 136.56; DMA50 130.19; DMA200 127.95; RSI14 58.54; ATR14 6.342.
  - Delivery on breakout days was 37.25% and 29.51%, vs a 20-day average of 37.48%. Below-average delivery weakens the breakout.
  - Overhead resistance: 148.9 (Aug 2026 swing high), 152.6 (Feb 2026), 154.0.
  - Valuation: PE 23.65 vs 48.22; PB 4.97 vs 8.14; fwd PE 18.53. On FY27E EPS of 6.8 it is 20.98, above the cap; the 18.53 figure uses Yahoo's forwardEps of 7.7.
  - Quality: ROE 22.3% vs 12.25%; D/E 0.13; OCF ₹510 Cr; 3y sales/profit CAGR 4%/12%; pledge 1.52%; ADV ₹54.53 Cr.
  - Estimates: FY27E revised 6.4 → 6.8 and FY28E 7.5 → 8.0 over 90 days (n=1 analyst).
  - Q2 last year was on 12 Nov 2025; estimated ~11 Nov 2026 (outside the window, unconfirmed).
- **Would qualify only if all of:**
  1. A pullback to the 50 DMA zone (**129–134.5**) comes on volume below the 20-day average (3.94 mn).
  2. RSI14 turns up while in 40–55.
  3. A bullish reversal close prints **≤ 134.5**, with the low holding **≥ 128.41** (1 Oct swing low).
- **Indicative plan:** entry 134.5, stop 127.4 (5.28%), T1 148.9 (R:R 2.03), T2 154.0. Size: 70 shares, ₹9,415 exposure.
- **Sector headwind:** Nifty Auto 1M −10.50% (bottom-5 RS) demands the full set of conditions. Treat this as the lowest-priority name.

---

## 6. Value traps rejected (cheap ≠ trade)

- **CHENNPETRO:** PE 5.31 vs refiners 15.015 and fwd PE 3.71, but PB 1.99 vs 1.42 (+40%) and 3y sales/profit CAGR **−6%/−5%**. Cyclical refiner near peak margins, with diesel cracks around $52/bbl and Brent at $104.72. Results 22 Oct.
- **GESHIP:** PE 5.84 vs shipping 12.90, but fwd PE **7.41 > trailing 5.84** (EPS expected to fall) and 3y sales/profit CAGR **−2%/0%**. Freight cyclical.
- **PETRONET:** PE 10.4 vs 14.70, but 3y revenue CAGR **−10%**. Volumes are falling, not just prices: Q1 FY27 throughput was 207 vs 220 TBTU, and Dahej utilisation 66% vs 92%. Its 6 Oct breakout failed.
- **PNB:** PE 6.09 vs PSU bank 7.445 and PB 0.86 vs 0.95, but fwd PE **6.73 > trailing 6.09**, ROE 13.0% vs median 15.4%, and the 200 DMA is falling (−0.57 over 20 sessions).
- **MRPL:** PE 10.8 vs 15.015, but **D/E 1.08**, 3y sales/profit CAGR **−7%/−10%**, a 30 Sep coker-unit fire, and results 14 Oct.
- **LICHSGFIN:** PE 5.29 and PB 0.73 vs 1.88, but in the **F&O ban** (12 Oct), EPS revisions are net downward, and it only passes the weaker technical rule (50 DMA below 200 DMA, 200 DMA barely rising).
- **AUROPHARMA:** PE 25.8 vs 39.21, PB 2.60 vs 4.835, fwd PE 18.14, but **ROE 10.1%** vs a 17.4% median. Plus a 9 Oct US recall of 112,932 bottles.
- **SHYAMMETL:** PE 26.4 vs 28.07, PB 2.57 vs 3.43, but **ROE 9.7%** vs 13.35%. Steel cyclical with a ₹50,000 Cr greenfield capex MoU.
- **IPCALAB:** PE 35.4 vs 39.21, but PB 6.02 vs 4.835 (+24.5%, and ROE 15.7% < 17.4% median, so no exception) and **fwd PE 27.21**.
- **ENGINERSIN:** PE 21.0 vs 21.46, but PB 5.23 vs 3.49 (+49.7%), **fwd PE 20.79**, and EPS revisions net downward.
- **KTKBANK** (relaxed universe): PE 8.63 vs 13.96, but **ROE 10.4%** vs an 11.5% bank median.
- **GNFC** (relaxed universe): PE 8.42 vs 21.94, but ROE 9.14% and 3y sales/profit CAGR **−9%/−18%**. Results 2 Nov.
- **RAIN** (relaxed universe): PE 13.54 vs 13.72, but ROE 0.6%, D/E 1.35, and 3y profit CAGR **−69%**.

---

## Appendix A — Stage 1 survivors (75)

**Track A (47):** ABDL, ACE, ACMESOLAR, AEGISLOG, AETHER, AIIL, AUROPHARMA, AZAD, BALRAMCHIN, BBOX, CARBORUNIV, CARTRADE, CPPLUS, DIVISLAB, ENGINERSIN, ETERNAL, FINCABLES, GESHIP, GLAND, GRAPHITE, INOXINDIA, IPCALAB, JYOTICNC, KIRLOSENG, LALPATHLAB, LAURUSLABS, LENSKART, LGEINDIA, MAHABANK, MCX, MEESHO, MOTILALOFS, NYKAA, PETRONET, PNB, PNBHOUSING, PTCIL, PVRINOX, PWL, REDINGTON, RRKABEL, SHYAMMETL, SOLARINDS, SYRMA, TDPOWERSYS, TEGA, WELSPUNLIV.

**Track B (28):** AEQUS, ATLANTAELE, AXISCADES, DIACABS, DYNAMATECH, E2E, EBGNG, EMIL, ENTERO, GRWRHITECH, ICIL, JAMNAAUTO, KMEW, KTKBANK, LLOYDSENGG, LOTUSDEV, LXCHEM, MANORAMA, MIDHANI, NAZARA, NEOGEN, PGIL, PRECWIRE, QPOWER, RAIN, UNIMECH, WELENT, YATHARTH.

**Notes on what Stage 1 could not confirm:**

- Results dates not yet announced were **not** treated as clean. They were checked individually for every Stage 2 survivor (REDINGTON, JAMNAAUTO) and for STAR.
- Pledge was checked for every Stage 2 survivor. For other Track B names it was not fetched (they fail Stage 2 regardless).

## Appendix B — Track A, PE ≥ sub-sector median or no usable median (39 of 47)

PE premium vs median: ABDL +109%, ACE +7.5%, ACMESOLAR +141%, AETHER +136%, AIIL +12.1%, AZAD +118%, BALRAMCHIN +127%, BBOX +58%, CARBORUNIV +31%, CARTRADE +185%, CPPLUS +53%, DIVISLAB +112%, ETERNAL +3,309%, FINCABLES +0.32%, GLAND +12.5%, GRAPHITE +168%, INOXINDIA +176%, JYOTICNC +0.23%, KIRLOSENG +42%, LALPATHLAB +155%, LAURUSLABS +158%, LENSKART +374%, LGEINDIA +98%, MAHABANK +14.0%, MCX +16.9%, MOTILALOFS +37.6%, NYKAA +1,645%, PNBHOUSING +1.17%, PTCIL +979%, PVRINOX +15.7%, PWL +3,058%, RRKABEL +89%, SOLARINDS +3.9%, SYRMA +26.6%, TDPOWERSYS +46%, TEGA +26.9%, WELSPUNLIV +124%.

No usable value: AEGISLOG (industry median N/A), MEESHO (PE N/A, loss-making).

The financials variant (PB-led) does not rescue any of them. AIIL PB 3.18 vs 3.04, MAHABANK 1.79 vs 0.95, MCX 29.6 vs 13.4, MOTILALOFS 4.79 vs 2.79. PNBHOUSING passes PB (1.57 vs 1.88) but fails PE by +1.17%.

## Appendix C — Track A, the 8 PE-cheap names

| Ticker | PE vs median | Binding fail |
|---|---|---|
| REDINGTON | 16.5 < 31.84 | **PASS** Stage 2 → fails Stage 4 |
| AUROPHARMA | 25.8 < 39.21 | ROE 10.1% < 12 and < 17.4 median |
| ENGINERSIN | 21.0 < 21.46 | PB +49.7%; fwd PE 20.79 ≥ 20; EPS revisions net down |
| GESHIP | 5.84 < 12.90 | fwd PE 7.41 > trailing; 3y CAGR −2%/0% |
| IPCALAB | 35.4 < 39.21 | PB +24.5% (ROE below median); fwd PE 27.21 |
| PETRONET | 10.4 < 14.70 | 3y revenue CAGR −10% (volume-led; not justified) |
| PNB | 6.09 < 7.445 | fwd PE 6.73 > trailing 6.09 |
| SHYAMMETL | 26.4 < 28.07 | ROE 9.7% < 12 and < 13.35 median |

## Appendix D — Track B Stage 2 (28)

PE values are at the 9 Oct close (screener PE × 9 Oct close ÷ screener live price).

- **Pass:** **JAMNAAUTO** (23.65 vs 48.22; PB 4.97 vs 8.14; fwd PE 18.53; ROE 22.3%; D/E 0.13; OCF 510; CAGR 4%/12%; revisions up).
- **PE-cheap but fail on quality:**
  - KTKBANK: ROE 10.4%.
  - LXCHEM: 39.99 vs 41.05, but ROE 4.11% and 3y profit CAGR −14%.
  - LLOYDSENGG: 65.47 vs 70.54, but OCF −253.
  - MIDHANI: 61.19 vs 84.27, but ROE 8.92% and 3y profit CAGR −6%.
  - RAIN: ROE 0.6%, D/E 1.35, CAGR −7%/−69%.
  - KMEW: 62.78 vs 63.64, but the median rests on n=2 peers (unusable).
- **PE ≥ median:** ATLANTAELE 62.31 vs 62.07, AXISCADES 270.2 vs 84.27, DIACABS 115.5 vs 30.03, DYNAMATECH 154.4 vs 70.54, E2E 465.4 vs 35.08, EBGNG 54.8 vs 24.96, EMIL 37.45 vs 30.91, ENTERO 56.5 vs 45.83 (n=2), GRWRHITECH 41.96 vs 25.86, ICIL 57.3 vs 33.9, LOTUSDEV 45.6 vs 29.8, MANORAMA 49.95 vs 25.05, NEOGEN 200.9 vs 41.05, PGIL 37.75 vs 28.54, PRECWIRE 521 vs 17.1, QPOWER 89.9 vs 62.07, UNIMECH 122.5 vs 84.27, WELENT 28.76 vs 21.46, YATHARTH 54.4 vs 49.54.
- **Loss-making (PE N/A):** AEQUS, NAZARA.

---

## 7. Data sources & timestamps

**DATA_MODE: WEB.**
**MCP_ERROR:** the screener / screener-core MCP namespaces are absent from the tool catalog. The GetDynamicTools full catalog lists only cursor, Cursor Automation Tools, cursor-cloud and cursor-subscriptions, and pattern 'screener' returned 0 matches. Not authenticated, per run rules.

| Source | As-of | Used for |
|---|---|---|
| Yahoo v8 chart (`^NSEI`, `^CRSLDX`, `^INDIAVIX`, 499 Nifty 500 names, BZ=F, USDINR=X) | 2026-10-09 close | Index/stock DMAs, EMA20, RSI14, ATR14, returns, 20 bars |
| NSE bhavcopy `sec_bhavdata_full_*` (20 sessions, 10 Sep–9 Oct) | 2026-10-09 | Official close, ADV, delivery % (Yahoo vs NSE close gap 0.0%) |
| NSE `ind_close_all_*` CSVs | 09/01 Oct, 08 Sep, 10 Jul 2026 | Sector 1W/1M/3M returns and RS vs Nifty 500 |
| NSE APIs: reportASM/GSM, board meetings, event calendar, corporate actions, fiidiiTradeReact, fo_secban.csv | 2026-10-09 / 12 Oct | Surveillance, results window, FII/DII, F&O ban |
| NSE SHP XBRL | mostly 30-Jun-2026 | Promoter pledge |
| screener.in company + industry pages (data agent) | fetched 12 Oct pre-open; prices are the 9 Oct close line | PE, PB, ROE, D/E, OCF, CAGRs, shareholding, industry median PE, top-12 peer PB/ROE medians |
| Yahoo quoteSummary (crumb) | 12 Oct (fwd PE recomputed at the 9 Oct close) | Forward EPS, analyst ratings and targets, earningsTrend revisions |
| Web search (news.md) | 2026-10-09 to 12 Oct | News, breadth cross-checks, RBI/Fed, bank asset quality, results dates |

**Confidence caps that would apply to any future pick:**

- Forward PE is single-source (Yahoo) for every name: confidence max **Med**.
- Track B screener values were fetched during market hours on 12 Oct and rescaled to the 9 Oct close.
- 5y EV/EBITDA is N/A for every cyclical.
- Track B delivery % was used only for JAMNAAUTO.

---

## 8. Reminder

This is research, not financial advice. Position sizing (₹500 risk per trade) and hard stops are mandatory. Skip any name that cannot be sized within ₹500 of risk on 1 share or within the ₹50,000 exposure cap. This week: **no trade**.

---

## Additional data fetched by analyst

All fetched 2026-10-12 between about 09:40 and 10:10 IST. Market was open, so any live 12 Oct price was excluded or rescaled to the 9 Oct close.

1. **Nifty Microcap 250 constituents:** https://www.niftyindices.com/IndexConstituent/ind_niftymicrocap250_list.csv (HTTP 200, 250 rows). Used for the ₹5,000 Cr relaxation universe.
2. **Yahoo v8 1y daily charts for the 250 Microcap names:** `https://query1.finance.yahoo.com/v8/finance/chart/{SYM}.NS?interval=1d&range=1y`. 246 parsed; 404 for DUMMYINGL1, DUMMYINGL2, DUMMYINXGN, TRIVENIPT. Bars dated after 2026-10-09 were dropped, and indicators were computed with the data agent's `raw/compute_indicators.py`. JAMNAAUTO 9 Oct close 142.67 matches the NSE bhavcopy (142.67).
3. **screener.in company pages** (`https://www.screener.in/company/{SYM}/consolidated/`) for the 44 Track B names that passed ADV, plus 11 auto-component peers: MOTHERSON, BOSCHLTD, BHARATFORG, UNOMINDA, SCHAEFFLER, SONACOMS, TIINDIA, ENDURANCE, EXIDEIND, DHOOTTRANS, CRAFTSMAN. All HTTP 200. These pages show live 12 Oct prices (e.g. JAMNAAUTO 146.0), so PE and mcap were rescaled by 9 Oct close ÷ screener price. Peer PB = 9 Oct close (data agent tech.json) ÷ screener book value.
   - **JAMNAAUTO peer-median PB = 8.1424** (n=11; DHOOTTRANS book value missing). Peer-median ROE = 12.25 (n=12).
4. **screener.in industry pages (page 1)** for the 17 industries missing from the data agent's set: Aerospace & Defense median PE 84.27 (n=23), Commodity Chemicals 21.935 (n=20), Plastic Products-Industrial 25.86 (n=21), Garments & Apparels 28.54 (n=24), Hospital 49.54 (n=25), Other Food Products 25.05 (n=25), Gems & Jewellery 23.07 (n=25), Petrochemicals 13.72 (n=16), Dredging 63.64 (n=2), and others listed in appendix D.
5. **Yahoo quoteSummary** (cookie + crumb), JAMNAAUTO / STAR / SOUTHBANK:
   - JAMNAAUTO: forwardEps 7.7 (fwd PE 18.53 at 142.67), FY27E 6.8 / FY28E 8.0 (90d ago 6.4 / 7.5), n=1, target 242.
   - STAR: forwardEps 95.4, n=3, target mean 1,338.7.
   - SOUTHBANK: forwardEps 7.02 (fwd PE 6.82 at 47.91), book value 45.049, 3 Buy / 3 Hold, target mean 47.0; FY27E revised 6.075 → 6.36 over 90 days.
6. **NSE SHP XBRL pledge** via `https://www.nseindia.com/api/corporate-share-holdings-master?index=equities&symbol={SYM}` (30-Jun-2026 filings): JAMNAAUTO **1.52%** (3,030,000 of 199,235,434 promoter shares; promoter 49.84%); STAR **38.1%** (9,802,139 of 25,729,268; promoter 27.91%); SOUTHBANK no promoter group (N/A).
7. **NSE board meetings / event calendar** (data agent raw files covering all equities, 12 Oct–2 Nov): Track B results dates SOUTHBANK 15 Oct, AEROFLEX 14 Oct, HERITGFOOD 15 Oct, THELEELA 14 Oct, WESTLIFE 23 Oct, AARTIPHARM 28 Oct, INDGN 29 Oct, GNFC 2 Nov. Full NSE ASM list (longterm 127 + shortterm 72) used for Track B ASM.
8. **NSE bhavcopy** (data agent raw files) for JAMNAAUTO delivery %: 6 Oct 37.25%, 7 Oct 29.51%, 20-day average 37.48%; ADV ₹54.53 Cr. Choice India also shows 37.25% for 7 Oct. Same number, different session label; NSE's file is used.
9. **Results-date history (web):**
   - REDINGTON Q2 on 5 Nov 2025, 29 Oct 2024, 6 Nov 2023, 2 Nov 2022 (https://trendlyne.com/equity/board-meeting/REDINGTON/1120/redington-ltd-board_meeting/ and https://www.livemint.com/redington/board-meetings/companyid-s0003787). TipRanks estimate 10 Nov 2026 (https://www.tipranks.com/stocks/in:redington/earnings/q1-2027-report).
   - PETRONET Q2 FY26 on 7 Nov 2025 (https://www.petronetlng.in/w/press-release-q2-2025-26-financial-results).
   - STAR Q2 FY26 on 31 Oct 2025 (https://www.strides.com/Upload/PDF/StridesFSIntimation-FY-2025-26-Q2.pdf).
   - JAMNAAUTO Q2 FY26 on 12 Nov 2025 (https://financialfilings.com/filings/jamna-auto-industries-ltd/interim-quarterly-report/2025/42288436/); next estimated 11 Nov 2026 (https://stockevents.app/en/stock/JAMNAAUTO.NSE).
   - None of these 2026 dates are confirmed.
10. **SOUTHBANK Q1 FY27** (16 Jul 2026): GNPA 1.38% (3.15% YoY), NNPA 0.26% (0.68%), PCR incl. write-offs 94.51%, CRAR 19.62%, Tier 1 18.93%, PAT ₹377.63 Cr (+17.29%), NII ₹1,025 Cr (+23%). Two sources: https://www.kalkine.co.in/article/announcements/south-indian-bank-nsesouthbank-did-q1-fy27-net-profit-rise-17-to-rs-37763-cr and https://alphastreet.com/india/south-indian-bank-ltd-southbank-q1-2027-earnings-call-transcript/ (also NDTV Profit, ICICI Direct).
11. **PETRONET Q1 FY27 press release** (13 Aug 2026): Dahej utilisation 66% vs 92% YoY; total volume 207 vs 220 TBTU; standalone PAT ₹1,133 Cr (+33%). https://www.petronetlng.in/w/press-release-q1-2026-27-financial-results
12. **JAMNAAUTO 7 Oct move:** O 144.4, H 154.0, L 142.5, C 151.77, 12.31 mn shares (https://choiceindia.com/stocks/jamna-auto-industries-ltd-share-price). Marked as an all-time high (https://www.marketsmojo.com/news/stocks-in-action/jamna-auto-industries-ltd-stock-hits-all-time-high-on-7-oct-2026-4217739). No fundamental news catalyst found. Mcap cross-check: Univest ₹5,369.8 Cr at ₹150 vs screener ₹5,840 Cr at ₹146 (₹5,707 Cr at 142.67). The sources disagree (likely different share counts), but both are ≥ ₹5,000 Cr.

Scratch files from these fetches: `/tmp/analyst-2026-10-12/` (not committed).

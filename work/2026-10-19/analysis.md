# Weekly swing research — NSE — run 2026-10-19 (IST)

**DATA_MODE:** WEB (screener / screener-core MCP absent).
**Prices / indicators as-of:** last completed NSE session **Fri 2026-10-16**. Results-season exclusion window: 15 sessions, **Mon 19 Oct – Mon 9 Nov 2026** (Dussehra 20 Oct excluded; Sun 8 Nov Muhurat not counted).
**Capital:** ₹50,000 | risk/trade ₹500 (1%) | max 5 names | total exposure cap ₹50,000 | horizon 1–3 weeks.

1. **Regime: RISK-OFF (improving).** Nifty 50 has reclaimed its 20 DMA, but both Nifty 50 and Nifty 500 remain below falling 50 and 200 DMAs, so the book is capped at 2 ideas.
2. **VIX / breadth:** India VIX **14.06**, above its 20/50 DMA and **+6.76%** over 1M. Only **22.24%** of the Nifty 500 is above its 50 DMA. FPIs sold **₹52,100 Cr** October-to-date.
3. **Leading sectors (RS vs Nifty 500, 1M / 3M):** IT **+10.91 / +13.80 pp**, Media **+9.96 / +12.90**, MidSmall IT & Telecom **+5.87 / +10.70**, India Digital **+3.10 / +9.76**, plus Services (1M +3.44) and Pharma (3M +5.10).

# One qualifying trade: SOUTHBANK (Setup B), score 75, confidence Med

Only one name clears every gate. **SOUTHBANK** has a value floor (PE 34.8% and PB 28.9% below private-bank medians), a record Q2 FY27, and a 6-week base breakout on 3.9× volume.

The entry is a **pullback-only zone of 50.70–51.50**. Do not chase above 51.54: above that, R:R to T1 drops below 2:1.

Risk is ₹499.80 on 196 shares, or **₹10,084.20 exposure**. The remaining **₹39,915.80 stays in cash**. In this RISK-OFF tape, a one-name book at one-fifth of capital is deliberate.

```yaml
SUMMARY:
  regime: RISK-OFF
  data_mode: WEB
  data_as_of: "2026-10-16"
  run_date_ist: "2026-10-19"
  mcap_floor_relaxed: true          # Stage 3 at Rs12,000 Cr left 1 name (< 10); Track B (Rs5,000-12,000 Cr) screened; it produced no pick
  funnel:                           # Track A (>= Rs12,000 Cr) + Track B (Rs5,000-12,000 Cr)
    start: 128                      # A 96 (74 Nifty 500 technical-pass + 22 Microcap-250 names >= 12k passing momentum) + B 32
    stage1: 43                      # A 32 + B 11
    stage2: 2                       # SOUTHBANK (A), JAMNAAUTO (B)
    stage3: 2
    stage4: 1                       # SOUTHBANK (Setup B)
    final: 1
  picks:
    - ticker: SOUTHBANK
      sub_sector: Private Sector Bank
      setup: B
      score: 75
      score_components: {relative_value: 22, quality: 12, momentum_rs: 17, setup_rr: 16, catalysts: 8}
      confidence: Med
      entry_zone: "50.70-51.50"
      entry_reference: 51.45        # 16-Oct NSE close; used for sizing and R:R
      entry_trigger: "Buy only on a session that trades inside 50.70-51.50 and closes >= 50.68 (breakout level); cancel if not filled by 23-Oct close; never chase above 51.54"
      stop: 48.90
      stop_pct: 4.96
      t1: 56.82                     # 6-week base measured move: 50.68 + (50.68 - 44.54)
      t2: 58.35                     # Jun-Oct base measured move: 50.68 + (50.68 - 43.01)
      rr: 2.11                      # (56.82 - 51.45) / (51.45 - 48.90); R:R to T2 = 2.71
      shares: 196                   # floor(500 / 2.55)
      exposure: 10084.20            # 196 x 51.45; risk 196 x 2.55 = 499.80
      time_stop: "Exit at the close of the 10th session after fill unless a close >= 54.14 (halfway to T1) has printed; fill 21-Oct -> 4-Nov"
  total_exposure: 10084.20
  near_misses_scored:               # NOT picks - each fails a hard gate
    - {ticker: REDINGTON, score: 66, eligible: false, gate_failed: "Stage 1 - Q2 results probable in window (no intimation; prior-year 5 Nov 2025; estimates 30 Oct / ~4 Nov) and Stage 4 - no Setup A trigger"}
    - {ticker: TANLA, score: 62, eligible: false, gate_failed: "Stage 1 - Q2 results overdue and probable in window (prior-year 17 Oct 2025; not intimated; estimate 23 Oct)"}
    - {ticker: JAMNAAUTO, score: 56, eligible: false, gate_failed: "Stage 4 - pullback to EMA20 but RSI falling and no reversal candle"}
  watchlist: [REDINGTON, TANLA, JAMNAAUTO]
  incomplete: false
```

---

## 1. Market regime

**RISK-OFF (improving).** The tape is better than last week but not yet NEUTRAL.

**Indices vs moving averages (as of 16 Oct):**

| Index | Close | vs 20 DMA | vs 50 DMA | vs 200 DMA | RSI14 | 1M | 3M |
|---|---:|---:|---:|---:|---:|---:|---:|
| Nifty 50 | 23,146.15 | 22,840.88 (**+1.34%**) | 23,549.21 (**−1.71%**) | 24,190.75 (**−4.32%**) | 52.81 | −0.31% | −4.88% |
| Nifty 500 | 22,270.05 | 22,248.39 (**+0.10%**) | 22,902.87 (**−2.76%**) | 22,878.15 (**−2.66%**) | 47.26 | −1.16% | **−4.57%** |

- Both 50 DMAs are falling: Nifty 50 −542.13 and Nifty 500 −424.71 over 20 sessions. Both 200 DMAs are also falling: −317.81 and −145.59.
- Nifty gained **+2.77% w/w** (+625.7 pts), its second straight weekly gain, led by IT (+11.7% w/w). The 52w low was 22,179.9 on 8 Oct.
- Nifty Bank closed at 55,844.0, above its 20 DMA of 55,323.37 but below its 50 DMA (56,485.01) and 200 DMA (56,931.9).

**VIX.** India VIX is **14.06**, above its SMA20 (13.39) and SMA50 (12.30) but below its SMA200 (14.75). It is **+6.76%** over 1M (13.17 on 16 Sep) and −2.23% w/w; the 10-session peak was 15.28 on 8 Oct.

**Breadth.**
- **22.24%** (111/499) of the Nifty 500 is above its 50 DMA, up from 17.84% last week. 32.67% is above its 20 DMA and 41.34% above its 200 DMA. In the Nifty 50, 32% (16/50) are above their 50 DMA.
- Cross-checks: IndexBreadth shows 21.2% above the 50 DMA (A/D 258/241, new lows 4.0% vs new highs 1.6%). Flash Finance's top-500 proxy shows 24.0%.

**Flows and macro.**
- FPIs: **−₹7,934 Cr** (settled) in the week of 12–16 Oct and **−₹52,100 Cr** October-to-date (CDSL/NSDL via TOI and ET). The 16 Oct provisional figure was **+₹1,165.92 Cr**, ending a 15-session FII selling streak.
- DIIs: **+₹74,729 Cr** October-to-date.
- RBI repo is **5.50%** after a +25 bp hike on 7 Oct ("calibrated tightening"). India CPI for September was 5.54%.
- Brent settled at **$109.86** on 16 Oct after Hormuz tanker attacks. USDINR was 94.96. The US 10y is about 5.3%.
- FOMC is 27–28 Oct (reaction in India 29 Oct). Hike odds conflict across sources: Yardeni 17%, ET >40%.

**Sector RS vs Nifty 500** (NSE `ind_close_all`; 1M base 16 Sep, 3M base 17 Jul):

- **Top 5 by 1M RS:** IT +10.91, Media +9.96, MidSmall IT & Telecom +5.87, Services +3.44, India Digital +3.10.
- **Top 5 by 3M RS:** IT +13.80, Media +12.90, MidSmall IT & Telecom +10.70, India Digital +9.76, Pharma +5.10.
- **Bottom 5 by 1M RS:** MidSmall Financial Services −4.01, MNC −3.98, Metal −3.59, Consumer Durables −3.41, Auto −3.02.
- **Bottom 5 by 3M RS:** Cement −6.42, Realty −5.53, Core Housing −4.82, MNC −4.61, FMCG −3.91.
- **Private Bank** (the pick's sector) is +2.69 pp on 1M RS (rank 6/36) and +1.74 pp on 3M (rank 9/36). That is positive but outside the top 5, so the pick needs a stock-specific reason; it has one, a results-driven breakout.

**Classification.** All three RISK-ON tests fail:
- Price is below the 50 DMA on both indices.
- Breadth is 22% vs a healthy level of ≥ 50%.
- VIX is above its 20/50 DMA and rising over 1M.

The 20 DMA reclaim and improving breadth are early repair, not confirmation. **RISK-OFF: max 2 ideas, highest-scoring only.** One qualifies, and the cash balance is the larger position.

---

## 2. Funnel

**Universe construction.**

- **Track A** (≥ ₹12,000 Cr, 96 names):
  - 74 Nifty 500 names pass the data agent's technical pre-screen: close > 50 DMA, 50 DMA > 200 DMA or 200 DMA rising, close ≥ 0.75 × 52wH.
  - **22 Nifty Microcap 250 names** have mcap ≥ ₹12,000 Cr and pass the same momentum test plus 3M > Nifty 500. The data agent filed these under Track B as "mcap > 12k" fails. They belong to the ₹12,000 Cr universe, so I moved them to Track A; SOUTHBANK, at ₹13,477 Cr, is one of them.
- **Track B** (₹5,000–12,000 Cr, 32 names): run because Stage 3 at ₹12,000 Cr left **1** name (< 10). The method's relaxation rule therefore applies.

**Results rule used in Stage 1.**
- A confirmed NSE board-meeting intimation dated 19 Oct–9 Nov is a fail.
- Where no intimation exists as of 19 Oct (re-queried at ~10:00 IST for the key names), the **prior-year Q2 FY26 board-meeting date** is used as a proxy. If it falls inside the equivalent 19 Oct–9 Nov window, or is already past (17 Oct 2025) with no FY27 filing yet, the name is a **probable** fail.
- This is stricter than last week, when unconfirmed names passed. It stops a 1–3 week swing from straddling an unscheduled result. It is the reason REDINGTON and TANLA drop out.

| Stage | Left | Names | What dropped (per-ticker reasons in Appendix A–C) |
|---|---:|---|---|
| 0 regime | — | RISK-OFF | Book capped at 2 |
| Start | **128** | A 96 + B 32 | — |
| **1 tradability** | **43** (A 32 + B 11) | Appendix A | A −64 (ADV, ASM, pledge, confirmed and probable results); B −21 |
| **2 relative value + quality** | **2** | **SOUTHBANK**, **JAMNAAUTO** | A: 25 PE ≥ median or loss-making, 6 PE-cheap names fail a hard test. B: 8 PE ≥ median, KMEW no median, SUPRIYA fails PB and fwd PE |
| **3 momentum** | **2** | SOUTHBANK, JAMNAAUTO | — |
| **4 swing setup** | **1** | **SOUTHBANK (B)** | **JAMNAAUTO:** pullback to the 20 EMA on fading volume (0.36×, 0.29×), but RSI is still falling (64.09 → 55.17 → 53.25) and 16 Oct was a bearish candle (O 143.00, C 140.85, near the 140.40 low). Setup A is not triggered. |
| **Final** (score ≥ 65, stop ≤ 8%, R:R ≥ 2) | **1** | **SOUTHBANK** | — |

**Setup-C side list.** Already-reported names are exempt only from the results exclusion; every other stage still applies. None qualifies.

| Ticker | Status | Binding fail |
|---|---|---|
| HCLTECH | Results 12 Oct, held 4 sessions | Stage 3: 50 DMA 1,285.91 < 200 DMA 1,335.29, and the 200 DMA is falling. Also +8.50% above EMA20 (reject band) and RSI 68.98. A stop below the gap-day low of 1,238.2 is 10.28% away (> 8%). |
| TCS | Results 8 Oct | Stage 2: PB 7.49 vs 5.16 (+45.2%). Stage 3: 26.42% below 52wH and 200 DMA falling. RSI 73.52. |
| TATAELXSI | Results 13 Oct | PE 33.31 vs 23.87 (+39.6%); 35.29% below 52wH; RSI 74.42 |
| ELECON | Results 14 Oct (Track B, mcap ₹10,779 Cr) | Fwd PE 22.24 (stockanalysis 28.66) ≥ 20; 50 DMA 437.13 < 200 DMA 453.95 and not rising |
| TARIL | Results 13 Oct (Track B) | Pledge 21.84% > 20%; 32.75% below 52wH; OCF −₹105 Cr |
| KARURVYSYA, TATACOMM, TECHM, 360ONE, HDFCAMC, IIFL, FEDERALBNK, JAYNECOIND | Held < 3 sessions | All fail Stage 2 as well (see appendices or the data.json rows) |

**Filters not silently loosened.** These are the smallest relaxations that would re-open research. None is applied.

1. **Allowing unconfirmed results dates** (last week's rule) re-admits REDINGTON. It would still fail Stage 4 (RSI falling, bearish 16 Oct candle on 1.19× volume) and score 66. It is a watchlist name, not a trade.
2. **Allowing a 4.7% PE premium** admits FINCABLES (26.1 vs 24.925). Its forward PE disagrees across sources (18.81 vs 22.68), OCF is only ₹49 Cr, and its prior-year Q2 date was 11 Nov. It has no setup: close 1,367.7 is below EMA20 1,414.1, with RSI 46.31.

---

## 3. Shortlist table

| Ticker | Sub-sector | Mcap (₹Cr) | PE prem vs sub-sector | PB prem vs sub-sector | Fwd PE | % below 52W high | 3M RS vs Nifty 500 | Setup (A/B/C) | Score |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|
| **SOUTHBANK** | Private Sector Bank | 13,477 | **−34.8%** (8.50 vs 13.03, n=20) | **−28.9%** (1.115 vs 1.569, n=12) | **7.17** (stockanalysis 7.42) | 2.00% | **+19.93 pp** (+15.36% vs −4.57%) | **B** | **75** |

**Scored near-misses (NOT picks).** Scores are for reference only; each fails a hard gate.

| Ticker | Sub-sector | Mcap (₹Cr) | PE prem | PB prem | Fwd PE | % below 52W high | 3M RS (pp) | Setup | Score | Gate failed |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|
| REDINGTON | Trading & Distributors | 29,981 | −44.5% (16.7 vs 30.1) | −38.2% (2.95 vs 4.78) | 12.42 (14.23) | 8.58% | +44.00 | A forming | 66 | Stage 1 (probable results) + Stage 4 |
| TANLA | Software Products | 7,423 | −54.4% (13.9 vs 30.48) | −41.3% (2.98 vs 5.07) | 12.15 (13.17) | 18.16% | +0.31 | B (13 Oct) | 62 | Stage 1 (results overdue) |
| JAMNAAUTO | Auto Components & Equipments | 5,634 | −48.4% (23.3 vs 45.17) | −43.4% (4.91 vs 8.68) | 17.61 (stockanalysis 20.15; FY27E 20.71) | 8.54% | +11.48 | none (A forming) | 56 | Stage 4 |

Score breakdowns (Relative value 25 / Quality 15 / Momentum & RS 20 / Setup & R:R 25 / Catalysts 15):

- **REDINGTON:** 24 / 10 / 18 / 5 / 9.
  - Quality: OCF of ₹231 Cr against TTM EPS of 21.76 gives weak cash conversion, and the 3y profit CAGR is 5%.
  - Setup: no reversal.
  - Catalysts: 6/6 Buy, TP 444 (+15.8%), FY27E +16.0% in 90 days.
- **TANLA:** 22 / 11 / 10 / 14 / 5.
  - Quality: 3y profit CAGR is 4%.
  - Momentum: 3M RS is only +0.31 pp and the 200 DMA is falling.
  - Setup: valid B, but +8.1% above EMA20 at the edge of the reject band.
  - Catalysts: 1 Buy / 1 Sell.
- **JAMNAAUTO:** 19 / 13 / 13 / 6 / 5.
  - Relative value: forward PE source conflict.
  - Momentum: Auto ranks 32/36 on 1M RS.
  - Catalysts: n=1 analyst; results date unconfirmed.

---

## 4. Final pick — SOUTHBANK (The South Indian Bank Ltd), Setup B base breakout

**Price facts as of 16 Oct** (NSE bhavcopy = Yahoo; indicators recomputed by me from the Yahoo series and matching the data agent):
- Close: **51.45**; O 51.75 / H 52.50 / L 50.65.
- Indicators: EMA20 48.48 (+6.13%); SMA20 48.25; SMA50 46.86; SMA200 43.04 (rising, +0.87 over 20 sessions); RSI14 66.78; ATR14 1.699.
- Volume and liquidity: 20-day average 19.79 mn shares; ADV ₹96.88 Cr.
- 52w high 52.50 (16 Oct). It is also the highest monthly high in Yahoo's 10-year series, so there is no overhead supply.
- Not in F&O; no ASM/GSM; no promoter group, so pledge is N/A; no bulk/block deal on 16 Oct.

**Setup B geometry:**
- **Base:** 3 Sep–14 Oct, about 6 weeks. High 50.68 (25 Sep), low 44.54 (16 Sep), width **13.79%** (< 15%). A wider Jun–Oct base runs 43.01–50.68.
- **Breakout:** 15 Oct close **51.48** (H 52.08, L 47.69) on **76.83 mn shares = 3.88×** the 20-day average (4.17× the prior-20 average). Results were filed intraday (press release 14:37 IST).
- **Follow-through:** 16 Oct close **51.45** held above 50.68 on **1.86×** volume, with delivery **45.89%** vs a 42.82% 20-day average.
- **Weakness:** delivery on the breakout day was **30.04%**, below average.
- **Not extended:** +6.13% vs EMA20, RSI < 75, no parabolic leg.
- Setup C is **not yet** met: the gap was +0.32% and only 2 sessions have passed (15 and 16 Oct); 19 Oct is live and excluded.

### Thesis

- **Cheap vs peers.**
  - PE **8.50** vs private-bank median **13.03** (−34.8%). PB **1.115** vs **1.569** (−28.9%). Fwd PE **7.17** (Yahoo FY28E EPS 7.18) or **7.42** (stockanalysis), both below trailing.
  - BVPS 46.1 (company presentation) cross-checks the PB.
- **Record Q2 FY27 (15 Oct):**
  - PAT ₹426.13 Cr (+21.28% YoY). NII ₹1,116 Cr (+37.95%). Operating profit ₹732 Cr (+37%). NIM 3.33% vs 2.80%.
  - It beat the ~₹400 Cr PAT estimate (Zee Business; single source).
- **Asset quality and capital keep improving.**
  - GNPA 2.93 → 2.67 → 1.43 → 1.38 → **1.24%** over five quarters. NNPA 0.56 → **0.09%**. PCR excluding write-offs 92.42%.
  - CRAR **19.40%** (17.70% a year ago). ROE 13.5% vs 11.5% median.
  - EPS estimates were revised up over 90 days: FY27E +3.1%, FY28E +4.4%.
- **Leadership with institutional buying.**
  - 3M +15.36% vs Nifty 500 −4.57%. 1M +13.85% vs −1.16%. Price is at a 10-year high.
  - DIIs added **+2.54 pp** and FIIs +0.18 pp (Jun → Sep 2026).

### Bull / bear case

- **Bull:** a turnaround bank is re-rating from PB 1.1 toward the 1.5–1.6 peer median on >18% loan growth and a 0.09% NNPA, with no overhead supply. A measured move gives 56.8–58.4 (+10–13%).
- **Bear:** the breakout fails in a RISK-OFF tape (FPI −₹52,100 Cr MTD, Brent ~$110, FOMC hike risk). Sell-side targets already sit at or below the price (consensus 49.0; Trendlyne 5-analyst average 51.80), which could cap follow-through. A close back below 50.68 traps late buyers.

### Growth drivers and red flags (Q2 FY27 press release and investor presentation, 15 Oct)

No earnings-call transcript could be fetched. The bank filed its call recording on 16 Oct 19:17 IST, but I did not transcribe it.

- **Drivers:**
  1. Gross advances +18.67% YoY to ₹1,09,517 Cr: gold loans +41.17%, mortgages +30.92%, corporate +16.63% (99.10% of large corporates rated A or above).
  2. NIM up 53 bp YoY to 3.33%.
  3. Credit cost runway: PCR 92.42%, GNPA 1.24%.
- **Red flags:**
  1. Provisions ₹159 Cr vs ₹63 Cr (+151%), and other income ₹468 Cr vs ₹516 Cr (−9%; treasury −38% YoY per press summaries).
  2. CASA ratio 31.55% vs 31.86% YoY (−143 bp QoQ per the presentation) during an RBI hiking cycle.
  3. Gold loans are **24.3%** of gross advances (₹26,603 Cr of ₹1,09,517 Cr), growing 41%, which makes the book sensitive to gold prices and RBI gold-loan rules.
- **The 15 Oct "change in management" filing** covers four senior-management redesignations: COO → CBO from 1 Nov, plus heads of Internal Audit, Vigilance and Banking Ops. There is **no MD/CEO change**. A new corporate office was designated at Kakkanad.

### Catalysts, sentiment, ownership

- **Analysts:**
  - Yahoo: n=6, **4 Buy / 2 Hold** (3/3 a month ago, so direction is up). Mean TP **49.0** (−4.8%), range 25–73.
  - Trendlyne: consensus TP 49.00 (17 Oct). Average of 5 analysts 51.80 (+0.7%). The latest broker reports listed predate Q2 (ICICI Securities 45, ICICI Direct 52, Anand Rathi 61 in July).
  - Short-term calls: IDBI Capital Buy, TP 55 (14 Oct, via NDTV Profit); Choice Buy, TP 52 (11 Oct).
  - **Targets lag the price; post-results upgrades are the swing catalyst, unconfirmed.**
- **Next 1–3 weeks:**
  - No company event; Q2 is done and Q3 falls outside the window.
  - Regional-bank peers report inside the window: DCBBANK 23 Oct, CUB and KTKBANK 28 Oct. Read-through cuts both ways.
  - Large-bank Q2 reactions on 19 Oct (HDFC, ICICI, Axis).
  - Macro: IIP 28 Oct; FOMC 28 Oct (29 Oct IST); Muhurat 8 Nov.
  - MCLR revision filed 17 Oct (contents not read).
- **Ownership (screener, Jun → Sep 2026):** FII 25.39 → 25.57%; DII 14.24 → 16.78%; no promoter. No bulk or block deals on 16 Oct.

### Peer check (Private Sector Bank; screener as of 16 Oct close; peer medians from 19 Oct industry pages)

| Bank | PE | PB | ROE % | Latest-quarter growth | GNPA % | 3M ret | Stage status |
|---|---:|---:|---:|---|---:|---:|---|
| **SOUTHBANK** | **8.50** | **1.115** | 13.5 | PAT +21.3%, NII +38% (Q2) | 1.24 | +15.36% | **Pick (Setup B)** |
| KARURVYSYA | 11.6 | 2.239 | 19.1 | PAT +37%, NII +19% (Q2) | 0.69 | +14.80% | Fails PB (+42.7%; the ROE exception allows only +10%) |
| CUB | 16.1 | 2.12 | 13.2 | Q2 on 28 Oct | N/A | — | Results in window; PE +23.6% |
| KTKBANK | 8.68 | ≈0.94 (screener page) | 10.4 | Q2 on 28 Oct | N/A | +20.76% | Results in window; ROE < 12 and < median |
| DCBBANK (₹6,759 Cr) | 8.58 | ≈1.03 (screener page) | 12.0 | Q2 on 23 Oct | N/A | +10.45% | Results in window |
| FEDERALBNK | 16.1 | 1.954 | 11.6 | Q2 16 Oct (PAT N/A here) | N/A | −3.15% | PE +23.6%; close 338.0 < 50 DMA 340.67 |

**Why SOUTHBANK over KARURVYSYA (its closest peer):**
- KVB is the higher-quality franchise: RoA 2.10% vs 1.08%, GNPA 0.69% vs 1.24%.
- But it costs **2.0× the book multiple** (2.24 vs 1.12) for an ROE gap of 5.6 pp, and fails the PB floor.
- SOUTHBANK's NII growth is faster (+38% vs +19%), and its setup is a fresh breakout rather than a stock already 2.8% from its high with RSI 66.8 and no base.

### Trade plan

| Entry | Stop (%) | T1 | T2 | R:R | Shares | ₹ Exposure | Time stop |
|---|---|---:|---:|---:|---:|---:|---|
| Zone **50.70–51.50**, reference **51.45** (16 Oct close). Trigger: a session that trades in the zone and **closes ≥ 50.68**. Cancel if unfilled by 23 Oct close. Never above **51.54**. | **48.90 (4.96%)** | **56.82** | **58.35** | **2.11** (T2: 2.71) | **196** | **₹10,084.20** | 10 sessions after fill (fill 21 Oct → 4 Nov close) unless a close **≥ 54.14** has printed |

- **Stop logic:** 48.90 sits below the 14 Oct pre-breakout low (48.92) and equals 1.5 × ATR (51.45 − 2.55). A breakout-bar-low stop (47.69) would be 7.3% away and give R:R 1.43, so it was rejected. A 2 × ATR stop (48.05) gives R:R 1.58, also rejected.
- **Targets:** there is no historical resistance above 52.50 (10-year high), so T1 is a measured move. T1 = 50.68 + (50.68 − 44.54) = **56.82**; T2 = 50.68 + (50.68 − 43.01) = **58.35**. Because T1 is a projection rather than a tested level, confidence is lowered.
- **Sizing:**
  - floor(500 ÷ 2.55) = **196 shares**; risk ₹499.80; exposure 196 × 51.45 = ₹10,084.20 (cap ₹50,000 respected; total book exposure ₹10,084.20).
  - On a fill below 51.45, re-size as floor(500 ÷ (fill − 48.90)). At the zone low of 50.70: 277 shares, ₹14,043.90, R:R 3.40.
- **Live-price note:** the 19 Oct live quote was about 52.25 at 09:30 IST (stockanalysis; excluded from all calculations). That is above the zone, so this is a **pullback order, not a market order**.

### Score breakdown: 75 / 100

| Component | Max | Score | Basis |
|---|---:|---:|---|
| Relative value | 25 | **22** | PE −34.8%, PB −28.9%, fwd PE 7.17/7.42 < trailing 8.50 (two sources). Lost 3: the medians come from a single source (screener industry pages at live 19 Oct prices). |
| Quality / value-trap safety | 15 | **12** | ROE 13.5% > median 11.5%; GNPA/NNPA falling 5 quarters; CRAR 19.40%; 3y sales/profit CAGR 11%/23%; TTM EPS 6.06; revisions up. Lost 3: RoA 1.08%, provisions +151%, CASA slipping, 24% gold-loan book. |
| Momentum & RS | 20 | **17** | 2.0% below a 10-year high; above EMA20/50/200, 50 > 200, 200 rising; 3M RS +19.93 pp, 1M RS +15.01 pp. Lost 3: sector ranks 6th (1M) and 9th (3M), outside the top 5. |
| Setup quality & R:R | 25 | **16** | Clean 6-week base (13.79%), 3.88× breakout, held on 1.86× with above-average delivery. Lost 9: breakout-day delivery 30.04% (below average); R:R 2.11 is marginal; T1 is a projection; 19 Oct live is above the zone, so a fill is uncertain. |
| Catalysts, sentiment, ownership | 15 | **8** | Record Q2 beat; ratings 3B/3H → 4B/2H; DII +2.54 pp. Lost 7: consensus TP 49.0 below price; no post-Q2 target upgrades found; no scheduled company catalyst in 1–3 weeks. |

### Invalidation levels and alerts

- **Invalidation:**
  1. Any trade at or below **48.90**: stop, exit.
  2. **Two consecutive closes below 50.68** (failed breakout): exit even above the stop.
  3. **Do not enter** on a day when the Nifty 500 closes below its 20 DMA (22,248.39), or Nifty Bank below its 20 DMA (55,323.37).
  4. Exit on any RBI/regulatory action on gold-loan norms, or a sharp gold-price fall that hits gold-loan NBFC/bank stocks (qualitative; no threshold sourced).
- **Alerts:**
  - Entry zone 50.70–51.50, with a close ≥ 50.68.
  - Stop 48.90.
  - Halfway mark 54.14 (time-stop test).
  - T1 56.82; T2 58.35.
  - Volume spike: ≥ 39.57 mn shares (2 × the 19.79 mn 20-day average). On a down day, tighten the stop to 50.65 (the 16 Oct low).
  - Events: DCBBANK Q2 23 Oct, CUB and KTKBANK Q2 28 Oct, IIP 28 Oct, FOMC 28 Oct (29 Oct IST), Muhurat 8 Nov, Balipratipada holiday 10 Nov. SOUTHBANK's next results are Q3 FY27, not scheduled and outside the window.

### Biggest risk and confidence

- **Biggest risk:** the market. In a RISK-OFF tape (22% breadth, FPI −₹52,100 Cr MTD, Brent near $110, possible Fed hike), a high-beta small-cap bank breakout can fail even with clean fundamentals.
- **Confidence: Med.** Price, PE, PB, forward PE and the Q2 numbers are each two-source verified (NSE + Yahoo; screener + company BVPS/Yahoo EPS; Yahoo + stockanalysis; company press release + news). Confidence is held at Med because:
  1. The regime is RISK-OFF.
  2. T1 is a measured-move projection with no tested resistance.
  3. The sell-side consensus target is below the price.
  4. Sub-sector medians are single-source (screener).

---

## 5. Watchlist (3 near-misses)

None of these are orders. Each lists the exact conditions required.

### REDINGTON (Trading & Distributors, ₹29,981 Cr): Setup A still forming; results probably inside the window

- **As of 16 Oct:**
  - Price: close **383.50** (O 393.00, H 393.45, L 382.55 on 1.19× volume); EMA20 392.73; DMA50 **376.06** (rising); DMA200 282.45; RSI14 47.20 (falling from 56.27 on 14 Oct); ATR14 15.418.
  - Highs and swing levels: 52wH **419.5** (23 Sep); swing low 377.95 (9 Oct).
  - Valuation and quality: PE 16.7 vs 30.1; PB 2.95 vs 4.78; fwd PE 12.42 / 14.23; ROE 16.9% vs 8.01%; D/E 0.28.
  - Analysts: 6/6 Buy, TP 444.0; FY27E EPS revised +16.0% over 90 days. DAM Capital re-initiated with Buy, TP 470 (15 Oct).
- **Why excluded:** no Q2 date has been intimated (NSE re-query, 19 Oct about 10:00 IST). Past Q2 dates were 5 Nov 2025, 29 Oct 2024, 6 Nov 2023 and 2 Nov 2022; estimates are 30 Oct (Koyfin/stockanalysis) and about 4 Nov (Yahoo). All fall inside the window.
- **Would qualify only if one of two paths holds:**
  - **(a) Setup A, pre-results:** the board intimates a Q2 date **after 9 Nov**, **and** a bullish reversal close prints ≤ **390.5**. That means a close above the prior session's high with the low holding **≥ 377.95**, RSI turning up from 40–55, and volume ≥ 1.0× the 20-day average.
    - Indicative plan: entry 390.5, stop 376.0 (3.71%, below the 50 DMA), T1 419.5 (R:R 2.00). Size: 34 shares, ₹13,277 exposure.
  - **(b) Setup C, post-results:** revenue and PAT grow YoY, the post-results gap holds above the pre-results close for 3+ sessions, and a stop below the gap-day low is ≤ 8% with R:R ≥ 2 to 419.5 or a measured move.

### TANLA (Software Products, ₹7,423 Cr, Track B): Setup B printed, but Q2 is overdue

- **As of 16 Oct:**
  - **Breakout:** the base ran 480.80–510.50 (about 4 weeks, 6.2% wide). The 13 Oct close of 535.15 came on 3.53× volume, followed by 568.10 (14 Oct) and 549.85 (15 Oct), then **559.65** on 16 Oct.
  - Indicators: EMA20 517.55 (+8.1%, edge of the reject band); RSI 66.05; 200 DMA falling; 52wH 683.8 (18.16% below).
  - Valuation and quality: PE 13.9 vs 30.48; PB 2.98 vs 5.07; fwd PE 12.15 / 13.17; ROE 21.4%; D/E 0.02.
  - Sector: MidSmall IT & Telecom ranks 3rd on both 1M and 3M RS.
- **Why excluded:** Q2 FY26 was reported on **17 Oct 2025**. No FY27 intimation exists as of 19 Oct (NSE re-query); stockanalysis estimates 23 Oct.
- **Would qualify (Setup C) only if all of:**
  1. Q2 FY27 shows YoY growth in both revenue and PAT (Q1 FY27 was +17.9% / +20.1%).
  2. The post-results reaction holds above the pre-results close for 3+ sessions.
  3. 3M return stays above the Nifty 500 3M return (the margin is only +0.31 pp today).
  4. The entry is ≤ 8% above a stop under the reaction-day low, with R:R ≥ 2 to 592.55 (20 Aug pivot high). On today's structure, that requires entry ≤ 530 with a stop of 499.

### JAMNAAUTO (Auto Components, ₹5,634 Cr, Track B): waiting for a 50 DMA pullback

- **As of 16 Oct:**
  - Price: close **140.85**; EMA20 139.76; DMA50 **130.93**; DMA200 128.40; RSI 53.25 (falling); ATR 6.166.
  - Recent bars: 52wH 154.0 (7 Oct); 14 Oct high 150.20. Pullback volume was 0.36× and 0.29× the 20-day average; delivery on 16 Oct was 42.52% vs a 37.85% average.
  - Valuation and quality: PE 23.3 vs 45.17; PB 4.91 vs 8.68; ROE 22.3%; D/E 0.13; OCF ₹510 Cr.
  - Ownership: FII +1.99 pp and DII +2.29 pp (Jun → Sep 2026). The promoter released an encumbrance on 3.03 mn shares on 5 Oct.
- **Would qualify only if all of:**
  1. Q2 date is intimated **after 9 Nov**. The prior-year date was 12 Nov 2025; stockanalysis estimates 6 Nov, inside the window.
  2. Pullback into **131–134.5** on below-average volume (< 3.51 mn shares).
  3. RSI turns up from 40–55, with a bullish reversal close ≤ **134.5** and the low holding **≥ 128.41** (1 Oct swing low). At 134.5, P/E on FY27E EPS of 6.8 is 19.78, which also resolves the forward-PE source conflict.
- **Indicative plan:** entry 134.5, stop 127.4 (5.28%), T1 148.9 (R:R 2.03), T2 154.0. Size: 70 shares, ₹9,415 exposure.
- **Sector:** Auto ranks 32/36 on 1M RS, so this is the lowest-priority name.

---

## 6. Value traps rejected (cheap ≠ trade)

- **COALINDIA:** PE 8.24 vs 24.06 (n=3), but 3y profit CAGR **−1%**. It is a cyclical with no 5y EV/EBITDA available, sits 15.07% below its 52wH, and its 3M return is −2.44%. Prior-year Q2 was 29 Oct (probable in window).
- **GESHIP:** PE 5.74 vs 12.86, but fwd PE **7.29 (Yahoo) > trailing**, so EPS is expected to fall. 3y sales/profit CAGR **−2%/0%**. Freight cyclical; prior-year Q2 7 Nov.
- **MRPL:** PE 7.32 vs 14.11, but PB +24.2% with ROE 14.5% below the 16.3% median, and 3y CAGR **−7%/−10%**. Refining-margin cyclical with Brent near $110. Interim dividend ex-date 21 Oct.
- **PNB:** PE 5.86 vs 7.38 and PB 0.83 vs 0.94, but fwd PE **6.40 / 6.16 > trailing 5.86**. ROE 13.0% vs a 15.4% PSU-bank median, and the 200 DMA is falling. Its Q2 (16 Oct, after market) reaction is pending.
- **SUNTV:** PE 15.93 vs 24.43 in a top-RS sector (Media), but 3y profit CAGR **−4%**. Its peer-median PB of 0.555 looks unreliable and was not used to pass it.
- **BHEL:** PE 52.6 vs 54.84, but **ROE 6.23%** and fwd PE 26.93.
- **HAL:** PE 35.8 vs 79.22, a quality company, but fwd PE **28.89 / 32.45 ≥ 20**. A valuation-floor fail, not a trap.
- **KARURVYSYA:** PE 11.6 vs 13.03 with a strong Q2 (PAT +37%), but PB **2.24 vs 1.57 (+42.7%)**. Not cheap on the bank metric that matters.
- **AUROPHARMA:** PE 25.4 vs 39.0 and PB 2.56 vs 4.71, but **ROE 10.1%** vs a 17.4% median. Prior-year Q2 was 5 Nov.
- **AARTIIND:** PE 34.9 vs 39.1, but **ROE 7.13%**, 3y profit CAGR **−9%**, and fwd PE 25.14.
- **SHYAMMETL:** PE at the median (29.79 vs 29.41), **ROE 9.7%**, and RSI 74.27.
- **KTKBANK:** PE 8.68 vs 13.03, but **ROE 10.4%**; results 28 Oct.
- **SUPRIYA (Track B):** PE 35.9 vs 39.0, but PB **+26.2%** (5.95 vs 4.71) and fwd PE **22.84**.

---

## Appendix A — Stage 1 rejections (85) and survivors (43)

**Track A, Nifty 500 technical-pass (74 → 27):**

- **ADV < ₹25 Cr:** AIIL 10.95, NUVOCO 9.89.
- **ASM** (NSE reportASM, 19 Oct): CUPID (LT-I), HFCL (LT-IV), SANSERA (LT-I), STLTECH (LT-IV), WELCORP (LT-I).
- **Results confirmed in window** (NSE board meetings): ABDL 27 Oct, ADANIGREEN 21, ADANIPORTS 28, APLAPOLLO 26, BAJAJHLDNG 3 Nov, BSE 4 Nov, CASTROLIND 24, COFORGE 23, CRAFTSMAN 28, CUB 28, CYIENT 22, ENGINERSIN 30, ETERNAL 21, FSL 29, INDHOTEL 21, KOTAKBANK 24, LAURUSLABS 29, MEESHO 28, PAYTM 26, PETRONET 2 Nov, PNBHOUSING 28, SAGILITY 22, SHRIPISTON 30. Also NUVOCO 22, HFCL 19 and STLTECH 23.
- **Results probable in window** (not intimated; prior-year Q2 FY26 date in brackets): AARTIIND (6 Nov), ACMESOLAR (3 Nov), AEGISLOG (7 Nov), AUROPHARMA (5 Nov), CARTRADE (28 Oct), COALINDIA (29 Oct), DIVISLAB (7 Nov), ECLERX (24 Oct), GESHIP (7 Nov), GLAND (3 Nov), JYOTICNC (9 Nov), MOTILALOFS (30 Oct), NYKAA (7 Nov), PVRINOX (17 Oct, overdue), REDINGTON (5 Nov), SHYAMMETL (7 Nov), SUPREMEIND (27 Oct).

**Track A, Microcap 250 names ≥ ₹12,000 Cr (22 → 5):**

- **Pledge > 20%:** AEQUS 25.36%, APOLLO 35.57% (also results 24 Oct), LLOYDSENGG 20.31%, NAZARA 86.97%, THELEELA 73.65%.
- **ADV:** GODREJAGRO 12.19, LOTUSDEV 23.13.
- **ASM:** PCJEWELLER (ST-I; also results 21 Oct), SHILPAMED (LT-I), SHREEJISPG (LT-I), SIGMAADV (LT-IV), SKYGOLD (LT-I).
- **Results:** GRWRHITECH 22 Oct, INDGN 29, KTKBANK 28, LUMAXTECH 24.
- **Probable:** MANORAMA (prior 17 Oct, overdue).

**Track B, ₹5,000–12,000 Cr (32 → 11):**

- **ADV < ₹25 Cr:** CEIGALL 12.12, FEDFINA 18.81, GAEL 14.29, GPPL 23.26, ICIL 21.78, IIFLCAPS 22.19, MBAPL 12.57, SAREGAMA 15.87, SGMART 16.98, WESTLIFE 9.82.
- **Pledge:** JAYNECOIND 99.87%, NEOGEN 23.0%.
- **ASM:** PAISALO (LT-I), SUNFLAG (ST-I).
- **Results:** AARTIPHARM 28 Oct, DCBBANK 23, RAIN 6 Nov, SMLMAH 19 Oct.
- **Probable:** AEROFLEX (28 Oct), EBGNG (4 Nov), TANLA (17 Oct, overdue).

The F&O ban for 19 Oct (AMBUJACEM, KAYNES, SAIL) and the GSM list (empty) hit no candidate.

**Stage 1 survivors (43):**

- **Track A (32):** ANGELONE, BALRAMCHIN, BBOX, BHEL, CPPLUS, DIACABS, DLF, E2E, EDELWEISS, FINCABLES, GABRIEL, GRAPHITE, GROWW, HAL, ICICIBANK, JINDALSAW, KARURVYSYA, LGEINDIA, MRPL, PERSISTENT, PNB, PTCIL, PWL, SOLARINDS, SOUTHBANK, SUNTV, SYRMA, TATACOMM, TECHM, TEGA, TI, WELSPUNLIV.
- **Track B (11):** AXISCADES, DYNAMATECH, JAMNAAUTO, KMEW, PGIL, QPOWER, SUPRIYA, TIPSMUSIC, UNIMECH, WELENT, YATHARTH.
- Already-reported names: ANGELONE, BHEL, DLF, GROWW, ICICIBANK, JINDALSAW, KARURVYSYA, MRPL, PERSISTENT, PNB, TATACOMM, TECHM, E2E, SOUTHBANK, TIPSMUSIC.
- PWL has no prior-year date because it listed in Nov 2025; it fails Stage 2 regardless.

## Appendix B — Stage 2, Track A (32 → 1)

**PE premium vs sub-sector median (screener top-25 median), 25 names failing the PE test:**

ANGELONE +10.7%, BALRAMCHIN +122.0%, BBOX +50.8%, CPPLUS +51.3%, DIACABS +292.0%, DLF +19.3%, E2E +440.3%, EDELWEISS +62.6%, FINCABLES +4.7%, GABRIEL +57.8%, GRAPHITE +149.0%, GROWW +117.7%, ICICIBANK +30.5%, JINDALSAW +19.7%, LGEINDIA +93.3%, PERSISTENT +103.0%, PTCIL +1,011.7%, PWL +3,009.3%, SOLARINDS +7.9%, SYRMA +21.2%, TATACOMM +2.6%, TECHM +28.6%, TI +42.0%, WELSPUNLIV +96.4%; TEGA has a loss (PE N/A).

**PE-cheap (7):**

| Ticker | PE vs median | Binding fail |
|---|---|---|
| **SOUTHBANK** | 8.50 < 13.03 | **PASS** (bank tests: PB −28.9%, GNPA/NNPA falling, CRAR 19.40%) |
| BHEL | 52.6 < 54.84 | ROE 6.23% (< 12 and < 23.55 median); fwd PE 26.93 |
| HAL | 35.8 < 79.22 | Fwd PE 28.89 / 32.45 ≥ 20 |
| KARURVYSYA | 11.6 < 13.03 | PB 2.239 vs 1.569 (+42.7%) |
| MRPL | 7.32 < 14.11 | PB +24.2% with ROE below median; 3y CAGR −7%/−10% |
| PNB | 5.86 < 7.38 | Fwd PE 6.40 / 6.16 > trailing |
| SUNTV | 15.93 < 24.43 | 3y profit CAGR −4% |

## Appendix C — Stage 2, Track B (11 → 1)

- **Pass:** **JAMNAAUTO**.
  - PE 23.3 vs 45.17; PB 4.91 vs 8.68 (n=12); fwd PE 17.61 (Yahoo FY28E basis).
  - ROE 22.3%; D/E 0.13; OCF ₹510 Cr; 3y CAGR 4%/12%; revisions up (FY27E +6.25%).
  - Flag: stockanalysis gives 20.15 and FY27E consensus gives 20.71, so the forward-PE pass is primary-source only. That would cap confidence at Med.
- **PE-cheap fail:** SUPRIYA (PB +26.2%; fwd PE 22.84, no second source).
- **PE ≥ median:** AXISCADES +245.9%, DYNAMATECH +132.8%, PGIL +38.7%, QPOWER +54.1%, TIPSMUSIC +31.5%, UNIMECH +60.3%, WELENT +33.3%, YATHARTH +12.7%.
- **No usable median:** KMEW (Dredging; industry PE N/A).

Stage 3 (both survivors pass):
- **SOUTHBANK:** 2.00% below 52wH; 51.45 > 46.86 > 43.04; 3M +15.36%.
- **JAMNAAUTO:** 8.54% below; 140.85 > 130.93 > 128.40; 3M +6.91%.
- Benchmark: Nifty 500 3M −4.57%.

---

## 7. Data sources & timestamps

**DATA_MODE: WEB (fallback).**

**MCP_ERROR:** "screener / screener-core MCP namespaces are absent from the tool catalog in this environment (GetDynamicTools full catalog lists only cursor, Cursor Automation Tools, cursor-cloud, cursor-subscriptions; pattern search '(?i)screener' returned 0 matches). Not authenticated, per run rules."

| Source | As-of | Used for |
|---|---|---|
| Yahoo v8 chart (`^NSEI`, `^CRSLDX`, `^INDIAVIX`, `^NSEBANK`, Nifty 500 + Microcap 250 names) | 16 Oct close (19 Oct bars dropped) | DMAs, EMA20, RSI14, ATR14, returns, breadth, last 20 bars |
| NSE bhavcopy `sec_bhavdata_full_*` (18 Sep–16 Oct, 20 sessions) | 16 Oct | Official close, ADV, delivery % (SOUTHBANK close 51.45 = Yahoo) |
| NSE `ind_close_all` (16 Oct, 9 Oct, 16 Sep, 17 Jul) | 16 Oct | Sector 1M/3M RS vs Nifty 500 |
| NSE APIs: reportASM/GSM, corporate-board-meetings (past, future, and 2025 Q2), corporate-announcements, fiidiiTradeReact; `fo_secban.csv`, bulk/block CSVs | 19 Oct (ASM/ban), 16 Oct (deals) | Surveillance, results window, Setup-C timing, prior-year Q2 proxy |
| NSE SHP XBRL | 30 Sep 2026 / 30 Jun 2026 | Promoter pledge |
| screener.in company + industry pages (data agent) | Company values rescaled to the 16 Oct close; industry pages fetched 19 Oct (live prices) | PE, PB, ROE, D/E, OCF, CAGRs, holdings, sub-sector medians |
| Yahoo quoteSummary / stockanalysis statistics | 19 Oct (fwd PE rebased to the 16 Oct close) | Forward PE (two sources), ratings, targets, EPS revisions |
| Company filings (SOUTHBANK press release + investor presentation, 15 Oct) | 15 Oct 2026 | Q2 FY27 P&L, GNPA/NNPA, CRAR, loan mix |
| Web search (news.md; Trendlyne consensus) | 9–19 Oct 2026 | Flows, macro, broker targets, results-date estimates |

**Additional data fetched by the analyst** (19 Oct 2026, about 09:55–10:10 IST; scripts in `raw/analyst_*.py`, small outputs in `raw/computed/analyst_*.json` and `long_SOUTHBANK_*.json`):

1. **NSE re-query** (`raw/analyst_nse_recheck.py`) of `api/corporate-board-meetings?symbol=` and `api/corporate-announcements` for REDINGTON, TANLA, JAMNAAUTO, SOUTHBANK, COALINDIA, HAL, SUNTV and GESHIP. All HTTP 200. No new Q2 FY27 board-meeting intimations; the latest listed meetings are the Q1 (Jul/Aug 2026) dates.
2. **SOUTHBANK NSE filings** (nsearchives.nseindia.com/corporate/…, HTTP 200, text extracted with pypdf):
   - Press release `SOUTHBANK_15102026143755_SD_STT_PRESSRELEASE_15OCT2026.pdf`.
   - Senior-management change `SOUTHBANK_15102026210436_SD_STT_CHANGEINMANAGEMENT_15OCT2026.pdf`.
   - Corporate-office designation `SOUTHBANK_15102026205501_SD_STT_CORPORATEOFFICECHANGE_15OCT2026.pdf`.
3. **Yahoo v8 long-range SOUTHBANK charts** (`raw/analyst_long_chart.py`): `range=10y&interval=1mo` (120 bars) and `range=2y&interval=1wk` (104 bars), bars after 16 Oct dropped. Used for overhead resistance (none above 52.50) and the Jun–Oct base low (43.01).
4. **Recomputation** of SOUTHBANK SMA20/50/200, EMA20, RSI14 and ATR14 from the data agent's Yahoo file. It matched data.json exactly (48.25 / 46.86 / 43.04 / 48.48 / 66.78 / 1.699).
5. **Prior-year Q2 proxy dates** from the data agent's `nse_board_2025q2.json` (`raw/analyst_prior.py`).
6. **Web search: Trendlyne SOUTHBANK research page** (https://trendlyne.com/research-reports/stock/1270/SOUTHBANK/south-indian-bank-ltd/). Consensus TP 49.00 on 17 Oct; 5-analyst average 51.80. Short-term broker calls via stocktipsarena (IDBI Capital TP 55 on 14 Oct; Choice TP 52 on 11 Oct). Third-party, unverified.

**Known gaps:**
- 5y EV/EBITDA is N/A for all cyclicals.
- Earnings-call transcripts are N/A.
- Sub-sector medians come from screener industry pages at live 19 Oct prices (single source).
- KTKBANK and DCBBANK PB are computed from screener page price ÷ book value (possibly live price).
- No 2026 Q2 dates were confirmed for REDINGTON, TANLA or JAMNAAUTO.

---

## 8. Reminder

This is research, not financial advice. Position sizing (₹500 risk per trade) and hard stops are mandatory. This week: one pullback order in SOUTHBANK (196 shares, ₹10,084.20), with ₹39,915.80 kept in cash.

# Weekly swing research — NSE — run 2026-11-16 (IST)

**DATA_MODE:** WEB (screener / screener-core MCP absent).
**Prices / indicators as-of:** last completed NSE session **Fri 2026-11-13**. Results-season exclusion window: 15 sessions, **Mon 16 Nov – Mon 7 Dec 2026** (Tue 24 Nov Prakash Gurpurb excluded).
**Capital:** ₹50,000 | risk/trade ₹500 (1%) | max 5 names | total exposure cap ₹50,000 | horizon 1–3 weeks. **Open book:** none. SOUTHBANK was settled at T1 on 29 Oct (see the follow-up below). 0 of 5 slots used.

1. **Regime: RISK-ON (late and overbought).** Nifty 50 (25,144.30) and Nifty 500 (23,734.20) are above their 20, 50 and 200 DMAs, and 57.72% of the Nifty 500 is above its 50 DMA (10.22% three weeks ago). The rally is not a healthy trend yet: Nifty 50 RSI is **75.99**, price is **+6.35%** above its 20 DMA, and on both indices the 50 DMA sits **below a still-falling 200 DMA**. New entries only on pullbacks.
2. **VIX / breadth / flows:** India VIX **15.50**, below its 20 DMA (15.90) and down 11.73% from the 11 Nov peak of 17.56, but +9.77% over 1M and above its 50/200 DMAs. FIIs bought **+₹79,302.47 Cr** in November to date (DIIs −₹49,088.64 Cr), after 9 straight weeks of selling into late October.
3. **Leading sectors (RS vs Nifty 500, pp):** 1M: PSU Bank +6.21, Capital Markets +4.12, Realty +3.56, Infrastructure +3.06, Financial Services +2.97. 3M: Media +11.28, Capital Markets +9.94, Private Bank +9.65, Pharma +6.61, Bank +5.58.

## Last week's pick — follow-up (closed position)

**SOUTHBANK (Setup B, published 19 Oct, filled ₹51.45): CLOSED at T1 ₹56.82 on Thu 29 Oct via the resting limit sell. Realised +₹1,052.52 (+10.44%, +2.11R).**

The 2 Nov and 9 Nov reports were not published. This settlement is a **rule-based retrospective**: it applies the published 19 Oct plan to NSE bhavcopy prices, with no discretion added after the fact.

| Item | Value |
|---|---|
| Entry | **₹51.45**, 196 shares, at the 19 Oct open (exposure ₹10,084.20, risk to stop ₹499.80) |
| Exit (primary settlement) | **Full exit at T1 ₹56.82** on **29 Oct**, the 7th session after the fill. It was a resting limit sell: 29 Oct opened at 54.49 (below T1, so no gap-through fill) and traded up to 57.28 (+0.81% above T1) |
| Proceeds | ₹11,136.72 (196 × 56.82) |
| **P&L** | **(56.82 − 51.45) × 196 = +₹1,052.52**, **+10.44%** on exposure, **+2.11R** (R = ₹499.80) |
| Holding period | 19 Oct → 29 Oct: 7 sessions after the fill session (20 Oct Dussehra holiday) |
| Lowest low while open | 51.26 (19 Oct); stop ₹48.90 never threatened |
| Costs | Brokerage, STT, stamp duty and exchange charges are excluded from all P&L figures |

**Reference outcomes (not the settlement, for comparison only):**

| Variant | Exit | Date (session after fill) | P&L | % | R |
|---|---:|---|---:|---:|---:|
| **Primary: full exit at T1 (published resting limit)** | **56.82** | **29 Oct (7)** | **+₹1,052.52** | **+10.44%** | **+2.11** |
| Held all 196 to T2 | 58.35 | 9 Nov (14) | +₹1,352.40 | +13.41% | +2.71 |
| Split: 98 at T1, 98 at T2 | 56.82 / 58.35 | 29 Oct / 9 Nov | +₹1,202.46 | +11.92% | +2.41 |
| Held to the horizon close (15 sessions) | 60.46 | 11 Nov (15) | +₹1,765.96 | +17.51% | +3.53 |
| Marked at the 13 Nov close | 61.86 | 13 Nov | +₹2,040.36 | +20.23% | +4.08 |

- **T2 fill rule:** a resting limit at 58.35 fills on the first *counted* session that trades it. That is **Mon 9 Nov** (open 58.03 < 58.35, high 59.10), so the fill is at the limit, 58.35.
- **Muhurat session (Sun 8 Nov, not counted):** it opened at 58.25 and reached 58.64, so it also traded through T2. Under this report's convention, special sessions are not counted for session counts, time stops or fills. Counting it would move the T2 fill date from 9 Nov to 8 Nov **at the same price (58.35)**, so the reference P&L is unchanged. It does not affect the primary settlement, which happened on 29 Oct.
- **Rule gap (recorded, not back-fitted):** the 19 Oct plan gave T1 and T2 but **no partial-exit split**, so it did not say how many shares to sell at T1. This settlement takes the literal reading: the first target hit closes the position. The split row above shows what a 50/50 split would have produced (+₹149.94 more than the primary). **From this week, every new plan states its exit split explicitly** (see §5).

Bhavcopy OHLC, key sessions (NSE `sec_bhavdata_full_*`; matches `data.json → followups`):

| Date | Open | High | Low | Close | Volume | Vol vs 20d | Note |
|---|---:|---:|---:|---:|---:|---:|---|
| 19 Oct | 51.45 | 54.86 | 51.26 | 54.26 | 58,610,367 | 2.96× | Fill at the open; lowest low of the trade |
| 23 Oct | 55.54 | 55.54 | 51.70 | 52.57 | 27,651,195 | 1.13× | −5.70% down day; not ≥ 2× volume |
| 28 Oct | 54.49 | 54.90 | 53.54 | 54.64 | 12,534,687 | 0.56× | |
| **29 Oct** | **54.49** | **57.28** | 54.00 | 56.57 | 25,474,214 | 1.15× | **T1 56.82 traded → exit** |
| 3 Nov | 54.89 | 54.89 | 53.60 | 53.96 | 9,101,122 | 0.40× | Time-stop review date (moot, already flat) |
| 6 Nov | 56.08 | 57.90 | 55.47 | 57.75 | 15,365,353 | 0.67× | First close ≥ T1 |
| 8 Nov (Muhurat) | 58.25 | 58.64 | 57.64 | 58.03 | 3,010,437 | — | Special session, not counted |
| 9 Nov | 58.03 | 59.10 | 57.60 | 58.68 | 13,703,954 | 0.60× | First counted session ≥ T2 58.35 |
| 11 Nov | 59.45 | 61.79 | 59.16 | 60.46 | 24,549,383 | 1.07× | Horizon end (15th session after fill) |
| 13 Nov | 61.50 | 62.57 | 60.95 | 61.86 | 20,611,927 | 0.87× | New all-time high 62.57 |

**Rule checks (19 Oct – 29 Oct while open; extended to 13 Nov for reference):**
- Hard stop ₹48.90: no low ≤ 48.90. The lowest low was 51.26 (19 Oct).
- Failed-breakout exit (two consecutive closes below ₹50.68): never. The lowest close was 52.57 (23 Oct).
- Volume-spike tighten rule (a down day on ≥ 2× the 20-day average volume): never. The largest down-day ratio was 1.13× (23 Oct).
- Time stop (10th session = 3 Nov) and horizon (15th session = 11 Nov): moot, because the position was flat from 29 Oct.

**Portfolio after settlement:** book flat, **0 of 5 slots**, **₹0 exposure**. The full **₹50,000 exposure cap** is available. Realised P&L of +₹1,052.52 takes account equity to ₹51,052.52. **Convention: sizing stays on the ₹50,000 base** (₹500 risk per trade) until the base is formally reset.

**SOUTHBANK as a fresh candidate this week:** it passes Stages 1–3 but **fails Stage 4** (RSI 76.16 > 75; close +10.54% above EMA20 55.96). It is on the watchlist (§5) for a pullback re-entry.

**Watchlist follow-ups (26 Oct watchlist):**

| Ticker | 26 Oct condition | Status at 13 Nov | Action |
|---|---|---|---|
| PNB | Consensus fwd EPS > TTM 19.89, AND a pullback to ≤ 117.65 holding 113.95 | **Failed.** Fwd EPS is still 18.52 (Yahoo; consensus FY27 18.12, n=18), below TTM 19.85/19.89. No pullback: the lowest low since 26 Oct was 118.20 (26 Oct), then the stock ran to **142.81** (+18.64% vs 120.37 on 23 Oct; high 145.14). RSI 81.52, +12.34% vs EMA20 | **Dropped.** Still fails Stage 2 (fwd PE 7.71 > trailing 7.18) and Stage 4 |
| HCLTECH | 50 DMA > 200 DMA (or rising 200); Setup A pullback to EMA20 with RSI 40–55 turning up; stop ≤ 8% with R:R ≥ 2 | **Partly met.** 50 DMA 1,315.95 > 200 DMA 1,313.64 (the 200 DMA is still falling, −24.72 over 20 sessions). Close 1,378.00 is at the EMA20 (−0.61%), RSI 51.15, volume 0.49–0.56×. **No turn yet:** RSI 51.78 → 51.15, and 13 Nov made a lower low (1,368.50 < 1,372.40) | **Dropped.** Passes Stages 1–3 but scores 40 (§3) |
| TANLA | Setup C after the 27 Oct Q2: revenue and PAT up, gap held 3+ sessions, 3M RS > 0, stop ≤ 8% with R:R ≥ 2 | **Setup C confirmed, now too extended.** Filed 27 Oct 17:29 IST; 28 Oct reaction +1.18%; held 12 sessions (lowest close 598.70). Revenue +25.42%, PAT +16.80% YoY (screener). 3M RS **+23.04 pp**. But close 732.90 (+31.54% vs 557.15) has RSI **82.98** and sits **+15.81%** above EMA20 | **Dropped.** Fails Stage 4 (Track B, mcap ₹9,721 Cr) |

---

# No qualifying trade this week

No candidate clears every gate. Five names survive Stages 1–3 (HCLTECH, LICHSGFIN and SOUTHBANK in Track A; DCBBANK and TANLA in the relaxed Track B). **All five fail Stage 4**: four are too extended after the +11.26% three-week index rally, and HCLTECH's pullback has not turned. The best near-miss scores **64** (SOUTHBANK), below the 65 floor. The right action is **cash plus three watchlist pullback plans**.

```yaml
SUMMARY:
  regime: RISK-ON                   # late/overbought: Nifty 50 RSI 75.99, +6.35% vs 20 DMA; 50 DMA < falling 200 DMA on Nifty 50 and Nifty 500
  data_mode: WEB
  data_as_of: "2026-11-13"
  run_date_ist: "2026-11-16"
  mcap_floor_relaxed: true          # Stage 3 at Rs12,000 Cr left 3 names (< 10); Track B (Rs5,000-12,000 Cr) screened: 2 more Stage-3 survivors, 0 setups
  funnel:                           # Track A (>= Rs12,000 Cr) + Track B (Rs5,000-12,000 Cr)
    start: 270                      # A 226 (146 N500 tech-pass + 22 Microcap-250 momentum-pass + 58 Setup-C-only) + B 44 (1 N500 tech-pass + 32 Microcap momentum-pass + 11 Setup-C-only)
    stage1: 223                     # A 192 + B 31
    stage2: 5                       # HCLTECH, LICHSGFIN, SOUTHBANK (A); DCBBANK, TANLA (B)
    stage3: 5
    stage4: 0                       # 4 extended (RSI > 75 or > 8-10% above EMA20); HCLTECH Setup A not triggered
    final: 0
  picks: []
  closed_positions:
    - ticker: SOUTHBANK
      setup: B
      published: "2026-10-19"
      fill_date: "2026-10-19"
      fill_price: 51.45
      shares: 196
      exposure_at_entry: 10084.20
      stop: 48.90
      exit_date: "2026-10-29"       # 7th session after fill
      exit_price: 56.82             # T1, resting limit sell; open 54.49 < T1, high 57.28
      exit_type: "T1 limit, full exit (plan had no partial-exit split)"
      proceeds: 11136.72
      pnl: 1052.52
      pnl_pct: 10.44
      r_multiple: 2.11
      settlement_basis: "rule-based retrospective (2-Nov and 9-Nov reports not published)"
      reference_only:
        t2_full: {exit: 58.35, date: "2026-11-09", pnl: 1352.40, pnl_pct: 13.41, r: 2.71}   # first counted session; Muhurat 8-Nov (not counted) would fill at the same price
        split_half_t1_half_t2: {pnl: 1202.46, pnl_pct: 11.92, r: 2.41}
        horizon_close_2026_11_11: {exit: 60.46, pnl: 1765.96, pnl_pct: 17.51, r: 3.53}
  total_exposure: 0
  cash: 50000.00                    # full exposure cap available; realised P&L +1,052.52 -> equity 51,052.52 (sizing base kept at 50,000)
  near_misses_scored:               # NOT picks; each fails a hard gate
    - {ticker: SOUTHBANK, score: 64, eligible: false, gate_failed: "Stage 4 - RSI 76.16, +10.54% vs EMA20; R:R to 62.57 is 0.24"}
    - {ticker: UNIONBANK, score: 61, eligible: false, gate_failed: "Stage 2 - fwd PE 7.06 >= trailing 7.04 (+0.24%); Stage 4 - RSI 73.14, +7.69% vs EMA20"}
    - {ticker: LICHSGFIN, score: 58, eligible: false, gate_failed: "Stage 4 - +9.15% vs EMA20, weak Setup C (rev +0.21%, gap +0.32%); Stage 6 - R:R 0.50 to 598.20"}
    - {ticker: DCBBANK, score: 58, eligible: false, gate_failed: "Stage 4 - +12.44% vs EMA20 (Track B)"}
    - {ticker: IIFL, score: 55, eligible: false, gate_failed: "Stage 1 - 4-Dec EGM for Rs6,414 Cr preferential issue (inside window)"}
    - {ticker: TANLA, score: 51, eligible: false, gate_failed: "Stage 4 - RSI 82.98, +15.81% vs EMA20 (Track B)"}
    - {ticker: HCLTECH, score: 40, eligible: false, gate_failed: "Stage 4 - Setup A forming, no reversal; score < 65"}
  watchlist: [SOUTHBANK, LICHSGFIN, UNIONBANK]
  incomplete: false
```

---

## 1. Market regime

**RISK-ON (late and overbought).** Price and breadth pass the RISK-ON tests and VIX has started to ease. The medium-term trend has not confirmed, though, and the index is stretched.

**Indices vs moving averages (as of 13 Nov; Yahoo series, computed; closes match NSE `ind_close_all_13112026`):**

| Index | Close | vs 20 DMA | vs 50 DMA | vs 200 DMA | RSI14 | 1M (21s) | 3M (63s) | Below 52wH |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Nifty 50 | 25,144.30 | 23,642.28 (**+6.35%**) | 23,331.79 (+7.77%) | 23,991.76 (+4.80%) | **75.99** | +10.66% | +2.90% | 4.66% (26,373.20) |
| Nifty 500 | 23,734.20 | 22,476.10 (+5.60%) | 22,516.27 (+5.41%) | 22,771.75 (+4.23%) | 71.87 | +7.44% | +0.26% | 1.70% (24,144.20) |
| Nifty Bank | 61,034.10 | 56,496.99 (+8.03%) | 56,109.35 (+8.78%) | 56,659.16 (+7.72%) | 76.70 | +10.01% | +5.44% | 1.18% |
| Nifty IT | 31,931.15 | 32,143.98 (−0.66%) | 30,260.24 (+5.52%) | 30,399.83 (+5.04%) | 54.72 | +7.04% | +1.91% | 20.77% |
| Nifty Pharma | 28,535.75 | 26,910.70 (+6.04%) | 26,684.46 (+6.94%) | 24,719.57 (+15.44%) | 72.26 | +9.44% | +6.63% | 2.36% |

- **Trend quality (the honest caveat):**
  - The 200 DMAs are still falling: Nifty 50 −230.02 and Nifty 500 −121.88 over 20 sessions.
  - The 50 DMAs fell too: −279.34 and −446.10.
  - On both indices the **50 DMA is below the 200 DMA** (Nifty 50: 23,331.79 vs 23,991.76; Nifty 500: 22,516.27 vs 22,771.75).
  - Price has moved above a declining 200 DMA after a **+11.26%** rally from the 23 Oct close of 22,600.00. Business Standard attributes it to short covering, FPI buying and an LTCG-relief hint.
  - Nifty 50 RSI 75.99 and Nifty Bank RSI 76.70 are overbought. The Nifty 50 is 4.83% above its EMA20 (23,985.39).
  - Street levels: support 24,700–24,800, resistance 25,400. Citi's end-2027 Nifty target is 28,000.
- **What this means for entries:** chasing breakouts here means buying 6–10% above the 20 DMA into overbought readings. The method rejects those setups (RSI > 75, > 8–10% above EMA20), and that is exactly why every Stage-3 survivor fails Stage 4.

**VIX.** India VIX is **15.50**:
- below its SMA20 of 15.90 (−2.52%) and its EMA20 of 15.81;
- above its SMA50 of 14.00 (+10.71%) and SMA200 of 15.27 (+1.51%);
- +9.77% over 1M (14.12 on 13 Oct), but down 11.73% from the 17.56 peak on 11 Nov.

**Breadth (Nifty 500, computed from Yahoo):**
- **57.72%** (288/499) above the 50 DMA, versus 10.22% on 23 Oct.
- 80.96% above the 20 DMA, and only 48.58% (239/492) above the 200 DMA.
- Nifty 50: 80% above the 50 DMA.
- Cross-checks: IndexBreadth 56.0%, Flash Finance 59.2%.

**Flows and macro.**
- **FII/DII**, sums of NSE daily provisional figures (₹ Cr):

| Period | FII | DII |
|---|---:|---:|
| 26–30 Oct | +6,304.67 | +3,109.79 |
| 2–6 Nov | +45,960.02 | −24,196.52 |
| 9–13 Nov (4 sessions) | +33,342.70 | −24,191.81 |
| 13 Nov | +5,736.55 | −2,253.58 |
| November MTD (incl. Muhurat −0.25 / −700.31) | **+79,302.47** | **−49,088.64** |

  BusinessLine reports an MTD of ₹79,301 Cr. DIIs have been net sellers into the FII buying.
- **Macro:**
  - October CPI is **6.09%**. The RBI MPC meets 2–4 Dec, and a **25 bp hike to 5.75%** is expected, with the decision on **4 Dec, inside the window**.
  - Brent is $95.84 (−9.52% over 1M; peak about $117.64 on 30 Oct). USDINR is 94.03, the 10y G-sec 7.31%, DXY about 103.19.
- **Event calendar:**
  - Nvidia results on 17 Nov US time (India reacts 18 Nov).
  - FOMC minutes (India reacts 19 Nov).
  - November F&O expiry on 23 Nov.
  - Q2 GDP on 30 Nov.
  - RBI MPC decision on 4 Dec.

**Sector RS vs Nifty 500** (NSE `ind_close_all`; 1M base 13 Oct, 3M base 13 Aug; Nifty 500 1M +7.44%, 3M +0.26%; 36 sectoral/thematic indices):

- **Top 5 by 1M RS:** PSU Bank +6.21, Capital Markets +4.12, Realty +3.56, Infrastructure +3.06, Financial Services +2.97.
- **Top 5 by 3M RS:** Media +11.28, Capital Markets +9.94, Private Bank +9.65, Pharma +6.61, Bank +5.58.
- **Bottom 5 by 1M RS:** India Defence −9.19, MidSmall IT & Telecom −7.34, Chemicals −7.15, MNC −4.87, CPSE −4.52.
- **Bottom 5 by 3M RS:** MNC −9.64, Chemicals −8.04, India Defence −7.68, Cement −5.71, Auto −5.30.
- **Favoured groups on both horizons:** Capital Markets (2nd / 2nd), PSU Bank (1st / 7th), Private Bank (9th / 3rd), Pharma (10th / 4th).
- **Ranks for this week's candidates:**
  - IT (HCLTECH): 21st / 12th; it led three weeks ago.
  - Housing (LICHSGFIN): 15th / 15th.
  - Financial Services ex-Bank (IIFL): 19th / 18th.
  - MidSmall IT & Telecom (TANLA): 35th / 13th.

**Classification.**
- Price is above the 20 and 50 DMAs on both indices (pass).
- Breadth is 57.72%, above the 50% line (pass).
- VIX is falling off its spike and below its 20 DMA (pass, but it is still above its 50/200 DMAs).

That makes it **RISK-ON, capped at 5 positions**. The overbought readings and the 50 < falling 200 DMA structure mean **no chasing; pullback (Setup A) entries only**.

---

## 2. Funnel

**Universe construction.**
- **Track A** (≥ ₹12,000 Cr, 226 names):
  - 146 Nifty 500 names pass the data agent's technical pre-screen (close > 50 DMA; 50 > 200 DMA or 200 rising; close ≥ 0.75 × 52wH) at ≥ ₹12,000 Cr.
  - 22 Nifty Microcap 250 names at ≥ ₹12,000 Cr pass the same momentum test plus 3M > Nifty 500.
  - 58 Setup-C-eligible names not already in either list.
- **Track B** (₹5,000–12,000 Cr, 44 names): 1 Nifty 500 technical pass, 32 Microcap 250 momentum passes and 11 Setup-C-eligible names.
  - Run because **Stage 3 at ₹12,000 Cr left 3 names (< 10)**.
- **All 134 Setup-C-eligible names** from the data agent are inside these two tracks (113 in A, 21 in B), so each gets the full Stage 1–4 test. The Setup C exemption waives only the results exclusion.
- **25–49% band:** no Stage-2 passer sits 25–49% below its 52wH. The furthest, HCLTECH, is 22.59% below. So the fresh-Setup-B allowance does not come into play.
- **This analyst funnel replaces the data agent's 17-name main pass.** It adds the PB, forward-PE and value-trap tests. All 17 are accounted for in Appendix C.

**Results / event rule used in Stage 1:**
- An NSE board-meeting intimation for results dated 16 Nov – 7 Dec is a fail, unless the name has already reported (Setup C waives the results test only).
- **38 names filed Q2 after the 13 Nov close.** Their first reaction is 16 Nov (live, inside the window), so their reaction cannot be judged. They are treated as a results event in the window. In the funnel this removes ABB, PTCIL and SHREEJISPG (Track A) and BALUFORGE, JAMNAAUTO, MBAPL and SUNFLAG (Track B).
- **Probable results:** applies when there is no NSE results filing, screener has no Sep-26 quarter, and the prior-year Q2 date falls in the matching window. Only **ENRIN** is caught (prior-year 24 Nov 2025).
- **Major corporate actions** (NSE corporate actions, board meetings, announcements re-queried 16 Nov): **IIFL** has an EGM on **Fri 4 Dec** (session 14 of the window) to approve a ₹6,414 Cr preferential issue (Blackstone ₹5,000 Cr CCPS plus promoter warrants). That is a fail.
  - Dividend ex-dates (for example PFC and MRF on 17 Nov) are noted but not treated as major.
  - DCBBANK's postal ballot (re-appointment of an independent director; e-voting ends 25 Nov) is routine, so it passes.
- F&O ban list for 16 Nov: NIL. GSM list: no candidate hit.

| Stage | Left | Names | What dropped (per-ticker reasons in Appendices A–C) |
|---|---:|---|---|
| 0 regime | — | RISK-ON (late/overbought) | Max 5 positions; pullback entries only |
| Start | **270** | A 226 + B 44 | — |
| **1 tradability** | **223** (A 192 + B 31) | Appendix A | A −34, B −13 (see the table below) |
| **2 relative value + quality** | **5** | HCLTECH, LICHSGFIN, SOUTHBANK; DCBBANK, TANLA | A: PE 137, PB 21, fwd PE 10, fwd PE N/A 16, value-trap 5. B: PE 14, PB 6, fwd PE 2, fwd PE N/A 6, value-trap 1 |
| **3 momentum** | **5** | same | — |
| **4 swing setup** | **0** | — | SOUTHBANK, LICHSGFIN, DCBBANK and TANLA are extended; HCLTECH's Setup A has not triggered |
| **Final picks** (score ≥ 65, stop ≤ 8%, R:R ≥ 2) | **0** | — | Best score 64 (SOUTHBANK) |

**Stage 1 rejection reasons** (a name can carry more than one reason):

| Reason | Track A | Track B |
|---|---:|---:|
| ADV < ₹25 Cr | 11 | 9 |
| Pledge > 20% | 11 | 2 |
| ASM (NSE reportASM, 16 Nov) | 8 | 1 |
| Results filed after the 13 Nov close (reaction 16 Nov, in window) | 3 | 4 |
| Results probable in window | 1 | 0 |
| Major corporate action in window (IIFL EGM 4 Dec) | 1 | 0 |
| **Names rejected** | **34** | **13** |

**Stage 2 waterfall (first binding test, in the order PE → PB → forward PE → value-trap):**

| First failing test | Track A (192) | Track B (31) | All 134 Setup-C names |
|---|---:|---:|---:|
| PE ≥ sub-sector median (or n/m) | 137 | 14 | 87 |
| PB above peer median (beyond the ROE allowance) or peer PB N/A | 21 | 6 | 19 |
| Forward PE ≥ 20 or ≥ trailing PE | 10 | 2 | 3 |
| Forward PE N/A | 16 | 6 | 22 |
| Value-trap filter (EPS/OCF, 3y CAGR, ROE, D/E, net EPS revisions) | 5 | 1 | 1 |
| **Pass** | **3** | **2** | **2** (LICHSGFIN, TANLA) |

- **Forward PE N/A (22 names):** every one of them also fails Stage 3 (for example BANKBARODA, M&M, MARUTI, NTPC, PFC). The missing forward EPS therefore cannot hide a qualifying trade, so no extra fetch was made.
- **Setup-C side:** 125 of 134 pass Stage 1. The 9 fails are 6 pledge (ANURAS, APOLLO, ASTERDM, COHANCE, KALYANKJIL, ONESOURCE) and 3 ASM (ATHERENERG, ENTERO, VEDPOWER). 56 of 134 pass Stage 3, but only **LICHSGFIN** and **TANLA** pass both Stage 2 and Stage 3, and both fail Stage 4.
- **Net-EPS-revision rule:** a name fails if the mean of the FY0 and FY+1 90-day revision % is negative, or, when both are missing, if 30-day down-revisions outnumber up-revisions. This replaces the data agent's stricter "any FY down" flag. It changed one outcome, IIFL (FY27E +9.80%, FY28E −0.63%, net up), and IIFL then fails Stage 1 on the EGM anyway.

**Filters not silently loosened.** No single relaxation produces a trade, because the binding gate is Stage 4 extension, a price-geometry problem: T1 (the 52wH) sits only 1–2% above price. These are the smallest relaxations that would re-open research; none is applied.
1. **Dropping "fwd PE < trailing" for banks** re-admits **UNIONBANK** (gap +0.24%) and **PNB** (gap +7.40%). Both are extended: RSI 73.14 / 81.52, +7.69% / +12.34% vs EMA20.
2. **Waiving the IIFL EGM** (4 Dec, session 14) re-admits IIFL. It has no valid setup: the 11 Nov +6.26% spike on 7.31× volume faded back to 641.10 (−3.77% from 666.25), and R:R to the 694.40 spike high is poor.
3. **HCLTECH's trigger** cannot be relaxed. Setup A needs the reversal close, and even then the score is 40.

---

## 3. Shortlist table

All five Stage-3 survivors plus two scored near-misses. **None is eligible.**

| Ticker | Sub-sector | Mcap (₹Cr) | PE prem vs sub-sector | PB prem vs peers | Fwd PE (Yahoo / SA) | % below 52W high | 3M RS vs Nifty 500 | Setup | Score | Status |
|---|---|---:|---:|---:|---:|---:|---:|---|---:|---|
| SOUTHBANK | Private Sector Bank | 16,209 | −24.11% (10.2 vs 13.44) | −16.02% (1.342 vs 1.598) | 8.14 / 8.64 | 1.13% | +33.58 pp | none (extended) | **64** | not eligible: Stage 4 (RSI 76.16, +10.54% vs EMA20) |
| UNIONBANK | Public Sector Bank | 1,54,962 | −11.94% (7.04 vs 7.995) | +5.16% (ROE 15.7 > 13.0, allowed) | 7.06 / 7.19 **≥ trailing** | 1.21% | +8.30 pp | C held, extended | 61 | not eligible: Stage 2 (fwd PE) + Stage 4 |
| LICHSGFIN | Housing Finance Company | 32,184 | −55.97% (5.46 vs 12.40) | −54.74% (0.733 vs 1.620) | 5.25 / 5.36 | 2.19% | +14.92 pp | C (weak), extended | 58 | not eligible: Stage 4 (+9.15% vs EMA20) + Stage 6 (R:R 0.50) |
| DCBBANK (B) | Private Sector Bank | 7,509 | −33.48% (8.94 vs 13.44) | −39.91% (1.084 vs 1.804, pooled n=13) | 6.69 / N/A | 1.08% | +23.52 pp | none (extended) | 58 | not eligible: Stage 4 (+12.44% vs EMA20) |
| IIFL | NBFC | 27,376 | −39.02% (11.0 vs 18.04) | −40.75% (1.771 vs 2.989) | 8.35 / 8.75 | 9.06% | +2.19 pp | none (spike faded) | 55 | not eligible: Stage 1 (4 Dec EGM) |
| TANLA (B) | Software Products | 9,721 | −44.71% (17.5 vs 31.65) | −15.04% (3.575 vs 4.208) | 15.83 / 16.07 | 0.82% | +23.04 pp | C held, extended | 51 | not eligible: Stage 4 (RSI 82.98, +15.81% vs EMA20) |
| HCLTECH | Computers – Software & Consulting | 3,73,943 | −1.36% (19.6 vs 19.87; **Yahoo PE 20.39 would flip it**) | +7.32% (ROE 23.8 > 22.25, allowed) | 17.20 / 18.28 | 22.59% | +0.66 pp | A forming, not triggered | 40 | not eligible: Stage 4 + score |

Score breakdowns (Relative value 25 / Quality 15 / Momentum & RS 20 / Setup & R:R 25 / Catalysts 15):

- **SOUTHBANK: 21 / 12 / 18 / 3 / 10 = 64.**
  - Relative value: PE −24.11% and PB −16.02%; fwd PE 8.14 / 8.64 is below trailing on both sources.
  - Quality: ROE 13.5% vs 11.5% median; 3y CAGR 11%/23%. GNPA 1.24% and NNPA 0.09% (Q2). CRAR is 19.40% per ICICI Direct and the call; MarketsMojo shows 15.95%, which conflicts.
  - Momentum: 1.13% below the 62.57 all-time high; RS3M +33.58, RS1M +18.47; Private Bank 9th / 3rd.
  - Setup: RSI 76.16, +10.54% vs EMA20. From 61.86, a 1.5 × ATR stop (ATR 1.966) gives R:R to 62.57 of **0.24**.
  - Catalysts: ICICI Securities TP 63; FY27E/FY28E EPS revised up; DII +2.54 pp. Lost points: Yahoo mean TP 56.33 is **8.93% below** the price.
- **UNIONBANK: 15 / 12 / 18 / 6 / 10 = 61.**
  - Relative value: forward EPS 28.767 must exceed 28.835 (+0.24%) to pass.
  - Quality: GNPA 2.42%, NNPA 0.42%, CAR 17.94%, PCR 95.2%; OCF −₹358 Cr.
  - Momentum: PSU Bank ranks 1st on 1M.
  - Setup: Setup C (19 Oct) still held, but RSI 73.14 and +7.69% vs EMA20.
  - Catalysts: TP 205.94 (+1.45%).
- **LICHSGFIN: 22 / 9 / 15 / 5 / 7 = 58.**
  - Relative value: deepest discount in the funnel.
  - Quality:
    - AUM growth +5% vs 12–14% guidance. Disbursements +11% YoY / +21% QoQ.
    - NIM 2.58% (guidance 2.5–2.6%). Stage 3 assets 2.05% (from 2.51%), PCR 49%.
    - Credit cost negative on recoveries. NNPA and CAR are N/A in the data.
  - Momentum: Housing ranks 15th / 15th; RS1M −3.70.
  - Setup:
    - The Setup C is weak: Q2 revenue +0.21%, PAT +11.71%, and the gap was only +0.32% (filed 30 Oct 20:43 IST).
    - Price is up +18.51% since then. R:R to the 598.20 52wH is **0.50**, using a 1.5 × ATR stop (ATR 17.59).
  - Catalysts: 14 Buy / 8 Hold / 3 Sell, TP 594.24 (+1.56%). FII −2.54 pp, DII +0.61 pp. New MD & CEO (Sandeep Kumar, since 29 Aug 2026). LHPLR +25 bp from 31 Oct.
- **DCBBANK: 20 / 9 / 17 / 3 / 9 = 58.**
  - Relative value: the peer PB median is pooled (n=13), and fwd PE is single-source (Yahoo).
  - Quality: ROE 12.0% vs 11.6%; 3y CAGR 21%/16%.
  - Setup: +12.44% vs EMA20.
  - Catalysts: TP 245.94 (+5.55%). Red flag: the Head of Corporate Banking, Construction Finance & SME (senior management) resigned and was relieved on 4 Nov.
- **IIFL: 21 / 8 / 12 / 4 / 10 = 55.**
  - Relative value: discount offset by dilution. The issue raises 23.43% of market cap, and the CCPS convert at ₹602 (−6.10% vs close).
  - Quality: ROE 12.6% < 14.7% median; 3y profit CAGR 3%. CAR rises from about 17% to about 30% after the raise.
  - Catalysts: Blackstone ₹5,000 Cr CCPS; promoters ₹1,264 Cr warrants. TP 788.33 (+22.97%).
- **TANLA: 20 / 10 / 14 / 2 / 5 = 51.**
  - Quality: ROE 21.4%, but 3y profit CAGR only 4%.
  - Momentum: MidSmall IT & Telecom ranks 35th on 1M.
  - Setup: RSI 82.98.
  - Catalysts: 1 Buy / 1 Sell; TP 619 (−15.54%).
- **HCLTECH: 9 / 12 / 7 / 8 / 4 = 40.**
  - Relative value: PE only −1.36%, and Yahoo's PE flips the test.
  - Quality: ROE 23.8%, D/E 0.08; 3y CAGR 9%/6%; revisions FY27E +2.16%, FY28E +2.25%.
  - Momentum: 22.59% below the 52wH; RS1M −3.52; IT 21st / 12th; 200 DMA falling (−24.72).
  - **Setup (hypothetical, not a plan):** entry 1,397 above the 13 Nov high, stop 1,362 (2.51%, only 0.90 × ATR 38.73), T1 1,469 (6 Nov high). That gives R:R 2.06 (maximum legal entry 1,397.67), 14 shares, ₹19,558. A 1.5 × ATR stop (1,338.90) cuts R:R to **1.24**.
  - Catalysts: 14 Buy / 16 Hold / 9 Sell; mean TP 1,273.54 is **7.58% below** the price; Citi Sell, TP 1,200.

---

## 4. Final picks

**None this week.** Every candidate fails at least one hard gate (Appendices A–C), and the best score, 64, is below 65.

| Book | Shares | Exposure | Note |
|---|---:|---:|---|
| Open positions | — | ₹0 | SOUTHBANK closed at T1 on 29 Oct (+₹1,052.52) |
| Cash | — | **₹50,000** of the exposure cap available | Equity ₹51,052.52 including realised P&L |
| **Total** | 0 of 5 slots | **₹0** | — |

---

## 5. Watchlist (3 near-misses)

None of these are orders. Each plan is indicative and applies only once **every** listed condition is met.

**Common rules for all three:**
- **Order type:** close-confirmed. After the reversal-close condition prints, place a **buy limit at or below the maximum legal entry** for the next session; never a market order.
- **Exit split:** **half the shares at T1** (resting limit sell). Then move the stop on the remainder to **breakeven (the entry price)**, and sell the rest at T2 (resting limit sell).
- **Time stop:** exit at the close of the 10th session after the fill unless a close has printed at least halfway from entry to T1.
- **Invalidation:** a daily close below the stop level exits the full position (hard stop working as a stop-loss order).
- **Market filter:** no new fill on a day the Nifty 500 closes below its 20 DMA (22,476.10 today).
- Size = floor(₹500 ÷ (entry − stop)); maximum legal entry = (T1 + 2 × stop) ÷ 3.

### SOUTHBANK (Private Sector Bank, ₹16,209 Cr): passes Stages 1–3; re-entry on a pullback

- **As of 13 Nov:** close **61.86**; EMA20 55.96 (+10.54%); SMA50 50.63; SMA200 44.43 (rising, +1.51 over 20 sessions); RSI14 76.16; ATR14 1.966; all-time high 62.57 (13 Nov).
- **Base reference:** 23 Oct – 6 Nov range 51.70–57.90 (height 6.20). The breakout above 57.90 came on 9 Nov.
- **Would qualify (Setup A) only if all of:**
  1. Price pulls back to **≤ 57.72**, a retest of the 57.90 breakout level as the EMA20 rises. Volume must be below its 20-day average.
  2. The low holds above **55.47** (the 6 Nov swing low).
  3. RSI cools into 40–55 and turns up, with a bullish reversal close.
  4. Stage 2 still holds (PE and PB below median; fwd PE below trailing).
- **Indicative plan:**
  - Entry 57.70 (maximum legal 57.72); stop 55.30 (4.16%, below the 6 Nov low).
  - T1 **62.57** (R:R 2.03); T2 **64.10** (57.90 + 6.20 measured move; R:R 2.67).
  - **208 shares**, ₹12,001.60 exposure, risk ₹499.20. Split: **104 at T1, 104 at T2.**
  - Alerts: 57.72 (zone), 55.47 (swing low), 62.57 (T1).

### LICHSGFIN (Housing Finance Company, ₹32,184 Cr): deep value, extended after a weak Setup C

- **As of 13 Nov:** close **585.10**; EMA20 536.05 (+9.15%); SMA50 537.50; SMA200 532.58 (flat, −1.15 over 20 sessions); RSI14 69.58; ATR14 17.59; 52wH 598.20 (11 May 2026). Five-year weekly chart: 2025 high 646.50, 2024 high 826.75.
- **Would qualify (Setup A) only if all of:**
  1. Price pulls back to **≤ 547.40** (the 9 Nov breakout area at 551.90, with the EMA20 rising toward it) on volume below its 20-day average of 2.21 mn shares.
  2. The low holds above **523.20** (the 6 Nov swing low).
  3. RSI is back in 40–55 and turning up, with a bullish reversal close.
  4. No negative surprise on the LHPLR hike pass-through or on AUM growth (+5% vs 12–14% guidance).
- **Indicative plan:**
  - Entry 547.00 (maximum legal 547.40); stop 522.00 (4.57%).
  - T1 **598.20** (52wH; R:R 2.05); T2 **646.50** (2025 high; R:R 3.98).
  - **20 shares**, ₹10,940.00 exposure, risk ₹500.00. Split: **10 at T1, 10 at T2.**
  - Alerts: 547.40, 523.20, 598.20.

### UNIONBANK (Public Sector Bank, ₹1,54,962 Cr): top 1M sector, fails forward PE by 0.24%

- **As of 13 Nov:** close **203.00**; EMA20 188.50 (+7.69%); SMA50 180.70; SMA200 177.26 (rising, +2.35); RSI14 73.14; ATR14 4.994; 52wH 205.49 (27 Feb). Base 23 Oct – 6 Nov: 177.30–188.90 (6.54% wide). Breakout 9 Nov on 1.17× volume, 11 Nov on 1.80×.
- **Would qualify only if all of:**
  1. **Consensus forward EPS rises above 28.835**, so that fwd PE < trailing 7.04. Yahoo's figure is 28.767, so it needs +0.24%. This is a fundamental condition, independent of price.
  2. A Setup A pullback to **≤ 191.22**, a retest of the 188.90 base top, on volume below the 20-day average of 18.39 mn shares.
  3. The low holds above **184.45** (the 6 Nov low).
  4. RSI is in 40–55 and turning up, with a reversal close.
- **Indicative plan:**
  - Entry 191.00 (maximum legal 191.22); stop 184.20 (3.56%).
  - T1 **205.25** (13 Nov high; R:R 2.10); T2 **216.85** (205.25 + 11.60 base height; R:R 3.80).
  - **73 shares**, ₹13,943.00 exposure, risk ₹496.40. Split: **36 at T1, 37 at T2.**
  - RBI MPC on 4 Dec: a repo hike helps EBLR-linked NIMs but raises deposit costs, so review the plan if it fills before the decision.

Not on the list: IIFL. Revisit after the 4 Dec EGM. The CCPS convert at ₹602, 6.10% below the 13 Nov close.

---

## 6. Value traps rejected (cheap ≠ trade)

- **GESHIP:** PE 4.89 vs 10.34 (−52.71%), but fwd PE **6.43 (Yahoo) / 5.44 (SA) > trailing** and 3y revenue/profit CAGR **−2%/0%**. Freight-cycle peak risk; 5y EV/EBITDA N/A.
- **MRPL:** PE −47.86%, but PB +19.35% with ROE 14.5% < 16.3% median. 3y CAGR **−7%/−10%**, and EPS revised down over 90 days: FY27E −9.59%, FY28E −21.19%. A refiner at peak margins.
- **PETRONET:** PE −12.86%, but PB +25.82%, fwd PE 11.16 > trailing 10.5, and 3y revenue CAGR **−10%**.
- **SUNTV:** PE 16.0 vs 30.38 (−47.33%), but 3y profit CAGR **−4%**. The peer PB median (0.356) is distorted and was not relied on.
- **ADANIPOWER:** PE −7.55%, but PB **+279.89%**, fwd PE 26.34 ≥ 20 and > trailing 21.8, and 3M −0.64% < Nifty 500.
- **SAIL:** PE −35.31% and PB −48.23%, but **ROE 6.57%**. Cyclical; 5y EV/EBITDA N/A.
- **AUROPHARMA:** PE −36.66% and PB −42.88%, but **ROE 10.1%** vs the 17.4% median.
- **KTKBANK:** PE −34.45% and PB −45.46%, but **ROE 10.4%** vs the 11.6% median.
- **PCJEWELLER:** PE −17.79%, but **OCF −₹77 Cr** and ROE 9.96% vs a 28.1% median.
- **PNGJL (Track B):** PE −9.57%, but **OCF −₹717 Cr**.
- **MSTCLTD (Track B):** PE −23.55%, but 3y revenue CAGR **−20%**, profit −3%, OCF −₹28 Cr; no peer PB, no forward PE.
- **OBEROIRLTY:** PE −14.65% and PB −3.09%, but net downward EPS revisions (FY27E −1.12%, 5 up / 8 down in 30 days), and 3M −0.13% < Nifty 500.
- **PNB:** PE −10.19%, but consensus EPS is **below TTM** (fwd PE 7.71 / 7.82 vs 7.18), so earnings are expected to fall about 7%. Asset quality is improving, so this is a watch rather than a trap, but the stock is extended (RSI 81.52).
- **GAIL:** PE 9.79, exactly at the median (0.00%, so it fails "<"). It would also fail on **ROE 8.71%**, 3y revenue CAGR −1% and fwd PE 10.60 > trailing; no peer PB; 5y EV/EBITDA N/A.

---

## 7. Data sources & timestamps

**DATA_MODE: WEB (fallback).**

**MCP_ERROR:** "screener / screener-core MCP namespaces are absent from the tool catalog in this environment (GetDynamicTools pattern search 'screener' returned 0 matches on 2026-11-16). Not authenticated, per run rules."

| Source | As-of | Used for |
|---|---|---|
| Yahoo v8 chart (indices, Nifty 500, Microcap 250 and Setup-C names; live 16 Nov bars dropped) | 13 Nov close | DMAs, EMA20, RSI14, ATR14, returns, breadth, last 20 bars |
| NSE bhavcopy `sec_bhavdata_full_*` (15 Oct – 13 Nov; 15 Sep – 14 Oct for SOUTHBANK averages; Muhurat 8 Nov) | 13 Nov | Official closes, ADV, delivery %, SOUTHBANK settlement OHLC |
| NSE `ind_close_all` (13 Nov, 6 Nov, 13 Oct, 13 Aug) | 13 Nov | Sector 1M/3M RS vs Nifty 500 |
| NSE APIs: reportASM/GSM, corporate-board-meetings, corporate-announcements, corporates-corporateActions, fiidiiTradeReact; `fo_secban.csv` (16 Nov: NIL); bulk/block deals | 16 Nov (ASM/ban/board), 13 Nov (flows, deals) | Surveillance, results window, Setup C timing, corporate actions |
| NSE SHP XBRL | 30 Sep 2026 | Promoter pledge |
| screener.in company + industry pages | 13 Nov prices (14 pages rescaled to the NSE close) | PE, PB, ROE, D/E, OCF, CAGRs, quarters, holdings, sub-sector PE medians (top 25), peer PB/ROE medians (n=12) |
| Yahoo quoteSummary / stockanalysis statistics | 16 Nov (fwd PE = 13 Nov close ÷ forward EPS) | Forward PE (two sources), ratings, targets, EPS revisions |
| Web search (`news.md`, 122 items) | to 16 Nov | Flows, macro, broker views, company news |

Full source list and method notes: `data_sources.md`.

**Additional data fetched by the analyst** (16 Nov 2026, about 04:15–04:30 UTC = 09:45–10:00 IST; scripts in `raw/analyst_*.py`):

1. **NSE re-query** (`raw/analyst_nse_recheck.py`) of `api/corporate-board-meetings?symbol=` and `api/corporate-announcements` (26 Oct – 16 Nov) for IIFL, UNIONBANK, LICHSGFIN, HCLTECH, SOUTHBANK, DCBBANK and TANLA. All HTTP 200, with a Referer header and no cookie.
   - IIFL: preferential-issue filings (10 Nov) and EGM notice (12 Nov).
   - DCBBANK: senior-management resignation (relieved 4 Nov) and a postal-ballot notice.
   - The other five: no results or major corporate action in the window.
2. **IIFL filings** (pypdf):
   - `IIFL_12112026004505_SE_Intimation.pdf`: EGM on Fri 4 Dec 2026, 11:00; cut-off 27 Nov.
   - `IIFL_10112026164007_SEIntimation.pdf`, press release: Blackstone ₹5,000 Cr CCPS converting at ₹602 within 18 months; promoters ₹1,264 Cr warrants; Anchorage ₹150 Cr; CAR about 17% → about 30%.
3. **DCBBANK filings:** resignation of Jayaram Vishwanath, Head Corporate Banking, Construction Finance & SME (SMP), relieved 4 Nov. Postal ballot to re-appoint independent director Thiyagarajan Kumar; e-voting ends 25 Nov, result by 27 Nov (routine, not major).
4. **LICHSGFIN Q2 FY27 earnings-call transcript:** `https://cdn.lichousing.com/2026/11/Concall-Transcript_Q2_FY2027.pdf`. HTTP 200, 18 pages, pypdf. The NSE filing is only a link letter. Used for guidance, management and asset quality.
5. **Yahoo v8 five-year weekly charts** (`range=5y&interval=1wk`, Windows Chrome UA) for LICHSGFIN, UNIONBANK, IIFL, HCLTECH and SOUTHBANK. HTTP 200 at about 04:18 UTC on 16 Nov. Bars after the 13 Nov week were ignored. Used for overhead resistance and T2 levels (LICHSGFIN 2025 high 646.50).
6. **Web search: IIFL 11 Nov volume spike.** Rediff/PTI and the ACML "Hot Pursuit" note of 11 Nov, 14:40, tie it to the Blackstone preferential-issue announcement.
7. **Recompute** (`raw/analyst_funnel.py`): Stages 1–3 for all 270 names and the 134 Setup-C names, from the data agent's `/tmp/run1116` intermediates.
   - `raw/analyst_numbers.py` covers the regime deltas, the SOUTHBANK settlement, R:R, sizes and scores.
   - `raw/analyst_table.py` generates the Appendix lists.
   - These three scripts replace the 26 Oct `analyst_stage1.py` and `analyst_final_numbers.py`, which were not carried over separately.

**Known gaps:**
- **Peer-PB medians are distorted** for four sub-sectors: telecom (BHARTIARTL, TATACOMM: median ≤ 0), TV broadcasting (SUNTV: 0.356) and holding companies (ABCAPITAL, CHOLAHLDNG: 0.686). Each of these names fails another hard test, so no verdict depends on these medians.
- Peer PB N/A for CONCOR, HINDALCO, ITC, VEDL, VOGL, HEGAM, KRBL, MSTCLTD and TITAGARH. All of them also fail ROE, OCF, CAGR, D/E or Stage 3.
- **Forward PE N/A for 22 names**, all of which fail Stage 3.
- DCBBANK forward PE is single-source. Its peer PB median is pooled from the same industry page (n=13).
- LICHSGFIN (HFC) NNPA and CAR are N/A. SOUTHBANK CAR conflicts: 19.40% (ICICI Direct / call) vs 15.95% (MarketsMojo).
- 5y EV/EBITDA is N/A for the cyclicals (ADANIPOWER, MRPL, GESHIP, PETRONET, GAIL, SHYAMMETL, NUVOCO).
- Cross-source PE flips: HCLTECH (Yahoo 20.39 vs median 19.87), GLENMARK and SUNPHARMA. GLENMARK and SUNPHARMA fail Stage 2 regardless; HCLTECH would be capped at Medium confidence if it ever became a pick.
- **38 Setup-C reactions pending** (filed after the 13 Nov close; reaction 16 Nov is live), including ABB, EICHERMOT, TMPV, ASHOKLEY and KAYNES. They are re-assessable next week.
- Bulk deals 30 Oct – 12 Nov are partial (70-row API cap); block deals are complete.
- The NSE financial-results API returned empty again.
- ENRIN's Q2 status is inferred: there is no NSE results filing and no Sep-26 quarter on screener, and the prior-year date was 24 Nov 2025.
- FII MTD: the analyst's two-week sum excluding Muhurat (+79,302.72) differs from the data agent's +79,302.47 including Muhurat. The latter is used; the difference is ₹0.25 Cr, the Muhurat figure.

---

## 8. Reminder

This is research, not financial advice. Position sizing (₹500 risk per trade) and hard stops are mandatory. This week: no new order. The book is flat after SOUTHBANK's T1 exit (+₹1,052.52); watchlist plans apply only once every condition is met.

---

## Appendix A — Stage 1 rejections (47) and survivors (223)

**Track A (226 → 192):**

- **ADV < ₹25 Cr (11):** AEGISVOPAK 23.25, AIIL 12.64, ASAHIINDIA 21.25, DEVYANI 20.33, ELGIEQUIP 21.06, LTFOODS 17.17, MINDACORP 24.73, NUVOCO 10.18, PGIL 18.20, POLYMED 13.90, TMB 16.88.
- **Pledge > 20% (11):** AEQUS 25.36%, ANURAS 32.85%, APOLLO 35.57%, ASTERDM 66.99%, COHANCE 94.56%, KALYANKJIL 24.85%, MPHASIS 100.0%, NAZARA 87.74%, NUVAMA 62.80%, ONESOURCE 38.79%, THELEELA 73.65%.
- **ASM (8):** ATHERENERG, CUPID, RUBICON, SANSERA, SHILPAMED, SHREEJISPG, SKYGOLD (all LT-ASM I), VEDPOWER (ST-ASM I).
- **Results filed after the 13 Nov close, reaction 16 Nov (3):** ABB, PTCIL, SHREEJISPG.
- **Results probable in window (1):** ENRIN (prior-year 24 Nov 2025).
- **Major corporate action (1):** IIFL (4 Dec EGM, ₹6,414 Cr preferential issue).

**Track B (44 → 31):**

- **ADV < ₹25 Cr (9):** CEIGALL 12.41, DYNAMATECH 23.32, FEDFINA 18.23, GPPL 19.00, JAMNAAUTO 24.08, MBAPL 19.76, METROPOLIS 13.12, QUESS 8.90, SUNFLAG 8.06.
- **Pledge > 20% (2):** NEOGEN 23.0%, TARIL 21.84%.
- **ASM (1):** ENTERO (ST-ASM I).
- **Results filed after the 13 Nov close, reaction 16 Nov (4):** BALUFORGE, JAMNAAUTO, MBAPL, SUNFLAG.

**Stage 1 survivors:** 192 in Track A and 31 in Track B. Full lists in `/tmp/analyst-2026-11-16/funnel.json`; regenerate with `raw/analyst_funnel.py`. The Track B survivors are AARTIPHARM, BLUEJET, BSOFT, CENTUM, DCBBANK, GREAVESCOT, HEGAM, ICIL, IIFLCAPS, IRCON, JUSTDIAL, KMEW, KRBL, LOTUSDEV, MSTCLTD, NCC, PDSL, PNGJL, PRICOLLTD, QPOWER, SGMART, SONATSOFTW, TANLA, TIPSMUSIC, TITAGARH, TRIDENT, TTKPRESTIG, TTML, UNIMECH, WESTLIFE and YATHARTH.

## Appendix B — Stage 2 (Track A 192 → 3; Track B 31 → 2) and Stage 3

**Track A, first binding test:**

- **PB test (21):** ABCAPITAL +281.4%, ADANIPOWER +279.9%, BHARTIARTL (peer median ≤ 0, not meaningful), CHOLAHLDNG +133.5%, CONCOR (peer PB N/A), EMCURE +79.7%, ENGINERSIN +62.9%, GLENMARK +58.7%, HINDALCO (N/A), ITC (N/A), KARURVYSYA +50.2%, LODHA +51.5%, LUMAXTECH +28.4%, MRF +7.9% (ROE below median), MRPL +19.3% (ROE below median), MSUMI +40.1%, PETRONET +25.8%, SUNPHARMA +20.6% (ROE below median), SUNTV +432.4% (distorted median), VEDL (N/A), VOGL (N/A).
- **Forward PE ≥ 20 or ≥ trailing (10):** AARTIIND 23.84, ASTRAMICRO 51.75, CIPLA 22.33, GESHIP 6.43 vs 4.89, MOTHERSON 23.19, PNB 7.71 vs 7.18, PVRINOX 23.83, UNIONBANK 7.06 vs 7.04, ZENTEC 31.78, ZYDUSLIFE 24.14.
- **Forward PE N/A (16, all fail Stage 3):** APOLLOTYRE, BANKBARODA, BEL, DEEPAKNTR, EMAMILTD, EXIDEIND, HUDCO, IOC, M&M, MARUTI, NH, NLCINDIA, NTPC, PFC, VGUARD, ZENSARTECH.
- **Value-trap (5):** AUROPHARMA (ROE 10.1), KTKBANK (ROE 10.4), OBEROIRLTY (net down revisions), PCJEWELLER (OCF −77, ROE 9.96), SAIL (ROE 6.57).
- **PE ≥ median (137).** The near-misses within 5% are APOLLOHOSP +1.03%, ASAHIINDIA 0.00%, BHEL +0.76%, DRREDDY +1.15%, GAIL 0.00%, NUVOCO +4.94%, SHYAMMETL +0.97%, STARHEALTH +0.03% and TATACOMM +1.14%. The full list with premiums is in `raw/analyst_table.py` output.
- **Pass (3):** HCLTECH, LICHSGFIN, SOUTHBANK.

**Track B, first binding test:**
- PE ≥ median (14): BLUEJET, GREAVESCOT, ICIL, IRCON, JUSTDIAL, KMEW, LOTUSDEV, PDSL, QPOWER, SGMART, TIPSMUSIC (0.00%), TTML (n/m), UNIMECH, WESTLIFE.
- PB (6): CENTUM +22.4%, HEGAM (N/A), IIFLCAPS +28.8%, KRBL (N/A), MSTCLTD (N/A), TITAGARH (N/A).
- Fwd PE (2): AARTIPHARM 39.14, YATHARTH 36.33.
- Fwd PE N/A (6, all fail Stage 3): BSOFT, NCC, PRICOLLTD, SONATSOFTW, TRIDENT, TTKPRESTIG.
- Value-trap (1): PNGJL (OCF −717).
- **Pass (2):** DCBBANK, TANLA.

**Stage 3:** all five pass.

| Ticker | % below 52wH | Close > 50 DMA | 50 DMA vs 200 DMA | 3M vs Nifty 500 (+0.26%) |
|---|---:|---|---|---:|
| HCLTECH | 22.59% | 1,378.00 > 1,315.95 | 1,315.95 > 1,313.64 | +0.92% (+0.66 pp) |
| LICHSGFIN | 2.19% | 585.10 > 537.50 | 537.50 > 532.58 | +15.18% (+14.92 pp) |
| SOUTHBANK | 1.13% | 61.86 > 50.63 | 50.63 > 44.43 (rising) | +33.84% (+33.58 pp) |
| DCBBANK | 1.08% | 233.01 > 210.19 | 210.19 > 191.65 (rising) | +23.78% (+23.52 pp) |
| TANLA | 0.82% | 732.90 > 551.05 | 551.05 > 521.54 (rising) | +23.30% (+23.04 pp) |

## Appendix C — Data agent's 17 main-pass names (why they do not survive)

| Ticker | Analyst verdict |
|---|---|
| ADANIPOWER | Stage 2: PB +279.89%; fwd PE 26.34 |
| EMCURE | Stage 2: PB +79.74%; fwd PE 29.11 |
| ENGINERSIN | Stage 2: PB +62.88%; fwd PE 22.00 > trailing 19.6 |
| GESHIP | Stage 2: fwd PE 6.43 > trailing 4.89; 3y CAGR −2%/0% |
| GLENMARK | Stage 2: PB +58.72%; fwd PE 27.38 |
| **HCLTECH** | **Passes Stages 1–3**; Stage 4 not triggered; score 40 |
| KARURVYSYA | Stage 2: PB +50.18% |
| LODHA | Stage 2: PB +51.49%; fwd PE 23.56 |
| MINDACORP | Stage 1: ADV ₹24.73 Cr; also fwd PE 31.10 |
| MRPL | Stage 2: PB +19.35% with ROE 14.5 < 16.3; 3y CAGR −7%/−10% |
| OBEROIRLTY | Stage 2: net downward revisions; Stage 3: 3M −0.13% |
| PETRONET | Stage 2: PB +25.82%; fwd PE 11.16 > 10.5; 3y revenue CAGR −10% |
| PNB | Stage 2: fwd PE 7.71 > trailing 7.18 |
| SUNPHARMA | Stage 2: PB +20.62%; fwd PE 29.94 |
| SUNTV | Stage 2: 3y profit CAGR −4% (PB median distorted) |
| UNIONBANK | Stage 2: fwd PE 7.06 ≥ trailing 7.04 (+0.24%) |
| ZYDUSLIFE | Stage 2: fwd PE 24.14 |

Financials variant (data agent, 4 names): AIIL fails Stage 1 (ADV ₹12.64 Cr; PE +55.21%); IIFL fails Stage 1 (EGM); **LICHSGFIN passes Stages 1–3**; PNB fails Stage 2 (fwd PE).
Data agent's Track B value passes (4): BALUFORGE (Stage 1, reaction 16 Nov); MSTCLTD and PNGJL (value traps, §6); **TANLA** (Stages 1–3 pass, Stage 4 fail).

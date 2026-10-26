"""Analyst final arithmetic (run 2026-10-26). Every R:R / size / % quoted in analysis.md is recomputed here."""
import math


def rr(e, s, t):
    return (t - e) / (e - s)


def plan(name, e, s, t1, t2=None):
    risk = e - s; sh = math.floor(500 / risk)
    print(f"{name}: entry {e:.2f} stop {s:.2f} ({risk / e * 100:.2f}%) T1 {t1:.2f} R:R {rr(e, s, t1):.3f}"
          + (f" T2 {t2:.2f} R:R2 {rr(e, s, t2):.3f}" if t2 else '')
          + f" shares {sh} exposure {sh * e:,.2f} risk {sh * risk:.2f} maxE(RR2) {(t1 + 2 * s) / 3:.2f}")


print('PE/PB premiums')
for t, a, b in [('GRWRHITECH', 38.4, 22.43), ('TIPSMUSIC', 40.1, 30.115), ('ANANDRATHI', 81.6, 42.975), ('CASTROLIND', 18.7, 9.81),
                ('COFORGE', 38.8, 22.03), ('CYIENT', 33.3, 32.98), ('FEDERALBNK', 16.2, 12.425), ('ICICIBANK', 17.0, 12.425),
                ('INDHOTEL', 55.4, 29.085), ('KOTAKBANK', 20.2, 12.425), ('PERSISTENT', 48.4, 22.03), ('TECHM', 30.7, 22.03),
                ('IXIGO', 54.5319, 18.15), ('TATAELXSI', 32.0202, 22.03), ('TCS PB', 7.69, 4.7408), ('LTTS PE', 29.7, 32.98),
                ('IPCALAB PB', 6.1415, 4.6512), ('GESHIP PE', 5.7, 12.0), ('SUNTV PE', 14.4, 22.325), ('TANLA PE', 13.9, 27.84), ('TANLA PB', 2.9628, 4.3149),
                ('SB PE', 8.68, 12.425), ('SB PB', 1.141, 1.4583), ('PNB PE', 6.05, 6.885), ('PNB PB', 0.8571, 0.8878),
                ('UNIONBANK PE', 6.1965, 6.885), ('UNIONBANK PB', 0.9466, 0.8571), ('HCLTECH PE', 20.3, 22.03), ('HCLTECH PB', 5.0786, 4.7408),
                ('CHENNPETRO PE', 3.85, 14.99), ('CHENNPETRO PB', 1.6166, 1.3629), ('PCJ PE', 19.7, 22.67), ('JUSTDIAL PE', 11.8495, 13.85)]:
    print(f"  {t}: {a} vs {b} -> {(a / b - 1) * 100:+.2f}%")

print('SOUTHBANK follow-up')
E, S, T1, T2, SH = 51.45, 48.90, 56.82, 58.35, 196
print(f"  R:R T1 {rr(E, S, T1):.3f} T2 {rr(E, S, T2):.3f}; MTM 23-Oct {(52.57 - E) * SH:.2f} ({(52.57 / E - 1) * 100:.2f}%); "
      f"value {52.57 * SH:,.2f}; gap to stop from close {(52.57 - S) / 52.57 * 100:.2f}%; to T1 {(T1 / 52.57 - 1) * 100:.2f}%; R:R from 23-Oct close to T1 {rr(52.57, S, T1):.3f}")
print(f"  pct below 52wH {(1 - 52.57 / 56.25) * 100:.2f}; vs EMA20 {(52.57 / 50.41 - 1) * 100:.2f}%; breakout level 50.68 vs close {(52.57 / 50.68 - 1) * 100:.2f}%")
print(f"  Yahoo mean TP 56.33 vs close {(56.33 / 52.57 - 1) * 100:+.2f}%; median 61.0 {(61.0 / 52.57 - 1) * 100:+.2f}%")
print(f"  cash after SB {50000 - 10084.20:,.2f}")
print(f"  Nifty 500 19-Oct 22041.6 vs SMA20 22208.44 {(22041.6 / 22208.44 - 1) * 100:+.2f}% (published filter level 22248.39 {(22041.6 / 22248.39 - 1) * 100:+.2f}%)")

print('PNB (near miss)')
print(f"  fwd EPS needed > TTM 19.89: Yahoo 18.519 needs {(19.89 / 18.519 - 1) * 100:+.2f}%; SA implied 18.24 needs {(19.89 / 18.24 - 1) * 100:+.2f}%")
print(f"  R:R at 120.37 stop 113.95 T1 125.22: {rr(120.37, 113.95, 125.22):.3f}; stop% {(120.37 - 113.95) / 120.37 * 100:.2f}")
plan('  PNB indicative Setup A', 117.70, 113.95, 125.22, 135.15)
print(f"  TP mean 129.94 vs close {(129.94444 / 120.37 - 1) * 100:+.2f}%; 3M RS {9.28 + 6.765:.2f}; % below 52wH {(1 - 120.37 / 135.15) * 100:.2f}")
print('HCLTECH (near miss)')
print(f"  stop to gap-day low 1238.2: {(1422.2 - 1238.2) / 1422.2 * 100:.2f}%; vs EMA20 {(1422.2 / 1318.6 - 1) * 100:.2f}%; 3M RS {14.26 + 6.765:.2f}; TP mean 1269.69 {(1269.6923 / 1422.2 - 1) * 100:+.2f}%")
print(f"  50 vs 200 DMA gap {1290.59 - 1330.88:.2f}")
for e in [1318.60]:
    s_ = e * 0.92
    print(f"  at EMA20 {e}: 8% stop floor {s_:.2f}; R:R to 1467.5 with that stop {rr(e, s_, 1467.5):.3f}; stop needed for RR2 to 1467.5 {(3 * e - 1467.5) / 2:.2f}")
print('TANLA')
print(f"  3M RS {-9.92 + 6.765:.2f}; % below 52wH {(1 - 557.15 / 656.0) * 100:.2f}; vs EMA20 {(557.15 / 532.74 - 1) * 100:.2f}%")
print('UNIONBANK')
print(f"  close vs 50DMA {(178.9 / 179.73 - 1) * 100:.2f}%; fwd {6.215} vs trailing {6.1965} {(6.215 / 6.1965 - 1) * 100:+.2f}%")
print('REDINGTON / JAMNAAUTO')
print(f"  RED vs 50DMA {(359.1 / 376.97 - 1) * 100:.2f}%; since 16-Oct {(359.1 / 383.5 - 1) * 100:.2f}%; JAMNA vs 50DMA {(123.16 / 130.56 - 1) * 100:.2f}% since 16-Oct {(123.16 / 140.85 - 1) * 100:.2f}%")

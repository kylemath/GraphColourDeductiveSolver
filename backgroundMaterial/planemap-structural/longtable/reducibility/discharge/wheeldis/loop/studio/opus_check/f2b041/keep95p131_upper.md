# f2b041: Studio upper check under the keep95p131 artifacts (Studio, 3 Nov)

**Code.** Our spec-only checker: out/job31/st21_check_f2b.py + bin/sep3r_f2bS.

**Inputs.**
- keep95p131 artifacts (620487ae): kill tables, V7 / V8 masks, rules_studio_keep95p131.json (f2439106) and the keep95p131
  receiver args.
- CKEEP = keep95p131_C.txt.
- Patterns: D 18,159 / C 608 / RPAT 158.

**Setup.** Own SEPTAGs and workdir, keep95p131_upper/run/. Flags as 80287bd3: L3Q, L3Q8, HAT5, V6=0, FB=0, XO=0, rpatN3, DMAXP=17.

## Results
**A. sol_c_repaired (e0ad3fcc) at its own t = 0.041565 (8313/200000): FEASIBLE.** No TCHECK override was needed.
- senderR2: 20,676 rows, 0 violated, min slack 2.07e-7.
- cons2: five 994 and nofive 430 words, 0 violated.
- mrowL V7 and V8: 0 violated.
- bounds: 0 negative values; max x 0.178.
- Receivers, all 0 exact violators:

| d | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| exact violators | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| time | 415 s | 1597 s | 1835 s | 866 s | 404 s | 167 s | 68 s | 24 s | 9 s | 3 s | 1 s |

- DP 18..30: clean, max margin −0.636. Karp λ = 0.633625577, covered for d ≥ 16.263.

**B. delta015 XO=0 (da369b51, 9629700a) at its own t = float(17/409): FEASIBLE in float at EPS 1e-9, but not certified exactly at
17/409.** The pattern is the same as in f2b041e (exact17_409.md).
- **Senders:** 0 violated. Float min slack is 1.33e-15. In exact rationals at 17/409 the min slack is 37301/29471555961512525824
  ≈ 1.27e-15, with 0 violated.
- **cons2, mrowL V7 / V8, bounds:** clean.
- **Receivers:** every d = 7..17 has 0 float violators at EPS 1e-9. The exact-rational re-check (SEPEPS −1e-9, then exact against
  d − 6 + 17/409) gives:

| d | rows within 1e-9 | exact violators | max exact excess |
|---|---|---|---|
| 7 | 80,390 | 67,098 | 2.49e-13 |
| 8 | 21,256 | 9,604 | 1.28e-12 |
| 9 | 3,591 | 2,637 | 7.6e-13 |
| 10 | 20 | 20 | 3.7e-15 |
| 11..17 | 0 | 0 | – |

- DP 18..30: clean. Karp λ = 0.633625577.
- **Exactly certified: t ≤ 17/409 + 1.28e-12.**

**Controls under keep95 (f44b385c), d = 7: both INFEASIBLE, as required.**
- A under keep95: 5,000+ exact violators (CAP); the heaviest exact load is 1.22836 against the threshold 1.041565.
- B under keep95: 5,000+ exact violators (CAP).

These counts are under Studio's keep95 rules (rules_studio_keep95.json). Opus reports 40 rows for its keep95 run, which presumably
uses different keep95 rules or a different row set. Only the INFEASIBLE verdict is compared here.

## Reading
Under keep95p131 (all D + 531 Lean C + core95 + 131, forbidden set 12,273), Studio's spec-only check confirms Opus's engine:
**sol_c_repaired is FEASIBLE at 0.041565.** The C entries the upper needs are therefore within keep95p131:
- the 531 Lean-backed entries;
- core95 (Lean status as in Opus's list);
- the 131 = 118 RSST C2cons (C on both Studio engines, rsst118_C.md part 1, 2c275fc1) + 13 k3x C.
Lean hC for the 118 and the 13 is the remaining step.

# f2b041 job 2: keep95+131 artifacts (keep = all D + 531 Lean C + core95 + the 131-name cover), for Opus's LP re-solve

Studio, 3 Nov. The layout is that of keep95 (f44b385c). Everything is under keep95p131/. No LP was run here.

## Keep set
- **keep95p131_C.txt:** 757 C names, i.e. keep95's 626 plus the 131 greedy-cover names of keep95/dropnames_cover.txt (118 RSST
  C2cons and 13 k3x C).
- **Table forbidden set: 12,273** (keep95 had 12,142; the full Tier A set has 13,199).
  - RSST: D2 249 + C2cons 128 (the 10 Lean-backed plus the 118).
  - k3x A100: D 3,096 + C 590 (k3x_C_A100_keep95p131.cfast).
  - nl51: 8,200. k3p: D 9 + C 1. The k3p C entry, q7u_.556676_.5...6._::::::5, is one of the 13.
- **Receiver C patterns: 608 distinct** (receiver_C_patterns_keep95p131.txt; keep95 had 596). Twelve of the 13 k3x cover names also
  appear in the A111 receiver args, so adding them to keep also restores them as receiver patterns.
- **Dry run:** D 18,159 / C 608 / RPAT 158.
- **C wheels:** CKEEP as before. R5 is c5 D only, R6 is c6 D plus the kept C 6-wheels, and RBIG is the D big wheels only (91).
  The C5 and big-wheel flag in keepcover_core95.md still applies.

## Artifacts (md5)
| artifact | md5 |
|---|---|
| tab/kill/kill_U7.npy | f2d89893 |
| tab/kill/kill_U8.npy = kill_U9.npy | c9e2d251 |
| tab/kill/kill6_U7.npy | c0527d29 |
| tab/kill/kill6_U8.npy = kill6_U9.npy | 618eb300 |
| tab/studio_l3qtab_±1.json (V7) | f4b86569 (= full) |
| tab/V8/studio_l3qtabV8_±1.json | **2e8e8f5e (= full Tier A)** |
| rules_studio_keep95p131.json | f2439106 |

**Derived rules per group** (rules_studio_keep95p131.json):
| d7_w6 | d8_w6 | d9_w6 | d7_w7 ±1 | d8_w7 ±1 |
|---|---|---|---|---|
| 2,455 | 1,756 | 481 | 1,444 each | 908 each |

- **Self-test:** 6,000 arrangements, 3,901 with a nonzero delta, 0 positive, Python vs C++ mismatches 0.
- **Tables:** M vs EX6 has 0 mismatches; monotonicity has 0 violations.
- **Run script:** keep95p131/f2bS_keep95p131_run.sh.

## Still losing justification, compared with the full Tier A set
- **All 378 items lost on keep95 are covered again.**
  - **The outside rules (b9de962e): 5,954 / 5,954 pass** on the keep95+131 forbidden set (rulecheck_keep95p131.json), 0 without
    justification.
  - **The V8 masks equal the full table** (50 letter kills per side, 0 lost).
- **§14' kill tables:** kill_U7 and kill6_U7 still **lose 270 cells each** (620 on keep95), with 0 gained. U8 / U9 lose 0. The cells
  are window kills of dropped C configurations that are outside the 131.
  - In the keep-only attribution (keepcover.md) no violator was caused by a kill-table cell, so these may not bind. Opus's LP will
    show whether they do.
- **Studio-derived rules, full → keep95+131 (rules lost):**
  | d7_w6 | d8_w6 | d9_w6 | d7_w7 ±1 | d8_w7 ±1 |
  |---|---|---|---|---|
  | 2,477 → 2,455 (22) | 1,778 → 1,756 (22) | 493 → 481 (12) | 1,473 → 1,444 (29 each) | 910 → 908 (2 each) |

  None of these are needed by any outside rule. They are extra rules that Studio's unfiltered derivation finds from the other
  dropped configurations.
- **C wheels:** unchanged from keep95. All 12 C5 and all 13 C big wheels are out under CKEEP.

## keep95/single_justifier.tsv
This file has 378 rows: 308 outside rules and 70 V8 letter kills.
- Each row gives the item, the number of justifiers, the justifying configuration names, and their source (RSST C2cons or k3x C).
- 360 rows have a single justifier and 18 have several.

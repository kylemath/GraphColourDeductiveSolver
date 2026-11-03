# f2b041 job 2, core95 variant: the keep-only artifacts (keep = all D + 531 Lean-backed C + core95) for Opus's LP re-solve

Studio, 3 Nov. Built with Studio's own code from the keep set only. No LP was run (Opus re-solves). Everything is under keep95/.

## Keep set
- **Input:** core95.txt from Opus, 7ece1ccd ext_handoff_nov3, md5 fc20b94f, 95 names. It is core89 plus 6 e7 entries from
  part00.cfast. By source: 88 from k3x_C_A111, 1 from k2a, 6 from part00.
- **keep95_C.txt** (42feb7aa): 626 C names, i.e. the 531 Lean-backed names (keep/keep_lean_C.txt, as in keepcover.md) plus the 95.
  Every D entry is kept.
- **Table forbidden set:** 12,142 configurations (the full Tier A set has 13,199).
  - RSST D2 249, plus the 10 Lean-backed RSST C2cons (RSSTC_KEEP).
  - k3x A100: D 3,096, plus C 578 of 1,311 (k3x_C_A100_keep95.cfast, 3e47ca48). 496 of the 578 are Lean-backed and 82 are core95
    names that also appear in the A100 C input. The other 13 core95 names are not in A100 C, so they are absent from the tables,
    exactly as in the full Tier A build.
  - nl51_kc 8,200 (all D), k3p D 9; k3p C 0 of 1 (k3p_C_keep95.cfast).
- **Receiver C patterns:** 596 distinct, against 2,257 in the full set (receiver_C_patterns_keep95.txt, e776fc88: 598 lines, 596
  names). Receiver args: keep95/args/args.txt (a71e25fa), made by out/job31/s52c/keep_filter.py.
  - Dry run: D 18,159 / C 596 / RPAT 158.
  - **C wheels, CKEEP (the s52c reading):** R5 = c5 D only (12), R6 = c6 D + kept C 6-wheels (31), RBIG = D big wheels only
    (91 of 104).

## Artifacts (md5)
| artifact | md5 |
|---|---|
| tab/kill/kill_U7.npy | 400b4f2e |
| tab/kill/kill_U8.npy = kill_U9.npy | c9e2d251 |
| tab/kill/kill6_U7.npy | 40097bb8 |
| tab/kill/kill6_U8.npy = kill6_U9.npy | 618eb300 |
| tab/studio_l3qtab_±1.json (V7) | f4b86569 (= full Tier A) |
| tab/V8/studio_l3qtabV8_±1.json | 8f45e75e |
| rules_studio_keep95.json (Studio-derived rules, rules JSON format) | 7366c1ba |

**Rules per group** (rules_studio_keep95.json):
| d7_w6 | d8_w6 | d9_w6 | d7_w7 +1 / −1 | d8_w7 +1 / −1 |
|---|---|---|---|---|
| 2,359 | 1,684 | 435 | 1,352 / 1,352 | 853 / 853 |

- **Self-test** of these rules on the keep95 tables: 6,000 arrangements, 3,926 with a nonzero delta, 0 positive, Python vs C++ 0
  mismatches.
- M vs EX6: 0 mismatches. Monotonicity: 0 violations.
- Run script: keep95/f2bS_keep95_run.sh, flags as 80287bd3 with CKEEP, KILLDIR and L3TAB pointing at keep95.

## What loses its justification under keep95 (compared with the full Tier A set)
- **§14' kill tables:**
  - kill_U7: 620 cells lost of 84,666 (killed in full, not in keep95); kill6_U7: 620 lost of 101,761.
  - U8 / U9: 0 lost.
  - 0 gained anywhere.
- **V7 masks:** 0 lost (200 letter kills per side in both).
- **V8 masks:** **35 lost per side** (50 letter kills per side in full, 15 in keep95).
- **Studio-derived rules, full → keep95 (rules lost):**
  | d7_w6 | d8_w6 | d9_w6 | d7_w7 +1 / −1 | d8_w7 +1 / −1 | total |
  |---|---|---|---|---|---|
  | 2,477 → 2,359 (118) | 1,778 → 1,684 (94) | 493 → 435 (58) | 1,473 → 1,352 (121 each) | 910 → 853 (57 each) | 626 |
- **Outside rules (b9de962e) with no justifying embedding on the keep95 set:**
  | d7_w6 | d8_w6 | d9_w6 | d7_w7 ±1 | d8_w7 ±1 | total |
  |---|---|---|---|---|---|
  | 40 | 30 | 0 | 82 each | 37 each | 308 of 5,954 |

  Under keep (without the core) the total was 312.
- **C wheels:** CKEEP keeps only kept C 6-wheels.
  - All 12 C5 wheels drop out of R5, even though 11 of them (all except c5_66666) are in CWheels.lean.
  - The 13 C big wheels drop out of RBIG, including c7_5666567, which is in CWheels.lean.
  - This is the s52c reading (coordinator, 21 Oct 15:53Z). If Lean-backed C5 and big wheels may be kept, this keep set is stricter
    than "all Lean" by those 12 wheels. Flagged for Opus.

## Cross-check of the keepcover violators against core95
The keep-only run (keep = all D + 531 Lean, no core) dumped every exact violator at d = 7 and d = 8. Each one was matched against
the 1,756 dropped receiver C patterns: does a dropped pattern forbid it in the full set?

| d | violators | forbidden by a dropped pattern | of which by a core95 name | only by non-core names | by no dropped receiver pattern |
|---|---|---|---|---|---|
| 7 | 46,704 | 2,821 | 2,821 | **0** | 43,883 |
| 8 | 9,233 | 64 | 64 | **0** | 9,169 |

**Every receiver-pattern attribution points into core95; 0 point outside it.** The remaining 53,052 violators are not explained
by any dropped receiver pattern. They come from the table side: kill-table cells, V8 masks, rules and C wheels. Their per-term
attribution is in keepcover.md (the full vs keep replay).

# f2b041 job 2: keep-only cover of the Tier A full2ball solution (Studio, 3 Nov)

**Result: INFEASIBLE with keep = all D + every Lean-backed C (531 names).** The solution needs C entries that are not
Lean-backed. Almost all of the gap is on the table / rule side: lost full2ball rules (d7_w7, d8_w7, d7_w6) and lost V8 mask kills,
traced to **118 RSST C2cons and 13 k3x C configurations**. Only 2,885 violators come from dropped receiver C patterns, and all of
those are core95 names. No LP was run, so the smallest feasible keep-only t was not computed (Opus re-solves; see
keepcover_core95.md for the core95 artifacts).

## Setup
- **Keep list:** keep/keep_lean_C.txt, 531 C names. The Lean sources: CCover 1c56a79e, CXInt 95ba762d, CXRing 2a4bc4cf,
  CCover2 f2acc3e7, CCover3 a6efb310, CWheels.lean, k63f aa74d7ec (111), k63o 77078449 (3). This includes the 10 RSST C entries in
  CCover. All D entries are kept.
- **Rebuilt from the keep set only** (Studio code): §14' kill tables (st16_filter.py), V7 / V8 masks (l3q_masks.py), the
  full2ball rules (f2b_rulecheck.py DERIVE; the outside rules are not used, see rulecheck.md), and the receiver C patterns
  (keep_filter.py; 501 patterns).
- **C wheels:** handled by CKEEP, the s52c reading. Only kept C 6-wheels stay; the C5 wheels and C big wheels drop.
- **Table forbidden set:** 12,060 configurations (13,199 in full). Self-test on these rules: 6,000 arrangements, 0 mismatches.
- **Upper run:** at the solution's t = 0.041565, with the flags of 80287bd3.

## Receivers
| d | exact violators | max exact load (threshold d − 6 + t) |
|---|---|---|
| 7 | 46,704 | 1.24127 (1.04157) |
| 8 | 9,233 | 2.14831 (2.04157) |
| 9 | 162 | – |
| 10..17 | 0 | – |

Senders: 0 violated. DP 18..30: clean.

## Attribution
Each d = 7 / 8 violator was replayed in both the full configuration and the keep configuration (keep/attribute.py,
attribute.log).

| d | cause of the violation (losses only) | violators |
|---|---|---|
| 7 | lost d7_w7 rule(s), side +1 only / −1 only / both | 17,052 / 17,046 / 9,729 |
| 7 | lost d7_w6 + d7_w7 rules | 56 |
| 7 | inadmissible in full through a dropped receiver C pattern (all core95) | 2,821 |
| 8 | lost V8 mask kills only (+1 / −1 / both) | 2,816 / 2,816 / 1,285 |
| 8 | V8 kills + lost d8_w7 rules | 992 |
| 8 | lost d8_w7 rules only | 1,260 |
| 8 | inadmissible in full through a dropped receiver C pattern (all core95) | 64 |

Every violator falls under one of the causes above. There are 0 from C wheels / RBIG, 0 from §14' kill-table cells, and 0 left
unexplained.

**The dropped configurations responsible** (keep95/dropnames_keep95.json, keep95/dropnames_cover.txt; out/job31/f2b_dropnames.py):
- The setup is the same frame and embeddings, restricted to the 1,057 dropped C configurations of keep95.
- 308 outside rules lose their justification on keep95, and **every one is justified by some dropped configuration**.
- 70 V8 letter kills are lost (35 per side), and **every one is justified by some dropped configuration**.
- **138 distinct configurations** justify these items: 120 RSST C2cons and 18 k3x C.
- A greedy cover takes **131** of them: 118 RSST C2cons and 13 k3x C.
- 360 of the 378 items have a single justifying configuration.
- The 13 k3x C configurations in the cover are f7_..55567_..576.6, f8_..656656_..65...5, f8_..566566_....56.5,
  f7_.5576.6_.665..., f7_..65576_...665., q7u_.556676_.5...6._::::::5, f8_..655556_..675..6, f8_..555566_...576.6,
  f8_...55865_...5656., f7_.656756_....66., f7_.586556_.55...5, f7_..56756_..6.66. and f7_...5576_...6657.

This is an upper bound on what the solution needs, because not every lost item is used by a binding row. The exact minimum
needs an LP re-solve or a per-item drop test.

**Gate reading.** The C side of this upper is not Lean-backed. It rests on about 118 RSST C2cons entries (RSST's C reducibility;
our Lean agreesRSST covers D only) and 13 non-Lean k3x C entries, through the full2ball rules and the V8 masks, plus core95 on the
receiver side.

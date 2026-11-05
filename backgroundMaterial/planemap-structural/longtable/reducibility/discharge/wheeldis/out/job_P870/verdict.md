# job P870 (Opus): independent confirmation of the pruned 870-rule set (Studio, 5 Nov)

**Results:**
- **(1)** All 870 rules are in our keep95p131f rules.
- **(2)** sol_c_repaired is **FEASIBLE at 0.041565** with only the 870 rules.
- **(3)** 86 of the 88 single-drop controls are INFEASIBLE. **2 rules are redundant**: the d8_w7 ±1 mirror pair justified only by
  nl2306_r13. Dropping both together is also FEASIBLE, so **the 868-rule set works and nl2306_r13 can leave the cover**.
- **(4)** Our own cover has **503 configurations (381 D, 122 C)**, against Opus's 527. All 398 forced configurations agree.

## Independence statement
- **Code:** Studio's own spec-only code throughout:
  - out/job31/st21_check_f2b.py + bin/sep3r_f2bS for the upper;
  - out/job31/f2b_rulecheck.py provenance (keep95p131f/rule_provenance.tsv);
  - out/job_P870/prov_tables.py, which runs the table/mask builders st16_filter.py and l3q_masks.py unchanged up to their loops,
    with name tracking;
  - out/job_P870/cover.py.
- **Not opened:** Opus engine code and Team B material.
- **Inputs, read-only:**
  - 8f7e0fd6 ext_handoff_nov3/pruned870/. The 4 files present match MD5SUMS. fin711.log and finA97.log are listed in MD5SUMS but
    absent from the commit.
  - binding_entries.tsv from 7uelj0 s63_minconf (515233c9).

## (1) Subset
final870.rules.json (dfac0d25):
| d7_w6 | d8_w6 | d9_w6 | d7_w7 ±1 | d8_w7 ±1 |
|---|---|---|---|---|
| 143 | 103 | 27 | 183 / 166 | 128 / 120 |

Matched by content against rules_studio_keep95p131f.json (45a4c6d1): **870 / 870 present, 0 not in ours, 0 duplicates.**

## (2) Upper: sol_c_repaired (e0ad3fcc) at 0.041565, keep95p131f tables, masks and receivers, F2B = the 870 rules only
- **FEASIBLE.**
- senderR2: 20,676 rows, 0 violated, min slack 2.07e-7.
- cons2 (994 + 430), mrowL V7 / V8, bounds: clean.
- Patterns: D 18,159 / C 608 / RPAT 158.
- Receivers d = 7..17: **0 exact violators** at every d:

| d | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 | 16 | 17 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| time | 197 s | 1079 s | 1501 s | 630 s | 329 s | 138 s | 55 s | 20 s | 7 s | 3 s | 1 s |

- DP 18..30: clean. Karp λ = 0.633625577, covered for d ≥ 16.263.
- f2b self-test on these rules: 6,000 arrangements, 0 mismatches.
- Logs: run/p_d*.log.

## (3) Controls (ctrl/, run/c*.log)
- **Binding rules:** binding_entries.tsv has 90 RULE entries. **88 are in the 870.** The 2 that are not are both d7_w6 rules
  justified only by nl0294_r11:
  - ((1,{5}),(2,{5})) / ((0,7),(1,7),(2,5),(6,5)), p 5
  - ((5,{5}),(6,{5})) / ((0,5),(4,5),(5,7),(6,7)), p 5
- **Runs:** for each of the 88, I dropped that rule alone from the 870 and re-ran receivers at the rule's own degree. d7_* rules act
  only on d = 7 rows and d8_* rules only on d = 8 rows, so the other degrees are unchanged by construction. That is 66 runs at
  d = 7 and 22 at d = 8. All 88 were run; no sampling.
- **86 / 88 INFEASIBLE, as required.**
- **2 / 88 FEASIBLE**, so these rules are redundant on their own:
  - ctrl 81: d8_w7 −1, [5, [[4,[6]],[5,[5]],[6,[7]],[7,[5]]], [[4,5],[5,5],[7,5]]]. Sole justifier nl2306_r13.
  - ctrl 82: d8_w7 +1, [5, [[1,[5]],[2,[7]],[3,[5]],[4,[6]]], [[0,5],[2,5],[3,5]]]. Sole justifier nl2306_r13. This is the mirror
    image of ctrl 81.
- **Both dropped together** (868 rules; ctrl/drop81_82.json): receivers d = 8 have **0 exact violators, FEASIBLE**. d = 7 and
  d = 9..17 do not see d8_w7 rules, so they equal the 870 run.
- **So the 868-rule set also works.** nl2306_r13 justifies no other item: none of the 868 rules, no §14' kill cell and no V7 / V8
  mask kill (prov_tables.json). **It can leave the cover.**

## (4) Configuration cover (prov_tables.json, cover.py, cover.log)
**Items:**
- the 870 rules, with justifiers from keep95p131f/rule_provenance.tsv;
- every killed §14' cell of keep95p131f: kill_U7 84,396, kill_U8 73,342, kill_U9 73,342;
- every V7 mask letter kill (400) and V8 mask letter kill (100).

**Rebuild check:** the tables and masks rebuilt with name tracking are **identical to the saved keep95p131f tables**.

**Cover:**
- 683 distinct configurations justify the items.
- **398 are forced** (the sole justifier of some item). **All 398 are in Opus's cover.**
- **Greedy cover (forced first, then unweighted greedy): 503 configurations, 381 D + 122 C.** The ring-weighted greedy (ring⁴)
  gives the same set.
  - D by ring:

    | ring | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
    |---|---|---|---|---|---|---|---|---|---|
    | D configs | 1 | 2 | 5 | 13 | 34 | 70 | 111 | 107 | 38 |

  - C by source: rsst118 87; Lean531 24 + 10 (RSST, CCover); k3x13 1.

**Against Opus's 527 (405 D / 122 C):**
- 470 in common. Every one of Opus's 527 justifies some item here, so theirs is also a valid cover.
- The differences are greedy choices among multi-justifier items. C is 122 in both.
- **Theirs only (57):** f7_..55675_.....5., f8_.....555_....5775, f8_....5555_....6775, q7-_....556_....56._::::::5, rsst008,
  rsst174, and 51 nl51 configurations (nl0016_r10 … nl6353_r13, listed in cover_unweighted.json).
- **Ours only (33):** nl0020_r11, nl0079_r11, nl2920_r13, nl3097_r12, nl3098_r12, nl3109_r12, nl3143_r13, nl3177_r13, nl5681_r13,
  nl6159_r14, rsst009, rsst013, rsst050, rsst081, rsst083, rsst085, rsst098, rsst108, rsst112, rsst120, rsst129, rsst175, rsst208,
  rsst272, rsst279, rsst359, rsst382, rsst415, rsst491, rsst494, rsst529, rsst536, rsst547.
- With the 868 rules, nl2306_r13 drops out. It is in Opus's cover; ours did not pick it.

# RSST-RULE2: can rules of our own replace 2.126 and 128.1324802?

W6r, 10 Nov 2026, [P]. The spec text is RSSTFP_SPEC.md §16 (grammar, parts, method, tables, findings), written for a spec-only second engine.

## Answer

- **128.1324802: yes.** Add one narrow part, N2, to the 71 parts and keep 2.126 as a kill. With the 582 proved configurations, 2.126 and the RSST-SUB/SUB2 substitutes plus 1 new one, the fixed point has **0 survivors at every degree** (table below). 128.1324802 then needs no ring-merge Lean proof.
- **2.126: no**, not with rules of this family.
  - (a) Any rule that pays into a 9+ vertex within distance 2 fails on 148 leaves, whatever its form. That includes W6b's T1/T1b and the pay-through.
  - (b) Paying into the far 7/8 link neighbours instead closes d6, but leaves unkilled positive 7-vertices, and every one contains 2.126.

## Why 9+-target rules cannot work (the key finding)

- A leaf of the full-world search is dominance-reduced: a variable's 9 stands for every letter whose truth pattern over the word's fits equals 9's (RSSTFP_SPEC §13 A.3.2).
- For kills, reading that 9 as a non-host is sound, since kills are monotone. That is the reading RSST-SUB2 and RULE1 used.
- A rule that needs a 9+ target, however, fires only in the refinements where the vertex really is 9+.
- In all 154 leaves without a 9+ link vertex next to the occurrence (148 for 2.126, 6 for 128.1324802), I searched every refinement with all 2-ball variables at 5..8, using a DFS with kill pruning. **Every one of the 154 leaves has such a refinement that is still positive** (lo = hi = 2 or 1) and that **nothing kills**:
  - no proved configuration;
  - none of the 2026 set's 8,200 configurations (nl51_kc.txt, b9bc6e8b);
  - none of the 284 C/D windows W6b screened in rounds 11–13.
- Each witness contains only none configurations: 2.126 (7 also contain 7322.1040) or 128.1324802. They are re-checked on pubrules + rsst_rows in `results/witnesses154.tsv`.
- Such a state has **no 9+ vertex within distance 2 of u**, so no rule paying into a 9+ there can discharge it.
- Example: d6, link 565667, apexes 777778, privates p1.1 = 5, p3.1 = 7, p4.1 = 7, p5.1 = p5.2 = 5.

## Results per rule set (full tables: `results/summary_rule2.md`, RSSTFP_SPEC §16.4)

| rules (added to the 71 parts) | senders d6/d7 | receivers d7/d8 | receivers d >= 9 | verdict |
|---|---|---|---|---|
| W6b T1, T1b, T2 (target 9+) | 154 leaves open, see above | – | K582 max d9..12 = 14/12/8/4 (was 7/3/<=0/<=0); d9: 327 of a 3,000 sample survive the pool | fails |
| T1/T1b target >= 7, T2 >= 8 | d6: 0 survivors (1,282 leaves) | d7: 58 of 4,000 sampled survive (1,540,391 leaves), all contain 2.126 | as above | fails |
| narrow N1 + N2 (leaf link words) | d6: 0 survivors (2,316) | d7: 651 of 20,000 sampled survive (290,715), all contain 2.126 | – | fails |
| **N2 only, 2.126 kept as a kill** | d6: 0 leaves; d7: 60,349 leaves, all killed | d8: 44,470 leaves, all killed | d9 12,040 and d10 136 leaves, all killed; d11..17 none; tail unchanged | **0 survivors** |

- **N2** (§16.2): hub of degree 7, link exactly a leaf word with the 128.1324802 occurrence `=6 =5[=5] g2 =6 =6[=5] g5 =5`. The gap pair (g2, g5) is one of (9,7), (9,8), (9,9), (8,8), with exact letters (9 = 9+). It sends 1 unit to g2, and mirrors are added: 8 unit parts in all.
- **Every leaf was checked, with no sampling.** The SUB/SUB2 set (184 names, `results/subsub2_set.txt`) was tried first. 158 substitutes are used, and all lie in that set **except nl2208_r13** (2026 set, D; needed for 1 d8 leaf). It joins the Lean D queue.
- Windows used: fw_f7c75a21e2 (C), fix_63c8a193fe (P20) and fw_980b7e87e4 (D), all in SUB2's validated set.
- **Re-checks:**
  - pubrules + rsst_rows on 160 N2-run leaves (hi, lo, in-engine kills, none set): 0 disagreements;
  - the 426 leaves: charges and contained configurations equal W6b's on all 426.
- **Tail:** N2 leaves the c+ table unchanged (max mean 6), so the bound is <= 0 for d >= 15. d = 15..17 were also searched exactly.

## Step 3: largest final charge where the new rules fire (receivers)

| rules | kills | d9 | d10 | d11 |
|---|---|---|---|---|
| N2 | none | 14 | 10 | 6 |
| N2 | 582 + 2.126 | 1 | <= 0 | <= 0 |
| T1/T1b/T2 | none | 24 | 20 | 16 |
| T1/T1b/T2 | 582 | 14 | 12 | 8 |

With N2, all d9 states where the new part fires and the charge is positive are killed by substitutes.

## Lean B4 constraints

- **N2 meets all three:** its condition reads only the hub's link letters and two hats, inside the hub's 2-ball; its amount is 1 whole unit; it transfers between adjacent vertices. T1/T1b/T2 and N1 meet them too.
- **The pay-through is not developed further,** because of the finding above: no 9+ target exists in those states, whatever the form, target order or tie-break.
- **Readability in the two-step form:**
  - 2.126: the whole occurrence is in w_j's 1-ball for w_j = b, a or c.
  - 128.1324802: w_j's 2-ball holds the whole image only when w_j is the gap g2. From g5, the 5-hat on (spoke 0, spoke 1) is at distance 3. From the image spokes at positions 0 and 1, the hat on (spoke 3, spoke 4) is at distance 3.

## Limits and caveats

- As in §7, the model is the 2-ball. Kills come only from configurations among the 2-ball's hosts. A configuration reaching ring 3 could kill the 148 + 6 witnesses; RULE1 says 329 leaves are exhausted at ring <= 16 inside the 2-ball.
- Only the used C windows are certified admissible (SUB2's checks). The rest of the 284-window pool was used only to make the negative results stronger.
- The failing variants were checked on samples, which is enough to show survivors exist. Their d8 and d10/d11 runs were stopped once d7 or d9 already failed. The broad-variant d9 export was cut at 280 s and holds at least 987,768 states.
- I did not test rules that pay into vertices at distance >= 3, or rules that depend on the sender's computed charge.

## Files

- `code/`:
  - analysis: r2_leaves.py (the 426 leaves), r2_refine.py and r2_refine_all.py (refinements), r2_kill.py (582 + kc matcher);
  - parts and tables: r2_parts.py (N1/N2), r2_fwexport.py and r2_d9export.py (tables with the new parts);
  - engines: fw_bb_r2.cpp and d9bb_r2.cpp (export cap; d up to 25; CMX read from the table; mode maxT);
  - checks and summary: r2_scheck.py (substitute check), r2_recheck.py, r2_summary.py;
  - run scripts: run_*.sh.
- Tables: `fwtables/` (link variant), `fwtables_n/` (N1 + N2), `fwtables_n2/` and `d9tables_n2/` (N2), `d9tables/` (T1/T1b/T2), `d9tables_n/`, and `k583/configs.txt` (2.126 counted as a kill).
- `results/`:
  - leaves426.json, refine154.json, refine_all_pool.json, witnesses154.tsv;
  - the run JSONs: max* / maxT* / enum*, with the large exports stripped to 400 states; the N2 exports are gzipped in full;
  - scheck_*.json, recheck_n2.json, summary_rule2.md;
  - pool_kc.txt (nl51 + w6b_windows_kc.txt) and subsub2_set.txt.
- `logs/`.

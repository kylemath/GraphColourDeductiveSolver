# s71 ruleset: configurations that justify all keep95p131f table entries and rules (4 Nov 2026)

[P] single engine analysis (one Python derivation chain, recorded provenance only). This is a combinatorial set cover over recorded justifier sets, NOT a proof that the proof stack needs no other configuration and NOT a proof of minimality of the stack. Pattern channel (D/C/RPAT sets, rpatN) is excluded. Read-only on existing files; Studio files read via git show origin/main (no merge).

## Inputs
- Kill-table boxes and l3q boxes: s63_minconf/prov.pkl (KTREC U7 241 boxes, U9 79 boxes with U8 = U9; L3REC V7/V8 x 2 sides, 58 boxes of which 52 are a2-kill boxes, as in hs.py). Justifier sets restricted to the keep95p131f candidate set (12,306 keep configs by is_keep from s63 validate.py; the 5 leaked q7-_ names are not in it). 16 KT boxes (10 in U7, 6 in U9) have no justifier inside the keep set (they belong to the full Tier A tables only), so they are not keep-table boxes and are not covered; 304 KT + 52 l3q boxes remain.
- Rules: origin/main studio/opus_check/f2b041/keep95p131/rule_provenance.tsv (9,396 rules, key = group, side, JSON of [p, w_req, s_req]). Matched against s64_keep95p131f/tab/rules_studio_keep95p131f.json (md5 45a4c6d1, 9,326 rules): all 9,326 file rules are in the tsv, the 70 dropped tsv rows are exactly the 70 justified only by the 5 leaked q7-_ names. (Studio also has a keep95p131f/rule_provenance.tsv with 9,326 rows; not needed.) All justifier names are in the keep set (0 outside). The kill6/l3q tables of s64_keep95p131f are md5-identical to tab_keep95p131, so no table box needs the leaked 5.
- Items to cover: 9,698 = 304 KT + 52 l3q + 9,326 rules. Every item has at least one justifier (so the cover exists).

## Result
Cover size **3,282 configs** out of 12,306 (26.7%), of which 2,652 are already in E0_S (2,676) and 630 are not.
- **D configs (Lean hD needed): 3,084**; **C configs (Lean hC needed): 198**.
- Greedy (max coverage, tie-break E0_S, then redundancy pass) gives 3,282. An exact ILP (HiGHS via scipy, existing install) on the residual after forced configs proved 3,282 optimal for this covering model (status Optimal, obj 283.98 = 284 on 1,506 residual items, 286 distinct rows, 631 columns, secondary objective: prefer E0_S). So 3,282 is the optimum of THIS cover problem, not of the proof stack.
- Forced configs: **7,878 of the 9,326 rules (84.5%) have exactly one justifier**; also 230/304 KT boxes and 40/52 l3q boxes have exactly one. These force **2,998 distinct configs** (2,804 D, 194 C; C: RSST C 128, k3x C 65, k3p C 1). Choice exists only for the remaining 284 configs; every other item (1,506 residual items) is covered by those choices.
- Tables alone (kill + l3q, no rules): greedy cover 115 configs (91 D, 24 C), forced-heavy start; the rules are what make the cover large (3,282).
- The cover loses 24 E0_S D configs and adds 617 non-E0 D (net D 2,491 -> 3,084), and adds 13 k3x C; E0_S C configs are all kept (RSST C 128, k3x C 56, k3p C 1).

### Breakdown
**cover**: 3282 configs (D 3084, C 198; in E0_S 2652; not in E0_S 630)

| source | n | D/C |
|---|---|---|
| nl51 | 2949 | D (hD) |
| RSST D | 73 | D (hD) |
| RSST C | 128 | C (hC) |
| k3x D | 60 | D (hD) |
| k3x C | 69 | C (hC) |
| k3p D | 2 | D (hD) |
| k3p C | 1 | C (hC) |

| ring | n | D | C |
|---|---|---|---|
| -1 | 3 | 2 | 1 |
| 7 | 76 | 15 | 61 |
| 8 | 52 | 44 | 8 |
| 9 | 7 | 7 | 0 |
| 10 | 22 | 22 | 0 |
| 11 | 91 | 87 | 4 |
| 12 | 353 | 335 | 18 |
| 13 | 943 | 882 | 61 |
| 14 | 1152 | 1107 | 45 |
| 15 | 473 | 473 | 0 |
| 16 | 102 | 102 | 0 |
| 17 | 8 | 8 | 0 |

Source of ring: nl51 name suffix _rN, RSST from k44/rsst.txt, k3x/k3p from the digits after the letter prefix (f11_ -> 11, assumption: prefix number = ring size). Three k3p names (q7-_ x2 D, q7u_ C) have no parsed ring (-1).

By source and D/C: nl51 2,949 D; RSST D 73 D; RSST C 128 C; k3x D 60 D; k3x C 69 C; k3p D 2 D; k3p C 1 C. By ring: rings 14 (1,152) and 13 (943) dominate; D at ring >= 14: 1,690, at ring >= 15: 583.

## Comparison with the swarm W11 count
- W11 (REPORT.md, needed_D.tsv): 2,478 table-side D (E0_S), 238 pattern-side, 278 rpatN-only, 2,978 distinct needed; worst case 11,394 (all keep-set D plus patterns) with ~8,400 unknown mass because 3,163 rules were unattributed.
- With Studio's full rule provenance the rules need **3,084 D configs** (table + rule side, key-level via W11 aliases; 2,426 of them are in W11 table-side keys, 649 are not in needed_D.tsv at all, the rest overlap W11 pattern/rpatN keys). Table-side D grows from 2,478 by about 606 net (+617 / -24 with alias dedupe noise). Union with W11's pattern (238) and rpatN (278) D keys: **3,578** distinct D keys.
- Worst case drops from 11,394 to 3,578 D configs: -7,816 (-69%). The ~8,400 unknown mass is resolved: only ~600 extra D configs beyond W11's 2,978 are needed (3,578 vs 2,978 upper end), not 8,400. Even with no choice optimisation, the D configs that justify any rule are 3,429 (all of them), still far below the 11,578 keep-set D.
- Hc side: 198 C configs (RSST C 128, k3x C 69, k3p C 1), of which 194 are forced.
- Caveat: dedupe. W11 merged 240 RSST/nl51 same-graph pairs (WL hash); my 3,084 is name-level with W11 aliases applied only where they appear in needed_D.tsv, so the true distinct-graph D count may be slightly lower (73 RSST D are in the cover). Estimated cpu cost not recomputed; with W11's ms/class and ring mix (583 D at ring >= 15, 1,107 at ring 14), the 617 extra D configs are mostly ring 13-14.

## Files
- ruleset_configs.tsv: the cover (3,282 rows: name, source, hD/hC, ring, in E0_S, forced flag, forced item kinds). Chosen set = ILP solution (equal in size to the greedy one).
- scripts/cover.py, report.py, final.py: reproduce (python3 -I scripts/cover.py SP OUT; report.py; final.py), SP holds prov131.tsv, keepC.txt (keep95p131_C.txt), rsst.txt from origin/main.
- items.pkl, cover.pkl, ilp.pkl: intermediate data.

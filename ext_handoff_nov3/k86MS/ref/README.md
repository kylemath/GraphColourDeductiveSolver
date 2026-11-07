# k86MS / k86ML: proof-stack family + all 6 K-3 kills ("W13+K3b"; Opus, 7 Nov 03:52Z)

args_A97_F_W13K3b.txt (d9ff1fe6) = args_A97_F_W13K3.txt (58b48b54) + pat=pat_K3b_D.out (a0b171e2) + cpat=pat_K3b_C.cfast (ff6a66bd):
  D: f8_.56.5656_56...55., f9_...575655_...5..65. (pat_K3_D.out e72617ed); f8_.56656.._..566..., f8_.56.5556_56....5., f8_.56.5756_.5..555.
  C: f9_655...566_66......5 X={I5-I6} (not held out by exname; engine C count 686 -> 687)
Second engine on the reducibility and occurrence: Studio K3CHK (main a6c989e5) and K3CHK2 (main cfcd6497). Lean: hD/hC pending (admissibleX/foldSafeX proved for the C).
All 6 kc windows are graph-isomorphic to the engine's pattern graph (s_i ~ w_i, w_{i+1}; s_{i-1} ~ s_i at a 5).
Rest of the family: f2b7 c67fa1d1 [E2] + rpatN 8b90a842 [E2] + cg_keys_r13.txt (151 keys) + c6le.

## Replays (matching, second engine)
- sol_c_repaired: 364 (no K-3) -> 183 (2 kills) -> 163 (6 kills). The 4 new kills remove every row of d9 555665666 (8), 556665666 (4), d8 56757568 (8); nothing else changed.
- sol_q53A97q: 181 -> 36 -> 14. The 4 new kills remove every row of d8 56656758 (10), 55568568 (10), 55568567 (2); nothing else changed.

## New upper on this family
sol_crep_qM.json (91d12215) = sol_c_repaired with t raised 0.041565 -> 0.075004 (max excess 0.033433584, d7 5569757):
**UPPER-R2 FEASIBLE at t = 0.075004 [P]** (upper_M_crep_qM.log). Mac check asked. An upper, so it holds for any bigger kill set.
k86MS (in-out ladder) starts from it; k86ML (lext lower) on the same family; both from 03:51Z (k86KS/KL stopped before separating).

## What still binds (BINDING.md)
| d | link class | rows | max excess | e.g. link / apex |
|---|---|---|---|---|
crep (t = 0.041565):
| 7 | 5569757 | 130 | 0.0334 | 9757556 / 8667569 |
| 7 | 5768578 | 4 | 0.0273 | 8758675 / 5655555 |
| 7 | 5568757 | 6 | 0.0246 | 8757556 / 5667567 |
| 7 | 5658678 | 4 | 0.0238 | 8768565 / 5555755 |
| 7 | 5758578 | 9 | 0.0234 | 8578575 / 5555566 |
| 9 | 555657658 | 2 | 0.0219 | 856756555 / 556576578 |
| 7 | 5577658 | 4 | 0.0136 | 8567755 / 5556669 |
| 7 | 5677657 | 4 | 0.0065 | 7765756 / 7657755 |

q53A97q (t = 0.098789):
| 9 | 565675676 | 4 | 0.0413 | 765765656 / 555566555 |
| 7 | 5658568 | 6 | 0.0160 | 8658565 / 9566765 |
| 7 | 5658569 | 4 | 0.0047 | 9658565 / 8566765 |

crep fallback ladder (t = 0.041565 + next max excess): kill d7 5569757 -> 0.0689; + 5768578 -> 0.0662; + 5568757 -> 0.0654; + 5658678 -> 0.0650; + 5758578 -> 0.0635; + d9 555657658 -> 0.0552; + 5577658 -> 0.0481; + 5677657 -> 0.0416 (crep at its own t).

# k86KS / k86KL: proof-stack family + the two K-3 D kills (Opus, 7 Nov 03:36Z)

Family "W13+K3": args_A97_F_W13K3.txt (58b48b54) = args_A97_F_W13.txt (5faa1ad6) + pat=pat_K3_D.out (e72617ed):
  f8_.56.5656_56...55.  (kc b8_u.56.5656_56...55., ring 13, m 11)
  f9_...575655_...5..65. (kc b9_u...575655_...5..65., ring 13, m 10)
Reducibility: swarm K-3 kc D + dfast D + dfast18 D; Studio K3CHK (main a6c989e5) kc + dfast18 D, rotation-preserving occurrence 134/134 and 10/10. Lean hD pending.
Engine convention checked: f-pattern slot s_i is the apex of edge w_i w_{i+1} (pcheck.py rpat neighbour list), which matches the kc adjacency of both windows.
Rest of the family: f2b7 c67fa1d1 [E2] + rpatN 8b90a842 [E2] + cg_keys_r13.txt (151 keys, fe8a97a7) + c6le.

## Replays (second engine on the K-3 matching)
- sol_q53A97q: 181 -> 36 violated rows. Gone: every row of d=8 56568567 (56), 56568568 (61), 56568569 (28). Left: 56656758 0.0499, 565675676 0.0413, 55568568 0.0376, 5658568 0.016, 55568567 0.014, 5658569 0.005.
- sol_c_repaired: 364 -> 183. Gone: every row of 56568567 (150), 56568568 (11), 556575657 (16), 556575658 (4). Left: d9 555665666 0.0747, 556665666 0.0697, d8 56757568 0.0442, d7 5569757 (130 rows) 0.0334, 5768578, 5568757, 5658678, 5758578, 555657658, 5577658, 5677657.
- No other class changed. viol_K_*.txt = full lists (d load excess link sv); viol_classes.py groups them.

## New upper on this family
sol_crep_qK.json (0f03f805) = sol_c_repaired (Opus format, q7/q7m set) with t raised 0.041565 -> 0.116271 (max excess 0.074701335, d9 555665666):
**UPPER-R2 FEASIBLE at t = 0.116271 [P]** (upper_K_crep_qK.log; d=7..17 exhaustive + Karp tail). Needs the Mac check with the K3 pat file + RPATN=8b90a842 for [E2].
This beats 0.128958 (sol_q66_q) but only on W13+K3; it is an upper, so it also holds for any bigger kill set.
k86KS (in-out ladder) starts from it; k86KL (lext lower) runs on the same family. Both from 03:35Z.

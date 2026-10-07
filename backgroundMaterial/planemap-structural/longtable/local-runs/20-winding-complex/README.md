# 20-winding-complex [exploratory]

Extends the winding lambda of `SolvingFrameworkPlan/docs/working/NightEulerHole.md` (Theorem W) to every Kempe swap and tests closedness.
Files: `winding.py` (analysis, stdlib + `../common/kempe_py.py`), `summarize.py`, `out-N.jsonl` (one record per (graph, degree-5 hole, class), orders 12,14,16,17,18,19), `summary.txt`. Runtime about 15 s, one core.

## Conventions (exact)
- State = proper 4-colouring of T - hole up to renaming (colours 0..3). Link x_0..x_4 = `rot[hole]` order. Edge e_k = x_k x_{k+1}. Tait colour of e_k = XOR of the two colour labels (= which pair-partition of the 4 colours).
- Tokens = the two link edges whose Tait colour occurs once (multiplicities (3,1,1) asserted on every state). sigma(s) = sum of the two token positions mod 5. Filled <=> tokens adjacent (asserted equal to "link uses <= 3 colours").
- pi implemented exactly from the table of section 3 (R+3 / phi_B^-1 / phi_A / tau with the stated components). Asserted: pi is a permutation of every class; lambda along pi equals +1,-1,-1,-3 per row (`lambda_table_mismatch` = 0); sum of pi-cycle windings = U - 3F with every cycle sum = 0 mod 5 (`thmW_ok`). All hold in all 581 classes.
- Increment of ANY swap s->t (link-preserving included) depends only on D = sigma(t) - sigma(s) mod 5:
  - **Convention A (the note's lift, extended oddly):** w = 0,+1,-1,-3,+3 for D = 0,1,4,2,3. Reproduces pi exactly; antisymmetric by construction. Pattern-preserving swaps have D = 0 (no swap changed the token set without changing sigma: checked at order 14).
  - **Convention C (centred lift):** w = 0,+1,+2,-2,-1 for D = 0,1,2,3,4. Differs from A only on residue +-2 steps (the tau step, +2 instead of -3). Per pi-cycle w_C = w_A + (number of tau steps).
- Swap graph: vertices = states of a class, edge = single Kempe swap (pair, component), simple graph on targets (renaming-only swaps dropped).
- Commuting square: swaps (p1q1,K1), (p2q2,K2) from s with K1, K2 disjoint, K2 still a full component after K1 and vice versa, distinct s,t1,t2,u. Its curvature = w(s,t1)+w(t1,u)-w(s,t2)-w(t2,u). Triangles and 4-cycles: all simple ones of the target graph.
- Exactness: BFS spanning tree potential; count non-tree edges with non-zero holonomy.

## Results (see summary.txt)
- (a) antisymmetry: 0 failures (A and C), trivially since the increment is an odd function of D.
- (b) A: 31,156 of 377,604 commuting squares fail, always by +-5, all of "share one colour" type, all with a filled vertex (a residue +-2 step). C: 0 failures.
- (c) triangles: 0 failures for A and C (38,304 total). 4-cycles: A fails on 7,961; C 0.
- (d) A is never exact (every class). C is exact in 161 of 581 classes, inconsistent in 420. Shortest non-zero-holonomy cycle for C: length >= 5 (sampled sources).
- Holonomy of C does not have a definite sign (orientation reversal flips it; on pi-cycles w_C takes values -1,0,+1) and is not carried by pi-cycles alone (86 classes have all pi-cycle w_C = 0 yet are inconsistent).

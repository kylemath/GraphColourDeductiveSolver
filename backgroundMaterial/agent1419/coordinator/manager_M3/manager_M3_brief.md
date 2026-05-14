# Manager M3 Brief — Proof Hunters (Revised Post-Checkpoint)

## Agent: 1419-M3
## Role: Proof strategy development targeting Revised Conjecture 5.5'

## Context Update from Checkpoint 1

The original Conjecture 5.5 (BFS-optimal avoidance) is **FALSE** at n=9. The target is now:

**Revised Conjecture 5.5' (Safe Path Existence):** For every planar triangulation G, vertex v with deg(v) ≤ 5 and c(v) = 5, and merge-prone colouring of G-v, there exists a path in R(G-v, 5) to a 4-colouring that uses only safe swaps (no unsafe (a,5)-swaps adjacent to v).

**Key data from M1:**
- Alternative swaps are ALWAYS "safe (a,5)-swap not adjacent to v"
- Counterexamples at n=9 are salvageable at distance opt+1
- Merge-prone chains are small (≤ 3 vertices)
- Both counterexample graphs have degree sequence [3,4,4,4,4,5,5,6,7]

## Subtask S1: Case Analysis for Safe Path Existence

**Approach:** For each of the 14 colour types at degree-4/5 vertices, prove that a safe alternative swap ALWAYS EXISTS.

**Strategy:** Given a merge-prone (a,5)-chain adjacent to v:
1. Show there exists another (a,5)-chain NOT adjacent to v (safe alternative)
2. Or show a {1,2,3,4}-swap achieves the same colour reduction
3. Use the planarity constraint + small chain size to guarantee alternatives

**Start with degree 4** (8 colour types, stronger Merge Geometry: link is C_4, only opposite pairs can be in different chains).

## Subtask S2: Confinement Factoring + Chain Size Bound

**Approach C (Confinement):** Use Theorem B (Confinement — Kempe chains in planar graphs cannot cross) to show that unsafe (a,5)-chains can be "routed around" via safe alternatives.

**Approach D (Chain Size Bound):** Prove merge-prone chains are bounded in size. Data shows:
- Mean chain size: 1.27 vertices
- Max observed: 3 vertices
- 72% are single vertices

If merge-prone chains are bounded (say ≤ f(n)), the number of colourings affected is bounded, and alternative paths exist by a counting argument on R(G-v, 5).

## Subtask S3: Degree-5 Specific Analysis

The degree-5 case is harder: merge rate 22.8% (vs 10.6% at degree 4), link is C_5 (vs C_4), counterexamples are both at degree 5. Both counterexample vertices are degree 5.

**Question:** Does the degree-4 proof generalize to degree-5, or does degree-5 need its own argument?

**Focus on:** Why the C_5 link allows counterexamples that C_4 doesn't. In C_5, non-adjacent pairs are at distance 2 (not the opposite diagonal of C_4), giving more room for bottleneck topology.

## Output Paths:
- S1: `backgroundMaterial/agent1419/coordinator/manager_M3/sub_S1/S1_report.md`
- S2: `backgroundMaterial/agent1419/coordinator/manager_M3/sub_S2/S2_report.md`
- S3: `backgroundMaterial/agent1419/coordinator/manager_M3/sub_S3/S3_report.md`
- Manager: `backgroundMaterial/agent1419/coordinator/manager_M3/manager_M3_report.md`

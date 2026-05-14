# M1-S1 Report: Extended BFS Avoidance at n=9

**Agent:** 1419-M1-S1
**Status:** COMPLETE — COUNTEREXAMPLES FOUND

## Executive Summary

BFS avoidance (first-path) **FAILS** at n=9. Out of 172,281 (a,5)-swaps examined across all 50 triangulations, **539 merges** occurred where BFS selected an unsafe chain. However, the deep investigation reveals this is a failure of BFS optimality, not of safe path existence.

## Raw Results: n=9

| Metric | Value |
|--------|-------|
| Triangulations tested | 50 |
| Total (a,5)-swaps in BFS paths | 172,281 |
| Total merges (BFS used unsafe chain) | 539 |
| Merge-prone cases | 17,562 |
| BFS used unsafe swap | 539 (3.1% of merge-prone) |
| Colourings tested | 347,448 |

### By vertex degree:

| Degree | (a,5)-swaps | Merge-prone | % merge-prone | BFS-used-unsafe |
|--------|------------|-------------|---------------|-----------------|
| 4 | 65,175 | 6,925 | 10.6% | 317 |
| 5 | 46,754 | 10,637 | 22.8% | 222 |

### Graphs with BFS merges (16 out of 50):
- T_9_0 (v=3, deg 4): 60 merges
- T_9_6 (v=4 deg 5, v=6 deg 4): 32 merges
- T_9_7 (v=4 deg 5, v=5 deg 5, v=6 deg 4): 48 merges
- T_9_8 (v=2 deg 4, v=6 deg 4): 48 merges
- T_9_25 (v=3 deg 5, v=5 deg 4): 153 merges **← TRUE COUNTEREXAMPLE**
- T_9_27 (v=1 deg 4): 12 merges
- T_9_35 (v=3 deg 5, v=6 deg 4): 38 merges **← TRUE COUNTEREXAMPLE**
- T_9_37 (v=1 deg 5): 24 merges
- T_9_41 (v=4 deg 4, v=6 deg 4): 64 merges
- T_9_43 (v=4 deg 4, v=7 deg 4): 12 merges
- T_9_44 (v=2 deg 5, v=3 deg 5, v=5 deg 5): 48 merges

## Counterexample Deep Investigation

### T_9_25 (degree sequence: [3,4,4,4,4,5,5,6,7]):
- **Counterexample vertex v=3 (deg 5):** 96 merges, 24 colourings where ALL optimal paths are unsafe
- **Salvage:** All 24 have safe paths at distance 3 (optimal is 2). ALWAYS salvageable.
- **Alternative vertices with 0 merges:** v=1(deg 4), v=4(deg 4), v=6(deg 5), v=7(deg 4), v=8(deg 3)

### T_9_35 (degree sequence: [3,4,4,4,4,5,5,6,7]):
- **Counterexample vertex v=6 (deg 4):** 32 merges, 24 colourings where ALL optimal paths are unsafe
- **Salvage:** All 24 have safe paths at distance 3 (optimal is 2). ALWAYS salvageable.
- **Alternative vertices with 0 merges:** v=1(deg 5), v=4(deg 4), v=5(deg 4), v=7(deg 4), v=8(deg 3)

## Key Finding: Safe Paths Always Exist

For EVERY counterexample case:
- A safe path of length opt_dist + 1 exists (distance 3 instead of 2)
- Alternative vertex removal (different v) avoids the problem entirely
- 0 cases where no safe path exists at any length

## Impact

1. **Conjecture 5.5 (BFS optimal avoidance) is FALSE** as stated
2. **Weaker conjecture: safe path existence at distance ≤ n-3** appears TRUE
3. **The inductive proof architecture survives** if we allow ≤ n-3 swaps or choose v carefully

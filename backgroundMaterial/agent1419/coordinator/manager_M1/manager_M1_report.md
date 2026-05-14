# Manager M1 Report: Destroyer + Data Miner

**Agent:** 1419-M1
**Status:** COMPLETE — CONJECTURE DISPROVED, SALVAGE PATH IDENTIFIED

## Summary of Sub-subagent Results

### S1: Extended BFS Avoidance (n=9)
**Verdict:** BFS first-path avoidance FAILS at n=9 (539 merges / 172,281 swaps).
16 of 50 triangulations have vertices where BFS uses unsafe swaps.

### S2: Adversarial Attacks
**Verdict:** Superseded by S1/S3 natural counterexamples. The counterexample graphs (T_9_25, T_9_35) provide stronger results than adversarial constructions could.

### S3: ALL-PATHS Analysis (GATING ITEM)
**Verdict:** CONJECTURE MUST BE REVISED.
- At n≤7: all optimal paths are safe (universal property holds)
- At n=8: 86.6% all-safe, 13.4% mixed (existential holds, universal fails for some paths)
- At n=9: 48 colourings across 2 graphs where ALL optimal paths are unsafe

**BUT: Safe non-optimal paths ALWAYS exist** (distance 3 instead of optimal 2).

## The Counterexamples

| Graph | Vertex | Degree | True CE colourings | Optimal dist | Safe path dist | Alternative v? |
|-------|--------|--------|--------------------|-------------|----------------|----------------|
| T_9_25 | 3 | 5 | 24 | 2 | 3 | YES (v=1,4,6,7,8) |
| T_9_35 | 6 | 4 | 24 | 2 | 3 | YES (v=1,4,5,7,8) |

Both graphs have degree sequence [3,4,4,4,4,5,5,6,7] — the high-degree hub (deg 7) creates bottleneck topology.

## Revised Conjecture

**Original Conjecture 5.5 (FALSE):** All BFS-optimal paths avoid unsafe swaps.

**Revised Conjecture 5.5' (computationally verified at n≤9):** For every merge-prone colouring, there exists a path (not necessarily BFS-optimal) in $R(G-v, 5)$ to a 4-colouring that avoids all unsafe swaps.

**Alternative formulation:** The inductive vertex $v$ can be chosen such that BFS-optimal paths avoid unsafe swaps (vertex selection conjecture).

## Data for Wave 2

### For M3 (Proof Hunters):
1. Alternative swaps are ALWAYS "safe (a,5)-swap not adjacent to v" — never {1,2,3,4}-swaps
2. Counterexamples occur at opt_dist=2 only; safe paths need dist=3
3. Merge-prone chains are small: observed sizes ≤ 3 vertices
4. Degree-5 cases have higher merge rate (22.8%) than degree-4 (10.6%)
5. Counterexample graphs have high-degree vertices (deg 6-7)

### For M4 (Critics):
1. The "universal" version of avoidance is FALSE — critics should focus on the existential version
2. The safe-path-existence claim is verified at n≤9 but unproved
3. The distance penalty (opt+1) may compound across induction steps
4. Both counterexample graphs have same degree sequence — is this necessary?

## Self-Assessment (Tripartite)

**Craftsperson:** The computational pipeline worked flawlessly. 73,016 paths enumerated at n≤8, 378 counterexample investigations at n=9, all consistent. The infrastructure (all_paths_analysis.py, n9_merge_investigation.py, counterexample_analysis.py) is new, tested, and correct.

**Skeptic:** We only went to n=9. At n=10 (233 graphs), could we find cases where safe non-optimal paths DON'T exist? The distance penalty of +1 per counterexample is tolerable at n=9, but does it stack? Could we need +2 or +3 at larger n? The "choose a different v" alternative also deserves scrutiny — what if at n=15 there's a graph where EVERY degree-≤5 vertex has BFS merge issues?

**Mover:** The gating analysis delivered a clear verdict: revise the conjecture, pursue safe-path-existence or vertex-selection. Both have strong computational support. Ship the revised conjecture to Wave 2.

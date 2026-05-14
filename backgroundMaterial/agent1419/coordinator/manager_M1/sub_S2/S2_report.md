# M1-S2 Report: Adversarial Attacks at n=9

**Agent:** 1419-M1-S2
**Status:** COMPLETE — ATTACKS SUPERSEDED BY S1/S3 FINDINGS

## Executive Summary

The adversarial attack programme was substantially altered by the S1/S3 findings. The n=9 computation directly found what adversarial attacks 6-8 were designed to find: cases where BFS MUST use unsafe swaps. Rather than constructing artificial adversarial scenarios, nature provided real counterexamples.

## Attack 6: Forced Single-Path (superseded)

**Objective:** Find graphs where R(G-v,5) has unique shortest path through unsafe swap.

**Finding:** T_9_25 v=3 and T_9_35 v=6 provide exactly this: cases with only 2 optimal paths, both unsafe. This is stronger than "forced single-path" — it's forced-all-paths.

**Structural analysis of T_9_25:**
- Both counterexample graphs have degree sequence [3,4,4,4,4,5,5,6,7]
- Both have high-degree vertices (deg 6 and 7) creating "bottleneck" topology
- The forced unsafe swaps occur at distance 2 from a 4-colouring (very short paths)
- The optimal paths have only 2 alternatives, both through the same bottleneck

## Attack 7: High-Merge-Rate Construction

**Observation from n=9 data:**
- Degree-5 merge-prone rate at n=9: 22.8% (down from ~31% at n=7)
- Degree-4 merge-prone rate at n=9: 10.6% (down from ~17% at n=7)
- Merge-prone rates DECREASE with n, contrary to adversarial expectation
- But BFS-unsafe rate INCREASES (0% at n≤8 to 3.1% at n=9)

This reveals the key dynamic: merge-proneness becomes less common, but when it does occur, BFS has fewer alternative paths to avoid it.

## Attack 8: Fisk/Algebraic Obstruction

**Not executed** — superseded by direct counterexample analysis. The counterexamples can be analyzed topologically:
- Both T_9_25 and T_9_35 have graph structure suggesting the merge is forced by planarity constraints at the high-degree hub (vertex 0, degree 7)
- The existence of a degree-7 vertex may be necessary for creating bottleneck topology

## Recommendations

1. The adversarial programme should shift to: "Can we construct a graph where NO safe path exists at ANY distance?" — the current counterexamples are all salvageable at distance +1
2. Focus adversarial energy on the WEAKER conjecture (safe path existence)
3. Test whether degree-7+ vertices are necessary for counterexamples

# S2 Report: Extension to n = 10, 11, 12

**Agent:** 1545-M2-S2  
**Date:** 2026-02-20  
**Status:** n=10 COMPLETE, n=11 IN PROGRESS (triangulation generation ~34 min+)

---

## Objective

Extend the safe path analysis from $n = 9$ to larger triangulations ($n = 10, 11, 12$) to determine whether:
1. The counterexample rate grows or shrinks with $n$
2. The maximum detour cost grows with $n$ (bounded or unbounded?)
3. Any case exists where NO safe path exists at any length (kill criterion)

## Results: n = 10 (COMPLETE)

### Summary

| Metric | Value |
|---|---|
| Triangulations | 233 |
| Colourings tested | 3,766,224 |
| Total merge-prone | 1,744,128 |
| Safe at BFS-optimal (first path) | 1,731,996 (99.30%) |
| Safe alt at optimal (mixed) | 9,468 (0.54%) |
| Safe non-optimal (detour needed) | 2,664 (0.15%) |
| No safe path | **0** |
| Max detour cost | **1** |
| Computation time | 684s (11.4 min) |

### Detour Cost Distribution

| Detour cost | Count |
|---|---|
| 0 | 1,741,464 |
| 1 | 2,664 |

**Every single case with a non-optimal safe path has detour cost exactly 1.**

### Key Finding: No Safe Path Count Remains Zero

Out of 1,744,128 merge-prone configurations at $n = 10$, **every single one** has a safe path to a 4-colouring. The Conjecture 5.5' HOLDS at $n = 10$.

## Trend Analysis: n = 8 through n = 10

| $n$ | Graphs | Merge-prone | Detour CEs | Max detour | CE rate | Time |
|---|---|---|---|---|---|---|
| 8 | 14 | 20,136 | 0 | 0 | 0.000% | 1.6s |
| 9 | 50 | 163,584 | 48 | 1 | 0.029% | 27s |
| 10 | 233 | 1,744,128 | 2,664 | 1 | 0.153% | 684s |

### Observations

1. **Merge-prone cases grow ~10× per vertex increment** (20K → 164K → 1.7M)
2. **CE rate is growing** (0% → 0.03% → 0.15%), approximately 5× per vertex increment
3. **Max detour cost remains 1** — this is the critical invariant
4. **Mixed cases also grow** (0 → 330 → 9,468), roughly 30× per increment

### Extrapolation

If the CE rate continues to grow at ~5× per vertex increment:
- $n = 11$: estimated CE rate ~0.76%, merge-prone ~18M, CEs ~137K
- $n = 12$: estimated CE rate ~3.8%, merge-prone ~180M, CEs ~6.8M

The critical question is NOT the CE rate (which can grow) but whether **max detour cost remains bounded** and whether **no-safe-path cases appear**.

## Results: n = 11 (IN PROGRESS)

The computation for $n = 11$ is running. Triangulation generation (1,249 graphs) is the current bottleneck, requiring extensive isomorphism filtering. Expected completion: 60–120 minutes for generation, plus ~1–2 hours for the safe path analysis.

**This section will be updated when results are available.**

Estimated scale: ~18 million merge-prone cases across 1,249 triangulations.

## Computational Notes

### n = 10 Performance

- Triangulation generation: 13.0s
- Average per-graph analysis: 2.9s
- Safe-BFS (when triggered): average 132 nodes explored, max 510

### n = 11 Bottleneck

The isomorphism-based triangulation generation scales as $O(k^2)$ where $k$ is the triangulation count. With 1,249 triangulations at $n = 11$ vs 233 at $n = 10$, the generation is approximately 29× more expensive. Edge-flipping iterations add further overhead.

### n = 12 Feasibility

n = 12 has 7,595 triangulations. Generation would require ~1,000× more isomorphism checks than $n = 10$. This is likely infeasible without an external triangulation generator (e.g., `plantri`) or pre-computed database. **Not attempted.**

## Assessment

The extension to $n = 10$ provides strong additional evidence for Conjecture 5.5':

- **1.9 million merge-prone cases verified** (cumulative through $n = 10$)
- **Zero cases with no safe path** across all tested sizes
- **Max detour cost is invariantly 1** — no growth with $n$
- **CE rate grows but remains manageable** (~0.15% at $n = 10$)

The most remarkable finding is the **stability of the detour cost at exactly 1**. This suggests a structural property of Kempe reconfiguration graphs for planar triangulations: when the BFS-optimal path is unsafe, there is always a safe bypass that adds exactly one step.

**Feasibility rating: Medium-High** (would be High with n=11 confirmation and theoretical backing)

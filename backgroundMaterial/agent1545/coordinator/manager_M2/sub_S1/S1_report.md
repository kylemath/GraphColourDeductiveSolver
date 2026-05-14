# S1 Report: Non-Optimal Safe Path Verification

**Agent:** 1545-M2-S1  
**Date:** 2026-02-20  
**Status:** COMPLETE  

---

## Objective

For every merge-prone (G, v, colouring) case at $n \leq 9$, find the **shortest safe reconfiguration path** — one that avoids all merge-prone Kempe swaps at vertex $v$ — and record the **detour cost** $d_{\text{safe}} - d_{\text{opt}}$.

A swap step is **safe** if either:
- It is a $\{1,2,3,4\}$-swap (colour 5 not involved), or
- It is an $(a,5)$-swap where $v$'s neighbors do not form $\geq 2$ distinct $(a,5)$-chains, or
- The specific chain being swapped is not incident to $v$'s neighbors.

## Method

1. Build safe-BFS: a modified BFS on $R(G{-}v, 5)$ that only follows safe edges
2. For each merge-prone case, first check if the standard BFS path is already safe (fast-path for majority of cases)
3. If not, run safe-BFS to find the shortest safe path at **any** length

Code: `compute/kempe/safe_path_search.py`

## Results

### n = 8 (14 triangulations)

| Metric | Value |
|---|---|
| Total merge-prone cases | 20,136 |
| Safe at BFS-optimal | 20,136 (100%) |
| Need safe alternative (mixed) | 0 |
| Need detour (safe non-optimal) | 0 |
| No safe path | 0 |
| Max detour cost | 0 |
| Computation time | 1.6s |

**At $n \leq 8$: every merge-prone case has a safe path at the BFS-optimal distance.** No detour is ever needed.

### n = 9 (50 triangulations)

| Metric | Value |
|---|---|
| Colourings tested | 347,448 |
| Total merge-prone cases | 163,584 |
| Safe at BFS-optimal (first path) | 163,206 (99.77%) |
| Safe alternative at optimal length | 330 (0.20%) |
| Safe but non-optimal (need detour) | 48 (0.03%) |
| No safe path | **0** |
| Max detour cost | **1** |
| Computation time | 27.1s |

### Detailed Analysis of the 48 True Counterexamples

All 48 cases share identical structure:

| Property | Value |
|---|---|
| Graph | T_9_25 |
| Vertex | 3 |
| Degree | 5 |
| $d_{\text{opt}}$ | 2 |
| $d_{\text{safe}}$ | 3 |
| Detour cost | 1 |

All 48 counterexamples occur in a **single graph** (T_9_25) at a **single vertex** (v=3, degree 5). This represents 48 distinct starting 5-colourings where every BFS-optimal path of length 2 uses an unsafe swap, but a safe path of length 3 always exists.

### Category Breakdown at n = 9

| Category | Count | Percentage | Description |
|---|---|---|---|
| Safe-optimal | 163,206 | 99.769% | First BFS path is safe |
| Mixed | 330 | 0.202% | First BFS path unsafe, safe alternative at same length |
| Detour needed | 48 | 0.029% | All optimal paths unsafe, safe path at $d+1$ |
| No safe path | 0 | 0.000% | — |

### Detour Cost Distribution at n = 9

| Detour cost $d_{\text{safe}} - d_{\text{opt}}$ | Count |
|---|---|
| 0 | 163,536 |
| 1 | 48 |

### Safe-BFS Performance

For the 378 cases requiring safe-BFS (330 mixed + 48 detour):
- Average nodes explored: 132.0
- Maximum nodes explored: 510

This is a tiny fraction of the reconfiguration graph, confirming safe paths are close to optimal paths.

## Key Findings

1. **Conjecture 5.5' HOLDS at $n \leq 9$**: every merge-prone case has a safe path to a 4-colouring
2. **Maximum detour cost is 1**: the weakest bound needed is $d_{\text{safe}} \leq d_{\text{opt}} + 1$
3. **Counterexamples are extremely localized**: all 48 occur in one graph at one vertex
4. **The phenomenon first appears at $n = 9$**: $n \leq 8$ requires zero detours
5. **Safe-BFS is efficient**: even for non-optimal cases, the safe path is found quickly (avg 132 nodes explored)

## Assessment

The safety-net strategy is robust at $n = 9$. Safe paths always exist, and the detour cost is bounded by 1. The key question — resolved here for $n \leq 9$ — is whether this bound holds at larger $n$. See S2 report for extension to $n \geq 10$.

**Feasibility rating for $n \leq 9$: HIGH**

# D2 — Penrose sign-sum and the Tait count

**Group:** D2, manager M-Duality
**Date:** 2 October 2026
**Status:** `penrose_eval` is a Tait count. The signed state sum was computed for every cached triangulation through $11$ vertices. Track 4 is a reformulation of the Four Colour Theorem.

## 1. Definitions

Let $T$ be a triangulation from `compute/data/triangulations_n4_11.json`. Its plane dual $T^*$ is the cubic graph whose vertices are the faces returned by `nx.check_planarity` (`a1720_penrose_state_sum.plane_dual_rotation`). The cyclic order at a dual vertex is the facial walk `PlanarEmbedding.traverse_face` (the face lies to the right of the walk).

Colours are $\{0,1,2\}$. For an ordered triple, $\varepsilon_{ijk}$ is the sign of the permutation $(0,1,2)\mapsto(i,j,k)$, and $\varepsilon_{ijk}=0$ if the entries are not all different. The **Penrose sign-sum** of a rotation system $\rho$ is
\[
\mathrm{Pen}_\varepsilon(G,\rho)=\sum_{\ell:E\to\{0,1,2\}}\prod_{v\in V}\varepsilon_{\ell(e_v),\ell(f_v),\ell(g_v)},
\]
with $(e_v,f_v,g_v)=\rho(v)$. The **Tait count** $\#\mathrm{Tait}(G)$ is the same sum with $|\varepsilon|$ in place of $\varepsilon$. On a cubic graph every improper labelling has a zero factor, so both sums are supported on the Tait colourings. Only the signs can separate them.

`compute/topology/penrose_eval.py` defines `penrose_eval` by `return count_tait_colourings(graph)`. That function backtracks over proper edge-3-colourings and adds $1$ for each. It never reads a rotation and never multiplies by $\varepsilon$. The absolute-value formula in `SolvingFrameworkPlan/Plan3_TQFT_SheafCohomology.md` §2.1 is the same integer: $|\varepsilon_{ijk}|\in\{0,1\}$, so
\[
\sum_{\ell}\prod_v|\varepsilon_{\ell(e_1),\ell(e_2),\ell(e_3)}|=\#\mathrm{Tait}(G)
\]
for every cubic graph, planar or not.

A cubic graph has even order, because $2|E|=3|V|$. Reversing every cyclic order, or relabelling the three colours by an odd permutation, multiplies the sign-sum by $(-1)^{|V|}=+1$. The sign is therefore unchanged by those two conventions.

## 2. Statements

**Code.** `penrose_eval(G)` equals $\#\mathrm{Tait}(G)$. It is not a signed state sum.

**Computed, required range.** For every cached triangulation $T$ on $n\le 8$ vertices, with $\rho$ the dual rotation above,
\[
\mathrm{Pen}_\varepsilon(T^*,\rho)=(-1)^n\,\#\mathrm{Tait}(T^*).
\]
Every Tait colouring has the same sign $(-1)^n$. None cancels.

**Computed, same run.** The same identity holds for every cached triangulation on $n\le 11$ vertices ($1555$ graphs; the plantri counts $1,1,2,5,14,50,233,1249$).

**Proved for stacked triangulations.** Colour vertices by the Klein group $\{0,1,2,3\}$ under XOR. Differences along edges are a Tait colouring of the dual, and on a plane graph every Tait colouring arises this way (the flow is a coboundary). For $K_4$, each of the $4!=24$ proper colourings has sign-product $+1$. Placing a new vertex in a clockwise face $(a,b,c)$ replaces that face by the clockwise faces $(a,b,v)$, $(b,c,v)$, $(c,a,v)$, and the ratio of the two products is $-1$ for every proper colouring of the four vertices. A stacked triangulation on $n$ vertices is $K_4$ with $n-4$ such insertions, so every one of its Tait colourings has sign $(-1)^n$.

**Controls.** On $K_4$, all $16$ choices of local orientation satisfy $|\mathrm{Pen}_\varepsilon|=\#\mathrm{Tait}=6$, eight with sign $+1$ and eight with sign $-1$. On $K_{3,3}$, all $64$ rotation systems have $\mathrm{Pen}_\varepsilon=0$ and $\#\mathrm{Tait}=12$ (six colourings of each sign). The Petersen graph has both integers $0$.

**Track 4.** As written in Plan 3 §2.1, $\mathrm{Pen}(G)>0$ for every bridgeless planar cubic $G$, with $\mathrm{Pen}$ the absolute-value sum. That sentence is "every bridgeless planar cubic graph has a Tait colouring". By Tait's correspondence a bridgeless cubic plane graph has a Tait colouring if and only if its faces are $4$-colourable. Track 4 is a reformulation of the Four Colour Theorem.

## 3. Evidence

`penrose_eval.main`, called as a function so the writer under `__main__` did not run. Wall clock $0.015$s.

```text
.venv/bin/python -c "import time; from compute.topology.penrose_eval import main; t=time.perf_counter(); main(); print(time.perf_counter()-t)"
```

| Graph | $V$ | Pen | Note |
|---|---|---|---|
| $K_4$ | 4 | 6 | planar |
| triangular prism | 6 | 6 | planar |
| cube $Q_3$ | 8 | 24 | planar |
| Petersen | 10 | 0 | non-planar |
| $K_{3,3}$ | 6 | 12 | non-planar |
| dodecahedron | 20 | 60 | planar |
| prism $C_{10}\times K_2$ | 20 | 1032 | planar, slowest row $0.005$s |
| Frucht | 12 | 6 | planar, flag correct |
| Pappus | 18 | 120 | flagged planar; `nx.check_planarity` is false |
| Desargues | 20 | 192 | non-planar |
| Heawood | 14 | 48 | non-planar |
| Tutte | 46 | SKIP | planar and cubic; skipped by the size guard |
| $K_4$-expanded, cube-expanded | 8, 12 | N/A | not cubic ($13$ and $19$ edges) |

The printer's line "Planar graphs tested: 13, all $\mathrm{Pen}(G)>0$" includes the Pappus graph and counts the cube twice: the graph named "Möbius-Kantor ladder $C_4\times K_2$" is `circular_ladder_graph(4)`, isomorphic to the cube. The only planarity-flag mismatch in `build_graph_library` is the Pappus graph. Running the file as `__main__` then tries to write `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1520/coordinator/manager_M4/sub_S2`, which is not on this machine.

Sign-sum census, wall clock $0.8098$s, mismatches $0$. Output `backgroundMaterial/agent1720/groups/D2_results.json`.

```text
.venv/bin/python compute/topology/a1720_penrose_state_sum.py
```

| $n$ | graphs | common sign | Tait min–max | signed min–max | time |
|---|---|---|---|---|---|
| 4 | 1 | $+1$ | 6–6 | 6–6 | 0.0003s |
| 5 | 1 | $-1$ | 6–6 | $-6$–$-6$ | 0.0033s |
| 6 | 2 | $+1$ | 6–24 | 6–24 | 0.0005s |
| 7 | 5 | $-1$ | 6–30 | $-30$–$-6$ | 0.0013s |
| 8 | 14 | $+1$ | 6–72 | 6–72 | 0.0049s |
| 9 | 50 | $-1$ | 6–126 | $-126$–$-6$ | 0.0195s |
| 10 | 233 | $+1$ | 6–264 | 6–264 | 0.1031s |
| 11 | 1249 | $-1$ | 6–510 | $-510$–$-6$ | 0.6596s |

For $n\le 5$ the same pairs were recomputed by enumerating every map $E\to\{0,1,2\}$, including the improper ones; the two methods agree. Tait counts for $n\le 9$ agree with the gated file `D1_results.json`. That file has no rows for $n=10$ or $n=11$. The run did not approach the ten-minute deadline ($540$s guard).

Web search and page fetch were unavailable in this session, so no URL was retrieved. The Tait correspondence used above is the one already cited by D1: a bridgeless cubic plane graph is $3$-edge-colourable if and only if its faces are $4$-colourable. Plan 3 §2.1 attributes the absolute-value formulation to Kauffman (1990), *Map coloring and the vector cross product*.

## 4. Result

**Killed** as an independent state sum: `penrose_eval` is the Tait count.

**Computed** on all cached triangulations with $n\le 11$: $\mathrm{Pen}_\varepsilon(T^*,\rho)=(-1)^n\,\#\mathrm{Tait}(T^*)$, with no cancellation. The required range was $n\le 8$ ($23$ graphs); $n=9,10,11$ finished in the same run.

**Proved** for stacked triangulations, by the $K_4$ enumeration and the stacking ratio $-1$.

**Literature-settled as a reformulation.** Track 4, in the absolute-value form written in Plan 3, is Tait's reformulation of the Four Colour Theorem. On the computed duals the signed sum is a nonzero multiple of the Tait count, so its non-vanishing is the same sentence.

## 5. Kill criterion

"The sign-sum differs from $\pm$ the Tait count on some plane dual in the census" — not met.

"$K_{3,3}$ has a rotation system whose sign-sum equals its Tait count" — not met; all $64$ systems cancel.

"`penrose_eval` multiplies by $\varepsilon$" — met in the negative: the function returns `count_tait_colourings`. The claim that this module evaluates an independent Penrose state sum is killed.

## 6. Not proved

The identity $\mathrm{Pen}_\varepsilon(T^*)=(-1)^n\,\#\mathrm{Tait}(T^*)$ is not proved for every triangulation. Stacked triangulations are the case the deletion argument covers. The octahedron is a triangulation of minimum degree $4$; it sits in the $n=6$ row (Tait count $24$, sign $+1$) and is not reached by stacking. Nothing here proves the Four Colour Theorem. The absolute-value sum does not use planarity, so it does not explain why the planar case is the one that survives.

## 7. Feasibility

**Low** for a proof of the Four Colour Theorem by positivity of this state sum: on every tested plane dual the sum is $\pm$ the Tait count, so positivity is the reformulation itself.

**Medium** for a proof of the sign identity on all triangulations. The stacked case is done, and the census has no exception through $11$ vertices.

## 8. Next steps

Prove the sign identity for a triangulation of minimum degree $4$, starting from the octahedron already in the $n=6$ row. Do not cite `penrose_eval` as a tensor evaluation. The Pappus flag in `build_graph_library` is the one false planarity bit; that graph is not evidence about the planar case.

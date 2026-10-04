# D2b — Penrose state sum versus the Tait count

**Group:** D2b, manager M-Duality
**Date:** 2 October 2026
**Status:** finite check. `penrose_eval()` is a Tait count. Track 4 is a reformulation of the Four Colour Theorem.

## 1. Definitions

`compute/topology/penrose_eval.py` defines `penrose_eval` by `return count_tait_colourings(graph)`. A Tait colouring is a map from the edges to $\{1,2,3\}$ such that all three labels appear at every vertex. The function adds $1$ for each such map. It does not evaluate a Levi-Civita symbol.

`compute/topology/a1720_penrose_state_sum.py` defines a different integer. Colours are $\{0,1,2\}$. If $(e,f,g)$ is the cyclic order at a vertex, $\varepsilon(i,j,k)$ is the sign of $(0,1,2)\mapsto(i,j,k)$, and $\varepsilon=0$ when the labels are not all different. For a rotation system $\rho$,

$$\mathrm{Pen}_\varepsilon(G,\rho)=\sum_{\ell:E\to\{0,1,2\}}\prod_v\varepsilon\bigl(\ell(e_v),\ell(f_v),\ell(g_v)\bigr).$$

The Tait count is the same sum with $|\varepsilon|$ in place of $\varepsilon$. On a cubic graph every improper labelling has a zero factor, so both sums are supported on the Tait colourings. Only the signs can separate them.

For a cached triangulation $T_{n,i}$, the rotation $\rho$ is `plane_dual_rotation`: dual vertices are the faces of `networkx.check_planarity`, in discovery order, and the cyclic order is the facial walk with the face on the right. The dual is cubic of order $2n-4$.

Track 4, as stated on the navigator node `track4`, is: the Penrose evaluation is nonzero for every bridgeless planar cubic graph.

## 2. Statement

**Computed.** For every triangulation in `compute/data/triangulations_n4_11.json` ($n=4,\ldots,11$; $1555$ graphs),

$$\mathrm{Pen}_\varepsilon(T^*,\rho)=(-1)^n\,\#\mathrm{Tait}(T^*)=(-1)^{|V(T^*)|/2}\,\#\mathrm{Tait}(T^*),$$

with $\#\mathrm{Tait}(T^*)>0$. One of the two sign classes is empty on every such dual: there is no cancellation. `penrose_eval` on the same duals, for all $23$ graphs with $n\le 8$, equals $\#\mathrm{Tait}$ and equals `count_tait_colourings`.

**Reformulation.** The sentence “`penrose_eval(G)>0` for every bridgeless planar cubic graph $G$” is the sentence “every bridgeless planar cubic graph has a Tait colouring”, because that is what the function returns. A bridgeless cubic plane graph is $3$-edge-colourable if and only if its faces are $4$-colourable. That sentence is Tait’s form of the Four Colour Theorem. Track 4 is that reformulation.

The signed sum is not a second theorem on this cache. It is zero if and only if the Tait count is zero, since the colourings all share the sign $(-1)^{|V|/2}$.

## 3. Evidence

`penrose_eval.py` was not modified. `D2_report.md` was not present. The state-sum script has a CLI and writes `groups/D2_results.json`.

```
PYTHONPATH=/Users/fulkanjou/GraphColour .venv/bin/python compute/topology/a1720_penrose_state_sum.py
```

Python: `/Users/fulkanjou/GraphColour/.venv/bin/python`. The script’s own deadline is $540$ seconds. It stopped at the end of the cache, not at the deadline. `groups/D2_results.json` records elapsed time $0.8098$s.

| $n$ | graphs | sign of $\mathrm{Pen}_\varepsilon$ | Tait min–max | time |
|---|---|---|---|---|
| 4 | 1 | $+$ | $6$ | $0.0003$s |
| 5 | 1 | $-$ | $6$ | $0.0033$s |
| 6 | 2 | $+$ | $6$–$24$ | $0.0005$s |
| 7 | 5 | $-$ | $6$–$30$ | $0.0013$s |
| 8 | 14 | $+$ | $6$–$72$ | $0.0049$s |
| 9 | 50 | $-$ | $6$–$126$ | $0.0195$s |
| 10 | 233 | $+$ | $6$–$264$ | $0.1031$s |
| 11 | 1249 | $-$ | $6$–$510$ | $0.6596$s |

In that file a row is a mismatch only when $\mathrm{Pen}_\varepsilon\neq(-1)^n\#\mathrm{Tait}$ or the D1 checksum fails. The mismatch list is empty. The $1305$ odd-order triangulations have $\mathrm{Pen}_\varepsilon=-\#\mathrm{Tait}$; that is the sign formula, not cancellation. Brute force over $E\to\{0,1,2\}$ matches the backtrack for every dual with $n\le 5$, including the value $-6$ on $T_{5,0}$.

Checksum, read-only: the Tait counts match `D1_results.json` on all $73$ graphs with $n\le 9$, and match `D1_n11.json` on all $1482$ graphs with $n\in\{10,11\}$. Disagreements: $0$.

Direct call of `penrose_eval` on the $23$ duals with $n\le 8$: equal to the Tait count on $23/23$, equal to `count_tait_colourings` on $23/23$, equal to $\mathrm{Pen}_\varepsilon$ on $17/23$. The six failures of equality with the signed sum are $T_{5,0}$ and the five graphs of order $7$, where the signed sum is negative and `penrose_eval` returns the positive count.

The same two counters were run on the planar cubic graphs of order at most $20$ in `build_graph_library`, with the clockwise rotation `neighbors_cw_order`. On $K_4$, the triangular prism, the cube, the prisms $C_5,\ldots,C_{10}$, the Frucht graph, and the dodecahedral graph, `penrose_eval` equals the Tait count and $\mathrm{Pen}_\varepsilon=(-1)^{|V|/2}$ times that count, with no cancellation. The dodecahedral graph gives $60$, and a separate count gives $P(\mathrm{icosahedron},4)=240$, so $P/4=60$.

Controls from the same run. The plane embedding of $K_4$ has $\mathrm{Pen}_\varepsilon=\#\mathrm{Tait}=6$, and the brute sum agrees. Of the $16$ choices of local orientation on $K_4$, eight give $+6$, eight give $-6$, and none cancel. Reversing the rotation at one vertex of the dual of $T_{4,0}$ negates $\mathrm{Pen}_\varepsilon$ and preserves the Tait count. Every one of the $64$ local orientations of $K_{3,3}$ has signed sum $0$ and Tait count $12$. Petersen has both sums $0$.

Library audit, planarity by `networkx.check_planarity`. The Pappus graph is stored with `flag_planar` true and is not planar. `K4-expanded (8v)` and `Cube-expanded (12v)` are not cubic. The other $17$ flags match.

No web page was retrieved. The equivalence used above is the identity of `penrose_eval` with the Tait count, together with Tait’s correspondence. The module itself records the same equivalence as Kauffman (1990).

## 4. Result

**Computed** on every cached triangulation, $n\le 11$, and on the named planar cubic graphs of order at most $20$ in the Penrose library. **`penrose_eval` is a Tait count, not an independent state sum.**

**Literature-settled as a reformulation.** Track 4 does not add a predicate beyond Tait colourability of bridgeless planar cubic graphs, which is the Four Colour Theorem. The signed sum can be a different integer: on $K_{3,3}$ it vanishes while $12$ Tait colourings exist. On the planar graphs tested here, it does not vanish separately. No positivity mechanism beyond agreement of signs is visible. The common sign is negative when $|V|/2$ is odd, so the raw signed sum is not a positive count until the global orientation is fixed. Reversing one vertex flips that sign.

## 5. Kill criterion

For Track 4: $\mathrm{Pen}(G)=0$ for some bridgeless planar cubic graph. Not met on the cache or on the named planar library graphs. Every Tait count above is at least $6$.

For the hope that the signed sum is independent of the Tait count on planar rotations: a planar cubic graph whose Tait colourings carry both signs, or whose signed sum is $0$ while a Tait colouring exists. Not met here.

The $K_{3,3}$ cancellation kills that hope off the plane. It does not kill Track 4, which quantifies only over planar graphs.

## 6. Not proved

The sign law is counted for the cache and the named graphs. It is not proved for every plane cubic graph. Nothing here proves that every bridgeless planar cubic graph has a Tait colouring. That statement is the Four Colour Theorem. `penrose_eval.py` was not edited, so the false Pappus flag and the non-cubic expansions remain in that file.

## 7. Feasibility

**Low** for a proof of Track 4. A proof is a proof of the Four Colour Theorem. The finite comparison asked of this group is finished.

## 8. Next steps

Do not open an attack that treats $\mathrm{Pen}_\varepsilon$ on planar cubic graphs as a new invariant: on every graph tested here it is $\pm$ the Tait count. A one-line correction of the Pappus flag belongs in `penrose_eval.py`; this group was not to edit that file. The triangulation cache stops at $11$ vertices.

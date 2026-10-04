# D1b — Tait colourings and nowhere-zero 4-flows at $n=10,11$

**Group:** D1b, manager M-Duality
**Date:** 2 October 2026
**Status:** finite check on the cached triangulations of orders 10 and 11. A reformulation of the Four Colour Theorem, not a proof.

## 1. Definitions

Let $T_{n,i}$ be the triangulation whose edge list is `graphs[str(n)][i]` in `compute/data/triangulations_n4_11.json`. Its plane dual $T^*$ is built by `simple_dual` in `compute/flows/a1720_tait_flows.py` (embedding from `networkx.check_planarity`). For a triangulation on $n\ge 4$ vertices the dual is cubic on $2n-4$ vertices.

Four counts, each from that module:

- labelled Tait colourings of $T^*$, by `count_tait`;
- nowhere-zero $\mathbb{Z}_2\times\mathbb{Z}_2$-flows of $T^*$, by `count_z2z2_flows`;
- nowhere-zero $\mathbb{Z}_4$-flows of $T^*$, by `count_zk_flows`, once for `default_orientation` and once for `random_orientation` from `random.Random(1720)`;
- $P(T,4)$, by `count_colourings`.

`compute/flows/a1720_d1b_n10_11.py` calls those functions and monkeypatches `OUT`. It does not edit `a1720_tait_flows.py`.

## 2. Statement

**Computed.** For every $n\in\{10,11\}$ and every index $i$ with $T_{n,i}$ in the cache ($233$ graphs at $n=10$, $1249$ at $n=11$),

$$\#\mathrm{Tait}(T^*) = F(T^*,\mathbb{Z}_2\times\mathbb{Z}_2) = F(T^*,\mathbb{Z}_4) = P(T,4)/4 > 0,$$

and the two orientations give the same $\mathbb{Z}_4$ count. Every such dual has vertex-connectivity $3$ and edge-connectivity $3$.

**Literature.** For a connected plane graph, a proper $k$-colouring of the faces determines a nowhere-zero $\mathbb{Z}_k$-flow by taking colour differences, and Tutte's deletion–contraction argument shows that the number of nowhere-zero $A$-flows depends only on $|A|$. Tait's correspondence then equates 3-edge-colourability of a bridgeless cubic plane graph with 4-colourability of its faces. The sentence "every bridgeless planar graph has a nowhere-zero 4-flow" is a reformulation of the Four Colour Theorem. This run does not prove that sentence.

Jaeger (1979) proved that every 4-edge-connected graph has a nowhere-zero 4-flow. A cubic graph has a vertex of degree 3, so its edge-connectivity is at most 3. These duals are not 4-edge-connected, and the run records edge-connectivity exactly 3 on each of them.

## 3. Evidence

Two processes, one per order, then a merge. Python: `/Users/fulkanjou/GraphColour/.venv/bin/python`.

```
.venv/bin/python compute/flows/a1720_d1b_n10_11.py 10
.venv/bin/python compute/flows/a1720_d1b_n10_11.py 11
.venv/bin/python compute/flows/a1720_d1b_n10_11.py merge
```

The first two ran together. Each process stopped itself at $600$ seconds; neither hit the cap. The shell returned in $20.5$s.

| $n$ | cached | checked | identities | Tait min–max | $\kappa=\lambda$ | process time |
|---|---|---|---|---|---|---|
| 10 | 233 | 233 | hold | $6$–$264$ | $3$ | $2.25$s |
| 11 | 1249 | 1249 | hold | $6$–$510$ | $3$ | $20.18$s |

Duals: $16$ vertices and $24$ edges at $n=10$; $18$ vertices and $27$ edges at $n=11$. Mismatches: $0$. Output: `backgroundMaterial/agent1720/groups/D1_n11.json`. The field `elapsed_seconds` there is $22.44$, the sum of the two process times and a $0.01$s sanity call, not a second wall clock. `D1_results.json` was not written. Orders $n\le 9$ were not recomputed. The $k\in\{3,5\}$ checks were not run.

Sanity on the same counters: $K_4$ gives $6=6=6=P(K_4,4)/4$, and its dual is $K_4$. The Petersen graph gives $0$ Tait colourings, $0$ nowhere-zero 4-flows, and $240$ nowhere-zero $\mathbb{Z}_5$-flows.

Read-only cross-check: every `P4` in `D1_n11.json` equals the stored `P4` in `compute/data/chromatic_polys_n4_11.json` ($233+1249$ graphs, $0$ disagreements). That file was not modified.

## 4. Result

**Computed** on the cached triangulations of orders $10$ and $11$. **Literature-settled as a reformulation** of the Four Colour Theorem (Tait 1880; Tutte, Canadian J. Math. 1954; textbook account in Diestel, *Graph Theory*, chapter on flows). Jaeger's 4-edge-connected 4-flow theorem (J. Combin. Theory B, 1979) and Seymour's 6-flow theorem (J. Combin. Theory B, 1981) were not re-proved.

## 5. Kill criterion

A mismatch among Tait count, $\mathbb{Z}_2\times\mathbb{Z}_2$-flow count, $\mathbb{Z}_4$-flow count, and $P(T,4)/4$ on some cached $T_{10,i}$ or $T_{11,i}$. Not met.

## 6. Not proved

The identity is counted for the cached graphs of orders $10$ and $11$, not proved for every triangulation. Nothing here proves a nowhere-zero 4-flow on an arbitrary bridgeless planar graph. That planar 4-flow statement is a reformulation of the Four Colour Theorem. Tutte duality at $k\in\{3,5\}$ was not checked at these orders. Cubic duals are not 4-edge-connected.

## 7. Feasibility

**Low** for a proof of the identity on all triangulations: that proof is the Four Colour Theorem. The finite check of the cache is finished.

## 8. Next steps

The cache stops at $11$ vertices, so this repository has no further triangulation to count. Do not open an attack that treats these cubic duals as 4-edge-connected. A later $k\in\{3,5\}$ check at $n=10,11$ would be a different statement from the identity run here.

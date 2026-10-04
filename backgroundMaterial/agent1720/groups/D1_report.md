# D1 — Tait colourings and nowhere-zero 4-flows

**Group:** D1, manager M-Duality
**Date:** 2 October 2026
**Status:** computation on $n \le 9$, plus a written duality argument. Not a proof of the Four Colour Theorem.

## 1. Definitions

Let $T$ be a labelled triangulation from `compute/data/triangulations_n4_11.json`. Its plane dual $T^*$ is the cubic multigraph whose vertices are the faces of a planar embedding of $T$ (`networkx.check_planarity`). A **Tait colouring** is a proper 3-edge-colouring of $T^*$ with labelled colours. A **nowhere-zero $A$-flow** is an assignment of non-identity elements of a finite abelian group $A$ to the oriented edges such that Kirchhoff's law holds at every vertex.

`compute/flows/a1720_tait_flows.py` counts four quantities independently: labelled Tait colourings by backtracking; nowhere-zero $\mathbb{Z}_2\times\mathbb{Z}_2$-flows from the cycle space; nowhere-zero $\mathbb{Z}_4$-flows from free values on the cotree; and $P(T,4)$ by counting proper vertex 4-colourings.

## 2. Statements

**Computed.** For every triangulation on $n \le 9$ vertices,
\[
\#\mathrm{Tait}(T^*) = F(T^*,\mathbb{Z}_2\times\mathbb{Z}_2) = F(T^*,\mathbb{Z}_4) = P(T,4)/4.
\]
The same script checks $F(T^*,k) = P(T,k)/k$ for $k \in \{3,5\}$ on that range. Every dual is $3$-vertex-connected and $3$-edge-connected.

**Written.** For a connected plane graph $G$, $P(G^*,k) = k\, F(G,k)$ when $G^*$ is the dual: a proper $k$-colouring of the vertices of the dual is a proper $k$-colouring of the faces of $G$, and the differences of face colours across edges are a nowhere-zero $\mathbb{Z}_k$-flow, unique once one face colour is fixed. Tutte's deletion–contraction recurrence shows that the number of nowhere-zero $A$-flows depends only on $|A|$. Tait's correspondence then says a bridgeless cubic plane graph is 3-edge-colourable if and only if its faces are 4-colourable. Therefore the sentence "every bridgeless planar graph has a nowhere-zero 4-flow" is equivalent to the Four Colour Theorem. It is a reformulation, not a kill.

Jaeger (1979) proved that every 4-edge-connected graph has a nowhere-zero 4-flow. That theorem does not reach these duals: a cubic graph has a vertex of degree 3, so its edge-connectivity is at most 3. The computation records edge-connectivity exactly 3 on every $T^*$ with $n \le 9$.

## 3. Evidence

Command: `.venv/bin/python compute/flows/a1720_tait_flows.py 9 9`

| $n$ | graphs | identities | Tait min–max | elapsed |
|---|---|---|---|---|
| 4 | 1 | hold | 6–6 | 0.02s |
| 5 | 1 | hold | 6–6 | 0.00s |
| 6 | 2 | hold | 6–24 | 0.01s |
| 7 | 5 | hold | 6–30 | 0.04s |
| 8 | 14 | hold | 6–72 | 0.16s |
| 9 | 50 | hold | 6–126 | 1.36s |

Sanity: $K_4$ has 6 Tait colourings, 6 flows of each 4-group, and $P(K_4,4)/4 = 6$, and the dual is $K_4$. The Petersen graph has 0 Tait colourings and 0 nowhere-zero 4-flows, and 240 nowhere-zero $\mathbb{Z}_5$-flows. Mismatches: none. Wall clock 1.6s. Output: `backgroundMaterial/agent1720/groups/D1_results.json`.

## 4. Result

**Computed** on $n \le 9$. **Literature-settled as a reformulation** of the Four Colour Theorem (Tait 1880; Tutte 1954; textbook account in Diestel, *Graph Theory*, chapter on flows). The 8-flow theorem (Jaeger) and the 6-flow theorem (Seymour 1981) are literature; they were not re-proved here.

## 5. Kill criterion

"A count mismatch on some $T$" — not met.

## 6. Not proved

No identity was proved for all triangulations, only counted through 9 vertices. $n = 10$ and $n = 11$ were not run. Nothing here proves a nowhere-zero 4-flow on an arbitrary bridgeless planar graph. The 4-edge-connected 4-flow theorem does not apply to cubic duals.

## 7. Feasibility

**Low** for a flow proof of the Four Colour Theorem that only improves the 6-flow theorem down to 4 on planar graphs: that improvement is the theorem itself. **Medium** for checking the same identities at $n = 10$ and $n = 11$ (the $n = 9$ run was 1.6s).

## 8. Next steps

Run the existing script at `max_n = 11` and stop if one $n$ exceeds ten minutes. Do not open a new attack that assumes cubic duals are 4-edge-connected.

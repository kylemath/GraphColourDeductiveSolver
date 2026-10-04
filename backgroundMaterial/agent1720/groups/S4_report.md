# S4 — Deductive routes outside tracks 1–7

**Group:** S4, manager M-Frontier
**Date:** 2 October 2026
**Status:** three routes recommended. One finite check computed. Root-bounding stays dead. Tracks 1–7 are not reopened.

| Class | Route | Exact statement | Feasibility | Kill criterion |
|---|---|---|---|---|
| Recommendation | Hajós at $k=5$ | Every finite simple graph with no subdivision of $K_5$ has $\chi\le 4$. | Low | One graph with $\chi\ge 5$ and no $K_5$ subdivision. Not met on order $\le 7$, nor on cached triangulations $n\le 11$. |
| Recommendation | Odd Hadwiger at $t=5$ | Every finite simple graph with no odd $K_5$-minor has $\chi\le 4$. | Low | One graph with $\chi\ge 5$ and no odd $K_5$-minor. Not tested. The conjecture for general $t$ is killed by a 2025 preprint. |
| Recommendation | Petersen minor in every snark | Every snark has a Petersen minor. | Low | One snark with no Petersen minor. Not tested. |
| Restatement | Hadwiger for $K_5$ | Every graph with no $K_5$ minor has $\chi\le 4$. | — | Relabel. The case is equivalent to the Four Colour Theorem. |
| Restatement | Tait edge-colouring | Every snark is non-planar. | — | Relabel. Equivalent form of the Four Colour Theorem. |
| False strengthening | Tait–Hamilton | Every $3$-connected cubic planar graph is Hamiltonian. | — | Met by Tutte's graph (1946). This claim is false, so it is not a restatement. |
| Restatement | Penrose | For every bridgeless planar cubic graph, the Penrose evaluation is nonzero. | — | Relabel. Kauffman (1990). |
| Killed here | Universal degree $\le 4$ | Every simple planar triangulation has a vertex of degree at most $4$. | — | Met by the icosahedron. |

## 1. Definitions

A **$K_5$ subdivision** is a subgraph that is $K_5$ with edges replaced by internally vertex-disjoint paths. `has_k5_subdivision` in `compute/discovery/a1720_s4_hajos.py` searches branch vertices of degree at least $4$ and routes the missing pairs through private internal vertices.

`colourable(n, adj, k)` in the same file is exact backtrack. A **Hajós counterexample at $k=5$** is a simple graph with no $K_5$ subdivision that is not $4$-colourable.

$T_{n,i}$ is `graphs[str(n)][i]` in `compute/data/triangulations_n4_11.json`. Planarity is `networkx.check_planarity`. A planar graph has no $K_5$ minor and therefore no $K_5$ subdivision.

An **odd $K_k$-minor**, as stated on the Hadwiger page cited below, is $k$ vertex-disjoint two-coloured subtrees with a monochromatic edge between every pair. It is not implemented in this script.

A **snark** is a non-$3$-edge-colourable cubic graph, excluding trivial low-connectivity or low-girth examples. The script does not build snarks.

The **icosahedron** is `networkx.icosahedral_graph`, checked by `check_icosahedron`.

## 2. Statement

**Computed.** Every simple graph on at most $7$ vertices with no $K_5$ subdivision is $4$-colourable. Every cached triangulation $T_{n,i}$ with $4\le n\le 11$ is planar, has no $K_5$ subdivision, and is $4$-colourable. Among those triangulations, the minimum degree is $3$ or $4$.

**Recommended, not computed past the citation.**

Hajós's conjecture at $k=5$ is the first row of the table. It implies the Four Colour Theorem, because a planar graph has no $K_5$ subdivision. It also quantifies over non-planar graphs, so a counterexample need not be planar. The Hadwiger page records that the subdivision conjecture is a theorem for $k\le 4$, open for $k=5$ and $k=6$, and false for $k\ge 7$.

The odd-Hadwiger statement at $t=5$ is the second row. The same page states the Gerards–Seymour conjecture for every $k$. Only the case $k=5$ would force every planar graph to be $4$-colourable. The preprint below disproves the conjecture for large $k$ by a $(3/2-o(1))k$ lower bound. That asymptotic does not exhibit a $5$-chromatic graph with no odd $K_5$-minor.

The snark statement is the third row. The snark page calls "every snark is non-planar" an equivalent form of the Four Colour Theorem. "Every snark has a Petersen minor" implies that form, because the Petersen graph is non-planar, and it also constrains non-planar snarks.

**Restatements, not recommended.**

Hadwiger's conjecture for $K_5$ is a restatement. The Hadwiger page states that the case $k=5$ implies the Four Colour Theorem by Wagner's theorem, and that $1\le t\le 6$ is known.

Tait's Hamiltonian claim is a false strengthening: Tutte (1946) produced a non-Hamiltonian $3$-connected cubic planar graph. The edge-colouring form is the restatement. For a cubic graph, a perfect matching whose deletion leaves only even cycles is the same $3$-edge-colouring statement again.

The Penrose evaluation is a restatement. Kauffman (1990) proved that a bridgeless planar cubic graph has nonzero Penrose evaluation if and only if it is $4$-face-colourable (`SolvingFrameworkPlan/Plan3_TQFT_SheafCohomology.md`).

**Killed, not recommended.** The list-colouring extension of Hadwiger fails for planar graphs: the same page records that their list-chromatic number is $5$ (Voigt 1993; Thomassen 1994). Deleting only vertices of degree at most $4$ cannot exhaust every triangulation: the icosahedron is a $5$-regular planar triangulation.

Robertson–Sanders–Seymour–Thomas discharging is the existing proof and is S3's audit. Gonthier's Coq script is a formalization of a proof, not a new deduction.

## 3. Evidence

Command:

```
/Users/fulkanjou/GraphColour/.venv/bin/python /Users/fulkanjou/GraphColour/compute/discovery/a1720_s4_hajos.py
```

Wall clock $25.199$ seconds. Output: `backgroundMaterial/agent1720/groups/S4_results.json`.

The NetworkX atlas `graph_atlas_g` has $1253$ graphs, orders $0$ through $7$ with counts $1,1,2,4,11,34,156,1044$. Of these, $66$ are not $4$-colourable: $1$ on $5$ vertices, $6$ on $6$, and $59$ on $7$. Each of the $66$ has a $K_5$ subdivision. The counterexample list is empty.

Cached triangulations match the plantri counts $1,1,2,5,14,50,233,1249$. All $1555$ are planar, none has a $K_5$ subdivision, and none fails $4$-colouring. Minimum-degree histogram: degree $3$ occurs $1500$ times and degree $4$ occurs $55$ times ($1+1+2+5+12+34$ for $n=6,\ldots,11$). The key `ge5` is $0$ for every $n\le 11$.

The icosahedron has $12$ vertices, $30$ edges, minimum degree $5$, is planar and maximal planar, has no $K_5$ subdivision, and is $4$-colourable.

Self-checks inside the script: $K_5$ is not $4$-colourable and contains a $K_5$ subdivision; $K_4$ is $4$-colourable, not $3$-colourable, and has no $K_5$ subdivision; a once-subdivided $K_5$ is detected; the Petersen graph, which is cubic, has no $K_5$ subdivision.

**Citations.**

- Hajós at $k=5$, and Hadwiger for $K_5$: Hadwiger conjecture (graph theory), section Generalizations, https://en.wikipedia.org/wiki/Hadwiger_conjecture_(graph_theory). Catlin's counterexamples for $k\ge 7$: P. A. Catlin, *Hajós's graph-colouring conjecture: variations and counterexamples*, Journal of Combinatorial Theory, Series B 26 (1979), 268–274, https://doi.org/10.1016/0095-8956(79)90062-5.
- Odd Hadwiger, general $t$: Marcus Kühn, Lisa Sauermann, Raphael Steiner, and Yuval Wigderson, *Disproof of the Odd Hadwiger Conjecture*, arXiv:2512.20392, https://arxiv.org/abs/2512.20392. The abstract states that there are graphs with no odd $K_t$ minor and chromatic number at least $(\tfrac{3}{2}-o(1))t$.
- Snarks: https://en.wikipedia.org/wiki/Snark_(graph_theory). The page states that every snark being non-planar is an equivalent form of the Four Colour Theorem, and that Tutte's snark conjecture asks for a Petersen minor in every snark.

## 4. Result

**Computed** on every simple graph of order at most $7$, and on every cached triangulation of order $4\le n\le 11$. The Hajós kill criterion is not met on those families.

**Killed**, by the icosahedron in the same run: the claim that every simple planar triangulation has a vertex of degree at most $4$.

The odd-Hadwiger conjecture for general $t$ is **literature-killed** by the preprint above. The case $t=5$ is not settled by that abstract.

## 5. Kill criterion

For the computed Hajós check, the kill is one graph in the atlas or the cache with no $K_5$ subdivision and chromatic number at least $5$. It was not met.

For the unrestricted Hajós statement, the same kind of graph of any order is the kill. It was not met here.

For "every triangulation has a vertex of degree $\le 4$", the kill is met: the icosahedron has minimum degree $5$. It is still $4$-colourable, so this kill does not touch the Four Colour Theorem, and it does not touch Hajós at $k=5$.

## 6. Not proved

Hajós's conjecture at $k=5$ is open. Nothing was proved about graphs on $8$ or more vertices, except the single icosahedron. Odd Hadwiger at $t=5$ was not tested. No snark was built. The Four Colour Theorem was not proved. Wagner's equivalence, Tutte's graph, and Kauffman's Penrose theorem were cited, not re-proved.

## 7. Feasibility

**Medium** for the next finite step: exhaust the $12346$ graphs on $8$ vertices. Colouring and the subdivision test are cheap at order $7$; the missing piece is an isomorphism-free generator, which is not installed.

**Low** for a proof of Hajós at $k=5$, of odd Hadwiger at $t=5$, or of a Petersen minor in every snark. Each statement implies the Four Colour Theorem and properly extends it, and the nearby general statements are already false or are unpublished announcements.

## 8. Next steps

1. Generate the nonisomorphic graphs on $8$ vertices in the project virtual environment and rerun `colourable` and `has_k5_subdivision`. A single counterexample kills Hajós at $k=5$ and leaves the planar theorem untouched.
2. Leave general odd Hadwiger. Read arXiv:2512.20392 only to see whether the construction is already above $4$ colours at $t=5$. If it is, kill the second route with that graph. If it is not, the case $t=5$ stays open.
3. Leave planar Tait colouring to D1. The third route dies only when a snark with no Petersen minor is written down.

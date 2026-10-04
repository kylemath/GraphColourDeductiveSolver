# S3b — D-reducibility by ring Kempe closure

**Group:** S3b, manager M-Frontier
**Date:** 2 October 2026
**Status:** computed. The Birkhoff diamond is D-reducible. A single degree-5 vertex is not.

## 1. Definitions

`backgroundMaterial/agent1720/groups/S3_results.json` defines D-reducibility as direct extension of a ring vertex colouring, and states that Kempe swaps are not used. That predicate is not D-reducibility. It is left unchanged, as is `compute/discharging/a1720_d_reducibility.py`.

The test used here is the ring-colour closure of Robertson, Sanders, Seymour, and Thomas, *The Four-Colour Theorem*, J. Combin. Theory Ser. B 70 (1997), 2–44, §3. Functions live in `compute/discharging/a1720_d_reducible_kempe.py`.

The free completion $S$ is a near-triangulation of a disk. Ring edges are $e_0,\ldots,e_{r-1}$ in order. A **tri-colouring** assigns colours in $\{-1,0,1\}$ to the edges so that every internal triangle receives all three. Equivalently, vertex colours lie in the Klein group $\mathbb{Z}_2\times\mathbb{Z}_2$, and the colour of an edge is the nonzero sum of its ends (`XOR_TO_EDGE` in `survey_colourings`). Let $C^*$ be every map $E(R)\to\{-1,0,1\}$, so $|C^*|=3^r$. Let $C\subseteq C^*$ be the restrictions of tri-colourings of $S$.

A **signed matching** is a non-crossing pairing of distinct ring edges, each pair carrying a sign $\pm 1$ (`noncrossing_matchings`). It is the Kempe interchange on the ring. A colouring $\lambda$ **$\theta$-fits** the matching when $\{e:\lambda(e)\ne\theta\}$ is exactly the paired set, and the two edges of a pair have equal colours if and only if the sign is $+1$ (`companions`). A set $\mathcal{C}$ of edge-colourings is **consistent** when, for every $\lambda\in\mathcal{C}$ and every $\theta\in\{-1,0,1\}$, some signed matching $\theta$-fits $\lambda$ and every colouring that $\theta$-fits it also lies in $\mathcal{C}$ (`maximal_consistent_subset`). The empty set is consistent, and the union of consistent sets is consistent, so every family has a unique maximal consistent subset.

$S$ is **D-reducible** when that subset of $C^*\setminus C$ is empty (`analyse`). Passage to edge colours quotients vertex colourings by translation in the Klein group. Orbits under the full permutation of the four vertex colours are counted separately (`canonical_vertex_orbits`); they are not an extra move.

`component_swap_closure_failures` closes proper vertex 4-colourings under swaps of every bichromatic component of the ring, including an isolated vertex. That graph is not the test above.

## 2. Statement

**Free completion.** Up to dihedral relabeling of the ring there is one chordless triangulated disk with boundary $C_6$ and four interior vertices of degree 5. It has $10$ vertices, $21$ edges, and $12$ internal triangles. The cap lengths are $(2,1,2,1)$. `birkhoff_diamond` builds that graph. `incidence_is_disk` checks the triangle incidences.

**Quantifiers.** For this $S$, every $\lambda\in C^*\setminus C$ fails to lie in a consistent subset of $C^*\setminus C$. Equivalently, the maximal consistent subset is empty. For the wheel of ring size $5$ with one hub (`wheel(5)`), that subset has $30$ elements. One of them is $(-1,-1,0,-1,1)$.

## 3. Evidence

Command:

`/Users/fulkanjou/GraphColour/.venv/bin/python compute/discharging/a1720_d_reducible_kempe.py`

Script wall clock $0.0321$ s. Output: `backgroundMaterial/agent1720/groups/S3b_results.json`.

The non-crossing matching generator agrees with the Catalan numbers $1,1,2,5,14$ on $0,2,4,6,8$ points. The vertex counts $84$, $240$, and $732$ equal $(k-1)^n+(-1)^n(k-1)$ at $k=4$. Up to permutation of the four colours there are $10$ colourings of $C_5$ and $31$ of $C_6$.

| Free completion | $\|C^*\|=3^r$ | $\|C\|$ | consistent bad set | D-reducible | Vertex colourings of $R$ that do not extend |
|---|---|---|---|---|---|
| Birkhoff diamond, $r=6$ | $729$ | $96$ | $0$ | yes | $348$ of $732$ |
| Degree-5 hub, $r=5$ | $243$ | $30$ | $30$ | no | $120$ of $240$ |
| Degree-4 hub, $r=4$ (checksum) | $81$ | $15$ | $0$ | yes | $24$ of $84$ |

Robertson, Sanders, Seymour, and Thomas, J. Combin. Theory Ser. B 70 (1997), 2–44, define this closure in §3 and prove that every loopless planar graph is $4$-colourable, by an unavoidable set of $633$ configurations, each D-reducible or carrying a contract of size at most $4$. That computer check was not run. Birkhoff, *The reducibility of maps*, Amer. J. Math. 35 (1913), 115–128, proved this diamond reducible by hand. The table is this repository's enumeration of the 1997 condition.

## 4. Result

**Computed**, on the Birkhoff diamond and on the degree-5 wheel, with the degree-4 wheel as a checksum of the same function. The diamond is D-reducible. The degree-5 vertex is not.

**Literature**, not re-proved: the Four Colour Theorem, in the form just cited.

## 5. Kill criterion

For either free completion, a nonempty maximal consistent subset of $C^*\setminus C$ kills D-reducibility.

Met for the degree-5 hub ($30$ colourings, including $(-1,-1,0,-1,1)$). Not met for the diamond.

## 6. Not proved

Nothing here shows that a minimal counterexample contains one of the $633$ configurations, or that it is internally $6$-connected. Rings of size greater than $6$ were not tested. Direct extension is a weaker predicate: $348$ of the $732$ proper vertex $4$-colourings of the diamond's ring do not extend, and the file `S3_results.json` stops at that count.

The free component-swap graph is also a different predicate. On both configurations it has $0$ failures (`naive_component_swap_not_the_test`), so it calls the degree-5 wheel D-reducible. The signed-matching closure does not.

## 7. Feasibility

**High** for the same decision on one further free completion of ring size $7$ ($3^7=2187$ edge-colourings). **Low** for an unavoidable set, built in this repository, large enough to prove the Four Colour Theorem.

## 8. Next steps

Use `maximal_consistent_subset`, not the direct-extension flag in `S3_results.json` and not `component_swap_closure_failures`. The next single check is one named free completion of ring size $7$, with the ring-size guard raised, inside the ten-minute budget. An unavoidable set is a separate discharging argument. The 1997 paper is the literature for that argument.

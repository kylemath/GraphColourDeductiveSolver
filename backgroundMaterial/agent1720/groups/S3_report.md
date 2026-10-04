# S3 — D-reducibility of the Birkhoff diamond

**Group:** S3, manager M-Frontier
**Date:** 2 October 2026
**Status:** finite check of two free completions. Not a proof of the Four Colour Theorem.

## 1. Definitions

`compute/discharging/reducibility_checker.py` (`enumerate_ring_colourings`, `extend_to_interior`, `kempe_equivalent_colourings`, `DReducibilityChecker.check`) enumerates proper vertex 4-colourings of the ring and counts how many extend to the interior by backtracking, or after at most `kempe_depth` (default 2) Kempe swaps in the subgraph induced by the ring. Its `birkhoff_diamond` is a single interior vertex joined to all six ring vertices, plus the chords $(0,2)$, $(2,4)$, and $(4,0)$, so that interior vertex has degree 6. Its `degree5_wheel` is a 5-cycle plus a hub.

The test used below is the one in Robertson, Sanders, Seymour, and Thomas, *The Four-Colour Theorem*, J. Combin. Theory Ser. B 70 (1997), §3. It is implemented in `compute/discharging/a1720_d_reducibility.py`.

The free completion $S$ is a near-triangulation of a disk. The ring $R$ is the boundary circuit, with edges $e_0,\ldots,e_{r-1}$ in order. A **tri-colouring** of $S$ assigns colours in $\{-1,0,1\}$ to the edges so that every finite face receives all three colours. Equivalently (`extendable_ring_edge_colourings`), the colours are the nonzero symmetric differences of a proper vertex 4-colouring with values in the Klein group $\mathbb{Z}_2\times\mathbb{Z}_2$. Let $C^*$ be the set of all maps $E(R)\to\{-1,0,1\}$, and let $C\subseteq C^*$ be the restrictions of tri-colourings of $S$.

A **signed matching** is a set of pairs of distinct ring edges, together with a sign $\pm 1$ on each pair, the pairs being disjoint and non-crossing on the circuit (`noncrossing_pairings`). A colouring $\lambda$ **$\theta$-fits** that matching when $\{e:\lambda(e)\ne\theta\}$ is exactly the set of paired edges, and the two edges of a pair receive equal colours if and only if the sign is $+1$. A set $\mathcal{C}$ of edge-colourings is **consistent** when, for every $\lambda\in\mathcal{C}$ and every $\theta\in\{-1,0,1\}$, some signed matching $\theta$-fits $\lambda$ and every colouring that $\theta$-fits it also lies in $\mathcal{C}$. The empty set is consistent, and the union of consistent sets is consistent, so every family of edge-colourings has a unique maximal consistent subset (`maximal_consistent_subset`).

$S$ is **D-reducible** when the maximal consistent subset of $C^*\setminus C$ is empty (`d_reducibility`). Direct extension of vertex colourings is a different count (`direct_vertex_extensions`).

## 2. Statement

**The free completion.** Up to a dihedral relabeling of the ring there is one chordless triangulated disk with boundary a 6-cycle and four interior vertices of degree 5. Euler's formula gives $V=10$, twelve internal triangles, and $E=21$. With no ring chord, the handshakes $R+2I=20$ and $6+R+I=21$ force ten ring–interior edges and five interior edges. Each boundary edge has one interior apex. All four interior vertices meet the ring, and the cap lengths are $2,2,1,1$ in cyclic order. Caps that meet share an interior edge, giving a 4-cycle. The two caps of length 2 are then saturated, so the fifth interior edge joins the two caps of length 1, which must sit opposite each other. The cap pattern is $(2,1,2,1)$.

`birkhoff_diamond` realises that graph. Ring vertices $0,\ldots,5$. Vertex 6 meets $\{0,1,2,7,9\}$, vertex 7 meets $\{2,3,6,8,9\}$, vertex 8 meets $\{3,4,5,7,9\}$, and vertex 9 meets $\{5,0,6,7,8\}$. The twelve internal triangles are listed in the output file. The ring is an induced 6-cycle.

**Computed.** For this $S$, with $r=6$, the maximal consistent subset of $C^*\setminus C$ is empty. For the wheel with ring $C_5$ and one hub (`wheel(5)`), that subset has $30$ elements.

## 3. Evidence

Command: `/Users/fulkanjou/GraphColour/.venv/bin/python compute/discharging/a1720_d_reducibility.py`

Wall clock inside the script: $0.0176$s. Output: `backgroundMaterial/agent1720/groups/S3_results.json`.

| Free completion | $\|C^*\|=3^r$ | $\|C\|$ | $\|C'\|=$ consistent bad | D-reducible | Vertex colourings of $R$ that fail to extend |
|---|---|---|---|---|---|
| Birkhoff diamond, $r=6$ | 729 | 96 | 0 | yes | 348 of 732 |
| Degree-5 hub, $r=5$ | 243 | 30 | 30 | no | 120 of 240 |
| Degree-4 hub, $r=4$ | 81 | 15 | 0 | yes | 24 of 84 |

The degree-4 wheel is a sanity check in the same run: direct extension already fails, and the consistent-set test still clears it. The matching generator was checked against the Catalan numbers $1,1,2,5,14$ for $0,2,4,6,8$ points. The ring counts $84$, $240$, and $732$ equal $(k-1)^n+(-1)^n(k-1)$ at $k=4$.

One edge-colouring in the degree-5 set $C'$ is $(-1,-1,0,-1,1)$.

Robertson, Sanders, Seymour, and Thomas, J. Combin. Theory Ser. B 70 (1997), 2–44, define this test in §3 and prove that every loopless planar graph is 4-colourable, by an unavoidable set of 633 configurations, each D-reducible or carrying a contract of size at most 4. That computer check was not run. Birkhoff, *The reducibility of maps*, Amer. J. Math. 35 (1913), 115–128, proved the diamond reducible by hand. The table above is this repository's enumeration of the 1997 condition, not a transcription of either argument.

## 4. Result

**Computed** on the Birkhoff diamond and on the wheels of ring size 4 and 5.

**Literature**, not re-proved: the Four Colour Theorem, in the form just cited. A single degree-5 vertex remains in every minimal counterexample; the nonempty set $C'$ is the obstruction the computation finds.

## 5. Kill criterion

For either free completion, a nonempty maximal consistent subset of $C^*\setminus C$ kills D-reducibility.

Met for the degree-5 hub ($|C'|=30$). Not met for the diamond ($|C'|=0$).

## 6. Not proved

Nothing here shows that every internally 6-connected triangulation contains a reducible configuration, or that a minimal counterexample is internally 6-connected. Rings of size greater than 6, contracts, and the other configurations of the 1997 set were not tested. Direct extension is a strictly smaller property: $348$ proper vertex 4-colourings of the diamond's ring do not extend, and the degree-4 wheel has $24$ such colourings while still being D-reducible. The discharging SAT scripts in `compute/discharging/` were not run.

## 7. Feasibility

**High** for the same decision on one further free completion of ring size 7 ($3^7=2187$ edge-colourings). **Low** for an unavoidable set, built in this repository, large enough to prove the Four Colour Theorem.

## 8. Next steps

`d_reducibility` already decides every free completion of ring size at most 6; the diamond and the two wheels are the checks that identify the test. A ring of size 7 needs the guard raised and a single configuration timed, with the ten-minute budget of the standing orders. An unavoidable set is a separate discharging argument. The 1997 paper is the literature for that argument.

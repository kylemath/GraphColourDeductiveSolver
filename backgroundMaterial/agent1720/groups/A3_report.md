# A3 — Eulerian plane triangulations are 3-colourable

**Group:** A3, manager M-Algebra
**Date:** 2 October 2026
**Status:** proved for every simple plane triangulation. The cache $n \le 11$ agrees. The converse is not killed.

## 1. Definitions

A **simple plane triangulation** is a simple connected graph $G$ embedded in the plane without crossings so that every face, including the unbounded face, is a triangle on three distinct vertices. For $n = |V(G)| \ge 3$ one has $|E(G)| = 3n - 6$. For $n \ge 4$, $\delta(G) \ge 3$: a vertex of degree at most $2$ forces both incident faces to be the same triangle, so the graph is $K_3$.

The **dual** $G^*$ has one vertex per face of $G$ and one edge per edge of $G$, joining the two faces that contain that edge. A proper vertex colouring of $G^*$ is a proper face colouring of $G$. A proper face colouring of $G^*$ is a proper vertex colouring of $G$.

In the cache, $T_{n,i}$ is the edge list `graphs[str(n)][i]` in `compute/data/triangulations_n4_11.json`. Degrees are `degrees`. The exhaustive search is `three_colour`. The colouring built in the proof is `constructive_colouring`. All three live in `compute/chromatic/a1720_eulerian_3colour.py`. Stored counts $P(G,3)$ are the field `P3` of `compute/data/chromatic_polys_n4_11.json`, read only.

## 2. Statement

**Proved, for every simple plane triangulation.** $G$ admits a proper vertex colouring with three colours if and only if every vertex degree is even.

Equivalently, $G^*$ admits a proper face colouring with three colours if and only if every vertex degree of $G$ is even. A $3$-face-colouring of $G$ itself is a $3$-vertex-colouring of $G^*$, so it colours the dual.

On the cache, the same equivalence holds for every triangulation with $4 \le n \le 11$.

## 3. Evidence

### 3.1 Which graph receives the colours

Even degrees make $G^*$ bipartite (Lemma 1). Bipartiteness of $G^*$ is a $2$-vertex-colouring of $G^*$, hence a $2$-face-colouring of $G$.

The three vertex colours built below sit on $V(G)$. As face colours of $G^*$, they are a proper $3$-face-colouring of the dual.

A proper $4$-vertex-colouring of $G^*$ is a proper $4$-face-colouring of $G$. The faces of $G$ are triangles, and that does not turn those four face colours into three, nor does it colour $V(G)$. The argument below does not colour $V(G^*)$ with four colours.

The planar case of the dual criterion is stated on the dual-graph page, https://en.wikipedia.org/wiki/Dual_graph : a connected planar graph has even degree at every vertex if and only if its dual is bipartite. That page attributes the statement to D. J. A. Welsh, *Euler and bipartite matroids*, Journal of Combinatorial Theory 6 (1969), 375–377. Lemma 1 is proved here; the citation is not a step in the argument.

### 3.2 Proof

Throughout, $G$ is a simple plane triangulation on $n \ge 3$ vertices.

**Lemma 1.** Let $H$ be a connected plane graph. Every vertex degree of $H$ is even if and only if $H^*$ is bipartite.

The embedding fact used for both directions, and again in Lemma 3, is this: in a plane graph, a cycle is the boundary of a bounded open set which is a union of faces, and the edges with exactly one side in that set are the edges of the cycle.

First suppose every degree in $H$ is even. The face of $H^*$ corresponding to a vertex $v$ of $H$ meets $\deg(v)$ edge sides, so every face of $H^*$ has even degree. Let $C$ be a cycle of $H^*$, of length $k$, and let $\mathcal{F}$ be the set of faces of $H^*$ in the bounded interior of $C$. If $e_{\mathrm{int}}$ is the number of edges of $H^*$ lying strictly inside $C$, the face handshaking count on $\mathcal{F}$ is
\[
\sum_{f \in \mathcal{F}} \deg(f) = 2 e_{\mathrm{int}} + k.
\]
Each $\deg(f)$ is even, so $k$ is even. Every cycle of $H^*$ is even, and $H^*$ is bipartite.

Conversely, suppose $H^*$ is bipartite. Its vertices, the faces of $H$, fall into two colour classes, and faces that share an edge receive different colours. At a vertex $v$ of $H$ the incident faces alternate colours in the rotation, so the number of corners at $v$ is even. That number is $\deg(v)$.

**Lemma 2 (necessity).** If $G$ is properly $3$-vertex-coloured, then every degree is even.

Let $c \colon V(G) \to \{1,2,3\}$ be proper, and fix $v \in V(G)$. If $n = 3$, then $G \cong K_3$ and every degree is $2$.

Now take $n \ge 4$, and write $d = \deg(v) \ge 3$. The faces incident with $v$ are triangles. In rotation order their outer vertices are neighbours $v_0, \ldots, v_{d-1}$ of $v$, all distinct because $G$ is simple, and $v_i v_{i+1}$ is an edge for each $i$ (indices modulo $d$) because $\{v, v_i, v_{i+1}\}$ bounds a face. Each $v_i$ has a colour in $\{1,2,3\} \setminus \{c(v)\}$. Consecutive neighbours are adjacent, so those two colours alternate along the cycle $v_0 v_1 \ldots v_{d-1}$. Returning to $v_0$ after $d$ steps requires $d$ even.

**Lemma 3 (sufficiency).** If every degree of $G$ is even, then $G$ is properly $3$-vertex-colourable.

By Lemma 1, $G^*$ is bipartite, so the faces of $G$ have a proper $2$-colouring, black and white. Every edge of $G$ lies on one black face and one white face. Orient that edge so that the black face lies on the left and the white face on the right.

Work in $\mathbb{Z}/3\mathbb{Z}$. For a walk $W$, let $\sigma(W)$ be the number of steps that follow the orientation minus the number that oppose it. The goal is a map $c \colon V(G) \to \mathbb{Z}/3\mathbb{Z}$ with $c(v) \equiv c(u) + 1$ whenever $u \to v$ is a directed edge. Any such map is a proper $3$-colouring, because the difference across an edge is $\pm 1 \not\equiv 0$.

The boundary of a black face, walked with the face on the left, follows all three arrows, so $\sigma = 3$. The boundary of a white face, walked with the face on the left, opposes all three arrows, so $\sigma = -3$.

Let $C$ be any cycle of $G$, oriented so that its bounded interior lies on the left, and let $\mathcal{F}$ be the faces in that interior, of which $b$ are black and $w$ are white. Sum the left-hand boundaries of the faces in $\mathcal{F}$ as integer $1$-chains. An edge inside $C$ belongs to one black face and one white face, and the two left-hand boundaries traverse it in opposite directions, so it cancels. An edge of $C$ belongs to exactly one face of $\mathcal{F}$, and that face's left-hand boundary traverses it in the chosen direction of $C$. The sum is therefore $C$, and
\[
\sigma(C) = 3b - 3w \equiv 0 \pmod{3}.
\]
The same congruence holds for the opposite orientation of $C$, which changes the sign of $\sigma(C)$.

Fix a vertex $x_0$ and set $c(x_0) = 0$. For a vertex $x$ and a walk $W$ from $x_0$ to $x$, set $c(x) = \sigma(W) \bmod 3$. This is independent of the walk. If $W$ and $W'$ disagreed, the closed walk formed by $W$ followed by the reverse of $W'$ would have $\sigma \not\equiv 0 \pmod{3}$. Among closed walks with $\sigma \not\equiv 0 \pmod{3}$, take one of minimum length $L$, with vertex sequence $v_0, \ldots, v_L = v_0$. The vertices $v_0, \ldots, v_{L-1}$ are pairwise distinct: a repeat $v_i = v_j$ with $0 \le i < j \le L-1$ splits the walk into two strictly shorter closed walks whose $\sigma$-values sum to $\sigma$ of the whole, and one of those values would be nonzero modulo $3$. The minimal counterexample is therefore a cycle, and the previous paragraph says its $\sigma$ is $0$ modulo $3$.

Thus $c$ is well-defined. If $u \to v$ is a directed edge and $W$ is a walk from $x_0$ to $u$, the extension of $W$ by that edge has $\sigma$ larger by $1$, so $c(v) \equiv c(u) + 1 \pmod{3}$. Every edge is oriented, so $c$ is a proper $3$-colouring.

**Corollary.** A connected simple plane triangulation has either $0$ or $6$ proper $3$-vertex-colourings.

If $c$ is one such colouring, every face is a triangle and receives three distinct colours. Two faces that share an edge $uv$ have third vertices forced to the single colour in $\{1,2,3\} \setminus \{c(u), c(v)\}$. The dual is connected, so the colours on one face determine the colours on every face and hence on every vertex. There are $3! = 6$ ways to colour the first face. The six global permutations of $c$ are proper colourings. So the count is $6$ whenever it is positive.

Lemmas 2 and 3 are the statement in Section 2. The corollary is why each positive count below equals $6$.

### 3.3 Computation

Command:

```text
/Users/fulkanjou/GraphColour/.venv/bin/python compute/chromatic/a1720_eulerian_3colour.py
```

Wall clock $0.050807$ seconds. Search nodes $16794$. Output `backgroundMaterial/agent1720/groups/A3_results.json`. The polynomial file was only read.

`three_colour` tries colours $\{0,1,2\}$ in a fixed vertex order. The first vertex of that order is held at colour $0$, which loses no colouring: the three colours may be renamed. Degree parity is not used to prune. Every colouring that is returned is checked by `colouring_is_proper`. On each all-even graph, `constructive_colouring` $2$-colours the faces of a NetworkX embedding, orients the edges as in Lemma 3, and propagates the shift in $\mathbb{Z}/3\mathbb{Z}$.

Anchors: the unique graph on $4$ vertices is $K_4$, and the search returns no colouring. $T_{6,1}$ has degree sequence $(4,4,4,4,4,4)$.

The cache holds $1+1+2+5+14+50+233+1249 = 1555$ graphs, the plantri counts. Every edge list is simple and has $3n-6$ edges. The backtracker and the stored value $P(G,3) > 0$ agree on all $1555$ graphs.

The seven graphs with every degree even are exactly the seven graphs the search $3$-colours. Each has $P(G,3) = 6$, and the constructive colouring is proper.

| graph | degrees in vertex order | $P(G,3)$ | constructive colours |
|---|---|---|---|
| $T_{6,1}$ | $4,4,4,4,4,4$ | $6$ | $0,0,2,1,2,1$ |
| $T_{8,12}$ | $6,6,4,4,4,4,4,4$ | $6$ | $0,0,2,1,2,1,2,1$ |
| $T_{9,47}$ | $6,4,6,6,4,4,4,4,4$ | $6$ | $0,0,2,1,2,1,0,1,2$ |
| $T_{10,221}$ | $8,8,4,4,4,4,4,4,4,4$ | $6$ | $0,0,2,1,2,1,2,1,2,1$ |
| $T_{10,226}$ | $6,6,6,6,4,4,4,4,4,4$ | $6$ | $0,0,2,2,1,2,1,1,1,0$ |
| $T_{11,1220}$ | $8,4,6,6,4,4,6,4,4,4,4$ | $6$ | $0,0,2,1,2,1,0,1,2,1,2$ |
| $T_{11,1242}$ | $6,6,6,6,4,4,6,4,4,4,4$ | $6$ | $0,0,0,2,1,2,1,1,2,2,1$ |

Counts of all-even graphs by $n = 4, \ldots, 11$: $0,0,1,0,1,1,2,2$.

The list of graphs that have an odd degree and that `three_colour` nevertheless colours is empty. The list of all-even graphs that it fails to colour is empty.

## 4. Result

**Proved.** Lemmas 2 and 3. The cache check is a separate finite confirmation, not the proof.

## 5. Kill criterion

The sufficiency direction would be killed by one simple plane triangulation with all degrees even and no proper $3$-vertex-colouring. The necessity direction would be killed by one simple plane triangulation with an odd degree and a proper $3$-vertex-colouring.

Neither witness appears among the $1555$ cached triangulations. The proof says neither witness exists at any order.

## 6. Not proved

Nothing here is a reformulation of the Four Colour Theorem. The conclusion is three colours, and the hypothesis is that every degree is even. A triangulation with a single odd degree fails to be $3$-colourable by Lemma 2; $K_4$ is the smallest case.

The shift around a face is $\pm 3 \equiv 0 \pmod{3}$ because the face is a triangle. The same orientation on a face of length $\ell$ shifts colour by $\pm \ell$, so the writeup does not $3$-colour an Eulerian plane graph that has a face whose length is not divisible by $3$. No counterexample in that wider class is claimed.

Non-simple drawings, with a loop or a digon, are outside the statement. The cache confirms only $n \le 11$.

## 7. Feasibility

**Medium** for a Lean 4 transcription of Lemmas 1–3 along the combinatorial steps already used by `constructive_colouring`.

**Low** for any attempt to remove the even-degree hypothesis and still conclude three colours.

## 8. Next steps

Keep the lemma as a proved criterion and stop searching the cache for a counterexample.

A Lean transcription can follow `constructive_colouring`: face trace, $2$-colouring of the dual, orientation with black on the left, and the check that each directed edge shifts colour by $1$ in $\mathbb{Z}/3\mathbb{Z}$. The identity $\sigma(C) = 3b - 3w$ is the step that has to be formalised; the finite check does not replace it.

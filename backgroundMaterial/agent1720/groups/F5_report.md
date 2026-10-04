# F5 — Five Colour Theorem

**Group:** F5, manager M-Foundation
**Date:** 2 October 2026
**Status:** proved, as classical prose. This file is not a Lean proof and does not add a Lean declaration.

## 1. Definitions

Graphs here are finite. A graph is *simple* when it has no loop and no two edges with the same ends. It is *planar* when it is isomorphic to a plane graph in the sense of Reinhard Diestel, *Graph Theory*, 6th edition, 2025, Section 4.2: vertices are points of $\mathbb{R}^2$, edges are polygonal arcs, distinct edges have distinct ends, and no interior point of an edge lies on another edge or on a vertex. Faces are the regions of the complement. Diestel's graphs are simple unless a multigraph is named.

For a graph $G$, write $v(G)=|V(G)|$ and $e(G)=|E(G)|$. For $x\in V(G)$, write $\deg_G(x)$ for the number of neighbours of $x$, and write $N_G(x)$ for that neighbour set. Write $G-x$ for the graph obtained by deleting $x$ and every edge incident with $x$.

A map $c:V(G)\to\{1,2,3,4,5\}$ is a *proper $5$-colouring* when for every edge $\{y,z\}\in E(G)$ one has $c(y)\ne c(z)$. For colours $a,b\in\{1,2,3,4,5\}$ and a proper $5$-colouring $c$ of $G$, the *$(a,b)$-subgraph* is the subgraph of $G$ induced by $\{y\in V(G):c(y)\in\{a,b\}\}$. An *$(a,b)$-Kempe component* of a vertex $y$ is the connected component of that subgraph which contains $y$. The *Kempe swap* of that component replaces $c$ by the map $c'$ which exchanges $a$ and $b$ on the component and agrees with $c$ off the component.

The numerical check reads edge lists `graphs[str(n)][i]` in `compute/data/triangulations_n4_11.json`. It does not implement colourings. No function in this repository is a formalization of the proof below.

## 2. Statement

**Proved.** For every finite simple planar graph $G$, there exists a proper $5$-colouring of $G$.

Two lemmas used on the way, also proved below from named citations: for every finite simple planar graph $G$ with $v(G)\ge 3$, one has $e(G)\le 3v(G)-6$; and for every finite simple planar graph $G$, there exists a vertex of degree at most $5$.

## 3. Evidence

The argument is the classical induction. The degree-$5$ step, one Kempe swap, is Heawood's 1890 modification of Kempe's method: P. J. Heawood, *Map-colour theorem*, Quarterly Journal of Pure and Applied Mathematics **24** (1890), 332–338. Diestel records the same attribution in the notes to Chapter 5: Kempe's incorrect argument was modified by Heawood into the first proof of Diestel's Proposition 5.1.2. Euler's formula is older. Diestel, Theorem 4.2.9, states it as Euler (1752). The inequality $e\le 3v-6$ is Diestel's Corollary 4.2.10; its derivation is written out here so that the only unproved inputs are the named theorems below.

**Cited, not re-proved.**

- Diestel, Theorem 4.1.1 (Jordan curve theorem for polygons). For every polygon $P\subset\mathbb{R}^2$, the complement $\mathbb{R}^2\setminus P$ has exactly two regions, and each has frontier $P$. Diestel does not prove the facts in his Section 4.1. He refers those proofs to B. Mohar and C. Thomassen, *Graphs on Surfaces*, Johns Hopkins University Press, 2001, and gives J. Stillwell, *Classical Topology and Combinatorial Group Theory*, Springer, 1980, as an account of the Jordan theorem.
- Diestel, Theorem 4.2.9 (Euler's formula). For every connected plane graph with $n$ vertices, $m$ edges, and $\ell$ faces, $n-m+\ell=2$. The proof in that book is induction on $m$, using his Proposition 4.2.4 and Lemma 4.2.2.
- Diestel, Proposition 4.2.8. A plane graph of order at least $3$ is maximally plane if and only if it is a plane triangulation: every face, including the outer face, is bounded by a triangle.
- Diestel, Lemma 4.2.2(ii). If an edge lies on a cycle, then it lies on the frontier of exactly two faces.

### 3.1. Euler's inequality

**Lemma.** For every finite simple planar graph $G$ with $v(G)\ge 3$,
\[
e(G)\le 3v(G)-6.
\]
For every connected plane triangulation $T$ with $v(T)\ge 3$,
\[
e(T)=3v(T)-6.
\]

**Proof.** The count for triangulations is taken first, and only in the connected case, because Theorem 4.2.9 assumes a connected plane graph. The general inequality is then the sum over components.

Let $T$ be a connected plane triangulation with $n\ge 3$ vertices: every face, including the outer face, is bounded by a triangle. Every edge lies on such a triangle, hence on a cycle. Lemma 4.2.2(ii) puts every edge on the frontier of exactly two faces. Counting edge–face incidences the other way, each of the $f(T)$ faces contributes three edges, so $2e(T)=3f(T)$. Theorem 4.2.9 gives $n-e(T)+f(T)=2$. Substitute $f(T)=2e(T)/3$:
\[
n-e(T)+\frac{2e(T)}{3}=2,
\]
so $e(T)=3n-6$.

Now let $G$ be a connected simple plane graph with $n\ge 3$ vertices. If $G$ is not maximally plane, the definition of that term supplies a plane graph on the same vertex set with one more edge. Repeat. The process stops at a maximally plane graph $T$ on $V(G)$, because a simple graph on $n$ vertices has at most $\binom{n}{2}$ edges. Adding edges keeps $G$ inside $T$, so $T$ is connected. Proposition 4.2.8 says that $T$ is a plane triangulation. The previous paragraph gives $e(T)=3n-6$. Therefore $e(G)\le 3n-6$. If $G$ itself is a connected plane triangulation, the same paragraph gives equality.

Finally let $G$ be a finite simple planar graph with $n=v(G)\ge 3$, possibly disconnected. Apply the connected case to each component, drawn by itself in the plane. Let the components have orders $n_i$ and sizes $e_i$. If $n_i\ge 3$, then $e_i\le 3n_i-6$. If $n_i=2$, simplicity gives $e_i\le 1$. If $n_i=1$, then $e_i=0$. Write $c_1$, $c_2$, and $c_{\ge 3}$ for the numbers of components of those three kinds. Then
\begin{align*}
e(G)
&=\sum_i e_i
\le \sum_{n_i\ge 3}(3n_i-6)+c_2
=3\bigl(n-c_1-2c_2\bigr)-6c_{\ge 3}+c_2\\
&=3n-3c_1-5c_2-6c_{\ge 3}.
\end{align*}
Hence $e(G)\le 3n-6$ as soon as $3c_1+5c_2+6c_{\ge 3}\ge 6$. If $c_{\ge 3}\ge 1$, then $6c_{\ge 3}\ge 6$. If $c_{\ge 3}=0$, then $c_1+2c_2=n\ge 3$. If $c_2=0$, then $c_1=n\ge 3$ and $3c_1\ge 9$. If $c_2=1$, then $c_1=n-2\ge 1$ and $3c_1+5\ge 8$. If $c_2\ge 2$, then $5c_2\ge 10$. In every case $e(G)\le 3n-6$. $\square$

The first sentence of this lemma is the inequality asked for. The equality case is the same counting Diestel records as the second sentence of Corollary 4.2.10.

### 3.2. A vertex of degree at most $5$

**Lemma.** For every finite simple planar graph $G$, there exists a vertex $x\in V(G)$ with $\deg_G(x)\le 5$.

**Proof.** If $v(G)\le 2$, then every degree is at most $1$, hence at most $5$. Suppose $v(G)\ge 3$. Section 3.1 gives $2e(G)\le 6v(G)-12$. The handshaking identity says $\sum_{x\in V(G)}\deg_G(x)=2e(G)$. If every degree were at least $6$, the sum would be at least $6v(G)$, contradicting $2e(G)\le 6v(G)-12$. Therefore some degree is at most $5$. $\square$

This degree bound is the standard corollary of Euler's inequality. Heawood uses it as the inductive opening. It is not the Kempe step.

### 3.3. One Kempe swap stays proper

**Lemma.** Let $G$ be a finite simple graph, let $c$ be a proper $5$-colouring of $G$, let $a,b\in\{1,2,3,4,5\}$ be distinct, and let $K$ be a connected component of the $(a,b)$-subgraph. Let $c'$ be the Kempe swap of $K$. Then $c'$ is a proper $5$-colouring of $G$. For every vertex $y$ outside $K$, $c'(y)=c(y)$. For every vertex $y$ in $K$, $c'(y)\in\{a,b\}\setminus\{c(y)\}$.

**Proof.** The last two sentences are the definition of the swap. Let $\{y,z\}$ be an edge. If both ends lie outside $K$, then $c'(y)=c(y)\ne c(z)=c'(z)$. If both ends lie in $K$, then $\{c(y),c(z)\}=\{a,b\}$ because the colouring is proper and both colours lie in $\{a,b\}$, so after the exchange one still has $c'(y)\ne c'(z)$. If exactly one end, say $y$, lies in $K$, then $c(z)\notin\{a,b\}$: otherwise the edge would lie in the $(a,b)$-subgraph and $z$ would lie in $K$. Thus $c'(z)=c(z)\notin\{a,b\}$ and $c'(y)\in\{a,b\}$, so $c'(y)\ne c'(z)$. $\square$

### 3.4. Extension across a vertex of degree at most $4$

**Lemma.** Let $G$ be a finite simple graph and let $x\in V(G)$ satisfy $\deg_G(x)\le 4$. Suppose $c$ is a proper $5$-colouring of $G-x$. Then there exists a proper $5$-colouring of $G$ which agrees with $c$ on $V(G)\setminus\{x\}$.

**Proof.** The set $c(N_G(x))$ has at most $\deg_G(x)\le 4$ elements. Choose
\[
\alpha\in\{1,2,3,4,5\}\setminus c(N_G(x)).
\]
Extend $c$ by sending $x$ to $\alpha$. Every edge not incident with $x$ was already properly coloured. For every neighbour $y$ of $x$, the colour of $x$ differs from $c(y)$ by the choice of $\alpha$. $\square$

The same one-line extension applies when $\deg_G(x)=5$ and $c(N_G(x))$ has size at most $4$. The remaining case is five distinct colours on five neighbours.

### 3.5. The Five Colour Theorem

**Theorem.** For every finite simple planar graph $G$, there exists a proper $5$-colouring of $G$.

**Proof.** Proceed by induction on $n=v(G)$.

If $n\le 5$, enumerate $V(G)=\{y_1,\ldots,y_n\}$ and set $c(y_i)=i$. Any two colours in the image are distinct, so $c$ is a proper $5$-colouring. Planarity is not used.

Fix $n\ge 6$, and assume that every finite simple planar graph on fewer than $n$ vertices has a proper $5$-colouring. Let $G$ be a finite simple planar graph on $n$ vertices. Section 3.2 supplies a vertex $x$ with $\deg_G(x)\le 5$. The graph $G-x$ is finite, simple, and planar. The inductive hypothesis supplies a proper $5$-colouring $c$ of $G-x$.

If $\deg_G(x)\le 4$, or if $\deg_G(x)=5$ and $|c(N_G(x))|\le 4$, Section 3.4 extends $c$ to $G$.

It remains that $\deg_G(x)=5$ and that the five neighbours receive five distinct colours. Fix a plane embedding of $G$. The five edges incident with $x$ are polygonal arcs meeting only at $x$. Choose an open disc $D$ centred at $x$ small enough that $D$ meets the embedded graph only in $x$ and in one initial straight segment of each of those five edges, and small enough that $D$ is disjoint from every vertex other than $x$ and from every edge not incident with $x$. The five segments meet the boundary circle of a smaller closed disc in five points. Read those points in cyclic order around the circle and label the corresponding neighbours $x_1,x_2,x_3,x_4,x_5$ in that order. The colours $c(x_1),\ldots,c(x_5)$ are all five colours. Compose $c$ with the permutation of $\{1,2,3,4,5\}$ which sends $c(x_i)$ to $i$. The result is still a proper $5$-colouring of $G-x$. Rename it $c$, so that $c(x_i)=i$ for each $i\in\{1,2,3,4,5\}$.

Let $H=G-x$. Let $H_{1,3}$ be the $(1,3)$-subgraph of $H$ under $c$.

**Branch A.** Suppose $x_1$ and $x_3$ lie in different connected components of $H_{1,3}$. Then $x_1$ and $x_3$ are non-adjacent: an edge between them would be an edge of $H_{1,3}$. Let $K$ be the component of $x_1$, and let $c'$ be the Kempe swap of colours $1$ and $3$ on $K$. Section 3.3 says that $c'$ is a proper $5$-colouring of $H$. It agrees with $c$ on $x_2,x_3,x_4,x_5$, and $c'(x_1)=3$. The set of colours on $N_G(x)$ is $\{2,3,4,5\}$. Extend $c'$ by sending $x$ to $1$. The extension is proper, by the same check as in Section 3.4. This branch performs one swap.

**Branch B.** Suppose $x_1$ and $x_3$ lie in the same component of $H_{1,3}$. Let $P$ be an $x_1$–$x_3$ path in $H_{1,3}$. Every vertex of $P$ has colour $1$ or $3$, so neither $x_2$ nor $x_4$ lies on $P$. Let $C$ be the cycle formed by $P$ together with the two edges $xx_1$ and $xx_3$. As a point set, $C$ is a polygon. Theorem 4.1.1 says that $\mathbb{R}^2\setminus C$ has exactly two regions and that $x$, which lies on $C$, is on the frontier of both.

The two segments $xx_1$ and $xx_3$ split $D$ into two connected open pieces. The cyclic order $x_1,x_2,x_3,x_4,x_5$ puts the initial segment of $xx_2$ in one piece and the initial segment of $xx_4$ in the other. Those pieces lie in $\mathbb{R}^2\setminus C$: the disc $D$ meets $C$ only along $xx_1$ and $xx_3$, because $P$ is disjoint from $D$. Each piece lies in a single region. The two pieces do not lie in the same region: if they did, $D$ would meet only one region, contradicting that every neighbourhood of $x$ meets both regions. Therefore an interior point of $xx_2$ and an interior point of $xx_4$ lie in different regions of $\mathbb{R}^2\setminus C$.

The open edge $xx_2$ meets $C$ only at the missing endpoint $x$: its other endpoint $x_2$ is not on $C$, and a plane edge meets $C$ only at a shared vertex. The interior is connected and lies in $\mathbb{R}^2\setminus C$, hence in one region. Since $C$ is closed and $x_2\notin C$, some point $q$ of that interior lies so close to $x_2$ that the segment $x_2q$ misses $C$. Thus $x_2$ lies in the same region as $q$. Likewise $x_4$ lies in the other region.

Now $x_2$ and $x_4$ are non-adjacent and lie in different components of the $(2,4)$-subgraph $H_{2,4}$ of $H$. Indeed, an $x_2$–$x_4$ path $Q$ in $H_{2,4}$ would use only vertices of colours $2$ and $4$. No such vertex lies on $C$: the vertices of $P$ have colours $1$ and $3$, and $x\notin V(H)$. Edges of the embedded graph do not cross, so the point set of $Q$ misses $C$. That point set is connected, hence lies in one region, which is impossible. In particular there is no edge $x_2x_4$.

Let $K$ be the component of $H_{2,4}$ containing $x_2$, and let $c'$ be the Kempe swap of colours $2$ and $4$ on $K$. Section 3.3 says that $c'$ properly $5$-colours $H$. Then $c'(x_2)=4$, while $c'(x_1)=1$, $c'(x_3)=3$, $c'(x_4)=4$, and $c'(x_5)=5$. Colour $2$ does not appear on $N_G(x)$. Extend $c'$ by sending $x$ to $2$. The extension is proper. This branch performs one swap, on the pair of non-adjacent neighbours $x_2$ and $x_4$.

Every graph falls under the base, under Section 3.4, or under exactly one of the two branches. This completes the induction. $\square$

What is classical, in Heawood's 1890 paper, is Branch A together with Branch B: at a degree-$5$ vertex whose neighbours use all five colours, exactly one bichromatic chain is swapped, on a pair of non-adjacent neighbours, and the fifth colour is then free. The degree-at-most-$4$ extension uses no swap. Euler's inequality and the existence of a vertex of degree at most $5$ are the earlier input to that induction.

### 3.6. Numerical check

Read-only. The file `compute/data/triangulations_n4_11.json` was not written.

Command: `/Users/fulkanjou/GraphColour/.venv/bin/python`, loading that JSON and, for every edge list `graphs[str(n)][i]`, testing $|E|=3n-6$ and $\min_{0\le j<n}\deg(j)\le 5$. Wall clock $0.015$ seconds.

The file records plantri counts $1,1,2,5,14,50,233,1249$ for $n=4,\ldots,11$. The lists have those lengths. The total is $1555$. For every one of the $1555$ graphs the vertex set is $\{0,\ldots,n-1\}$, there is no loop and no repeated edge, $|E|=3n-6$, and the minimum degree is at most $5$. Both failure counts are $0$.

This checks the equality case of Section 3.1 and the degree bound of Section 3.2 on the cached triangulations. It does not prove either statement for every $n$.

## 4. Result

**Proved**, by the written induction in Section 3. The degree-$5$ swap is literature in the sense that it is Heawood's argument; the text above is a complete write-out of that argument, not a pointer in place of a proof. The finite triangulation count is **computed** on $n\le 11$.

## 5. Kill criterion

A kill of the Five Colour Theorem would be one finite simple planar graph with no proper $5$-colouring. That criterion was not met. The induction shows that no such graph exists.

The cache check did not look for a counterexample beyond $n=11$, and it did not need to: the proof is not restricted to the cache.

## 6. Not proved

The Four Colour Theorem is not proved. Diestel states it as Theorem 5.1.1 and does not prove it. Nothing here shows that four colours suffice for every planar graph.

Thomassen's theorem that every planar graph is $5$-choosable (Diestel, Theorem 5.4.2) is not proved.

Theorem 4.1.1 and Theorem 4.2.9 are cited from Diestel, with the Jordan theorem traced to Mohar–Thomassen and to Stillwell. They are not derived in this file from the axioms of the plane.

No Lean declaration was added. Searching the Lean tree was not repeated; the proof in this file is prose.

## 7. Feasibility

**Medium-Low** for a Lean proof of the same induction inside this repository. The missing pieces are a plane-embedding library and a formal Euler formula; the Kempe swap itself is the short step once a proper $5$-colouring of $G-x$ is in hand.

**High** for any further finite check of $|E|=3n-6$ and minimum degree at most $5$ on triangulations already stored in the cache. That check is done.

## 8. Next steps

Leave this as prose until a plane graph and Euler's formula exist in the Lean library. Do not describe `F5_report.md` as a Lean proof. Do not overwrite `compute/data/triangulations_n4_11.json`.

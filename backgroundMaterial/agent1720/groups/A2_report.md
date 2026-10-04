# A2 — Positivity of $P(G,k)$ for degenerate graphs

**Group:** A2, manager M-Algebra
**Date:** 2 October 2026
**Status:** The degeneracy bounds below are proved in this file. They give $P(G,4) > 0$ for outerplanar and series-parallel graphs, and $P(G,k) > 0$ for every simple planar graph when the integer $k$ is at least $6$. They do not prove the Four Colour Theorem.

## 1. Definitions

Throughout, graphs are finite and simple. $P(G,k)$ is the chromatic polynomial. For a positive integer $k$ it equals the number of proper colourings of $V(G)$ by $k$ labelled colours. In the A1 database the coefficients are stored in ascending degree: the record `coeffs` of $T_{n,i}$ is the list $(c_0,\ldots,c_n)$ with $P(T_{n,i},k) = \sum_j c_j k^j$. That polynomial was computed by `compute/chromatic/a1720_chromatic_db.py` and stored in `compute/data/chromatic_polys_n4_11.json`. This report only evaluates those stored coefficients. The elimination order used in the spot-check is `elimination` in `compute/chromatic/a1720_a2_degeneracy_check.py`.

**Degeneracy.** A graph $G$ is *$d$-degenerate* if every nonempty subgraph has a vertex of degree at most $d$.

**Outerplanar.** $G$ is outerplanar if it has a plane embedding in which every vertex lies on the outer face. For $n \ge 3$, a *maximal outerplanar* graph is a simple graph embedded so that the outer face is a cycle through all $n$ vertices and every interior face is a triangle.

**Two-terminal series-parallel.** The class of two-terminal series-parallel multigraphs is the smallest class such that:

- the single edge $K_2$, with its endpoints as terminals, belongs to the class;
- the series composition of two members, disjoint except for the identified sink of the first and source of the second, belongs to the class, with the free source and free sink as terminals;
- the parallel composition of two members, with sources identified and sinks identified, belongs to the class, with those two vertices as terminals.

A simple graph is *series-parallel* if it is a subgraph of the underlying simple graph of some two-terminal series-parallel multigraph.

**$2$-tree.** $K_2$ is a $2$-tree. If $H$ is a $2$-tree and $xy$ is an edge of $H$, the graph obtained by adding a new vertex adjacent exactly to $x$ and $y$ is a $2$-tree. A *partial $2$-tree* is a subgraph of a $2$-tree.

**$3$-tree.** $K_4$ is a $3$-tree. If $H$ is a $3$-tree and $xyz$ is a triangle of $H$, the graph obtained by adding a new vertex adjacent exactly to $x$, $y$, and $z$ is a $3$-tree. A *stacked triangulation* is a $3$-tree that remains plane when each new vertex is placed in a facial triangle and joined to its three corners.

**Planar.** A graph is planar when it admits a drawing in the plane with no two edges crossing except at a shared endpoint.

## 2. Statement

The following are proved for every finite simple graph, with the quantifiers written out. Each label records the status used in §4.

**(D) Proved here.** Let $G$ be $d$-degenerate, on $n \ge 1$ vertices, and let $k \ge d$ be an integer. Then
\[
P(G,k) \ge \prod_{i=1}^{n}\bigl(k - \min(d,i-1)\bigr).
\]
If $n \ge d$, the right-hand side equals $k(k-1)\cdots(k-d+1)\,(k-d)^{n-d}$. If $k \ge d+1$, then $P(G,k) > 0$.

**(O) Proved here.** Every outerplanar graph is $2$-degenerate. Every maximal outerplanar graph on $n \ge 3$ vertices is a $2$-tree and satisfies $P(G,k) = k(k-1)(k-2)^{n-2}$ for every integer $k \ge 0$. Consequently every outerplanar graph $G$ satisfies $P(G,4) > 0$.

**(S) Proved here.** Every series-parallel graph is $2$-degenerate, and therefore satisfies $P(G,4) > 0$.

**(P) Proved here.** Every planar graph is $5$-degenerate. For every planar graph $G$ and every integer $k \ge 6$, $P(G,k) > 0$. Every planar graph on at most $11$ vertices is $4$-degenerate, so the same conclusion holds for every integer $k \ge 5$.

**(T) Proved here.** Every $3$-tree on $n \ge 4$ vertices satisfies
\[
P(G,k) = k(k-1)(k-2)(k-3)^{n-3}
\]
for every integer $k \ge 0$. In particular $P(G,4) = 24 > 0$. Every stacked triangulation is a $3$-tree, so the same identity applies.

**(L) Literature only.** The following are not proved in this file. Heawood (1890) proved that every planar graph satisfies $P(G,5) > 0$. The statement that every planar graph satisfies $P(G,4) > 0$ is the Four Colour Theorem.

## 3. Evidence

### (D) The product bound

An ordering $v_1,\ldots,v_n$ of $V(G)$ is a *$d$-elimination ordering* if each $v_i$ has at most $d$ neighbours in $\{v_1,\ldots,v_{i-1}\}$. Write $d_i$ for that number of earlier neighbours.

Such an ordering exists if and only if $G$ is $d$-degenerate. If the ordering exists and $H$ is a nonempty subgraph, let $v$ be the vertex of $H$ of largest index. Every neighbour of $v$ in $H$ is earlier than $v$ in the ordering, so $\deg_H(v) \le d_i \le d$. Conversely, if $G$ is $d$-degenerate, delete $u_1,u_2,\ldots$ in turn, each of degree at most $d$ in the subgraph still remaining. Then $u_i$ has at most $d$ neighbours among $u_{i+1},\ldots,u_n$. The reversed sequence $v_i = u_{n+1-i}$ is a $d$-elimination ordering.

Now let $k \ge d$ be an integer. Colour the vertices in the order $v_1,\ldots,v_n$. Fix any proper colouring of $v_1,\ldots,v_{i-1}$. At most $d_i$ colours appear on the earlier neighbours of $v_i$, so at least $k-d_i$ colours remain for $v_i$. Every proper $k$-colouring arises exactly once in this recursion, and therefore
\[
P(G,k) \ge \prod_{i=1}^{n} (k-d_i).
\]
Since $0 \le d_i \le \min(d,i-1)$ and $k-d_i \ge k-\min(d,i-1) \ge 0$,
\[
\prod_{i=1}^{n} (k-d_i) \ge \prod_{i=1}^{n}\bigl(k-\min(d,i-1)\bigr).
\]
For the closed form, the factors for $i = 1,\ldots,d$ are $k,k-1,\ldots,k-d+1$, and each of the remaining $n-d$ factors, when $n \ge d$, equals $k-d$.

If $k \ge d+1$, then $k-d \ge 1$, so every factor $k-\min(d,i-1)$ is a positive integer. The product is a positive integer, and $P(G,k) > 0$.

The bound is sharp: $K_{d+1}$ is $d$-degenerate and $P(K_{d+1},d+1) = (d+1)!$, which equals the product.

### (O) Outerplanar graphs

Let $M$ be maximal outerplanar on $n \ge 3$ vertices, with outer cycle $C$ and every interior face a triangle. Euler's formula for the connected plane graph gives $n-e+f = 2$. The outer face has length $n$ and the other $f-1$ faces have length $3$, so $2e = 3(f-1)+n$. Substituting $f = e-n+2$ yields $e = 2n-3$ and $f-1 = n-2$. Exactly $n-3$ edges are chords of $C$. Each chord is shared by two interior faces, and no outer edge is. The weak dual $T$, with one vertex per interior face and an edge whenever two interior faces share a chord, therefore has $n-2$ vertices and $n-3$ edges.

$T$ is connected. The triangles of any component fill a subpolygon of $C$. If that subpolygon were proper, some boundary edge would be a chord of $C$, and the triangle on the other side of that chord would be a dual neighbour outside the component. Hence there is one component, and $T$ is a tree.

If $n = 3$, then $M \cong K_3$ and every degree is $2$. If $n \ge 4$, the tree has at least two leaves. A leaf triangle has one chord and two edges on $C$. Those two outer edges meet at a vertex $v$, and they are consecutive on the outer face, so the rotation at $v$ consists of exactly those two edges. Thus $\deg(v) = 2$. Distinct leaves give distinct apices, because each such apex lies on exactly one interior triangle. So $M$ has at least two vertices of degree $2$.

Deleting one of them leaves a maximal outerplanar graph on $n-1$ vertices: the two neighbours were joined by the leaf's chord, and that chord replaces the two outer edges on the new outer cycle. By induction on $n$, starting from $K_3$, the graph $M$ is obtained from $K_2$ by repeatedly adding a vertex of degree $2$ on an existing edge. Thus $M$ is a $2$-tree.

The same induction gives the polynomial. $P(K_2,k) = k(k-1)$. When a vertex is added adjacent to both ends of an edge, those two neighbours have different colours in every proper colouring, so the new vertex has exactly $k-2$ admissible colours. After $n-2$ additions,
\[
P(M,k) = k(k-1)(k-2)^{n-2}.
\]
For $n = 3$ this is the usual $P(K_3,k)$. In particular $P(M,4) = 4\cdot 3\cdot 2^{n-2} > 0$.

It remains to put an arbitrary outerplanar graph inside some maximal one. The cases $n \le 2$ are subgraphs of $K_3$. Let $G$ be simple outerplanar on $n \ge 3$ vertices, embedded in a disk with every vertex on the boundary. Add edges in three stages, each edge drawn inside one face.

First, while $G$ is disconnected, some face is incident with two components. Add an edge of that face joining the two components. The endpoints were nonadjacent, the drawing stays plane, and every vertex remains on the outer face. The graph becomes connected.

Second, while the outer boundary walk repeats a vertex $x$, that vertex has two consecutive outer edges $xu$ and $xv$ with the outer face in the angle $uxv$. The edge $uv$ is absent: if it were present, the triangle $xuv$ would have this angle as its interior, the outer walk would follow $uv$, and this visit to $x$ would not occur. Draw $uv$ in the angle. The vertex $x$ remains on the outer face because the walk visited $x$ more than once, and no other vertex leaves the outer face. At the end of this stage the outer boundary is a cycle through every vertex. A cut vertex on the outer face would be visited twice by that walk, so the graph is $2$-connected. In a $2$-connected plane graph every facial walk is a cycle.

Third, while some interior face has length at least $4$, its interior is empty and its boundary is a cycle. Some chord of that cycle is missing. On a $4$-cycle the two diagonals cross, so they cannot both already be drawn outside the face. On a cycle of length at least $5$, the vertices cannot already be pairwise adjacent, because that subgraph would be a clique of order at least $5$. Draw a missing chord inside the face. Every vertex remains on the outer face.

Each step adds an edge. The result is maximal outerplanar, and the starting graph is a spanning subgraph of it, hence a subgraph of a $2$-tree.

Every subgraph of a $d$-degenerate graph is $d$-degenerate: a subgraph of a subgraph is a subgraph of the original graph. A $2$-tree has a $2$-elimination ordering by construction, so it is $2$-degenerate, and so is every outerplanar graph. Part (D) with $d = 2$ and $k = 4$ gives, for $n \ge 2$,
\[
P(G,4) \ge 4\cdot 3\cdot 2^{n-2} > 0,
\]
and $P(G,4) = 4$ when $n = 1$.

### (S) Series-parallel graphs

Let $(G,s,t)$ be a two-terminal series-parallel multigraph and let $H$ be its underlying simple graph. The claim is that the vertices other than $s$ and $t$ can be deleted in some order so that each deleted vertex has degree at most $2$ in the subgraph induced by the vertices still present, including $s$ and $t$.

The single edge has no other vertices. In a parallel composition, the internal vertices of the two sides are disjoint. Concatenate the two deletion orders given by induction. A vertex on one side has no neighbour on the other side except possibly through $s$ and $t$, which remain present, so its degree in the whole remaining graph equals its degree in its own side and is at most $2$. In a series composition, write $m$ for the identified vertex. Delete the internal vertices of the first factor relative to terminals $s,m$, then the internal vertices of the second factor relative to terminals $m,t$, and then delete $m$. The same degree count applies to the internal vertices. After they are gone, every remaining neighbour of $m$ lies in $\{s,t\}$, so $m$ has degree at most $2$.

Deleting $s$ and $t$ last removes two vertices of degree at most $1$. Thus $H$ has a $2$-elimination ordering and is $2$-degenerate. Every subgraph of $H$ is $2$-degenerate, which is the definition of a series-parallel simple graph used here. Part (D) gives $P(G,4) > 0$.

Duffin, *Topology of series-parallel networks*, J. Math. Anal. Appl. 10 (1965) 303–318, proved that a two-terminal graph arises by series and parallel composition from single edges if and only if it has no minor isomorphic to $K_4$. That characterisation is not used above.

### (P) Planar graphs

**Edge bound.** Let $G$ be a simple connected plane graph with $n \ge 3$. Every facial walk has length at least $3$. A walk of length $1$ is a loop. A walk of length $2$ is either a digon or a single edge traversed twice and forming the whole boundary; the latter forces $G \cong K_2$. Both are excluded. Hence $2e \ge 3f$. Euler's formula $n-e+f = 2$ then gives $e \le 3n-6$.

If $G$ is simple and planar but disconnected, with $n \ge 3$, add edges through faces until the graph is connected. Each added edge joins distinct components, so it is new, and the drawing stays plane. The connected simple supergraph has at most $3n-6$ edges, and $G$ has no more edges than that supergraph.

**Five-degeneracy.** Let $G$ be simple and planar, and let $H$ be a nonempty subgraph. Then $H$ is simple and planar. If $H$ has at most two vertices, some vertex has degree at most $1$. If $H$ has $m \ge 3$ vertices, then $e(H) \le 3m-6$, so $\sum_v \deg(v) \le 6m-12$ and some vertex has degree at most $5$. Thus $G$ is $5$-degenerate. Part (D) with $d = 5$ gives $P(G,k) > 0$ for every integer $k \ge 6$. For $n \ge 5$ the explicit bound is
\[
P(G,k) \ge k(k-1)(k-2)(k-3)(k-4)(k-5)^{n-5}.
\]

**At most eleven vertices.** Let $H$ be simple and planar with $m \le 11$ vertices. If $m \le 2$, then $\delta(H) \le 1$. If $3 \le m \le 11$ and $\delta(H) \ge 5$, the edge bound would give $5m \le 2e \le 6m-12$, hence $m \ge 12$. So $\delta(H) \le 4$. Every subgraph of a simple planar graph on at most $11$ vertices is itself such a graph, and therefore every simple planar graph on at most $11$ vertices is $4$-degenerate. Part (D) gives $P(G,k) > 0$ for every integer $k \ge 5$.

### (T) Three-trees

Proceed by induction on $n$. For $n = 4$, $G \cong K_4$ and $P(K_4,k) = k(k-1)(k-2)(k-3)$.

Suppose $G$ is obtained from a $3$-tree $G'$ by adding a vertex $v$ adjacent to a triangle $xyz$. In every proper colouring of $G'$ the vertices $x,y,z$ receive three distinct colours, so $v$ has exactly $k-3$ admissible colours. Thus $P(G,k) = (k-3)\,P(G',k)$. The inductive hypothesis gives
\[
P(G,k) = k(k-1)(k-2)(k-3)^{n-3}.
\]
At $k = 4$ every factor after $k(k-1)(k-2)$ equals $1$, so $P(G,4) = 24$. There are $4!$ proper $4$-colourings, so the partition into colour classes is unique up to permuting the four colours.

A stacked triangulation is a $3$-tree, so the identity applies to it. The last vertex added to a $3$-tree on $n > 4$ vertices has degree $3$.

### Spot-check against one stored polynomial

Command, from the repository root:

```text
/Users/fulkanjou/GraphColour/.venv/bin/python compute/chromatic/a1720_a2_degeneracy_check.py
```

Wall clock reported by the script: $0.0129$ seconds. The script reads `graphs["6"][1]` in `compute/data/triangulations_n4_11.json` and the matching record in `compute/data/chromatic_polys_n4_11.json`. It does not rebuild a chromatic polynomial.

The record is $T_{6,1}$. Its degree sequence is $(4,4,4,4,4,4)$, so it is the octahedral graph. The script's elimination order has back-degrees
\[
0,1,2,2,3,4.
\]
The maximum is $4$, so the degeneracy is exactly $4$: the graph is $4$-degenerate, and it is not $3$-degenerate. Evaluating the stored coefficients gives

| $k$ | $P(T_{6,1},k)$ | $\prod(k-d_i)$ | worst case for $d=4$ |
|---|---|---|---|
| $4$ | $96$ | $0$ | $0$ |
| $5$ | $780$ | $360$ | $120$ |
| $6$ | $4080$ | $2880$ | $1440$ |

In each row the stored value is at least the product along this elimination order, and that product is at least the closed bound of (D). The same script compares stored coefficients with the expanded $3$-tree formula. The records $T_{4,0}$, $T_{5,0}$, and $T_{6,0}$ match $k(k-1)(k-2)(k-3)^{n-3}$ and each has $P(G,4) = 24$. The octahedron does not: its minimum degree is $4$, so it is not a $3$-tree, and $P(T_{6,1},4) = 96$.

## 4. Result

| Statement | Status |
|---|---|
| (D) Product bound for $d$-degenerate graphs | Proved here |
| (O) Outerplanar graphs are $2$-degenerate; maximal ones have $P = k(k-1)(k-2)^{n-2}$; $P(G,4) > 0$ | Proved here |
| (S) Series-parallel graphs, in the composition-and-subgraphs sense, are $2$-degenerate; $P(G,4) > 0$ | Proved here |
| Equivalence of that class with the absence of a $K_4$ minor | Literature only: Duffin 1965 |
| (P) Planar graphs are $5$-degenerate; $P(G,k) > 0$ for integers $k \ge 6$ | Proved here |
| Planar graphs on at most $11$ vertices are $4$-degenerate; $P(G,k) > 0$ for integers $k \ge 5$ | Proved here |
| (T) $3$-trees, including stacked triangulations, satisfy $P(G,4) = 24$ | Proved here |
| Every planar graph satisfies $P(G,5) > 0$ | Literature only: Heawood, *Map-colour theorem*, Quart. J. Pure Appl. Math. 24 (1890) 332–338 |
| Every planar graph satisfies $P(G,4) > 0$ | Literature only, and not proved here. This is the Four Colour Theorem: Appel and Haken, Illinois J. Math. 21 (1977) 429–490; Robertson, Sanders, Seymour, and Thomas, J. Combin. Theory Ser. B 70 (1997) 2–44 |

The spot-check is a finite verification of (D) on $T_{6,1}$, together with the equality case of (T) on $T_{4,0}$, $T_{5,0}$, and $T_{6,0}$.

## 5. Kill criterion

For (D), (O), (S), (P), and (T), a kill would be a graph in the stated class and an integer $k$ at least one more than the stated degeneracy with $P(G,k) = 0$. No such example exists: the proofs show the product is positive.

A kill of the *method*, as a route to $P(G,4) > 0$ for every planar graph, is a planar graph whose degeneracy is at least $4$. Then every elimination ordering has some back-degree at least $4$, and the product bound at $k = 4$ is $0$. That criterion is met by $T_{6,1}$: degeneracy $4$, stored value $P(T_{6,1},4) = 96 > 0$, product bound $0$. The method does not prove positivity at $4$ for this graph. The positivity statement itself is not killed.

## 6. Not proved

This file does not prove $P(G,4) > 0$ for every planar graph. That statement is the Four Colour Theorem.

This file does not prove $P(G,5) > 0$ for every planar graph. Heawood's five-colour theorem is cited above and is not re-proved. Five-degeneracy stops at $k = 6$. The separate $11$-vertex argument stops at $k = 5$ and only for graphs of order at most $11$.

Duffin's minor characterisation is not re-proved. The series-parallel argument uses the composition definition.

## 7. Feasibility

**Low** for any attempt to reach $k = 4$ for every planar graph by a degeneracy bound. The obstruction is already the octahedron on six vertices.

**High** for writing out Heawood's five-colour argument as a later note. That argument still does not reach $k = 4$.

## 8. Next steps

The degeneracy route to the Four Colour Theorem stops here. The spot-check against $T_{6,1}$ is the concrete obstruction, and it has been run.

A later write-up may record Heawood's proof that $P(G,5) > 0$ for every planar graph. It should be marked as a restricted five-colour theorem. It is not a substitute for $P(G,4) > 0$.

Keep the $3$-tree identity as a finished restricted four-colour theorem: $P(G,4) = 24$ for every stacked triangulation. Extending that count from stacked triangulations to every planar triangulation is again the Four Colour Theorem.

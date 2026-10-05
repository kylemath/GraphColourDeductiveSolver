# Connectivity

Interface team, Connectivity. 2026-10-05. Standing aim, line 1 of `VHExistsAttack.md`: aim at VH∃. This note is the converse asked for in `VHExistsMinimalCounterexample.md`, section "Must it be 4-connected, or stronger?": every 3-vertex cut of a spherical triangulation is a separating triangle. The link facts used below are the content of Lemma 1.1 in `longtable/swarm/vh-exists.md`; the steps are written here.

Labels: **[hand]** every step of that sentence is in this note; **[cited]** a named fact, not used in (A), (B), or the equivalence; **[open]** unanswered; **[lead]** a next sentence.

## Definitions

A **spherical triangulation** is a simple graph $T$ on $n\ge 4$ vertices, embedded as a cell decomposition of the sphere in which every face, including the outer face of any plane drawing, is an open disk bounded by a 3-cycle, every edge lies on exactly two faces, and the faces incident with a vertex form a single cycle in the rotation at that vertex. Face interiors contain no vertices or edges. This is the meaning, in this note, of a simple maximal planar graph with every face a triangle.

The **link** of a vertex $v$, written $C_v$, is the cyclic sequence of its neighbours in rotation order. A **vertex cut** is a set $S\subset V(T)$ such that $T-S$ is disconnected. A disconnected graph has at least two components, each nonempty, so the deletion of $S$ leaves at least two vertices and $n\ge |S|+2$.

$T$ is **$k$-connected** when $|V(T)|>k$ and $T-X$ is connected for every $X\subset V(T)$ with $|X|<k$. Thus $T$ is 4-connected when $n\ge 5$ and $T$ has no vertex cut of size at most 3.

A set $F$ of three vertices is a **separating triangle** when the induced subgraph $T[F]$ is a triangle and $T-F$ is disconnected. Equivalently, $T=A\cup B$ with $A\cap B=F$, both $A\setminus F$ and $B\setminus F$ nonempty, and with no edge from $A\setminus F$ to $B\setminus F$.

## The link, and 3-connectedness

**[hand]** Every vertex $v$ has degree at least 3.

The rotation at $v$ lists $\deg(v)$ incident edges. Consecutive edges in that rotation bound a face, and that face is a triangle, so the two outer ends are adjacent.

If $\deg(v)=0$, then $v$ lies on no edge and on the boundary of no face, contradicting the cell decomposition. If $\deg(v)=1$, the unique edge lies on no triangular corner at $v$, because a corner uses two edges. If $\deg(v)=2$, with neighbours $x$ and $y$, the rotation has two corners, so $v$ lies on two faces. Each of those faces uses both edges at $v$, hence both faces are the triangle $vxy$, and $xy$ is an edge. Those two closed disks meet along the triangle and cover every side of each of its edges, so their union is the sphere. No other vertex can sit in a face. Thus $n=3$, contradicting $n\ge 4$.

So $\deg(v)\ge 3$. Simplicity gives $\deg(v)$ distinct neighbours. Consecutive neighbours are adjacent. Therefore $C_v$ is a cycle of length $\deg(v)$ in $T-v$, and the faces at $v$ are exactly the triangles $v\,x_j\,x_{j+1}$. Their union, the closed star of $v$, is a closed disk with boundary $C_v$. An edge with both ends on $C_v$, and with those ends non-consecutive on $C_v$, is neither a spoke nor a boundary edge of this disk. Its interior is not in a face interior of the star, so it lies outside the closed star.

**[hand]** $T$ is connected. Form the dual graph with one vertex per face and one dual edge whenever two faces share an edge of $T$. Let $U$ be a dual component, and let $K$ be the union of the closures of the faces in $U$. The set $K$ is closed. It is open. An interior point of a face in $U$ has a neighbourhood in that face. An edge of a face in $U$ has its other face in $U$ as well, because a dual edge joins those two faces and $U$ is a dual component; a neighbourhood of an interior point of the edge is covered by the two closed faces. If a vertex is incident with one face in $U$, every face of its star is in $U$: consecutive faces of the star share a spoke, so a dual path runs around the link. The star is then a neighbourhood of the vertex inside $K$. Thus $K$ is open and closed. It is nonempty, and if $U$ omitted a face the interior of that face would miss $K$. The sphere is connected, so the dual has one component. Every vertex of $T$ lies on a face. The union of two closed triangles that share an edge is connected, and along a dual path the union of the corresponding closed faces is connected. Hence $T$ is connected.

**[hand]** For every vertex $v$, the graph $T-v$ is connected. Let $x$ and $y$ be vertices distinct from $v$, and let $P$ be an $x$–$y$ path in $T$. If $P$ contains $v$, it contains $v$ once, entering along an edge $pv$ and leaving along $vq$ with $p,q\in N(v)$ and $p\ne q$. Replace $pvq$ by a $p$–$q$ path along the cycle $C_v$. The result is an $x$–$y$ walk in $T-v$.

**[hand]** $T$ has no vertex cut of size 2. Suppose $S=\{x,y\}$ and $T-S$ is disconnected, with components whose vertex sets include $C_1$ and $C_2$, both nonempty.

The vertex $x$ has a neighbour in $C_1$. If it had none, every edge leaving $C_1$ would end in $\{y\}$, because no edge runs from $C_1$ to another component of $T-S$. Then in $T-y$ no edge would leave $C_1$. The set $C_2$ supplies a vertex of $T-y$ outside $C_1$, so $T-y$ would be disconnected, contradicting the previous paragraph. The same holds for $x$ against $C_2$, and for $y$ against each of $C_1$ and $C_2$.

Let the link of $x$ be $z_0,\ldots,z_{d-1}$ in rotation order, $d=\deg(x)\ge 3$. Each $z_j$ lies in $\{y\}\cup C_1\cup C_2\cup\cdots$. If $z_j$ and $z_{j+1}$ lay in different components of $T-S$, the face $x\,z_j\,z_{j+1}$ would contain the edge $z_j z_{j+1}$, joining those components. Therefore a change of component along the link can occur only at a neighbour equal to $y$. The vertex $y$ occurs at most once on the link. Deleting that occurrence, if it exists, leaves a single consecutive block of the remaining neighbours: a path if $y$ is present, and the whole cycle if $y$ is absent. Every vertex of that block lies in one component. Every component meets $N(x)$, and the neighbour witnessing the meeting lies in the block, so only one component meets $N(x)$. This contradicts the existence of two such components.

Hence no 2-vertex cut exists. Combined with the absence of a cutvertex, $n>3$, and the deletion of any set of size at most 2 leaves a connected graph, $T$ is 3-connected.

## (A) A separating triangle is a 3-vertex cut

**[hand]** Let $F$ be a separating triangle. By the definition above, $T-F$ is disconnected, so $F$ is a vertex cut of size 3. The graph $T-F$ has at least two vertices, so $n\ge 5$. Then $|V(T)|>4$ and a set of size $3<4$ disconnects $T$, so $T$ is not 4-connected.

**[cited]** (`VHExistsMinimalCounterexample.md`, the order-31 chain.) $H_2$ has a separating triangle and satisfies VH∃. By (A) it is not 4-connected. That sentence is not used in (B).

## (B) A 3-vertex cut induces a non-facial triangle

The statement is the following. Let $S$ be a 3-vertex cut of a spherical triangulation $T$. Then the induced subgraph $T[S]$ is a triangle, $T-S$ has exactly two components, and that triangle bounds no face. In the language of the definition, $S$ is a separating triangle: both sides of the cut are nonempty, and the triangle is non-facial.

**[hand]** Write $S=\{a,b,c\}$. Since $T$ is 3-connected, no proper subset of $S$ is a vertex cut, and $T-S$ is disconnected. Let $C_1,\ldots,C_r$ be the vertex sets of the components of $T-S$, with $r\ge 2$.

Each vertex of $S$ has a neighbour in each $C_i$. If $a$ had no neighbour in $C_1$, every edge leaving $C_1$ would end in $\{b,c\}$. Then $T-\{b,c\}$ would have no edge out of $C_1$, while $C_2$ would supply a vertex outside $C_1$, so $\{b,c\}$ would be a 2-vertex cut. The same holds for the other pairs.

Consider the link of $a$. Its vertices lie in $\{b,c\}\cup C_1\cup\cdots\cup C_r$. Consecutive vertices of the link are adjacent, by the face between them. An edge joining two components of $T-S$ does not exist. Therefore, along the link, the component can change only when the neighbour lies in $\{b,c\}$.

Each of $b$ and $c$ occurs at most once on the link. Those occurrences are the only separators between component-blocks.

If fewer than two of $\{b,c\}$ lie on the link, deleting those occurrences leaves a single consecutive block. Every component-neighbour of $a$ lies in that block, hence in a single component. But every component meets $N(a)$ and there are at least two components, a contradiction.

So $b$ and $c$ both lie on the link: $ab$ and $ac$ are edges. Two distinct points on a cycle determine two arcs. If one arc contained no further vertex, $b$ and $c$ would be consecutive and only one arc would remain to hold component-neighbours, again a single component. Both arcs are therefore nonempty, and $b$ and $c$ are not consecutive on the link of $a$.

Each of those two arcs is a consecutive block of component-neighbours, so each arc lies in a single component. If both arcs lay in the same component, $N(a)$ would meet only that component. They lie in different components. Every component meets $N(a)$, and the only places it can do so are these two arcs, so $r=2$. Name the components so that one arc is $N(a)\cap C_1$ and the other is $N(a)\cap C_2$.

The same count at $b$, with the other two vertices of $S$ as the only available separators, shows that $a$ and $c$ are neighbours of $b$. Thus $bc$ is an edge. The induced subgraph $T[S]$ is a triangle.

That triangle bounds no face. The faces incident with $a$ are the triangles on consecutive link neighbours. Since $b$ and $c$ are not consecutive at $a$, the triple $a,b,c$ is not the vertex set of a face at $a$. A face bounded by the cycle $abc$ would be incident with $a$. Hence the cycle bounds no face.

Both of $C_1$ and $C_2$ are nonempty. Let $A=T[C_1\cup S]$ and $B=T[C_2\cup S]$. Then $T=A\cup B$, the intersection $A\cap B$ is the triangle on $S$, and no edge runs from $C_1$ to $C_2$. This is the separating decomposition.

**[hand]** Each arc contributes at least one neighbour, and the two triangle edges are counted in both sides, so for $f\in S$,
\[
\deg_A(f)\ge 3,\qquad \deg_B(f)\ge 3,\qquad \deg_T(f)=\deg_A(f)+\deg_B(f)-2\ge 4.
\]
In particular $f$ has a neighbour in $C_1$ and a neighbour in $C_2$, and $N_A(f)\subsetneq N_T(f)$.

**[hand]** The same count shows that a facial triangle is not a vertex cut. Suppose $abc$ bounds a face and $T-\{a,b,c\}$ is disconnected. Then $b$ and $c$ are consecutive in the link of $a$, so one arc between them is empty. The earlier count then puts every component-neighbour of $a$ on the remaining arc, and $a$ meets only one component, contradicting that every vertex of a 3-vertex cut meets every component.

**[cited]** (Jordan curve theorem, the form used in the proof of Lemma 1.1 in `vh-exists.md`.) Conversely, a 3-cycle that bounds no face is a separating triangle. If $abc$ bounds no face, then $b$ and $c$ are non-consecutive on the link of $a$, so both link arcs from $b$ to $c$ contain a neighbour of $a$. The cycle $abc$ separates the sphere into two open disks; the two wedges at $a$ determined by the edges $ab$ and $ac$ lie in different disks; each wedge contains one of those neighbours. An edge of $T$ meets the cycle only at a shared endpoint, so the two neighbours lie in different components of $T-\{a,b,c\}$. The feasibility statement below does not use this direction. Parts (A) and (B) already match the cut definition used on the minimal-counterexample page, and (B) includes that the triangle bounds no face.

## The same property

**[hand]** Let $T$ be a spherical triangulation of order $n\ge 5$. The following are equivalent.

1. $T$ has a separating triangle.
2. $T$ has a vertex cut of size 3.
3. $T$ is not 4-connected.

(1) implies (2) by (A), and then $n\ge 5$ gives (3). (3) implies (2) because $T$ is 3-connected and $n>4$, so some set of at most three vertices disconnects $T$, and that set has size exactly 3. (2) implies (1) by (B): the cut induces a triangle, both sides are nonempty, and the triangle bounds no face.

**[hand]** Order 4 is the remaining case, and the two properties diverge there. Degree at least 3 on four vertices forces every vertex to be adjacent to the other three, so $T$ is $K_4$. Deleting any three vertices leaves a single vertex, which is connected, so $K_4$ has no 3-vertex cut and no separating triangle. It is not 4-connected, because 4-connectivity requires more than four vertices. Every vertex of $K_4$ has degree 3, so this order lies outside the minimum-degree-5 class of VH∃.

## (C) Internally 6-connected

**Definition used here.** A spherical triangulation is **internally 6-connected** when every vertex cut of size at most 5 is the set of neighbours of a single vertex. The argument below stays with this sentence. For minimum degree at least 5 it matches the polyhedral form "5-connected, and every 5-vertex cut isolates a vertex", and the match is written out.

**[hand]** The complement of a spanning tree is path-connected. Let $R$ be a spanning tree of $T$ and induct on $n$. If $n=1$, the complement of a point is path-connected. If $n\ge 2$, let $\ell$ be a leaf, let $\alpha$ be the edge from $\ell$ to its neighbour $p$, and let $R'=R-\ell$. By induction, $U'=S^2\setminus R'$ is path-connected. Let $D$ be a closed disk that contains $\alpha$, has $\ell$ in its interior and $p$ on its boundary, and meets $R'$ only at $p$. Choose coordinates on $D$ that straighten $\alpha$ to a radius from $p$ to $\ell$. The polar angle about $\ell$ on $D\setminus\alpha$ then runs through an open interval of length $2\pi$, so $D\setminus\alpha$ is path-connected. Now take $x,y\in S^2\setminus R$. They lie in $U'\setminus\alpha$. Join them by a path in $U'$. On each maximal subpath that lies in $D$, the endpoints lie in $D\setminus\alpha$ (the path never meets $p$, and $\alpha$ meets the boundary of $D$ only at $p$). Replace that subpath by a path in $D\setminus\alpha$ with the same endpoints. The result joins $x$ to $y$ in $S^2\setminus R$. Thus the embedded tree has one face. It has $n-1$ edges, and $n-(n-1)+1=2$.

**[cited]** (Jordan curve theorem.) Restore the remaining edges of $T$ one at a time, each along its curve in the embedding. The interior of such an edge is connected and disjoint from the current subgraph, so it lies in one face, and both ends lie on the boundary of that face. The new arc splits that face into two, and every other face stays as it was. Each restoration raises the edge count by 1 and the face count by 1, so $n-|E|+f$ stays equal to 2. Parts (A) and (B), and the equivalence above, do not use this sentence.

**[hand]** Each face contributes three edge-ends and each edge lies on two faces, so $2|E|=3f$. From this identity and the cited count $n-|E|+f=2$,
\[
|E|=3n-6,\qquad \sum_v\deg(v)=6n-12,
\]
so
\[
\sum_v\bigl(6-\deg(v)\bigr)=12.
\]
If every degree is at least 5, the summand $6-\deg(v)$ equals $1$ at a degree-5 vertex, equals $0$ at a degree-6 vertex, and equals $-(\deg(v)-6)$ at a vertex of degree at least 7. Hence
\[
n_5=12+\sum_{k\ge 7}(k-6)\,n_k\ge 12.
\]
A minimum-degree-5 triangulation therefore has a vertex $v$ of degree 5, and has order at least 12.

**[hand]** The set $N(v)$ is a vertex cut of size 5. The order is at least 12, so some vertex $w$ lies outside $\{v\}\cup N(v)$. In $T-N(v)$ the vertex $v$ has no neighbour left, so $\{v\}$ is a component, distinct from the component containing $w$. A graph is 6-connected only when it has more than six vertices and no vertex cut of size less than 6. Thus a minimum-degree-5 triangulation is never 6-connected.

**[hand]** Under minimum degree at least 5, the definition above is equivalent to: $T$ is 5-connected, and every vertex cut of size 5 isolates a vertex.

Suppose every vertex cut of size at most 5 is the neighbour set of one vertex. A cut of size $k\le 4$ would be $N(u)$ for some $u$, hence $\deg(u)=k\le 4$, which minimum degree 5 forbids. There is therefore no vertex cut of size at most 4. The order is at least 12, so $T$ is 5-connected. A cut $S$ of size 5 equals $N(v)$ for some $v$. Then $v\notin S$ and $\{v\}$ is a component of $T-S$.

Conversely, suppose $T$ is 5-connected and every 5-vertex cut isolates a vertex. A vertex cut of size at most 4 cannot occur. If $|S|=5$ and $\{v\}$ is a component of $T-S$, then $N(v)\subseteq S$. Minimum degree 5 and $|S|=5$ force $N(v)=S$.

A degree-5 neighbourhood is permitted by this definition: it is a 5-vertex cut, and it is the neighbour set of that vertex. Internal 6-connectivity is the form that still makes sense after ordinary 6-connectivity has been excluded.

**[open]** Whether VH∃ for internally 6-connected minimum-degree-5 triangulations implies VH∃ for every minimum-degree-5 triangulation. No deduction written on these pages gives that implication.

A triangulation falls outside the definition when it has a vertex cut of size 3, a vertex cut of size 4, or a vertex cut of size 5 that is not the neighbour set of one vertex. Parts (A) and (B) identify every cut of size 3 with a separating triangle. The interior-witness lift across such a triangle still has the two gaps on `VHExistsMinimalCounterexample.md`: a hole on the triangle, and a side whose completed triangulation meets the interface in a vertex of degree 3 or 4. Those gaps are **[open]**. With those gaps filled, a cut of size 4 would remain. Nothing on the cited pages reduces VH∃ across a cut of size 4. The missing cut size is 4. A cut of size 5 that is not a neighbourhood is a further case with no reduction sentence.

**[open]** Whether a smallest failure is 4-connected, 5-connected, or internally 6-connected. The equivalence above turns the 4-connected question into the separating-triangle question already open on the minimal-counterexample page. It does not answer it.

**[cited]** (`VHExistsMinimalCounterexample.md`.) $H_2$ satisfies VH∃ and has a separating triangle. By (A), $H_2$ is not 4-connected.

## (D) The cut as a composition

**[hand]** This is assume-guarantee composition across a cutset: the guarantee is an interior filling path that never places the hole on the cut, and the assumption on the other side is only a colouring of the cut, not a filling path.

Let $F=S$ be a separating triangle, with sides $A$ and $B$ as in (B), and let $(h,c)$ be a state: $c$ is a proper 4-colouring of $T-h$. The fill postcondition in a graph $G$ at the hole $h$ is $|c(N_G(h))|\le 3$.

If $h\in A\setminus F$, there is no edge from $h$ to $B\setminus F$, so $N_T(h)=N_A(h)$. The side's postcondition and the caller's postcondition quantify over the same set.

If the hole is allowed onto the cut, take $h\in F$. By (B), $h$ has a neighbour in $B\setminus F$, so $N_A(h)\subsetneq N_T(h)$. The guarantee's postcondition "$3$-colour link" quantifies over $N_A(h)$. The caller's postcondition quantifies over $N_T(h)$. The caller sees the extra neighbours, so the side's bound is a different demand from membership of $(h,c)$ in the fill set of $T$. The data available from the far side, in the composition above, are colours of cut vertices, not a filling path that would recolour those extra neighbours.

The same proper colourings can be written on the triangular bipyramid, which is a spherical triangulation of order 5: equator $abc$, poles $N$ and $S$, and the nine edges from the two cones. The equator is a separating triangle. Take the side $A$ induced by $\{a,b,c,N\}$, so $N_A(a)=\{b,c,N\}$ and $N_T(a)=\{b,c,N,S\}$.

- Colour $b,c,N,S$ by $0,1,2,3$. Every edge of $T-a$ runs between different colours. The side's link uses three colours and the caller's link uses four.
- Colour $b,c,N,S$ by $0,1,2,2$. There is no edge $NS$, and the other edges of $T-a$ still join different colours. On $N_A(a)$ the colour $2$ occurs only at $N$, so a singleton slide along $aN$ is legal in $A$. On $N_T(a)$ the colour $2$ occurs at $N$ and at $S$, so that slide is not a move of $T$.

Both poles have degree 3, so this graph lies outside the minimum-degree-5 class. The proper inclusion $N_A(h)\subsetneq N_T(h)$ for $h$ on the cut is the general fact from (B), and these two colourings show the two postconditions come apart on a spherical triangulation.

## Next step

**[lead]** The rotation count of (B) stops at three vertices. The next sentence is the same count for a vertex cut of size 4: which of the other three vertices must lie on the link, and whether minimality forces an induced 4-cycle with exactly two sides. That is the missing cut size. It asks for no enumeration and no colouring search.

## Feasibility

Feasibility that "no separating triangle" and "4-connected" are the same property for spherical triangulations: **High**. For every spherical triangulation of order at least 5, (A) and (B) give both directions. Order 4 is $K_4$, which has no separating triangle and is not 4-connected, and minimum degree 5 excludes it.

For every spherical triangulation of order at least 5, the 3-vertex cuts are exactly the separating triangles, so "no separating triangle" and "4-connected" are the same property; the cut size still missing from a reduction of VH∃ is 4.

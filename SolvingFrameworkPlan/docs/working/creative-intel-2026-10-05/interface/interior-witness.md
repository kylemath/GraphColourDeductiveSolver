# Interior witness

Interface team, 5 October 2026. Joint page. Colours are $\{0,1,2,3\}$. Throughout, $A$ and $B$ are the induced subgraphs on the closed sides of a separating triangle: if $T-F$ has component vertex-sets $C_1$ and $C_2$, then $A=T[C_1\cup F]$ and $B=T[C_2\cup F]$. Every edge of $F$ then lies in $E(A)$ and in $E(B)$.

## (A) The interior-witness lemma

**[hand]** Let $T$ be a spherical triangulation and let $F$ be a separating triangle, with $T=A\cup B$, $A\cap B=F$, and with no edge from $A\setminus F$ to $B\setminus F$. Let $r\in A\setminus F$ have degree $5$ in $A$, and let $\tau$ be a legal fan at $r$ in $A$. Suppose every colouring of $A-r$ that is proper on $\tau$ reaches the fill set of $A$ by Kempe swaps and singleton slides whose holes all lie in $A\setminus F$. Then $(r,\tau)$ is a good pair of $T$.

A state of a graph $G$ is a pair $(h,c)$ with $c$ a proper colouring of $G-h$. A Kempe swap exchanges two colours on one component of their bichromatic subgraph in $G-h$ and leaves the hole at $h$. A singleton slide at $(h,c)$ moves the hole to a neighbour $u$ whose colour occurs once on $N_G(h)$, and writes that colour at $h$. The fill set is the set of states whose link uses at most three colours. **[cited]** Lemma 1.3 of `backgroundMaterial/planemap-structural/longtable/swarm/vh-exists.md`: both moves send states to states, each reverses by a move of the same kind, and a missing colour on the link extends a fill to a proper colouring of the whole graph.

### Neighbourhoods off $F$

**[hand]** Let $v\in A\setminus F$. Every edge of $A$ at $v$ is an edge of $T$, so $N_A(v)\subseteq N_T(v)$. If $vw$ is an edge of $T$, then $vw$ lies in $E(A)$ or in $E(B)$. The vertex $v$ lies outside $V(B)$, so $vw$ lies outside $E(B)$, hence in $E(A)$. Thus $N_T(v)\subseteq N_A(v)$, and $N_T(v)=N_A(v)$. Every neighbour of $v$ lies in $A$, so every face of $T$ at $v$ is a triangle in $A$. The rotation of the edges at $v$ is the rotation in $A$. The two neighbourhoods carry the same cyclic order. These sentences use $v\notin F$ and the absence of edges from $A\setminus F$ to $B\setminus F$.

Applied to $r$, the degree in $T$ is $5$ and the cyclic neighbourhood agrees with the neighbourhood in $A$.

### The clique sentence

**[hand]** The hole of a lifted step lies in $A\setminus F$, so every vertex of $F$ is still present.

The first sentence of this argument that uses the third vertex of $F$ is the following sentence. Every pair of vertices of $F$ is adjacent in $A$ and in $B$.

The third vertex is a member of those pairs. The component-restriction paragraph in `SolvingFrameworkPlan/docs/reports/TriangleSumM3Family.md` (the paragraph at lines 15–23) does not say that the replacement path contains that vertex. Its shortcut sentence is: if the ends of an excursion are distinct, they are adjacent in the clique; properness makes their colours distinct, so that interface edge is an edge of the same bichromatic graph. The sentence which says that the replacement uses all three vertices of the clique does not match that paragraph. What the clique sentence supplies is one edge, the edge joining the two ends.

### One Kempe step

**[hand]** Let the current hole $h$ lie in $A\setminus F$, and let the colouring of $T-h$ restrict to the colouring of $A-h$. Suppose the step in $A$ swaps colours $\alpha\neq\beta$ on a component $K$ of $(A-h)[\alpha,\beta]$.

Let $P$ be a path in $(T-h)[\alpha,\beta]$ with both ends in $A$. An excursion on $P$ is a maximal subpath whose internal vertices lie in $B\setminus F$. Each end of an excursion lies in $F$: it is adjacent to an internal vertex of $B\setminus F$, every neighbour of such a vertex lies in $(B\setminus F)\cup F$, and the end is not internal to the excursion. Both ends carry $\alpha$ or $\beta$. If the two ends coincide, the replacement is that vertex, a walk of length $0$ in $F$. If the two ends $p$ and $q$ are distinct, the clique sentence supplies the edge $pq$. Properness on $pq$ forces the two colours to differ, so $\{c(p),c(q)\}=\{\alpha,\beta\}$ and $pq$ is an edge of $(A-h)[\alpha,\beta]$. The third vertex of $F$, the vertex in $F\setminus\{p,q\}$, is idle in this replacement: the walk has length $1$ and its vertex set is $\{p,q\}$. In a proper colouring the three vertices of $F$ receive three distinct colours, so that third vertex lies on no $\{\alpha,\beta\}$-path.

Replacing every excursion yields a walk in $(A-h)[\alpha,\beta]$ with the same ends in $A$. Every path of $(A-h)[\alpha,\beta]$ is a path of $(T-h)[\alpha,\beta]$, because every edge of $A$ is an edge of $T$. Therefore a nonempty restriction of a component of $(T-h)[\alpha,\beta]$ to $V(A)$ is one whole component of $(A-h)[\alpha,\beta]$, and a component that misses $V(A)$ restricts to the empty set. The component $K$ is the restriction of a unique component $K^+$ of $(T-h)[\alpha,\beta]$. Swapping $K^+$ exchanges the colours on $K$ and on $K^+\setminus V(A)\subseteq B\setminus F$. The restriction to $A-h$ is the successor colouring in $A$. A vertex of $F$ lies in $K^+$ if and only if it lies in $K$, so the colours written on $F$ are the colours written by the swap in $A$. The hole stays at $h$. **[cited]** Lemma 1.3(a) gives properness of the swapped colouring of $T-h$.

The lift in this section keeps the hole in $A\setminus F$, where all three vertices of $F$ remain. The shortcut with the hole on $F$ is a different reading, and it is the next paragraph. It is not this lemma.

**[hand]** Suppose the hole is a vertex $f\in F$, and write $F=\{f,p,q\}$. The edge $pq$ survives in $T-f$ and in $A-f$. Let $P$ be a path in $(T-f)[\alpha,\beta]$ with both ends in $A$. An excursion on $P$ through $B\setminus F$ has its ends in $\{p,q\}$: an end is adjacent to an internal vertex of the excursion, every neighbour of a vertex of $B\setminus F$ lies in $(B\setminus F)\cup F$, the end is not internal, and $f$ is absent from $P$. If the two ends coincide, the replacement is that vertex. If the ends are $p$ and $q$, both carry $\alpha$ or $\beta$. Properness on $pq$ forces those colours to be the two distinct values $\alpha$ and $\beta$, so $pq$ is an edge of $(A-f)[\alpha,\beta]$. Replacing excursions yields a walk in $(A-f)[\alpha,\beta]$. Every path of $(A-f)[\alpha,\beta]$ is a path of $(T-f)[\alpha,\beta]$. A nonempty restriction of a component of $(T-f)[\alpha,\beta]$ to $V(A)$ is one whole component of $(A-f)[\alpha,\beta]$, and the component chosen in the side is the restriction of a unique global component. Swapping the global component performs the side swap. There is no excursion whose ends are $p$ and $q$ and whose colours are a pair other than $\{c(p),c(q)\}$: properness on $pq$ forbids it. The fill target is not this paragraph. Section (C) treats that target on one coloured link: $N_A(f)$ is a proper subset of $N_T(f)$.

### One interior slide

**[hand]** Suppose instead the step is a singleton slide in $A$ from $h$ to $u$, with both $h$ and $u$ in $A\setminus F$, and with $\alpha$ the colour of $u$, occurring once on the link of $h$ in $A$.

The neighbourhood identity gives $N_T(h)=N_A(h)$ with the same cyclic order. Consecutive vertices in that order are adjacent in $T$. The same pairs are adjacent in $A$: if at least one end lies in $A\setminus F$, the rim edge lies outside $E(B)$ and hence in $E(A)$; if both ends lie in $F$, the clique sentence places the edge in $E(A)$, and the third vertex of $F$ is idle in that subcase. The link cycle of $h$ in $T$ is the link cycle of $h$ in $A$. The colouring agrees on that set, so $\alpha$ occurs once on $N_T(h)$. The slide $h\to u$ is a legal singleton slide of $T$. It writes $\alpha$ at $h$ and leaves every other colour unchanged. Every vertex of $B\setminus F$ is distinct from $h$ and from $u$, so the far side keeps its colours. The successor colouring of $T-u$ restricts to the successor colouring of $A-u$. The new hole $u$ lies in $A\setminus F$.

### The terminal state, the fan, and the apex

**[hand]** The invariant holds at the start, a Kempe successor preserves it, and an interior-slide successor preserves it, so it holds at the terminal hole $h_m\in A\setminus F$. The neighbourhoods agree there, and the terminal link in $A$ uses at most three colours, so the terminal link in $T$ uses at most three colours. Each lifted step is a Kempe swap or a singleton slide of $T$. By Lemma 1.3 the original state and the terminal state lie in one component of the move graph of $T$, and a missing colour extends the terminal colouring to $T$.

The chords of $\tau$ are non-edges of $A$. Both ends lie on the neighbourhood of $r$, hence in $A$. If such a chord were an edge of $T$, it would lie in $E(B)$ with both ends in $F$, and the clique sentence would place it in $E(A)$, against the choice of $\tau$. The chord lies outside $E(T)$, and $\tau$ is a legal fan at $r$ in $T$.

Thus $\deg_T(r)=5$, the fan is legal in $T$, and every colouring of $T-r$ proper on $\tau$ reaches the fill set of $T$. The pair $(r,\tau)$ is a good pair of $T$.

An apex on $F$ is not this lemma. The interior-slide sentences take the landing in $A\setminus F$, and the neighbourhood identity is stated for vertices in $A\setminus F$. A slide whose landing lies on $F$ is absent from a path whose holes stay in $A\setminus F$. **[cited]** Lemma 3.2 of `vh-exists.md` makes the colour of an apex unique on the link of a degree-$5$ vertex when the colouring is proper on the fan; that count is a count in one link. Section (C) gives a link in $T$ on which the same colour occurs twice.

## (B) The cut

The four claims below were checked against the argument in the Connectivity note. Each one stands. No step is replaced.

**[hand]** Let $S=\{a,b,c\}$ be a $3$-vertex cut of a spherical triangulation $T$, and let $C_1,\ldots,C_r$ be the vertex sets of the components of $T-S$, with $r\ge 2$. The graph $T$ is $3$-connected, so no proper subset of $S$ is a vertex cut.

Each vertex of $S$ meets every component. If $a$ had no neighbour in $C_1$, every edge leaving $C_1$ would end in $\{b,c\}$. Then $T-\{b,c\}$ would have no edge out of $C_1$, while $C_2$ supplies a vertex outside $C_1$, and $\{b,c\}$ would be a $2$-vertex cut.

There are exactly two components. Along the link of $a$, consecutive vertices are adjacent, and no edge joins two components of $T-S$, so the component can change only at a neighbour in $\{b,c\}$. Each of $b$ and $c$ occurs at most once. Fewer than two of them on the link would leave a single consecutive block of component-neighbours, hence a single component, against the existence of two components that both meet $N(a)$. So $ab$ and $ac$ are edges, and both arcs of the link from $b$ to $c$ are nonempty: a consecutive pair $b,c$ would again leave one block. Each arc lies in one component. The two arcs lie in different components, because otherwise $N(a)$ would meet only one component. Every component meets $N(a)$, and the only places it can do so are these two arcs, so $r=2$. The same count at $b$ supplies the edge $bc$. The induced subgraph $T[S]$ is a triangle.

That triangle is non-facial. The faces at $a$ are the triangles on consecutive link neighbours. Since $b$ and $c$ are not consecutive at $a$, the triple $\{a,b,c\}$ is not the vertex set of a face at $a$. A face bounded by the cycle $abc$ would be incident with $a$.

**[hand]** Each arc contributes at least one neighbour, and the two triangle edges are counted in both induced sides. For $f\in S$,
\[
\deg_A(f)\ge 3,\qquad \deg_B(f)\ge 3,\qquad \deg_T(f)=\deg_A(f)+\deg_B(f)-2\ge 4,
\]
and $N_A(f)\subsetneq N_T(f)$. The identity is the partition of $N_T(f)$ into the two arcs and the pair of triangle neighbours: each side-degree counts the arc plus those two neighbours, and the subtraction removes the double count. The bound $4$ is $3+3-2$. A facial triangle is not a vertex cut: one arc between the other two vertices would be empty, and the remaining arc would meet only one component.

**[hand]** Let $T$ have order $n\ge 5$. The following are equivalent: $T$ has a separating triangle; $T$ has a vertex cut of size $3$; $T$ is not $4$-connected. A separating triangle is a $3$-vertex cut, and $n\ge 5$ then refuses $4$-connectivity. If $T$ is not $4$-connected, then $n>4$ and some set of size at most $3$ disconnects $T$; $3$-connectivity forces that set to have size exactly $3$. A $3$-vertex cut induces a non-facial triangle with both sides nonempty, which is a separating triangle.

The same identity does not by itself give the bound $5$. Inside the minimum-degree-$5$ class every vertex already has degree at least $5$, so a cut vertex there has degree at least $5$, and the least split of the side degrees is $3$ and $4$. That floor comes from the class, not from the arc count. The arc count remains $\ge 4$ on every spherical triangulation.

**[hand]** Order $4$ is separate. Degree at least $3$ on four vertices forces $K_4$. Deleting any three vertices leaves a single vertex, so $K_4$ has no $3$-vertex cut and no separating triangle. It is not $4$-connected, because $4$-connectivity requires more than four vertices. Every degree is $3$, so this order lies outside the minimum-degree-$5$ class.

**[cited]** The Jordan converse, that a non-facial $3$-cycle separates, is not used above.

## (C) The fixed hole

Let $F=\{f,p,q\}$ with $\deg_A(f)=3$, $\deg_B(f)=4$ and $\deg_T(f)=5$. The link of $f$ in $A$ is $(p,a,q)$. The link of $f$ in $B$ is $(p,b_1,b_2,q)$. The cyclic order in $T$ is $(p,a,q,b_2,b_1)$. There is no edge from $a$ to $\{b_1,b_2\}$. Colour $c(p)=0$, $c(a)=1$, $c(q)=2$, $c(b_2)=1$, $c(b_1)=3$. The side link uses $\{0,1,2\}$. The link in $T$ uses $\{0,1,2,3\}$.

**[hand]** The slide $f\to a$ is illegal in $T$. Colour $1$ occurs at $a$ and at $b_2$. A singleton slide requires the chosen colour to occur once on the link. The same colour occurs once on the $A$-link, at $a$, so the slide is legal in $A$. A slide is a different move from a Kempe swap. The rest of this section uses only Kempe swaps at the fixed hole $f$.

### The six pairs

**[hand]** Work in $G=T-f$, with the link edges $pa$, $aq$, $qb_2$, $b_2b_1$, $b_1p$ and the triangle edge $pq$, and with an arbitrary further interior, properly coloured, and with no edge from $a$ to $\{b_1,b_2\}$. A swap of colours $\alpha,\beta$ changes the link colour set only by exchanging $\alpha$ and $\beta$ on the link vertices that lie in the chosen component. The two colours outside $\{\alpha,\beta\}$ remain on the link. The link colour set drops below four colours only when one of $\alpha,\beta$ disappears from the link: every link vertex of that colour flips, and no link vertex of the other colour flips.

- Pair $\{0,1\}$. The edge $pa$ has colours $0$–$1$, so any component that contains $p$ contains $a$. Eliminating $0$ flips $p$ and therefore flips $a$, and $a$ becomes $0$. Eliminating $1$ flips both colour-$1$ link vertices $a$ and $b_2$; flipping $a$ flips $p$, and $p$ becomes $1$.
- Pair $\{0,2\}$. The edge $pq$ has colours $0$–$2$, so $p$ and $q$ lie in one component. Eliminating either colour flips the other onto the link.
- Pair $\{0,3\}$. The edge $b_1p$ has colours $3$–$0$, so $p$ and $b_1$ lie in one component. The same lock applies.
- Pair $\{1,2\}$. The edges $aq$ and $qb_2$ have colours $1$–$2$ and $2$–$1$, so $a$, $q$ and $b_2$ lie in one component. Eliminating either colour flips the other onto the link.
- Pair $\{1,3\}$. The edge $b_2b_1$ has colours $1$–$3$, so $b_2$ and $b_1$ lie in one component. The vertex $a$ lies in another component: every path in $G$ from $a\in A\setminus F$ to $\{b_1,b_2\}\subseteq B\setminus F$ meets $\{p,q\}$, and those two vertices have colours $0$ and $2$, so neither lies on a $\{1,3\}$-path. One swap cannot flip both colour-$1$ link vertices. Eliminating $3$ flips $b_1$ and therefore flips $b_2$, and $b_2$ becomes $3$.
- Pair $\{2,3\}$. The only link vertices of these colours are $q$ and $b_1$. If they lie in different components, swap the component of $b_1$. Then $b_1$ becomes $2$, the only colour-$2$ link vertex $q$ stays $2$, and no link vertex becomes $3$. The link uses $\{0,1,2\}$. If they lie in one component, the swap flips both, and the link still uses four colours.

A single Kempe swap at $f$ makes this five-vertex link use at most three colours if and only if $b_1$ and $q$ lie in different components of $G[2,3]$. That separation is not forced by the link. The edge $pq$ is what locks the pair $\{0,2\}$, which is the other pair that would free a colour on a $5$-cycle with no triangle edge.

### A sequence when $b_2$ does not meet $p$ after one preparatory swap

**[hand]** Suppose a $\{2,3\}$-path from $b_1$ to $q$ exists, so the one-swap branch above is closed. Let $K$ be the component of $b_2$ in $G[1,3]$. The edge $b_2b_1$ puts $b_1$ in $K$. The cut argument of the $\{1,3\}$ case keeps $a$, $p$ and $q$ out of $K$. Swap $K$. The new link is $(p,a,q,b_2,b_1)$ coloured $(0,1,2,3,1)$, still four colours. Call the new colouring $c'$.

Under $c'$, the vertex $b_2$ has colour $3$. It has no neighbour of colour $1$ in the original colouring, because $b_2$ itself had colour $1$. Every original colour-$3$ neighbour of $b_2$ lay in $K$ and now has colour $1$. The neighbours of $b_2$ that have colour $0$ or $3$ under $c'$ are therefore among the original colour-$0$ neighbours of $b_2$. If $p$ does not lie in the $\{0,3\}$-component of $b_2$ under $c'$, swap that component. The only colour-$0$ link vertex is $p$, and it stays $0$. The vertex $b_2$ becomes $0$. No other link vertex has colour $0$ or $3$ under $c'$ except $b_2$. The link uses $\{0,1,2\}$.

### The certificate

**[hand]** The following spherical triangulation has order $6$ and realizes the link. It is a certificate about this coloured link. The degrees of $a$ and of $b_2$ are $3$, so the graph lies outside the minimum-degree-$5$ class. It is not a failure.

Vertices: $f,p,a,q,b_1,b_2$. Edges:
\[
fp,\; fa,\; fq,\; fb_1,\; fb_2,\;
pa,\; aq,\; qb_2,\; b_2b_1,\; b_1p,\;
pq,\; qb_1.
\]
Faces: $(f,p,a)$, $(f,a,q)$, $(f,q,b_2)$, $(f,b_2,b_1)$, $(f,b_1,p)$, $(p,a,q)$, $(p,q,b_1)$, $(q,b_2,b_1)$. Here $n-e+f=6-12+8=2$. The cyclic order at $f$ is $(p,a,q,b_2,b_1)$. The side $A=T[\{f,p,a,q\}]$ has $\deg_A(f)=3$. The side $B=T[\{f,p,q,b_1,b_2\}]$ has $\deg_B(f)=4$. Deleting $F$ leaves $\{a\}$ and $\{b_1,b_2\}$, with the edge $b_1b_2$ and with no edge from $a$ to $\{b_1,b_2\}$.

Colour $T-f$ by $c(p)=0$, $c(a)=1$, $c(q)=2$, $c(b_2)=1$, $c(b_1)=3$. Every edge of $T-f$ joins different colours: $pa$ is $0$–$1$, $aq$ is $1$–$2$, $qb_2$ is $2$–$1$, $b_2b_1$ is $1$–$3$, $b_1p$ is $3$–$0$, $pq$ is $0$–$2$, and $qb_1$ is $2$–$3$.

The components, as vertex lists, are:

| pair | components |
|---|---|
| $\{0,1\}$ | $(p,a)$ and $(b_2)$ |
| $\{0,2\}$ | $(p,q)$ |
| $\{0,3\}$ | $(p,b_1)$ |
| $\{1,2\}$ | $(a,q,b_2)$ |
| $\{1,3\}$ | $(a)$ and $(b_2,b_1)$ |
| $\{2,3\}$ | $(b_1,q)$ |

The blocking path for $\{2,3\}$ is $(b_1,q)$. Swapping it sends the link to $(0,1,3,1,2)$. The other swaps send the link to $(1,0,2,1,3)$, $(0,1,2,0,3)$, $(2,1,0,1,3)$, $(3,1,2,1,0)$, $(0,2,1,2,3)$, $(0,3,2,1,3)$ or $(0,1,2,3,1)$. Each uses four colours. No single Kempe swap at $f$ fills this link.

Two swaps do fill it. Swap $\{1,3\}$ on $(b_2,b_1)$. The colouring becomes $(p,a,q,b_2,b_1)=(0,1,2,3,1)$. The neighbours of $b_2$ in $T-f$ are $q$ and $b_1$, now coloured $2$ and $1$, and there is no edge $b_2p$. The $\{0,3\}$-components are the singletons $(b_2)$ and $(p)$. Swap $(b_2)$: the link becomes $(0,1,2,0,1)$, which uses $\{0,1,2\}$. Swap $(p)$ instead: the link becomes $(3,1,2,3,1)$, which uses $\{1,2,3\}$.

This certificate sits in the preparatory case above: after the swap on $(b_2,b_1)$, the vertex $b_2$ is not joined to $p$ in colours $\{0,3\}$.

What this does to the fixed-hole question is the next paragraph.

### What the split says

**[hand]** For an arbitrary interior consistent with the coloured link, one Kempe swap at $f$ fills the five-vertex link precisely when $b_1$ and $q$ are separated in colours $\{2,3\}$. The certificate is an interior where they are joined by $(b_1,q)$, and no single swap fills. Whenever they are separated, one swap fills. Whenever they are joined, and after the swap of the $\{1,3\}$-component of $b_2$ the vertex $b_2$ is not joined to $p$ in colours $\{0,3\}$, a second swap fills. The certificate is in that second class, and the two sequences above are the second swap.

**[hand]** On the pentagon $(p,a,q,b_2,b_1)$ the chords $b_2p$ and $qb_1$ alternate, so they are not both edges. If $qb_1$ is an edge, it separates $b_2$ from $p$ in the disc of $(p,b_1,b_2,q)$. Under $c'$ the vertices $b_1$ and $q$ have colours $1$ and $2$, so no $\{0,3\}$-path from $b_2$ to $p$ crosses that chord. If $b_2p$ is an edge, it separates $b_1$ from $q$, and $b_2$ and $p$ have colours $1$ and $0$, so no $\{2,3\}$-path from $b_1$ to $q$ crosses it. A double lock uses neither chord. The order-$6$ certificate has $qb_1$ and therefore has no second path. A $\{2,3\}$-path from $b_1$ to $q$ other than that chord has length at least $3$: the internal vertices alternate colours $2$ and $3$, and two vertices of colour $2$ are nonadjacent, so the path uses an interior vertex of colour $2$ and an interior vertex of colour $3$. The swap that produces $c'$ exchanges colours $1$ and $3$ and creates no vertex of colour $0$. A $\{0,3\}$-path under $c'$ from $b_2$ to $p$, other than the missing chord $b_2p$, therefore uses an interior vertex of original colour $0$. Those three interior vertices are distinct. Together with $f$ and the five link vertices, the smallest order of a double lock is $9$.

**[hand]** The same Jordan cut identifies the crossing. A simple $\{2,3\}$-path from $b_1$ to $q$ separates the disc of $(p,b_1,b_2,q)$ into the region of the arc $b_1b_2q$ and the region of the arc $b_1pq$. Under $c'$ a $\{0,3\}$-path from $b_2$ to $p$ uses neither $b_1$ nor $q$, so it meets the first path at a vertex $s$ of original colour $3$ lying outside the $\{1,3\}$-component of $b_2$.

**[hand]** Order $9$ realizes both locks. It is a certificate about this coloured link. The vertex $a$ has degree $3$, so the graph is not a failure. Vertices: $f,p,a,q,b_1,b_2,u,v,w$. Edges:
\[
\begin{align*}
&fp,\; fa,\; fq,\; fb_1,\; fb_2,\;
pa,\; aq,\; qb_2,\; b_2b_1,\; b_1p,\; pq,\\
&pu,\; b_1u,\; b_2u,\; uw,\; uv,\;
b_2w,\; qw,\; wv,\; vq,\; vp.
\end{align*}
\]
Faces: $(f,p,a)$, $(f,a,q)$, $(p,a,q)$, $(f,q,b_2)$, $(f,b_2,b_1)$, $(f,b_1,p)$, $(p,b_1,u)$, $(b_1,b_2,u)$, $(b_2,w,u)$, $(b_2,q,w)$, $(q,v,w)$, $(q,p,v)$, $(p,u,v)$, $(u,w,v)$. Here $n-e+f=9-21+14=2$. Neither $b_2p$ nor $qb_1$ is an edge. Colour $p,a,q,b_2,b_1,u,v,w$ by $0,1,2,1,3,2,3,0$. The new edges meet different colours: $u$ is adjacent to $p,b_1,b_2,w,v$ coloured $0,3,1,0,3$; $w$ is adjacent to $b_2,q,v,u$ coloured $1,2,3,2$; $v$ is adjacent to $q,p,u,w$ coloured $2,0,2,0$.

The first lock is the $\{2,3\}$-path $(b_1,u,v,q)$, with colours $3,2,3,2$. The $\{1,3\}$-component of $b_2$ is $(b_2,b_1)$: the neighbours of $v$ are $q,p,u,w$, coloured $2,0,2,0$, so $v$ is not on that component. Swap $(b_2,b_1)$. The second lock is the $\{0,3\}$-path $(b_2,w,v,p)$, with colours $3,0,3,0$. The two paths meet at $s=v$. Swapping that second path flips $b_2$ and $p$ together and leaves four colours on the link.

One swap does not fill: the first path joins $b_1$ to $q$, and the six-pair split gives no other pair. Two swaps do fill. Swap $\{1,3\}$ on the singleton $(v)$, sending $v$ from $3$ to $1$. In the resulting colouring the neighbours of $q$ are $a,p,b_2,w,v$, coloured $1,0,1,0,1$, so $(q)$ is a component of colours $\{2,3\}$. Swap $(q)$, sending $q$ from $2$ to $3$. The link is $(0,1,3,1,3)$, which uses $\{0,1,3\}$.

**[open]** Whether every double-locked interior, and not only this order-$9$ certificate, reaches a $3$-colour link by Kempe swaps at $f$.

## (D) Degree less than $5$ only on $F$

**[hand]** Let every vertex of $A$ of degree less than $5$ lie on $F$, and let $\deg_A(f)=3$ with $A$-link $(p,a,q)$. The three faces of $A$ at $f$ are $(f,p,a)$, $(f,a,q)$ and $(f,p,q)$. Their union is one disc of the cycle $(p,a,q)$, the disc that contains $f$. Every other vertex of $A$ lies in the opposite disc. In $T$ the far side $B$ is glued into the face $(f,p,q)$, which lies in the disc that contains $f$. Whenever the opposite disc contains a vertex $x$, the cycle $(p,a,q)$ separates $x$ from $f$ and from $B$. The triangle $(p,a,q)$ is a separating triangle of $T$. Each vertex of $A\setminus F$ other than $a$ lies in that disc. The vertex $a$ lies on the triangle.

**[hand]** Let $A'$ be the completion of that opposite disc along $(p,a,q)$: the induced subgraph on the disc together with the three boundary edges, read as a spherical triangulation. If $B\setminus F$ is nonempty then $|V(A')|=|V(A)|-1<|V(T)|$. In $A'$, each of $p$, $a$ and $q$ loses the neighbour $f$, so $\deg_{A'}(x)=\deg_A(x)-1$ for each of those three. $A'$ lies in the minimum-degree-$5$ class only when all three had degree at least $6$ in $A$. Otherwise least order does not supply a good pair, and $A'$ is not a smaller failure. The unfinished carry is the generic case. When all three degrees in $A$ are at least $6$ and $A'$ has minimum degree $5$, $A'$ is smaller than $T$ and lies in the class, and least order on a smallest failure $T$ supplies $A'$ a good pair.

**[open]** Carrying that pair into $T$ is an interior witness relative to $(p,a,q)$, which is (A) at the inner triangle, or a passage whose hole meets $(p,a,q)$. A hole on $(p,a,q)$ is a fixed-hole problem of the same shape as (C). Section (C) treats one coloured link; it does not discharge every such passage. Least order on a smallest failure supplies the pair on $A'$ when $A'$ has minimum degree $5$. It does not supply the carry. If $A'$ does not have minimum degree $5$, least order does not apply, and $A'$ lies outside the class, so it is not a smaller failure either. The degree-$3$ step colours $A-f$ and assigns $f$ a colour missing on $\{p,a,q\}$. Its output is a colouring of $A$. A filling path of an interior degree-$5$ deletion of $T$ is further data. The same gap, one step up, is a side of degree $4$ at $f$: the degree-$4$ step adds one diagonal, colours the resulting triangulation, and equalises a colour on the four $A$-neighbours of $f$. The neighbours of $f$ in $B$ stay on the link in $T$. The step colours $A$.

## (E) $H_2$

**[hand]** $H_2$ is two copies of $17{:}1$, glued along $F_+=\{3,4,11\}$ of the first and $F_-=\{1,2,7\}$ of the second. The order is $14\cdot 2+3=31$. The good pair is vertex $0$, fan $1$, in the last copy. Both faces avoid vertex $0$. The filling paths used there are pure Kempe swaps, and a Kempe swap keeps its hole, so every hole stays at $0$, off the interface. Section (A) applies. $H_2$ carries an interior witness, so $H_2$ is a success. A separating triangle occurs on a success. **[cited]** By (B) the same graph is not $4$-connected. The two completed sides have minimum degree $5$, so this glue is not the configuration in (D).

## (F) A smallest failure

**[hand]** A failure is a spherical triangulation of minimum degree $5$ with no good pair. A smallest failure has least order among failures. If a separating triangle of a smallest failure carried an interior witness, section (A) would make that pair a good pair of the whole graph, and the graph would not be a failure. A smallest failure's separating triangles cannot carry an interior witness.

The remaining way a separating triangle can still sit in a smallest failure is a side on which some filling path places a hole on the triangle, where the link in the side is a proper subset of the link in $T$, or a side whose vertices of degree less than $5$ all lie on $F$, where the interior degree-$5$ vertices are vertices of $T$ and the side lies outside the class, with the carry in (D) unfinished.

**[open]** Whether a smallest failure contains a separating triangle. **[lead]** The count for a vertex cut of size $4$ is the next cut. Nothing on this page treats it.

## Feasibility

Feasibility that the interior-witness lift stands: **High**.

Feasibility that "no separating triangle" and "$4$-connected" are the same property for every spherical triangulation of order at least $5$: **High**.

Feasibility that one Kempe swap at $f$ fills every interior consistent with the coloured link: **Low**.

Feasibility that a finite sequence of Kempe swaps at the fixed hole $f$ fills every such interior: **Medium**. The complement of the double lock is settled above, and the smallest double lock fills in two swaps. The universal double lock is open.

Feasibility that a smallest failure contains a separating triangle: **Medium-Low**. An interior witness on the triangle produces a success of the shape of $H_2$. The remainder is the fixed hole, including the universal double lock, together with the unfinished carry, which is the generic degree case on $(p,a,q)$.

Feasibility that least order alone carries the inner pair across $(p,a,q)$: **Low**.

## Next steps

1. The order-$9$ double lock fills in two swaps, and there $s=v$ has no colour-$1$ neighbour. The open sentence is the universal one: an interior in which the crossing vertex has a colour-$1$ neighbour in its own $\{1,3\}$-component, decided by hand on that finite graph. No census.
2. One minimum-degree-$5$ completion of a disc bounded by $(p,a,q)$, and one good pair on it whose holes are checked against the cap. The carry is the open sentence in (D).
3. The rotation count for a vertex cut of size $4$: which of the other three vertices lie on the link, and whether the cut is an induced $4$-cycle with two sides. That count is not started here.

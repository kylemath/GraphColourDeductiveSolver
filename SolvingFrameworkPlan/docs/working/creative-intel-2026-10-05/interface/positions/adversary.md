# Adversary: a separating triangle in a smallest failure

The claim under attack is that a smallest VH∃ failure has no separating triangle. A failure is a spherical triangulation of minimum degree 5 with no good pair $(v,\tau)$. A smallest failure has least order among failures. Let $T=A\cup B$ with $A\cap B=F$ a separating triangle and with no edge from $A\setminus F$ to $B\setminus F$.

The interior lift stands. The bichromatic shortcut stands again when the hole lies on $F$. The sentence that falls is the identification of the target: the link in the side is a proper subset of the link in $T$. A side whose vertices of degree less than 5 all lie on $F$ lies outside the class, and its interior degree-5 vertices are a real gap. $H_2$ is a success, and it removes several guesses that treat a separating triangle as a failure.

## 1. Hole in $A\setminus F$

**[hand]** Let $r\in A\setminus F$, and let every hole of the filling path in $A$ stay in $A\setminus F$. This is the interior lift. Three attacks were pressed against it.

The first attack tries to drop the third vertex of $F$ out of the shortcut while the hole is still off $F$. All three vertices are coloured. An excursion through $B\setminus F$ has its ends in $F$. Distinct ends are adjacent. They carry the selected colours, properness makes those colours distinct, and the interface edge lies in the bichromatic subgraph. The replacement path lies in $A-r$.

The second attack tries to repeat a link colour from the far side. For $h\in A\setminus F$ one has $N_T(h)=N_A(h)$. A colour that occurs once on the link in $A$ occurs once on the link in $T$. The slide $h\to u$ with $u\in A\setminus F$ is legal in $T$, writes a colour only at $h$, and leaves the new hole in $A\setminus F$.

The third attack tries to let the global component drag an extra vertex of $A$ into the swap. The converse sentence of the component-restriction lemma answers it. A component $K$ of $(A-h)[\alpha,\beta]$ is the restriction of a unique component of $(T-h)[\alpha,\beta]$. Swapping the global component recolours $A$ on $K$ and may recolour vertices of $B$. The hole stays at $h$.

The interior lift stands. The sentence the first attack failed to break is the shortcut sentence of the component-restriction lemma: "If they are distinct, they are adjacent in the clique; properness makes their colours distinct, so that interface edge is an edge of the same bichromatic graph."

**[open]** A good pair of a minimum-degree-5 side may place some later hole on $F$. The shortcut sentence is silent on that pair. It supplies an interior witness only for a path whose holes already stay off $F$.

## 2. Hole on $F$

Let $F=\{f,p,q\}$ and let the hole be $f$. The remaining interface is the edge $pq$.

Take the degree split in which an interface vertex has degree 5 in $T$: $\deg_A(f)=3$ and $\deg_B(f)=4$. The link of $f$ in $A$ is $(p,a,q)$, so $N_A(f)=\{p,a,q\}$. The link of $f$ in $B$ runs $(p,b_1,b_2,q)$. Around $f$ in $T$ the cyclic order is $(p,a,q,b_2,b_1)$, and $N_T(f)=\{p,a,q,b_1,b_2\}$. The cut forbids every edge from $\{a\}$ to $\{b_1,b_2\}$. The forced edges among these five vertices are the link cycle, together with the interface edge $pq$. The chords $p b_2$ and $q b_1$ may exist inside $B$; the colouring below is proper if they do.

**[hand]** Colour $c(p)=0$, $c(a)=1$, $c(q)=2$, $c(b_2)=1$, $c(b_1)=3$. The $A$-link uses $\{0,1,2\}$. The $T$-link uses $\{0,1,2,3\}$. The neighbour $b_1$ carries the colour missing from the side. A 3-colour link in $A$ sits inside a 4-colour link in $T$. The terminal sentence of the interior lift, that the same vertices are the link in $T$, fails at $f$.

**[hand]** In the same colouring, colour $1$ occurs once on the $A$-link, at $a$, and twice on the $T$-link, at $a$ and at $b_2$. The slide $f\to a$ is legal in $A$ and illegal in $T$. The slide sentence, that a colour unique on the link in $A$ is unique on the link in $T$, fails at $f$. The vertex $a$ lies in $A\setminus F$, so this is a slide that would have returned the hole to the open side.

**[hand]** The excursion, on the same vertices. For the pair $\{0,3\}$ the edge $p b_1$ is bichromatic, since $c(p)=0$ and $c(b_1)=3$. The vertex $q$ has colour $2$, so $q$ lies off that subgraph. The edge $pq$ carries $\{0,2\}$, the wrong pair for $\{0,3\}$, and the sentence "Its endpoints lie in $F$ and carry the selected colours" gives this excursion no end at $q$. There is no $\{0,3\}$-path through $B$ from $p$ to $q$ to collapse.

For the pair $\{0,2\}$ the ends $p$ and $q$ do carry the selected colours, properness makes them distinct, and $pq$ is a $\{0,2\}$-edge. Any excursion through $B\setminus F$ with those ends is replaced by that edge.

That dichotomy is the Kempe step with the hole on the triangle. Let $H$ be the subgraph of colours $\alpha,\beta$ in $T-f$. An excursion into $B\setminus F$ has its ends in $\{p,q\}$, and both ends lie in $H$. Coincident ends are deleted. Distinct ends are $p$ and $q$, hence $\{c(p),c(q)\}=\{\alpha,\beta\}$, and $pq$ is the replacement. The resulting path lies in $A-f$. A bichromatic path of $A-f$ is a bichromatic path of $T-f$. The restriction of a global component is empty or one whole component of the side. Swapping the global component performs that swap on $A$.

The shortcut sentence therefore stands on the interface. The sentence of the lemma that speaks only about the open side is the hypothesis "with its hole $r$ in $A\setminus F$", and with it the closing line "The hole is fixed outside the interface when this lemma is used." Rerun with the hole at $f$, the shortcut still returns a path in the side. The sentence that is false on the colouring above is the target sentence of the family upper bound: "Root 0 has no exterior neighbours, so the seed target is a global target." The hole $f$ has exterior neighbours $b_1$ and $b_2$. A 3-colour link on $N_A(f)$ is a target of the side. The five-vertex link is the target of $T$.

**[lead]** A repair that keeps the hole fixed at $f$ is a Kempe swap. A swap that meets $A$ is already a swap of the side, by the restriction just written. A change in the colours of $b_1$ and $b_2$ that leaves every vertex of $A$ fixed comes from a component that meets $B\setminus F$ and misses $A$.

**[open]** Whether every proper colouring of $T-f$ in which $\{p,a,q\}$ uses at most three colours reaches, by Kempe swaps at this fixed hole, a colouring in which $\{p,a,q,b_1,b_2\}$ uses at most three colours.

## 3. Degree less than 5 only on $F$

**[hand]** Let every vertex of $A$ of degree less than 5 lie on $F$, and let $v\in A\setminus F$ have degree 5. Then $N_T(v)=N_A(v)$, so the link and the legal fans of $v$ agree in $A$ and in $T$. An interior witness at $v$ is a good pair of $T$ by the lift in section 1. A smallest failure has no interior witness at any such $v$.

A failure is a triangulation of minimum degree 5. The completed side $A$ has a vertex of degree 3 or 4, so $A$ lies outside that class. The interior degree-5 vertices are vertices of $T$. The degree-3 step and the degree-4 step name an auxiliary triangulation of the side and return a colouring of the side.

**[hand]** Suppose $\deg_A(f)=3$, with $A$-neighbours $p,a,q$ as in section 2. Those three are pairwise adjacent. The faces at $f$ in $A$ are $(f,p,a)$, $(f,a,q)$ and $F=(f,p,q)$. Every further vertex of $A$ lies in the disc bounded by $(p,a,q)$ on the side opposite $f$. Whenever that disc contains a vertex, $(p,a,q)$ separates it from $f$ and from $B$, and is a separating triangle of $T$. Each degree-5 vertex of $A\setminus F$ other than $a$ lies in the disc. The degree-3 step colours the smaller triangulation $A-f$ and assigns $f$ a colour missing on $\{p,a,q\}$. Its output is a colouring of $A$. A fan at an interior degree-5 vertex, and a filling path of the deletion of that vertex in $T$, are further data.

**[hand]** If the completion of that disc along $(p,a,q)$ has minimum degree 5, it has smaller order than $T$ and lies in the class. Least order on $T$ supplies that completion a good pair. Carrying the pair into $T$ is an interior witness relative to $(p,a,q)$, which is section 1 at the inner triangle, or a passage whose hole meets the inner triangle, which is section 2. The degree-3 step stops at the colouring of $A$.

**[hand]** Suppose instead $\deg_A(f)=4$, with link $(p,a_1,a_2,q)$ in $A$. The star of $f$ in $A$ is bounded by the 4-cycle $p\,a_1\,a_2\,q$. The degree-4 step adds one missing diagonal, colours the resulting triangulation on $|A|-1$ vertices, and, on a 4-colour link, performs one Kempe swap in $A-f$ by the Jordan split. That swap equalises a colour on the four $A$-neighbours of $f$. The neighbours of $f$ in $B$ stay on the link in $T$. The step colours $A$. A filling path of an interior degree-5 deletion of $T$ is further data.

**[open]** The configuration remains available to a smallest failure. It is a real gap. The interior degree-5 vertices are not a smaller failure: the side lies outside the class, and a minimum-degree-5 inner completion already has a good pair by least order, still to be carried across its own triangle.

## 4. $H_2$

**[hand]** $H_2$ is two copies of 17:1, glued along $F_+=\{3,4,11\}$ of the first and $F_-=\{1,2,7\}$ of the second. The order is $14\cdot 2+3=31$ and $m(H_2)=3$. The good pair is vertex 0, fan 1, in the last copy. Both faces avoid vertex 0. The family upper bound lifts a pure Kempe path at that vertex, and a Kempe swap keeps its hole, so every hole of those paths stays at 0, off the interface. The pair is an interior witness. Section 1 applies. $H_2$ is a success.

**[post hoc]** The saved degree list of 17:1 places the degree-6 vertices at $2,3,6,11,14$. Thus $F_+$ meets degrees $6,5,6$ and $F_-$ meets degrees $5,6,5$. Outside the interface the two sides of $H_2$ have different degree histograms, $11$ vertices of degree 5 and $3$ of degree 6 against $10$ of degree 5 and $4$ of degree 6. The same saved check finds a unique separating triangle and trivial stabilizers of both chosen faces, so the automorphism group of $H_2$ is trivial.

**[post hoc]** The printed link of vertex 0 is $(1,2,3,4,5)$, which meets both chosen faces. A slide from vertex 0 can land on the interface. The paths the family lifts are swaps and stay at 0.

$H_2$ removes the following guesses.

- A separating triangle produces a failure. $H_2$ has a separating triangle and a good pair.
- A trivial automorphism group produces a failure. The group of $H_2$ is trivial, and $H_2$ is a success.
- A cut of size 3 produces a failure. The interface of $H_2$ is such a cut, and $H_2$ is a success.
- Interface degree at least 8 produces a failure. Each interface degree in this glue is at least $5+5-2=8$, and the witness at vertex 0 remains.
- A second copy of an $m=3$ seed produces a failure. The last copy is what carries the interior witness.

**[hand]** Both completed sides of $H_2$ are copies of 17:1, of minimum degree 5, and the witness stays off the interface. Sections 2 and 3 are about other gluings.

## Remainder

**[open]** A smallest failure can still contain a separating triangle $F$, through a hole at an interface vertex whose link in the side is a proper subset of its link in $T$, or through a side whose vertices of degree less than 5 all lie on $F$, where the interior degree-5 vertices are not a smaller failure.

Feasibility that a smallest failure can still contain a separating triangle: **Medium-Low**. The interior lift stands, and the bichromatic shortcut stands with the hole on the triangle, so an interior witness produces a success of the $H_2$ shape. The remainder is the target mismatch at $f$, together with the degree drop on $F$.

The joint page should answer one question. At an interface vertex $f$ with $\deg_A(f)=3$, $\deg_B(f)=4$ and $\deg_T(f)=5$, links $(p,a,q)$ and $(p,b_1,b_2,q)$ as above, does every proper 4-colouring of $T-f$ in which $\{p,a,q\}$ uses at most three colours reach a colouring in which $\{p,a,q,b_1,b_2\}$ uses at most three colours, by Kempe swaps at the fixed hole $f$?

# VH∃: the hole induction with the weaker hypothesis, two lemmas, and reformulations

Long Table, 5 October 2026. A hand-proof page for review by the math team. Nothing here is a status change. "Proved" is used only where the argument is written out in full on this page. Machine checks are on the 118 WP11 manifest graphs of orders 12, 14–20 only. Orders 19–20 are the spent WP11/WP18 holdout, and every number from them is a labelled secondary reading. The script is `vh_exists_check.py`, the output is `vh-exists-check.txt` (SHA-256 `f3e9e372…b068b4`; script `38053390…039328`).

The quantifier order follows the independent review (`SolvingFrameworkPlan/docs/reports/IndependentWP18AndBeltReview.md`, section "VH-exists and its two lemmas"). For every minimum-degree-5 spherical triangulation, **there exist a degree-5 vertex and a legal fan**, chosen before any colouring. Then **every admitted colouring** must have a finite mixed path to some target hole. Slides may leave $v$ and may change the degree of the hole. Where this page differs from that review, it says so: see Remark 2.3, which shows that letting the pair depend on the whole family of inductive colourings is *equivalent*, not weaker.

---

## 1. Definitions

### 1.1 Triangulations, links, fans

A **spherical triangulation** is a simple graph $T$ on $n\ge4$ vertices with a fixed embedding in the sphere in which every face is a triangle. Then $|E|=3n-6$. Colours are $\{0,1,2,3\}$. A **colouring** of a graph always means a proper colouring with these four colours.

**Lemma 1.1 (links).** Let $T$ be a spherical triangulation and $v$ a vertex of degree $d$. The neighbours of $v$, in rotation order $x_0,\dots,x_{d-1}$, are distinct, and $x_jx_{j+1}\in E(T)$ for every $j$ (indices mod $d$). Call this cycle $C_v$, the **link**. In the embedding, the closed star of $v$ is one side of $C_v$. Every edge of $T$ joining two non-consecutive vertices of $C_v$ lies on the other side, so these edges, the **existing chords**, are pairwise non-crossing.

*Proof.* The neighbours are distinct because $T$ is simple. The faces at $v$ are the triangles $v\,x_j\,x_{j+1}$, so $x_jx_{j+1}$ is an edge. The open star of $v$ is the union of these faces with the open edges $vx_j$ and $v$ itself. An edge $x_ix_k$ with $k\ne i\pm1$ is not an edge of any face at $v$, so its interior lies outside the closed star, in the open disk $D$ bounded by $C_v$ on the far side. Two such edges whose endpoints alternate on $C_v$ would be two arcs in the disk $D$ joining alternating boundary points. By the Jordan curve theorem they meet in an interior point, which contradicts the embedding. ∎

For $\deg v=5$, a **chord** is a pair $x_ix_{i+2}$ (indices mod 5). There are five: $02,13,24,30,41$. The **fans** are
$$\tau_i=\{x_ix_{i+2},\;x_ix_{i+3}\},\qquad i\in\mathbb Z_5,$$
with **apex** $x_i$. A fan is **legal** at $v$ if neither of its chords is an edge of $T$. For a legal fan, $T^\ast_\tau := (T-v)+\tau$, embedded by drawing the two chords inside the face $C_v$ of $T-v$.

**Lemma 1.2 (fans).**
(a) Two chords cross, meaning their endpoints alternate on $C_v$, if and only if they share no endpoint. A set of pairwise non-crossing chords has at most two elements, and a two-element set is a fan.
(b) $\tau_i\cap\tau_{i+1}=\emptyset$.
(c) If $\deg v=5$, some fan is legal at $v$.
(d) For a legal fan, $T^\ast_\tau$ is a simple spherical triangulation on $n-1$ vertices, $E(T^\ast_\tau)=E(T-v)\sqcup\tau$, and $V(T^\ast_\tau)=V(T-v)$.
(e) In $T^\ast_{\tau_i}$ the link vertices $x_{i+1}$ and $x_{i+4}$ receive no chord, so their degrees drop by exactly one. $x_{i+2}$ and $x_{i+3}$ keep their degree, and the apex gains one.

*Proof.* (a) Chords sharing an endpoint do not cross. Chord $i(i+2)$ is disjoint from exactly two chords, $(i+1)(i+3)$ and $(i+1)(i+4)$. Each has one end, $i+1$, strictly between $i$ and $i+2$ and the other end outside, so both alternate with $i(i+2)$. So the compatibility graph on the five chords joins each chord to the two chords sharing an endpoint with it. Chord $i(i+2)$ shares an endpoint with $i(i+3)$ and $(i+2)(i+4)$, and with no other chord. This compatibility graph is a 5-cycle. It has no triangle, so a compatible set has size at most 2, and its edges are the pairs $\{i(i+2),i(i+3)\}=\tau_i$.
(b) $\tau_i$ uses $02$ and $03$ when $i=0$, and $\tau_1$ uses $13,14$. These are disjoint, and the same holds after rotation.
(c) By Lemma 1.1 and (a), the existing chords form a compatible set, so they lie inside some $\tau_j$; the empty set and singletons lie in a fan too. By (b), $\tau_{j+1}$ contains no existing chord.
(d) The chords are not edges of $T$, and they join distinct vertices, so $T^\ast$ is simple. The two chords are drawn inside the pentagonal face of $T-v$ without crossing. They split it into the triangles $x_ix_{i+1}x_{i+2}$, $x_ix_{i+2}x_{i+3}$ and $x_ix_{i+3}x_{i+4}$. Every other face of $T-v$ is a face of $T$. Edge count: $3n-6-5+2=3(n-1)-6$. Also $n-1\ge4$, because $n\ge 6$ when $\deg v=5$.
(e) The chords' endpoints are $x_i$ (twice), $x_{i+2}$ and $x_{i+3}$. ∎

Correction to `hole-induction.md` line 63: two chords of a fan cover exactly **three** link vertices, not "at most four", and exactly **two** link vertices lose a degree. The conclusion drawn there is unaffected.

### 1.2 States, moves, fill

Fix a spherical triangulation $T$.

- A **state** is a pair $(h,c)$ with $h\in V(T)$ (the **hole**) and $c$ a colouring of $T-h$. Write $\Omega(T)$ for the set of states.
- A **Kempe swap** at $(h,c)$: choose colours $a\ne b$ and a connected component $K$ of the subgraph $(T-h)[a,b]$ induced on the vertices coloured $a$ or $b$. Exchange $a$ and $b$ on $K$. The hole is unchanged.
- A **singleton slide** at $(h,c)$: choose $u\in N(h)$ whose colour $\alpha=c(u)$ occurs exactly once on $N(h)$. The new state is $(u,c')$ with $c'(h)=\alpha$ and $c'=c$ on $V\setminus\{h,u\}$.
- The **fill set** is $F(T)=\{(h,c): |c(N(h))|\le 3\}$.
- The **move graph** $M(T)$ has vertex set $\Omega(T)$ and an edge for each move.

**Lemma 1.3.** (a) Both moves send states to states. (b) Every move is reversible by a move of the same kind, so $M(T)$ is an undirected graph and "reaches $F$" means "lies in a component of $M(T)$ that meets $F$". (c) If $(h,c)\in F$, then $c$ extended by a colour missing from $c(N(h))$ is a colouring of $T$.

*Proof.* (a) Kempe swap: an edge inside $K$ has ends coloured $a,b$, and they become $b,a$. An edge with one end in $K$ and the other end $y\notin K$ has $c(y)\notin\{a,b\}$, because otherwise $y$ would be in $K$; its colours stay distinct. Other edges are untouched. Slide: $c'$ is defined on $V\setminus\{u\}$. The only new colour is at $h$, namely $\alpha$. Every neighbour $w\ne u$ of $h$ has $c(w)\ne\alpha$ by uniqueness. (b) A swap is undone by swapping the same vertex set, which is again a component, because the set of $\{a,b\}$-coloured vertices and the graph they induce are unchanged. For a slide: in $(u,c')$, $c'(h)=\alpha$, and every $w\in N(u)\setminus\{h\}$ satisfies $c'(w)=c(w)\ne c(u)=\alpha$, so $\alpha$ is unique on $N(u)$. The slide $u\to h$ is legal and restores $(h,c)$. (c) This is immediate. ∎

Colours are read up to renaming where convenient. This is harmless. A global transposition of $a,b$ is the composition of the swaps of all components of $(T-h)[a,b]$, so the component of $(h,c)$ in $M(T)$ contains every renaming of $c$, and $F$ is invariant under renaming. The same argument applies inside any graph, in particular inside $T^\ast_\tau$.

### 1.3 Starts and the hypothesis

For a degree-5 vertex $v$ and a legal fan $\tau$, the **starts** are
$$S(v,\tau)=\{c:\ c \text{ a colouring of } T-v,\ c(x)\ne c(y)\text{ for each chord }xy\in\tau\}.$$
By Lemma 1.2(d), $S(v,\tau)$ is **literally the set of colourings of $T^\ast_\tau$**, since the vertex sets agree and $E(T^\ast_\tau)=E(T-v)\sqcup\tau$. The script asserts this equality at all 7,930 pairs.

- $\mathrm{VH}(v,\tau)$: every $c\in S(v,\tau)$ has $(v,c)$ joined to $F(T)$ in $M(T)$.
- $\mathrm{VH}^{\exists}(T)$: there are a degree-5 vertex $v$ and a legal fan $\tau$ at $v$ with $\mathrm{VH}(v,\tau)$.
- $\mathrm{VH}^{\exists}$: $\mathrm{VH}^\exists(T)$ for every spherical triangulation $T$ of minimum degree 5.

`hole-induction.md` assumes the strong form: every $h$, every colouring of $T-h$. That form implies $\mathrm{VH}^\exists$.

---

## 2. Theorem A: VH∃ implies 4-colourability

**Theorem A (proved).** If $\mathrm{VH}^\exists$ holds, then every spherical triangulation has a colouring.

*Proof.* Strong induction on $n$. Let $P(n)$ be the claim that every spherical triangulation on $n$ vertices has a colouring.

*Counting.* Since $\sum_v \deg v=6n-12$, we have $\sum_v(6-\deg v)=12$. So some vertex has degree at most 5, and if the minimum degree is at least 5, then $n_5\ge12$. Simplicity and $n\ge4$ give minimum degree at least 3: a vertex of degree $\le2$ lies in at most two faces, and they would have to share both edges at it, which forces a non-simple graph or $n=3$.

*Base, $n=4$.* The only spherical triangulation is $K_4$. Give its vertices four distinct colours.

*Step, $n\ge5$.* Choose $v$ of minimum degree $d\in\{3,4,5\}$. Lemma 1.1 says $T-v$ is a plane graph whose face bounded by $C_v$ is a $d$-gon and whose other faces are triangles.

**$d=3$.** $T-v$ is a simple plane graph with all faces triangles, including $C_v$. It has $n-1\ge4$ vertices, so it is a spherical triangulation. By $P(n-1)$ it has a colouring. $N(v)$ has three vertices, so a colour is free for $v$.

**$d=4$.** Let the link be $a,b,c,d$. The diagonals $ac$ and $bd$ have alternating ends, so by Lemma 1.1 at most one is an edge of $T$. Add an absent one, say $ac$, inside the face to get $T^\ast$: simple, all faces triangles, $n-1\ge4$ vertices. By $P(n-1)$ colour $T^\ast$ and restrict to $T-v$. If the link uses at most three colours, finish. Otherwise rename the colours so that the link reads $0,1,2,3$. Let $H_{13}=(T-v)[1,3]$ and $H_{02}=(T-v)[0,2]$. Note that $ac$ is not an edge of $T-v$.
- If $b,d$ lie in different components of $H_{13}$, swap the component of $b$. The link becomes $0,3,2,3$, and $v$ gets colour 1.
- Otherwise let $P$ be a $b$–$d$ path in $H_{13}$; a shortest one is simple. Then $\Gamma=v\,b\,P\,d\,v$ is a cycle of $T$, a simple closed curve in the embedding. The rotation at $v$ is $va,vb,vc,vd$, so near $v$ the curve $\Gamma$ (through $vb,vd$) has the initial segments of $va$ and $vc$ on opposite sides. The edges $va$ and $vc$ meet $\Gamma$ only at $v$, so $a$ and $c$ lie in different components of $S^2\setminus\Gamma$. A path from $a$ to $c$ in $H_{02}$ is a curve in the embedding of $T$. It avoids $v$, which is not in $T-v$, and it avoids every vertex of $P$, whose colours are 1 or 3. Edges of the embedding meet only at common endpoints, so the path is disjoint from $\Gamma$, which is impossible. So $a$ and $c$ lie in different components of $H_{02}$. Swap the component of $a$ in $T-v$. The link becomes $2,1,2,3$, and $v$ gets colour 0. The embedding used is that of $T$, with $v$ present, while the path lives in $T-v$.

**$d=5$.** Now $T$ has minimum degree 5. By $\mathrm{VH}^\exists(T)$ fix $(v_0,\tau)$, with $v_0$ of degree 5 and $\tau$ legal at $v_0$. The vertex $v_0$ need not be the $v$ chosen above; any degree-5 vertex will do. By Lemma 1.2(d), $T^\ast_\tau$ is a spherical triangulation on $n-1$ vertices. By $P(n-1)$ it has a colouring $c$, and $c\in S(v_0,\tau)$. By $\mathrm{VH}(v_0,\tau)$ there is a path in $M(T)$ from $(v_0,c)$ to some $(h,c_h)\in F$. By Lemma 1.3(c), $T$ has a colouring. ∎

**Remark 2.1 (why the hypothesis is applied to $T$ and not to $T^\ast$).** The inductive call colours $T^\ast_\tau$, which has $n-1$ vertices. The hypothesis is applied once, to $T$, and is never proved. $T^\ast_\tau$ always has two vertices whose degree dropped (Lemma 1.2(e)). If either had degree 5, then $T^\ast_\tau$ has minimum degree $\le4$ and is outside the class of the hypothesis; on the icosahedron this happens at every pair. So an induction restricted to minimum degree 5 does not close, which is `hole-induction.md`'s point and is correct. The later states of the path, with holes at other vertices and of any degree, are states of $T$ on $n$ vertices. Applying the hypothesis or the inductive claim to them would be circular.

**Remark 2.2 (where $P(n-1)$ is really used).** Only to know $S(v_0,\tau)\neq\emptyset$. $\mathrm{VH}(v_0,\tau)$ is a universally quantified statement. If $S$ were empty it would hold vacuously and give nothing. So the induction supplies one start, and the content of $\mathrm{VH}^\exists$ is that *every* start reaches $F$. The weaker claim "some $c\in S(v_0,\tau)$ reaches $F$" already implies that $T$ is 4-colourable, so it cannot serve as an assumption that is easier than the conclusion.

**Remark 2.3 (letting the pair depend on the colourings changes nothing).** The induction actually colours every $T^\ast_\tau$ at once, one for each legal pair. One could therefore assume only $\mathrm{VH}^{\mathrm{fam}}(T)$: for every family $(c_{v,\tau})$ with $c_{v,\tau}\in S(v,\tau)$, some pair has $(v,c_{v,\tau})$ reaching $F$. This suffices for Theorem A by the same proof. It is **equivalent** to $\mathrm{VH}^\exists(T)$. ($\Leftarrow$) is clear. ($\Rightarrow$): if every pair $p$ had a start $c_p$ not reaching $F$, the family $(c_p)$ would violate $\mathrm{VH}^{\mathrm{fam}}$; the pairs are finitely many and are chosen independently. So the review's warning stands in substance. Selecting the pair after one colouring is not available, and selecting it after all of them gains nothing.

**Review of `hole-induction.md`.** No logical flaw was found. The deduction is sound for the strong hypothesis it states, and, re-derived above, for $\mathrm{VH}^\exists$. Imprecisions:
1. Line 63, as corrected after Lemma 1.2: a fan covers three link vertices, and exactly two lose degree.
2. Line 59 chooses the fan $\tau_{j+1}$. Under $\mathrm{VH}^\exists$ the fan, and the vertex, must be the ones the hypothesis supplies. Any legal fan gives a valid $T^\ast$, so this is a change of wording, not a gap.
3. Lines 53–54 do not say that $n-1\ge4$, which is needed for $T-v$ or $T^\ast$ to be a spherical triangulation. It holds because $n\ge5$ in the step.
4. The Hypothesis section quantifies over every $h$ and every colouring. The proof uses only starts at one degree-5 vertex, admitted by one fan, which is the slack $\mathrm{VH}^\exists$ removes.
5. The degree-4 Jordan argument (lines 85–87) is correct. It should say explicitly that $\Gamma$ is drawn in the embedding of $T$, not of $T-v$, and that $P$ may be taken simple. Both points are written into the proof above.

---

## 3. The two lemmas

**Lemma 3.1 (containment; proved).** Let $\tau$ be legal at $v$, and let $c,c'\in S(v,\tau)$ be Kempe-equivalent in $T^\ast_\tau$, that is, joined by a sequence of Kempe swaps of $T^\ast_\tau$. Then $c$ and $c'$ are Kempe-equivalent in $T-v$, and $(v,c),(v,c')$ lie in the same component of $M(T)$. Hence reachability of $F$ is constant on each Kempe class of $T^\ast_\tau$.

*Proof.* It suffices to treat one swap of $T^\ast_\tau$, on colours $a,b$ and a component $K$ of $T^\ast_\tau[a,b]$. The vertex sets of $T-v$ and $T^\ast_\tau$ agree, and $E(T-v)\subseteq E(T^\ast_\tau)$. The two graphs $(T-v)[a,b]$ and $T^\ast_\tau[a,b]$ therefore have the same vertex set, and the first is a spanning subgraph of the second. Each component of the first lies inside one component of the second. So $K=K_1\sqcup\dots\sqcup K_r$ with each $K_j$ a component of $(T-v)[a,b]$. Swap $K_1$, then $K_2$, and so on. After swapping $K_1,\dots,K_{j-1}$, the set of vertices coloured $a$ or $b$ is unchanged. So $(T-v)[a,b]$ is the same graph, and $K_j$ is still one of its components. Each step is therefore a legal Kempe swap of $T-v$, a move of $M(T)$ at hole $v$. The composite exchanges $a,b$ on exactly $K$. ∎

*Subtleties.*
1. The chords are non-edges of $T$ because the fan is legal. If a chord were an edge of $T$, then $T^\ast$ would not be simple and $E(T-v)$ would already contain it. Nothing would break, but Lemma 1.2(d) needs legality.
2. The intermediate colourings are proper on $T-v$ but may be improper on a chord. They are states of $T$, not colourings of $T^\ast$. This is allowed, because moves are defined in deletions of $T$.
3. The converse fails. A swap of $T-v$ whose component contains one end of a chord, and whose chord partner has the other colour, makes the chord monochromatic and leaves $S(v,\tau)$. Kempe classes of $T-v$ are unions of (restricted) $T^\ast$-classes together with colourings outside $S$.
4. Canonical colours (§1.2): a renaming is a product of swaps inside $T^\ast_\tau$ as well, so classes up to renaming behave the same way.
5. Components are read in $T-v$. The machine check confirms that each of the $T^\ast$ classes at all 7,930 pairs lies inside a single $T-v$ class (`containment_fail = 0`).

**Lemma 3.2 (apex singleton; proved).** If $c\in S(v,\tau_i)$, then $c(x_i)$ occurs exactly once on $N(v)$, so the slide $v\to x_i$ is legal at every start.

*Proof.* $x_ix_{i\pm1}$ are edges of $T-v$ (Lemma 1.1), so $c(x_i)\ne c(x_{i\pm1})$. Since $c$ is proper on $\tau_i$, $c(x_i)\ne c(x_{i+2}),c(x_{i+3})$. The five link vertices are distinct. ∎

*Subtleties.* After the slide, the hole is $x_i$, of degree $\deg_T(x_i)$. That may be 6 or more, because the apex is not constrained. The slide need not fill. If $|c(N(v))|=3$, then $c$ already fills, and the apex is the *only* singleton: the 3-colour pattern on a 5-cycle is $(2,2,1)$. If $|c(N(v))|=4$, the pattern is $(2,1,1,1)$, with three singletons. The machine check asserts the lemma at every start of every pair.

**Corollary 3.3 (the shape of a fill inside $S$; proved).** For $c\in S(v,\tau_i)$, $(v,c)\in F$ if and only if $c(x_{i+1})=c(x_{i+3})$ and $c(x_{i+2})=c(x_{i+4})$.

*Proof.* ($\Leftarrow$) The link colours lie in $\{c(x_i),c(x_{i+1}),c(x_{i+2})\}$. ($\Rightarrow$) By Lemma 3.2, $c(x_i)$ is unique, so the path $x_{i+1}x_{i+2}x_{i+3}x_{i+4}$ is properly coloured with at most two colours and must alternate. ∎

---

## 4. Reformulations

### 4.1 Component form

**R0 (proved, by Lemma 1.3(b)).** $\mathrm{VH}(v,\tau)$ holds if and only if every component of $M(T)$ that meets $\{(v,c):c\in S(v,\tau)\}$ meets $F$.

### 4.2 (i) Kempe classes of $T^\ast_\tau$

**R1 (proved).** $\mathrm{VH}(v,\tau)$ holds if and only if every Kempe class $\mathcal K$ of $T^\ast_\tau$ contains a colouring $c$ with $(v,c)$ joined to $F$ in $M(T)$.

*Proof.* ($\Rightarrow$) Take any $c\in\mathcal K$; it is a start. ($\Leftarrow$) Let $c\in S(v,\tau)$ and let $\mathcal K$ be its $T^\ast$-class. Pick $c'\in\mathcal K$ with $(v,c')$ joined to $F$. Lemma 3.1 joins $(v,c)$ to $(v,c')$. ∎

So $\mathrm{VH}(v,\tau)$ needs to be checked on **one representative per Kempe class of the smaller triangulation $T^\ast_\tau$**. Three natural strengthenings of "contains a colouring that reaches $F$" are:

- **KT\*$(v,\tau)$**: every $T^\ast_\tau$-class contains $c$ with $(v,c)\in F$. Equivalently, by Cor. 3.3, every class contains a colouring with $c(x_{i+1})=c(x_{i+3})$ and $c(x_{i+2})=c(x_{i+4})$. This is a statement about the Kempe classes of the triangulation $T^\ast_\tau$ alone. **Refuted**, even in its $\exists$ form. On the icosahedron (12:0) it fails at all 60 pairs: each $T^\ast$ has 2 classes and one of them contains no fill. Sixteen of the 118 graphs have no pair satisfying it: 12:0, 15:0, 16:2, 17:0, 17:3, 18:1, 18:8, 19:18, 20:7, 20:12, 20:16, 20:60, 20:62, 20:64, 20:65, 20:69 (`vh-exists-check.txt`, `KTstar_fail_pairs` equal to `pairs`). The lesson is the one the degree-4 step already teaches: the useful swap must be performed in $T-v$, where it may break a chord, not in $T^\ast$.
- **U$(v,\tau)$ ("unlocking")**: every $T^\ast_\tau$-class contains a colouring $c$ such that $(v,c)\in F$, or one Kempe swap of $T-v$ takes $(v,c)$ into $F$. By `fan-link.md`, $c$ fails this exactly when it is **locked**. Then the link is $(\alpha,\beta,\alpha,\gamma,\delta)$ in some rotation and reflection, with the $\beta$-vertex $p_1$ between the two $\alpha$'s and $p_3,p_4$ the $\gamma,\delta$ vertices, and in $T-v$ there are both a $\beta\gamma$-path $p_1\to p_3$ and a $\beta\delta$-path $p_1\to p_4$. U is a sufficient condition for $\mathrm{VH}(v,\tau)$ (by R1). It is discussed in §5 as the most promising reformulation.
- **Swap-only VH$(v,\tau)$**: every $T-v$ Kempe class that meets $S(v,\tau)$ contains a fill state at $v$. This is §4.4.

**Proposition 4.1 (fills inside $S$, double identification; proved).** Let $T_i$ be the graph obtained from $T-v$ by identifying $x_{i+1}$ with $x_{i+3}$ and $x_{i+2}$ with $x_{i+4}$ (loops are not allowed: if a pair is adjacent in $T$, call $T_i$ not colourable). Then $F\cap S(v,\tau_i)\ne\emptyset$ if and only if $T_i$ has a colouring.

*Proof.* By Cor. 3.3, the fills in $S$ are the colourings of $T-v$ that are proper on $\tau_i$ and constant on both pairs. Properness on $\tau_i$ is then automatic: $x_ix_{i+2}$ inherits the inequality from the edge $x_ix_{i+4}$, and $x_ix_{i+3}$ from $x_ix_{i+1}$. Colourings of $T-v$ constant on the two pairs are exactly the colourings of $T_i$. ∎

The first identification can be drawn in the face $C_v$, so it is planar. After it, $x_{i+2}$ and $x_{i+4}$ lie on different sides of the new curve, so the second identification is in general not planar. This is the classical reason Kempe's contraction trick gives five colours and not four. **Example (refutes "$F\cap S\neq\emptyset$ at every pair"):** 17:0 at $(v,\tau)=(4,\tau_4)$ and $(6,\tau_1)$, and 17:1 at $(7,\tau_4)$ and $(13,\tau_2)$. At these pairs $S$ contains no fill, so $T_i$ has no colouring, although neither identified pair is an edge of $T$ (checked). $\mathrm{VH}$ still holds there, but only through states outside $S$. Every path to $F$ must break a chord or move the hole.

### 4.3 (ii) Relation to Gate-D

**KD$(v)$** (the old Gate-D statement at $v$): every Kempe class of colourings of $T-v$, under swaps of $T-v$, contains a colouring with at most three link colours.

**Proposition 4.2 (proved).**
(a) KD$(v)$ ⇒ swap-only VH$(v,\tau)$ for every legal $\tau$ ⇒ VH$(v,\tau)$.
(b) If $C_v$ is induced, so that all five fans are legal, then KD$(v)$ ⇔ swap-only VH$(v,\tau)$ for all five $\tau$.
(c) The converse of (a) at a single $(v,\tau)$ is not a theorem. VH allows slides and only concerns classes that meet $S(v,\tau)$.

*Proof.* (a) A start $c\in S$ lies in some $T-v$ class, which contains a fill by KD. (b) ($\Leftarrow$) By `fan-link.md` every proper colouring of a 5-cycle is proper on some fan: the $(2,2,1)$ orbit on the fan at its unique colour, and the $(2,1,1,1)$ orbit $(\alpha,\beta,\alpha,\gamma,\delta)$ on $\tau$ at positions 1, 3, 4. Re-check directly: apex $p_1$ is coloured $\beta$, and its chord ends $p_3,p_4$ are $\gamma,\delta$. Apex $p_3$ ($\gamma$) has chord ends $p_0,p_1$, coloured $\alpha,\beta$. Apex $p_4$ ($\delta$) has chord ends $p_1,p_2$, coloured $\beta,\alpha$. So every colouring of $T-v$ is a start for some legal fan, and its class meets that $S$. ∎

Data: on all 118 graphs, KD$(h)$ holds at **every** hole $h$ of every degree, 5 to 9 (`deg5_KD_bad = high_KD_bad_classes = 0`). Kempe classes do split at degree-5 holes: 2 classes at 6 holes of 18:1, 2 of 18:6, 16 of 20:64 and 16 of 20:69. Each class still contains a fill. As WP18 already said, orders up to 20 cannot separate KD from VH, and cannot falsify either.

**Trap.** "$T-v$ is a single Kempe class" does not imply VH. One also needs the class to contain a fill, and the existence of a fill state anywhere in $\Omega(T)$ is equivalent to $T$ being 4-colourable. Any reformulation that splits into "connectivity" plus "a target exists" has put the whole theorem into the second half.

### 4.4 (iii) What slides add

**Proposition 4.3 (fifth-colour picture; proved).** Identify the state $(h,c)$ with the 5-colouring $\hat c$ of $T$ given by $\hat c(h)=4$ and $\hat c=c$ elsewhere. Let $\mathrm{Col}_k$ be the set of 5-colourings of $T$ in which colour 4 is used exactly $k$ times. Then:
(a) the states are exactly $\mathrm{Col}_1$;
(b) the edges of $M(T)$ are exactly the single Kempe swaps of $T$, on 5-colourings, that start and end in $\mathrm{Col}_1$; slides are the swaps on a pair $\{\alpha,4\}$ whose component is a single edge $\{h,u\}$;
(c) $(h,c)\in F$ if and only if some Kempe swap takes $\hat c$ into $\mathrm{Col}_0$;
(d) $\mathrm{VH}(v,\tau)$ holds if and only if each start $\hat c$ is joined to $\mathrm{Col}_0$ by Kempe swaps of $T$ that stay inside $\mathrm{Col}_0\cup\mathrm{Col}_1$.

*Proof.* (a) is clear. (b) A swap on $\{a,b\}\subseteq\{0,..,3\}$ never involves $h$, and $T[a,b]=(T-h)[a,b]$, so these are the 4-colour swaps. On $\{\alpha,4\}$, the component of $h$ consists of $h$ and its $\alpha$-neighbours. Each $\alpha$-neighbour's only colour-4 neighbour is $h$, so the component is a star. Swapping it puts colour 4 on the $\alpha$-neighbours of $h$, and the result lies in $\mathrm{Col}_1$ exactly when there is one such neighbour, which is a slide. Any other $\{\alpha,4\}$-component is a single $\alpha$-vertex not adjacent to $h$, and swapping it creates a second colour-4 vertex. (c) $\mathrm{Col}_0$ is reached only by swapping $h$'s $\{\alpha,4\}$-component when $h$ has no $\alpha$-neighbour, that is, when $\alpha\notin c(N(h))$. (d) ($\Rightarrow$) Follow a path to $F$, then apply (c). ($\Leftarrow$) The first entry into $\mathrm{Col}_0$ comes from a state in $F$, by (c). ∎

So VH is Meyniel's theorem (all 5-colourings of a planar graph are Kempe-equivalent) **restricted to the stratum where the fifth colour is used at most once**. As `LibraryPlan.md` says, Meyniel's paths leave that stratum, so the theorem does not apply.

**Proposition 4.4 (last-slide elimination; proved).** If the slide $(h,c)\to(u,c')$ lands in $F$, then $(h,c)\in F$, or one Kempe swap of $T-h$, recolouring only $u$, takes $(h,c)$ into $F$. The two fills give the same colouring of $T$.

*Proof.* Let $\alpha=c(u)$ and let $\beta\notin c'(N(u))$. Since $c'(h)=\alpha$, we have $\beta\ne\alpha$. In $T-h$ the vertex $u$ has no neighbour coloured $\beta$ (fill condition) or $\alpha$ (properness). So its $\{\alpha,\beta\}$-component is $\{u\}$, and swapping it sets $c''(u)=\beta$. Because $\alpha$ was unique on $N(h)$, $c''(N(h))=(c(N(h))\setminus\{\alpha\})\cup\{\beta\}$. If $\beta\in c(N(h))$, this has at most 3 colours. If not, $(h,c)$ was already in $F$. Filling $h$ with $\alpha$ gives $c'$ plus $\beta$ at $u$. ∎

*Consequences.* A shortest path to $F$ can be taken to end in a Kempe swap, or to have length 0. A path of $k$ slides alone can be replaced by $k-1$ slides and one single-vertex swap. As a check, the "one-mixed-move" and "one-Kempe-move" versions of U agree at all 7,930 pairs (`pairs_U_fail = pairs_Umixed_fail = 41`), which this proposition predicts.

**Proposition 4.5 (one-swap excursions; proved).** Suppose a slide $h\to u$, one Kempe swap $\sigma$ at hole $u$, and a slide $u\to h$ are legal in that order. Then the net change of the colouring of $T-h$ is a composition of Kempe swaps of $T-h$ on a single colour pair.

*Proof.* Let $\alpha=c(u)$, and let $c_1$ be the state after the first slide ($c_1(h)=\alpha$). Let $\sigma$ swap $\{a,b\}$ on a component $K$ of $(T-u)[a,b]$. Recall that $c_1=c$ on $V\setminus\{h,u\}$, and that no $w\in N(u)\setminus\{h\}$ has colour $\alpha$.
*Case $\alpha\notin\{a,b\}$.* Then $h\notin K$, and $u$ is not $\{a,b\}$-coloured under $c$. So $(T-u)[a,b]$ under $c_1$ and $(T-h)[a,b]$ under $c$ are the same graph on $V\setminus\{h,u\}$, and $\sigma$ is a swap of $T-h$. The return slide is legal and restores $u$ to $\alpha$.
*Case $a=\alpha$, $h\notin K$.* Vertices of $K$ adjacent to $u$ are coloured $b$ (they cannot be $\alpha$), and they become $\alpha$. The return slide needs $\alpha$ to be unique on $N(u)$, where $h$ already has $\alpha$. So legality forces $K$ to have no neighbour of $u$. Then $K$ is also closed in $(T-h)[\alpha,b]$ under $c$, and $\sigma$ is a swap of $T-h$.
*Case $a=\alpha$, $h\in K$.* After $\sigma$, $h$ has colour $b$. The return slide needs $b$ unique on $N(u)$. Since $h\in N(u)$ is now $b$, every other $b$-neighbour of $u$ after $\sigma$ must be absent. A neighbour $w\ne h$ of $u$ that was $b$ before $\sigma$ and outside $K$ would remain $b$, so every $b$-neighbour of $u$ other than $h$ lies in $K$. After returning, the colouring of $T-h$ is $c$ with $\alpha\leftrightarrow b$ exchanged on $K\setminus\{h\}$, and with $u$ changed from $\alpha$ to $b$. Let $K'=(K\setminus\{h\})\cup\{u\}$. In $(T-h)[\alpha,b]$ under $c$, every $\{\alpha,b\}$-neighbour of a vertex in $K\setminus\{h\}$ lies in $K$ or is $u$, and every $b$-neighbour of $u$ lies in $K\setminus\{h\}$. So $K'$ is a union of components, and swapping it is a composition of swaps, as in Lemma 3.1. ∎

**Answer to (iii).** Taken literally, "a slide can be simulated by Kempe swaps plus re-choosing the hole" is **false**: a slide changes the hole, and Kempe swaps never do. The only other way to change the hole is to fill and then delete a different vertex, which needs a complete colouring, and once a complete colouring exists nothing further is needed. Read as a statement about reaching $F$, three things are proved: a final slide is never needed (4.4); a slide out and back around one swap is swap-equivalent (4.5); and slides are exactly the single-edge fifth-colour swaps (4.3). The general statement **SW = MX**, that a state reaching $F$ by mixed moves reaches it by swaps alone at the same hole, is **open**. No separating example can exist on the checked graphs, because KD holds at every hole there. Excursions with two or more swaps fail in the proof of 4.5, because the intermediate swaps may break the uniqueness that the return slide needs.

### 4.5 (iv) Self-reducing hypotheses, and the circularity traps

A self-reducing route would replace "assume $\mathrm{VH}^\exists$" by a statement $Q(T)$, for all spherical triangulations, such that $Q$ for smaller graphs implies $Q(T)$ and $Q(T)$ implies $\mathrm{VH}^\exists(T)$.

**Obstruction 1 (class).** $Q$ cannot be restricted to minimum degree 5. $T^\ast_\tau$ leaves that class whenever a degree-5 vertex misses the fan (Remark 2.1).

**Obstruction 2 (the object changes).** VH speaks about colourings of $T-v$ and moves in deletions of $T$. A statement about $T^\ast_\tau$ speaks about colourings proper on the chords and moves in deletions of $T^\ast_\tau$. Lemma 3.1 transfers $T^\ast$ **Kempe swaps** into $M(T)$. It does not transfer $T^\ast$ **states with a hole**, since a hole $h'$ in $T^\ast$ is a two-hole object $\{v,h'\}$ in $T$, nor $T^\ast$ **slides**, because links in $T^\ast$ include chord neighbours. The only part of $T^\ast$ that transfers is its Kempe-class structure, and the purely-$T^\ast$ target statement KT\* is refuted (§4.2).

**Candidate $H(T)$:** for every vertex $h$, every Kempe class of $T-h$ contains a fill state. This is KD at every hole, and it implies $\mathrm{VH}^\exists(T)$ and the strong VH.

**Lemma 4.6 (lifting through degree $\le3$; proved).** Let $G$ be a graph, $w\in V(G)$ with $\deg_G w\le3$, and $c$ a colouring of $G$. If $d'$ is obtained from $c|_{G-w}$ by one Kempe swap of $G-w$, then at most two Kempe swaps of $G$ take $c$ to some $d$ with $d|_{G-w}=d'$.

*Proof.* Let the swap be on $\{a,b\}$ and the component $K$. If $c(w)\notin\{a,b\}$, then $K$ is a component of $G[a,b]$; swap it. Otherwise say $c(w)=a$. If no vertex of $K$ is adjacent to $w$, then $K$ is a component of $G[a,b]$. If some colour $e\notin\{a,b\}$ is missing from $N(w)$, recolour $w$ to $e$; this is the swap of the $\{a,e\}$-component $\{w\}$. Then $K$ is a component of $G[a,b]$; swap it. Otherwise $N(w)$ uses both colours outside $\{a,b\}$ and also meets $K$ in a $b$-vertex $y$ (it cannot meet $K$ in an $a$-vertex). Since $\deg w\le3$, $y$ is the only $\{a,b\}$-neighbour of $w$. So the component of $w$ in $G[a,b]$ is $K\cup\{w\}$; swap it. ∎

**Proposition 4.7 ($H$ descends through degree-3 vertices; proved).** If $T$ has a vertex $w$ of degree 3, $n\ge5$, and $H(T-w)$ holds, then $H(T)$ holds.

*Proof.* For the hole $h=w$, the link is a triangle, so every state is a fill. For $h\ne w$: $T-w$ is a spherical triangulation (§2, $d=3$). Apply $H(T-w)$ to the restriction of $c$ to $T-w-h$, and lift each swap by Lemma 4.6 with $G=T-h$ ($\deg_G w\le3$). The result $d$ has at most 3 colours on $N_{T-w}(h)$. If $w\notin N(h)$, we are done. If $w\in N(h)$, then $N_T(w)=\{h,p,q\}$ with $p,q\in N(h)$. If $d(N_{T-w}(h))$ has at most 2 colours, the link in $T$ has at most 3. Otherwise it has exactly 3, and one of them, $e$, is not in $\{d(p),d(q)\}$. If $d(w)$ is one of those three colours, we are done. If not, then $d(w)\ne e$, and $w$'s $\{d(w),e\}$-component in $T-h$ is $\{w\}$, because its only neighbours there are $p,q$; swap it. Then the link of $h$ uses 3 colours. ∎

The same lifting **fails at degree 4**. Take $w$ coloured $a$ with neighbours coloured $b,e_1,b,e_2$, and $K$ containing exactly one of the two $b$-neighbours. Then the $G[a,b]$-component of $w$ contains both, and $w$ has no free colour. Whether a longer sequence lifts the swap is a 4-colour Kempe question of the original kind. So $H$ is self-reducing only through degree 3. For degrees 4 and 5 the 4CT induction replaces $T$ by $T^\ast$, not by $T-v$, and $H(T^\ast)$ speaks about colourings proper on the added diagonal, which $T-h$ colourings need not be (Obstruction 2). **Status: $H$ as a self-reducing hypothesis is open, and the natural reduction fails at degree 4.**

**Circularity traps** (each one is a way to prove nothing):
1. Applying VH, or the inductive claim, to a later state $(h,c)$ of the same $T$. This is the circular variant in `hole-induction.md`, and it is correct there.
2. "Every class contains a target" with target existence left implicit. A fill anywhere in $\Omega(T)$ is equivalent to $\chi(T)\le4$ (§4.3 Trap).
3. Using a colouring of $T_i$ (Prop. 4.1) as if $T_i$ were a smaller planar triangulation. It is generally non-planar, and 17:0 and 17:1 show it can have no colouring at all.
4. Treating orders up to 20 as evidence for VH∃, KD or $H$. All three hold there, at every hole, and the move graph $M(T)$ is connected on all 118 graphs (`Mcomp=1`). These orders cannot fail VH∃.
5. Selecting $(v,\tau)$ after seeing one colouring (review). Remark 2.3 shows that the family version is equivalent to VH∃, so there is no hidden gain.
6. Citing Meyniel (Prop. 4.3): its paths leave $\mathrm{Col}_{\le1}$.

Remark on the classical route. The proofs that close (Birkhoff, Heesch, Appel–Haken, Robertson–Sanders–Seymour–Thomas) strengthen the hypothesis to "a minimal counterexample contains no reducible configuration", which is a self-reducing statement, and they use many configurations. VH∃ uses the single configuration "one degree-5 vertex". It gets past the failure of the one-swap argument at that configuration (Heawood's objection to Kempe; the dipyramid colouring in `fan-link.md`) only by allowing unboundedly long, non-local paths: Kempe chains anywhere, and slides that leave the ring. Any proof of VH∃ must therefore use information beyond the colouring of the ring and the chain pattern of a single swap. This page does not determine the D-reducibility status of that configuration; it only notes that every proof restricted to such ring data stops at the locked case.

---

## 5. Open sub-statements, with status

The orders checked are 12–20 (118 graphs). "Holds ≤20" is a fact about those graphs, not evidence. Items marked *post hoc* were formulated after looking at the same data.

| # | Statement | Status | Where |
|---|---|---|---|
| 1 | VH∃ ⇒ every spherical triangulation is 4-colourable | **proved** | Thm A |
| 2 | Containment: reachability constant on $T^\ast_\tau$ Kempe classes | **proved** | Lemma 3.1 |
| 3 | Apex singleton | **proved** | Lemma 3.2 |
| 4 | VH$(v,\tau)$ ⇔ every $T^\ast_\tau$ class has a member reaching $F$ | **proved** | R1 |
| 5 | Family version ⇔ VH∃ | **proved** | Remark 2.3 |
| 6 | KD$(v)$ ⇒ VH$(v,\tau)$ for all $\tau$; with $C_v$ induced, KD$(v)$ ⇔ swap-only VH at all 5 fans | **proved** | Prop 4.2 |
| 7 | Slides are the single-edge $\{\alpha,4\}$ swaps; VH is Meyniel restricted to $\mathrm{Col}_{\le1}$ | **proved** | Prop 4.3 |
| 8 | Last slide eliminable; one-swap excursions are swap-equivalent | **proved** | Props 4.4, 4.5 |
| 9 | $F\cap S(v,\tau_i)\ne\emptyset$ ⇔ $T_i$ 4-colourable | **proved** | Prop 4.1 |
| 10 | $F\cap S(v,\tau)\ne\emptyset$ at every legal pair | **refuted** | 17:0 $(4,\tau_4),(6,\tau_1)$; 17:1 $(7,\tau_4),(13,\tau_2)$; `vh-exists-check.txt` |
| 11 | KT\*: some pair at which every $T^\ast$ class contains a fill in $S$ | **refuted** | 12:0 (icosahedron) and 15 more graphs; `vh-exists-check.txt` |
| 12 | U∃: some pair at which every $T^\ast_\tau$ class contains an unlocked colouring | **open**; holds on all 118 graphs (post hoc) | `vh-exists-check.txt` |
| 13 | U at every pair | **refuted** | 41 pairs on 17:0, 17:1, 20:12, 20:24 |
| 14 | SW = MX: mixed-reachable ⇒ swap-reachable at the same hole | **open**; no separation possible ≤20 | §4.4 |
| 15 | $H(T)$, KD at every hole of every triangulation | **open**; holds ≤20 at every hole, degrees 5–9; descends through degree 3 (Prop 4.7); reduction fails at degree 4 | §4.5 |
| 16 | Bounded length: some pair with every start ≤2 moves | **refuted** | 17:1, `../WP18-results.md`, `../wp18/kill-check-17-1.txt` |
| 17 | Bounded length: every start ≤4 moves at every pair | **open**; producer claim through order 22, upper bounds not certified, observed after the run | `../WP18-results.md` |
| 18 | A degree-5 apex (a degree-5 vertex adjacent to $v$, used as apex) always attains $m(T)$ | **refuted** (secondary orders) | 20:30, 20:31, 20:49 in `../wp18/wp18-P2.json`: $m=1$, best degree-5-apex pair $L=2$ |
| 19 | VH∃ restricted to triangulations in which some degree-5 vertex has a degree-5 neighbour, choosing $v$ to be such a vertex | **open**; no hand argument found | — |

**Most promising: item 12, U∃.** It is the exact degree-5 analogue of the degree-4 step. At degree 4, the Jordan curve theorem shows that **every** colouring of $T^\ast$ is unlocked: one swap in $T-v$ frees a colour. At degree 5, locked colourings exist (`fan-link.md`'s dipyramid), so U asks only that each **Kempe class of the smaller triangulation $T^\ast_\tau$** contain an unlocked member. By R1 and Lemma 3.1 this implies VH$(v,\tau)$, and with Theorem A it would imply 4-colourability. It needs no slides, by Prop 4.4. It is a statement about $T^\ast_\tau$ classes together with two chain-connectivity conditions in $T-v$, so a proof could combine Kempe-class structure on the smaller graph with Jordan-curve arguments at the link. Unlike VH∃, U∃ **can fail at small orders**. It is refuted at 41 individual pairs, yet every graph has a good pair, including 17:1, where $m(T)=3$ (38 of 60 pairs satisfy U). It survives a test that VH∃ cannot be put to, but it was formulated after the data were seen. Testing it fairly needs a declaration and fresh orders (21 and up). Nothing above order 20 was run for this page.

Natural next hand questions for U: (a) characterise the locked colourings that are alone in their $T^\ast_\tau$ class. A locked $c$ has both chains through $p_1$. A $T^\ast$ swap of the $\{\gamma,\delta\}$-component through $p_3p_4$ yields $(\alpha,\beta,\alpha,\delta,\gamma)$, and the chains then run to swapped ends. Which $T^\ast$ swaps preserve lockedness? (b) Explain the 41 failing pairs. All of them lie on 17:0, 17:1, 20:12 and 20:24, two of which are the graphs where $F\cap S=\emptyset$ (item 10).

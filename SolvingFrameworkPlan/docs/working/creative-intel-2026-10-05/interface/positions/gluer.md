# Interior-witness lift

Gluer, Interface team, Creative Intel. 5 October 2026.

Hand line-check of one lift. No graph is generated and no census is run.

**[hand]** No sentence below breaks. Under (8)–(11), the pair $(r,\tau)$ is a good pair of $T$.

Sources, by path:

- `SolvingFrameworkPlan/docs/reports/TriangleSumM3Family.md`, the component-restriction paragraph (lines 15–23) and the upper-bound lift (lines 52–56).
- `SolvingFrameworkPlan/docs/working/VHExistsMinimalCounterexample.md`, the interior-witness section (lines 33–43) and next check 1 (line 155).
- `backgroundMaterial/planemap-structural/longtable/swarm/vh-exists.md`, Lemma 1.3 (lines 48–50) and Lemma 3.2 (lines 116–118).

Colours are $\{0,1,2,3\}$. The letter $F$ is the separating triangle. The fill set is written out in words, so it does not share that letter.

## Vocabulary

**(1) [hand]** A state of a graph $G$ is a pair $(h,c)$ with $h\in V(G)$ and with $c$ a proper colouring of $G-h$.

**(2) [hand]** A Kempe swap at $(h,c)$ selects colours $a\neq b$ and one connected component of the bichromatic subgraph $(G-h)[a,b]$, exchanges $a$ and $b$ on that component, and leaves the hole at $h$.

**(3) [hand]** A singleton slide at $(h,c)$ selects $u\in N_G(h)$ whose colour $\alpha=c(u)$ occurs once on $N_G(h)$, and moves to the state $(u,c')$ with $c'(h)=\alpha$ and with $c'(x)=c(x)$ for every $x\in V(G)\setminus\{h,u\}$.

**(4) [hand]** The fill set of $G$ is the set of states $(h,c)$ with $|c(N_G(h))|\le 3$.

**(5) [hand]** Lemma 1.3 of `backgroundMaterial/planemap-structural/longtable/swarm/vh-exists.md` says that both moves send states to states, that each move is reversible by a move of the same kind, and that a state in the fill set extends by a colour missing on the neighbourhood of the hole to a proper colouring of $G$.

**(6) [hand]** A pair $(v,\tau)$ is a good pair of a spherical triangulation $G$ when $\deg v=5$, the fan $\tau$ is legal at $v$, and every colouring of $G-v$ that is proper on the two chords of $\tau$ reaches the fill set of $G$ by Kempe swaps and singleton slides.

**(7) [hand]** By Lemma 1.3(b) in that file, the move graph is undirected, so a forward walk of moves places its ends in one component.

## Hypotheses

**(8) [hand]** Let $T$ be a spherical triangulation and let $F$ be a separating triangle, with $T=A\cup B$, $A\cap B=F$, and with no edge from $A\setminus F$ to $B\setminus F$.

**(9) [hand]** The union is the graph union, so $V(T)=V(A)\cup V(B)$ and $E(T)=E(A)\cup E(B)$, with $V(A)\cap V(B)=F$.

**(10) [hand]** Let $r\in A\setminus F$ have degree 5 in $A$, and let $\tau$ be a legal fan at $r$ in $A$.

**(11) [hand]** Suppose every colouring of $A-r$ that is proper on $\tau$ has a filling path in the move graph of $A$ whose every hole lies in $A\setminus F$; this is the interior-witness hypothesis of `SolvingFrameworkPlan/docs/working/VHExistsMinimalCounterexample.md` (lines 33–34) at the pair $(r,\tau)$ relative to $F$.

## Neighbourhoods off $F$

**(12) [hand]** Let $v\in A\setminus F$.

**(13) [hand]** Every edge of $A$ incident with $v$ is an edge of $T$, so $N_A(v)\subseteq N_T(v)$.

**(14) [hand]** If $vw$ is an edge of $T$, then $vw$ lies in $E(A)$ or in $E(B)$.

**(15) [hand]** The vertex $v$ lies outside $V(B)$, so $vw$ lies outside $E(B)$.

**(16) [hand]** Therefore $vw$ lies in $E(A)$, and $N_T(v)\subseteq N_A(v)$.

**(17) [hand]** Hence $N_T(v)=N_A(v)$.

**(18) [hand]** Every face of $T$ incident with $v$ is a triangle on $v$ and two neighbours of $v$, and those three vertices lie in $A$, because every neighbour of $v$ lies in $A$.

**(19) [hand]** The edges of $T$ incident with $v$ are edges of $A$ by (16), and the rotation of those edges at $v$ is the rotation at $v$ in the completed side $A$, so $N_T(v)$ and $N_A(v)$ carry the same cyclic order.

**(20) [hand]** The third vertex of $F$ is idle in (12)–(19): those sentences use $v\notin F$ and the absence of edges from $A\setminus F$ to $B\setminus F$.

## The start

**(21) [hand]** Applied to $r$, (17) and (19) give $\deg_T(r)=5$ and the same cyclic neighbourhood of $r$ in $T$ and in $A$.

**(22) [hand]** Let $c$ be a proper colouring of $T-r$ that is proper on the two chords of $\tau$, and let $c_A$ be its restriction to $V(A)\setminus\{r\}$.

**(23) [hand]** Every edge of $A-r$ is an edge of $T-r$, so $c_A$ is a proper colouring of $A-r$.

**(24) [hand]** The ends of the chords lie on the neighbourhood of $r$, hence in $A$, and $c$ agrees with $c_A$ on those ends, so $c_A$ is proper on $\tau$.

**(25) [hand]** By (11) there is a path $(h_0,c_0),\ldots,(h_m,c_m)$ in the move graph of $A$ with $h_0=r$, $c_0=c_A$, each step a Kempe swap or a singleton slide, each $h_i\in A\setminus F$, and $|c_m(N_A(h_m))|\le 3$.

**(26) [hand]** The invariant at index $i$ says that $h_i\in A\setminus F$ and that some proper colouring $C_i$ of $T-h_i$ restricts to $c_i$ on $V(A)\setminus\{h_i\}$.

**(27) [hand]** The colouring $C_0=c$ satisfies the invariant at $i=0$.

## One Kempe step

**(28) [hand]** Suppose the step from $i$ to $i+1$ swaps colours $a\neq b$ on a component $K$ of $(A-h_i)[a,b]$, and write $h=h_i$ and $C=C_i$.

**(29) [hand]** The hole $h$ lies in $A\setminus F$, so every vertex of $F$ remains present in $T-h$ and in $A-h$.

**(30) [hand]** This is the setting of the component-restriction paragraph in `SolvingFrameworkPlan/docs/reports/TriangleSumM3Family.md` (lines 15–23), once $F$ is a clique: the hole lies in $A\setminus F$, and there is no edge from $A\setminus F$ to $B\setminus F$.

**(31) [hand]** The next sentence is the first sentence of this argument that uses the third vertex of $F$.

**(32) [hand]** **Reading $A\cap B=F$ as graphs, the triangle $F$ contributes its three edges to both $E(A)$ and $E(B)$, so any two distinct vertices of $F$ are adjacent in $A$ and in $B$.**

**(33) [hand]** Let $P$ be a path in $(T-h)[a,b]$ with both ends in $A$.

**(34) [hand]** An excursion on $P$ is a maximal subpath whose internal vertices lie in $B\setminus F$.

**(35) [hand]** Each end of an excursion lies in $F$: along $P$ that end is adjacent to an internal vertex in $B\setminus F$, every neighbour of a vertex of $B\setminus F$ lies in $(B\setminus F)\cup F$, and the end is not internal to the excursion, while the hole $h$ is absent from $P$.

**(36) [hand]** Each such end is coloured $a$ or $b$, because it lies on $P$.

**(37) [hand]** If the two ends coincide, the replacement of that excursion is that single vertex, a walk of length $0$ in $F$.

**(38) [hand]** The third vertex of $F$ is idle in (37), and (37) uses no edge of $F$.

**(39) [hand]** If the two ends $p$ and $q$ are distinct, then (32) supplies the edge $pq$.

**(40) [hand]** Sentence (39) uses only that the two excursion endpoints are adjacent; the third vertex of $F$, the vertex in $F\setminus\{p,q\}$, is idle in (39).

**(41) [hand]** Properness of $C$ on the edge $pq$ forces $C(p)\neq C(q)$.

**(42) [hand]** Together with (36), this yields $\{C(p),C(q)\}=\{a,b\}$, so $pq$ is an edge of $(A-h)[a,b]$.

**(43) [hand]** Neither $p$ nor $q$ equals $h$, because both lie in $F$ and $h\notin F$, so $pq$ is still an edge of $A-h$.

**(44) [hand]** Replacing each excursion through $B\setminus F$ by the walk of length $0$ or $1$ in $F$ with the same ends produces a walk in $(A-h)[a,b]$ with the same ends in $A$.

**(45) [hand]** Every path in $(A-h)[a,b]$ is a path in $(T-h)[a,b]$, because every edge of $A$ is an edge of $T$.

**(46) [hand]** Let $K^+$ be a component of $(T-h)[a,b]$ whose intersection $S$ with $V(A)$ is nonempty.

**(47) [hand]** Any two vertices of $S$ are joined by a path in $K^+$; sentence (44) replaces the excursions of that path and yields a walk in $(A-h)[a,b]$, so $S$ lies in a single component $K_A$ of $(A-h)[a,b]$.

**(48) [hand]** Sentence (45) joins every vertex of $K_A$ to a vertex of $S$ by a path in $(T-h)[a,b]$, so $K_A\subseteq K^+$; every vertex of $K_A$ lies in $V(A)$, so $K_A\subseteq S$; together with $S\subseteq K_A$ this gives $S=K_A$.

**(49) [hand]** Thus a nonempty restriction of a component of $(T-h)[a,b]$ to $V(A)$ is exactly one whole component of $(A-h)[a,b]$, which is the claim on line 17 of `TriangleSumM3Family.md`, drawn from the two facts on line 19.

**(50) [hand]** A component of $(T-h)[a,b]$ that misses $V(A)$ restricts to the empty set, and the path in $A$ does not ask for that component to be swapped.

**(51) [hand]** The component $K$ lies in a unique component $K^+$ of $(T-h)[a,b]$, and (48) gives $K^+\cap V(A)=K$, which is the converse sentence on line 21 of that file.

**(52) [hand]** The complement of $V(A)$ in $V(T)$ is $B\setminus F$, so $K^+\setminus V(A)\subseteq B\setminus F$.

**(53) [hand]** Swapping $a$ and $b$ on $K^+$ exchanges those colours on $K$ and on $K^+\setminus V(A)$.

**(54) [hand]** The restriction of the swapped colouring to $A-h$ is the colouring $c_{i+1}$ produced by swapping $K$ in $A$.

**(55) [hand]** A vertex of $F$ lies in $K^+$ if and only if it lies in $K$, by (51), so the colour written on each vertex of $F$ is the colour written by the swap in $A$.

**(56) [hand]** The hole stays at $h$, and the step in $A$ keeps its hole at $h$, so $h_{i+1}=h\in A\setminus F$.

**(57) [hand]** Lemma 1.3(a) of `vh-exists.md`, applied in $T$, says that the swapped colouring $C_{i+1}$ is a proper colouring of $T-h$; the same properness is the last clause of line 21 in the component-restriction paragraph.

**(58) [hand]** The invariant holds at index $i+1$.

**(59) [hand]** Line 23 of `TriangleSumM3Family.md` requires the hole to lie outside the interface when that paragraph is applied, and (29) keeps the hole there for this step.

## One interior slide

**(60) [hand]** Suppose instead that the step from $i$ to $i+1$ is a singleton slide in $A$ from $h=h_i$ to $u=h_{i+1}$.

**(61) [hand]** Both $h$ and $u$ lie in $A\setminus F$: every hole of the path (25) lies in $A\setminus F$, and the landing of the slide is the next hole.

**(62) [hand]** Let $\alpha=c_i(u)$; the slide in $A$ includes the hypothesis that $\alpha$ occurs once on the link of $h$ in $A$.

**(63) [hand]** By (17) and (19) the neighbour-sets $N_T(h)$ and $N_A(h)$ are equal and carry the same cyclic order.

**(64) [hand]** Consecutive vertices in that order are adjacent in $T$, by the facial triangles in (18).

**(65) [hand]** The same pairs are adjacent in $A$: if at least one end lies in $A\setminus F$, then the rim edge lies outside $E(B)$ and hence lies in $E(A)$; if both ends lie in $F$, then (32) places that edge in $E(A)$.

**(66) [hand]** In the subcase of (65) where both ends lie in $F$, the sentence uses only that those two vertices are adjacent, and the third vertex of $F$ is idle there.

**(67) [hand]** Sentences (63)–(66) identify the link cycle of $h$ in $T$ with the link cycle of $h$ in $A$.

**(68) [hand]** The colouring $C_i$ agrees with $c_i$ on that vertex set, so $\alpha$ occurs once on $N_T(h)$.

**(69) [hand]** The slide from $h$ to $u$ is therefore a legal singleton slide of $T$.

**(70) [hand]** Define $C_{i+1}$ on $V(T)\setminus\{u\}$ by $C_{i+1}(h)=\alpha$ and by $C_{i+1}(x)=C_i(x)$ for every $x\notin\{h,u\}$.

**(71) [hand]** The slide in $A$ defines $c_{i+1}$ on $V(A)\setminus\{u\}$ by $c_{i+1}(h)=\alpha$ and by $c_{i+1}(x)=c_i(x)$ for every $x\in V(A)\setminus\{h,u\}$.

**(72) [hand]** On $A-u$ the two successor colourings agree, because both write $\alpha$ at $h$ and on the remaining vertices of $A$ they inherit the agreement of $C_i$ with $c_i$.

**(73) [hand]** Every vertex of $F$ lies in $A$, and $h\notin F$, so the slide writes its new colour off $F$; the colours on $F$ already agree by (72).

**(74) [hand]** Every vertex of $B\setminus F$ is distinct from $h$ and from $u$, so $C_{i+1}$ agrees with $C_i$ on $B\setminus F$.

**(75) [hand]** The slide in $T$ therefore lands on one colouring of $T-u$, namely $C_{i+1}$, which equals $c_{i+1}$ on $A-u$ and equals the previous colouring on $B\setminus F$.

**(76) [hand]** Lemma 1.3(a) of `vh-exists.md` gives properness of $C_{i+1}$: the new colour sits at $h$ and equals $\alpha$, and every neighbour of $h$ in $T-u$ has a colour other than $\alpha$ by (68).

**(77) [hand]** The successor hole $u$ lies in $A\setminus F$, so the invariant holds at index $i+1$.

**(78) [hand]** The sentences that make the slide legal and that name this colouring of $T-u$, namely (60)–(63) and (68)–(77), do not use the third vertex of $F$; the only appeal to (32) inside the link identification is the rim subcase (66), and there the third vertex is idle.

## The terminal state

**(79) [hand]** The invariant holds at $i=0$ by (27), a Kempe successor preserves it by (58), and an interior-slide successor preserves it by (77), so it holds at $i=m$.

**(80) [hand]** By (17) at the terminal hole, $N_T(h_m)=N_A(h_m)$.

**(81) [hand]** The colourings $C_m$ and $c_m$ agree on that set, and $|c_m(N_A(h_m))|\le 3$ by (25), so $|C_m(N_T(h_m))|\le 3$.

**(82) [hand]** The state $(h_m,C_m)$ lies in the fill set of $T$.

**(83) [hand]** Each passage from $C_i$ to $C_{i+1}$ is a Kempe swap or a singleton slide of $T$.

**(84) [hand]** Lemma 1.3(b) says each of those moves reverses by a move of the same kind, so $(r,c)$ and $(h_m,C_m)$ lie in the same component of the move graph of $T$.

**(85) [hand]** Lemma 1.3(c) says that a colour missing from $C_m(N_T(h_m))$ extends $C_m$ to a proper colouring of $T$.

**(86) [hand]** Definition (6) uses (82) and (84); sentence (85) records the further clause of Lemma 1.3(c), that a fill colours the hole.

## The fan in $T$

**(87) [hand]** The chords of $\tau$ are non-edges of $A$.

**(88) [hand]** Both ends of a chord of $\tau$ lie on the neighbourhood of $r$, hence in $V(A)$, by (21).

**(89) [hand]** If such a chord $xy$ is an edge of $T$, then $xy\in E(B)$ and $\{x,y\}\subseteq F$, because $xy\notin E(A)$ and $E(T)=E(A)\cup E(B)$.

**(90) [hand]** In that case (32) makes $xy$ an edge of $F$ lying in $E(A)$.

**(91) [hand]** Under the hypothesis of (89), sentence (90) places $xy$ in $E(A)$, while (87) places $xy$ outside $E(A)$, so that hypothesis is empty, $xy$ lies outside $E(T)$, and $\tau$ is a legal fan at $r$ in $T$.

## The apex slide

**(92) [hand]** Lemma 3.2 of `vh-exists.md` says that if a colouring of the deletion of a degree-5 vertex is proper on a fan with apex $x_i$, then the colour of $x_i$ occurs once on the link: the two link edges at $x_i$ and the two fan chords force the other four link vertices off that colour, and the five link vertices are distinct.

**(93) [hand]** At the start $(r,c_A)$ in $A$, Lemma 3.2 makes the slide from $r$ to the apex $x_i$ legal in $A$.

**(94) [hand]** The same four inequalities hold for $c$ on the link of $r$ in $T$: (21) matches the cyclic neighbourhood with the fan in $A$, (18) makes consecutive link vertices adjacent in $T$, and $c$ is proper on $\tau$, so the slide from $r$ to $x_i$ is legal in $T$.

**(95) [hand]** If the apex $x_i$ lies in $A\setminus F$, the slide is an interior slide of the form (60)–(77), and the successor hole lies in $A\setminus F$.

**(96) [hand]** If the apex $x_i$ lies on $F$, the landing is a different case.

**(97) [hand]** The interior-slide sentences (60)–(77) take the landing in $A\setminus F$, and the neighbourhood identity (17) is stated for vertices in $A\setminus F$, so both are silent on the successor once the hole lies on $F$.

**(98) [hand]** Every hole of the path (25) lies in $A\setminus F$, so a slide whose landing lies on $F$ is absent from that path, and the lift follows (25).

**(99) [open]** Whether a successor state with its hole on $F$ matches a move of $A$ is untouched by (28)–(91).

**(100) [lead]** With the hole on $F$, one vertex of the triangle is deleted and the surviving interface is a single edge, so a Kempe shortcut in that successor would have to be read again from the component-restriction paragraph with a vertex of $F$ missing; that reading is not the argument above.

## Closure

**(101) [hand]** Every colouring of $T-r$ proper on $\tau$ reaches the fill set of $T$, by (22)–(27), (58), (77), (82) and (84).

**(102) [hand]** With $\deg_T(r)=5$ from (21) and with $\tau$ legal in $T$ from (91), the pair $(r,\tau)$ is a good pair of $T$.

**(103) [hand]** Both steps require the current hole to lie in $A\setminus F$. The Kempe step (28)–(59) uses (32) on every pair of distinct excursion ends, and the interior slide cites (32) only in the rim subcase (65)–(66), where the third vertex is idle. Neither step uses the degree, inside $A$, of a vertex of $F$.

**(104) [hand]** The upper-bound lift in `TriangleSumM3Family.md` (lines 52–56) is the Kempe step repeated while the hole remains the original root: each component chosen in $A-r$ is the restriction of a unique global component, the colouring of $A$ follows those swaps, and the target link is the global link because that root has no neighbour in $B\setminus F$.

**(105) [hand]** That upper bound contains no slide; the interior slide (60)–(78) is the step left unwritten in `SolvingFrameworkPlan/docs/working/VHExistsMinimalCounterexample.md` (lines 35 and 40), which next check 1 (line 155) asks to write.

**(106) [hand]** The Kempe successor stays on the invariant by (58), the interior-slide successor stays on it by (77), and the terminal state lies in the fill set of $T$ by (82).

## Feasibility

Feasibility that the interior-witness lift stands: **High**.

## The sentence to attack

**(44) [hand]** Replacing each excursion through $B\setminus F$ by the walk of length $0$ or $1$ in $F$ with the same ends produces a walk in $(A-h)[a,b]$ with the same ends in $A$.

## A sentence about paths

**[hand]** In a proper colouring the three vertices of $F$ receive three distinct colours, so an $\{a,b\}$-path in $T-h$ meets $F$ in at most two vertices; when an excursion through $B\setminus F$ has distinct ends, those ends are adjacent by (32), the edge they span is the length-$1$ walk used in (44), and the remaining vertex of $F$ receives a colour outside $\{a,b\}$, hence lies on no $\{a,b\}$-path in $T-h$.

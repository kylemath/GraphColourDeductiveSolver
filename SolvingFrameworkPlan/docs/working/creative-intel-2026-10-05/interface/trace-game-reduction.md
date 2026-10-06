# The trace game: a 4-ring reduction with a constrained far side

Long Table (Creative Intel), 5 October 2026, 17:22 MDT. Answers Math's 17:15 request to focus on the constrained four-ring. It builds on:
- Math's trace lemma (`docs/reports/MathTriangleCarryResearch.md`, "Four-cycle interface");
- the restriction lemma of `four-cycle-reduction.md` §1;
- the accepted triangle reduction (Math, 17:15).

Math reviewed §1–§2 at 17:29 (see the status note). §2b has not been reviewed. The computations at the end are exploratory and post hoc.

> **Status note, 17:36.** The original §2(a) used one ordinary-edge graph $B^\ast$, and that construction is **withdrawn**. Math found two defects (17:27): ordinary edges are not pair-specific, and crossing same-unused-colour bridges cannot be drawn as edges. §2 below has been repaired with pair-labelled bridges and a Jordan argument on the two paths' own bridges. **The reference proof is Math's `docs/reports/MathTraceGameLiftReview.md`**, which uses pair-specific graphs $H_P,B_P$ and coloured snapshot gadgets. It states that the triangle and induced-4-cycle lifts are valid after the correction. §2b, the 5-cycle extension, has not been reviewed. For a pentagon it needs either the two-path Jordan argument used here, or pentagon snapshot gadgets.

## 0. Why the free game was the wrong model

The free adversary of `four-cycle-reduction.md` §2 may decline or force a merge at will. In VH∃ the path is chosen knowing all of $T$, including the far side and its colouring. Reachability games with perfect information are determined, so the free game fails exactly when some history-dependent merge rule blocks every path. The question is whether such a rule can be **realised** by a planar far side and its evolving colouring.

Two facts constrain the realisation:
- **[hand, Math]** the trace lemma: at a fixed colouring, the far side's extra connections on $Q$ have at most three states for a boundary word with three or four colours, and at most nine Boolean bridge matrices for a two-colour word;
- **[hand, new] the frozen-pair fact, stated below.**

**[hand] Frozen-pair fact.** A Kempe swap in colour pair $P=\{\alpha,\beta\}$ does not change the set of vertices coloured from $P$, nor the set coloured from the complementary pair $\bar P$. The induced subgraphs on these sets are unchanged. So on any part of the graph, connectivity in $P$ and in $\bar P$ is unchanged by a swap in $P$. A slide that moves the hole within $A\setminus Q$ changes no colour on $B$.

## 1. Bridge bits and the trace game

Let $\varphi$ be an induced 4-cycle $(q_0,q_1,q_2,q_3)$ that bounds a face, and let $c$ be a colouring with the hole off $\varphi$.

- A colour pair $P$ is **relevant** at $c$ when the vertices of $\varphi$ coloured from $P$ are exactly one opposite pair, $\{q_0,q_2\}$ (diagonal $0$) or $\{q_1,q_3\}$ (diagonal $1$).
- A **bit assignment** gives each relevant pair a bit.
- It is **admissible** when no two set bits lie on different diagonals with disjoint colour pairs.

For a word with three or four colours this gives Math's three states. For a two-colour word it gives Math's nine matrices.

**The trace game on $(G,\varphi)$.** A position is a state (hole off $\varphi$, colouring) together with an admissible bit assignment. The player moves:
- **Kempe swap** of a component $K$ in pair $P$. If $P$ is relevant, its bit is set, $K$ meets $\varphi$, and a second $P$-component $K'$ meets $\varphi$, then $K\cup K'$ is swapped. Otherwise $K$ alone is swapped. Afterwards the bits of $P$ and $\bar P$ keep their values, since relevance is unchanged for these two pairs. The adversary then chooses any admissible values for the other relevant pairs.
- **Singleton slide** to a vertex off $\varphi$. Every bit is kept.

The player wins on a state whose link uses at most three colours. When $\varphi$ is a triangle there are no relevant pairs and no bits, and the game is ordinary move-graph reachability with holes off $\varphi$.

**Hypothesis.** $\mathcal C^{\rm tr}$ is the class of pairs $(G,\varphi)$ satisfying three conditions:
- $G$ is a plane graph, all of whose faces are triangles except $\varphi$;
- $\varphi$ is a triangle or an induced 4-cycle;
- every vertex off $V(\varphi)$ has degree $\ge5$.

$\mathrm{VH}^{\rm tr}_\varphi(G)$ asks for a degree-5 vertex $v\notin V(\varphi)$ and a legal fan $\tau$ such that, from every start in $S(v,\tau)$ and every admissible initial bit assignment, the player wins the trace game. On minimum-degree-5 triangulations with a triangular $\varphi$ this is $\mathrm{VH}_\varphi$, so it implies VH∃.

**[hand] The trace game is weaker than the free game.** Every merge pattern the trace adversary can produce, the free adversary can also produce. So a pass in the free game implies a pass in the trace game.

## 2. The 4-cycle lift

**[hand] Theorem.** Let $(G,\varphi)\in\mathcal C^{\rm tr}$, and let $Q=(q_0,q_1,q_2,q_3)$ be an induced separating 4-cycle of $G$. Let the closed sides be $A$ and $B$, named so that the face $\varphi$ lies in $B$. Then $(A,Q)\in\mathcal C^{\rm tr}$, $|A|<|G|$, and a pair that wins the trace game on $(A,Q)$ wins the trace game on $(G,\varphi)$.

*Proof.*

*Membership.* The faces of $A$ are the faces of $G$ on the $A$-side, together with the face $Q$. Vertices of $A\setminus Q$ keep their $G$-neighbourhoods, and they are off $\varphi\subseteq B$, so their degrees are $\ge5$. Also $B\setminus Q\neq\emptyset$, which gives the order.

*Induced bits (repaired 17:29 after Math's 17:27 review).* Take a position of the $G$-game: a state with hole $h\in A\setminus Q$, and $\varphi$-bits if $\varphi$ is a quadrilateral.

The bridges are **pair-labelled**. For each colour pair $P$, let $B_P$ be the graph on the $P$-coloured vertices of $B-h$ with the edges of $B$ between them. Add one labelled bridge edge for each set $\varphi$-bit **of the pair $P$**, joining its opposite pair. A bridge edge of pair $R\neq P$ is never an edge of $B_P$.

The earlier draft used ordinary virtual edges, and that was wrong. An $\{\alpha,\delta\}$-bridge joins two $\alpha$-vertices, so as an ordinary edge it would also serve an $\{\alpha,\varepsilon\}$-path. Math caught this.

For a pair $P$ relevant on $Q$, define the $Q$-bit of $P$ to be set exactly when the opposite $P$-vertices of $Q$ are joined by a path in $B_P$ whose internal vertices lie in $B\setminus Q$. Such a path may be a single bridge edge.

*(a) Admissible.* Suppose two set $Q$-bits lie on different diagonals of $Q$ and have disjoint pairs $P$ and $R$. Take witnessing paths $\pi_P$ in $B_P$ and $\pi_R$ in $B_R$. They share no vertex, because their colours are disjoint. Draw in the disc $B$ only the bridge edges these two paths use, each as a curve inside the face $\varphi$.
- A $P$-bridge and an $R$-bridge on crossing diagonals of $\varphi$ are excluded by $\varphi$-admissibility.
- Both cannot lie on the same diagonal: its two ends carry one colour, and the disjoint pairs $P$ and $R$ cannot both contain it.
- On a 4-face a relevant pair meets $\varphi$ in exactly one opposite pair, so it has at most one bridge, and each path uses at most one bridge edge.

So the drawing of $\pi_P\cup\pi_R$ is planar. Its two curves join alternating boundary points of the disc $B$ and are disjoint, which Jordan forbids. Math's coloured snapshot gadgets (`MathTraceGameLiftReview.md`, when written) give an alternative realisation of every admissible state.

*(b) Moves match.* Consider a $G$-move by the player at $h\in A\setminus Q$: a swap of the $G$-game component, including any $\varphi$-merge from a set $\varphi$-bit. Restricted to $A$, it is the $A$-component $K$ or $K\cup K'$. The $G$-game component of pair $P$ is a component of $G_P$ plus the $P$-labelled $\varphi$-bridges. By the restriction lemma (`four-cycle-reduction.md` §1, applied to that pair graph), it is $K\cup K'$ exactly when the $Q$-bit of $P$ is set. That is the $A$-game's rule. A slide inside $A\setminus Q$ is the same move in both games.

*(c) Dynamics match.* After a swap in $P$, the $P$-coloured and $\bar P$-coloured vertex sets of $B$ are unchanged (frozen-pair fact). The $\varphi$-bits of $P$ and $\bar P$ are kept by the $G$-game. So the $Q$-bits of $P$ and $\bar P$ are unchanged, which is what the $A$-game requires. The other $Q$-bits take some admissible values by (a), and the $A$-adversary may choose any admissible values. Concretely, $B_P$ and $B_{\bar P}$ have unchanged vertex sets and edges, and their labelled bridges are kept. After a slide nothing in any $B_P$ changes, so every $Q$-bit is kept.

*(d) Starts and fills.* A start of $G$ restricts to a start of $A$, and its induced bits are admissible. The $A$-strategy wins from every admissible bit assignment. At the final hole, $N_G(h)=N_A(h)$, so the link is the same and the fill is the same.

So the $A$-strategy, applied through this correspondence, wins the $G$-game against every $G$-adversary. Every hole lies in $A\setminus Q$, which is disjoint from $V(\varphi)$. ∎

**[hand] Triangle cuts inside the class.** Let $F$ be a separating triangle of $G$, with the side $A_1$ away from $\varphi$. Then $(A_1,F)\in\mathcal C^{\rm tr}$ has no bits, and a plain $F$-good path of $A_1$ lifts.

When a $G$-component meets $\varphi$ and $A_1\setminus F$, it contains every vertex of $F$ coloured from $P$, because those vertices are pairwise adjacent. The extra component of a $\varphi$-merge therefore misses $F$, and so misses $A_1$. The restriction to $A_1$ is the $A_1$-component, as in the accepted triangle reduction.

**[hand] Corollary.** A least-order failure of $\mathrm{VH}^{\rm tr}$ on $\mathcal C^{\rm tr}$ has no separating triangle and no separating 4-cycle. Without separating triangles, every separating 4-cycle is induced: a chord would split it into two triangles, both facial, and the cycle would then bound two faces on one side.

## 2b. The 5-cycle lift (17:29, hand, pending review)

**Runs.** On a face of length $k\le5$, the vertices coloured from a pair $P$ form at most two runs: maximal blocks that are consecutive on the face. Three runs would need three separating vertices, so $k\ge6$. Each run is connected through the face's own edges. A pair is **relevant** when it has exactly two runs, and its bit says that the two runs are joined through the far side in $P$, by pair-labelled paths as in §2. A set of bits is **admissible** when no two set bits have disjoint pairs whose runs **alternate** around the face, meaning one pair's runs lie in different gaps between the other's runs. For $k=4$ this is exactly §1.

**[hand] Theorem.** Extend $\mathcal C^{\rm tr}$ to allow $\varphi$ to be an induced 5-cycle, provided that **at least two vertices lie on the non-$\varphi$ side of it**. Let $Q$ be an induced separating 5-cycle of $G$, and let $A$ be the side away from $\varphi$, with $|A\setminus Q|\ge2$. Then a trace-game win on $(A,Q)$ lifts to $(G,\varphi)$.

*Proof.* As in §2, with three changes.
- In the restriction step, each run lies in one $A$-component. At most two runs per pair means at most two $A$-components meet $Q$ in that pair, so the restriction is $K$ or $K\cup K'$.
- In (a), disjoint-pair paths joining alternating runs are vertex-disjoint curves joining alternating boundary arcs of the disc. Jordan forbids them. The only bridges used are those of the two pairs, and they do not cross, by admissibility on $\varphi$.
- The dynamics are the frozen-pair fact. ∎

**Bridge endpoints and non-crossing on a pentagon [hand; added 20:40 in response to Math's review; accepted by Math 20:49, conditional on the open pentagon trace-game hypothesis; simplified after Math's cosmetic note].**

*Endpoints.* Let $P$ be a pair with exactly two runs on the face $\varphi=(q_0,\dots,q_4)$. A **run** is a maximal block of cyclically consecutive face vertices coloured from $P$. Consecutive face vertices are adjacent in $G$ (the face is an induced cycle) and have different colours, so a run is a path in the pair graph, hence lies in one $P$-component. The bridge of $P$ is a relation between the **two runs**, not between two chosen vertices: it says the two runs lie in one $P$-component of the far side. Any $u\in$ run$_1$ and $v\in$ run$_2$ serve as endpoints, because each run is already connected inside $G_P$. So the pair-labelled graph $H_P$ is $G_P$ together with one abstract connection between the two runs, labelled $P$ and appearing in no other $H_R$.

*Non-crossing.* Two bridges matter together only through the Jordan argument of §2(a), which needs a pair $P$ and a pair $R$ with **disjoint colour sets**, both bits set, and vertex-disjoint witness paths $\pi_P\subset B_P$ and $\pi_R\subset B_R$. By pair labelling, $\pi_P$ uses at most the $P$-hop of $\varphi$ and $\pi_R$ at most the $R$-hop, each at most once (a path is simple, and each pair has one bridge).

On a pentagon, disjoint pairs $P,R$ use all four colours between them, so every face vertex lies in a $P$-run or an $R$-run. If each has two runs, the maximal blocks around the face go $P,R,P,R$: the runs **always alternate**. So $\varphi$-admissibility forbids both $\varphi$-bits being set. (Math's 20:49 review made this observation, and it makes the "same gap" case vacuous. An earlier version of this paragraph argued that case; it was harmless and is removed.)

Hence at most one of $\pi_P,\pi_R$ uses a $\varphi$-hop. A single hop is one chord drawn inside the face $\varphi$, and the face interior contains no vertex or edge of $G$, so the chord meets no actual edge and no other path. Replace the hop, if there is one, by that chord. The result is two disjoint curves in the disc $B$ whose endpoints lie in the runs of $P$ and $R$ on $Q$. If those runs alternate on $Q$, the curves join alternating boundary points, which Jordan forbids. So two set $Q$-bits of disjoint pairs with alternating $Q$-runs do not occur: the induced $Q$-bits are admissible.

*Pairs that share a colour.* Pairs $P,R$ with a common colour are not constrained by admissibility, and nothing is claimed for them. This is the reason the argument is pair-by-pair: the labelled graphs $H_P$ and $H_R$ never exchange hops, as in Math's snapshot-gadget construction for the quadrilateral.

*What this does not cover.* A pentagon pair with three or more runs cannot occur (it would need six or more face vertices). A pentagon realisation by snapshot gadgets, as Math gave for the quadrilateral, is not written here; the pair-labelled argument above replaces it.

**Why wheels are excluded [computed, exploratory].** If $A\setminus Q$ is a single vertex $u$, then $Q=N(u)$ and $A$ is the 5-wheel. In the trace game on the 5-wheel, the player has no slide, since every neighbour of $u$ is on $\varphi$. Every fan at $u$ loses $3$ of $36$ (start, bit) positions. So the wheel would be a failure of the extended hypothesis, and it must be outside the class. That loses nothing: a separating 5-cycle that is a vertex neighbourhood is never reduced.

**[hand] Corollary.** A least-order failure of the extended $\mathrm{VH}^{\rm tr}$ has:
- no separating triangle;
- no separating 4-cycle;
- no separating 5-cycle with at least two vertices on each side.

That is cyclic 5-connectivity, as for classical minimal counterexamples, but here for the move hypothesis. Chords of a 5-cycle would create a separating 3- or 4-cycle, unless the cycle bounds faces on one side.

## 3. Exploratory readings [computed, exploratory, post hoc, undeclared]

The user approved downloading plantri 5.8 in this session. The source is from Brendan McKay's site; the tarball's SHA-256 is `e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8`. It was built locally and is not committed. Orders are $\le18$. The code is in `longtable/explore-vhphi/`.

1. **Triangle faces, exhaustive.** Members are all `plantri -c4m4 n` triangulations, $n\le18$, whose vertices of degree $<5$ lie on one face. There are $435$ members at orders $12$–$18$ and none at orders $7$–$11$, consistent with Math's order-$\ge11$ hand bound. All pass with pure fills. The degree-4 count is $0$, $1$ or $2$; Math's hand lemma excludes $3$ in the 4-connected core. The members with no degree-4 vertex number $1,1,1,3,4,12$ at orders $12$, $14$–$18$, matching the known minimum-degree-5 counts.
2. **Quadrilateral faces, free game, exhaustive in one family.** The family is $G=T-st$ with $T$ from `plantri -c4m4 n`, $n\le18$, $\varphi$ the merged face induced, and off-$\varphi$ degrees $\ge5$. That gives $4004$ (graph, edge) members. The free game fails only on $16{:}1-st$, where $16{:}1$ is the second `plantri -m5 16` triangulation and $s,t$ are adjacent degree-6 vertices; the two such edges are equivalent. The random search had found the same member.
3. **Realised far sides on that member.** The far sides were the two diagonals and every chordless disc triangulation with $1$–$5$ interior vertices (`plantri -P4`), in all $8$ alignments: $2146$ glued graphs. All $50$ (vertex, fan) pairs at the ten degree-5 vertices off $\varphi$ stay pure-good in every one.
4. **Trace game on that member, pure.** Every fan at every degree-5 vertex off $\varphi$ wins from every start and every admissible initial bit assignment; for example, vertex $2$, fan $0$ wins $168$ of $168$. Since the trace game is weaker than the free game, **the pure trace game passes on all $4004$ members of reading 2.**

5. **All 4-face and 5-face members from `plantri -m4`** (17:44). Members are $G=T-x$, where $\deg x\in\{4,5\}$, the link is chordless, every vertex outside $N[x]$ has degree $\ge5$, and wheels are excluded. $T$ ranges over orders $12$–$18$, so $G$ has order $11$–$17$. Every chordless $k$-face member arises this way. The trace game (`vhphi_trace_members.py`) passes with pure fills on all **$2002$** members: $940$ with a 4-face and $1062$ with a 5-face. There are no failures. The 5-wheel fails, as expected, which is why it is excluded.

So the 4-ring obstruction found by the free game is not realised by any small far side, and it disappears under the trace constraint.

## 4. What is open

- $\mathrm{VH}^{\rm tr}$ itself. Its least failure has no separating 3- or 4-cycle. A separating 5-cycle that is not a vertex neighbourhood is the next cut. A 5-face has at most two components per pair meeting it, so a bit model is plausible, but the bridge-state count for five boundary vertices is not done.
- The data cover quadrilateral members of one family only ($T-e$ with $T$ 4-connected), and orders up to $18$.
- Independent replay of every reading above: requested from Audit.
- This is not a finite-state controller or a termination proof. The game is solved per graph by computation, and nothing here proves the player wins in general.

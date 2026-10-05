# The trace game: a 4-ring reduction with a constrained far side

Long Table (Creative Intel), 5 October 2026, 17:22 MDT. Answers Math's 17:15 request to focus on the constrained four-ring. It builds on:
- Math's trace lemma (`docs/reports/MathTriangleCarryResearch.md`, "Four-cycle interface");
- the restriction lemma of `four-cycle-reduction.md` §1;
- the accepted triangle reduction (Math, 17:15).

Math has not reviewed this page. The computations at the end are exploratory and post hoc.

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

*Induced bits.* Take a position of the $G$-game: a state with hole $h\in A\setminus Q$, and $\varphi$-bits if $\varphi$ is a quadrilateral. Let $B^\ast$ be $B$ with one virtual edge, drawn inside the face $\varphi$, for each set $\varphi$-bit, joining that opposite pair. For a pair $P$ relevant on $Q$, define the $Q$-bit of $P$ as "the opposite $P$-vertices of $Q$ are joined by a $P$-path in $B^\ast-h$ whose internal vertices lie in $B\setminus Q$".

*(a) Admissible.* Two virtual edges with disjoint colour pairs on crossing diagonals of $\varphi$ are excluded by $\varphi$-admissibility. Two on the same diagonal share the colour of its ends. So the virtual edges can be drawn inside $\varphi$ without crossings, and $B^\ast$ is a plane disc. Two set $Q$-bits on different diagonals of $Q$ with disjoint pairs would be vertex-disjoint paths joining alternating boundary points of that disc. Jordan forbids this, exactly as in Math's trace lemma.

*(b) Moves match.* Consider a $G$-move by the player at $h\in A\setminus Q$: a swap of the $G$-game component, including any $\varphi$-merge from a set $\varphi$-bit. Restricted to $A$, it is the $A$-component $K$ or $K\cup K'$. By the restriction lemma (`four-cycle-reduction.md` §1, with $B^\ast$ in place of $B$), it is $K\cup K'$ exactly when the $Q$-bit of $P$ is set. That is the $A$-game's rule. A slide inside $A\setminus Q$ is the same move in both games.

*(c) Dynamics match.* After a swap in $P$, the $P$-coloured and $\bar P$-coloured vertex sets of $B$ are unchanged (frozen-pair fact). The $\varphi$-bits of $P$ and $\bar P$ are kept by the $G$-game. So the $Q$-bits of $P$ and $\bar P$ are unchanged, which is what the $A$-game requires. The other $Q$-bits take some admissible values by (a), and the $A$-adversary may choose any admissible values. After a slide nothing in $B^\ast$ changes, so every $Q$-bit is kept.

*(d) Starts and fills.* A start of $G$ restricts to a start of $A$, and its induced bits are admissible. The $A$-strategy wins from every admissible bit assignment. At the final hole, $N_G(h)=N_A(h)$, so the link is the same and the fill is the same.

So the $A$-strategy, applied through this correspondence, wins the $G$-game against every $G$-adversary. Every hole lies in $A\setminus Q$, which is disjoint from $V(\varphi)$. ∎

**[hand] Triangle cuts inside the class.** Let $F$ be a separating triangle of $G$, with the side $A_1$ away from $\varphi$. Then $(A_1,F)\in\mathcal C^{\rm tr}$ has no bits, and a plain $F$-good path of $A_1$ lifts.

When a $G$-component meets $\varphi$ and $A_1\setminus F$, it contains every vertex of $F$ coloured from $P$, because those vertices are pairwise adjacent. The extra component of a $\varphi$-merge therefore misses $F$, and so misses $A_1$. The restriction to $A_1$ is the $A_1$-component, as in the accepted triangle reduction.

**[hand] Corollary.** A least-order failure of $\mathrm{VH}^{\rm tr}$ on $\mathcal C^{\rm tr}$ has no separating triangle and no separating 4-cycle. Without separating triangles, every separating 4-cycle is induced: a chord would split it into two triangles, both facial, and the cycle would then bound two faces on one side.

## 3. Exploratory readings [computed, exploratory, post hoc, undeclared]

The user approved downloading plantri 5.8 in this session. The source is from Brendan McKay's site; the tarball's SHA-256 is `e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8`. It was built locally and is not committed. Orders are $\le18$. The code is in `longtable/explore-vhphi/`.

1. **Triangle faces, exhaustive.** Members are all `plantri -c4m4 n` triangulations, $n\le18$, whose vertices of degree $<5$ lie on one face. There are $435$ members at orders $12$–$18$ and none at orders $7$–$11$, consistent with Math's order-$\ge11$ hand bound. All pass with pure fills. The degree-4 count is $0$, $1$ or $2$; Math's hand lemma excludes $3$ in the 4-connected core. The members with no degree-4 vertex number $1,1,1,3,4,12$ at orders $12$, $14$–$18$, matching the known minimum-degree-5 counts.
2. **Quadrilateral faces, free game, exhaustive in one family.** The family is $G=T-st$ with $T$ from `plantri -c4m4 n`, $n\le18$, $\varphi$ the merged face induced, and off-$\varphi$ degrees $\ge5$. That gives $4004$ (graph, edge) members. The free game fails only on $16{:}1-st$, where $16{:}1$ is the second `plantri -m5 16` triangulation and $s,t$ are adjacent degree-6 vertices; the two such edges are equivalent. The random search had found the same member.
3. **Realised far sides on that member.** The far sides were the two diagonals and every chordless disc triangulation with $1$–$5$ interior vertices (`plantri -P4`), in all $8$ alignments: $2146$ glued graphs. All $50$ (vertex, fan) pairs at the ten degree-5 vertices off $\varphi$ stay pure-good in every one.
4. **Trace game on that member, pure.** Every fan at every degree-5 vertex off $\varphi$ wins from every start and every admissible initial bit assignment; for example, vertex $2$, fan $0$ wins $168$ of $168$. Since the trace game is weaker than the free game, **the pure trace game passes on all $4004$ members of reading 2.**

So the 4-ring obstruction found by the free game is not realised by any small far side, and it disappears under the trace constraint.

## 4. What is open

- $\mathrm{VH}^{\rm tr}$ itself. Its least failure has no separating 3- or 4-cycle. A separating 5-cycle that is not a vertex neighbourhood is the next cut. A 5-face has at most two components per pair meeting it, so a bit model is plausible, but the bridge-state count for five boundary vertices is not done.
- The data cover quadrilateral members of one family only ($T-e$ with $T$ 4-connected), and orders up to $18$.
- Independent replay of every reading above: requested from Audit.
- This is not a finite-state controller or a termination proof. The game is solved per graph by computation, and nothing here proves the player wins in general.

# The 4-cycle: a valid lift, and a game hypothesis that is false

Long Table (Creative Intel), 5 October 2026, 17:09 MDT. Follow-up to `face-avoiding-reduction.md`. Math has not reviewed this page.

The first part is a hand lift across a separating 4-cycle. The second part is a strengthened hypothesis that would make that lift an induction, and an exploratory computation that kills that hypothesis on an order-$16$ member of its class. The kill is exploratory. It comes from undeclared code in `longtable/explore-vhphi/`, and it needs an independent check before anyone cites it.

## 1. What a swap in $T$ does to one side of a 4-cycle

**[hand] Lemma (4-cycle restriction).** Let $G$ be a plane graph, and let $Q=(w,x,y,z)$ be an induced 4-cycle. Let $A$ and $B$ be the closed sides, with $A\cap B=Q$ and no edge from $A\setminus Q$ to $B\setminus Q$. Let the hole $h$ lie in $A\setminus Q$. Let $K^+$ be a component of $(G-h)[\alpha,\beta]$ that meets $A$. Then $K^+\cap V(A)$ is either one component $K$ of $(A-h)[\alpha,\beta]$, or the union $K\cup K'$ of the two components of $(A-h)[\alpha,\beta]$ that contain two opposite vertices of $Q$.

*Proof.* Take a path of $K^+$ with both ends in $A$. As in `interior-witness.md` (A), every excursion through $B\setminus Q$ has its ends on $Q$.
- If the ends coincide, or are adjacent on $Q$, the excursion is replaced by a vertex or by an edge of $A$ whose colours are $\alpha$ and $\beta$.
- If the ends are opposite, say $w$ and $y$, the excursion may join two components of $(A-h)[\alpha,\beta]$.

So $K^+\cap V(A)$ is a union of components of $(A-h)[\alpha,\beta]$, glued only at opposite pairs of $Q$. Count the components of $(A-h)[\alpha,\beta]$ that meet $Q$. The vertices of $Q$ with colours in $\{\alpha,\beta\}$ induce a subgraph of the 4-cycle. If three or four of them carry these colours, they form a path or the whole cycle, which lies in one component. If two do, they are adjacent, so in one component, or opposite. If one does, there is one component. So at most two components meet $Q$, and they meet it at opposite vertices. ∎

**[hand]** A slide from $h\in A\setminus Q$ to $u\in A\setminus Q$ lifts unchanged: $N_G(h)=N_A(h)$ with the same rotation.

So a path of $T$ with holes in $A\setminus Q$, read on $A$, is a path of $A$ in which some swaps of a component meeting $Q$ also swap the second component meeting $Q$. Which of these happens depends on $B$ and on the current colours there.

## 2. The game hypothesis and its closure

**Definition.** The class $\mathcal C^4$ consists of pairs $(G,\varphi)$ satisfying three conditions:
- $G$ is a plane graph whose faces are all triangles except $\varphi$;
- $\varphi$ is a triangle or an induced 4-cycle;
- every vertex off $V(\varphi)$ has degree $\ge5$.

The game at a state with hole off $\varphi$ runs as follows.
- The player chooses a singleton slide to a vertex off $\varphi$, or a Kempe component $K$.
- If $K$ meets $\varphi$ and a second component $K'$ of the same two colours meets $\varphi$, the adversary decides whether $K'$ is swapped as well.
- The player wins on reaching a link with at most three colours.

$\mathrm{VH}^4_\varphi(G)$ says that some degree-5 vertex $v$ off $\varphi$, with a legal fan, wins the game from every start. When $\varphi$ is a triangle, the adversary has no move, because the $\{\alpha,\beta\}$-vertices of a triangle are adjacent, and $\mathrm{VH}^4_\varphi$ is $\mathrm{VH}_\varphi$.

**[hand] Closure.** Let $(G,\varphi)$ be a least-order failure of $\mathrm{VH}^4$ on $\mathcal C^4$. Then $G$ has no separating triangle and no separating 4-cycle.

- **Separating 4-cycle.** By the lemma, a $G$-swap restricted to the side $A$, with $\varphi$ on the other side, is a legal outcome of $A$'s game, so $A$'s winning strategy lifts. If $\varphi$ is itself a quadrilateral, $G$'s own adversary adds a component meeting $\varphi$. That component meets $A$ only in the second component meeting $Q$, so the outcome on $A$ is again one of $K$ and $K\cup K'$.
- **Separating triangle $F$.** The extra component of $G$'s adversary cannot reach the side $A_1$ away from $\varphi$. The swapped component already contains every vertex of $F$ coloured $\alpha$ or $\beta$, because those vertices are pairwise adjacent. So the side path is followed exactly.

A separating 4-cycle is induced in the absence of separating triangles. A chord would split the cycle into two triangles, both facial, and the cycle would then bound two faces on one side.

So if $\mathrm{VH}^4$ held on $\mathcal C^4$, a least-order failure of VH∃ would have no separating 3-cycle and no separating 4-cycle.

## 3. The game hypothesis is false (exploratory)

**[computed, exploratory, undeclared code]** The member is $G=T-st$, where $T$ is an order-$16$ minimum-degree-$5$ triangulation, with twelve vertices of degree $5$ and four of degree $6$. The edge $st$ joins two of the degree-$6$ vertices. $\varphi$ is the 4-face formed by the two faces at $st$; it is induced. Every vertex off $\varphi$ has degree $5$ or $6$. The face list is in `longtable/explore-vhphi/vhphi-quad-explore-seed2-mixed0.json`.

Results:
- **No adversary.** Every legal fan at each of the ten degree-5 vertices off $\varphi$ wins every start by pure Kempe swaps.
- **With the adversary, pure Kempe.** No fan wins every start.
- **With the adversary and slides off $\varphi$ allowed.** No fan wins every start. The closure has $1186$ states. The best fans win $44$ of $46$ starts.

Two independent random seeds produced this member, and the numbers agree. So $\mathrm{VH}^4$ fails on a member of $\mathcal C^4$. The closure in section 2 is valid, but its hypothesis is false. The 4-cycle reduction in this form is **killed**, pending an independent check of the game code.

The adversary is stronger than any real far side. In the real triangulation $T$, the far side is the single edge $st$. There, $s$ and $t$ never share a colour, and their components merge whenever both carry the swapped colours. The free adversary may decline the merge, and on $G$ it may also merge when $c(s)=c(t)$. What dies is the free adversary, not the 4-cut question.

## 4. What survives

- The triangle reduction (`face-avoiding-reduction.md`) is untouched. Its triangle faces have no adversary.
- Lemma 1 (4-cycle restriction) and the slide lift are hand facts. Any later 4-cut reduction will use them.
- **[lead]** The adversary should be constrained by a fixed far side: the merge pattern is a function of the far side's graph and of its colouring, which evolves with the swaps. One honest form quantifies over far sides: "for every disc $B$ glued along $Q$" with interior degrees $\ge5$. That is the original statement on $T$ unless a finite set of boundary behaviours is enough. Birkhoff's 4-ring argument is the classical template: in a 4-ring, the far side can only realise the two Kempe-connection patterns of the quadrilateral. Not started.

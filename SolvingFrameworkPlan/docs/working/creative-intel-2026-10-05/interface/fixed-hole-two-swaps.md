# The fixed hole on a separating triangle fills in two swaps

Long Table (Creative Intel), 5 October 2026, 16:43 MDT. Follow-up to `interior-witness.md` section (C) and to the open sentence in `../DIRECTOR.md`. No graph was generated and no census was run. Math has not reviewed this page.

Notation is that of `interior-witness.md`. $T$ is a spherical triangulation, $F=\{f,p,q\}$ is a separating triangle with sides $A$ and $B$, $A\cap B=F$, and there is no edge from $A\setminus F$ to $B\setminus F$. A state at the hole $f$ is a proper $4$-colouring $c$ of $T-f$. Moves at a fixed hole are Kempe swaps in $T-f$.

## The cut fact

**[hand]** Let $x\in A\setminus F$ and $y\in B\setminus F$. Every path in $T-f$ from $x$ to $y$ meets $\{p,q\}$. Such a path has a first vertex outside $A\setminus F$. That vertex is adjacent to its predecessor in $A\setminus F$, so it lies in $F$, and it is not $f$. Consequently, for colours $\alpha,\beta$ with $\{\alpha,\beta\}\cap\{c(p),c(q)\}=\emptyset$, no component of $(T-f)[\alpha,\beta]$ meets both $A\setminus F$ and $B\setminus F$.

## The theorem

**[hand] Theorem (fixed hole).** Let $f\in F$ have $\deg_T(f)=5$. Then every proper $4$-colouring of $T-f$ reaches a colouring whose link at $f$ uses at most three colours by at most two Kempe swaps at the fixed hole $f$. The interior on both sides is arbitrary.

### The shape of the link

By `interior-witness.md` (B), $\deg_T(f)=\deg_A(f)+\deg_B(f)-2$ with both side degrees at least $3$, so $\{\deg_A(f),\deg_B(f)\}=\{3,4\}$. Name the sides so that $\deg_A(f)=3$. The rotation at $f$ is $(p,a,q,b_2,b_1)$ with $a\in A\setminus F$ and $b_1,b_2\in B\setminus F$. The edge $pq$ is in $T$. The vertex $a$ is adjacent to neither $b_1$ nor $b_2$.

If the link already uses at most three colours, zero swaps suffice. Otherwise the link uses four colours on five vertices, so exactly one colour occurs twice, on two vertices that are nonadjacent in $T$. Consecutive link vertices are adjacent, and $pq$ is an edge, so the repeated pair is one of $\{p,b_2\}$, $\{q,b_1\}$, $\{a,b_2\}$, $\{a,b_1\}$. The reflection $p\leftrightarrow q$, $b_1\leftrightarrow b_2$ preserves the configuration, so two cases remain. Colours are named by first occurrence along $(p,a,q,b_2,b_1)$.

### Case 1: the repeat is at $\{p,b_2\}$

The link is $(0,1,2,0,3)$. Let $K$ be the component of $a$ in $(T-f)[1,3]$. The vertices $p$ and $q$ have colours $0$ and $2$, so by the cut fact $K\subseteq A\setminus F$. The link vertices with colour $1$ or $3$ are $a$ and $b_1$, and $b_1\notin K$. Swapping $K$ sends $a$ to $3$ and changes no other link vertex. The link becomes $(0,3,2,0,3)$, which uses $\{0,2,3\}$. **One swap.**

### Case 2: the repeat is at $\{a,b_2\}$

The link is $(0,1,2,1,3)$, which is the coloured link of `interior-witness.md` (C). Consider two locks.

- $L_1$: a path in $(T-f)[2,3]$ from $b_1$ to $q$.
- $L_3$: a path in $(T-f)[0,1]$ from $b_2$ to $p$.

**[hand] Lemma (no double lock).** $L_1$ and $L_3$ do not both exist.

Suppose both exist. $L_1$ avoids $f$, and its vertices have colours $2$ and $3$, so it avoids $p$ (colour $0$) and $b_2$ (colour $1$). Let $Z$ be the cycle $f\,b_1\,L_1\,q\,f$. It is a simple closed curve in the embedding. At $f$ it uses the edges $fb_1$ and $fq$. In the rotation $(p,a,q,b_2,b_1)$ the edge $fb_2$ lies strictly between $fq$ and $fb_1$ on one side, and $fp$ lies on the other. Near $f$ the two sides of $Z$ are these two wedges. The edges $fb_2$ and $fp$ meet $Z$ only at $f$, because $b_2,p\notin Z$ and edges of a plane graph meet only at common endpoints. So **[cited]** by the Jordan curve theorem $b_2$ and $p$ lie in different components of the complement of $Z$. $L_3$ is a curve from $b_2$ to $p$. It avoids $f$. Its vertices have colours $0$ and $1$, so it shares no vertex with $L_1$, whose colours are $2$ and $3$. Its edges do not cross edges of $Z$. So $L_3$ misses $Z$, which is a contradiction.

The separating triangle is not used in this lemma. It is used in the swaps below.

**If $L_1$ does not exist.** Let $K_1$ be the component of $b_1$ in $(T-f)[2,3]$. Then $q\notin K_1$. The link vertices with colour $2$ or $3$ are $q$ and $b_1$. Swapping $K_1$ sends $b_1$ to $2$ and changes no other link vertex. The link becomes $(0,1,2,1,2)$, which uses $\{0,1,2\}$. **One swap.** This is the separated branch of (C).

**If $L_1$ exists.** By the lemma, $L_3$ does not exist. Let $K_3$ be the component of $b_2$ in $(T-f)[0,1]$. Then $p\notin K_3$. The link vertices with colour $0$ or $1$ are $p$, $a$ and $b_2$. Suppose $a\in K_3$. A path in $K_3$ from $b_2\in B\setminus F$ to $a\in A\setminus F$ meets $\{p,q\}$ by the cut fact. $q$ has colour $2$, so the path meets $p$, and $p\in K_3$, which contradicts $p\notin K_3$. So $a\notin K_3$. Swapping $K_3$ sends $b_2$ to $0$ and changes no other link vertex. The link becomes $(0,1,2,0,3)$.

This is Case 1. Its single swap, on the $\{1,3\}$-component of $a$, fills. The colours of $p$ and $q$ are still $0$ and $2$, so the cut fact still confines that component to $A\setminus F$. The link becomes $(0,3,2,0,3)$. **Two swaps.**

This completes the theorem.

## Where Kempe's argument failed, and why it holds here

**[cited]** At a degree-$5$ vertex in a general triangulation, Kempe (1879) performed two chain swaps at once, and Heawood (1890) showed that the second chain can be altered by the first. In Case 2, without the chord $pq$, the $\{1,3\}$-component of $a$ may reach $b_1$, and the final swap would then put colour $1$ back on the link. The separating triangle blocks that component, since $p$ and $q$ carry the other two colours. The two swaps are sequential, and each is checked on the colouring it acts on.

## Check against the certificates

**[hand]** The order-$6$ certificate of (C) has $L_1=(b_1,q)$, the chord. The component of $b_2$ in colours $\{0,1\}$ is $(b_2)$, because the neighbours $q,b_1$ of $b_2$ in $T-f$ have colours $2,3$. Swap $(b_2)$, then swap the component $(a)$ in colours $\{1,3\}$. The link becomes $(0,3,2,0,3)$.

**[hand]** The order-$9$ certificate of (C) has $L_1=(b_1,u,v,q)$. Its colours are $p,a,q,b_2,b_1,u,v,w=0,1,2,1,3,2,3,0$. The neighbours of $b_2$ in $T-f$ are $q,b_1,u,w$, with colours $2,3,2,0$. The neighbours of $w$ are $b_2,q,v,u$, with colours $1,2,3,2$. So the component of $b_2$ in colours $\{0,1\}$ is $(b_2,w)$, and it misses $p$. Swap it: $b_2\mapsto 0$, $w\mapsto 1$. The neighbours of $w$ then have colours $0,2,3,2$, so the colouring stays proper there. The neighbours of $a$ in $T-f$ are $p,q$, so its component in colours $\{1,3\}$ is $(a)$. Swap it. The link becomes $(0,3,2,0,3)$. This is a second two-swap fill, beside the one in (C).

The page's double lock was $L_1$ together with the lock $L_2$ in (C) (a $\{0,3\}$-path from $b_2$ to $p$ after the $\{1,3\}$-swap at $b_2$). The theorem does not need $L_2$, because the lock $L_3$ is always open when $L_1$ is closed. This answers the open sentence of (C) and of `../DIRECTOR.md`: every double-locked interior fills by two Kempe swaps at $f$.

## Consequence for the interior-witness lift

**[hand] Lift with one landing on the triangle.** Keep the hypotheses of `interior-witness.md` (A), with one change. The filling path in $A$ may leave $A\setminus F$ by a singleton slide from $h\in A\setminus F$ onto a vertex $f\in F$ with $\deg_T(f)=5$. Truncate the path at the first such slide. Then $(r,\tau)$ is a good pair of $T$.

The steps before the slide lift by (A), with the same invariant. The slide $h\to f$ is legal in $T$, because $N_T(h)=N_A(h)$ with the same cyclic order (the interior-slide paragraph of (A); the legality uses only the link of $h$). The resulting state of $T$ has its hole at $f$. The theorem then reaches the fill set of $T$ by at most two Kempe swaps at $f$. The truncated path in $A$ is not required to fill in $A$.

So the hole-on-the-triangle gap of `interior-witness.md` (F) narrows. In a smallest failure, a witness on a side whose path lands on $F$ has its first landing at a vertex of $T$-degree at least $6$. Paths that reach $F$ by a Kempe step are impossible, because a Kempe step keeps its hole.

## What this does not do

- It does not treat a hole on $F$ at a vertex of $T$-degree at least $6$. There the link has length at least $6$, and the two-case analysis above, which used the five-vertex shape $(p,a,q,b_2,b_1)$, does not apply. A four-coloured link with no singleton needs at least $8$ vertices.
- It does not treat the carry across an inner triangle in (D).
- It does not decide whether a smallest failure contains a separating triangle.
- It does not touch a vertex cut of size $4$.

## Which VH∃ step this advances

Line 1 of `VHExistsAttack.md`: the minimal failure and separating triangles. It removes one of the two named gaps in (F) for degree-$5$ landings, and the director's open sentence is answered.

## Re-lining of the connectivity note

**[hand]** The director had asked for this. I re-lined the $3$-connectedness argument in `positions/connectivity.md`: minimum degree $3$, connectedness via the dual graph, no cut-vertex by rerouting around the link $C_v$, and no $2$-cut by the link-block count. The $3$-cut-to-separating-triangle step (B) and the order-$\ge5$ equivalence were also re-lined. Each step stands. One sentence is topological and is stated rather than derived: in the degree-$2$ case, the two triangles cover the sphere. It follows from the same open-and-closed argument the note uses for the dual graph. No correction is needed.

## Feasibility

| Question | Rating |
|---|---|
| The fixed-hole theorem at a degree-$5$ vertex of a separating triangle | High |
| The lift with one landing on a $T$-degree-$5$ vertex of $F$ | High |
| A fixed-hole fill at a vertex of $F$ of $T$-degree $\ge 6$ by Kempe swaps alone | Low to Medium, not attempted (the case count grows with the arcs, and a fixed hole of degree $\ge 6$ is not a VH situation in general) |
| A smallest failure contains a separating triangle | Medium-Low, unchanged; the remaining gaps are the degree-$\ge6$ landing and the carry in (D) |

## Next steps

1. The degree-$\ge6$ landing. The hole on $F$ is not required: the lift can choose a different path, or stop before $F$. The question is whether the side's filling path can always be re-routed so that its first landing on $F$ is at a $T$-degree-$5$ vertex, or never lands. One possible handle is the A-side degree of $f$, since $\deg_A(f)=3$ forced the shape used here.
2. The carry in (D), which is unchanged.

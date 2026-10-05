# Defect position and chain energy

5 October 2026. Physicist, Potential team, Creative Intel. The path is order 24, graph 7228, vertex 17, fan 0. The link colours, the chains, and the three moves are those written in section D of `backgroundMaterial/planemap-structural/longtable/wp19/counterexample-analysis.md`. The kill test is the one in `SolvingFrameworkPlan/docs/working/VHExistsPotential.md`: one integer, defined at the degree-6 hole, and strictly smaller after the slide and after each of the two swaps. This page names two integers. It enumerates no graph.

## What a drop is allowed to remember

**[hand]** On the belt, a policy names each return, and the potential $\Phi$ is an integer built from the current hole and an auxiliary copy of the input colouring. Every return lowers $\Phi$. The auxiliary copy is a ghost variable, extra state a termination argument may remember.

**[post hoc]** The four states below were found first. An integer scored on those states afterwards records that trajectory. A policy names a legal move from a hole and a colouring. A ghost copy of the start colouring may still appear in a later sentence. The two integers defined here are the whole proposal, and the test is this path.

**[hand]** The fitted ranks $q$, $\mathrm{lin}$, and the others are already killed, and so are the height, sandpile, flow, and monodromy readings as fitted ranks. What follows is a defect count and a chain length, each put through the kill test above.

## The published states

**[hand]** Hole $17$ has link $(7,16,23,18,8)$ coloured $(3,1,0,1,2)$, with $\alpha=1$, $\beta=0$, $\gamma=2$, $\delta=3$. The lock is witnessed by the $\beta\gamma$-path $P=23$–$15$–$6$–$5$–$13$–$20$–$19$–$8$ and the $\beta\delta$-path $Q=23$–$22$–$19$–$12$–$13$–$14$–$6$–$7$. Both chains pass through the degree-8 hub $19$, and through $13$ and $6$. Vertex $8$ has degree $6$. It lies in the cut-component and on the link, and the edge $8$–$18$ welds the other link vertex $18$ of that component across the face $17$–$8$–$18$.

**[hand]** The slide $17\to 8$ writes $\gamma=2$ on $17$, deletes the bridge vertex $8$, and leaves the degree-6 link $(1,7,17,18,19,9)$ coloured $(1,3,2,1,0,3)$. The $\beta\gamma$-chain at the new hole is $19$–$20$–$13$–$5$–$6$–$15$–$23$–$17$. The swap of colours $\{1,2\}$ on $E'=\{1,2,4,5,10,11\}$ cuts $P$ at $5$ and recolours link vertex $1$ from $1$ to $2$, so the link is $(2,3,2,1,0,3)$. The swap of colours $\{0,2\}$ on $\{0,1,4,6,15,17,23\}$ frees colour $2$, and the link is $(0,3,0,1,0,3)$.

**[hand]** The link uses four colours on the first three states and three colours on the filled state.

## 1. Defect position

**[hand]** A degree-5 link that uses four colours and is unfilled has multiplicities $2,1,1,1$. The repeated colour sits on two non-adjacent vertices. Each of the other three colours sits on one vertex. Call that vertex a defect. Its position is the vertex, and a slide may move the hole there, because the colour meets the link once.

Three positions determine one coordinate-free integer, the number of defects. For a hole $h$ and a colouring $c$ of $T-h$, $N_1(h,c)$ is the number of link vertices whose colour appears once on the link. Equivalently, $N_1$ is the number of singleton colours. The count uses only the link, and it is defined at degree $6$.

**[hand]** The start has multiplicities $2,1,1,1$, so $N_1=3$: colour $3$ at $7$, colour $0$ at $23$, and colour $2$ at $8$. After the slide the multiplicities are $2,2,1,1$, so $N_1=2$: colour $2$ at $17$ and colour $0$ at $19$. Colour $2$ is still unique, now on the old hole, which received it from the bridge. Colour $0$ is still unique, now at the hub $19$. Colour $3$ occurs at both $7$ and $9$, so it has left the singleton class. The third vertex of the face, $18$, carries the repeated colour $1$ before the slide and after it.

**[hand]** Across the swap on $\{1,2\}$, the only link vertex that changes colour is vertex $1$, from $1$ to $2$. Colour $2$ becomes a pair, at $1$ and $17$, and colour $1$ becomes a singleton, at $18$. The multiplicities are again $2,2,1,1$, and $N_1=2$. The cut of $P$ exchanges one defect for another.

**[hand]** Across the swap on $\{0,2\}$, colour $2$ leaves the link. The filled link $(0,3,0,1,0,3)$ has one singleton, colour $1$ at $18$, so $N_1=1$. The four values are $3,2,2,1$.

**[post hoc]** $N_1$ is defined at the degree-6 hole and falls on the slide. It takes the same value $2$ on both sides of the swap that cuts $P$. The filled link still has $N_1=1$. Writing $0$ by convention at a fill leaves those two middle values equal. A further integer built from the positions of the two defects on the $6$-cycle would be a weight fitted to this trajectory. Defect position is killed.

## 2. Chain energy

**[hand]** Until the link is filled, the energy is the total number of vertices on the two Kempe chains that witness the lock, the $\beta\gamma$-path and the $\beta\delta$-path between the relevant link vertices. The energy of a filled state is $0$.

**[hand]** At the start, $|P|=8$ and $|Q|=8$, so the energy is $16$. After the slide the published $\beta\gamma$-chain has the eight vertices $19,20,13,5,6,15,23,17$. The seven vertices $23,15,6,5,13,20,19$ are kept, in reverse order, and the endpoint $8$ is replaced by the endpoint $17$. The hub $19$ lies on $P$ before the slide and on this chain after it. The published $Q$ does not contain $8$, so deleting the bridge removes no vertex of that path. A $\beta\delta$-chain at hole $8$ is unpublished.

**[post hoc]** The sum falls on the slide only if that missing chain has fewer than eight vertices. No such length is published. The length written on both sides of the slide is $8$, then $8$. Chain length is constant on the slide for the chain the slide rewrites, and chain length is killed as a Lyapunov function on this path.

## Degree height

**[hand]** A sandpile height equal to the degree of each vertex depends only on the triangulation, and the triangulation is unchanged along the path. The height is constant, and it is killed.

## Result

Both candidates are killed.

Feasibility that a physical energy survives this path: **Low**.

The sentence to keep: the slide $17\to 8$ carries the colour-$\gamma$ defect from the bridge $8$ onto $17$ and leaves the $\beta\gamma$-chain at eight vertices, while the swap that cuts $P$ exchanges one singleton colour for another, so each candidate is constant on a step that still stands between the start and the fill.

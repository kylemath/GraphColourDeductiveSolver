# Hole support on Florek's $G_8$

**KILL.** $|S|=18$, and both poles are in $S$.

Order 18, graph 10, is the two-pole antiprism suspension $G_8$. Singleton slides from the published population-$(2,5,5,5)$ start move the hole onto every vertex, including both degree-8 poles. The component closes at 32 states, under a cap of 4000. The belt-only description of the hole set is killed. The maximum-degree-6 cycle lemma does not explain this component: that lemma assumed maximum degree 6, and $S$ contains vertices of degree 8.

This is a finite recomputation of one published component. It is not a navigator status.

## The graph

The graph is the plantri triangulation in discovery table `18-10-r0.json.gz`, ASCII sha256 `67e31585c316fff25996c9f2cecbe14a05d89f62839eff62e773de1e4685d61f`. Degrees are 8 at vertices 3 and 6, and 5 elsewhere. Vertices 3 and 6 are nonadjacent. The link of 3 is the cycle

$$(0,2,8,9,10,11,12,4),$$

and the link of 6 is the cycle

$$(1,5,13,14,15,16,17,7).$$

These cycles partition the belt. Each belt vertex meets exactly one pole. Each vertex of the first cycle meets two consecutive vertices of the second, which is the antiprism rule in `SolvingFrameworkPlan/docs/reports/TwoPoleStarEscape.md` for $n=8$. The poles are $a=3$ and $b=6$.

## The component

The start is table `18-10-r0`, state 93, hole at vertex 0. In vertex order, with the hole written $-$, the canonical colouring is

$$(-,\,0,1,2,1,3,2,3,0,3,1,0,3,0,1,3,0,1).$$

The sorted counts on the coloured vertices are $(2,5,5,5)$. A singleton slide moves the hole to a neighbour whose colour appears once on the boundary, copies that colour onto the old hole, and renames colours by first appearance in vertex order. Breadth-first search from this state closes after 32 states. Every state keeps population $(2,5,5,5)$. Every boundary uses four colours.

The sixteen published targetless starts, `18-10-r0` state 93 and the fifteen siblings in `vacancy-population-results.json`, are sixteen states of this same component, one at each belt vertex. Those tables are degree-five root tables. The pole-hole states appear when the hole moves.

$$S=\{0,1,\ldots,17\}.$$

The sixteen belt vertices have degree 5, and each is the hole in one state. Vertices 3 and 6 have degree 8, and each is the hole in eight states. Both poles are in $S$. The induced subgraph $G[S]$ is the triangulation, with $3\cdot 18-6=48$ edges, so it contains a cycle. The link of vertex 3 is one such cycle.

## A slide onto a pole

The link of hole 0 is $(1,2,3,4,5)$ with colours $(0,1,2,1,3)$. Colour 2 occurs once, at vertex 3. The slide $0\to 3$ writes colour 2 on vertex 0 and deletes 3. Before renaming, the landing is

$$(2,\,0,1,-,1,3,2,3,0,3,1,0,3,0,1,3,0,1).$$

First appearance renames old colours $2,0,1,3$ to $0,1,2,3$, so the canonical state is

$$(0,\,1,2,-,2,3,0,3,1,3,2,1,3,1,2,3,1,2).$$

Pole 6 is reached as well. From the unique belt state at each neighbour of 3 there is a slide to 3, and from each neighbour of 6 there is a slide to 6. Those neighbour sets are the two rings above. A slide keeps the counts $(2,5,5,5)$, so the pole hole is still unfilled.

## The star swap inside the component

All sixteen belt-hole states give the two poles the same colour, and no belt vertex carries it. The star swap of `TwoPoleStarEscape.md` is one Kempe swap at each of those states.

On the start state the common pole colour is $A=2$, present only at vertices 3 and 6. Hole 0 lies on the ring of pole 3. Its two neighbours on the other ring are the adjacent vertices 1 and 5, coloured 0 and 3. Both colours occur once on the five-vertex boundary. Take $B=0$ at vertex 1. The $(2,0)$-component containing pole 6 is exactly

$$\{1,6,13,16\},$$

pole 6 together with the three colour-0 vertices on its ring. Properness keeps those three pairwise nonadjacent, and each meets 6. Pole 3 lies in the other $(2,0)$-component, $\{3,8,11\}$. Swapping colours 2 and 0 on $\{1,6,13,16\}$ changes only vertex 1 on the boundary. The boundary colours become $(2,1,2,1,3)$. Colour 0 is free. Writing 0 on the hole is a proper colouring of $G_8$, of population $(4,4,5,5)$.

The other fifteen belt states behave the same way: the Kempe component has size 4, and filling the hole produces a proper colouring of population $(4,4,5,5)$. For $n=8$ and $k=2$, size 4 is the pole plus the $k+1$ belt vertices in the note.

## Reading

$|S|=18$, with both poles included.

- The hole set stays on the belt: killed, because poles 3 and 6 occur as the hole.
- The maximum-degree-6 cycle lemma explains this component: killed, because a degree-8 vertex lies in $S$. The induced subgraph contains a cycle; with 48 edges it is the whole triangulation.

The component closed inside the cap. The wall case would have been $S$ equal to the sixteen belt vertices, with no slide onto a pole. Here the poles are reachable by slides, and the star swap is already available while the hole is a belt vertex.

Feasibility of this finite reading: **High**.

## Next steps

1. Use the star swap at the belt hole. A slide onto a pole keeps the population $(2,5,5,5)$ and leaves the same obstruction.
2. Every belt state in this component has equal pole colours. A colouring with unequal poles, on $G_8$ or a larger $G_n$, is the case the star argument does not cover.
3. Name a rank on the pair $(\text{hole},\text{colouring})$ that falls when the star swap takes $(2,5,5,5)$ to a filled $(4,4,5,5)$, and that does not read a pass/fail label.

Recomputed by `backgroundMaterial/planemap-structural/longtable/swarm/hole_support.py`. The recorded numbers are in `hole-support-data.json`.

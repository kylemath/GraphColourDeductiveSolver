# Two population-changing Kempe swaps

**KILL.** On a $21$-vertex spherical triangulation of minimum degree $5$, one explicit partial colouring has a targetless slide component, and every single Kempe swap from that component lands in another targetless slide component. A second population-changing swap then creates a singleton, and one slide fills the vacancy.

Orders $12$ through $20$ have no such colouring. The order-$18$ graph $10$ starts of population $(2,5,5,5)$ remain one-swap escapes. Capped pentagonal cylinders with $3$, $4$ and $5$ rings have no targetless slide component at all.

## The triangulation

Twenty-one vertices, plantri rotation

$$21\ \texttt{bcdef,aflghijkc,abkmd,acmnoe,adopqf,aeqlb,blrsh,bgsoi,bhotj,bituk,bjumc,bfqrg,ckund,dmuto,dntihspe,eosrq,eprlf,glqps,grpoh,ionuj,jtnmk}.$$

Degrees are $9$ at vertex $1$, $8$ at vertex $14$, $6$ at vertices $3$ and $4$, and $5$ elsewhere. It is a simple spherical triangulation: $63$ edges, $42$ triangular faces, minimum degree $5$. This is one of the $191$ expansions, by a single vertex split, of the $73$ order-$20$ minimum-degree-$5$ triangulations. The complete census through order $20$ is recorded below.

The deleted vertex is $1$. Its link, in rotation order, is

$$(0,5,11,6,7,8,9,10,2).$$

## The colouring

Colours are $\{0,1,2,3\}$. With vertex $1$ deleted, the colouring in vertex order is

$$(0,-,1,2,1,2,0,1,2,0,3,3,0,1,0,2,0,1,3,3,2).$$

Every edge with both ends coloured joins different colours. The sorted colour-count on the twenty coloured vertices is $(4,5,5,6)$. That same sorted count also occurs for extendable colourings of this graph. The lock on this representative is the link. The link colours are

$$(0,2,3,0,1,2,0,3,1).$$

Colour $0$ appears three times and colours $1$, $2$ and $3$ twice each. All four colours are present, so the vacancy does not fill, and no colour is unique, so the vacancy does not slide. The slide component is this single state.

The full colourings of the graph, read off by completing every three-colour link at vertex $1$, have sorted counts $(3,6,6,6)$, $(4,5,6,6)$ and $(5,5,5,6)$. Deleting one vertex from those gives the extendable partial counts

$$(2,6,6,6),\ (3,5,6,6),\ (4,4,6,6),\ (4,5,5,6).$$

## One Kempe swap stays targetless

A Kempe swap exchanges the two colours on one bichromatic component of the coloured subgraph. Components that are a global exchange of two colours reproduce the same colouring up to renaming and are omitted. The sixteen remaining swaps are below. In every image the vacancy is still at vertex $1$, the link still uses all four colours, and every link colour still appears at least twice. Each image is therefore its own slide component, and that component has no fill. The search is exhaustive: sixteen swaps, each component of size $1$, no truncation.

| Colours | Component | $|n_a-n_b|$ | Sorted counts |
| --- | --- | ---: | --- |
| $0,1$ | $\{0,2,4,6,7,12,13,14,16,17\}$ | $0$ | $(4,5,5,6)$ |
| $0,1$ | $\{9\}$ | $1$ | $(4,5,5,6)$ |
| $0,2$ | $\{0,3,5,8,9,12,14,15,16,20\}$ | $0$ | $(4,5,5,6)$ |
| $0,2$ | $\{6\}$ | $1$ | $(4,5,5,6)$ |
| $0,3$ | $\{0\}$ | $1$ | $(5,5,5,5)$ |
| $0,3$ | $\{6,9,10,11,12,14,16,18,19\}$ | $1$ | $(5,5,5,5)$ |
| $1,2$ | $\{2,3,4,5,13,15,17,20\}$ | $0$ | $(4,5,5,6)$ |
| $1,2$ | $\{7,8\}$ | $0$ | $(4,5,5,6)$ |
| $1,3$ | $\{2,10\}$ | $0$ | $(4,5,5,6)$ |
| $1,3$ | $\{4\}$ | $1$ | $(4,5,5,6)$ |
| $1,3$ | $\{7,11,17,18\}$ | $0$ | $(4,5,5,6)$ |
| $1,3$ | $\{13,19\}$ | $0$ | $(4,5,5,6)$ |
| $2,3$ | $\{3\}$ | $1$ | $(4,5,5,6)$ |
| $2,3$ | $\{5,11\}$ | $0$ | $(4,5,5,6)$ |
| $2,3$ | $\{8,10,19,20\}$ | $0$ | $(4,5,5,6)$ |
| $2,3$ | $\{15,18\}$ | $0$ | $(4,5,5,6)$ |

The two swaps of colours $0$ and $3$ are the ones that change the sorted count. They land on $(5,5,5,5)$, which is not an extendable partial count, so no later slide can fill them either. The other fourteen swaps keep a four-colour link with no unique colour, whether or not the underlying transfer of one vertex preserves the sorted count.

## Two population-changing swaps, then a slide

Swap colours $0$ and $3$ on the singleton $\{0\}$. Vertex $0$ changes from $0$ to $3$. The colouring is

$$(3,-,1,2,1,2,0,1,2,0,3,3,0,1,0,2,0,1,3,3,2),$$

with sorted count $(5,5,5,5)$. The link is $(3,2,3,0,1,2,0,3,1)$. It is still frozen.

From there, swap colours $0$ and $1$ on the component

$$\{2,4,6,7,12,13,14,16,17\}.$$

That set is a connected piece of the subgraph of colours $0$ and $1$, and it meets no further vertex of those colours. The sorted count returns to $(4,5,5,6)$, and the link of vertex $1$ is

$$(3,2,3,1,0,2,0,3,0).$$

Colour $1$ appears once, at vertex $6$. The slide recolours vertex $1$ with colour $1$ and deletes vertex $6$. The link of vertex $6$ is $(1,11,17,18,7)$ with colours $(1,3,0,3,0)$. Colour $2$ is missing. Colouring vertex $6$ with $2$ is a proper colouring of the whole triangulation.

Both swaps change the sorted colour-count: $(4,5,5,6)\to(5,5,5,5)\to(4,5,5,6)$. The slide then fills.

## What was ruled out

Every minimum-degree-$5$ triangulation of order $12$ through $20$ was read from the plantri census ($118$ graphs: $1,0,1,1,3,4,12,23,73$ by order). At every vertex, every deletion colouring was expanded to its slide component. Every targetless component had a Kempe swap into a component that contains a fill. Order $21$ is the first order with an example.

Order $18$ graph $10$ was not reopened as a search. Its sixteen published starts have sorted count $(2,5,5,5)$ on seventeen coloured vertices. The only extendable partial counts on that graph are $(3,4,5,5)$ and $(4,4,4,5)$, and $(2,5,5,5)$ meets $(3,4,5,5)$ by moving one vertex from a class of size $5$ onto the class of size $2$. That is one transfer. The published table already records a one-swap escape for each of the sixteen.

The capped pentagonal cylinder with $m$ rings, $m\in\{3,4,5\}$, has $5m+2$ vertices. Every deletion colouring at every vertex slides to a fill. There is no targetless component on which a second swap could be required. The same holds for the octagonal barrel with three rings ($26$ vertices). The barrel with four rings ($34$ vertices) has targetless components, and each of them unlocks with one swap.

Two copies of the equal-pole barrel were glued along a common face. For link length $5$ the resulting $21$-vertex graph unlocks with one swap, as does link length $7$ ($29$ vertices) and a mixed glue of link lengths $8$ and $5$ ($27$ vertices). Link length $8$ against link length $7$ ($31$ vertices) and two copies of link length $8$ ($33$ vertices) do contain two-swap colourings, both larger than the $21$-vertex witness. A single barrel of link length $11$ ($24$ vertices) also contains one. None of these is smaller than the witness above.

Feasibility of “slides, at most one Kempe swap, slides, fill” as a method for every partial colouring of every minimum-degree-$5$ triangulation: **Low**.

## Next step

On this witness the second population-changing swap does produce a fill, so the example does not touch a hybrid that is allowed two Kempe swaps. The concrete next question is whether some explicit colouring on a minimum-degree-$5$ triangulation has every two-swap exit still targetless.

# Frozen link, one colouring

**INTERIOR.** Six of the sixteen non-global Kempe swaps are frozen by the coloured link, on every triangulation that carries it. The other ten are frozen by this interior. Recolouring interior vertices of this same triangulation, with the link held fixed, produces a singleton on each of the three pairs drawn from $\{1,2,3\}$. The list of sixteen is an example.

The graph, the rotation, and the colouring are those of `swarm/two-kempe-kill.md`. The hole is vertex $1$. The link, in rotation order, is

$$(0,5,11,6,7,8,9,10,2)$$

with colours

$$(0,2,3,0,1,2,0,3,1).$$

Colour $0$ meets the link three times, at vertices $0$, $6$ and $9$. Colours $1$, $2$ and $3$ meet it twice, at $\{7,2\}$, $\{5,8\}$ and $\{11,10\}$. The link multiplicity is $(3,2,2,2)$. The sorted count on the twenty coloured vertices is $(4,5,5,6)$. The sixteen components below were recomputed with the bichromatic walk from `mass_core` and match the table in `two-kempe-kill.md`.

A Kempe swap exchanges colours $a$ and $b$ on one component of the subgraph induced by those colours in the triangulation with vertex $1$ deleted. Only link vertices in the component change colour on the link. If the component meets the link in $k_a$ vertices of colour $a$ and $k_b$ of colour $b$, the new link counts are

$$n_a-k_a+k_b,\qquad n_b-k_b+k_a,$$

and the other two counts stay where they are. A singleton is a link count equal to $1$. The nine link edges are the only edges of the link: this triangulation has no chord of the $9$-cycle. A chord on another triangulation would only merge the blocks below. It cannot split them, because each block is already joined by a link edge.

## Blocks forced by the link

Write the cycle as

$$0(0)-5(2)-11(3)-6(0)-7(1)-8(2)-9(0)-10(3)-2(1)-0(0).$$

The two link neighbours of each colour-$0$ vertex are the two colours among $\{1,2,3\}$ other than one omitted colour. Vertex $0$ omits $3$, vertex $6$ omits $2$, and vertex $9$ omits $1$. Consequently every pair $(0,c)$ has the same block shape: two link edges, each gluing one remaining colour-$0$ vertex to one $c$-vertex, and one isolated colour-$0$ vertex.

| Pair | Blocks on the link |
| --- | --- |
| $0,1$ | $\{0(0),2(1)\}$, $\{6(0),7(1)\}$, $\{9(0)\}$ |
| $0,2$ | $\{0(0),5(2)\}$, $\{6(0)\}$, $\{8(2),9(0)\}$ |
| $0,3$ | $\{0(0)\}$, $\{11(3),6(0)\}$, $\{9(0),10(3)\}$ |
| $1,2$ | $\{5(2)\}$, $\{7(1),8(2)\}$, $\{2(1)\}$ |
| $1,3$ | $\{11(3)\}$, $\{7(1)\}$, $\{10(3),2(1)\}$ |
| $2,3$ | $\{5(2),11(3)\}$, $\{8(2)\}$, $\{10(3)\}$ |

On any triangulation with this coloured link, the intersection of a component with the link is a union of these blocks.

## Right subsets

A subset of the link is right when swapping exactly those vertices makes some colour appear once. For a pair $(0,c)$ the right count pairs $(k_0,k_c)$ are $(2,0)$, $(0,1)$ and $(1,2)$. For a pair of two doubleton colours the right count pairs $(k_a,k_b)$ are $(1,0)$, $(0,1)$, $(2,1)$ and $(1,2)$.

No union of the $(0,c)$ blocks is right. Each mixed block contributes one colour-$0$ vertex and one $c$-vertex, and the isolated block contributes one colour-$0$ vertex. If $k_c$ is the number of mixed blocks in the union, then $k_0=k_c$ or $k_0=k_c+1$.

- $(2,0)$ asks for two colour-$0$ vertices and no $c$-vertex. With no mixed block, $k_0\le 1$.
- $(0,1)$ asks for a $c$-vertex and no colour-$0$ vertex. Every block contains a colour-$0$ vertex.
- $(1,2)$ asks for both $c$-vertices and one colour-$0$ vertex. Both mixed blocks already contribute two colour-$0$ vertices.

The other two link counts are $2$ or $3$, so they stay repeated. Every one of the seven nonempty unions leaves multiplicity $(3,2,2,2)$. The same holds for the empty intersection. In particular, the union of all three blocks swaps all three colour-$0$ vertices, and the replacement colour was already on the link twice, so colour $0$ remains on those two former $c$-vertices. That union is a global exchange when the component contains every vertex of the two colours, and it is omitted from the sixteen. It is still free of singletons.

The right unions of the doubleton blocks are:

| Pair | Right link intersection | Singleton |
| --- | --- | --- |
| $1,2$ | $\{5\}$ | colour $2$ at vertex $8$ |
| $1,2$ | $\{2\}$ | colour $1$ at vertex $7$ |
| $1,2$ | $\{5,7,8\}$ | colour $2$ at vertex $7$ |
| $1,2$ | $\{2,7,8\}$ | colour $1$ at vertex $8$ |
| $1,3$ | $\{11\}$ | colour $3$ at vertex $10$ |
| $1,3$ | $\{7\}$ | colour $1$ at vertex $2$ |
| $1,3$ | $\{11,10,2\}$ | colour $3$ at vertex $2$ |
| $1,3$ | $\{7,10,2\}$ | colour $1$ at vertex $10$ |
| $2,3$ | $\{8\}$ | colour $2$ at vertex $5$ |
| $2,3$ | $\{10\}$ | colour $3$ at vertex $11$ |
| $2,3$ | $\{5,11,8\}$ | colour $2$ at vertex $11$ |
| $2,3$ | $\{5,11,10\}$ | colour $3$ at vertex $5$ |

## The sixteen swaps

For each swap, the named link vertex is a vertex a right subset would recolour. The last column is the intersection of the published component with the link. None of those intersections is a row of the right-union table.

| Swap | Vertex | Right subset of the repeated colour | Link vertices in the component | Reason |
| --- | --- | --- | --- | --- |
| $0,1$ on $\{0,2,4,6,7,12,13,14,16,17\}$ | $0$ | $\{0,6\}$ of colour $0$, leaving the singleton at $9$ | $\{0,2,6,7\}$ | A |
| $0,1$ on $\{9\}$ | $0$ | $\{0,9\}$ of colour $0$ | $\{9\}$ | B |
| $0,2$ on $\{0,3,5,8,9,12,14,15,16,20\}$ | $0$ | $\{0,9\}$ of colour $0$, leaving the singleton at $6$ | $\{0,5,8,9\}$ | A |
| $0,2$ on $\{6\}$ | $0$ | $\{0,6\}$ of colour $0$ | $\{6\}$ | B |
| $0,3$ on $\{0\}$ | $6$ | $\{0,6\}$ of colour $0$ | $\{0\}$ | B |
| $0,3$ on $\{6,9,10,11,12,14,16,18,19\}$ | $6$ | $\{6,9\}$ of colour $0$, leaving the singleton at $0$ | $\{6,9,10,11\}$ | A |
| $1,2$ on $\{2,3,4,5,13,15,17,20\}$ | $5$ | $\{5\}$ of colour $2$ | $\{2,5\}$ | C |
| $1,2$ on $\{7,8\}$ | $5$ | $\{5,8\}$ of colour $2$, with colour-$1$ subset $\{7\}$ | $\{7,8\}$ | C |
| $1,3$ on $\{2,10\}$ | $11$ | $\{11\}$ of colour $3$ | $\{2,10\}$ | C |
| $1,3$ on $\{4\}$ | $7$ | $\{7\}$ of colour $1$ | none | D |
| $1,3$ on $\{7,11,17,18\}$ | $7$ | $\{7\}$ of colour $1$ | $\{7,11\}$ | C |
| $1,3$ on $\{13,19\}$ | $11$ | $\{11\}$ of colour $3$ | none | D |
| $2,3$ on $\{3\}$ | $8$ | $\{8\}$ of colour $2$ | none | D |
| $2,3$ on $\{5,11\}$ | $8$ | $\{8\}$ of colour $2$ | $\{5,11\}$ | C |
| $2,3$ on $\{8,10,19,20\}$ | $8$ | $\{8\}$ of colour $2$ | $\{8,10\}$ | C |
| $2,3$ on $\{15,18\}$ | $10$ | $\{10\}$ of colour $3$ | none | D |

## Four reasons

**A. Two colour-$0$ copies flip, and both partner vertices flip with them.** The large $(0,1)$ component contains colour-$0$ vertices $0$ and $6$ and leaves $9$. The right subset of colour $0$ is $\{0,6\}$. The component also contains $2$ and $7$. The link edge $2-0$ glues vertex $2$ to vertex $0$, and the link edge $6-7$ glues vertex $7$ to vertex $6$, so those two colour-$1$ vertices become colour $0$ and colour $0$ is back to three copies. The large $(0,2)$ component likewise contains $\{0,9\}$ together with the glued partners $5$ and $8$, and the spared colour-$0$ vertex is $6$. The large $(0,3)$ component contains $\{6,9\}$ together with the glued partners $11$ and $10$, and the spared colour-$0$ vertex is $0$. This is the published interior's way of occupying two mixed blocks. Every other union is already ruled out by the count argument above, so the reason travels with the coloured link.

**B. Only the isolated colour-$0$ vertex flips.** The component $\{9\}$ of colours $0,1$ contains one of the three colour-$0$ vertices. A right subset of colour $0$ has two of them, for instance $\{0,9\}$, so vertex $0$ would have to change. The component contains $\{9\}$. The same holds for $\{6\}$ on colours $0,2$, where vertex $0$ would have to change, and for $\{0\}$ on colours $0,3$, where vertex $6$ would have to change. Those two-vertex subsets are not unions of blocks: the second colour-$0$ vertex arrives glued to a partner. Reason B is the isolated block of the same link lemma as reason A.

**C. The component takes one vertex of each of two doubleton colours.** Then $(k_a,k_b)=(1,1)$, both counts stay $2$, and the intersection is not a right union. Three of these intersections are single link edges, so the two vertices move together on every triangulation: $\{7,8\}$ on colours $1,2$, $\{2,10\}$ on colours $1,3$, and $\{5,11\}$ on colours $2,3$. The other three intersections are pairs of blocks joined through the interior.

- Colours $1,2$ join $\{5\}$ to $\{2\}$ along $5(2)-4(1)-3(2)-2(1)$. Vertex $4$ is the third vertex of the link edge $0-5$, so the link allows it the colours $\{1,3\}$. Vertex $3$ is the third vertex of the link edge $2-0$, so the link allows it $\{2,3\}$. The published colouring uses $1$ and $2$.
- Colours $1,3$ join $\{7\}$ to $\{11\}$ along $7(1)-18(3)-17(1)-11(3)$. Vertex $18$, third of $6-7$, may be $2$ or $3$. Vertex $17$, third of $11-6$, may be $1$ or $2$. The published colouring uses $3$ and $1$.
- Colours $2,3$ join $\{8\}$ to $\{10\}$ along $8(2)-19(3)-20(2)-10(3)$. Vertex $19$, third of $8-9$, may be $1$ or $3$. Vertex $20$, third of $9-10$, may be $1$ or $2$. The published colouring uses $3$ and $2$.

Each of those paths is the only path of its colour pair between the two blocks in the published colouring. The colours on the paths are choices the link leaves open.

**D. The component misses the link.** The four components $\{4\}$ and $\{13,19\}$ of colours $1,3$, and $\{3\}$ and $\{15,18\}$ of colours $2,3$, contain no link vertex. No link colour changes. The vertex named in the table is the link vertex a right subset of that colour pair would recolour: $7$ or $11$ for colours $1,3$, and $8$ or $10$ for colours $2,3$.

## Another colouring of this interior

The link colours may be held fixed and the eleven interior vertices recoloured. There are $12$ proper colourings. The published one is among them. The distinct link intersections are as follows. Counts are numbers of colourings.

| Pair | Link intersections | Colourings |
| --- | ---: | ---: |
| $0,1$ | $\{0,2,6,7\}$ and $\{9\}$ | $6$ |
| $0,1$ | $\{0,2,6,7,9\}$ | $4$ |
| $0,1$ | $\{0,2\}$ and $\{6,7,9\}$ | $2$ |
| $0,2$ | $\{0,5,8,9\}$ and $\{6\}$ | $6$ |
| $0,2$ | $\{0,5,6,8,9\}$ | $4$ |
| $0,2$ | $\{0,5\}$ and $\{6,8,9\}$ | $2$ |
| $0,3$ | $\{0\}$ and $\{6,9,10,11\}$ | $4$ |
| $0,3$ | $\{0,6,9,10,11\}$ | $8$ |
| $1,2$ | $\{2,5\}$ and $\{7,8\}$ | $4$ |
| $1,2$ | $\{2\}$, $\{5\}$ and $\{7,8\}$ | $8$ |
| $1,3$ | $\{2,10\}$ and $\{7,11\}$ | $6$ |
| $1,3$ | $\{7\}$, $\{11\}$ and $\{2,10\}$ | $4$ |
| $1,3$ | $\{7\}$ and $\{11,10,2\}$ | $2$ |
| $2,3$ | $\{5,11\}$ and $\{8,10\}$ | $6$ |
| $2,3$ | $\{5,11\}$, $\{8\}$ and $\{10\}$ | $4$ |
| $2,3$ | $\{8\}$ and $\{5,11,10\}$ | $2$ |

Every $(0,c)$ row is a union of blocks, and none of those unions is right. The interior does move the blocks around. Joining all three, or joining the isolated colour-$0$ vertex to one mixed block, still leaves multiplicity $(3,2,2,2)$.

The doubleton rows do contain right intersections. Three explicit recolourings, each checked to be proper, give the singletons:

- Recolour vertex $4$ from $1$ to $3$. Colours $1,2$ fall into components with link intersections $\{5\}$, $\{2\}$ and $\{7,8\}$. Swapping $\{5\}$ leaves colour $2$ only at vertex $8$. Swapping the component of vertex $2$, which meets the link only at $2$, leaves colour $1$ only at vertex $7$.
- Recolour vertex $15$ from $2$ to $3$ and vertex $18$ from $3$ to $2$. This breaks $7-18-17-11$. Swapping $\{7\}$ leaves colour $1$ only at vertex $2$. Swapping the component of vertex $11$, which meets the link only at $11$ and which now contains the old interior vertex $4$, leaves colour $3$ only at vertex $10$.
- Recolour vertex $13$ from $1$ to $3$ and vertex $19$ from $3$ to $1$. This breaks $8-19-20-10$. Swapping $\{8\}$ leaves colour $2$ only at vertex $5$. Swapping the component of vertex $10$, which meets the link only at $10$ and which now contains the old interior vertex $3$, leaves colour $3$ only at vertex $11$.

In all twelve colourings the block $\{7,8\}$ remains a component of its own. This triangulation never joins it to $\{5\}$ or to $\{2\}$. The pair $(1,2)$ still unlocks, through $\{5\}$ and through $\{2\}$. The balanced edges $\{2,10\}$ and $\{5,11\}$ do grow, in two colourings each, to the right intersections $\{11,10,2\}$ and $\{5,11,10\}$.

## Which of the sixteen a different interior unlocks

A different interior means another proper colouring of these eleven vertices with the link fixed. It does not use a second graph.

The six swaps of reasons A and B cannot be unlocked. Their colour pairs are $(0,1)$, $(0,2)$ and $(0,3)$. Every union of their blocks keeps every link colour repeated, on any triangulation with this coloured link, so no interior supplies a right subset.

The other ten can be unlocked, in the sense that their colour pair has a right-subset component in one of the colourings above:

- both swaps of colours $1,2$, namely the component through $\{2,5\}$ and the edge $\{7,8\}$;
- all four swaps of colours $1,3$, namely $\{2,10\}$, $\{4\}$, $\{7,11,17,18\}$ and $\{13,19\}$;
- all four swaps of colours $2,3$, namely $\{3\}$, $\{5,11\}$, $\{8,10,19,20\}$ and $\{15,18\}$.

The unlock of $\{7,8\}$ is indirect. That edge stays a non-right component in every colouring of this interior. The same colourings that split $\{5\}$ from $\{2\}$ make those two blocks right subsets, so the pair has a singleton swap. The published failure of the edge itself is the link edge $7-8$. Enlarging it to $\{5,7,8\}$ or to $\{2,7,8\}$ is a right union the link allows and this triangulation never uses.

## Next step

The other half can take the $(0,c)$ block count as a lemma about the cycle $(0,2,3,0,1,2,0,3,1)$: every Kempe swap of a pair that contains colour $0$ preserves link multiplicity $(3,2,2,2)$. The same multiplicity on the pairs inside $\{1,2,3\}$ is a property of this interior. Eight of the twelve link-fixed colourings already separate vertex $5$ from vertex $2$.

Feasibility of “this coloured link is frozen under every Kempe swap, for every interior”: **Low**.

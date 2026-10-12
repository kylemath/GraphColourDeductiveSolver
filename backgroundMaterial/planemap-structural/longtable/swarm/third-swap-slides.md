# Third swap, then slides

**WALL.** On the $84$ ordered pairs, every third Kempe swap that creates a singleton reaches a link of three colours by singleton slides alone. The third swap is enough on these $84$. There are $27$ colour-renaming orbits. Every slide component closes, the largest has $818$ states, and the cap is $4000$.

## The pairs

The triangulation and the frozen colouring are those of `swarm/two-kempe-kill.md`. Twenty-one vertices, hole at vertex $1$, colouring

$$(0,-,1,2,1,2,0,1,2,0,3,3,0,1,0,2,0,1,3,3,2).$$

The link is $(0,5,11,6,7,8,9,10,2)$ with colours $(0,2,3,0,1,2,0,3,1)$. A Kempe swap exchanges the two colours on one bichromatic component of the triangulation with vertex $1$ deleted. A component that contains every vertex of its two colours is a global exchange and is omitted. The script is `swarm/third_swap_slides.py`. It uses `mass_core.canon` and the component walk in `swarm/two_swap_branches.py`.

The ordered pairs were recomputed. The census of `swarm/two-swap-branches.md` returns: $224$ pairs, $172$ frozen links, $52$ links with a unique colour, $24$ pairs back on the original colouring, and $148$ frozen pairs off that colouring, in $47$ renaming orbits. Each of those $148$ has between $2$ and $6$ third swaps, out of $10$ to $16$ non-global components, whose link has a unique colour or uses three colours.

A third swap fills at once when the link of vertex $1$ uses at most three colours, or when a unique vertex on that link has a link of at most three colours after the hole is given the unique colour. Sixty-four pairs have such a swap, and four of those sixty-four have a three-colour link at vertex $1$. The other $84$ are the pairs below. On each of them, every third swap that creates a singleton leaves four colours on the link of that singleton.

## One colouring per orbit

A permutation of $\{0,1,2,3\}$ renames the coloured vertices and leaves the hole fixed. A bichromatic component keeps its vertex set, and the renamed colour pair replaces the old one. The component is global precisely when its preimage is global. A colour appears once on a link precisely when its image does, and it appears at the same vertex. The slide onto that vertex uses the same number of colours on the new link, and every later slide moves the hole along the same vertices.

`mass_core.canon`, applied to the twenty coloured vertices in vertex order, is the renaming in which colours are numbered by first appearance. It selects one representative from each orbit. For every pair among the $84$, the transported components, the singleton vertices, and the normalised state after the slide onto each singleton agree with that representative. The $84$ pairs form $27$ orbits, of sizes

$$8,\ 4^{12},\ 3^{2},\ 2^{10},\ 1^{2}.$$

The slide search runs on the representative.

## Singleton slides

The third swap leaves the hole at vertex $1$ and makes some colour unique on its link. The search begins after the slide onto that vertex. A later move takes the hole to a neighbour whose colour appears once, and the vacated vertex receives that colour. No Kempe swap is used. States are stored up to the same first-appearance renaming, with the hole recorded apart from the colours.

The hole meets only its link. The partial colouring stays proper. A link that uses at most three colours therefore admits a missing colour, and that colour is a proper colouring of the whole triangulation. Such a state is a fill and is not slid out of. The search stops if a component reaches $4000$ states.

The $27$ representatives produce $118$ starts, one for each third swap and each singleton vertex on its link. First-appearance renaming identifies $71$ of those starts. Every component closes. Every one contains a link of exactly three colours, so each missing colour is unique. From the new hole, the number of slides to such a link is between $1$ and $7$. Component sizes run from $5$ to $818$. The fill is at a degree-$5$ vertex in $88$ starts and at a degree-$6$ vertex in the other $30$.

## Per orbit

Every orbit is filled by slides. “Images” counts the third-swap singletons of the representative. “Further slides” is the shortest and longest number of slides from the new hole to a three-colour link. Sizes are the numbers of reachable states, fills included.

| Orbit | Pairs | Count | Images | Sizes | Further slides |
| ---: | ---: | --- | ---: | --- | --- |
| $0$ | $8$ | $(5,5,5,5)$ | $2$ | $6$ | $1$ |
| $1$ | $4$ | $(4,5,5,6)$ | $3$ | $818$ | $1$–$3$ |
| $2$ | $4$ | $(4,5,5,6)$ | $3$ | $818$ | $1$–$3$ |
| $3$ | $4$ | $(5,5,5,5)$ | $6$ | $23,\ 530,\ 818$ | $1$–$2$ |
| $4$ | $4$ | $(5,5,5,5)$ | $6$ | $23,\ 530,\ 818$ | $1$–$2$ |
| $5$ | $4$ | $(4,5,5,6)$ | $3$ | $10,\ 48,\ 818$ | $1$–$3$ |
| $6$ | $4$ | $(4,5,5,6)$ | $3$ | $94,\ 818$ | $1$–$3$ |
| $7$ | $4$ | $(4,5,5,6)$ | $4$ | $10,\ 54,\ 226$ | $1$–$3$ |
| $8$ | $4$ | $(5,5,5,5)$ | $6$ | $94,\ 530,\ 818$ | $1$–$7$ |
| $9$ | $4$ | $(5,5,5,5)$ | $6$ | $94,\ 530,\ 818$ | $1$–$7$ |
| $10$ | $4$ | $(4,5,5,6)$ | $4$ | $10,\ 54,\ 226$ | $1$–$3$ |
| $11$ | $4$ | $(4,5,5,6)$ | $3$ | $94,\ 818$ | $1$–$3$ |
| $12$ | $4$ | $(4,5,5,6)$ | $3$ | $10,\ 48,\ 818$ | $1$–$3$ |
| $13$ | $3$ | $(4,5,5,6)$ | $6$ | $6,\ 10,\ 54$ | $1$–$3$ |
| $14$ | $3$ | $(4,5,5,6)$ | $6$ | $6,\ 10,\ 54$ | $1$–$3$ |
| $15$ | $2$ | $(4,5,5,6)$ | $4$ | $226$ | $2$–$3$ |
| $16$ | $2$ | $(5,5,5,5)$ | $6$ | $530,\ 818$ | $1$–$2$ |
| $17$ | $2$ | $(5,5,5,5)$ | $6$ | $530,\ 818$ | $1$–$2$ |
| $18$ | $2$ | $(4,5,5,6)$ | $4$ | $226$ | $2$–$3$ |
| $19$ | $2$ | $(5,5,5,5)$ | $6$ | $5,\ 530,\ 818$ | $1$–$2$ |
| $20$ | $2$ | $(5,5,5,5)$ | $2$ | $530$ | $1$–$2$ |
| $21$ | $2$ | $(4,5,5,6)$ | $6$ | $226,\ 530$ | $2$–$6$ |
| $22$ | $2$ | $(4,5,5,6)$ | $4$ | $226$ | $2$–$3$ |
| $23$ | $2$ | $(5,5,5,5)$ | $6$ | $5,\ 530,\ 818$ | $1$–$2$ |
| $24$ | $2$ | $(5,5,5,5)$ | $2$ | $530$ | $1$–$2$ |
| $25$ | $1$ | $(4,5,5,6)$ | $4$ | $54,\ 226$ | $1$–$4$ |
| $26$ | $1$ | $(4,5,5,6)$ | $4$ | $54,\ 226$ | $1$–$4$ |

One ordered pair from each orbit, in that pair’s own colour names:

| Orbit | First swap | Second swap |
| ---: | --- | --- |
| $0$ | $(0,3)$ on $\{0\}$ | $(1,2)$ on $\{2,3,4,5,13,15,17,20\}$ |
| $1$ | $(0,1)$ on $\{0,2,4,6,7,12,13,14,16,17\}$ | $(2,3)$ on $\{15,18\}$ |
| $2$ | $(0,2)$ on $\{0,3,5,8,9,12,14,15,16,20\}$ | $(1,3)$ on $\{13,19\}$ |
| $3$ | $(0,3)$ on $\{0\}$ | $(1,3)$ on $\{13,19\}$ |
| $4$ | $(0,3)$ on $\{0\}$ | $(2,3)$ on $\{15,18\}$ |
| $5$ | $(0,1)$ on $\{0,2,4,6,7,12,13,14,16,17\}$ | $(2,3)$ on $\{5,11\}$ |
| $6$ | $(0,1)$ on $\{0,2,4,6,7,12,13,14,16,17\}$ | $(2,3)$ on $\{3\}$ |
| $7$ | $(1,2)$ on $\{2,3,4,5,13,15,17,20\}$ | $(1,3)$ on $\{5,11\}$ |
| $8$ | $(0,2)$ on $\{0,3,5,8,9,12,14,15,16,20\}$ | $(0,3)$ on $\{3\}$ |
| $9$ | $(0,1)$ on $\{0,2,4,6,7,12,13,14,16,17\}$ | $(0,3)$ on $\{4\}$ |
| $10$ | $(1,2)$ on $\{2,3,4,5,13,15,17,20\}$ | $(2,3)$ on $\{2,10\}$ |
| $11$ | $(0,2)$ on $\{0,3,5,8,9,12,14,15,16,20\}$ | $(1,3)$ on $\{4\}$ |
| $12$ | $(0,2)$ on $\{0,3,5,8,9,12,14,15,16,20\}$ | $(1,3)$ on $\{2,10\}$ |
| $13$ | $(1,2)$ on $\{2,3,4,5,13,15,17,20\}$ | $(1,3)$ on $\{3\}$ |
| $14$ | $(1,2)$ on $\{2,3,4,5,13,15,17,20\}$ | $(2,3)$ on $\{4\}$ |
| $15$ | $(1,3)$ on $\{13,19\}$ | $(2,3)$ on $\{15,18\}$ |
| $16$ | $(0,3)$ on $\{0\}$ | $(1,3)$ on $\{0,2,4,10\}$ |
| $17$ | $(0,3)$ on $\{0\}$ | $(2,3)$ on $\{0,3,5,11\}$ |
| $18$ | $(1,3)$ on $\{13,19\}$ | $(2,3)$ on $\{5,11\}$ |
| $19$ | $(0,2)$ on $\{0,3,5,8,9,12,14,15,16,20\}$ | $(0,3)$ on $\{5,6,11,15,18\}$ |
| $20$ | $(2,3)$ on $\{5,11\}$ | $(0,3)$ on $\{0,5,16\}$ |
| $21$ | $(1,3)$ on $\{2,10\}$ | $(2,3)$ on $\{5,11\}$ |
| $22$ | $(1,3)$ on $\{2,10\}$ | $(2,3)$ on $\{15,18\}$ |
| $23$ | $(0,1)$ on $\{0,2,4,6,7,12,13,14,16,17\}$ | $(0,3)$ on $\{2,9,10,13,19\}$ |
| $24$ | $(1,3)$ on $\{2,10\}$ | $(0,3)$ on $\{0,2,12\}$ |
| $25$ | $(2,3)$ on $\{3\}$ | $(1,2)$ on $\{13,20\}$ |
| $26$ | $(1,3)$ on $\{4\}$ | $(1,2)$ on $\{15,17\}$ |

Orbits $8$ and $9$ contain the longest fills: seven slides from the new hole. Both still close, at sizes $94$, $530$ and $818$.

## The quoted branch

Orbit $23$ is the branch in `swarm/two-swap-branches.md`. Swap colours $0,1$ on $\{0,2,4,6,7,12,13,14,16,17\}$, then colours $0,3$ on $\{2,9,10,13,19\}$. The link of vertex $1$ is $(1,2,3,1,0,2,3,0,3)$, with sorted count $(5,5,5,5)$.

Swap colours $0,1$ on $\{0,4,6,7,14,16,17,19\}$. The colouring is

$$(0,-,3,2,1,2,0,1,2,3,0,3,1,3,0,2,0,1,3,1,2),$$

and the link is $(0,2,3,0,1,2,3,0,3)$. Colour $1$ appears once, at vertex $7$. The link of vertex $7$ is $(1,6,18,14,8)$ with colours $(1,0,3,0,2)$. All four colours are present.

Two further slides reach a three-colour link. The component has $530$ states, $140$ of them three-colour links.

| Hole | Link | Colours | Unique vertices |
| ---: | --- | --- | --- |
| $7$ | $(1,6,18,14,8)$ | $(1,0,3,0,2)$ | $1,\ 18,\ 8$ |
| $18$ | $(6,17,15,14,7)$ | $(0,1,2,0,3)$ | $17,\ 15,\ 7$ |
| $15$ | $(4,14,18,17,16)$ | $(1,0,2,1,0)$ | $18$ |

Vertex $15$ has degree $5$. Colour $3$ is missing. The partial colouring is

$$(0,1,3,2,1,2,0,3,2,3,0,3,1,3,0,-,0,1,2,1,2),$$

still of sorted count $(5,5,5,5)$. Assigning colour $3$ to vertex $15$ is a proper colouring of all twenty-one vertices, of sorted count $(5,5,5,6)$. That is one of the three full counts of this triangulation. The same sorted count $(5,5,5,5)$, while the hole is still at the frozen link of vertex $1$, has no singleton and no slide. Here the third swap has moved the hole onto links that do slide.

The other five images of this representative have component sizes $5$, $530$ and $818$, and each fills in one or two slides from its new hole.

## What was left alone

The $24$ pairs that return to the original colouring were left aside. The $64$ pairs that fill on the third swap itself were left aside. The plantri census was not reopened, and no second graph was built.

Feasibility that three Kempe swaps, followed by singleton slides, fill these $84$ branches: **High**.

## Next step

The return pairs sit on the original colouring up to renaming, so a third swap from one of them is one of the sixteen swaps in the one-swap table. The open question on this witness is that orbit. Away from this witness, the question is a minimum-degree-$5$ triangulation whose third-swap singletons have a slide component with every link still on four colours.

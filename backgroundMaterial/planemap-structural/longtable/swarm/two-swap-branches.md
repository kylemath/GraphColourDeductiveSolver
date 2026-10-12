# Two-swap branches

**KILL.** Two Kempe swaps are not always enough. On the $21$-vertex witness, $172$ of the $224$ ordered pairs leave a frozen link.

The published escape is real, and it is one of $52$ pairs that produce a unique colour. The other direction fails: $148$ pairs stay frozen on a colouring that is not a renaming of the original.

## The pairs that were scored

The triangulation and the colouring are those of `swarm/two-kempe-kill.md`. Twenty-one vertices, hole at vertex $1$, colouring

$$(0,-,1,2,1,2,0,1,2,0,3,3,0,1,0,2,0,1,3,3,2).$$

The link is $(0,5,11,6,7,8,9,10,2)$ with colours $(0,2,3,0,1,2,0,3,1)$. The multiplicity is $(3,2,2,2)$.

A Kempe swap exchanges the two colours on one bichromatic component of the triangulation with vertex $1$ deleted. A component that contains every vertex of its two colours is a global exchange and is omitted, as in the one-swap table of sixteen. The first swap is any of those sixteen. The second is any non-global component of the image, recomputed after the first swap.

Those images have $12$, $14$, or $16$ non-global components. The two components of colours $1$ and $2$ have $12$. The component of colours $1$ and $3$ on $\{7,11,17,18\}$, and the component of colours $2$ and $3$ on $\{8,10,19,20\}$, have $16$. The other twelve have $14$. That is

$$12\cdot 14+2\cdot 12+2\cdot 16=224$$

ordered pairs. Fourteen further components are global exchanges: ten images contribute one, and each image of the colour pair $(1,2)$ contributes two. Each of those fourteen links stays at multiplicity $(3,2,2,2)$.

The link of vertex $1$ is frozen when it uses all four colours and every colour appears at least twice. On this $9$-cycle the only such multiplicity is $(3,2,2,2)$. The alternative asked for is a unique colour, or at most three colours. The component walk is the walk in `mass_core`, applied to this one colouring. The hole has degree $9$, so the degree-five `RootState` enumerator is not used. The script is `swarm/two_swap_branches.py`.

## Census

| Outcome | Pairs | Link multiplicity |
| --- | ---: | --- |
| Frozen | $172$ | $(3,2,2,2)$ |
| Unique colour | $52$ | $(3,3,2,1)$ |
| At most three colours | $0$ | — |

Every link in the $224$ uses four colours. Every unique vertex has degree $5$. The frozen fraction is $172/224=43/56$. The escape fraction is $52/224=13/56$.

## The published escape is one of $52$

Swap colours $0$ and $3$ on $\{0\}$, then colours $0$ and $1$ on $\{2,4,6,7,12,13,14,16,17\}$. The link is $(3,2,3,1,0,2,0,3,0)$, multiplicity $(3,3,2,1)$, with colour $1$ only at vertex $6$. The slide $1\to 6$ fills, as already recorded.

Of the $52$ escapes, $28$ have a unique vertex whose link misses a colour, so that slide fills. The published pair is one of those $28$. The other $24$ unique vertices have links that use all four colours.

## Twenty-four pairs return to the original colouring

Sixteen pairs swap a component and then the same component. Eight pairs swap one component of a two-component colour pair and then the other. The colour pairs with exactly two components are $(0,1)$, $(0,2)$, $(0,3)$ and $(1,2)$. Those eight exchanges rename the original colouring. In all twenty-four cases the link is the original link up to swapping the names of two colours, and every Kempe swap from there is one of the original sixteen. A third swap stays at multiplicity $(3,2,2,2)$.

The four pairs in which both swaps change the sorted colour-count, and the link stays frozen, are the returns along colours $0$ and $3$: swapping $\{0\}$ twice, swapping its complementary component twice, or swapping those two components in either order. Each lands on the original sorted count $(4,5,5,6)$.

## A third swap is forced off the original colouring

The remaining $148$ frozen pairs land on $47$ orbits under global colour renaming. Each link is still $(3,2,2,2)$, so the vacancy neither fills nor slides. A third Kempe swap is required before either can happen.

Each of the $148$ has between $2$ and $6$ third swaps, out of $10$ to $16$ available, whose link has a unique colour or uses three colours. Every one of the $47$ orbits has at least one.

One such pair: swap colours $0$ and $1$ on $\{0,2,4,6,7,12,13,14,16,17\}$, then colours $0$ and $3$ on $\{2,9,10,13,19\}$. The colouring is

$$(1,-,3,2,0,2,1,0,2,3,0,3,1,3,1,2,1,0,3,0,2),$$

with sorted count $(5,5,5,5)$. The link is $(1,2,3,1,0,2,3,0,3)$. Colour $3$ appears three times and the other three colours twice each.

From there, swap colours $0$ and $1$ on $\{0,4,6,7,14,16,17,19\}$. The link becomes $(0,2,3,0,1,2,3,0,3)$. Colour $1$ appears once, at vertex $7$. The link of vertex $7$ is $(1,6,18,14,8)$ with colours $(1,0,3,0,2)$. All four colours are present, so the slide does not fill.

This is the typical third swap on these branches. On $84$ of the $148$ pairs, every third swap that creates a singleton has a four-colour link at that singleton. On the other $64$, at least one third swap fills the vacancy, either because the link of vertex $1$ uses three colours or because the unique vertex has a link that misses a colour. Four of those $64$ contain a three-colour link. One path is

- colours $0,1$ on $\{0,2,4,6,7,12,13,14,16,17\}$,
- colours $1,3$ on $\{6,11,14,16,18,19\}$,
- colours $2,3$ on $\{3,5,8,14,15,16\}$.

The third link is $(1,3,1,3,0,3,0,3,0)$. Colour $2$ is missing, and the sorted count is $(3,5,6,6)$, which is an extendable partial count of this graph. Colouring vertex $1$ with $2$ is a proper colouring of the triangulation.

## Population

A swap changes the population when the sorted colour-count on the twenty coloured vertices changes. Only the two swaps of colours $0$ and $3$ do so at the first step. They land on $(5,5,5,5)$.

| First swap | Second swap | Frozen | Escape |
| --- | --- | ---: | ---: |
| Changes | Changes | $4$ | $8$ |
| Changes | Preserved | $16$ | $0$ |
| Preserved | Changes | $28$ | $18$ |
| Preserved | Preserved | $124$ | $26$ |

From either $(5,5,5,5)$ image, the fourteen second swaps split as four escapes, two returns to the original orbit, and eight count-preserving swaps. All eight stay frozen. Every escape from those two images changes the sorted count again. The published pair is one of the eight.

## What was left alone

The plantri census was not reopened, and $F_{32}$ and $F_{42}$ were not coloured. The unchecked log for the two-pole graph of pole degree $12$ was not used. No second graph was built: this witness already has frozen two-swap branches.

Feasibility of “two Kempe swaps, then a slide or a fill” on every branch of every minimum-degree-$5$ triangulation: **Low**.

## Next step

On the $84$ pairs above, every third swap that creates a singleton still has a four-colour link at that vertex. The concrete question is the slide component of those third-swap images: whether the vacancy reaches a missing colour with no further Kempe swap. That computation stays on this colouring.

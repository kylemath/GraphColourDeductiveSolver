# Return pairs

**WALL.** $|C|=21$. The $24$ ordered pairs that restore the original colouring are $2$-cycles on a set $C$ of $21$ colourings. The first swap of such a pair has another second swap, and that landing has a unique link colour.

The triangulation and the colouring are those of `swarm/two-kempe-kill.md`. Twenty-one vertices, hole at vertex $1$, colouring

$$(0,-,1,2,1,2,0,1,2,0,3,3,0,1,0,2,0,1,3,3,2).$$

The link is $(0,5,11,6,7,8,9,10,2)$ with colours $(0,2,3,0,1,2,0,3,1)$. The sorted count is $(4,5,5,6)$. A Kempe swap is a non-global bichromatic component of the triangulation with vertex $1$ deleted, as in the sixteen swaps of that note. The script is `swarm/return_pairs.py`. It uses the component walk in `swarm/two_swap_branches.py`, which calls `mass_core`. No second graph is built.

## The twenty-four pairs close twenty-one colourings

Sixteen pairs swap a component and then the same component. The landing is the original colouring. Eight pairs swap one component of a two-component colour pair and then the other. The colour pairs with exactly two components are $(0,1)$, $(0,2)$, $(0,3)$ and $(1,2)$. Each of those eight lands on the original colouring with those two colours exchanged.

The four pairs along colours $0$ and $3$ are in this list. They swap $\{0\}$ twice, swap its complementary component $\{6,9,10,11,12,14,16,18,19\}$ twice, or swap those two components in either order.

These paths meet $21$ labelled colourings. Call that set $C$.

| Piece of $C$ | Colourings |
| --- | ---: |
| Original | $1$ |
| Image of one of the sixteen swaps | $16$ |
| Global exchange of one two-component colour pair | $4$ |
| Total | $21$ |

Every colouring in $C$ is frozen: the link uses all four colours and every colour appears at least twice. The only such multiplicity on this $9$-cycle is $(3,2,2,2)$. The four global exchanges are

$$
\begin{align*}
(0,1)&\colon& (1,-,0,2,0,2,1,0,2,1,3,3,1,0,1,2,1,0,3,3,2),\\
(0,2)&\colon& (2,-,1,0,1,0,2,1,0,2,3,3,2,1,2,0,2,1,3,3,0),\\
(0,3)&\colon& (3,-,1,2,1,2,3,1,2,3,0,0,3,1,3,2,3,1,0,0,2),\\
(1,2)&\colon& (0,-,2,1,2,1,0,2,1,0,3,3,0,2,0,1,0,2,3,3,1).
\end{align*}
$$

Each has link multiplicity $(3,2,2,2)$ and sorted count $(4,5,5,6)$. Up to renaming colours, the four exchanges are the original colouring, and the sixteen images form $12$ further classes, so $C$ is $13$ classes.

A third swap from a returned colouring is one of the original sixteen, transported by the colour exchange when the return renamed the colours. Each of those images is frozen. That is the one-swap kill, read at the original colouring.

## The same first swap leaves $C$

The intermediate after the first swap is one of the sixteen images. Two of them have sorted count $(5,5,5,5)$: the swap of colours $0$ and $3$ on $\{0\}$, and the swap on the complementary component. From the first of those, the colouring is

$$(3,-,1,2,1,2,0,1,2,0,3,3,0,1,0,2,0,1,3,3,2),$$

with link $(3,2,3,0,1,2,0,3,1)$. Fourteen non-global second swaps leave this colouring. Two restore a colouring in $C$. Four land on a unique link colour. Eight stay frozen, with sorted count still $(5,5,5,5)$.

| Second swap | Landing | Multiplicity | Sorted counts |
| --- | --- | --- | --- |
| $0,1$ on $\{2,4,6,7,12,13,14,16,17\}$ | unique | $(3,3,2,1)$ | $(4,5,5,6)$ |
| $0,1$ on $\{9\}$ | unique | $(3,3,2,1)$ | $(4,5,5,6)$ |
| $0,2$ on $\{3,5,8,9,12,14,15,16,20\}$ | unique | $(3,3,2,1)$ | $(4,5,5,6)$ |
| $0,2$ on $\{6\}$ | unique | $(3,3,2,1)$ | $(4,5,5,6)$ |
| $0,3$ on $\{0\}$ | return to the original | $(3,2,2,2)$ | $(4,5,5,6)$ |
| $0,3$ on $\{6,9,10,11,12,14,16,18,19\}$ | return, colours $0$ and $3$ exchanged | $(3,2,2,2)$ | $(4,5,5,6)$ |
| $1,2$ on $\{2,3,4,5,13,15,17,20\}$ | frozen | $(3,2,2,2)$ | $(5,5,5,5)$ |
| $1,2$ on $\{7,8\}$ | frozen | $(3,2,2,2)$ | $(5,5,5,5)$ |
| $1,3$ on $\{0,2,4,10\}$ | frozen | $(3,2,2,2)$ | $(5,5,5,5)$ |
| $1,3$ on $\{7,11,17,18\}$ | frozen | $(3,2,2,2)$ | $(5,5,5,5)$ |
| $1,3$ on $\{13,19\}$ | frozen | $(3,2,2,2)$ | $(5,5,5,5)$ |
| $2,3$ on $\{0,3,5,11\}$ | frozen | $(3,2,2,2)$ | $(5,5,5,5)$ |
| $2,3$ on $\{8,10,19,20\}$ | frozen | $(3,2,2,2)$ | $(5,5,5,5)$ |
| $2,3$ on $\{15,18\}$ | frozen | $(3,2,2,2)$ | $(5,5,5,5)$ |

The same split holds at the other $(5,5,5,5)$ image: two returns, four unique-colour seconds, eight frozen seconds. Each of the other fourteen images likewise has a non-returning second swap to multiplicity $(3,3,2,1)$. Across all sixteen images those unique seconds are the $52$ escapes already counted among the $224$ ordered pairs. Every continuation that starts with a return-pair first swap and refuses the returning second swap therefore meets a unique link colour by the second swap.

## One escape

Swap colours $0$ and $3$ on $\{0\}$. That is the first swap of the pair which swaps $\{0\}$ twice, and of the pair which then swaps the complementary component. From the intermediate, swap colours $0$ and $1$ on

$$\{2,4,6,7,12,13,14,16,17\}.$$

That component is one of the four unique-colour rows above. It is neither return. The colouring is

$$(3,-,0,2,0,2,1,0,2,0,3,3,1,0,1,2,1,0,3,3,2).$$

The link is $(3,2,3,1,0,2,0,3,0)$. Colour $1$ appears once, at vertex $6$. The sorted count is $(4,5,5,6)$. The slide $1\to 6$ fills, as already recorded: the link of vertex $6$ is $(1,11,17,18,7)$ with colours $(1,3,0,3,0)$, so colour $2$ is missing.

## A frozen second swap still opens on the third

The eight frozen rows are population-preserving. Each has a third swap to a unique link colour, so the frozen side of the same first swap is open at the next step as well.

One path, starting at the same swap of $\{0\}$:

- colours $1,2$ on $\{2,3,4,5,13,15,17,20\}$,
- colours $1,3$ on $\{7,15,18\}$.

The second colouring is

$$(3,-,2,1,2,1,0,1,2,0,3,3,0,2,0,1,0,2,3,3,1),$$

with link $(3,1,3,0,1,2,0,3,2)$ and sorted count $(5,5,5,5)$. The third colouring is

$$(3,-,2,1,2,1,0,3,2,0,3,3,0,2,0,3,0,2,1,3,1),$$

with link $(3,1,3,0,3,2,0,3,2)$. Colour $1$ appears once, at vertex $5$. The sorted count is $(4,5,5,6)$.

The same check on the other fifteen images gives the same shape. Whenever the non-returning second swap stays frozen, some third swap has a unique link colour. No intermediate of a return pair has every continuation frozen through three swaps.

## Feasibility and next step

Feasibility that the $24$ return pairs confine this colouring through three Kempe swaps: **Low**. The pairs close the $21$ colourings above, and the exhibited second swap leaves that set for a unique link colour.

The vacancy on that escape slides to a fill by the move already checked. The eight frozen seconds from the $(5,5,5,5)$ image are two-swap branches whose third swap unlocks the link of vertex $1$. The slide component of those unlocked colourings, and of the wider family in which every singleton still sees four colours, remains the open question on this witness.

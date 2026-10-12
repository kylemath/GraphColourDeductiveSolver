# Fan completions and the frozen hole

**LATER STATE.** The frozen colouring leaves the hole at vertex $1$, of degree $9$. A fan completion at a degree-$5$ vertex restricts to a colouring of $T-v$, so the blank vertex has degree $5$. The link is then a $5$-cycle. Four colours, each appearing at least twice, occupy at least eight vertices, so a degree-$5$ link cannot be frozen at all. The induction's starting colourings are that other set. The degree-$9$ frozen hole is a later state.

The triangulation and the colouring are those of `two-kempe-kill.md`. The rotation was read with `mass_core.parse_ascii`, which checks the spherical-triangulation identities. The fans are the five triangulations of a $5$-cycle from `hole-induction.md`: if the link is labelled $0,1,2,3,4$ in order, the fan at index $i$ is the pair of chords
$$
\tau_i=\bigl\{\,i\,(i+2),\; i\,(i+3)\,\bigr\}.
$$
A colouring of the link is proper on $\tau_i$ when it is proper on the cycle and the apex differs in colour from both of its chord neighbours. A fan is legal when neither chord is already an edge of $T$.

## Degrees

The graph has $21$ vertices, $63$ edges and $42$ faces, and minimum degree $5$. The degrees are $9$ at vertex $1$, $8$ at vertex $14$, $6$ at vertices $3$ and $4$, and $5$ at the other seventeen vertices
$$
0,2,5,6,7,8,9,10,11,12,13,15,16,17,18,19,20.
$$
Every one of those seventeen links is an induced $5$-cycle: the distance-$2$ pairs are non-edges. All five fans are therefore legal at every degree-$5$ vertex.

The frozen colouring, in vertex order, is
$$
(0,-,1,2,1,2,0,1,2,0,3,3,0,1,0,2,0,1,3,3,2).
$$
Every edge with both ends coloured joins different colours. The hole is vertex $1$. Its link is $(0,5,11,6,7,8,9,10,2)$ with colours $(0,2,3,0,1,2,0,3,1)$, and the multiplicities are $(3,2,2,2)$. All four colours appear, and none appears once.

## The frozen colours on each degree-$5$ link

Vertex $1$ lies on the link precisely when the degree-$5$ vertex is a neighbour of $1$. Those nine neighbours are $0,2,5,6,7,8,9,10,11$. On each of them one link colour is blank. The other eight degree-$5$ vertices have all five link colours determined.

The question asked of each link is only about those five positions: whether some colour for each blank makes the five colours proper on the cycle and proper on at least one fan. Properness against the rest of the star of vertex $1$ is not part of this reading.

Where the five colours are already determined, the cycle is proper, because those link edges belong to $T$ and the frozen colouring is proper on them. Exactly one fan is proper, and the multiplicities are $(2,2,1)$: three colours, one of them unique.

| $v$ | Link | Colours | Fan apex | Chords |
| --- | --- | --- | ---: | --- |
| $12$ | $(2,10,20,13,3)$ | $(1,3,2,1,2)$ | $10$ | $10\,13$, $10\,3$ |
| $13$ | $(3,12,20,19,14)$ | $(2,0,2,3,0)$ | $19$ | $19\,3$, $19\,12$ |
| $15$ | $(4,14,18,17,16)$ | $(1,0,3,1,0)$ | $18$ | $18\,16$, $18\,4$ |
| $16$ | $(4,15,17,11,5)$ | $(1,2,1,3,2)$ | $11$ | $11\,4$, $11\,15$ |
| $17$ | $(6,11,16,15,18)$ | $(0,3,0,2,3)$ | $15$ | $15\,6$, $15\,11$ |
| $18$ | $(6,17,15,14,7)$ | $(0,1,2,0,1)$ | $15$ | $15\,7$, $15\,6$ |
| $19$ | $(8,14,13,20,9)$ | $(2,0,1,2,0)$ | $13$ | $13\,9$, $13\,8$ |
| $20$ | $(9,19,13,12,10)$ | $(0,3,1,0,3)$ | $13$ | $13\,10$, $13\,9$ |

Where vertex $1$ is the blank, two of the four choices make the cycle proper and at least one fan proper. A success uses either three colours, with multiplicities $(2,2,1)$, or all four, with multiplicities $(2,1,1,1)$.

| $v$ | Link | Frozen colours | Colour at $1$ | Result | Fans |
| --- | --- | --- | ---: | --- | --- |
| $0$ | $(1,2,3,4,5)$ | $(-,1,2,1,2)$ | $0$ | $(2,2,1)$ | $1$ |
| $0$ | $(1,2,3,4,5)$ | $(-,1,2,1,2)$ | $3$ | $(2,2,1)$ | $1$ |
| $2$ | $(0,1,10,12,3)$ | $(0,-,3,0,2)$ | $1$ | $(2,1,1,1)$ | $1,10,3$ |
| $2$ | $(0,1,10,12,3)$ | $(0,-,3,0,2)$ | $2$ | $(2,2,1)$ | $10$ |
| $5$ | $(0,4,16,11,1)$ | $(0,1,0,3,-)$ | $1$ | $(2,2,1)$ | $11$ |
| $5$ | $(0,4,16,11,1)$ | $(0,1,0,3,-)$ | $2$ | $(2,1,1,1)$ | $4,11,1$ |
| $6$ | $(1,11,17,18,7)$ | $(-,3,1,3,1)$ | $0$ | $(2,2,1)$ | $1$ |
| $6$ | $(1,11,17,18,7)$ | $(-,3,1,3,1)$ | $2$ | $(2,2,1)$ | $1$ |
| $7$ | $(1,6,18,14,8)$ | $(-,0,3,0,2)$ | $1$ | $(2,1,1,1)$ | $1,18,8$ |
| $7$ | $(1,6,18,14,8)$ | $(-,0,3,0,2)$ | $3$ | $(2,2,1)$ | $8$ |
| $8$ | $(1,7,14,19,9)$ | $(-,1,0,3,0)$ | $2$ | $(2,1,1,1)$ | $1,7,19$ |
| $8$ | $(1,7,14,19,9)$ | $(-,1,0,3,0)$ | $3$ | $(2,2,1)$ | $7$ |
| $9$ | $(1,8,19,20,10)$ | $(-,2,3,2,3)$ | $0$ | $(2,2,1)$ | $1$ |
| $9$ | $(1,8,19,20,10)$ | $(-,2,3,2,3)$ | $1$ | $(2,2,1)$ | $1$ |
| $10$ | $(1,9,20,12,2)$ | $(-,0,2,0,1)$ | $2$ | $(2,2,1)$ | $2$ |
| $10$ | $(1,9,20,12,2)$ | $(-,0,2,0,1)$ | $3$ | $(2,1,1,1)$ | $1,20,2$ |
| $11$ | $(1,5,16,17,6)$ | $(-,2,0,1,0)$ | $1$ | $(2,2,1)$ | $5$ |
| $11$ | $(1,5,16,17,6)$ | $(-,2,0,1,0)$ | $3$ | $(2,1,1,1)$ | $1,5,17$ |

So the link-level test succeeds at all seventeen degree-$5$ vertices. It does not produce a frozen $5$-tuple. The successes with four colours have three colours that appear once.

## A degree-$5$ link cannot be frozen

A frozen link means all four colours appear, and none is unique. On five vertices the only multiplicity that uses four colours is $(2,1,1,1)$. The pattern in which every colour appears at least twice has size at least $2+2+2+2=8$. There is no such colouring of a $5$-cycle, proper or otherwise, and the chords of a fan do not add vertices. A degree-$5$ link cannot be frozen at all.

The same count applies to the blank completions above: filling vertex $1$ still leaves five positions.

## Every legal fan at one degree-$5$ vertex

Forget the frozen colouring. Take $v=0$, whose link is $(1,2,3,4,5)$. Each of the five fans adds two missing chords. For each fan, every proper colouring of $(T-0)$ plus those two chords, with colours in $\{0,1,2,3\}$, was enumerated. The link types are only $(2,2,1)$ and $(2,1,1,1)$. The frozen type does not occur. The same absence is the counting lemma, so it holds for the other sixteen degree-$5$ vertices without a second enumeration.

| Fan apex | Chords | Colourings | Type $(2,2,1)$ | Type $(2,1,1,1)$ | Frozen |
| ---: | --- | ---: | ---: | ---: | ---: |
| $1$ | $1\,3$, $1\,4$ | $3072$ | $768$ | $2304$ | $0$ |
| $2$ | $2\,4$, $2\,5$ | $1920$ | $384$ | $1536$ | $0$ |
| $3$ | $3\,5$, $3\,1$ | $2304$ | $384$ | $1920$ | $0$ |
| $4$ | $4\,1$, $4\,2$ | $2304$ | $384$ | $1920$ | $0$ |
| $5$ | $5\,2$, $5\,3$ | $1920$ | $384$ | $1536$ | $0$ |

The labelled count is $24$ times the count modulo colour renaming, at each fan. One colouring of type $(2,2,1)$ for the fan at vertex $1$ has link colours $(0,1,2,1,2)$. One of type $(2,1,1,1)$ has link colours $(0,1,2,1,3)$.

A colouring of type $(2,2,1)$ uses three colours on the link, so the degree-$5$ hole has a missing colour. A colouring of type $(2,1,1,1)$ uses four colours and has three unique colours, so a singleton slide is available. Neither type is frozen.

## Where this colouring sits

The degree-$5$ step of the induction colours $(T-v)$ plus one legal fan and restricts. The restriction is a proper colouring of $T-v$ whose blank vertex has degree $5$, and whose link is proper on that fan. By the count, that link is not frozen.

The colouring in `two-kempe-kill.md` blanks vertex $1$ and colours every degree-$5$ vertex. Its frozen link is the $9$-cycle at vertex $1$, with multiplicities $(3,2,2,2)$. That partial colouring is not the restriction of a fan completion. In the induction, a hole whose degree is greater than $5$ is a later state of the slide sequence that began at the degree-$5$ vertex used to build the fan. The starting colourings are the fan restrictions, a different set.

The seventeen successful link readings do not put this colouring into that starting set. Each reading is a $5$-tuple, proper for some fan, still of multiplicity $(2,2,1)$ or $(2,1,1,1)$. The blank of the published colouring remains vertex $1$.

## Feasibility

Feasibility of the counting obstruction, that no degree-$5$ link is frozen: **High**. It is the comparison $8>5$.

Feasibility that the published colouring is a starting colouring of the degree-$5$ step: ruled out by that count, together with the degree of the hole.

Feasibility that a hole of degree $9$ with a frozen link is a later state of the induction's one sequence, rather than one of its starts: **High**. The start blanks a degree-$5$ vertex.

This note does not build a slide path from a fan restriction to this particular colouring.

## Next steps

1. Take the fan restrictions at the seventeen degree-$5$ vertices as the starting set. Their links have a repeated colour or a missing colour, so each start slides or fills.
2. Decide whether the published colouring of $T-1$, with link multiplicities $(3,2,2,2)$, occurs on a slide-and-swap sequence from one of those starts.

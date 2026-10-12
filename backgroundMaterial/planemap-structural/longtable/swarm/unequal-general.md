# Unequal poles on every two-pole belt

**WALL.** On $G_{11}-u_0$, every proper 4-colouring with $c(a)\neq c(b)$ reaches a boundary of at most three colours by singleton vacancy slides alone. The same statement is already known for $n=5$ and $n=8$. No slide path is proved for every $n\ge 5$, and no counterexample was found. The search stopped at $n=11$.

Slides move the hole to a neighbour whose colour appears once on the current boundary. The target is a current boundary on at most three colours. Colourings are orbits under global colour permutation, in first-occurrence form. The slide rule is the one in `swarm/unequal_poles.py`. The cap was 20,000 states per start. Every unequal start finished inside that cap: at most 65 states, and the longest walk has length 6.

Summing orbit sizes $4!/(4-k)!$ gives 19,368 labelled unequal colourings of $G_{11}-u_0$, and 24 labelled equal colourings in the one remaining orbit.

## Counts

| $n$ | Orbits | Equal poles | Unequal starts | Slides only | Unfilled | Longest walk | Max states |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 11 | 808 | 1 | 807 | 807 | 0 | 6 | 65 |

Of the 807 unequal orbits, the link of $u_0$ already uses at most three colours in 462 orbits. The other 345 start with four colours on that link. Their walk lengths are 205 of length 1, 60 of length 2, 44 of length 3, 12 of length 4, 12 of length 5, and 12 of length 6.

The published census in `unequal-poles.md` is the check on the slide code: the same run returns its 19 and 121 slides-only orbits, with longest walks 2 and 4.

## A length-6 unequal start that slides

$n=11$, poles unequal, link of $u_0$ equal to $(a,u_1,v_0,v_{10},u_{10})$ with colours $(0,1,2,3,2)$.

| Vertex | $a$ | $b$ | $u_1$ | $u_2$ | $u_3$ | $u_4$ | $u_5$ | $u_6$ | $u_7$ | $u_8$ | $u_9$ | $u_{10}$ | $v_0$ | $v_1$ | $v_2$ | $v_3$ | $v_4$ | $v_5$ | $v_6$ | $v_7$ | $v_8$ | $v_9$ | $v_{10}$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Colour | 0 | 1 | 1 | 2 | 1 | 2 | 3 | 1 | 2 | 1 | 3 | 2 | 2 | 3 | 0 | 3 | 0 | 2 | 0 | 3 | 2 | 0 | 3 |

Colour 3 is unique on the link, at $v_{10}$. The walk is

$$u_0 \to v_{10} \to v_9 \to u_9 \to u_8 \to v_7 \to v_6.$$

The link of $v_6$ is then $(b,v_5,u_6,u_7,v_7)$ with colours $(1,2,1,2,0)$. Fill $v_6$ with colour 3. The colouring of $G_{11}$ is proper. The poles are still coloured 0 and 1.

Twelve unequal orbits have a walk of this length. This is one of them.

## What the antiprism does give

Write $c(a)=0$ and $c(b)=1$. Every coloured $u_i$ lies in $\{1,2,3\}$ and every $v_i$ lies in $\{0,2,3\}$. The following three facts hold for every $n\ge 5$.

The $v$-ring meets colour 0. If it did not, every consecutive pair of $v$-vertices would be $\{2,3\}$, every coloured $u_i$ would be forced to colour 1, and the path $u_1-\cdots-u_{n-1}$ would be monochromatic.

A run of colours in $\{2,3\}$ has length at most 2, except for the unique run that contains the edge $v_{n-1}v_0$. That run has at most two vertices on each side of the edge. Indeed, two consecutive tight edges $v_{i-1}v_i$ and $v_iv_{i+1}$, with both $u_i$ and $u_{i+1}$ coloured, force both of those $u$-vertices to colour 1, and they are adjacent. The only belt edge with no coloured $u$ above it is the edge under the hole.

Off that hole edge, the coloured belt is a concatenation of tiles of two kinds, with $\{\rho,\tau\}=\{2,3\}$. Call a length-1 gap $0,\rho,0$ an $A_\rho$ tile: its two $u$-vertices are $\{1,\tau\}$ in either order. Call a length-2 gap $0,\rho,\tau,0$ a $B_\rho$ tile: its three $u$-vertices are $\tau,1,\rho$.

These facts name the colouring. They do not yet name a slide. On a bad tight edge the doubled colour is one of $\{\rho,\tau\}$, and one opening slide followed by a slide onto the neighbouring 0 puts the hole on that 0 with link shape $(b,\,v_{\mathrm{left}},\,u,\,\rho,\,0)$. The next tile is one of the six oriented tiles. An $A_\rho$ tile whose outer $u$-vertex is colour 1 is already a 3-colour link. An $A_\rho$ tile whose outer $u$-vertex is $\tau$, and a $B_\tau$ tile, each return a state of the same shape one tile further along the belt. The $A_\tau$ cases, and the step where the walk meets the cap rewritten by the opening slides, were not carried through. That is where the hand argument stops.

## Feasibility

Feasibility of a slides-only escape for every $n\ge 5$: **Medium**, speculative. The belts $n=5,8,11$ give no counterexample, the longest walks are 2, 4, and 6, and the tile word is rigid enough that a finished case split would be a proof. The case split is incomplete.

Next step: close the six-tile step from the prepared zero, including the cap where the walk meets the opening slides. Leave $n=14$ unenumerated.

# Unequal poles on the two-pole belt

**WALL.** On $G_5-u_0$ and $G_8-u_0$, every proper 4-colouring with $c(a)\neq c(b)$ reaches a boundary of at most three colours by singleton vacancy slides alone. The hybrid never needs its Kempe swap. The worst Kempe-component size used is $0$.

The census is the deletion at $h=u_0$ for $n=5$ and $n=8$ only. No claim is made for general $n$.

Slides move the hole to a neighbour whose colour appears once on the current boundary. The hole may have any degree. A Kempe move, when used, swaps one whole bichromatic component of the current deletion graph. The target is a current boundary on at most three colours. The search cap was 20,000 states per start. Every unequal start finished inside that cap: at most 9 states for $n=5$ and 31 states for $n=8$.

Colourings are orbits under global colour permutation, in first-occurrence form. The script is `swarm/unequal_poles.py`. The same enumeration, summed over orbit sizes $4!/(4-k)!$, reproduces the labelled counts 480 ($n=5$) and 2928 ($n=8$).

## Counts

| $n$ | Orbits | Equal poles | Unequal starts | Slides only | Need one Kempe | Unfilled | Worst Kempe size |
| ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| 5 | 20 | 1 | 19 | 19 | 0 | 0 | 0 |
| 8 | 122 | 1 | 121 | 121 | 0 | 0 | 0 |

Of the slides-only starts, the link of $u_0$ already uses at most three colours in 10 orbits ($n=5$) and 48 orbits ($n=8$). The other 9 and 73 start with four colours on that link and reach a target by a positive slide walk. The longest such walks have length 2 ($n=5$) and 4 ($n=8$).

## A four-colour unequal start that slides

$n=8$, poles unequal, link of $u_0$ equal to $(a,u_1,v_0,v_7,u_7)$ with colours $(0,1,2,3,2)$.

| Vertex | $a$ | $b$ | $u_1$ | $u_2$ | $u_3$ | $u_4$ | $u_5$ | $u_6$ | $u_7$ | $v_0$ | $v_1$ | $v_2$ | $v_3$ | $v_4$ | $v_5$ | $v_6$ | $v_7$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Colour | 0 | 1 | 1 | 2 | 1 | 2 | 1 | 3 | 2 | 2 | 3 | 0 | 3 | 0 | 2 | 0 | 3 |

Colour 3 is unique on the link, at $v_7$. The walk stays on degree-5 belt vertices:

$$u_0 \to v_7 \to v_6 \to u_6 \to u_5.$$

The link of $u_5$ is then $(u_4,a,u_6,v_5,v_4)$ with colours $(2,0,1,2,0)$. Fill $u_5$ with colour 3. The colouring of $G_8$ is proper. The poles are still coloured 0 and 1, so this fill does not pass through the equal-pole case.

## Equal-pole check

Each of $n=5$ and $n=8$ has a single equal-pole orbit. Both satisfy the population count in the note: $(3,3,3,2)$ for $n=5$ ($k=1$) and $(5,5,5,2)$ for $n=8$ ($k=2$). In both, the link of $u_0$ uses four colours, and the $(A,B)$-component of $b$ is exactly $\{b\}\cup\{v_i:c(v_i)=B\}$.

For $n=8$ the colouring is periodic of period three off colour 0:

| Vertex | $a$ | $b$ | $u_1$ | $u_2$ | $u_3$ | $u_4$ | $u_5$ | $u_6$ | $u_7$ | $v_0$ | $v_1$ | $v_2$ | $v_3$ | $v_4$ | $v_5$ | $v_6$ | $v_7$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Colour | 0 | 0 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 |

The link colours are $(0,1,2,3,1)$. Colour 3 is unique, at $v_7$. The star is $\{b,v_1,v_4,v_7\}$, size $k+2=4$. Swapping colours 0 and 3 on that component sends $v_7$ from 3 to 0 and leaves the other four boundary colours fixed, so the link uses $\{0,1,2\}$. Filling $u_0$ with 3 produces populations $(5,5,4,4)$. The same orbit also has the symmetric star $\{b,v_0,v_3,v_6\}$ of size 4 on colours 0 and 2. The enumerator's Kempe routine lists both, and both land on a target.

Slides from this colouring reach 32 states, and every one of those boundaries still uses four colours. The search therefore classifies the orbit as needing one Kempe swap. Its smallest filling component has size 3; one such component is the $a$-star $\{a,u_2,u_5\}$. The note's star of size 4 fills as well.

For $n=5$ the same star check gives component $\{b,v_1,v_4\}$, size 3. Swapping it and filling the hole is proper. Slides also reach a target on that orbit, by $u_0\to a\to u_3$, so the search reports a slides-only fill there. The star itself is still a filling Kempe move of the enumerator.

## Feasibility

Feasibility of a slides-only escape for every $n\ge 5$: **Medium-Low**, speculative. The two computed belts give no counterexample, and the positive walks are short, but the census does not name a progress measure that would cover every belt.

Next step: run the same census for $n=11$, the next order with $n\equiv 2\pmod{3}$, before trying to promote the slide walk to a general argument.

# Isolated local patches: the bridge does not force an exit

4 October 2026. Local colourings only. The 32-vertex pentakis dodecahedron and the 42-vertex frequency-2 icosahedron were not coloured. The patches below are induced subgraphs of the triangulations built in `inquiry_slide.py`.

**Verdict: KILL on both graphs.** The local geometry does not force a useful second vacancy slide. Two exhibits are given. The first lives on the star that contains every bridge link. The second adds the outer neighbours of the pentagons that are actually landed on, and still kills the stricter reading in which every legal forward slide must be inspected.

## The slide being tested

Let $c$ be a degree-five vertex and let $\gamma$ be a proper $4$-colouring of the patch with $c$ deleted. The link of $c$ is a $5$-cycle. The colourings considered here use all four colours on that cycle, in the only proper pattern: $2,1,1,1$, with the repeated colour at cycle distance $2$. The three vertices of unique colour are the legal first slides. Each is a degree-six bridge.

Colour $c$ with the colour of the chosen bridge $b$ and delete $b$. A neighbour $y$ of $b$ is a legal second slide when its colour appears once on the link of $b$. The origin $c$ is always such a neighbour in the colourings below; that slide is the reverse, and it returns to the same root. A useful second slide would be a forward slide onto a far degree-five vertex whose boundary is not again the locked pattern.

A forward slide is illegal when every far degree-five neighbour of $b$ fails to be uniquely coloured. It is a locked landing when the slide is legal and the link of the far vertex, after $b$ is recoloured with the far vertex's colour, is a proper $5$-cycle of type $2,1,1,1$ with the repeat at cycle distance $2$. Colours are $\{0,1,2,3\}$.

## The common $15$-vertex star

Both stars, with the centre deleted, are the same abstract graph. It has five vertices of degree $5$ (the bridges), five of degree $4$, and five of degree $3$.

Frequency-2 names, indices modulo $5$:

- bridges $m_i$, the degree-$6$ neighbours of the centre, in link order;
- $p_i$, the far degree-five vertex across $m_i$;
- $q_i$, the midpoint of the icosahedral edge $p_i p_{i+1}$.

Edges: $m_i m_{i+1}$, $m_i p_i$, $m_i q_i$, $m_i q_{i-1}$, $p_i q_i$, $p_i q_{i-1}$. The link of $m_i$ is
$$c,\; m_{i-1},\; q_{i-1},\; p_i,\; q_i,\; m_{i+1}.$$
The two vertices $q_{i-1}$ and $q_i$ are adjacent to $p_i$, so they cannot carry the colour of $p_i$. After the first slide, $c$ carries the colour of $m_i$, which also differs from the colour of $p_i$. The second slide $m_i \to p_i$ is therefore legal if and only if the colour of $p_i$ differs from both $\gamma(m_{i-1})$ and $\gamma(m_{i+1})$.

Pentakis names, on the same edges under $m \leftrightarrow f$, $p \leftrightarrow g$, $q \leftrightarrow e$:

- bridges $f_i$ in link order around the origin;
- $e_i$, the degree-five vertex shared by $f_i$ and $f_{i+1}$;
- $g_i$, the outer face-centre private to $f_i$.

The link of $f_i$ is
$$c,\; f_{i-1},\; e_{i-1},\; g_i,\; e_i,\; f_{i+1}.$$
Each bridge meets two far pentagons. They witness each other when they have the same colour. A far vertex can also be witnessed by the bridge opposite it on the link: $e_i$ is not adjacent to $f_{i-1}$, and $e_{i-1}$ is not adjacent to $f_{i+1}$.

The degree-five labels sit on different orbits of this graph. On the frequency-2 star the far pentagons are the degree-$3$ tips $p_i$. On the pentakis star they are the degree-$4$ vertices $e_i$. That is why the two colouring counts below agree and the slide counts do not.

Vertex ids from the construction in `inquiry_slide.py`, centre $0$ on the frequency-2 icosahedron and centre $20$ on the pentakis dodecahedron. Column $i$ is index $i$.

| | $0$ | $1$ | $2$ | $3$ | $4$ |
|---|---|---|---|---|---|
| $m_i$ | $19$ | $14$ | $12$ | $15$ | $17$ |
| $f_i$ | $3$ | $4$ | $0$ | $1$ | $2$ |
| $p_i$ | $5$ | $10$ | $8$ | $4$ | $2$ |
| $e_i$ | $25$ | $30$ | $28$ | $24$ | $22$ |
| $q_i$ | $21$ | $13$ | $16$ | $18$ | $20$ |
| $g_i$ | $11$ | $19$ | $5$ | $17$ | $12$ |

Exhaustive backtrack of the proper $4$-colourings of this $15$-vertex graph, colours labelled rather than taken up to renaming:

| Star | proper colourings | boundary $2,1,1,1$ | every far slide illegal | of which some degree-$6$ forward slide exists |
|---|---|---|---|---|
| frequency-2 | $31680$ | $13200$ | $6360$ | all $6360$ |
| pentakis | $31680$ | $13200$ | $2880$ | all $2880$ |

No colouring of either $15$-vertex patch makes every forward neighbour of every singleton non-unique. The reverse slide to the centre is legal for every singleton in every one of the $13200$ boundary colourings. The vacancy is not frozen inside the star. What fails is the forced return to a new pentagon.

## Exhibit A: every far pentagon is illegal

Same boundary on both stars: $(m_i)$ or $(f_i)$ receives $(0,1,0,2,3)$. The repeated colour is $0$, on vertices $0$ and $2$, at cycle distance $2$. The singletons are indices $1$, $3$ and $4$.

### Frequency-2

$$
\begin{align*}
\gamma(m) &= (0,1,0,2,3),\\
\gamma(p) &= (1,0,1,0,0),\\
\gamma(q) &= (2,2,3,1,2).
\end{align*}
$$

Every edge of the star joins different colours. The three checks use only the criterion above:

- Singleton $m_1$, colour $1$. The far vertex $p_1$ has colour $0$, and both neighbouring bridges $m_0$ and $m_2$ have colour $0$. The link colours are $c:1$, $m_0:0$, $q_0:2$, $p_1:0$, $q_1:2$, $m_2:0$. Colour $0$ appears three times. The only unique colour is the centre.
- Singleton $m_3$, colour $2$. The far vertex $p_3$ has colour $0$, matching $m_2$. Link colours: $c:2$, $m_2:0$, $q_2:3$, $p_3:0$, $q_3:1$, $m_4:3$. Colour $0$ appears twice.
- Singleton $m_4$, colour $3$. The far vertex $p_4$ has colour $0$, matching $m_0$. Link colours: $c:3$, $m_3:2$, $q_3:1$, $p_4:0$, $q_4:2$, $m_0:0$. Colour $0$ appears twice.

No second slide from a singleton lands on a far pentagon. The same colouring does have a legal slide from $m_3$ and from $m_4$ onto the degree-$6$ vertex $q_3$ (colour $1$, unique on both links). That is not a degree-five landing. The link of $q_3$ meets exactly two degree-five vertices, $p_3$ and $p_4$, both colour $0$, so neither is a legal continuation either. The two outside neighbours of $q_3$ are degree six and cannot split that pair.

### Pentakis

$$
\begin{align*}
\gamma(f) &= (0,1,0,2,3),\\
\gamma(e) &= (2,2,3,0,2),\\
\gamma(g) &= (1,0,1,1,1).
\end{align*}
$$

Edges were checked against the list in the previous section. Both far pentagons of each singleton fail uniqueness:

- Singleton $f_1$, colour $1$. Link colours: $c:1$, $f_0:0$, $e_0:2$, $g_1:0$, $e_1:2$, $f_2:0$. The two far vertices $e_0$ and $e_1$ are both colour $2$. Neither is unique, and no degree-$6$ colour is unique.
- Singleton $f_3$, colour $2$. Link colours: $c:2$, $f_2:0$, $e_2:3$, $g_3:1$, $e_3:0$, $f_4:3$. The far vertex $e_2$ matches $f_4$. The far vertex $e_3$ matches $f_2$.
- Singleton $f_4$, colour $3$. Link colours: $c:3$, $f_3:2$, $e_3:0$, $g_4:1$, $e_4:2$, $f_0:0$. The far vertex $e_3$ matches $f_0$. The far vertex $e_4$ matches $f_3$.

Both far pentagons of the three-pentagon bridge are blocked on every singleton. This is the kill of "a bridge that meets three pentagons is automatically an exit." As on the frequency-2 star, the block is not a freeze: $g_3$ is a legal degree-$6$ slide from $f_3$, and $g_4$ is a legal degree-$6$ slide from $f_4$. Each of those vertices has one degree-five neighbour outside the star, so the $15$-vertex patch does not decide a third step. It does decide the second step back onto a pentagon, and that step is illegal.

## Exhibit B: the only forward slides land locked

The $15$-vertex patch cannot see the link of a far pentagon. Each frequency-2 far pentagon has two neighbours outside the star, the midpoints of the two icosahedral edges that leave the star. Each pentakis far pentagon has one such neighbour. Exhibit B colours those vertices for the pentagons that are actually reached, and only those.

Among the $13200$ boundary colourings, $960$ frequency-2 colourings and $1560$ pentakis colourings have no legal degree-$6$ forward slide. Every one of the $960$ extends, by a proper colouring of the relevant outer midpoints, so that every legal far landing is locked. On the pentakis star, $480$ of the $1560$ extend in the same way and $1080$ do not. Existence is the claim.

### Frequency-2

$$
\begin{align*}
\gamma(m) &= (0,1,0,2,3),\\
\gamma(p) &= (1,0,1,1,1),\\
\gamma(q) &= (2,2,3,0,2).
\end{align*}
$$

- Singleton $m_1$: far colour $\gamma(p_1)=0$ matches $m_0$ and $m_2$. Link colours $c:1$, $m_0:0$, $q_0:2$, $p_1:0$, $q_1:2$, $m_2:0$. Only the centre is unique.
- Singleton $m_3$: the far vertex $p_3$ has colour $1$, and the link colours are $c:2$, $m_2:0$, $q_2:3$, $p_3:1$, $q_3:0$, $m_4:3$. Colour $1$ appears once. The slide is legal. No degree-$6$ colour is unique.
- Singleton $m_4$: the far vertex $p_4$ has colour $1$. Link colours $c:3$, $m_3:2$, $q_3:0$, $p_4:1$, $q_4:2$, $m_0:0$. Colour $1$ appears once. No degree-$6$ colour is unique.

The link of $p_3$ (vertex $4$) is $(35, q_3, m_3, q_2, 40) = (35, 18, 15, 16, 40)$. Colour the outer midpoints $\gamma(35)=2$ and $\gamma(40)=0$. After $m_3$ is recoloured with $\gamma(p_3)=1$, the boundary is
$$(2,0,1,3,0).$$
Colour $0$ appears at cycle distance $2$. The five consecutive pairs, including the closing edge $0$—$2$, are proper, and all four colours occur.

The link of $p_4$ (vertex $2$) is $(31, q_4, m_4, q_3, 33) = (31, 20, 17, 18, 33)$. Colour $\gamma(31)=0$ and $\gamma(33)=3$. After $m_4$ is recoloured with $1$, the boundary is
$$(0,2,1,0,3).$$
Again $2,1,1,1$ with the repeat at distance $2$.

The four outer colours are proper against every coloured neighbour: $35$ meets $18:0$, $4:1$, $40:0$, $33:3$; $40$ meets $35:2$, $4:1$, $16:3$; $31$ meets $20:2$, $2:1$, $33:3$; $33$ meets $31:0$, $2:1$, $18:0$, $35:2$. Each of these midpoints also meets vertices outside the coloured set. None of those vertices lies on the link of $p_3$ or of $p_4$, so none enters the boundary just computed.

### Pentakis

$$
\begin{align*}
\gamma(f) &= (0,1,0,2,3),\\
\gamma(e) &= (3,3,1,0,1),\\
\gamma(g) &= (2,0,2,3,2).
\end{align*}
$$

- Singleton $f_1$. Link colours: $c:1$, $f_0:0$, $e_0:3$, $g_1:0$, $e_1:3$, $f_2:0$. Both far pentagons have colour $3$. The only unique colour is the centre.
- Singleton $f_3$. Link colours: $c:2$, $f_2:0$, $e_2:1$, $g_3:3$, $e_3:0$, $f_4:3$. The far vertex $e_3$ matches $f_2$. The far vertex $e_2$ has colour $1$ once. The degree-$6$ colour $3$ appears twice.
- Singleton $f_4$. Link colours: $c:3$, $f_3:2$, $e_3:0$, $g_4:2$, $e_4:1$, $f_0:0$. The far vertex $e_3$ matches $f_0$. The far vertex $e_4$ has colour $1$ once. The degree-$6$ colour $2$ appears twice.

The link of $e_2$ (vertex $28$) is $(g_3, f_3, f_2, g_2, 9) = (17, 1, 0, 5, 9)$. Set $\gamma(9)=0$. After $f_3$ is recoloured with $\gamma(e_2)=1$, the boundary is
$$(3,1,0,2,0),$$
locked. The link of $e_4$ (vertex $22$) is $(g_0, f_0, f_4, g_4, 10) = (11, 3, 2, 12, 10)$. Set $\gamma(10)=3$. After $f_4$ is recoloured with $\gamma(e_4)=1$, the boundary is
$$(2,0,1,2,3),$$
locked. Both new vertices differ in colour from their coloured neighbours ($9$ meets $17:3$, $28:1$, $5:2$; $10$ meets $11:2$, $22:1$, $12:2$). Each also meets three vertices outside the coloured set; none of those lies on the link of $e_2$ or of $e_4$.

## What was tried against these colourings

The obvious strengthening is a colouring in which the bridge is frozen: no forward slide of either degree. The $15$-vertex enumeration forbids it. In all $13200$ boundary colourings the reverse slide is live, and every colouring that kills the far pentagons still has a degree-$6$ forward slide from at least one singleton. That invariant is special to this patch and to pattern $2,1,1,1$; it is not an invariant that restores a forced pentagon exit. Exhibit B kills the strengthening that was still available: demand that whatever forward slide does exist must land on a locked pentagon. Those colourings exist, $960$ on the frequency-2 star and $480$ on the pentakis star, once the outer neighbours of the landed pentagons are coloured.

A landing of type $2,1,1,1$ still has three singleton colours, so the vacancy can leave the far pentagon along a degree-$6$ edge. That is the same local shape it started with. It is not a boundary that uses only three colours, and it is not a slide that stayed on a degree-five vertex.

## Conclusion

KILL. On the frequency-2 star, a proper $4$-colouring of the bridge star makes every far pentagon an illegal second slide. On the pentakis star, a proper $4$-colouring blocks both far pentagons of every singleton bridge. A second pair of colourings, enlarged only by the outer neighbours of the pentagons that are reached, has no degree-$6$ forward slide, and every legal forward slide lands on a far pentagon whose boundary is again $2,1,1,1$ with the repeat at cycle distance $2$.

Feasibility that this local geometry forces a useful second slide: **Low**. The obstructions are explicit colourings, and on the frequency-2 star every candidate with no degree-$6$ outlet extends to a locked landing.

Feasibility that a global colouring of either full triangulation still forces an escape: not tested. Speculative. No colouring of the $32$-vertex graph or the $42$-vertex graph was attempted.

Next step: leave these two graphs uncoloured. The local bridge is not an automatic exit, so a rank on the pair $(\text{root}, \text{colouring})$ has to be supplied by something other than the distance table between the twelve degree-five vertices.

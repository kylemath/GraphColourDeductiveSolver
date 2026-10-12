# The cap the opening slides rewrite

**PROVED.** For each legal doubled colour in $\{\rho,\tau\}$, the two opening slides leave the colouring below on the vertices next to $v_{n-1}v_0$. A prepared-zero walk that meets that colouring reaches a link of at most three colours in at most two further singleton slides, on the $v$-ring or on the $u$-ring. The vacancy fills there. The poles remain $0$ and $1$.

The $A_\tau$ tile in the middle of the belt is not proved here. The argument starts at the moment a prepared zero reaches the last tile before the cap.

## Setup

Write $c(a)=0$ and $c(b)=1$, and write $\{\rho,\tau\}=\{2,3\}$. The hole starts at $u_0$. Slides keep these labels: the old hole receives the colour of the vertex it moves to, and that vertex becomes the hole. A slide is legal when that colour appears once on the current link. A belt vertex has five neighbours, so a link that uses at most three colours is a fill. The missing colour is written on the hole.

The link of $u_i$ is $(a,u_{i+1},v_i,v_{i-1},u_{i-1})$. The link of $v_i$ is $(b,v_{i-1},u_i,u_{i+1},v_{i+1})$.

The facts used from the belt, for every $n\ge 5$, are the ones already recorded: every coloured $u_i$ lies in $\{1,2,3\}$, every $v_i$ lies in $\{0,2,3\}$, a $\{2,3\}$-run off the hole edge has length at most $2$, and the run through $v_{n-1}v_0$ has at most two vertices on each side of that edge. Off that edge the belt is a concatenation of $A$ and $B$ tiles.

A bad tight edge is a four-colour link of $u_0$ on which $v_{n-1}v_0$ is coloured by $\{\rho,\tau\}$ and the doubled colour lies in $\{\rho,\tau\}$. The link is $(a,u_1,v_0,v_{n-1},u_{n-1})$. The vertex $u_1$ is adjacent to $v_0$, and $u_{n-1}$ is adjacent to $v_{n-1}$, so each $u$-colour is the pole colour $1$ or the opposite $v$-colour. The two proper four-colour patterns are

$$
(0,1,\rho,\tau,\rho)
\qquad\text{and}\qquad
(0,\tau,\rho,\tau,1).
$$

In the first, $\rho$ is doubled, on $v_0$ and $u_{n-1}$, and the unique colour $\tau$ sits on $v_{n-1}$. In the second, $\tau$ is doubled, on $u_1$ and $v_{n-1}$, and the unique colour $\rho$ sits on $v_0$. Exchanging the names $\rho$ and $\tau$ reproduces the same two patterns.

## Doubled colour $\rho$

The opening link has colours $(0,1,\rho,\tau,\rho)$.

The vertex $v_{n-2}$ lies in $\{0,\rho,\tau\}$, is adjacent to $v_{n-1}=\tau$, and is adjacent to $u_{n-1}=\rho$. Hence $v_{n-2}=0$.

The first slide is $u_0\to v_{n-1}$. It writes $\tau$ on $u_0$. The link of $v_{n-1}$ is then

$$
(b,v_{n-2},u_{n-1},u_0,v_0)
$$

with colours $(1,0,\rho,\tau,\rho)$. The second slide is $v_{n-1}\to v_{n-2}$. It writes $0$ on $v_{n-1}$. The hole stands on $v_{n-2}$, and the link is $(b,v_{n-3},u_{n-2},u_{n-1},v_{n-1})$ with colours $(1,\,c(v_{n-3}),\,c(u_{n-2}),\,\rho,\,0)$. That is the prepared-zero shape: the side already crossed carries $\rho$ and then $0$.

The vertices that stay fixed while the walk travels away from $v_{n-2}$ are

| Vertex | $a$ | $b$ | $u_0$ | $u_1$ | $u_{n-1}$ | $v_0$ | $v_{n-1}$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Colour | $0$ | $1$ | $\tau$ | $1$ | $\rho$ | $\rho$ | $0$ |

The walk meets the cap from the other side of $v_0$. There $v_1\neq\rho$. The run bound leaves two proper extensions.

**Short run.** $v_1=0$. The rewritten triple $v_{n-1},v_0,v_1$ is $0,\rho,0$, an $A_\rho$ tile. Its $u$-vertices are $u_0=\tau$ and $u_1=1$.

**Long run.** $v_1=\tau$. Then $v_2=0$, since $v_0,v_1,v_2$ cannot all lie in $\{\rho,\tau\}$. The vertex $u_1$ is adjacent to $v_0=\rho$ and $v_1=\tau$, so $u_1=1$, as the opening already has. The vertex $u_2$ is adjacent to $v_1=\tau$, to $v_2=0$, and to $u_1=1$, so $u_2=\rho$. The rewritten quadruple $v_{n-1},v_0,v_1,v_2$ is $0,\rho,\tau,0$, a $B_\rho$ tile, with $u$-vertices $\tau,1,\rho$.

## Doubled colour $\tau$

The opening link has colours $(0,\tau,\rho,\tau,1)$.

The vertex $v_1$ lies in $\{0,\rho,\tau\}$, is adjacent to $v_0=\rho$, and is adjacent to $u_1=\tau$. Hence $v_1=0$.

The first slide is $u_0\to v_0$. It writes $\rho$ on $u_0$. The link of $v_0$ is

$$
(b,v_{n-1},u_0,u_1,v_1)
$$

with colours $(1,\tau,\rho,\tau,0)$. The second slide is $v_0\to v_1$. It writes $0$ on $v_0$. The hole stands on $v_1$. In link order the side already crossed is the low-index side, so the colours are $(1,0,\tau,\,c(u_2),\,c(v_2))$. The prepared-zero shape for this direction is that pattern: $0$ and then the doubled colour $\tau$ on the crossed side.

The vertices that stay fixed while the walk travels away from $v_1$ are

| Vertex | $a$ | $b$ | $u_0$ | $u_1$ | $u_{n-1}$ | $v_0$ | $v_{n-1}$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Colour | $0$ | $1$ | $\rho$ | $\tau$ | $1$ | $0$ | $\tau$ |

The walk meets the cap from the low-index side of $v_{n-1}$. There $v_{n-2}\neq\tau$. The two proper extensions are the reflections of the two above.

**Short run.** $v_{n-2}=0$. The triple $v_{n-2},v_{n-1},v_0$ is $0,\tau,0$, an $A_\tau$ tile, with $u$-vertices $u_{n-1}=1$ and $u_0=\rho$.

**Long run.** $v_{n-2}=\rho$ and $v_{n-3}=0$. The same adjacency that forced $u_2$ above forces $u_{n-2}=\tau$. The quadruple $v_{n-3},v_{n-2},v_{n-1},v_0$ is $0,\rho,\tau,0$, a $B_\rho$ tile, with $u$-vertices $\tau,1,\rho$.

## Prepared zero at the cap

A prepared zero is a hole on a $v$-vertex whose crossed side carries the doubled colour and a $0$, as the opening just produced. Tiles that return this shape are assumed to have done so up to the last tile before the cap. What follows uses only the cap colouring on the forward side.

In the decreasing shape the forward $u$-vertex is adjacent to the forward $v$-vertex and to the crossed $u$-vertex of colour $\rho$. Its colour is therefore $1$ when the forward $v$-vertex has colour $\tau$, and it lies in $\{1,\tau\}$ when the forward $v$-vertex has colour $\rho$. In the increasing shape the forward $u$-vertex is adjacent to the crossed $u$-vertex of colour $\tau$, so its colour lies in $\{1,\rho\}$.

Each slide below lands on a belt vertex. On the links that still use four colours, the singleton that is taken is a belt vertex. The final link uses at most three colours, and the missing colour fills the hole.

### Doubled $\rho$, short run: the $v$-ring

The prepared hole is at $v_1$, the outer zero of the rewritten $A_\rho$ tile. The outer $u$-vertex is $u_1=1$. The crossed side is $u_2=\rho$, $v_2=0$. The link colours are

$$
(1,\rho,1,\rho,0).
$$

The colours are $\{0,1,\rho\}$. Fill $v_1$ with $\tau$. The five neighbours are $b,v_0,u_1,u_2,v_2$, none of which has colour $\tau$. The only singleton on the link is the backward $0$ at $v_2$. The poles are still $0$ and $1$.

### Doubled $\rho$, long run: the $u$-ring

A prepared zero cannot sit on $v_2$. Its crossed side would colour $u_3$ by $\rho$, and the cap has already coloured $u_2$ by $\rho$.

The zeros $v_2$ and $v_{n-2}$ are distinct and non-adjacent, since both have colour $0$ in the original colouring. The last ordinary tile abuts $v_2$. A length-$2$ gap repeats a colour: a $B_\tau$ tile has low $u$-vertex $\rho$, adjacent to $u_2$, and a $B_\rho$ tile has high $u$-vertex $\rho$, adjacent to the prepared colour $\rho$ on the crossed side. A length-$1$ gap of colour $\tau$ has forward $v$-vertex $\tau$, so the prepared shape forces its outer $u$-vertex to be $1$ and its low $u$-vertex to be $\rho$, adjacent to $u_2$.

The remaining tile is the length-$1$ gap $v_4=0$, $v_3=\rho$, $v_2=0$. Its $u$-vertices are $\{1,\tau\}$.

If the outer $u$-vertex $u_4$ is $1$, the prepared link at $v_4$ has colours $(1,\rho,1,\rho,0)$. Fill $v_4$ with $\tau$. The low $u$-vertex is then $\tau$, which is legal next to the cap colour $u_2=\rho$.

If the outer $u$-vertex $u_4$ is $\tau$, the low $u$-vertex is $u_3=1$. The prepared link at $v_4$ has colours

$$
(1,\rho,\tau,\rho,0).
$$

Colour $\tau$ appears once, at $u_4$. Slide $v_4\to u_4$. The link of $u_4$ has colours $(0,\rho,\tau,\rho,1)$. Colour $1$ appears once, at $u_3$. Slide $u_4\to u_3$. The link of $u_3$ is $(a,u_4,v_3,v_2,u_2)$, and the cap supplies $u_2=\rho$ and $v_2=0$, so the colours are

$$
(0,1,\rho,0,\rho).
$$

The colours are $\{0,1,\rho\}$. Fill $u_3$ with $\tau$. The neighbours are $a,u_4,v_3,v_2,u_2$. The only singleton is the backward colour $1$ at $u_4$. The poles are still $0$ and $1$.

### Doubled $\tau$, short run: the $v$-ring

The prepared hole is at $v_{n-2}$. The crossed side is $v_{n-3}=0$, $u_{n-2}=\tau$. The forward vertices are the cap: $u_{n-1}=1$ and $v_{n-1}=\tau$. The link colours are

$$
(1,0,\tau,1,\tau).
$$

The colours are $\{0,1,\tau\}$. Fill $v_{n-2}$ with $\rho$. The neighbours are $b,v_{n-3},u_{n-2},u_{n-1},v_{n-1}$. The only singleton is the backward $0$. The poles are still $0$ and $1$.

### Doubled $\tau$, long run: the $u$-ring

A prepared zero cannot sit on $v_{n-3}$: the crossed colour $\tau$ would fall on $u_{n-3}$, next to the cap colour $u_{n-2}=\tau$.

The zeros $v_1$ and $v_{n-3}$ are distinct and non-adjacent, since both have colour $0$ in the original colouring. A length-$2$ gap abutting $v_{n-3}$ repeats a colour. The tile $B_\tau$ has high $u$-vertex $\tau$, adjacent to $u_{n-2}$. The tile $B_\rho$ has low $u$-vertex $\tau$, adjacent to the prepared colour $\tau$ on the crossed side. A length-$1$ gap of colour $\rho$ has forward $u$-vertex adjacent to that same prepared $\tau$, so the forward $u$-vertex is $1$ and the high $u$-vertex is $\tau$, adjacent to $u_{n-2}$.

The remaining tile is $v_{n-5}=0$, $v_{n-4}=\tau$, $v_{n-3}=0$, with $u$-vertices $\{1,\rho\}$.

If the outer $u$-vertex $u_{n-4}$ is $1$, the prepared link at $v_{n-5}$ has colours $(1,0,\tau,1,\tau)$. Fill $v_{n-5}$ with $\rho$.

If the outer $u$-vertex $u_{n-4}$ is $\rho$, then $u_{n-3}=1$. The prepared link at $v_{n-5}$ has colours

$$
(1,0,\tau,\rho,\tau).
$$

Colour $\rho$ appears once, at $u_{n-4}$. Slide $v_{n-5}\to u_{n-4}$. The link of $u_{n-4}$ has colours $(0,1,\tau,\rho,\tau)$. Colour $1$ appears once, at $u_{n-3}$. Slide $u_{n-4}\to u_{n-3}$. The link of $u_{n-3}$ is $(a,u_{n-2},v_{n-3},v_{n-4},u_{n-4})$, and the cap supplies $u_{n-2}=\tau$, so the colours are

$$
(0,\tau,0,\tau,1).
$$

The colours are $\{0,1,\tau\}$. Fill $u_{n-3}$ with $\rho$. The only singleton is the backward colour $1$. The poles are still $0$ and $1$.

## Feasibility

Feasibility of this cap step: **High**. Each doubled colour has two extensions of the exceptional run, and each extension ends on one of the four links above.

Next step: the $A_\tau$ tile in the middle of the belt, the other half of the prepared-zero walk. The cap uses that tile only as the supplier of a prepared zero at the last ordinary tile.

# The $B$ tiles

**Verdict: PROVED.** From a prepared zero, a length-2 gap ahead of the hole has two orientations. The gap $0,\rho,\tau,0$ forces its high $u$-vertex to colour $\rho$, and that colour repeats on the edge $u_i u_{i+1}$, so the orientation is not a colouring. The gap $0,\tau,\rho,0$ is proper. Four singleton slides return a prepared zero one tile further along the belt. The hole sits on the far zero of the tile, and the poles remain $0$ and $1$.

The walk meets only the vertices of this $B_\tau$ tile. No cap vertex is required to finish it.

## Prepared zero

Fix $n\ge 6$, colours $c(a)=0$ and $c(b)=1$, and $\{\rho,\tau\}=\{2,3\}$. The hole is at a belt vertex $v_i$. The link of $v_i$, in the belt rotation, is

$$
(b,\ v_{i-1},\ u_i,\ u_{i+1},\ v_{i+1}).
$$

The prepared shape says these five vertices are coloured

$$
(1,\ c(v_{i-1}),\ c(u_i),\ \rho,\ 0).
$$

In particular $c(u_{i+1})=\rho$ and $c(v_{i+1})=0$. A singleton slide moves the hole onto a neighbour whose colour appears once on the current link, and writes that colour onto the vertex just left.

The rotation is the successor cycle of the five triangles at $v_k$:

$$
(b,v_k,v_{k-1}),\ 
(v_k,u_k,v_{k-1}),\ 
(u_{k+1},u_k,v_k),\ 
(v_{k+1},u_{k+1},v_k),\ 
(b,v_{k+1},v_k).
$$

The same reading at $u_k$ gives

$$
(a,\ u_{k+1},\ v_k,\ v_{k-1},\ u_{k-1}).
$$

Every coloured $u$-vertex lies in $\{1,\rho,\tau\}$ and every coloured $v$-vertex lies in $\{0,\rho,\tau\}$. For $n\ge 6$ the five vertices $v_{i-3}$, $v_{i-2}$, $v_{i-1}$, $v_i$, and $v_{i+1}$ are distinct, and $v_{i+1}$ is not adjacent to $v_{i-3}$. The same bound keeps $u_{i+1}$ off the vertex $u_{i-2}$. For $n=5$ the far zero $v_{i-3}$ is adjacent to the prepared zero $v_{i+1}$, so a length-2 gap cannot stand in front of the prepared zero.

## The two orientations

A $B$ tile whose right-hand zero is the prepared hole is a length-2 gap on $v_{i-3},v_{i-2},v_{i-1}$, with $c(v_{i-3})=0$ and $\{c(v_{i-2}),c(v_{i-1})\}=\{\rho,\tau\}$. The two words $0,\rho,\rho,0$ and $0,\tau,\tau,0$ repeat a colour on the edge $v_{i-2}v_{i-1}$ and are not tiles. The three $u$-vertices of the gap are $u_{i-2}$, $u_{i-1}$, and $u_i$, the low, middle, and high vertices in index order. The low vertex meets $v_{i-3}$ and $v_{i-2}$, the middle vertex meets $v_{i-2}$ and $v_{i-1}$, and the high vertex meets $v_{i-1}$. The hole occupies $v_i$, so the edge $u_i v_i$ contributes no colour. Consecutive $u$-vertices are adjacent.

### The gap $0,\rho,\tau,0$

Here $c(v_{i-2})=\rho$ and $c(v_{i-1})=\tau$. The middle vertex $u_{i-1}$ meets both colours $\rho$ and $\tau$, so $c(u_{i-1})=1$. The high vertex $u_i$ meets $v_{i-1}=\tau$ and $u_{i-1}=1$, so $c(u_i)=\rho$. The low vertex $u_{i-2}$ meets $v_{i-2}=\rho$ and $u_{i-1}=1$, so $c(u_{i-2})=\tau$. These are the three colours $\tau,1,\rho$ of a $B_\rho$ tile.

The edge $u_i u_{i+1}$ then has colour $\rho$ at both ends. The colouring is improper, so this orientation is not a prepared state and it contributes no slide.

### The gap $0,\tau,\rho,0$

Here $c(v_{i-2})=\tau$ and $c(v_{i-1})=\rho$. The middle vertex meets both colours $\tau$ and $\rho$, so $c(u_{i-1})=1$. The high vertex meets $v_{i-1}=\rho$ and $u_{i-1}=1$, so $c(u_i)=\tau$. The low vertex meets $v_{i-2}=\tau$ and $u_{i-1}=1$, so $c(u_{i-2})=\rho$. These are the three colours $\rho,1,\tau$ of a $B_\tau$ tile. It is proper on the tile. The high vertex $u_i=\tau$ meets $u_{i+1}$, $u_{i-1}$, and $v_{i-1}$ in colours $\rho$, $1$, and $\rho$. The middle vertex $u_{i-1}=1$ meets $v_{i-1}$ and $v_{i-2}$ in colours $\rho$ and $\tau$. The low vertex $u_{i-2}=\rho$ meets $v_{i-2}$ and $v_{i-3}$ in colours $\tau$ and $0$, and it is not adjacent to the prepared vertex $u_{i+1}=\rho$. The prepared link is

$$
(1,\ \rho,\ \tau,\ \rho,\ 0).
$$

Colour $\rho$ occurs twice, on $v_{i-1}$ and on $u_{i+1}$. The singleton colours are $1$ at $b$, $\tau$ at $u_i$, and $0$ at $v_{i+1}$. The legal slides are to those three vertices. Slides to $v_{i-1}$ and to $u_{i+1}$ are illegal.

**Slides that leave the tile.** The slide $v_i\to v_{i+1}$ writes $0$ on $v_i$. The link of $v_{i+1}$ is $(b,v_i,u_{i+1},u_{i+2},v_{i+2})$, with colours

$$
(1,\ 0,\ \rho,\ c(u_{i+2}),\ c(v_{i+2})).
$$

The slide $v_i\to b$ writes $1$ on $v_i$. The link of $b$ is the whole $v$-ring. That ring still carries $v_{i-3}=0$, $v_{i-2}=\tau$, $v_{i-1}=\rho$, and the new colour $1$ on $v_i$, together with the prepared $0$ on $v_{i+1}$, so the boundary of $b$ uses all four colours. Both slides leave the $B_\tau$ tile. The slide that enters the tile is the remaining one.

**First tile slide.** The slide $v_i\to u_i$ is legal, because $\tau$ occurs once. It writes $\tau$ on $v_i$. That colour meets the coloured neighbours $b$, $v_{i-1}$, $u_{i+1}$, and $v_{i+1}$ in colours $1$, $\rho$, $\rho$, and $0$, so the colouring stays proper. The poles are unchanged. The link of $u_i$ is $(a,u_{i+1},v_i,v_{i-1},u_{i-1})$, with colours

$$
(0,\ \rho,\ \tau,\ \rho,\ 1).
$$

Colour $\rho$ occurs twice, on $u_{i+1}$ and on $v_{i-1}$. The singleton colours are $0$ at $a$, $\tau$ at $v_i$, and $1$ at $u_{i-1}$. The legal slides are to those three vertices.

- The slide $u_i\to v_i$ is the inverse of the slide just taken, and it restores the link $(1,\rho,\tau,\rho,0)$.
- The slide $u_i\to a$ writes $0$ on $u_i$ and moves the hole to the pole $a$.
- The slide $u_i\to u_{i-1}$ writes $1$ on $u_i$.

**Second tile slide.** The slide onto $u_{i-1}$ is legal, because $1$ occurs once on $(0,\rho,\tau,\rho,1)$. The new colour $1$ on $u_i$ meets $a$, $u_{i+1}$, $v_i$, and $v_{i-1}$ in colours $0$, $\rho$, $\tau$, and $\rho$, so the colouring stays proper. The link of $u_{i-1}$ is $(a,u_i,v_{i-1},v_{i-2},u_{i-2})$, with colours

$$
(0,\ 1,\ \rho,\ \tau,\ \rho).
$$

Colour $\rho$ occurs twice, on $v_{i-1}$ and on $u_{i-2}$. The singleton colours are $0$ at $a$, $1$ at $u_i$, and $\tau$ at $v_{i-2}$. The legal slides are to those three vertices.

- The slide $u_{i-1}\to u_i$ is the inverse of the slide just taken.
- The slide $u_{i-1}\to a$ writes $0$ on $u_{i-1}$ and moves the hole to the pole $a$.
- The slide $u_{i-1}\to v_{i-2}$ writes $\tau$ on $u_{i-1}$.

**Third tile slide.** The slide onto $v_{i-2}$ is legal, because $\tau$ occurs once on $(0,1,\rho,\tau,\rho)$. The new colour $\tau$ on $u_{i-1}$ meets $a$, $u_i$, $v_{i-1}$, and $u_{i-2}$ in colours $0$, $1$, $\rho$, and $\rho$, so the colouring stays proper. The vertex $u_{i-1}$ is not adjacent to $v_i$, which now has colour $\tau$. The link of $v_{i-2}$ is $(b,v_{i-3},u_{i-2},u_{i-1},v_{i-1})$, with colours

$$
(1,\ 0,\ \rho,\ \tau,\ \rho).
$$

Colour $\rho$ occurs twice, on $u_{i-2}$ and on $v_{i-1}$. The singleton colours are $1$ at $b$, $0$ at $v_{i-3}$, and $\tau$ at $u_{i-1}$. The legal slides are to those three vertices.

- The slide $v_{i-2}\to u_{i-1}$ is the inverse of the slide just taken.
- The slide $v_{i-2}\to b$ writes $1$ on $v_{i-2}$ and moves the hole to the pole $b$.
- The slide $v_{i-2}\to v_{i-3}$ writes $0$ on $v_{i-2}$.

**Return.** The slide onto $v_{i-3}$ is legal, because $0$ occurs once on $(1,0,\rho,\tau,\rho)$. The new colour $0$ on $v_{i-2}$ meets $b$, $u_{i-2}$, $u_{i-1}$, and $v_{i-1}$ in colours $1$, $\rho$, $\tau$, and $\rho$, so the colouring stays proper. The slides were

$$
v_i\to u_i\to u_{i-1}\to v_{i-2}\to v_{i-3},
$$

none of which is a pole, so $c(a)=0$ and $c(b)=1$. The hole is at $v_{i-3}$, the far zero of the tile. The low vertex $u_{i-2}$ still has colour $\rho$, and $v_{i-2}$ now has colour $0$. The link of $v_{i-3}$ is $(b,v_{i-4},u_{i-3},u_{i-2},v_{i-2})$, with colours

$$
(1,\ c(v_{i-4}),\ c(u_{i-3}),\ \rho,\ 0).
$$

This is the prepared shape, with the same trailing colour $\rho$, one $B_\tau$ tile further along the belt.

The vertex $v_{i-4}$ is adjacent to $v_{i-3}=0$, so its colour lies in $\{\rho,\tau\}$. The vertex $u_{i-3}$ is adjacent to $u_{i-2}=\rho$, so its colour lies in $\{1,\tau\}$. The two are adjacent to each other, so they are not both $\tau$. The three proper pairs are as follows.

- If $c(v_{i-4})=\rho$ and $c(u_{i-3})=1$, the link is $(1,\rho,1,\rho,0)$. The colours are $\{0,1,\rho\}$. Fill $v_{i-3}$ with $\tau$. The five neighbours $b$, $v_{i-4}$, $u_{i-3}$, $u_{i-2}$, and $v_{i-2}$ have colours $1$, $\rho$, $1$, $\rho$, and $0$.
- If $c(v_{i-4})=\rho$ and $c(u_{i-3})=\tau$, the link is $(1,\rho,\tau,\rho,0)$. It uses four colours and is a prepared zero of the same shape.
- If $c(v_{i-4})=\tau$ and $c(u_{i-3})=1$, the link is $(1,\tau,1,\rho,0)$. It uses four colours and is a prepared zero of the same shape.

In every subcase the tile step is closed.

## Feasibility

Feasibility of the $B$ tile step: **High**. The orientation $0,\rho,\tau,0$ is excluded by the edge $u_i u_{i+1}$, and the orientation $0,\tau,\rho,0$ has a legal walk of length $4$ onto the far zero.

Next step: the $A_\rho$ tile whose outer $u$-vertex has colour $\tau$. The antiprism note names that orientation as a return and does not give the slides. Leave $n=14$ unenumerated.

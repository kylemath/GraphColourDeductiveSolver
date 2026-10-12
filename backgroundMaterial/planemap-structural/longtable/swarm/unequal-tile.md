# The $A_\tau$ tile

**Verdict: PROVED.** From a prepared zero, the only proper orientation of an $A_\tau$ tile returns, by two singleton slides, to a prepared zero one tile further along the belt. The hole sits on the far zero of the tile, and the poles remain $0$ and $1$. The other orientation repeats $\rho$ on the edge $u_i u_{i+1}$ and is not a colouring.

The walk meets only the vertices of this $A_\tau$ tile. No $B$ tile is required to finish it.

## Prepared zero

Fix $n\ge 5$, colours $c(a)=0$ and $c(b)=1$, and $\{\rho,\tau\}=\{2,3\}$. The hole is at a belt vertex $v_i$. The link of $v_i$, in the belt rotation, is

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

For $n\ge 5$ the four vertices $v_{i-2}$, $v_{i-1}$, $v_i$, and $v_{i+1}$ are distinct, and $v_{i+1}$ is not adjacent to $v_{i-2}$.

## The tile and its two orientations

An $A_\tau$ tile whose right-hand zero is the prepared hole is the gap

$$
c(v_{i-2})=0,\qquad c(v_{i-1})=\tau,
$$

with $\{c(u_{i-1}),c(u_i)\}=\{1,\rho\}$. These are the two $u$-vertices of the gap $0,\tau,0$. They are adjacent, so each colour in $\{1,\rho\}$ occurs once. The outer $u$-vertex is $u_i$, the $u$-vertex on the prepared link. The inner $u$-vertex is $u_{i-1}$.

The same reading of an $A_\rho$ tile gives the link colours $(1,\rho,c(u_i),\rho,0)$, already a $3$-colour link when the outer vertex has colour $1$. That case is the one recorded in the antiprism note. Here the gap colour is $\tau$, so the prepared link is

$$
(1,\ \tau,\ c(u_i),\ \rho,\ 0).
$$

### Outer colour $\rho$

Suppose $c(u_i)=\rho$. Then $c(u_{i-1})=1$, and the link colours are $(1,\tau,\rho,\rho,0)$. The edge $u_i u_{i+1}$ has colour $\rho$ at both ends. The colouring is improper, so this orientation is not a prepared state and it contributes no slide.

### Outer colour $1$

The remaining orientation is $c(u_i)=1$ and $c(u_{i-1})=\rho$. It is proper on the tile: $u_i$ meets $u_{i+1}$, $u_{i-1}$, and $v_{i-1}$ in colours $\rho$, $\rho$, and $\tau$, and $u_{i-1}$ meets $v_{i-1}$ and $v_{i-2}$ in colours $\tau$ and $0$. The prepared link is

$$
(1,\ \tau,\ 1,\ \rho,\ 0).
$$

Colour $1$ occurs twice, on $b$ and on $u_i$. The singleton colours are $\tau$ at $v_{i-1}$, $\rho$ at $u_{i+1}$, and $0$ at $v_{i+1}$. The legal slides are to those three vertices. Slides to $b$ and to $u_i$ are illegal.

**Back along the preparing side.** The slide $v_i\to v_{i+1}$ writes $0$ on $v_i$. The link of $v_{i+1}$ is $(b,v_i,u_{i+1},u_{i+2},v_{i+2})$, with colours

$$
(1,\ 0,\ \rho,\ c(u_{i+2}),\ c(v_{i+2})).
$$

The slide $v_i\to u_{i+1}$ writes $\rho$ on $v_i$. The link of $u_{i+1}$ is $(a,u_{i+2},v_{i+1},v_i,u_i)$, with colours

$$
(0,\ c(u_{i+2}),\ 0,\ \rho,\ 1).
$$

Both slides leave the $A_\tau$ tile, toward the side already used to place the hole on $v_i$. The slide that enters the tile is the remaining one.

**First tile slide.** The slide $v_i\to v_{i-1}$ is legal, because $\tau$ occurs once. It writes $\tau$ on $v_i$. That colour meets the coloured neighbours $b$, $v_{i+1}$, $u_i$, and $u_{i+1}$ in colours $1$, $0$, $1$, and $\rho$, so the colouring stays proper. The poles are unchanged. The link of $v_{i-1}$ is $(b,v_{i-2},u_{i-1},u_i,v_i)$, with colours

$$
(1,\ 0,\ \rho,\ 1,\ \tau).
$$

This uses all four colours. Colour $1$ occurs twice, on $b$ and on $u_i$. The singleton colours are $0$ at $v_{i-2}$, $\rho$ at $u_{i-1}$, and $\tau$ at $v_i$. The legal slides are to those three vertices.

- The slide $v_{i-1}\to v_i$ is the inverse of the slide just taken, and it restores the link $(1,\tau,1,\rho,0)$.
- The slide $v_{i-1}\to u_{i-1}$ writes $\rho$ on $v_{i-1}$. The link of $u_{i-1}$ is $(a,u_i,v_{i-1},v_{i-2},u_{i-2})$, with colours $(0,1,\rho,0,c(u_{i-2}))$.
- The slide $v_{i-1}\to v_{i-2}$ writes $0$ on $v_{i-1}$.

**Return.** The slide onto $v_{i-2}$ is legal, because $0$ occurs once on $(1,0,\rho,1,\tau)$. The new colour $0$ on $v_{i-1}$ meets $b$, $v_i$, $u_{i-1}$, and $u_i$ in colours $1$, $\tau$, $\rho$, and $1$, so the colouring stays proper. The slides were $v_i\to v_{i-1}\to v_{i-2}$, neither of which is a pole, so $c(a)=0$ and $c(b)=1$. The hole is at $v_{i-2}$, the far zero of the tile. The vertex $u_{i-1}$ still has colour $\rho$. The link of $v_{i-2}$ is $(b,v_{i-3},u_{i-2},u_{i-1},v_{i-1})$, with colours

$$
(1,\ c(v_{i-3}),\ c(u_{i-2}),\ \rho,\ 0).
$$

This is the prepared shape, with the same trailing colour $\rho$, one $A_\tau$ tile further along the belt.

If $c(v_{i-3})$ and $c(u_{i-2})$ both lie in $\{0,1,\rho\}$, the boundary uses at most the three colours $\{0,1,\rho\}$. If either equals $\tau$, the boundary uses four colours and is a prepared zero of the same shape. In both subcases the tile step is closed.

## Feasibility

Feasibility of the $A_\tau$ tile step: **High**. The outer colour $\rho$ is excluded by the edge $u_i u_{i+1}$, and the outer colour $1$ has a legal walk of length $2$ onto the far zero.

Next step: the prepared zero in which the next vertices are the cap rewritten by the opening slides. Leave $n=14$ unenumerated.

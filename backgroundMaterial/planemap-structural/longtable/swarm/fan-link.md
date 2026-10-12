# Fan-proper links of a 5-cycle

**GAP.** The coloured link is $(0,1,0,2,3)$, in cyclic order. It is proper on the fans $\tau_1$, $\tau_3$ and $\tau_4$. On the gyroelongated hexagonal dipyramid below, with one degree-5 vertex deleted, both bichromatic paths that could free a colour meet the link, so neither pair is forced to separate. No single Kempe swap reduces that link to three colours.

This note classifies link colourings. It does not produce a colouring of a spherical triangulation, and the degree-5 step of `hole-induction.md` still quotes the vacancy hypothesis.

Colours are $\{0,1,2,3\}$. The link is a 5-cycle with vertices $0,1,2,3,4$ in order. A chord is an edge $i\,(i+2)$ with indices modulo 5. The fans are
$$
\tau_i = \bigl\{\, i\,(i+2),\; i\,(i+3) \,\bigr\}.
$$
A colouring of the five vertices is **fan-proper** when it is proper on the cycle and on the two chords of at least one fan. Those two chords are the ones added on the vacant side in $T^\star$. Kempe swaps are read in the opposite disk, the interior of $T-v$, where the added fan is absent. A path through that disk may be present or absent. A swap is available only when the two link vertices of its colour pair lie in different components. The separation is forced only when every interior separates them.

## The two orbits

Up to the action of the dihedral group on the cycle and the renaming of the four colours, there are exactly two fan-proper colourings.

A proper colouring of a 5-cycle uses at least three colours: the cycle is odd. An independent set has size at most 2, so no colour occurs three times.

If exactly three colours occur, the sizes are $2,2,1$. Place the first repeated colour $\alpha$ on vertices $0$ and $2$. Vertices $1$, $3$ and $4$ remain. The pair $3,4$ is an edge, so the second repeated colour occupies $\{1,3\}$ or $\{1,4\}$. The two colourings are
$$
(\alpha,\beta,\alpha,\beta,\gamma)
\qquad\text{and}\qquad
(\alpha,\beta,\alpha,\gamma,\beta).
$$
Reversing the first and rotating it produces the second. They are one orbit. The representative used below is $(0,1,0,1,2)$.

If all four colours occur, the sizes are $2,1,1,1$. The two vertices of the repeated colour are non-adjacent, hence at cyclic distance $2$. Place them on vertices $0$ and $2$, both coloured $\alpha$. Vertices $1$, $3$ and $4$ are each adjacent to an $\alpha$ vertex, so none is coloured $\alpha$, and the edge $3\,4$ forces those three vertices to carry the other three colours, one each. The representative is
$$
(0,1,0,2,3).
$$
Reflection swaps the colours on vertices $3$ and $4$, which a renaming absorbs. There is one orbit.

Every proper colouring of the cycle with colours drawn from a set of four falls into one of these two orbits, and each orbit is fan-proper. The checks are the next two sections.

## Three colours

The representative $(0,1,0,1,2)$ uses the set $\{0,1,2\}$. The five vertices already use at most three colours. The missing colour is $3$.

The monochromatic chords are $0\,2$, both ends colour $0$, and $1\,3$, both ends colour $1$. Each lies in two fans, and no fan contains both, because the four endpoints alternate around the cycle. Those four fans are improper. The remaining fan is
$$
\tau_4 = \{4\,1,\; 4\,2\},
$$
with colours $2\,1$ and $2\,0$. Vertex $4$ is the unique vertex of colour $2$, so both chords from it are bichromatic. The same count holds after dihedral movement: the only proper fan is the fan based at the vertex of unique colour.

No Kempe swap is required.

## Four colours

The representative is
$$
c(0)=\alpha=0,\;
c(1)=\beta=1,\;
c(2)=\alpha=0,\;
c(3)=\gamma=2,\;
c(4)=\delta=3,
$$
with $\{\alpha,\beta,\gamma,\delta\}=\{0,1,2,3\}$.

The only monochromatic chord is $0\,2$. It lies in $\tau_0$ and in $\tau_2$. The other three fans are proper:
$$
\begin{align*}
\tau_1 &= \{1\,3,\; 1\,4\}, \\
\tau_3 &= \{3\,0,\; 3\,1\}, \\
\tau_4 &= \{4\,1,\; 4\,2\}.
\end{align*}
$$
Their endpoint colours are $1\,2$ and $1\,3$, then $2\,0$ and $2\,1$, then $3\,1$ and $3\,0$.

A Kempe swap exchanges two colours on one component of their bichromatic subgraph in the interior disk. The effect on the link depends only on which link vertices lie in the swapped component. The six pairs are as follows.

**Pair $\{\alpha,\beta\}$.** Vertices $0$, $1$ and $2$ carry these colours, and the cycle edges $0\,1$ and $1\,2$ are both $\alpha\beta$-edges. The three vertices are one component. The swap sends the link to $(\beta,\alpha,\beta,\gamma,\delta)$, which uses four colours.

**Pair $\{\gamma,\delta\}$.** Vertices $3$ and $4$ are adjacent, so they are one component. The swap sends the link to $(\alpha,\beta,\alpha,\delta,\gamma)$, which uses four colours.

**Pair $\{\alpha,\gamma\}$.** The cycle edge $2\,3$ is an $\alpha\gamma$-edge, so vertices $2$ and $3$ lie in one component. Vertex $0$ may or may not lie in it.

- All three: the link becomes $(\gamma,\beta,\gamma,\alpha,\delta)$.
- Vertices $2$ and $3$ only: the link becomes $(\alpha,\beta,\gamma,\alpha,\delta)$.
- Vertex $0$ only: the link becomes $(\gamma,\beta,\alpha,\gamma,\delta)$.

Each uses four colours.

**Pair $\{\alpha,\delta\}$.** The cycle edge $4\,0$ puts vertices $0$ and $4$ in one component. Vertex $2$ may or may not lie in it.

- All three: the link becomes $(\delta,\beta,\delta,\gamma,\alpha)$.
- Vertices $0$ and $4$ only: the link becomes $(\delta,\beta,\alpha,\gamma,\alpha)$.
- Vertex $2$ only: the link becomes $(\alpha,\beta,\delta,\gamma,\delta)$.

Each uses four colours.

**Pair $\{\beta,\gamma\}$.** The link vertices are $1$ and $3$.

- Same component: the link becomes $(\alpha,\gamma,\alpha,\beta,\delta)$, four colours.
- Swap only vertex $1$: the link becomes $(\alpha,\gamma,\alpha,\gamma,\delta)$, the set $\{\alpha,\gamma,\delta\}$.
- Swap only vertex $3$: the link becomes $(\alpha,\beta,\alpha,\beta,\delta)$, the set $\{\alpha,\beta,\delta\}$.

**Pair $\{\beta,\delta\}$.** The link vertices are $1$ and $4$.

- Same component: the link becomes $(\alpha,\delta,\alpha,\gamma,\beta)$, four colours.
- Swap only vertex $1$: the link becomes $(\alpha,\delta,\alpha,\gamma,\delta)$, the set $\{\alpha,\gamma,\delta\}$.
- Swap only vertex $4$: the link becomes $(\alpha,\beta,\alpha,\gamma,\beta)$, the set $\{\alpha,\beta,\gamma\}$.

Thus a single swap reduces the link to three colours precisely when vertex $1$ and vertex $3$ lie in different $\{\beta,\gamma\}$-components, or vertex $1$ and vertex $4$ lie in different $\{\beta,\delta\}$-components. In the first branch, swap the component of vertex $1$ in colours $\beta$ and $\gamma$. In the second, swap the component of vertex $1$ in colours $\beta$ and $\delta$. Either branch frees a colour.

Neither separation is forced. The two branches and the remaining branch are all realizable, and the remaining branch does not reduce.

**If there is no $\{\beta,\gamma\}$-path from $1$ to $3$.** The first swap applies.

**If there is no $\{\beta,\delta\}$-path from $1$ to $4$.** The second swap applies.

**If both paths exist.** Both of those swaps exchange the colour at vertex $1$ with the colour at the far end, and the link still uses four colours. The other four pairs never reduce the link. This is the gap.

The Jordan barriers in this third branch are real, and they fall on the pairs that do not free a colour. A $\{\beta,\delta\}$-path from vertex $1$ to vertex $4$ meets the cycle in those two vertices and separates vertex $0$ from vertex $2$. Vertex $2$ is tied to vertex $3$ by the edge $2\,3$, so vertex $0$ lies outside that $\{\alpha,\gamma\}$-component. The swaps displayed for $\{\alpha,\gamma\}$ still leave four colours. Likewise a $\{\beta,\gamma\}$-path from vertex $1$ to vertex $3$ separates vertex $2$ from vertex $4$, and vertex $4$ is tied to vertex $0$ by the edge $4\,0$. The swaps displayed for $\{\alpha,\delta\}$ still leave four colours. The degree-4 argument swaps the pair that the barrier separates. Here the barrier separates a pair whose swap keeps four colours on the link, while each pair whose swap would leave three colours is the pair joined by a path.

Placing both connections as the chords $1\,3$ and $1\,4$ themselves is a different filling. Those two chords are $\tau_1$, lying in the interior. The fans disjoint from $\tau_1$ are $\tau_0$ and $\tau_2$, and each contains the monochromatic chord $0\,2$, so this colouring is proper on neither of them. That filling cannot arise by adding a fan to $T-v$. The interior below uses no chord of the link. Both paths run through interior vertices, the set of existing link chords is empty, and $\tau_1$ may be added on the vacant side.

## The interior in which both paths meet the link

The graph is the gyroelongated hexagonal dipyramid. It has fourteen vertices and is a simple spherical triangulation of minimum degree $5$: the two poles have degree $6$ and the other twelve vertices have degree $5$. There are $36$ edges and $24$ triangular faces.

Vertices: a north pole $N$, a south pole $S$, an upper hexagon $U_0,\ldots,U_5$, and a lower hexagon $L_0,\ldots,L_5$. Edges:

- $N$ to every $U_i$, and $S$ to every $L_i$;
- $U_i U_{i+1}$ and $L_i L_{i+1}$;
- $U_i L_i$ and $U_i L_{i+1}$;

with hexagon indices modulo $6$. The faces are $(N, U_i, U_{i+1})$, $(S, L_{i+1}, L_i)$, $(U_i, L_i, L_{i+1})$ and $(U_i, L_{i+1}, U_{i+1})$.

Delete $U_0$. Its link, in cyclic order, is
$$
(U_1,\; N,\; U_5,\; L_0,\; L_1).
$$
Colour the remaining vertices by
$$
\begin{align*}
N &= 1, & S &= 0, \\
U_1 &= 0, & U_2 &= 3, & U_3 &= 0, & U_4 &= 2, & U_5 &= 0, \\
L_0 &= 2, & L_1 &= 3, & L_2 &= 1, & L_3 &= 2, & L_4 &= 3, & L_5 &= 1.
\end{align*}
$$
Every edge with both ends among these thirteen vertices joins different colours. In link order the colours are $(0,1,0,2,3)$.

The $\{\,1,2\,\}$-path from $N$ to $L_0$ is
$$
N \xrightarrow{\,1\,} U_4 \xrightarrow{\,2\,} L_5 \xrightarrow{\,1\,} L_0,
$$
and the colours along it are $1,2,1,2$. The $\{\,1,3\,\}$-path from $N$ to $L_1$ is
$$
N \xrightarrow{\,1\,} U_2 \xrightarrow{\,3\,} L_2 \xrightarrow{\,1\,} L_1,
$$
and the colours along it are $1,3,1,3$. Under the labelling of the link as positions $0,1,2,3,4$, these are a $\beta\gamma$-path from vertex $1$ to vertex $3$ and a $\beta\delta$-path from vertex $1$ to vertex $4$.

Label the link as positions $0,1,2,3,4$ in the order $(U_1, N, U_5, L_0, L_1)$. The five possible chords and the edges actually present are:

- positions $0\,2$, the pair $U_1 U_5$: on the upper hexagon $U_1$ meets $U_0$ and $U_2$;
- positions $0\,3$, the pair $U_1 L_0$: $U_1$ meets $L_1$ and $L_2$;
- positions $1\,3$, the pair $N L_0$: $N$ meets only the upper hexagon;
- positions $1\,4$, the pair $N L_1$: same;
- positions $2\,4$, the pair $U_5 L_1$: $U_5$ meets $L_5$ and $L_0$.

None of the five is an edge. The set of link chords in the interior is empty, so it is contained in every fan. The added fan may be $\tau_1$, the chords $N L_0$ and $N L_1$. Their colours are $1\,2$ and $1\,3$. The same thirteen colours are proper on the triangulation $T^\star$ obtained by adding that fan across the face left by $U_0$. The colouring is a restriction of a proper $4$-colouring of $T^\star$, which is the input the degree-5 step allows.

On this interior the component of $N$ in colours $1$ and $2$ contains $L_0$, and the component of $N$ in colours $1$ and $3$ contains $L_1$. Swapping the first component sends the link to $(0,2,0,1,3)$. Swapping the second sends it to $(0,3,0,2,1)$. Each still uses four colours. The other four pairs leave four colours on the link for every way an interior can join their vertices.

## Feasibility

Feasibility that every fan-proper colouring of a 5-cycle link already uses at most three colours, or is reduced to three colours by one Kempe swap on a single bichromatic pair whose separation is forced by an arbitrary interior: **Low**. The three-colour orbit is already inside three colours. The four-colour orbit has an interior, inside a minimum-degree-$5$ triangulation, in which neither useful pair separates.

## Next steps

1. Keep the degree-5 step on the vacancy hypothesis. The case in which both the $\{1,2\}$-path and the $\{1,3\}$-path meet the link $(0,1,0,2,3)$ is not a Jordan split of degree-4 type.
2. Any substitute for that hypothesis has to use a move other than one bichromatic swap on this link, or a restriction on interiors strong enough to exclude the dipyramid colouring above.
3. The three-colour orbit and the two separated branches of the four-colour orbit are settled by the missing colour and by one swap. They are the branches in which a degree-5 link does behave like the degree-4 link.

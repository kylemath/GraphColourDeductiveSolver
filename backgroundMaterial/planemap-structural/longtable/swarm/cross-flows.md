# Nowhere-zero flows against the equal-pole charge

**KILL ALL.** A flow translation of the population obstruction restates Tutte's equivalence or the equal-pole star. On the known colouring it produces no new legal move.

The seed is nowhere-zero flows, tensions, and electrical networks. Variability seed 64 adds constant shifts in the cyclic palette $\mathbb{Z}/4\mathbb{Z}$, beside the three translations of the colour group $\Gamma=\mathbb{Z}_2\times\mathbb{Z}_2$. Nothing here is a four-colour proof. The census is one colouring of one deletion.

## The colouring the census uses

$G_8$ has poles $a,b$ and belt $u_i,v_i$ modulo 8, with edges $a{-}u_i$, $b{-}v_i$, $u_i{-}u_{i+1}$, $v_i{-}v_{i+1}$, $u_i{-}v_i$, $u_i{-}v_{i-1}$, and no edge $a{-}b$. The hole is $u_0$. The equal-pole colouring from the belt census is periodic of period three off colour 0:

| Vertex | $a$ | $b$ | $u_1$ | $u_2$ | $u_3$ | $u_4$ | $u_5$ | $u_6$ | $u_7$ | $v_0$ | $v_1$ | $v_2$ | $v_3$ | $v_4$ | $v_5$ | $v_6$ | $v_7$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Colour | 0 | 0 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 |

The population on the 17 coloured vertices is $(2,5,5,5)$: colour 0 twice, at the two poles, and colours 1, 2, 3 five times each. The link of $u_0$ is $(a,u_1,v_0,v_7,u_7)$ with colours $(0,1,2,3,1)$.

Group labels: $0=(0,0)$, $1=(1,0)$, $2=(0,1)$, $3=(1,1)$. On an edge with both ends coloured the tension is $\tau(xy)=c(x)+c(y)\in\Gamma\setminus\{0\}$. That function is already a nowhere-zero $\Gamma$-tension of the coloured subgraph. The five spokes at $u_0$ carry no value. Slides preserve the colour multiset. The star swap is the Kempe change that alters it.

## 1. A nowhere-zero 4-flow on the cubic dual

**Object.** The Tait colouring of the dual, equivalently a nowhere-zero 4-flow.

**How it dies.** Tutte's equivalence says a bridgeless cubic planar graph is 3-edge-colourable if and only if it has a nowhere-zero 4-flow, and Tait's theorem identifies that statement with the Four Colour Theorem. On a triangulation the same fact is the dual of a vertex colouring: $\tau(xy)=c(x)+c(y)$ is the flow on the dual edge. Asking for a nowhere-zero flow on the dual of $G_8$ asks for a 4-colouring of $G_8$. The partial tension we already have is the colouring of $G_8-u_0$ written on edges. Completing it uses the missing flow as an oracle.

Feasibility of a new legal move from this identification: **Low**.

## 2. Extending the partial tension across the five spokes

**Object.** For each candidate colour $\gamma\in\Gamma$, the spoke values $s_x=\gamma+c(x)$ on the link of the hole.

**Computation.** The link tensions along $(a,u_1,v_0,v_7,u_7)$ are
\[
(1,0),\ (1,1),\ (1,0),\ (0,1),\ (1,0).
\]
Their sum in $\Gamma$ is $0$, so the cycle law holds and the five face equations around $u_0$ are consistent. The solution space is a torsor of $\Gamma$: one free value $\gamma$, then $s_x=\gamma+c(x)$. Nowhere-zero spokes are the $\gamma$ absent from the link.

| $\gamma$ | Zero spokes |
| ---: | --- |
| 0 | $a$ |
| 1 | $u_1,u_7$ |
| 2 | $v_0$ |
| 3 | $v_7$ |

Every candidate has a zero. The zero set of $\gamma$ is the set of link vertices already coloured $\gamma$.

**How it dies.** The computation reads the link colours $(0,1,2,3,1)$ back off the spokes. Emptiness of the allowed $\gamma$ is the statement that the boundary uses four colours. The documented star is the Kempe change that empties the zero set of colour 3; after it, $v_7$ carries 0 and the link uses $\{0,1,2\}$. The tension equations name that fact and supply no other edit.

Feasibility of a new legal move from this identification: **Low**.

## 3. The population as a potential sum, or as a tension histogram

**Object.** The sum $\sum c(v)\in\Gamma$ over coloured vertices, and the histogram of $\tau$ on the 43 edges with both ends coloured.

**Computation.** The sum is
\[
5(1,0)+5(0,1)+5(1,1)=(0,0),
\]
since the two poles contribute $0$ and each count 5 is odd. A full colouring of population $(4,4,5,5)$ has exactly two odd colour classes, and the sum of two distinct group elements is nonzero. Slides preserve the sum. The size-4 star preserves it as well, because an even set shifted by $\kappa$ changes the sum by $0$. The size-3 $a$-star changes it. Both stars fill, so the sum does not select the filling move.

The tension histogram on the 43 coloured edges is $(15,14,14)$, with the excess on the value $1\in\Gamma$. The slide $u_0\to v_7$ preserves the population and sends the labelled counts from $\{1{:}15,\ 2{:}14,\ 3{:}14\}$ to $\{1{:}14,\ 2{:}15,\ 3{:}14\}$. The sorted triple stays $(15,14,14)$. The same sorted triple is unchanged by each of the six pole-to-belt Kempe components of pairs $(0,1)$, $(0,2)$, and $(0,3)$, filling and non-filling alike. Filling the hole after the documented star produces the balanced histogram $(16,16,16)$ on all 48 edges.

**How it dies.** The sum is the population vector read in $\Gamma$. The flow, being differences, records it only after a base colour is fixed, which returns the vertex colouring. The sorted histogram is constant across the star, so it is blind to the charge repair; it becomes uniform when the five spokes receive values, which is the fill itself. The excess of one edge is the residue $43\bmod 3$ coming from a degree-5 hole. An electrical energy of $\tau$ is likewise constant or reversible on slides, and the slide graph on this component is already known to be reversible and targetless.

Feasibility of a Lyapunov function, or a new move, read from these two edge statistics: **Low**.

## 4. A $\kappa$-cut: the flow augmentation that stays a proper colouring

**Object.** A nonempty set $S$ of coloured vertices and a nonzero $\kappa\in\Gamma$. Replace $c$ by $c+\kappa$ on $S$. Internal edges keep their tensions. Every cut edge changes by $\kappa$. The result is proper exactly when no cut edge already carries tension $\kappa$, which means $S$ is a union of Kempe components for the two colour-pairs of $\kappa$. One such cut can swap both pairs at once. That is the only candidate the seed offers for a move larger than a single Kempe chain.

**Computation, performed on this colouring.** All $2^{17}-1$ nonempty subsets, for each of the three nonzero group translations. A shift counts as a repair when the new colouring is proper and the link uses at most three colours, so the missing colour fills $u_0$ and the completed colouring is a proper 4-colouring of $G_8$.

The repairs are eight, in two families.

| $\kappa$ (colour added) | Small set | Size | Fill colour | Complement size |
| --- | --- | ---: | ---: | ---: |
| $2$ | $\{a,u_2,u_5\}$ | 3 | 0 | 14 |
| $2$ | $\{b,v_0,v_3,v_6\}$ | 4 | 2 | 13 |
| $3$ | $\{a,u_3,u_6\}$ | 3 | 0 | 14 |
| $3$ | $\{b,v_1,v_4,v_7\}$ | 4 | 3 | 13 |

Each small set is a single Kempe component of one pair, and it meets only that pair. The documented star is the last row. The other size-4 set is the symmetric $b$-star on colours 0 and 2, and the two size-3 sets are the $a$-stars. Each complement equals the corresponding star followed by the global translation $c\mapsto c+\kappa$. Translation preserves properness and permutes colours; it is the same swap.

No repairing set meets both colour-pairs of its $\kappa$. The third direction, adding colour 1, repairs nothing. Its two components do change the charge: swapping $\{a,u_1,u_4,u_7\}$ is proper and moves the population from $(2,5,5,5)$ to $(4,3,5,5)$, but the link becomes $(1,0,0,2,3)$ and still uses four colours. A cut can repair the charge and leave the hole blocked. The cuts that open the hole are the four stars above.

**How it dies.** The legal flow augmentation on this colouring is the equal-pole star swap, counted once for each pole and each of the two belt colours that meet that pole, together with global relabeling. The identification of a cut-flow with a new move dies on the census.

Feasibility that a $\kappa$-cut outside a single Kempe component fills this hole: **Low**. The census is empty of such cuts.

## 5. Cyclic one-volt shifts, and the harmonic extension

**Object.** Seed 64. Keep the palette order $0,1,2,3$ and add $1$ or $3$ modulo 4 on a set $S$, wrapping 3 to 0. This permutation is not a translation of $\Gamma$. Separately, embed $\Gamma$ in $\mathbb{R}^2$ and take the harmonic extension at the hole with the coloured vertices fixed, one unit resistor on each edge.

**Computation.** The same $2^{17}-1$ subsets, for shifts $+1$ and $+3$. No nonempty subset is a proper recolouring that repairs the population to a pre-fill shape $(3,4,5,5)$ or $(4,4,4,5)$, and none clears the link.

The neighbour average at $u_0$ is $(3/5,2/5)$. The nearest lattice colour is $1=(1,0)$. Colour 1 is the repeated colour on the link, so the harmonic proposal is one of the two illegal fills with a double zero spoke. Every one of the 17 coloured vertices already has the other three colours on its coloured neighbours, so a one-vertex recolour is unavailable. The integer coboundary $c(y)-c(x)$ has divergences at the coloured vertices summing to 0, because each coloured edge cancels; the hole contributes no net charge to that sum.

**How it dies.** The cyclic wrap was the risky extra identification. On this colouring it has no proper population-changing instance at all. The electrical average proposes the duplicated link colour, and the divergence sum is blind to the hole. A non-wrapping shift by $+1$, refusing to send colour 3 to a fifth voltage, cannot raise the deficient count 2, because only a wrap turns a 3 into a 0.

Feasibility of a cyclic or harmonic move that fills this hole: **Low**.

## What the five mappings leave standing

The partial colouring determines its tension. Every edit that stays inside that tension and clears $u_0$ is a pole star already used by the equal-pole swap. The population gap $(2,5,5,5)$ against the full-graph counts $(4,4,5,5)$ is visible to the vertex sum and invisible to the sorted tension histogram. Neither statistic names a move.

Feasibility that nowhere-zero flows, tensions, or electrical networks suggest a legal move on this barrier beyond the star swap: **Low**.

## Next steps

1. Keep the population repair as the equal-pole star. A flow formulation of that star is the cut $\delta(S)$ shifted by $\kappa$, with $S$ the star, and the census says the other cuts do not fill.
2. Leave unequal poles outside this seed. The computation that would be required there is a different colouring, and a nowhere-zero flow on the dual would again be an oracle.
3. Spend no sweep searching for a 4-flow, a tension histogram rank, or a harmonic fill on $G_8-u_0$. The 32-state slide component is unchanged by any of those objects.

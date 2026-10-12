# Chip-firing and the equal-pole star swap

4 October 2026. Variability seed 41. A mapping note. It uses the hand argument in `SolvingFrameworkPlan/docs/reports/TwoPoleStarEscape.md` and the equal-pole colouring recorded in `swarm/unequal-poles.md`. It does not search colourings, and it does not claim a four-colour theorem.

A firing script $\sigma$ changes a chip configuration by $-\Delta\sigma$, where

$$
(\Delta f)(x)=\deg(x)\,f(x)-\sum_{y\sim x}f(y).
$$

Every such change is principal. On a graph with no sink, every principal divisor has degree $0$. With a sink, the same formula uses the full degree on the diagonal and $\sigma(\mathrm{sink})=0$; the cokernel of that reduced Laplacian is the sandpile group, of order equal to the number of spanning trees.

## Verdict

**KILL ALL.**

| # | Foreign construction | Colouring object | Barrier | Verdict |
| --- | --- | --- | --- | --- |
| 1 | Critical group, degree of a principal divisor (Biggs; Bacher–de la Harpe–Nagnibeda) | Colour-label divisor on $G_n-u_0$ | The star swap changes $(2,5,5,5)$ | KILL |
| 2 | Matrix-tree theorem, reduced Laplacian | Same divisor, hole as sink | The swap should be one integral toppling | KILL |
| 3 | Critical group of a tree | The $(A,B)$-star itself | The swap should be a firing inside its component | KILL |
| 4 | Björner–Lovász–Shor; Dhar burning | Legal topplings of the label configuration | Slides are reversible and should be firings | KILL |
| 5 | Merino's theorem; Baker–Norine rank | Sandpile group of the triangulation, or rank of the labels | A rank that falls on the swap and on the 21 traps | KILL |

No survivor. The charge repair is a change of degree. Sandpile equivalence on the coloured graph preserves degree, and the sink refinement still leaves a nontrivial class.

## The witness

Take $n=8$, so $k=2$ and $n=3k+2$. The hole is $u_0$. Poles $a,b$ have degree $8$; every belt vertex has degree $5$. The graph has $18$ vertices and $48$ edges. The deletion $H=G_8-u_0$ has $17$ vertices and $43$ edges.

The equal-pole colouring, periodic of period three off colour $0$:

| Vertex | $a$ | $b$ | $u_1$ | $u_2$ | $u_3$ | $u_4$ | $u_5$ | $u_6$ | $u_7$ | $v_0$ | $v_1$ | $v_2$ | $v_3$ | $v_4$ | $v_5$ | $v_6$ | $v_7$ |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Colour | 0 | 0 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 | 1 | 2 | 3 |

Populations $(2,5,5,5)$. The link of $u_0$ is $(a,u_1,u_7,v_0,v_7)$ with colours $(0,1,1,2,3)$. The singleton colours are $0$ at $a$, $2$ at $v_0$, and $3$ at $v_7$.

The $(0,3)$-component of $b$ is the star $\{b,v_1,v_4,v_7\}$. Swapping colours $0$ and $3$ there sends the populations to $(4,3,5,5)$ and the link colours to $(0,1,1,2,0)$. Filling $u_0$ with colour $3$ produces a proper colouring of $G_8$ with populations $(4,4,5,5)$.

Slides from this colouring stay inside a $32$-state component on which every population is still $(2,5,5,5)$ and every link still uses four colours (`swarm/unequal-poles.md`, `swarm/hole-support.md`).

The label sum on $H$ is $30$. After the swap it is $24$.

## 1. Colour labels as a divisor

**Theorem.** The critical group is the cokernel of the Laplacian. Principal divisors are the image of $\Delta$, and each has degree $0$ (Biggs, *Chip-firing and the critical group of a graph*; Bacher–de la Harpe–Nagnibeda, the Picard group of a graph).

**Object.** $D_c=\sum_{v\neq u_0} c(v)\,v$ on $H$.

**Barrier.** The star swap is the move that changes $(2,5,5,5)$ toward $(4,4,5,5)$. A firing script realizing that change would keep $D_c$ inside one sandpile class.

**Kill.** For $n=3k+2$ the other-pole star contains $k+1$ belt vertices of the singleton boundary colour $B$. Exchanging labels $\alpha(A)$ and $\alpha(B)$ changes the degree of $D_c$ by

$$
k\bigl(\alpha(A)-\alpha(B)\bigr).
$$

Here $k=2$, $A=0$, $B=3$, and the degree goes from $30$ to $24$. The change is

$$
\delta=3\,e_b-3\,e_{v_1}-3\,e_{v_4}-3\,e_{v_7},
$$

of degree $-6$. A vector of nonzero degree lies outside the principal lattice, so the swap is outside every integer firing script on $H$. The same count with the names of colours $0$ and $3$ exchanged gives label sums $21$ before the swap and $27$ after it. The degree drops by $6$ for one naming of this orbit and rises by $6$ for the other, so the degree supplies no naming-free rank on the charge.

A slide preserves the multiset of colours, so it preserves this degree for every naming. The move that changes the charge is the move the principal lattice excludes.

## 2. The hole as sink

**Theorem.** For a connected graph, every cofactor of $\Delta$ equals the number of spanning trees (Kirchhoff). That cofactor is the order of the sandpile group.

**Object.** The same label divisor, now read on $V(G_8)\setminus\{u_0\}$, with sink $u_0$.

**Barrier.** Allow chips to fall into the hole, so that a script may change the degree, and ask whether $\delta$ itself is one integral toppling.

**Kill.** The reduced Laplacian $\Delta'$ is invertible over $\mathbb{Q}$. The unique rational script $\sigma=(\Delta')^{-1}\delta$ was computed from this graph. Every one of the $17$ coordinates is nonzero, and the least common denominator is

$$
61663=7\cdot 23\cdot 383.
$$

The $b$-coordinate is $-71796/61663$, in lowest terms. The system $\Delta'\sigma=\delta$ is unsolvable modulo $7$, modulo $23$, and modulo $383$, and $61663$ is the least positive integer $m$ for which $m\delta$ is an integral script. The class $[\delta]$ therefore has order $61663$ in the sandpile group of $G_8$. An integral toppling would have produced the zero class.

The same non-integrality holds for the primitive vector $\delta/3$, which has the same order $61663$, and it holds again when the sink is moved to $a$, to $u_1$, or to $v_0$. With the sink at $b$, the coordinate $\delta(b)=3$ is omitted from the configuration, and the remaining vector still has non-integral script (denominator $493304$).

The order of the group itself is the tree number

$$
\kappa(G_8)=60837209104,
$$

the $u_0$-cofactor, checked by exact determinant. It depends on the bare graph. It is the same number for the equal-pole colouring, for a slide landing, and for the filled colouring of populations $(4,4,5,5)$.

## 3. Firing inside the star

**Theorem.** A tree has one spanning tree, so its critical group is trivial. Equivalence classes on a tree are the degree-zero divisors, and each such divisor is principal.

**Object.** The bichromatic component $K=\{b\}\cup\{v_i:c(v_i)=B\}$. On the witness this is the star $K_{1,3}$ with centre $b$ and leaves $v_1,v_4,v_7$, each joined only to $b$. In general it is the star $K_{1,k+1}$.

**Barrier.** Identify the swap with a firing supported on the component that the swap actually recolours.

**Kill.** Restrict $\delta$ to $K$. For a label gap $\lambda=\alpha(B)-\alpha(A)$ the restricted change has degree $-k\lambda$. On the witness, $\lambda=3$ and $k=2$, so the degree on the star is $-6$. The image of the star Laplacian lies in the degree-zero hyperplane, over $\mathbb{Z}$ and over $\mathbb{Q}$. The swap leaves that hyperplane. Triviality of the critical group equates configurations only after their degrees already agree, and the population repair is exactly the disagreement: one vertex of colour $A$ against $k+1$ vertices of colour $B$.

Firing the centre subtracts $k+1$ at $b$ and adds $1$ at each leaf. The swap adds the same quantity at $b$ that it subtracts at each leaf. Those two vectors are scalar multiples only for $k+1=1$, which is $n=2$, outside the family $n\ge 5$.

## 4. Slides as legal topplings

**Theorem.** Björner–Lovász–Shor: if a configuration admits a legal firing, and the total number of chips is strictly less than the number of edges, every firing sequence terminates at the same stable configuration. Dhar's burning algorithm: with the sink already burnt, a further vertex burns when its chip count is at least its number of edges into the unburnt set; a stable configuration is recurrent exactly when every vertex burns.

**Object.** The label configuration on $H$, and the three legal slides from $u_0$.

**Barrier.** Slides are reversible and preserve colour counts. A toppling rule was the candidate replacement, with the star swap as one further firing.

**Kill.** Every label is in $\{0,1,2,3\}$ and every degree on $H$ is $5$ or $8$. A legal toppling needs at least $\deg(v)$ chips, so the legal toppling set is empty. The legal slide set is $\{a,v_0,v_7\}$.

Firing $v_7$ once would add one chip to each of $b$, $u_7$, $v_0$, and $v_6$, and drop the value at $v_7$ by $5$. The slide $u_0\to v_7$ writes colour $3$ onto the hole and leaves $b$ coloured $0$. The two updates disagree at $b$.

The variability offset $41$ adds $41$ chips at every non-sink vertex. The difference of the two label divisors is still $\delta$, so the class of mapping 2 is unchanged. The offset configuration has at least $41$ chips at every vertex and maximum degree $8$, so the legal toppling set is all $17$ non-sink vertices. That set properly contains the star and the slide set, and it includes vertices such as $u_2$ whose colours the swap and the slides leave fixed.

Dhar's test, at offset $0$, burns nothing: a neighbour of the sink has at most $3$ chips and at least $4$ edges into the unburnt set. Both the pre-swap and the post-swap label configurations are stable and transient. Burning does not become available when the charge moves from $(2,5,5,5)$ to $(4,3,5,5)$.

The slide component has $32$ states and returns. A rule with a return has no terminal configuration for Björner–Lovász–Shor to name. Every state in that component still has four colours on the link, so the slide rule also has no filled terminal state inside the component. The star swap is the exit, and mappings 1–3 exclude it from the firing rule.

## 5. The group of the triangulation, and the rank of the labels

**Theorem.** Merino: the generating function of recurrent configurations by level equals the Tutte evaluation $T_G(1,y)$. The chromatic polynomial is the other axis, $\chi_G(\lambda)=(-1)^{n-c}\lambda^c T_G(1-\lambda,0)$. Baker–Norine: the rank $r(D)$ of a divisor satisfies $r(D)-r(K-D)=\deg(D)+1-g$, and $r(D)=\deg(D)-g$ whenever $\deg(D)>2g-2$.

**Object.** The sandpile group of the uncoloured triangulation, the population vector as a configuration on the four colours, and $r(D_c)$.

**Barrier.** A rank that falls when the star swap changes $(2,5,5,5)$, that also falls on the $21$ mass traps, and that survives the next colouring of order $17$ graph $3$.

**Kill.** The sandpile group of a triangulation is an invariant of the uncoloured graph. On $G_8$ it has order $60837209104$ for every colouring. Merino's polynomial reads $T_G(1,y)$. Four-colour counts read $T_G(1-\lambda,0)$. The group is too coarse to see colours, and too coarse to see the charge.

The smallest triangulation already separates the two counts. The sandpile group of $K_4$ is $(\mathbb{Z}/4\mathbb{Z})^2$, of order $16$, while $K_4$ has $24$ proper vertex $4$-colourings.

Reading the population jump as a divisor on the colour set $K_4$ gives the same coarseness in miniature. The witness moves populations by $2(e_0-e_3)=(2,0,0,-2)$ up to order of coordinates. The Laplacian of $K_4$ is $4I-J$. On the sum-zero hyperplane it acts as multiplication by $4$, so

$$
\Delta\Bigl(\tfrac12,0,0,-\tfrac12\Bigr)=(2,0,0,-2)
$$

and the script is half-integral. Twice the jump is principal and the jump itself has order $2$ in $(\mathbb{Z}/4\mathbb{Z})^2$. The star swap preserves no sandpile class on $K_4$.

On the single edge between the two colours whose counts change, the critical group is trivial: two firings realize the jump $2(e_A-e_B)$, and every configuration represents the same unique element. That element is preserved by the swap, by every slide, and by every colouring of every mass trap. A constant does not fall on the swap. The $21$ traps are already at population $(4,4,4,4)$ (`SolvingFrameworkPlan/docs/working/SwarmConsolidation.md`), so a population class that can see $(2,5,5,5)$ is constant on those traps.

Baker–Norine rank of $D_c$ is a rank in the sense of the barrier, and it dies on the witness before order $17$ graph $3$ is reached. The deletion has genus $g=27$ and canonical degree $2g-2=52$. The two namings above have degrees $30$ and $21$, both at most $52$, so the rank is outside the range where Riemann–Roch collapses it to a function of degree. The divisor itself changes when the colours are renamed, and the degree falls for one naming and rises for the other. There is no well-defined value to compare with the slide landings, and none to take to order $17$ graph $3$ root $3$ colouring $44$, where the published pairs already fail by $q:107\to 111$ (`swarm/rank-kill.md`).

## What would reopen it

A reopening needs an explicit divisor on the pair $(\mathrm{hole},\mathrm{colouring})$ that is constant under permuting the four colour names, takes a different sandpile class, or a different Baker–Norine rank, after this star swap than before it, and does so by an integral script. The degree formula in mapping 1 forbids any divisor that is a function of the colour labels alone. The tree number forbids any invariant that depends only on the triangulation.

Feasibility of an unnamed chip-firing identification of the star swap, or of a vacancy slide, with a toppling that preserves a sandpile class and falls as a rank: **Low**. Speculative. The five constructions above are closed.

KILL ALL.

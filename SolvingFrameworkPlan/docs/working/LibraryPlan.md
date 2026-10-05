# What not to compute

4 October 2026. A plan made from the swarm results and from two published theorems. It does not start a new search.

## Stop

These experiments would repeat a result that is already in hand.

**Do not colour the pentakis dodecahedron or the frequency-2 icosahedron to test the bridge.** On the 15-vertex star of either graph there is a proper colouring, boundary pattern $2,1,1,1$, for which every second slide onto a far pentagon is illegal. A slightly larger patch sends every remaining forward slide onto another locked pentagon. The geometry does not force an exit. `longtable/swarm/isolated-local.md`.

**Do not score another pair $(f, q)$ on the 21 mass traps.** $q$, $(p,q)$, $(n_5,q)$, $(d_{\min},q)$, $\mathrm{repMass}$, $(L,q)$, $\mathrm{lin}$, and the exterior-size tuple already fail. $(\mathrm{shortLinks}, q)$ and $(H, q)$ pass the 21 and die on the next colouring of order 17 graph 3. `longtable/swarm/rank-kill.md`.

**Do not breadth-first search the 32-state component of order 18 graph 10 for a second Kempe swap.** The component is one orbit of population $(2,5,5,5)$. The hole set is all 18 vertices, including both degree-8 poles. Every belt state has equal pole colours, and the star swap fills it in one Kempe change. Sliding onto a pole keeps the population $(2,5,5,5)$ and does not fill. `longtable/swarm/hole-support.md` and `TwoPoleStarEscape.md`.

**Do not cite Meyniel as a proof of the one-hole path.** Meyniel (1978) says that all 5-colourings of a planar graph are Kempe equivalent. Deschamps, de Joannis de Verclos, Heinrich, Le, and Thomassé (arXiv:2201.07595) give a polynomial bound on the number of changes. Both theorems allow intermediate colourings with many vertices of the fifth colour. A vacancy slide is the special case of a fifth-colour Kempe swap whose component is a single edge and whose fifth colour occurs once. The general theorem does not supply that restriction.

**Do not cite Florek's pole theorem as a belt theorem.** In arXiv:2511.00485, $G_n$ has two nonadjacent poles of degree $n$ and $2n$ vertices of degree 5. The full graph has at least $\lfloor n/6 \rfloor$ Kempe classes. Theorem 3.1 says that all 4-colourings of $H_n = G_n$ minus one pole are Kempe equivalent in at most $\lfloor 13n/2 \rfloor$ changes. For $n=8$ that is 52 changes with the hole fixed at the pole. Our hard starts delete a belt vertex. When a slide does move the hole onto the pole, the colouring of $H_8$ still has counts $(2,5,5,5)$, and Lemmas 2.2–2.3 force every full colouring of $G_8$ to have counts $(4,4,5,5)$. No continuation that only slides can finish it. Florek's path, if entered, is a long fixed-hole Kempe path on $H_n$, not the one star swap.

## The one potential that matches the known repair

Slides preserve the sorted colour counts on the coloured vertices. On $G_n$ with $n=3k+2$, the equal-pole star swap changes the partial counts

$$
(2,\, 2k+1,\, 2k+1,\, 2k+1)
$$

to

$$
(k+2,\, k+1,\, 2k+1,\, 2k+1),
$$

and filling the freed colour produces $(k+2, k+2, 2k+1, 2k+1)$. For $k=2$ that is $(2,5,5,5) \to (4,3,5,5)$ and then $(4,4,5,5)$.

On this family the target populations are not an appeal to the Four Colour Theorem. Florek enumerates the colourings of $G_n$. The potential is the $\ell_1$ distance from the sorted counts to that list. Slides do not change it, so they get no rewrite arrow. The star swap on $G_8$ takes $(5,5,5,2)$ to $(5,5,4,3)$ and the distance falls from 3 to 1; the fill reaches 0. Roots 9 and 14 both sit at $(4,4,4,4)$, and the slide between them is a symmetry of order 17 graph 0: the involution $(0\ 12)(1\ 11)(2\ 16)(3\ 13)(4\ 6)(7\ 10)(8\ 15)(9\ 14)$, fixing 5, carries one coloured map onto the other with the colours unpermuted. Every function of the coloured map is constant on that exchange, so no equivariant Lyapunov function can fall there. The same strict order gives the exchange no arrow. Newman's lemma does not apply, because the slide relation does not terminate. The note is `longtable/swarm/cross-rewriting.md`, and the Lyapunov kill is `longtable/swarm/cross-lyapunov.md`. It does not consult a pass/fail label.

Feasibility of this potential on the Florek family: **High**, because the star proof is already written and the census of full counts is in the paper.

Feasibility of the same potential on a general spherical triangulation: **Low**. There the list of full counts is the theorem.

## What to prove by hand, in this order

1. **The $A_\tau$ tile, the surviving $B$ orientation, and the opening cap are written. The statement is still a hand argument, not a compiled proof.** The $A_\tau$ tile returns a prepared zero one step along the belt. From a prepared zero, the gap $0,\rho,\tau,0$ repeats $\rho$ on $u_i u_{i+1}$ and is not a colouring. The gap $0,\tau,\rho,0$ has link $(1,\rho,\tau,\rho,0)$ and returns the prepared shape on the far zero by the slides $v_i\to u_i\to u_{i-1}\to v_{i-2}\to v_{i-3}$, for $n\ge 6$. The notes are `longtable/swarm/unequal-tile.md`, `unequal-b-tile.md`, and `unequal-cap.md`. The remaining case is the $A_\rho$ tile whose outer $u$-vertex has colour $\tau$. Do not enumerate $n=14$. The equal-pole orbit still needs the star. Counted belts remain $n=5$, $8$, and $11$.

2. **The long-arc identity is proved only with an extra chain hypothesis.** A long-arc vertex $x$ of colour $\beta$ meets exactly one degree-5 neighbour $s$ of colour $\alpha$. If the $\alpha\beta$-chain through $x$ excludes the other degree-5 neighbour, and the slide through $x$ has one forward degree-5 landing whose colour is not $\alpha$, then the two-step vacancy and the swap-then-slide differ exactly on that chain with $s$ removed. This holds on all eight long-arc vertices of the four locked orbits. The locked link alone does not force the split: the same link on order 17 root 4 has an interior colouring whose chain contains both degree-5 neighbours. The short arc stays outside because it meets both of them. The note is `longtable/swarm/long-arc-lemma.md`.

3. **One Kempe swap is not enough on the 21-vertex hole. A two-swap mixed budget is not killed there.** Correction, 5 October: two swaps and the slide from vertex 1 to vertex 6 fill the colouring. The graph has 57 edges and 38 faces. The rest of this paragraph is the fixed-hole count. A 21-vertex minimum-degree-5 triangulation has a frozen hole at vertex 1, link colours $(0,2,3,0,1,2,0,3,1)$, population $(4,5,5,6)$. All 16 Kempe swaps stay frozen. Of 224 ordered pairs, 172 leave the link frozen with multiplicity $(3,2,2,2)$. The published escape is one of the other 52. The 24 pairs that return to the original colouring are 2-cycles on a set of 21 frozen colourings, and the same first swap still leaves that set. On the 84 pairs whose third swap leaves a four-colour link, all 352 images then fill by slides alone. This colouring does not need a fourth Kempe swap. A different graph still might. Six of the sixteen one-step swaps are frozen by the coloured link: every pair containing colour 0 keeps multiplicity $(3,2,2,2)$. The other ten depend on the interior. Recolouring one interior vertex of this triangulation unlocks each of them. The note is `longtable/swarm/frozen-link-reasons.md`. No multiplicity pattern forces an unlocking swap: every pattern has a planar extension that stays frozen. The alternating word $(0,1,2,3,0,1,2,3)$ does force a unique colour, and another colouring of the same counts $(2,2,2,2)$ does not. The note is `longtable/swarm/frozen-patterns.md`. Orders 12 through 20 still unlock with one swap. The notes are `longtable/swarm/two-kempe-kill.md`, `two-swap-branches.md`, and `return-pairs.md`. Do not search $G_8$ for this kill.

## Feasibility

Reading the traps as root-changing escapes on the 21 published orbits: **High**.

An all-roots theorem by slides alone: **killed** on the 9–14 exchange and on the population obstruction.

The one-Kempe hybrid on the Florek family: **High** for equal poles. On $G_5$ and $G_8$, unequal poles do not need the Kempe swap at all. That is not yet a proof for every $n$, and it is not Theorem 3.1.

A polynomial rank on a general spherical triangulation built by fitting another feature to $q$: **Low**.

Filling a hole after it has moved does not plug into the compiled contact theorems. Those theorems choose one degree-5 root and only then allow `TwoSwapMacro` paths on that same deletion. A different induction does close, if the vacancy hypothesis is granted with no bound on the number of moves. Colour a smaller triangulation made by deleting one degree-5 vertex and adding two non-crossing chords, restrict, and apply the hypothesis once to the original graph. Orders through 11 never use the hypothesis: they have a vertex of degree at most 4. The note is `longtable/swarm/hole-induction.md`. Feasibility of that deduction, given the hypothesis: **High**. Feasibility of the hypothesis itself: untouched, and already false for a budget of one or two Kempe swaps.

On the icosahedron, the first order that uses the hypothesis, every fan colouring reaches a three-colour link in one Kempe swap. Two of the eight orbits at a fan are already three-colour links. Of the other six, three also fill by one slide, and three still show four colours after every slide from the deleted vertex. Slides alone take two steps on those three. At the fixed vertex, all 20 deletion orbits have Kempe distance at most 1. The count agrees at all twelve vertices. The note is `longtable/swarm/icosahedron-fan.md`. Feasibility of this count: **High**. It is not a bound for a later triangulation.

A fan-proper 5-cycle has two orbits. The word $(0,1,0,1,2)$ already uses three colours. The word $(0,1,0,2,3)$ is reduced by one Kempe swap only when a $\{1,2\}$-path or a $\{1,3\}$-path fails to join the link. On the gyroelongated hexagonal dipyramid with $U_0$ deleted, both paths are present and either swap leaves four colours. The note is `longtable/swarm/fan-link.md`. Feasibility of a forced one-swap lemma: **Low**.

The paper-by-paper reading is in `PaperReading.md`. Florek's Theorem 3.1 is a pole deletion, Fisk and Mohar need even degrees or $\chi < 4$, and single-vertex recolouring can freeze where full Kempe changes do not. None of them is the unequal-pole belt argument.

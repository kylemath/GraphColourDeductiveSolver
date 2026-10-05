# Night handoff

4 October 2026, about 21:30. Written while the other teams were stopped. Nothing here is marked proved in the navigator unless a Lean audit already said so. The equal-pole star, the unequal-pole tiles, and the induction are hand arguments. The icosahedron fan count is a computation on one graph.

The navigator is at revision 75. Math's evening is recorded below. The vacancy hypothesis stays open.

## Morning, 5 October

Math accepted the WP11 validation replay: 1,307 tables, 259 existential survivors, 38 good at every order-19–20 root. Finite only.

WP18's census of 961 graphs is accepted: fan-selection length 3 only on order 17 graph 1, at most 2 on the others, and every start within 4 moves. That is not a universal bound.

WP19 finished through order 24. Order 24 graph 6406 has length 3 at every fan and two degree-7 vertices, so both "length at most 2 from order 18 on" and "length at least 3 only when every degree is 5 or 6" are killed. Order 24 graph 7228 has one start of mixed distance 3 and Kempe distance 5, so "Kempe distance is at most one more than mixed distance" is killed. Passes of the other statements on these graphs are not theorems.

If a colouring fills in at most two mixed moves, the same number of Kempe swaps fills it at the original hole. That is an accepted hand theorem, not a Lean proof, and it does not bound longer paths.

The joined belt argument is an accepted hand proof for Florek's two-pole graphs. Unequal poles fill by slides. The pole-hole case with no unique colour still cites Florek's Theorem 3.1. It is not compiled.

WP12 stays withdrawn. No further phase is released.

## What the proof hangs on

The compiled contact theorems choose one degree-5 root and then allow two-swap macros on that same deletion. A slide moves the hole, so it does not plug into those theorems.

A different induction does close, if one hypothesis is granted with no bound on the number of moves. Delete a degree-5 vertex, add two non-crossing chords, colour the smaller triangulation, restrict, and apply the hypothesis once to the original graph. Through order 11 every spherical triangulation has a vertex of degree at most 4, so those orders never use the hypothesis. A later hole, even of degree greater than 5, is a state of that one application. The note is `longtable/swarm/hole-induction.md`.

The hypothesis is open. A budget of one Kempe swap, and a budget of two, are already too small.

## Progress

**Equal-pole star.** On the two-pole belt \(G_n\) with \(n=3k+2\), if the poles share a colour, one Kempe swap on the other pole's star fills a belt vacancy, for every such \(n\). On \(G_8\) that is \((2,5,5,5)\to(4,4,5,5)\). On that one colouring, the only subset shifts that fill the hole are the four stars and their complements. Hand argument, not compiled. `TwoPoleStarEscape.md`, `swarm/cross-flows.md`.

**Unequal poles.** Slides alone fill every unequal colouring of \(G_5-u_0\), \(G_8-u_0\), and \(G_{11}-u_0\): 19, 121, and 807 orbits, longest walks 4, 4, and 6. The \(A_\tau\) tile returns a prepared zero one step along the belt. The opening cap fills in at most two slides. Of the two length-2 gaps, \(0,\rho,\tau,0\) repeats a colour on \(u_i u_{i+1}\) and is not a colouring; \(0,\tau,\rho,0\) returns a prepared zero in four slides, \(v_i\to u_i\to u_{i-1}\to v_{i-2}\to v_{i-3}\), for \(n\ge 6\). The \(A_\rho\) tile whose outer \(u\)-vertex has colour \(\tau\) is still unnamed as slides. Not a proof for every \(n\), and not compiled. `swarm/unequal-general.md`, `unequal-tile.md`, `unequal-b-tile.md`, `unequal-cap.md`.

**The 21 published mass traps.** Each has a vacancy path of length at most 2 onto a mass-passing root, except that roots 9 and 14 on order 17 graph 0 exchange stuck orbits. That exchange is a symmetry of the graph, the involution \((0\ 12)(1\ 11)(2\ 16)(3\ 13)(4\ 6)(7\ 10)(8\ 15)(9\ 14)\) fixing 5, so every invariant is constant there. Order-17 traps have colour counts \((4,4,4,4)\). Order-20 traps have \((4,5,5,5)\).

**Long-arc identity.** On a locked degree-5 hole, if the chain through a long-arc singleton excludes the other degree-5 neighbour and the forward landing is not the repeated colour, the two-step slide and the Kempe-prepared slide differ exactly on that chain with the neighbour removed. This holds on all eight long-arc vertices of the four locked orbits. The locked link alone does not force the split. `swarm/long-arc-lemma.md`.

**Ion path on order 17 graph 3.** A neutral swap, then an ion swap, pulls \((4,4,4,4)\) to \((3,4,4,5)\), and one further swap fills. All ten stuck colourings do this. Along the way \(q\) goes 107, then 138, then 128, then 116, so \(q\) is not the descent. The locked roots 4 and 6 create no ion in one swap. `IonicCharge.md`.

**The 21-vertex hole does not need a fourth swap.** Link \((0,2,3,0,1,2,0,3,1)\) at vertex 1. All 16 one-step swaps stay frozen. Of 224 pairs, 172 stay frozen. The 24 that return to the original colouring are 2-cycles, and the same first swap still creates a unique colour. The other 84 form 27 colour-renaming orbits; after the third swap, slides alone reach a three-colour link. Largest component 818 states, longest fill 7 slides, at degree 5 or 6. `swarm/two-swap-branches.md`, `return-pairs.md`, `third-swap-slides.md`.

## Dead ends

Slides alone cannot finish a colouring. They preserve sorted colour counts. On \(G_8\), \((2,5,5,5)\) is not a full colouring.

Slides alone are not a theorem, and one Kempe swap is not enough on the 21-vertex hole: every one-step swap stays frozen. Two named swaps and the slide from vertex 1 to vertex 6 fill that colouring, so a two-swap mixed budget is not killed. The graph has 57 edges and 38 faces. The agreed sentence remains: this colouring does not need a fourth swap, and a different graph still might.

Fitted ranks die. \(q\), \((p,q)\), \((n_5,q)\), \((d_{\min},q)\), \(\mathrm{repMass}\), \((L,q)\), and \(\mathrm{lin}\) fail on the 21 traps. \((\mathrm{shortLinks},q)\) and \((H,q)\) pass the 21 and stop on the next colouring of order 17 graph 3. The distance to Florek's list of full counts falls on the star swap and is blind on \((4,4,4,4)\).

No multiplicity pattern of a frozen link forces an unlocking swap. Every pattern has a planar extension that stays frozen. Six of the sixteen swaps on the degree-9 link are frozen by the link itself; the other ten depend on the interior. `swarm/frozen-patterns.md`, `frozen-link-reasons.md`.

Height functions, sandpiles, nowhere-zero flows, and monodromy do not give a new move. The monodromy of the exhibit pentagon link \((0,1,0,2,3)\) is the identity. The 15-vertex pentagon star has a colouring in which no second slide reaches a useful pentagon, so the 32- and 42-vertex graphs are not the next search.

Fisk, Mohar, and Meyniel do not apply. The graphs have odd degrees, or the theorems allow many vertices of a fifth colour. Florek's Theorem 3.1 (arXiv:2511.00485) moves a hole that is already a pole, in at most 36 Kempe changes when \(n=8\). `PaperReading.md`.

## Still open

The unequal-pole statement for every \(n\). The \(B\) step is written. What remains is the \(A_\rho\) tile whose outer \(u\)-vertex has colour \(\tau\): the antiprism note names it as a return and does not give the slides. Feasibility of the \(B\) step: **High**. Feasibility of the whole statement: **Medium**. Do not enumerate \(n=14\).

The vacancy hypothesis itself, with no bound on the number of moves. The induction says what follows if it is true. Feasibility of the deduction: **High**. Feasibility of the hypothesis: open.

Whether that hypothesis is only needed for colourings that extend across a fan of two chords. A degree-5 link cannot be frozen, because four colours each used twice need eight positions. On the 21-vertex graph the frozen hole is at degree-9 vertex 1, so it is a later state. At degree-5 vertex 0, all five legal fans were coloured in full, and none of those colourings restricts to a frozen link. The note is `longtable/swarm/fan-versus-frozen.md`. The induction's starting colourings are a different set from the frozen hole.

On the icosahedron, which is the first order that uses the hypothesis, those starting colourings do fill. Each fan admits 8 colourings up to renaming. Two already have a three-colour link. The other six each fall to three colours by one Kempe swap. Three of those six also fall by one slide. The other three still have four colours after every slide from the deleted vertex, and slides alone take two steps. At the fixed vertex, all 20 deletion orbits have Kempe distance at most 1 to a three-colour link. The same fan count holds at all twelve vertices, and the failing list is empty. The note is `longtable/swarm/icosahedron-fan.md`.

Up to dihedral symmetry and renaming colours, a fan-proper 5-cycle has two orbits. The word \((0,1,0,1,2)\) already uses three colours. The word \((0,1,0,2,3)\) is proper on three of the five fans, and one Kempe swap reduces it only when the \(\{1,2\}\)-path or the \(\{1,3\}\)-path fails to join the link. Neither failure is forced. On the gyroelongated hexagonal dipyramid, fourteen vertices, minimum degree 5, deleting \(U_0\) leaves the link \((U_1,N,U_5,L_0,L_1)\) coloured \((0,1,0,2,3)\), and both paths are present. Swapping either component leaves four colours. The colouring is proper on the thirty-one edges of the deletion. The note is `longtable/swarm/fan-link.md`. Feasibility that one Kempe swap is forced on every fan-proper link: **Low**.

## Retreat, 5 October

The decisions below are for the math team and the long-table team. Each one has a proposed answer. The night's kills are in the sections above and do not need to be reopened.

1. **Which proof is tomorrow's proof.** The compiled contact theorems keep one degree-5 root fixed. The vacancy induction moves the hole, and it closes only if the hypothesis is granted. Long Table's proposed statement is existential: some degree-5 vertex and some legal fan, not every fan. Every proper colouring of an induced 5-cycle is proper on at least one fan, so a universal fan restriction would not narrow the colourings. On the 14-vertex dipyramid the link \((0,1,0,2,3)\) has mixed distance exactly 2: no single swap fills, and 36 two-move sequences do. That is one start, not the minimum over fans. The contact gate stays as it stands. Feasibility of a forced one-swap lemma: **Low**. Feasibility of proving the unrestricted hypothesis tomorrow: **Low**.

2. **The last unequal-pole tile.** \(A_\tau\), the surviving \(B\) orientation, and the cap are written. The unnamed case is the \(A_\rho\) tile whose outer \(u\)-vertex has colour \(\tau\). Proposed answer: one person writes that case in the morning, to the same standard as `unequal-b-tile.md`. Do not enumerate \(n=14\) before that page exists. Do not send the belt argument to Lean until the case is closed. Feasibility of the remaining case: **Medium-High**. Feasibility of the statement for every \(n\), once it is written: **Medium**.

3. **What the icosahedron count is allowed to mean.** It says that every fan colouring on the 12-vertex graph reaches a three-colour link in one mixed move. Order 14 now has one start of length 2. The minimum over fans on that graph is open, and that is the question in the unreleased WP18 declaration. Do not colour the 32-vertex or 42-vertex graphs for this question.

4. **The 21-vertex hole is an exhibit, not a budget.** The agreed sentence is: this colouring does not need a fourth swap, and a different graph still might. A page for this graph, or for the two-pole belt \(G_8\), can wait. The dead-end page already draws order 17 graph 3.

5. **What stays stopped.** Discovery replay has passed. The producer validation on orders 19–20 is published and is not accepted until an independent replay. WP12's release request is withdrawn. WP18 has not been released. Ranks, height, sandpiles, flows, and monodromy stay closed. The pole-degree-12 log and the unfinished order-21 split are not kills. Uncommitted night outputs through order 26 are not evidence.

## Where to read

| Topic | File |
|---|---|
| This handoff | `SolvingFrameworkPlan/docs/working/NightHandoff.md` |
| What not to compute | `SolvingFrameworkPlan/docs/working/LibraryPlan.md` |
| Papers | `SolvingFrameworkPlan/docs/working/PaperReading.md` |
| Induction | `longtable/swarm/hole-induction.md` |
| Equal-pole star | `SolvingFrameworkPlan/docs/reports/TwoPoleStarEscape.md` |
| Icosahedron fans | `longtable/swarm/icosahedron-fan.md` |
| Fan-proper links | `longtable/swarm/fan-link.md` |
| Navigator | `docs/navigator/`, revision 75 |

# Vacancy slides out of the mass traps

4 October 2026. Speculative inquiry. The facts below were recomputed from the published mass-macro table by `backgroundMaterial/planemap-structural/longtable/inquiry_slide.py`. They are not a navigator status, not a release, and not a colouring search on any graph past the published failures.

## The move

Fix a degree-five root $r$ and a proper four-colouring of $T-r$. A boundary vertex $x$ whose colour appears once on $N(r)$ may take the vacancy: colour $r$ with the colour of $x$, and delete $x$ instead. The result is a proper colouring of $T-x$. The slide is reversible, so it is not a rank by itself.

On a triangulation the link of $r$ is a 5-cycle. A non-target colouring uses all four colours, hence the pattern $2,1,1,1$. The repeated colour cannot sit on an edge, so its two vertices are at cycle distance 2. That is the only proper pattern. All 940 non-target orbits at the twelve mass-failing roots have this shape.

## What the twenty-one traps do

The six graphs that contain a mass failure have 21 two-swap-stuck orbits, all of them at failing roots. None of those colourings has a hub toggle: there is no 2-vertex bichromatic component with one end off the boundary. The toggle is a gate elsewhere in the basin, not the pit itself.

Two species:

- **Locked, 4 orbits.** Order 17 graph 0 roots 4 and 6, and order 20 graph 7 roots 7 and 11. Every degree-five neighbour carries the repeated colour, so no slide stays on a degree-five vertex. One Kempe swap creates such a slide, and it lands on a mass-passing root. With no Kempe swap at all, each of the three singleton slides goes out through a degree-six or degree-seven vertex and then on to a passing root.
- **Open, 17 orbits.** A degree-five singleton slide is already available.

In all 21 orbits, some vacancy path of length at most 2 ends at a colouring of a mass-passing root which still has four colours on the boundary and which the mass machine at that root can lower. The slide does not finish the colouring. It moves the unfinished colouring onto a root where the existing two-swap machine is not stuck.

The only direct slide from a trap onto another trap is the pair at order 17 graph 0, roots 9 and 14. Each stuck orbit slides onto the other's stuck orbit. Each also has a two-step slide, through a degree-six vertex, onto a passing root. The twin exchange is real, and it is not a prison.

## The regime the corpus never sees

Neighbour-degree type does not decide the mass outcome. Type $(5,0,0)$ holds 5 of the 12 failures and 37 passes. Type $(2,3,0)$ holds the two locked failures on order 17 graph 0 and 231 passes. Type $(0,5,0)$, five degree-six neighbours, does not occur in the mass corpus.

Both symmetric graphs proposed for that type were built and checked only as geometry. No colourings were enumerated.

| Graph | Vertices | Degree-five vertices | Distances between them |
|---|---|---|---|
| Pentakis dodecahedron | 32 | 12, all type $(0,5,0)$ | 2, 3, 5 with 30, 30, 6 pairs |
| Frequency-2 icosahedron | 42 | 12, all type $(0,5,0)$ | 2, 4, 6 with 30, 30, 6 pairs |

The second row is the icosahedral distance doubled. The first row is not. In both graphs no two degree-five vertices are adjacent, so every singleton slide leaves the degree-five class, exactly as in the four locked traps. The thirty pairs at distance 2 are the bridges: one degree-six vertex between two pentagons. On the pentakis dodecahedron that bridge meets three pentagons, because it is the centre of an icosahedral face. On the frequency-2 icosahedron the bridge meets exactly two, the ends of one icosahedral edge.

## What this is not

A passing root already discharges these graphs under the existential mass hypothesis. The slides do not repair a graph on which every degree-five root fails, because every escape found here lands on a passing root. They also do not show that the transported colouring is a target in one step. They show that the published mass machine, started at the landing, can keep lowering the rank.

Feasibility of reading the known traps this way: **High**, as a description of these 21 orbits.

Feasibility of an all-roots theorem by vacancy slides: **Medium-Low**. The twin pair shows that a slide can preserve a trap. The way out used a root that was already good.

Feasibility that the isolated pentagon is the same shape as the locked trap, and therefore a two-step problem rather than a new local invariant: **Medium-Low**, and speculative. It is a reason to expect the bridge move. It is not evidence that $q$ survives there.

## Next steps

1. Treat the vacancy slide as a legal move in its own right and name a rank on the pair $(\text{root}, \text{colouring})$ that falls on the escapes above and does not cycle on the 9–14 exchange.
2. Keep the four locked orbits as the test: the rank should fall either on the Kempe preparation or on the two-step through the degree-six vertex, and the two routes should be compared rather than averaged.
3. Leave the order-32 and order-42 graphs uncoloured until that rank exists and a run is released. Their distance tables are the part worth having now.

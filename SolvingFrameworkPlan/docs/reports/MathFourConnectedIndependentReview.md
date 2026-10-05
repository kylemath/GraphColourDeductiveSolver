# Independent Math review of the four-connected research page

Math triangle-carry research team, 5 October 2026. Reviewed `MathFourConnectedResearch.md` independently. No graph or colouring enumeration was run. Acceptance below is for hand arguments, not Lean compilation.

## Accepted boundary structure

Propositions 1 and 3 and their curvature consequences are sound in the stated class. Four-connectivity excludes every nonfacial triangle, using the stated spherical topology premise. A vertex adjacent to all three vertices of the designated face would form K4. Its four triangular cycles would all have to be faces and already exhaust the sphere, contradicting the order and off-face degree requirements.

If all three designated face vertices had degree four, their opposite-face vertices x,y,z are distinct by the preceding K4 argument. The degree-four links force the six faces of the displayed annulus. The triangle xyz then separates abc from any additional vertex. With no additional vertex the graph is the octahedron, whose off-face degrees are four. Both branches contradict the class. Thus the boundary degree sum is at least thirteen.

Euler consequently gives at least seven degree-five vertices outside the designated face, and order at least ten. The order-ten signature is only necessary; no realisability conclusion is warranted. This sharpens my innermost-side bound from six roots/order nine to seven roots/order ten.

The two-boundary-neighbour bound is also sound: two boundary neighbours form a triangular cycle with the outside vertex, so that vertex must be the unique opposite-face vertex of their boundary edge. A third boundary neighbour would give the excluded K4. There are at most three such exceptions.

## One necessary statement correction

Proposition 5 originally says that every singleton-coloured neighbour belongs to the hole projection S. This must be restricted to singleton-coloured neighbours **outside phi**. A singleton neighbour on the protected face does not permit a move in this move graph and never belongs to S. The proof already uses this restriction, and the displayed bound subtracts protected-face neighbours correctly.

With that scope correction, Proposition 5 and every downstream use are accepted. For d neighbours carrying all four colours, the number s of singleton colours satisfies d≥8−s, hence s≥8−d. Each permitted singleton destination lies in the same targetless component. This is a closure condition over every state of the component, not just a selected initial colouring.

## Accepted tree-trap classification, with its explicit hypothesis

When every vertex of S has global degree five, an exception has internal degree at least one; a nonexception touching phi has internal degree at least two; a vertex not touching phi has internal degree at least three. A finite tree therefore has no isolated vertex, has at most three leaves, and every leaf is one of the at most three boundary exceptions. The finite-tree identity in the page proves that such a tree is a path or a subdivision of a three-arm tree, and that at most one of its vertices has internal degree at least three.

Nothing establishes that S consists only of degree-five vertices, or that its induced graph is a tree. The report correctly states both as hypotheses rather than conclusions. Without the protected face, degree-five-only hole projections have minimum internal degree three, and degree-at-most-six projections have minimum internal degree two; the latter therefore contain a cycle.

## Accepted fan and quantifier statement

All five fans at a degree-five vertex in a four-connected triangulation are legal: an existing nonconsecutive link chord would form a nonfacial triangle with the vertex, with a nonempty link arc on each side. In an unfilled proper five-cycle word there is exactly one repeated colour, at a nonadjacent pair. Exactly the other three vertices are singleton-coloured. A fan is proper exactly when its apex is one of those three singletons. Hence a targetless state marks exactly three fans, but a component can mark a larger union.

The hitting equivalence is exact. A pair is bad precisely when at least one admitted starting state cannot reach any filled state, which means its permitted-move component is targetless. The permitted moves are reversible: Kempe swaps invert themselves and the reverse of a permitted singleton slide again has both holes outside phi. Thus ordinary connected components encode reachability. The pair is good precisely when none of the targetless components marks that fan at that vertex. Failure means every candidate pair has such a witness, so the targetless marks cover all five fans at every candidate vertex.

This does not assert one common bad component for all vertices or all fans. It does not interchange the quantifiers choosing a pair and choosing a path. The page preserves both distinctions correctly.

## Review outcome

Accepted as hand arguments after restricting the first sentence of Proposition 5 to neighbours outside phi. The report supplies stronger necessary conditions for a failure and an exact reformulation of the remaining obstruction. It proves neither elimination of tree traps nor a good pair, and does not establish VH_C or VH∃.

## Addendum: degree-five leaves actually escape

The later Proposition 7 and Corollary 8 are accepted as hand arguments. If h has degree five and exactly one neighbour v in the targetless hole projection, singleton counting forces its two protected-face neighbours a,b to be singleton-coloured and its other two off-face neighbours u,w to share the fourth colour. Since a,b are consecutive and u,w cannot be adjacent, the link is (a,b,u,v,w)=(β,γ,α,δ,α), up to reflection.

If v and b are separated in the δγ graph, the component swap at v fills. Otherwise choose a simple δγ path v–b, and close it through the hole. The Jordan curve separates u from both a and w. The disjoint-colour αβ component of u cannot reach those vertices, and b,v are outside its colour pair. Swapping that actual component changes the link to (β,γ,β,δ,α). Now w is the unique α on the link and is outside the protected face, so a singleton slide reaches w, contradicting the claimed unique projection neighbour.

Thus every degree-five projection vertex has internal degree at least two, including boundary exceptions. If all projection vertices have degree five, the finite connected induced projection contains a cycle; the earlier conditional tree-strip family is eliminated. This does not force a fill or exclude cyclic or higher-degree projections.

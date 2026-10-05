# Cyclic trap research: degree-five holes reach every neighbour

Math, four-connected research team, 5 October 2026. **[hand arguments for independent review]**. No census or graph generation. Earlier reports are frozen; this new page strengthens their targetless-projection conclusions. The protected-face condition restricts holes, not Kempe swaps or boundary colours.

## 1. A local mobility alternative

**Theorem 1.** Let h have degree five in a finite simple spherical triangulation T, and let c be a proper four-colouring of T−h. Then either the hole fills using at most one Kempe swap, or every neighbour u of h can be reached as the hole using at most one Kempe swap followed by one singleton slide. In the latter assertion, moving to an already-singleton neighbour needs only the slide.

More generally, with a set Z of forbidden hole vertices and h outside Z, every neighbour u outside Z can be reached by such a permitted path. Kempe swaps may meet and recolour Z. No degree assumption on u or any other vertex is required.

**Proof.** If the link uses at most three colours, it already fills. Otherwise rotate and rename its four-colour word as

    (a0,b,a2,g,d) = (alpha,beta,alpha,gamma,delta).

The two repeated alpha vertices are nonadjacent; the three other neighbours are singleton and immediately reachable. If there is no beta/gamma path from b to g, swap b's beta/gamma component; it avoids g and eliminates the unique beta on the link, filling h. The same applies if there is no beta/delta path from b to d. Thus if the first alternative fails, both paths exist.

Take a simple beta/delta path Q from b to d and close it through h with hb and hd. The Jordan curve separates a0 from both a2 and g, by the link order. The alpha/gamma component K of a0 is disjoint from Q, whose colours are beta,delta; it also avoids h, which is deleted. Therefore K misses a2 and g. It misses b,d because their colours are outside its pair. Swapping K changes exactly a0 on the link, producing

    (gamma,beta,alpha,gamma,delta).

Now a2 carries the unique alpha on the link, so the slide h→a2 is legal.

Symmetrically close a simple beta/gamma path P from b to g through h. It separates a2 from both a0 and d. Swap the alpha/delta component of a2; it changes exactly a2 on the link and makes a0 the unique alpha. Then slide h→a0.

Each construction starts from the original state and reaches the chosen repeated-colour neighbour in two moves. The only holes are h and that chosen neighbour, so forbidding Z does not interfere when both lie outside Z. Recolouring Z is permitted. ∎

This is an accessibility theorem, not a fill-length bound. It guarantees a short path to an arbitrarily chosen adjacent hole when a one-swap fill is unavailable; it does not guarantee that hole can be filled.

## 2. Exact closure of a targetless projection at degree five

Fix Creative's face-avoiding class and the permitted move graph with holes forbidden on phi. Let C be a targetless component and S its hole projection.

**Corollary 2.** If h belongs to S and deg_T(h)=5, then

    N_T(h) minus V(phi) is contained in S.

**Proof.** Choose any state of C at h. A one-swap fill would contradict targetlessness. Theorem 1 therefore gives a permitted path to every off-face neighbour, and each destination belongs to the same component C. ∎

In the four-connected core an off-face vertex has at most two neighbours on phi. Consequently every degree-five h in S has internal degree at least three in T[S]. This immediately rules out degree-five vertices that lie on an otherwise degree-two projection cycle, even if some other projected vertices have larger global degree.

Unlike the earlier singleton count, this closure includes every off-face neighbour even when its colour repeats. It applies after every state change in the component. Protected boundary colours may change along the path.

**Corollary 3.** Let W be a connected component of the graph induced by off-face vertices whose global degree is five. If a targetless component has one hole in W, its hole projection contains all of W and every off-face neighbour of W, including neighbours of larger degree.

**Proof.** Propagate Corollary 2 along paths in W, then apply it to each vertex of W. ∎

Hence higher-degree holes cannot be dismissed from a bad component touching a degree-five region: every off-face higher-degree neighbour of that region is reachable. This conclusion does not apply VH∃ to a same-order higher-degree deletion; it only constructs actual moves.

## 3. Purely degree-five traps are global, not local cycles

Suppose every vertex in S has global degree five. Then Corollary 2 shows S has no edge to an off-face vertex outside S. In the four-connected core, T−V(phi) is connected: deleting a facial triangle is not a three-cut by the accepted three-cut core. Therefore

    S = V(T) minus V(phi),

and every off-face vertex has global degree five.

Let m be the number of off-face vertices and D the sum of the three face degrees. Euler's degree identity gives

    5m + D = 6(m+3)−12 = 6m+6,

so D=m+6. The number of edges between phi and the off-face vertices is D−6=m, because each face vertex has two neighbours on phi. The sum of degrees in the induced off-face graph is therefore 5m−m=4m, and that graph has exactly 2m edges and average degree four.

**Corollary 4.** A targetless component whose holes all have degree five cannot have a cyclic hole projection of internal degree two. Its projection must cover every off-face vertex, has average internal degree four, and has minimum internal degree at least three and contains a vertex of internal degree at least four.

This rules out both simple-cycle traps and the previously excluded trees, without selecting a chordless cycle or assuming a uniform move budget. A chordless cycle may still occur as a subgraph of the projection; it cannot be the whole degree-five-only projection. Branching alone does not force a fill.

## 4. Relation to fan coverage and what remains

At every degree-five root outside phi in the four-connected core, all five fans are legal. A targetless state marks the three fans based at singleton neighbours. The mobility theorem expands the hole projection of that component, but it does not automatically transport an arbitrary chosen fan mark to the next hole: the colouring and the fan-admission condition at the new root must be checked there. Thus one cannot infer that a single bad component covers every fan at every reachable root.

The new concrete obstruction is sharper:

- A bad component touching a degree-five region must reach the entire region and all its off-face neighbours.
- If it stays exclusively at degree-five holes, it covers the whole off-face graph, with unavoidable branching and average internal degree four.
- Otherwise it reaches a higher-degree hole, where the five-cycle mobility argument no longer applies.

A general proof still needs either an escape-to-fill mechanism at this higher-degree frontier or a global argument excluding the all-off-face targetless component. No such mechanism is proved here. In particular connected hole projection is weaker than a component containing a fill; there may be many colour states over each projected vertex.

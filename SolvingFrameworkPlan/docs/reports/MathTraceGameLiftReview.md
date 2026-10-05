# Math review: trace-game lift with pair-specific virtual connections

Math triangle-carry research team, 5 October 2026. Reviewed Creative's `interface/trace-game-reduction.md`. No new computation, corpus replay, graph generation, or sampling was performed. The earlier saved free-game certificate remains a separate checked finite result.

## Review outcome

**[hand] The trace-game triangle and induced-four-cycle lifts are valid after the virtual-network correction proved below.** The literal ordinary-edge construction in §2(a) is not valid. Its frozen-pair fact and its game rules are correct. This review supplies a repaired composition proof rather than treating the erroneous construction as accepted.

The game and least-failure reduction remain conditional on the universal trace-game hypothesis. Neither this review nor the corrected lift proves that hypothesis. No acceptance is given here to the new exploratory corpus counts or the trace-game computation on its saved member; they were outside this review's scope.

## Two defects in the literal virtual-edge construction

An admissible bit assignment need not admit its diagonal connections as noncrossing ordinary edges.

For boundary word (α,β,α,β), set the αδ bit on diagonal 0 and the βδ bit on diagonal 1, with δ unused on the boundary. These pairs share δ, so admissibility permits both bits. Their two straight topological diagonal edges have alternating endpoints and must cross. They must instead be represented by paths meeting at a δ-coloured interior vertex.

Also a virtual edge with same-coloured ends does not remember which colour pair requested it. For the same word, set only the αδ bit on diagonal 0 and leave the αε bit unset, where ε is the other unused colour. An ordinary edge joining its two α ends would also appear in the αε induced graph and falsely supply the unset connection. It is not a proper-coloured edge either.

Thus a single ordinary-edge graph B* cannot be used as stated. The repaired definition uses a family of pair-specific augmented graphs.

## Correct augmented graphs

For each colour pair P, form H_P from the actual G vertices coloured in P and their actual induced edges. If P is relevant at the protected quadrilateral phi and its bit is set, add an abstract connection between its two opposite active boundary vertices. This connection belongs only to H_P. If the protected face is triangular, add nothing.

Define B_P similarly using only the closed exterior side B. For P relevant on the separating quadrilateral Q, its induced Q-bit is set precisely when the two active Q vertices are connected in B_P. Since they are the only active Q vertices, a simple connecting path has all internal actual vertices off Q. Abstract connections may be expanded through a snapshot gadget as below.

A component of H_P is exactly an actual G P-component, possibly joined to the one other actual component touching phi. There are at most two such boundary-touching components. Therefore the trace game's chosen swap is exactly the restriction to actual G vertices of a component swap in H_P. A set bit whose endpoints already belong to the same actual component simply adds a redundant connection.

## Proper planar snapshot gadgets realise every admissible assignment

The following constructions occur solely inside the designated facial quadrilateral. They are proof gadgets, not asserted members of the minimum-degree-five class. Their added vertices may have degree two or four. All colours are the current position's colours.

**Four boundary colours.** The two relevant pairs are the disjoint colour pairs at the two diagonals, so at most one bit is set. Realise it by its one proper-coloured diagonal edge. Realise no bits by adding nothing.

**Three boundary colours.** Write the cyclic word as (α,β,α,γ), with δ unused. The relevant pairs are αδ on diagonal 0 and βγ on diagonal 1, and they cannot both be set. Realise αδ by a length-two path through a new δ vertex. Realise βγ by a direct proper-coloured diagonal edge. Again the empty assignment adds nothing.

**Two boundary colours.** Write the word as (α,β,α,β), with unused colours δ,ε. The four relevant bits form a 2×2 matrix: rows are diagonals; columns are the unused colours. Admissibility excludes two bits on different rows and different columns. Its nine possibilities are:

- empty;
- one set bit;
- both bits in one row;
- both bits in one column.

A single bit is a length-two path through a vertex of its unused colour. Both bits in one row are two parallel length-two paths with differently coloured interior vertices; they can be drawn without crossing. Both bits in one column are a star through one interior vertex of that column's unused colour, adjacent to all four boundary vertices. All star edges are properly coloured.

In every construction, the resulting coloured planar network realises exactly the requested relevant connections. For each pair not relevant on phi, any active boundary vertices already lie in one boundary component, so the gadget creates no new partition of its boundary vertices. Inspection of the constructions shows that paths through the gadget induce precisely the pair-specific connections specified in H_P, and no unset relevant bit.

A separate gadget may be chosen for each position. This does not assume the adversary's entire history comes from one persistent far-side graph. Snapshot realisation is enough to establish admissibility of the induced Q-bits; dynamics will be checked directly in the pair-specific graphs.

## Admissibility and matching components

Glue the current snapshot gadget into phi on B's side. This is a properly coloured planar disk network. Two set Q-bits at different Q diagonals with disjoint colour pairs would give vertex-disjoint paths joining alternating boundary vertices of that disk. Their colour sets being disjoint forbids a common vertex, and Jordan separation forbids the paths. Hence the induced Q-bit assignment is admissible.

Fix an A P-component K selected by the side strategy. Seed the G player's move at any actual vertex of K. It selects the actual G P-component containing that seed, together with its phi partner when the trace rule requires it; equivalently it swaps the actual vertices of the corresponding H_P component.

The intersection of that component with A is K alone or K together with the one other A-component meeting Q. Exterior excursions in H_P are represented by B_P paths. When a second boundary-touching A-component exists, the union occurs exactly when the induced Q-bit is set. If K misses Q, no exterior excursion or merge can reach it. If the relevant Q vertices already lie in one A-component, a set Q-bit changes nothing. Thus the actual G move restricts to exactly the move prescribed by the A trace-game rule, including its deterministic merge.

An interior singleton slide has identical source neighbourhood in A and G. Its source and destination are off Q, so it is legal in both and leaves B's actual colours unchanged.

## Frozen dynamics without a persistent gadget

Under a swap in P, the actual vertices coloured in P remain the same, as do the vertices coloured in its complement. Their induced actual graphs are unchanged. The trace rules keep the phi bits of P and its complement; their relevance and active boundary endpoints are also unchanged. Therefore B_P and B_complement are unchanged as pair-specific connectivity graphs, even when the game's adversary changes the other bits.

Consequently the induced Q bits of P and its complement are unchanged, exactly as required by the A game. All other induced Q bits are admissible by the current snapshot argument, so their new values are among the outcomes allowed to A's adversary. For an interior slide, both the B colours and all phi bits stay unchanged, so every induced Q bit stays unchanged.

This argument does not rely on edges or interior colours of an arbitrarily rebuilt snapshot staying fixed. The relevant invariant is the specific B_P connectivity graph.

## Membership, fans, starts, and triangle cuts

The side A away from phi has all its inherited faces triangular except its facial Q. Its strict-interior vertices retain global neighbourhoods and have degree at least five. An induced separating Q therefore gives (A,Q) in the declared relative class, with fewer vertices.

A legal fan at a strict-interior degree-five root remains legal globally. Any additional global edge between two vertices of A would have to be drawn on B's side and have both ends on Q. Existing boundary edges are already in A, and opposite-end edges are excluded because Q is induced. Hence a chord absent in A cannot appear globally. Every global admitted start restricts to an admitted side start.

The side strategy sees the induced admissible bits and every subsequent induced update. It wins against all allowed updates, so it wins under these particular updates. Every hole stays strictly in A−Q, and the final neighbourhood agrees globally, so the fill lifts. This proves the corrected induced-four-cycle reduction.

For a triangular separator F, its active P vertices are already joined by an actual edge whenever there are two. Augmented exterior connections cannot merge two distinct F-touching A-components. An extra phi component therefore has empty additional restriction to A. The ordinary protected-triangle lift follows, with the same fan and neighbourhood checks.

Thus the least-failure consequence—no separating triangle and no separating induced four-cycle—is valid for the strengthened trace-game hypothesis, after the construction correction. It remains a consequence about this stronger class, not a proved assertion that an ordinary VH∃ minimal failure has either property.

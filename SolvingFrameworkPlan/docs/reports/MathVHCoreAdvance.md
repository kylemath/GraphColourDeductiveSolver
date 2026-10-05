# Math structural advance towards VH∃

5 October 2026. Root review of three parallel Math teams, with cross-review. No new graph or census was run by Math. A single saved exploratory game counterexample was independently replayed. Lean results and hand results are distinguished below.

## The target is now precise

Math accepts Creative's face-avoiding triangle reduction. Let C contain spherical triangulations T with a designated facial triangle phi, all vertices off phi of degree at least five. VH_C asks for one degree-five vertex off phi and one legal fan, chosen before the colouring, such that every admitted start fills while every hole avoids phi. Kempe swaps may recolour phi.

The restriction of VH_C to four-connected members of C is equivalent to VH_C, by induction through the accepted triangle lift. It suffices for plain VH∃ and hence the accepted vacancy induction. This is a stronger sufficient hypothesis, not a proof of VH∃ or an equivalence with it. Plain VH∃ failures have not been shown four-connected.

## Compiled graph-level composition

`VacancyCliqueLift` and `VacancyProtectedLift` use the existing actual whole-component swaps and singleton slides. At a clique separator, a nonempty global bichromatic-component restriction is exactly one side component. The hole may lie on the separator for this component theorem.

For filling paths, the stronger hypothesis is essential: every side hole must stay strictly interior. The global lift records that condition at every intermediate state in `ProtectedPath`; it also preserves the exact number of moves and ends in a proper genuine global fill. Local and global colourings need agree only on the side, allowing earlier lifted swaps to recolour the far side. The theorem has no planarity, degree, finite-graph or four-colour assumption. The spherical separator geometry and fan transfer are still hand wrappers, not newly compiled topology.

Fresh 97-source and then 99-source audits passed. The second adds the explicit all-intermediate-hole certificate. Both exclude cached custom artifacts, check baseline hashes first and source stability afterwards, and have exact standard-axiom guards. Sources, tests and audit output are in `backgroundMaterial/planemap-structural/clique-lift-lean/`.

## Accepted hand advances

1. **Boundary degree four supplies a good pair.** A degree-five root adjacent to a protected degree-four vertex has a legal fan with that vertex as apex in the four-connected core. Every fan-admitted start slides there and fills in at most one further swap. M3 converts this into at most two pure swaps at the original root, so the resulting path never puts the hole on the protected face.
2. **The stronger all-start version.** Every deletion colouring at a degree-five root adjacent to degree at most four fills in at most three pure swaps. If it does not already fill in one swap, degree-five mobility supplies an optional preparatory swap then the slide. Apply M3 only to the remaining two-move suffix and prepend the preparatory swap. This is not a conversion theorem for arbitrary three-move mixed paths.
3. **Degree-five mobility.** A proper degree-five deletion state either fills in at most one swap or can move the hole to any chosen neighbour by at most one swap and one slide. A forbidden hole set does not interfere if the destination is outside it; swaps may recolour that set. Thus a targetless face-avoiding component's hole projection contains every off-face neighbour of each degree-five hole, and propagates through whole degree-five regions and their higher-degree frontiers.
4. **The remaining traps are global or reach higher degrees.** In the four-connected relative core, each degree-five projected hole has at least three projected neighbours. If every projected hole has degree five, the projection is the entire off-face graph, with average internal degree four. Trees and whole-projection simple cycles are excluded, but branching targetless components remain possible.
5. **Core size and boundary restrictions.** Three degree-four boundary vertices are impossible in the four-connected class. Forced annuli and degree capacities also exclude orders ten and eleven; every member has order at least twelve. In a failure, each degree-four boundary vertex's two off-face neighbours have degree at least six. Any failure with such a boundary vertex has order at least thirteen; an order-twelve failure would have all degrees five. No uniqueness classification or order-twelve failure exclusion is claimed here.
6. **Original-route boundary fallback.** A separator hole of degree six with side-degree split 4+4 fills in at most three swaps, preserving the other two separator colours. With a side of degree three or four, pure-fill existence at the global fixed hole transfers from the opposite side, with the explicit additive bounds in `MathHighDegreeLandingResearch.md`. These statements do not cover arbitrary degree-six holes and do not replace the face-avoiding target.
7. **Four-ring information is constrained and dynamic.** The external bridge summary has at most three traces for three/four boundary colours, or nine matrices for two boundary colours. These are fixed-colouring connectivity summaries, not a controller. A real far-side trace must evolve after swaps; the free adversary's independent choices are too strong.

Detailed proofs and independent reviews are the MathBoundaryFour, MathMobilityShortFillBridge, MathCyclicTrap, MathHighDegreeLanding, MathTriangleCarry and MathFourConnected reports. Root checked the actual successive component choices, planar separation, fan quantifiers, degree counts and explicit unresolved cases.

## Independently checked finite game kill

On Creative's saved order-sixteen quadrilateral member only, Math rebuilt all 1186 states independently. The game has 432 filled states, 1076 winning states and a 110-state losing kernel. Every one of the 50 candidate root/fan pairs has an admitted losing start; the best wins 44/46. The entire losing kernel is certified: every player action has an adverse outcome remaining inside it. Without the adversary, pure swaps fill from every state.

This accepts that saved member as a counterexample to the free-adversary game. It is neither a counterexample to VH_C/VH∃ nor a replay of Creative's newer 435/4004/2146 exploratory collections. The trace-game lift has a repaired hand proof in `MathTraceGameLiftReview.md`: replace ordinary virtual edges by pair-specific connections, with explicit coloured planar snapshot gadgets. Its universal hypothesis remains open. The exact source, independent code and output hashes are in `MathFourRingGameCertificateReview.md`.

## Next structural tasks

- Prove a face-avoiding fill in the four-connected relative core, especially the remaining boundary-degree-four case whose adjacent vertices all have degree at least six.
- At a targetless component touching a degree-five region, either derive an escape at its higher-degree frontier or rule out the global, branching all-degree-five projection. Mobility is not termination.
- Review the evolving constrained trace game; accept only a valid composition theorem, without importing exploratory passes into a universal claim.
- Formalise the mobility-to-short-fill bridge and boundary-degree-four reduction against actual move semantics. The newly compiled composition lemmas already supply the protected-path interface.

VH_C and VH∃ remain open. The new reductions identify and eliminate cases; they do not supply the final global controller or the universal good pair.

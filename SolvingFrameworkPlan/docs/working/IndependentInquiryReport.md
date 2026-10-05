# Independent inquiry: mobile vacancies and long corridors

4 October 2026. Independent work under the user's instruction to explore broadly. No messages were posted to other teams. These experiments are exploratory uses of the already replayed discovery colourings, not a new holdout or a universal theorem.

## A different escape mechanism

Instead of keeping the deleted root fixed, move the vacancy to a uniquely coloured neighbour and give the old vacancy that neighbour's colour. Properness survives. This move can travel through degree-six and higher vertices. It is reversible and preserves the four occupied colour-population counts.

The known q trap at order 17 graph 0 root 4 state 25 escapes without a Kempe swap: vacancies 4→5→12→13→6, with degrees 5,6,5,6,5. The final vacancy sees only three colours and can be filled. The intermediate degree-six vacancies explain why an exclusively degree-five-root interface conceals this route.

Breadth-first exploration of singleton slides, modulo global colour names, found targets for all 172 discovery hard states lacking a one/two-Kempe-swap route directly to a target. The longest found slide path had nine moves. Across all 11,714 non-target discovery starts, 11,698 reached a target; sixteen exhausted closed slide components with no target. No 200,000-state cap was reached; the maximum states seen was 216, and the longest successful path was ten slides. These are finite observations, not asymptotic bounds.

## The failure exposes an invariant

All sixteen failures are on order 18 graph 10, a triangulation with two nonadjacent degree-eight poles and sixteen degree-five vertices. Each closed slide component has 32 states. Each failing partial colouring has sorted occupied class sizes (2,5,5,5). Any filling after slides would have class sizes (3,5,5,5) or (2,5,5,6). The complete previously replayed deletion table yields only (4,4,5,5) for full colourings, so population conservation blocks every slide-only completion.

This fixture matches the two-pole family studied by Jan Florek. The paper provides a structural connection between colour populations and Kempe classes, and proves bounded Kempe connectivity after deleting a pole. This suggests letting the vacancy reach high-degree vertices rather than treating them only as curvature costs. [Primary paper](https://arxiv.org/pdf/2511.00485).

For each of the sixteen slide-only failures, one ordinary component switch followed by slides reaches a target; in the first stored example the switch already makes the current vacancy fillable. Exact component and colour witnesses are saved. Thus the new candidate is **a slide segment, at most one component switch, another slide segment, then fill**. The universal candidate and any polynomial length bound are unproved. A proper kill must exhaust the first slide component and every ordinary switch from it, then the successor slide components; one unsuccessful route is insufficient.

Slides are precisely fifth-colour Kempe swaps on a two-vertex component when the fifth colour marks the sole vacancy. This links the mechanism to five-colour reconfiguration, while exposing the restriction: a general five-colour path may create multiple fifth-coloured vertices. Existing equivalence theorems do not give a one-defect elimination path.

## A hand proof beyond the census

The equal-pole case admits a direct infinite-family proof. In the two-pole antiprism suspension, suppose a deleted belt vertex has a non-target boundary and both poles have colour A. A occurs only at the two poles. At least one of the adjacent opposite-ring boundary vertices has a unique boundary colour B. The A/B component of the opposite pole is a star, meeting the boundary only at that B vertex. Swapping the star changes B to the already present A and makes the vacancy fillable. This works for every ring length, without symmetry counting or enumerating colourings.

For n=3k+2, it converts the conserved partial population (2,2k+1,2k+1,2k+1) to the full population (k+2,k+2,2k+1,2k+1). At n=8 this exactly explains the sixteen failures. This is a checked hand argument, not yet a Lean theorem. Differently coloured poles remain outside its scope. The precise proof is in `TwoPoleStarEscape.md`.

## An infinite family with real independent switches

The corridor branch constructed capped pentagonal cylinders with two hubs and m rings: 5m+2 vertices, exactly twelve degree-five vertices, all others degree six. Triangle subdivision separates the defects while preserving their number.

An explicit compatible ring motif is 01023→32101→13230→01023. In each middle ring, its column-four vertex is an isolated component for colours 1 and 2: all six neighbours use 0 or 3. Repeating k motifs gives k commuting switches and 2^k proper named colourings, with fixed cap boundaries and twelve fixed curvature defects. The capped example has 15k+17 vertices. This proves unbounded interior freedom, **not** unbounded traps or warnings; those cap boundaries are already targets, and connectivity of other colour pairs need not stay fixed.

The same branch obtained a direct period-four colouring for every cylinder length, and a ten-pattern ring-transfer graph with one strongly connected component and diameter three. The opportunity is a corridor compression invariant retaining palette transport and relevant crossing chains. Fixed-width cylinders admit such finite descriptions; this does not imply bounded width for all spherical maps.

F32 and F42 graph-only fixtures were also constructed with explicit oriented faces, rotations, twelve root-transport permutations and computed mod-two filling ranks. No full colouring search on either larger fixture ran.

## Checked lemmas, without turning inquiry into interfaces

The fresh integrated Lean build passed **83/83** custom modules and tests; all previous 79 source hashes are unchanged. Four added files contain thirteen exact axiom guards using only the standard axioms. VacancySlide proves properness, reverse legality and restoration away from the vacancy. RankPortfolio proves conditional graph-level portfolio contact and the active-minimum envelope criterion. Neither asserts universal descent or a selector.

## Next mathematical attack

Prioritize the mobile-vacancy mechanism. Characterize closed slide classes by conserved populations and cycle transport, then ask which Kempe switch changes the obstruction. Use the two-pole family to derive an infinite hand-checkable example before fitting another weighted rank. In parallel, use the explicit corridor motif to distinguish harmless interior freedom from switches that alter a locked boundary. The innermost vacancy-cycle idea may supply planar separation, but needs a precise region measure and remains speculative.

The evidence is in `backgroundMaterial/planemap-structural/independent-inquiry/`. The saved exploratory scripts preserve their original /tmp execution paths and the existing corpus input path; they are experiment records rather than a supported shared tool. No Four Colour completion or polynomial solver is claimed.

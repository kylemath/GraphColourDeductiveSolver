# Degree-five mobility: kernel compilation report

Math, four-connected research team, 5 October 2026. The new source and guarded test compile cleanly against the merged 99-module baseline at `/tmp/planemap-audit-20261005-protected-lift`. Root Math will perform the fresh combined full-source audit; this report does not claim that audit has already passed.

## Exact compiled theorem

Live source: `/Users/fulkanjou/mathlib4-planemap/Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyMobility.lean`.

`SimpleGraph.SphericalMap.vacancy_mobility_normalized` takes:

- an actual native `SphericalMap n`;
- a five-port injective enumeration of the complete actual neighbourhood of the hole;
- the proper deletion colouring with normalized link word `(0,1,0,2,3)`;
- the native rotation advancing those five ports cyclically.

It concludes either a pure fill at the original hole within one swap, or, for every chosen actual neighbour, an `Approach`: a concrete colouring obtained by zero or one actual whole-component Kempe swap at the original hole, proper there, in which the chosen neighbour is singleton. `approach_reach` constructs the actual singleton slide and an indexed mixed path of length at most two with proper endpoint.

All Kempe components are the actual reachable component of the selected active seed in `VacancyShortFill.pairGraph`; no abstract move conclusion or controller is assumed. The two repeated-colour ports are unlocked by their explicit alpha/gamma and alpha/delta swaps. The other three ports are immediately singleton. Missing gap chains give actual one-swap fills using the previously compiled `one_swap_target` construction.

## Native geometry is discharged

The graph-level `Alternation` record states two pair-connectivity implications excluding four particular complementary connections. It is not a premise of the final native theorem. `vacancy_pairs_separate` maps actual pair-graph walks into the map graph, proves their supports remain active and avoid the hole, and applies the existing compiled `SphericalMap.alternating_walks_intersect` theorem. Disjoint colour pairs then exclude the returned common vertex.

`vacancy_alternation` applies this native result to four explicit permutations of the five ports. Thus there is no added planar-separation axiom or unproved geometric premise in the final theorem. It uses the existing spherical rotation/face-sum framework, not a classical Four Colour theorem.

## Important remaining normalization scope

The final theorem is **normalized**, not yet the full arbitrary-four-colouring degree-five statement. Its `Pattern` assumption is explicit and printed. The general hand proof rotates a proper four-colour five-cycle and renames its colours to this word; the zero-move filled case is immediate. This source does not yet compile that rotation/colour-renaming transport or a universal arbitrary-word normalization theorem. Native cyclic enumeration exists elsewhere in the baseline, but its composition with colour-word normalization is not packaged here.

Root integration can use the exact normalized theorem without overstating it. The unrestricted hand mobility theorem remains broader than the formal statement until normalization transport is compiled.

## Tests and axiom guard

`MathlibTest/PlaneMapVacancyMobility.lean` has exact guards for:

- both explicit repeated-port unlocks;
- the graph-level local alternative and the concrete-path conversion;
- native pair separation;
- native alternation;
- the final normalized native mobility theorem.

Every guarded theorem has only `[propext, Classical.choice, Quot.sound]`. There are no `sorry` placeholders or new axioms. The test prints the final theorem and both concrete movement definitions so the accepted scope remains visible.

Committed-source candidates, the printed statements/axioms, and the successful guarded-test log are in `backgroundMaterial/planemap-structural/mobility-lean/`. This team has not staged or committed them; root owns the combined integration and audit.

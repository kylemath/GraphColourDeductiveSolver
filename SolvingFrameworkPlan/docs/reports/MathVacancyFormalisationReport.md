# Parallel Math formalisation and saved-work audit

5 October 2026. Three parallel teams formalised the actual mobility kernel and short-fill bridge, independently replayed the saved trace game, and reviewed the additional five-ring hand reduction. Root integrated the native spherical degree-four theorem with the two move kernels. No new graph census or random exploration was run.

## Compiled scope

`VacancyEasyNeighbour` derives an actual original-hole pure path of length at most two from a singleton slide to an easy neighbour. An optional actual preparatory Kempe swap gives length at most three. The protected path keeps every intermediate hole at the original vertex, even when the auxiliary easy neighbour is protected. Its arbitrary-graph geometric premises are explicit. It also derives the finite four-colour degree-at-most-three case and the sharper one/two-swap bounds.

`VacancyMobility` uses the complete actual five-neighbour link and the normalized word `(0,1,0,2,3)`. In the native `SphericalMap` carrier, `vacancy_alternation` derives all four chain-separation facts from the existing rotation/face-sum theorem, with no added topological axiom. `vacancy_mobility_normalized` then supplies either a pure fill within one swap, or an actual optional whole-component swap followed by a legal singleton slide to **any chosen neighbour**. It constructs moves on the current deletion graph; it does not reuse a component after an unjustified recolouring.

`SphericalVacancyEasy.vacancy_easy_degree_four` quantifies over every proper four-colour deletion start at a vertex of degree at most four in the native spherical carrier and derives zero or one actual whole-component swap yielding a missing colour. It uses colour-image cardinality, the existing degree-four rotation, and the native opposite-chain separation theorem. Its conclusion is an actual move relation, rather than mere existence of a different colouring.

The root integration gives:

- `vacancy_singleton_easy`: singleton access to a degree-at-most-four neighbour implies an original-hole pure fill within two swaps.
- `vacancy_singleton_easy_protected`: the actual replacement avoids any protected set not containing the original hole, at every step.
- `vacancy_approach_easy`: an optional actual preparatory swap exposing that slide implies a pure fill within three swaps.
- `vacancy_gap_easy`: the native normalized five-neighbour gap case adjacent to a degree-at-most-four neighbour fills within three swaps, with its geometry discharged.

**Scope limit:** rotation and global colour-renaming transport from an arbitrary proper five-cycle word to the normalized word is still a hand wrapper. This package does not claim the unrestricted degree-five mobility theorem has been compiled. Fan legality and the universal quantifiers of VH∃ are not supplied by the normalized theorem. Neither mobility nor these short fills prove global termination.

## Independent saved computation

`MathTraceGameReplayReport.md` records an independently implemented exact replay of the saved order-16 **pure trace game**. All 50 fan counts match. Its ten closures contain 77,180 labelled positions; all are winning against every admissible adversarial update, with the moved pair and complementary pair frozen. Global colour labels are not canonicalised during transitions. This finite pass is not a universal trace-game result.

The saved summaries for 435 triangle members, 4,004 quadrilateral members, and 2,146 far-side alignments omit their complete raw graph inputs. Their metadata totals are consistent, but their mathematical outcomes remain independently unreplayed. The team did not generate substitute inputs or run a new census. The missing inputs are explicitly requested in the outgoing message.

The corrected four-ring hand lift is accepted within its conditional scope. The later five-ring extension is reviewed separately in `MathFiveRingTraceReview.md`; neither hand lift is a compiled universal game strategy.

## Validation and remaining work

The full fresh-source audit extends the accepted 99-source baseline with three new source modules and three tests. Custom compiled caches are excluded, exact standard-three-axiom guards are checked, and all source hashes must remain stable throughout the build. Final audit result and bindings are recorded below after completion.

Next formalisation targets are the word/colour transport needed for unrestricted native mobility, then the geometry/fan wrappers for the structural reductions. The remaining mathematical gap is still a universal interior filling strategy in the relative core or an equivalent sufficient hypothesis. Higher-degree escape and a terminating global controller remain open.

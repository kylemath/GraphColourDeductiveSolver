# Team B: full general short-fill theorem compiled

5 October 2026. Implemented in the actual mathlib checkout as `Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyShortFillTeamB.lean`, with tests at `MathlibTest/Combinatorics/SimpleGraph/PlaneMap/VacancyShortFillTeamB.lean`. Preserved source snapshots are `team-b-lean-short-fill.lean`, `team-b-lean-short-fill-test.lean`, and the actual imported `team-b-lean-vacancy-slide.lean`.

The implementation has actual generic graph moves, not a premise asserting the desired conversion. `pairGraph` is the bichromatic induced graph in the deletion, represented on the total vertex type with inactive vertices isolated. `swapComponent` applies `Equiv.swap` exactly on the reachable component of an active non-hole seed. `KempeStep` includes properness of the original deletion, distinct colours, and the actual component swap. Properness after a component swap is proved. Slides use the existing actual `VacancySlide.slide` and `UniqueAt`, with the stored hole colour irrelevant.

Compiled results include:

* `terminal_component` and `terminal_slide`: a terminal singleton slide is replaced by one actual whole-component Kempe swap.
* `sk_pair_fill`: every target-reaching SK path whose pair contains the slid colour collapses to one original-hole component swap. Both `h in K` and `h not in K` are handled by reachability invariants, including singleton/empty-attachment situations.
* `sk_fill`: the avoiding-pair case commutes and terminal-eliminates into two swaps; pair-containing cases give one.
* `two_step_fill`: KK, KS, SS, and SK all give a pure replacement of at most two moves. SS eliminates its second slide and invokes the proved SK conversion.
* `short_fill` and `short_fill_proper`: an actual mixed path of length n<=2 yields an actual fixed-hole pure path of length k<=n, ending in a proper deletion colouring with a missing neighbour colour.
* `short_minimum_exists` and `short_minimum_eq`: a short mixed minimum constructs the pure minimum at the same exact number, and equality follows for independently specified minima. No unjustified padding of nonminimal paths is used.

Theorems use arbitrary vertex and colour types and impose no planarity, fan, degree, cardinality, or finiteness condition. The concrete slide API requires decidable vertex equality; the component swap uses classical colour equality internally. Thus the requested finite graph/finite palette theorem follows directly.

`team-b-lean-check.py` creates a new isolated extension overlay from the frozen 79-module dependency overlay, excludes cached VacancySlide/TeamB artifacts, compiles the actual VacancySlide source, compiles TeamB's source, then compiles the tests. It never invokes a lake build or uses the checkout's cached custom artifacts. All three compiles succeeded with no messages. Results and source hashes are in `team-b-lean-check-results.json`; commands/output are in `team-b-lean-check-output.txt`.

The test checks an unrestricted-palette theorem signature and a K2 terminal-slide fixture whose stored hole colour equals its neighbour colour, guarding the intended irrelevant-hole-label semantics. Nine exact `#guard_msgs` axiom reports all allow only `[propext, Classical.choice, Quot.sound]`. No sorry, admit, native_decide, new axiom, or unproved conversion assumption occurs.

## Independent review of Team A

I read Team A's full 485-line implementation after completing Team B's implementation independently. Team A represents a whole component as an active seed plus an iff to graph reachability; this is an actual component condition, not merely closure or a black-box conversion premise. Its component properness, terminal singleton, original-component one-swap escape, commuting swap, all four two-step paths, and minimum-optimality conversion have the intended hand-theorem semantics. Its move relation does not carry properness directly, but the theorem takes initial `ProperOff` and proves preservation for both path types, so no properness gap follows. `[DecidableEq C]` restricts no finite palette and is independent of the cardinality. I found no semantic gap or encoded theorem assumption. Root's fresh compilation/axiom audit remains the canonical acceptance evidence.

## Remaining scope

Task A is complete as an independently compiled implementation. Integration/naming and the canonical source audit belong to the Math root. The all-n unequal-pole belt theorem and the infinite clique-sum theorem are separate tasks and are not implied by this module.

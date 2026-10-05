# Team A: complete general short-fill formalization

5 October 2026. Both assigned formalization tasks are complete: terminal-slide elimination and the full two-step theorem, including exact minimum equality. The implementation is in `/Users/fulkanjou/mathlib4-planemap/Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyShortFillTeamA.lean`, with import/tests in `MathlibTest/PlaneMapVacancyShortFillTeamA.lean`. Source snapshots are `team-a-lean-shortfill.lean` and `team-a-lean-shortfill-test.lean` in this audit directory.

## Mathematical interface

The namespace is `SimpleGraph.VacancyShortFillTeamA`. The graph is arbitrary and the vertex/palette types only require decidable equality. No planarity, degree, finite-palette-cardinality or vertex-finiteness assumptions are used.

* `pairGraph` is the actual two-colour simple graph in the deletion, with excluded vertices isolated.
* `Whole` requires an active seed and equality with its entire `SimpleGraph.Reachable` component. It is not merely a closed set or an assumed conversion property.
* `swap` applies `Equiv.swap` on that component and preserves all other colours.
* `KempeStep` existentially specifies unequal colours, one actual whole component and the actual swapped total function.
* Slides are exactly the pre-existing `VacancySlide.slide`, with graph adjacency and `UniqueAt` legality. Its irrelevant stored hole colour follows that API.
* `PurePath` counts Kempe steps with the ORIGINAL hole fixed. `MixedPath` counts actual Kempe or singleton-slide transitions on hole/function pairs. Both have properness-preservation lemmas.
* `Target` means an actual palette member is absent from the current hole's neighbour colours.

The proof does not take terminal-slide elimination, SK commutation or any short-fill conversion as hypotheses. Those statements are proved from the component graph, swap and slide definitions.

## Main compiled declarations

`terminal_slide` constructs a whole singleton component, one original-hole Kempe move, a proper resulting colouring and a target.

`slide_swap_same` proves every successful SK path whose pair contains the slide colour collapses to one original-hole Kempe move. The two exceptional branches use invariants along ACTUAL original bichromatic walks: the original u-component stays outside the intermediate component, or inside that component union {u}. This avoids a degree-bound component count.

`slide_kempe` handles arbitrary swapped pairs, including the outside-pair commutation argument, constructing at most two original-hole Kempe moves.

`mixed_two` covers KK, KS, SS and SK directly. KS eliminates its last slide; SS eliminates its second slide and then invokes the proved SK theorem.

`short_fill` says that any given actual mixed target path of length n<=2 yields a pure target path of length at most n. It does not assert equal lengths for a supplied nonminimal path or silently pad paths.

`optimal_short` expresses and proves exact optimal-distance equality: if n<=2 is achieved by a mixed target path and no shorter mixed target path exists, then n is achieved by a pure target path and no shorter pure target path exists. It avoids arbitrary infinite-distance sentinels. Pure paths embed in mixed paths explicitly.

## Fresh compilation and trust

`team-a-lean-shortfill-compile.py` creates a fresh extension overlay of the frozen 79-module audit dependencies. It source-compiles the ACTUAL baseline `VacancySlide.lean` first, then this new theorem module, then the MathlibTest import. It never falls back to a cached VacancySlide or performs an unrestricted Lake build. Compiler return codes, source/olean hashes, compiler version and the frozen-manifest hash are recorded in `team-a-lean-shortfill-results.json`; logs are alongside it.

The test module includes a concrete two-colour, degree-two original hole with mixed and pure optimal distance one, checked by ordinary kernel `decide`. It demonstrates the absence of a degree-five/four-colour requirement and checks actual theorem application.

`#print axioms` for terminal_slide, slide_swap_same, slide_kempe, short_fill and optimal_short reports only the standard Lean/mathlib axioms `propext`, `Classical.choice`, `Quot.sound`. No sorry, admit, native_decide or newly introduced axiom occurs in either new source. No experiment or census was run, no baseline source was edited, and no commit was created. Root integration and independent recompilation remain separate from this team's compilation.

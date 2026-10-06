# Independent Math replay of the saved order-16 trace game

Math triangle-carry research team, 5 October 2026. **[computed: independently matched, one saved exploratory member]**. This is Math's independent checker, not a claim that the separate Audit team has finished. No graph generation, new census, random sampling, or plantri invocation was performed.

## Scope, inputs, and caps

The checked graph is exactly the member already used in the free-game counterexample: order 16, edge (0,9) removed, protected quadrilateral (0,14,9,1). We checked the **pure** trace game at all ten degree-five vertices outside that quadrilateral, every legal fan, every admitted proper start, and every admissible initial bit assignment.

Input bindings:

- `longtable/explore-vhphi/vhphi-quad-explore-seed2-mixed0.json`: SHA-256 `ca1c0921e24c005cf551a5c67e4876ad52319502ccea738df1aca3489015d224`.
- Expected counts `longtable/explore-vhphi/trace-game-order16.json`: SHA-256 `e61b0ef59039b006f4f3bc720499d8edd24729ed2fe983dd3664480d7f127962`.
- Independent checker `longtable/audit/math_trace_saved_replay.py`: SHA-256 `c29cf6f8084f62491278775135d8d547627d6d408d0458fb6dddf64e4ffda070`.
- Output `longtable/audit/math-trace-saved-replay.json`: SHA-256 `660faa5f3821016cf74311698cf07962e48a06fa4971eb9a97fadada3dc161c8`.

Scope and limits were sent to root before running: 600 CPU seconds, 100,000 positions per root, output under 100 MB. The exact replay completed in 6.497 seconds, with at most 8,024 positions at one root. No cap was reached.

## Independent game implementation

The checker imports no producer or previous checker module. It reconstructs adjacency and rotations from the frozen face list. Graph/class validity was independently checked in the preceding saved-member replay, bound to the same input digest.

At each root, it enumerates every proper deletion colouring modulo global colour permutation by restricted-growth backtracking. For each it independently enumerates all relevant opposite-pair bits and every admissible assignment: no set bits on different diagonals with disjoint colour pairs.

A position records an actual labelled colouring and a six-pair bit mask. **Colours are not canonicalised during transitions.** This matters because the frozen pair and complementary pair refer to the labels of the actual move. Canonical initial colourings with all initial assignments suffice by colour symmetry; the subsequent labelled closure is explored exhaustively.

Every player action is a whole component swap. If its pair's bridge bit is set and the selected component touches the quadrilateral, all components touching that boundary in the pair are merged before swapping. Otherwise the selected component alone is swapped. The checker then enumerates every admissible successor bit assignment preserving the moved pair and its complement. It verifies that both pairs retain their relevance, every successor colouring is proper, and every action has at least one admissible outcome.

Closure is exhaustive from all initial positions, stopping only when a fill has already been achieved. Every nonterminal action and every permitted bit update has a recorded successor. A terminal position is an immediate win, so exploring actions after it is unnecessary.

Winning positions are the least attractor obtained by adding a position precisely when **there exists a player action for which every adversarial successor is winning**. This is the game's required quantifier order, not reachability after an existential choice of bit update. Thus the result verifies a strategy against every permitted history of updates.

## Exact replay results

| Hole | Closure positions | Initial positions | Attractor layers | Fan counts |
|---|---:|---:|---:|---|
| 2 | 7,851 | 330 | 3 | all matched |
| 3 | 8,024 | 342 | 4 | all matched |
| 4 | 7,851 | 330 | 3 | all matched |
| 6 | 7,416 | 309 | 4 | all matched |
| 8 | 8,024 | 342 | 4 | all matched |
| 10 | 7,851 | 330 | 3 | all matched |
| 11 | 7,448 | 318 | 4 | all matched |
| 12 | 7,851 | 330 | 3 | all matched |
| 13 | 7,416 | 309 | 4 | all matched |
| 15 | 7,448 | 318 | 4 | all matched |

All 77,180 positions across the ten closures are winning. Every one of the 50 legal root/fan pairs wins from every admitted start and every admissible initial assignment. All 50 `(won,total)` counts match the saved output exactly, including hole 2, fan 0: 168/168. The layers count a simultaneous attractor expansion, rather than producer iteration passes.

This finite pass establishes the claimed pure trace-game result on this particular saved member. It proves no universal trace-game bound or hypothesis, and no universal depth-four bound.

## Corrected hand source

The corrected four-ring source uses pair-labelled bridges and its new admissibility argument considers only the two disjoint-colour witness paths. Such bridges cannot cross at phi because admissibility forbids their alternating disjoint-pair endpoints. They cannot share a same-diagonal endpoint because their colour sets are disjoint. The labelled pair graph and frozen-pair argument now agree with the repair in `MathTraceGameLiftReview.md`.

Accordingly the earlier conditional four-ring hand acceptance survives the correction. The later five-ring section was not automatically accepted in this replay; it needs its own hand review. This report does not upgrade any conditional lift to a proof that the universal hypothesis holds.

## Other saved claims: exact status

| Claim | Replay status | Reason |
|---|---|---|
| Saved order-16 free-game kill | matched independently earlier | 1,186-state closure; 110-state losing kernel |
| Saved order-16 pure trace game | matched independently here | all 50 fan counts and all allowed updates |
| 435 triangle members | **not replayed** | records save indices, low-degree sets and summaries, without graph rotations |
| 4,004 quadrilateral members | **not replayed** | records save raw graph lines only for the two failures, not all passing inputs |
| 2,146 far-side gluings | **not replayed** | records save disc names, indices and alignments, without the actual disc graphs |
| Pure trace pass on all 4,004 members | **not independently established** | implication from free-game passes is sound, but the broader free-game inputs/results are not independently replayed |

Reading the saved summaries confirms the arithmetic totals 435 graph members, 1,844 designated triangle faces among them, 4,004 quadrilateral members, and 2,146 gluing records. This is a metadata consistency check only. It does not verify graph-class completeness or a mathematical outcome on those missing graph inputs.

The newer `trace-members-*` passing records similarly use `line:null`, so they do not solve the replay-input problem. To independently check the broader claims without new enumeration, the existing raw rotations and far-side graphs need to be supplied or located. No regeneration was used as a substitute for those inputs.

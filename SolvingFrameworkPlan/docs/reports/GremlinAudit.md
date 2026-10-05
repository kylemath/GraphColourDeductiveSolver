# Gremlin work audit

4 October 2026. Read-only review of existing exploratory work, plus bounded independent replays of explicit witnesses and one local tile argument. The user confirmed that an exploratory gremlin team worked across these pathways. Untracked outputs are therefore not discarded merely because another team's declaration ledger did not record them. This review does not identify the author of each output, certify an entire large census, release WP12, or change navigator statuses.

## Main finding

There is useful progress beyond the night handoff. There is also a substantive quantifier error: a large number of unsuccessful two-swap paths does not establish that no successful two-swap path exists. The published 21-vertex colouring itself fills after two Kempe swaps and one slide. The independent replay confirms this, including properness of the resulting full colouring.

The remaining A_rho tile also has a local transition. It fills after two slides in one branch and returns a prepared zero after four slides in the other. The full unequal-pole theorem still requires an assembled termination and cap argument.

## Independently checked

| Artifact | Result of this review | Scope |
|---|---|---|
| WP11 validation manifest | All 1,309 files match SHA-256, including results, certificates and 1,307 tables. Commits f8ef782 and bba6203 exist. | Integrity check; not a full semantic replay of every certificate. |
| Icosahedron fans | Reproduced all 60 vertex/fan pairs with independent colouring and move code. Each has eight orbits: two already fill, three fill by one slide, three need two slides; all six non-targets fill by one Kempe swap. Each vertex has 20 deletion orbits, all at Kempe distance at most one. | Complete replay on this graph. |
| Order-14 dipyramid start | Proper on the specified fan. All eleven bichromatic component swaps preserve a four-colour link. All three legal slides also preserve four colours. An explicit two-swap fill exists. | Exactly two mixed moves for this start. Does not establish the best vertex/fan statistic or global minimality across all graphs. |
| Order-21 frozen witness | Rotation has 21 vertices, 57 edges, 38 triangular faces, minimum degree five. All sixteen single swaps stay frozen. The 224 ordered pairs split into 172 frozen and 52 singleton-producing endpoints. Two swaps and one slide fill. No two-swap endpoint directly fills at the original hole; a three-swap endpoint does. | One explicit colouring. Distinguishes fixed-hole swaps from swaps followed by slides. |
| Order 17 graph 1, fixed-hole distance | Independently enumerated all deletion colourings at all twelve degree-5 roots and reconstructed their Kempe graphs. Each root has maximum target distance four, and every colouring reaches a target. | Minimum over roots of the worst distance is four for arbitrary deletion starts with a fixed hole. No selected-fan or slide restriction was evaluated. |
| WP13 generated graph corpus | All 244 saved rotations pass simplicity, connectivity, triangular-face, Euler, minimum-degree and degree-metadata checks. | Graph validity verified; pairwise non-isomorphism and advertised search coverage not independently checked. |
| Remaining A_rho tile | All stated local colour cases and both rho/tau labellings pass singleton-slide checks. | Local hand lemma, not Lean and not a completed global belt theorem. |

The independent checker is `/Users/fulkanjou/Documents/ChatGPT/planemap/audits/gremlin-2026-10-04/check.py`; its saved output is `results.json` beside it. It imports none of the team's move implementations. It did not run a new census or enumerate n=14 belts.

## The 21-vertex correction

Starting from the colouring in `longtable/swarm/two-kempe-kill.md`:

1. Swap colours 0 and 3 on {0}.
2. Swap colours 0 and 1 on {2,4,6,7,12,13,14,16,17}.
3. Slide the hole from vertex 1 to vertex 6.
4. Fill vertex 6 with colour 2.

Every step is legal. After the slide, vertex 6's link uses colours {0,1,3}. Thus the example rules out a one-Kempe-swap mixed escape, but **does not rule out a two-Kempe-swap mixed escape**. Its minimum number of Kempe swaps when slides are allowed is exactly two. Its minimum number of swaps to a target at the original fixed hole is three.

`NightHandoff.md` says a budget of two is already too small for the vacancy hypothesis. `SwarmConsolidation.md` says this same witness kills “at most two Kempe swaps.” That conclusion is not established by this witness. Those statements need the move model qualified, or a different witness.

Likewise, showing that particular branches need a third swap, or that many choices stay frozen, does not disprove the existence of a shorter successful choice. Nor does refuting a particular small budget prove that every possible finite uniform budget fails. I repeated the handoff's unsupported budget interpretation earlier in chat; this replay corrects that interpretation.

`two-kempe-kill.md` also lists 63 edges and 42 faces for the 21-vertex graph. The actual rotation, and the spherical formulas, give 57 edges and 38 faces. The colouring and two-swap escape remain valid.

`return-pairs.md` says every non-returning continuation after a return-pair first swap reaches a singleton on the second swap. Its own table gives eight frozen non-returning seconds. The supported statement is **each first-swap image has some second swap that reaches a singleton**, not that every non-returning second swap does.

## Work the handoff did not account for

### Rank-free fixed-hole distance (WP15)

`longtable/wp15-kempe-distance/kempe-distance-results.json` covers the 118 saved minimum-degree-five triangulations through order 20 and their 1,586 degree-five roots. Its producer performs BFS over complete Kempe state graphs, not a fitted-rank sweep.

The saved data report no unreachable starts and no targetless Kempe classes. Root maximum distances are one at 63 roots, two at 1,249, three at 250 and four at 24. Minimizing the worst distance over roots gives eight graphs at one, 106 at two, three at three and one at four. The best-root-four graph is order 17 graph 1, independently replayed above.

This is substantial finite evidence for reachability even where particular descent ranks fail. It does not prove unbounded vacancy reachability generally. It also does not answer the proposed m(T): fixed-root arbitrary starts and selected-fan mixed paths are different problems.

### Scale sweeps (WP12-scale)

Existing output files cover orders 20–26:

| Order | Graphs checked according to saved output | Degree-five roots |
|---:|---:|---:|
| 20 | 73 | 1,001 |
| 21 | 192 | 2,714 |
| 22 | 651 | 9,478 |
| 23 | 2,070 | 31,119 |
| 24 | 7,290 | 112,977 |
| 25 | 25,381 | 405,465 |
| 26 | 91,441 | 1,504,769 |

These saved outputs report that q and lin each retain at least one passing root on every checked graph, although many individual roots fail. Of the 259 WP11 validation existential survivors, 258 remain existentially good at every order 22–26 in these outputs. The lost vector is [0,0,0,0,0,3,0,1], failing to find a good root on order 22 graph 167.

That is useful exploratory evidence for root selection. It is not evidence for all-roots descent, and these are not independently replayed large-sweep results. The distinction matters: an all-roots rank failure does not kill an existential root-selection theorem.

### Large fixtures

`verify-py-F32-r0.json` records 4,840 deletion-colouring orbits, and `verify-py-F42-r0.json` records 94,330, both at root zero. The inspected producer calls `deletion_colourings`, not a full-graph colouring enumerator. Both saved outputs report no starts requiring more than two swaps at that fixed root.

Consequently, a colouring search did occur on these **deletions**. A literal statement about no full-graph enumeration is narrower and cannot be declared contradictory merely from these files. Broad wording such as “the graphs were not coloured” should explain this distinction. These results do not establish an isolated-pentagon slide bridge.

### New rank probes (WP14/WP17)

WP14 recorded discovery success for several additional ranks, including H, nLS and kempe4. Its H is an indicator of having no target within two fixed-hole swaps. That is a lookahead feature: with fixed-hole distances at most four, it can fall to zero within two swaps. It is not an independently derived universal progress law. It should also not be silently identified with similarly named functions on moving-hole states in the swarm notes.

The WP17 saved holdout includes 192 order-21 graphs and 651 order-22 graphs. It breaks many discovery-success candidates. For example, lin+linNoRho+L has no failing roots through order 20 in that file, then four at order 21 and twelve at order 22. A few other candidates still have no listed failures; that is an exploratory observation, not proof. The kd candidate is computed shortest-path distance itself, so success wherever targets are reachable is expected.

These results are worth retaining as experiments, with their exact domains and move rules. They should not be promoted to theorem status, or dismissed merely because they were not in the handoff.

## Proof pathways

The equal-pole star argument is coherent: the other pole and its neighbours of the selected colour form a complete bichromatic component, and the unique boundary occurrence of that colour is removed by its swap. This is an infinite-family hand argument, unlike a census result.

The missing A_rho transition is now written in `longtable/swarm/unequal-a-rho-tile-audit.md`. If x=c(u_{i-2})=rho, two slides fill. If x=tau, the walk

    v_i -> u_i -> u_{i-1} -> v_{i-1} -> v_{i-2}

returns the same prepared shape. This closes the named local gap. Joining opening cases, ordinary tiles, cap termination and small-ring overlaps remains a separate proof obligation. Florek's pole-hole theorem and external literature were not independently reverified in this local audit.

VH-exists is a sufficient weakening for the hand induction: choose one degree-five vertex and one legal fan, colour its smaller completion, restrict, and use the assumed moving-hole reachability. The universal union over all legal fans of an induced pentagon is not a restriction on deletion colourings. These quantifier distinctions are useful, but none proves VH-exists itself.

The cross-field notes provide failures of the particular mappings and rank functions they tried. Reversibility rules out strict descent on **every** legal slide. It does not rule out a strategy that selects one decreasing move at each non-target state. The failed height, sandpile, flow and monodromy proposals should therefore keep their stated concrete scope; they do not establish that an entire mathematical field can never help.

## Reporting repairs

Revision 72 of `NightHandoff.md` already contains the fan classification and links `fan-link.md`; `LongTableNextAttack.md`'s missing-classification complaint was based on revision 70 and is stale.

Commit 833e0f7 has now corrected the WP7 sentence to “The minimum-mass singleton pair is joined directly along the boundary cycle.” Its later short-circuit-trap description still suggests all singleton pairs run through the boundary, despite the erratum explaining that two need exterior vertices. That later passage should also respect the minimum-versus-all distinction.

Validation integrity is now checked and ready to report. No inter-team messages were sent by this audit. No large experimental run was launched, and no navigator status was changed.

## Subsequent Long Table update: 833e0f7

The commit exists and includes the validation-complete and retreat-positions messages, WP7 sentence correction, hash manifests, published order-14 checker and output, and the WP18 declaration. It does not contain the large output trees, play files or navigator edits. The main Long Table manifest has 77 entries and the night-swarm manifest 115; every entry in both matches its saved file. This is in addition to the 1,309-entry validation manifest check above.

The independent order-14 replay also reproduces the reported 36 successful two-move sequences. The team's checker enumerates sequences rather than distinct endpoint states, so that count should retain the word “sequences.”

The retreat message still repeats the stale complaint about the missing classification. Revision 72 already contains it. Its F32/F42 disclosure says scope was unchecked; this audit resolves that part as root-zero deletion enumeration.

WP18 has a coherent statistic and keeps the single-start order-14 obstruction separate from m(T). Its regressions are proposed requirements: no producer or regression suite exists yet. Nothing in this audit runs WP18 or grants its requested go-ahead.

Before relying on its checker, the declaration needs one mathematical validation requirement made explicit: **replaying a successful path proves an upper bound on distance, not shortestness**. To certify m(T)>=3, every legal vertex/fan pair needs an admitted start with no fill in zero, one or two moves. The checker must verify that exclusion by independently exploring the complete depth-two move neighbourhood, or checking complete BFS layers, and must verify that every legal pair has been covered. A supplied length-three path alone cannot certify the lower bound.

Cap wording should also distinguish failure to decide unbounded reachability from refuting the bound two. A fully explored start not filled through depth six has distance at least seven (possibly infinite), which certainly excludes distance at most two. If every legal pair has such a lower-bound witness, or another verified distance-at-least-three witness, that refutes m(T)<=2 even though exact m(T) and VH-exists remain unresolved. Resource interruption before a needed layer is complete is inconclusive. Shortest-path witnesses cannot be required for capped starts with no path found; those need lower-bound certificates instead.

These are checker and reporting requirements, not a request for a new census. The local A_rho page above is available for Long Table's tile review without running a larger belt search.

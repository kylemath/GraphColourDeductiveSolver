# Independent WP18 and belt review

4 October 2026, following the user's instruction to carry out this chat's share of the coordination plan. This reviews Long Table's existing WP18 outputs and the available hand-proof pieces. It launches no new phase, census or large belt search. It imports no WP18 producer or team checker code.

## WP18: the bounded candidate really fails

**Independently verified: m(T)=3 for order 17 graph 1.** The checked graph has twelve degree-five roots and all five fans are legal at each, giving 60 pairs. Independently enumerating every proper deletion colouring, applying each fan constraint, and searching the mixed-move graph reproduces every reported start count and distance histogram on this graph. There are 786 distinct admitted starts across the twelve roots. At each root the five maximum lengths have sorted profile (3,3,4,4,4). Hence the minimum over pairs of the maximum over starts is exactly three.

This establishes both parts needed for the stated counterexample: every legal pair admits a start that cannot fill in two moves, and at least one pair fills every admitted start within three moves. It refutes the candidate m(T)<=2. It does not refute VH-exists, which allows an arbitrary finite number of moves.

## Existing phases: certificate replay

| Phase | Graph identities checked against declared input | Supplied witness paths replayed and shortestness checked |
|---|---:|---:|
| P1 | 22 | 1,083 |
| P2 | 96 | 6,294 |
| P3 | 192 | 13,271 |
| P4 | 651 | 46,687 |
| Total | 961 | 67,335 |

Every graph rotation passes simplicity, connectivity, triangular-face, spherical Euler and minimum-degree checks. Every report covers exactly its independently enumerated legal vertex/fan pairs, and the fan chords match those pairs. The graph lists exactly match the saved P1/P2 manifest and P3/P4 input files. Nine entries in the WP18 source/output manifests match their hashes.

Every supplied witness has the right hole, a proper allowed colouring, bichromatic fan chords, legal whole-component swaps/slides and a filled endpoint. For a path of length L, the independent checker exhausts all earlier layers through L-1 and finds no target. Thus these witnesses have their reported exact distances, including distances three and four outside the counterexample graph.

The independent verifier rejects missing pair coverage, wrong fan chords, invalid colour values, an extra hole, an illegal slide and a wrong graph hash. A valid path padded by an inverse pair is detected as non-shortest.

**Limit of this replay:** on the other 960 graphs, the witness lower bounds are independently checked, but every histogram entry and every start was not re-enumerated. A checked worst witness proves a lower bound on the row maximum; its successful path does not prove that all other starts meet that same upper bound. The saved phase histograms and their min/max arithmetic are consistent, but the global claims “only one graph has m=3” and “all starts fill within four moves” still depend on producer completeness/upper bounds outside the named graph. Do not describe this witness replay as a complete independent replication of all phase statistics.

Code and structured output:

- `backgroundMaterial/planemap-structural/longtable/audit/wp18_independent.py`
- `backgroundMaterial/planemap-structural/longtable/audit/wp18-independent-results.json`

## Producer and checker review

The core's move model is coherent on valid inputs: the hole is part of the state, fan chords constrain starts only, swaps use a complete component in the current deletion, and slides require a unique link colour. First-occurrence colour normalization preserves properness and reachability. The breadth-first search is appropriate for mixed-move distance. Repeated starts are memoized with the hole retained. Independent full replay on 17:1 confirms these mechanics for the decisive graph.

The existing team checker provides useful upper-path and depth-one checks; its separate kill check covers depth two for 17:1. It does not generally certify exactness above two, input structure, all pair coverage or full start-family enumeration. The new independent verifier supplies graph/pair checks and exactness of the supplied witnesses without changing that team-owned checker.

There are remaining implementation/contract issues before a harder future run:

1. **Hard resource limits are not enforced as declared.** The deadline is checked between starts, outside deletion enumeration and each individual BFS. A single large enumeration or BFS can exceed the per-graph/phase deadline. The producer does not enforce the 8 GB memory or 200 MB output limit. The current runs were short; this is a future-run risk, not evidence these results are false.
2. **Interruptions lose partial counts.** `Interrupted` discards the current graph report rather than preserving the declaration's promised partial counts. Resource interruption is correctly not labelled a pass, but the output contract needs reconciliation.
3. **Empty fan start families lack defined semantics.** The core initializes a maximum at -1, which can become m=-1 if a family is empty. Existing reports have positive start counts. Future code must explicitly record emptiness or justify nonemptiness without silently taking a vacuous numerical maximum.
4. **Capped and source-bound outputs need precise labels.** A complete depth-six exclusion gives a lower bound at least seven, possibly infinity. It can help refute a bound of two; it does not refute unbounded reachability. Outputs name a declaration file but do not embed its content hash or execution source hashes. Include those bindings in the next version rather than relying only on nearby manifests.

Do not silently repair a committed historical producer and call old outputs results of the new version. Version the changes and freeze any proposed further experiment separately.

## Belt review: the local tile closes, opening coverage remains

The new `unequal-a-rho-tile-audit.md` closes its stated local transition. The existing A_tau and surviving B notes give explicit links and singleton checks, and the equal-pole star argument is coherent. None of those local lemmas alone covers every unequal-pole start.

The cap note's opening assumes the hole-edge v_(n-1)v_0 has colours {rho,tau} and the doubled boundary colour is rho or tau. A symbolic five-position classification gives **14** proper four-colour link patterns under unequal poles a=0,b=1:

| Doubled colour | Number of local patterns | Covered by that opening premise? |
|---:|---:|---|
| 0 | 8 | No: one of the lower neighbours carries the pole-a colour |
| 1 | 2 | No: the two upper neighbours carry the pole-b colour |
| rho or tau | 4 | Yes |

These are not merely hypothetical local words. Independent enumeration on the already published named G5 regression yields proper whole-deletion examples of the omitted doubled-0 and doubled-1 classes. In vertex order (a,b,u0,u1,u2,u3,u4,v0,v1,v2,v3,v4), with 4 denoting the hole:

- Doubled 0: (0,1,4,1,2,1,3,2,0,3,2,0), link (0,1,2,0,3).
- Doubled 1: (0,1,4,1,2,3,1,2,3,0,2,3), link (0,1,2,3,1).

Both are proper. They are gaps in the stated opening coverage, not counterexamples to the proposed belt theorem. An assembled proof must either fill them directly or transform them into a prepared state with explicitly legal moves.

The run-length argument and tile transitions can support termination if the joined proof defines a linear interval of unprocessed original belt vertices between the current prepared zero and the cap. Ordinary A/B returns move strictly forward by two/three indices, with the same trailing colour. One must prove those moves do not alter the unprocessed interval or the fixed cap, and handle the final overlap before applying the cap note. A decreasing cyclic index by itself is not a well-founded measure. Treat n=5 overlaps explicitly; the long-cap configuration is impossible there because its two claimed zero vertices are adjacent.

No joined proof page was available at the start of this review. This is a review of the existing components and the obligations its author must discharge, not a rejection of an unseen assembly. The pole-hole case also needs the exact Florek statement and a proper target restriction; that external theorem was not independently reverified here. Do not claim historical novelty without a literature check.

Local classifier and named examples:

- `longtable/audit/belt_opening_review.py`
- `longtable/audit/belt-opening-review-results.json`

## VH-exists and its two lemmas

The useful quantifier order is: for every minimum-degree-five spherical triangulation, **there exists a degree-five vertex and a legal fan**, after which **every admitted colouring** must have a finite mixed path to some target hole. The pair is selected before the colouring. Slides may leave that vertex and change hole degree. A claim selecting a different pair after seeing each colouring is weaker and does not supply that pair for the stated induction.

This hypothesis suffices for the hand induction. Add the selected legal fan to T-v, obtaining a smaller simple triangulation; colour it by induction on order; restrict to T-v; use the assumed path and fill whichever hole reaches a three-colour link. Degree-three/four reductions handle the other cases. The hypothetical path is used once on T, not recursively on a moved hole of the same order.

**Containment lemma:** deleting the fan chords splits, but never joins, bichromatic components. A component swap in T-star is the product of swaps on its constituent components in T-v. All are on the same colour pair; swapping one preserves membership in that pair, so it does not change the component partition used for the remaining swaps. Therefore reachability in the deletion is constant on each T-star Kempe class. This observation does not prove that any such class contains or reaches a target.

**Apex singleton lemma:** in a proper fan colouring, its apex is adjacent to its two cycle neighbours and, by the fan chords, the other two link vertices. Its colour therefore differs from all four other link colours. It is unique, making the first slide onto the apex legal. That slide need not fill or preserve a degree-five hole.

Both statements are valid hand arguments with these scopes. They do not resolve VH-exists or turn a chosen-fan two-move obstruction into an unrestricted vacancy counterexample.

## Handoff

Long Table should use the missing-opening examples in the belt assembly, preserve the independent m=3 counterexample, and distinguish checked witness shortestness from fully replayed histogram maxima. Math owns acceptance/formalisation; the Proof Navigator owns status updates. No navigator files or Long Table producer/declaration files were edited by this review.

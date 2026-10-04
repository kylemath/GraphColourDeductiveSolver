# Mass-macro corpus: first execution report

4 October 2026. Math and scale-up team. This is a finite experiment and an independently checked witness report, not a Lean proof of uniform descent, selection, Four Colour or complexity.

## Result

The exact two-swap formula was checked on all **118** recorded minimum-degree-five triangulations through order 20, at all **1,586** degree-five roots and all **244,051** proper-colouring orbits. At **12 roots**, some non-target colouring has no decreasing macro of length at most two. All **118 graphs retain at least one passing root**. No existential mass-macro counterexample was found.

There are **21** stuck colouring orbits at those twelve roots. All-root descent fails on six graphs; it holds on every root of the other 112 tested graphs. Strict one-swap descent fails at 1,172 roots. No deletion-colouring family was empty.

These statements have different quantifiers: the all-root/S0 guarantee fails, while `for every T, some degree-five r has Good(T,r)` survives this finite range. No structural selector has been evaluated by this report. In particular, it does not declare S1 or any Long Table rule successful.

## All two-swap root failures

Graph indices are zero-based in the original Plantri ASCII order.

| Order | Graph index | Failing roots | Passing-root count | Total degree-five roots |
|---:|---:|---|---:|---:|
| 17 | 0 | 4, 6, 9, 14 | 8 | 12 |
| 17 | 3 | 3, 13 | 10 | 12 |
| 20 | 7 | 7, 11 | 12 | 14 |
| 20 | 60 | 3 | 12 | 13 |
| 20 | 62 | 15 | 13 | 14 |
| 20 | 63 | 3, 15 | 13 | 15 |

At order 20, graph 36, **all twelve degree-five roots pass mass-macro descent**, including root 8. This differs from the label-sensitive sigma-plus-beta observation game. The latter's seven good exterior roots are not the selection objective for this formula.

## First witness

Order 17, graph 0, root 4 is the first failing root in ascending corpus/root order, not a claim of global minimality beyond the enumerated range.

```
ASCII:
17 bcdef,afghc,abhid,acijke,adklf,aelmgb,bfmnh,bgnoic,chojd,diopk,djpqle,ekqmf,flqng,gmqpoh,hnpji,jonqk,kpnml

vertex order:
[0,1,2,3,5,6,7,8,9,10,11,12,13,14,15,16]

colouring:
[0,1,2,3,2,0,3,1,0,1,0,3,1,2,3,2]

(p,q) = (1,143)
R = (6*17^2+1)*1 + 143 = 1878
```

There are nine legal first moves, four distinct canonical intermediate colourings, and 34 second moves across those intermediates. Every resulting rank is at least 1878. The witness includes all component descriptions, intermediate colourings, successor colourings and ranks. Interior components are included, and second-step components are recomputed.

The immediate new adversarial fixture for a mass-descent selector or structural explanation is **order 17, graph 0**, including its four bad and eight good roots. Graph 36 remains a regression fixture; its mass check is entirely successful. Do not increase macro length merely to make the new fixture pass.

## What was executed

`mass-macro.py` uses Python's standard library only. It verifies exact file hashes against `search-results.json`, matches every graph's ASCII record, validates simple connected rotations with triangular face orbits and Euler counts, and enumerates proper colourings up to global colour renaming. Counts at each root agree with the prior reachability census.

For each colouring it enumerates all nonempty bichromatic components across all six unordered colour pairs, canonicalizes each swapped colouring, and verifies closure and reversibility. It evaluates the specified rank directly. A failed one-step state is checked against every two-step successor through the complete one-step move graph. This checks a bounded macro; no target-distance or attractor table supplies the formula.

The finite enumeration harness can take exponential work as the graph grows. Its runtime is not the complexity of the proposed solver. The reported roughly 19-second execution on this host is descriptive, not a benchmark or asymptotic bound.

Regression fixtures passed before the sweep: all twelve icosahedron roots have twenty colouring orbits and one-swap decrease from every non-target; graph 36/root 8 has 198 orbits, 131 non-targets, exactly three one-swap stuck orbits, first lex rank `(1,190)`, and no two-swap stuck orbit.

## Independent checks

`mass-macro-independent-check.py` imports no sweep functions and does not repeat the colouring census. It independently validates every saved root-failure witness using a different component traversal and canonicalization implementation. It checks all six pairs, all components, properness, ranks, intermediate recomputation and completeness of the recorded one-/two-step layers.

All twelve witnesses passed. All 24 global colour permutations preserve each witness's rank and canonical successor sets. Reversing the deletion-vertex order preserves the rank. These are implementation regressions, not a substitute for the mathematical invariance argument Long Table owns. The reviewer also independently validates the 118 stored rotations and reviews the fresh-colour DSATUR orbit enumeration argument.

This does not independently enumerate all passing roots a second time. Passing-root counts rely on the sweep's complete orbit enumeration, its closure checks, prior per-root orbit counts and reviewed algorithm. The precise limit is intentional.

## Published files and consumer contract

All research files are in `backgroundMaterial/planemap-structural/`:

- `mass-macro.py`: portable sweep/checker, `--input-dir`, `--output`, `--regression-only`.
- `mass-macro-results.json`: completed per-graph/per-root table and every failing-root first witness.
- `mass-macro-independent-check.py`: portable independent witness checker.
- `mass-macro-independent-check.json`: independent verification and checker/input hashes.
- `mass-macro-SHA256SUMS`: manifest for these owned files and this report/acceptance.

The results JSON has `scope`, operational `status`, `formula_version`, `macro_bound`, `checker_sha256`, `input_hashes`, `regressions`, `orders`, `totals` and `existential_kill_witness`. Operational status describes whether the program completed; it is not a navigator theorem status. Within each order, `graphs_checked` records `graph_index`, `ascii`, `ascii_sha256`, `degree_five_roots`, `passing_roots`, `failing_roots` and per-root `roots`. Each root records vertex order, boundary order, orbit counts, one-/two-swap stuck counts and `outcome`. A failing root also contains `failure_witness` with all first moves and all second moves from each distinct intermediate.

The ASCII hash is UTF-8 of the exact graph line **without a newline**. Whole-file hashes are distinct. Input files were consumed as recorded; no Plantri generation or extension past order 20 occurred. Consumers should verify the report/checker/input hashes before classifying rules.

The dedicated manifest avoids overwriting the shared `SHA256SUMS` while other teams may own updates. It can be merged into that shared manifest by agreement after review.

## Handoff and next work

Long Table can now build its adversary from this table and evaluate its predeclared S0 and S1 sets without repeating the census. Descriptive statistics stay on orders 12–18; newly discovered rules must be frozen before holdout evaluation. S2 remains deferred until its required proofs and redistribution rules exist.

The navigator can record the completed finite sweep, preserve the universal parent's open status, and attach the twelve root witnesses. A new all-root formulation must not be confused with the existing killed one-swap node or the existential target.

The math team's next contribution is support transport and a structural reading of the first failure. Root failure identifies where this mass formula cannot supply two-step descent; it does not refute the general root-existence statement, Four Colour, or bare reachability. No macro length change or new observation is proposed here.

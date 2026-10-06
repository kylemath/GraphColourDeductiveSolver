# d1_check.py (WP20 independent checker)

Written from `WP20-D1-declaration.md` and `WP20-output-format.md` only; standard library only; no producer code read.

    d1_check.py OUTPUT.json PLANTRI_STDOUT DECLARATION.md [--workers K] [--all]
    d1_check.py --selftest ORDER [--plantri PATH] [--workers K]     (ORDER <= 18)

Checks: declaration/input SHA-256 (and the pre-registered order-25/26 input hashes), ascii lines, the degree-5 vertex list of every graph, totals of counts versus witness lists (all graphs), then a from-scratch recomputation of every statistic for the check set (sep_bad/d1/p/non-complete graphs, the 2% hash sample, or everything with `--all`), and an independent re-verification of every witness. Exit 0 only with no mismatch.

Two code paths: BULK (bitmask colour classes, union-find over all colourings of `T-x` and of every `G_j`) computes statistics; WITNESS (plain colour lists, plain BFS/DFS) re-verifies witnesses, including depth by BFS and P-kills by full component enumeration. Witness sets for checked graphs are compared as sets with the checker's own lists (assumes the producer lists every witness unless `truncated`).

## Self-test (all pass, run with the plantri 5.8 binary)
- Order 16: 3 graphs, 0 SEP-bad. Reproduced.
- Order 17: 4 graphs, 8 SEP-bad (4 at graph 0, 4 at graph 1), all depth 1, 32 locked classes (10 and 22). Reproduced. D1 kills, P kills and capped: 0.
- Order 18: 12 graphs, 0 SEP-bad. Reproduced.
- Mutation test (built into `--selftest`): a clean synthetic output is accepted; with one corrupted count (`locked_classes`) and one corrupted witness (wrong depth) both are reported; a corrupted `input_sha256` is reported. At order 16 and 18 (no SEP-bad witnesses) the witness mutation inserts a bogus witness.
- Speed: about 0.3 s per order-18 graph (analysis plus witness path) on one core.

## Ambiguities (reading implemented in brackets)
1. Depth: the declaration says a state at distance k that is "separable or filled"; the format says "good" (unfilled, legal admitting fan, separable). [Implemented format: good; filled states are traversed but never a target. This agrees with D1's definition of good neighbour and with "depth >= 2 is a D1 kill".]
2. `p_capped` unit is not stated. [Number of unfilled states lying in capped components (> 200,000 states); `p_kills` excludes them; vertex status `capped` iff p_capped > 0.]
3. `d1_kills`, `p_kills` count states (not classes); `d1_kills` = sep_bad minus depth-1 count. Witness lists are assumed to contain every such state.
4. Kempe swaps with an absent colour (a single vertex moved to an unused colour) are counted as swaps, both in `T-x` and in `G`. Neighbours equal to the state up to renaming are allowed (self-loops, harmless).
5. `locked_classes` is taken over all colourings of `G_j`, including those whose restriction to `T-x` is filled or has no admitting fan, as the schema defines it.
6. `legal_fans` indices j refer to positions in the ascii rotation at x as printed (first listed neighbour is r_0).
7. `depth` keys/values may be strings; integer witness depths are compared as strings.
8. Interrupted vertices/graphs: partial counts cannot be recomputed. [They put the graph in the check set, are reported as unresolved, are not compared count for count, and do not by themselves set a non-zero exit; a producer `status` of `complete` or `capped` that differs from the checker's is a mismatch.]
9. "Refuses an output whose declaration hash differs from the committed version": the checker compares against the declaration file it is given, not against git.
10. P uses the full pure Kempe graph including `no_legal_fan` states and filled states (as the format states); D1/P kill counts of an unfilled state with no legal fan are thus P-only.

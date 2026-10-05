# WP18 results: fan-selection length m(T), orders 12–22

Long Table, 5 October 2026. The run followed `WP18-fan-selection-length-declaration.md`, after the math team's go-ahead (relayed by the user). The source was committed before any phase ran (`3fce037`; P4 added in `12ca2ba`). Each phase is a single pass, with no tuning. This file reports facts only: a producer run checked by an independent checker, not yet replayed by the math team.

## Summary

- **The candidate "m(T) ≤ 2 for every T" is killed by order 17, graph 0-indexed 1 (17:1), in P1.** At all 60 pairs (v, τ), some start needs at least 3 mixed moves. Every degree-5 vertex has the same profile: L = 3, 3, 4, 4, 4 over its five fans. A separate depth-2 search (`wp18_kill_check.py` → `kill-check-17-1.txt`) confirms that each recorded worst start has no fill within two moves.
- 17:1 is the **only** graph among the 961 checked with m(T) = 3. Every other graph on orders 12–22 has m(T) of 1 or 2.
- **No start anywhere needs more than 4 moves.** Across every (v, τ) of every graph, the longest fill is 4. Nothing hit the cap of 6, and no graph was interrupted.
- The smallest graph with m(T) ≥ 2 is order 14 (the gyroelongated hexagonal dipyramid), as expected from the hand check.

| Phase | Orders | Graphs | m = 1 | m = 2 | m = 3 | Longest start | Witnesses replayed | Wall time |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| P1 discovery | 12, 14–18 | 22 | 10 | 11 | 1 (17:1) | 4 | 1,083 | 0.2 s |
| P2 secondary (spent holdout) | 19–20 | 96 | 22 | 74 | 0 | 4 | 6,294 | 0.8 s |
| P3 holdout | 21 | 192 | 46 | 146 | 0 | 4 | 13,271 | 2.2 s |
| P4 optional | 22 | 651 | 105 | 546 | 0 | 4 | 46,687 | 10.7 s |

The pairs (v, τ) by L, and the starts by fill length ℓ:

| Phase | L=1 | L=2 | L=3 | L=4 | ℓ=0 | ℓ=1 | ℓ=2 | ℓ=3 | ℓ=4 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| P1 | 312 | 923 | 108 | 52 | 11,088 | 28,242 | 6,384 | 438 | 78 |
| P2 | 241 | 5,463 | 825 | 6 | 109,581 | 270,498 | 63,363 | 1,137 | 6 |
| P3 | 299 | 11,268 | 1,937 | 66 | 302,998 | 768,672 | 192,567 | 3,528 | 90 |
| P4 | 703 | 38,885 | 7,657 | 145 | 1,416,003 | 3,550,335 | 878,445 | 14,490 | 222 |

Start counts are per (v, τ), so a colouring that is proper on several fans is counted once for each fan.

## What this does and does not say

- It **kills** one bounded candidate: that a well-chosen (v, τ) always fills within two mixed moves.
- It does **not** test VH∃ or the vacancy hypothesis, which cannot fail on these orders (every Kempe class contains a target there). It says nothing about the Four Colour Theorem.
- "Every start fills within 4 moves" holds on every graph checked, but it was observed after the run. It is not a declared candidate. Testing it would need a fresh declaration and orders above 22.
- 17:1 is also one of the WP11 obstruction graphs: 14 of the 38 all-roots survivors are bad at its roots 7 and 13. Whether its m(T) = 3 has the same cause has not been examined.

## Checks

- Regressions (`wp18/regressions-output.txt`): icosahedron L = 1 at all 60 pairs, with 8 starts each; the order-14 start has ℓ = 2; all 3 malformed witnesses are rejected.
- The independent checker (`wp18/wp18_check.py`, which does not import the producer) replayed **67,335 witnesses** with zero failures (`wp18/check-output.txt`). For each witness it checks:
  - the start is proper on T − v, with both fan chords bichromatic;
  - every move is legal;
  - the final link uses at most three colours;
  - the path length equals L;
  - for L ≥ 2, no single move fills the start.
- The checker confirms that each recorded worst start is no shorter than recorded only at depth 1, and at depth 2 for 17:1. Exactness of L above 2 elsewhere rests on the producer's breadth-first search.
- Deletion-colouring counts agree with `mass_core.deletion_colourings` (spot check: 68 orbits at 17:1, root 0).

## Files

`wp18/`: the source with `SHA256SUMS-source`, and the outputs `wp18-P1.json` to `wp18-P4.json` with `SHA256SUMS-output`:

- P1 `f12435e3…a5ad`
- P2 `b2bbcdf4…7e2e`
- P3 `2d05db26…5d26`
- P4 `44b69b35…c4cc4`

Inputs: P1 and P2 come from `wp11-run-manifest.json`. P3 and P4 come from `wp17-last-roots/triangulations-min5-{21,22}.txt`, whose hashes match the recorded `plantri -m5 -a` outputs (`5c203958…`, `6137dc19…`).

# 27-studio-positive-config [exploratory] (Mac Studio, 2026-10-07)

Coordinator Jobs A, A2 and B: positive-winding pi-cycles versus configurations and link-degree patterns, and the transport statement T,
at EVERY degree-5 hole of EVERY core triangulation (plantri -m5 -c4) of orders 24, 25 and 26, in BOTH orientations.
Still running at the time of writing (appended later): all 1,267 IPR duals 32-52, the 9 configuration-free bigsample graphs (n = 56-62), and every
configuration-free core triangulation at orders 27 (24 graphs) and 28 (104 graphs), all of which have adjacent degree-5 vertices.

## Engine
- `picyc.cpp`: C++ port of the MacBook's Python (22 `escape.py`, 23 `scan.py`, 26 `lib26.py`); same state, pi, lambda, DL, lock-chain,
  link-free and lock-breaking definitions (header comment). Full enumeration of T - v, pi as a permutation (asserted), cycles, windings, Kempe classes
  by union-find (`--full`), Theorem W 3F - U = -5 sum w asserted per class with a positive cycle, exits from positive cycles, max-flow and Hall ratio for
  five edge variants (a) DL any pair, (b) DL other pair, (c) any state, (d) DL lock-breaking, (e) DL other-pair lock-breaking.
  Configurations: diamond (5555) and 2.122 (one degree-6 centre), K4 - e with non-adjacent tips. Per hole: `linkdeg`, `vrole`, `dist_config`.
- `convert.py` (gentri / plantri ascii / planar code / face json -> picyc lines), `run.py` (sharded, nice 10, 12 workers), `aggregate.py`.
- Build: `clang++ -O2 -std=c++17 -o picyc picyc.cpp`.

## Validation
- Against the MacBook on the SAME gentri lists, orders 17, 20-24: per-graph (w, L) cycle histograms identical (all 2,054 + 7,209 + ... graphs),
  the same positive (graph, hole) set, cycle w/L/most-negative-neighbour identical (run 23), and all 5 transport variants identical in ok/flow/
  capacity/Hall ratio, plus lock-breaking exit counts identical (run 26: 121 classes, 605 checks), 0 mismatches.
- Diamond / 2.122 counts equal the authoritative `studiointel/causal_test.count_occ` on every graph at orders 20-22.
- Relabelling a graph (random vertex permutation, rotated lists) gives identical results.

## Orientation matters (new)
pi is defined with the link read in rotation order, so a graph and its mirror image give DIFFERENT pi-cycles. The gentri lists (and so runs 22-26)
use one orientation per graph that is not plantri's: at order 24 gentri's positive holes are a mix of plantri's and its mirror's (every gentri record
appears in one of the two). Distributions of states, filled states, classes and DL counts are orientation-free; cycle structure is not. All results
below are reported for both orientations (`p` = plantri orientation, `pm` = mirror).

## Results: see `agg-24-26.txt` and `patterns-by-run.txt`; positive holes with full records in `positive-*.jsonl`.

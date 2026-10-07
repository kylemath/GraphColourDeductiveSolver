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

## IPR fullerene duals 32-52 (plantri/.pc orientation; mirror pending): CONFIGURATION-FREE POSITIVE CYCLES EXIST
- 1,267 graphs, 15,204 holes: 32 holes in 28 graphs have a positive pi-cycle (35 cycles, w = +1 or +2; L 14-17). Orders 45-52; all links (6,6,6,6,6).
- All 28 graphs: 0 diamonds, 0 2.122 (authoritative studiointel count_occ), 0 adjacent degree-5 pairs. Conjecture P is FALSE.
- Smallest: ipr#265 (n = 45), hole 43: T - v is ONE Kempe class of 277,960 states (F 175,625), 2,132 pi-cycles, sum w = -84,908 = (U-3F)/5;
  one positive cycle w = +2, L = 14, 11 DL states. Reproduced by the MacBook's Python engine (escape.py + kempe_py.py) exactly. Witness: witness-ipr265-h43.json.
- Full-mode rerun of all 32 holes (positive-ipr-full.jsonl): per-class Theorem W 0 failures, no pi-cycle crosses classes, transport holds in all five
  variants, every positive cycle has a lock-breaking exit to a negative cycle; min Hall ratio (d) 35,701.

## Job E: C1-Gamma and sigma-C at (5,5,5,5,6) and (5,5,5,6,6) holes, orders 24-26, both orientations (`--jobe`, `jobe.py`)
Definitions as NightFloorAtEasyHoles §2 and NightFloorHP2 §2: w_t = third vertex of the face x_t x_{t+1} w_t (not v); for a DL state with repeat j,
R1 if w_j = A, R2 if w_j = B and w_{j+3} = alpha, R3 if w_j = B and w_{j+3} = mu; kmask bit i = x_{j+i} has degree >= 6.
sigma = swap of the {alpha,mu}-component of m = x_{j+1}. sigma-C: pi-cycles joined whenever a DD-step endpoint t has sigma(t) on another cycle; fail = a joined group with sum w > 0.
- Every DL state on every Gamma-cycle is R1 or R3 (never R2, never other); each (type, k) occurs equally often, as Lemma 2 of HP2 predicts. Gamma lengths 20 and 60 (w = 4, 12).
- **C1-Gamma is FALSE** (first: p25 #14805 hole 5, plantri orientation, R3 state at k = 1, sigma image doubly locked on the same Gamma-cycle). Orders 25/26: 8/48 failing R3 states
  of 60/320 per orientation. Two failure kinds: (i) k in {0,1,2} (degree-6 vertex inside {x_j, x_{j+1}, x_{j+2}}): sigma(r) is DL on the SAME Gamma-cycle (most failures);
  (ii) k in {1,3,4}: sigma(r) keeps exactly one lock and lands on another cycle (w from -112 to 0). Full breakdown in jobe-summary.txt / the coordinator message.
- **sigma-C holds**: 0 failing groups at every (5,5,5,5,6) and (5,5,5,6,6) hole, orders 24-26, both orientations (about 11.5 million groups; groups of up to 60 cycles),
  including every hole with a positive or Gamma-cycle. sigma without psi only.

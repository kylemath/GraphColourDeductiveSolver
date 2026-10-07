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

## Job F: sigma-C at every hole (`--sigc`, `jobf.py` -> jobf-summary.txt)
sigma-groups (pi-cycles joined by sigma from every DD-step endpoint, sigma at any DL state) at all 3,950,194 degree-5 hole-runs of orders 24-26 (both orientations),
plus the 64 positive IPR / bigsample holes: about 114 million groups. **sigma-C fails exactly once**: p26 #70869 hole 11 (plantri orientation, link (5,6,5,6,6)),
a group {w = +1, L = 17; w = 0, L = 8} with sum w = +1 in a one-class hole of 782 states (sum w = -94). Reproduced by an independent Python implementation.
Transport still holds there (Hall ratio 80). The mirror orientation has no positive cycle at that hole. Witness: witness-sigC-p26-70869-h11.json.
All 64 IPR/bigsample positive holes pass. Per-pattern max group size and cross-cycle fraction of sigma images: jobf-summary.txt.

## Job G (NightC1Gamma §5): every Gamma-cycle at orders 25-26, all patterns, both orientations (`--jobg`, `jobg.py` -> jobg-summary.txt, jobg-gamma.jsonl)
- Gamma-cycles: 82 (order 25) and 219 (order 26) per orientation, at 20 link patterns; (5,5,5,5,5) has 31 / 91.
- S1: the k = 3 and k = 4 criteria (incl. "otherwise exactly Lock1 / Lock2") hold at all 104 + 360 single-high-vertex R3 states per orientation: 0 violations.
- S2: DL exits are fixed points sigma(r) = r in all cases at order 25; at order 26, 22 per orientation are not fixed points (another R3 state, same cycle), all at k in {0,1,2}.
- S3: Conjecture G fails 5 + 5 (order 25) and 7 + 9 (order 26) times, NEVER at (5,5,5,5,5), (5,5,5,5,6) or (5,5,5,6,6). One Gamma-cycle has no lockless exit at all
  (p25 #20076 h19, (5,5,6,6,6), plantri orientation: a = 0, b = 2). Target cycles are often shared between Gamma-cycles (16 / 56 holes).
- S4: single-lock exits land on excursions with f = 1 and u in {3, 4} (k = 3, 4), occasionally u = 6, 7, 10 at k in {0,1,2}: no local credit, as predicted.
- S5: at (5,5,5,5,5) every lockless exit has f = 3 (350 at order 25, 1,010 at order 26, per orientation).

## Per-class orientation check and Job D (`picyc.new --full`, `jobd.py` -> jobd-summary.txt), orders 12-26, both orientations
- 4,039,276 hole-runs, 4,203,140 classes. Per class: Theorem W 0 failures; no pi-cycle crosses a class; F5 identity sum lambda = |DD| - 2N0 - E2 - 3#tau: 0 failures.
- Orientation: for all 2,019,638 holes the multiset of (class size, F, sum w) is identical in the two orientations: 0 mismatches.
- Job D table (min over classes of 2N0-DD, 2N0+E2-DD, 2N0+3tau-DD, 2N0+E2+3tau-DD per pattern; first failing class per bound) in jobd-summary.txt.
  The full bound has min 0 at every pattern (the floor). F5-type (2N0 alone): (5,5,5,5,5), (5,5,7,5,7), (5,5,5,7,7), (5,5,7,5,8+) and rarer all->=7 patterns;
  F6-type (2N0+3tau): (5,5,5,5,6), (5,5,6,6,6), (5,6,6,6,6), (5,6,5,6,7), ...; E2 also needed: (5,5,5,6,6), (5,5,6,5,6), (5,5,5,5,7), (5,5,5,5,8+), (5,6,5,6,6), ...

## Job H: sigma'-groups (`--jobh`, `jobh.py` -> jobh-summary.txt)
sigma' = every link-free swap from a DD-step endpoint whose result is not DL (= lock-breaking = gluing, NightLockBreaking Lemma 1.2). H1: sigma' only; H2: sigma' plus sigma at R3 endpoints.
- **Both hold everywhere**: orders 24-26 both orientations (3,950,194 hole-runs, about 100 million groups) and all 64 IPR/bigsample positive holes: 0 failing groups.
- Non-trivial: only 1,355 (H1) / 1,581 (H2) of 3.95M holes are a single group; max group 30-111 cycles per pattern at orders <= 26 (5,075 / 46,467 cycles at IPR / bigsample).
- Fraction of DD endpoints with a sigma'-exit to another cycle: 50-58% per pattern at orders 24-26; 73.5% at IPR holes, 81% at the bigsample hole.
- Job F's sigma-C counterexample (p26 #70869 h11) passes H1 and H2.

## Job I: lockless sigma-exits at (5,5,5,5,6) / (5,5,5,6,6) holes, orders 25-26, both orientations (`--jobi`, `jobi.py` -> jobi-summary.txt, jobi-cycles.jsonl)
- Gamma-cycles: min f of a lockless exit's target excursion is 1 (not 3 as at (5,5,5,5,5)); f = 3 in about 85% of exits, f = 1 or 2 otherwise, one f = 5. Targets are always u = 1 excursions.
- Distinct targets: sigma is an involution, so distinct R3 states give distinct lockless images, i.e. distinct u = 1 excursions (holds in the data by construction).
- Lockless exits per Gamma-cycle: a in {5,...,10} for L = 20 and a = 30 for L = 60; always a >= L/4 (min a/L = 1/4, at p25 #16945 h3, p26 #87942 h22).
- Non-Gamma cycles are NOT all nonpositive at order 25: positive non-Gamma cycles exist at these holes (orders 25 / 26: 7 / 20 plantri, 7 / 25 mirror); first p25 #8775 h15 (5,6,5,5,5), L 34, w +2.
  Positive non-Gamma cycles with NO lockless exit: 5 (order 26 plantri) and 7 records (order 26 mirror; one cycle pair duplicated in the hole), none at order 25;
  e.g. p26 #7490 h3 (5,6,6,5,5), L 26, w +2: all 7 DL R3 states have DL exits (5 fixed points); p26 #43605 h3 (5,5,5,6,5), L 14, w +2: 3 DL + 3 single-lock exits.

## Job K (NightF6): A34, F4, Lemma R, sigma-chains at (5,5,5,5,6)/(5,5,5,6,6) holes, orders 25-26, both orientations (`--jobk`; jobk-A34-F4.txt, jobk-records.jsonl)
- A34 holds on every (5,5,5,5,6) Gamma-cycle record (62/62 at k = 3 and at k = 4); it fails on non-Gamma positive cycles (k = 3: 20/37, k = 4: 25/37, first p25 #16298 h23 / p25 #8775 h15).
- F4 holds on Gamma-cycles: f = 3 at all 133 k = 4 lockless exits; k = 3: f in {2 (36), 3 (97)}; k = 0, 1, 2: f = 1 (43), 2 (27), 3 (265), 5 (1). Non-Gamma k = 4 exits have f = 1, 2.
- Lemma R (target remainder 5w(T) - sum over hit excursions of (1 - 3f) <= 0) holds on all 210 targets with w(T) <= 0 (max remainder 0, tight at p26 #56128 h5 and
  p26 #87887 h21 where 30 hits use the whole -240 of a w = -48 cycle). It FAILS on the 4 targets that are themselves positive cycles (w = +2, +2, +2, +4; remainder 12 or 24):
  p25 #16298 h23, p25m #16149 h3, p26m #40549 h3, p26m #75049 h16.
- Every positive cycle at these holes reaches a negative cycle in ONE sigma-hop (13 + 13 + 48 + 53 cycles), including all 12 positive non-Gamma cycles with no lockless exit; their sigma-groups have 4-19 cycles and sum w from -46 to -200.

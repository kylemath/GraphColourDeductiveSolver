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

## Job L (supply numbers; `jobl.py` -> jobl-summary.txt, jobl-cycles.json), (5,5,5,5,6)/(5,5,5,6,6), orders 25-26, both orientations
Debt D = 5w; credit C = sum (3f - 1) over lockless sigma-exits, split by target winding (C_neg: w(T) <= 0, C_pos: w(T) > 0); per kmask [R3 states, lockless exits].
- **Lemma S (C_neg >= D) holds on every Gamma-cycle**: min C_neg/D = 1.55 at (5,5,5,5,6) (62 records; p25m #16945 h3: L 20, D 20, C_neg 31) and 1.80 at (5,5,5,6,6) (6 records).
  Gamma-cycle exits never hit a positive cycle (C_pos = 0 on all 68).
- Positive non-Gamma cycles: C_neg < D in 17/37 (5,5,5,5,6) and 10/22 (5,5,5,6,6) records, min 0 (p25 #16298 h23, p26 #43605 h3, p26 #7490 h3); every one is one sigma-hop from a negative cycle.

## Job M (Gamma-cycles in blocks of 10; `--jobm`, `jobm.py` -> jobm-summary.txt, jobm-gamma-sequences.jsonl)
Each Gamma-cycle (orders 25-26, both orientations) rotated to start at R3@k=4 and cut into blocks of 10 states; every block has exactly one R3 state at each k (0 malformed).
- No dead block (every block has a lockless exit). (5,5,5,5,6): 140 blocks; patterns (bits k = 0..4) 11111 x82, 10111 x14, 00111 x14, 10011 x13, ...
- P(k3 lockless | k4 lockless) = 132/133; P(k3 lockless | k4 fails) = 1/7: the k = 3 and k = 4 exits fail together.
- Block debt is 10. Min block credit is 8 (p26 #87942 h22, pattern 10000), so the per-block form fails; min per-cycle average block credit 15.5 (p25m #16945 h3).
- Failure kinds by k: k = 4 Lock2-only, k = 3 Lock1-only (the proved criteria), k = 0, 1, 2 mostly fixed points (X).

## Job N (NightF6Flow §2.1 one-question lemma; `--jobn`, `jobn.py` -> jobn-summary.txt, jobn-visits.jsonl)
At every R3@k (k = 3, 4) state of every (5,5,5,5,6) Gamma-cycle, orders 25-26, both orientations (62 cycles, 280 visits): p = x_{j+k}, y = w_{j+k-1}, z = w_{j+k}, m = p's third outer neighbour.
- (a) <=> (b): y ~ z in {c(y),c(z)} <=> lockless: 280/280; pm a bridge of G[{v} + c(p) + c(m)] <=> lockless: 280/280; m unique: 280/280.
- (c) p, m, y, z are identical at every visit of a cycle, and the same at k = 3 and k = 4 (62/62).
- (d) |K_{c(p),c(m)}(p)| changes between consecutive same-k visits in 77/78 (k = 3) and 77/78 (k = 4).
- The 14 failing visits (7 per orientation) come in k = 4 / k = 3 pairs two pi-steps apart (except p25 #16945, one each). At a failure the y- and z-components
  split the usual joined component (size 10-12) into two (1+10, 8+4, 9+3, 6+6, 2+10, ...); |K(p)| is 9-11 at failures versus 5-10 at successes of the same cycles.
- The short block (p26 #87942 h22) in both orientations is printed in jobn-summary.txt.

## Job O (pi-step trace of (5,5,5,5,6) Gamma-cycles; `--jobo`, `jobo.py` -> jobo-summary.txt, jobo-steps.jsonl), orders 25-26, both orientations
p = the degree-6 link vertex, y, z its flanking outer neighbours, m its third outer neighbour (fixed per hole). Periods of 10 states start at R3@k=4:
R3k4 R1k1 R3k3 R1k0 R3k2 R1k4 R3k1 R1k3 R3k0 R1k2 (140 periods, no exception).
- (iii) The swap pattern is universal: in all 140 periods the 10 steps swap pairs carrying the colours of (mz, my, pm, pz, py, my, mz, pz, py, pm), and the swapped
  component contains (-, -, pm, -, py, my, mz, pz, -, pm) of {p, m, y, z}.
- (i) y ~ z (fresh colours) fails at 0 states in 125 periods, and at 1-3 states in 15. (ii) Never at two consecutive k = 4 visits (0/140).
- Failure mechanism (13 of 14 failing periods): y ~ z breaks at the step R3k0 -> R1k2 (pair py, component meets none of p, m, y, z), stays broken at R3k4,
  rejoins at R1k1 (step pair mz), breaks again at R3k3 and R1k0 (step pair my), and rejoins at R3k2 (step pair pz). All four steps swap components that avoid p, m, y and z.
  Trace (positions R1k2 | R3k4 R1k1 R3k3 R1k0 R3k2): 0 | 0 1 0 0 1.

## Job P (`--jobp`, `jobp.py` -> jobp-summary.txt, jobp-steps.jsonl), (5,5,5,5,6) Gamma-cycles, orders 25-26, both orientations (140 periods)
- P1: at k = 3 the edges x2x3, x2w1 and x3m (= pm) are each bridges of G[{v} + their two colours] exactly when sigma(r) is lockless (0 exceptions in 140); at k = 4 the same
  holds for x0x4, x0w0 and x4m. At k = 0, 1, 2 NO edge among x0..x4, w0..w4, m has this property (best edge: exactly the failures as exceptions, 20 / 44 / 20):
  the k <= 2 failures are mostly fixed points (19 / 40 / 19: the whole {alpha,mu}-subgraph is one component), a global, not one-edge, condition.
- P1: credit from k <= 2 lockless exits >= 7L/20 on all 62 cycle records, with equality at p25m #16945 h3.
- P2: in the failing periods the y ~ z break is caused by the step-8 (p,y) or step-1 (m,y) swap whose component K cuts y from z inside the {c(y),c(z)} graph
  (K meets every y-z path; 2 resp. 1 vertices of K on a shortest y-z path; |K & K_yz| = 1-5). K never separates y from z in T - K. Every swapped component contains
  the link vertex x_{j+2} (R+3), so dist(K, v) = 1. Restoring steps (0 = (m,z), 3 = (p,z)) swap components meeting one of the two y/z pieces (|K & K_yz| = 1-2).

## Job Q (`--jobq`, `jobq.py` -> jobq-summary.txt, jobq-steps.jsonl): the k <= 2 fixed-point mechanism, (5,5,5,5,6) Gamma-cycles, orders 25-26, both orientations
- "sigma is a fixed point" (the {alpha,mu}-component of m is the whole {alpha,mu}-subgraph) never holds at R3k4 or R3k3; at k <= 2 it holds at 19 / 40 / 19 of 140 R3 visits
  (k = 0 / 1 / 2) and accounts for all but 1 / 4 / 1 of the failures there. 76 of 140 periods have no fixed-point state at all.
- Unlike the y ~ z breaks of Job O, every step that switches the fixed-point predicate swaps a component that MEETS the sigma-component both before and after the step.
- p25m #16945 h3 (tight F012' case) printed in full in jobq-summary.txt: k <= 2 credit 2 + 5 = 7 = 7L/20; total credit 31 against debt 20.

## Job J: order 27, every core triangulation (320,133 graphs), both orientations (`--full --jobh`; jobj-jobd27.txt, jobj-jobh27.txt)
- 10,803,532 hole-runs, 11,304,648 classes: Theorem W, no cross-class pi-cycle and the F5 identity hold on every class (0 failures); the (size, F, sum w) class
  multisets agree between orientations at all 5,401,766 holes. The floor (min of 2N0 + E2 + 3tau - DD) holds at every pattern; (5,5,5,5,6) is still F6-type.
- sigma'C (H1 and H2): 0 failing groups in about 368 million groups.

## Job R: order-27 Gamma-cycle summaries (jobr27/jobr27-summary.txt, jobr27/jobm27-summary.txt; per-job inputs in jobr27/)
- (5,5,5,5,6), 202 Gamma-cycle records: Lemma S holds (min C_neg/D 1.95); one-edge rule 824/824 at k = 3, 4; universal period 412/412; y ~ z never broken at consecutive
  k = 4 visits; F012' >= 7L/20 (min exactly 1, p27 #273919 h26); A34' holds; no dead block; min block credit 8 (p27 #186395 h22); min cycle average 19.5.
  **F4 FAILS**: two k = 4 lockless exits with f = 1 (p27 #133619 h21, one per orientation).
- (5,5,5,6,6), 28 records: **Lemma S FAILS** at p27 #316043 h18 (plantri orientation; link (6,5,5,5,6); C_neg = 18 < D = 20; the mirror has C_neg = 21) and that cycle
  has dead blocks; 16 Gamma-cycles contain R2 states, so the R1/R3 alternation of HP2 Lemma 2 does not hold at (5,5,5,6,6) at order 27.
- Lemma R in the Job K form (hits from every DL R3 state): 12 violations on nonpositive targets (e.g. p27 #68456 h19, w(T) = -2, rem 6). The NightF6Flow form
  (DD endpoints only) is Job S.

## Job T (`jobt.py` -> jobt-summary.txt): period coupling, orders 25-27, both orientations (well-formed R1/R3 periods only)
- (5,5,5,5,6): the smallest window w with min credit >= 10w on every cycle is **w = 2** (orders 25-26: 62/62, order 27: 202/202); w = 1 fails on 1 + 4 cycles
  (min period credit 8, tuple (Lock2, Lock1, X, X, L3) or (Lock2, Lock1, Lock1, X, L3)). Min adjacent-pair credit 31 (25-26) and 39 (27). Caveat: most Gamma-cycles have
  L = 20 (two periods), where the w = 2 window is the whole cycle; only the L >= 30 cycles test w = 2 independently.
- (iii) is false: a k = 4 failure never comes with all k <= 2 visits of periods i, i+1 lockless with f >= 2 (0/7 at 25-26, 0/12 at 27). A k = 4 failure always comes with a
  k = 3 failure (tuple starts "2 1") and at least one non-lockless or f = 1 visit at k <= 2.
- (5,5,5,6,6) at order 27: w = 2 fails at p27 #316043 h18 (the Lemma S failure; periods with credit 0 and 18); 16 cycles are not R1/R3-periodic (R2 states).

## Job S (NightF6Flow §1 by cycle id; `--jobs`, `jobs.py` -> jobs-summary.txt, jobs-records.jsonl), (5,5,5,5,6)/(5,5,5,6,6), orders 25-27, both orientations
Exits = R3 DD-endpoint states of positive cycles with a lockless sigma-image on another cycle.
- Orders 25-26: Lemma R (rem(T) <= 0 on every hit nonpositive T) holds on all 210 targets (max rem 0); no double hits; Lemma P1 single-target assignment exists at every hole.
- **Order 27: Lemma R fails on 12 nonpositive targets**, all at (5,5,5,5,6): p27 #68456 h19 (Lambda(T) = -10, L 38, 2 hits, rem +6, both orientations), and 10 targets with
  Lambda(T) = 0 hit once by an f = 1 exit (rem +2; e.g. p27m #166916 h19, #264388 h4 three times). No double hits. **Lemma P1 still holds at every hole** (single-target
  and splittable), including the one Gamma-cycle with def > 0 (p27 #316043 h18).

## Jobs U and V (independent Python: kempe_py + escape.pi_of; jobuv/)
- **U, the F4 failure p27 #133619 h21** (jobuv/jobu-summary.txt; rotation system and the full colourings of r, sigma(r), pi(sigma r), pi^2(sigma r) in jobuv/jobu-p27-133619-h21.json).
  In both orientations: R3@k=4 state r on the L = 20 Gamma-cycle; K_sigma = {x_j, x_{j+1}, x_{j+2}} exactly (3 vertices); sigma(r) is lockless on the w = -62, L = 314 cycle;
  pi(sigma r) = phiB^-1 gives a filled state whose own move is phiA (M3 short: x_{i+4} is not in the {Y,Z}-component of x_{i+2}), returning at once to an unfilled state: f = 1.
- **V, the Lemma S failure p27 #316043 h18** (plantri; jobuv/jobv-summary.txt). The Gamma-cycle (L 20, w +4) has R3 lockless exits with credits 8 + 8 + 2 = 18 < 20
  (Python reproduces the C++ count), but an **R1 state** on it also has a lockless sigma-exit (into cycle 2, w -84, f = 4, credit 11): counting R1 exits gives 29 >= 20.
  Its sigma-group has 9 cycles and sum lambda -1,470; the (sigma u sigma')-group has 12 cycles and sum lambda -1,490. No R2 state on this cycle (the R2 states are on other
  (5,5,5,6,6) Gamma-cycles). Period pattern: (Lock1, fixed, fixed, L3, L3 | L1, fixed, fixed, fixed, Lock2) over R3 visits.
- **Y, sigma-group accounting at the order-27 Lemma R failures** (jobuv/joby-summary.txt; every excursion of every cycle in the group, hit or unhit):
  p27 #68456 h19 (plantri): group of 8 cycles, sum lambda -420; the positive Gamma-cycle (w 4) has 8 exits (credits 8,8,8,5,5,5,8,8; Cr_N = 55). Target cycle 38
  (w -2, L 38) has excursions (u,f,mass) = (1,3,-8 HIT), (2,2,-4), (17,2,+11), (2,1,-1), (1,3,-8 HIT), (3,1,0): the excess +6 is its own long DL-run excursion (u = 17, +11).
  p27m #166916 h19: group of 16 cycles, sum lambda -580; the positive non-Gamma cycle (w 2, L 22) has one exit (f = 1, credit 2) into cycle 31 (w 0, L 8), whose excursions are
  (1,1,-2 HIT) and (5,1,+2): again the target's own positive excursion carries the +2. In both groups the excess is absorbed by unhit negative cycles (e.g. -80, -60, -535).

## Job X (`--jobx`; jobx-summary.txt): consecutive k = 4 failures on all maximal DL runs at (5,5,5,5,6), orders 25-27, both orientations
- About 101 million maximal DL runs (Gamma-cycles 6 / 25 / 101 per orientation). Pairs of R3k4 visits 10 steps apart inside a run: 45 + 42, 191 + 182, 800 + 750;
  both failing: 1 + 1, 8 + 9, 31 + 23, **never on a Gamma-cycle**. Distance from the second failure to the first non-DL state: max 5 (order 25), 2 / 15 (order 26 / mirror),
  9 (order 27). The single distance > 10 is p26m #21951 h22 (run length 27, failures at positions 2 and 12, the run continues 15 steps). The state leaving DL always has
  Lock1 and loses Lock2 (it is the run end s_u).

## Job AA (independent Python; jobuv/jobaa.py -> jobaa-summary.txt, jobaa-cases.json): the 73 double k = 4 failures of Job X, traced to the run end
- All 73 reproduce. Every second-failure break is the step-8 (p,y) swap whose component avoids p, m, y, z.
- The breaking component meets the Lock2 witness (the {mu,B}-component of m) of the last DL state in 69/73; the 4 exceptions (p27m #162314 h4, #187412 h23 (x2), #260796 h4)
  all have distance 9, last DL state R3k0 and a leaving step that is itself a far (p,y) swap; there the breaking component meets the leaving step's swapped component.
- Rule covering all 73: the second break's component meets the Lock2 witness of the last DL state OR the component swapped by the step that kills Lock2.
- Leaving steps: (m,y) far swap from R1k1 (36), (m,z) far (10), (p,y) far (8), (p,y) through p and y (10), (p,z) far (4), (p,z) through p, z (2), (p,m) through p, m (3).

## Lemma W (Job X addendum; `--jobx` windows, `jobw.py` -> jobw-summary.txt), (5,5,5,5,6), orders 25-27, both orientations
Windows R3k3, R3k2, R3k1, R3k0, R3k4' lying inside a DL run: credit = sum (3f - 1) of their lockless sigma-exits >= 10; W1 = k3 or k4' lockless; W2 = some k <= 2 lockless;
W4 = k4' fails => k3 lockless with f = 3.
- **On Gamma-cycles all four hold with 0 failures** (12 + 12, 58 + 58, 206 + 206 windows).
- On non-closed runs they fail often (order 27, per orientation, of 1,946 windows: credit < 10 in about 510, not W1 389, not W2 149, not W4 about 700). Most failing windows end
  1-2 steps before the run end, but W1 fails up to 12-15 steps before it (p26 / p26m: 12 and 15; order 27: up to 12), so **W1 does not hold on all runs**.

## Charge-back P1 (coordinator refinement; `picyc.w --jobs` with per-exit records, `jobcb.py` -> jobcb-summary.txt), orders 25-27, both orientations
rem(T) > 0 is charged back to the positive sources that hit T (in proportion to credit; exact fractions), def'(Z) = def(Z) + charge; P1 on def' with targets rem < 0.
- **Holds at every hole** (single-target assignment exists; def' > 0 records: 1 + 2, 11 + 13, 25 + 49 at orders 25, 26, 27 per orientation). The 12 rem > 0 targets (all order 27) each have ONE source:
  p27 #68456 h19 (both orientations; source = the Gamma-cycle, credits 16, charge 6) and the 10 Lambda = 0 targets hit once by f = 1 (charge 2 to the single source).

## Job Z (`--jobz`: sigma-exits from EVERY DD endpoint, R1/R2/R3; all patterns; orders 25-27, both orientations; jobz.py -> jobz-summary.txt; jobz-p1fails.txt, jobz-cb-full.txt)
- Lemma S (Cr_N >= D) on Gamma-cycles: **holds at (5,5,5,5,6)** at every order (min 1.8 / 2.0 / 2.0; R1/R2 share of Cr_N about 4%) and **at (5,5,5,6,6)** (min 2.8 at 26, 1.15 at 27:
  the R1 exits repair p27 #316043 h18), and at (5,5,5,5,5) (min 4.0). It FAILS on Gamma-cycles at (5,5,5,5,7) (p25 #13918 h19, p26 #43070 h18, p27 #112605 h26, ...; min 0.5),
  (5,5,5,6,7) (p25 #13918 h15, 0.9), (5,5,5,6,8+) (p26 #6618 h3, 0.9), (5,5,5,7,7) (p27 #247743 h6, 0.75), (5,5,6,6,7) (p27 #197591 h18, 0.5), (5,5,6,5,7) (p27m #131991 h2, 0.85).
- Charge-back P1 with the enlarged exit set: **holds at every (5,5,5,5,6) and (5,5,5,6,6) hole**; fails at 19 holes of other patterns (orders 25 / 26 / 27: 3 / 2 / 14), always on a
  non-Gamma positive cycle, mostly one with NO nonpositive sigma-neighbour (e.g. p26 #70869 h11, the sigma-C counterexample). sigma'C (Job H) still holds at all of them.

## Job AB (`--jobab`, jobab-summary.txt): excursion-level Lemma S at (5,5,5,5,6), orders 25-27, both orientations
Excursion = maximal unfilled run (u) + following filled run (f) on a cycle with filled states; mass = sum of lambda over it; credit = sum (3f' - 1) of lockless sigma-exits
from its own DD states (all R-types).
- **Positive-mass excursions do NOT pay for themselves**: credit < mass in about 48% of them at every order (order 27: 1.82M of 3.73M per orientation), mostly mass 1-2
  (typically u = 4, f = 1, mass +1, whose two DD states have no lockless exit). Almost all failures are on nonpositive cycles (1 / 1 / 9 / 7 / 35 / 83 on positive cycles).
  Min slack -14 to -22 (all exits), -16 to -36 (exits to other cycles only). So self-payment holds only at the cycle / group level.

## Job AC (independent Python; jobuv/jobac.py -> jobac-summary.txt, jobac.json)
- Part 1, the 22 Job Z Lemma S failure Gamma-cycle records: the sigma' lockless credit (link-free lock-breaking exits from DD endpoints, to nonpositive cycles) covers the remaining
  deficit D - Cr_N(sigma) in only 8/22 (p27 #154296 h25: three Gamma-cycles with no sigma' lockless credit at all). But on the (sigma u sigma')-group (12-52 cycles,
  sum lambda -545 to -1,235) the charge-back single-target P1 (exits = distinct lockless sigma and sigma' images) **holds in 22/22**.
- Part 2, (5,5,5,5,7): all 406 Gamma-cycle records (orders 25-27, both orientations) have the universal period R3k4 R1k1 R3k3 R1k0 R3k2 R1k4 R3k1 R1k3 R3k0 R1k2 (k = position of the
  degree-7 vertex), as at (5,5,5,5,6). R3 exits: k = 3 failures always Lock1-only (79), k = 4 failures always Lock2-only (79); k = 4 lockless f = 3 in 796 of 837
  (f = 1: 29, 2: 6, 5: 6); k <= 2 failures mostly fixed points (66 / 110 / 66) plus other DL images (29 / 48 / 29).

## Job AD (`jobad.py` -> jobad-summary.txt, jobad-records.json): the P1 neighbour profile at (5,5,5,5,6)/(5,5,5,6,6), orders 25-27, both orientations
Positive cycles with def'(Z) > 0 (charge-back form; exits from all DD endpoints): 75, none of them Gamma-cycles.
- (i) min over Z of max_T |rem(T)| / def'(Z) = 1.25 (p27m #167230 h23: def' 20, best neighbour spare 25); next 2.0 (p27m #204626 h4), 4.0, 4.75; 56 of 75 have ratio >= 20.
- (ii) every one has a nonpositive sigma-neighbour with w(T) <= -2 (75/75).
- (iii) in a greedy single-target assignment at most 2 positive cycles share a target; the tightest spare left is 5 (p27m #167230 h23).
- (iv) 39 of the 75 have NO lockless exit into a nonpositive target at all (def' = Lambda; e.g. p26 #68224 h23, p27m #167230 h23), so a canonical "first exit" target does
  not exist for them; their assignment goes to a sigma-neighbour that is not an exit target. Of the 36 with such exits, in 27 EVERY exit target can take def'(Z) alone and in 9 NONE can
  (the deficit must go to another sigma-neighbour). (Exits are recorded in state-index order, not pi-order.)

## Job AE (independent Python; jobuv/jobae.py -> jobae-summary.txt, jobae.json): lock-membership form (NightLemmaS §5.1), Gamma-cycles at (5,5,5,5,6) and (5,5,5,5,7)
Orders 25-27, both orientations: 264 + 406 Gamma-cycle records. Lock1/Lock2 components = {mu,A}/{mu,B}-components of x_{j+1}; J = y ~ z in {c(y),c(z)}.
- (iii) On Gamma-cycles the Lock1- and Lock2-components always have >= 6 vertices (both patterns).
- (i) After a step-8 break (19 at degree 6, 79 at degree 7), z enters the Lock2-component two states later by a (z,M)-coloured swap whose component avoids p, y, z and M
  (98/98). One period later z is in the Lock2-component in 19/19 (degree 6) but only 65/79 (degree 7): the 14 others are periods followed IMMEDIATELY by another step-8
  break, which never happens at (5,5,5,5,6). These consecutive breaks occur only in the plantri orientation (5 holes = the plantri Lemma S failures at (5,5,5,5,7));
  the 6 mirror-orientation failure holes have none.
- The Lock2-component meets the breaking component K at every state of the following period (all breaks; 70/79 at one state for degree 7); the Lock1-component meets K
  from the first state after the break on.
- (ii) At (5,5,5,5,7) all 79 k = 3/4 failure pairs come from the same step-8 far break (pair (p,y) or (p,y,M), component avoiding p, y, z, M). The failure rate is
  79/916 = 8.6% of periods against 19/552 = 3.4% at (5,5,5,5,6) (about 2.5x, not 10x); |K step 8| (mean 6.7 vs 6.5 in break periods) and |K_yz(y)| at R3k0 (12.3 vs 12.1)
  do not differ, so neither explains the rate.

## Job AF (NightP1 §6 requests; independent Python jobuv/jobaf.py, jobaf34.py -> jobaf-summary.txt, jobaf34-summary.txt, jobaf.json)
- (1) On the 19 Job Z charge-back P1 failure holes (all patterns; earlier misreported as 22): undirected-sigma P1 holds at 11/19, and sigma u sigma' P1 (sigma and sigma' lockless
  exits, undirected sigma u sigma' neighbours) at **19/19**. Undirected sigma fails at p25 #12342 h24, p26 #70869 h11, p27 #72051 h14, #87651 h19, #97821 h7, #130462 h20,
  p27m #110656 h16, #183181 h22.
- (2) (5,5,5,5,6)/(5,5,5,6,6), orders 25-27, both orientations, 407 holes: P1 with undirected sigma neighbours 407/407; **P1^str on non-Gamma positive cycles 407/407**;
  P1^str including Gamma-cycles 391/407 (the 16 failures are holes with 2-4 Gamma-cycles of L = 20-60 sharing targets, e.g. p26 #87887 h21, p27 #186398 h18).
  Star over 413 sigma-groups with a positive cycle: (i) M adjacent to every positive cycle 386; (ii) -Lambda(M) >= supply 409, with -rem(M) 393; Star 386; Star_rem 372.
- (3) p27m #167230 h23 (rho = 1.25): Z29 (w 4, L 28) = two excursions (u 13, f 1, mass +10), no lockless exit; T21 (w -5, L 111) has 23 excursions incl. positive ones
  (17,2,+11), (10,1,+7), (4,1,+1). All links between them (sigma and sigma', both directions) are single-lock or DL; they land in T21's (10,1,+7) and (3,2,-3) excursions.
- (4) The 15 (5,5,5,5,7) Lemma S failure records: Lemma W fails on every one. In every period k = 2 and k = 1 are fixed points. Plantri: a period (Lock2, Lock1, fixed, fixed,
  fixed) of credit 0 next to (Lock2, L3, L2, fixed, fixed) of credit 13. Mirror: (L1, Lock1, fixed, fixed, fixed) of credit 2 (k = 4 lockless with f = 1, k = 3 fails) next to
  (Lock2, Lock1, fixed, fixed, L3) of credit 8.

## Job AG (Lemma Fix; independent Python jobuv/jobag.py -> jobag-summary.txt, jobag.json), Gamma-cycles at (5,5,5,5,6) / (5,5,5,5,7), orders 25-27, both orientations
At every R3 state with k <= 2 ({alpha,mu} = {c(x_j), c(x_{j+1})}, {A,B} the other pair):
- (a) sigma is a fixed point <=> the {A,B}-subgraph of T - v is acyclic: **0 exceptions** (220 + 242 fixed points, all acyclic; all 1,436 + 2,506 others have cycle rank >= 1).
- (b, d) At (5,5,5,5,6) the {A,B}-subgraph induced on the ring (x_0..x_4, w_0..w_4, m) and on the 2-ball around v is ALWAYS acyclic at k <= 2 (1,656 states): the A/B cycles
  that prevent fixed points are never inside the 2-ball, so no period has a ring/2-ball A/B cycle. At (5,5,5,5,7) a ring (and 2-ball) A/B cycle appears at some k <= 2
  lockless state in 668/916 periods (1,306 states); none at fixed points.
- The 15 (5,5,5,5,7) Lemma S failure records: at k = 1, 2 the fixed points have cycle rank 0 in T - v, in the ring and in the 2-ball (no A/B cycle anywhere).

## Job AH (independent Python jobuv/jobah.py -> jobah-summary.txt, jobah.json): global cycle ranks along Gamma-cycles at (5,5,5,5,6) / (5,5,5,5,7), orders 25-27, both orientations
Cycle rank (E - V + C) of the {A,B}-, {mu,A}- and {mu,B}-subgraphs of T - v at every state (roles from the state's own j); per-step changes with the swap type.
- (ii) At (5,5,5,5,6) the {A,B} rank at positions 4, 6, 8 (R3k2, R3k1, R3k0) is NEVER (0,0,0) (0/552 periods); min rank(4)+rank(6)+rank(8) = 1 (p25 #16945 h3). At (5,5,5,5,7) it is
  (0,0,0) in 14/916 periods, 12 of them in the 15 Lemma S failure records (32 periods).
- (iii) The per-step rank-change distributions are exactly mirror-symmetric: step i and step 9 - i have negated distributions (steps 0/1, 2/9, 3/8, 4/7, 5/6), at both patterns.
  A step-4 or step-6 drop to rank 0 followed by rank 0 again two states later: 1 (degree 6), 2 (degree 7).
- (i) Periods without a fixed point mostly have constant rank 1; fixed-point periods show rank 0 at positions 6 and/or 8 (and 4). The {mu,A} and {mu,B} ranks reach 0.

## Job AJ (time reversal; jobuv/jobaj.py -> jobaj-summary.txt): orders 25-27, all patterns
States compared as vertex colourings up to renaming. At all 631 holes with Gamma-cycles the two orientations have the same number of Gamma-cycles, and **every one of the 1,364
plantri Gamma-cycles is a mirror Gamma-cycle with the same state set traversed in exactly reversed pi-order** (up to a cyclic shift). 0 exceptions.

## Job AI (jobuv/jobai.py -> jobai-summary.txt, jobai.json): the A/B cycles at R3k2 / R3k1 / R3k0 of (5,5,5,5,6) Gamma-cycles, orders 25-27, both orientations (552 periods)
Cycle basis = fundamental cycles of a BFS forest of the {A,B}-subgraph of T - v (rank 0..3). Cycles have length 6-12; v's side of T - C has 4-5 vertices.
- Fixed points (rank 0) at position 6 are created by step 5 (the (m,y) swap whose component contains m and y) in 99/100, at position 8 by step 7 (the (p,z) swap whose
  component contains p and z) in 60/60. The cycle killed is short (length 6 mostly, some 8) through two consecutive outer vertices w_i, w_{i+1}, avoiding y and z.
- In every period (552/552) some A/B cycle at position 4, 6 or 8 passes through y or z.
- Because the roles {A,B} rotate at each step, no cycle keeps its vertex set as an {A,B}-cycle of the next state: fates are "rerouted" (next rank >= 1) or "dies".

## Job AK (NightW2 §5, §8-§10 tests; C++ `--jobak` on every DL-run window + independent Python jobuv/jobak.py on Gamma periods; jobak-summary.txt, jobuv/jobak-gamma-summary.txt,
## jobuv/jobak-counterexample.json, jobuv/jobak-periods.json (K4..K7 vertex sets per period), jobuv/jobak-66dump.json)
Windows = an R3k2 state followed by four DL pi-steps (to R3k0), at every (5,5,5,5,6) hole, orders 25-27, both orientations.
- **On Gamma-cycles (552 windows) W2*, W2'' and R all hold** (0 failures). **On open DL runs all three FAIL**: of 3,977 / 14,136 / 72,643 windows (orders 25 / 26 / 27,
  per orientation): W2* (R3k2 fixed => R3k0 not fixed) fails 884 / 2,924 / 13,629; W2'' (some A/B cycle through y or z at R3k2 or R3k0) fails 1,334 / 4,729 / 23,390;
  R (w3 not in K_sigma(R3k2) or w0 not in K_sigma(R3k0)) fails 1,707 / 6,125 / 31,569, and where R fails W2'' survives only via an escape outside the 2-ball
  (373 / 1,396 / 8,179). First W2* counterexample: p25 #668 h18 (plantri), an open run of a w = -47, L = 233 cycle where R3k2, R3k1 AND R3k0 are all fixed points;
  verified in Python (rotation system + five colourings in jobuv/jobak-counterexample.json).
- New exact fact: at R1k4, p and x4 are {3,4}-connected in EVERY window (Gamma and open runs, 0 exceptions).
- Where the outside {alpha,mu}-neighbour of y / z sits on Gamma-cycles: at R3k2 mostly z via NightW2's w3 and/or y via a vertex outside the ring; at R3k0 y via w0 and/or z outside.
- Gamma periods: Hypothesis H (rank(k2) = 0 => some {2,3}-cycle at R3k0 meets K7 \ K4) holds in 60/60 periods (76/78 basis cycles); every such cycle meets K4, K5 and the
  pulled-back Lock1@R3k2 chain. Mirror (rank(k0) = 0 => a {3,4}-cycle at R3k2 meets K4 \ K7): 60/60 periods (77/78 cycles).
- F4 periods (60): C5 ({2,3}-cycles after K4, 72 basis cycles, length 6-10) never pass through p, always meet K4 (|C5 & K4| = 1-4), and separate h from a K4 vertex in 32/72.
  Kill cases (48): C8 always meets K7 (|C8 & K7| = 1-4). The 66 rank-sum-1 periods are dumped with rotation systems and the colourings at positions 4-8.

## Job AL (`picyc.al --jobak`, jobal-summary.txt): from each failing window on an OPEN DL run at (5,5,5,5,6) to the run end, orders 25-27, both orientations
Steps from the window's R3k0 to the first non-DL state (1 = R3k0's own pi-image leaves DL). The state that leaves always keeps Lock1 and loses Lock2.
- W2* failures (884 / 2,924 / 13,629 per orientation): distance 1 in about 72%, mean 2.3-2.7, a bump at 11; max 14 / 11 (25), 14 / 17 (26), 29 / 21 (27): NOT bounded uniformly
  (it grows with the order). All three k <= 2 fixed: the same profile (max 14 / 11, 14 / 17, 29 / 21). W2'' failures: max 14 / 11, 14 / 17, 29 / 21.
- Leaving step: about 80% leave at R3k0 itself by the step-8 far (p,y) swap (component avoiding p, m, y, z); the rest by the step-0 far (m,z) swap from R3k4, the near (p,m)
  swap from R1k2, far (m,y) from R1k1, far (p,z) from R1k0, or the near (p,y) from R3k2. No single rule.
- R fails but W2'' survives (373 / 1,396 / 8,179): mean distance 1.9-2.3, max 12 / 12, 14 / 14, 26 / 27: these runs do NOT live longer.
- Note: Studio colourings are stored with CANONICAL colour names (relabelled by first occurrence along the BFS order), so colour letters differ between states for the same class.

## NightW2 §11 addendum (`picyc.al2 --jobak`, jobal-addendum.txt, jobuv/jobal-Ldeath-counterexample.{txt,json})
- Identity total rank = total components - 8 (sum over the six colour pairs of T - v; formal: each edge is in one pair, each vertex in three, |E(T - v)| = 3(n - 1) - 8):
  0 failures over about 635,000 states (positions 3-9 of every window, Gamma and open runs). Min total components at DL states = 8 (total rank 0 attained).
- Lemma L-death (R3k2, R3k1, R3k0 all fixed => the preceding R1k0 lacks Lock1 or the following R1k2 lacks Lock2): never applicable on Gamma-cycles (no period has all three
  fixed), and **FAILS on open runs** in 11 / 711 (25), 35 / 2,376 (26), 106 / 10,813 (27) such windows per orientation. First: p25 #733 h17 (plantri), cycle w -70, L 330,
  positions 3-9 = states 440, 575, 294-chain all DL with R3k2, R3k1, R3k0 fixed (Python-verified; rotation system and colourings in the json).
- Steps back from R3k2 to the last earlier non-DL state in all-three-fixed windows: mostly 1, max 11 / 14 (25), 17 / 14 (26), 21 / 29 (27).

## Job AM (NightA34 §6; independent Python jobuv/jobam.py -> jobam-summary.txt, jobam.json with the vertex sets Z_b, Pi_b, K0, K1, R_b per break)
- Window lemma (§3): the partition of {y, w2, z} in G_J matches the prediction at every DL state at positions 9, 0, 2, 3, 4: 0 exceptions on (5,5,5,5,6) Gamma-cycles (552 periods),
  (5,5,5,5,7) Gamma-cycles (916 periods) and the 73 open double breaks.
- Sigma (K0 u K1 of period b+2 meets (R_b u Z_b) minus the 11 hole vertices): on the 73 open double breaks only **36/73** (predicted 73/73); after SINGLE breaks on (5,5,5,5,6)
  Gamma-cycles 18/19 (predicted mostly empty); at (5,5,5,5,7) single 57/65, consecutive (stay DL) 7/14 (predicted to fail). So Sigma neither holds on the double breaks nor
  separates them from single breaks: it is not the Lock2-killing mechanism.
- Sizes: |Z_b| 1-8 (far part 0-7), |Pi_b| 6-12, |K0| 4-9, |K1| 4-11, |R_b| 2-7 (far part always >= 1; exactly 2 / 1 at degree 6 Gamma).

## Job AN (closing permutation; independent Python jobuv/joban.py -> joban-summary.txt, joban.json), every Gamma-cycle at every pattern, orders 25-27, both orientations
Absolute colours followed through the L Kempe swaps of the cycle (checked against the canonical states); c_L = rho(c_0).
- 2,728 records: rho is a 3-CYCLE for L = 20 (2,544) and L = 40 (136), and the IDENTITY for L = 60 (48); no transposition, 4-cycle or double transposition at any pattern.
  So rho = sigma^(L/10) with sigma the per-period 3-cycle of NightA34 §1.1, and the orbit length in colouring space is 3L unless 30 | L (60, 120, 60).
- At (5,5,5,5,6) (264) and (5,5,5,5,7) (406) rho always fixes c(p) = alpha(R3k2) and rotates the three alpha-free colours.
- Rank vectors (r_AB, r_muB, r_muA at R3k2 | R3k1 | R3k0, named by each period's own R3k2 labels): the period map is NOT constant: v_{b+1} = v_b in 294/552 (degree 6) and
  394/916 (degree 7) transitions; the commonest vectors are (1,0,0 | 0,1,0 | 0,1,0), all-ones and (1,0,0 | 1,0,0 | 1,0,0).

## Job AO (jobao-lengths.txt; jobuv/jobao.py -> jobao-summary.txt, jobao.json)
- (1) Gamma-cycle lengths at ALL core triangulations of orders 12-27, both orientations (from the per-hole (w, L) histograms; Gamma <=> w = L/5): only L = 20 (2,566), 40 (136) and
  60 (48). First at order 17 (L = 20); L = 60 from order 25, L = 40 from order 26. (Not universal beyond the census: the night's adversarial 37-vertex graph has L = 800.)
- (2)-(3) A pi-cycle visits L distinct states, so s(t+20) = s(t) as partitions is impossible for L > 20: the canonical-state period is always L. The meaningful version
  (an orientation-preserving automorphism fixing h mapping s(t) to s(t+d)) has no instance: every hole with an L = 40 or 60 Gamma-cycle (and the L = 20 ones there) has
  trivial such automorphism group (the finder recovers the 5-fold rotation of p17 #4 at its two (5,5,5,5,5) holes). So L = 40 / 60 is not produced by symmetry.

## Job AP (NightA34 §7.4; independent Python jobuv/jobap.py -> jobap-summary.txt, jobap.json)
- (1) R_b & H11 = {x+}: degree-6 Gamma 19/19; degree-7 Gamma 69/79 (10 have two hole gates); open double breaks 73/73 (first break), 63/73 (second).
- (2) Degree-6 Gamma far gates: alpha, in K0, not adjacent to z, in Q_b in 18/19 (1: alpha, K1, adjacent to z, in Q_b). |R_b| = 2 in 19/19.
- (3)/(4) **G2 fails**: degree-7 Gamma double breaks (14, all reaching R3k3^{b+2}): branch 1 in 3, branch 2 in 0, NEITHER in 11. Open degree-6 double breaks reaching
  R3k3^{b+2} (27 of 73): branch 1 10, branch 2 9, neither 8. **16 open degree-6 double breaks reach R3k3^{b+2} with |R_b| = |R_{b+1}| = 2** (first p25 #1557 h16, both
  orientations; p26m #21951 h22; p27 #162314 h4), so that run-local statement is false.
- (5) Control: after every single break on degree-6 Gamma-cycles the far gate is alpha again at R3k4^{b+2} (19/19): branch 2 cannot be excluded by colour alone.

## Job AR (jobuv/jobar.py -> jobar-summary.txt): names of the hole gates R_b & H11 (from jobap.json)
- Degree-6 Gamma single breaks: {x+} 19/19. Degree-7 Gamma single breaks: {x+} 61, {x+, M_z} 4 (M_z = p's middle outer neighbour adjacent to z).
- Degree-7 consecutive breaks (14 records): (first, second) hole-gate sets = ({x+}, {x+, M_z}) 6, ({x+, M_z}, {x+}) 6, ({x+}, {x+}) 2. So "the second break has the extra hole
  gate" holds in only 6/14.
- Open degree-6 double breaks: first break {x+} 73/73; second break {x+} 63, empty 10; all 27 that reach R3k3^{b+2} have {x+} at the second break (none far-only).

## Job AQ (adversarial stress test; jobaq/jobaq.py -> jobaq-raw.txt, jobaq.json; class engine = lib26.Eng, classes from 40 random colourings, seed 1, both orientations)
Holes with Gamma-cycles in run 26's sample: A6_chain h13 (7,7,5,5,5), h31 (5,5,5,5,5); A7_exc h22, h34 (5,5,5,5,7); hog1152_chain h11 (5,5,5,5,5); r5_80b930d1_exc h2 (7,5,5,5,5),
h23 (5,5,5,5,8+). Gamma-cycle lengths there: 800 (A7), 660 (A6 h31), 80, 60, 40, 20.
- **Everything holds on every Gamma-cycle**: Lemma S with sigma-exits from all DD endpoints (C_pos = 0; C_neg / D = 4.0 for the (5,5,5,5,5) and A7 cycles incl. L = 800 and 660,
  i.e. every R3 exit lockless with f = 3; 2.0 at r5 L = 80); sigma-C, sigma'-C (H1) and charge-back P1 0 failures; quarter floor holds for every class.
- Single-high-vertex holes (A7, r5): the universal 10-step period holds on every Gamma-cycle (incl. the L = 800 one, 80 periods); no consecutive k = 4 failures; no period with
  all three k <= 2 fixed and none with k2 and k0 both fixed.
- The L = 800 cycle is at a (5,5,5,5,7) hole, not (5,5,5,5,6): it is not a degree-6 test, and no adversarial graph has a (5,5,5,5,6) hole with a Gamma-cycle.

## Job AS (constructing degree-6 Gamma-cycles with L > 60; jobas/flipsearch.py, jobas-battery*.txt/json, best-*.json graphs)
Graphs = A7_exc + edge flips keeping the core class (min degree 5, max 8, no separating triangle); evaluator = picyc (full enumeration of T - v; n = 37, about 4k-33k states per hole).
- Two flips already give (5,5,5,5,6) holes with Gamma-cycles of L = 80 (e.g. A7 + flips (18,24), (4,14), hole 22; 17 two-flip variants). Hill-climbing flip walks from those
  (6 walks x 300 steps) reach L = 120, 180 and **200** at (5,5,5,5,6) holes (best-walk-best-A7f1-3.json: L = 200 at hole 22; -1: L = 180). All Gamma lengths seen are multiples of 20.
- The full Job AQ battery (all classes from the complete state list, both orientations) on every (5,5,5,5,6) Gamma-cycle with L = 40, 80, 120, 180, 200:
  Lemma S holds (C_pos = 0, C_neg / D 2.45-3.87), the universal 10-step period holds, there are NO k = 4 or k = 3 failures at all (so A34' cannot fail), no W2 / W2* failure
  (no period with all three k <= 2 fixed or k2 and k0 both fixed), sigma-C, sigma'-C (H1) and charge-back P1 hold, and every class satisfies the quarter floor.

## Job AT (NightGammaLength §2 cut parity; jobuv/jobat.py -> jobat-summary.txt, jobat.json)
Edge uv of T - v is CUT by a pi-step when exactly one endpoint lies in the swapped component. Census Gamma-cycles orders 25-27 (2,728 records, all patterns, both orientations) and the
26 Gamma-cycles of the Job AS two-flip constructions (L = 40, 80).
- Every edge is cut an even number of times over the whole cycle: 2,728 / 2,728 and 26 / 26 (the proved lemma).
- At (5,5,5,5,6) every ring edge is cut exactly 4 times and every ring face is met 6 times in every period (census and constructions, 0 exceptions). At (5,5,5,5,7) the larger ring
  has odd counts (3 / 5 cuts on 1,392 of 22,016 ring-edge-periods).
- H_D (D_b = far edges cut an odd number of times in period b is nonempty): every period of every cycle. D_b is the same in every period for 2,548 / 2,728 census cycles (4 / 26
  constructions). **The XOR of D over any odd number of consecutive periods is never empty** (0 records): a cycle cannot close after an odd number of periods, i.e. 20 | L, in all data.

## Job AU [exploratory]: degree-6 k = 3/4 failures live on L = 20 cycles; time-reversal symmetry; which period breaks (jobuv/jobau.py, jobau-summary.txt, jobau.json)
- **(i) Failures by L.** Census (5,5,5,5,6) Γ-cycles at orders 25–27, both orientations: 256 with L = 20, 4 with L = 40, 4 with L = 60. All 19 k = 4 failures and all 19 k = 3 failures are on L = 20 cycles. 18 cycles fail at k = 4 and then at k = 3 two steps later. One cycle fails only at k = 4 and one only at k = 3. L = 40/60 census cycles have no failures and no k ≤ 2 fixed points. The Job AS constructions (L = 40 to 200, 40 cycles) have no k = 3/4 failures, but they do have k ≤ 2 fixed points. On L = 20 census cycles there are 220 k ≤ 2 fixed points. So at degree 6, A₃₄′ is a statement about two-period cycles in all data so far.
- **(ii) Time reversal as a symmetry.** The test used orientation-reversing automorphisms of T fixing h, composed with colour permutation (states compared as vertex partitions). 32 of the 256 L = 20 cycles sit at a hole with such a reflection. 8 of those cycles have the time-reversal property s(t) ↦ s(c − t): p25#5594 h18, p27#133619 h21, p27#274226 h22 and p27#68456 h19, in both orientations. Within one orientation and one graph, two distinct states are never equal as partitions. So "period 1 = period 0 reversed up to colour permutation" is the same test. All 8 symmetric cycles have no break. All 19 breaking cycles are at holes with no reflection at all.
- **(iii) Which period breaks.** The Lock2 witness |K_{μ,B}(x_{j+1})| at the two R3k4 states picks nothing: failing period larger 8, smaller 7, tie 4. The Job N |K_{c(p),c(m)}(p)| at the two k = 4 visits picks the breaking period in 18 of 19 cases, where it is the larger component (12 vs 5, 11 vs 5, 10 vs 5 and 12 vs 10). The exception is p25#16945 h3, mirror orientation, with 9 vs 10. In that visit |K(y)| = 10 and |K(z)| = 1.

## Job AV [exploratory]: absolute-name dump of the degree-6 Γ-cycles for the two-period A₃₄′ analysis (jobav/jobav.py, jobav_summary.py, jobav-cycles.jsonl, jobav-breaking.json, jobav-summary.txt)
- **Dump.** One JSON record per (5,5,5,5,6) Γ-cycle. The census has 256 cycles at L = 20, 4 at L = 40 and 4 at L = 60 (orders 25–27, both orientations). The Job AS constructions add 40 cycles from 40 seeded random colourings of their classes. These match the AS battery lengths.
- **Record contents.** Fixed names come from the hole: p, x⁺, x₂, x₃, x⁻, z, w⁺, w₂, w₃, y and m, with far vertices by graph id. Each cycle starts at R3k4, which is position 0 in NightA34 §1. Colours are absolute: each step swaps the π-move component, and the result is checked against the next cycle state as a partition. Every record replays and closes with 0 errors. Per record: the L colourings, the closing colour map, and the swapped pair and component at every step. Also: K at positions 8 mod 10; the pocket at positions 9 mod 10, meaning the {c(p),c(m)}-component of m in T − h − p − x⁺, and whether it reaches w⁺; |K_{c(p),c(m)}(p)| at positions 0 mod 10; J at every position; and the k4fail, k3fail and step8break flags.
- **Checks over 896 periods, 0 exceptions.** K₈ contains x₂, x₃ and w⁺ and avoids p, m, y and z. The pocket reaches w⁺ ⇔ J is false at position 9 (the pocket lemma). A step-8 break in period b ⇔ a k = 4 failure at the R3k4 of period b + 1. k4fail = k3fail in every period except the two orientations of p25#16945 h3. The plantri orientation has a k = 3 failure with no break. The mirror orientation has a break followed by a k = 4 failure without a k = 3 failure, and it is also the Job AU |K(p)| exception.
- **K₈ ∩ K₁₈.** It is always nonempty, because it always contains {x₂, x₃, w⁺}. On every L = 20 cycle it has at least one far vertex: 237/237 with no break and 19/19 with a break. At a break it is {x₂, x₃, w⁺} plus 1 far vertex (16 cycles) or 2 far vertices (3 cycles). Consecutive K₈'s share a far vertex in every period of every census and construction cycle.
- **Non-breaking K₈ against the breaking pocket.** They always meet, 19/19. In 16 of 19 the intersection is just {w⁺}, which is forced. Only 3 cycles meet at far vertices: p25#16945 mirror (2) and p27#146733 and p27#152697 mirror (1 each). The two K₈ pairs always differ, as the period relabelling requires.

## Job AX [exploratory]: NightCutParity §3 u* alternation (jobax/jobax.py, jobax.json, jobax-summary.txt)
u* is the apex of the face on the ring edge w₃–y away from x⁻. ω = c(x⁺) at R3k4. Census Γ-cycles at orders 25–27, both orientations, are replayed in absolute colours. At (5,5,5,5,5) every q is tried, and all 5 give a valid universal-period labelling. Degree-6 constructions use the Job AV replays.
- **Table facts hold everywhere, 0 exceptions.** ω is in every swap pair. The free steps are exactly steps 0 and 7, and x⁻ is in both free components. "u* in exactly one of K₀, K₇" ⇔ "u* ∈ S_b" (the §3 reduction). A never recurs at odd distance in any cycle at any pattern.
- **The u* alternation is [killed].**

| set | periods | u* in exactly one of K₀, K₇ | cycles where u* flips every period |
|---|---|---|---|
| census (5,5,5,5,6) | 552 | 384 | 180 / 264 |
| constructions (5,5,5,5,6) | 344 | 344 | 40 / 40 |
| census (5,5,5,5,7) | 916 | 834 | 365 / 406 |
| census (5,5,5,5,8) | 544 | 494 | 213 / 238 |
| census (5,5,5,5,5), all q | 12,400 | 11,308 | 5,142 / 5,670 |

  At degrees 6–8 every failure is "u* in neither". At (5,5,5,5,5) there are 1,004 "neither" and 88 "both".
- **Every-period flippers.** The intersection over b of S_b is nonempty in every cycle at every pattern, with size 2–8. So some vertex always flips ω-membership every period, but it is not one fixed named vertex. When u* fails at degree 6, the flippers are far neighbours of w₃ and z. "S_all contains a far vertex adjacent to the ring" holds in 262/264 degree-6 census cycles, 406/406 at degree 7, 238/238 at degree 8 and 5,606/5,670 at degree 5.
- **α-class period 2.** A_{b+2} = A_b in 528/552 census degree-6 periods, 59/344 construction periods, 760/916 at degree 7, 414/544 at degree 8 and 10,844/12,400 at degree 5.

## Job AY [exploratory]: NightSigmaImage fixed-point language on all degree-6/7 Γ periods (jobay/jobay.py, jobay-periods.jsonl, jobay-summary.txt)
σ at every position uses that state's own j. It is fixed ⇔ the {c(x_j), c(x_{j+1})}-component of x_{j+1} contains every vertex of that colour pair. Colours are named in the period's position-4 frame: 1 = c(p), 2 = c(m) (the fourth colour), 3 = c(y), 4 = c(z). Data: 552 census degree-6 periods (264 cycles), 344 construction periods (40 cycles) and 916 census degree-7 periods (406 cycles), orders 25–27, both orientations, absolute replay, 0 replay errors.
- **"k = 3 or k = 4 failure ⇔ σ fixed at position 1".**
  - Degree 6: 550/552 census periods and 344/344 constructions. The constructions are vacuous: they have no failures and nothing fixed at position 1.
  - The 2 degree-6 exceptions are p26#87942 h22, one period in each orientation. That period fails at both k = 4 and k = 3 with no fixed point at position 1. It is the Job M short-block cycle, with patterns 0000001000 / 0000001000 and 0000001000 / 0000100000.
  - Degree 7: 858/916. There are 50 failing periods with no fixed point at position 1, and 8 fixed periods with no failure.
- **A₃₄′ and W2.**
  - Degree 6: no two consecutive periods are fixed at position 1, and none have consecutive k = 4 failures. W2 (positions 4, 6, 8 not all fixed) and W2* (positions 4 and 8 not both fixed) hold in 552/552 census and 344/344 construction periods.
  - Degree 7: consecutive periods are fixed at position 1 in 20 of 916 period pairs. 7/406 cycles have consecutive k = 4 failures, so A₃₄′ fails at degree 7. W2 and W2* each fail in 14 periods, on 14 cycles.
- **σ pair at each fixed position.** It is the same at every position, at both degrees. Fixed points never occur at positions 0 and 2. Lemma Fix holds: the complement pair has rank 0 at every fixed position.

| position | 1 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|
| σ pair | 12 | 13 | 12 | 14 | 13 | 12 | 14 | 13 |
| acyclic complement | 34 | 24 | 34 | 23 | 24 | 34 | 23 | 24 |

  Usually 3–6 of the six pairs are acyclic at a fixed position. The full six-rank vectors are in jobay-periods.jsonl.
- **Patterns.** Degree 6 has 19 distinct 10-bit patterns. 0000000000 occurs 374 times, then 0000001010 (36) and 0000101000 (33). Joint patterns of consecutive periods: 59 distinct at degree 6 and 90 at degree 7, with 29 shared. All are listed in jobay-summary.txt.

## Job AZ [exploratory]: complete dump of p26#87942 h22 (jobaz/jobaz.py, jobaz-p26-87942-h22.json, jobaz-table.txt)
Both orientations. Each has one Γ-cycle, with L = 20. The dump uses absolute names and colours and starts at R3k4. The order is 26. The far vertices within distance 2 of the ring are 0, 1, 5, 8, 9, 10, 11, 13, 18, 19 at distance 1 and 2, 3, 4, 12 at distance 2. No far vertex is at distance 3, so the whole graph lies within distance 2 of the ring.
- **Plantri orientation.** p = 16 and m = 7.
  - Period 0 fails at k = 4 (position 0, Lock2-only) and at k = 3 (position 2, Lock1-only).
  - At position 1, σ is not fixed: the image is a DL state. The period's only σ fixed point is at position 6 (R3k1).
  - The break is at position 19 of the previous period: J is false and the pocket reaches w⁺. Position 18 (R3k0) is σ-fixed.
  - |K(p)| is 10–13 in period 0 and 3–7 in period 1, except 13 at the fixed position 18.
- **Mirror orientation.** Period 1 fails at k = 4 (position 10) and at k = 3 (position 12).
  - Position 11 again has a DL σ-image, not a fixed point. The period's only σ fixed point is at position 14 (R3k2).
  - Position 8 (R3k0) has a Lock2-only σ-image. This is a k ≤ 2 failure that is not a fixed point, like Job U's hole.
  - The break is at position 9, where J is false and the pocket reaches w⁺, followed by a Lock1-only σ-image at R1k2.

## Job BA [exploratory]: σ-image classification on all degree-6/7 Γ-cycles (jobba/jobba.py, jobba-cycles.jsonl, jobba-summary.txt, jobba-offsets.txt)
Data, all under the uv_lib.Hole full state space:
- census orders 25–27, both orientations: degree 6, 264 cycles; degree 7, 406 cycles;
- Job AS constructions: 40 degree-6 cycles;
- Job AQ adversarial graphs A7_exc h22/h34 and r5_80b930d1_exc h2: 54 degree-7 cycles, including L = 800.

Each state r of each cycle is labelled by its period position.

**(a) "Non-fixed R3 images are never DL" is [killed].**
- Degree-6 census: 24 counterexamples, all on L = 20 cycles, 8 each at positions 4, 6 and 8 (k = 2, 1, 0). 16 of them land on another Γ-cycle.
- Degree-6 constructions: 80 counterexamples.
- Degree-7 census: 106 counterexamples. Degree-7 adversarial: 0.
- At k = 3, 4 the claim holds with 0 exceptions: positions 0 and 2 are never DL.

**(b) Non-fixed R3 images do not always land on w < 0.**

| set | w < 0 | w = 0 | w > 0 (Γ) | w > 0 (non-Γ) | on Z itself |
|---|---|---|---|---|---|
| degree-6 census | 2,502 | 22 | 16 | 0 | 0 |
| degree-6 constructions | 1,506 | 0 | 40 | 0 | 24 |
| degree-7 census | 4,187 | 99 | 44 | 4 | 4 |
| degree-7 adversarial | 2,584 | 24 | 0 | 0 | 0 |

Every w > 0 target and every on-Z target is a DL image at positions 4/6/8. The w = 0 targets are mostly the k = 4/k = 3 failure images.

**(c) R1 image on Z.** σ(r) = π¹⁰(r) holds on every L = 20 cycle: 808/808 at degree 6 and 1,016/1,016 at degree 7. On longer cycles σ(r) = π^d(r) with d ∈ {10, 30, 50, …, 190}. At degree 6, d is always an odd multiple of 10 (all 1,000 cases), consistent with 20 | L. At degree 7, d is an odd multiple of 10 except for 4 images at offset 20 on L = 40 cycles.

**(d) U34 holds, 0 exceptions.** Every k = 4 failure image is Lock2-only and starts an unfilled run with (u, f) = (3, 1) or (4, 1).

| set | (3, 1) | (4, 1) |
|---|---|---|
| degree-6 census | 6 | 13 |
| degree-7 census | 59 | 20 |
| degree-7 adversarial | 24 | 0 |

Every k = 3 failure image is Lock1-only and is the last unfilled state of its run: forward (u, f) = (1, 1).

**(e)** Position-by-position kind tables for degree 6 and degree 7 are in jobba-summary.txt. Fixed points never occur at positions 0 and 2. Lock2-only at k = 4 and Lock1-only at k = 3 are the only failure kinds there, at both degrees.

## Job BB [exploratory]: NightA34Two §9 (jobbb/, picyc.cpp --jobbb, jobav/jobav-cycles.jsonl now with rotation + edges)
- **(1)** Every Job AV record now carries `rotation` (the rotation system in that record's orientation) and `edges`. That is 304 records over 162 distinct (graph, orientation) pairs.
- **(2) The one-period Φ test.** This is the new `--jobbb` engine flag, run on every (5,5,5,5,6) hole at orders 25–27, both orientations. A pair is an R3k4 state u₀ with u₀..u₁₀ all DL. There are 1,458 open-run pairs (185 with a break) and 552 Γ pairs (19 with a break).
  - B = k = 4 failure at u₁₀. It equals "J false at u₉" with 0 mismatches.
  - The test is "B ⇒ Φ(u₀) < Φ(u₁₀)". The table gives the number of break pairs and the failures of the strict form and of the ≤ form.

| Φ | open runs: n / fail(<) / fail(≤) | Γ: n / fail(<) / fail(≤) |
|---|---|---|
| \|K_pm(p)\| at R3k4 | 185 / 68 / 56 | 19 / 1 / 1 |
| Lock2 witness at R3k4 | 185 / 133 / 46 | 19 / 11 / 7 |
| \|K_i\|, i = 0, 1, 4, 5, 8, 9 (open n shrinks with i) | 185–7 / 4–118 / 4–95 | 19 / 18 / 18 |
| \|K_i\|, i = 2, 3, 6, 7 | 83–22 / 8–31 / 5–22 | 19 / 1 / 1 |

  The single Γ failure is always p25#16945 mirror h3, where |K_pm(p)| is 10 → 9. The steps 2/3/6/7 components give exactly the |K_pm(p)| verdict on Γ. **No candidate has 0 exceptions on open runs, so the one-sided form does not close A₃₄′ by an open-run argument.** Per-candidate no-break baselines are in jobbb-phi-summary.txt.
- **(3) Degree 7, inserted vertices.** M is adjacent to y and M′ to z. A pocket passes p through X ⇔ c(X) = c(x⁺) and X is joined to w⁺ in G_{c(p),c(x⁺)} − h − p − x⁺.
  - Census: 79 breaks, 46 through M′ and 33 through M. Adversarial: 24 breaks, 12 each. Each break uses exactly one of them.
  - **The 7 consecutive-break pairs (14 periods, all L = 20 census cycles, all in the plantri orientation) use M′ in both periods.** So the NightA34Two §8 prediction "different inserted vertices" is [killed].

## Job BD [exploratory]: exchange-pair pockets at position 9 (jobbd/jobbd.py, jobbd.json, jobbd-summary.txt)
Definitions follow NightA34Two §1–3. ρ is read off the hole, c₁₀ = ρc₀. d₉ = ρ⁻¹c₁₉ and X₉ = {v : c₉(v) ≠ d₉(v)}. P_c and P_d are the {c(p),c(m)}-components of m in T − h − p − x⁺ in c₉ and d₉; at degree 7, m is replaced by M′. For a pocket that reaches w⁺, C = p x⁺ w⁺ Q m p, where Q is a shortest pocket path. The sides of C are the components of T − C, with h included. Hole synchronisation at position 9 holds 256/256 and 7/7.
- **Degree 6, the 19 breaking cycles.** Exactly one pocket reaches w⁺, and its curve always separates z from y. In 15/19 the other pocket is {m} alone, nested inside the breaking pocket. In 4/19 they overlap without nesting: p27#186395 h22, two cycles per orientation, with sizes 6 and 10. In 2/19 the non-breaking pocket crosses the breaking curve and enters z's region. It meets the curve at m plus 2–3 far vertices, and **none of those shared curve vertices is in X₉**. |X₉| is 4–8, with |X₉ ∩ breaking pocket| 2–4 and |X₉ ∩ other pocket| 0–3.
- **Degree 6, the 237 non-breaking cycles.** P_c = P_d in 187. One is inside the other in 31, and they overlap without nesting in 19. The commonest (|P_c|, |P_d|, |X₉|) is (1, 1, 2), in 51 cycles.
- **Degree-7 control: the 7 consecutive-break cycles, both pockets through M′.** Both curves separate z from y. The pockets always overlap without nesting, |P_c ∩ P_d| = 4–6. Neither pocket crosses the other's curve: 0/14. They share M′, w⁺ and 1–3 far vertices, none in X₉. In 7/14 the other pocket lies in z's region.

## Job BE [exploratory]: m's neighbourhood at position 9 in c₉ and d₉ (jobbe/jobbe.py, jobbe.json, jobbe-summary.txt)
This covers all 256 L = 20 degree-6 census cycles, using the Job BD conventions. m's ring neighbours are always exactly p, y, z, so x⁺ and the w's never touch m. deg(m) = 5 at 182 cycles, 6 at 62 and 7 at 12. The far neighbours number deg(m) − 3.
- **(i) At the 19 breaks.** In the non-breaking colouring, every far neighbour of m has a non-pair colour (so P = {m}) in 15/19. All 15 have deg(m) = 5. The 4 overlap cases are p27#186395 h22, where deg(m) = 6 and 2 of the 3 far neighbours carry pair colours. In the breaking colouring, 1 far neighbour of m carries a pair colour in 17/19 cases and 2 in the other 2.
- **(ii) All cycles.** "Both colourings have a far pair-coloured neighbour of m" occurs in 4/19 breaking cycles (the overlap cases) and in 90/237 non-breaking cycles, so it does not mark breaks. With no break, the commonest count is 0 in both colourings (132), then 1 in both (86).
- **(iii) Steps 9–18.** These are the swaps that recolour far neighbours of m; the full pattern table is in jobbe-summary.txt. **Step 13 never recolours a far neighbour of m on a breaking cycle (0/19), against 86/237 non-breaking cycles.** Breaking cycles use 14, 15, 16 (6), 16, 17 (2) or start 9, 12 (11).

## Job AW [exploratory]: adversarial flip search. **Degree-6 counterexamples to A₃₄′, W2, W2* and Lemma S** (jobaw/: jobaw.py, verify_hits.py, jobaw-walks.jsonl, jobaw-summary.txt, jobaw-verified.json, jobaw-verify.txt, hits/, counterexamples.txt, jobaw-chain-on-counterexamples.txt)
**Search.** Moves are edge flips that keep the core class (simple, min degree 5, max degree 8, no separating triangle), each followed by up to 3 repair flips for degree-4 vertices. Flips never touch the hole's star. The search keeps link pattern (5,5,5,5,6) at the hole and a Γ-cycle there. The evaluator is picyc.n --jobm --jobn on both orientations. Seeds: the 8 breaking census graphs of Job AV and the 6 Job AS constructions. There are three objectives: A34 (consecutive k = 4 failures), W2s (k = 2 and k = 0 fixed in one period) and W3 (k = 2, 1, 0 all fixed). Budget: 6 walks × 1,000 steps per seed and objective, 252 walks, 438,871 evaluations.

**Census seeds never moved.** No walk from a census seed improved its primary score; the order 25–27 seeds are too rigid. Every hit comes from the 37-vertex AS constructions.

**Independent verification.** Each of the 61 distinct hit graphs was rechecked. The graph checks are: Euler F = 2n − 4, every edge in two oppositely oriented faces, and core_ok. The cycle checks use the Python uv_lib.Hole full state space and the Job AY absolute replay. All 61 are valid triangulations in the core class.
- **A₃₄′ is false at degree 6:** 11 graphs from 3 families, A7f2 (walk 5), A7f4 (walk 3) and walk-best-A7f1-3 (walk 4). Each has an L = 20, w = 4 (5,5,5,5,6) Γ-cycle with **both k = 4 visits failing**, in one orientation. That is the mirror orientation in the Hole convention and "plantri" in the Job AQ convention. Representatives: hits/A7f2-A34-w5-it918.json, hits/A7f4-A34-w3-it967.json and hits/walk-best-A7f1-3-A34-w4-it575.json, all with hole 22. counterexamples.txt holds their rotation systems.
- **W2 and W2* are false at degree 6:** 45 graphs have a Γ-cycle period with positions 4, 6, 8 all σ-fixed, and 55 have positions 4 and 8 fixed. Many are L = 20 cycles with the AY pattern 21XXX (k = 4, 3 failing; k = 2, 1, 0 fixed).

**The rest of the F6 chain on the three representatives** (Job AQ battery, all states; C++ Job S):

| graph | class states / F | Σw | Job S: Λ / Cr_N / deficit | AQ C_neg ≥ D = 20? |
|---|---|---|---|---|
| A7f2-it918 | 17,512 / 8,048 | −2,936 | 20 / 16 / **4** (both orientations, both cycles) | 21, holds |
| A7f4-it967 | 18,592 / 8,078 | −2,744 | 20 / 32 / −12 and 20 / 26 / −6 | 26, 32, holds |
| walk-best-A7f1-3-it575 | 23,306 / 10,774 | −3,958 | 20 / 10 / **10** and 20 / 16 / **4** | 27; **15, fails** |

- **Lemma S fails** in the Job S form (R3 lockless DD-endpoint exits) on A7f2 and walk-best-A7f1-3. In the Job AQ form (σ-exits from all DD endpoints) it fails on walk-best-A7f1-3 in the orientation where W2/W2* fail.
- **What still holds:** the quarter floor (class Σw < 0, F ≥ states/4), σC, σ′C (H1) and charge-back P₁, on all three.

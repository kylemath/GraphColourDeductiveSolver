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

# s61_t3: fy2 face-apex cells (class of t beyond a 5-5-5 face) on the s60 hat5 + f2b stack, tkill table, oracle -- 2026-11-03

Labels: [P] proved / exhaustive run of our engine, [M] measured, [C] conjecture. Plan: /mnt/project-files/threeball/SCOPE.md (STEP 1 + STEP 2 only).
No existing dir edited. Nothing committed. Scratch in scratchpad/s61 (cleaned). 2 CPU threads.

## Decision: enable s43's fy + fy2 on the hat5 stack instead of re-implementing
- s60's prelay2.py already holds s43's fy/fy2 code verbatim (fy_vis, fykey, fy_recv_key, fy2_allowed, fy2_cells, window ZT, cell rows, lowerR2
  cell check, upperR2 fy2 flag check; diff of the fy block vs s43/eng/prelay2.py is empty). jsepf.cpp already inherits jsep6's ZT leaf (via jsep7).
  The one blocker was f2bglue's `assert not FY`, plus jsepf's eval mode printed before the ZT coupling.
- So the "port" changes nothing on any existing flag path. All new behaviour sits behind `fy fy2` + `f2b=`, in a new glue file and a new binary.
  This keeps every old path bit-identical. A fresh face cell on hat5 would have meant duplicating code that is already there.
- Why z is needed: in the hat5 stack no receiver coefficient depends on t. Without fy's z columns (five -> big, key K2 with h2 = class(t) at a face),
  every cell of a row would have identical coefficients, so the cells would carry no information.

## What was built (P/s61_t3)
- `eng/` = copy of s60_f2b/eng, plus:
  - `t3glue.py` (new). exec'd by pcheck.py after f2bglue.py. It acts only when fy2 AND f2b= are both on. Otherwise it defines nothing that runs, and the
    old s43 fy2 path without f2b is untouched. When active it:
    * redefines `fy2_cells` with the tkill classes;
    * redefines `run_sep`: every d goes through bin/jsept, which gets ZT, the f2b file at d = 7..9 and the tkill file;
    * wraps `recv_coef_R2` so reporting callers of a row that tkill excluded get its s43 first cell;
    * adds the self-test `t3self=N` (`zrand=SEED` gives random z values, `t3selftk` builds a random kill table).
  - `jsept.cpp` / `bin/jsept` (new). It is jsepf plus:
    * argv[12] = tkill file;
    * the leaf kills t classes per face and drops a row that has no class left;
    * the eval print moved after the fy2 coupling.
    DFS bounds are unchanged: WIN holds the UB over s43's A_i, a superset of the kept classes, so they stay valid.
  - Three one-line edits:
    * pcheck.py: exec t3glue.py;
    * f2bglue.py: the assert `not FY` became `(not FY or FY2)`;
    * prelay2.py: the `t3self` hook in upperR2.
  - jsepf/jsep6/jsep7 sources and binaries are byte-identical to s60's.
- Cells (s43 43.1 + tkill). A face i is w_i = w_{i+1} = s_i = 5, and t_i is the 4th neighbour of the apex five s_i.
  K_i = the OR of the kill letters of every entry that fires at i (plus {5,6} under `toracle7`).
  - K_i empty: A_i = fy2_allowed(s_{i+1}, s_{i-1}), exactly s43 (non-R5 apex link, fallback {0,1}).
  - K_i non-empty: A_i = {c : some x in CLS2[c], x not in K_i, (5,5,s_{i+1},x,s_{i-1}) not R5}.
  - A_i empty: the row is excluded (no cell). This is sound if the table is sound: every letter of t is R5 at s_i or killed.
- tkill format, text, `tkill=FILE` (documented in t3glue.py and tk/):
  - Line: `D  w@OW=WPAT  s@OS=SPAT  kill=LETTERS`.
  - D is the exact degree, or `*` for any d.
  - Patterns are read relative to the face index i. Letters are 5..9, `.` or `[78]`.
  - The face letters w@0=55 and s@0=5 are implied.
  - Each entry is applied in both orientations (mirror: w offset o -> 1-o, s offset o -> -o).
  - Example `tk/tkill_example_D11.txt`: `7 w@-1=6556 s@-1=657 kill=6`. This only checks the format; the real table is STEP 3.
  - In C++ the patterns are 128-bit one-hot masks (d <= 17).
- `env61.sh` = env60.sh with E -> s61_t3/eng (tables stay in s60_f2b), plus SOLC / SOLC2 / plant paths.
- `sol/sol_c_fy2.json` = sol_c_repaired_opusfmt.json with `fy2: true, fy: true, z: []`. upperR2 refuses a sol whose fy2 flag differs from the run's.
- `sol/plant_{big,small}.json` are the planted controls. `run61K.sh` is STEP 2. `cellrows.py` and `senderfree.py` are analysis drivers.

## md5 (engine_md5.txt)
t3glue.py b53b5acee55c6eba3e1bc1f9e7b414a9 | jsept.cpp acb2a9589f9d1cb60c5dca385fd04e93 | bin/jsept ade55721c69b277cba44539affde359b |
pcheck.py c3e1569731ef047f4add8184e7457997 | f2bglue.py c57c42138a46c11c4ab74f68dd7c65e3 | prelay2.py 595854a07510b87827f94e4e65763546 |
jsepf.cpp f3680646d89c25bda7832fdb12166312 (= s60) | bin/jsepf dfcf30d8d9b676c7d5806132392bce58 (= s60) | jsep6.cpp 2902caf8... (= s60/s43) | others = s60.

## Results
| # | check | result |
|---|---|---|
| a1 | flag off: upperR2 on sol_c with the s61 engine (f2b rules on, A97 hygiene) | **FEASIBLE at 0.041565**, 0 violated at d=7..17, sender 0, cons 0, Karp 0.5217. The log is identical modulo timings to s60's `val/upper_solc_on_A97hygiene.log` and to a fresh s60-engine run [P] (val/a_upper_flagoff*.log, val/ref_upper_s60engine.log) |
| a2 | flag off: F2B self-test (f2bself=300, python exact vs jsepf leaf) | identical log to the s60 engine. max diff 4.99e-13 / 4.9e-13 / 4.98e-13 at d=7/8/9 (< 1e-12) PASS [P] (val/a_selftest_f2b_flagoff.log) |
| a3 | flag on: T3 self-test, python max over cells vs jsept eval, d=7..10, 300 arrangements each, random z, empty tkill | max diff <= 4.99e-13. 217-225 rows per d with >1 cell, all with cell values that differ. PASS [P] (val/selftest_t3_empty.log) |
| a4 | same with toracle7 | <= 4.99e-13, PASS. No row excluded: A_R5 ∩ {1} was never empty in the samples (val/selftest_t3_oracle.log) |
| a5 | same with a random kill table (54-68 entries/d incl. mirrors, read off sample faces) | <= 4.99e-13. 13-45 rows/d excluded, 12-27 rows/d with fewer cells. 0 drop mismatches. The python dict matcher and the C++ 128-bit matcher are independent code. PASS [P] (val/selftest_t3_randtk.log) |
| b | flag on (fy fy2), empty tkill, upperR2 on sol_c_fy2 (z = 0) | **FEASIBLE at 0.041565**, 0 violated d=7..17, sender 0, Karp 0.5217 [P] (val/b_upper_fy2_tkempty.log). The relaxation only adds cells and columns; with z = 0 every cell equals the s60 row. No counter-example to (b). |
| c1 | NEGATIVE CONTROL: sol_c + z = 0.5 on the 8 keys (7,5,5,6,6; h0,h1,**h2=1**,·,h4), empty tkill | **INFEASIBLE (20)**, all at d=7. The sender rows stay at 0 violated (z only adds sender outflow). The violated rows (e.g. 9578655/5555657) carry the 0.5 only in their t-big cell (cellrows.py) [P] (val/c1_plant_big.log) |
| c2 | same planted sol, UNSOUND tkill `* kill=789` (removes the legal class t >= 7) | FEASIBLE. Leaf: 1.55M face kills, 310,750 arrangements dropped at d=7. A wrong table hides the violation, so tkill soundness is load-bearing [P] (val/c2_plant_big.log) |
| c3 | sol_c + z = 0.5 on the h2=0 (t small) keys, toracle7 | FEASIBLE (the oracle removes every t-small cell) [P] (val/c3) |
| c4 | same planted sol, empty tkill | **INFEASIBLE (20)** at d=7. The 0.5 sits only in the t-small cell [P] (val/c4) |

## STEP 2: oracle `toracle7` (t >= 7 at every face, receiver rows; class 1 only)
**Short K stages.** Same warm set for all three runs: s60's rows_q60A97.txt + the s53/A83/A84/A87 row files, as run60.sh does. Settings: K=300, keeppen, xpen=1e-3, lpmax=45, 2 threads.

| run | rows at iter 0 | iteration trace (LP t) | max violation, iter 0 -> last (d=7 / 9 / 17) |
|---|---|---|---|
| fy off (s60 stack) | 149,359 | 0.039068 (1 iter; consistent with s60's 0.03888 at iter 41) | 7: 1.3 |
| fy fy2, empty tkill | 210,184 (every cell of each warm row) | 0.019488, 0.019488 (2 iters) | 2.2 -> 1.6 at d=7 |
| fy fy2 toracle7 | 150,984 (~59k t-small cells gone) | 0.000000, 0.000000, 0.000000, 0.000000 (4 iters) | 2.27/14.9/19.8 -> 1.29/4.86/3.43 |

[M] The z columns are new and essentially unbounded by the warm rows. So both fy runs restart far below 0.039, while violations of 2-20 show these LPs are
nowhere near converged. The trace values are lower bounds on their LP optima (partial rows, up to the keeppen x penalty) and say nothing about the
converged t* yet. Iterations under fy take ~9 min here (separation at d >= 10 slows down with large z). Convergence would take tens of iterations,
i.e. a long solve, which was not run as instructed.

**Sanity checks.**
- [P] upperR2: sol_c is FEASIBLE under fy2 + toracle7 (z = 0; c3 is the same check with planted z). So **t*(oracle) <= 0.041565**. The oracle cannot hurt.
- [M] Where the gain could come from. Under the oracle, a z key with h2 = 0 at a face is paid by senders but received by no receiver row. So every
  sender context with a visible face toward a big and h2 = 0 becomes free (z -> large). Receivers gain nothing new: z(h2=1) only adds load.
  At sol_c (`senderfree.py`, val/oracle_sender_freed.log):
  - 6,736 sender contexts are near-tight (slack < 6e-4, i.e. the rows that break at t = 0.0410);
  - only 840 of them are freed by the oracle;
  - 5,896 tight contexts are not freed, spread over 281 of the 284 words that have tight contexts.
  y is keyed per word root, not per hat context, so the y of almost every binding word stays bound by a non-freed context.
- No lowerR2 certificate exists for either stack: there is no converged L stage, here or in s60.

**Assessment [C].** The oracle can only lower t* and caps the benefit of any real tkill table. The measured structure suggests the gain is small: ~12% of
the binding sender contexts are freed, almost no binding word is freed entirely, and the oracle gives the receivers nothing. My estimate: below ~0.002, i.e. t* stays
roughly in [0.039, 0.0416]. This is not proved. The short K traces cannot decide it, because the new z columns dominate the first iterations.
A decisive answer needs a converged K stage for fy2 and for fy2 + toracle7 from the same warm set (Mac Studio), or a dual certificate of the s60 stack
priced as in s43 §43.5.

## Reproduce
```
P=.../P_own_lp; . $P/s61_t3/env61.sh; cd $E        # build: c++ -O2 -std=c++17 -pthread -o bin/jsept jsept.cpp
# (a) flag off, and the f2b self-test
python3 pcheck.py upperR2 $FUP $X f2b=$RULES nomax sol=$SOLC $A threads=2 work=$SC/w_a
python3 pcheck.py upperR2 $FUP $X f2b=$RULES nomax sol=$SOLC $A threads=2 f2bself=300 work=$SC/w_st
# flag on: self-tests (empty / oracle / random table) and (b)
python3 pcheck.py upperR2 $FUP fy fy2 [toracle7|t3selftk] $X f2b=$RULES nomax sol=$SOLC2 $A threads=2 t3self=300 zrand=1 work=$SC/w_t
python3 pcheck.py upperR2 $FUP fy fy2 $X f2b=$RULES nomax sol=$SOLC2 $A threads=2 work=$SC/w_b
# (c) planted controls
python3 pcheck.py upperR2 $FUP fy fy2 tkill=$Z61/tk/tkill_empty.txt $X f2b=$RULES nomax sol=$PLB $A threads=2 work=$SC/w_c1        # INFEASIBLE
python3 pcheck.py upperR2 $FUP fy fy2 tkill=$Z61/tk/tkill_wrong_kill789.txt $X f2b=$RULES nomax sol=$PLB $A threads=2 work=$SC/w_c2 # FEASIBLE (unsound table)
python3 pcheck.py upperR2 $FUP fy fy2 toracle7 $X f2b=$RULES nomax sol=$PLS $A threads=2 work=$SC/w_c3                              # FEASIBLE
# STEP 2 short K runs
cd $Z61 && MAXIT=4 bash run61K.sh
```
Real solve (not run): `python3 pcheck.py solveR2 $FUP fy fy2 [toracle7|tkill=FILE] $X f2b=$RULES keeppen tag=... $A $CB warm=... K=300 xcap=3 xpen=1e-3 lpmax=45 threads=N`.

## Not done / caveats
- No converged K/L stage, no lowerR2 cert and no binders for fy2 or the oracle (STEP 2 asked for a short run only).
- The fy2 K run was planned for 4 iterations. It was stopped by hand and re-run for 2, and the fy-off run for 1, to fit the time (run.log says so).
- toracle7 and tkill act on the exhaustive receiver part d = 7..17 only. The tail d >= 18 keeps the window UB (sound). Sender rows are unchanged:
  the oracle frees them only through z.
- Mode-2 (K stage) dedupe ids do not encode the kill table, the same limitation as s43's cells. This can change which rows one iteration returns, never
  whether a violated row exists.
- The tkill drop rule (A_i empty -> row excluded) is stricter than s43's fallback. It applies only when some entry fired; with no firing entry, s43's
  fallback {0,1} is kept.

## Converged oracle (4 Nov 2026) -- NOT CONVERGED, run still going [P] single engine
- Coverage: `toracle7` is one table entry with d = any and no window pattern, so it fires at EVERY 5-5-5 face of every receiver row d = 7..17 (all link
  classes; jsept log: ~3.4e8 face fires at d=7..9 per separation sweep). Apex t in {5,6} is killed; t in {7,8,9} is the single class-1 cell; a row whose class-1
  apex link is R5 for all of 7,8,9 is dropped. This is a fixed-class oracle ("t >= 7"), not a per-context min over cells (a min over cells is a disjunction, not an LP).
  No code was changed to widen it.
- Run: `run61L.sh` (nohup, nice 10, threads=3, K=300, keeppen xpen=1e-3 lpmax=45, maxit=400). Warm = s60/s53/A83/A84/A87 rows + the 5,985 z-bearing rows
  from the STEP 2 oracle run (run_L/ckpt/seed_K_oracle.txt), 106,799 admitted. Rows are checkpointed to eng/rows_q61L_p1.txt every iteration; the wrapper re-warms from run_L/ckpt/*.txt on restart.
- Trace (run_L/L_p1.log), LP t (lower bound on the oracle LP optimum), max violation d=7 / d=17:
  iter 0: t=0.000000 rows 157,751 cols 47,936, viol 1.16 / 7.9; iter 1: t=0 rows 159,449 cols 48,108, viol 1.00 / 1.7; iter 2: t=0 rows 161,278 cols 48,427, viol 0.86 / 1.9.
  ~1,700 rows added per iteration; iterations take 10 min to 90 min (d=17 separation is the sink, 4,264 s once). After 2.5 h only 3 iterations: far from converged.
- Result: no converged oracle t. The only [P] bound remains t*(oracle) <= 0.041565 (upperR2 FEASIBLE with z=0 under toracle7, see c3). LP t = 0 is only the empty lower bound.
  Active z columns / contexts in the dual: not measurable until convergence (cols grew 47,936 -> 48,427, includes all column types).
- Verdict: undecided. Violations ~1 at d=7 are not shrinking quickly; convergence needs hundreds of ~1,700-row iterations (days at this speed), so this should go to the Mac Studio.

# s60_f2b: outside team's upgraded kill tables + 2-ball masks in OUR discharging-LP pipeline (registry A97, Opus engine) -- 2026-11-01

Labels: [P] proved/verified by exhaustive run of our engine, [M] measured, [C] conjecture / reliance.
Dir: .../opus/P_own_lp/s60_f2b  (engine copy eng/, tables tab/, logs val/, run_A97/). Copies of logs/solution adapter in scratchpad/ext_a97/. No existing engine dir or file edited; nothing committed.

## Headline
- [P] OUR engine (upperR2, exhaustive d=7..17, relaxed DP 18..30, Karp tail, sender rows, conservation) says FEASIBLE at **t = 0.041565** on registry A97
  with exname_rm128 hold-outs, own rpat/rpatN, upgraded kill6 + l3q (V7,V8) tables and the 2-ball masks ON, for the outside team's repaired solution
  (sol_c_repaired, via an adapter, see below). So **t* <= 0.041565 (A97 hygiene stack, upgraded tables + 2-ball masks)**, down from 0.098789365409. 0 violated rows at every d, sender rows violated 0, conservation 0.
  The same solution on the outside team's own A100-minus-1 pattern set (their args, no hold-outs) is also FEASIBLE at 0.041565 (cross-engine check, their Studio checker gave the same verdict at d=7,8).
- [M] Our own K stage (A97, same stack as s53 plus upgraded tables + masks) did NOT converge in the time here: LP value trace reaches t = 0.0389 at iteration 41 (about 3.2 min each, 150.7k rows; it sat at 0.038322 for iterations 35-38),
  so our own LP optimum under this stack lies roughly in [0.039, 0.041565] [C: 0.0389 is the partial-row LP value, a lower bound on the LP optimum up to the small x-penalty (keeppen)]. It is therefore NOT yet our own solution; the 0.041565 comes from the outside team's solution verified by our checker.
- No lowerR2 certificate and no binders for the new stack yet (those need the converged K solution). Ready-to-run command set for the Mac Studio is at the end.

## What was built
1. `eng/` = copy of s51/eng (pcheck.py, prelay2.py, psolve.py, ... , bin/) + three additions (existing dirs untouched):
   - `eng/f2b.py`: the rule loader/matcher of ext_f2b (rule = (p_deg, w_req, s_req); fires at spoke i iff listed w/s letters match at the given offsets).
   - `eng/f2bglue.py` (exec'd by pcheck.py right after prelay2.py; flag `f2b=RULES.json`, `f2boff` = plumbing with an empty rule set):
     * `recv_coef_R2` wrapper: at every w_i = 6 spoke of a d = 7,8,9 row, rules remove p_deg from the allowed-private mask: ('M', sig + (am,)) -> ('M', sig + (am & ~bit,)).
     * `l3q_terms` / `l3q_terms_payeeV` wrappers: at every link-7 side of a d = 7 (V=7 table) / d = 8 (V=8 table) row with c, apex in {5,6}: ('lQ', (c, ap, m)) -> (c, ap, m & ~bit) (4-tuple key with V for d = 8).
       Because the Python wrappers sit at the single place the row coefficients are produced, the K/L solve (row generation), lowerR2, binderR2 and upperR2 all use the masked rows.
     * `f2b_write(d)`: per-d binary table for the separator (kill-mask table, M value at every (sig, mask), Qeff at every mask, bucketed rules).
   - `eng/jsepf.cpp` / `bin/jsepf` (= jsep7 + f2b leaf correction, all d = 7,8,9; optional eval mode): the DFS and its relaxed window bounds are unchanged (masks only remove options, so the unmasked window
     values remain valid upper bounds); at the leaf, for every w_i = 6 spoke where a rule hits the allowed mask: tot += M(sig, mask & ~ex) - M(sig, mask); for every link-7 side: tot += Qeff(c,a,m & ~ex) - Qeff(c,a,m).
     Corrections are <= 0 (clamped and counted; 0 clamps occurred). Mode-2 (K stage) dedupe ids get the new masks. pcheck.py `run_sep` routes d = 7,8,9 to jsepf when f2b is on.
2. `conv_tables.py` + `tab/`: conversion of the verified upgraded Studio-format tables to Opus DICT format.
   Studio rows `[c, ap, w2, w3, w4, o, mask]` -> key `"%+d c w2 w3 w4 ap o"`: value `[mask, {}]` (pcheck reads v[0] only). kill6_U7/8/9.npy copied unchanged from tierA (same layout and bit meaning: bit set = letter killed; consistent with `amask = 31 & ~KT`).
   Checks [M]: (a) the Opus A97 baseline -> Studio list -> Opus round trip reproduces the baseline masks exactly; (b) the tierA tables and our own Studio-code rebuild (ext_kills) give identical Opus-format files;
   (c) upgraded V7 vs the A97 baseline: 10 rows per side differ (letter 5 bit removed), upgraded masks are subsets of baseline everywhere, V8 identical (matches ext_kills/REPORT.md); kill6 upgraded is a bit-superset of the A97 baseline kill6 in all three U (+20,074 / +16,878 / +16,878 cells), kill6 == bit-packing of the own-rebuild kill_U*.npy. md5 in tab/md5.txt.
3. `env60.sh` (paths and flag sets FBASE / FUP), `run60.sh` (K -> L -> upperR2 -> binder, same stack as s53/run53.sh, lpmax=45 so a stalled simplex falls to IPM after 45 s, which was needed: lpmax=900 cost 11 min per iteration).
   The warm set is the s53 one: s53's own added rows (rows_q53A97.txt) + the A83/A84/A87 row files (rows_q53A97.txt alone is NOT enough: it holds only the 21k rows s53 added on top of the warm files).

## Validation (all before trusting any solve)
| # | check | result |
|---|---|---|
| 1 | plumbing, rules empty (`f2boff`, jsepf path), baseline A97 tables, sol_q53A97, upperR2 | FEASIBLE at 0.098789365409; all log lines identical to s53/run_A97/upper_early.log except the f2b banner [P] (val/upper_A97_baseline_f2boff.log) |
| 2 | self-test C++ leaf vs exact Python row value (recv_coef_R2 with masks and the solution's M/lQ/r/y/x values), 300 arrangements per d, rules empty | max abs difference 5e-13 at d = 7,8,9 [P] (val/selftest_off.log) |
| 3 | same, rules ON, upgraded tables, 3000 arrangements per d (half built from random rules) | max abs difference 5e-13 at d = 7,8,9; changed by the rules: 972 / 698 / 460; fire counts w6 897/887/1362, w7 1536 (d=7), 1313 (d=8) [P] (val/selftest_on.log) |
| 4 | sol_q53A97 (baseline-feasible) under upgraded tables + rules ON | FEASIBLE at 0.098789365409 (masks only remove options) (val/upper_q53A97_upgraded_rulesON.log) |
| 5 | cross-engine: sol_c_repaired (t 0.041565) -> Opus format (adapter: the Studio JSON's scalar `z` = 0.17799 is a report-only max of xo, replaced by `[]`; every other key is already in Opus R6x2 format: y,g,h,x,r,lq,lQ), their A100-minus-1 args, upgraded tables + rules ON | **FEASIBLE** at 0.041565: d=7 57 s, d=8 36 s, d=9 18 s (0 violated), d=10..17 0, Karp lambda 0.5217 d0 12.46; pattern counts D 18159, C 2257 equal Studio's EXPECT_PAT (val/upper_solc_repaired.log) [P] |
| 6 | negative control: same, rules empty | INFEASIBLE (20 violated rows reported per cap at d = 7, 8, 9; 60 total) (val/upper_solc_repaired_RULESOFF.log) |
| 7 | attribution: baseline A97 tables + rules ON on the A97-hygiene stack | INFEASIBLE (120): the kill-table upgrade AND the masks are both needed for this solution (val/upper_solc_on_A97hygiene_BASELINE_TABLES_rulesON.log) |
| 8 | **sol_c_repaired on the A97 hygiene stack** (A97 registry + args_A97, exname_rm128, rpatD, rpatN3; upgraded tables + rules ON) | **FEASIBLE at t = 0.041565**, 0 violated rows at d=7..17 (d=7 28 s, d=8 18 s, d=9 9 s), sender rows 0, conservation 0, Karp lambda 0.5217 d0 12.46 [P] (val/upper_solc_on_A97hygiene.log) |
| 9 | tightness: same solution with t lowered to 0.0410 | INFEASIBLE (5900 sender rows): the solution is a vertex at 0.041565 (val/upper_solc_t0410.log) |

## K stage (our own LP) on A97, upgraded tables + masks
- first run with the 21k-row warm set was started with the wrong warm list (killed after 2 iterations); second run with the full s53 warm set but lpmax=900: 11 min/iteration, killed;
  third run (lpmax=45, threads 2 for the separator): iteration 0 t=-0.0088 (125.6k rows), ... iteration 41 t = 0.03888 (150.7k rows, 40.9k cols), still adding about 450 rows per iteration (max violations at iteration 36: d=7 0.46, d=8 0.46, d=9 0.34).
  A parallel K=1000 run (run60b.sh) was at t = 0.0345 after 8 iterations when it was stopped to free a CPU for the sol_c checks.
  Both were stopped on the time budget; rows are in eng/rows_q60A97.txt and run_A97b/rows_q60B_partial.txt (warm-start files). [M]
- No binders: they need a converged cert (L stage). Binders of the outside solution (c) were not extracted.

## Caveats
- [C] The upgraded kill tables embed Tier A configurations (RSST D2/C2cons 582, nl51 8,200, k3p 10, k3x 4,407), not exactly our own registry; ext_kills/REPORT.md verified them sound relative to the Tier A set being reducible.
  17,772 of the 20,122 new U7 cells and 14,466 of the 16,878 new U9 cells rest on nl51. This breaks the "own rules only" reading for the TABLES (the A97 pattern/rule inputs are untouched and keep the hold-outs). Needs a policy decision before quoting 0.041565 as "own-rules-only".
- [C] The 2-ball rules are used as given and only for the sign/side convention fixed in ext_f2b (w_i=7: sg=+1 private next to s_0, apex s_i; sg=-1 apex s_{i-1}), which matches our l3q key orientation (ap,o) = (s_i, s_{i-1}) for sg=+1.
  Our implementation re-uses the ext_f2b matcher (not independent of it); the independent confirmations are the Python/C++ self-test, the empty-rule control reproducing the baseline, and Studio's separate checker giving the same d=7,8 verdict on (c).
- [C] Selftests compare the C++ leaf with the Python rows built by the same rule matcher; they validate the leaf correction, not the semantic reading of the rules.
- The sol_c solution was produced by the outside team against A100-minus-1; its verification here on A97 hygiene is a statement about OUR rows, with our own exhaustive separator (not Studio's).
- xo (x-outer) is not in the A97 stack (flags `xon` only); the f2b glue asserts xo/fy/v6/q7/pcell are off.

## Ready-to-run on the Mac Studio (K stage to convergence, ~6x faster)
```
# 1. copy P_own_lp/s60_f2b and the s33z/reg_A97, s47/tabV8_A97, s53/run_A97, s44/s47/s51 row files; set B,SC in env60.sh; build the separator once:
cd P_own_lp/s60_f2b/eng && c++ -O2 -std=c++17 -pthread -o bin/jsepf jsepf.cpp
# 2. quick re-check of the outside solution on A97 hygiene (2 min):
cd eng && . ../env60.sh && python3 pcheck.py upperR2 $FUP $X f2b=$RULES nomax sol=<ext_a97/sol_c_repaired_opusfmt.json> $A threads=4 work=/tmp/w60
# 3. full own solve K -> L -> upper -> binders (warm admission ~25 min here, ~4 min on the Mac; LP ~3 min/iteration here):
cd .. && LPMAX=45 TH=4 TO=86400 setsid nohup bash run60.sh > run60.out 2>&1 &     # writes run.log lines "[s60] ..."; results in run_A97/{sol,cert}_q60A97*.json, upper.log, lower.log, binders.log
```

# Upper side of t* = 7/27 (Studio, for the Opus LP checker; branch studio/lp-upper)

The solution feascheck certified FEASIBLE on 17 Oct 2026 (17:15Z), giving the upper bound t* <= 7/27 for L2 (and
notx) on run29b's registry.

- `round13_7_27_sol.json`: copy of wheeldis/out/wlp3x_j29_13_notx_sol.json.
  - Written by `wlp3x.py notx tag=j29_13 warm=out/job28/all_13.txt <round-13 args>`, i.e. the round-13 optimum
    re-solved in wlp3x's format.
  - Keys: `t` (0.25925925925925924), `z9` (0), `y` (690 nonzero rooted-word weights, key "u|abce" = root (u,a,b,c,e)),
    `x` (empty: no transfers), `args`.
  - **Precision: IEEE double as written by Python's json (about 17 significant digits). No exact rationals exist;**
    the LP is HiGHS floating point. feascheck tests with slack EPS = 1e-7.
- `feascheck.args`: the pattern arguments feascheck loaded (round-13 args `out/job28/j28_13.args` + loop/n9 win9,
  win25, win25b, win27, win29, win31), one per line, paths relative to wheeldis/.
- Kill / drop list: run with `WLP3X_DEF=1`, so the loader exclusion is `EXCL = ('hr1_or1',)`: files whose path
  contains `hr1_or1` are skipped. None of the args matches it, so nothing was dropped (the `out/def_*` defect files
  are kept). Within each file only `D=true` lines (pat=) or `C-REDUCIBLE` blocks (cpat=) with names `^[epf]\d+_` load.
  16,411 patterns loaded.
- `feascheck.py`: the checker, at commit c207d917 (later edits only add the WLP_SEPF switch, off here). It runs exhaustive
  bin/sep3x_new (SEP_NODELIMIT=0) at d = 7..15, threshold d - 6 + t + EPS, then the max-plus DP for d = 16..30 with z9.
- `feascheck_round13.out`: its output: 0 violated at every d = 7..15, FEASIBLE (19 s).

Command: `cd wheeldis; WLP3X_DEF=1 python3 feascheck.py out/wlp3x_j29_13_notx_sol.json $(cat lp_upper/feascheck.args)`.
Job 30 A and B solutions, certificates, args and kill lists will be added here when they converge.

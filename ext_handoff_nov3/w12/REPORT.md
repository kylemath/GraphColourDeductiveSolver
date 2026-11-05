# W12: Studio-side cutting-plane K loop with rr + z + zr + q7 on keep95p131f (5 Nov 2026)

Saved by the swarm lead from W12's hand-back (the harness refused the worker's own write). Labels: [C] = Studio-side checker, [M] = measured LP, not a bound.

**Status: not converged, no new certified in-point.** No t below 0.041565 is claimed from this work.

## What changed mid-run
- The compressed core (set711 patterns + final870 rules) cannot be used below 0.041565. At Opus in03 it reports 238 violators at d = 7 (max excess 0.0131); the full keep95p131f stack reports 0 for the same arrangements (17 of the 163 classes are inadmissible there; the other 146 are tight or slack because of f2b rules final870 pruned). [C] So compression results hold for the fixed solution only; any new solution must be checked on the full stack.
- Everything after 12:40Z ran on the full stack, in-point Opus in03, q penalty 1e-3.

## LP t trace (xpen'd, not lower bounds)
| Core | Iteration | t | Size | Note |
|---|---|---|---|---|
| Compressed | it0 | 0.007916 | 229,850 rows x 93,230 cols | q mass 17,010; excess at x_LP up to 39.7 (q-payer rows missing) |
| Compressed | it1.0 | 0.011748 | | |
| Full | it0 | 0.011202 | 282,334 rows | q mass 3.06 |
Each LP solve takes 18-31 min (the bottleneck).

## Full-stack checks of blends lam*x_LP + (1-lam)*in03 (Studio rows, sep3r_w12)
| lam | t | d = 7..17 | other checks |
|---|---|---|---|
| 0.05 | 0.039043169 | d = 7, 10-17 clean; d = 8: 146 violators (max 0.0215); d = 9: >= 4000, capped (max 0.306) | pass |
| 0.015 | 0.040068902 | d = 7 clean; 128 known d = 9 rows violated (max 0.0126) | pass |
| 0.006 | 0.040332661 | d = 7 clean; d >= 8 unfinished (stopped by the lead at 14:56Z to free cores) | not run |
Control: families forced to 0 give LP t = 0.031334; blend at lam = 0.3 (t = 0.0385) fails (298 violators d = 7, 4,380 d = 8). sol_c_repaired stays FEASIBLE (W10 ctrlB).

## Other findings [C]
- **Separator pre-check bug** in the lineage sep3x.cpp, sep3r_ak.cpp, sep3r_f2bS.cpp, sep3r_w10.cpp: the first pruning test of a transition uses (d - NRES[i+1]) * XINMAX, counting positions resolved at this step as already in nw although their transfer terms are added after it. A positive x term can be pruned away (found at d = 7: 5566997 / 5696767 lost in one rotation, kept in others). Searches restricted by slot masks or one-rotation-per-class lose arrangements; full-rotation search compensated in the cases checked (d = 7 class count 28,150 matches W10). Fixed in sep3r_w12 (SEP_BUGFIX=0 restores the old line). Impact on past FEASIBLE verdicts is being quantified (W12 round 2).
- Under final870 the rows are not reflection invariant; under the full rules they are.
- All 180,616 full-stack pool rows have non-negative coefficients on M, Q7 and lQ.

## Files (this folder)
- sol/: three candidates named by t and status (two _NOTclean_, one _unchecked/_UNFINISHED).
- pool/ (pcheck format `R d LINK SWORD tag`): rows_w12_studio_full.txt (4,145 full-stack violators at lam = 0.05), rows_w12_studio_on.txt, _centre_tight.txt, _ctrl.txt. W12's own rows only.
- ckpt/full/: rows_on_full_pool.jsonl.gz (180,616 rows), lp2_on_it000.json, state2.json, base_on.json.
- code/: lpk2.py, cand.py, lamstar.py, hook_k.py, sep3r_w12.cpp. logs/.

## Best next probe
Start from in04 with the full-stack LP point plus the 4,145 rows violated at lam = 0.05 (they limit d = 8, 9) and the q penalty; check lam ~ 0.005-0.01 on d = 8, 9 first.

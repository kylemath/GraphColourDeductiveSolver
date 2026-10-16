# Job 28 (Studio): the defect-driven loop for the Track 1 K = 2 plan [exploratory]

Pre-registration, written 2026-10-15 23:40 MDT, before any Job 28 computation. Background: README §7–7.3.1 (main 60db0d91).
Every verdict here is engine level (dfast18 / cfast). Nothing is Lean.

**Tasks.**
1. **Forbidden-pattern LP (`wlp3.py` + `sep3.cpp`, new).**
   - `wlp3.py` extends `wlp2.py`: a pattern position can carry an exact big letter 7 or 8, or a free big letter F (any
     degree ≥ 7, a ring vertex), not only {5, 6, B}.
   - The sender code of a receiver arrangement becomes the full 5-letter tuple (w_{i+1}, s_i, s_{i-1}, w_{i-1}) over
     5..9 (9 = degree ≥ 9). A pattern position holds a letter set per slot, with 5 → {5}, 6 → {6}, 7 → {7}, 8 → {8},
     B/F → {7, 8, 9}.
   - An exact pattern letter 9 is never used: letter 9 covers every degree ≥ 9.
   - Validation before use: with only the old B-free patterns, `wlp3` must reproduce `wlp2`'s t* on the same inputs
     (A6: 5/17).
   - Forbidden patterns:
     - every D or C-candidate receiver-centred configuration already in the registry (pairs, pairs2/eq, lp_dfast, the
       Job 27 C-candidates);
     - every B-fixed configuration that the loop finds D or C.
   - Receivers d = 7..15. d ≥ 16 is covered by the 1/b rule (README §1).
2. **Loop (`gen28.py`, `loop28.sh`).**
   - Take the arrangements with positive dual weight (and the tight rows) at the LP optimum.
   - For each arrangement and each sender set S (|S| ≥ 2), build the **B-fixed** configuration: u at exact degree d,
     S, and every link vertex of S at its exact degree from the arrangement. A letter 9 stays free.
   - Ring by the layered build; it must be a simple induced cycle, otherwise the configuration is skipped and
     counted.
   - Test with dfast18 at ring ≤ 16. If not D, run cfast `--search` (|X| ≤ 4, first hit). Greedy as `gen.py`: the
     cheapest untested S per arrangement first.
   - Add the D/C ones as patterns, re-solve, and repeat.
   - An arrangement whose every B-fixed S with ring ≤ 16 is tested and neither D nor C is **HARD28**.
3. **K ≤ 4 defect search, centres 5, 6, 7 (`bin/defectc` resumable by ring-1 word, `defect_bfloop.sh`).**
   - This runs in parallel, on the cores k19 and studio14c leave. Centre 7 is the long one.
   - Every new candidate is checked against R_opt+, and every survivor is fully verified.

**Cores.** k19 (studio14d) has top priority. Job 28 runs at nice ≥ 15 on what studio14c frees.

**H28.** The loop converges: t* ≤ 0 (to 1e-7) using configurations at ring ≤ 16 only.

**Kill (by 20 Nov at the latest).**
- New defects or binding arrangements keep appearing without slowing: the number of new D/C patterns needed per round
  does not fall over 5 consecutive rounds while t* stays > 0.
- Or a binding arrangement is HARD28: it needs a ring ≥ 17 configuration and has no ring ≤ 16 alternative.
- Or the HARD rows alone give an LP lower bound > 0 (as `hardlp.py`). That certifies that no further ring ≤ 16 B-fixed
  verdict can close it.

On a kill: stop and report.

**Prediction (mine, before computing).** I expect a slow loop. The §6.1 obstruction is partly in the rule class:
rooted-word rules cannot tell apart two big neighbours with the same rooted word. Forbidding B-fixed patterns
removes arrangements but does not change the rule class. So I expect t* to fall from 5/17 but to stall above 0, with
HARD28 rows appearing at d = 7. Most likely outcome: killed by the HARD-row lower bound, not converged.

**Milestone reports.** Each order of magnitude in defects processed or configurations tested, and LP feasible or killed.

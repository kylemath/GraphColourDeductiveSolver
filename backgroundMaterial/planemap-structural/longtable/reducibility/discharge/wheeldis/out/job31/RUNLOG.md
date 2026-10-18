# Job 31: the 6-relay LP class (Studio, 18 Oct; Long Table, sealed origin)

## Rule class
L2 (wlp3x: rooted-word y, big-big transfers x), plus:
- y56[r]: a five sends charge to a 6-neighbour. r is the five's word rooted at the 6 (294 vars).
- y6b[q]: a six passes charge to a big neighbour. q is the six's wheel word rooted at the big (4,760 vars).

## Rows
- Senders (342 non-R five words): Σ_{big roots} y + Σ_{6 roots} y56 ≥ 1 − t.
- Sixes (every non-R6 link word, with the maximising s letters): Σ_{link fives} y56 − Σ_{link bigs} y6b ≤ t. This is
  the receiver form d − 6 + t with d = 6, so a six may end at most at t, like every other vertex. Separated exactly in
  Python: for each link word, a DP over the s letters.
- Bigs (d ≥ 7): as L2, plus inflow from each link 6 at w_i. That inflow is y6b[(u, w_{i+1}, s_i, p, s_{i−1}, w_{i−1})
  rooted at u], with the private p taken at its current maximum over non-R6 p: one row per completion, generated
  lazily, a per-transition constant in the bound. The d > DMAXP letter-9 DP and the Karp tail get the same inflow.

## Hypothesis and kill line (written before any solve)
- H31: t*(6-relay) < t*(A).
- Kill: t*(6-relay) = t*(A), with FEASIBLE (exhaustive separation of all three row families on the solution).

## Validation plan
1. With y56 = y6b = 0: separator byte-identical to sep3xf, and the LP reproduces 7/27 on the round-13 registry.
2. Conservation bijection: every y6b a six sends is receivable at its big through the inflow table, and vice versa.
3. Separator weights equal the Python row values (random weights, inflow-heavy).
4. Counts against an independent enumerator, and the six-row DP against brute force over the s letters.

## Validation (18 Oct ~18:45Z): structural checks pass
- Counts (RCHECK): 294 y56 and 4,760 y6b, each set-equal to an independent brute-force enumerator over raw tuples;
  1,424 non-R6 link words.
- Conservation (RCHECK): every y6b a six sends is receivable at its big through sep3r's inflow table (4,760 and 4,760),
  and nothing is receivable that is not sent.
- Weights (RSELF, inflow-heavy): 160 separated big rows, all with six inflow; |sep3r weight − Python row| ≤ 4.8e-10.
- Six rows (RSELF): the max-plus DP equals brute force over the 5^6 s letters on 200 link words, 0 mismatches.
- y6b = 0: sep3r is byte-identical to sep3xf on the 6 regression queries (regress.py MODE=R).
- Still to do: `rzero` LP reproduction of 7/27 on the round-13 registry, once cores free (after 24b).

## First solve (Long Table 18:48Z)
- Registry: exactly the new 1/4 registry, i.e. Opus's argsA (loop/studio/opus_check/argsA_local.txt): our B claim
  registry minus the broad 126.8168 pair, no Rule T.
- L2 (xcap 3) + 6-relay. Warm start: Opus's 1/4 rows are not on disk here, so it uses A's last row dump (re-checked by
  sep `c`).
- **H31 (restated): t*(6-relay) < 1/4.** Kill line: t*(6-relay) = 1/4, with FEASIBLE.
- It starts automatically when rzero (y56 = y6b = 0, round-13) converges, and only if rzero reproduces 7/27.

## First solve: registry and hypothesis reset (Long Table 20:17Z)
- Registry: the no-T registry = 5/21 + the full k43 batch (184 D + 198 C) + RSST-D (rpat=), with L2 and no Rule T.
  Args: loop/studio/opus_check/argsNoT_local.txt, a copy of argsA43_local.txt, which already carries rpatD.
- **H31: t*(relay) < t*(no-T). Kill line: t*(relay) = t*(no-T).** The baseline t*(no-T) comes from Opus's no-T
  solve, second-engined by Studio.
- It starts when rzero converges at 7/27, on the first core that frees (24b keeps priority). T + relay comes later.

## Baseline in, and solve held (18 Oct 20:45Z)
- The no-T baseline t* = 11/47 is [E2]: Opus s7 fa4705f2, plus Studio's lowercheck VALID and feascheck FEASIBLE on the
  drop44 registry (loop/studio/opus_check/README.md). **H31: t*(relay) < 11/47; kill line t*(relay) = 11/47.**
- rzero reproduced 7/27 at 20:32Z, so the first solve launched. Long Table 20:36Z held it, and it was stopped at
  iteration 1 (TERM). It restarts on the corrected and expanded registry (drop44 + k44 + k45) once that settles, and
  H31 is restated against the new t*.

## First solve, blind (Long Table option (b), 20:45Z)
- Registry: 30f86cd4 / 74bad798 = drop44 + k44 + k45 (argsK45_local.txt: twoeng 378 D / 383 C, k43fix files, rsstD
  rpat, L2, no Rule T) + 6-relay (wlp3r6).
- Runs blind: no no-relay baseline on this registry yet, and nothing of Opus's relay work opened. H31 (Long Table): t*(relay) < t*(no-relay,
  same registry); kill line equality. Then feascheck exhaustive in relay mode; t* and certificate recorded and committed
  here before any of Opus's relay work is opened.
- Started 10-18 20:45Z on the core freed by Job 30 B.
- 21:06Z: no-relay baseline on the same registry is t* = 2/9 [E2] (Opus s9 f1a052b4 + Studio feascheck FEASIBLE and
  exact lowercheck, 6 rows). **H31: t*(relay) < 2/9; kill line t*(relay) = 2/9.**

## Lighter restart (Long Table 22:13Z), 18 Oct ~22:20Z
- Run 1 stopped (TERM, PIDs 47678/47689/47692) after iteration 21: t = −0.151515, 82,123 rows; iteration times rose
  from about 30 s to 2,572 s, with t flat since iteration 16.
  - Saved and committed (59b300b7): j31_it20_rows.txt (the iteration-20 receiver dump, 71,435 rows) and j31_run1.log.
  - Run 1 kept no slack history, and its dump held only receiver rows. The six and recv9 rows and iteration 21's 241
    rows were not recoverable from the running process; the restart re-separates them.
- **Sign convention:** t in the log is the master LP's own objective, not its negation. solve() minimises t
  (`cvec[IT] = 1.0`, then `res = linprog(cvec, ...)`; `t = res.x[IT]`). Receiver rows read load − t <= d − 6 and
  sender rows −Σy − t <= −1. So −0.151515 is the current master optimum, which is a lower bound on t*(relay): the
  master has a subset of the rows and rises toward t*.
- Same class (wlp3r6), same registry (argsK45_local.txt = 30f86cd4), same separator (sep3r). Blind to sol_s10.
- New options, off by default:
  - `lp=ds`: scipy HiGHS dual simplex. highspy is not installed, so there is no basis carry-over between solves.
  - `drop=5`: a cut row (receiver/six/recv9) slack (> 1e-9) for 5 consecutive solves is dropped, and its key is cleared
    so it can be re-separated. Drops happen only on iterations that add rows, so the final solve is over a row set the
    iterate satisfies, and it is not repeated.
  - A full row dump with ages (out/wlp3r6_j31r_x_R6_rows_all.txt) is written every iteration.
- Warm start: j31_it20_rows.txt, each row re-checked by sep3r `c`.
- **H31r:** converges within 3 iterations of the restart, at a value comparable to 217/1129. **Kill line:** t still flat
  after 3 iterations. Then report the iterate's value and what it means against H31 (t*(relay) < 2/9).
- 22:20Z launch fixes:
  - (a) The first launch crashed on a bookkeeping bug: recv_row also appends z9 rows through xcol(). n0 is now recorded
    before separation.
  - (b) The second launch loaded the wrong registry (16590/893), because out/job30/k3x had moved to 42c4c876.
    It was stopped at iteration 1. argsK45_pinned.txt now pins k3x to 30f86cd4 (loop/studio/opus_check/k3x_*_30f86cd4).
  - The valid restart runs from ~22:29Z with patterns=16587 full=752, the same as run 1. Warm rows: 71,430 of 71,435
    accepted (the 5 others are key duplicates or rejected by `c` at the zero iterate).
- **H31r falsified at 3 iterations:** iterations 0–3 give t = −0.276923, −0.276923, −0.276923, −0.252632. This is
  iterate-for-iterate the same as run 1's iterations 0–3. **The kill line is not met as worded** (t moved at iteration
  3), but there is no convergence and nothing near 217/1129.
  - Cause: the binding rows are the six (relay) rows. Run 1 never dumped them, so the warm start rebuilds the relay
    side 241 rows per iteration, exactly as run 1 did.
  - The dual simplex alone did not cut the solve time: iteration 1 took 552 s. No row had reached age 5 yet.
- **Against H31:** the iterate −0.2526 is a master lower bound, nowhere near the 2/9 threshold, so it says nothing
  about t*(relay) < 2/9 yet.
- 22:38Z (Long Table 22:36Z, options (d) + (a)): the restart was stopped after: iter 7 t=-0.252632 rows 16596 xcols 23066 z9=3.0000 added 241 dropped 758 (736s)
  Drops began once rows aged: 81k → 16.6k rows, iterations ~15 s. Its lossless dump is saved as j31r_rows_all.txt
  (receivers + six + recv9, with ages). Relaunched as j31r2: same class, registry (argsK45_pinned) and separator,
  lp=ds, drop=5, **many6=120** (new option: the cap on six rows per iteration; receivers keep many=40), warm from that
  dump, nice 19. Its value no longer gates anything; it becomes a third, class-independent number.

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

# P2 / s9: main-line re-solve on the round 44/45 registry (written from P2's report)

**t* = 2/9 = 0.2222** (was 11/47). Lower VALID t >= 2/9 (exact, `lower_s9.log`). Upper FEASIBLE (`upper_s9.log`): 342
senders and d = 7..17 exhaustive, 0 violated; relaxed DP holds at d = 18..30; Karp lambda 0.5185, tail covered for d >= 12.

## Registry `argsA44.txt`
argsA43noT, with k3x_D/k3x_C replaced by the commit 30f86cd4 versions (`k3x_D_30f86cd4.out` 378 D, `k3x_C_30f86cd4.cfast`
383 C), the k43_kills_* lines removed (no double load), plus `rpat=../rpatD.txt`. 30f86cd4 = old k3x (3 D / 11 C) + k43
minus drop44 (173 D / 193 C) + k44 (196 D / 181 C) + k45 (7 D), with 1 D and 2 C overlaps removed; none of the 16 drop44
names is present. Loaded: D 15,413, C 1,429, RPAT 158; 10 job28 r_* files missing, as in every earlier run.
Cross-check: an independent assembly (`argsA44_ownassembly.txt`, k44 pats44 via `conv44.py`) equals Studio's set up to
symmetry, apart from 5 extra k45 D windows.

All 8 receivers of the 11/47 dual are forbidden (`chk_recv.py`): 7 by k44, and 8558655/6665666 only by k45.

## drop44 recheck
`argsA43noT_drop.txt`: sol_s7 is FEASIBLE and cert_s7 is VALID at 11/47; sol_s6 is FEASIBLE at 5/21. `chk_drop.py` checks
by pattern: 16 of 16 drop44 patterns are loaded in argsA43noT and 0 of 16 in the drop args.

## Solve
`cmd_s9.sh`: 52 iterations, 533 s, 3 threads, warm start from rows_s7/s6t43/s6. Dual has 6 rows: senders 55667 (2/9),
56668 (2/9), 55767 (1/9), 58778 (1/9); receivers d = 7 8655675/5756585 (2/9) and d = 8 75576556/78756665 (1/9).

Rerun gotcha: pass root=$SCRATCH/P/m/.../wheeldis (it has out/job30/). The default root silently drops addA_dfast18 and
the k3x files, which gives a false INFEASIBLE at d = 7 (link 9655757). Engine files are snapshotted here (md5 sums in
engine_md5.txt).

# Round 24 (H-N9): small windows against the d = 9/10 family that holds the transfer LP at 1/5

Engine level (dfast verdicts, w2.py matching; no Lean). 17 Oct 2026, 01:06Z-01:45Z.

**Family.** The 218 rows tight at a 4-iteration rerun of round 23's transfer LP (t* = 1/5, `tight23.txt`) with
d = 9 or 10 and no 7/8 link vertex: 56 at d = 9, 162 at d = 10 (`fam9.txt`, built by `mk9.sh`). Deviation from the
pre-registration: it named "max-fives d = 9 rows from a sep3 enumeration"; that enumeration timed out, and the
LP's own tight rows include d = 10.

**Before.** No existing pattern forbids any of the 218 (`cov9_before.txt`, 0.0%).

**Windows.** 413 untested small B-fixed windows at ring <= 14 (`win9_r14.txt`; 148 centred at a 9, 265 at a 10),
dfast on 3 cores in about 6 minutes: **140 D** (`win9.out`). Centred at a 9: 16 D of 148 (11%). Centred at a 10:
124 D of 265 (47%).

**After** (`cov9.txt`): **179 of 218 forbidden (82.1%)**. d = 9: 23 of 56 (41%). d = 10: 156 of 162 (96%).

**Verdict.** H-N9 lives on the family as built (bar: at least half). On the d = 9 rows alone, which is what the
pre-registration named, 41% sits between the bars (guess was about 40%).

**Still free: 39 rows** (33 d = 9, 6 d = 10), among them round 23's binder **559565656/565566666**. Its t* = 1/5
cannot move until that row is forbidden, so the LP was not rerun. Others: 565656565/657667566, 565656595/666666585,
555565595/858795995, 595595555/669667777, 5655655555/7797758585.

**Next supply.** The 39 free rows have 202 untested windows at ring 15-16 (93 at 15, 109 at 16). The binder has
11 (8 at ring 15, 3 at ring 16) and none beyond; 9 of its 20 windows are already tested and not D.

# Round 25 (H-N9b): ring 15-16 windows for the 39 rows round 24 left free

17 Oct 2026, 01:47Z-02:40Z. Same engine and matching as round 24.

**Windows.** 202 untested windows of the 39 free rows (`win25.txt`, binder first). In the 45-minute cap dfast ran
185 (all 93 at ring 15, 92 of 109 at ring 16): **10 D** (`win25.out`). The binder's 11: **6 D** (4 at ring 15, 2 at
ring 16).

**Coverage** (`cov25.txt`): 184 of 218 forbidden (84.4%); d = 9 28 of 56, d = 10 unchanged at 156 of 162. Newly
forbidden, all d = 9: **559565656/565566666 (round 23's binder)**, 565656565/657667566, 565656565/657567566,
565656595/666666585, 565656595/666666565.

**Verdict.** H-N9b lives (bar: the binder is forbidden). 5 of 39 rows by count. Guess ("binder stays free") wrong.

**Tail (02:42Z-02:56Z, `run25b.sh`).** The 17 ring-16 windows the cap missed, on 2 cores: 6 D (`win25b.out`), but
they forbid no new row (`cov25b.txt`: still 184 of 218). Every ring <= 16 window of the 34 free rows is now tested.

**LP check (after the verdict, not pre-registered).** `l2.py` with every explore window as a pattern (win14, win8,
win89, win9, win25), 6 iterations, 424 s: **t* = 7/33 = 0.2121**, reached at iteration 3 and unchanged for 3 more,
not converged (`l2_r25.txt`, tight rows `tight25.txt`). Binding rows: d = 7 5576576/5756756 (dual 0.12),
5675765/9555596, 5567576/5756656, and d = 10 5656556565/6576565765.

**Correction to round 23 [I].** Extra patterns only delete rows, so this LP relaxes round 23's, and a cutting-plane
value is a lower bound on its LP. Round 23's true optimum is therefore at least 7/33: its 1/5 (11 iterations) was an
under-separated lower bound, not the floor. 7/33 is still under round 23's 0.22 bar but is not converged either.

# Round 26 (H-L2c): the transfer LP with every explore window

17 Oct 2026, 02:41Z-03:42Z. `run26.sh`; iteration log `run26_iters.txt`.

**Run.** `l2.py` with win14, win8, win89, win9 and win25 as patterns. t* by iteration: 1/7, 1/6, 0.1776, then
**7/33 = 0.2121 from iteration 3 through 8** (115,587 rows, 12,536 transfer columns at iteration 8). Not converged:
each iteration still added about 37,000 v-side rows. The 45-minute cap is only checked between iterations, and
iteration 9's separation ran past the 60-minute wall, so the run was killed before its final report (no binder list,
no tight rows, no dump).

**Verdict.** The go stands (bar: under 0.22 at the end), as a lower bound only. The kill line is not met: t* is not
converged and is not rising, and the binders below have untested small windows. Guess ("climbs to 0.215-0.225")
wrong: it never moved off 7/33.

**Binders.** Taken from round 25's 6-iteration solve, which reached the same 7/33 (`l2_r25.txt`), since this run
lost its report. By row: d = 7 5576576/5756756 (dual 0.12), 5675765/9555596 (0.06), 5567576/5756656 (0.06); d = 10
5656556565/6576565765 (0.06). By degree: d = 7 three rows, dual 0.24; d = 10 one row, 0.06.
- 5567576/5756656 is already forbidden by a D window in Studio's `out/job28/r_12.partial.out`, which l2.py does not
  load (its patterns are the j28_12 snapshot plus the pat= files).
- The other three are free, and the four rows have 16 untested small windows at ring <= 16 (1 at ring 11, 2 at 13,
  3 at 14, 7 at 15, 3 at 16; `bind25.txt` is the row list).

# Round 27 (H-B26): small windows on the 7/33 binders

17 Oct 2026, 03:43Z-03:47Z. `run27.sh`.

**Windows.** All 16 untested windows of the four binders at ring <= 16 (`win27.txt`): **6 D** (`win27.out`), 2 of 5
at d = 7 (both ring 13) and 4 of 11 at d = 10.

**Coverage** (`cov27.txt`): 3 of 4 binders forbidden. Newly forbidden: d = 7 **5675765/9555596** (two ring-13
windows) and d = 10 **5656556565/6576565765** (three windows). 5567576/5756656 was already forbidden (Studio's
r_12 partial).

**Verdict.** H-B26 lives (bar: 2 of the 3 free binders). Guess ("one dies, likely the d = 10 row") was low.

**Still free: 5576576/5756756**, the heaviest binder (dual 0.12). Its windows at ring 11 and 16 here are not D; Studio
has dfast18/cfast running on its other B-fixed S.

# Round 28 (H-L2d): the transfer LP with the full registry

17 Oct 2026, 03:49Z-03:56Z. `run28.sh` (`../l2/full_extra.args`); iterations `run28_iters.txt`, report `l2_r28.txt`,
tight rows `tight28.txt`.

**Patterns.** Of the extra files, only the f/e/p-named ones load as patterns: r_12.partial added 37 (d = 7), the
explore windows the rest. z_lone_studio_dfast18 (62 D, `z_` names), def_b7_k5d14 and b7/k5_d14 (hash-named
configurations) and fans (`f_F` names) add none, since wlp3 parses only `[epf]<d>_` names.

**Run.** t* by iteration: 1/7, 0.1463, 0.1888, then **9/43 = 0.2093 from iteration 3 through 7**. maxit 8 was
reached after 368 s (61,572 rows), so not converged; v-side separation still adds rows each iteration.

**Verdict.** The go stands (under 0.22), as a lower bound. Kill line not met: not converged, not rising, and the
binders have untested small windows. Guess ("about 0.20-0.21, d = 7 rows bind") right.

**Binders** (`bind28.txt`). By row: d = 7 5775656/6565579 and 5675765/6557576 (dual 0.084 each), 5576576/5757756 and
5567576/5756756 (0.065 each), 5765575/7565777 (0.028), three v-side d = 7 rows with 7s in the link (0.009 each); d = 9
565656565/677667766 (0.021). By degree: d = 7 eight rows, dual 0.353; d = 9 one row, 0.021. None is forbidden by the
registry (`cov28.txt`). The nine have 14 untested small windows at ring <= 16 (1 at 12, 3 at 13, 1 at 14, 6 at 15,
3 at 16), plus 6 already in Studio's queue.

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

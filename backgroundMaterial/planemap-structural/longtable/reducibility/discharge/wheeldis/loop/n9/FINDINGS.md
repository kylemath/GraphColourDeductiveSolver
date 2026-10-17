# Round 24 (H-N9): small windows against the d = 9/10 family that holds the transfer LP at 1/5

Engine level (dfast verdicts, w2.py matching; no Lean). 17 Oct 2026, 01:06Z-01:50Z.

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

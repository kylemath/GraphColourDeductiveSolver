# RSST D configurations in the Job 28 registry (Studio, 18 Oct, Long Table low-priority task)

**Question 1 (are they in already?).** No. The registry's patterns are receiver-centred windows (e/p/f names) built
from u's link. No RSST name occurs in any pattern file. Opus (loop/opus/B_rsst_rows on claude/project-thread-7uelj0)
found the RSST fans around u to be new. For example 122.8406 (D, ring 11) kills the old binder 5675765/6575575,
which the registry left alive.

**Mapping.** `rsst_rows.py` is Opus's file, with one change: `RSST_ONLYD=1` keeps only RSST D configurations.
- RSST appearance: interior injective, exact degrees, induced, triangles to faces.
- The "fixed" mode only uses slots some 5-sender's rooted word reads, so each pattern is a conjunction of sep3 masks
  at 5-positions.
- D verdicts: Lean `agreesRSST` (DCheckThms / DCheckThms11 / DCheckR12*-R14*) states the checker's D result
  equals RSST's label for each configuration.
- Patterns come from every fixed-mode embedding in the rows tight_12, tight_13, loop/b7/binders, binders_self and
  loop/lf/seeds (4,627 rows). Output: 158 distinct patterns (27 at d=7, 55 at d=8, 76 at d=9), in `out/rpatD.txt`.

**Run rD1.** wlp3r (wlp3 + raw sep3 patterns `rpat=`, no transfers), registry = round-13 args + loop/n9 windows +
rpatD, warm = tight_13.
- Hypothesis: t* = 7/27 with the same certificate. No RSST configuration fits row R's pinned slots (Opus B), but rows
  behind R die.
- Kill line: t* > 7/27 + 1e-6 means a bug in the pattern encoding or loading (patterns can only lower t*). Stop and
  report. t* < 7/27 is impossible (feascheck's upper bound); if it happens, the encoding forbids an allowed arrangement:
  stop and report.

## Result rD1 (converged 10:5xZ, 312 iterations, 35,163 rows, last iteration added 0)
- **t* = 7/27 exactly, certificate unchanged:** 10/27 sender 55667, 5/27 sender 55767, 2/27 sender 77777, and 10/27
  receiver d=7 5675765/6577575.
- Lower bound: every row is RSST-D-free (warm rows re-checked with sep `c`; separated rows are free by construction).
- Upper bound: feascheck's 7/27 on the registry without RSST, since adding patterns only lowers t*.
- H (7/27 holds) survives. RSST-D clears rows behind R but not R itself (0 of 249 D configurations fit R's pinned
  slots, networkx control).
- Spot-checks (`spotcheck.py`): 10 of 10 tight_13 hits agree with an independent networkx induced-subgraph matcher.
  Negative control: row R takes none of the 249. The old binder 5675765/6575575 takes exactly 122.8406.

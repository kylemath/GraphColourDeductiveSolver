# Round 18: H-LF, are the HARD28 rows artefacts of receiver-centring? (16 Oct 2026) [exploratory, no new dfast]

**Question** (Long Table, 14:23Z). Do the HARD28 rows complete to isolated positive defects that survive the existing
registry? If not, receiver-centring is what makes them hard, and a neighbour-aware LP is the lever.

**Rows** (`seeds.txt`): the 15 HARD28 rows of Studio's round 12, plus the 34 other HARD28-like rows of `supply.py`.
That is 49 rows.

**Search** (`../b7/defectb9.cpp`, `runlf.sh`). defectc9 with letters 5-9 allowed on rings < K, plus defectb7's fixed
2-ball: the centre is 7, the row's link and s are fixed, and the p slots are free.
- An exact 9 here is a sub-case of "degree >= 9".
- A 10th argument, FREEMAX, caps the free slots.
- Validated: on 5567576/6755556 at K = 4 it reproduces defectb7's 4 leaves, with MAXL 7 and with MAXL 9 / FREEMAX 7.

**Check** (`lfcheck.py`). `defect_check2 bf` runs at every 7 of the patch, over every S. It uses existing verdicts
only.
- A bridge keys 948 named D/C configurations (f7_ from Job 28 and the explore windows) by lemmaA `la.ckey`, so they
  count too. In a control on 50 of round 10's leaves, all 50 were killed, 10 of them through the bridge.
- No dfast or cfast was run.

**Results.**

| depth | free letters | rows with leaves | leaves | killed | surviving |
|---|---|---|---|---|---|
| K = 3 | 5-9 | 0 of 49 | 0 | - | - |
| K = 4 | 5-7 (the row's 8/9 kept) | 22 of 49 (4 of the 15 HARD28) | 1,521 | **1,521** | 0 |

- K = 3 is complete and vacuous. No 2-ball with these 8s and 9s closes into a positive defect inside a 6-sea at ring 3.
- K = 4 is **incomplete**: every row hit the 2-minute cap. 27 rows found no leaf within it, including 11 of the 15
  HARD28 rows.
- **Every kill is away from the row's own 7.** No leaf is killed at the centre u. The nearest killing 7 is in u's
  link for 680 leaves (45%), in ring 2 for 727 (48%), and only in ring 3 for 114 (7%). 1,042 kills come through the
  bridge (Job 28 / explore f7_ windows centred at those other 7s).

**Verdict by the pre-registered bars: H-LF leads.** 49 of 49 rows have no surviving leaf, against a bar of 2/3.

**How much that is worth.**
- At K = 3 the result is vacuous. At K = 4 it is a 2-minute sample per row, with free letters 5-7 only.
- A 6-sea search rules out isolated defects only. It does not show that a row is sound to forbid.
- The positive part: wherever these rows do complete, the obstruction is a reducible configuration centred at a
  neighbouring 7 (93% within distance 2 of u). It is never at u. The LP cannot see that, because it charges u alone.
  This supports a neighbour-aware rule (u's row forbidden or discounted when a neighbouring 7 carries a D window).
  More ring-17+ windows at u would not help.

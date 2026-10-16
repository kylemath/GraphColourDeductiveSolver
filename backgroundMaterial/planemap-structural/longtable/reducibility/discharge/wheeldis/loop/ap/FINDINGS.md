# Round 21: H-A', HARD28-like rows through a neighbouring 7 (16 Oct 2026) [exploratory; existing verdicts only]

**Tool.** `ap.py SEEDS`. For each of the 49 HARD28-like rows (`../lf/seeds.txt`) and each exact link 7 v of u, v's
arrangement as fixed by u (`pairs.py view`) is filled over 5-9 in every free letter (9 = 9+, matched only by B). A
filling is killed by a registered D/C window centred at v (all 9,355 d = 7 f/e/p names with D or C in the
registries, w2.py matching on the fives of S) or by a reducible wheel (R5 at v's link fives, R6 for every p at its
link sixes, RBIG at v). No new dfast or cfast. Runtime 14 s.

**Result: H-A' dies. 0 of 49 rows have a closed view** (bars: lives >= 17, dies < 9).
- 25 rows have an exact link 7; 32 views; 487,500 fillings. 435,524 are not killed (89%); per view 58%-99%.
- 411,159 of the misses (94%) have an 8 in the filling.
- Misses also include all-5 s words at v (e.g. v = 7657665 / 5555555 for 5576576/5658856). Those die to
  configurations centred at v's fives, not at v. That is outside this test's kill set, so the test is narrow.
- Kills that do land: R5 at v (520 per view), RBIG, and a few windows (f7_.556757_.B6.55., e7_B5B5556_...).

**Reading.** On the current registry, no HARD28-like row can be forbidden through one neighbouring 7: v's free
letters leave most fillings untouched by v-centred windows, mostly because they carry 8s. Round 18's kills at
neighbouring 7s came from leaves that were complete 6-sea patches, not from v's 2-ball alone. Caveats: existing
verdicts only (untested v-centred windows could be D); exact 7s only (8-neighbours not tried); v-centred kills only.

**Follow-up (`ap8.py`, `ap8.txt`): kills at the 8.** Of the 435,524 misses, 308,600 have an 8 on v's link. Reading
that 8's arrangement off the filling (its own ball is mostly '?'), only 288 (0.1%) die to a d = 8 D/C window
centred at it, 264 of them to round 16's windows. "Neighbour 7 or 8" does not change the verdict.

# G9: positive defects that contain a vertex of degree 8 (16 Oct 2026) [exploratory, engine level: dfast + registries, no Lean]

Round 6 of the exploration loop (EXPLORE-LOG.md). Every defect search before this used degrees 5-7 on the rings
inside the 6-sea.

## Answer

At K <= 3, no defect that contains an 8 survives. Every leaf with an 8 dies to a receiver-centred configuration (B
free) with a tested D verdict, and a few also die to C. The centre-8 K = 3 search is complete (all 4,380 admissible
ring-1 words). K = 4 was not run.

## Tools (this folder)

- `defect_tables8.py` writes `defect_tables8.txt`, the 5/6/7/8-wheel tables over {5,6,7,8}.
  - Restricted to {5,6,7}, it is identical to `bin/defect_tables.txt`, line by line.
  - Any wheel word with an 8 that was never tested counts as **not** reducible.
- `defectc8.cpp` is `defectc.cpp` with the alphabet {5,6,7,8} on rings < K. Build it with
  `g++ -O2 -std=c++17 -o defectc8 defectc8.cpp`. The binaries are not committed.
- `mk_check8.py` generates `defect_check2_8.py`, a copy of defect_check2 that:
  - also takes receivers of degree 8 (the original skips every u with degree != 7);
  - reads `c8_` wheel verdicts and the verdicts in this folder.

## Validation (8 disallowed, same tables)

`defectc8` matches `defectc` exactly: node counts, pruned counts and byte-identical leaf files.

| K | centre 5 | centre 6 | centre 7 |
|---|---|---|---|
| 3 | 465,976 nodes, 5 leaves | 2,679,131 nodes, 22 leaves | 14,318,384 nodes, 40 leaves |
| 2 | 134 nodes, 0 leaves | 379 nodes, 0 leaves | 913 nodes, 0 leaves |

With the strict7 tables, K = 3 has 67 leaves, not the 153 in README §7. The 153 predate the §7.3 tables, which count
cfast C-candidate 7-wheels as bad. (Inferred from the README, not rerun.)

## Leaves (CMIN = 1, letters 5-8 on rings < K)

| K | centre | leaves | with an 8 | status |
|---|---|---|---|---|
| 2 | 5, 6, 7, 8 | 0 | 0 | complete |
| 3 | 5 | 16 | 11 | complete, 10 s |
| 3 | 6 | 44 | 22 | complete, 81 s |
| 3 | 7 | 261 | 221 | complete, 551 s |
| 3 | 8 | 376 | 376 | complete: 630 s up to ring-1 word 56878867, then the other 1,429 words gave 0 leaves (16 Oct, ~55 min) |


## Checks (defect_check2_8, bf)

- **Centres 5, 6, 7.** All 254 leaves with an 8 are killed by a D receiver-centred configuration at a 7 from the
  existing registry.
- **Centre 8.**
  - The existing registry killed 359 and left 17 open. All 17 have ring 1 = 55557557, 55557558 or 55657557.
  - 178 new dfast runs at ring <= 12 (`g9_c8_r1.in` / `.dfast.out`, 22 s) gave 103 D.
  - After those, all 376 are killed. Each of the 17 has a D receiver-centred configuration at the centre 8 (ring 10-12).
- No kill uses a 7- or 8-wheel or the non-simple-ring rule.

## Untested, counted not reducible (where an 8 enters R_opt)

| wheel | canonical words with an 8 | tested | reducible |
|---|---|---|---|
| 5-wheel | 97 | 87 (Job 17) | 9 C |
| 6-wheel | 338 | 0 | 19, through 2.122 |
| 7-wheel | 1,102 | 191 dfast | 0 D |
| 8-wheel | 4,435 | 291 | 55 D (all with links over 5-7) |

- The 10 untested 5-wheels are 58888, 67888, 68788, 68888, 77788, 77878, 77888, 78788, 78888 and 88888.
- No 7-wheel with an 8 and no 8-wheel has ever been C-tested.
- G6 note: pre-registered R_opt counts untested 6-wheels with an 8 as reducible. This search did not, and still
  found no survivor.

## Next

- K = 4 at centres 5-7, capped and sampled the way defectr2 does it at K = 5.
- Commit `defect_check2_8`'s degree-8 receivers into defect_check2 if G9 grows.

## Probe 2: centres of degree 9-12 (16 Oct, after the LP floor moved to a degree-10 receiver)

Tools:
- `defectc9.cpp` takes centres 5-12. Letter 9 means "degree >= 9" and is used for the centre only.
- `defect_tables9.py` writes `defect_tables9.txt`. That file (1.9 MB) is not committed; regenerate it with
  `python3 defect_tables9.py`.
- A word with a 9 counts as reducible only through D fans with a free vertex or through 2.122. 7/8-wheels with a 9 and
  the centre's own wheel count as not reducible.
- Validation: with C0 <= 8 the output is identical to defectc8 (K = 2, centres 5-8; K = 3, centres 5-7).
- `defect_check2_9.py` (from `mk_check9.py`) takes receivers of every degree >= 7 and reads f-name verdicts from
  out/job28, loop/lp and loop/g9.

Results:
- **K = 2, complete, centres 9-12: 0 leaves.**
  - With ring 2 all 6, a ring-2 vertex next to a ring-1 five has link 566666 or 556666. Both are Job 17 D 6-wheels.
  - Charge >= 1 forces ring-1 fives to be adjacent, so this cannot be avoided (`why_k2.py`).
- **K = 3, 150 s cap per centre, far from complete:**
  - Leaves: 897 / 650 / 292 / 113 for centres 9 / 10 / 11 / 12.
  - No leaf has more than 4 lone fives.
  - The existing registries kill 1,761 of the 1,952 leaves.
  - 1,801 new dfast runs at ring <= 12 (`g9_big_r1.dfast.out`; 1,590 D) kill the other 191.
  - Every leaf dies to a D receiver-centred configuration.
- **The LP's d = 10 arrangement** (link 5656556565, s 6566666665):
  - Its B-fixed S = {0, 2, 4} at ring 14 is D (`g9_lp10_r14.dfast.out`).
  - Its ring-1 word gives no K = 3 defect (0 leaves).

Not done: K = 3 complete for centres 9-12; K = 4.

The check outputs `big_chk_c1{0,1,2}.d` (lists of untested configurations, 1.7-3 MB each) are not committed. Rerun
`defect_check2_9.py` to regenerate them.

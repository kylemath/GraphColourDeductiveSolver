# G9: positive defects that contain a vertex of degree 8 (16 Oct 2026) [exploratory, engine level: dfast + registries, no Lean]

Round 6 of the exploration loop (EXPLORE-LOG.md). Every defect search before this used degrees 5-7 on the rings
inside the 6-sea.

## Answer

At K <= 3, no defect that contains an 8 survives. Every leaf with an 8 dies to a receiver-centred configuration (B
free) with a tested D verdict, and a few also die to C. Two gaps remain:
- The centre-8 K = 3 search is partial: 2,951 of 4,380 admissible ring-1 words.
- K = 4 was not run.

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
| 3 | 8 | 376 | 376 | partial, about 630 s; stopped in ring-1 word 56878867 |

Of the 1,429 centre-8 ring-1 words left, all but 6 have at most three fives.

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

- Resume centre 8 at K = 3 from word 56878867.
- K = 4 at centres 5-7, capped and sampled the way defectr2 does it at K = 5.
- Commit `defect_check2_8`'s degree-8 receivers into defect_check2 if G9 grows.

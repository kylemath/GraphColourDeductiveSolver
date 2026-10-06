# Status: WP20 P1 attempt 2 is produced and merged; the independent check over every graph is running

- **From:** Long Table (Creative Intel), main session
- **To:** the coordination session; Navigator; Math; Audit; the user
- **Sent:** 2026-10-06 11:35 MDT
- **Replies to:** the coordinator's 10:4x message
- **Asks for:** information only. **The numbers below are provisional and not for citation: the independent checker has not passed.**

**Produced and merged.** All 10 chunks finished at 11:34:49 (9 × 2,539 + 2,530 = 25,381 graphs); the merge reports 25,381 graphs and 658 witnesses, which equals the sum of the chunks' SEP-bad counts, so nothing was lost. The merged output has declaration `8758a9f8…`, input `92e482ed…`, producer `bb350d3b…`, and output SHA-256 `e68c44a3…793e`. **`d1_check.py --all` (every graph, 14 workers) started at 11:34:56; about 75 minutes (expected done about 12:50).** If it passes, the pipeline writes the report numbers and the digest automatically; if it reports any mismatch it stops and I report that.

**Provisional counts from the producer (not yet checked):** 405,465 degree-5 vertices, all complete; 142,792,092 unfilled states; 658 SEP-bad (all depth 1) in 70 of 25,381 graphs, per-graph counts 2, 4, 8, 12 or 24; `filled_neighbour_for_bad` 0; **D1 kills 0; P kills 0; P capped 0**; interrupted 0; locked classes 5,448; `no_legal_fan` 1,140 (at separating-triangle vertices, as explained in my 10:4x message; D1 excludes them, P evaluates them, 0 kills).

**A post hoc pattern, provisional.** At order 25 the colour classes of **every** SEP-bad state are (6,6,6,6) (594) or (5,6,6,7) (64): equitable or near-equitable, the pattern first seen at orders 14, 15 and 17, now at a fresh order where the hand bounds (each class at most 7) leave slack, so nothing forces it. It is a pattern read from the data after the fact, not a pre-registered statement, and I make no claim from it.

**Studio.** I have not yet received phase A's branch (a watcher polls every 90 seconds). When it arrives: first its `RECORD.txt` (M4 Max, 16 cores, 128 GB), then `wp21_mac_checks.sh` with 2 workers while the P1 check runs.

— Long Table

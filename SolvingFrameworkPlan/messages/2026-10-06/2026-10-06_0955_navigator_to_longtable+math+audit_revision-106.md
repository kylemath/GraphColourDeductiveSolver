# Revision 106: R = 3 killed (radius 4 at T4); A_r structure; P1 at 6 of 10

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit
- **Sent:** 2026-10-06 09:55 MDT
- **Replies to:** Math 09:38 (`…_0938_math_…_conjecture-R-hand-attack-radius-4.md`); Long Table 09:35 and 09:36 (`…_0935_longtable_…_reply-stray-run-already-stopped.md`, `…_0936_longtable_…_A-r-structure-census-and-lemma-B.md`), all in `SolvingFrameworkPlan/messages/2026-10-06/`
- **Asks for:** audit, an independent replay of the T4 radius table; Math, a look at Lemma B and Conjecture J; Long Table, use T4 as an S2 regression case (radius 4 at hole 4)

- **Killed: "radius at most 3"** (node `structural-conj-r-radius3-killed`). T4 (17 vertices, one edge flip of A_3, hole 4) has doubly locked states of radius 4; histogram over the 68 canonical colourings {0: 22, 1: 25, 2: 15, 3: 4, 4: 2}. Math recomputed it from the face list with its own code and it equals the worker's table, which I count as Math's review; the audit replay is pending. **T4's 4-connectivity is unchecked.** Conjecture R itself is **open**; the page's other results are the worker's, unreviewed, recorded as notes on `structural-conj-r-prereg`.
- **A_r structure** (node `structural-a-structure`, `exploring`): Lemma A and Lemma B (hand), a census for r = 3 to 8 (20, 20, 60, 100, 220, 420 classes, 20 times Jacobsthal), Conjecture J unproved, radius 2 on A_4 to A_8 in the census. The audit's independent census equals 20, 20, 60 classes times the 6 renamings; r = 6, 7, 8 are not independently checked. Long Table's earlier "ring-wrapping" lead is corrected to radial hairpins.
- **Stray run:** Long Table did not launch it to its knowledge; its `RECORD.txt` head `5caa496` exists only in the first Mac checkout (unpushed), so it ran from that working tree. The launcher is still unknown. Long Table's proposals (the Studio command issued only in the Studio's session; check an M4 Max, 16 cores, 128 GB record before accepting output; do not edit `wp21_studio.sh` while it runs) are recorded.
- **P1:** chunks 0 to 5 of 10 done, chunk 6 running (checked on disk). No D1 or P kill in any finished chunk; SEP-bad per chunk 20, 26, 12, 4, 134, 84, all at depth 1. **Intermediate chunk logs, not a result**; the result is the merged file after the `--all` checker and the audit replay. ETA about 11:15.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). No finite check is upgraded.

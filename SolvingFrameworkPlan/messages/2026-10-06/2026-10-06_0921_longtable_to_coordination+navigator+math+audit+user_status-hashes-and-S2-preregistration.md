# Status: WP21 version 2 hashes confirmed; S2 pre-registered; P1 and the Studio

- **From:** Long Table (Creative Intel), main session
- **To:** the coordination session; Navigator; Math; Audit; the user
- **Sent:** 2026-10-06 09:21 MDT
- **Replies to:** the coordinator's 09:32 message and plan
- **Asks for:** information only

**1. WP21 version 2 announcement and hashes (the Navigator's check).** The announcement exists: `messages/2026-10-06/2026-10-06_0829_longtable_…_WP21-version-2-announcement.md`. I compared every file hash in its table with (a) the file on disk and (b) `wp21/PACKAGE-SHA256SUMS`, mechanically. **All 11 announced file hashes equal the files on disk, and equal `PACKAGE-SHA256SUMS` wherever listed.** One announced file, `wp21_pipeline.sh` (the first Mac's own pipeline, stopped to avoid a double run), is deliberately not in `PACKAGE-SHA256SUMS`, which lists what the Studio needs. The phase-A selection file `24e381cb…` is in the package list and on disk. Declaration `8fdd1aa5…`, package commit `24e3551`.

**2. S2 (Kempe radii) is pre-registered**, in `backgroundMaterial/planemap-structural/longtable/WP22-S2-preregistration.md`, SHA-256 `c8ae2f62ce5d0729f493b5ab22b481c590d650f89abba1ab1574ffdf35ca166e`. It fixes the statement (Conjecture R), the two searches (S2a hill-climb and S2b exhaustive census of the stated symmetric families), the objective, the kill (an exhaustively closed Kempe class of $T-v$ with no filled state, re-verified by a separate verifier and then rechecked against the project's protected-face definitions), what is only a result, seeds (`wp22|s2a|t001..t040`), caps (120 CPU-seconds per tag, depth 6, 20,000 states, orders at most 30) and the gates. **S2 has never been run and its code does not exist yet.** It will be written, tested (determinism, planted faults, reproducing $r=2$ on W6 and $r\in\{2,3\}$ on $A_3$), committed and hashed in an addendum message before any run, and nothing runs until WP20 P1 has reported. It states that S2 was formulated after the Conjecture L data, so any bound read from those values is post hoc.

**3. P1 attempt 2.** 4 of 10 chunks done at 09:21; no D1 kill and no P kill so far; every SEP-bad state at depth 1; intermediate, not a result. Expected finish about 11:30, then `d1_check.py --all`, the report, and the digest for comparison with the Studio's replay.

**4. Studio.** Remote branches containing "studio": 0. I will run `wp21_mac_checks.sh` when the Studio's phase A and B outputs arrive, and compare the replay digest when it does. Math is checking the Conjecture L certificates and the audit is replaying them; I have nothing further to add on that until they report.

— Long Table

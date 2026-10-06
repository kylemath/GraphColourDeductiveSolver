# Status: the Studio's phase A intake; record confirmed; checks running here

- **From:** Long Table (Creative Intel), main session
- **To:** the coordination session; Navigator; Math; Audit; the user
- **Sent:** 2026-10-06 11:44 MDT
- **Replies to:** the coordinator's 11:4x message
- **Asks for:** information only. Nothing here is a pass beyond "on the sampled graphs", and the independent check of phase A on this machine is still running.

**1. Record confirmed.** `wp21/studio/RECORD.txt` (read first): **Kyles-Mac-Studio.local, Apple M4 Max, 16 cores, 137,438,953,472 bytes (128 GiB), Python 3.9.6, git head `e6110ff`, 16 workers, started 09:30:07 MDT.** I fetched the branch into a separate worktree (main is untouched). All 16 files of `wp21/PACKAGE-SHA256SUMS` match in the Studio's checkout, so it ran the announced package. `A-m5-26.json` is SHA-256 `1371118b…a839`, equal to the record and to what you relayed.

**2. Checks on this machine, in progress.** Done: the **subset-rule check passes** (the input is exactly the 4,578 of 91,441 graphs selected by the declared hash rule from the full order-26 list, whose hash `88acad11…` matches) and the whole-file checks pass (`RANGE 0..0 OK`). Running: the **sharded independent check over every graph** (23 ranges, ledger `wp21/mac-check/A-ledger`), with 2 workers so that the P1 check, which has the other 12 cores, is not starved; expected done within about 1.5 hours. I ran the phase A commands of `wp21_mac_checks.sh` directly and identically because the script also demands phase B's files; the script is unmodified. **One extra independent confirmation:** I recomputed phase B's seeds here from phase A's output with the declared rule: **the same 12 indices and the same hash `6582d4e8…` as the Studio's record.**

**3. P1.** The independent check `d1_check.py --all` over all 25,381 graphs started 11:34:56 and is running; expected done about 12:50, perhaps ten minutes later because of the phase A check sharing the machine. Then the full report with D1 kills (and P verdict and `filled_neighbour` count), `no_legal_fan` with both readings, and the digest.

**4. From the Studio's log, relayed and not yet verified by me.** Phase B ran 10:33:26 to 11:19:51 (12 of 12 shards), evaluated 4,812 graphs with 1,626 SEP-bad states, 0 D1 kills, 0 P kills, and passed its own sharded check at 11:38:29. Its files are not on the branch yet. When they arrive I run the same checks on them. The log also prints "max chain objective 1000" for the search; the objective gives 1000 points per kill and 20 per SEP-bad state, so with 0 kills that value comes from SEP-bad and locked-class counts, but I will confirm it from the data and not assume it.

— Long Table

# WP21 chronology (version 2)

All times MDT, 6 October 2026. Facts only.

1. Version 2 package committed `24e3551`, announced in `messages/2026-10-06/` (hashes in the announcement). Nothing run on WP21 data.
2. **09:18: machine assignment decided.** Phases A and B and their sharded checks are to be **produced on the Mac Studio** (Apple M4 Max, 16 cores, per the coordination session), so that WP21 runs in parallel with WP20 P1 on the first Mac; the **independent checks of those outputs are repeated on the first Mac** (a different machine from the one that produced them). The first Mac's own WP21 pipeline (`wp21_pipeline.sh`) was stopped at 09:18 before it began any phase, so that no phase runs twice. WP20 P1 attempt 2 is **not** split across machines.
3. The record of what each machine ran will be `wp21/studio/RECORD.txt` (written by the Studio script: machine, cores, memory, Python version, commit, workers, start and end times, output hashes) and `wp21/mac-check/checks.log`.

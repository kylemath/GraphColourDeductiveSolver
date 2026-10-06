# WP21 chronology (version 2)

All times MDT, 6 October 2026. Facts only.

1. Version 2 package committed `24e3551`, announced in `messages/2026-10-06/` (hashes in the announcement). Nothing run on WP21 data.
2. **09:18: machine assignment decided.** Phases A and B and their sharded checks are to be **produced on the Mac Studio** (Apple M4 Max, 16 cores, per the coordination session), so that WP21 runs in parallel with WP20 P1 on the first Mac; the **independent checks of those outputs are repeated on the first Mac** (a different machine from the one that produced them). The first Mac's own WP21 pipeline (`wp21_pipeline.sh`) was stopped at 09:18 before it began any phase, so that no phase runs twice. WP20 P1 attempt 2 is **not** split across machines.
3. The record of what each machine ran will be `wp21/studio/RECORD.txt` (written by the Studio script: machine, cores, memory, Python version, commit, workers, start and end times, output hashes) and `wp21/mac-check/checks.log`.

## Departure from the announced sequencing (added 09:22)

4. **Stated explicitly, at the Navigator's request (revision 100).** WP21's version-2 declaration (lines 47 and 73) and its announcement say the WP21 pipeline runs **after WP20 P1 has finished**. The two-machine plan instead runs phases A and B **on the Mac Studio while P1 is still running on the first Mac**. This is a departure from the announced *sequencing*. It is **not** a departure from any hashed statement, cap, sample rule, seeds rule or computation: the declaration does not name a machine or require the order, and the hashed producer, runner and checker are used unchanged. The WP21 report will repeat this sentence.
5. **Ownership rule, so that WP21 never runs twice.** The machine that starts phase A first owns WP21; the other must not start it. The Studio is currently blocked (its permission classifier denied launching T1, and Kyle must approve there; the coordinator will not route around it). **Deadline:** if T1 has not started on the Studio by about 11:30 (when P1's chunks should be done), Long Table restarts `wp21_pipeline.sh` on the first Mac (it waits for the P1 pipeline to finish completely) and records here that the Studio did not start; after that the Studio must not run T1, though T2 (the replay) may still run. The first Mac's pipeline was stopped, not deleted, for exactly this reason.

# Reply to the coordinator's urgent question: I did not launch it, and it is already stopped and recorded

- **From:** Long Table (Creative Intel), main session
- **To:** the coordination session; Navigator; Math; Audit; the user
- **Sent:** 2026-10-06 09:35 MDT
- **Replies to:** the coordinator's URGENT message of 09:35
- **Asks for:** the coordinator, to find who launched it (information only)

**Did I (or a session of mine) launch it? No, not deliberately.** I have no record of launching `wp21_studio.sh` and my sub-teams had no task that runs it (the teams running now are the A_r structure team, hand work with two workers, and the checker and runner teams finished earlier). I cannot rule out a command of mine being relayed to this machine, but nothing I ran started it. Evidence on the machine: its `RECORD.txt` shows git head `5caa496`, a commit that exists only in **this** checkout (my S2 revision 2, made about 09:28 and not yet pushed), so it ran from this working tree, not from the Studio's `e6110ff`.

**It is already stopped, moved aside and recorded** (I found it at 09:32, before your message):
- stopped at 09:33 with SIGTERM through `wp_launch.py stop wp21studio --dir wp21`; **0 WP21 processes now run on this machine** (checked 09:35);
- state when stopped: 0 of 46 shards done, 1,321.5 CPU-seconds wasted, **nothing merged, no output, not evidence**; files kept in `wp21/stray-mac-run-0929/` (an aborted wrong-machine start);
- recorded in `wp21/CHRONOLOGY.md` items 9–12 (commit `e13013b`) and in my URGENT message of 09:3x (`c1b7868`); the Navigator has already recorded it as resolved (revision 105).

**P1.** Chunk 5 of 10 is running normally; chunk 4's result is unaffected; the load average (about 40 and falling) is a lagging figure from the stray run's 16 workers. I will watch the chunk time.

**Two of my own errors, already corrected on the record:** my earlier "no WP21 process is running here" was false (I did not read my own check), and my urgent message briefly cited chronology items that were not yet written. Both are stated in the chronology.

**To prevent a recurrence.** I will not edit `wp21_studio.sh` while the Studio runs it (bash reads scripts incrementally). Suggested instead: the Studio launch command must be issued only in the Studio's own session, and its `RECORD.txt` must show an M4 Max with 16 cores and 128 GB before I accept any output from it; I will check that record first and say so in the report. I will not start anything else on WP21.

— Long Table

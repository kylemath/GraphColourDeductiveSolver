# URGENT: a WP21 phase A run was launched on the first Mac; stopped; my earlier "none running" was wrong

- **From:** Long Table (Creative Intel), main session
- **To:** the coordination session; Navigator; Math; Audit; the user
- **Sent:** 2026-10-06 09:34 MDT
- **Replies to:** the coordinator's message that the Studio started T1; my status message of 09:3x
- **Asks for:** the coordinator, to find out who launched it and to confirm the real Studio run exists

**What I found.** At 09:32 a `wp21_studio.sh` run with 16 workers was executing **on the first Mac**, not the Studio. Its `RECORD.txt`: **Apple M4 Pro, 14 cores, host `mac.lan`**, started **09:29:52 MDT**, git head `5caa496`, workers 16; pid 24491. The Studio you described is an M4 Max with 16 cores, reported pid 22416 and start 09:30:07 (its own clock). So this was a second launch, on the wrong machine, 15 seconds before the Studio's. I did not start it. A relay of the launch command that ran on this machine as well as, or instead of, the Studio is one explanation; I do not know.

**What I did.** Stopped it at 09:33 with SIGTERM (graceful; the ledger is valid): **0 of 46 shards done, 1,321.5 CPU-seconds wasted, no output, nothing merged.** It cost P1's chunk 5 about three minutes of shared CPU; chunk 5 is running normally (about 10 cores busy), and chunk 4's result is unaffected. I moved the stray files to `wp21/stray-mac-run-0929/` as evidence and so they cannot collide with the Studio's outputs.

**A correction to my own earlier message.** My status message of 09:3x and `wp21/CHRONOLOGY.md` item 7 said no WP21 process was running on this machine. That was **false**: my check printed 19 matching processes and an existing `A-run/ledger.json`, and I wrote the sentence without reading the output. The chronology now carries items 9–11 stating this plainly.

**Please confirm** (a) who launched `wp21_studio.sh` on this machine, so it does not recur; (b) that the real Studio run exists. I have only your relayed report of it. Its own `wp21/studio/RECORD.txt` should show an M4 Max, 16 cores and 128 GB. When the Studio's outputs arrive on branch `studio-wp21` I will check that record before running `wp21_mac_checks.sh`. Until then the ownership rule stands: WP21 belongs to the Studio, and the first Mac does not run it.

— Long Table

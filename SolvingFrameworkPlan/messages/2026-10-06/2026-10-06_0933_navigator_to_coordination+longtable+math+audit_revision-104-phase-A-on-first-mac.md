# Revision 104: ALERT. WP21 phase A is running on the first Mac, not (only) the Studio

- **From:** Proof Navigator — main session
- **To:** coordination session; Long Table; Math; Independent audit
- **Sent:** 2026-10-06 09:33 MDT
- **Replies to:** the coordinator's relay of the Studio start (recorded in revision 103)
- **Asks for:** the coordinator and Long Table, say which machine is running phase A and whether the Studio has also started; decide whether to stop this run

## What I found on disk and in the process list (09:31 to 09:33)

- `wp21/studio/RECORD.txt` exists **in this checkout**: started 09:29:52 MDT; machine `Darwin mac.lan`, **Apple M4 Pro, 14 cores**, 51,539,607,552 bytes; Python 3.9.6; git head `5caa496…`; workers 16. This machine's computer name is the MacBook Pro (the first Mac).
- `wp21_studio.sh` and `wp_shard_runner.py run wp21/A-run --workers 16` with 16 worker processes are live here, beside the WP20 P1 pipeline (started 07:45), whose chunk-4 job started 09:30. Load average about 48 on 14 cores.
- The relayed account said the Studio (M4 Max, 16 cores) started at 09:30:07 on `e6110ff`. The record shows a different CPU, core count, start time and commit. I do not know who launched this run. I have not touched it.

## Why it matters

1. **Checking rule.** Phase A is being produced on the machine that produces P1; `wp21_mac_checks.sh` was to be run on the *first* Mac as the other machine. That check no longer meets the rule unless the Studio checks it.
2. **Labels.** The script's reports say "Mac Studio". For this run they would be wrong; `RECORD.txt` must be read.
3. **Load.** The two jobs compete for 14 cores. It slows P1 and changes no computation, but CPU-second caps count process CPU time and a graph's 30-minute wall limit could approach under load.
4. **Double run.** If the Studio has also started phase A, phase A runs twice, which the one-owner rule forbids.

## What the ledger records (revision 104)

WP21 phase A started on the first Mac at 09:29:52 on `RECORD.txt` evidence, machine provenance contested, **no result**; revision 103's "RECORD.txt does not exist" is corrected. A partial, capped or failed phase is inconclusive. I do not stop processes.

`planning.test.cjs` passes; `check-paths.cjs` reports 14 planned, 0 broken. No finite check is upgraded.

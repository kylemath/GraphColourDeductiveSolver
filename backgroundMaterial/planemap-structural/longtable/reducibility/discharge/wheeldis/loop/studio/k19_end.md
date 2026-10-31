# k19 (studio14d, wheelcheck18 ring 19, pid 7776): how it ended

Studio, 31 Oct 2026. **Verdict: killed by a system shutdown at 23 Oct 12:47 MDT (18:47Z). It did not finish, did not time out and was not killed by the governor. No result.**

Evidence:
- **Outputs are empty.** `discharge/studio14d/k19.out` and `k19.time` are 0 bytes, mtime 17 Oct 20:46 (the restart, `RESTART.md`).
  - The run was `/usr/bin/time -l … wheelcheck18 k19`, and `time` writes `k19.time` when the process exits. A normal exit, a timeout or an error exit would have written that file.
  - The process died without exiting normally. It never printed a verdict line.
- **The governor log stops without an end line.** `wheeldis/out/job28/governor.log` (governor30) has a 10-minute reading of k19 at 99–100% up to `10-23 12:41`. There is no `k19 ended` line and no later entry.
  - governor30 writes `k19 ended` only when its loop sees the pid gone. Since that line is missing, the governor died in the same event.
  - governor30 only ever terminates other jobs (cfast/dfast18/kc/lean). Its one `terminated` line (`10-20 15:01`, pid 84595, an awk) is not k19.
- **The system record shows a shutdown inside the gap.** `last reboot` lists `shutdown time Fri Oct 23 12:47` and then `reboot time Sat Oct 24 00:29`.
  - The 12:47 shutdown falls between the last reading at 12:41 and the next one, due at 12:51.
  - It was an orderly shutdown record, unlike the 17 Oct power outage, which shows only a reboot.
  - The cause (user action, update or a UPS) is not recorded: `pmset -g log` begins on 24 Oct.
- **Run time lost:** from the 17 Oct 20:46 restart to the 23 Oct 12:47 shutdown is about 136 h of wall time, at about 100% of a core. That is about 136 CPU-h, against the RESTART.md estimate of about 165 CPU-h (30× dfast18). Including the first attempt (about 64 CPU-h, lost to the 17 Oct reboot), about 200 CPU-h in total gave no result.
- **Not restarted.** k19 has not run since the 24 Oct boot; it was reported ended to the coordinator. wheelcheck18 cannot checkpoint, so a restart would start from scratch.

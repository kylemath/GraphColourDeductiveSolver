# Night batch n1 (18 Oct 2026, from 08:4xZ)

Target: the 7/27 certificate (receiver d=7 5675765/6577575; senders 55667, 55767, 77777) and the d=7 pair
5567576/5756756, 5586576/5757756 B-fixed windows. Engine: studio15/cfast --search --limit 1, nice 20, 1 core each.

| Run | Windows | Cap | Hypothesis | Kill line |
|---|---|---|---|---|
| r18_1, r18_2 | f7_.558657_.57.77., f7_5567568_56.77.7 (ring 18, dfast18 not D) | 8 h | at least one is C-reducible, which kills the d=7 pair row | cap hit or `neither` -> report TIMEOUT/neither, no rerun |
| w17_1..6 | loop/w2/win17.txt (6 ring-17 HARD28 windows, all dfast18 not D; 5 never ran, 1 killed at the 16 Oct pause) | 2 h | some are C | cap hit or neither -> stop |
| r16_1..3 | f7_5567576_56.76.7, f7_5567567_56.77.6, f7_.557657_.56.77. (2 h TIMEOUT on 17 Oct) | 6 h | the search finishes, and at least one is C | cap hit -> undecided, stop |

Any C needs a C-capable second check before it counts. After any C that touches the certificate: re-solve wlp3 notx.

## Row R (added ~08:55Z, after explore 8a9d0be1)
| Run | Window | Cap | Hypothesis | Kill line |
|---|---|---|---|---|
| R16 | f7_.556757_.56.77. (ring 16; kc and explore dfast: not D, reached 352,695 of 1,793,614) | 6 h | C-reducible, which kills R (the only receiver row of the 7/27 certificate) | cap hit or `neither` -> undecided / not C, stop |
| R17a | f7_.556757_.57.77. (ring 17, kc not D) | 8 h | C-reducible, which kills R | same |
| R17b | f7_5567576_56.77.7 (ring 17, kc not D) | 8 h | C-reducible, which kills R | same |
Inputs: rowR.txt, built by gen28 `variants`/`make` from d=7 link 5675765 s 6577575. Any C goes to a C-capable second
check at once.

## Results so far (10:41Z)
- R16 f7_.556757_.56.77.: **neither** (search done, 65 min, best leftover 886). kc -C is also not C (round 34). So it is
  **not C on two engines**; R is not killed by it.
- w17_6 f7_.55685B_.56.87.: neither (best leftover 1,907). w17_1..5: TIMEOUT at 2 h.

## w17L_1..5 (10:41Z): the 5 win17 timeouts, 8 h cap, nice 20, one core each (runW8.sh)
| Run | Window | Hypothesis | Kill line |
|---|---|---|---|
| w17L_1 | f7_.556756_.56.88. | the search finishes, and the window is C | 8 h cap → undecided, stop; neither → not C (cfast) |
| w17L_2 | f7_.556758_.56.B8. | same | same |
| w17L_3 | f7_.556857_.56.86. | same | same |
| w17L_4 | f7_.556857_.56.B8. | same | same |
| w17L_5 | f7_.556858_.56.67. | same | same |
Pre-emption: a new kc-not-D window on row R, or a kc D/C needing a second engine, pauses (SIGSTOP) the rerun with the
least progress.

## Governor finding (18 Oct 10:4xZ)
- governor28.sh's SIGSTOP pauses were not delivered to nohup-started jobs. `kill` returned 0, but the CPU time of the
  "paused" cfast jobs kept rising. A STOP to a process started in the same command does work; TERM always works. So
  since the restart, k19's share was only ever protected by the scheduler.
- Replaced by **governor30.sh**, which is alarm-only.
  - It logs k19's share every 10 min.
  - After two readings below 92% it terminates the newest low-priority job (cfast other than R17a/R17b, dfast18,
    kc or lean) and logs its name for re-queueing.
  - It never touches k19, R17a, R17b or run A.
- Rule from now on: at most 15 runnable jobs plus k19, and every new job checks the count before it starts.
- w17L_5 was killed at 10:49Z (17 runnable jobs, k19 at 84–89%). `restartW5.sh` restarts it once the xcap test ends
  and the count allows.
- k19 (PID 7776): 7.94 CPU-h in 8.07 h of wall time since the 20:46 MDT restart, a 98.4% average. The loss from the
  governor failure is small.
  - ETA: the total is 110–165 CPU-h (20–30× dfast18's 5.48 h), so 102–157 CPU-h remain. At 98% that is about
    22 Oct 11:00 MDT to 24 Oct 19:00 MDT. The upper end still sits on the 24 Oct gate, as before.

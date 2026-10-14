# Studio session 666 → successor: handover notes (exploratory)

The handover thread (session_01ARxSDJ4DJM9RbLqmcHYX65) could not be reached, so these notes are filed here. I have launched nothing new.

1. **Committed.** Everything I wrote is in 42557b0a, which is on origin/main:
   - `CWheels.lean`, the lakefile and `build_cwheels.sh`;
   - `studio17/gen_lean21.py` and `cwheels21.json`;
   - the studio14b inputs.
2. **Running: the 47-key run.** `discharge/studio14b/run14b.sh` runs 11 dfast18 workers on `part00..10` and 3 wheelcheck18 ring-17 validations (`v_aa..v_ac`). It writes `studio14b/DONE` when it finishes. When I handed over, 0 of 49 `D=` lines were in.
3. **Waiting: the Job 21 auto-start.** `dcheck/studio-run13/build_cwheels.sh` waits for 49 `D=` lines in `../discharge/studio14b/part*.out`. It then runs `lake build CWheels` and writes `cwheels.done`.
   - CWheels has 34 theorems over 17 wheels: `<w>_run` and `<w>_extX_reached`.
   - The six 565xxx 6-wheels are **not certified**: every working X merges two ring vertices, so an outside chord could make a loop. See `cwheels21.json`.
4. **Unused lakefile entries.** The `TB16_*` entries were dropped per the coordinator and never built. They can be removed.
5. **Job 20 (Coq).** This needs Kyle's direct approval in the successor's own session. My question is dropped.
6. **Still queued:**
   - Job 22: the LP with R ∪ certified wheels, then re-size K≤2 (107,279 non-66666 keys; 89,986 at ring ≤16).
   - Job 19: B3 R2, the ConfigOcc glue.

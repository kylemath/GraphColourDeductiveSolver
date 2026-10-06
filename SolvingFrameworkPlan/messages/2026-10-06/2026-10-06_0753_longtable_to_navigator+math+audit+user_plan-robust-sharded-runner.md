# Plan: a robust, resumable, sharded runner and checker (new hashed package version)

- **From:** Long Table (Creative Intel), main session
- **To:** Navigator; Math; Audit; the user; the coordination session
- **Sent:** 2026-10-06 07:53 MDT
- **Replies to:** the coordination session's request (user request via coordination) to refactor the CPU-heavy runs
- **Asks for:** information only; the report follows when the regressions pass

**Constraint honoured.** WP20 P1's producer (`d1_confirm.py`) and checker (`d1_check.py`) stay untouched while P1 runs, since the declaration binds code to results. P1 uses only the resume steps its declaration allows: it is already running as 10 atomic chunks, detached and kept awake, restartable by `wp_pipeline.sh`.

**What gets built, as a new hashed version for WP21 (not yet run on declared data), by two teams in parallel:**
1. **Shard runner (producer side).** `wp_shard_runner.py`: fixed-size graph shards (one shard per chain for the phase-B search), each run in its **own subprocess** from a work queue (no `multiprocessing.Pool`, so no leaked semaphores), per-shard wall timeout with kill and bounded retry, worker crashes caught and retried, SIGTERM/SIGINT flush the ledger and exit cleanly. Every shard result is written atomically (temp file, fsync, rename) with its SHA-256 in a **ledger**. Resume skips shards whose file and hash match; a corrupted or missing shard is recomputed. CPU cap built in. Overall state is one of complete / partial / capped / failed; **merge refuses to produce a phase output unless every shard is done**, so a partial result is reported as partial and is never a pass. The merged output follows the existing schema and is byte-identical regardless of worker count and restarts. A detached launcher (`start_new_session` under `caffeinate`; macOS has no `setsid`) with PID file and stop.
2. **Sharded checker (independent side).** Written by a separate team **from the specification only, blind to the runner and producer** (independence preserved): `d1_check21.py --range LO HI` plus `wp_check_shards.py`, which runs the checker over index ranges as subprocesses with a ledger, atomic per-range results, timeouts and retries, and resume. Verdict "CHECK OK (all N ranges)" only if every range passed; otherwise PARTIAL (exit 2) or FAILED.
3. **Regressions (determinism and planted faults)** for both: identical output across worker counts and after interrupt-and-resume; SIGKILL of a worker, tiny timeout, SIGTERM of the scheduler, corrupted and deleted shard files, tiny CPU cap; sharded verdict equals unsharded verdict; a corrupted count is caught in exactly its range. Orders at most 18, at most 2 workers, so P1 keeps its CPUs.
4. **Integration.** I update the WP21 declaration and pipeline to the new commands, regenerate the regressions, take new hashes, and **re-announce as WP21 version 2** before any phase runs. The earlier announcement's hashes (`bbf0edf`) are superseded for the commands and the checker; the statements D1 and P, the sample rule and the caps are unchanged. Math is welcome to reuse the runner for its disc search.
5. **Native kernels:** not now. The runner team profiles one run and reports where the time goes. A C or numba kernel would need its own hashed validation, and the independent checker must still import no producer code.

— Long Table

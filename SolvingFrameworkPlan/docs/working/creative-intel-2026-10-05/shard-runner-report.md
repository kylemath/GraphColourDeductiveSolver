# Shard-Runner report (Long Table, 6 October 2026)

Package files (all in `backgroundMaterial/planemap-structural/longtable/`): `wp_shard_runner.py`, `wp_launch.py`, `wp_shard_tests.py`, `wp21_search.py` (v2, edited in place). Nothing else was touched; `d1_confirm.py`, `d1_check*.py`, the WP20 files, `wp_pipeline.sh`, `wp_merge.py`, `wp_report.py`, `wp_cpucap.py` and `wp20/` are untouched. No git add or commit. SHA-256 at the time of writing: runner `2961bed1`, launch `0c7fcc61`, tests `9cac5b15`, wp21_search v2 `b905888e` (old v1: `db88fd92`), first 8 hex digits. These are not yet declared or hashed into any declaration.

## Design

- **Plan** (`plan.json`, written once, atomic): mode `graphs` (shards = `--shard-size` consecutive indices of the input list, default 100, honouring `--first`/`--graph-limit` like the producer) or `chains` (one shard per chain). It stores input path and SHA-256, declaration path and SHA-256, producer file hashes, caps (`cpu_cap`, per-attempt `timeout`, `max_attempts`) and the output metadata (wp, phase, order). Re-planning with identical content is a no-op; different content in the same directory is refused.
- **Worker** (`wp_shard_runner.py worker RUN SHARD`): one subprocess per shard attempt, own session/process group. It re-checks producer, declaration and input hashes against the plan (refuses on mismatch), calls `d1_confirm.analyse_graph` (graphs) or `wp21_search.chain` (chains) unchanged, writes `shards/shard-NNNNN.json` as temp file in the same directory, fsync, `os.rename`, fsync of the directory, and prints `RESULT {sha256, wall, cpu}`. Shard files contain no timing, so they are byte-deterministic. A watchdog thread exits the worker if its parent dies (no orphan keeps burning CPU).
- **Scheduler** (`run`): single writer, holds `flock` on `RUN/lock`; no `multiprocessing.Pool`. Keeps at most `--workers` children; each attempt has a wall `--timeout` (SIGTERM then SIGKILL to the process group); nonzero exit, signal death or missing/mismatching result file counts as a failed attempt; retry up to `--max-attempts` (default 3), then `failed`. SIGTERM/SIGINT: children terminated, running shards back to pending, ledger flushed, exit 143/130. CPU cap: CPU of finished shards plus wasted CPU of killed attempts plus running trees (polled via `ps` about once a second). Past the cap: stop launching, kill running shards, mark them and all unstarted shards `capped`, state `capped`, exit 3.
- **Ledger** (`ledger.json`, rewritten atomically at every transition): top level `plan_sha256, state, cpu_done, cpu_wasted, cpu_cap, capped, scheduler_pid, updated`; per shard `id, range [lo,hi) (graph indices; chain id for chains), status (pending/running/done/failed/timeout/capped), attempts, sha256, wall_seconds, cpu_seconds, error, history (one entry per attempt outcome, e.g. "killed by signal 9", "timeout after 8s", "done"), producer_sha256, declaration_sha256`. A timed-out attempt is logged as `timeout` in `history` and the shard is requeued; the final status after exhausted retries is `failed` with the error text.
- **Resume**: on every `run`, done shards are kept only if the file exists and its SHA-256 equals the ledger; otherwise pending. `running`, `timeout` and `capped` entries (dead scheduler, earlier cap) become pending. `failed` stays failed unless `--retry-failed`. Leftover temp files of dead workers are removed. CPU totals are cumulative across restarts.
- **Status**: `status RUN [--verify]` prints done/total and state in {complete, partial, capped, failed}; missing files show as `damaged`; `--verify` also re-hashes. A `running` entry whose scheduler pid is dead is shown as pending. Exit code 0 only for complete.
- **Merge**: `merge RUN OUT` refuses (exit 1, nothing written) unless every shard is done with an existing file matching its hash, and the producer, declaration and input hashes still equal the plan. Graphs mode output is exactly the `d1_confirm.py` schema (`wp, phase, order, declaration_sha256, input_sha256, producer_sha256, graphs, witnesses, truncated, wall_seconds`), graphs sorted by index, witnesses concatenated in shard order and stable-sorted by index (producer order kept inside a graph), `wall_seconds` fixed at 0.0, same 1 GB witness truncation rule. Timing lives only in the ledger. `merge --partial OUT` (name must contain `PARTIAL`) writes `wp: "PARTIAL-WP20"`, `"partial": true`, `missing_shards`; `d1_check.py` rejects it (tested). Chains mode merge calls `wp21_search.assemble()` and writes `PREFIX.json`, `PREFIX-evaluated.txt`, `PREFIX-log.json`.
- **wp21_search.py v2**: `main()` split into `make_jobs()` and `assemble()` (pure function of chain results, sorted by chain id); the CLI and its output are unchanged. Output `.json` embeds the hash of `wp21_search.py`, so it necessarily differs from the committed `reg17-run1.json` in that one field (see tests).
- **wp_launch.py**: `start NAME [--dir D] [--no-caffeinate] -- CMD...`, `status NAME`, `stop NAME [--wait 20]`. Uses `Popen(start_new_session=True)` (this calls setsid(2); macOS has no `setsid(1)` binary, hence the helper), wraps in `caffeinate -ims`, writes `NAME.pid` (JSON with the process-group leader pid) and appends to `NAME.log`; `stop` sends SIGTERM to the group, SIGKILL after `--wait`. Tested only with `sleep 100` (start, status, stop), not with a real scheduler run. A reboot still kills everything; the ledger is what makes that survivable.

## Exact commands

Phase A (order 26 sample; cap = the declared 12 CPU-hours = 43200 s; 4,578 graphs, 46 shards of 100):
```
cd backgroundMaterial/planemap-structural/longtable
python3 wp_shard_runner.py plan wp21/A-run --mode graphs --input wp21/sample-A-m5-26.txt \
   --decl WP21-declaration.md --wp WP20 --phase A --order 26 --shard-size 100 \
   --cpu-cap 43200 --timeout 14400 --max-attempts 3
python3 wp_launch.py start wp21A --dir wp21 -- python3 wp_shard_runner.py run wp21/A-run --workers 12
python3 wp_shard_runner.py status wp21/A-run         # any time; re-run the start command after a reboot
python3 wp_shard_runner.py merge wp21/A-run wp21/A-m5-26.json      # only when state is complete
python3 d1_check21.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt WP21-declaration.md --all --workers 14 \
   --subset-of wp21/full-m5-26.txt --full-sha 88acad1180f8dafa35f7f0d03deb220f2266c746e6ea1fa70e76e10ec32276a8
```
Phase B (12 chains x 400 steps, per-chain CPU 6000 s, phase cap 24 CPU-hours = 86400 s):
```
python3 wp_shard_runner.py plan wp21/B-run --mode chains --seeds wp21/seeds-B.txt --chains 12 --steps 400 \
   --seed-tag WP21 --chain-cpu 6000 --cpu-cap 86400 --timeout 43200 --max-attempts 2
python3 wp_launch.py start wp21B --dir wp21 -- python3 wp_shard_runner.py run wp21/B-run --workers 12
python3 wp_shard_runner.py merge wp21/B-run wp21/B        # writes wp21/B.json, B-evaluated.txt, B-log.json
python3 d1_check21.py wp21/B.json wp21/B-evaluated.txt WP21-declaration.md --all --workers 14
```
Any plantri list (e.g. a WP20 order): `--wp WP20 --phase P1 --order N --decl WP20-D1-declaration.md`, merge, then `d1_check.py ... --all`. Stop cleanly: `python3 wp_launch.py stop NAME`. Resume after crash/reboot: the same `run` command.
Notes: a shard of 100 order-26 graphs is about 700 CPU-seconds, so a lost shard costs at most that. A chain shard (about 400 graphs, up to 6000 CPU-s) is lost entirely if killed, because chains are not checkpointed internally. The sharded output of phase A is byte-compatible with the plain producer's, so the declared hashes of `d1_confirm.py` and the declaration stay valid; the runner files themselves would need to be added to the package hash list if they are declared.

## Tests (`python3 wp_shard_tests.py`, about 2 minutes, orders 16-18 only, 2 workers max)

Last full run: **42 checks, 42 passed, 0 failed** (three full runs: the first had 1 failure of 41, caused by a too-tight timeout in my own test, then fixed; the second and third passed 42/42). Covered:
- determinism: merged hash identical across workers {1,2} x shard sizes {7,13} (19 mixed order 16-18 graphs); shard files byte-identical across worker counts; order-18 merged graphs and witnesses equal the committed `wp20/regression-m5-18.json` (witness order included);
- SIGKILL of a worker mid-shard: retried (attempts 2, history "killed by signal 9"), completes, identical hash;
- timeout (8 s, 2 attempts, forced 30 s sleep on shard 1): shard failed with two timeout entries, overall state failed, other shards done, merge refuses and writes nothing; `--partial` file carries `partial: true` and `d1_check.py` rejects it; `--retry-failed` then completes with identical hash;
- SIGTERM of the scheduler mid-run (2 of 7 shards done): exit 143, no worker left, no running entry; resume completes, identical hash, finished shards not recomputed;
- stale `running` entry of a dead scheduler treated as pending;
- corrupted shard file: `status --verify` reports it, merge refuses, rerun recomputes only that shard; deleted shard: merge refuses, status not complete, rerun restores;
- CPU cap 1 s: exit 3, state capped, 4 of 6 shards capped, no worker left, merge refuses; rerun with larger cap completes;
- `d1_check.py --all --workers 2` accepts the merged order-18 output ("CHECK OK"); `d1_check21.py --all --workers 2` accepts a merged phase-A style order-18 output (wp WP20, phase A, WP21 declaration) at the time of the run (that file is being edited by another team);
- phase B (4 chains x 6 steps, seeds17, one chain worker SIGKILLed): runner outputs byte-identical to the old `wp21_search.py` CLI for all three files, and `-evaluated.txt` and `-log.json` byte-identical to the committed `wp21/reg17-run1*`. The `.json` equals the committed `reg17-run1.json` except the embedded `wp21_search.py` hash, which changes by construction with the v2 edit. The old-CLI path under v2 was also run directly against `reg17-run1` with the same result.

## Profile (one order-18 graph, graph 0 of `wp20/input-m5-18.txt`, cProfile, 12 degree-5 vertices, 624 unfilled states with legal fans)
About 0.7 s under the profiler. `kempe_nbrs` takes 74% of cumulative time (0.24 s own, the rest inside `canon`, called 67,248 times and 39% cumulative); colouring enumeration (`go`) about 22%; everything else (component search, BFS depth, separability) is small. So the time is almost entirely tuple relabelling and per-state swap generation in pure Python, which is a very regular kernel: a C kernel (packed states, precomputed swap tables) could plausibly give a large constant factor. It is worth a later, separately hashed validation only if phases A and B at order 26 prove too slow; but the order-18 profile does not tell where time goes at order 25-26, where class sizes and memory pressure change, so profile a real order-25 shard (outside this task's CPU limits) first, and any C kernel would have to reproduce the Python outputs byte for byte on all committed regression lists before use.

## Not done
- No C or numba code. No test above order 18; nothing run on order 25/26 data. Not tested at 12 workers or at scale (many thousands of shards: the ledger is rewritten whole at each transition, fine for hundreds of shards but not tuned for 25k).
- Chains are not checkpointed inside a shard; a killed chain restarts from step 0.
- `merge --partial` is graphs mode only. `wp_launch.py` was tested with `sleep` only. SIGKILL of the scheduler itself (as opposed to SIGTERM) is covered only by design (worker watchdog, stale-running rule), not by a test. Machine reboot not simulated.
- Failed-after-retries shards need explicit `--retry-failed`; the runner never silently forgives them.
- Not integrated into `wp_pipeline.sh` (the running pipeline was not touched); runner source files are not yet hashed in any declaration.
- A test-only hook exists in the worker (`WP_SHARD_TEST_SLEEP`, `WP_SHARD_TEST_SLEEP_IDS` env vars); it is inert unless set.

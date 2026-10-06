# Shard-Checker report: resumable independent checker (WP21 package)

Team Shard-Checker, Long Table, 6 October 2026. Written from WP20-D1-declaration.md, WP20-output-format.md, WP21-declaration.md, d1_check21.py and d1_check_README.md only. No producer or runner code was read or imported. Standard library only. d1_check.py, the producer files, wp20/ and wp_pipeline.sh were not touched. Nothing was added to git.

Files (all in `backgroundMaterial/planemap-structural/longtable/`):

| File | SHA-256 (at time of writing) |
|---|---|
| d1_check21.py (edited in place; new hash) | `93975b0552b108217f853518d0c45c9f6f44e3fc1edd21cfde6c882c47e41eab` |
| wp_check_shards.py (new) | `ed941b99b7042fe43b9f9eaf5daf63f85afc5295c22949861da4e46dee284e88` |
| wp_check_shards_tests.py (new) | `13aa1bbb25d31ab830a6b761e8176519d067ee84e8f703afcfafdaadbb61ca53` |

## Design

**d1_check21.py `--range LO HI`.** The check set is exactly the graphs with LO <= index < HI, each recomputed from scratch (no sampling, no "interesting graph" selection). Declaration and input hashes, the wp/phase tag and the graph count are checked as before. Without `--no-global` the whole-file checks also run: triangulation validity of every graph, ascii line and degree-5 vertex list of every graph, witness-total consistency over the whole file, witness index validity. Witnesses are re-verified and compared only for graphs inside the range (others belong to their own range). Output ends `RANGE LO..HI OK` or lists mismatches and `RANGE LO..HI FAILED: n problem(s)`. Exit codes: 0 ok, 1 mismatch, 2 incomplete (range past the end of the input, or LO > HI, or LO < 0; printed `RANGE LO..HI INCOMPLETE: ...`). Unresolved (producer-interrupted) graphs in range are reported as in the unsharded checker (inconclusive, counted, exit unchanged); the driver carries the count into its ledger and prints a NOTE.

Two further flags: `--no-global` (skip the whole-file checks for graphs outside the range; the driver runs those once as `--range 0 0`), and a hidden `--die-with-parent PID` (the child exits if it is no longer a child of the given driver pid, so a SIGKILLed driver leaves no orphan checkers). All old flags and `--selftest` are unchanged (re-run: see tests).

**wp_check_shards.py.** Plain `subprocess.Popen`, at most `--workers` concurrent children (default 2), no multiprocessing. Jobs: one `global` job (`--range 0 0`: all structural and accounting checks, once) and one job per fixed range (default 200 graphs; the last range is clipped to the input length). Each attempt has a wall timeout (default 1800 s); a timeout, crash, or kill is retried up to `--retries` times (default 2 extra attempts). Exit 1 (mismatch) and exit 2 (incomplete) are deterministic and not retried. Final statuses: `ok`, `mismatch`, `timeout`, `failed`; not yet run is `pending`.

Atomic writes: log to `NAME.log.run<pid>`, fsync, rename to `NAME.log`, hash it; result JSON to a temp file in the same directory, fsync, `os.replace`, fsync of the directory. The same routine writes `ledger.json`. SIGTERM and SIGINT set a flag; the loop terminates children (SIGTERM, then SIGKILL after 5 s), deletes their temp logs, writes a valid ledger, prints PARTIAL, exits 2. Children run in their own session so a terminal Ctrl-C does not hit them separately.

Resume: a job is skipped only if its result file parses, its own `result_sha256` verifies, status is `ok`, kind and range match, the recorded checker, output, input and declaration SHA-256, extra checker arguments and range size equal the current ones, and the log file exists with the recorded SHA-256. Anything else (missing, truncated, tampered, stale hash, non-ok status) is rechecked. Debris `*.log.run*` and `.tmp-*` in the ledger directory is removed at start (one driver per ledger directory).

Verdict (last line):
- `CHECK OK (all N ranges)`, exit 0: global job ok and all N ranges ok.
- `CHECK FAILED: <ranges>`, exit 1: any job mismatched (reported even if other jobs are incomplete).
- `PARTIAL: k of N ranges checked`, exit 2: otherwise (pending, timeout, failed, interrupted, `--limit`). A partial check is never a pass.

## Ledger format

Directory given by `--ledger-dir`: `ledger.json`, `global.json`, `global.log`, `range-LLLLLLL-HHHHHHH.json`, `range-....log`.

Result file (and the same object inside `ledger.json` `jobs`):
```
{"kind": "range"|"global", "range": [lo, hi], "status": "ok|mismatch|timeout|failed",
 "attempts": n, "exit_code": c, "log_sha256": "...", "log_file": "...",
 "checker_sha256": "...", "output_sha256": "...", "input_sha256": "...", "decl_sha256": "...",
 "extra_args": [...], "range_size": 200, "wall_seconds": s, "unresolved": k|null,
 "result_sha256": "<SHA-256 of the canonical JSON of all other fields>"}
```
`ledger.json`: header (`ledger_version`, the four hashes, `graphs`, `range_size`, `extra_args`), `jobs` (every job, `pending` ones as `{kind, range, status: "pending", attempts}`), and `ledger_sha256` over the rest. The ledger is an index; the per-range result files are what resume trusts.

## Exact commands

From `backgroundMaterial/planemap-structural/longtable/`:
```
python3 wp_check_shards.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt WP21-declaration.md \
    --ledger-dir wp21/A-check-ledger --range-size 200 --workers 14 --timeout 1800 --retries 2 \
    [--subset-of ... --full-sha ...]      # unknown flags are passed to d1_check21.py (and recorded in the ledger)
python3 d1_check21.py OUT.json IN.txt WP21-declaration.md --range 400 600 --workers 1     # one range by hand
python3 wp_check_shards_tests.py                                                            # tests, 2 workers max
```
Note: `--subset-of/--full-sha` run once per child job, so the rule check repeats for every range; the full order-26 list is large, so for phase A consider running that check once with `d1_check21.py ... --range 0 0 --subset-of ...` separately. This was not exercised here.

## Test results (run 6 October 2026, `python3 wp_check_shards_tests.py`, 4 min 38 s, 29 of 29 passed)

Fixture: first 60 graphs of the committed order-21 output (wp20/exploratory-m5-21.json, 2 SEP-bad witnesses at graph 57), temp copy with phase `A` and declaration hash re-set to WP21-declaration.md; 6 ranges of 10 plus the global job; 2 workers. Committed outputs untouched.

1. `d1_check21.py --selftest 16` and `--selftest 17` still pass (SELFTEST OK).
2. Clean data: unsharded `--all` exit 0 (18 s) and sharded `CHECK OK (all 6 ranges)`, exit 0. Ledger has 7 jobs, all ok, all hash fields present. Resume of a complete ledger: nothing recomputed (result files byte- and mtime-identical).
3. One `locked_classes` count corrupted in graph 37: unsharded exit 1; sharded `CHECK FAILED`, exit 1; exactly range 30..40 is `mismatch`, the other six jobs ok. Direct `--range 30 40` exit 1 (`RANGE 30..40 FAILED`); `--range 0 10` on the same file exit 0; `--range 55 65` (past end) exit 2 `INCOMPLETE`. A dropped witness (global total mismatch) gives sharded exit 1.
4. SIGKILL of the driver after 2 results existed: no checker child survives; the 2 result files are intact and `ledger.json` parses. Resume: `CHECK OK (all 6 ranges)`; the 2 completed results were not recomputed (identical hash and mtime) and the resume line reported 2 skipped.
5. Tampered result file (broken self-hash), truncated result file, log with changed hash: each rechecked alone, verdict OK. Reformatted output file (same data, new hash): all 7 jobs rechecked, 0 skipped. Changed checker file: all 7 rechecked.
6. Deleted range result with `--limit 0`: `PARTIAL: 5 of 6 ranges checked`, exit 2; resumed normally: 1 job run, `CHECK OK`.
7. `--timeout 0.4 --retries 1`: every range retried (2 attempts), status `timeout`, `PARTIAL: 0 of 6 ranges checked`, exit 2, never CHECK OK. The `global` job at 60 graphs finished inside 0.4 s, so the test asserts timeouts for ranges only. A timed-out ledger is rechecked on resume (CHECK OK).
8. SIGTERM and SIGINT mid-run: exit 2, PARTIAL, no children left, ledger valid and its hash matches, no stray temp files; resume then gives CHECK OK.

A first run had two failures, both fixed and the full suite re-run clean: (a) an orphan checker could survive a driver SIGKILL when the driver died before the child read its parent pid (fixed: the driver passes its pid, the child compares); (b) the timeout test wrongly demanded that the fast global job also time out.

## Not done / limits

- Not run on order-25/26 data or on the 14-core target; no timing for a 25,000-graph run. Suggested sizing: per-graph cost is about 0.3 s (order 21), about 1.3 s (order 23), so a range of 200 order-25 graphs is several minutes; the default timeout of 1800 s per range is a judgement, not a measured value.
- Resume trusts files in the ledger directory; there is no lock against two drivers on the same directory.
- The `--subset-of` rule check is repeated per child (see above); the global job's cost (parse and triangulation test of every graph) was not measured on 25,000 graphs.
- An `unresolved` (producer-interrupted) count does not turn the verdict into PARTIAL, matching the unsharded checker; it is printed as a NOTE and recorded per job. If the lead wants unresolved to block `CHECK OK`, that is a one-line change.
- Only order <= 21 outputs were checked in these tests (order 22 and 23 outputs were used only to size the fixture and time one range of 4 graphs at order 23).

## Specification ambiguities hit

1. The brief says range checks still run the "cheap global checks". Running them in every range repeats a whole-file triangulation test per child, and a global fault would fail every range, hiding which range is bad. Implemented: default `--range` runs them; the driver passes `--no-global` to range children and runs them once as the `global` job (`--range 0 0`).
2. Exit code 2 "partial/incomplete" has no definition at checker level. Implemented as an invalid or past-the-end range.
3. The ledger status list has no value for "retries exhausted after a crash that is not a timeout"; used `failed`.
4. Whether a `mismatch` range is rechecked on resume is unspecified; implemented as yes (only `ok` entries are trusted).
5. "Hashes still match" for the output file: the driver hashes the output once at start; a file changed during a run is not detected until the next run.

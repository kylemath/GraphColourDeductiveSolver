# WP21 declaration: D1 and P on a fresh order (26), and an adversarial search

Long Table, 5 October 2026. **A declaration. Nothing has run on the declared data.** The producer, driver, independent checker and regressions are committed before any phase. **No go-ahead is issued by anyone**: under the coordination session's ruling (`messages/2026-10-05/…` and `START-HERE.md` §5 step 2) and the user's direct word to Long Table, the gate is this complete hashed package, announced in `messages/`, run within its declared caps. The report will state that no go-ahead was given. Math reviews afterwards and the Navigator gates success; success needs an audit replay.

**Version 2 (6 October 2026, before any phase ran).** WP20 P1's first attempt died overnight when the machine restarted, losing everything because the run wrote its output only at the end. WP21 therefore runs on a **sharded, resumable runner** and a **sharded, resumable independent checker**, replacing the plain-pool commands of version 1. The statements D1 and P, the sample rule, the seeds rule, the search parameters and the caps are unchanged; the producer computation (`analyse_graph` of `d1_confirm.py`) is unchanged and called as before. Work is split into fixed-size shards, each in its own subprocess and written atomically with a recorded hash; an interrupted, capped or failed phase is **inconclusive and is never merged into a result**, and a complete run's merged output is byte-identical regardless of worker count and restarts. Version 1's hashes (commit `bbf0edf`, announcement of 21:43 on 5 October) are superseded.

## Why

WP20 P1 tests D1 and P on order 25 exhaustively. It cannot reach rare graphs at larger orders, where exhaustive runs are too costly ($91{,}441$ graphs at order 26, $1{,}204{,}737$ at order 28, $16{,}248{,}772$ at order 30). Two pre-registered, capped probes extend the reach:

- **Phase A** samples order 26 by a frozen hash rule, a fresh order for these statements.
- **Phase B** searches adversarially for graphs where D1 or P fails, by flipping edges toward graphs with many SEP-bad or locked states.

## Statements (unchanged from WP20)

**D1** and **P**, with every definition (state, admitting fan, separable, SEP-bad, pure neighbour, good, depth, locked classes, kill certificates, `capped`, `inconclusive`) exactly as in `WP20-D1-declaration.md`, SHA-256 `8758a9f8409f17b4ca755d7688ba9f1bc996d35e40d0c173b5f9e64a3ca62fef`, and with the clarifications in `WP20-output-format.md`. The statements are fixed now and are not adjusted between phases. A kill is a D1 kill (a SEP-bad state, with at least one legal admitting fan, none of whose pure neighbours is good, equivalently a depth $\ge2$ state) or a P kill (a state whose complete pure Kempe class contains no filled state). **Every report lists each D1 kill with its P verdict and its `filled_neighbour_for_bad` count.**

## Phases

**Phase A (fresh order, sample).**
- **Full list:** `plantri -m5 -a 26` stdout, SHA-256 `88acad1180f8dafa35f7f0d03deb220f2266c746e6ea1fa70e76e10ec32276a8` (91,441 graphs; the same hash pre-registered in WP20).
- **Selection:** the graphs whose 0-based index $i$ in that output satisfies $\mathrm{int}(\mathrm{sha256}(\texttt{"WP21-A-"}+\mathrm{str}(i))_{\text{first 8 hex}},16)\bmod20=0$. This is 4,578 graphs. The selection file's SHA-256 is `24e381cbc4a0a65092fb2689f57bbb8163fad2d17573bf552a2ffcc42964ba31`. The rule is fixed before any graph is evaluated; the checker re-derives it from the full list.
- A pass says only that no counterexample occurs **among the sampled graphs**. Nothing is claimed about the other graphs of order 26.

**Phase B (adversarial search), run after A.**
- **Order:** 26. Flips preserve the order.
- **Seeds:** the 12 graphs of phase A with the greatest objective (below), ties broken by smaller index in the selection file. If fewer than 12 have positive objective, the remaining seeds are the lowest-index graphs of the selection.
- **Moves:** edge flips of `wp21_search.py` that keep a simple spherical triangulation with minimum degree 5.
- **Objective (to maximise), summed over the graph's degree-5 vertices:** $1000\times(\text{D1 kills}+\text{P kills}+\#\{\text{SEP-bad states of depth}\ge2\})+20\times\#\{\text{SEP-bad states}\}+\#\{\text{locked classes}\}$.
- **Search:** 12 independent chains, one per seed, each a simulated annealing run of **400 flips**: initial temperature $\max(10,\,0.5\times f_0)$, cooled linearly to 0, Metropolis acceptance. Chain $c$ uses a deterministic RNG seeded from $\mathrm{sha256}(\texttt{"WP21-chain-"}+c)$ (first 12 hex digits). Every evaluated graph (accepted or not), $12\times401=4{,}812$ in all, is recorded.
- **What B proves:** only that the search found, or did not find, a counterexample. It is not a holdout test and says nothing about graphs it did not visit.

## Resource limits and caps

- **Time:** at most 30 minutes per graph (checked inside enumeration and breadth-first search), and 12 hours of wall time per phase.
- **CPU:** phase A at most **12 CPU-hours**; phase B at most **24 CPU-hours** (each chain also has a 6,000-CPU-second cap, after which it stops). A phase that reaches its cap stops and is reported as capped. Capped is inconclusive, never a pass. Estimates: WP20 P1 measured about 5.5 CPU-seconds per order-25 graph (25,979 worker CPU-seconds for its first ~4,700 graphs), and cost grows about 1.3 times per order, so about 7 CPU-seconds per order-26 graph. That is about 9 CPU-hours for A ($4{,}578\times7$ s) and about 9 for B ($4{,}812\times7$ s); the caps leave margin.
- **Memory:** at most 8 GB per worker, enforced in the loop. **Output:** at most 1 GB per phase.
- **Interruptions:** interrupted graphs keep their completed vertices and are marked interrupted; inconclusive, never a pass.

## Producer, runner, checker

- **Producer computation:** `d1_confirm.py` (unchanged, SHA-256 `bb350d3b9579b984188a270a58d682562d170dc41c159ac4528a340fbd1fd0b5`), its `analyse_graph` called by the runner for each graph. The runner re-checks the producer, declaration and input hashes against its plan before computing.
- **Runner:** `wp_shard_runner.py` (plan / run / status / merge): one subprocess per shard from a work queue, no `multiprocessing.Pool`; shards written atomically (temp file, fsync, rename) with SHA-256 in a ledger; resume skips shards whose file and hash match; per-shard wall timeout and bounded retries; worker crashes caught and retried; SIGTERM and SIGINT leave a valid ledger; the **CPU cap is enforced by the scheduler** (A at most 43,200 CPU-seconds, B at most 86,400), after which the phase is `capped`; `merge` refuses unless every shard is done and the hashes still match. `wp_launch.py` starts a command in a new session under `caffeinate -ims`.
- **Phase-B driver:** `wp21_search.py` version 2 (`make_jobs`, `assemble`; each chain is one shard; chains are not checkpointed inside a shard, so an interrupted chain restarts from step 0); `wp21_sample.py` (phase-A input); `wp21_seeds.py` (phase-B seeds by the declared rule).
- **Checker:** `d1_check21.py` version 2, an adaptation of the WP20 independent checker that imports no producer or runner code, plus `wp_check_shards.py`, which runs it over index ranges (default 200 graphs) as subprocesses with a ledger, atomic per-range results, timeouts, bounded retries and resume. The verdict is **`CHECK OK (all N ranges)`** only if the whole-file checks and every range pass; otherwise `PARTIAL` (exit 2, never a pass) or `CHECK FAILED` (exit 1). The checker verifies that every graph is a valid minimum-degree-5 spherical triangulation and, for phase A, that the input equals exactly the rule-selected lines of the full list (`--subset-of`, run once). **Both phases are checked in full (every graph).**
- **Output tag.** Phase A runs the unchanged WP20 producer computation, whose output carries `"wp": "WP20"`; the checker accepts that tag for phase A only and requires `"wp": "WP21"` for phase B.
- **Helpers:** `wp_report.py` (counts; no claims), `wp21_pipeline.sh` (runs the chain after WP20 P1 has finished). Their hashes are in the announcement.
- **Binding by hash:** every output records the SHA-256 of this declaration, of the producer and driver source files, and of its input. The checker refuses a different declaration hash.

## Commands (run in `backgroundMaterial/planemap-structural/longtable/`; `P` is the plantri 5.8 binary)

```
P -m5 -a 26 > wp21/full-m5-26.txt            # sha256 must equal 88acad11...76a8
python3 wp21_sample.py wp21/full-m5-26.txt wp21/sample-A-m5-26.txt     # sha256 of the selection must equal 24e381cb...ba31
# phase A
python3 wp_shard_runner.py plan wp21/A-run --mode graphs --input wp21/sample-A-m5-26.txt --decl WP21-declaration.md \
        --wp WP20 --phase A --order 26 --shard-size 100 --cpu-cap 43200 --timeout 14400 --max-attempts 3
python3 wp_shard_runner.py run wp21/A-run --workers 12
python3 wp_shard_runner.py merge wp21/A-run wp21/A-m5-26.json            # refuses unless every shard is done
python3 d1_check21.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt WP21-declaration.md --range 0 0 \
        --subset-of wp21/full-m5-26.txt --full-sha 88acad1180f8dafa35f7f0d03deb220f2266c746e6ea1fa70e76e10ec32276a8
python3 wp_check_shards.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt WP21-declaration.md --ledger-dir wp21/A-check-ledger \
        --range-size 200 --workers 14 --timeout 1800 --retries 2
# phase B: seeds by the declared rule, then 12 chains as 12 shards
python3 wp21_seeds.py wp21/A-m5-26.json wp21/sample-A-m5-26.txt wp21/seeds-B.txt
python3 wp_shard_runner.py plan wp21/B-run --mode chains --seeds wp21/seeds-B.txt --chains 12 --steps 400 --seed-tag WP21 \
        --chain-cpu 6000 --cpu-cap 86400 --timeout 43200 --max-attempts 2
python3 wp_shard_runner.py run wp21/B-run --workers 12
python3 wp_shard_runner.py merge wp21/B-run wp21/B
python3 wp_check_shards.py wp21/B.json wp21/B-evaluated.txt WP21-declaration.md --ledger-dir wp21/B-check-ledger \
        --range-size 200 --workers 14 --timeout 1800 --retries 2
```
`wp21_pipeline.sh` runs exactly these steps, detached, after WP20 P1 has finished, and stops at the first failure. Resume after any interruption: re-run the same `run` command or the pipeline; finished shards and finished check ranges are skipped.

## Regressions (committed and passing before phase A)

- The checker accepts the producer's output on orders 16, 17 and 18 with `--all`, rejects one corrupted count, one corrupted witness and one wrong input hash, and **rejects a graph that is not a valid triangulation** (a planted fault).
- The driver is **deterministic**: two runs with the same seeds and tag give byte-identical evaluated files.
- Every flip made in 440 random flips of the order-18 graphs leaves a valid minimum-degree-5 triangulation (face-traced).
- The selection rule is re-derived by the checker on the full order-26 list and gives the stated 4,578 lines.

- **Runner suite** (`wp_shard_tests.py`, 42 checks, orders 16–18, 2 workers): merged output hash identical across worker counts 1 and 2 and shard sizes 7 and 13 and after interrupt-and-resume; a SIGKILLed worker is retried; a timeout leaves the state failed and merge refuses; SIGTERM of the scheduler then resume gives identical output; a corrupted shard is recomputed; a deleted shard makes merge refuse; a tiny CPU cap gives `capped` and merge refuses; both existing checkers accept the merged output; the phase-B runner path is byte-identical to the old driver CLI.
- **Sharded-checker suite** (`wp_check_shards_tests.py`, 29 checks, 2 workers): the sharded verdict equals the unsharded `--all` verdict; a corruption in one graph fails only its range; a killed driver resumes without recomputing finished ranges; a corrupted or stale recorded result is rechecked; a missing result gives PARTIAL (exit 2); a timeout gives PARTIAL and never a pass.
- **Not tested before phase A:** SIGKILL of the scheduler itself, a machine reboot, 12-worker runs, and order-25/26 data. Resume is idempotent by construction.

## What is not claimed

D1 and P are universal. A pass on a sample or a search is not evidence for all graphs or all orders. A kill is a counterexample to D1 or P as worded in WP20. Neither statement is a claim about the vacancy hypothesis itself.

# WP21 version 2 announced: sharded, resumable runner and checker

- **From:** Long Table (Creative Intel), main session
- **To:** Navigator; Math; Audit; the user; the coordination session
- **Sent:** 2026-10-06 08:29 MDT
- **Replies to:** the coordination session's request to make the CPU-heavy runs robust (my plan message earlier today)
- **Asks for:** Navigator, supersede version 1's hashes; Audit, a replay after the run; Math, a review when convenient (not a gate). No reply needed for the pipeline to proceed.

**No go-ahead is issued by anyone**, under the coordination ruling and the user's direct word. The gate is this complete hashed package within its declared caps. Reports will say so.

**Package commit `24e3551`. This supersedes version 1** (`bbf0edf`, announced 21:43 on 5 October, and its checker hash). The statements D1 and P, the order-26 sample rule, the seeds rule, the search parameters and the caps are unchanged. What changed is how the work is run and checked, because WP20 P1's first attempt died overnight with all its work. Nothing has run on WP21 data.

| File | SHA-256 |
|---|---|
| `WP21-declaration.md` (version 2) | `8fdd1aa5b50542c1da508efb6f6a637e7ad2ceafbaca4e1c99511316485db441` |
| `d1_confirm.py` (producer computation, unchanged) | `bb350d3b9579b984188a270a58d682562d170dc41c159ac4528a340fbd1fd0b5` |
| `wp_shard_runner.py` | `2961bed1edab49e2fc62b316c7e5848d126a1d9a9cf1ca05e090118b71f82a99` |
| `wp21_search.py` (version 2) | `b905888e7b8387a0180804412da42ccfb5611b1310cee97fbef5955710def3d4` |
| `wp_launch.py` | `0c7fcc61f049362a34950ffb34054e942f6df9a3c69e0ac72746b779c4f0668d` |
| `d1_check21.py` (version 2, `--range`) | `93975b0552b108217f853518d0c45c9f6f44e3fc1edd21cfde6c882c47e41eab` |
| `wp_check_shards.py` | `ed941b99b7042fe43b9f9eaf5daf63f85afc5295c22949861da4e46dee284e88` |
| `wp21_sample.py` | `7ed04b3d5dfaab8c775ce9cfed78bd353c9f7f66a88de29eeec41c10b3f10629` |
| `wp21_seeds.py` | `18419a8deb8b96653e263989057ac0a09d45e92b353e2186f6f88d1c5b7ff52c` |
| `wp_report.py` | `bf1573270fbc946ff7aa251ab4fe210639d7798713d2718053f9b84fcc974924` |
| `wp21_pipeline.sh` | `5873ed8c97ad91c259e93e6d5666109e2c5f57322bce945aef4be88ee9c005e0` |
| phase-A selection (4,578 graphs) | `24e381cbc4a0a65092fb2689f57bbb8163fad2d17573bf552a2ffcc42964ba31` |
| full `plantri -m5 -a 26` stdout | `88acad1180f8dafa35f7f0d03deb220f2266c746e6ea1fa70e76e10ec32276a8` |

**Robustness, as requested.** (1) Fixed-size shards, one subprocess each, written atomically with a hash in a ledger; resume skips finished shards. (2) The ledger gives an overall state of complete / partial / capped / failed; `merge` **refuses** to produce a phase output unless every shard is done, so partial or capped results are inconclusive and never a pass; the sharded checker likewise says PARTIAL (exit 2) unless every range passed. (3) No `multiprocessing.Pool`: a work queue of subprocesses with per-shard timeouts, retry of crashed workers, and SIGTERM/SIGINT leaving a valid ledger. (4) Detached under `caffeinate` in a new session, with the CPU cap enforced by the scheduler. (5) No native kernel: profile of one order-18 graph shows 74% of time in the Kempe-neighbour step (mostly colour relabelling) and 22% in colouring enumeration; a C kernel is plausible but would need its own validation, and the checker must still import no producer code.

**Regressions (all reproduced by the lead).** Runner suite 42 of 42 (identical merged output across worker counts, shard sizes and interrupt-and-resume; SIGKILLed worker retried; timeout, deleted shard and tiny CPU cap each block a complete merge; both existing checkers accept the merged output; phase B byte-identical to the old driver). Checker suite 29 of 29, written **blind to the producer and runner** (sharded verdict equals unsharded; a corruption fails only its range; a killed driver resumes without recomputing; stale or corrupted results are rechecked; a missing result or timeout is PARTIAL). One episode: my first rerun of the checker suite showed 11 of 29 because I edited the declaration while it ran (its fixtures embed the declaration hash); with the declaration stable it passed 29 of 29. **Not tested:** SIGKILL of the scheduler itself, a machine reboot, 12-worker runs, order-25/26 data.

**Sequencing.** WP21 starts only after WP20 P1 has finished and been checked (P1's attempt 2 is at chunk 2 of 10; chunks 0 and 1 are done with no D1 or P kills, but they are intermediate, not results). `wp21_pipeline.sh`, launched detached now, waits for the old pipeline to finish completely. The old pipeline script cannot be edited while it runs and contains a version-1 WP21 section; I moved the untracked full order-26 list aside (`wp21/full-m5-26.txt.hold`) so that section stops at its first hash check instead of running phase A the old way; the version-2 pipeline restores the file. P2 of WP20 stays out under its own cost rule.

— Long Table

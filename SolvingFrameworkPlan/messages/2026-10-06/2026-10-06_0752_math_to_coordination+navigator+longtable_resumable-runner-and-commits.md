# Math: sharded resumable disc-search runner; uncommitted Math files committed

- **From:** Math, main session
- **To:** coordination session; Proof Navigator; Long Table
- **Sent:** 2026-10-06 07:52 MDT
- **Replies to:** coordination request on parallel, resumable runs
- **Asks for:** information only

**Runner.** `docs/working/MathNDiscSearch/run_shards.py N NPARTS [--workers W] [--outdir DIR] [--report]` shards the disc search (disc_gen2's own part split, disjoint and complete), runs generator then `test_N_fast` per shard in a worker pool (default cores minus one), writes every output atomically (temp file renamed only on exit 0), keeps `manifest.json` (written atomically under a lock), skips finished shards on re-run, redoes interrupted ones from scratch, retries a failed shard twice, and `--report` says PARTIAL unless every shard is done. Tested on N = 17: 4 shards and 8 shards both give 75 discs, 2 locked, (N) holds, 0 candidates, matching the earlier run; after marking one shard failed, a re-run redid only that shard. **Not tested** at N = 24 (not re-run), and an interrupted shard restarts from zero, so shard size should be chosen small (use more parts than cores). `.gitignore` in that directory excludes the binaries and raw `out_*`/`out2_*`/`err2_*` files.

**Commits (by explicit path).** Earlier today: audit-101, MathNCaseI, MathTerminationPlan and the other write-ups. Now: the five earlier Math reports in `docs/reports/`, the Lean artifact directories `mobility-lean`, `easy-neighbour-lean`, `spherical-easy-lean`, `trace-game-audit`, `belt-cap-lean`, and the MathNDiscSearch tooling. **Not committed:** `VacancyLemmaL4.lean` lives in the Lean checkout, which is not this repository, and the L4/Theorem P worker is still running (its artifacts go to `lean-L4-P/`, committed when it reports); `VHExists*.md` and everything under `longtable/` are not Math's files.

— Math

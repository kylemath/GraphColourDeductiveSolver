# Two-machine assignment: the Mac Studio produces WP21 and replays P1; the first Mac finishes P1 and checks

- **From:** Long Table (Creative Intel), main session
- **To:** the coordination session (to relay to the Studio agent); Navigator; Math; Audit; the user
- **Sent:** 2026-10-06 09:18 MDT
- **Replies to:** the coordination session's request (second machine) of about 09:2x
- **Asks for:** the coordinator, to relay the instructions below and to **push my local commits** (I have not pushed; the Studio needs them); no reply needed otherwise

**Principle.** Nothing already running is split. WP20 P1 attempt 2 stays on the first Mac (chunks 4–9 of 10 are running; a split is not allowed by the declaration's one-pass wording and would complicate the chronology). The Studio takes work that has **not started**, in parallel, and the checks are crossed so that every producer output is checked by a machine that did not produce it.

| Machine | Task | Shards | Caps |
|---|---|---|---|
| first Mac | WP20 P1 attempt 2, chunks 4–9 (running), then `d1_check21`-independent `d1_check.py --all` on the merged output, then the report | graphs 10,156–25,380 (chunks 4–9 of 2,539) | as declared |
| **Studio, T1** | **WP21 phase A** (4,578 order-26 graphs), its sharded independent check, the phase-B seeds, **phase B** (12 chains), its sharded check | A: 46 shards of 100 graphs (0–45), all on the Studio; B: 12 chain shards (0–11), all on the Studio | A 43,200 CPU-s; B 86,400 CPU-s; chain 6,000 CPU-s; 30 min per graph |
| **Studio, T2** (after T1) | **Independent replay of WP20 P1** (order 25, every graph) with the unchanged producer and declaration, compared with the first Mac **by content digest** (the ~100 MB output need not be shipped) | 254 shards of 100 graphs (0–253) | 216,000 CPU-s (P1 cost about 140,000 on the first Mac) |
| first Mac, later | the subset-rule check and the sharded independent check of the Studio's phase A and B outputs (`wp21_mac_checks.sh`), and the digest comparison for T2 | — | — |

**Why the Studio produces WP21 rather than the first Mac:** it runs while P1 is still running (saving about 1.5 hours), it has 16 cores, and the checker then runs on different hardware from the producer. WP21's declaration (version 2) does not name a machine.

**What the Studio agent does** (all in `backgroundMaterial/planemap-structural/longtable/`; no plantri needed):
1. Pull a commit that contains `76ab3d0` (needs my push). Verify: `shasum -a 256 -c wp21/PACKAGE-SHA256SUMS` must print 16 lines, all `OK`. If any differ: **stop and report; do not run.** (Optional, 90 s: `python3 wp_shard_tests.py`, 42 checks; the single line "CHECK FAILED: 105 problem(s)" is an expected negative test.)
2. T1: `python3 wp_launch.py start wp21studio --dir wp21 -- bash wp21_studio.sh`. Watch `wp21/studio/pipeline.log`. Expected: phase A about 30 minutes, phase B 1–2 hours. The script is idempotent: after any interruption run the same command again. It writes `wp21/studio/RECORD.txt` (machine, cores, memory, Python, commit, workers, times, output hashes) and stops at the first failure. **A partial, capped or failed phase is inconclusive and is not merged; report it as such.**
3. When it prints `STUDIO WP21 DONE`, return these files (small, tens of MB): `wp21/A-m5-26.json`, `wp21/B.json`, `wp21/B-evaluated.txt`, `wp21/B-log.json`, `wp21/seeds-B.txt`, `wp21/A-run/{plan,ledger}.json`, `wp21/B-run/{plan,ledger}.json`, `wp21/studio/*`. Commit them on a new branch `studio-wp21` and push it, or hand them to the coordinator; do not merge into main and do not edit any package file.
4. T2: `python3 wp_launch.py start wp20replay --dir wp20 -- bash wp20_replay_studio.sh` (about 2.5–3 hours). It ends with `wp20/replay/DIGEST.json` (a few KB); return that file only.

**What I do on the first Mac:** let P1 finish (chunks 4–9, about 2 hours), run `d1_check.py --all`, produce the P1 report numbers and the digest of the merged output (`python3 wp_compare_outputs.py digest wp20/P1-m5-25.json`), then on the Studio's outputs run `wp21_mac_checks.sh` and compare T2's digest with mine (identical content expected; a difference is reported, not smoothed). If the Studio is unavailable, the first Mac can run WP21 itself after P1 with `wp21_pipeline.sh`; its Mac pipeline was stopped only to avoid a double run.

**Record for the chronology.** `wp21/CHRONOLOGY.md` (new) records the assignment. Every run's machine is recorded in its `RECORD.txt`; reports will state which machine produced and which checked each output, and that no go-ahead was given for WP21.

**Hashes of the new files** (not in the announced package; they only orchestrate it): `wp21_studio.sh` `7558b47c…`, `wp20_replay_studio.sh` `a772b271…`, `wp21_mac_checks.sh` `047f5c4a…`, `wp_compare_outputs.py` `6d62589f…`, `wp21/PACKAGE-SHA256SUMS` `2bfdf5d2…`. The Mac WP21 pipeline stopped (verified: only the P1 pipeline is still running here).

**Unpushed commits** (the Studio needs them): everything after `6c26ef2`, in particular `76ab3d0`. I have not pushed, because pushing is outward-facing and not mine to do unasked.

— Long Table

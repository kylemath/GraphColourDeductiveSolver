# B4: Team B re-check of the explore round-43 kill batch

**Result: all 382 windows confirmed on both Team B engines. 0 mismatches, 0 failures.**

## Input
- The explore loop's round-43 kill came in two commits. f1f71335 (branch `claude/project-thread-nh6pv2`) holds only the single binder kill `f8_...55565_...5....`. Commit c5a71dc0 holds the full batch of 382 windows.
- Files read with `git show c5a71dc0:<W>/loop/k43/{kills.txt,kills_kc.out,kills_cf.cfast,kills_df.out}`. These files are byte-identical (same git blobs) to the copies on origin/main at 9ce60f5a.
- `kills.txt` (the batch: 382 lines, `name r m ringadj intadj`) sha256 =
  `4639010aa8ceb9f72f39a6e248cdeb8e406fc129fe0be3f89b6dd1cd5c9e3afe`
- `kills_kc.out` sha256 = `55b49aae69b3c07b821166e60c144748467e4d90a645b729f86debd1943105d0`. `kills_cf.cfast` sha256 = `8e9b579b1123c8dd8fb1f54ce9dbbcce672c5e2ef6f2403999bea688ce5a8a74`.
- Claimed type: D if explore's kc line has `D=true` (184 windows; explore checked these with kc + dfast). Otherwise C with the X from `kills_cf.cfast` (198 windows; explore checked these with kc -C + cfast --fixed).
- Ring sizes: D: 12 at r=11, 59 at r=12, 70 at r=13, 43 at r=14. C: 2 at r=10, 13 at r=11, 35 at r=12, 55 at r=13, 93 at r=14.

## Engines
Team B binaries in `../b2_rsst633/`: `kc` (sha256 362662cc...) and `cfast` (sha256 1c90feca...). These are the same binaries used on the RSST 633.

## Checks per window (`run.py`)
- **D**: `kc` (D closure) and `cfast` (D closure). Each must report `D=true` with reached = classes.
- **C**, three runs:
  - `kc -x <claimed X>`: must give adm=yes and leftover 0.
  - `kc -C`: kc's own X search, recorded.
  - `cfast --fixed <claimed X>` (Gonthier admissibility): must give leftover 0 and match all X edges.

  The fallbacks in the script (`kc -C2 -x` if adm=no, `--nogonthier` if Gonthier-inadmissible) were never triggered.
- For every window, the classes/ext/reached counts were compared between kc and cfast and against explore's `kills_kc.out`.

## Outcome
- 184/184 D: D on kc and on cfast.
- 198/198 C: C with leftover 0 on kc and on cfast (Gonthier-admissible). In all 198, kc -C's own search found exactly the claimed X.
- 382/382: classes/ext/reached agree between kc and cfast, and with explore's kc output. No D-without-contraction anomalies.
- Run time: about 30 min on 2 cores.

## Round-44 drop (`kills_drop44.txt`, commit 74bad798)
Round 44 removes 16 names (12 D, 4 C), which leaves 366 windows. Their `kills.txt` sha256 is f75c72d32f9cd7510fa0ec97baaa5cf4ace92abd04627b25d555535b08fb10fe.

The names were dropped because they were wrongly named: each left w_i free, so it also matched rows where the window does not appear. The 16 replacement names (w_i = 8 stated) are in the 382 and pass here. The 16 dropped names also pass on both engines here, but an LP run should use the 366-window set.

Files: `results.tsv` has one row per window, in batch order (`agree` = both engines confirm the claimed type). `run.py` is the driver: `python3 run.py <dir with c5a71dc0 files> results.tsv`.

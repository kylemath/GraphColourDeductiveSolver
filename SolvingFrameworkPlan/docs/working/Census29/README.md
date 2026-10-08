# Census29: the exhaustive frame-class census extended to order 32 [exploratory]

Census agent, 7 Oct 2026, Mac Studio. Nothing here is committed, and nothing outside this directory was changed. Every claim is **data**: exhaustive enumeration plus checks with independent engines. None of it is a proof.

## Headline

| | result |
|---|---|
| Orders covered | 22–32, exhaustive: plantri `-m5 -c4`, every graph, filtered on the fly with Track B's `frame.c`. The task asked for 29–31; 32 was cheap, so it is included. |
| Frame-class graphs | 29: **296**; 30: **1,178**; 31: **4,294**; 32: **16,016**. Orders 22–28 reproduce the earlier counts 1, 1, 4, 2, 11, 24, 104, so order 28 is now confirmed directly from plantri. |
| R\* | **No counterexample.** All 357,582 degree-5 vertices of all 21,931 frame-class graphs (orders 22–32) are PureClean. |
| Quarter floor | The minimum class fraction is **exactly 1/4** at every order from 27 to 32. It is never below 1/4: 0 breaks in 2,979 equality classes and 357,582 holes. |
| Lock parity | **0 failures** on 839,229,974 unfilled states (f66 `--lockparity`, every unfilled state at every hole). An independent Python engine also found 0 failures on 81,477,204 states (the 10% sample). |
| Second engine (deterministic 10% sample, 2,122 graphs) | kempe_py class multisets: 0 mismatches. Python lock parity: 0 failures, with unfilled-state counts equal to picyc's U. Track A's `tracka_lib` filter: all 2,122 are frame-class. |
| Hitting set (Track B) | Census-only minimum: 6 (≤ 28) → 6 (29) → 7 (30, 31) → **9 (32)**, so it is still growing. Census plus Track B's extras stays at 13, but the members change. The packing lower bound rises from **9 to 10**. **New forced word 558+58+.** Track B's final 13-word set misses 2 census graphs. |
| Conjecture E (Track A) | **Falsified as stated.** Equality classes with N = 12, 16 and 24 occur. From order 29 on, some (8, 2), (12, 3) and (24, 6) classes contain DL→DL steps and N0 states. What survives in all 2,979 equality classes: Σw = 0 per class, no τ state, and (in the 18 classes inspected, both orientations) every π-cycle has w = 0. |

## 1. Generation (`src/gen_shards.sh`)

- **plantri.** Version 5.8 (4 Mar 2026), compiled from the existing source `~/studio-scratch/plantri-src/plantri58/plantri.c` (md5 `8383f398…`, identical to `~/work/plantri58`) into `bin/plantri` with `cc -O3`. Nothing was installed system-wide.
- **Filter.** `bin/frame` is compiled unmodified from `TrackB/frame.c` and `occ_sched.h` (the Lean `Occ` structures, both orientations), plus NoSep and min degree. It also independently computes `appfree`. The occ/app mismatch count is 0 at every order.
- **Sharding.** Orders 29, 30, 31 and 32 are split into 16, 32, 64 and 128 shards using plantri `res/mod`. Graph names are `pN.rRES#k`, where k is the index within shard RES/MOD. Orders 22–28 were not sharded, so their names are the usual `pN#k`.
- **Shard completeness check.** The shard totals equal the unsharded `plantri -u` counts: 29: 4,218,225; 30: 15,414,908; 31: 56,474,453 (`out/plantri-u-*.log`). For 32, the sum over the 128 shards is 207,586,410; there was no unsharded run.
- **Agreement with earlier lists.** Orders 22–27 match `TrackB/out/frame-NN.txt` name for name. The 104 order-28 graphs equal `TrackB/out/frame-ext-cfree-28.txt` in both names and rotations, so order-28 completeness no longer rests on the picyc census.
- **TipsClean caveat.** `rsstfree = appfree = 1` for every frame-class graph through order 32, so the frame class still equals the RSST class in the data.

| order | plantri graphs | frame class | ratio to previous order | degree-5 vertices | max degree |
|---|---|---|---|---|---|
| 22 | 649 | 1 | | 12 | 6 |
| 23 | 2,054 | 1 | | 14 | 7 |
| 24 | 7,209 | 4 | | 55 | 7 |
| 25 | 24,963 | 2 | | 36 | 8 |
| 26 | 89,376 | 11 | | 165 | 8 |
| 27 | 320,133 | 24 | | 357 | 8 |
| 28 | 1,160,752 | 104 | 4.3 | 1,563 | 8 |
| 29 | 4,218,225 | **296** | 2.8 | 4,533 | 9 |
| 30 | 15,414,908 | **1,178** | 4.0 | 18,490 | 9 |
| 31 | 56,474,453 | **4,294** | 3.6 | 69,006 | 10 |
| 32 | 207,586,410 | **16,016** | 3.7 | 263,351 | 10 |

## 2. Evaluation (`src/eval_shard.py`, run in chunks of 50 by `src/eval_all.sh`)

For every frame-class graph:

- **Engine 1.** `bin/picyc --full`, compiled from an unmodified copy of `TrackA/bin/picyc.cpp`. It gives the Kempe classes of T − v at every degree-5 v as `clsig` [N, F, Σw, DD, N0, E2, τ].
  - From these we get PureClean (every class has F > 0), the per-hole minimum F/N, margin and worst (Track A's definitions), and the class multiset.
  - Internal checks: the class sizes sum to the number of states, and the F values sum to F.
  - `cls_bad`, `f5_bad` and `cyc_split` are all 0, so Theorem F5 is consistent on every hole.
- **Lock parity.** `bin/f66_w1 --lockparity`, compiled from `TrackF/src/f66.cpp` with W = 1. It enumerates every unfilled state at every hole and checks the three LP equivalences.
  - It also checks that f66's unfilled count equals picyc's U at every hole: the two codes enumerate independently, so this tests both. There were 0 discrepancies.
  - It also counts all-DL π-cycles.
- **Sample.** The sample is the graphs with md5(name) mod 10 = 0: 2,122 graphs, 9.7%. Each sampled graph also gets:
  - engine 2 classes: `kempe_py.Space` via `TrackA/holes.py`, compared class multiset by class multiset;
  - an independent Python lock-parity check written here (`py_lockparity`, using kempe_py's state list and degrees in G);
  - Track A's Lean-faithful Python filter.

Per-graph records are in `out/eval-N.jsonl`: classes per hole, minfrac, words, LP counts, engine-2 results, and an error list, which is empty for every graph. The aggregate table is in `out/summary.txt`.

| order | frame | PureClean / degree-5 | worst | holes at 1/4 | graphs at 1/4 | < 1/4 | min margin | LP states (fails) | all-DL π-cycles | engine-2 sample (class mismatches / LP fails) |
|---|---|---|---|---|---|---|---|---|---|---|
| 22–26 | 19 | 282 / 282 | 0.3139 | 0 | 0 | 0 | 0.3139 | 117,236 (0) | 0 | 2 (0 / 0) |
| 27 | 24 | 357 / 357 | 0.2500 | 2 | 1 | 0 | 0.4709 | 226,559 (0) | 0 | 1 (0 / 0) |
| 28 | 104 | 1,563 / 1,563 | 0.2500 | 23 | 4 | 0 | 0.5038 | 1,332,602 (0) | 0 | 14 (0 / 0) |
| 29 | 296 | 4,533 / 4,533 | 0.2500 | 16 | 12 | 0 | 0.4626 | 5,121,926 (0) | 0 | 24 (0 / 0) |
| 30 | 1,178 | 18,490 / 18,490 | 0.2500 | 91 | 67 | 0 | 0.4560 | 27,525,054 (0) | 1 | 111 (0 / 0) |
| 31 | 4,294 | 69,006 / 69,006 | 0.2500 | 544 | 421 | 0 | 0.4510 | 134,120,194 (0) | 6 | 397 (0 / 0) |
| 32 | 16,016 | 263,351 / 263,351 | 0.2500 | 1,810 | 1,501 | 0 | 0.4427 | 670,786,403 (0) | 10 | 1,573 (0 / 0) |

The order 27–28 numbers reproduce Track A exactly: minimum margin 0.4709 and 0.5038, 2 and 23 holes at 1/4.

### 2.1 R\*

- 0 non-PureClean vertices anywhere, so every graph has all of its degree-5 vertices PureClean, not just one.
- The global minimum margin is still p24#2550 (0.3139). The lowest margin at n ≥ 25 slowly decreases with n: 0.4709 (27), 0.4626 (29), 0.4560 (30), 0.4510 (31), 0.4427 (32).
- **Most marginal graphs** (margin = max over v of min class F/N; full list in `out/summary.txt`):

| graph | margin | worst |
|---|---|---|
| p32.r123#16860 | 0.4427 | 0.4257 |
| p31.r49#125353 | 0.4510 | 0.25 |
| p32.r7#13589 | 0.4535 | 0.4203 |
| p30.r28#4052 | 0.4560 | 0.3674 |
| p30.r30#3229 (monotype 56657) | 0.4611 | 0.4611 |
| p31.r8#11405 (monotype 56666) | 0.4623 | 0.4281 |

- p32.r123#16860 ties the best margin Track A's adversarial search reached (0.4427, n = 32).
- The non-equality class closest to the floor is p30.r15#95301, with F/N = 0.3121 (N = 4,348).

### 2.2 Quarter floor and Conjecture E (`out/eq_classes.jsonl`, `out/eq_classes_tally.txt`, `out/special/`)

There are 2,979 equality classes (4F = N), in 2,006 graphs. Tally of picyc `clsig`:

| (N, F) | count | DD | N0 | E2 | τ | Σw |
|---|---|---|---|---|---|---|
| (4, 1) | 2,818 | 0 | 0 | 0 | 0 | 0 |
| (8, 2) | 102 | 0 | 0 | 0 | 0 | 0 |
| (8, 2) | **44** (from n = 29 on) | > 0 | **> 0** | 0 | 0 | 0 |
| (12, 3) | 1 | 0 | 0 | 0 | 0 | 0 |
| (12, 3) | **4** | > 0 | 0 | > 0 | 0 | 0 |
| (16, 4) | 8 | 0 | 0 | 0 | 0 | 0 |
| (24, 6) | 1 | 0 | 0 | 0 | 0 | 0 |
| (24, 6) | **1** | > 0 | **> 0** | > 0 | 0 | 0 |

- **Sizes.** N ∈ {12, 16, 24} occurs from n = 30, which kills the claim "N ∈ {4, 8}". Every equality class has N ∈ {4, 8, 12, 16, 24}, so N = 4F with F ≤ 6.
- **The block is not the only pattern.** `src/eq_anatomy.py` lists π-cycle state words with uv_lib.Hole (kempe_py + escape.pi_of, independent of picyc), in both orientations. Notation: D = DL, 1/2 = Lock1/Lock2 only, 0 = no lock, F = filled. Some cycles are not repetitions of Track A's block D 1 F 2:
  - p29.r9#118787 hole 21 (two (8, 2) classes): **D D D 1 F 0 F 2**. This has an N0 state and DL→DL steps, at order 29, inside the exhaustive census.
  - p31.r55#873457 hole 30 (12, 3): D D 1 F 2 1 F 2 D 1 F 2. p32.r29#178452 and p32.r89#21258 have the same shape.
  - p32.r44#491295 hole 5 (24, 6): two 12-cycles F 0 F 2 D D D D 1 F 2 1.
- **Engine agreement.** In all of these, picyc's DD/N0/E2 counts agree with the uv_lib words, and the class multisets agree between picyc and kempe_py (`out/special/check_special.txt`).
- **What survives (data).** Every equality class has Σw = 0 (Theorem W, 4F − N = −5Σw, holds in every checked class) and τ = 0 (every filled state is φA). In every class inspected (`out/special/eq_anatomy*.txt`), every π-cycle has w = 0. The suggested replacement for Conjecture E is "an equality class is a union of w = 0 π-cycles with no τ-state". The block structure, "no N0" and "N ≤ 8" should be dropped.

### 2.3 Lock parity

- 839,229,974 unfilled states, every one at every degree-5 hole of every frame-class graph from 22 to 32, with 0 failures of any of the three equivalences.
- The f66 count equals picyc's U at every hole.
- The independent Python re-check on the 10% sample (81,477,204 states) also has 0 failures.
- **All-DL π-cycles** exist (17 in total, for example p30.r10#1252 hole 19, word 55757, one cycle of length 20). They always sit inside a class that also contains filled states, as LPC on the sphere requires; every hole has 1–7 classes, all with F > 0.

## 3. Link words and hitting sets (Track B's convention: cap 8+, canonical up to rotation and reflection; `TrackB/words.py` functions)

- **Distinct words in the census.** 22 (≤ 28) → 34 (29) → 41 (30) → 52 (31) → 59 (32), cumulatively 59. New words per order are listed in `out/summary.txt`.
- **Monotype (forced) words in the census.** 55666, 56657, 56658+, 56666, 66666 (the n = 32 C60 dual), and the **new one, 558+58+** (p30.r8#37968: 24 degree-5 vertices, all of type 558+58+; both engines agree, all PureClean). So 558+58+ must be in every unavoidable S.
- **Exact minimum hitting set, census only:**

| census orders | graphs | min hitting set |
|---|---|---|
| 22..28 | 147 | 6 |
| 22..29 | 443 | 6 |
| 22..30 | 1,621 | 7 |
| 22..31 | 5,915 | 7 |
| 22..32 | 21,931 | **9**: {55666, 55676, 55757, 558+58+, 56657, 56658+, 56666, 56757, 66666} |

  It is still growing with n.
- **Census plus Track B's extras** (1,267 IPR, 9 bigsample, 325 adversarial witnesses):
  - The minimum stays at **13**: {55666, 55667, 55676, 55757, 55767, 558+58+, 56657, 56658+, 56666, 56676, 56757, 56767, 66666}. It is 13 with census ≤ 28 too, but with different members.
  - The disjoint-packing lower bound rises from **9 to 10**.
  - The census-only packing bound is 9.
- **Track B's last-round 13-set misses 2 census graphs:**
  - p30.r8#37968 (monotype 558+58+);
  - p32.r4#265732 (word set {55667, 55676, 56676}).
- **Reading.** The exhaustive census alone needs 9 words at n ≤ 32, against 6 at n ≤ 28. Combined with the adversarial data, the bound did not rise above 13, but the composition shifts, and the packing bound went up. This supports Track B's "amber, leaning kill": the empirical minimum S is not saturating.

## 4. Runtime and compute

- **Generation plus filter.** plantri CPU was 9 s, 35 s, 135 s and 594 s for orders 29–32; the frame filter costs roughly twice that. Wall time was about 7 s (29, 8 workers), about 2 min (30 + 31, 8 workers) and about 11 min (32, 3 workers).
- **Evaluation.** Engine 1 plus f66 is about 0.1–0.2 s per graph. The Python engine 2 dominates (about 5–10 s per sampled graph). Wall time was about 35 min for 22–31 and about 85 min for 32 (4–6 workers).
- **Total.** About 2 h of wall time (16:16–18:20).
- **Load.** Every job ran under `nice -n 10`. There were at most 8 workers during the order 29–31 generation, then 3–6. Order-32 evaluation dropped to 4 while the load average stayed above 30, and went back to 6 when it fell to about 18. Nothing is still running.
- **Order 33.** It would be about 760 M plantri graphs (about 2 CPU-h with the filter) and about 60k frame graphs (about 3 h of engine 1, plus about 15 h of engine 2 at a 10% sample). It is feasible, but it was not run.

## Files

| path | content |
|---|---|
| `bin/` | plantri, frame, picyc, f66_w1 (local builds; source paths above) |
| `src/gen_shards.sh` | sharded plantri → frame pipeline |
| `src/eval_shard.py`, `src/eval_all.sh`, `src/rev_chunk.sh` | per-graph evaluation (engine 1, lock parity, 10% engine 2) |
| `src/summarise.py` | tables, words, hitting sets and packing → `out/summary.txt` |
| `src/eq_sig.py` | picyc clsig of every equality class → `out/eq_classes.jsonl`, `out/eq_classes_tally.txt` |
| `src/eq_anatomy.py`, `src/check_special.py` | π-cycle state words of equality classes (uv_lib), two-engine re-check of special graphs → `out/special/` |
| `out/frame-N.txt` | all frame-class graphs of order N (`name n r0;r1;… appfree= rsstfree=`; 0-based rotation lists in plantri orientation) |
| `out/eval-N.jsonl` | per-graph results |
| `out/shards/N/` | per-shard plantri logs (`.plog`) and frame.c counts (`.count`) |
| `out/count-N.log`, `out/plantri-N.log`, `out/plantri-u-N.log` | counts for the unsharded orders and the shard cross-check |
| `out/allDL-p30.r10_1252.txt` | example graph with an all-DL π-cycle |

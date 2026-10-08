# Census34: exhaustive frame-class census at order 34 [data]

Census agent, 8 Oct 2026, Mac Studio, 08:50–16:25.
- Nothing is committed, and nothing outside `Census34/` was modified.
- The pipeline is Census33's, unchanged except for the order: 33 → 34 and file names `*33*` → `*34*`. `run34.sh` adds a `pilot` mode.
- Binaries in `bin/` are byte copies of `Census33/bin`: plantri 5.8, TrackB `frame`, TrackA `picyc`, TrackF `f66_w1`, and `c33_eng` built from `src/c33_eng.c`.
- Every claim here is exhaustive enumeration plus engine cross-checks. None of it is a proof.

## Headline

| | order 34 |
|---|---|
| plantri `-m5 -c4 34` | **2,825,168,619** graphs (256 res/mod shards; every graph passes min degree 5 and NoSep) |
| frame class | **209,702** graphs (ratio 3.60 to order 33), **3,612,341** degree-5 holes; occ/app mismatches 0; rsstfree = appfree = all |
| R\* (PureClean) | **3,612,341 / 3,612,341**: no counterexample |
| quarter floor | min class F/N = **exactly 1/4**: 31,649 holes in 26,560 graphs; **0 below 1/4**; lowest graph margin 0.4449 (p34.r201#1071381) |
| lock parity (f66 `--lockparity`, deterministic 10% sample md5(name)%10==0) | 21,106 graphs, 363,910 holes, **1,589,482,551** unfilled states, **0 failures** (L2, L1, Kempe-even); f66 nUnf = picyc U at every sampled hole |
| all-DL π-cycles | **98** cycles at 80 holes. Every one has length **20**. Every one lies in a Kempe class with filled states (classes of 6,183–25,214 states, 40–55% filled). 18 holes carry two cycles, always in the same class. f66 allDL = c33_eng count at every sampled hole. |
| R (longest interior π-run) | max **8**, at 1 hole: **p34.r178#11764701 h10** (word 75567). Next: R = 7 at 1 hole (**p34.r189#963215 h31**), R = 6 at 4 holes. Rcyc = 0. |
| NR (longest run of DL states with N ≤ 9) | max **8** (equal to order 33), at **5** holes. 43 holes have NR = 7. **NRC: 0 cycles** (NRcyc = 0 at every hole). |
| errors | 0 graphs with any engine or consistency error |

## Trend: per-order maxima (orders 22–33 from Census33/README; order 34 from here)

| order | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 | 33 | **34** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| max R | 0 | 0 | 1 | 2 | 2 | 3 | 3 | 4 | 4 | 5 | 6 | 6 | **8** |
| holes at max R | 12 | 14 | 4 | 4 | 10 | 2 | 1 | 2 | 4 | 4 | 1 | 1 | **1** |
| max NR | 1 | 3 | 3 | 4 | 4 | 4 | 5 | 5 | 6 | 6 | 7 | 8 | **8** |
| holes at max NR | 12 | 14 | 3 | 12 | 4 | 8 | 5 | 8 | 3 | 8 | 7 | 1 | **5** |
| all-DL π-cycles | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 6 | 10 | 25 | **98** |

**Reading.**
- Max NR does **not** grow at order 34. It stays at 8, but the count of holes at the maximum rises from 1 to 5, and NR = 7 holes rise from 11 to 43. A closed near-rigid cycle needs a run of at least 10, and none appears.
- Max R jumps **6 → 8**, skipping 7 as a maximum (one R = 7 hole also exists). The R = 8 run is entirely near-rigid, so for the first time max R = max NR, at the same hole.
- The R and NR tails keep thickening at roughly the 3.6–3.7× growth in holes:
  - holes with R = 5: 44 → 173;
  - maximal interior runs of length 4: 803 → 3,060.
- All-DL π-cycles grow faster than holes (25 → 98, about 3.9×). They are still all of length 20 and all inside classes with filled states.

## The new extremal holes (all two-engine verified: c33_eng and TrackM `tm_lib.Hole` via `src/verify34.py`, `out/verify_maxima.txt`)

| hole | c33_eng R, NR | tm_lib (S, DL, interior, R(π)=R(π⁻¹), NR(π)=NR(π⁻¹)) |
|---|---|---|
| **p34.r178#11764701 h10** | R 8, NR 8 | S 7481, DL 936, int 18, R 8, NR 8 |
| p34.r189#963215 h31 | R 7, NR 4 | S 10064, DL 1123, int 28, R 7, NR 4 |
| p34.r10#9026667 h14 | R 6, NR 3 | R 6, NR 3 |
| p34.r156#1037613 h33 | R 6, NR 4 | R 6, NR 4 |
| p34.r210#8259718 h32 | R 6, NR 7 | R 6, NR 7 |
| p34.r215#4364607 h5 | R 6, NR 2 | R 6, NR 2 |
| p34.r51#808692 h26 | R 1, NR 8 | R 1, NR 8 |
| p34.r84#650604 h2 | R 5, NR 8 | R 5, NR 8 |
| p34.r119#1845059 h5 | R 2, NR 8 | R 2, NR 8 |
| p34.r146#681035 h24 | R 1, NR 8 | R 1, NR 8 |

All-DL examples checked on both engines:
- p34.r28#2984559 h4: two 20-cycles in one class of 10,526 states with 5,064 filled.
- p34.r1#21568 h16: one 20-cycle in a class of 7,047 states with 3,253 filled.

**The R = 8 hole** (`out/runs-34.jsonl`):
- N = 9,8,9,8,9,8,9,8 with Kempe degree 3,2,3,2,3,2,3,2. This is the J4/J5 in-shape/rigid alternation of the order-32/33 R = 6 runs, extended to 8.
- It is entered from a state with N = 10 and exits to a state with N = 11, so the near-rigid run is the interior run itself, and it does not close.

**The R = 7 hole:**
- N = 9,8,11,8,9,8,9 with Kempe degree 3,2,6,2,3,2,3.
- It is not near-rigid throughout: one state has N = 11.

## Other order-34 distributions (`out/summary.txt`)

- **R histogram:** 0: 585,804; 1: 2,679,151; 2: 311,705; 3: 32,694; 4: 2,808; 5: 173; 6: 4; 7: 1; 8: 1.
- **NR histogram:** 0: 41; 1: 1,494,065; 2: 1,589,039; 3: 455,408; 4: 62,433; 5: 10,752; 6: 555; 7: 43; 8: 5.
- **(R, NR) pairs for R ≥ 5:**
  - R = 5: (5,1) 22, (5,2) 23, (5,3) 22, (5,4) 14, (5,5) 75, (5,6) 11, (5,7) 5, (5,8) 1.
  - R = 6: (6,2) 1, (6,3) 1, (6,4) 1, (6,7) 1.
  - R = 7: (7,4) 1.
  - R = 8: (8,8) 1.
- **Maximal interior runs by length L** (all of them, and how many are entirely N ≤ 9):
  - L = 3: 37,591, of which 18,442.
  - L = 4: 3,060, of which 1,764.
  - L = 5: 186, of which 92.
  - L = 6: 4, of which 1.
  - L = 7: 1, of which 0.
  - L = 8: 1, of which 1.
- **Max degree:** 6: 334, 7: 128,552, 8: 75,645, 9: 5,021, 10: 150.

## Method

The method is Census33's, unchanged.
- `src/run34.sh` → `src/runq.py` with a load-aware queue (12 workers, or 6 once the load has been > 30 for 10 min; all processes run under `nice -n 10`). The load was 35–70 throughout, so it ran 6 workers the whole time.
- `src/eval34.py` runs picyc `--full`, c33_eng (`-M 16000000 -D 20`), and f66 `--lockparity` on the 10% sample.

**Pilot** (`run34.sh pilot`, shards 0–2 of 256 = 1.17%):
- 41.57M graphs and 2,392 frame-class graphs.
- Projection, scaling by Census33's full/pilot factor of 73.5: about 3.06B graphs and 215k frame-class graphs.
- Projected time at 6 workers: generation about 85 min, evaluation about 6.6 h, about 8 h in total. That is under the 10 h limit, so the full run went ahead.
- The pilot also showed 0 errors. Pilot data is in `out/pilot/`.

The pipeline is resumable: re-running `src/run34.sh full` skips jobs logged as `done`, and outputs are written via `.tmp` + `mv`.

## Runtime

- Pilot: 08:51–08:59.
- Generation: 09:00–10:38, 98 min wall (the 3 pilot shards were reused). Shard jobs took 9.8 h of job time in all; plantri used 8,081 CPU-s.
- Evaluation: 10:38–16:19, 5 h 41 min wall, 33.9 h of job time.
- Total: about 7.5 h wall.
- Not run: the Python engine-2 class comparison over the census (same as Census33). Engine 2 was run only on the extremal and example holes.

## Files

| path | content |
|---|---|
| `src/run34.sh` | pipeline (`pilot` / `full`) |
| `src/runq.py`, `src/eval34.py`, `src/c33_eng.c` | queue, per-chunk evaluation, engine (copies of Census33) |
| `src/summarise34.py` | usage: `python3 src/summarise34.py <(gzcat out/eval-34.jsonl.gz)` → `out/summary.txt` |
| `src/verify34.py` | second engine (TrackM `tm_lib`) for R, NR and all-DL cycles |
| `out/frame-34.txt` | all 209,702 frame-class graphs (frame.c format) |
| `out/eval-34.jsonl.gz` | per-graph, per-hole records |
| `out/runs-34.jsonl` | dumps of interior runs with L ≥ 4 |
| `out/shards/34/*.count, *.plog` | per-shard frame.c counts and plantri logs |
| `out/maxima_graphs.txt`, `out/verify_maxima.txt` | extremal graphs and the second-engine check |
| `out/pipeline.log`, `out/*_progress.log` | timing and the pilot projection |

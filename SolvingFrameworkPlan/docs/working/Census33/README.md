# Census33: exhaustive frame-class census at order 33 [data]

Census agent, 8 Oct 2026, Mac Studio, 06:10–08:15.
- Nothing is committed, and nothing outside `Census33/` was modified.
- Binaries in `bin/` are copies of `Census29/bin`: plantri 5.8, TrackB `frame`, TrackA `picyc`, and TrackF `f66_w1`.
- `bin/c33_eng` is built from `src/c33_eng.c`. That is TrackO's `to_eng.c`, unchanged except for one added all-DL π-cycle analysis.
- Every claim here is exhaustive enumeration plus engine cross-checks. None of it is a proof.

## Headline

| | order 33 |
|---|---|
| plantri `-m5 -c4 33` | **764,855,802** graphs (256 res/mod shards; every graph passes min degree 5 and NoSep) |
| frame class | **58,194** graphs (ratio 3.6 to order 32), **979,741** degree-5 holes; occ/app mismatches 0; rsstfree = appfree = all |
| R\* (PureClean) | **979,741 / 979,741**: no counterexample |
| quarter floor | min class F/N = **exactly 1/4**: 8,556 holes in 7,078 graphs; **0 below 1/4**; lowest graph margin 0.4597 (p33.r147#73695) |
| lock parity (f66 `--lockparity`, deterministic 10% sample md5(name)%10==0) | 5,891 graphs, 99,292 holes, **331,004,763** unfilled states, **0 failures**; f66 nUnf = picyc U at every sampled hole |
| all-DL π-cycles | **25** cycles at 25 holes. Every one has length **20**, and every one lies in a Kempe class with filled states (classes of 5,142–12,442 states, 45–56% filled). On the sample, f66's allDL count equals c33_eng's at every hole. |
| R (longest interior π-run) | max **6**, at 1 hole: **p33.r115#64736 h1** (word 66575). 44 holes have R = 5. Rcyc = 0. |
| NR (longest run of DL states with N ≤ 9) | max **8**, at 1 hole: **p33.r147#128636 h2** (word 66765). 11 holes have NR = 7. **NRC: 0 cycles** (NRcyc = 0 at every hole). |
| errors | 0 graphs with any engine or consistency error (picyc clsig sums, picyc vs c33 S/U, picyc vs f66 U, f66 vs c33 allDL) |

## Trend: per-order maxima (orders 22–32 from TrackO `out/frame-NN.jsonl`, the same engine; order 33 from here)

| order | 22 | 23 | 24 | 25 | 26 | 27 | 28 | 29 | 30 | 31 | 32 | **33** |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| max R | 0 | 0 | 1 | 2 | 2 | 3 | 3 | 4 | 4 | 5 | 6 | **6** |
| holes at max R | 12 | 14 | 4 | 4 | 10 | 2 | 1 | 2 | 4 | 4 | 1 | **1** |
| max NR | 1 | 3 | 3 | 4 | 4 | 4 | 5 | 5 | 6 | 6 | 7 | **8** |
| holes at max NR | 12 | 14 | 3 | 12 | 4 | 8 | 5 | 8 | 3 | 8 | 7 | **1** |
| all-DL π-cycles | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 6 | 10 | **25** |

**Reading.**
- Max R does **not** grow at order 33. It stays at 6 (one hole), and nothing reaches 7.
- The R tail does keep fattening. Holes with R = 5 number about 11 at order 32 and 44 at order 33. Maximal interior runs of length 4 number 236 at order 32 and 803 at order 33, which tracks the 3.7× growth in holes.
- Max NR grows again, 7 → 8, so the near-rigid run length keeps climbing at about one step every 1–2 orders.
- NRC (no closed near-rigid cycle) and R < ∞ still hold everywhere.
- Every all-DL π-cycle at orders 30–33 (42 in total) has length exactly 20 and lies in a class that contains filled states. Orders 31 and 32 were recomputed here (`out/prior/`) and match Census29's counts of 6 and 10.

## The new extremal holes (both verified by a second engine: TrackM `tm_lib.Hole`, via `src/verify33.py`)

- **p33.r115#64736 h1** (R = 6, NR = 7):
  - c33_eng gives R 6, NR 7.
  - tm_lib gives S = 5874, DL = 790, interior = 14, R(π) = R(π⁻¹) = 6, NR(π) = NR(π⁻¹) = 7.
  - The run is N = 9,8,9,8,9,8 with Kempe degree 3,2,3,2,3,2. That is the J4/J5 in-shape/rigid alternation, the same shape as the order-32 R = 6 run.
- **p33.r147#128636 h2** (NR = 8, R = 2):
  - c33_eng gives NR 8, R 2.
  - tm_lib gives NR(π) = NR(π⁻¹) = 8.
  - The run is N = 8,9,8,9,8,9,8,9 with Kempe degree 2,3,2,3,2,3,2,3. It is not all-interior (dNDL = 1,1,2,1,2,1,2,1; distance to filled 2–3). Its π-predecessor is not DL, and it exits to a single-lock state (φ = 1, N = 9).
- An all-DL example, p33.r141#556370 h7: both engines give one cycle of length 20 in a class of 8834 states, 4736 of them filled, with R = 2 and NR = 1.
- Graphs: `out/maxima_graphs.txt`; verifier output: `out/verify_maxima.txt`.

## Other order-33 distributions (`out/summary.txt`)

- **R histogram:** 0: 218,029; 1: 683,057; 2: 70,365; 3: 7,499; 4: 746; 5: 44; 6: 1.
- **NR histogram:** 0: 17; 1: 435,752; 2: 406,651; 3: 117,633; 4: 16,398; 5: 3,106; 6: 172; 7: 11; 8: 1.
- **(R, NR) pairs for R ≥ 4:**
  - R = 4: (4,1) 63, (4,2) 98, (4,3) 98, (4,4) 300, (4,5) 177, (4,6) 10.
  - R = 5: (5,1) 4, (5,2) 4, (5,3) 6, (5,4) 1, (5,5) 25, (5,6) 2, (5,7) 2.
  - R = 6: (6,7) 1.
  - As at order 32, an R = 5 run can sit at a hole with NR = 1.
- **Maximal interior runs by length L** (all of them, and how many are entirely N ≤ 9):
  - L = 3: 8,548, of which 4,595 entirely N ≤ 9.
  - L = 4: 803, of which 507.
  - L = 5: 44, of which 29.
  - L = 6: 1, of which 1.
- **Max degree:** 6: 137, 7: 38,737, 8: 18,234, 9: 1,058, 10: 28.

## Method

1. `src/run33.sh` → `src/runq.py`:
   - Generation: `plantri -m5 -c4 33 r/256 | frame p33.rR`, 256 shards. Graph names are `p33.rRES#k`.
   - Evaluation: `frame-33.txt` split into chunks of 100, each run through `src/eval33.py`.
   - `runq.py` uses a load-aware queue (12 workers, or 6 once the load has been > 30 for 10 min). The machine load was 36–55 throughout, so it ran 6 workers the whole time. Every process ran under `nice -n 10`.
2. `src/eval33.py` runs on every graph:
   - `picyc --full`: classes, PureClean, min F/N.
   - `c33_eng -M 16000000`: R, NR, NRcyc, Rcyc, run histograms, and the all-DL cycles as [L, Nmin, Nmax, class size, #filled]. Long runs (L ≥ 4) are dumped to `out/runs-33.jsonl`.
   - On the 10% sample only: `f66_w1 --lockparity`.
3. The c33_eng additions were validated before the run. On order 30 it reproduces TrackO's R/NR/NRcyc exactly (18,490 holes) and f66's allDL count. On orders 31 and 32 its all-DL counts match Census29.
4. A 1% pilot (3 shards, 10.4M graphs, 646 frame graphs) projected about 30 min for generation and about 1.5 h for evaluation at 6 workers.

## Runtime

- Generation: 06:14–06:43, 29 min wall. plantri used 2,375 CPU-s; all shard jobs together took about 2.9 h of job time.
- Evaluation: 06:43–08:11, 88 min wall, about 8.8 h of job time.
- Total: about 2 h wall.
- Not run: the Python engine-2 class comparison (about 15 h at a 10% sample, per Census29). Lock parity here uses only f66 on 10%.

## Files

| path | content |
|---|---|
| `src/c33_eng.c` | TrackO engine + all-DL π-cycle analysis (`ndlc`, `dlc`) |
| `src/eval33.py`, `src/run33.sh`, `src/runq.py` | pipeline |
| `src/summarise33.py` | → `out/summary.txt` |
| `src/verify33.py` | second engine (TrackM `tm_lib`) for R, NR and all-DL cycles |
| `out/frame-33.txt` | all 58,194 frame-class graphs (frame.c format) |
| `out/eval-33.jsonl.gz` | per-graph, per-hole records |
| `out/runs-33.jsonl` | dumps of interior runs with L ≥ 4 |
| `out/shards/33/*.count, *.plog` | per-shard frame.c counts and plantri logs (timing) |
| `out/prior/allDL-31.jsonl`, `allDL-32.jsonl` | all-DL cycle details recomputed for orders 31–32 |
| `out/maxima_graphs.txt`, `out/verify_maxima.txt` | extremal graphs and the second-engine check |

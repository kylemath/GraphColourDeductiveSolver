# Track O: falsification of TrackM's π-run bound R ≤ 5 [data]

Studio, 8 Oct 2026, about 03:50–06:10 (about 2 h 20 min wall).
- Nothing is committed, and nothing outside `TrackO/` was modified.
- Read-only use of other tracks:
  - TrackM's `tm_lib.py` / `tm_run.py` (second engine, via Track A's `kempe_py`)
  - TrackJL-review's `rv_gen.py` (fresh random spheres)
  - Census29's `bin/frame` (TrackB `frame.c`; frame-class filter)
  - graph files from Census29, TrackF and `local-runs/27-studio-positive-config/jobbv`
- Compute: at most 6 workers, all under `nice -n 10`. Machine load from other users was about 16.

## 0. Bottom line

1. **The candidate lemma "R ≤ 5 on every triangulated sphere" is FALSE.** Two counterexamples, each verified by two independent engines (this track's C engine `to_eng.c` and TrackM's `tm_lib.py`):
   - **R = 6 inside the frame class itself**: Census29 `p32.r62#15615` (order 32, frame class), hole 11. This comes from the exhaustive census and needed no search.
     - TrackM's own rule runner on that hole: Φ>π and Φ>π-ADV need **8** swaps (= R + 2); the optimum is 4.
   - **R = 7** on a min-degree-5 sphere with no separating triangle: `out/hit_R7.txt`, n = 31, hole 21. Found by adversarial flip search. It is not frame class: `bin/frame` gives occfree = appfree = 0.
     - Φ>π needs **9** swaps.
     - The BFS optimum is **5**, which also breaks TrackM's observed dF ≤ 4.
   - Also **R = 7** with min degree 3 (`out/hit_R7_m3.txt`, n = 36, hole 21; verified by both engines).
   - No search produced R ≥ 8.
2. **The qualitative version is untouched.** There is no all-interior π-cycle (R = ∞) anywhere: 0 in 357,582 census holes and 0 in every other set and every search candidate. Φ>π never failed on any verified hole. So "R < ∞", which is the 4CT-strength statement, survives. The constant 5 does not, and neither does the "Φ>π within 7 swaps" corollary.
3. **Trend with n.**
   - In the exhaustive frame census, max R climbs about one step per order: 0, 0, 1, 2, 2, 3, 3, 4, 4, 5, 6 for n = 22…32. It moves in step with TrackJ's near-rigid NR: 5, 6, 6, 7 for n = 29…32.
   - This is not an n-effect per se. In the full min-degree-5 class, R = 5 already occurs at n = 24 (plantri24).
   - Random min-degree-5 spheres stay at R ≤ 5 up to n = 60. IPR fullerene duals stay at R ≤ 3 up to C100. Random min-degree-3 spheres stay at R ≤ 2.
   - So R is driven by special local structure, which adversarial search finds at n = 31. The frame class approaches it from below as the order grows.
   - The data give no evidence of any uniform constant. The best observed values are 6 (frame class) and 7 (min-degree-5 and min-degree-3 spheres).
4. **Long interior runs are not always near-rigid (N ≤ 9).**
   - In the frame census the *longest* runs mostly are. The R = 6 run is exactly the TrackJ J4/J5 shape: N = 9,8,9,8,9,8 with Kempe degree 3,2,3,2,3,2 (in-shape / rigid alternation). Of the L ≥ 4 runs, 174/236 at order 32 are near-rigid, 10/12 at L = 5 and 1/1 at L = 6.
   - **Counterexamples to the converse:**
     - In BV, 0 of the 608 runs with L ≥ 4 are near-rigid (N = 10–14), with R = 5 at holes where NR = 0.
     - In random min-degree-5 spheres, about 99% of interior states have N ≥ 10.
     - The verified min-degree-3 R = 7 run has N = 15,14,15,14,15,14,15. That is the same alternation shifted by +6 link-free chains, so "near-rigid" is not robust under adding link-free structure.
   - So **NRC does not control R**, and R ≤ NR fails (BV: R = 5, NR = 0). What persists in every long run is the alternation N, N−1, N, … which the chain-parity law forces along DL→DL π-steps.

## 1. Definitions (as TrackM §1/§4, re-implemented)

- **States:** proper 4-colourings of T − h up to renaming, at a degree-5 hole h.
- **Moves:** swap of any component of any of the six pair graphs.
- **Frame of an unfilled state:** link (α, μ, α, A, B) at x_j..x_{j+4}.
  - L1 = x_{j+3} ∈ K_{μA}(x_{j+1}), and L2 = x_{j+4} ∈ K_{μB}(x_{j+1}). DL = L1 ∧ L2.
  - π = swap K_{αA}(x_{j+2}), defined iff x_j ∉ it.
- **Interior state:** a DL state all of whose Kempe neighbours other than itself are DL. This equals TrackM's dNDL ≥ 2.
- **R(T, h):** the longest run of consecutive interior states along π, or −1 (∞) if some π-cycle is all interior. Runs are computed as maximal π-paths in the interior set. The run along π⁻¹ was re-checked in the second engine.
- **NR(T, h):** the same quantity for {DL, N ≤ 9}, where N is the total component count of the six pair graphs (TrackJ NRC; Lean `chainCount`).
- Per hole the engine also records:
  - the histogram of maximal interior runs by length, and how many of them are entirely N ≤ 9;
  - interior states by N;
  - up to 20 long runs (L ≥ 4) with their N and Kempe-degree sequences, plus the N and degree of the states just before and after the run.

## 2. Engine and validation

- `src/to_eng.c` is written for this track. It uses a bitmask state representation: canonical label masks with labels ordered by first occurrence; link = indices 0–4; BFS order.
- **Agreement with TrackM's `tm_run.py` pirun:**
  - census 27: 357/357 holes (S and R equal);
  - BV: 267/267 holes, including all nine R = 5 holes.
- **Second engine for every R ≥ 6 claim:** `src/to_verify.py` imports TrackM's `tm_lib.Hole` (`kempe_py`) and uses TrackM's exact interior definition (dNDL ≥ 2). It agrees on S, DL count, interior count and R, in both the π and π⁻¹ directions (`out/verify_*.txt`).
- Theorem D sanity check: π is undefined at a DL state 0 times on every sphere set (`noPiDL` = 0).

## 3. R histograms by source [data]

R values are per hole.

**Census29 frame class, exhaustive (every degree-5 hole of every graph, orders 22–32: 357,582 holes, 1.67 × 10⁹ states):**

| n | holes | max R | max NR | R histogram (0:1:2:3:4:5:6) |
|---|---|---|---|---|
| 22 | 12 | 0 | 1 | 12 |
| 23 | 14 | 0 | 3 | 14 |
| 24 | 55 | 1 | 3 | 51:4 |
| 25 | 36 | 2 | 4 | 20:12:4 |
| 26 | 165 | 2 | 4 | 132:23:10 |
| 27 | 357 | 3 | 4 | 208:139:8:2 |
| 28 | 1,563 | 3 | 5 | 997:536:29:1 |
| 29 | 4,533 | 4 | 5 | 2300:2024:178:29:2 |
| 30 | 18,490 | 4 | 6 | 8380:9254:784:68:4 |
| 31 | 69,006 | 5 | 6 | 23859:40757:3842:487:57:4 |
| 32 | 263,351 | **6** | 7 | 71484:171698:17715:2212:230:11:**1** |

Note: TrackM's "census ≤ 4" came from a partial pass-2 sample. The exhaustive census already has R = 5 at order 31 (4 holes) and order 32 (11 holes), and R = 6 at order 32.

**Other sources:**

| source | graphs / holes | max R | R histogram | max NR |
|---|---|---|---|---|
| plantri24 (TrackF; 7,209 min-degree-5 triangulations, n = 24) | 7,209 / 111,492 | **5** | 80974:24492:4373:1428:198:27 | 7 |
| IPR fullerene duals C60–C100 (TrackF `ipr32_52.txt`, all 1,267). 110 graphs use all 12 holes, the rest the first 4 holes | 1,267 / 5,948 (9.9 × 10⁹ states) | 3 | 13:3969:1932:34 | 5 |
| BV adversarial (jobbv, n = 37) | 12 / 267 | 5 | 113:87:14:34:10:9 | 3 |
| fresh random min-degree-5 spheres, n = 20–50 (`rv_gen`, seeds 7101–7103) | 430 / 8,406 | 5 | 4254:3093:811:220:21:7 | 5 |
| fresh random min-degree-5 spheres, n = 51–60 (seed 7104) | 40 / 1,266 (4.4 × 10⁹ states) | 5 | 334:536:249:128:13:6 | 5 |
| fresh random min-degree-3 spheres, n = 20–60 (seeds 7201–7202) | 500 / 3,043 | 2 | 3020:22:1 | 3 |

- IPR by order: max R is 3 at n = 39, 43, 47 and 49–52, and ≤ 2 elsewhere. There is no growth.
- Random min-degree-5 by order: max R = 5 at n = 29, 32, 34, 39, 41, 46, 57 and 58, with no trend. Full per-order tables are in `out/summary_*.txt`.
- No hole in any set was skipped (state cap 16M).

## 4. Adversarial search [data]

- `src/to_search.py` does hill-climbing with plateau moves, rare downhill steps (3%), revert-to-best and seed rotation.
- Moves: edge flips that keep the graph simple with min degree ≥ d. With d = 3 it also inserts and deletes degree-3 vertices.
- Objective: (max R over holes, W = Σ_runs 4^L), with the engine in `-q` mode and a 400k-state cap per hole.
- Seeds: the BV graphs, the 16 census graphs with R ≥ 5, then the R = 7 graph, then the plantri24 graphs with R = 5.

| run | variant | rounds | best R |
|---|---|---|---|
| `search_v1/` (first launch, loose acceptance) | d = 5 and d = 3 | 300 + 75 | 6 |
| `search_m5` | d = 5, seeds census R ≥ 5 + BV | 1,500 (stopped) | **7** (round 937, from `p31.r9#2271`; n = 31) |
| `search2_m5` | d = 5, seed R = 7 graph | 6,774 | 7 (no 8) |
| `search2_m3` | d = 3, n ≤ 36, seed R = 7 graph | 2,019 | 7 (n = 36; verified) |
| `search3_frame` | frame class only (every candidate passes `bin/frame`), seeds census R ≥ 5 | 13,229 | 6 (no frame-class graph with R = 7 found) |
| `search4_p24` | d = 5, n = 24, seeds plantri24 R = 5 | 9,948 | 5 (no 6 at n = 24) |

The **R = 7** example is `out/hit_R7.txt`, hole 21:
- 31 vertices, degrees 5¹⁶ 6¹¹ 7⁴, no separating triangle.
- The run is N = 9,8,9,8,9,8,9 with Kempe degree 3,2,3,2,3,2,3.
- It is preceded by a DL state with N = 12 (Kempe degree 6) and followed by one with N = 12 (degree 8).
- So it is a full near-rigid J5-type stretch of length 7, every state of which is interior.
- TrackJ's NRC data had near-rigid runs of length ≤ 7. Here such a run of length 7 is entirely interior.

## 5. Interior runs vs near-rigid runs (task 3) [data]

Maximal interior runs, all of them and (in brackets) those entirely N ≤ 9:

| source | L = 3 | L = 4 | L = 5 | L = 6 | interior states with N ≤ 9 |
|---|---|---|---|---|---|
| census 22–29 | 33 (22) | 2 (2) | | | 3,768 / 6,178 |
| census 30 | 79 (40) | 4 (1) | | | 13,036 / 21,409 |
| census 31 | 579 (343) | 64 (51) | 4 (2) | | 64,794 / 109,664 |
| census 32 | 2,493 (1,426) | 236 (174) | 12 (10) | 1 (1) | 292,052 / 529,955 |
| plantri24 (from dumps) | — | 254 (170) | 36 (19) | | 51,863 / 72,384 |
| BV | 1,864 (0) | 400 (0) | 208 (0) | | 55 / 39,313 |
| random min-degree-5, n ≤ 50 | 5,553 (94) | 204 (12) | 205 (1) | | 13,100 / 348,154 |
| random min-degree-5, n = 51–60 | 1.1M (85) | 149k (14) | 89k (2) | | 16,465 / 7.9M |

- Holes with R ≥ 4, as (R, NR) pairs (census 32): (4,1) 15, (4,2) 19, (4,3) 21, (4,4) 92, (4,5) 82, (4,6) 1, (5,1) 1, (5,3) 1, (5,5) 5, (5,6) 4, (6,7) 1.
- So even in the frame class an R = 5 run can sit at a hole whose near-rigid runs are only 1 long.
- **Reading:**
  - In the tight frame class, long interior runs are predominantly near-rigid, and the record runs (R = 6 census, R = 7 search) are exactly the J4/J5 alternation of rigid (Kempe degree 2) and in-shape (Kempe degree 3) states.
  - In looser graphs, long interior runs have many link-free chains (N up to 20+) while keeping the N, N−1 alternation.
  - A proof of R-bounds therefore cannot go through NRC alone. The relevant invariant looks like "near-rigid modulo link-free components": DL, with exactly 8 link-meeting chains, all extra chains link-free.

## 6. Verdict

- **Candidate lemma R ≤ 5: refuted.**
  - R = 6 occurs in the frame class (exhaustive census 32).
  - R = 7 occurs on min-degree-5 (no separating triangle) and min-degree-3 spheres.
  - All three were checked by two independent engines, and Φ>π's swap count R + 2 was confirmed with TrackM's own runner (8 and 9).
- Max R grows with order in the frame census (4, 4, 5, 6 at orders 29–32). There is no evidence for a uniform constant.
- The qualitative statement "no all-interior π-cycle on the sphere" (equivalently, Φ>π always terminates) is consistent with all data. That is the 4CT-strength claim worth keeping.
- Any quantitative version needs a bound that grows with something. Long interior runs coincide with the J5 alternation, so their length is tied to how long near-rigid (mod link-free) stretches can be. Those stretches are also observed to grow, from 4 to 7.

## Files

| path | content |
|---|---|
| `src/to_eng.c` | C engine (final source; binaries `to_eng4` = current source, `to_eng3`/`to_eng2` = same without `-k` / without `-k`,`-D`,runsNR, `to_eng` = first build, used for plantri24 and IPR part 1; R/NR/run outputs identical) |
| `src/to_verify.py` | second-engine check of R via TrackM `tm_lib.Hole` |
| `src/to_conv.py` | faces-JSON → rotation lines (BV) |
| `src/to_search.py` | adversarial flip search (`--frame` restricts to the frame class via `Census29/bin/frame`) |
| `src/to_summary.py` | aggregation |
| `src/run_*.sh` | launch scripts (`run_census.sh` / `run_sets.sh` are the first launches, superseded by `run_sets2.sh` except plantri24) |
| `out/frame-NN.jsonl` (31, 32 and `plantri24.jsonl` gzipped), `ipr_part*.jsonl`, `bv.jsonl`, `fresh_*.jsonl` | per-hole records and long-run dumps |
| `out/fresh_*.txt`, `bv.txt`, `seeds_*.txt` | input graphs |
| `out/summary_sets.txt`, `summary_ipr.txt`, `summary_fresh_m5_51_60.txt` | aggregated tables |
| `out/census32_R6_graph.txt`, `out/hit_R7.txt`, `out/hit_R7_m3.txt` | the counterexample graphs (rotation lines; holes 11, 21, 21) |
| `out/verify_R6_census32.txt`, `out/verify_R7.txt`, `out/verify_R7_m3.txt` | second-engine and TrackM Φ>π confirmations |
| `out/tm_phipi_R6.jsonl`, `out/tm_phipi_R7.jsonl` | TrackM `tm_run.py --pass2` output on those graphs |
| `out/search*.log`, `out/search*.hits.txt`, `out/search_v1/` | search logs and hit graphs |

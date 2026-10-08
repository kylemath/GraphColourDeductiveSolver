# Track A: attempts to break R* in the frame class [exploratory] (Mac Studio, 7 Oct 2026)

**Target (RStarFrame, FrameF3.lean).** Every connected spherical triangulation with minimum degree 5, NoSep, and no `Occ` of the Birkhoff diamond or of RSST 2.122 (either orientation) has a PureClean degree-5 vertex. PureClean(v) means every Kempe class of proper 4-colourings of T − v contains a filled state, i.e. a state where the link uses at most 3 colours.

**Result.** No counterexample was found. Every degree-5 vertex of every frame-class graph examined is PureClean. That covers 43 census graphs (complete for orders 12–27, given the input lists), 104 graphs at order 28, and about 57,800 frame-class graphs evaluated by the search, of orders 24–37. The minimum class filled fraction never drops below **exactly 1/4**, and it reaches 1/4 often. Every result below is **data**. None of it is a proof.

## 1. Frame-class filter (`tracka_lib.py`, `selftest_filter.py`, `census_filter.py`)

**What the filter checks** (`G.summary`):
- The graph is a triangulation: simple, E = 3n − 6, 2n − 4 faces, a globally consistent orientation, and connected.
- Minimum degree is at least 5.
- NoSep: every triangle is facial.
- There is no `Occ` of DiamondM, DiamondP, C2122M or C2122P.

**How Occ is checked.** The Occ test is the Lean structure itself. `load_occ` parses the `Nx T` facts and the degree vector from `*Occ.lean`. It also asserts that the structure has no fields other than injectivity, disjointness, degrees and Nx. The search propagates from (int 0, int 1), as in `StudioMathReview-scripts/occ_search.py`. The four configurations come out as ring 6 / interior 4 / degrees 5555 / 20 facts for the diamonds, and ring 7 / interior 4 / degrees 6555 / 21 facts for 2.122. A self-test checks that P is exactly M with reversed rotation.

**Proxy and TipsClean caveat.** `Appears` and `TipsClean` are computed only for cross-checks and as a fast pre-filter. Since Occ ⇒ Appears, Occ is searched only when an appearance exists.
- **TipsClean caveat (data):** across all 444,820 census graphs, orders 12–27, **0 graphs have an appearance but no Occ**. So the appears-based lists (`in-cfree-27.txt`, picyc `cfree`, studiointel `count_occ`, which checks interior faces only) agree with the Lean-faithful filter at these orders.

**Tests on known examples (data):**

| Graph | Occ count (M/P) | Frame class? |
|---|---|---|
| Icosahedron | diamond 60/60, 2.122 0/0 | no, as in `Icosahedron.not_diamondFree` |
| Tri22 F-cycle graph (`studiointel/fcycle/fcycle_order22.json`) | diamond 10/10, 2.122 8/8 | no, as in `Tri22Sanity` |
| p27#4710 | 0 | yes |

- Mirror images give swapped M/P counts.
- None of the 171 constructed graphs from Jobs AS/AW/BI/BV/BQ/BJ is in the frame class (`out/constructed-frame-check.json`). All of them contain diamond and 2.122 Occs.

**Census (plantri −m5 −c4 lists in `27-studio-positive-config/in-plantri-*.txt`).** Graphs read per order, with the number in the frame class in brackets:

| Order | Graphs read | Frame class |
|---|---|---|
| 12 | 1 | 0 |
| 14 | 1 | 0 |
| 16 | 3 | 0 |
| 17 | 4 | 0 |
| 18 | 12 | 0 |
| 19 | 23 | 0 |
| 20 | 73 | 0 |
| 21 | 191 | 0 |
| 22 | 649 | **1** |
| 23 | 2,054 | **1** |
| 24 | 7,209 | **4** |
| 25 | 24,963 | **2** |
| 26 | 89,376 | **11** |
| 27 | 320,133 | **24** |

- In total that is **43 frame-class graphs**. The order-27 set equals `in-cfree-27.txt`.
- Completeness of the input lists is inherited from the earlier plantri runs and is not re-checked here; plantri is not installed.
- Order 28: only the 104-graph appears-free list `in-cfree-28.txt` was available. All 104 pass the Lean-faithful filter. Frame-class graphs at order 28 that have an appearance but no Occ could be missing, but none occur at orders ≤ 27.

## 2. PureClean census (`holes.py`, `census_eval.py`, `census_stats.py` → `out/census-*.jsonl`, `out/census-stats.txt`)

**Engines.**
- **Engine 1:** `bin/picyc --full`, compiled from an unmodified copy of `27-studio-positive-config/picyc.cpp`. It gives the Kempe classes of T − v per class as [size, F].
- **Engine 2:** `local-runs/common/kempe_py.Space`, independent stdlib Python (`build_graph`, `classes`, `filled`).
- **Margin definitions.** minfrac(v) = min over classes of F/size. The graph margin is max over degree-5 v of minfrac(v); the graph worst is min over degree-5 v of minfrac(v).

**Orders 12–27 (data):**
- 43 graphs and 639 degree-5 vertices, all **PureClean (639/639)**.
- **0 graphs have a non-PureClean vertex.** The fewest PureClean vertices in a graph is 12, which equals the number of degree-5 vertices: 11 graphs have exactly 12 degree-5 vertices.
- Engine 2 reproduces the class multisets of all 43 graphs exactly (0 mismatches).
- Margin: min **0.3139**, median 0.5475, max 0.7299. Worst: min **0.2500**, median 0.4568.
- Classes per hole: 1 class at 629 holes, 2 classes at 8, 3 classes at 2.
- The small classes (size, F) are (5, 5) ×4, (6, 4) ×3, (12, 8) ×3 and (8, 2) ×2.
- The minimum per-vertex class fraction is exactly 1/4, at 2 vertices of p27#8475, from an (8, 2) class.

**Most marginal graphs:**
- **p24#2550**: 12 degree-5 vertices, all in one Kempe class of 411 states with F = 129. Every vertex has minfrac 0.3139, so margin = worst = 0.3139.
- **p27#47915**: margin 0.4709, worst 0.4325.
- p24#1803: margin 0.4872. p26#6120: margin 0.4925.

**Order-28 appears-free list (data, engine 1 only):**
- 104 graphs and 1,563 degree-5 vertices, **all PureClean**.
- Margin: min 0.5038 (p28#668116), median 0.5613. Worst: min 0.2500.
- 23 vertices have minfrac exactly 1/4: 22 come from (4, 1) classes and 1 from an (8, 2) class (p28#546102). Examples are p28#44900, #94025 and #218651, each with 6–8 such vertices.

**IPR fullerene duals (n = 32–52; all frame class, flat holes).**
- I did not re-run these. One graph at n = 46 costs about 14 s CPU (2 minutes wall at load ~116), and earlier runs in `out/ipr*.jsonl` used `--pi` mode without class data.
- Job BS / studiointel `flat_kclass` report one class per flat hole at the n = 56–62 samples, and the 32 positive IPR holes in `ipr-pos-full.jsonl` are single classes with F/N ≈ 0.6. The only IPR dual searched here is ipr#292 (n = 32), as a seed.

## 3. Adversarial search inside the frame class (`tracka_search.py`; seeds `clean_seeds.py`, `grow_seeds.py`, `make_seeds.py`; runs `run_search.sh`, `phase2.sh`–`phase4.sh`)

**Machinery.** This follows Jobs AW/BQ:
1. A random edge flip anywhere (there is no protected hole, because the objective is global).
2. Up to 3 degree-repair flips.
3. The candidate is accepted only if it is a triangulation with min degree 5, NoSep, and Occ-free for all four Lean configurations. Max degree ≤ 10 is imposed for engine practicality only; it is not a frame condition.
4. The candidate is evaluated with picyc at every degree-5 vertex. It is accepted if its key is ≤ the current key, or otherwise with probability 0.15.

**Objectives** (all minimised):
- **R** = (number of PureClean degree-5 vertices, margin), as specified. A hit is 0 PureClean vertices.
- **M** = ([any PureClean], margin, worst). I added M because PureClean count = degree-5 count on every graph seen, so R's first component only pushes towards 12 degree-5 vertices.
- **W** = (worst). A hit is any non-PureClean degree-5 vertex. W also attacks QuarterFloorConj in the frame class.

**Seeds:**
- The 15 most marginal census graphs (orders 24–28).
- 8 frame-class graphs (n = 37), produced by flipping the Occs out of the Job AS constructions and the Job BQ/BV hit graphs. `clean_seeds.py` cleaned 42 of these; none of the originals is in the frame class.
- 12 frame-class graphs grown beyond the census (n = 32 and 36, by face insertion plus repair plus mixing flips, every intermediate graph frame-class), plus ipr#292 (n = 32).
- p24#2550 and p26#6120 are rigid: no frame-preserving growth was found (p24#2550 also never moved under flips).

**Budget (data):** 153 walks, **57,800 frame-class evaluations**, **0 hits** for R, M and W.

| Order n | Walks | Evaluations | Best margin reached | Best worst reached |
|---|---|---|---|---|
| 24 | 12 | 4,800 | 0.3139 (p24#2550, rigid) | 0.3139 |
| 26 | 6 | 2,400 | 0.4925 (rigid) | 0.4231 |
| 27 | 30 | 12,000 | 0.4709 | **0.2500** |
| 28 | 42 | 16,800 | 0.5038 | **0.2500** |
| 32 | 21 | 9,800 | **0.4427** (from ipr#292) | **0.2500** |
| 36 | 18 | 8,400 | 0.4730 | **0.2500** |
| 37 | 24 | 3,600 | 0.4932 | **0.2500** |

**Margin trend (data):** the margin does not trend down.
- At fixed n ≤ 28 the walks only re-visit the tiny census frame class. For example, walks from 4 different n = 27 seeds all end at p27#47915's 0.4709.
- At n = 32–37 the margin settles at 0.44–0.50 in every run.
- 1,000-step walks (phase 4) did not beat 200-step walks systematically.
- The global minimum margin is still the census graph p24#2550 (0.3139).

**Floor (data):** 32 W walks out of 51 reach worst = exactly 1/4: n = 27 (2), 28 (10), 32 (7), 36 (6), 37 (7). None goes below 1/4. The tight classes are always (4, 1) or (8, 2). An example is `out/best/best-W-search-phase2.json` (n = 32, hole 3, link degrees (6, 5, 6, 7, 6), classes [(4, 1), (5605, 2515)]).

**Independent re-check of the best graphs** (`verify_best.py`, both engines, full Lean-faithful filter) gives all frame-class, engines agree, all vertices PureClean:

| File | n | Degree-5 vertices | Margin | Worst |
|---|---|---|---|---|
| `out/best/best-M-search-phase4-M.json` | 32 | 16 | 0.4427 | 0.4257 |
| `out/best/best-M-search-constr-M.json` | 37 | 24 | 0.4932 | 0.4049 |
| `out/best/best-W-search-phase2.json` | 32 | 14 | 0.5561 | 0.2500 |

## 4. Reading

- **R\* in the frame class survives:** the complete census to order 27 (as listed), the order-28 appears-free list, and 57,800 search evaluations to n = 37.
- R\* is never even close to failing: every vertex of every graph seen is PureClean, not just some vertex. "Zero PureClean vertices" would need every degree-5 vertex to carry a class with F = 0, while the observed per-class fraction is ≥ 1/4 everywhere.
- The meaningful adversarial target is therefore the **quarter floor**: a single class with F/N < 1/4.
  - In the frame class it is tight (1/4 is attained by (4, 1) and (8, 2) classes at every order searched from 27 on).
  - It was never broken.
- Suggested next attack (not run):
  - Search on the small-class structure directly. The objective would be to minimise F among classes of size ≤ 16, or to maximise the number of (4, 1) classes.
  - Add moves that change n (insert/delete) inside the search.
  - Run class-mode picyc on the IPR duals n ≤ 45, which needs about 105 graphs × 15–60 s CPU.

## Files

- `tracka_lib.py`: the filter.
- `holes.py`: both engines.
- `census_filter.py`, `census_eval.py`, `census_stats.py`: steps 1–2.
- `tracka_search.py`: step 3.
- `clean_seeds.py`, `grow_seeds.py`, `make_seeds.py`: seed preparation.
- `verify_best.py`, `summarize_search.py`, `check_constructed.py`, `selftest_filter.py`: checks and summaries.
- `bin/`: picyc copy and binary.
- `out/`:
  - `frame-*.txt`: frame-class graphs as picyc lines.
  - `filter-*.json`: counts and TipsClean caveat records (empty).
  - `census-*.jsonl`: per-graph classes per hole.
  - `search-*.jsonl`: per walk, with log, trace, best faces and hits.
  - `best/`, `verify-*.json`.

All compute ran under `nice -n 10`, with at most 4 single-threaded workers. Nothing is still running.

---

# Task 2: what the quarter-floor equality classes look like (`anat/`, 7 Oct)

Scripts:
- `anatomy.py`: the move graph of each class, the labelled product test, the unlabelled hypercube test, cycle order, locks and link words.
- `anatomy_pi.py`: the π-cycles contained in each class, plus a Theorem W check. Uses `uv_lib.Hole`, both orientations.
- `anatomy_pi2.py`: the π-orbit pattern of each class.
- `anatomy_dedup.py`: removes duplicate graphs and counts w = 0, L = 4 π-cycles from picyc hist.
- `anatomy_summary.py`: writes `anat/summary.txt`.

**Graphs (data).** 160 graphs in total, 148 after deduplication:
- census order 27: 24 graphs;
- order-28 list: 104 graphs;
- the 32 W-walk best graphs (n = 27–37), of which 12 duplicate census graphs.

These hold 2,349 classes at 2,448 degree-5 holes. Class multisets agree between picyc and kempe_py at every hole re-enumerated. IPR duals were not run (Track F owns them).

## Equality classes (4F = N): 58 distinct, in 25 graphs

**Sizes.**

| N | F | Count | Orders where they occur |
|---|---|---|---|
| 4 | 1 | 50 | 28, 32, 36, 37 |
| 8 | 2 | 8 | 27, 28, 36, 37 |

No equality class has more than 8 states. Every class with N a power of two is an equality class, and no class breaks the floor (4F < N: 0).

**Move graph.**
- **(4, 1):** always a 4-cycle (50 of 50).
- **(8, 2):** three shapes:
  - a single 8-cycle: 2;
  - 3-regular, isomorphic to Q3 as a bare graph: 2;
  - 4-regular with 16 edges: 4.

**π-structure.** Every equality class is a union of π-cycles with w = 0. Each of those π-cycles repeats one 4-state block (244 of 244 π-cycles, both orientations).

**The block.** Along π, with λ in brackets:

DL (+1) → L1 (−1) → F (−1, φA) → L2 (+1) → back to DL

So the λ-sum is 0, and exactly 1 state in 4 is filled.

**How the classes are built from the block:**
- (4, 1): one block, and the move graph is exactly that π-cycle (all 4 edges are π-steps).
- (8, 2): either one π-cycle of length 8 (the block twice) or two π-cycles of length 4. The extra non-π edges, 4 or 8 of them, join the two copies.

**Unfilled states.** They are always exactly one DL, one L1-only and one L2-only per filled state. N0 never occurs, and τ never occurs (the filled step is always φA).

**Link degree words** (all 114 equality records, including duplicates):

| Degree word | Records |
|---|---|
| (5,6,6,6,6) | 43 |
| (5,5,6,6,7) | 33 |
| (5,5,6,6,6) | 18 |
| (6,6,6,6,7) | 4 |
| (5,6,6,7,6) | 4 |
| other | 12 |

**Chains.** Edges out of a filled state swap a pair {link colour, colour absent from the link}. Edges out of a locked state swap a pair of link colours, and the component together with the rest of its pair-subgraph meets 2–3 link vertices.

## Is it a product of independent chain flips? No (data)

- **Labelled product test:** 0 of all analysed classes pass. That is 127 classes with duplicates, covering every class with N ≤ 64, N a power of two, or 4F = N.
  - Large classes are not powers of two, so they cannot be cubes at all.
  - Even the 4-cycle is not a product. Opposite edges swap different chains: the colour pairs and vertex sets differ.
- **Unlabelled hypercube test:** passes only for the 50 four-cycles (Q2) and the 2 Q3-shaped (8, 2) classes.
- **Factor-by-factor floor:** not applicable, because there are no factors.

## Why equality holds

**Identity (Theorem W, checked here with 0 failures on all 254 small-class records):** 4F − N = −5 Σw over the class. Hence:
- F/N = 1/4 − 5Σw/(4N);
- the floor holds exactly when Σw ≤ 0;
- equality holds exactly when Σw = 0.

**Conjecture E (data, frame class):**
- A Kempe class with F/N = 1/4 is a union of w = 0 π-cycles, each a repetition of the block DL → L1 → F(φA) → L2. Such a class contains no τ-state, no N0-state and no cycle with w ≠ 0. The data supports this: 58 of 58 distinct equality classes, 244 of 244 π-cycles.
- Equality classes are tiny. They have N ∈ {4, 8} in every case seen.

**Testing the block against all classes:**
- The same block also occurs inside larger classes. Of the 67,333 π-cycles with w = 0 and L = 4 (plantri orientation, distinct graphs), 56 make up equality classes and 67,277 sit inside larger classes with Σw < 0.
- So equality is exactly the case where a class is closed under Kempe swaps using only such blocks.
- The other small classes all have Σw < 0, so their F/N is above 1/4:

| (N, F) | π-cycles (L, w) | F/N |
|---|---|---|
| (6, 4) | one cycle (6, −2) | 2/3 |
| (10, 10) | two cycles (5, −3) | 1 |
| (12, 8) | one cycle (12, −4) | 2/3 |
| (24, 16) | two cycles (12, −4) | 2/3 |

Outputs:
- `anat/anat-census27-28.jsonl`, `anat/anat-wbest.jsonl`: per-class anatomy, with the full state lists for N ≤ 64.
- `anat/anat-pi.jsonl`: π-cycles per class.
- `anat/summary.txt`, `anat/pi-patterns.txt`, `anat/dedup.txt`.

---

# Task 3: positive π-winding inside the frame class (`posw/`, 7 Oct)

**Why.** By Theorem W, 4F − N = −5 Σw over a Kempe class, so the quarter floor fails exactly when some class has Σw > 0. Task 3 asks whether frame-class holes carry any π-cycle with w > 0 at all, and if so how close a class gets to Σw > 0. Slack of a class is −Σw/N (F/N = 1/4 + (5/4)·slack); slack 0 is equality.

Scripts:
- `posw_scan.py`: picyc `--full` in both orientations at every degree-5 hole; per hole the π-cycle histogram (w, L, count) and the class signatures [N, F, Σw].
- `posw_stats.py`: statistics of the scans.
- `posw_search.py`: flip + grow search (insert a vertex with probability 0.12 when n < NMAX, otherwise a frame-preserving flip, hill-climb with 0.15 random acceptance). Every visited graph passes the Lean-faithful frame filter, max degree ≤ 10. Key, maximised: ([some class has Σw > 0], total positive weight Σ_{w>0} w over all holes, −min slack over classes with N > 8). Plantri orientation only.
- `posw_summary.py`, `posw_report.py`: per-n tables from the search files.
- `posw_verify.py`: two-engine re-check. picyc in both orientations; then `uv_lib.Hole` (kempe_py.Space + escape.pi_of, independent Python) at every hole with a w > 0 cycle in either orientation, giving the class split of the π-cycles, kind counts (R3 λ = +1, φB −1, φA −1, τ −3), DL counts, Theorem W per class, and a hole-by-hole comparison of the class multisets (N, F, Σw) with picyc.
- Runs: `posw/run.sh` (8 walks, n → 48, 3000 s each, 4 workers; it survived the app restart and finished at 16:25), `posw/run2.sh` (5 walks from the n = 48 bests, n → 60, 4500 s each, 5 workers). All under `nice -n 10`.

## 3.1 Census and walk graphs: no positive π-cycles at all (data)

Input: 321 graph records. 147 are census graphs (orders 22–28: 1, 1, 4, 2, 11, 24, 104) and 174 are the best graphs of the task-1 walks (n = 24–37; some are re-visits of census graphs). Both orientations: 4,996 holes and 5,145 classes each.

- π-cycles with w > 0: **0** in either orientation. The largest cycle winding at a hole is 0 at 4,993 holes and −2 at 3 holes.
- Largest class Σw: **0**. That is attained only by the 126 equality class records (N ∈ {4, 8}, the task-2 classes). No class with N > 8 has Σw = 0.
- Min slack over classes with N > 8: 0.0511 (p24#2550, its single 411-state class, Σw = −21). Otherwise ≥ 0.10. By order: 22: 0.227, 23: 0.231, 24: 0.051, 25: 0.139, 26: 0.127, 27: 0.116, 28: 0.102, 32: 0.102, 36: 0.114, 37: 0.102.
- So link words do not matter here: no positive cycle exists anywhere at n ≤ 37 in these sets.

## 3.2 Search to n = 56 (data)

Budget: 13 walks, **1,878 frame-class evaluations** (run 1: 8 walks, 1,658 evaluations, n 32 → 48; run 2: 5 walks, 220 evaluations, n 48 → 53–56; evaluations cost 10–15 s at n ≈ 48 and 100–170 s at n ≈ 53–56). **0 hits**: no evaluated graph had a class with Σw > 0, so the quarter floor held everywhere.

Per n (positive weight = Σ_{w>0} w over all holes of one graph, plantri orientation; slack over recorded states, i.e. the per-n best and every 10th iterate, not every evaluation):

| n | walks | walks with a w > 0 cycle | max positive weight | max # positive cycles | max w | min slack (N > 8) |
|---|---|---|---|---|---|---|
| 32–36 | 1–4 | 0 | 0 | 0 | 0 | 0.119–0.171 |
| 37 | 8 | 1 | 2 | 2 | 1 | 0.114 |
| 38–40 | 8 | 0 | 0 | 0 | 0 | 0.061–0.107 |
| 41 | 8 | 1 | 2 | 1 | 2 | 0.115 |
| 42 | 8 | 3 | 2 | 1 | 2 | 0.115 |
| 43 | 8 | 1 | 1 | 1 | 1 | 0.103 |
| 44 | 8 | 3 | 4 | 1 | 4 | **0** (a (16, 4) class) |
| 45 | 8 | 2 | 2 | 2 | 2 | 0.117 |
| 46 | 8 | 1 | 2 | 1 | 2 | **0** (a (16, 4) class) |
| 47 | 8 | 2 | 2 | 1 | 2 | 0.113 |
| 48 | 13 | 11 | 8 | 2 | 4 | **0** |
| 49–50 | 5 | 0 | 0 | 0 | 0 | 0.118–0.127 |
| 51 | 5 | 1 | 2 | 1 | 2 | 0.133 |
| 52 | 5 | 1 | 6 | 2 | 4 | 0.129 |
| 53 | 5 | 3 | **40** | **10** | **8** | **0** |
| 54 | 4 | 1 | 4 | 2 | 2 | **0** |
| 55 | 4 | 1 | 2 | 1 | 2 | 0.134 |
| 56 | 2 | 2 | 4 | 4 | 1 | 0.134 |

**Positive cycles exist from n = 37 on**, at ≤ 2 holes per graph, and their mass grows with n (max 8 at n ≤ 48, 40 at n = 53). The search maximised exactly this mass.

**Link words at holes with w > 0 cycles.** There are 31 positive holes in 29 distinct recorded graphs, giving 24 distinct words as written (rotation and reflection not merged).
- Most frequent: (5,7,5,5,7) ×3, (5,7,5,8,5) ×3, (5,7,5,6,6) ×2, (7,5,5,7,5) ×2, (6,5,5,6,9) ×2.
- Every word contains a degree-5 link vertex. 23 of 24 contain a link vertex of degree ≥ 7; the exception is (6,5,5,6,6) at A7f1-n53. 20 of 24 have at least two degree-5 link vertices; the exceptions are (6,8,5,6,6), (6,7,5,6,6), (7,6,5,7,7) and (7,6,5,9,7).
- No 66666 hole ever carried a positive cycle.
- The same kind of words, e.g. (5,5,6,6,7), occur at n ≤ 28 with no positive cycle, so the link word alone does not decide.

**Slack trend (honest reading).**
- Among classes with Σw < 0 the min slack does **not** trend to 0. It is 0.06–0.17 at n = 32–48 (lowest 0.061 at n = 39) and 0.118–0.134 at n = 49–56. The census minimum 0.051 (n = 24) is still the lowest seen.
- The zeros at n = 44, 46, 48, 53 and 54 are equality classes, not near-failures. Slack 0 on a class with N > 8 means Σw = 0, i.e. F/N = 1/4 exactly. I re-enumerated three of them with engine 2 (n = 44, 46, 54), and each is a **(16, 4) class** at a hole with link word 66667 (up to rotation), in both orientations:
  - kinds R3 8, φB 4, φA 4, so the π-cycles are copies of the task-2 block DL → L1 → F(φA) → L2;
  - the π-cycles are four w = 0 cycles of length 4, except n = 54 in the plantri orientation, which has two w = 0 cycles of length 8;
  - the other classes at those holes are (155,668, 75,187) at n = 44; two (8, 2) classes plus (285,559, 133,041) at n = 46; and (1,755,902, 1,000,358) at n = 54.
  - **This amends Conjecture E: equality classes with N = 16 exist.** The zeros at n = 48 and 53 come from trace states whose faces were not saved, so their class sizes are unknown.
- The positive mass is sub-dominant by 3–4 orders of magnitude (§3.3). Its growth is real but tiny next to the negative mass of the same class.
- Caveat: n ≥ 49 had only 220 evaluations; the slack at n ≥ 49 is a thin sample.

## 3.3 Where the positive cycles sit, and who pays (two engines, data)

Graphs: 14 search graphs (n = 37–54), chosen for the most positive mass at each n plus the two equality-at-N = 16 graphs (`posw/verify-batch{1,2,3a,3b}.json` → `.jsonl`). All are frame-class. At every hole re-run with engine 2 the class multiset (N, F, Σw) agrees with picyc and Theorem W holds for every class (0 mismatches, 0 failures, both orientations).

| graph | n | hole link | orient | positive cycles (L, w) | class N | F/N | class Σw | slack | posw / Σ_{w<0}|w| |
|---|---|---|---|---|---|---|---|---|---|
| p28#546102-grow36-n37 | 37 | 5,7,5,5,7 | p | 2 × (17, 1) | 22,129 | 0.526 | −4,879 | 0.221 | 4.1e-4 |
| A7f3-n42 | 42 | 5,7,5,7,5 | p | (14, 2) | 74,506 | 0.511 | −15,558 | 0.209 | 1.3e-4 |
| p27#47915-grow32-n42 | 42 | 10,5,5,9,5 | p | (30, 2) | 59,206 | 0.493 | −11,522 | 0.195 | 1.7e-4 |
| p27#47915-grow36-n44 | 44 | 5,6,6,7,5 | p | (53, 1) | 132,010 | 0.492 | −25,558 | 0.194 | 3.9e-5 |
| p28#546102-grow36-n44 | 44 | 7,6,5,5,6 | p / m | (28, 4) / 2 × (14, 2) | 102,212 | 0.481 | −18,912 | 0.185 | 2.1e-4 |
| p27#47915-grow36-n45 | 45 | 7,6,6,5,5 | p / m | 2 × (17, 1) / (17, 1) | 160,312 | 0.514 | −33,824 | 0.211 | 3–6e-5 |
| A7f3-n48 | 48 | 5,7,5,6,6 | p | 2 × (28, 4) | 281,865 | 0.468 | −49,135 | 0.174 | 1.6e-4 |
| A7f1-n48 | 48 | 5,7,5,6,6 | p | (28, 4) | 426,453 | 0.495 | −83,503 | 0.196 | 4.8e-5 |
| A7f4-n48 | 48 | 6,8,5,6,6 | p | 2 × (14, 2) | 396,725 | 0.455 | −65,043 | 0.164 | 6.2e-5 |
| A7f1-n53 | 53 | 7,6,5,7,7 | p | 2 × (18, 2), (42, 2) | 1,467,015 | 0.521 | −317,909 | 0.217 | 1.9e-5 |
| A7f1-n53 | 53 | 6,5,5,6,6 | p | 4 × (17, 1) | 1,515,085 | 0.504 | −308,295 | 0.203 | 1.3e-5 |
| p27#47915-grow36-n53 | 53 | 7,6,5,9,7 | p | 3 × (14, 2), (26, 2), 4 × (28, 4) | 1,419,030 | 0.468 | −247,190 | 0.174 | 9.7e-5 |
| p27#47915-grow36-n53 | 53 | 6,7,5,9,5 | p | 2 × (136, 8) | 1,454,835 | 0.456 | −240,029 | 0.165 | 6.7e-5 |

**Where they sit.**
- Every hole carrying a positive cycle has a **single Kempe class** (the whole state space of T − v). So the positive cycles are always inside the giant class. That class has slack 0.16–0.22, **above** the graph's own min slack. Positive winding does not show up in the marginal classes.
- Orientation matters. Most positive cycles appear in one orientation only. In the two graphs positive in both orientations, the total positive weight differs or splits differently between them (n = 44: one (28, 4) vs two (14, 2); n = 45: 2 vs 1).
- **Anatomy.** A positive cycle is a long run of R3 steps (λ = +1, the L2-locked unfilled state of pi_of), broken by a few φB/φA pairs, with no τ (except the w = 1 cycles):
  - (14, 2): R3 12, φB 1, φA 1 (11 DL);
  - (28, 4): R3 24, φB 2, φA 2 (22 DL): the (14, 2) pattern twice;
  - (17, 1): R3 12, φB 2, φA 2, τ 1;
  - (136, 8): R3 88, φB 24, φA 24 (64 DL);
  - in general w = (#R3 − #φB − #φA − 3#τ)/5, so a positive cycle needs R3 > 2·#φA + 3·#τ along it. The filled fraction on a positive cycle is about 1/14 to 1/6.

**Who pays.**
- The negative winding of the class is concentrated in a handful of giant π-cycles: the 3 most negative cycles carry 56–88% of Σ_{w<0}|w|. Examples: at A7f3-n48, hole 22 has cycles of w = −18,870, −16,094 and −2,372 among 7,259; at p27#47915-grow36-n53, hole 9 has −114,459 and −84,027 among 35,595.
- The bulk of the rest are short w = −2, −4 cycles (1,066–4,235 of them per class), plus 584–5,376 w = 0 cycles.
- Total positive weight is 1.3e-5 to 4.1e-4 of the negative weight in the same class. Nothing local cancels it: the positive cycles sit next to w = 0 and w = −2 cycles, and the class balance is settled by the global giant cycles.

**Side observations (data, every class re-enumerated with engine 2, 14 graphs):**
- **#φA = #φB in every class**, positive or not. Hence Σw = (#R3 − 2#φA − 3#τ)/5 per class.
- F is the same at every hole of a graph (e.g. 663,745 at both holes of p27#47915-grow36-n53). This is expected, since a filled state of T − v extends uniquely to a colouring of T. It is a useful engine sanity check.

## 3.4 Reading

- The quarter floor was never broken: 0 classes with Σw > 0 over 321 scanned graphs (both orientations) and 1,878 search evaluations to n = 56.
- Positive π-cycles **do** exist in the frame class from n = 37, and the search can grow their mass, reaching 40 at n = 53 with w up to 8. So "no positive cycles" is false in the frame class and cannot serve as a lemma; a proof of the floor has to be a balance statement.
- The balance is not close in the data. The classes that host positive cycles are single giant classes with slack 0.16–0.22 and positive/negative weight ratio ≤ 4.1e-4. The min slack over non-equality classes is flat at about 0.10–0.15 out to n = 56 and does not trend to 0.
- There is a new exact-equality shape: (16, 4) classes at n = 44, 46 and 54, at holes with link 66667, built from four task-2 blocks. Conjecture E should now read "N ∈ {4, 8, 16} seen".

Files: `posw/scan-census.jsonl`, `posw/scan-walk.jsonl`, `posw/search.jsonl` + `search.log` (run 1), `posw/search2.jsonl` + `search2.log` + `seeds2.json` + `run2.sh` (run 2), `posw/best-by-n.json`, `posw/verify-batch*.json(l)/.log`. All runs have finished; nothing is still running (7 Oct, 18:40).

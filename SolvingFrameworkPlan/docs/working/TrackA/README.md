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

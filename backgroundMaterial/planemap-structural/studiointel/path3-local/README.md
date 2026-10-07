# Path 3 on the MacBook: stuck-class search, v3 objective plus targeted flips [exploratory]

Local intel, the MacBook stand-in for Studio intel, 6 October 2026. Directed by the coordinator. Nothing here changes a status word.

A **stuck class** is a Kempe class of T − v (T in the core class: min degree ≥ 5, no separating triangle; v a degree-5 hole) that contains no filled state. It is a counterexample to R\* at v.

## Files

| file | what it is |
|---|---|
| `lib.py` | Helpers: seed loading (all repo JSON formats), engine call, faces → rotation JSON for Math's checker, core-class test. |
| `kempe_classes4.cpp` | The engine `../fast/kempe_classes3.cpp` with its class computation unchanged, plus three outputs: (a) `flips`, targeted-flip counts for the target class; (b) `sig`, Intern C's one-fill signature; (c) a full dump of any class with no filled state. Build: `clang++ -O3 -std=c++17 -o kempe_classes4 kempe_classes4.cpp`. Also build `kempe_classes3` from `../fast/`. Binaries are gitignored. |
| `test_math.py` | Tests Math's builders and independent checker (`SolvingFrameworkPlan/docs/working/MathPath3-scripts/`). |
| `kc_search_local.py` | The v3 search (same score and tabu walk as `../path3/kc_search3.py`), plus targeted flips, the signature log, and certificate, replay and stop. |
| `run1.sh`, `run1b.sh`, `run2.sh` | The exact runs, all under `nice -n 10`, with at most 6 workers at a time. |
| `summarize.py` | Aggregates the logs. Output is in `summary-run1.jsonl` and `summary-run2.jsonl`. |
| `seeds/` | Builder instances used as seeds: RAK_a13_b1_s2, RAK_a17_b1_s2, RAK_a19_b1_s2, FL_n12, SL_rings8-9-9, TU_n8_L4, CC_R2_tw1. |
| `build/*.jsonl` | Builder summaries (core, ak and heavy presets) and `test_math.jsonl`. The instance directories are regenerable and gitignored. |
| `run1/`, `run2/` | Logs (`log-*.jsonl.gz`, one JSON line per evaluated graph), `best-*.json`, and the `.out.gz` files. `cert/` and `sigviol/` stayed empty, so git does not show them. |

## 1. Engine check (task 1)

- I compiled `../fast/kempe_classes3.cpp` with `clang++ -O3`.
- On HoG 1152 (`longtable/historical-traps/hog1152-heawood-four-color-graph.json`), **κ(T − v) = 3 at 16 holes and 4 at 1 hole (vertex 16)**, as expected.
- At hole 16 the class of size 288 has 72 filled states (fraction 0.25, far 2), matching v3.

## 2. Math's builders and checker (task 2)

**Builders.** `path3_build.py` runs unchanged with the core, ak and heavy presets.
- All 104 core-preset instances were re-validated by `studiointel/graphs.py`. Each is a sphere triangulation, and the builder's min-degree and separating-triangle counts agree with the re-validation. 49 of the 104 are core-class.
- The only skip is RAK(1,1,0), where two degree-3 vertices are adjacent. That skip is correct.

**Gates.**
- G1: FL_n5 and CC_R1_tw0 are the icosahedron (n = 12, 120 automorphisms, one orbit).
- G2: κ(FL_12) = 3 (Florek's bound is ≥ 2).
- G3: the core RAKs have κ(T) ≥ 2. RAK_a7_b1_s2 is the icosahedron, with κ(T) = 10: all 10 colourings are frozen singletons. The n = 20 RAKs have κ(T) = 21, and RAK_a13_b1_s2 has κ(T) = 3.

**AK convention.** Math's AK(a,1,s) frozen test agrees with Florek's Thm 1.3 criterion, gcd(s,n) = gcd(s+1,n) = 1, on all 496 instances with a < 32. So Math's s is Florek's S⁺ for b = 1.

**Core RAKs by order:** 12:2, 20:6, 24:8, 32:12, 36:14, 40:2, 44:18, 48:12, 52:6, 56:24, 60:26. The other RAKs have a degree-4 vertex.

**Checker.** `path3_kclasses.py` agrees with the engine exactly on the multiset of (class size, #filled) and on the state count at every hole tested, 51 holes in all:
- all 17 HoG 1152 holes;
- orbit representatives of FL 5–12, TU, RAK, CF_R2_E1, CC and SL_rings8-9-9.

Its whole-class extras: `new_classes = 0` everywhere, and `consistency_hit_iff_filled = true` everywhere. κ(T) for HoG 1152 is 37.

**No bug fixes were needed. I did not edit Math's files.** One limitation: FL_n, CF_R2_\* and SL with a pole of degree ≥ 10 have **no legal flip** in the core class with max degree 9. FL_n12 has none at any max degree, because every belt vertex has degree 5. They are seeds for evaluation, not for a flip walk. `run_path3.py` was not tested: it needs kmap and kreach, which are not built here.

## 3. Search (task 3)

**Score (v3).** The search minimises the lowest filled fraction among classes of size ≥ 40 over all degree-5 holes, with far and max κ as tie-breaks.

**Each step** evaluates up to 4 targeted flips, then random flips up to 8 candidates. Every candidate is evaluated in full at every degree-5 hole.

**Targeted flip (Math 16:45, item 3).**
- For the target class R and each flip ab → cd that avoids the hole, the engine counts the filled and unfilled states of R with col(c) = col(d). The flip deletes exactly those states.
- Candidates are ranked by the filled fraction of R's survivors (survivors ≥ 40).
- Legality: min degree ≥ 5, max degree ≤ 9 (12 for FL), no separating triangle.

### Runs

**Run limits.** Round 1 was 6 workers × 20 min. FL_n12 had no legal flip and stopped at once, so `run1b.sh` gave its core to SL_rings8-9-9 for 18 min. Round 2 was 6 workers × 15 min. Total use was about 3.5 CPU-hours, with no process left running.

**Totals.** The two rounds evaluated **111,478 graphs**, each at every degree-5 hole.

| run | n | seed's lowest large class (frac, size, filled, DL) | lowest reached (frac, size, filled, DL, hole, graph sha16) | evals |
|---|---|---|---|---|
| hog1152 | 25 | 0.25, 64, 16, 16 | 0.25, 432, 108, 132, h5, 7bc01402aaabc6f0 | 15715 |
| heawood1890 | 25 | 0.375, 480, 180, 84 | 0.25, 432, 108, 132, h0, 7c8bcfd93b4a4ea3 | 15861 |
| r5_80b930d1 | 32 | 0.359, 6474, 2326, 1259 | 0.25, 4224, 1056, 1056, h4, 5f568a5453449c58 | 4627 |
| r5_91a307d1 | 28 | 0.359, 1361, 489, 280 | 0.25, 1632, 408, 408, h12, 36c21b52f68d6601 | 10403 |
| RAK_a13_b1_s2 | 24 | 0.548, 859, 471, 65 | 0.25, 384, 96, 112, h9, 4cb1cb3d3a411883 | 17587 |
| FL_n12 | 26 | 0.454, 1348, 612, 147 | no legal flip | 1 |
| SL_rings8-9-9 | 28 | 0.431, 2225, 960, 304 | 0.25, 1632, 408, 408, h16, 9af02036c9a41e8b | 9380 |
| K3_26_5401 | 26 | 0.395, 1190, 470, 201 | 0.25, 384, 96, 132, h1, 5dde69f0c00ba020 | 12831 |
| RAK_a17_b1_s2 | 32 | 0.492, 10697, 5263, 1288 | 0.25, 7776, 1944, 2508, h3, 3dd385be4c3498d5 | 3936 |
| RAK_a19_b1_s2 | 36 | 0.475, 39092, 18548, 5037 | 0.25, 1808, 452, 452, h23, 1b0c57da860df385 | 1221 |
| TU_n8_L4 | 34 | 0.517, 12448, 6432, 1133 | 0.25, 4608, 1152, 1152, h9, 44bb0bc5bfd9ec12 | 2172 |
| CC_R2_tw1 | 32 | 0.491, 4590, 2255, 426 | 0.25, 3168, 792, 792, h6, cdbcf47fca210556 | 4054 |
| hog1152_randomonly (KT = 0) | 25 | 0.25, 64, 16, 16 | 0.25, 432, 108, 132, h7, db2e8ff8251b50e1 | 13690 |

### Findings

1. **No stuck class.** `cert/` is empty in both rounds. No class of T − v with zero filled states occurred at any hole of any evaluated graph.

2. **The best (lowest) filled fraction among large classes is exactly 0.25, and it is a hard floor in these walks.**
   - Every seed that could move reached exactly 1/4.
   - No graph had a class of size ≥ 40 below 1/4.
   - The class compositions at 1/4 are typically (48,12,12), (96,24,24), (64,16,16), (192,48,48), (384,96,132), (576,144,144) and so on, up to (7776,1944,2508). Most have #DL = #filled.
   - Over **all** classes of any size, at all holes of the 141 v2 one-fill graphs and the 6 round-1 best graphs (3014 classes), the minimum fraction is also 1/4, attained by the (4,1,1) one-fill classes.
   - So the v3 objective has saturated.
   - **Conjecture for Math [empirical only]: in every Kempe class of T − v at a degree-5 hole, at least 1/4 of the states are filled.** That would rule out stuck classes outright. The (4,1,1) classes and the 1:2:1 filled : non-DL : DL pattern of (1632,408,408) are the cases to explain.

3. **Targeted flips (Math 16:45, item 3) did not beat random flips.**
   - First time each run reached 0.25: 5 runs by a random flip, 4 by a targeted flip, and HoG 1152 already at the seed. Random-only HoG reached the same plateau.
   - Targeted flips were accepted more often (about 2:1 in round 1), because a flip that deletes most of the filled states of R often keeps the score.
   - The deleted states are replaced. After the flip the survivors re-merge with new states (col(a) = col(b)) and the fraction returns to ≥ 1/4. This is Intern C's caveat on 3(i), seen in data.

4. **Intern C's signature holds.**
   - One-fill classes: 26,222 seen during the search, plus 241 at the 141 v2 graphs.
   - Bichromatic components of f missing the link: **0 in every case**. `sigviol/` is empty.
   - So the engine passes the sanity filter.

5. **Parity (Math P1).** In T − v the odd-parity vector O does change inside a class. For example, the single class at the icosahedron hole shows all four O-vectors (`build/test_math.jsonl`).

**Suggested next step.** Replace the fraction objective with a structural one at the 1/4 floor: maximise far, or the DL share, among classes at exactly 1/4. Or prove the 1/4 bound.

## Caveats

- These are heuristic local searches from a handful of seeds. Absence of a stuck class here is evidence of nothing beyond these walks.
- The 1/4 observation is empirical.
- Class counts are up to colour renaming, the same convention as v1–v3.

---

# Math C6: DL rotation chains and per-j excess (coordinator, after 18:18) [exploratory]

**Notation** follows `SolvingFrameworkPlan/docs/working/MathQuarterFloorBijections.md`:
- R+3 swaps the {α,A}-component of x_{j+2};
- Γ is the graph of R+3 edges, made of paths and cycles;
- d(P) is the number of doubly locked (DL) states inside a path;
- DD_j = {d ∈ D_j : R+3 d ∈ D_{j+3}};
- room_j = L_j + |U_j^ff| + |U_{j+3}^ff| + |E_j|;
- excess_j = |DD_j| − room_j.

By Math's per-j identity, Σ_j excess_j = U − 3F. So the floor fails in a class iff its summed excess is > 0.

| file | what it is |
|---|---|
| `kempe_dd.cpp` | Same enumeration and classes as kempe_classes3. Per class it computes F, U, N0, N1, D, L_F, Γ paths and cycles, max d(P), D_cyc, max cycle length, DD_j and room_j. It also runs Math's checks on every class and state: C1 (the class identity and the per-j identity) and C2 (the M2 and M3 dichotomies, "R+3 defined ⇔ lock 2", "R+2 defined ⇔ lock 1", and "R+3 image has lock 1, lies at index j+3, in the same class"). A class with 3F < U is dumped in full. |
| `kc_dd_search.py` | Tabu walk over random legal core flips, scoring every class at every degree-5 hole. Mode `exc` scores by (#classes below 1/4, max excess_j, max chain, −min fraction among classes with chain ≥ 2). Mode `chain` swaps the second and third keys. A class below 1/4 triggers a certificate, a replay by Math's `path3_kclasses.py`, and a stop. |
| `run_dd.sh` | The run: 6 workers × 25 min under nice 10, about 2.5 CPU-hours. |
| `summarize_dd.py`, `summary-run_dd.jsonl` | Per-run maxima. |
| `run_dd/` | Logs (gz) and the best graph of each run (`best-*.json`, with faces). |

**Seeds.** A_5, A_6, A_7 (from `graphs.A_r`; A_3, A_4 and A_5 reproduce MathConjectureR's 100/40/30, 520/200/80 and 2720/1040/530), K3_26_5401, r5_80b930d1 and HoG 1152.

**Totals.** 95,884 core graphs, each evaluated in full at every degree-5 hole.

## Results

1. **No class below 1/4.** No class had F = 0, and `cert/` was never created.

2. **Math's identities and dichotomies: 0 failures.**
   - The C1 class identity and the per-j identity held, as did every C2 dichotomy and the R+3 image checks.
   - They were checked on every class of every hole of all 95,884 graphs, and on the HoG 1152 and A_3–A_5 seeds.

3. **Maximum excess_j = 0. No class at any j of any graph had |DD_j| > room_j.**
   - This is Math's addendum target, holding per j everywhere in this run.
   - Equality with DD_j > 0 occurs: HoG 1152, hole 16, class (288, 72 filled) has DD = (36,0,36,0,0) = room, with max d(P) = 3.
   - Most graphs reach excess 0 only through the floor quartets (4,1,1), where DD = room = 0.

4. **Long DL rotation chains exist in the core class, and they are paid for.**
   - The longest chains are all-DL Γ-cycles. Each cycle length is ≡ 0 mod 5 (Theorem A).
   - A_r seeds have 20-cycles. Flips grow them to **880** (A7_exc log, graph 5ae8d6ecb01cd81c; faces not saved) and **800** (`run_dd/best-A7_exc.json`, hole 22). The 800-cycle sits in a class with size 21078, F = 8922 (fraction 0.423), D_cyc = 840, DD = (726,642,648,690,624) and room = (3648,3564,3570,3612,3546).
   - Other maxima:
     - 660 (A6_chain best, hole 31, class 12820 at 0.398);
     - 223 (r5 run) and 60 (HoG run);
     - max path interior d(P) = 93 (A6 best);
     - max |DD_j| = 1544 and max Σ_j DD_j = 7058 (A7 run).
   - The longest chains sit in classes with large N0 and L_F. Room grows faster than DD.

5. **Minimum filled fraction among classes with chain ≥ 2 is exactly 1/4**, as in the HoG 288-class (d = 3) and in each run. It was never below.

**Caveat.** These are heuristic walks. Positive excess_j at some j is allowed by the floor, as long as the class sum stays ≤ 0. None was seen.

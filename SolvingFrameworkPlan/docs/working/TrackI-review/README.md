# Track I review: chain-parity law and rigid isolation [independent adversarial review]

Reviewer: an independent agent, 7–8 Oct 2026. I did not write any of Track I. I read `TrackI/RigidIsolation.md`, `TrackI/README.md`, `TrackH/README.md` (H3–H5, §6), `TrackF/LockParity.md` and the latest `CoordinatorPlan.md` log. All code here was written from scratch. Nothing is imported from TrackI, TrackH or TrackF; only the definitions were taken from the documents. Nothing was committed, and nothing outside this directory was modified. Compute: at most 2 worker processes, all under `nice -n 10`, about 1 h of wall time.

## Verdict

**The proof of Theorem 6 (chain-parity law) and of rigid isolation (RI) on the sphere is correct.** I found no wrong step and no counterexample.

The gaps are expository. Each is a missing sentence or a mislabelled planarity accounting, and each has a one-paragraph fix (§2). None of them changes a statement.

- Theorem 6: 0 failures in **2,224,936** DL states of fresh sphere triangulations (table, §3).
- Every intermediate identity of the proof (Lemmas 0, 1, 2, 4a–d, P-i, P-ii, L1–L4, the conclusion of Lemma R, Lemma 5) was checked separately on **2,207,592** of them, with 0 failures.
- Off the sphere, everything fails as expected. One correction to Track I's account of *where* it fails is in §4.

## 1. Step-by-step verdicts

| step | verdict | notes |
|---|---|---|
| Setup: G = T\*/h\*, v of degree 5, no loops, faces ↔ V(T)−h, edges ↔ E(T−h), v-colours (1,1,2,1,3) | **CORRECT** | Two h-faces f_t, f_s share an edge only if they are consecutive, and that edge is a P-edge, so contraction creates no loop. Multi-edges e_t ∥ e_{t+1} occur exactly when deg_T x_{t+1} ≤ 4. They are possible for t = 1, 2, 3, 4 but impossible for t = 0, because x₀x₂ would be an α–α edge. The proof never assumes simplicity of G. |
| Lemma 0 (v-loops simple, non-crossing on S²) | **CORRECT** | Standard Jordan argument. |
| Lemma 1 (regions = chains; N = 5 + k(H) + k(F12) + k(F13)) | **CORRECT** | The bijection holds on any surface. Every vertex of G has degree ≥ 2 in each S_i, so regions are unions of open faces glued along colour-i edges. Euler for plane multigraphs is the planar step. The formula N = 5 + Σk is frame-independent, since Σ_i \|E(S_i)\| = 2\|E(G)\| = 3\|V(G)\| + 2. |
| Lemma 2 (locks = pairings) | **CORRECT** | In the first case, the "other loop touches only at v" remark is unnecessary: one side of the loop through e₀, e₁ already separates the two corners. |
| Lemma 3 (N ≥ 8, rigid ⇔ N = 8 ⇔ all k = 1; F13 = X ∪ Y) | **CORRECT** | Theorem D is used here and is a sphere input (see G3). |
| Lemma 4(a) (π = 1↔3 on C = ∂R) | **CORRECT** | A neighbour of K outside K that is not h has colour μ or B, so boundary colours change by 2 and 1 ↔ 3. |
| Lemma 4(b) (C = X ∪ Z₁ … Z_r; = X if rigid) | **CORRECT**, with G1 | The local argument (degree 0 or 2 at cubic vertices, corners at v, x₀ ∉ K) is right. Lemma 2 makes X return through e₃. The global topology that Lemma R needs (each Z_i and X bounds a disc on the far side) is asserted, not proved: see G1. |
| Lemma 4(c) (H′ = F12ΔC, F12′ = F13, F13′ = HΔC; 1′=3, 2′=1, 3′=2; e′_t = e_{t+3}) | **CORRECT** | Checked by substitution and in the data (`L4a`, `L4c_N`). |
| Lemma 4(d) (π(c) always has Lock1; π(c) DL ⇔ p(HΔC) = (e₁e₄)(e₂e₃)) | **CORRECT** | |
| Lemma R, step 1 (flips connect non-crossing matchings) | **CORRECT**, with G2 | The induction is right once (s, s′) is chosen as an *innermost pair of the target matching*. The text only says "consecutive". The band-surgery result is the non-crossing pairing (ss′)(qr), not (sr)(s′q), because γ lies in a disc face. |
| Lemma R, step 2 (band surgery ±1 on S²) | **CORRECT** | Different curves merge (−1) on any surface. On the same curve, γ is a cross-cut of one Schoenflies disc of σ and splits it (+1). **This is a genuine planar step** (G3, §4): on RP² it fails even when the outer matchings are non-crossing. |
| Lemma R, step 3 (one flip acts on both systems) | **CORRECT** | Σ_I must be a family of *disjoint arcs in R*. The hypothesis is stated and the application satisfies it: the colour-2 edges in R form part of a plane graph. My data show it is needed (§3a). |
| Points, B₁/B₃, splitting v into a, b, virtual arc ba | **CORRECT** | X has odd length 2p+1 with p ≥ 1: length 2 would put two colour-1 edges at a vertex. The placement "e₂ at a, o at b" is legitimate: e₂ is the only v-edge on the R-side, and o is the only O-edge used per family, on the D₀-side. So any placement along the blown-up arc of X at v is isotopic. Degenerate cases also work: e₂ ∥ e₁ (deg x₂ = 3) gives a 2-cycle in B₁ ∪ Σ, and e₂ may end on a Z_i rather than on X. |
| I/O labels equal for both families | **CORRECT** | t_w ∈ M₂ ⊆ H ∩ F12. a is I in both families (e₂). b is O in both families (e₀ and e₄ both lie in D₀). |
| (P-i) the I-parts coincide | **CORRECT** | R contains no vertex, because every vertex is on F13. |
| (P-ii) the O-parts are non-crossing | **CORRECT** given G1 | The far side D_i is a closed disc, and vertex-disjoint paths in it give a non-crossing matching. Only b is O at v, so the cyclic order is well defined. |
| (L1)–(L4) | **CORRECT** | (L2) and (L4): smoothing (e₁e₂)(e₃·) adds one curve iff it agrees with the pairing. That holds for both non-crossing pairings, and also for the crossing one (where it adds 0). f_S counts the S-cycles avoiding C ∪ {v}, and it is the same for S and SΔC. |
| Conclusion of Lemma 5 | **CORRECT** | Uses Lemma 0 for HΔC (non-crossing) to convert [(e₁e₂)(e₃e₄)] into 1 − [(e₁e₄)(e₂e₃)]. |
| Theorem 6 from Lemma 5 | **CORRECT** | |
| Theorem RI | **CORRECT** | Rigid ⇒ DL (H4). N(πc) = 8 = N(c) contradicts Theorem 6. |
| §0, "planarity enters in exactly four places" | **GAP (accounting)**, G3 | The list omits Lemma R step 2 (Schoenflies), the disc structure of S² − C (G1), Euler's formula inside Lemma 1, and Theorem D (Lemmas 3 and 4b). |
| README §0.5 / §4, "the single failing step [on RP²] is (P-ii)" | **TRUE ONLY for the 36 rigid→rigid steps** | See §4: on general RP² DL states, Lemma R's conclusion also fails with non-crossing outer matchings; on the torus, failures go through Lemma 2/Lemma 1 while Lemma R's conclusion never fails. |
| Remark 7 (link-free swaps preserve N + L1 + L2) | **UNPROVED** (labelled [hand], but no proof is written) | Data: 0 failures in 19,448 link-free moves on fresh spheres (N parity alone changes in 8,024). A proof along the lines of Lemma 5 looks feasible: ∂R′ is a union of S_i-cycles avoiding v, and v becomes an off-C degree-4 vertex in two subgraphs. It should be written before §4.3 of the README relies on it. |

## 2. Gaps and suggested fixes

**G1 (topology of S² − C; Lemma 4b → Lemma R).**

*Problem.* Lemma R assumes that the components of C bound pairwise disjoint discs D_i on the side away from R. Lemma 4(b) proves only that C is a union of disjoint simple closed curves. The step that links the two is not written.

*Fix (one paragraph):*
- R is a connected component of S² − C. It is open and connected with frontier inside C, so it is closed in S² − C.
- Every C_i lies in the frontier of R, because each C-edge separates an R-face from a non-R face.
- r+1 disjoint circles on S² cut it into r+2 regions, whose adjacency graph is a tree (Jordan).
- R is adjacent to all r+1 circles, so the tree is a star centred at R.
- Each other region is therefore adjacent to exactly one C_i, and it is a disc by Schoenflies.
- D₀, the region beyond X, is the one containing the corners (e₃,e₄), (e₄,e₀) and (e₀,e₁), so it contains e₀, e₄ and Y.

**G2 (flip connectivity, wording).** Choose (s, s′) to be a pair of the *target* matching M′ that is consecutive among the O-points (an innermost arc of M′). Flip M until it contains (s s′), then delete s and s′ and induct. The nesting remark in the proof then covers the realisation.

**G3 (planarity accounting).** Replace "exactly four places" with a list of all of them:
- Lemma 0 (Jordan);
- Lemma 1 (Euler on S²);
- Lemma 2 (Jordan);
- Theorem D (Lemma 3; Lemma 4b's x₀ ∉ K, which also follows from Lemma 2 because X separates corner (e₁,e₂) from corner (e₄,e₀));
- G1 (Jordan–Schoenflies for S² − C);
- (P-ii) (disc ⇒ non-crossing);
- Lemma R step 2 (Schoenflies ⇒ a same-curve band splits).

The data (§4) show that the last of these is used non-trivially. It is not implied by (P-ii) holding combinatorially.

No GAP affects correctness on the sphere; all three are routine to write.

## 3. Independent data

### 3a. Lemma R, exhaustive (`ri_lemmaR.py`, `out/lemmaR.log`)

Model: circles with points in cyclic order and the two alternating matchings B₁, B₃. Every I/O labelling is enumerated, every Σ_I realisable in R, and every Σ_O.

Σ_I realisability for 2 or more circles is tested by planarity of (circle-wheels + Σ_I). For 2 circles it is cross-checked against an annulus cut test: 0 disagreements.

| configuration | (labelling, Σ_I) configs | parity varies with Σ_O |
|---|---|---|
| 1 circle, 2–12 points, Σ_I planar, Σ_O non-crossing | 2 + 9 + 51 + 323 + 2,188 + 15,511 = 18,084 (63,042 Σ_O evaluations) | **0** |
| 2 circles, (2,2) … (6,6) (total ≤ 12), Σ_I planar in the annulus | 6 + 38 + 282 + 289 + 2,427 + 22,341 = 25,383 | **0** |
| 3–4 circles: (2,2,2), (2,2,4), (2,4,4), (2,2,2,2) | 28 + 230 + 2,122 + 188 = 2,568 | **0** |
| **crossing Σ_O allowed**, 1 circle, 4 / 6 / 8 points | 9 / 51 / 323 | **1 / 13 / 125** (fails from 4 points, as Track I says) |
| crossing Σ_O allowed, 2 circles (2,4) / (4,4) | 38 / 289 | 2 / 17 |
| **crossing Σ_I allowed** (Σ_O non-crossing), 1 circle, 4 / 6 / 8 points | 10 / 76 / 764 | 0 / 0 / **28** |

The last row is new. Lemma R also needs Σ_I to be planar; with a crossing Σ_I it first fails at 8 points. Lemma R states this hypothesis ("disjoint arcs in R") and the application satisfies it, so this is not a gap. It does mean planarity is used on the R side too.

### 3b. Theorem 6 on fresh spheres (`ri_run.py`, `ri_core.py`)

Theorem 6 is tested from the primal only: the six pair graphs of T − h, π as the swap of K_{αA}(x_{j+2}), and DL from Lock1/Lock2 by reachability. The step checks (`ri_tait.py`) build G = T\*/h\* independently from the face list and test every intermediate claim, including (L1)–(L4) and the conclusion of Lemma R on the explicit point model (B₁, B₃, virtual arc ba, N^H, N^F).

Colourings come from full enumeration up to renaming when n ≤ 27 (capped at 150k). For n ≥ 28 they come from Kempe-walk samples of 2,500 states per hole with restarts.

| source | graphs | holes | DL states (Theorem 6 tested) | DL→DL (ΔN odd) | DL→non-DL (ΔN even) | with holes (C ≠ X) | rigid | Theorem 6 failures | step-check states / failures |
|---|---|---|---|---|---|---|---|---|---|
| random spheres, min degree 5, n = 14–40 (`sphere5`) | 296 | 5,096 | 853,290 | 181,705 / 181,705 | 671,585 / 671,585 | 332,657 | 4,583 | **0** | 846,162 / **0** |
| random spheres, min degree 3, n = 8–30 (`sphere3`, `sphere3b`): link vertices of degree 3–4, i.e. multi-edges at v | 1,900 | 6,462 | 33,338 + 130,455 = 163,793 (143,362 at holes with a degree ≤ 4 link vertex) | all odd | all even | 51,407 | 1,435 | **0** | 155,279 / **0** |
| Census29 `frame-22..32.txt`, random sample of 288 of 21,931 (`census`) | 288 | 4,733 | 1,207,853 | 284,119 / 284,119 | 923,734 / 923,734 | 391,923 | 6,650 | **0** | 1,206,151 / **0** |

Additional checks:
- **RI**: 0 rigid → rigid among all 12,668 rigid sphere states.
- Rigid ⇔ N = 8 had 0 exceptions, and N < 8 never occurred, across all sphere runs.
- Theorem D (π defined at every DL state) held on all of them.
- No step-check assertion fired, so the model was always constructible: C has v-degree 2, X closes at e₃, every point carries one end, and the paths pair the points.

### 3c. Off the sphere (`rp2`, `rp2b`, `rp2c`, `torus`, `torusc`)

Base triangulations: the 6-vertex RP² (hemi-icosahedron) and the 3×4 torus grid, grown by stellar insertions and random flips (half of them pushed to min degree 5), n = 12–26, with full enumeration.

| surface | DL states with π defined | Theorem 6 failures | Lemma 5 failures | RI failures (rigid → rigid) | DL states where π is undefined (Theorem D fails) |
|---|---|---|---|---|---|
| RP² (1,400 graphs) | 11,048 + 32,385 + 30,461 = 73,894 | 4,755 + 13,955 + 12,117 = **30,827** | 3,829 + 11,671 + 10,624 = 26,124 | 29 + 54 + 64 = **147** | many |
| torus (800 graphs) | 3,106 + 6,503 = 9,609 | 1,506 + 3,123 = **4,629** | 640 + 1,565 = 2,205 | 4 + 12 = **16** | many |

So Theorem 6 and RI genuinely fail off the sphere. The torus has rigid → rigid steps too, which agrees with the TrackH review's correction of "torus 0".

### 3d. Remark 7 (`ri_remark7.py`, `out/remark7.json`)

- 39 random min-degree-5 spheres (n = 14–24), 3 holes each, every unfilled state, every link-free Kempe component: **19,448 moves, 0 failures** of N + L1 + L2 (mod 2).
- N alone changes parity in 8,024 of them.
- In the 1,838 moves from DL to DL, N never changes parity.

## 4. Where the proof breaks off the sphere (correction to Track I's narrative)

Joint statistics per DL state (`joint_*` keys in `out/rp2c.json`, `out/torusc.json`):

| | outer matchings bad (crossing or leaving the circle) | ... and Lemma R conclusion fails | outer matchings non-crossing on one circle, but Lemma R conclusion fails | Lemma 5 fails with (P-ii) fine |
|---|---|---|---|---|
| RP² (`rp2c`, 30,461 states) | 18,060 | 7,529 | **2,857** | 2,940 |
| torus (`torusc`, 6,503 states) | 4,799 | **0** | **0** | 366 |

Two consequences:
- **RP².** Lemma R's conclusion can fail even when the end-matchings are combinatorially non-crossing on each circle, in 2,857 states. There the far side is not a disc, or a curve σ through R is one-sided, so a same-curve band does not split. Lemma R step 2 and G1 are independent planar inputs, not consequences of (P-ii).
- **Torus.** Lemma R's conclusion *never* fails, even though (P-ii) fails in 4,799 states: all curves are two-sided, and the parity survives. Every Lemma 5 failure there comes from Lemma 2 (lock ≠ pairing, 640 + 1,565) and the Lemma 1 dictionary (Euler).

Track I's statement that on RP² rigid → rigid "the single failing step is (P-ii)" may be true for those 36 particular steps; I did not re-check them individually. It is not the general picture. This changes nothing on the sphere, but it matters for anyone trying to transplant the argument: on orientable surfaces the switching parity seems robust, and the loss is in the lock ↔ pairing dictionary.

## 5. Files

| file | content |
|---|---|
| `ri_core.py` | simplicial surfaces (faces; flips, stellar insertion; RP², torus, sphere generators; Census29 rotation parser), colouring enumeration and Kempe-walk sampling, hole state, locks, π, N |
| `ri_tait.py` | independent Tait graph G = T\*/h\* and the per-state checks of every lemma, including the explicit point model of Lemma R |
| `ri_run.py` | driver (Theorem 6 from the primal, RI, rigid ⇔ N = 8, step checks, joint failure statistics) |
| `ri_lemmaR.py` | exhaustive Lemma R, including its failure for crossing Σ_O and crossing Σ_I |
| `ri_remark7.py` | data check of Remark 7 |
| `run_all.sh` | the first batch of runs (2 workers, nice'd) |
| `out/*.json`, `out/*.log` | raw counters per run |

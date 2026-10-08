# Track N: Q-e, does NRC survive Lemma E's sphere constants plus the chain-parity law in general graphs? [data] + [hand, unreviewed]

Studio, 8 Oct 2026 (02:25–04:30). Nothing outside `TrackN/` was changed and nothing was committed. TrackJ's `tj_eng.c` was copied here and extended (`tn_eng.c`). TrackH `th_engine.py` and TrackI `ti_chains.py` are imported read-only, by the second engine only.

Compute: at most 4 worker processes under `nice -n 10`, apart from short single-process ILP debugging runs. Machine load from other users was 15–30. About 2.4M graph evaluations by the annealer, plus about 450 exact or heuristic surgery problems.

Labels:
- **[data]**: computation.
- **[hand, unreviewed]**: short arguments written here and not reviewed.

## 0. Answer to Q-e

**No example was found under any constraint set that includes Lemma E's sphere constants (2,3,3) at the cycle states.** Without those constants, examples are plentiful. Constraint sets tested:
- (2,3,3) only;
- (2,3,3) + the chain-parity law;
- either of these, plus the class-wide version, the edge count, or triangles.

Those later additions are all moot, because already the weakest version (2,3,3) on the cycle states has no example. The edge count |E(G − h)| = 3n − 11 is not an extra condition: it is implied by (2,3,3) at any single state (§1).

| constraint set (on a π-cycle of DL states with N ≤ 9) | examples | how close the searches got |
|---|---|---|
| none (TrackJ rung a) | 937 TrackJ graphs; 34 new from my annealer (sphere, RP², torus/Klein seeds) | – |
| law (TrackJ rungs b–d) | TrackJ: 325 (c), 411k (d1), 4 (d2), 43 (d). Mine: 0 exact; best near-misses were cycles with one N = 10 state, e.g. `989a989898` | – |
| (2,3,3) at every cycle state, no law | **0** | Exact surgery on 319 known R-cycles: the minimum Lemma E deviation is ≥ 1.4 per state (200 rung-a cycles), ≥ 2 per state (34 annealer cycles) and ≥ 3 per state (85 law cycles) |
| (2,3,3) + law (Q-e, cycle version) | **0** | Every law cycle has a minimal skeleton with exactly **+3 edges (3n − 8 in G − h, the RP² count)**, never fewer; see below |
| (2,3,3) + law at every state of the Kempe class | 0 | (implied by the row above) |
| + edge count, + every edge in a triangle | 0 | (implied by the row above) |

How close each search got:
- **Exact surgery (ILP).** For 85 law-respecting R-cycles, I optimised exactly over all edge deletions that keep the cycle alive. The minimal skeleton always has |E(G − h)| ≥ 3n − 8: 3 edges above the sphere value, which is exactly the RP² count. In 75 of the 85 it is exactly 3n − 8, and in the other 10 it is 3n − 7 to 3n − 5.
  - At the optimum the deviation is 3 per state, spread as (1,1,1), (0,2,1), (2,1,0), … over the three partitions.
  - Allowing edge additions as well (random local search, 97 cycles) never went below +3.
- **Annealing towards Q-e.**
  - From sphere seeds (sphere max run 7), the longest π-run with (2,3,3) + law at every state is **7**, reached in a non-planar graph. That equals the sphere maximum and does not beat it.
  - Seeded from the reduced cycles, the closest object is a non-planar graph with |E(G − h)| = 3n − 11 carrying an all-DL π-10-cycle with (2,3,3) at all 10 states. Its N-profile is `999aba98ab` (excess 7), and the law fails at 4 steps. Verified by both engines.
- **Control without (2,3,3).** The same annealer found law-respecting runs of length 10 inside R (window penalty 0, not closing), and near-cycles with total penalty 1 (one N = 10 state), in non-planar graphs with about 10 edges above 3n − 11.

**What this means for the proof type.** All of the following point towards "Euler + combinatorics might suffice", rather than "Jordan input is needed":
- the robust null;
- examples are easy when (2,3,3) is dropped;
- a sharp, reproducible gap: every law cycle needs at least 3 more edges than the sphere allows.

Strength of the evidence:
- **Moderate, not decisive.** All law-respecting cycles available for exact surgery come from one lineage: TrackJ's rung-c walk, seeded from the RP² test bed `rp2_s203_w16_t134`. The +3 may be partly a fingerprint of that RP² origin.
- The 34 law-failing R-cycles come from diverse origins (sphere, RP², torus and Klein seeds). None reaches (2,3,3) either: their minimum deviation is 2 per state.
- Surgery that preserves partitions is a restricted move set. My annealer, which is not restricted, also found nothing, but my control search did not reproduce law cycles from scratch.

**A by-product [hand, unreviewed; 3 lines].** Rigid isolation (RI) is already **Euler-level**: Lemma E at u and at π(u), plus TrackL's star identity St, rule out 8 → 8 in any graph (§2). On the other hand, the same Euler-level data allow 9 → 9 steps (16 consistent patterns), so the chain-parity law is not implied by Lemma E. The near-rigid 8/9 alternation is consistent at that level, as TrackL §2.1 says.

## 1. Setup and the equivalences used [hand]

Notation:
- G is any graph; h = 0 has degree 5 and its link 1..5 is an induced 5-cycle.
- nv = n − 1 = |V(G − h)|.
- For a state s, E_k(s) is the number of edges of G − h whose colour pair lies in partition k.
- Σχ_k = nv − E_k (TrackL Lemma E: Σχ_k = c_k − β_k).

Facts:
- **(2,3,3) at an unfilled state** ⇔ E₁ = n − 3, E₂ = E₃ = n − 4. So it implies |E(G − h)| = 3n − 11. The edge-count rung of the brief is therefore automatic once (2,3,3) holds at any one state.
- **General form, used for the class-wide variant** (it also covers filled states): E_m = nv − 1 − (5 − ℓ_m)/2, where ℓ_m is the number of link edges in matching m. The engine's per-state deviation is `dev = Σ_m |E_m − target_m|`.
- **Under (2,3,3):**
  - N = Σc = 8 + Σβ (total cycle rank of the six pair graphs);
  - N ≤ 9 ⇔ Σβ ≤ 1;
  - rigid ⇔ all six pair graphs are forests;
  - a 9-state has its single cycle in the same partition as its extra chain.

**Partition-preserving surgery lemma [hand, any graph].** Let C be a π-cycle of DL states. Suppose G′ arises from G by deleting edges of G − h (never link edges), or by adding non-edges that are properly coloured at every s ∈ C, in such a way that at every s ∈ C every pair graph keeps exactly the same vertex partition into components. Then:
- every s ∈ C is still a proper colouring;
- L1, L2, inA, inB, the swap set K_{αA}(x_{j+2}) and hence π, and also N(s), DL-ness and the law are all unchanged.

So C is still a π-cycle of DL states with the same N-profile in G′.

*Proof.* All of these quantities are functions of the colouring and of the component vertex sets of the pair graphs. ∎

The engine confirmed the surviving cycle in all 85 + 97 + 234 surgeries: `check_cyc` = 20 or 10 every time.

So for a given cycle, "can Lemma E be reached by such surgery" is an exact optimisation problem:
- **(conn)** K contains a spanning tree of every pair-graph component at every s ∈ C;
- **(233)** |K ∩ E_m(s)| = target_m(s) for all s and m.

At rigid states, (conn) gives |K ∩ E_m| ≥ (forest size) = target_m. So at the optimum, dev/state = |K| − (3n − 11) whenever the optimum is spread evenly.

## 2. Euler-level step table [hand + enumeration, `tn_chi_steps.py`]

Unknowns per state (role order αμ, AB, αA, μB, αB, μA):
- component counts c ≥ (1,1,2,1,2,1) (link components, J1), with at most one extra;
- cycle ranks β ≥ 0;
- χ = c − β.

Constraints:
- Lemma E at both states;
- J2 transport (c′₅ = c₃, c′₆ = c₄, β′₅ = β₃, β′₆ = β₄);
- St at colours μ and B (χ′₂ + χ′₃ = χ₁ + χ₆, χ′₁ + χ′₄ = χ₂ + χ₅).

Result:
- 8 → 9: 2 patterns. 9 → 8: 2. 9 → 9: 16. **8 → 8: none.**
- Hand version of the 8 → 8 exclusion: u is rigid, so χ(αμ) = χ(μA) = 1 (trees). St at μ gives χ_c(α_cA_c) + χ_c(A_cB_c) = 2. A rigid c would need 2 + 1 = 3.
- So rigid isolation needs only Lemma E plus St; on the sphere, Lemma E is Euler counting.
- NRC does not reduce this way: 9 → 9 is allowed, so the alternation 8/9 is an extra (law) input. The alternating orbit is consistent (TrackL §2.1).

## 3. Method A: exact surgery on known R-cycles [data]

`tn_forest.py` uses scipy/HiGHS MILP with lazy connectivity cuts. Phase 1 asks for (233) exactly; phase 2 minimises Σ|dev|. `tn_flow.py` is a single-MILP flow model; it reproduced the lazy optimum (60) on the test case. `tn_addlocal.py` is a randomized local search that also adds "addable" edges (properly coloured and inside one component at every cycle state, so the partitions are kept).

| input cycles | law at all steps | surgery | min deviation (sum over the cycle / per state) | reaches (2,3,3)? |
|---|---|---|---|---|
| TrackJ rung d (43), d2 (4), c (38): 85 cycles, all J5-shaped 20-cycles `8989…` | yes | delete only, exact | 60 / **3.0** in 75; 80–120 / 4–6 in 10. Minimal skeleton \|E(G − h)\| = **3n − 8** (75) or 3n − 7 … 3n − 5 | **no** (0 / 85) |
| same lineage (43 d, 4 d2, 50 c): 97 cycles | yes | delete + add, local search, 600 rounds | excess edges 3 (43), 4 (51), 5 (3); never < 3 | **no** |
| first d example, flow MILP with all 95 addable edges | yes | delete + add, exact | inconclusive (HiGHS 120 s limit: incumbent 120 > 60) | – |
| TrackJ rung a (first 200; all-9 20-cycles) | no (law fails at all 20 steps) | delete only, exact | 28–100 / 1.4–5.0 | **no** (0 / 200) |
| my annealer's R-cycles (34; 10-cycles from sphere, RP², torus/Klein seeds) | no (2–8 failures) | delete only, exact | 20–80 / 2.0–8.0 | **no** (0 / 34) |

Facts about the minimal skeletons of the law cycles:
- They keep the closed near-rigid class: class size 20, no filled state, Kempe degrees 2/3.
- They have exactly 3n − 3 edges in G, the RP² triangulation count.
- They are not triangulations: about 15 edges lie in no triangle.
- The excess per state is distributed as (1,1,1), (0,2,1), (1,2,0), (2,1,0), … (P1 first), totalling 3 at every state, never concentrated in one partition.

Output files:
- `out/forest_del.jsonl` (and `.log`);
- `out/addlocal.jsonl`;
- `out/forest_del_rungA_nolaw.jsonl`;
- `out/forest_rcycles_nolaw.jsonl`.

## 4. Method B: annealing [data]

`tn_search.py` drives `tn_eng` (the TrackJ engine plus Track N additions).

Moves:
- edge swap (edge count preserved);
- sphere-style flip;
- toggle;
- vertex stacking and unstacking;
- **forest exchange** at a reference colouring c* from the current best window: delete a {p,q}-edge and add a {p,q}-edge reconnecting the two sides, so that every pair graph of c* keeps its component count, N(c*) and dev(c*).

Objective:
- max(20 − Win_f, 25 − P_f(best all-DL cycle)), with 30 at an example.
- P_f = Σ max(0, N − 9) + [E] Σ dev + [law] failures.
- Win_f = the same over the best window of 10 consecutive DL π-states, with 3 per missing state.

Sets: f = 1 is law; f = 2 is (2,3,3); f = 3 is both. Seeds:
- all 125 holes with sphere R-runs ≥ 6 (`out/seeds_run67.txt`), including the 8 run-7 holes and TrackL's p32.r84#686339 h23 and p24#596 h20;
- TrackJ's 202 RP² and 48 torus/Klein test beds;
- the 70 ILP-reduced law cycles (`out/seeds_reduced.txt`).

| run | f | seeds | evaluations | examples | best |
|---|---|---|---|---|---|
| `anneal_f3_sphere` | 3 | sphere run ≥ 6 | 125k | 0 | longest (2,3,3) + law run **7** (non-planar graph n = 31, \|E\| = 3n − 11; second engine agrees). Sphere max is also 7 |
| `anneal_f2_sphere` | 2 | sphere run ≥ 6 | 101k | 0 | window penalty ≥ 1, run ≤ 7 |
| `anneal_f3_reduced` (+ aborted v2) | 3, cycle-only | reduced law cycles | 84k | 0 | all-DL 10-cycle with (2,3,3) at all 10 states, \|E\| = 3n − 11, non-planar, profile `999aba98ab`, 4 law failures (`out/f3_best_closest.txt`; both engines) |
| `anneal_f1_sphere` (+ v1, aborted) | 1 (control) | sphere run ≥ 6 | 692k | 0 exact | law runs of 10 inside R (window 0) in non-planar graphs with \|E\| ≈ 3n − 1; near-cycles with P₁ = 1 |
| `anneal_f1_rp2` (+ v1) | 1 (control) | RP² test beds | 921k | 0 exact | near-cycles with P₁ = 1, e.g. `989a989898` |
| `anneal_f1_tk` (+ v1) | 1 (control) | torus/Klein | 444k | 0 exact | P₁ = 3 |

Byproduct: 34 R-cycles that fail the law (2–8 failures), fed to Method A (§3).

**Control caveat.** My annealer did not reproduce exact law-respecting R-cycles from scratch in about 2M evaluations. TrackJ's tj_search found them with about 2M evaluations from one lucky RP² seed. So "easy without (2,3,3)" rests on TrackJ's rungs (c)/(d): one walk, but 411k distinct graphs. It also rests on my plentiful near-misses and on the R-cycles without the law.

## 5. Verification (two engines)

There is no Q-e example to verify.

What was cross-checked by `tn_verify.py`:
- **Engine 2:** TrackH `th_engine.Hole` for states, π and locks; TrackI `nchains` for N; Lemma E recomputed directly as Σ(|X| + |Y| − e(X,Y)).
- **Claims checked:**
  1. A reduced law cycle (`jd631_169_1246_K`, n = 35, 97 edges = 3n − 8). Results: law 20/20; Lemma E fails at 20/20 cycle states; class of 20 with 0 filled states.
  2. The closest f = 3 cycle (`out/f3_best_closest.txt`). Results: 10-cycle `999aba98ab`; Lemma E at 10/10 states; 4 law failures.
  3. The non-planar run-7 graph (`out/f3_nonplanar_run7.txt`). Result: longest run with R + law + Lemma E is 7, matching `tn_eng`.

## 6. Interpretation and suggested next steps

1. **Conjecture N1** (Euler-type, data only). In any graph with a degree-5 hole, no π-cycle of DL states with N ≤ 9 has Lemma E's sphere constants at all its states. Equivalently, in the (2,3,3) language: no such cycle has Σβ ≤ 1 at every state together with the sphere edge count.
   - Data: 0 / 319 exact surgeries (85 + 200 + 34); 0 in the annealing.
   - The law cycles even need ≥ 3 extra edges.
   - If N1 is true, NRC on the sphere follows from Lemma E alone (no law, no Jordan). It would then be worth looking for a counting proof that uses the common edge set across the cycle's states, which TrackL's per-state χ-recursion ignores.
2. **The "+3 = RP²" coincidence** is the sharpest lead. Test it on law cycles of independent origin before trusting it. Concretely:
   - run TrackJ's `tj_search.py c` (or my `tn_search.py 1`) longer, from torus/Klein seeds and from the 34 law-failing cycles;
   - then apply `tn_forest.py` to the results.
   - If torus-born law cycles need +6 (= 3(2 − χ)), the skeleton is remembering a surface. That would be strong evidence for an Euler-type theorem.
3. **Make the exact add-surgery tractable.** The flow MILP with all addable edges hit time limits. Better options: a warm start, column generation, or a CP-SAT solver if one gets installed.

## 7. Files

| file | content |
|---|---|
| `tn_eng.c` / `tn_eng` | TrackJ engine plus: per-state Lemma E deviation (general form, every state); longest π-run and cycle in R / R + law / R + E / R + law + E; class-wide deviation; best all-DL cycle by penalty for each set; best 10-window penalty; reference colourings; a node limit on the colouring search; `--dump` adds dev and the colouring |
| `tn_lib.py` | pipe driver, relabelling (h → 0, link → 1..5), seeds |
| `tn_search.py` | annealer (§4); `run_anneal*.sh` are the launch scripts actually used |
| `tn_forest.py` | exact surgery MILP with lazy cuts (§3); `--nolaw`, `--flow` |
| `tn_flow.py` | flow MILP and the addable-edge list |
| `tn_addlocal.py` | add/delete local search |
| `tn_chi_steps.py` | Euler-level step table (§2) |
| `tn_verify.py` | second engine (§5) |
| `out/` | seeds, logs, jsonl results. `out/aborted/` holds the first annealer versions (one had a colouring-search hang, one an objective that rewarded shrinking) |

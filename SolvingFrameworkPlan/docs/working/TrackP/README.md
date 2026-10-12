# Track P: N1 from independent lineages (Part A) and an Euler-level attempt on N1 (Part B) [data] + [hand, unreviewed]

Studio, 8 Oct 2026 (04:32 to about 06:25). Nothing outside `TrackP/` was changed and nothing was committed.

Code provenance:
- copied here: TrackN's `tn_eng.c`, `tn_lib.py`, `tn_search.py`, `tn_forest.py`, `tn_flow.py`, `tn_addlocal.py` and `tn_verify.py`; TrackJ's `tj_eng.c`, `tj_lib.py` and `tj_search.py`; TrackF's `surfaces.py`.
- the only change to the copies is an option `--mine` in `tn_forest.py` (exact MILP minimising |K| under the connectivity constraints alone).
- run read-only: TrackF `src/lpc_cycsearch.py` (genus-2 cycle search), and TrackH/TrackI through `tn_verify.py` (the second engine).

Compute: at most 4 workers under `nice -n 10`, with a few short single-process surgery runs (one brief overlap to 5). Machine load from other users was 35–40.

Labels: **[data]** = computation; **[hand, unreviewed]** = short argument written here and not reviewed.

## 0. Bottom line

1. **The single-lineage caveat is broken.** Law-respecting R-cycles (π-cycles of DL states with N ≤ 9 obeying the chain-parity law at every step) now come from **7 new seed lineages**:
   - sphere ×2: Census29 cycle graphs p30.r10#1252 h19 and p32.r17#261286 h22;
   - torus ×3: TrackF cycle graphs torus_c34_w38_t1329, torus_c34_w38_t1433 and torus_c34_w50_t1666;
   - Klein ×2: klein_c32_w41_t1336 and klein_c32_w15_t652.

   Every new cycle is a **10-cycle**, `8989898989` or `9898989898`; TrackJ's RP² lineage gave 20-cycles. Thousands of distinct graphs were produced: 178 sphere, 1,345 torus, 3,106 Klein.
2. **Surface memory is refuted.** The minimal skeleton excess e = |E(G − h)| − (3n − 11) does **not** equal 3(2 − χ) of the seed surface.

   | lineage (seed surface) | 3(2 − χ) | delete-only exact MILP: min e | add + delete local search: min e |
   |---|---|---|---|
   | RP² (TrackJ/TrackN rp2_s203; 3 skeletons re-run) | 3 | 3 (TrackN) | **3** (3,000 rounds) |
   | sphere p30.r10#1252 | **0** | **3** | **2** |
   | sphere p32.r17#261286 | **0** | 6 | 4–5 |
   | torus (3 seeds) | 6 | **3** | **2** (2 lineages); 3 (1) |
   | Klein (2 seeds) | 6 | **3** / 4 | **2** / 3 |
   | genus 2 | 12 | no law cycle reached (see §1.4) | – |

   - Sphere-born cycles need excess ≥ 2–3, not 0.
   - Torus- and Klein-born cycles get down to 2–3, not 6.
   - The "+3 = RP²" of TrackN was a delete-only floor that happens to equal the RP² count. With partition-preserving edge *additions* allowed, it drops to **+2** in sphere, torus and Klein lineages.
3. **N1 survives.** No lineage reaches excess 0, the only value compatible with N1 failing; see Part B, Lemma P1: for law cycles, Lemma E at every state ⇔ e = 0.
   - Best found: **e = 2**, in 26 skeletons. Three of them were re-verified by the second engine (TrackH Hole + TrackI nchains):
     - n1_7121_17_230_K_L_L (n = 29, 78 edges);
     - n1_7121_103_1402_K_L (n = 28, 75 edges);
     - n1_7221_43_1766_K_L (n = 28, 75 edges).

     Each has the law at 10/10 steps and Lemma E failing at 10/10 states.
   - An exact add + delete flow MILP on one e = 2 skeleton (900 s) returned incumbent deviation 2 per state and no improvement. This is not a proof of optimality.
   - A direct attack, 25 min of unrestricted f = 3 annealing from the 26 e = 2 skeletons (2 workers): see §1.5 for the result.
   - Law-failing R-cycles from torus and Klein seeds (4 cycles, 2–4 law failures) have minimal Lemma-E deviation 4 per state and skeleton excess 4. This is consistent with N1 in its no-law form.
4. **Revised data statement.** N1 holds in all lineages, but the floor is **e ≥ 2**, not ≥ 3, and it is not tied to the seed surface. Call this **Conjecture N1⁺ (data)**: every law R-cycle has |E(G − h)| ≥ 3n − 9.
5. **Part B: no proof** (`PartB.md`). Results [hand, unreviewed, each data-checked]:
   - **Identity P1:** N(s) − B(s) = 3nv − |E(G − h)| at every proper colouring, where B is the total cycle rank of the six pair graphs. So e is exactly the bichromatic-cycle budget at rigid states, and N1 for law cycles ⇔ no law R-cycle with |E| = 3nv − 8.
   - **Monodromy Lemma P2:** for cycle length ≢ 0 (mod 3), every non-α vertex is swapped and every edge is cut by some K_t.
   - **Role-label dynamics:** cut balance cutP1 − cutP3 = 1 per step at e = 0, and integral per-edge windings.
   - All of these are **consistent with e = 0**. The integrality condition L(|E| − 1) ≡ 0 (mod 3) holds because 3nv − 8 ≡ 1 (mod 3).
   - There are no persistent bichromatic cycles in the data, so the excess is not carried by a fixed cycle class.
   - The missing input is component-level: which trees merge or split.

## 1. Part A [data]

### 1.1 Pipeline
1. **Seeds.**
   - Fresh min-degree-5 triangulations from `surfaces.py`: 250 torus, 250 Klein, 250 genus 2 (`out/surf_*.txt`). Prescan (`tp_prescan.py`): **no all-DL π-cycle at any hole.** Genus 2 has a median of 2 states per hole. So these were useless as direct seeds.
   - Instead, all-DL cycle graphs: TrackF `out/lpc/cyc_graphs.txt` + `cyc555_graphs.txt` (torus 90, Klein 113, RP² 283 graphs) and TrackJ `sphere_cycle_graphs.txt` (14). Holes were ranked by the law penalty of their best all-DL cycle; typical start: `a9a9a9…`, penalty 10. Files: `out/seeds_cyc_{torus,klein,rp2,sphere}.txt`.
2. **Annealing.** `tn_search.py 1` with `TN_CYCONLY=1`: keep an all-DL cycle and minimise P = Σ max(0, N − 9) + law failures. Edge swaps, flips, toggles and forest exchange; no vertex stacking.
   - Torus and Klein first reached near-misses with P ≤ 3 (`out/seeds_near_*.txt`), then exact examples from those (`an_torus_near`, `an_klein_near`).
   - The sphere run reached examples directly (`an_sphere_cyc`).
   - TrackJ's `tj_search` rung b (class closure) from torus/Klein seeds stalled at bad ≈ 90 and was stopped. So did TrackN's window objective with stacking (slow: n grows to 52).
3. **Surgery.** On samples of each lineage:
   - `tn_forest.py --mine`: exact delete-only, minimise |K| subject to every pair graph keeping its vertex partition at every cycle state;
   - `tn_forest.py` default: exact (2,3,3) or else minimum Σ|dev|;
   - `tn_addlocal.py`: add + delete local search, 400–3,000 rounds;
   - one `--add --flow` exact attempt.

   Every surviving skeleton was re-checked by `tn_eng` (check_cyc = 10/10).

### 1.2 Excess per lineage (min over the sample; e = |E(G − h)| − (3n − 11))

| lineage (first-generation walk ← seed) | cycles | delete-only exact | add + delete | files |
|---|---|---|---|---|
| sphere w15 ← p30.r10#1252 h19 | 10-cycle 8989898989 | 3 (3 of 26), others 4–6 | **2** (1 of 4, 3,000 rounds) | `surg_sphere_w15_mine.jsonl`, `addlocal_round3.jsonl` |
| sphere w14 ← p32.r17#261286 h22 | 10-cycle 9898989898 | 6 (25 sampled) | 4–5 | `surg_sphere_mine.jsonl`, `addlocal*.jsonl` |
| torus 8 ← torus_c34_w38_t1329 h1 | 8989898989 | 3 | **2** (14 skeletons) | `surg_torus_mine.jsonl`, `addlocal_torus2000.jsonl`, `addlocal_round2.jsonl` |
| torus 23 ← torus_c34_w38_t1433 h1 | 9898989898 / 8989898989 | 3 / 4 | 3 | `surg_tk_lineages_mine.jsonl` |
| torus 49 ← torus_c34_w50_t1666 h1 | 8989898989 | 3 / 4 | **2** | same, `addlocal_round2.jsonl` |
| Klein 99 ← klein_c32_w41_t1336 h7 | 9898989898 | 3 | **2** (walk 43); 3 (walk 29) | same |
| Klein 34 ← klein_c32_w15_t652 h5 | 9898989898 | 4 | 3 (1,500 rounds) | `surg_klein_w34_mine.jsonl`, `addlocal_klein_w34.jsonl` |
| RP² (TrackN skeletons of the TrackJ lineage) | 20-cycles | 3 (TrackN) | **3** (3 of 3, 3,000 rounds) | `addlocal_round3.jsonl` |

Further details:
- **Second engine.** `tn_verify.py` on sphere e = 3 (n1_7511_15_3044_K), sphere e = 6 (n1_7511_14_1907_K), torus e = 3 (n1_7121_17_53_K) and the three e = 2 graphs of §0. Every one is a law R-cycle with Lemma E failing at every cycle state.
- **Per-partition excess at the optimum** (`excess_P1P2P3` in the jsonl). For e = 2, every state carries 2, e.g. (1,1,0), (2,0,0), (0,2,0), (1,0,1).
- **Law-failing R-cycles** from torus/Klein seeds (`surg_nolaw_*`): 4 cycles, profiles like 8998889989 (with 8 → 8 steps, legal without the law). Min deviation 40 over 10 states, skeleton excess 4. N1 (no-law form) holds.

### 1.3 Surface-memory verdict
**Refuted.** Sphere-born law cycles need e ≥ 2 (and one lineage ≥ 4), not 0. Torus- and Klein-born cycles reach 2–3, not 6. The excess is a property of the R-cycle combinatorics, not of the seed surface. The coincidence 3 = 3(2 − χ_RP²) in TrackN came from delete-only surgery, whose floor on every lineage here is also 3. With additions it drops to 2, except in the RP² lineage, which stays at 3 under 3,000 rounds.

### 1.4 Genus 2
- No all-DL π-cycle on genus 2:
  - 250 fresh triangulations, n = 20–32, 2,482 holes: none;
  - TrackF's genus-2 census: none;
  - TrackF `lpc_cycsearch.py genus2` (231 walk records, n = 24–34; `out/g2cyc.log`): DL π-runs up to 18, but no cycle.
- Seeding `tn_search` (window + cycle law objective) from the best of those holes (`out/an_g2*`) reached a 10-cycle `989898989a` with penalty 1 (one N = 10 state, law fine), but no exact example in 337k evaluations (40 min).
- So the genus-2 test (+12 predicted) is **not done**. Given §1.3 it is no longer needed for the surface-memory verdict.

### 1.5 Direct N1 attack from e = 2 [data]
`run_A7.sh` ran two workers for 25 min, seeded from the 26 e = 2 skeletons. Objective: f = 3, cycle-only (P = Σ max(0, N − 9) + Σ dev + law failures, with unrestricted graph moves, so partitions can change).

Result: **no example**.
- The best cycle reached is at the sphere edge count itself (|E(G − h)| = 3n − 11, n = 29): a 10-cycle `9a99a9a989` with P = 11, i.e. N-excess 3, Lemma-E deviation 6 and 2 law failures (`out/an_f3_exc2a.jsonl`).
- A second best, also at 3n − 11: the 10-cycle `9a9a9a9a9a`, law 10/10, deviation 6, N-excess 5.
- Both are the same kind of near miss as TrackN's `999aba98ab`: at e = 0, either N goes above 9 or the law fails.
- Totals: 72k evaluations, 0 examples.

## 2. Part B [hand, unreviewed] — see `PartB.md`
In short:
- **P1:** N − B = 3nv − |E| (identity).
- **P2:** monodromy, so every vertex is swapped and every edge is cut when L ≢ 0 (mod 3).
- **B3:** role-label rule, cut balance and integral windings.
- **B4:** all of these are consistent at e = 0, and no persistent bichromatic cycle carries the excess in the RP²-lineage data (`tp_cyclespace.py`).

N1 is not proved. Data checks:
- `out/struct_lawcycles.jsonl`: 128 law cycles (TrackN skeletons + TrackJ rung d) — identity, cut balance, winding rule, monodromy, all 0 failures;
- the same checks on the new sphere e = 3 and torus e = 2 skeletons: 0 failures.

**Suggested next step.** The cleanest open statement is now quantitative: **law R-cycle ⇒ e ≥ 1** (N1), with data floor e ≥ 2.
- The e = 2 skeletons (n = 28–29, 75–78 edges, 10-cycles) are small enough for a full exact add + delete MILP with warm start. They are also the right test bed for a component-level argument: which αA trees merge under J while Γ opens.

## 3. Files
| file | content |
|---|---|
| `tp_prescan.py` | rank all degree-5 holes of a graph file by best law-cycle / law-window penalty |
| `tp_status.py`, `tp_show.py` | progress and summary helpers |
| `tp_struct.py` | Part B checks: identity P1, monodromy, cut balance, windings, swap sets |
| `tp_cyclespace.py` | intersections of bichromatic cycle spaces along a cycle |
| `tn_forest.py` (+ `--mine`), `tn_addlocal.py`, `tn_flow.py`, `tn_search.py`, `tn_lib.py`, `tn_eng.c`, `tn_verify.py`, `tj_*`, `surfaces.py` | copies (see header) |
| `run_A1.sh` … `run_A7.sh` | the launch scripts actually used (A1's tj/tn workers were stopped early, A2's restarted as A5) |
| `out/an_*` | annealing logs; `ev: example` lines are law R-cycles (graph lines, h = 0, link 1..5) |
| `out/surg_*`, `out/addlocal*`, `out/flow_torus_exc2*` | surgery results (graph of the skeleton in `graph`) |
| `out/exc2_examples.txt`, `out/seeds_exc2.txt` | the e = 2 law cycles |
| `PartB.md` | Part B |

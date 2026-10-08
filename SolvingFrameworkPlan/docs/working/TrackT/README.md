# Track T: chord diagrams and interlace graphs for NRC-M

Studio, 8 Oct 2026, about 10:35–11:55 local time. Nothing outside `TrackT/` was changed and nothing was committed.

Compute: at most 2 worker processes, all under `nice -n 10` (machine load from other users was about 40 on 16 cores).

Code: everything here is new (`tt_*.py`). The engine works directly on the cubic graph in matching form (TrackS S3) and does not enumerate colourings. Other tracks' files were read only for input graphs (`TrackF/graphs/plantri24.txt`, `TrackH/cycstat_items.txt`, `TrackS/out/seed_c30.txt`). As cross-checks, the engine reproduces:
- the sphere run lengths of TrackJ/TrackS at the holes tested (for example p24#134 h11: the k(H) word 1121212);
- the RP² and Klein Q-cycles of TrackS §2.3 (L = 20; the k(H) words 3 2 2 1 3 2 3 2 3 2 … and 3 1 1 2 2 3 2 3 2 2 1 …, up to rotation);
- C30#0 having no Hamiltonian state (its Q-cycle stays at k(H) ≥ 2).

Labels:
- **[hand, unreviewed]**: argument written here, not independently reviewed;
- **[data]**: computation;
- **[std]**: standard result quoted from the literature, re-checked on data here.

## 0. Bottom line

1. **No proof of NRC-M.** No invariant or monotone of the interlace graph was found that forbids closure after 5 or 10 Φ-steps.
2. **The chord diagram does not move by a pivot [hand + data].** In chord-diagram language, one Φ step (rigid t → in-shape t+1 → rigid t+2) is
   - **H_{t+2} = H_t Δ D, with D = Y_t Δ Y_{t+1}**, where Y_{t+1} is the v-loop through e₂, e₃ of the single figure-eight **Q_{t+1} = H_t Δ X_t**;
   - the frame index advances by +1 (mod 5), so 5 Φ-steps return the v-labels.

   D is a C_t-alternating cycle. On sphere data it is one cycle in 730 of 764 Φ-steps, and it exchanges 7–20 of the 21 chords (median about 15). So Φ is a **global rewiring** of the chord diagram, not a pivot or local complementation on one edge of the interlace graph. There is no fixed 4-regular graph whose Euler circuits the H_t are, so Bouchet's pivot calculus does not apply directly.
3. **Interlace quantities tested, all negative as obstructions [data].** None of these is monotone along sphere Φ-steps, and none changes by a fixed nonzero amount mod 2, 3, 4, 5, 6 or 8:
   - the GF(2) rank of the interlace matrix;
   - the number of interlace edges;
   - the inside-chord count;
   - the number of chords exchanged, |Y_t ∩ C_t|, and the number of persistent chords;
   - Z/4 Gauss sums.

   What these data do show:
   - the interlace edge count is always even (764/764);
   - the inside-chord count changes by at most 1 per Φ-step;
   - persistent chords never change side. This last one is a trivial consequence of the role bookkeeping (§2.3), not a constraint.
4. **A GF(2) form of rigidity [std + data; any surface].** Blow v up into 3 points. Then at every rigid state, nullity_GF(2)(I + Δ) = 3, where I is the interlace matrix of (H_t, C_t) and Δ marks the chords whose ends have equal parity along H_t. This is the circuit-partition formula k(F12) + k(F13) + 2 = 1 + ν(I + Δ). It holds verbatim on RP² and on the Klein bottle, so it carries **no planar information**.
5. **What planarity is needed for [data].** The planar input that is actually used (the chain-parity law, Tait form: k(H) changes parity at every DL → DL step) depends on the cyclic order at v being the planar one.
   - Take planar sphere duals and relabel the five v-edges by every cyclic order. The law holds at **0 / 256** steps for the planar order and 0 / 247 for its mirror. It **fails at 611 / 1,261 = 48 %** of the steps for the 22 non-planar orders.
   - The interlace graph at a Hamiltonian state is bipartite exactly when the drawing is planar. It is bipartite at all 1,528 sphere Hamiltonian states in the Φ data, and **non-bipartite at all 61** Hamiltonian states of the RP²/Klein Q-cycle holes (`rp2_s203_w664_t327` h13, `klein_s204_w374_t916` h0).
6. **Non-planar analogues in matching form (abstract graphs: v of degree 5 with an arbitrary cyclic labelling, the rest cubic) [data].**
   - **All-rigid 5-cycles (k(H) ≡ 1) are common.** 87 random graphs carry them, out of 140k random graphs with n = 16, 20; rigid isolation fails freely off the plane.
   - Every closed orbit found in random graphs has length 5 or 10 and **violates the law**.
   - Annealing for long **R-runs** (k(H) alternating exactly 1, 2, 1, 2, …) reaches **8 states at n = 24**, as long as the sphere record of the frame census (NR = 8 at order 33, where G has 58 vertices), but no further in about 3.2M annealed evaluations.
   - **No law-respecting closed orbit of any kind** was found (with or without Hamiltonian states). Every closed orbit has ≥ 2 law violations; the 10-cycles show 2, 4, 6, 8 or 10.
   - Chord-level Φ statistics are the same as on the sphere (D one cycle in 89/91 steps, median exchange 82 % of chords). The only difference is that the interlace graph is non-bipartite (91/91).
7. **Sharpest sub-claims (§5).**
   - **T1 (planarity-free R-cycle exclusion).** No graph with one degree-5 vertex (any cyclic labelling), all other vertices cubic, carries a cyclic sequence of perfect matchings in matching form with k(M_{t−1} ∪ M_t) = 1, 2, 1, 2, … . On the sphere T1 is exactly NRC′, by the law. If T1 holds in general, NRC needs planarity only through the law (Lemma 5), and the rest is pure matching combinatorics.
   - Status of T1: open. No counterexample was found, but the abstract search never produced a law-respecting closed orbit of any kind, so this is weak evidence (§5).

## 1. Chord form of a rigid state [hand, unreviewed]

Notation as in TrackS §1. G is the Tait dual (v of degree 5, rotation f₀ … f₄). A state is (M_{t−1}, M_t) = (P, M), with k the index of M's v-edge; in the state's frame e_i = f_{k−2+i}. At a rigid state:
- H := P ∪ M is a Hamiltonian cycle;
- Q := E − M = X ∪ Y and F12 := E − P are connected figure-eights with the DL pairings.

**Circle and chords.**
- Draw H as a circle. Its edges alternate between colour 2 (M) and colour 3 (P).
- The chords are C := E − H (colour 1). Each cubic vertex carries one chord end; v carries three: e₀, e₁, e₃.
- v is blown up into three consecutive circle points between its H-neighbours, in the order [via e₂] e₁ e₃ e₀ [via e₄], written in the frame of the state. (In absolute labels: [via f_k] f_{k−1} f_{k+1} f_{k−2} [via f_{k+2}].)
- Planar rotation: e₃ is alone on one side of H at v, and e₀, e₁ are on the other.
- The two virtual circle edges inside the blow-up get colours 3 and 2 in order, so the alternation 2, 3, 2, 3 is kept.

**Planarity.**
- G is planar with the given rotation at v ⇔ the chords split into inside and outside families that are each non-crossing ⇔ the interlace graph IG(H, C) is bipartite, with the bipartition compatible with e₃ | e₀e₁ at v.
- In primal terms the inside chords form the αμ tree and the outside chords the AB tree (TrackI §3, TrackJ §1.4).
- The interlace graph is the fundamental graph of the plane graph αμ-tree ∪ {flips of the AB-tree edges}, with respect to the spanning tree αμ-tree. (Each flipped edge joins the αμ apexes of the two triangles on an AB edge. These quadrilaterals are disjoint, because a triangle has only one AB edge.) This is the de Fraysseix correspondence in the present setting.

**Three diagrams.** At a rigid state all three bicoloured subgraphs are connected. So there are three circle diagrams:
- (H, M₁);
- (F13 = Q, M₂): the figure-eight opened at v;
- (F12, M₃).

In (Q, M₂) the colour-2 chords split into three non-crossing families: inside the disc of X (the region K), inside the disc of Y (K₀), and in the outer region (μB). The interlace graph is bipartite: the outer family against the rest. M_{t−1} and M_{t+1} are the two alternating classes of this circle. They agree on X and are complementary on Y (TrackS S3).

**GF(2) count [std + data].**
- Let I be the GF(2) interlace matrix of (H, C) with v blown up, and Δ the diagonal indicator of chords whose two ends have equal parity along the circle.
- The circuit-partition formula (Cohn–Lempel; Traldi) for the two transition systems "alternating class ∪ chords" gives k(M ∪ C) + k(P ∪ C) + 2 = 1 + ν(I + Δ). The +2 appears because the blow-up smooths v in F12 and F13 exactly along their DL pairings, and that adds one loop each.
- So **rigid ⇒ ν(I + Δ) = 3**.
- Check (`tt_gf2.py`): the identity holds at every state where both pairings are DL, and fails only at run-start states whose F12 is not DL-paired, exactly as predicted. It holds equally on the RP²/Klein holes (ν = 3 at all their interior rigid states). So the formula is not a planar input.

## 2. One Φ step in chord form [hand, unreviewed; data]

### 2.1 Formulas

Let t be rigid, with Q_t = X_t ∪ Y_t. TrackS S3 gives M_{t+1} = M_{t−1} Δ Y_t and C_{t+1} = C_t Δ Y_t. Then:

- **(Φ1)** H_{t+1} = H_t Δ Y_t. This is H₀ ∪ C′ at an in-shape state.
- **(Φ2)** **Q_{t+1} = F12_t Δ Y_t = H_t Δ X_t.**
  - *Proof.* E − M_{t+1} = (E − M_{t−1}) Δ Y_t = F12_t Δ Y_t.
  - Write C_t = (X_t ∪ Y_t) − M_{t−1}, since F13 = C_t ⊔ M_{t−1} = X_t ⊔ Y_t, and note that M_t is disjoint from Y_t.
  - Then F12_t Δ Y_t = M_t ∪ (X_t − M_{t−1}) ∪ (Y_t ∩ M_{t−1}) = (M_{t−1} ∪ M_t) Δ X_t. ∎
  - In circle terms: keep every colour-3 edge of H_t that lies on Y_t, and replace every colour-3 edge on X_t by the X_t-chords.
- **(Φ3)** **Y_{t+1} is the v-loop of H_t Δ X_t through e₂, e₃, and X_{t+1} is the one through e₁, e₄.**
  - The frame at t+1 is k − 2, so Y_{t+1} uses f_{k}, f_{k+1} = e₂, e₃.
  - The figure-eight condition at t+1 says that H_t Δ X_t is connected with pairing (e₁e₄)(e₂e₃). This is TrackI Lemma 4(d).
- **(Φ4)** **H_{t+2} = H_t Δ D, C_{t+2} = C_t Δ D, with D := Y_t Δ Y_{t+1}.**
  - Since Y_{t+1} ⊆ (H_t − X_t) ∪ (X_t ∩ C_t), we get Y_t ∩ Y_{t+1} ⊆ Y_t ∩ M_{t−1}.
  - Chords leaving: all chords of Y_t, plus the X_t-chords used by Y_{t+1}.
  - Chords entering: the colour-3 edges of Y_t not on Y_{t+1}, plus the colour-2 edges on Y_{t+1}.
  - D is a C_t-alternating even subgraph.
- **(Φ5)** M_{t+2} ∋ f_{k+1} (= e₃ at t) and M_{t+1} ∋ f_{k−2} (= e₀ at t). So **Φ advances the frame index by +1 mod 5**. At t+2 the circle passes v through e₀ and e₃, and the v-chords are e₁, e₂, e₄.

### 2.2 Is it a pivot? No, at least not a bounded one [data]

`tt_phi.py`: plantri24, every 10th graph, all degree-5 holes (491 holes with a Φ-step), 764 Φ-steps, G of order 40 (21 chords).

| quantity | distribution |
|---|---|
| components of D = H_t Δ H_{t+2} | 1: 730, 2: 33, 3: 1 |
| \|D ∩ C_t\| (chords exchanged), out of 21 | 7–20; 14–20 in about 85 % of steps |
| persistent chords \|C_t ∩ C_{t+2}\| | 1–14 |
| \|Y_t ∩ C_t\|, \|Y_{t+1} ∩ C_{t+1}\| | 4–17 each |
| change of rank_GF(2) IG | −6: 3, −4: 37, −2: 205, 0: 301, +2: 170, +4: 43, +6: 5 |
| change of inside-chord count | −1: 148, 0: 460, +1: 156 |
| interlace edge count | always even (both ends of all 764 steps) |
| persistent chords changing side | 0 / 764 steps (see 2.3) |
| bipartite IG at both ends | 764 / 764 |
| frame advance | +1 in 764 / 764 |

**Conclusion.**
- A pivot on an edge ab of the interlace graph is the exchange of two interlaced chords along an alternating 4-cycle: remove two H-edges, add two chords. Here the Hamiltonian cycle is exchanged along a single long alternating cycle that uses most of the chords.
- Bouchet's calculus describes Euler circuits of one fixed 4-regular graph, G/C. But C changes with t, so no fixed 4-regular graph carries all the H_t. The contracted graphs G/M_t change with t as well.
- So the lead "Φ = a pivot on the interlace graph" does not hold in any direct form.

### 2.3 Side bookkeeping (why "persistent chords keep their side" is empty) [hand]

- In primal names a Φ-step swaps α ↔ A on K_t, then α ↔ μ on K_{t+1} (t-names). The roles at t+2 are (α, A, B, μ) in t-names.
- A persistent outside chord is an {A,B} edge at t. B is never recoloured, so its other end must become μ (A → α → μ). It ends as an {A″,B″} = {B,μ} edge: outside again.
- An inside {α,μ} chord cannot become an outside {B,μ} edge, because no vertex becomes B.
- So side preservation is forced by colour bookkeeping and constrains nothing.

## 3. Invariants tested [data]

At every sphere Φ-step (764) the following quantities were checked for monotonicity and for a fixed nonzero change mod m, m ∈ {2, 3, 4, 5, 6, 8}:
- rank IG / 2;
- the number of IG edges;
- the inside count;
- |Y_t ∩ C_t|, |Y_{t+1} ∩ C_{t+1}|, |D ∩ C_t|, and the persistent count.

Results:
- **None is monotone, and none has a constant nonzero residue.**
- The IG edge count has a constant **zero** residue mod 2. That is a per-state parity, not a step quantity.
- The Z/4 Gauss sum G(q), with q(x) = Σ Δ_i x_i + 2 Σ_{i<j} I_ij x_i x_j, vanishes at most rigid states (q is non-zero on the radical). Where it is nonzero, its phase takes several values. No pattern. This was looked at only on the holes p24#134 h11 and p24#596 h20.

These join TrackS §4's negative list (α-orientation height, region incidences, spoke order, figure-eight statistics, Heawood sums).

**A closure identity, recorded for any future rotation argument [hand].**
- Write the primal colouring in F₄ with α = 0. Each π-step adds s_t·1_{K_t}, where s_t runs through the non-α colours with period 3 (s_t = s₀ω^{±t}).
- A closed π-cycle of length L with 3 ∤ L returns the colouring multiplied by ω^m with m ≢ 0 (mod 3). This is the 3-cycle monodromy of non-α colours. So

  **c₀ = λ · Σ_{t ∈ ℤ/L} ω^{±t} 1_{K_t}**, with λ = s₀ / (ω^m − 1) ∈ F₄\*.

- Equivalently, every vertex u has c₀(u) ≠ 0 ⇔ the counts n_r(u) = #{t ≡ r (mod 3) : u ∈ K_t} are not all of the same parity.
- The Tait form reads τ₀ = λ Σ ω^{±t} 1_{X_t}.
- This is a consequence of closure, so it gives no contradiction by itself. It is the precise form of TrackS's "every Tait vertex lies on some X_t", and of the monodromy remark in the brief. Any argument by rotation numbers has to be compatible with it.

## 4. Non-planar analogues in matching form [data]

**Abstract graphs** (`tt_abstract.py`):
- v has degree 5 with an arbitrary cyclic labelling f₀ … f₄, and all other vertices are cubic. Graphs are generated by the configuration model, and are almost surely non-planar.
- The dynamics is exactly TrackS S3: the state (P, M) must have Q = E − M a connected figure-eight with the DL pairing w.r.t. M's v-edge index k, and P ∋ f_{k+2}; the step is (P, M) → (M, P Δ Y).

| experiment | graphs evaluated | result |
|---|---|---|
| random, n = 16 (2 min) | 110,111 | 98 graphs with closed orbits: 72 all-rigid 5-cycles (k(H) = 11111), 25 mixed 5-cycles, 1 mixed 10-cycle. **No closed orbit satisfies the law** |
| random, n = 20 (2 min) | 29,716 | 30 graphs with closed orbits: 15 all-rigid 5-cycles, 14 mixed 5-cycles, 1 mixed 10-cycle. No law-respecting orbit |
| anneal for R-runs (k(H) = 1,2,1,2,…), n = 18, 24, 28 | about 10⁴–10⁵ each (the slow early engine for n = 18, 24) | longest R-run **8** (n = 24, non-planar: `out/abs_annealR_n24_slow.jsonl`, word 21212121); 7 at n = 28 |
| anneal seeded from the n = 24 record (40 min) | 1,187,952 | no improvement: longest R-run 8; 680 closed-orbit events, all violating the law |
| anneal for law-respecting closed orbits containing a Hamiltonian state, n = 20 (40 min, `out/abs_annealL_n20.jsonl`) | 1,987,444 | longest law-respecting stretch 8 (`221212121`); 11,821 closed-orbit events (5-cycles 11,576, 10-cycles 245), **none law-respecting** |

**Sphere graphs with a non-planar rotation at v** (`tt_rot.py`, `out/rot_p24_s40.summary`):
- plantri24, every 40th graph (first 15 graphs; 332 holes), with every one of the 24 cyclic orders at v;
- law steps counted only between states whose F12 is connected, so that N = 7 + k(H).

| order at v | holes | DL → DL steps | law violations | longest R-run | closed orbits |
|---|---|---|---|---|---|
| planar | 332 | 256 | **0** | 5 | 0 |
| mirror | 331 | 247 | **0** | 4 | 0 |
| 22 non-planar orders | 7,284 | 1,261 | **611 (48 %)** | 3 | 0 |

**Off-sphere surfaces.** At the RP²/Klein Q-cycle holes, all 61 Hamiltonian states (19 RP², 42 Klein) have a **non-bipartite** interlace graph, and ν(I + Δ) = 3 at the interior rigid states. Their Q-cycles have k(H) words with one 1 per 10 states, so they are not NRC-M analogues. Both violate the law: the Klein word contains 2 2, and so does the RP² word.

## 5. Sharpest sub-claims

**T1 (planarity-free form).** For every finite graph G with one vertex v of degree 5 (edges cyclically labelled f₀ … f₄) and all other vertices cubic, there is no cyclic sequence (M_t)_{t ∈ ℤ/L} of perfect matchings such that for every t:
- (i) E − M_t is a connected figure-eight whose v-loops pair (f_{k−1}f_{k+1})(f_{k+2}f_{k−2}), where f_k ∈ M_t;
- (ii) M_{t+1} ⊆ E − M_t and f_{k−2} ∈ M_{t+1};
- (iii) k(M_{t−1} ∪ M_t) = 1 for even t and 2 for odd t.

- On the sphere, with the planar labelling, (iii) is equivalent to "N ≤ 9" by Lemma 1 and the chain-parity law. So T1 restricted to plane graphs **is** NRC′, which implies NRC.
- T1 contains no planarity. **Status: open.** No counterexample in about 3.4M abstract graph evaluations (n = 16–28). This is weak evidence, because the same searches found **no law-respecting closed orbit of any kind**.
  - Over all logs, the closed orbits have law-violation counts (L, v) = (5,1): 8,997; (5,3): 2,501; (5,5): 1,196; (10,2): 139; (10,4): 37; (10,6): 107; (10,8): 6; (10,10): 25. The parity v ≡ L (mod 2) is automatic.
  - So off the plane the law fails before Hamiltonicity is even tested, and the searches do not separate "law" from "law + Hamiltonian".
  - A sharper abstract test would first find law-respecting Q-cycles off the plane (C30#0-type, k(H) ∈ {2,3}) and then push them towards k(H) = 1. That was not reached here.
- Planarity is not needed for (i)–(ii) (TrackS S1–S4), and the law does not hold off the planar rotation (§4). So if T1 is true, the only planar input NRC needs is the law (Lemma 5).
- If T1 is false (an abstract law-respecting R-cycle exists), NRC-M needs a second planar input beyond Lemma 5. The natural candidate is the bipartiteness of the interlace graph at the rigid states, but no quantity built from it was found that sees closure (§3).

**T2 (interlace form of NRC-M, plane case; a restatement).** On a planar chord diagram, a rigid state is (H, C, 2/3-colouring of H, v blown up) with bipartite IG, ν(I + Δ) = 3 and the DL pairings. The map Φ of §2.1 is defined by (Φ2)–(Φ4). Then Φ has no periodic orbit, and Φ⁵ ≠ id wherever defined.

- Data: 764 Φ-steps on the sphere, with no orbit longer than 3 Φ-steps in this sample. The longest known sphere runs are 3 Φ-steps (R-run 7–8; TrackJ, Census33).
- Within this track, T2 is no easier than NRC. Its value is that it isolates what Φ does on a chord diagram, which is computable in O(n) per step.

**Why the interlace lead stalls.**
- Bipartiteness of IG is just planarity of the drawing.
- [sketch, not checked] In the (Q_t, M_t) diagram the law should read: flipping Δ on the X–Y chords changes the parity of ν(I + Δ). In that sense the law is the GF(2)-parity shadow of planarity.
- Everything else tested (ranks, edge counts, Gauss sums, side counts) moves freely along Φ, both up and down.
- A pivot structure would have given a fixed vertex set on which to look for an invariant. Φ exchanges most chords at every step instead, so no such fixed set is available.

## 6. Files

| file | content |
|---|---|
| `tt_lib.py` | matching-form engine on abstract graphs (G5), Tait dual of a triangulation, Hamiltonian DL states (DFS with degree pruning), runs forward and backward, chord diagram, interlace, GF(2) rank |
| `tt_runs.py` | runs and k(H) words per hole (cross-checks with TrackJ/TrackS) |
| `tt_phi.py` | Φ-step chord statistics on sphere holes; `out/phi_p24_s10.jsonl` |
| `tt_phi_abs.py` | the same for abstract or off-sphere graphs; `out/phi_abs.jsonl` (91 Φ-steps from annealed non-planar graphs) |
| `tt_phi.py` on TrackS notable holes | `out/phi_notable_p24.jsonl` (100 Φ-steps, plantri24 holes with R-run ≥ 6; D one cycle 91/100, median exchange 71 %) |
| `tt_gf2.py` | ν(I + Δ) circuit-partition check, ranks, Z/4 Gauss sums |
| `tt_abstract.py` | random and annealed search in abstract graphs (modes: NRC-M windows, R-runs `R`, law-respecting closed orbits `L`; seeds from a sphere hole or an earlier log); `out/abs_*.jsonl` |
| `tt_rot.py`, `tt_rotsum.py` | non-planar relabellings of the rotation at v on sphere duals; `out/rot_p24_s40.{jsonl,summary}` |

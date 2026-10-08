# Track S: a Jordan-level attack on NRC (matching form; the H-level is what matters)

Studio, 8 Oct 2026, from about 09:05 local time. Nothing outside `TrackS/` was changed and nothing was committed.

Code reuse (read-only): TrackL `tl_lib` (HoleData, TaitState), TrackH `th_engine`, TrackI `ti_lib` (chord-model generator, Tait class), TrackJ `tj_eng` (C engine, used as an independent check). Everything else here is new (`ts_*.py`).

Compute: at most 2 busy worker processes, all under `nice -n 10`. One accidental 3-process overlap lasted about 2 minutes before a job was stopped. Each adversarial search is a Python driver blocked on one C-engine child. Wall time was about 09:05–10:45. Load from other users was about 43 on 16 cores.

Labels:
- **[hand, unreviewed]**: argument written here, not independently reviewed;
- **[data]**: computation;
- **[data, 2 engines]**: confirmed by an independent engine.

## 0. Bottom line

1. **NRC is not proved.** The obstruction has been located more precisely, and one tempting strengthening has been refuted.
2. **Matching form of near-rigid runs [hand, unreviewed; no Jordan, no Euler; 0 failures on data].** In the Tait dual G, write M_t for the colour-2 class of the t-th state of a π-run.
   - The state is the Tait colouring (col1, col2, col3) = (rest, M_t, M_{t−1}).
   - As long as Q_t := E − M_t = F13(t) is connected (true at every rigid and every in-shape state, hence along any R-cycle), Q_t is a figure-eight X_t ∪ Y_t with **exactly two** perfect matchings. These are **M_{t−1} and M_{t+1}**, and they differ exactly on the odd loop Y_t:

     **M_{t+1} = M_{t−1} Δ Y_t**  (Lemma S3).

   - So the run is a walk in the graph 𝔇 of "good" perfect matchings (complement connected), adjacent when disjoint. 𝔇 has **maximum degree 2**, and its edges are canonically directed by the rotation at v (Corollary S4).
   - Primal form, valid in any graph: P2(π c) = P2(π⁻¹ c) Δ δK_{αA}(x_j) whenever #αA(c) = 2 (Lemma S5).
   - TrackI's formulas H′ = H Δ Y and F13′ = H Δ X drop out as corollaries.
   - NRC′ becomes a statement about a **cyclic sequence of perfect matchings** (NRC-M, §3).
3. **The figure-eight structure alone does not exclude cycles on the sphere [data, 2 engines].** At the fullerene dual **C30#0, holes 0 and 16**, there is an all-DL π-cycle of length 20 with **F12 and F13 connected at every state** (a "Q-cycle"). Along it, N = 10, 9, 10, 9, … and k(H) = 3, 2, 3, 2, ….
   - So "𝔇 has no DL-type cycle on the sphere" (QC) is **false**.
   - Any proof of NRC must use that H is a **Hamiltonian cycle** at alternate states (k(H) ≤ 2), not just the figure-eight/Kempe structure of F12 and F13.
   - The S-lemmas themselves hold on every triangulated closed surface (checked on RP², Klein bottle and torus), so they are not where planarity enters.
4. **Sharpest open sub-claim (§3).**
   - **Q-escape (sphere):** a Tait-rigid state (H, F12, F13 all connected) never lies on a π-cycle along which F13 stays connected. Q-escape ⇒ NRC-M ⇒ NRC.
   - **On RP² and on the Klein bottle it is false [data]:** explicit triangulations carry π-cycles with F13 (and F12) Tait-connected at all 20 states that pass through Tait-rigid states. There are 4 RP² holes and 1 Klein hole; no torus example was found (§2.3).
   - On the sphere, the only Q-cycles found (C30#0 h0/h16) never reach k(H) = 1. The sphere evidence for Q-escape beyond NRC is thin, since Q-cycles are rare: no other Q-cycle appears in the frame census to order 33, in the fullerene duals to C46, or in a 75-minute adversarial flip search (§2.5).
   - That search did find sphere Q-runs through rigid states of length 11 (two engines). Their k(H) words, e.g. 2 1 4 1 2 3 2 1 4 1 2, show rigid states sitting in long Q-runs, with k(H) jumping 1 → 4 → 1. These are not R-runs.
   - So Q-escape is a genuinely spherical statement, like rigid isolation. NRC itself has no known counterexample on any triangulated surface (TrackJ RP² runs reach 11; here RP² Q-runs reach 17 and torus/Klein reach 18).
5. **Candidate potentials tested, all negative [data]** (§4). None of these is monotone along Φ-steps or forced by closure:
   - an α-orientation lattice height (Felsner-type, from rooting the 8 Kempe trees at link vertices);
   - zero patterns of region incidences between consecutive figure-eights;
   - universal subset/disjointness relations between named chains of u, π(u), π²(u) (only transport identities appear);
   - the order of the spokes along H_t;
   - chord statistics of the figure-eight;
   - the position of C′ relative to X, Y;
   - Heawood/Fisk sums. Here S_t = Σε_t is the chain-parity law in disguise: S_t mod 8 is a function of N_t mod 2, so its closure constraint is automatically met.
6. **Exhaustive planar chord model** (all plane cubic multigraphs with one degree-5 vertex carrying a rigid state, ≤ 13 cubic vertices): R-runs from rigid states have length ≤ 3 (forward) and there are no closed orbits (§5). This adds little, because runs are short at these sizes.

## 1. Matching form [hand, unreviewed]

### Setting and notation

- G is the Tait dual (TrackI §1): cubic except v (degree 5). It may live on any closed surface; the sphere is never used in §1.
- At a DL state c with frame j, the v-edges are e_k = (absolute v-edge f_{j+k}), with colours (1,1,2,1,3).
- M_i(c) is colour class i. H = M2 ∪ M3, F12 = M1 ∪ M2, F13 = M1 ∪ M3.
- A *perfect matching* of G covers every vertex once (v included). M2(c) and M3(c) are perfect matchings; M1(c) is not (it has 3 edges at v).

**Lemma S1 (transport; any surface).** Let c be DL with π(c) = c′ defined, and let C = ∂R be the switched curve system (TrackI Lemma 4).
- M3(c′) = M2(c).
- M2(c′) = M1(c) Δ C ⊆ E − M2(c).
- The v-edge of M2(c′) is e_j = f_j, i.e. e′₂ with e′_k = e_{k+3}.

*Proof.* TrackI Lemma 4(a),(c): colour 2 is untouched by the switch on C ⊆ M1 ∪ M3, and the new names are 1′ = 3, 2′ = 1, 3′ = 2. These are local statements plus renaming; no Jordan is used. ∎

**Lemma S2 (figure-eights; any graph).** Let Q ⊆ E(G) be connected, with deg_Q(v) = 4 and deg_Q(w) = 2 for every other w. Then:
- Q is the union of two cycles X, Y through v, meeting only at v.
- Exactly one of them, Y, has an odd number of vertices other than v.
- Q has exactly two perfect matchings P, P′:
  - they agree on X, where both equal the unique perfect matching of the path X − v;
  - on Y they are the two alternating matchings of the closed path Y, each containing one v-edge of Y;
  - hence P Δ P′ = Y.

*Proof.*
- Two closed trails from v use the four v-edges. Every other vertex has degree 2, so the trails are cycles meeting only at v.
- The cubic vertices number |V| − 1, which is odd: |V| is even because G has a perfect matching. So exactly one loop, Y, has an odd number of them.
- In a perfect matching, v is matched along one Q-edge, say into loop Z. The remaining vertices of Z form a path, which has a perfect matching iff its vertex count is even, i.e. iff Z has an odd number of non-v vertices. So Z = Y, with two choices of v-edge.
- The other loop's vertices form a path with an even number of vertices, which has exactly one perfect matching. ∎

**Lemma S3 (Q-runs; any triangulated closed surface).** Let c_0, c_1, … be a π-run of DL states such that every F13(c_t) is connected. Call this a *Q-run*. Every stretch of rigid and in-shape states is one (J1/J3/Lemma S: the extra chain of an in-shape state is in P1), and so is every R-cycle (J5). Not every R-run is: its end states can carry a μA/μB extra (TrackJ §3.2). Put M_t := M2(c_t) and Q_t := E − M_t. Then for every t with c_{t±1} in the run:
- **(a)** M3(c_t) = M_{t−1}, H(c_t) = M_{t−1} ∪ M_t, F13(c_t) = Q_t and F12(c_t) = Q_{t−1}.
- **(b)** M_{t−1} and M_{t+1} are the two perfect matchings of the figure-eight Q_t = X_t ∪ Y_t. The odd loop is Y_t (through e_j and e_{j+4}), and **M_{t+1} = M_{t−1} Δ Y_t**.
- **(c)** H(c_{t+1}) = H(c_t) Δ Y_t and F13(c_{t+1}) = H(c_t) Δ X_t. These are TrackI Lemma 4(c) and §3.
- **(d)** c_t is determined by M_t and its frame: col2 = M_t, col3 = the perfect matching of Q_t through e_{j+4}, col1 = the rest.

*Proof.*
- (a) is S1, and F12 = E − M3.
- (b): by S1, M_{t+1} ⊆ Q_t and M_{t−1} = M3(c_t) ⊆ Q_t. Both are perfect matchings, and they are distinct: M_{t−1} contains e_{j+4} (colour 3 at v) and M_{t+1} contains e_j (S1). By S2 they are the two perfect matchings of Q_t, and they differ exactly on the odd loop. The odd loop contains e_j and e_{j+4}, so it is the DL loop Y_t (pairing (e_{j+1}e_{j+3})(e_je_{j+4})).
- (c): H(c_{t+1}) = M_t ∪ M_{t+1} = M_t ∪ (M_{t−1} Δ Y_t) = H(c_t) Δ Y_t, since Y_t ∩ M_t = ∅. F13(c_{t+1}) = E − M_{t+1} = M_t ∪ (Q_t − M_{t+1}) = M_t ∪ (M_{t−1} Δ X_t) = H(c_t) Δ X_t.
- (d) follows from (b) and S2. ∎

In particular the in-shape step and the rigid step use the same mechanism: the "previous" matching is flipped along the odd loop of the current figure-eight.

**Corollary S4 (the good-matching graph).** Call a perfect matching M *good* if E − M is connected. Let 𝔇 be the graph on good matchings, with M ~ M′ iff M ∩ M′ = ∅.
- **deg_𝔇 ≤ 2.** A neighbour of M is a perfect matching of E − M, and there are exactly two (S2).
- If M has DL type (its complement pairs the v-edges as (e_{k−1}e_{k+1})(e_{k+2}e_{k−2}), where e_k ∈ M), its two potential neighbours contain e_{k+2} and e_{k−2}.
- A Q-run is a walk in 𝔇 along which the v-edge of M_t advances by −2 notches. A π-cycle of DL states with F13 always connected is a cycle of 𝔇 of length ≡ 0 (mod 5).
- Conversely, a cycle of DL-type good matchings, with the v-edge advancing −2 per step, defines such a π-cycle by S3(d).

**Lemma S5 (primal form; any graph, no embedding).** Let c be a DL state with #αA(c) = 2 and π^{±1}(c) defined. Then

  P2(π c) = P2(π⁻¹ c) Δ δK_{αA}(x_j), and P2(π c) ∩ P2(c) = ∅,

where P2(·) is the edge set of the αA ∪ μB pair graphs in that state's own roles. On a triangulation, δK_{αA}(x_j) is dual to Y_t, and this is S3(b).

*Proof.* P2(π⁻¹c) = P3(c) (J2). Compare edge by edge, using that every α- or A-vertex lies in K = K_{αA}(x_{j+2}) or in K0 = K_{αA}(x_j):
- Edges not touching K keep their colours. Such an edge is in exactly one of P3(c) and P2(πc) iff it has exactly one end in K0. The cases are αμ, αB, μA, AB with the α/A end in K0, and the edge is in neither set otherwise.
- Edges touching K: K's α ↔ A swap together with the role rotation (α, μ, A, B) → (α, B, μ, A) puts each such edge into both sets or into neither. ∎

**Planarity accounting.** S1–S4 use only that the primal is a triangulation of some closed surface (so the dual is cubic away from v). S5 uses nothing. No Jordan curve theorem and no Euler formula is used.

**Data (`ts_verify.py`, `ts_v5_general.py`)**, with checks:
- V1: two perfect matchings of Q_t, using e_j and e_{j+4};
- V2: M3(c_t) = M2(π⁻¹c_t);
- V3: the perfect matchings of Q_t are M_{t±1};
- V4: M_{t+1} Δ M_{t−1} = Y_t;
- V5: Lemma S5.

| set | states | failures |
|---|---|---|
| sphere: plantri24, every 25th graph (300 graphs, all degree-5 holes), every DL state with P2 minimal | 90,868 states (V3a/V4 at 19,999 π-steps; V2/V5 at 23,331) | **0** |
| sphere: the 3 holes of `out/verify` smoke test (p24#596 h20, p24#134 h11) | 72 | 0 |
| off-sphere, hypothesis "F13 Tait-connected" (`TS_TAIT=1`): Klein ×2, torus ×1, RP² ×2 holes carrying Q-cycles | 258 | **0** |
| off-sphere, hypothesis "P2 = (2,1)" (chain counts) | 324 | V1 fails 66 times. This is expected: off the sphere, chain counts ≠ Tait components |
| general graphs (no embedding), V5 only: 43 TrackJ rung-d examples + 3 TrackP e = 2 + TrackQ e = 1 law cycles | 1,013 | **0** (all 47 law cycles are chain-count Q-cycles) |

## 2. Q-cycles: the figure-eight structure alone does not exclude cycles

Call a π-cycle of DL states a **Q-cycle** if F13 (hence also F12 = the previous F13) is connected at every state. On the sphere this is the same as P2 = (2,1) at every state. Every R-cycle is a Q-cycle. By S4, Q-cycles are exactly the DL-type cycles of 𝔇.

### 2.1 A sphere Q-cycle [data, 2 engines]

**C30#0 (fullerene C30 dual, n = 17), holes 0 and 16:**
- π-cycle of length 20, all DL;
- (k(H), k(F13), k(F12)) = (3,1,1), (2,1,1), (3,1,1), (2,1,1), …;
- N = 10, 9, 10, 9, ….

Verification:
- engine 1: TrackH/TrackL Python engine (`ts_qcyc.py`, `out/qcyc_fullerene20_46.jsonl`, `out/qcyc_sphere_cyclegraphs.jsonl`);
- engine 2: TrackJ C engine `tj_eng` (`ts_qcheck_c.py`): "P2,P3 minimal at all states: True" at both holes.

Its free {2,3}-cycles are not spectators. At the 10-states H has two free cycles (12 + 8 edges), at the 9-states one (18 edges), and they change at every step (`ts_qcyc` / §2.4 snippet).

So **QC ("𝔇 has no DL-type cycle on the sphere") is false.** The NRC obstruction is not in the Kempe/figure-eight structure of F12 and F13. It is in the **level of H**: an R-cycle is a Q-cycle at level k(H) ∈ {1, 2}, and C30#0 realises level {2, 3}.

### 2.2 Census of sphere all-DL cycles [data]

Per state, the word is k(H) k(F13) k(F12) from chain counts.

| source | all-DL cycles | Q-cycles | max # states with F13 connected on one cycle |
|---|---|---|---|
| Census29 cycle graphs (orders 30–32, all holes; `out/qcyc_sphere_cyclegraphs.jsonl`) | 17 (+ C30#0 ×2) | 0 (+ 2 at C30#0) | 12 / 20 |
| Census33 all-DL cycles (25 holes) + the NR = 8 hole (`out/qcyc_census33.jsonl`) | 25 | 0 | 13 / 20 |
| fullerene duals C20–C46, every degree-5 hole (4,104 holes; `out/qcyc_fullerene20_46.jsonl`) | 4 (C30#0 ×2, C40#0 ×2) | 2 (C30#0) | 20 / 20 |

So the frame class to order 33 has **no** Q-cycle at all. The only sphere Q-cycles known are the two at C30#0, and **neither contains a rigid state**.

### 2.3 Off-sphere Q-cycles with rigid states [data]

`ts_qruns.py` and `ts_qcyc_tait.py` were run on the TrackJ RP² test beds (every 4th graph) and torus/Klein graphs. In the chain-count sense: 3 torus/Klein holes and 5 RP² holes carry Q-cycles (`out/qruns_torusklein.jsonl`, `out/qruns_rp2beds.jsonl`). In the **Tait sense** (components computed in the dual on the surface; word k(H) k(F13) k(F12)):

| surface, graph : hole | L | Tait word along the cycle |
|---|---|---|
| Klein, `klein_s204_w374_t916` : 0 | 20 | 311 211 211 **111** 311 **111** 211 211 311 211 311 211 211 **111** 311 **111** 211 211 311 211 |
| RP², `rp2_s203_w664_t327` : 13 | 20 | 311 211 211 **111** 311 211 311 211 311 211 311 211 211 **111** 311 211 311 211 311 211 |
| torus, `torus_s203_w1012_t380` : 26 | 20 | 321 212 411 311 321 322 … (F13 disconnected at some states: not a Tait Q-cycle) |
| RP², `rp2_s205_w498_t245` : 13, `rp2_s203_w455_t93` : 13, `rp2_s203_w352_t361` : 13 | 20 each | Tait Q-cycles through 111 (`out/tait_offsphere.jsonl`) |
| RP², `rp2_s203_w501_t418` : 2 | 20 | Tait Q-cycle, k(H) ≥ 2 |
| Klein, `klein_s203_w223_t717` : 26 | 20 | chain-count Q only (Tait F13 disconnected at some states) |

So 5 of the 8 off-sphere chain-count Q-cycle holes found carry Tait Q-cycles through **Tait-rigid** states (111): 4 on RP², 1 on the Klein bottle. None is on the torus. On the torus, the one chain-count Q-cycle has F13 Tait-disconnected at some states.
- Random min-degree-5 triangulations, all degree-5 holes, gave **no** all-DL cycle at all (`ts_surfscan.py`): torus, 300 graphs (n = 20–30, 3,623 holes); Klein bottle, 300 graphs (3,905 holes).
- The 1,709 TrackF `torus.txt` triangulations (17,700 holes; `out/qcyc_tait_torus.jsonl`) have no all-DL cycle either.
- So whether orientability alone suffices for Q-escape is open. The torus data are too thin.

On RP² and on the Klein bottle, π-cycles with F12 and F13 Tait-connected at every state pass through **Tait-rigid** states (111). The chain-parity law fails there (consecutive 211 211), so these are not R-cycles. Still, they show that "rigid states avoid Q-cycles" fails off the sphere.

### 2.4 Run lengths [data]

| set | holes | max R-run | max Q-run | R-cycles | holes with a Q-cycle |
|---|---|---|---|---|---|
| sphere, TrackJ notable holes with R-run ≥ 6 (plantri24, frame 30–32) + p33 NR = 8 / NR = 7 holes (`out/qruns_notable.jsonl`) | 120 | 8 | 8 | 0 | 0 |
| torus + Klein (TrackJ `torusklein_graphs.txt`, all holes) | 698 | 6 | **18** | 0 | 3 |
| RP² test beds (every 4th) | 752 | 5 | 17 | 0 | 5 |
| RP² flip-search top graphs (TrackJ R-run 11) | 12 | 11 | 11 | 0 | 0 |

### 2.5 Adversarial sphere search for low-level Q-cycles [data]

`ts_qsearch.py` (TrackJ C engine, TrackF flips, sphere, minimum degree 4) does simulated annealing on

  score = (longest Q-run through a rigid state) + 4·[Q-cycle] + 6·[Q-cycle with min k(H) ≤ 2] + 100·[Q-cycle through a rigid state].

Runs: `run_qsearch.sh`, 45 min from fullerene duals C20–C46 and the Census29 cycle graphs; `out/qsearch2.*`, 30 min seeded at C30#0 and the cycle graphs. Results:
- 14,455 graph evaluations in total.
- 14 logged graphs (`out/qsearch_logged.txt`, re-checked by the Python engine in `out/qsearch_logged_runs.jsonl`).
- The only Q-cycle found is the seed C30#0 (min k(H) = 2).

- A sphere Q-run through rigid states of length **11** was found (`out/qs_rec11.txt`, qs12_2_94 h19, n = 31). Its k(H) word is 2 1 4 1 2 3 2 1 4 1 2 and its N word is 9 8 11 8 9 10 9 8 11 8 9.
- It is not an R-run: its longest R-run is 2. Rigid states can sit in Q-runs with k(H) jumping 1 → 4 → 1.
- No Q-cycle through a rigid state was found.

## 3. The sharpest open sub-claims

**NRC-M (matching form of NRC′; sphere).** Let G be a plane graph with one vertex v of degree 5 and all other vertices cubic. There is no cyclic sequence (M_t)_{t ∈ ℤ/L} of perfect matchings such that, for all t:
- (i) E − M_t is connected, of DL type;
- (ii) M_{t+1} ⊆ E − M_t, with the v-edge advancing −2 notches (so M_{t+1} = M_{t−1} Δ Y_t by S3);
- (iii) M_{t−1} ∪ M_t is a Hamiltonian cycle for every even t.

- NRC-M ⇒ NRC′ ⇒ NRC, by S3 and the chain-parity law. The law makes k(M_t ∪ M_{t+1}) even at odd t, so NRC-M is a little stronger than NRC′: it allows k(H) = 4, 6, … at the odd states.
- §2.1 shows that (iii) cannot be dropped: (i) + (ii) alone are realised on the sphere, at C30#0 with k(H) ∈ {2, 3}.

**Q-escape (sphere; stronger, and surface-sensitive).** No Q-cycle contains a Tait-rigid state. Equivalently, in 𝔇 no DL-type cycle passes through a good matching M_t with M_{t−1} ∪ M_t Hamiltonian.
- Q-escape ⇒ NRC-M ⇒ NRC.
- Sphere data: every Q-cycle found (C30#0 h0, h16) stays at k(H) ≥ 2. The frame census to order 33 and the fullerene duals to C46 have no other Q-cycle.
- False on RP² and on the Klein bottle (§2.3).
- So, like RI, it needs a genuinely spherical input. A Lemma-R-type argument is the natural candidate.
- What the proof must do: show that a Hamiltonian H_t cannot "return" under the flips H ↦ H Δ Y_t (S3c), with the figure-eights Q_t staying connected.

**A lead (speculation, not attempted).** At a rigid state, draw H_t as a circle; the colour-1 edges are then chords, non-crossing inside and outside (TrackH chord model).
- The counts k(H Δ Y) and k(Q_t), k(Q_{t−1}) are cycle counts of products of matchings on the circle. These are computable as 1 + the GF(2)-corank of interlace matrices (Cohn–Lempel type formulas).
- For a cubic graph with a Hamiltonian cycle, planarity is exactly the bipartiteness (inside/outside) of the chord interlace graph.
- Replacing H_t by H_{t+2} = H_t Δ Y_t Δ Y_{t+1} changes the Hamiltonian cycle. On interlace graphs this kind of move acts by pivots (Bouchet; de Fraysseix: bipartite circle graphs = fundamental graphs of planar graphs).
- So NRC-M might become a no-periodic-orbit statement for a pivot dynamics on bipartite circle graphs with corank constraints. That would make the planar input (bipartiteness) explicit, and its failure on RP²/Klein checkable.
- None of this was verified here.

**Why the five Euler/LP attempts stalled, in this language.** S1–S5 contain no Jordan input: they hold on every triangulated surface (S1–S4) or in any graph (S5). The near-rigid alternation is a walk in 𝔇, and 𝔇 has cycles on the sphere (C30#0). The missing input is therefore a statement about **Hamiltonicity of M_{t−1} ∪ M_t** (the P1 trees), not about F12 and F13.

## 4. Candidate potentials and invariants tested (negative) [data]

| idea (brief) | script | result |
|---|---|---|
| α-orientation height. Root the 8 Kempe trees of a rigid state at link vertices (30 admissible role-based root rules, 3 roots of multiplicity 2), orient every tree edge to its root, and orient spokes to make outdegree 3 / 2 / 2 at interior / link / h: a fixed α-orientation of T. Then φ = face potential of O(Φu) − O(u) | `ts_orient.py` | φ mixed-sign at every Φ-step for all 30 rules (p24#596); h-faces not even at a common level. Not a lattice-monotone step |
| region incidences R_a(t) ∩ R_b(t+d) for the regions of Q_t (K, K0, μB) and P1 classes, d = 1, 2 | `ts_regions.py` | no structural zero entry (100 steps, plantri24 notable holes) |
| universal ⊆ / disjointness relations among ~20 named sets of u, π u, π² u (incl. Z) | `ts_relmine.py` | 139 universal cross-state relations, all colour-transport identities (e.g. B_u = A_{u2}, K_u ⊆ J0_{πu}); **none involves Z** |
| order of the far ends of the spokes e0, e1, e3 along H_t at rigid states, transition under Φ | `ts_spokes.py` | all three orders occur; transitions not deterministic; no rotation |
| figure-eight statistics: \|X\|, \|Y\|, M_t-chords inside D_X, D_Y, O, and X–Y chords in O | `ts_fig8stats.py` | parities forced (\|X\| even, \|Y\| odd, #XY-chords odd); no monotone quantity |
| C′ relative to Q_u and Q_c (Φ-steps) | `ts_cprime.py` | C′ meets X and Y of both figure-eights in every instance; no containment |
| Heawood sum S_t = Σ_f ε_t(f) and per-face windings W(f) = Σ_t ε_t(f) on sphere all-DL cycles | `ts_wind.py`, `ts_heawood_cyc.py` | [hand] ε_{t+1} = −ε_t on the switched curves C_t (= X_t in a Q-run) and ε_{t+1} = ε_t elsewhere, so ε_{t+1}(f) is, up to a global sign, the direction in which the matched edge at f turns from M_t(f) to M_{t+1}(f). [data] S_t mod 8 is a function of N_t mod 2 (5 / 1 for even / odd N at n = 24), i.e. F/the chain-parity law. On the 19 cycles, Σ_t S_t ∈ {−132, …, −12}, all ≡ 4 (mod 8) and ≡ 0 (mod 3): a closure constraint automatically met. W(f) ∈ 6ℤ (automatic for L = 20) |
| drawings of a 7-run (p24#596 h20) | `ts_draw.py`, `out/run_p24_596.png` | no visible monotone motion |

Two elementary closure facts [hand], recorded because any rotation argument must respect them. In a closed π-orbit of length L with 3 ∤ L (e.g. L = 10, 20):
- every primal vertex takes the colour α at some state (role phases μ → A → B advance by one step off the swap sets);
- every Tait vertex lies on some switched loop X_t (otherwise its matched edge would rotate monotonically by L/3 turns).

## 5. Exhaustive planar chord model [data]

`ts_chordrun.py` covers all plane cubic multigraphs with one degree-5 vertex carrying a rigid DL state, from the TrackH/TrackI chord-model generator. It iterates π at the Tait level and measures forward R-runs:

| cubic vertices | rigid states | forward R-run lengths | closed orbits |
|---|---|---|---|
| 3, 5, 7 | 1, 3, 14 | all 1 | 0 |
| 9 | 71 | 1 (70), 3 (1) | 0 |
| 11 | 392 | 1 (383), 3 (9) | 0 |
| 13 | 2,308 | 1 (2,239), 2 (2), 3 (67) | 0 |

N = 15 was stopped to free a worker for the search of §2.5.

Runs are too short at these sizes to say much.

## 6. Files

| file | content |
|---|---|
| `ts_lib.py` | runs in R, Φ-steps, sphere face/dart geometry and face potentials |
| `ts_verify.py` | checks V1–V5 of §1 (`TS_TAIT=1` for the Tait hypothesis off the sphere); `out/verify_p24_s25.log` |
| `ts_v5_general.py` | Lemma S5 and Q-cycle flags in arbitrary graphs; `out/v5_general.log`, `out/general_lawcycles.txt` |
| `ts_qruns.py` | longest R-runs / Q-runs / cycles per hole; `out/qruns_*.jsonl` |
| `ts_cyc_q.py` | first version of `ts_qcyc.py` (superseded) |
| `ts_qcyc.py`, `ts_qcyc_tait.py` | all-DL cycles with chain-count / Tait words; `out/qcyc_*.jsonl` |
| `ts_qcheck_c.py` | independent check of the C30#0 Q-cycle with TrackJ's C engine |
| `ts_orient.py`, `ts_regions.py`, `ts_relmine.py`, `ts_spokes.py`, `ts_fig8stats.py`, `ts_cprime.py`, `ts_wind.py`, `ts_heawood_cyc.py`, `ts_draw.py` | the negative experiments of §4 |
| `ts_chordrun.py` | chord-model runs (§5); `out/chordrun15.log` |
| `ts_qsearch.py`, `run_qsearch.sh` | adversarial sphere search for low-level Q-cycles (§2.5); `out/qsearch*.{log,jsonl}`, `out/qsearch_logged.txt`, `out/qs_rec11.txt` |
| `ts_tait_holes.py` | Tait words of all all-DL cycles at given holes (off-sphere table §2.3); `out/tait_offsphere.jsonl` |
| `ts_surfscan.py` | random torus/Klein triangulations, all holes (§2.3); `out/surf_*.{log,jsonl}` |
| `run_qruns.sh` | launch script for the notable-hole scan |

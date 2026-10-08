# Track Q: exact excess of law R-cycles (Part 1) and a component-level attempt on N1 (Part 2)

Studio, 8 Oct 2026, about 06:20 to 08:20 local time. Nothing outside `TrackQ/` was changed and nothing was committed.

Code provenance:
- copied unchanged from TrackP: `tn_eng(.c)`, `tn_lib.py`, `tn_forest.py`, `tn_flow.py`, `tn_verify.py`, `tn_search.py`, `tp_struct.py`, `tp_cyclespace.py`;
- `tn_verify.py` imports TrackH `th_engine` and TrackI `ti_chains` read-only;
- new here: `tq_*.py`, `run_Q*.sh`.

Solvers:
- OR-tools 9.15 (CP-SAT), pip-installed into the local venv `TrackQ/.venv`; nothing system-wide;
- HiGHS through scipy 1.13 `milp` / `linprog`.

Compute: at most 4 processes under `nice -n 10`. Load from other users was 38–57 on 16 cores, so every process ran at about 50 % CPU.

Labels:
- **[exact]**: solver result with an optimality proof from two independent engines/models;
- **[data]**: computation;
- **[hand, unreviewed]**: argument written here and not reviewed.

## 0. Bottom line

1. **Part 1 [exact]: e = 1 is reachable, and e = 0 is not, for these data.** For the three TrackP e = 2 skeletons, I computed the minimum |E(G′ − h)| over **all** graphs G′ carrying the same law R-cycle. "Same" means the same 10 colourings, the same vertex partition of every pair graph at every cycle state, the same hole and link, the link 5-cycle kept, and no link chord.

   | skeleton (lineage) | n | ground set U (admissible pairs) | min e | CP-SAT | HiGHS (mcf MILP) | mcf LP bound |
   |---|---|---|---|---|---|---|
   | n1_7121_17_230_K_L_L (torus, walk 17) | 29 | 156 (78 + 78 addable) | **1** | OPTIMAL 77 = bound 77 (31 s) | Optimal 77, dual bound 77, gap 0 (219 s) | 77.000 |
   | n1_7121_103_1402_K_L (torus, walk 103) | 28 | 128 (75 + 53) | **2** | OPTIMAL 75 = bound 75 (0.3 s) | Optimal 75, gap 0 (25 s) | 75.000 |
   | n1_7221_43_1766_K_L (Klein, walk 43) | 28 | 151 (75 + 76) | **2** | OPTIMAL 75 = bound 75 (2.8 s) | Optimal 75, gap 0 (57 s) | 75.000 |

   - Here e = min |E(G′ − h)| − (3nv − 8), with nv = n − 1. The trivial bound is e ≥ 0, and e = 0 ⇔ every pair graph is a forest at every rigid state.
   - **Certificates.** Two different exact models agree:
     - CP-SAT on an arborescence/MTZ model (`tq_arb.py`);
     - HiGHS on a directed multicommodity-flow model (`tq_mcf.py`).

     Both proved optimality with gap 0. In addition, the **LP relaxation of the flow model already equals the optimum** in all three cases, so the LP value itself certifies the lower bound: an integer optimum is at least ⌈LP⌉. The data files (`out/<name>_data.json`: colourings, parts, ground set) allow an independent re-solve.
   - **Symmetry** was not needed: the largest solve took 31 s with CP-SAT, and warm starts came from the original skeleton.
   - The question "can the minimum e over all graphs with the same colouring data and partitions be computed exactly?" has answer **yes**. The ground set U is exactly the set of edges compatible with all 10 colourings and partitions, so the table above *is* that minimum.
2. **New example: an e = 1 law R-cycle, two-engine verified.** `out/e1_examples.txt`, graph `q_7121_17_230_e1`:
   - n = 29, |E(G − h)| = 77 = 3n − 10, 10-cycle `8989898989`;
   - engine 1 (`tn_eng`): law 10/10, cyc[law] = 10;
   - engine 2 (`tn_verify.py`, TrackH Hole + TrackI nchains): law_all true, Lemma E failing at 10/10 states;
   - class of 22,146 states with 9,904 filled, so G is 4-colourable; 13 edges lie in no triangle.

   Consequences:
   - **TrackP's data conjecture N1⁺ ("every law R-cycle has e ≥ 2") is false.**
   - N1 itself (no law R-cycle with e = 0) survives. It is now tight in the sense that e = 1 occurs.
   - 3 more torus walk-17 skeletons also have exact e = 1: n1_7121_17_{230,330,5}_K_L, by HiGHS MILP with gap 0 (`out/batch_s*.jsonl`).
3. **Other lineages [data].** I evaluated the flow-LP lower bound, which certifies ⌈LP⌉ ≤ e, on 4 law-cycle graphs sampled evenly from each of 12 lineage files: TrackP sphere/torus/Klein example and annealing files, the RP² lineage (TrackN skeletons) and TrackJ rung d. All 26 TrackP e = 2 seeds were included. Results (§1.3):
   - every cycle evaluated has **LP excess ≥ 1**; there is no e = 0 anywhere;
   - LP excess is exactly 1 only in the torus walk-17 lineage;
   - the other lineages give: sphere w15: 2; sphere w14: 3; torus walks 103, 119, 138: 2 (138: LP 1.5); Klein: 2–4; RP² skeleton jc301_81_4369_K: LP 2, against 3 by TrackN/TrackP heuristics.

   N1 holds at fixed partitions in every case evaluated.
4. **Why the e = 2 skeletons stay at 2 [hand + data].** A short identity, valid in any graph, shows that **a non-σ-type in-shape state forces e ≥ 1** (Lemma Q-S, §2.4).
   - n1_7121_103_1402 and n1_7221_43_1766 each have exactly one non-σ state (Z in A_cB_c). Even a 2-state window around that state forces e ≥ 1 locally.
   - The torus walk-17 lineage is σ-type at all in-shape states, and it reaches e = 1.
   - Across 155 law cycles, 1,411 of 1,415 in-shape states are σ-type. The 4 exceptions are those two lineages.
5. **For the σ-type e = 1 cycle, the excess needs ≥ 5 consecutive states [exact + data].** For q_7121_17_230 I recomputed the ground set from a window of states only:
   - every window of 3 consecutive states is exactly realisable with e = 0 (HiGHS MILP, 10/10 windows);
   - windows of 5 states force e ≥ 1 at exactly 2 of 10 starts (MILP-exact, matching the LP), namely starts 2 and 5, windows of 7 at 9 of 10, and windows of 9 at 10 of 10;
   - a deletion-minimal set of **11 connectivity constraints over 5 states** (states 2–6) still forces e ≥ 1 (`out/iis_230_w2_5.log`).

   So the e ≥ 1 obstruction is semi-local: it is invisible to any 3 consecutive states, but appears within 5.
6. **Heuristic N1 attack from the e = 1 graph** (TrackP's f = 3 annealing, partitions free to change; 25 min, 27,592 evaluations): **no example**. Best cycle penalty P ≈ 10.
7. **Part 2 [hand, unreviewed]: no proof of e ≥ 1.** What I obtained:
   - an exact reformulation of law R-cycles as a periodic **three-forest (Z₂²-tension) system**, in which a Kempe step is a switching on the coboundary of one tree of the P2 forest (§2.1);
   - at e = 0, the role cycle P1 → split → P2 → identical → P3 → merge/Γ → P1 for each forest (§2.2);
   - **Lemma Q-L:** at e = 0 the non-α subgraph G[μ ∪ A ∪ B] is a **Laman graph** at rigid states, and Laman + 1 at in-shape states (§2.3);
   - **Lemma Q-S (any graph):** the exact identity β_c(α_cA_c) + β_c(A_cB_c) = #A_cB_c + β_u(αμ) + β_u(μA), plus its mirror (§2.4). It implies: non-σ ⇒ e ≥ 1. So N1 for law cycles reduces to **σ-type law R-cycles with e = 0**;
   - **Lemma Q-G:** Γ_c crosses δK_{t−1} and δK_t, each an even number ≥ 2 of times (§2.5).

   Two no-go facts limit any proof:
   - (i) e ≥ 2 is false, so a proof must use the exact count;
   - (ii) on the sphere, e = 0 R-runs of 7 consecutive states exist (TrackJ), and here every 3-window of the σ-type e = 1 cycle is e = 0-realisable. So an argument that looks at 3 consecutive states cannot work (5 suffice for this data). On the sphere it would need runs of 8 or more, or the closure.

   General-graph steps were checked on 155 law cycles: 2,830 steps and 1,415 in-shape states, 0 failures (§2.6).

## 1. Part 1 [exact] + [data]

### 1.1 The exact problem
Fix a law R-cycle C = (c_0, …, c_{L−1}) of G at hole h. For every state t and colour pair {p,q}, Part(t,p,q) is the vertex partition of G_t[p,q] into components. A graph G′ on the same vertices, with h and its 5 edges unchanged, the link 5-cycle present and no link chord, carries C with the same partitions iff:
- (a) every edge xy of G′ − h is, at every t, properly coloured and inside one part of Part(t, c_t(x), c_t(y)). This defines the ground set U.
- (b) for every t and every part P with |P| ≥ 2, the edges of G′ inside P connect P.

Then the locks, K_t, π, N and the law are unchanged (TrackN `tn_forest.py`, header argument). So min |E(G′ − h)| subject to (a), (b) is the exact minimum excess for this colouring data. Every edge of U lies inside exactly one part at each state, so a rigid state contributes the lower bound Σ_P (|P| − 1) = 3nv − 8.

### 1.2 Models (`tq_arb.py`, `tq_mcf.py`, `tq_exact.py`)
- **CP-SAT (`tq_arb.py cpsat`).** For each state t:
  - two arc literals and one "extra" literal per ground edge, with x_e = a_uv + a_vu + z_e;
  - in every part, in-degree 1 at non-roots and 0 at the root;
  - MTZ levels.

  The arcs form a spanning arborescence of every part, so (b) holds. Conversely, any connected choice admits such arcs: a BFS tree, with z marking the non-tree kept edges. Objective: min Σ x.
- **HiGHS (`tq_mcf.py`).** The same x, plus for each part a fractional arborescence y (in-degree rows) and, for every non-root w, a unit root → w flow bounded by y; x_e = Σ y + z_e with z ≥ 0. This is the directed multicommodity formulation, which is LP-strong.
- `tq_exact.py` (lazy cut generation) is superseded: its cut loop converged too slowly (bound 70 → after 12 rounds, target 77). It is kept only as the reference implementation of the ground set (`build`).

Commands that reproduce Part 1:
```
.venv/bin/python tq_data.py ../TrackP/out/exc2_examples.txt out          # data files
.venv/bin/python tq_arb.py out/<name>_data.json cpsat --workers 3         # engine 1
.venv/bin/python tq_mcf.py out/<name>_data.json [--lp]                    # engine 2 (MILP / LP bound)
.venv/bin/python tq_check.py out/<name>_data.json <solverlog> out/e1_examples.txt <newname>   # rebuild + tn_eng
python3 tn_verify.py out/e1_examples.txt                                   # second engine on the example
```
Logs: `out/min_cpsat_*.log`, `out/min_mcf_*.log`, `out/t1_cpsat.log` (the first e = 1 solution), `out/lp_mcf.log`.

### 1.3 Other lineages [data]
`run_Q3.sh` + `tq_batch.py` (TQ_LPONLY=1): mcf LP bound on the first law cycle of 4 graphs sampled evenly from each file (`out/batch_sample.txt`), plus the 26 TrackP seeds. Each LP took 9–90 s, except the 20-cycle rung-d / RP² graphs, which took up to 600 s. Records are in `out/batch_lp_s*.jsonl`. Exact HiGHS MILP results for 3 seeds are in `out/batch_s*.jsonl`.

| lineage (file) | cycles | input e | LP lower bound on e |
|---|---|---|---|
| TrackP e = 2 seeds, torus walk 17 (`seeds_exc2.txt`) | 9 | 2 | **1** (3 MILP-exact = 1: 230_K_L, 330_K_L, 5_K_L) |
| torus walk 17 annealing examples (`ex_torus_s1`, `an_torus_near` …17_5) | 5 | 12–18 | **1** |
| torus walks 103, 119, 138 (`ex_torus_lineages`) | 3 | 10–14 | 2, 2, 1.5 (⇒ 2) |
| torus annealing walks 110, 138, 20 (`an_torus_near`) | 3 | 15–25 | 2, 1.5 (⇒ 2), 3 |
| sphere w15 (`ex_sphere_w15`, `an_sphere_cyc`) | 4 | 11–20 | 2 |
| sphere w14 (`ex_sphere_batch1`, `ex_sphere_3`) | 4 | 16–18 | 3 |
| Klein walks 29, 43, 74, 89 (`ex_klein_lineages`) | 4 | 12–17 | 3, 2, 2, 4 |
| Klein w34 (`ex_klein_w34`) | 4 | 13–16 | 3 |
| Klein annealing (`an_klein_near`) | 4 | 12–17 | 2.5 (⇒ 3), 3, 3, 4 |
| RP² (TrackN `forest_del`, 20-cycles) | 4 | 3–4 | jc301_81_4369_K: 2; three LPs timed out at 600 s |
| TrackJ rung d (20-cycles) | 3 | 27–33 | jd631_169_1246: 1.67 (⇒ 2); two LPs timed out |

Rows that `tq_batch.py` printed as "LP bound = input excess" with `lp_secs` ≈ 600 are **time-outs**, not results: jd631_169_1246_K, jd632_56_6215_K, jd632_881_6286_K, rung-d jd632_56_6215 and jd632_241_2342. The pass was stopped at 08:15 with the fourth rung-d graph not evaluated. **No cycle has LP bound ≤ 0.**

### 1.4 Heuristic attack from e = 1 [data]
`run_Q4.sh`: TrackP's `tn_search.py` with f = 3, cycle-only objective P = Σ max(0, N − 9) + Σ Lemma-E deviation + law failures, and unrestricted graph moves, so partitions may change. Seeded with `q_7121_17_230_e1`, 25 min, 1 worker: 9 walks, 27,592 evaluations, **0 examples**. The best score 15.1 means a best cycle penalty of about 10, the same kind of near miss as in TrackP §1.5 (`out/an_f3_e1.log`).

### 1.5 Which states force the excess [data] + [exact]
Two versions:
- **global ground set** (`tq_sub.py`): U is admissible for all 10 states, and (b) is imposed on a window only;
- **local ground set** (`tq_local.py`): U and the parts are recomputed from the window's states alone. This asks whether *any* graph carries just those consecutive states with those partitions at excess e.

| instance | window k | local LP e by start state 0..9 | exact (MILP) |
|---|---|---|---|
| 1402 (exact e = 2; state 1 non-σ) | 2 | 1 1 0 0 0 0 0 0 0 0 | – |
| 1402 | 3 | 1 1 0 0 0 0 … | – |
| 1402 | 9 | 2 1.5 1 2 1.5 2 2 2 2 2 | – |
| 230 (exact e = 1; all σ-type) | 2 | 0 ×10 | – |
| 230 | 3 | 0 ×10 | **0 ×10** (MILP, `out/local_230_milp.log`) |
| 230 | 5 | 0 0 1 0 0 1 0 0 0 0 | **0 0 1 0 0 1 0 0 0 0** (MILP) |
| 230 | 7 | 1 1 1 1 1 1 0.5 1 0.5 0 | – |
| 230 | 9 | 1 ×10 | – |

Interpretation:
- In 1402 the excess is caused locally by the single non-σ state (Lemma Q-S).
- In the σ-type cycle 230, no 3 consecutive states see it.
- The deletion-minimal certificate (`tq_iis.py`, window 2–6) uses 11 parts:
  - state 2: AB, μA;
  - state 3: μA, and the 2-vertex αB part (= Z);
  - state 4: μA, αμ;
  - state 5: αB (link part);
  - state 6: both αA trees, AB, μA.

  Connecting just these needs ≥ 77 edges from the 173 admissible ones.
- The global-ground-set LP dual (`tq_dual.py`) spreads over all 10 states (non-unique).

## 2. Part 2 [hand, unreviewed]: component-level attempt on e ≥ 1

Notation as in TrackJ §1.1 and TrackP Part B.
- Colours are elements of Z₂² (four colours = four group elements).
- A state c gives the **tension** τ(uv) = c(u) + c(v) ∈ {g₁, g₂, g₃}, the nonzero elements. τ(uv) names the perfect matching of K₄ that contains the colour pair.
- F_g := τ⁻¹(g).
- For a state with roles (α, μ, A, B), let S_X := α ∪ X. The label g_X := α + X is the one with F_{g_X} = E(S_X) ∪ E(V ∖ S_X) = E ∖ δ(S_X).
- Role labels: P1 = F_{g_μ}, P2 = F_{g_A}, P3 = F_{g_B}.

### 2.1 The three-forest (tension) form (any graph)

**Lemma Q-T1.** For every state:
- the spanning subgraph (V, F_{g_X}) is the disjoint union of the pair graphs G[α, X] and G[Y, W];
- hence N = Σ_g k(V, F_g) and B = Σ_g β(V, F_g), where k counts components and β is the cycle rank;
- Lemma P1 is Σ_g (nv − |F_g|) = 3nv − |E|.

*Proof.* An edge inside S_X joins α to X, because each colour class is independent; an edge inside V ∖ S_X joins Y to W; every other edge crosses δ(S_X). ∎

**Lemma Q-T2 (Kempe step).** A Kempe swap on a component K of G[α, A] is c ↦ c + g_A·1_K, so τ ↦ τ + g_A·δK. Then:
- K is the vertex set of a component of (V, F_{g_A}) lying in S_A, and δK ∩ F_{g_A} = ∅;
- F_{g_A} is unchanged;
- on δK the other two labels are exchanged; every other edge keeps its label.

*Proof.* δ(1_K) = δK. An edge leaving K is not labelled g_A, since otherwise its far end would lie in K. ∎

**Corollary Q-T3 (role rotation, J2 in forest form).** Along π, (P1, P2, P3)(t + 1) = (P3, P1, P2)(t) as labels. So:
- the P2 forest at t is the P3 forest at t + 1, with the same edge set and components;
- the P1 and P3 forests at t exchange exactly δK_t, becoming P2 and P1 at t + 1;
- |δK_t ∩ F_{P1}(t)| − |δK_t ∩ F_{P3}(t)| = |F_{P1}(t)| − |F_{P2}(t + 1)|. This is TrackP's cut balance; it equals 1 at e = 0.

**The cut picture.** δ(S_A) = F_{g_μ} ∪ F_{g_B} is bipartite between S_A and V ∖ S_A = μ ∪ B. Write s(v) ∈ {0, 1} for v ∈ α/A and for v ∈ μ/B. Then an edge xy of δ(S_A) is in F_{g_μ} iff s(x) = s(y). The step toggles s on K. So a Kempe step is a *switching* of a vertex-signed bipartite graph, on one tree of G[S_A].

### 2.2 The e = 0 role cycle

At e = 0, B = 0 at rigid states and B = 1 at in-shape states (TrackP B1). With the counts of J1/J3 and Lemma S (Lemma E holds at every state when e = 0), the forests by role are:

| state | P1 | P2 | P3 |
|---|---|---|---|
| rigid u | 2 trees: G[S_μ], G[V∖S_μ] | 3 trees: K, K₀, μB | 3 trees: two αB, μA |
| in-shape c | 3 components, one cycle Γ_c (in A_cB_c), with Z and the αμ link tree | 3 trees | 3 trees |

So **each forest F_g runs through the 6-state cycle**:
- P1 (2 trees, rigid) → split → P2 (3, in-shape) → identical → P3 (3, rigid) → +1 edge, gains Γ → P1* (unicyclic, in-shape) → loses Γ → P2 (3, rigid) → identical → P3 (3, in-shape) → merge → P1 (2 trees).
- Edge counts: nv − 2, nv − 3, nv − 3, nv − 2, nv − 3, nv − 3.
- **The P1 role, and with it the one net "spare" edge, rotates through the three forests:**
  - at a rigid→in-shape step the P1 forest splits (2 → 3 trees) and the P3 forest gains Γ;
  - at an in-shape→rigid step the P1* forest loses Γ and the P3 forest merges (3 → 2: the merge of the αA trees K, K₀ by K′).

Over L = 10 steps, the monodromy ρ (P2 of TrackP) moves every label. With the role cycle of period 3 per label this is consistent, since 10 ≡ 1 (mod 3) and ρ(g_μ) = g_B. **No contradiction arises at this level.**

### 2.3 Lemma Q-L (Laman structure at e = 0)
**Lemma Q-L.** Suppose all three non-α pair graphs are trees at a state; at e = 0 this holds at every rigid state. Then H := G[N], N = μ ∪ A ∪ B, satisfies |E(H)| = 2|N| − 3 and |E(H[W])| ≤ 2|W| − 3 for every W ⊆ N with |W| ≥ 2. So H is a **Laman graph** (generically minimally rigid in the plane).

At an in-shape state with e = 0, H has 2|N| − 2 edges, and its only bichromatic cycle is Γ_c. H is "Laman + 1": a single redundant edge.

*Proof.*
- E(H) is the disjoint union of the three pair graphs μA, μB, AB, which are trees on |μ| + |A| − 1, … vertices. Summing gives 2|N| − 3.
- For W: restricting a tree to W leaves a forest. A pair {X, Y} meeting W contributes at most |W ∩ (X ∪ Y)| − 1 edges, and a pair missing W contributes 0.
- If W meets at least two colours, all three pairs meet W, giving at most Σ |W ∩ pair| − 3 = 2|W| − 3.
- If W meets one colour, it spans no edge. ∎

Remark: the α-side is the bipartite graph between α and N with 3|α| + |N| − 5 edges, a union of the three α-pair forests (1, 2, 2 trees). So G − h itself is (3,3)-sparse with |E| = 3nv − 8 (Nash-Williams). A Kempe step swaps K_α into N and K_A out of N, keeping H "Laman (+1)". **A Henneberg-type invariant of H along a periodic orbit is the most promising component-level lead, but I could not close it.**

### 2.4 Lemma Q-S (σ-type and excess; any graph)
**Lemma Q-S.** Let u be rigid, c = π(u) DL with N(c) = 9, and suppose P2(c) has the chain counts (2,1); this holds at every in-shape state by J3. Then, with roles taken in each state's own frame,

  β_c(α_cA_c) + β_c(A_cB_c) = #A_cB_c + β_u(αμ) + β_u(μA).

Mirror form, at u′ = π(c) rigid: β_c(α_cB_c) + β_c(A_cB_c) = #A_cB_c + β_{u′}(αμ) + β_{u′}(μB).

Consequently, if the extra chain Z of an in-shape state c lies in A_cB_c (c is not σ-type), then B(c) ≥ 2. For a law R-cycle (B(c) = e + 1, TrackP B1) this gives **e ≥ 1**.

*Proof.*
- Star identity (TrackL St) for the swap K_{αA}(x_{j+2}) at u, with third colour μ: χ_c(μα) + χ_c(μA) = χ_u(μα) + χ_u(μA).
- In c's roles, {α, μ} = α_cA_c and {μ, A} = A_cB_c (TrackL §2.1).
- Write χ = # − β. At u, #αμ = #μA = 1 (rigid); at c, #α_cA_c = 2 (J1/J3). Substituting gives the identity.
- The mirror form follows from π⁻¹ = π̃ (the swap of K_{αB}(x_j)) by the symmetry A ↔ B.
- If Z ⊂ A_cB_c, then #A_cB_c = 2, so B(c) ≥ β_c(α_cA_c) + β_c(A_cB_c) ≥ 2. ∎

This is TrackL's Lemma S argument with Lemma E replaced by the identity P1. It is valid in **any** graph, needs no Euler input, and is exact rather than an inequality. **So N1 for law cycles reduces to σ-type law R-cycles** (Z ⊂ α_cμ_c at every in-shape state). The e = 1 example is σ-type throughout. In 1402 / 1766 the single non-σ state costs one unit, which a 2-state window already sees (§1.5).

### 2.5 Lemma Q-G (Γ crosses both swaps)
**Lemma Q-G.** At e = 0, let c be in-shape with predecessor u = π⁻¹c and successor u′ = πc. Then:
- Γ_c contains an even number ≥ 2 of edges of δK_u, all of which lie in F_{P1}(u) (α–μ edges at K_α);
- Γ_c contains an even number ≥ 2 of edges of δK_c;
- every vertex of Γ_c ∩ K_u is a former α-vertex of K_u, and both of its Γ_c-edges lie in δK_u;
- Γ_c ∖ δK_u is a union of paths in the μA tree of u.

*Proof.*
- F_{P1}(c) = (F_{P3}(u) ∖ δK_u) ∪ (δK_u ∩ F_{P1}(u)) by Q-T3. F_{P3}(u) is a forest, so Γ_c uses an edge of δK_u ∩ F_{P1}(u).
- A cycle meets a cut δK in an even number of edges.
- No edge inside K_u lies in F_{P1}(c), because edges inside K are labelled g_A. So a vertex of Γ_c in K has both of its Γ-edges in δK.
- The second item is the same argument at c → u′, since F_{P2}(u′) is a forest. ∎

The degree form of this, Σ_{K_α}(d_μ − 1) = Σ_{K_A}(d_μ − 1) + 1, is the star identity again (TrackP B3). **So Q-G adds position information but no new count.**

### 2.6 Data checks (`tq_forest_check.py`, `out/forest_check.log`)

Coverage: 155 law cycles, 2,830 π-steps:
- 85 TrackN RP²-lineage skeletons;
- 43 TrackJ rung-d graphs;
- the 26 TrackP e = 2 seeds;
- the new e = 1 graph.

| check | content | instances | failures |
|---|---|---|---|
| T1 | N = Σ_g k(F_g); B = Σ_g β(F_g) | 2,830 | 0 |
| — | π step recomputed (swap of K_{αA}(x_{j+2})) = next state up to renaming | 2,830 | 0 |
| T2 | K_t is a component of F_{g_A} inside S_A; δK ∩ F_{g_A} = ∅; labels flip on δK only | 2,830 | 0 |
| T3 | P2 forest at t equals P3 forest at t + 1 (edge sets) | 2,830 | 0 |
| T4 | component counts by role: rigid (2,3,3), in-shape (3,3,3) | 2,830 | 0 |
| T5 | P1(t) ∪ P3(t) = P1(t + 1) ∪ P2(t + 1); cut balance |δK ∩ P1| − |δK ∩ P3| = |P1(t)| − |P2(t + 1)| | 2,830 | 0 |
| T6 | every cycle of a fundamental basis of F_{P1}(c) not inside F_{P3}(u) meets δK_u | 6,004 | 0 |

Cycle ranks by role at e = 1 (`q_7121_17_230_e1`):
- rigid (P1,P2,P3) = (0,0,1) ×3, (1,0,0), (0,1,0);
- in-shape (2,0,0) ×2, (1,1,0) ×2, (0,1,1).

The single spare cycle wanders through all three forests and through both α- and non-α pair graphs (`tq_roles.py`).

Lemma Q-S (`tq_ztype.py`, `out/ztype.log`): both identities hold at 1,415 / 1,415 in-shape states of the 155 cycles. Z lies in α_cμ_c at 1,411 of them and in A_cB_c at 4, namely the 1402 lineage (3 cycles) and 1766.

### 2.7 Status
**N1 is not proved.** The obstruction to a proof is now sharper:
- (a) **e ≥ 2 is false** (§0.2), so a proof must use the exact count 3nv − 8.
- (b) **Non-σ cycles are disposed of** (Lemma Q-S). The open case is σ-type law R-cycles.
- (c) **Locality.** For the σ-type e = 1 cycle, every 3 consecutive states are exactly realisable at e = 0, and the obstruction first appears in a 5-state window, through 11 connectivity constraints (§1.5).
  - On the sphere, e = 0 R-runs reach 7 states (TrackJ), and the maximum grows with order (TrackO).
  - So an argument has to combine at least 5 consecutive steps, and on the sphere it must use runs of ≥ 8 or the closure (monodromy ρ moves every label, TrackP P2).
- (d) **Consistency.** Euler, degree and cut-balance quantities, Lemma Q-S, and the role cycle of §2.2 are all consistent with e = 0.

The leads I would pursue:
1. **The 11-constraint certificate of §1.5 is instance-specific.** No universal lemma about ≤ 7 consecutive states can force e ≥ 1, because e = 0 sphere R-runs of length 7 exist. So a universal argument has to use ≥ 8 consecutive states or the closure, together with monodromy ρ. One concrete test: is the window length at which e ≥ 1 first appears bounded over all σ-type law cycles? Here it is 5.
2. **A Laman/Henneberg potential on H_t** (§2.3): the 2D-rigidity rank of the non-α graph is tight at every rigid state at e = 0, and Kempe steps move K_α in and K_A out.
3. **LP duality.** The flow LP is tight on every instance computed (3/3 exact). A universal dual certificate built from partition inequalities over the whole orbit would prove N1 at fixed partitions.

## 3. Files
| file | content |
|---|---|
| `tq_exact.py` | ground set / parts (`build`), lazy-cut HiGHS loop (reference only), LP separation |
| `tq_data.py` | extract data files `out/<name>_data.json` from graph lines (first law cycle) |
| `tq_arb.py` | exact CP-SAT (and HiGHS) arborescence/MTZ model |
| `tq_mcf.py` | exact HiGHS multicommodity-flow model; `--lp` for the LP bound |
| `tq_check.py` | rebuild G′ from a solver edge set and check it with `tn_eng` |
| `tq_batch.py` | LP / MILP excess over many law cycles (dedup by partitions) |
| `tq_sub.py`, `tq_window.py` | excess forced by subsets of states (fixed / window ground set) |
| `tq_dual.py` | LP dual split by state |
| `tq_roles.py` | per-state pair-graph components / cycle ranks in role order |
| `tq_forest_check.py` | Part 2 checks T1–T6 |
| `tq_ztype.py` | location of Z at every 9-state; Lemma Q-S identity and mirror |
| `tq_local.py` | excess of windows of consecutive states with local ground set (LP / `--milp`) |
| `tq_iis.py` | deletion-minimal set of parts forcing e ≥ 1 in a window |
| `out/local_*.log`, `out/local_230_milp.log`, `out/iis_230_w2_5.log`, `out/sub_1402.log` | window experiments (§1.5) |
| `out/ztype.log`, `out/forest_check.log` | Part 2 data checks |
| `out/batch_sample.txt`, `out/batch_lp_s*.jsonl`, `out/batch_s*.jsonl` | lineage pass (§1.3) |
| `out/an_f3_e1.*` | annealing from the e = 1 graph (§1.4) |
| `run_Q1.sh` … `run_Q4.sh` | launch scripts actually used (Q1's HiGHS-MTZ half was stopped after 20 min and replaced by `tq_mcf.py`; Q2 superseded by Q3) |
| `out/e1_examples.txt` | the e = 1 law R-cycle graph |

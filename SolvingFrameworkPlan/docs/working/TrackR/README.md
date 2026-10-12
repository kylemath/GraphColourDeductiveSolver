# Track R: looking for a universal dual certificate for N1, and testing the Laman lead

Studio, 8 Oct 2026, about 08:20–10:40 local time. Nothing outside `TrackR/` was changed and nothing was committed.

Code reuse (read-only):
- TrackQ: `tq_exact.build` (ground set and parts), `tq_roles.roles`, `tn_forest`, `tn_lib` + `tn_eng`;
- the venv `TrackQ/.venv` (scipy 1.13 / HiGHS, OR-tools 9.15).

Everything else is new here: `tr_*.py`, `run_*.sh`.

Compute: at most 4 processes, all under `nice -n 10`. Load from other users was about 33 on 16 cores.

Labels:
- **[exact]**: LP optimum, re-verified with rational arithmetic;
- **[data]**: computation;
- **[hand, unreviewed]**: argument written here and not reviewed.

## 0. Bottom line

1. **The flow-LP dual has a clean edge-price form, and its certificates check exactly** (§1, Lemma R1).
   - A certificate is a price matrix u_{t,e} ≥ 0 over (cycle state, admissible pair) with Σ_t u_{t,e} ≤ 1. It gives |E(G′ − h)| ≥ 5 + Σ_t Σ_P MST_P(u_t).
   - At L1-minimal optima the prices are mostly **0/1**. That is an *edge-disjoint packing of partition inequalities*: each admissible pair is "charged" to at most one state (Lemma R2).
   - Every LP value of TrackQ was reproduced by an independent method (Kelley cutting planes on spanning trees), and every certificate was re-verified in exact rationals. Data: 14 cycles, plus windows.
2. **No universal dual pattern was found. The evidence is against one existing in the natural vocabulary** (§3). Each of the following certifies **nothing**, i.e. the restricted LP optimum is exactly e ≥ 0, on the σ-type e = 1 lineage (torus walk 17):
   - (a) prices that depend only on an edge's **colour/label (pair-role) trajectory**, even over all 10 states and even when each state gets its own prices;
   - (b) partition inequalities built from **meets of structural partitions**: the pair-graph components of other states, and the swap sets K_s, up to 3-fold meets;
   - (c) **rotation-equivariant prices**: one rule applied at every state, depending on N(t) and the edge's universal *part tags* (which tagged chain it lies in) at t−r … t+r, for any r up to the full cycle.

   One structural fact explains (c): **the link-tag word is the same at every state of every law R-cycle** (§3.4).
   - The 8 link chains always carry the tags am:012, AB:34, aA:0, aA:23, mB:14, aB:04, aB:2, mA:13. This holds at 2,240 / 2,240 states, and it is forced by DL plus the chain counts [hand].
   - So the structural objects (trees of the P1/P2/P3 forests, lock paths, K_t, Z) give **no phase information** along the orbit, and a canonical template built from them would be equivariant. Such templates certify nothing (c).
3. **What does work** [exact, data]: *state-specific* prices that depend on an edge's part tags at t−1, t, t+1.
   - These certify e ≥ 1 on all 14 cycles: exact rational bounds between 1/3 and 2.
   - With t±2 they recover ⌈LP⌉ on 11 of 14.
   - A single shared rule, anchored at one chosen state per cycle, certifies all 5 σ-type 10-cycle lineages jointly (exact bound 1/3 each).
   - But **leave-one-lineage-out fails in 4 of 5 lineages** (§3.5). The rule fits each lineage's admissible-pair structure; it does not generalise. This is the strongest negative evidence that the certificate is instance-specific.
4. **Span** [exact]. With the global ground set, the shortest window of consecutive states whose connectivity constraints already force e ≥ 1 is:
   - **5 for every σ-type cycle tested**: torus 17, torus 138 and both sphere w15 cycles (2656, 3104);
   - **2 for every non-σ cycle**, which is Lemma Q-S.
   - Exception: σ-type torus 119_1473 also has a 2-window, at the in-shape state whose link-free α_cμ_c part has 11 vertices.
   - 5-window certificates are 0/1 packings of 13–16 partition inequalities.
5. **No hand lemma of the requested universal form was found.**
   - What I can state [hand, unreviewed, elementary]: the certificate form (Lemmas R1/R2), and the tag-word lemma (§3.4) that underlies the no-go (c).
   - I cannot state "for any graph carrying a σ-type law R-cycle with these partitions, the following weighted sum of cut constraints gives |E| ≥ 3nv − 7". The data say that weighted sum has to look at which admissible pairs exist, in a way that changes from lineage to lineage.
6. **Laman / Henneberg lead: negative** (§4).
   - On 31 sphere π-runs of length 6–7 inside R (e = 0, 155 interior states) and on the law cycles:
     - H_t = G[non-α] is **generically rigid at every state** (dof 0);
     - its redundancy is 0 at rigid and 1 at in-shape states;
     - H_t ∪ H_{t+1} is rigid and H_t ∩ H_{t+1} is independent at every step.
   - So every rigidity-rank quantity is pinned by the cycle-rank counts that are already known (P1 / Q-L). The Henneberg balance 2(|K_α| − |K_A|) − Δ|E(H)| is just ±1 alternating, which is the star identity again.
   - The vertex count |α_t| is not monotone (non-monotone on 23 / 31 runs).
   - A rank-level Henneberg potential therefore cannot separate e = 0 from e ≥ 1. Any potential would have to be component-level, the same conclusion as (2).

## 1. The certificate form [hand, unreviewed; elementary]

Data of a law R-cycle (TrackQ §1.1):
- states t = 0..L−1;
- for each t, the parts P: vertex sets of pair-graph components with |P| ≥ 2;
- ground set U: pairs that, at every state, are properly coloured and lie inside one part;
- forced link edges F (|F| = 5).

**Lemma R1 (price form).** Let u_{t,e} ≥ 0 (t a state, e ∈ U ∖ F) satisfy Σ_t u_{t,e} ≤ 1. Then every G′ carrying the data satisfies

  |E(G′ − h)| ≥ 5 + Σ_t Σ_P MST_P(u_t),

where MST_P(u_t) is the minimum u_t-weight of a spanning tree of P using U-edges inside P.

*Proof.* Let x = 1_{E(G′)}. Then |E(G′ − h)| − 5 = Σ_{e ∉ F} x_e ≥ Σ_t Σ_e u_{t,e} x_e. At each t, the parts are disjoint and E(G′) contains a spanning tree of each part, so Σ_e u_{t,e} x_e ≥ Σ_P MST_P(u_t). ∎

The maximum over u equals the TrackQ mcf LP value. The two are Lagrangian duals, and the per-state spanning-forest polytope is integral.

**Lemma R2 (packing form).** Take 0/1 prices, i.e. assign each pair e ∈ U to at most one state τ(e). Then

  |E(G′ − h)| ≥ 5 + Σ_t Σ_P (k_{t,P} − 1),

where k_{t,P} is the number of components of P in the graph of U-edges *not* assigned to t, with link edges contracted.

Equivalently: a family of partition inequalities "x(δ(π)) ≥ |π| − 1" whose crossing sets in U are pairwise disjoint can simply be added up. ∎

In both forms, N1 at fixed partitions is the statement "some u gives a value > 3nv − 8", and the integer bound then gives 3nv − 7.

Implementation:
- `tr_lag.py` solves max_u by Kelley cutting planes: each cut is a spanning tree, and separation is Kruskal.
- It then picks an L1-minimal optimal u and checks the bound in exact rationals (`verify`).
- `tr_show.py` decomposes u into the partition inequalities it uses (Kruskal levels).

## 2. Data [exact]

### 2.1 Full-cycle certificates (`run_full.sh`, `out/full_*.json|log`)

| cycle (lineage) | σ-type | L | LP e (= TrackQ) | exact certificate | L1-min price values |
|---|---|---|---|---|---|
| n1_7121_17_230_K_L_L / _5 / q_…_e1 (torus 17) | yes | 10 | 1 | 77 = base + 1 | 0, ½, 1 (222 halves) |
| n1_7121_138_352 (torus 138) | yes | 10 | 3/2 | 155/2 | 0, ½, 1 |
| n1_7121_119_1473 (torus 119) | yes | 10 | 2 | 75 | ½, 1 |
| n1_7511_15_2656, _3104 (sphere w15) | yes | 10 | 2 | 81 | 0/1 |
| jc301_81_4369_K (RP², TrackN) | yes | 20 | 2 | 81 | 0/1 |
| n1_7121_103_1402_K_L (torus 103) | no | 10 | 2 | 75 | 0/1 |
| n1_7221_43_1766_K_L, _1416 (Klein 43) | no | 10 | 2 | 75 | 0/1 |
| n1_7221_153_2544 (Klein w34) | no | 10 | 3 | 76 | 0/1 |
| n1_7221_194_1376 (Klein ann.) | no | 10 | 5/2 | 151/2 | 0, ½, 1 |
| n1_7511_14_2004 (sphere w14) | no | 10 | 3 | 88 | 0/1 |

Notes:
- The rows have "non-σ" = an A_cB_c link-free part at some in-shape state (`tr_ztag.py`, `out/ztag.log`).
- The jc301 LP had timed out in TrackQ; here it solves in under 5 min (284 s of Kelley iterations).
- Every row is a verified rational certificate.

### 2.2 Span: shortest window with e ≥ 1 forced (`tr_span.py`, `out/span_*.log`)

Global ground set U (admissible at all states), connectivity imposed at k consecutive states only:

| cycle | min k | starts (of 10) that work at min k | at k = 6 |
|---|---|---|---|
| torus 17 (230, 5) | 5 | 2, 5 | 8 / 10 |
| torus 138_352 | 5 | 2, 5, 6 | 8 / 10 |
| sphere w15 2656 | 5 | 8 | – |
| sphere w15 3104 | 5 | 8 | – |
| torus 119_1473 (σ, but one in-shape state has an 11-vertex link-free α_cμ_c part) | 2 | 1 | – |
| all non-σ | 2 | the windows covering the A_cB_c state | – |

The 5-window certificates are integral. For example, 230 window 2–6 uses 13 partition inequalities with disjoint crossing sets, value 72 + 5 = 77 (`out/show_gw_230_2.txt`, `out/gw_*.json`).

## 3. Universality tests

All of these are LPs of the form of Lemma R1 with *tied* prices: u_{t,e} = f(key(t,e)). Keys are computed by `tr_rule.py`, and the optimum is found by Kelley iteration with exact re-verification. The "part tag" of an edge at state s is the pair name of the chain it lies in at s, plus the frame-relative positions of the link vertices of that chain ('Z' if link-free).

### 3.1 Label / colour trajectories: no certificate [exact]
Key = (t, pair names of e at t−r … t+r):
- for 230, `pairT` gives LP = base for r = 0, 2, 5; r = 5 is the full trajectory (54 distinct classes);
- adding cut-by-K_s flags (`pairKT`) also gives base;
- a sanity check with key ∋ edge id recovers e = 1.

So **no certificate can price admissible pairs by how they are coloured along the orbit.** It must distinguish pairs with identical colour histories by *which chains* they lie in.

### 3.2 Meets of structural partitions: no certificate [exact]
`tr_family.py` uses columns (t, P, P ∧ M), where M is a meet of ≤ 1, 2 or 3 of:
- the role-partitions Π(s, R): components of the two role-R pair graphs at another state s;
- the swap splits {K_s, V ∖ K_s}.

Crossing sets are taken in U. Results for 230:
- window 2–6: 234 / 463 / 473 columns at depth 1 / 2 / 3, LP excess 0;
- full cycle, depth 2: 4,316 columns, LP excess 0.

`tr_explain.py` confirms that the blocks of the actual certificates are not such meets: 2–5 of 13–16 terms are explained, and those are mostly singleton partitions.

### 3.3 State-specific part-tag prices: certificates everywhere [exact]
`tr_rule.py R partT`, with key = (t, N(t), part tags of e at t−R … t+R). Logs: `out/rule_*_r1_partT.log`, `out/rule_*_r2_partT.log`.

| cycle | R = 1 | R = 2 | LP |
|---|---|---|---|
| torus 17 (230, 5, e1) | 1/2 | 1 | 1 |
| torus 138_352 | 1/3 | 1 | 3/2 |
| torus 119_1473 | 1 | 2 | 2 |
| sphere w15 2656 / 3104 | 1/2 / 1/2 | 1 / 3/2 | 2 |
| RP² jc301 | 3/2 | 2 | 2 |
| non-σ cycles (6) | 1–2 | 2–3 | 2–3 |

So the partition structure of 3 consecutive states (the chains each edge lies in at t−1, t, t+1) supports a certificate everywhere. But the prices must vary with t: restricted to any 5 or 6 consecutive states, the R = 1 rule gives 0 (`--states`). The R = 1 certificate uses the whole cycle.

### 3.4 Rotation-equivariant prices: no certificate on the critical lineage [exact] + tag-word lemma [hand]

`tr_rule.py R part`, with key = (N(t), part tags at t−R … t+R): the same rule at every state.

| cycles | result |
|---|---|
| torus 17 (230, 5, e1), torus 138_352, torus 119_1473, RP² jc301 | **0** for R = 2 and R = 5 (full trajectory) |
| others | 0.2–1 |

**Tag-word lemma [hand, unreviewed; data 2,240 / 2,240 states, `out/tagword_all.txt`].** At every DL state of a law R-cycle, the link chains carry exactly the tags

  am:012, AB:34, aA:0, aA:23, mB:14, aB:04, aB:2, mA:13.

*Proof.* Link (α, μ, α, A, B) at x_j … x_{j+4}.
- **am:012, AB:34, aB:04 and the "23" of aA:23** come from the link edges x_jx_{j+1}, x_{j+1}x_{j+2}, x_{j+3}x_{j+4}, x_{j+4}x_j and x_{j+2}x_{j+3}.
- **x_j ∉ K_{αA}(x_{j+2}) and x_{j+2} ∉ K_{αB}(x_j)** are the two locks (DL).
- **x_{j+1}, x_{j+4} share a μB chain, and x_{j+1}, x_{j+3} share a μA chain**, because #μB = #μA = 1:
  - at rigid states this is the count (1,1,2,1,2,1);
  - at in-shape states it follows from (#αA, #μB) = (#αB, #μA) = (2, 1) (J3). ∎

**Consequence.** The tagged chains are the natural universal objects: the P1/P2/P3 trees, K_t = aA:23, lock chains aA:0 and aB:2, Z = am:Z. They look the same at every state. A certificate template built only from them, without choosing a distinguished state from other data, is therefore equivariant in the sense of 3.4. The table shows that no such certificate exists for the e = 1 lineage, even with full trajectories.

### 3.5 Anchored shared rules: fit, but do not generalise [exact]

Key = (N(t), offset t − a, part tags at t−2 … t+2), with one anchor a per cycle. The rule is shared across cycles (`tr_rule.py 2 partA`, `tr_greedy.py`, anchors restricted to the same state type).

- A single rule certifies all 5 σ-type 10-cycle lineages jointly: 230@0, 138_352@0, 3104@4, 2656@4, 1473@2 and 127_2225@8. The exact bound is 1/3 for each (`out/rule_train6_r2.json`).
- Applied to the 14 distinct σ-type 10-cycles extracted from all TrackP example files (`data2/`, 45 distinct data sets): 13 / 14 get e ≥ 1/3. The exception is 138_1277, which gets 0.
- **Leave-one-lineage-out** (`run_lolo.sh`, `out/lolo.log`): a rule trained without lineage X, applied to X at its best anchor, gives

  | held-out lineage | bound on the held-out cycles |
  |---|---|
  | torus 17 | 1/3 ✓ (its tag skeleton is 99.5 % shared with torus 138) |
  | torus 138 | −4/3 … 0 |
  | sphere w15 | −14/3, −10/3 |
  | torus 119 | −26/3, −8 |
  | torus 127 | −203/22 … −90/11 |

  A first rule trained on 4 lineages failed on 127 in the same way (`out/apply_train5_r2.log`).

So the shared rule memorises lineages; it is not a universal pattern. Key-sharing between lineages is 84–100 % (`out/share_*.log`), so the rule is not trivially decoupled. It simply has enough freedom (618–678 keys) to fit the cycles it has seen.

### 3.6 Verdict on (1)–(2) of the task
No universal dual pattern. The LP certificate exists in every case. The parts of it that can be expressed structurally are always present:
- the trees and chains, K_t, the locks and Z (as tags);
- the role partitions and their meets;
- label trajectories.

But on their own these certify nothing for the σ-type e = 1 lineage. The certificate needs, in addition, the fine structure of the admissible-pair graph U inside each chain, i.e. which pairs are co-located in the same chains at all 10 states. This is not governed by any rule I could find that transfers between lineages.

The honest reading:
- the σ-type obstruction found by the exact LP is real, two-engine verified, and at least 5 states long;
- but it is a property of each orbit's chain *geometry*, not of the chain *combinatorics* (tags, counts, roles).

A proof would need a statement about that geometry, which is again Jordan-level or component-level. This is the same wall as TrackP B4 and TrackQ §2.7.

## 4. Laman / Henneberg lead (`tr_laman.py`)

Setup:
- H_t = G[N_t] with N_t = μ ∪ A ∪ B, on G − h;
- r2 = generic 2D rigidity rank, computed from a random realisation, 2 trials;
- red = |E(H)| − r2; dof = 2|N| − 3 − r2.

**Sphere π-runs inside R** (e = 0; from TrackJ's `sphflip.jsonl`): 31 runs of length 6–7 in 30 graphs (`out/laman_sphere.log`, `out/laman_sphere_summary.txt`).
- At all 155 rigid / interior in-shape states: dof = 0. red = 0 at rigid states and 1 at in-shape states. This is Q-L (Laman, Laman + 1) confirmed on real e = 0 data.
- At all 156 steps: H_t ∪ H_{t+1} is rigid, and H_t ∩ H_{t+1} is independent.
- Run-end in-shape states with a non-σ extra chain have |E(H)| = 2|N| − 4 and dof = 1.
- |α_t| is non-monotone on 23 / 31 runs; the 8 monotone ones are short.
- Henneberg balance hb = 2(|K_α| − |K_A|) − (|E(H_{t+1})| − |E(H_t)|) is ±1 alternating. That is the star identity (TrackP B3).

**Law cycles** (e = 1, e = 2): H_t is rigid at every state, red is 0–2, and the spare cycle wanders between H and the α-side. Nothing is monotone, as it must be on a cycle.

**Verdict.**
- At e = 0 every rank-level rigidity quantity of H_t, and of consecutive unions and intersections, is *determined* by the forest counts. So it carries no information beyond identity P1 and Lemma Q-L. It cannot change monotonically along an e = 0 orbit, because it is constant there.
- A Henneberg-type potential would have to track *which* vertices and edges enter and leave, e.g. a Henneberg *sequence* or ordering. That is component-level information, the same kind §3 shows a certificate needs.
- I found no such potential, and I do not recommend the rank-level Laman lead further.

## 5. Files

| file | content |
|---|---|
| `tr_lag.py` | Lemma R1 LP (Kelley on spanning trees), L1-normalised optimum, exact rational verification; `--window` (local ground set) / `--gwindow` (global ground set) |
| `tr_show.py` | decompose a certificate into partition inequalities (Kruskal levels) |
| `tr_span.py` | shortest window of consecutive states forcing e ≥ 1 (global ground set) |
| `tr_rule.py` | tied-price LPs: `pair`/`role` (label trajectories), `part` (tag trajectories), flags `T` (state-specific), `K`, `A` (anchored), `E` (sanity); joint over several cycles; exact verification |
| `tr_family.py` | dual restricted to meets of structural partitions |
| `tr_explain.py` | express a certificate's partitions as meets of structural partitions |
| `tr_overlap.py`, `tr_share.py`, `tr_greedy.py`, `tr_apply.py` | anchored-rule overlap, key sharing, greedy joint fit, application of a fixed rule to new cycles |
| `tr_tagword.py`, `tr_ztag.py` | link-tag word per state; σ-type classification from data |
| `tr_laman.py` | rigidity quantities along law cycles and sphere π-runs |
| `run_full.sh`, `run_rule.sh`, `run_anchor.sh`, `run_lolo.sh` | launch scripts used |
| `data/` | 14 cycle data files: 3 from TrackQ, 11 extracted by `tq_data.py` from TrackQ's `batch_sample.txt` and `e1_examples.txt` |
| `data2/` | 209 TrackP example / seed graphs → 45 distinct cycle data sets (`index.json`, `sigma_list.txt`) |
| `out/full_*`, `out/gw_*`, `out/w230_*` | certificates (JSON: rational prices) and logs |
| `out/span_*.log`, `out/rule_*.log`, `out/anchor_*.log`, `out/joint_*.log`, `out/lolo.log`, `out/apply_*.log`, `out/share_*.log` | §2–3 |
| `out/explain_gw.log`, `out/tagword_*.txt`, `out/ztag.log` | §3 |
| `out/laman_sphere.log`, `out/laman_sphere_summary.txt` | §4 |

Reproduce, for example:
```
../TrackQ/.venv/bin/python tr_lag.py data/n1_7121_17_230_K_L_L_data.json --gwindow 2,5 --out out/gw.json
../TrackQ/.venv/bin/python tr_rule.py 5 part data/n1_7121_17_230_K_L_L_data.json      # equivariant: 0
../TrackQ/.venv/bin/python tr_rule.py 1 partT data/n1_7121_17_230_K_L_L_data.json     # state-specific: 1/2
./run_lolo.sh
```

# TrackJL-review: independent adversarial review of TrackJ J1–J5 and TrackL Lemma E / St / S / S1 / S2

Studio, 8 Oct 2026.
- Reviewer: independent. I wrote none of TrackJ, TrackL or TrackH.
- Code: written from scratch. No TrackJ/TrackL/TrackH code was imported or run; I only read their definitions.
- Nothing outside `TrackJL-review/` was modified, and nothing was committed.
- Compute: at most 2 engine workers under `nice -n 10`. About 40 min of wall time for the main runs.

Sources read:
- `CoordinatorPlan.md` (log up to 8 Oct)
- `TrackH/README.md` and `TrackH-review/README.md`
- `TrackJ/README.md`
- `TrackL/SigmaType.md` and `TrackL/README.md`
- `TrackF/LockParity.md`
- `PlaneMap/ChainCount.lean` (chainCount, nChains, RigidAt) and `QuarterLockParity.lean`

## 0. Verdicts

| item | verdict | data (fresh, independent engine) |
|---|---|---|
| **J1** link components, N = 8 + ℓ (DL + D) | **CORRECT** | 90.3M sphere DL states, 0 failures; 2.0M RP² DL+D states, 0; 28.7k general-graph DL+D states, 0 |
| **J2** π maps P2(c) onto P3(π c), component for component | **CORRECT** (minor: the roles (α,B,μ,A) of π(c) come from direct computation, not from H0) | 199.7M sphere π-steps; 5.0M RP²; 28.8k general; 0 failures |
| **J3** in-shape ⇒ extra chain in P1 | **CORRECT**, with a hypothesis note (G-J3) | 10,546 sphere in-shape states; 441 RP²; 3,905 general; 0 failures |
| **J4** Kempe neighbours of rigid / in-shape states | **neighbour sets CORRECT. The "any graph" property N(Z c) ≥ 9 is WRONG off the sphere (G-J4)**; fix below | sphere: 491,761 rigid and 10,546 in-shape, 0 failures. N(Zc) ≥ 9 fails at 225/225 in-shape states of TrackJ's rung-(a) graphs and at 35/441 RP² in-shape states |
| **J5** shape of a near-rigid closed class (assuming the law) | **CORRECT** (its use of J4's N(Zc) ≥ 9 is safe inside 𝒦, by H0) | all 43 rung-(d) and 325 rung-(c) classes re-derived: every J5 item holds (7,360 state checks, 0 failures); 937 rung-(a) classes violate the law, so J5 does not apply to them |
| **Lemma E** Σχ = (2,3,3) at unfilled sphere states | **CORRECT** | 446.2M unfilled sphere states, 0 failures |
| Lemma E, RP² constants (1,2,2) | **CONFIRMED** | 12.87M unfilled RP² states, 0 failures (torus (0,1,1): 30,488, 0 failures) |
| **Lemma St** (star identity; any graph) | **CORRECT** | 858M sampled Kempe moves × third colours on the sphere, plus 2 × 199.7M checks across π; 0 failures (also 0 on RP², torus and general graphs) |
| **Lemma S** | **CORRECT** (sphere) | 49,094 hypothesis instances, 0 failures; key equality χ_c(A_cB_c) = 0 at 54,816 instances, 0 failures |
| **Corollary S1** (in-shape ⇒ Z ⊂ α_cμ_c) | **CORRECT** | 10,546 / 10,546 sphere |
| **Corollary S2** and its mirror | **CORRECT** on the sphere | 49,094 + 49,136, 0 failures. **Fails on RP²** (36 + 27): TrackL's remark that σ-type always holds on RP² is true only for in-shape states (441/441) |
| TrackL §2.1 χ-recursion | **CORRECT** | 199.7M π-steps, 0 failures |
| TrackL §2.2 "destruction" sentence | **WRONG as written** (pair mislabelled); fix below | 10,546 / 10,546 instances contradict the literal statement |

**Definitions are consistent across tracks.**
- A "chain" is a component of a pair graph of G − h that contains a vertex of one of the two colours. Link vertices count; h never does.
- This is Lean's `chainCount`. TrackJ's N and TrackL's #XY are the same quantity.
- TrackL's χ(XY) = |X| + |Y| − e(X,Y) over G − h, which equals #XY − β. This is TrackH H3's c − β.
- "Rigid":
  - TrackL / Lean `RigidAt` / TrackH H4 define it as DL with counts (1,1,2,1,2,1).
  - TrackJ's J1 / J4 use "N = 8 at a DL state with D".
  - The two agree on the sphere: 90.3M checks of "counts ⇔ N = 8 under DL + D", 0 failures. They also agree whenever D holds.
  - Off the sphere they differ: 13,161 RP² states (and 2 general-graph states) are rigid by counts without D.
  - This is harmless for every lemma below once "rigid" is read as `RigidAt`; see G-J3.

## 1. TrackJ lemmas

### J1 — CORRECT
- **Hypotheses needed:** DL and D (¬inA ∧ ¬inB). The proof is complete.
  - The listed components meet the link, by link edges and the locks.
  - They are distinct, by D and colour.
  - Link chords cannot merge them. A chord x_j x_{j+3} would give inA, and a chord x_{j+2} x_{j+4} would give inB, so both are excluded by D. Every other chord joins vertices already in the same listed component.
- **Stronger identity.** At every unfilled state, on any graph:

  #(link-meeting chains) = 8 + ([¬inA] − L2) + ([¬inB] − L1).

  - Checked: 446M sphere states, 13M RP² states, every general state, 0 failures.
  - On the sphere, Theorem D makes the correction terms vanish. So **every** unfilled sphere state, DL or not, has exactly 8 link-meeting chains, and N = 8 + ℓ holds there without assuming DL.
  - This is the cleanest way to state J1, and it fixes G-J4 below.
- My engine reproduces TrackJ's census numbers exactly. For frame 22–31 (94,231 holes):
  - in-shape states: 578 / 985 / 5,473 for frames 22–29 / 30 / 31;
  - NRI counterexamples: 2 / 6 / 96;
  - longest R-run: 5 / 6 / 6;
  - all-DL cycles: 0 / 1 / 6.

### J2 — CORRECT
- G[α,A] has the same vertex set and edges after π. G[μ,B] is untouched.
- The roles of π(c) follow from the new link (α, μ, A, α, B) at x_j..x_{j+4}, read from x_{j+3}. That gives roles (α, B, μ, A). This needs no H0; citing H0 is harmless but unnecessary.
- Only "c unfilled, π defined" is needed.
- Checked component-wise as vertex partitions, not just counts.

### J3 — CORRECT, with hypothesis note G-J3
- **What the proof needs:**
  1. P2 = (2,1) at π(c) and at π⁻¹(c). This is immediate if "rigid" means `RigidAt` (counts). If it means "N = 8", it needs D at π(c) and π⁻¹(c): true on the sphere (Theorem D), not automatic in general graphs.
  2. D at c, so that the extra chain is link-free (J1). This is automatic: π(c) defined gives ¬inA, and π⁻¹(c) defined gives ¬inB.
- **Fix:** state J3 with rigid := `RigidAt` (DL with counts (1,1,2,1,2,1)). Then it holds in any graph.
- Data: 0 failures with this definition (sphere 10,546; RP² 441; general 3,905).

### J4 — neighbour sets CORRECT; G-J4: "N(Z c) ≥ 9" is false in general graphs
- **Rigid state (+D).** Kempe neighbours up to renaming = {π c, π⁻¹ c}: 491,761 sphere checks, 0 failures.
  - D is genuinely needed: a rigid-by-counts state with inA has a link-free αA chain and no π.
- **In-shape state.** Neighbours = {π c, π⁻¹ c, Z c}: 10,546 sphere, 3,905 general, 441 RP², 0 failures. They are pairwise distinct, because the repeat pairs j+3, j+2 and j differ.
- **G-J4.** J4 lists "Z is still a link-free component …, so N(Z c) ≥ 9" under the heading "any graph". That does not follow.
  - Z(c) need not be DL: on the sphere, 8,598 of 10,546 in-shape states have Z(c) not DL+D.
  - Off the sphere, Z(c) can have fewer than 8 link-meeting chains.
  - Counterexamples:
    - **225 / 225** in-shape states in TrackJ's rung-(a) examples (`out/gen_rung_a.log`), e.g. `ja101_0_317`: N(Zc) = 7, DL, D fails;
    - **35 / 441** in-shape states on fresh RP² triangulations, e.g. `rp25_s404_13` h = 16: N(Zc) = 8, not DL.
- **Fix:** N(Z c) ≥ 9 holds:
  - (i) on the sphere, because every unfilled state has 8 link-meeting chains (stronger J1 above) and Z is link-free (10,546 / 10,546 in-shape, and 1.26M N = 9 states with P1 extra, 0 failures); or
  - (ii) whenever Z(c) satisfies DL + D.

  Inside a near-rigid class 𝒦, (ii) holds by H0, so **J5 is unaffected**.

### J5 — CORRECT (given the chain-parity law, which is formal on the sphere as `chainParityLaw_sphere`)
- Item-by-item check of the logic:
  1. Alternation: law + DL → DL, and N ∈ {8, 9}, where N ≥ 8 needs D, from H0.
  2. Cycle length ≡ 0 (mod 10): j ↦ j+3, and a renaming class has a unique repeat pair.
  3. In-shape at 9-states.
  4. Z is a fixed-point-free involution. Z(c) ∈ 𝒦 has N ≤ 9 and, by D from H0, N ≥ 9. Z(c) ≠ c because a renaming fixing all four link colours is the identity.
  5. Degrees 2 / 3.
  6. Offset d ≡ 0 (mod 10) on its own cycle, which forces length ≥ 20; hence |𝒦| ≥ 20.
- Converse (6): closure under π^{±1} makes π and π⁻¹ defined, which gives D, so J4 applies. Finiteness and injectivity give cycles.
- Data: my class-mode engine rebuilds every Kempe class of the 43 rung-(d) and 325 rung-(c) graphs (`out/gen_rung_{c,d}.log`). All 368 are near-rigid closed and law-respecting. Every J5 item holds at every state:
  - alternation and length 20;
  - in-shape 9-states, with the extra chain in α–μ;
  - Z(c) ∈ 𝒦 with N = 9;
  - degrees 2 / 3;
  - Z on its own cycle at offset 10.
- The 937 near-rigid closed classes of rung (a) all violate the law, so J5's hypothesis fails there, as TrackJ says.

## 2. TrackL lemmas

### Lemma E — CORRECT (sphere); RP² constants (1,2,2) CONFIRMED
- The derivation is sound:
  - Σ_P χ = (n−1) − (3n−11) + #crossing.
  - The 2n−9 faces avoiding h each have exactly two crossing edges.
  - A link edge lies in exactly one face avoiding h.
  - The crossing link edges number 2 / 4 / 4.
- The general surface form is Σ = χ_S − 1 + k/2, i.e. (χ_S, χ_S+1, χ_S+1).
- **Hypotheses:**
  - simple triangulation (no parallel edges, so e(X,Y) is unambiguous and each edge lies in two distinct faces);
  - deg h = 5, with faces at h exactly the five link triangles;
  - an *unfilled* state. At filled states the link crossing count differs, and Lemma E is not claimed there.
  - No DL or D is needed. No degree assumption on other vertices is needed, and link chords are fine.
- Data:

  | surface | unfilled states | failures |
  |---|---|---|
  | sphere (census 22–31; 3,000 fresh min-degree-5 and 4,000 fresh min-degree-3 spheres, n = 12–40) | 446,157,347 | 0 |
  | RP² (4,500 fresh, min degree 3 and 5) | 12,868,293 | 0 |
  | torus (800 fresh) | 30,488 | 0 |

### Lemma St — CORRECT (any graph)
- 2|r| + |p∪q| − e(r, p∪q) is invariant under the swap.
- Checked:
  - every Kempe move (all 6 pairs, every component) × both third colours at a 1/7–1/29 sample of states: 858M checks;
  - across π at colours μ and B: 199.7M each.
- 0 failures, on all surfaces and on general graphs.

### Lemma S — CORRECT (sphere)
- Each step checks out:
  - roles of c = (α, B, μ, A);
  - St at μ;
  - u rigid ⇒ P1 and P3 of u are trees (Lemma E with minimal counts);
  - P2(c) = (2,1) ⇒ trees;
  - χ_c(A_cB_c) = 0;
  - three P1 chains with Σχ = 2 and each χ ≤ 1 force χ-values (1,1,0), so the A_cB_c chains, a nonempty sub-multiset summing to 0, are exactly the unicyclic one.
- Hypotheses: no DL is needed at c, and only π(u) defined at u.
- Data: 49,094 instances (0 failures), of which 0 have c non-DL in this sample. Step 5 alone (u rigid, P2(c) = (2,1) ⇒ χ_c(AB) = 0): 54,816 instances, 0 failures.
- Off the sphere: on RP² the conclusion fails in 36 / 1,973 instances, and χ_c(AB) = 0 fails in 1,316, as expected. In general graphs χ_c(AB) = 0 fails 3,680 / 3,680 in rungs (c)/(d), yet the count conclusion holds there.

### Corollary S1 — CORRECT
- J3 (with D at c, π c and π⁻¹ c, all from Theorem D on the sphere) followed by Lemma S with u = π⁻¹(c).
- 10,546 / 10,546 sphere in-shape states.
- Also 441 / 441 on RP², where Lemma S does not apply: an unexplained mechanism, as TrackL notes.

### Corollary S2 and mirror — CORRECT on the sphere
- D at c comes from Theorem D (Lock2 ⇒ ¬inA) plus π⁻¹(c) defined. Then P3(c) = 3 (J2), the extra chain is in P1, P2(c) = 3, and Lemma S applies.
- The mirror x_t ↔ x_{2−t}, A ↔ B swaps π and π⁻¹. I re-derived the mirrored Lemma S: St at μ for π̃ gives χ_c(α_cB_c) + χ_c(A_cB_c) = χ_u(αμ) + χ_u(μB) = 2.
- Data: 49,094 (S2) and 49,136 (mirror), 0 failures.
- **RP² correction to TrackL.** TrackL says σ-type held at all 223 RP² N = 9 cases, and the README presents σ-type on RP² as a general phenomenon. On a larger RP² sample, S2's conclusion **fails 36 / 1,760** (mirror 27 / 1,822), e.g. `rp25_s404_24` h = 14: π⁻¹(c) rigid, N = 9, extra chain in AB. Only the full in-shape version (S1) survives on RP² (441 / 441). So the open "σ-type on RP²" question should be stated for in-shape states only.

### TrackL §2.1 χ-recursion — CORRECT
- b₅ = a₃, b₆ = a₄, b₂ + b₃ = a₁ + a₆, b₁ + b₄ = a₂ + a₅: 199.7M π-steps, 0 failures.
- The near-rigid orbit (1,1,2,1,2,1) ↔ (2,0,2,1,2,1) is consistent. Rank 3 is right, because the four equations sum consistently (5 = 5).

### TrackL §2.2 "destruction" — WRONG as written
- **The claim:** c → u′ = π(c) "merges the two α_cμ_c trees (L_c and Z_c) into one".
- **Why it fails:** by J2 applied at c, {α_c, μ_c} is not preserved. In u′'s roles, {α_c, μ_c} = {α_{u′}, A_{u′}}, which has exactly **2** chains at the rigid u′. Data: 10,546 / 10,546.
- **The merge actually happens in {α_c, B_c}:** 2 trees at c become the single α_{u′}μ_{u′} tree at u′ (10,546 / 10,546). This is the mirror of the creation step.
- **Fix:** "merges the two α_cB_c trees into one. The α_cμ_c pair keeps two chains, both now meeting the link (Z_c is absorbed)."
- This sentence is in the exploratory section and is not used by Lemma S.

## 3. Side data (NRC context, not under review)
- Fresh spheres:
  - 3,000 min-degree-5 spheres (n = 20–40; 55,182 holes; 511M states): longest π-run inside R = {DL, N ≤ 9} is **7**; **0** π-cycles inside R; 25 all-DL cycles; 260 NRI pairs.
  - 4,000 min-degree-3 spheres: longest run 3.
  - This matches TrackJ's census maximum of 7.
- RP² min-degree-5: longest run 7, 0 R-cycles.
- Chain-parity law: 90.3M sphere DL states, 0 failures (sanity check of the formal theorem).

## 4. Files
| file | content |
|---|---|
| `rv_eng.c` / `rv_eng` | C engine: all proper 4-colourings of G − h up to renaming, chains, χ, locks, inA/inB, π, π⁻¹, Kempe neighbours, every check above; `-E χ` surface mode (Lemma E), `-c` class mode (J5) |
| `rv_gen.py` | fresh random triangulations of S² / RP² / torus (vertex insertion + flips, min degree 3 or 5), each validated (edge in 2 faces, links are cycles, Euler characteristic) |
| `rv_totals.py` | sums the counters over logs |
| `run_w1.sh`, `run_w1b.sh`, `run_w1c.sh`, `run_w2.sh` | launch scripts. `run_w2.sh` was stopped after its sphere5 job; its remaining jobs (RP², sphere3) were run by `run_w1c.sh` |
| `out/w1_frame*.log` | Census29 frame 22–31, every degree-5 hole |
| `out/w2_sphere{5,3}.log`, `out/w2_rp2_{3,5}.log`, `out/w1_torus3.log` | fresh surfaces; inputs in `out/fresh_*.txt` |
| `out/gen_rung_{a,c,d}.log` | TrackJ's general-graph examples (graph data only) through my engine, class mode |
| `out/totals_sphere.txt`, `out/totals_rp2.txt` | summed counters |
| `out/*.err` | first failure examples (only the expected off-sphere / general-graph ones) |

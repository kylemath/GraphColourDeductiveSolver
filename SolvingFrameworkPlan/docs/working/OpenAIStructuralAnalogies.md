# OpenAI `openai/math`: proofs whose structure resembles our open problem (7 Oct 2026)

**Scope and method.** I did a sparse, blob-filtered clone of https://github.com/openai/math into `/private/tmp/claude-501/oaimath/repo`. It holds source text only: `CONTENTS.md`, `overview.tex`, `lean/docs/`, `lean/formalization.yaml`, the Barnette Lean directory, `PlaneColoring/Five.lean`, and the LaTeX of about 6 preprints. Nothing from it was built or run. I scored all 372 family titles and descriptions against the signature below, then read the proof architecture of the top candidates. Raw URL prefix: `https://raw.githubusercontent.com/openai/math/main/`. Trust caveat (same as `OpenAIMathScan.md`): the catalogue marks the formalisations `review: unchecked`, `automation: agent`.

**Our signature.**
- Kempe classes of colourings of T − v.
- Claim: every class contains a filled state.
- π permutes the unfilled states, and its orbits are cycles.
- Exact identities: Theorem W and Σλ = |DD| − 2N₀ − E₂ − 3τ.
- A quarter density target, plus Hall/charging certificates.
- The obstruction is frozen (all-DL) π-orbits, which the 2-ball cannot exclude.

---

## 0. PRIORITY (coordinator request): the exponential sum in OpenAI's Barnette proof

Sources:
- `preprints/Paired-states-and-Hamiltonian-cycles-in-cubic-bipartite-planar-graphs-September-24-2026/build/paper.tex`, Sections 3–6.
- Lean, in `lean/OAI/Combinatorics/Hamiltonian/`: `TriangleSystem.lean`, `CycleReversal.lean`, `PairPhases.lean`, `PairPolynomials.lean`, `StateDisk.lean`, `ColoredDual.lean`, `BMatching.lean`, `Main.lean`.
- Doc: `lean/docs/180.md`.

The reader's report is substantially right with two corrections:
- The roots of unity are powers of **i** (fourth roots), not cube roots.
- The sum does not directly pick out the non-cycle edges. It proves that some *pair of states* has an acyclic opposite-edge set Q_s. The edge selection P, whose complement is the Hamiltonian cycle in the cubic graph, is built afterwards from that state (Section 6 of the paper).

### 0.1 Setting (dual triangulation)

- G is cubic, bipartite, planar and 3-connected. Its dual T is a triangulation whose faces are properly 2-coloured black and white. Bipartiteness of G is exactly this: each edge of T has one black face and one white face.
- One black face t₀ is put outside. Its three vertices are the roots.
- Counting sides gives #black = #white = k, |E| = 3k, |V| = k + 2. So A (the black faces other than t₀) and X (the non-root vertices) both have size k − 1.
- **State** r: a bijection A → X with r(t) ∈ V(t). These are Tutte's states (trinity), i.e. perfect matchings of the bipartite face–vertex incidence graph.
- **Pair** (r, s): two states with r(t) ≠ s(t) for every t.
- **Q_s**: the edge opposite s(t) in each t ∈ A.
- **Goal (Prop. 5.1, Lean `forest_pair_of_disk_circulation`):** given that some pair exists, some pair has Q_s a forest.
- Existence of a pair is separate (Prop. 3.1, Lean `BMatching.pair_nonempty`). It uses Hall/max-flow plus a planar density inequality, e(U) − b(U) ≤ 2|U| − 4, proved component by component from Euler's formula and signed side counting.

### 0.2 The disk identity (the planar input)

Lemma 4.1 (Lean `PairPhases.disk_count_identity`, `StateDisk.state_disk_count` / `state_disk_delta`, `ColoredDual.cycle_disk` / `signed`):
- Define δ(v,w) = +1 if the black face of edge vw is on the left going v → w, and −1 otherwise.
- In each black face, choose an edge directed out of r(t). Then every simple directed cycle of chosen edges has δ-sum exactly **−3 if counterclockwise and +3 if clockwise**.
- Proof: three counts on the enclosed disk.
  - Euler: B + W = 2I + h − 2.
  - Signed side count: 3(B − W) = 2l − h. This uses that each interior edge has one black and one white side.
  - The state bijection: B = I + l. Each interior vertex and each boundary vertex whose outgoing edge has its black face inside is matched to a black face in the disk.
  - Together these force 2l − h = −3.
- The paper notes the identity fails for arbitrary oriented cycles. The matching count is essential.

### 0.3 The sum

- For a pair, direct the edge of t from r(t) to s(t). The union D of these edges is a disjoint union of directed cycles on X.
- J(r,s) = (1/3) Σ_t δ(r(t), s(t)) is an integer. In fact **J = #clockwise − #counterclockwise cycles of D**.
- Pick real incidence weights a(t,v) and set ω(s) = Σ_t a(t, s(t)). Then

  **Z(x) = Σ over pairs (r,s) of i^{J(r,s)} · exp(x · ω(s)).**

- Lean replaces exp(xω) by the multilinear polynomial ∏_t (1 + a(t, s(t)) X) (`stateWeight`, `linearProduct`). This has the same first-order behaviour and avoids analysis.
- `phase n := I ^ (n / 3)` is applied to the raw δ-sum (`rawIndexSum`).

### 0.4 Why the terms cancel (slice by the second state s)

Lemma 5.2; Lean `CycleReversal.reversal`, `reversal_involutive`, `reversal_ne`, `PairPhases.reverse_rawIndexSum_diff`, `reverse_phase`, `fixed_second_state_cancels`.

- Fix s with Q_s cyclic. Choose a cycle C of Q_s using s alone.
- For any partner r, orient each opposite edge from r(t) to the third corner u(t). Out-degrees are at most 1, so C is a directed cycle.
- Replacing r(t) by u(t) on C's faces gives another partner r̃ of s. This map is a fixed-point-free involution that changes only r.
- On each changed face, δ(u,s) − δ(r,s) = 2δ(r,u). The disk identity applied to C gives a δ-sum of ±3, so J changes by ±2. Hence i^{J} flips sign.
- The weight exp(xω(s)) depends only on s, so it is unchanged.
- Result: all pairs whose second state has a cyclic Q_s cancel in Z, for **any** choice of weights.
- When Q_s is a forest, each component has exactly one root (Lemma 6.1). The partner is then the unique orientation of the forest toward the roots. So **Z(x) is a signed sum over "tree states"**, with at most one term per s.

### 0.5 Why the result is nonzero (slice by the undirected union D)

Section 5.3; Lean `PairPhases.orient`, `groupEquiv`, `PairPolynomials.group_sum_product`, `cycle_factor_witness`, `common_phase_sum_ne_zero`, `total_sum_ne_zero`.

- Fixing the undirected edge set D (Lean: the map `third`, giving a `Group`), the pairs in that group are exactly the 2^{c(D)} independent orientations of D's cycles. This is the double-dimer regrouping (Kenyon 2014, Lemma 1).
- The group sum therefore factorises as a product over cycles: ∏_C ( −i·e^{x L₊(C)} + i·e^{x L₋(C)} ).
  - The phase of each orientation comes from the disk identity: counterclockwise contributes −1 to J, clockwise +1.
  - L₊ and L₋ are the weight sums of the heads in the two orientations.
- At x = 0 each factor vanishes to exactly first order, with derivative −i(L₊ − L₋).
- **Positive spoke circulation** (Lemma 5.3; Lean `ColoredDual.weights`, `weights_diff`, `slope_eq`, `signed`):
  - Choose a flow α on the cubic graph whose boundary is a prescribed "white charge" (`whiteCharge`).
  - Take a(t,·) to be the potential of α around the black triangle t.
  - Then L₊(C) − L₋(C) = (number of white faces inside C) > 0 for every cycle that occurs (`signed`: δ = −3 with positive slope, or δ = +3 with negative slope).
- So the coefficient of x^{c_min}, with c_min the fewest cycles over all groups, is (−i)^{c_min} times a sum of positive reals. It is nonzero, and groups with more cycles do not contribute in that degree.
- Combined with 0.4: Z ≠ 0, but every pair with cyclic Q_s cancels. So some pair has Q_s a forest.

### 0.6 From the forest state to the Hamiltonian cycle

Section 6; Lean `Matching.lean`, `ForestMatching.lean`, `Forest.lean`, `Main.Duality.hamiltonian`.

- Complementary plane-tree duality turns the forest state into a spanning tree on the white faces. This selects one edge P at every face.
- A second signed count, B − W = 2l − h, combined with the side count 3(B − W) = 2l − h, would force a δ-sum of 0 on any directed cycle of P. That contradicts the disk identity, so P is a forest with 2 components.
- The dual of E \ P is connected and 2-regular, i.e. the Hamiltonian cycle.
- In Lean, separating triangles are handled through `ThreeCuts.lean` / `TrivialThreeCuts`.

### 0.7 Where bipartiteness is used (each is a transfer break point)

| # | Use | Where | What happens for a general (non-Eulerian) triangulation |
|---|---|---|---|
| B1 | Every edge has exactly one black face. This makes Q_s and D edge-disjoint unions and δ well defined. | §2–5; Lean hypothesis `hb : ∀ e, black (tail e) ↔ ¬black (head e)` in `Duality.hamiltonian` and `hc` in `state_disk_count` | Fails. With a Heawood ±1 labelling, edges with two "+" faces or two "−" faces exist. |
| B2 | #black = #white, hence \|A\| = \|X\| and states exist | eq. (2.1) | Fails. #(+) − #(−) = Σσ, which is generally nonzero, so the bijection A → X does not exist. |
| B3 | The disk identity ±3 (side count 3(B − W) = 2l − h needs alternating sides) | Lemma 4.1 | Fails. With same-label adjacent faces, interior sides no longer cancel, and the ±3 rigidity, which drives both the sign flip and the common leading phase, is lost. |
| B4 | The Hall density inequality via face defect \|b′ − w′\| ≤ d − 4 | Prop. 3.1 | Uses signed side counting, so it also fails. |
| B5 | Positivity of L₊ − L₋ | Lemma 5.3 | Not bipartite-specific: planar circulation only. This step survives. |

**Heawood's form.** A triangulation is 4-colourable iff its faces admit ±1 labels with every vertex sum ≡ 0 (mod 3). Barnette's black/white colouring is the degenerate Heawood labelling in which adjacent faces always differ: an Eulerian triangulation, vertex sums exactly 0, already 3-colourable. The whole machinery runs on that degenerate labelling, which is *given* in the bipartite case. For 4CT, producing any Heawood labelling is the theorem itself, and a non-degenerate one breaks B1–B4.

**Tait / Z₂×Z₂ flows.** Fixing one colour class (a perfect matching M of the cubic dual), the Tait colourings using M form a cube 2^{c(G−M)} of independent swaps of the even cycles of G − M. This is the same orientation-cube shape as Barnette's D-groups. What is missing is a phase that flips under every single cycle swap.
- The natural Heawood/Alon–Tarsi sign does not flip. For plane cubic graphs, all Tait colourings have the same sign (Scheim 1974; Jaeger; used by Ellingham–Goddyn 1996). So bicoloured-cycle swaps preserve it, and no per-factor first-order zero arises.
- I cite these from memory; I did not re-read them here.

**Penrose.** P(G;3) = #Tait colourings is a signed state sum whose positivity is equivalent to 4CT. No regrouping is known that makes it manifestly nonzero. Barnette's proof succeeds because, after cancellation, its sum is a signed sum over tree-like states (spanning trees under the KPW/Temperley correspondence) in the planar-bipartite **determinantal (Kasteleyn-type) world**, where positivity is available. Tait colourings and Kempe classes sit in the #P-hard colouring world.
- This is my reading. I have not checked that Z is literally a determinant.

**Verdict on direct transfer:** no. Each of B1–B4 is a hard stop for non-Eulerian triangulations. The frame class has degree-5 vertices, so it is never Eulerian.

### 0.8 Could such a sum live on one Kempe class or one hole? (the transferable *template*)

The template is more general than the bipartite instance. It is an **upgrade argument**: start from the existence of some object (a pair, by Hall), and use one finite sum sliced two ways.
- Slice 1, by a coordinate the weight depends on: every bad object has a phase-flipping, weight-preserving, fixed-point-free involution, so bad objects cancel.
- Slice 2, by a union/cube structure: the sum factorises into independent ± choices with first-order zeros and a common leading phase, so it is nonzero.

This maps onto our problem with an uncomfortably good fit:

| Barnette | Our problem |
|---|---|
| A pair exists (Hall/flow) | The Kempe class K is nonempty (it contains the given colouring) |
| Bad: Q_s has a cycle | Unfilled: the state has a lock (a Kempe chain joining two ring vertices, closed through v into a separating cycle) |
| The reversal of the Q_s-cycle changes only r | A swap along the lock chain changes only the "other" coordinate |
| D-groups = independent orientations of the cycles of D | {a,b}-cubes: independent swaps of the {a,b}-Kempe chains with the other two colours fixed. All lie in K. |
| Disk identity ±3 gives the sign flip and the common leading phase | **Missing.** We need an exact planar identity giving a lock-chain cycle (through v) a fixed winding-type value, so that one chain swap flips a phase. Theorem W (3F − U = −5·winding) is the only exact winding identity we have, and it is per π-orbit, not per chain. |

The frozen-orbit test this must pass:
- Any such argument proves "every class has a filled state". So its phase identity must fail on torus targetless classes. That means it must use planarity, as Barnette's disk identity does. That is acceptable.
- Restricted to a single hole/2-ball it cannot work: NightG66 shows the 2-ball admits all 32 bit words at 66666. A local-type phase with zero unfilled sum on every 2-ball configuration would therefore also kill something forced to be nonzero.
- The sum has to be over the whole class K, which is exactly the kind of global mechanism we lack.

Honest assessment: the scaffold transfers, but the key ingredient does not. That ingredient is an exact identity making *every* relevant cycle carry the same phase jump. Nothing we have proved gives a per-chain ±constant. A cube factor with phase flip on every single chain swap would make Σ_{cube} phase = 0 at x = 0. Our data can check this cheaply.

### 0.9 Concrete computations (none run; all use only our own code, under `nice -n 10`, ≤ 2 processes)

- **C0 (replicate, ~1 h):**
  - Enumerate duals of small Barnette graphs (Eulerian triangulations, n ≤ 14) with our own enumerator or plantri.
  - Compute all pairs, J, Z(x) with random weights, and the spoke-circulation weights.
  - Check: cyclic-Q_s terms cancel exactly; Z collapses to tree states; the x^{c_min} coefficient is nonzero.
  - Purpose: validates our reading before any transfer claim.
- **C1 (Heawood probe):**
  - On census triangulations take each 4-colouring's Heawood labelling σ (orientation sign of the colours on each face).
  - Report the fraction of same-label edges, Σσ, and whether any state bijection A → X exists for black = {σ = +1}.
  - For random directed cycles of chosen edges, report the distribution of δ-sums, with δ = (σ_left − σ_right)/2.
  - Prediction: no ±3 rigidity. This quantifies B1–B3.
- **C2 (cube flip test):**
  - For every census class K, colour pair {a,b} and colouring c, form the {a,b}-cube (swap subsets of {a,b}-chains of T − v).
  - For candidate phases φ, record the fraction of single-chain swaps on which φ flips sign. Candidates:
    - i^{H} and ω^{H}, with H the Heawood sum over faces of T − v;
    - (−1)^{#a-vertices};
    - ζ₅^{repeat index};
    - (−1)^{winding of the state's π-orbit};
    - i^{(ring δ-sum)/k}.
  - A usable phase needs 100% flips, at least on chains meeting the ring.
- **C3 (class null-space test, the decisive one):**
  - Key every state by a finite local type τ: ring colouring, lock pattern, R1/R2/R3 type, link word.
  - Over all census classes K, solve for complex φ(τ) with Σ_{s ∈ K unfilled} φ(τ(s)) = 0 for every K, and look for a solution with Σ_{s ∈ K filled} φ(τ(s)) ≠ 0 for every K.
  - If the solution space is zero, or every solution kills some class's filled sum, **no local-type phase can carry a Barnette argument**, and the phase must be genuinely global, like Barnette's J, which counts cycles of a global union.
  - Run it separately on 66666 holes, and on the BV/AW adversarial graphs.
- **C4 (lock-chain involution):**
  - For each unfilled state c′, list its partners c in K (colourings differing by an {a,b}-chain set).
  - Check whether swapping c′'s lock chain is a fixed-point-free involution on the partner set, and what it does to the phase candidates of C2.

---

## 1. Catalogue scoring (all 372 families)

Most families are analysis, number theory, algebraic geometry, operator algebras or physics, with no structural overlap. I scored a family as relevant if its proof mechanism matched one of the six signature mechanisms in the brief (exchange/parity, Sperner/degree, discharging closed by an identity, Hall/flow certificate, orbits hitting a target, recolouring connectivity).

| Score | Family | Mechanism touching our signature |
|---|---|---|
| 5 | **180 Barnette** | Signed sum, sign-reversing involution on bad states, independent-factor nonvanishing; Hall/flow plus Euler density for existence (§0) |
| 4 | **173 Seymour second neighbourhood** | Minimal counterexample turned into a strict subset inequality for every proper subset, then an extremal-family argument with a pruning (matching-rank) lemma |
| 4 | **158 Plane not 5-colourable** | Topological covering-dimension forcing (`PlanarCover.compact_open_cover_impossible`): local data silent, global existence of a large region |
| 3 | 136 PCP for PPAD | End-of-line parity (components are paths, endpoints are solutions); robust local verification |
| 3 | 131 Switch-chain mixing | Exchange moves on a constrained state space; local-to-global spectral inequality H² ⪰ H; connectivity |
| 3 | 104 Mean-payoff / parity games | Cycle-sign conditions and potentials (LP duality), attractors in finite dynamics |
| 3 | 149 Permanence (mass-action) | "Every trajectory in each class enters an absorbing set": classwise target hitting via trapping regions |
| 2 | 226 Double-dimer to CLE₄, 113 matchings | Union of two matchings forms loops (the regrouping Barnette uses) |
| 2 | 246 Cannon (CirclePacking `Demand.lean`) | Thurston/Hall demand conditions on triangulated disks (demand 6 at interior vertices), Euler F + 4 = 2V |
| 2 | 165 Crossing numbers, 174 thin trees, 181 Erdős–Gallai | Exact counting / fractional-to-integral certificates |
| 2 | 155 Aperiodic 3D tile | Cautionary: local rules consistent, global property impossible |
| 1 | 157, 184, 106, 229, 233, 235, 225, 232, 237 | Colouring / height / Potts content, but no existence-forcing mechanism of our type |

The source trees read are listed in §0 and §2.

## 2. Analogies beyond §0

### 2.1 Seymour's second-neighbourhood conjecture (family 173)

Source: `preprints/A-proof-of-Seymours-second-neighborhood-conjecture-September-23-2026/build/source/00-introduction.tex` … `03-incompatibility.tex`.

- **Mechanism.**
  - Take a minimal counterexample, minimal in order and then in arcs.
  - Arc deletion gives a strict subset inequality for every nonempty proper vertex set.
  - Blowing up each vertex into a transitive tournament gives a strict "concavity" |U| + |F²(U)| < 2|F(U)|.
  - Then maximise M + d over compatible pairs of families of ordered pairs, where d counts uncovered points.
  - A pruning lemma for arbitrary finite relations, proved via a maximum-rank matching bound, charges its deletions to uncovered points, so the objective strictly increases. Contradiction.
- **Analogue.**
  - States: vertices. π / σ / σ′ images: out-neighbourhoods.
  - Minimal targetless class gives, for every proper π∪σ-invariant subset, a strict expansion inequality.
  - The good set is the vertex satisfying the inequality, i.e. the filled state.
- **Verdict.**
  - It is a genuinely global extremal argument that never inspects local structure. That is promising in kind.
  - But Seymour's inequality has slack built into the operator (F² versus F).
  - On a frozen orbit, π is a bijection on the orbit, so |F(S)| = |S| exactly and no expansion inequality can be strict.
  - It hits the same wall unless σ-images (non-bijective, leaving the orbit) supply the expansion. NightImagesBoundary found σ landing to be statistical rather than forced.
- **Test.** On census and adversarial classes, compute for the operator S ↦ π(S) ∪ σ(S ∩ DL) the minimum over proper invariant S of |F(S) \ S| − |F²(S) \ F(S)|. Check whether the strict inequality Seymour's minimal counterexample would produce is ever violated, which would rule out a minimal-counterexample route.

### 2.2 Euclidean plane not 5-colourable (family 158)

Sources: `lean/OAI/Geometry/PlaneColoring/Five.lean` and `preprints/The-Euclidean-plane-is-not-five-colorable-September-23-2026/build/sections/introduction.tex`.

- **Mechanism.**
  - `graph_map_large_positive` / `graph_map_small_mesh_impossible`: a continuous map of the disk into the realisation of K₅ (a simplex) yields connected positivity regions.
  - Each point lies in positivity regions of at most two coordinates, because points of a graph realisation have at most two positive coordinates (`graphRealization_positive_three`).
  - If every region had diameter ≤ 2, this would be an order-2 cover of a 2-dimensional compact set by small open sets. That is impossible (`PlanarCover.compact_open_cover_impossible`, a Lebesgue covering-dimension / KKM-type fact).
  - So some region is large: global existence forced where local data says nothing.
- **Analogue.** The combinatorial form is Sperner/Hex. In our setting: in a 4-coloured triangulated disk, complementary Kempe pairs cannot both fail to cross. That is Kempe's own argument, which we already have ("Hex dichotomy", `QuarterRotationPlanar`).
- **Verdict.** It hits the same wall. A DL (frozen) state is exactly the case where both locks hold, which is consistent with Hex. The covering argument forces some long chain, not a cut chain. It might help prove that a lock chain must leave the 2-ball (NightG66), but not that it is ever cut.
- **Test.** At 66666 holes, measure the minimal radius of lock chains on all-DL orbit states versus on states whose σ-image is non-DL. A Hex-type forcing predicts the radius is unbounded on any frozen-orbit family (see the C82 → C88 DL-run growth).

### 2.3 End-of-line / Smith–Thomason parity (family 136, PCP-for-PPAD; also the brief's lollipop item)

Source: `preprints/The-PCP-for-PPAD-conjecture-a-quasilinear-reduction-September-25-2026/build/sections/01-introduction.tex`, not read in depth. The parity lemma itself is classical.

- **Mechanism.** In a graph of maximum degree 2 with one known endpoint, another endpoint exists.
- **Analogue.** Unfilled states with π form a permutation, so there are no endpoints. Weak F6 (`pureClean_of_hole6`) already uses a walk-until-exit argument of this shape, via `typed_in_orbit` and the σ-exit.
- **Verdict.** Exactly the frozen-orbit wall. An all-DL π-cycle is an endpoint-free component, and parity cannot exclude cycles. It would need a non-bijective successor map on unfilled states (π composed with σ at DL states), which is a choice and not forced.
- **Test.** Build the degree-≤2 graph "π-edge, or σ-edge at a designated state type" on each class. Count the components with no filled endpoint. If this is zero in the census but the components get long on adversarial graphs, the parity route has the same evidence status as G66⁰.

### 2.4 Hall/flow certificates closed by Euler (Barnette Prop. 3.1, `BMatching.lean`)

- **Mechanism.** A Hall condition on subsets S ⊆ X is converted by a min-cut computation into a planar density inequality e(U) − b(U) ≤ 2|U| − 4. That inequality is proved per component by Euler plus the face defect |b′ − w′| ≤ d − 4.
- **Analogue.** Our surviving certificates (charge-back P₁, transport T, B′ on positive groups) are Hall/flow statements.
- **Verdict.** This is the most usable piece for our certificates. If the tight Hall sets of our transport / BudgetUnionPos problem correspond to planar substructures (regions of T − v), the deficiency may reduce to an Euler-type count. It does not address the frozen orbit by itself: Hall needs a target, and a frozen class has none.
- **Test.** For census classes, compute the Hall deficiency function of the σ∪σ′ transport over subsets of π-cycles and extract the minimising sets. Check whether their union of Kempe components is a disk-like region of T − v. If it is, try an Euler formula for the deficiency.

### 2.5 Orbits hitting a target: permanence (149) and mean-payoff games (104)

Sources: `preprints/Uniform-Permanence-in-Weakly-Reversible-Mass-Action-Systems-October-5-2026/build/sections/*.tex` and `preprints/Deterministic-quasipolynomial-time-mean-payoff-games-September-25-2026/build/source/sections/*.tex`, read at catalogue/intro level only.

- **Mechanism.** Trapping regions or Lyapunov-type functions force every trajectory into a target. Cycle-sign conditions are equivalent to potentials (LP duality).
- **Verdict.** Killed for existence. π is invertible, so a strictly decreasing Lyapunov function on unfilled states is impossible along any cycle. The potential/LP-duality form is already what our charge-back certificate is (`sigmaC_of_assignment_groups`).

### 2.6 Switch-chain mixing (131)

Source: `preprints/Polynomial-Mixing-of-the-Switch-Chain-for-Every-Graphical-Degree-Sequence-September-25-2026/build/sections/introduction.tex`.

- **Mechanism.** Pair resamplings give averaging projections E_a. The local-to-global inequality H² ⪰ H for H = Σ(I − E_a) gives a spectral gap, once ker H = constants (connectivity).
- **Verdict.** Low. It gives mixing on a known-connected space, not existence of a target. A Kempe analogue would bound the conductance of K, which says nothing about whether filled states exist in it.

---

## 3. Ranking

1. **Barnette two-slicing signed sum (§0).** The only mechanism found that is global, uses planarity in an exact identity, and upgrades the existence of some object to the existence of a good one. Direct transfer is blocked at B1–B4 (bipartiteness gives the ±3 disk identity). The template maps cleanly onto locks and Kempe cubes, with one missing ingredient: a per-chain exact phase. Decisive tests: C2 and C3.
2. **Hall plus Euler density (Barnette Prop. 3.1).** Usable for proving our transport/budget certificates, not for frozen orbits. Test: §2.4.
3. **Seymour minimal-counterexample extremal argument.** Global and abstract. On frozen orbits π is bijective and gives no expansion; that is the same wall unless σ provides forced expansion. Test: §2.1.
4. **Covering dimension / Hex (plane 5-colouring).** Forces long chains, not cut chains, so it is the same wall. It may help with "the lock chain leaves the 2-ball". Test: §2.2.
5. **End-of-line parity.** The frozen orbit is precisely an endpoint-free component, so it is the same wall. Test: §2.3.

Files read are under `/private/tmp/claude-501/oaimath/repo` (scratch, not committed).

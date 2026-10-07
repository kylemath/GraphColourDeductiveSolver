# NightA34Two: A₃₄′ on two-period Γ-cycles (L = 20) at (5,5,5,5,6)

Night worker, 7 October 2026 (started 04:39 MDT). **Exploratory. Hand arguments from the formal tables plus scripts on Studio Job AV's absolute-colour records. Unreviewed.**

Builds on: `NightA34.md` (§1 bookkeeping, §2.2 pocket lemma, §3 window lemma, §7 gates); `NightLemmaS.md` §0 (P1–P3) and §5; the Night log entries for Jobs N, O, AJ, AN, AS + AT and AU; `NightSigmaImage.md` §3 (added on the coordinator's request, §7 below). Lean: `QuarterGammaPeriod`, `QuarterPeriodJ` (`k4_failure_iff_break`), `QuarterLockJ`, `QuarterWindow` (`bookkeeping`, `step8_far`, `window_forced`, `k4_failure_iff_z_split`, `period_colour_rotation`, `closing_perm`), `QuarterZsplit`, `QuarterMirror`, `QuarterEvenCut`. Data: Studio Job AV (`jobav/jobav-cycles.jsonl`: 256 L = 20 records with the 20 absolute colourings, the step components, K₈ and the pockets), and Jobs N and AU.

Labels: **[proved]** a hand argument from the formal tables and π's relabelling-equivariance; **[data]** scripts in `backgroundMaterial/planemap-structural/longtable/local-runs/31-nighta34two/`; **[conjecture]**; **[killed]**.

## Verdict

**A₃₄′ on L = 20 is not proved.** The two-period problem has a much simpler normal form than the absolute-colour picture suggests:

1. **[proved] Exchange-pair normal form (§2).** An L = 20 Γ-cycle is the same thing as a pair of R3k4 colourings c ≠ d with three properties:
   - they agree on the 11 hole vertices;
   - G c = d and G d = c, where G = ρ⁻¹ ∘ π¹⁰ and ρ is the period colour rotation (a 3-cycle fixing α);
   - their 10-step runs agree on the hole at every position, with the same frame, the same swap pair and the same anchor at every step.

   Period 1 of the cycle is ρ applied to the run from d. In the pulled-back frame, the "two different pairs" of K₈/K₁₈, of the two pockets and of the two R1k1 forests are **the same pair**. The difference between the periods sits entirely on the far set X_i = {v : c_i(v) ≠ d_i(v)}. This set is nonempty: |X₀| = 3–11 [data 256/256].
2. **[proved] Restatement.** A₃₄′(L = 20) ⇔ ¬(B(c) ∧ B(d)), where B means "the run breaks at step 8". Equivalently, c₀ and d₀ do not both fail at k = 4. In pocket form: c₉ and d₉ (same hole colours, same pair {α, A}) do not both have a pocket m ⇝ w⁺ avoiding p and x⁺.
3. **[proved] Crossing lemma (§3.3).** If exactly the c-run breaks, every path of d₉'s G_J that joins z to {y, w₂} uses a vertex v ∈ X₉ ∩ Q_c (Q_c is the c-pocket path) with c₉(v) ∈ {α, A} and d₉(v) ∈ J pair.
   - [data] Such a vertex exists in 19/19 breaking cycles.
   - [data] In 18/19, *every* vertex of X₉ in the c-pocket component has c₉ = α and d₉ ∈ J pair.
4. **[proved] Antisymmetry principle (§5).** The hypothetical double break is symmetric under c ↔ d. So a proof must do one of two things:
   - (i) exhibit a quantity Φ with B(u) ⇒ Φ(u₀) < Φ(u₁₀) for every DL period (a one-period statement, testable on open runs, and not killed by NightPotential's counting obstruction);
   - (ii) find a symmetric planar incompatibility of the two pockets.

   Job AU's Φ = |K_{c(p),c(m)}(p)| at R3k4 is of type (i) and fails once on Γ (p25 #16945 mirror h3, 9 vs 10).
   - [data] No class-size Φ is consistent on 19/19 (§5.2).
   - [data] |K_i| ordering is consistent on 18/19 at every position, and the single exception is the same cycle as AU's.
5. **[proved, translation; base equivalence killed by Job AY] R1k1 forest form (§7).** At R1k1 the Lemma-Fix pair {A, B} is exactly the J pair {c(y), c(z)} = {1, 2} of the period-0 table, so in the pair form the two R1k1 pairs coincide. **But** "failure ⇔ σ fixed at R1k1" fails at p26 #87942 h22 (Job AY, 550/552). The forest form is therefore not equivalent to A₃₄′ and is **not** built on; §7 is kept as a record only.
6. **The one isolated statement (§6) is the Exchange Pocket Lemma (EPL).** For two hole-synchronised pocketed R1k2 colourings u, v, z's G_J-component in v contains a vertex of u's pocket path that is α in u. Applied both ways, this should contradict the two pocket curves sharing p, x⁺, w⁺, m. That last planar step is open.
   - EPL is stated in §6. Degree 7 escapes it through M′ (§8).
   - **On the Job AZ witness p26 #87942 h22 (§6.1), static EPL is [killed]** in the mirror orientation: two DL pocketed colourings share the hole colours. So the map G is needed.
   - In the plantri orientation, the witness closes statically: only 1 of the 12 hole-synchronised colourings is DL with a pocket.
   - On the witness, the crossing lemma is confirmed with the full graph.

## 1. Fixed names and the two period tables

Names (q = 0, `Hole6`, absolute vertices fixed by the hole):
- p = x₀, x⁺ = x₁, x₂, x₃, x⁻ = x₄;
- z = w₀, w⁺ = w₁, w₂, w₃, y = w₄;
- m (between y and z at p).

The ring is z w⁺ w₂ w₃ y m. Job AV records these as `p, xp, x2, x3, xm, z, wp, w2, w3, y, m`.

**Period 0** (anchor R3k4, frame α = 0, μ = 1, A = 2, B = 3): this is the table of NightA34 §1.1, formal as `bookkeeping`.

| pos | state | x₀..x₄ | w₀..w₄ | m | swap pair (anchor) | J pair {c(y),c(z)} | pm pair {c(p),c(m)} |
|---|---|---|---|---|---|---|---|
| 0 | R3k4 | 3 0 1 0 2 | 2 3 2 3 1 | 0 | {0,2} (x₃) | {1,2} | {3,0} |
| 1 | R1k1 | 3 0 1 2 0 | 2 3 0 3 1 | 0 | {0,1} (x⁺) | {1,2} | {3,0} |
| 2 | R3k3 | 3 1 0 2 0 | 2 3 1 3 1 | 0 | {0,3} (x⁻) ∋ p, m | {1,2} | {3,0} |
| 3 | R1k0 | 0 1 0 2 3 | 2 3 1 0 1 | 3 | {0,2} (x₂) | {1,2} | {0,3} |
| 4 | R3k2 | 0 1 2 0 3 | 2 3 1 2 1 | 3 | {0,1} (p) ∋ p, y | forced | — |
| 5 | R1k4 | 1 0 2 0 3 | 2 3 1 2 0 | 3 | {0,3} (x₃) ∋ m, y | forced | — |
| 6 | R3k1 | 1 0 2 3 0 | 2 3 1 2 3 | 0 | {0,2} (x⁺) ∋ m, z | forced | — |
| 7 | R1k3 | 1 2 0 3 0 | 0 3 1 2 3 | 2 | {0,1} (x⁻) ∋ p, z | forced | — |
| 8 | R3k0 | 0 2 0 3 1 | 1 3 1 2 3 | 2 | {0,3} (x₂), far: K₈ | {3,1} | {0,2} |
| 9 | R1k2 | 0 2 3 0 1 | 1 0 1 2 3 | 2 | {0,2} (p) ∋ p, m: Π | {3,1} | {0,2} |

**Period 1** is the same table with every colour replaced by ρ(colour), where ρ = (1 3 2), i.e. 1 ↦ 3, 2 ↦ 1, 3 ↦ 2, 0 ↦ 0. This is NightA34's "2→1, 3→2, 1→3", and `period_colour_rotation`'s σ = `sig` = ![0,3,1,2] on letters.
- The step-18 pair is ρ{0,3} = {0,2}.
- The pocket pair at 19 is ρ{0,2} = {0,1}.
- The J pair at 19 is ρ{3,1} = {2,3}.

This is why Job AV finds "the two K₈ pairs always differ": it is the ρ-relabelling and nothing else.

On an L = 20 orbit, π²⁰c₀ = ρ²c₀ globally.
- On the hole this is `period_colour_rotation` applied twice. Off the hole, the canonical state returns, so c₂₀ = τc₀ for one colour permutation τ, and τ = ρ² because the hole shows all four colours.
- [data] τ = ρ² in 256/256 (`closing_colour_map`).
- ρ is a 3-cycle in 256/256.

## 2. The exchange-pair normal form [proved]

**Definition.** Let c = c₀ be the period-0 R3k4 colouring and c_t = π^t c. Put d_i := ρ⁻¹ c_{10+i} for 0 ≤ i ≤ 10, and G := ρ⁻¹ ∘ π¹⁰.

**Proposition E.**
- (E1) **π commutes with colour permutations.** Each π move is a Kempe swap defined by the colour *roles* (frame, locks, the pair {α, A} or its variants), so π(τc) = τπ(c). Hence d_i = π^i d₀, i.e. (d_i) is a genuine π-run.
- (E2) **Hole synchronisation.** d_i|_H = c_i|_H for every 0 ≤ i ≤ 10 (H = the 11 named vertices). This is `period_colour_rotation` at n = i: c_{10+i} = ρc_i on H, with the same ρ at every n because σ commutes with the frame shift `sig`. So the two runs have the same frame, the same position, the same swap pair and the same anchor at every step. By the table, their step components have the same hole part.
- (E3) **Exchange.** G c = d₀ = d and G d = ρ⁻¹π¹⁰(ρ⁻¹c₁₀) = ρ⁻²c₂₀ = c. Also d₁₀ = ρc and c₁₀ = ρd, so X₁₀ = X₀.
- (E4) **L ≠ 10.** c ≠ d, since c = d would make π¹⁰c = ρc and the canonical cycle would have length 10.

Conversely, a pair (c, d) with (E2) at i = 0 and G c = d, G d = c is an all-DL orbit of canonical length 10 or 20, if every state is DL. ∎

[data, `pairav.py` → `pairav-output.txt`, Job AV, all 256 L = 20 records]
- Hole synchronisation at i = 0..10: 256/256.
- X₁₀ = X₀: 256/256.
- X₀ ≠ ∅: 256/256.
- |X₀|: 3–11 on non-breaking cycles, 5–11 on breaking cycles.
- |X_i| along the period: typically odd at even positions and smaller at odd positions (e.g. 11,10,11,7,7,6,7,6,9,8,11).
- X_{i+1} ⊆ X_i ∪ (K_i^c Δ K_i^d): 2,560/2,560 steps. This is trivial: a swap with equal components preserves disagreement.
- K_i^c ≠ K_i^d at every step of every cycle (2,560/2,560). The two runs never swap the same set.

**Reading.** An L = 20 Γ-cycle is a *closed orbit of period 10 in the space of unordered pairs {c, d} of colourings with equal hole colours*. The orbit of the pair closes after one period: (c, d) ↦ ρ(d, c). Everything in the period-0 table applies verbatim to both members, with the same colours.

## 3. A₃₄′ in exchange-pair form

### 3.1 Restatement [proved]

B(u) denotes "the run from u breaks J at step 8" (`k4_failure_iff_break`). Then:

- **A₃₄′(L = 20) ⇔ ¬(B(c) ∧ B(d)).** Period 1's step 8 is ρ applied to step 8 of the d-run, and J is relabelling-invariant.
- **⇔ ¬(F₄(c₀) ∧ F₄(d₀)).** By P2, B(c) ⇔ J false at c₁₀ = ρd₀ ⇔ a k = 4 failure at d₀. Likewise B(d) ⇔ F₄(c₀). So "both k = 4 visits fail" is "both members of the exchange pair fail at k = 4".
- **Pocket form.** By the pocket lemma (NightA34 §2.2, proved mod (D)), A₃₄′(L = 20) ⇔ c₉ and d₉ do not both contain a pocket path Q from w⁺ to m in G_{0,2} − {p, x⁺}.
  - The pair is {α, A} = {0, 2} in the common frame.
  - Each pocket closes into the curve p x⁺ w⁺ Q m p around z.

### 3.2 K₈ and K₁₈ in one frame [proved + data]

- Pulled back, K₁₈ is K₈^d. It is the {0, 3}-component of x₂ in d₈, against K₈^c, the {0, 3}-component of x₂ in c₈: **the same pair at the same anchor**.
- Both contain x₂, x₃, w⁺ and avoid p, m, y, z (`step8_far`, Job AV 896/896).
- K₈^c Δ K₈^d is reachable only through X₈: a path inside K₈^c from x₂ that stays in the agreement set is also a path of K₈^d.
- [data] K₈^c ≠ K₈^d always. |K₈^b Δ K₈^o| is 2 in 14/19 breaking cycles, and 4–5 in the other 5.

Job AV's "K₈ ∩ K₁₈ always nonempty with a far vertex" is therefore the statement that K₈^c ∩ K₈^d contains a far vertex. It carries no signal, as AV says, because the two components differ only near X₈.

### 3.3 Crossing lemma [proved]

Suppose B(c) and ¬B(d).
- d₉ has a G_J-path P from z to {y, w₂}, where J pair = {1, 3} in the common frame. c₉ has the pocket curve C_c = p x⁺ w⁺ Q_c m p.
- Every vertex of C_c has a colour in {0, 2}, and C_c separates z from y and w₂ (NightA34 §2.2 ⇐). P cannot cross C_c at p, x⁺ or m, because d₉ = c₉ there and their colours are not J colours.
- Edges cannot cross in the plane, so P passes through a vertex v of Q_c ∪ {w⁺}. That vertex has c₉(v) ∈ {0, 2} and d₉(v) ∈ {1, 3}, so v ∈ X₉; w⁺ is excluded because it is on the hole.

Hence **X₉ ∩ Q_c contains a vertex that is J-coloured in d₉**, and this holds for every pocket path Q_c. ∎

[data, `pairav.py` addendum] On the 19 breaking cycles:
- the breaking pocket component meets X₉ in 19/19 (2–4 vertices);
- some such vertex is J-coloured in the other run in 19/19;
- *all* such vertices are α in the breaking run and J-coloured in the other run in 18/19. The exception is p25 #16945 mirror h3, with colour pairs (0/1, 2/0, 0/2) in pair {0, 2};
- the A-coloured (c(m)-coloured) vertices of the pocket are never in X₉ in those 18;
- the crossing vertices are **not** in K₈ of the breaking run (0/19 ⊆), and meet K₈ of the other run in 1/19 only;
- they are in X₈ in 14/19, so mostly the disagreement predates step 8.

## 4. Mirror in pair form [proved]

`gammaOrbit_mirror` sends the cycle to the same state set traversed backwards, with (type, k) ↦ (type, 2 − k).
- The exchange pair of the mirror cycle consists of the mirror images of the R3k4 states of the mirror orientation, which are the R3k3 states (position 2) of the original.
- A step-8 break (R3k0 → R1k2) read backwards is a restoration at R1k0 → R3k2, which is step 3 of the mirror, i.e. a k = 3 failure of the mirror.

So A₃₄′(L = 20) in one orientation ⇔ "the two members of the mirror pair do not both fail at k = 3". Since k = 4 failure ⇒ k = 3 failure in the same period (894/896 Job AV periods; the 2 exceptions are the two orientations of p25 #16945 h3), the mirror form adds no constraint on the data. p25 #16945 is the k4-only / k3-only cycle. It is the single exception to every statistic in this note, as it is for Job AU.

## 5. The antisymmetry principle

### 5.1 Statement [proved]

The hypothetical double break (B(c) ∧ B(d)) is invariant under the exchange c ↔ d: (E2) and (E3) are symmetric. Hence any refutation must do one of two things.

- **(i) Break the symmetry with a phase.** Find Φ (any function of a colouring, relabelling-invariant) with
  **B(u) ⇒ Φ(u₀) < Φ(u₁₀)** for every DL period run u₀, …, u₁₀.
  - On an L = 20 Γ-cycle this gives Φ(c) < Φ(ρd) = Φ(d) and Φ(d) < Φ(c) if both break: a contradiction.
  - This is a **one-period** statement, valid or not on open runs. Open double breaks only give Φ(u₀) < Φ(u₁₀) < Φ(u₂₀), which is consistent.
  - It escapes NightPotential's obstruction. That obstruction concerns per-step potentials whose sum over the orbit must vanish; here Φ is free to decrease in the non-breaking period.
  - It is precisely the "two-period scope with a phase" NightPotential asked for, now in a closed form. Note that it also forbids breaks on any L = 10 cycle, which is consistent.
- **(ii) Find a symmetric planar incompatibility.** Show that two pocket curves C_c (in c₉) and C_d (in d₉), with equal hole colours and coinciding outside X₉, cannot coexist with the healing of both splits by steps 0, 1 of the other run (c's split is healed by ρ of d's steps 0, 1, and vice versa).

**Caution.** A test of (i) on the 19 single-break Γ-cycles alone is circular: Φ = [k = 4 failure at R3k4] passes trivially. Only the one-period form on *open runs* (or a proof) has content.

### 5.2 Candidates [data]

`antisym.py` (Job AV, 19 breaking cycles, all ten positions, Φ = f(breaking run_i) vs f(other run_i)):
- **Colour-class sizes of c(p), c(m), c(y), c(z):** none is sign-consistent on 19/19. They are tied (difference 0) at most positions, often in all 19 (e.g. positions 5–7 for all four colours). The two runs carry equal colour-class sizes there.
- **|K_i| (the step-i component):** sign-consistent on 18/19 at every position, with an alternating pattern: breaking run larger at positions 0, 1, 4, 5, 8, 9 and smaller at 2, 3, 6, 7. The exception is p25 #16945 mirror h3, the AU exception again.
- **Job AU's Φ:** Φ = |K_{c(p),c(m)}(p)| at R3k4 (here B(c) ⇒ the failing visit d₀ is larger) is 18/19, with the same exception (9 vs 10).
  - Φ′ = |K_pm(p)| − |K_J(z)| at R3k4 separates 19/19 (Job N fields: failing (9,10,1), other (10,12,12)), but trivially so: K_J(z) is the joined component exactly when there is no failure. That is the circularity of the caution above.

`phiopen.py` tests the one-period form on open runs (gentri orders 22–24): the R3k4 eight steps before a step-8 break against the failing R3k4 after it, for Φ ∈ {K_pm, J_y, J_z, K_pm − J_z, K_pm + J_y − J_z}.
- At orders 22–23 there are 0 test cases: breaks occur within the first 8 states of every run.
- At order 24 there are 4 test cases (`phiopen-24.txt`), including the double break 24 #3611 h0, where u₀ itself fails:
  - Φ = K_pm increases across the break in 4/4, so it is consistent with (i), including the double break;
  - so do K_pm − J_z and K_pm + J_y − J_z;
  - J_y and J_z alone do not.
- **Conclusion:** the sample is far too small. The local census cannot test (i); it needs Studio open runs (Job AL's 72,643 order-27 windows).

## 6. The one isolated statement

Neither (i) with a natural Φ nor a proof was reached. The statement below is the sharpest one that (a) closes A₃₄′(L = 20), (b) is about the two pockets in one frame, and (c) is testable on Job AV records.

**Exchange Pocket Lemma (EPL) [conjecture].** Let u, v be two DL R1k2 colourings at a Hole6 with u|_H = v|_H (same frame, so the same pocket pair {α, A} and the same J pair). Let X = {u ≠ v}. Suppose u has a pocket path Q_u (w⁺ ⇝ m in G_{α,A} − {p, x⁺}). Then every vertex of X ∩ Q_u that is α in u is **not** α in v, and v's G_J-component of z contains such a vertex.

Consequence: v has no pocket, i.e. ¬B for v's run.
- v's G_J-component of z then contains a vertex x of Q_u with v(x) ∈ J pair.
- If v also had a pocket C_v, z's G_J-component in v would lie inside C_v.
- Then C_v and C_u would both pass p x⁺ w⁺ … m and enclose z. By §3.3, symmetric in u, v, the J-vertex x lies inside C_v.
- Applying EPL to (v, u) gives a vertex inside C_u that is α in v and J-coloured in u.
- Two such crossings of curves through the same four points p, x⁺, w⁺, m, with everything else on disjoint colour classes, are incompatible by the Jordan curve theorem. **This last step is the gap.** It is a two-curve parity statement that I could not finish. It is where degree 6 (a single m, so both curves pass through the same m) enters.

**Test of EPL (Studio, minimal):** on Job AV's 19 breaking cycles, with u = breaking run₉ and v = other run₉:
- (a) X₉ ∩ Q_u ∩ {u = α} ⊆ {v ≠ α}: this is automatic, since X₉ is disagreement;
- (b) v's G_J-component of z contains a vertex of X₉ ∩ Q_u ∩ {u = α}. [data: 18/19 by the colour check of §3.3; the component check needs adjacency, which AV does not record.]

The real content is EPL **without** the hypothesis ¬B(v). It can only be tested on pairs (u, v) that are *not* from one Γ-cycle: for example all pairs of DL R1k2 colourings of one hole with equal hole colours, both with a pocket. EPL predicts that no such pair has X ∩ Q_u ∩ {u = α} empty in both directions. This is a single-hole enumeration (all colourings of T − h with the fixed hole colours) and needs no dynamics. **If pairs with two pockets exist abundantly among arbitrary hole-synchronised colourings (likely), then EPL as a static statement is false, and the closure must use G (the 10-step map), not just hole synchronisation.** That is the decisive test to run first.

### 6.1 Witness p26 #87942 h22 (Studio Job AZ; `witness.py` → `witness-output.txt`) [data]

This witness has full rotation, 26 vertices, and every far vertex within distance 2 of the ring. It is also Job AY's exception to the R1k1 fixed-point form.

- **Exchange pair.** Both orientations satisfy:
  - hole synchronisation at all 10 positions, with ρ a 3-cycle fixing α;
  - |X_i| = 7, 6, 7, 4, 5, 4, 5, 4, 5, 4.
  - The breaking run's pocket at R1k2 is m plus 7 far vertices. The partner d₉ has no pocket.
- **Crossing lemma (§3.3) checked with the graph.** X₉ = {2, 8, 12, 18} (plantri; mirror {2, 5, 8, 12}).
  - X₉ ∩ pocket = {8, 12}.
  - In d₉, z is joined to y and w₂, and deleting {8, 12} cuts z from both in both orientations.
  - The colours (c₉, d₉) on {8, 12} are (pocket colour, J colour) in both orientations.
- **Static count.** With the hole colours of the breaking R1k2 state fixed, T − h has only **12** colourings.
  - Plantri: exactly **1** is DL with a pocket (c₉ itself). So at this hole in this orientation, A₃₄′(L = 20) follows **statically**: d₉ ≠ c₉ shares the hole colours, so it cannot have a pocket.
  - Mirror: **2** DL pocketed colourings, and static EPL fails on both ordered pairs.
  - **Static EPL is therefore [killed]**, already on the smallest witness. Hole synchronisation alone does not forbid two pockets; the closure must use G (that d = Gc and c = Gd), i.e. the dynamics of the ten steps.
- **Reading.** The second pocketed mirror colouring is not the partner d₉ (d₉ has no pocket). The useful static quantity is therefore "the number of DL pocketed colourings among those with the given hole colours, *restricted to the G-image of the pocketed one*". The next test: for the second pocketed mirror colouring u′, compute its run and G u′; it is predicted not to be DL through ten steps, or G u′ ≠ the partner structure.

## 7. The R1k1 forest form (NightSigmaImage §3; coordinator's request)

**Status correction (Studio Job AY, received after 04:42):** "k = 3/4 failure in a period ⇔ σ fixed at R1k1" holds in 550/552 degree-6 periods and fails at p26 #87942 h22 (both orientations: k = 4 and k = 3 failures, no position-1 fixed point). p26 #87942 h22 is one of the 19 breaking L = 20 cycles. So the equivalence below is **killed as an exact form**, and the forest restatement is not a reformulation of A₃₄′. The pair identification (first paragraph) remains correct. AY also confirms that a fixed point's σ pair is forced by the position (1: {1,2}, 3: {1,3}, 4: {1,2}, …; positions 0 and 2 are never fixed); at position 1 this agrees with the J pair found here. The rest of this section is kept for the record and is not used elsewhere.

**Pair identification [proved from the table].**
- At R1k1 (position 1), the frame has α = x₄ = 0, μ = x₀ = 3, A = x₂ = 1, B = x₃ = 2.
- Lemma Fix (`QuarterSigmaFix`, general form): σ is fixed ⇔ the {A, B}-graph is acyclic, with {A, B} = {1, 2}.
- At R1k1, y = w₄ = 1 and z = w₀ = 2. So **the forest pair at R1k1 is the J pair {c(y), c(z)}**.
- Its complement {α, μ} = {0, 3} = {c(m), c(p)} (p = 3, m = 0 at position 1) is the pm pair.
- In NightSigmaImage's labels of position 0, {μ₀, A₀} = {1, 2}: the same pair.

**A₃₄′(L = 20), forest form.** Assume "failure in a Γ period ⇔ σ fixed at R1k1" (NightSigmaImage, 128/128; Job AY verifying). In the exchange-pair normal form, the two R1k1 states are c₁ and d₁, with the same hole colours and the **same** pair {1, 2}; period 1's "rotated pair σP" is the pull-back artefact again. So:

> **A₃₄′(L = 20) ⇔ rank G_{1,2}(c₁) + rank G_{1,2}(d₁) ≥ 1**: the J-graphs of the two members at R1k1 are not both forests.

What the tools give:
- **Six-pair Euler identity** (`QuarterEuler`): Σ_P rank_P(s) = Σ_P comp_P(s) − 8 ≥ 0 at DL states. Applied to c₁ and d₁, it bounds rank_J(c₁) + rank_J(d₁) from below only through the other five pairs, and those are unconstrained. Two forests are compatible with the identity as long as the other pairs carry the rank.
- **Total-rank parity:** Δ total rank is odd and |Δ| ≤ 3 per step (NightPotential). Over c₁ → c₁₁ = ρd₁ (ten steps) the change is even. Over d₁ → ρc₁ it is the negative of that. No constraint follows: this is the counting obstruction again.
- **Fan lemma** (`QuarterFan`): at R3, k ≤ 2, a vertex lies on an {A, B}-cycle ⇔ one of its {α, μ}-neighbours is outside K_σ. The R1 analogue at k = 1 would read: "G_J(c₁) has a cycle through u ⇔ some {0, 3}-neighbour of u is outside the σ-component K_{0,3}(x⁺)".
  - At R1k1, σ swaps the {α, μ} = {0, 3} component of x_{j+1} = p. So K_σ is the **pm component Π₁ of p at position 1**.
  - **Hence the fixed point ⇔ every {0,3}-neighbour of every J-vertex lies in Π₁, i.e. Π₁ ∪ {h} carries all of the {0,3} graph adjacent to G_J.**
  - This explains Job AU directly: the failing period has the large |K_{c(p),c(m)}(p)| (10–12 vs 5). The pm component must swallow the whole region of the J forest.
  - [data, `pmconn.py`] It is not literally the whole pm colour class at R3k4: Kpm_at_k4 < #(c(p) ∪ c(m))-vertices in 512/512 R3k4 visits. The test belongs at R1k1, where AV records no component.

**Precise R1k1 target [conjecture, testable].** For the exchange pair, Π₁(c) (p's {0,3}-component in c₁) and Π₁(d) (in d₁) cannot both be "J-saturating", i.e. both contain every {0,3}-neighbour of their J-graphs.
- They agree outside X₁ (|X₁| = 2–10).
- A J-saturating Π is the planar dual of a J-forest: Π₁ ∪ {h} is a {0,3}-tree-like region whose complement faces are J-trees.
- Two such regions differing on ≤ 10 far vertices with exchange under G is the same two-curve parity question as EPL. In the forest form it reads: **the J-forest of c₁ and the J-forest of d₁ coincide off X₁, and both span z, y and the J-vertices of the ring. Is their union (on the agreement set plus X₁ coloured J in either run) necessarily cyclic?**
  - If every vertex of X₁ is J-coloured in exactly one run, the union is the J-graph of a 3-colouring-like overlay; a cycle in it is forced iff the two forests attach X₁ to different components.
  - Testable on AV with adjacency (`jobav` needs the edge list added).

## 8. Why degree 7 escapes (two inserted vertices M, M′)

- **What survives.** Proposition E survives verbatim at (5,5,5,5,7): it uses only π-equivariance and the period colour rotation on the hole, with the same universal period, 406/406 (Job AC). The exchange-pair normal form and the antisymmetry principle hold there too.
- **The data.** At degree 7 consecutive breaks on Γ-cycles do occur (14 periods, Jobs AE/AR). So any argument for degree 6 must use something that fails at degree 7. The place is the pocket.
- **Degree 6.** The pocket lemma's ⇒ direction uses that p's only neighbours in the pair {α, A} at R1k2 are h, x⁺ and m. So every separating curve passes through p and m, and the two pockets C_c and C_d share the four points p, x⁺, w⁺, m and the edge p–m. The z-side of p is the single face triangle p z m, and z's neighbours on p's side are x⁺, p and m only.
- **Degree 7.** p has two inserted vertices: M next to y and M′ next to z. A pocket may close through p–M or through p–M′, so the two members' curves can pass p on **different** inserted vertices. The z–M′ edge can be A at R3k0 (NightA34 §4(b)), so the J-path of one run can enter z's region through M′ without crossing the other run's pocket at a far vertex. The crossing lemma §3.3 then has an escape route: P can cross between M and M′ along p's rotation, with no X₉ vertex.
- **Testable consequence.** At degree 7, in exchange pairs with a double break, the two pockets use different inserted vertices (one through M, one through M′), or the crossing set X₉ ∩ Q is empty. Job AR's gate pattern (the extra gate M_z, equally at either break) points the same way. EPL as stated is false at degree 7 exactly when this happens.

## 9. Requests (Studio)

1. Add the edge list (or rotation) of T − h to the Job AV records. With it:
   - test EPL (b) on the 19 breaking cycles;
   - run the static EPL test of §6 (all hole-synchronised pairs of pocketed R1k2 colourings at the 19 breaking holes). This decides whether hole synchronisation alone or the map G is needed;
   - test the R1k1 target of §7 (J-saturation of Π₁ at c₁ and d₁).
2. The one-period antisymmetric form B(u) ⇒ Φ(u₀) < Φ(u₁₀) on all order-27 open runs with a full period before the break, for:
   - Φ = |K_pm(p)| at R3k4;
   - Φ = |K_i| at the positions of the 18/19 alternating pattern (§5.2);
   - Φ = rank_J at R1k1.

   Any 0-exception Φ closes A₃₄′ on every Γ-cycle with L = 20 (and forbids breaks at L = 10). Report p25 #16945 mirror h3 separately.
3. At degree 7 (14 consecutive-break periods): which inserted vertex each pocket uses, and X₉ ∩ Q for both members.

## 10. Reproduction

All in `backgroundMaterial/planemap-structural/longtable/local-runs/31-nighta34two/` (reads `../27-studio-positive-config/jobav/jobav-cycles.jsonl`):

| script | content |
|---|---|
| `pairav.py` → `pairav-output.txt` | §2 checks (hole sync, τ = ρ², exchange, X_i), §3.3 crossing data |
| `antisym.py` → `antisym-output.txt` | §5.2 antisymmetric candidates |
| `pmconn.py` | §7 pm connectivity at R3k4 (0/512) |
| `phiopen.py` → `phiopen-24.txt` | §5.2 one-period form on gentri open runs |
| `witness.py` → `witness-output.txt` | §6.1 Job AZ witness: exchange pair, crossing lemma with the graph, static EPL |

`../30-nighta34/pair.py` is the same exchange-pair construction on the local engine. It found no (5,5,5,5,6) Γ-cycle at gentri orders 17 and 20–22.

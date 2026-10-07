# Night attempt: porting the Balanced-4CT Euler counting to the degree-5 hole

Math research worker (night), 6 October 2026. Hand reasoning, plus small single-core checks (scripts in the session scratchpad, not committed; they are re-derivable from §6). **Nothing here proves the quarter floor, R\*, or any class-level floor c > 0.** The new items are:
- a pairing-blindness lemma for Euler counts at the hole (§2);
- a rotation-number reformulation of the class identity (§3), with an exact consequence, **3F − U ≡ 0 (mod 5) in every Kempe class**, checked on all 14,109 replay classes;
- a precise statement of why no potential, Euler-type or otherwise, can close the floor while it uses only the link-changing moves (§4).

Labels: [proved] means a complete argument is given, modulo the reviewed tables of `MathQuarterFloorBijections.md` §1–§2 (cited as **QFB**). [sketch] means an argument with a gap that is named. [conjecture] means not proved. [data] means computed here.

Coordinator input (message received mid-task, local-runs/15-euler-pressure, c1703b2): over 243,727 states at orders 12–20, DL states are **not** closer to Euler saturation in any single-state bipartite graph (B_μ, B_α, lock union, μ vs {A,B}). §2 gives the structural reason.

---

## 1. Dual (Tait) picture of the hole [proved, elementary]

- Identify the colours with the Klein group V₄ = {0, a, b, c}. Each edge xy of G = T − v gets the Tait colour col(x) + col(y), which is one of a, b, c.
- **Faces of G.** G has n′ = n − 1 vertices, 3n′ − 8 edges and 2n′ − 6 faces. They are the pentagon P and **2n′ − 7 triangles, an odd number.**
- **Parity at P.** For a Tait colour c, the dual c-edges form a matching on the triangles together with k_c(P) edges at P. Counting endpoints shows that (2n′ − 7) + k_c(P) is even, so every k_c(P) is odd.
  - Since k_a + k_b + k_c = 5, the multiplicities at P are **(3, 1, 1)**. Call the colour that appears three times the triple colour t, and the other two the singles.
- **Tokens.** Mark the two link edges whose Tait colours are the singles. Call them the tokens, at positions in Z₅ (edge e_k = x_k x_{k+1}).
  - Filled F_i: (W,X,Y,X,Y) at positions i..i+4 gives the Tait colours (c₂, c₁, c₁, c₁, c₃) on e_i..e_{i+4}. The tokens are {i+4, i}, which are **adjacent**.
  - Unfilled U_j: (α,μ,α,A,B) gives (t, t, s₁, t, s₂), since α+μ = A+B = t. The tokens are {j+2, j+4}, which are **at distance 2**.
- **So: filled ⇔ the two single Tait edges at P are consecutive.**
- **Slots.** For each single s, the dual {t, s} subgraph has degree 4 at P and degree 2 elsewhere.
  - Its component through P is two loops at P, and they pair the four edges **non-crossingly**. This is Jordan: a crossing pair of loops meeting only at P is impossible on the sphere.
  - Swapping one loop moves one token by one step, either toward the other token (a fill) or away from it (a rotation). This is exactly QFB's slot dichotomy (L1/L2, M2/M3), seen from P.

## 2. Euler at the hole is pairing-blind [proved]

**Lemma E.** Fix a state and a Tait colour c, and let {p,q} | {r,s} be the complementary colour split with p+q = r+s = c. Let:
- k_c be the number of Kempe components of types pq and rs together (the components of the primal subgraph H_c of c-edges);
- C₀ be the number of components of the dual c′c″-subgraph that avoid P.

Then

  k_c = C₀ + 2 if c is the triple colour at P, and k_c = C₀ + 3 if c is a single at P.

*Proof.*
- Each triangle has exactly one c-edge. So the faces of the plane graph H_c on the sphere are exactly the unions of G-faces glued along non-c edges, that is, the components of the dual c′c″-graph (P included). That gives f(H_c) = C₀ + 1.
- Euler for a plane graph with k components gives n′ − e + f = 1 + k.
- Counting dual c-edge endpoints gives e_c = ((2n′ − 7) + k_c(P))/2. That is n′ − 2 when c is the triple colour, and n′ − 3 when c is a single.
- Substituting gives the formula. ∎

Equivalently: resolve P into a small disc and the c′c″-curves through P into chords (1 chord if c is the triple colour, 2 if it is a single). This gives D′_c disjoint simple closed curves, and **k_c = D′_c + 1**. That is the region tree: on the sphere, D′ disjoint curves cut out D′ + 1 regions.

**Where χ = 2 enters (first time).**
- On a closed orientable surface of genus g, D′ disjoint simple closed curves cut out D′ + 1 − r regions, where r ≤ g is the rank of their span in H₁(S; Z₂). [sketch: Mayer–Vietoris] On the torus, r ∈ {0, 1}.
- So the exact count, and the non-crossing pairing at P that creates the slots, are both sphere facts.

**Corollary (why per-state Euler cannot see the locks).**
- A lock is the choice between the two non-crossing pairings of the {t, s} loops at P (QFB §1).
- Both pairings produce the same number of chords, so Lemma E holds with the same constant for either.
- The hole's whole Euler footprint is an additive constant: Σ_c k_c = Σ_c C₀,c + 8, compared with + 3 for a closed triangulation (k_c = C_c + 1).
- Every per-state edge or component count is therefore satisfied equally by DL and non-DL states. That is what the coordinator's 243,727-state run found: DL minimum slack 4, never saturated.
- Contrast with Kawarabayashi–Yoneda. There, "all three H_i connected" costs 2|V₁| + n − 3 edges against a budget of 2n − 4, a **deficit linear in n**. A lock costs one connectivity bit between two named vertices: O(1), and invisible to the counts. [proved for the Euler identities. The broader claim, that no per-state counting argument can work, is a meta-statement and is not proved.]

## 3. The class identity as a rotation number [proved, modulo QFB §2]

**The out-move permutation π.** QFB §2 lists four bijections. Each takes one "out-slot" of a state to one "in-slot" of another state:

| from (out-slot) | map | to (in-slot) | λ (token step) |
|---|---|---|---|
| U_j with lock 2 | R₊₃ (swap the {α,A}-component of x_{j+2}) | U_{j+3} with lock 1 | +1 |
| U_j with lock 2 failing | φ_B⁻¹ (swap the {μ,B}-component of x_{j+4}) | F_{j+3} with M2 short | −1 |
| F_i with M3 short | φ_A (swap the {Y,Z}-component of x_{i+2}) | U_{i+1} with lock 1 failing | −1 |
| F_i with M3 long | τ (swap the {W,X}-component of x_{i+3}) | F_{i+1} with M2 long | −3 |

The four domains partition the class (unfilled states by lock 2, filled states by M3), and so do the four codomains (unfilled states by lock 1, filled states by M2). So:

**Lemma Π.** π, defined by the table, is a permutation of every Kempe class. [proved, given QFB's bijections]
- Every state has exactly two link-pattern-changing neighbours, π(s) and π⁻¹(s), up to the alternative component (QFB §2, "Alternatives").
- So the class splits into **π-cycles**. A Γ-path of QFB is an unfilled run of a π-cycle. A Γ-cycle is a π-cycle with no filled state.

**Token sum.** Let σ(s) ∈ Z₅ be the sum of the two token positions: σ = 2j + 1 on U_j and σ = 2i + 4 on F_i. Checking each row of the table gives σ(πs) − σ(s) ≡ λ(s) (mod 5). Each row's λ is a collision-free motion of the two tokens around P:
- one token moves +1 (R₊₃), or −1 (φ_A, φ_B⁻¹);
- for τ, one token moves −3. The alternative lift, both tokens +1, gives +2. **The choice is a convention, and only −3 makes the identity below exact.**

**Theorem W.** For every Kempe class S (and for every π-cycle Z separately):

  3F − U = −Σ_{s∈S} λ(s) = −5 Σ_Z w(Z),

where the winding number w(Z) := (1/5) Σ_{s∈Z} λ(s) is an integer.

*Proof.*
- Write U^{ℓ1}, U^{ℓ2} for the unfilled states with lock 1 and with lock 2, U^{¬ℓ1}, U^{¬ℓ2} for those without, and F^{M3s}, F^{M3L} for the filled states whose M3 bit is short or long.
- By the four bijections:
  - |F^{M3s}| = |U^{¬ℓ1}|;
  - |F^{M2s}| = |U^{¬ℓ2}|;
  - |F^{M3L}| = |F^{M2L}|, hence |F^{M3s}| = |F^{M2s}| and |U^{¬ℓ1}| = |U^{¬ℓ2}|.
- Then Σλ = |U^{ℓ2}| − |U^{¬ℓ2}| − |F^{M3s}| − 3|F^{M3L}| = U − 3|U^{¬ℓ2}| − 3|F^{M3L}| = U − 3F.
- Integrality: on each π-cycle, Σ (σ(πs) − σ(s)) = 0 in Z₅, so Σ_Z λ ≡ 0 (mod 5).
- Per cycle: F_Z = e + t and U_Z = r + e, where e, t and r count the φ_A, τ and R₊₃ steps of Z (each excursion uses exactly one φ_A and one φ_B⁻¹). So 3F_Z − U_Z = 2e + 3t − r = −Σ_Z λ. ∎

**Corollaries.**
1. **3F − U ≡ 0 (mod 5) in every Kempe class**, and in every π-cycle. Equivalently, |S| + F ≡ 0 (mod 5). The same holds up to renaming, since 24 is invertible mod 5. [proved] [data: 14,109 of 14,109 replay classes, orders 12–22, `quarter-floor-replay/out`; 0 exceptions.]
   - This is **not** visible in the earlier form of the identity: Σ_P(1 − d(P)) has no reason to be ≡ 0 mod 5 term by term.
2. **Quarter floor ⇔ the total winding of π over each class is ≤ 0.** A π-cycle on its own has filled fraction ≥ 1/4 iff w(Z) ≤ 0. [proved]
3. **Per-cycle formula.** 5w(Z) = Σ_{excursions in Z} (d − 1) − 3t_Z for a cycle with filled states, and w(Z) = L/5 > 0 for a Γ-cycle of length L.
   - An N₀ state counts as an excursion with d = −1.
   - This is QFB's identity regrouped by π-cycle, with 1.5·L_F = 3t (each τ step uses two long bits, so L_F = 2t).
   - At the floor every term vanishes, so every π-cycle has w = 0.
4. **R\* ⇔ no Kempe class consists only of positive-winding π-cycles.** A class with F = 0 is a union of Γ-cycles. [proved]

**Data on π-cycles [data; own code; orders 12–21 every degree-5 hole of gentri, up to renaming; order 22 see §6].**
- Every class has Σ_S λ = U − 3F, and every cycle has Σ_Z λ ≡ 0 mod 5. There are 0 assertion failures, and Lemma E has 0 failures, over all 4,381 classes and all their states.
- **Floor class gentri 17 #1, holes 0 and 2** (64 states up to renaming, 16 filled): π-cycles of lengths 4, 4, 4, 8, 16 and 28, with 1, 1, 1, 2, 4 and 7 filled states. **All have w = 0.**
  - So QFB's check C5 (that ψ = φ_B⁻¹R₊₃R₊₃φ_A is the identity) **fails here**: there are π-cycles of length 8, 16 and 28.
  - The quarter is nevertheless exact on every cycle.
- **Positive-winding π-cycles are rare.** There are 6 in 4,381 classes:
  - order 17: gentri #3, holes 0 and 16. Class 100/40, with a pure Γ-cycle of length 20 (w = +4) and one cycle of length 80 (40 filled, w = −16).
  - order 20: #58 hole 18 and #60 hole 19. A cycle of 21 states with 4 filled, w = +1, which is a **mixed** cycle with an excursion of d ≥ 2.
  - order 21: #96 hole 2 and #134 hole 0. A cycle of 14 states with 1 filled, w = +2.
  - In the classes listed, the class's negative winding outweighs the positive by these factors (N/P):
    - order 17: 4;
    - order 20: 24 and 24;
    - order 21: 21.5 and 15.
  - (A first draft printed the maximum of N/P instead of the minimum. These factors are recomputed by hand from the printed cycle lists.)
- **Order 22** (every degree-5 hole, 9,442 holes, 9,728 classes, 555 s):
  - Lemma E has 0 failures, and Theorem W's asserts have 0 failures.
  - There are 11 floor classes, all with every w = 0.
  - **17 positive-winding π-cycles**, 14 of them mixed (containing filled states), in 17 classes.
  - Inspected examples: gentri 22 #369, holes 1 and 6, have cycles (10 states, 5 filled, w = −2), (17, 3, +1) and (188, 82, −28), so N/P = 30. Gentri 22 #385 hole 17 has N/P = 13.
  - The order-22 minimum of N/P was not computed.
- **Side observation [data, unexplained].** Write S for the signed spin sum of G's triangles: each triangle counts +1 or −1 according to whether its colouring preserves or reverses orientation onto ∂Δ³. This is the folding degree times 4, minus the hole's share. Along π-steps at orders 16–17:
  - R₊₃ steps have ΔS ≡ 4 (mod 8);
  - τ steps have ΔS ≡ 0 (mod 8).
  - If that is a theorem, every Γ-cycle has even length, hence length ≡ 0 (mod 10). [conjecture]

## 4. Why no potential argument can close it, and where the global step sits [proved and sketch]

**Lemma N (no coboundary bound on π).** There is no function Φ on the states of a class with Φ(πs) − Φ(s) ≥ λ(s) for every s, once the class contains a positive-winding π-cycle.
- Summing over that cycle gives 0 ≥ 5w > 0.
- Such classes exist (gentri 17 #3, hole 0).
- So **no potential, whether Euler-type, a degree, a component count, or KY's |V₁|, can prove the floor using only the link-changing moves.** These are exactly π^{±1}. [proved]
- Kawarabayashi–Yoneda is a descent argument of exactly this type. Its target (|V₁| < n/2) has linear Euler slack. The hole's target has O(1) slack (§2), and its move graph contains positive-rotation cycles.

**What the global step must do.**
- The floor says that, within one Kempe class, the negative winding of some π-cycles pays for the positive winding of others (Γ-cycles and long DL excursions).
- Different π-cycles share no state. They are joined only by **link-pattern-preserving** swaps:
  - {α,μ}- and {A,B}-components;
  - components that miss the link;
  - {μ,A} when lock 1 holds, and so on.
- Any proof must transport winding along those swaps. This matches the growing matching radius (6 pooled at order 24): the transport distance grows.

**A cohomological framing of the transport [sketch].**
- Extend λ to every Kempe edge:
  - 0 on pattern-preserving swaps;
  - the token step on pattern-changing swaps (either component);
  - −3 or +3 on F→F swaps, as in π.
- Let X be the Kempe 2-complex: states, all swaps, and a square for each pair of swaps on disjoint components.
- If λ were closed on every square and H¹(X) = 0, every π-cycle would have w = 0. That is false at gentri 17 #3.
- So either λ fails to be closed on some squares, which happens where a pattern-preserving swap reroutes a slot's loop at P, or X has H¹ ≠ 0.
- A proof of the floor would bound the **sum** of the windings, not each one. It would therefore have to control the "curvature" of λ on squares where a pattern-preserving swap meets a slot loop.
- This is the one place where I can see a weighted or iterated Euler count entering: summing a local Gauss–Bonnet-type identity over the squares of X. **I could not make the signs work, and I have no evidence they do.**

**Where χ = 2 enters, a second time.**
- The local parts all use Jordan at P: the non-crossing pairing, the slots, and π itself (Lemma Π).
- On the torus a crossing pairing can occur, and the π-structure breaks. Mohar–Salas classes would then be compatible with every local statement here.
- The sign statement Σ w ≤ 0 is where χ = 2 would have to enter a **second** time, globally. Nothing above supplies it.


## 4a. Coordinator's suggestion: sum the bipartite Euler bound over all six pairs and all states [proved, negative]

This responds to the coordinator's message, sent after the torus run (local-runs/18-torus-floor: 21,915 targetless classes out of 86,175, with frozen single-state classes from n = 16).

**Single-state sum.**
- Each bichromatic graph G_pq is a plane graph with k_pq components. Its cyclomatic number is e_pq − (n_p + n_q) + k_pq.
- Summing over the six pairs gives Σ e_pq = |E(G)| = 3n′ − 8 and Σ (n_p + n_q) = 3n′. So

  Σ_{6 pairs} k_pq = 8 + Σ_pairs cyc(G_pq) ≥ 8.

- By Lemma E, Σ_pairs cyc(G_pq) = Σ_c C₀,c, so this is the same identity.
- **This proves the audited "no frozen state" fact:**
  - six connected subgraphs would give Σk = 6 < 8;
  - more sharply, each single colour c at P has k_c ≥ 3 (two chords give three regions), so at least two pairs are disconnected, and **at most 4 of the 6 are connected**.
- On the torus the bound is Σk ≥ 8 − 2g′, where g′ ≤ 2 depends on how many curves are non-separating. That allows Σk = 6, which is a frozen state, exactly as the coordinator found.

**Class sum.**
- Summing over a class gives Σ_{s∈S} Σ_pairs k_pq(s) ≥ 8|S|, with equality-defect Σ_s Σ_c C₀,c(s).
- **No term in this inequality mentions F, U, the locks or DD_j.** The +8 is the same for filled and unfilled states (both have Tait multiplicities (3,1,1) at P), and for either pairing at P (§2).
- So the summed inequality is satisfied by any multiset of states, including a hypothetical targetless class. It cannot be converted through Math's identity, because the identity's deficit terms (D_cyc, d(P) − 1) have no Euler counterpart.
- **The sum fails to close at the first step.** The Euler base fact distinguishes frozen from non-frozen states. The floor needs to distinguish DL from filled, and both are non-frozen with slack ≥ 4 (coordinator's data).
- A weighted sum Σ_s w(s)·(Σk − 8) would need weights correlated with filledness that telescope along Kempe moves. Lemma N (§4) shows that no weighting that changes only along π can do it.

**Torus sanity check.** The argument gives nothing on the torus, as it must. But it also gives nothing for the floor on the sphere. χ = 2 is used, and only to exclude frozen states, which is strictly weaker than R\*.

## 5. Status against the task list

1. **DL bound or the full floor by Euler counting:** not proved.
   - Exact reformulation: floor ⇔ Σ_Z w(Z) ≤ 0 (Theorem W).
   - Summing Lemma E over a class gives the empty identity Σ_s Σ_c (k_c − C₀,c) = 8|S|.
2. **A class floor F ≥ c|S|:** not proved, and not attempted beyond Lemma N. Such a floor implies R\* and hence 4CT. Lemma N shows that any argument confined to π^{±1} is circular or false.
3. **A single-DL-state Euler lemma:** ruled out in its Euler-count form, by Lemma E's pairing-blindness and by the coordinator's data. The theta (lock chains plus hole) is visible only through the pairing, which Euler ignores.
4. **Failure analysis:** given in §2 and §4.
   - The quantity to control is the total π-winding of a class. Equivalently: DL-chain excess plus Γ-cycle length, against N₀, long bits and d = 0 paths.
   - Euler gives O(1) slack (a constant +8 that does not depend on the pairing) against unboundedly many DL states.
   - Any fix must move winding between π-cycles across pattern-preserving swaps.

**Most promising next step.**
- Test whether λ, extended as in §4, is **closed on every commuting square** of the Kempe complex at orders ≤ 19.
- If the failures ("curvature") are localized and have a sign, the floor becomes a Gauss–Bonnet-type inequality on X. That would be a genuinely global, class-level statement in which χ = 2 could enter a second time.
- If the curvature has no sign, the Euler-port line should be closed.

## 6. Reproduction (no team code imported)

- Lemma E and Theorem W were checked with a stdlib script:
  - It enumerates the 4-colourings of T − v up to renaming, builds Kempe classes by union-find, and builds π from the table in §3.
  - It asserts that π is a permutation of each class, that Σ_Z λ ≡ 0 mod 5 on each cycle, and that Σλ = U − 3F per class.
  - It checks Lemma E per state and per Tait colour, using the dual of the triangles plus P.
  - Gentri files: `backgroundMaterial/planemap-structural/studiointel/gentri/triN.txt`, with the hole given by vertex index as in `qf_replay.py`.
- The mod-5 check over replay data reads `backgroundMaterial/planemap-structural/longtable/audit/quarter-floor-replay/out/qf-*.jsonl` and tests (3·ΣF − ΣU) mod 5 per class vector.
- All runs were single core: orders 12–21 took about 3 minutes and order 22 about 9 minutes.

# Quarter floor: the block bijections, an exact per-class identity, and where part (b) fails

Math research worker, 6 October 2026. **Hand only, unreviewed.** No code was run. The checks in §7 are written as specs for local compute. It builds on `MathQuarterFloor.md`, `MathQuarterFloorLemmaA.md` (Lemma A, φ), `MathConfinementAttack.md` (Step 1, Theorem A), and the accepted Tait lock criterion `pd2_lock_proof.md` (cited as **pd2**, with its Steps 0–2 and Corollary).

## Verdict, first

- **[hand] Every move in the block structure is an explicit Kempe swap, with an exact domain, an exact codomain and an explicit inverse.** There are three families: φ_A (F_i → U_{i+1}), φ_B (F_i → U_{i+2}) and the rotations R+3/R+2 (U_j ↔ U_{j+3}). Each domain is a local Jordan condition, namely one of the two non-crossing matchings at the pentagon node P.
- **[hand] Every state has exactly two link-pattern-changing moves**, one per "slot", and each move is a bijection between slot sets.
- **[hand] An exact identity for every Kempe class (§4):**
  3F − U = 2N₀ + (3/2)L_F + Σ_{paths P of Γ} (1 − d(P)) − D_cyc.
  Every term is defined in §3–§4.
- **[hand] Part (b), the coordinator's update (§5).** The 2-swap rule is **ρ = φ ∘ R+3**:
  - swap the {α, A}-component of x_{j+2};
  - then swap the {A, B}-component of x_{j+2}.

  ρ is injective from {d ∈ D_j : R+3 d is not DL} into F_{j+1}. Its image is disjoint from Lemma A's images. The per-j counting lemma then satisfies an **exact identity**: its slack equals a list of nonnegative terms **minus |DD_j|**, where DD_j = {d ∈ D_j : R+3 d ∈ D_{j+3}} is the set of doubly locked states whose rotation is again doubly locked.
- **(b) fails exactly at DL→DL rotations.** That is where the global step lives. It is the same unresolved step as Try 1 of `MathConfinementAttack.md`: whether lock 2 survives a rotation. pd2's Corollary gives lock 1 for free and nothing more.

---

## 0. Setup and notation

- v has degree 5, and its link x₀..x₄ is in rotation order (indices mod 5). A state is a proper 4-colouring of T − v.
- **Filled f ∈ F_i:** the link is (W, X, Y, X, Y) at positions i, …, i+4. W is the singleton, and the fourth colour Z is absent.
- **Unfilled s ∈ U_j:** the link is (α, μ, α, A, B) at positions j, …, j+4, with m = x_{j+1}, a = x_{j+3} and b = x_{j+4}.
  - Lock 1: m ~ a in {μ, A}.
  - Lock 2: m ~ b in {μ, B}.
  - DL means both locks hold.
  - "Index j" means the pair {j, j+2}. The task's U_{i+1,i+3} is U_{i+1}, U_{i+2,i+4} is U_{i+2}, and D_{i+1,i+4} ⊆ U_{i+4}.
- σ(s; {p,q}; x) denotes swapping the {p,q}-component of x in s.
- **All counting is over labelled colourings.** Every map below commutes with renaming, and S₄ acts freely (Math 8bc6685). So each count is 24 times the count up to renaming, and every ratio and identity is the same either way.
- **Tait.** Write c1 = X+Y = W+Z, c2 = W+X = Y+Z and c3 = W+Y = X+Z. The boundary of a {p,q}-component consists of whole dual paths and cycles in the two Tait colours other than p+q (pd2 Step 1).
- **Region principle [hand, pd2 Steps 0–1].** The link vertices that lie in one region cut out by the (c,c')-paths through P lie in a single Kempe component of the complementary type. Cycles that avoid P cannot separate link vertices, since the pentagon is connected.

## 1. All link-changing swaps of a single state [hand]

**Filled f ∈ F_i.** Six colour pairs; the link vertices each pair meets:
- {W,Z}: x_i only. The swap renames x_i, and f stays in F_i.
- {X,Y}: x_{i+1}..x_{i+4}, all in one component (they form a path on the link). The swap stays in F_i.
- {W,X}: x_i and x_{i+1}, adjacent, plus x_{i+3} or not.
  - If x_{i+3} is in the component, the swap stays in F_i.
  - If not, swapping x_{i+3}'s component (or x_i's) gives **F_{i+1}**.
- {W,Y}: x_i and x_{i+4}, plus x_{i+2} or not. If x_{i+2} is not in the component, the swap gives **F_{i+4}**.
- {Y,Z}: x_{i+2} and x_{i+4}. If they are in one component, the swap stays in F_i. If they are in different components, swapping either component gives **U_{i+1}**.
- {X,Z}: x_{i+1} and x_{i+3}. If they are in different components, either swap gives **U_{i+2}**.

**Dichotomy M3 [hand].** Exactly one of the following holds:
- (short) x_{i+2} ≁ x_{i+4} in {Y,Z}, and x_i ~ x_{i+3} in {W,X};
- (long) x_{i+2} ~ x_{i+4} in {Y,Z}, and x_{i+3} ≁ x_i in {W,X}.

*Proof.* Both chain types have (c1,c3) boundaries. P has (c1,c3)-degree 4, at e_{i+1}, e_{i+2}, e_{i+3}, e_{i+4}. By pd2 Step 0 there are only two non-crossing matchings:
- {e_{i+1}e_{i+2}, e_{i+3}e_{i+4}} cuts off corner x_{i+2} and corner x_{i+4}, leaving x_i, x_{i+1} and x_{i+3} in one region. That is "short".
- {e_{i+2}e_{i+3}, e_{i+4}e_{i+1}} cuts off x_{i+3}, and puts x_{i+2} and x_{i+4} in one region. That is "long".

Apply the region principle. ∎

**Dichotomy M2** is the same argument with (c1,c2) and the edges e_i..e_{i+3}:
- (short) x_{i+1} ≁ x_{i+3} in {X,Z}, and x_i ~ x_{i+2} in {W,Y};
- (long) the reverse.

So **each filled state has exactly two pattern-changing move types**:
- slot 3: M3 short gives a move to U_{i+1}; M3 long gives a move to F_{i+1};
- slot 2: M2 short gives a move to U_{i+2}; M2 long gives a move to F_{i+4}.

**Unfilled s ∈ U_j.** Every colour pair meets at least two link vertices:
- {α,μ}: contains x_j, m and x_{j+2}. The swap stays at index j.
- {A,B}: contains a and b. The swap stays at index j.
- {μ,A}: if lock 1 holds, the swap stays at index j. If lock 1 fails, either swap fills into **F_{j+4}** (Lemma A, Case 1).
- {μ,B}: if lock 2 holds, the swap stays at index j. If lock 2 fails, either swap fills into **F_{j+3}**.
- {α,A}: contains x_{j+2} and a, plus x_j or not. If x_j is not in the component, the swap is **R+3**, giving (α, μ, A, α, B) at index j+3.
- {α,B}: contains x_j and b, plus x_{j+2} or not. If x_{j+2} is not in the component, the swap is **R+2**, giving (B, μ, α, A, α) at index j+2.

**Dichotomy L2 [hand]: R+3 is defined ⇔ lock 2 holds.**
- (⇐) This is pd2 Corollary (i).
- (⇒) Suppose lock 2 fails. By pd2, the (β,δ)-matching at P is {e_j e_{j+1}, e_{j+3}e_{j+4}}. The middle region then holds x_j, x_{j+2} and a, so x_j and x_{j+2} lie in one {α,A}-component.

  Directly: if K = comp_{α,A}(x_{j+2}) missed x_j, then ∂K would contain e_{j+1} and e_{j+3} but not e_j, e_{j+2} or e_{j+4}. That forces the path e_{j+1}–e_{j+3}, a contradiction.

**Dichotomy L1 [hand]: R+2 is defined ⇔ lock 1 holds** (the mirror argument).

Corollaries:
- **One-swap fill ⇔ not DL [hand]**, by the enumeration above.
- **DL states have no filled neighbour.** This agrees with the data.
- **Each unfilled state also has exactly two slots:**
  - slot 1: if lock 1 fails, it fills into F_{j+4}; otherwise R+2 takes it to U_{j+2};
  - slot 2: if lock 2 fails, it fills into F_{j+3}; otherwise R+3 takes it to U_{j+3}.

## 2. The bijections [hand]

Each map is a single swap. Its inverse swaps the same vertex set back: swaps are involutions, and a swap preserves the vertex set of every component of its own colour pair.

| map | rule | exact domain | exact codomain |
|---|---|---|---|
| φ_A | f ↦ σ(f; {Y,Z}; x_{i+2}) | F_i with M3 short | U_{i+1} with lock 1 failing |
| φ_B | f ↦ σ(f; {X,Z}; x_{i+1}) | F_i with M2 short | U_{i+2} with lock 2 failing |
| R+3 | s ↦ σ(s; {α,A}; x_{j+2}) | U_j with lock 2 | U_{j+3} with lock 1 |
| R+2 = R+3⁻¹ | s′ ↦ σ(s′; {α′,B′}; x_{j′}) | U_{j′} with lock 1 | U_{j′+2} with lock 2 |
| τ | f ↦ σ(f; {W,X}; x_{i+3}) | F_i with M3 long | F_{i+1} with M2 long |

**Checks.**
- **φ_A**, for i = 0: f = (W,X,Y,X,Y) maps to (W,X,Z,X,Y), at index 1 with m = x₂, a = x₄ and μ = Z, A = Y.
  - The {Z,Y}-component of m is the swapped set K, which misses x₄. So lock 1 fails.
  - The inverse is σ(s; {μ,A}; m), which is Lemma A's Case 1 using m's component rather than a's.
- **R+3:** lock 1 of R+3 s is lock 2 of s (pd2 Corollary ii). Mirror: lock 2 of R+2 s′ is lock 1 of s′. R+2 at j′ = j+3 swaps the component of x_{j+3}, which is the same component R+3 swapped, so the two are mutually inverse.
- **Alternatives.** The alternative components give other bijections with the same domains and codomains: x_{i+4} for φ_A, x_{i+3} for φ_B, and x_j for R+3. The two choices give the same state up to renaming iff the relevant bichromatic subgraph has exactly two components. (Some vertex outside the two components carries each of the other two colours, so the only possible renaming is the transposition.)
- **Injectivity on the class:** every map above is a bijection between the stated subsets, and all images lie in the class, so each map is injective.
- **Staying in the stated block.**
  - **Always [hand]:** φ_A lands in index i+1 and is non-DL; φ_B lands in index i+2 and is non-DL; R+3 lands in index j+3 with lock 1.
  - **Not decided locally [open]:** the *other* slot of the image. Examples: whether φ_A f has lock 2 (else it also fills into F_{i+4}), and whether R+3 s is DL. The image's other matching is not a function of the source's local type, because the swap reroutes chains along all of ∂K.

**Composite into D_{i+1,i+4} = D_{i+4}.**
- R+3 ∘ φ_A is defined iff φ_A f has lock 2. It then lands in index i+4 with lock 1, and it is DL iff lock 2 holds there.
- The mirror composite R+2 ∘ φ_B is defined iff φ_B f has lock 1, and it is DL iff lock 1 holds there.

## 3. The rotation graph Γ [hand]

Join s to R+3 s for every unfilled s with lock 2. Every unfilled state then has Γ-degree equal to its number of locks:
- DL states are interior vertices (degree 2);
- states with exactly one lock (the set N₁) are path endpoints;
- states with no lock (the set N₀) are isolated.

So Γ is a disjoint union of:
- **paths:** each runs from an endpoint e₋ (lock 1 fails, lock 2 holds) along R+3 to an endpoint e₊ (lock 1 holds, lock 2 fails), with d(P) ≥ 0 interior DL states;
- **cycles:** made entirely of DL states, with total D_cyc. Each cycle has length ≡ 0 mod 5, since every step adds 3 to the index. This is Theorem A's orbit.

On paths:
- A path's two endpoints fill into the **same** F_i: e₋ at index j fills into F_{j+4}, and e₊ at index j+3(d+1) fills into F_{j+3(d+1)+3}. These agree when d = 1.
- No renaming can reverse a path, since its two ends have different lock types. So everything descends to the quotient.

## 4. The class identity [hand]

Let:
- N₁ and N₀ be the unfilled states with exactly one and with no lock;
- D = Σ d(P) + D_cyc be the number of DL states;
- L_F = Σ over filled states of #{long bits among M2 and M3}.

By φ_A and φ_B, the fill slots are in bijection:

  N₁ + 2N₀ = #(failed locks) = #(short bits) = 2F − L_F.

With U = N₀ + N₁ + D and N₁ = 2·#paths, this gives

  **3F − U = 2N₀ + (3/2)·L_F + Σ_P (1 − d(P)) − D_cyc.**

(τ gives #long-M3 bits = #long-M2 bits, so (3/2)L_F is an integer.)

Sanity checks:
- **Wheel T − v** (T is the pentagonal bipyramid): every state is filled with both bits long, so U = 0 and 3F = (3/2)·2F. ✓
- **Floor quartet:** N₀ = 0, L_F = 0, D_cyc = 0 and every d(P) = 1 give 3F − U = 0. ✓

**Consequences.**
- **Strongest local inequality [hand]:**
  - N₀ + N₁ ≤ 2F − L_F − N₀ ≤ 2F (Lemma A's 2ΣF, sharpened);
  - #paths ≤ F;
  - U ≤ 3F + D_cyc + Σ_{P : d ≥ 2} (d(P) − 1).
- **Hypothesis (H):** no R+3 edge joins two DL states. (H) gives 3F − U ≥ 0, so the floor holds.
- **Equality under (H)** holds iff N₀ = L_F = 0 and every d(P) = 1. Each path is then U_{i+1}(lock 1 fails) → D_{i+4} → U_{i+2}(lock 2 fails), with both ends filling into F_i.
  - This gives **|F_i| = |U_{i+1}| = |D_{i+4}| = |U_{i+2}|** for each i that occurs. That is exactly the 4-block structure of the 405 classes.
  - Classes with several values of i present are exactly the "mixed" equality classes. Classes with compensating terms (N₀ > 0 or L_F > 0 balanced by some d ≥ 2) are the other possible source of "mixed" floor classes. See check C3.
- **"One neighbour per non-DL block" (365 of 405 classes).** Each f has exactly two swaps into U_{i+1}, via the components of x_{i+2} and of x_{i+4}. They give one state up to renaming iff f's {Y,Z}-subgraph has exactly 2 components. In size-4 classes this is forced by intern C's signature (every component meets the link). [hand, assuming "neighbour" means a distinct state up to renaming]

## 5. Part (b): the 2-swap rule from D_j to F_{j+1}

**The rule.** For d ∈ D_j with link (α, μ, α, A, B):
1. **Swap 1 (R+3):** swap the {α,A}-component of x_{j+2}. It contains a and misses x_j, because lock 2 holds. Call the result d′ = (α, μ, A, α, B), at index j+3. By pd2 Corollary it has lock 1.
2. **Swap 2 (Lemma A, Case 2, at d′):** swap the {A,B}-component of x_{j+2}. This is defined iff x_{j+2} ≁ x_{j+4} in {A,B} in d′, i.e. iff **d′ is not DL**. The result is ρ(d) = (α, μ, B, α, B), whose singleton μ is at position j+1. So **ρ(d) ∈ F_{j+1}** (with M2 short).

**Inverse:** ρ⁻¹ = R+2 ∘ φ⁻¹.
- First swap the {B,A}-component of x_{j+2}, where A is the colour missing from f's link.
- Then swap the {α,A}-component of x_{j+3}.

So ρ is injective on Dom ρ = D_j ∖ DD_j, where DD_j = {d ∈ D_j : R+3 d ∈ D_{j+3}}. [hand]

**Disjointness from Lemma A.** For fixed j:
- Lemma A's φ sends U_j ∖ D_j into F_{j+3} ⊔ F_{j+4};
- ρ sends into F_{j+1}.

So φ ⊔ ρ is injective from U_j ∖ DD_j into F_{j+1} ⊔ F_{j+3} ⊔ F_{j+4}. [hand]

**Exact per-j identity [hand]** (from the bijections φ_A, φ_B and R±):

  F_{j+1} + F_{j+3} + F_{j+4} − U_j = L_j + |U_j^{ff}| + |U_{j+3}^{ff}| + |E_j| − |DD_j|,

where:
- L_j = |F_{j+4}^{M3 long}| + |F_{j+3}^{M2 long}| + |F_{j+1}^{M2 long}|;
- U^{ff} is the set of states in which both locks fail;
- E_j = {s ∈ U_j : lock 1 fails, lock 2 holds, R+3 s is not DL} (the d(P) = 0 path starts).

Summing over j recovers §4. **So the per-j counting lemma holds for a class iff |DD_j| ≤ L_j + |U_j^{ff}| + |U_{j+3}^{ff}| + |E_j|.**

At the floor:
- all terms vanish for every j;
- every D state reaches F_{i} = F_{j+1} in exactly 2 swaps, via ρ;
- ρ is onto F_{j+1}. ✓ This matches the data.

**Mirror rule ρ′ = φ ∘ R+2.**
- Swap the {α,B}-component of x_j; then swap the {A,B}-component of x_j. The result is (A, μ, α, A, α) ∈ F_{j+1}, with M3 short.
- It is defined iff R+2 d is not DL.
- The mirror identity has |DD′_j| = #{d : R+2 d ∈ D_{j+2}}, with M2 and M3 exchanged and F_{j+3} and F_{j+4} exchanged.

**Combining ρ and ρ′ [open].**
- Using ρ, and then ρ′ on DD_j, can collide. This happens when f ∈ F_{j+1} has both bits short and its two Γ-paths pass through two *different* DL states of D_j. That depends on whether the 4-cycle f → φ_A → R+3 → R+3 → φ_B⁻¹ returns to f, which is not local.
- Even a collision-free combination would still miss D_j ∩ DD_j ∩ DD′_j: the DL states that are interior to a DL chain on both sides. These include every Γ-cycle.

**Where (b) fails, exactly.** DD_j consists of DL states whose rotation is again DL: Γ-paths with d ≥ 2, and Γ-cycles.
- For d ∈ DD_j, R+3 d already has lock 1 for free (pd2 Corollary).
- Whether it also has lock 2 is precisely the Jordan question left open in MathConfinementAttack Try 1. The δγ path Q must cross P1 at a vertex that is γ in the new colouring, and nothing forces P1's γ vertices into K.
- No hand argument here bounds |DD_j|.

### 5a. Aimed at Math's addendum target [hand]

The target is an injection of D_j into F_{j+1} ⊔ (the part of F_{j+3} ⊔ F_{j+4} not hit by φ|U_j). Using the bijections of §2, the unhit parts are exactly:

- **Unhit part of F_{j+4}** = F_{j+4}^{M3 long}. Case 1 of φ on U_j is φ_A⁻¹ (using a's component), and it is onto F_{j+4}^{M3 short}.
- **Unhit part of F_{j+3}** = F_{j+3}^{M2 long} ⊔ φ_B(U_j^{ff}). The states of U_j in which both locks fail are sent by Lemma A to F_{j+4} (Case 1), so their F_{j+3} partners are free.

**Target slack.** |target| − |D_j| equals the per-j identity of §5, because |U_j ∖ D_j| = |φ(U_j ∖ D_j)|.

**Where ρ lands.** ρ maps D_j ∖ DD_j injectively into F_{j+1}, which is disjoint from the unhit parts. Inside F_{j+1}, the following are left unused by ρ, and are available for DD_j:
- F_{j+1}^{M2 long};
- φ_B(U_{j+3}^{ff});
- the states f ∈ F_{j+1} with R+2 φ_B⁻¹ f ∈ E_j.

So the full room left for DD_j is

  L_j + |U_j^{ff}| + |U_{j+3}^{ff}| + |E_j|,

and the target injection exists **iff |DD_j| ≤ that room** (cardinality). It is the same identity as in §5.

**No 2-swap rule reaches the room.** Some candidate moves land in the right blocks:
- a long-bit filled state is one F–F swap (τ) from another filled state;
- a U^{ff} state is one swap from a filled state.

But for a state d ∈ DD_j, the pattern-changing moves (R+3 and R+2) give no 2-swap route to a filled state:
- R+3 d is DL, so it has no fill neighbour. If d ∈ DD′_j as well, R+2 d is DL too.
- So any 2-swap route d → s′ → filled must have a **link-pattern-preserving** first swap (§1), one that changes a lock without changing the link pattern. Typical examples are a component that avoids the link, or the {α,μ}- or {A,B}-swap.
- Which such swap works, if any, is not determined by local data. So no *fixed* 2-swap rule of the ρ type covers DD_j [hand]. A rule that chooses the first swap from the outside structure has no injectivity proof [open]: it is exactly where the global step would have to sit.

(Correction to a first draft: I had written that DD_j states are ≥ 3 swaps from every filled state. That is false in general, because of the pattern-preserving swaps above. It is true only along Γ.)

**Summed form.** Σ_j |DD_j| = D_cyc + Σ_P (d(P) − 1)₊. So the condition Σ_j |D_j| ≤ ΣF + s is the §4 identity again. The deficit, if any, sits entirely in long DL rotation chains and DL cycles.

## 6. The global step (task item 4)

- Everything in §§1–5 is local and holds at **every** degree-5 hole of **every** triangulation.
- The identity puts the whole deficit into one term:

  U − 3F = D_cyc + Σ_P (d(P) − 1) − 2N₀ − (3/2)L_F.

- **A targetless class** (Theorem A) has F = 0, N₀ = N₁ = 0 and Γ consisting entirely of cycles, so U − 3F = D_cyc = U. It is consistent with every local fact proved here. So no local argument can give the floor, and this is where the "floor ⇒ R\* ⇒ 4CT" caution bites.
- **The global step must be:** *DL→DL rotation chains, and in particular DL rotation cycles, are paid for by N₀, by long filled bits, or by d = 0 paths.*
  - (H) is a sufficient form of it.
  - (H) at every degree-5 vertex excludes targetless classes, so it already has 4CT strength in the minimal-counterexample frame.
- **The step that fails** is "R+3 of a DL state is not DL" (lock 2 after rotation).
- The data at degree 5 and orders ≤ 24 say the compensation always wins. At degrees 6 and 7 the local model differs (the link has more patterns, and there is no 2-slot structure), and the data show no floor there.

## 7. Check specs for local compute (no code here)

- **C1 (identity).** For every degree-5 class at orders 12–24, compute:
  - F, U, N₀, N₁, L_F;
  - Γ, built with the canonical R+3: σ(s; {α,A}; x_{j+2}) when lock 2 holds;
  - each d(P), and D_cyc.

  Verify that 3F − U = 2N₀ + 1.5·L_F + Σ(1 − d(P)) − D_cyc, and the per-j identity of §5. **Expect 0 mismatches.** Any mismatch means an error in this page or a bug in the code.
- **C2 (dichotomies).**
  - For every filled f: (x_{i+2} ≁ x_{i+4} in {Y,Z}) XOR (x_{i+3} ≁ x_i in {W,X}) is true.
  - The same holds for M2.
  - For every unfilled s: "R+3 defined" ⇔ lock 2, and "R+2 defined" ⇔ lock 1.
- **C3 (where compensation lives).**
  - Report the distribution of d(P) and D_cyc over all 160,979 classes, and the maximum of |DD_j|.
  - For the 419 floor classes, list which terms are nonzero.
  - For the 14 "mixed" classes, say whether they are multi-i classes or compensated ones.
- **C4.** In the 365 classes, check that every filled state's {Y,Z}- and {X,Z}-subgraphs have exactly 2 components.
- **C5 (ψ).** In floor classes, check whether f ↦ φ_B⁻¹ R+3 R+3 φ_A f is the identity on F_i. This decides whether the combined ρ/ρ′ rule can collide.
- **C6 (search objective).** In the scale or fullerene searches, maximise D_cyc + Σ(d(P) − 1)₊ (long DL rotation chains). Any class below 1/4 must have a large value here.

- **C7 (2-swap reach).** For every DL state d, record:
  - whether R+3 d and R+2 d are non-DL;
  - the swap distance from d to its nearest filled state;
  - for the states d ∈ DD_j ∩ DD′_j that are at distance 2, which pattern-preserving first swap is used.

  Report max |DD_j| and max |DD_j ∩ DD′_j| over all classes, and in particular the largest DD_j relative to its room.

## 8. Ledger and KILLED lines

- [hand]: all of §1–§5 except the items marked [open].
- [open]: bounding |DD_j| (the global step); injectivity of the combined ρ/ρ′ rule; ψ.
- **KILLED: the "one word with four (M₂, M₃) combinations, one filled" picture of the 4-blocks** (MathQuarterFloor §2A).
  - In floor classes, every filled state has the *same* combination (both short).
  - The four blocks are four different link patterns (F_i, U_{i+1}, D_{i+4}, U_{i+2}), joined by the bijections φ_A, R+3, R+3 and φ_B⁻¹.
  - The 4 comes from the accounting 1 + 2·½·2 + 1: one filled state, two fill slots, and each path having two ends and one interior DL state.
- **KILLED: "the states of a block agree outside the 1-ball of P"** (MathQuarterFloor §3/§5.1 as worded). φ_A changes a whole Kempe chain K, whose boundary is a full (c1,c3)-path through P plus any inner cycles. Block-mates differ along whole chains, not just at P.
- **KILLED: proving the floor or part (b) by local counting alone.** Targetless classes satisfy every local identity proved here, with U − 3F = U.
- **Not edited:** no other file. No status word changes.

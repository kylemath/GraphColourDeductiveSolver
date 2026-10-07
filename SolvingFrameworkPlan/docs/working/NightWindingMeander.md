# Night: the π-winding in the Tait/meander picture

Night worker, 7 October 2026 (started 6 October). **Exploratory. Hand work plus small single-core checks. Unreviewed.**

This note merges `NightEulerHole.md` (cited as **EH**: Theorem W, the π-permutation, Lemma E) with `NightThetaAttempt.md` (cited as **TA**). Definitions follow `MathQuarterFloorBijections.md` (cited as **QFB**).

Labels:
- [proved]: a complete argument is given, modulo QFB §1–§2.
- [sketch]: the argument is outlined and the gap is named.
- [conjecture]: not proved.
- [data]: computed with the scratchpad scripts described in §7. The scripts are not committed.

**Nothing here proves the floor, R\*, or any escape statement.** Each of those implies the Four Colour Theorem, or a Kempe-class strengthening of it.

## Verdict

1. **Task 1 (exact) is done** [proved, data 0 failures].
   - A π-step moves one token. Both alternative components give the same jump.
   - λ is the token's displacement along the arc of ∂P that avoids the other token, so w is the rotation number of the unordered token pair, counted in half-turns.
   - The sign of λ is a **Jordan crossing parity** of two dual meanders:
     - B_T, the {t, s_T}-path of the moving token;
     - C, the {s_T, s_T′}-path joining the two singleton edges.
   - Locally the sign is a **Heawood product** along B_T (Proposition H).
   - Consistent with the coordinator's §7 update: λ = +1 on every lock-2 (R₊₃) step, and the parity only re-encodes lock 2.
2. **Task 2 (global) is not closed.**
   - Exact Euler content [proved]:
     - (i) ∂K has exactly cyc(K) + 1 dual curves, one of which is B₁;
     - (ii) Σ_pairs k(s) − 8 counts the closed bicoloured dual cycles that avoid P;
     - (iii) a **saturated** state (slack 0) has exactly the two Kempe neighbours π(s) and π⁻¹(s), up to renaming.
   - Hence: **a π-cycle that is not a whole Kempe class contains a non-saturated state.**
   - Euler cannot force non-saturation state by state: saturated DL and even saturated DD states exist on the sphere [data].
   - **The coordinator's escape route through {α,A}/{α,B} is false at gentri 17 #3** [data]. That Γ-cycle has no spare {α,c}-component, and every K is a tree (the pure meander case). It escapes only through **t-chains** ({α,μ} or {A,B} components that avoid the link), i.e. closed components of the C-system.
3. **Torus.** The sphere already enters at Lemma Π and at the mod-5 congruence. A frozen torus state has 3F − U = −1 ≢ 0 (mod 5), and no π is defined on it.
4. **Fallback.** w(Z) = (|Z| − 4F_Z)/5, together with the saturation lemma and its corollary. Revised escape conjecture E_t: tested on all positive cycles at orders 16–21 (6 cycles), with 0 failures.

---

## 1. One π-step in the Tait picture

Setup (EH §1):
- G = T − v; its dual G* is cubic except at the pentagon node P.
- Tait colours are col(x) ⊕ col(y) in V₄.
- The colours at P have multiplicities (3,1,1): the triple colour is t, and the singles s₁ and s₂ sit on the two **token** edges.
- For each single s, the dual {t,s}-subgraph has degree 4 at P. Its P-component is two loops that pair those four edges **non-crossingly** (Jordan).
- The dual {s₁,s₂}-subgraph has degree 2 at P. Its P-component is a single path **C** from one token edge to the other. Its other components are closed cycles, C₀(t) of them, which are the boundaries of the link-free {α,μ}/{A,B} chains.

**Lemma 1.1 (token jump) [proved].**
- Let a Kempe swap change the link pattern. Swapping a {p,q}-component exchanges the two Tait colours ≠ p+q along every dual curve of its boundary.
- The link-changing swaps are exactly the swaps of one of the two {t,s}-loops at P, for a single s. Call T the token of colour s and T′ the other token.
  - If the swapped loop pairs e_T with a t-edge e_q: T moves to q.
  - If the swapped loop pairs two t-edges: the new triple colour is s, and the new singles are the remaining t-edge, which is e_q (the partner of e_T in the other loop), and T′.
- **So either loop moves T to its partner q, and T′ stays put.** The alternative components of QFB §2 therefore give the same token motion.
- Rows of the table:
  - R₊₃ swaps the t–t loop {e_{j+1}, e_{j+3}}, and T moves along the other loop from j+4 to j.
  - φ_B⁻¹ swaps the token's own loop {e_{j+3}, e_{j+4}}.
  - φ_A swaps {e_{i+1}, e_{i+2}}, and T moves from i+4 to i+3.
  - τ swaps {e_{i+2}, e_{i+3}}, and T moves from i+4 to i+1.

**Lemma 1.2 (λ is the arc avoiding the other token) [proved; data: asserted on every state, orders 16–21].**
- λ(s) equals the signed displacement of T along the arc of ∂P from p_T to q that does **not** contain p_{T′}.
- This explains τ's convention: −3 rather than +2, because +2 would pass through T′.
- Tokens never collide or pass each other. So a π-cycle is a loop in UConf₂(S¹), the open Möbius band, with π₁ = Z, and **w(Z) = (1/5)Σλ is its degree in half-turns of the unordered pair** [proved].
- w is invariant under reflection: the mirror image swaps π with π⁻¹ and negates positions.

**Proposition H (crossing parity and Heawood product) [proved; global sign fixed by convention and checked].**

Definitions:
- B_T is the {t, s_T}-path from e_{p_T} to e_q. Its internal dual vertices are u₀, then pairs (v₁u₁), …, (v_k u_k) joined by s_T-edges.
- ε(x) = ±1 is the cyclic order of the three Tait colours around triangle x, measured against (1,2,3).
- χ = ±1 is the order sign of (t, s_T, s_T′).

Claim:
- For unfilled states, **λ = χ · (−1)^k · Π_{x ∈ int B_T} ε(x)**.
- For filled states the right-hand side is always −1.

*Proof.*
- Close C through P to a Jordan curve Ĉ. The three t-edges at P fall into the arc A₊ (from p_T to p_T′ in the + direction) and the arc A₋.
- B_T shares e_{p_T} with C. At u₀, B_T leaves on the side of Ĉ given by χ·ε(u₀), with a fixed global convention.
- B_T meets the {s_T, s_T′}-curves only along the s_T-edges v_i u_i. At such an edge the two curves cross iff ε(v_i) = ε(u_i) (check the two local pictures).
- Every closed {s_T,s_T′}-cycle C′ avoids P, and B_T starts and ends at P. So B_T crosses each C′ an even number of times (Jordan).
- Hence Π_i(−ε(v_i)ε(u_i)) = (−1)^{cr(B_T, C)}, and the side of e_q is χ ε(u₀)(−1)^{cr}.
- Unfilled states (tokens j+2 and j+4): A₊ = {j, j+1} and A₋ = {j+3}. So the side is +1 iff q = j iff λ = +1.
- Filled states (tokens i and i+4): A₊ = ∅, so the side is always −1. Within A₋, φ_A and τ are told apart by the *other* {t,s_T}-loop, not by C. ∎

[data] Orders 16–21, every degree-5 hole of gentri (4,246 holes): the right-hand side matched λ's sign on every state, with value −1 on every filled state.

**Reading.**
- Lock 2 (unfilled) **is** the statement "B_T crosses C an odd number of times", with the start convention fixed.
- On DL states λ = +1 is constant (coordinator §7). There is no further region-dependent sign to find: Σλ over a cycle is the signed count of steps by type.

**Hand check, gentri 17 #3, hole 0** (line 4 of tri17.txt; T-labels; link 1,2,3,4,5).
- The Γ-cycle has length 20, w = +4, and every step is an R₊₃.
- State 28 (canonical index):
  - type U₃, colouring {1:0, 2:3, 3:2, 4:0, 5:1, 6:2, 7:1, 8:0, 9:1, 10:3, 11:0, 12:3, 13:2, 14:3, 15:2, 16:1};
  - link Tait word (3,1,2,1,1), tokens {0,2}, moving token 2 → 3.
- B_T from e₂ (x₂x₃ = 3–4) runs through 13 triangles:
  - 349, 4910, 91015, 101115, 111516, 111216, 121316, 71213, 6712, 61112, 61011, 5610, 4510;
  - their ε are + + + + + + + − + + − − −;
  - it ends at e₃.
- So k = 6 and Πε = (−1)⁴ = +1. With χ(1,2,3) = +1 this gives λ = +1. ✓

## 2. Euler content available for a π-cycle

**Lemma 2.1 (boundary curves of K) [proved; uses χ = 2].**
- Let K be a {p,q}-component of a state. Then ∂K consists of exactly **cyc(K) + 1** dual curves.
- If K meets the link, exactly one of them passes through P. For the R₊₃ component, that one is B₁ = the loop {e_{j+1}, e_{j+3}}.

*Proof.*
- K is connected and plane. By Euler it has e − v + 2 = cyc(K) + 1 faces, each an open disc.
- A {p,q}-subgraph contains no G-triangle. So every face of K contains P or a vertex outside K.
- The boundary walk of a disc face is one closed walk, so the dual edges crossing it form one closed curve.
- The face containing P carries B₁. P lies in only one face, and K meets ∂P in two corners, so B₁ crosses ∂P exactly twice. ∎

**So the pure case of TA §7 (∂K = B₁) is exactly "K is a tree".**
- On a surface of genus g, the count is cyc(K) + 1 minus a correction for non-contractible cycles of K [sketch]. For example, a non-separating cycle K on the torus has 1 face but 2 boundary curves.

**Lemma 2.2 (saturation) [proved, from EH Lemma E].**
- Σ_{6 pairs} k_pq(s) = 8 + Σ_c C₀,c(s), where C₀,c counts the closed dual {c′,c″}-cycles avoiding P.
- Call s **saturated** if the slack Σk − 8 is 0.
- For a DL state, saturation ⇔ the component counts are exactly {α,μ}: 1, {A,B}: 1, {μ,A}: 1, {μ,B}: 1, {α,A}: 2, {α,B}: 2 ⇔ every Kempe component meets the link.
- The same holds for every state type, by the same Lemma E bookkeeping: triple colour, two connected pairs; each single colour, one pair with 2 components and one connected pair.

**Corollary 2.3 [proved].**
- A saturated state has, up to renaming, exactly two Kempe neighbours: π(s) and π⁻¹(s).
  - A connected pair's swap is a renaming.
  - A 2-component pair's two swaps agree up to renaming, and these are the two slots.
- **Hence a π-cycle consisting only of saturated states is a whole Kempe class**, and that class is targetless iff the cycle is a Γ-cycle.
- Contrapositive: **if Z is not a whole class, some state of Z carries a Kempe chain avoiding the link**, i.e. a closed bicoloured dual cycle off P.

**What Euler does *not* give [data].**
- Saturated DL states exist on the sphere: 0, 136, 90 and 161 of them at orders 16, 17, 18 and 19.
- Saturated **DD** states (R₊₃ s again DL) also exist: 0, 81, 20 and 59.
- So neither "DL ⇒ unsaturated" nor "DD ⇒ unsaturated" holds. Any escape statement is genuinely about a whole cycle, not about one state.
- The Euler slack changes across an R₊₃ step by −3 to +3, symmetrically. It has no relation to cyc(K) (orders 16–18, 4,328 steps).
- So I found **no Euler relation among the successive ∂K systems** that bounds a DL run.

**Answer to the coordinator's question** ("what does Euler say about the meander arrangement of a closed all-DL chain?"):
- Only that, at every state, the closed dual cycles off P number Σk − 8 ≥ 0, and that each swapped K has cyc(K) closed boundary curves besides B₁.
- Both quantities may be 0 along an entire Γ-cycle without contradicting Euler or Jordan.
- If they were 0 everywhere, the Γ-cycle would *be* a targetless class (Corollary 2.3). This is the Kempe-fallacy configuration, and ruling it out is R\*-strength.
- So the escape step is exactly where the counting input of 4CT strength (TA §5) must enter. [proved as a reduction; no proof of the escape]

## 3. Escape data (positive cycles, orders 16–21; every degree-5 hole of gentri)

| order, graph, hole | L | F | w | slack values on Z | exit via {α,A}/{α,B} | exit via t-chain ({α,μ}/{A,B}) | class cycles (L, w) |
|---|---|---|---|---|---|---|---|
| 17 #3 h0 and h16 | 20 | 0 | +4 | {1, 2} | **none** | 20 swaps, all into the w = −16 cycle | (20, +4), (80, −16) |
| 20 #58 h18 | 21 | 4 | +1 | {0, 1, 2, 3} | 2 | 21 | (4,0), (8,0), (18,−2), (21,+1), (48,−12), (54,−10) |
| 20 #60 h19 | 21 | 4 | +1 | {0, 1, 2, 3, 4} | 2 | 27 | (4,0)×2, (8,0)×3, (21,+1), (54,−10), (86,−14) |
| 21 #96 h2 | 14 | 1 | +2 | {0, 1, 2, 3} | 2 | 14 | (4,0)×6, (6,−2), (10,−2), (14,+2), (153,−39) |
| 21 #134 h0 | 14 | 1 | +2 | {0, 1, 2, 3} | 2 | 25 | (4,0)×4, (6,−2), (8,0), (14,+2), (64,−12), (88,−16) |

At 17 #3, every state of the Γ-cycle has:
- {α,A}, {α,B} and {α,μ} with exactly 2 components each;
- {μ,A} and {μ,B} connected;
- K a tree (pure meander, Lemma 2.1);
- {A,B} with 1 or 2 components, alternating.

So the only exits are swaps of the closed C-system component (C₀(t) ≥ 1), and they all land in the negative cycle.

**Conjecture E_t (revised escape) [conjecture].** Every Γ-cycle, and more generally every π-cycle with w > 0, contains a state with C₀(t) ≥ 1. That is, the {s₁,s₂}-system has a closed component off P, and swapping its chain lands in a π-cycle of negative winding.
- [data] Holds for all 6 positive cycles at orders 16–21.
- The first clause alone, for Γ-cycles, implies "no targetless class is a single saturated Γ-cycle".
- Circularity check: E_t says nothing about classes with several Γ-cycles. So even E_t does **not** give R\*, let alone the floor.

## 4. Why nothing here survives on the torus

- **Lemma Π needs Jordan.** On the torus the two {t,s}-loops at P may cross. Then L2 fails: R₊₃ can be undefined on a lock-2 state (TA §5), and π is not a permutation.
- **The congruence is already a sphere fact.** A frozen single-state class (local-runs/18-torus-floor, n ≥ 16) has F = 0, U = 1, so 3F − U = −1 ≢ 0 (mod 5). Theorem W's mod-5 corollary therefore fails on the torus, and **its failure is detected by the token structure, not by any count.** A frozen state has no π-step, so its "winding" is undefined rather than positive.
- **Proposition H** uses two sphere facts: Ĉ separates A₊ from A₋, and closed cycles are crossed an even number of times. Both fail for non-separating curves.
- **Lemmas 2.1 and 2.2** use χ = 2. On the torus Σk ≥ 8 − 2g′ allows Σk = 6 (frozen), and the boundary-curve count changes.
- So the sphere enters three times: twice qualitatively (non-crossing pairing at P, Jordan parity in H) and once quantitatively (Euler in 2.1 and 2.2).
- The **sign** statement Σ_Z w ≤ 0 per class would need a fourth, global entry, which nothing here supplies.

## 5. Fallback: exact single-cycle lemmas

1. **w(Z) = (|Z| − 4F_Z)/5** [proved].
   - Counting step types: L = r + 2e + t and 5w = r − 2e − 3t. Here r, e and t count the R₊₃, φ_A (equivalently φ_B⁻¹) and τ steps of Z.
   - Consequences: |Z| + F_Z ≡ 0 (mod 5); −3|Z|/5 ≤ w ≤ |Z|/5; w = |Z|/5 iff Z is a Γ-cycle.
2. **Token-loop degree:** w = the half-turn degree of the token pair (Lemma 1.2) [proved].
3. **Saturation corollary:** Z ≠ class ⇒ Z has an unsaturated state (2.3) [proved].
4. **Γ-length ≡ 0 (mod 10)** (EH conjecture): only 2 Γ-cycles occur at orders 16–21, both of length 20 [data, not evidence].

## 6. Circularity and controls

- **Floor class 17 #1, holes 0 and 2:** cycles (4,0)×3, (8,0), (16,0), (28,0). Proposition H holds there. Saturated states occur in the w = 0 four-cycles, consistent with 2.3, since those cycles are not whole classes and contain unsaturated states as well.
- **Positive class 17 #3, hole 0:** see §1 and §3.
- Every positive claim above is either local (Jordan or Euler at one state) or a reduction. None asserts a class-level inequality, so none implies 4CT, and none was claimed to.

## 7. Reproduction

Stdlib scripts in the session scratchpad (not committed, no team code imported).

- `wm.py`:
  - enumerates the 4-colourings of T − v up to renaming and builds Kempe classes;
  - builds π from the EH table and asserts that it is a permutation;
  - checks the token-sum rule, Lemma 1.2's arc rule and Proposition H's Heawood product on every state.
- `t3.py`: positive cycles and their link-preserving exits, tagged by colour role.
- `t4.py` and `t5.py`: slack distributions; saturated DL and DD states.
- `t6.py`: slack change against cyc(K).

Run times, single core:
- orders 16–19: 5 s;
- order 20: 18 s;
- order 21: 64 s.

The graph files are `backgroundMaterial/planemap-structural/studiointel/gentri/triN.txt`; the hole is a vertex index, as in `qf_replay.py`.

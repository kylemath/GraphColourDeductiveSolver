# Adversarial read of the chain R\* ⇒ VH_C ⇒ VH∃ ⇒ 4-colourability: all six links correct by hand (L5's repair re-derived). R\* is not weaker than VH∃; it is a sufficient condition at least as strong

- **From:** Independent audit, main session
- **To:** coordination session; Math; Proof Navigator; Long Table
- **Sent:** 2026-10-06 13:25 MDT
- **Replies to:** `2026-10-06_1240_math_…_chain-to-VHE-reviewed-one-lemma-left.md`; `docs/working/MathReviewCleanToVHE.md`; the coordinator's 12:5x request
- **Asks for:**
  - Navigator: record the chain as [hand, reviewed by the Math worker and re-derived independently by the audit].
  - Coordinator: if this goes to the user, use the framing in §3.

This is hand work only; nothing was computed. The audit re-derived each link from the definitions in `MathReviewCleanToVHE.md` §0, which it checked against `vh-exists.md` and the VH_C sources cited there.

## 1. Per link

| Link | Audit verdict | What the audit checked |
|---|---|---|
| **L1** Theorem A | **CORRECT** (not needed by the chain) | Step 1: the βγ-component of x₁ contains no other link vertex once the x₁~x₃ path is missing, so x₁ → γ fills. Step 2: C₂ = v x₁ P₂ x₄ v is simple; at v, the edges to x₁ and x₄ split x₀ from {x₂, x₃}; an αγ path avoids every vertex of C₂ (coloured β, δ, or v, which is deleted), so it cannot cross. So the αγ-component of x₂ contains x₃ and misses x₀, x₁, x₄. Swaps are unrestricted under VH_C, so there is no frozen-φ problem. The audit had checked the same steps in its 08:37 review. |
| **L2** Corollary B | **CORRECT** (only the trivial direction is used) | Fan τᵢ is proper on its chords xᵢx_{i+2} and xᵢx_{i+3} ⇔ xᵢ is not in the repeat pair. Targetlessness is fan-independent. "All five fans legal" is not needed if "every legal fan" is meant. |
| **L3** finite radius ⇒ clean | **CORRECT** | An unfilled state at a degree-5 hole has exactly one repeated colour, at non-adjacent positions. If it is not doubly locked, one swap fills: the βγ-component of x₁ misses x₀, x₂ (α), x₄ (δ) and x₃. So "every DL state's Kempe class contains a fill" ⇒ every state at v reaches F by pure swaps. Pure swaps are permitted moves, and v ∉ φ keeps the states permitted. Only finiteness is used. |
| **L4** clean ⇒ φ-good fan | **CORRECT** | A legal fan exists (vh-exists Lemma 1.2(c)). Every admitted start is a state at v, so it reaches F. |
| **L5** least failure ⇒ contradiction | **CORRECT** (the separating-triangle step and the Euler repair re-derived; see §2) | The step across a separating cycle transports a φ-good **pair**, not "cleanness". It uses only separating **triangles**, and the clique lift. See §2. |
| **L6** VH_C ⇒ VH∃ | **CORRECT** | Any face is a valid φ, because all degrees are ≥ 5. The permitted graph is a subgraph of M(T) with the same fill set F and the same starts S(v,τ). |

The chain does **not** need Theorem A, four-connectivity of a plain failure, frozen-φ swaps, or a uniform radius bound. It **does** need these accepted inputs, which the audit did not re-derive and treats as accepted by Math:
- TriangleCarry (the separating-triangle reduction);
- `VacancyCliqueLift` (compiled);
- FourConnected Prop 1 (≤ 2 degree-4 vertices on φ);
- VHCoreAdvance (order ≥ 12);
- vh-exists Theorem A (VH∃ ⇒ 4-colourability).

## 2. L5 in detail: the two points the coordinator flagged

**Across the separating triangle F.**
- Let A be the closed side not containing the face φ. A separating triangle is not a face, so φ ≠ F. φ lies in the other closed side, so no vertex of φ is in A − F.
- The vertices of A − F keep their full T-neighbourhoods, so they have degree ≥ 5. So (A, F) ∈ 𝒞, and it is smaller.
- Lifting a good pair (v, τ) of (A, F) to T:
  - **Starts:** T's start restricts to an A-start, with the same chords. A T-edge between two A-vertices outside F is an A-edge, so legality and admission agree.
  - **Swaps:** for colours {p, q}, at most two F-vertices carry p or q, and they are adjacent. So each global {p,q}-component meets A in one A-component, and the global swap realises the A-swap. That is `VacancyCliqueLift`.
  - **Slides and fills:** at a hole h ∈ A − F, N_T(h) = N_A(h).
  - **Holes:** they stay in A − F, which is off φ, as VH_C requires.
- So the pair is φ-good in T. What crosses the separating cycle is the pair, not "cleanness" or the protected face. No gap.

**The Euler repair (≥ 9 − n₄ ≥ 7 off φ).** Re-derived:
1. In the relative class, Σ(6 − d) = 12 with n₄ ≤ 2 degree-4 vertices, all on φ. So Σ_{d≥7}(d − 6) = n₅ − 12 + 2n₄.
2. Let H be the vertices of degree ≥ 12, and B the degree-5 vertices with ≥ 2 neighbours in H.
3. Then Σ_H (d − 6) ≥ max(6|H|, 2|B| − 6|H|) ≥ |B|. So |B| ≤ n₅ − 12 + 2n₄, and at least 12 − 2n₄ degree-5 vertices are not in B.
4. At most 3 − n₄ of them lie on φ, so **at least 9 − n₄ ≥ 7 lie off φ.** ✓

This repair is needed only for the P-A\* attack on R\*, not for the chain itself.

## 3. Is R\* weaker than VH∃? No

- **R\* ⇒ VH_C ⇒ VH∃** (L3–L6). R\* is a **sufficient condition**, at least as strong as VH∃. The coordinator asked whether it is "genuinely weaker or equivalent". It is neither weaker nor known to be equivalent.
- **It is stronger per vertex.** By Corollary B (with Theorem A), VH_C at (T, φ) ⇔ some degree-5 v ∉ φ is clean in the **mixed** (slides and swaps) sense. R\* asks for **pure-swap** cleanness: VH_C with slides removed. Pure-clean ⇒ mixed-clean. The converse is open, since slides might rescue a targetless Kempe class. The data so far (`vh-exists-check`: deg5_KD_bad = 0 at small orders; WP19: no start without a pure fill) never needed slides. That is [computed, finite], not evidence for a theorem.
- **It is stated on a larger class.** It covers four-connected triangulations with up to two degree-4 vertices on φ, not only minimum degree 5.
- **Consequence for how to present it.**
  - R\* for all four-connected members of the relative class implies the Four Colour Theorem. It is therefore a **clean reformulation of the whole open problem** in swap-only, one-vertex form, not "one lemma left" in the sense of a small remaining gap.
  - What it does buy:
    - only one vertex per graph;
    - no fan;
    - no slides;
    - no radius bound;
    - a four-connected setting.

    That is a cleaner target than VH∃ as originally stated, and every known kill (L, R ≤ 3, (6^5) radius 2, link-class determination) leaves it untouched.

**Suggested sentence for the user:** "Math's chain (checked independently by the audit) shows that the Four Colour Theorem follows from Lemma R\*: in every four-connected triangulation of the relative class, some degree-5 vertex off the protected face has every doubly locked colouring Kempe-connected to a filled one. R\* is open and at least as hard as VH∃; it is the cleanest form of the open problem so far, not a nearly finished proof."

— Independent audit

/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.ChainMod4
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TutteSides

/-!
# Conjecture F (the mod-4 chain-count formula) is a theorem

`TrackK/FProof.md` (hand proof, reviewed CORRECT), formalised without topology and without the
filled map `T°`. For a triangulated spherical map without isolated vertices, a degree-5 hole
`h` with link `x 0, …, x 4`, and a proper colouring of `T − h` that is unfilled in the frame `j`
(link colours `(α, μ, α, A, B)`):

`2 N ≡ cw + (n − 1) − hand + 2 (L1 + L2)  (mod 4)`  (`chainFormulaF`, hence `conjectureF`).

## Proof

1. **cw mod 8** (`cw_dart_mod8`; Lemma 0 and 0′ in one table). `omT μ` is an antisymmetric
   weight on ordered colour pairs whose coboundary is `σ − 4 + 4·#μ` on every proper triangle
   (`omT_face`, by `decide`). It exists because `σ − 4·1_t` has total `0` on `∂Δ³` mod 8.
   Summing over darts whose face avoids `h` telescopes to the ten darts of the star of `h`, and
   `omT_link` evaluates the link part as `5 − 2·hand`.
2. **Three Tutte identities** (`TutteSides.tutte_sides`), one for each partition containing
   `μ`. The vertex `h` is placed on a side so that its side edges play the role of the two lock
   diagonals of the filled map:
   - `{h} ∪ {μ, A}` against `{α, B}`;
   - `{h} ∪ {μ, B}` against `{α, A}`;
   - `{α, μ}` against `{h} ∪ {A, B}`.

   Every face, including the five at `h`, then has a corner on the second side (`face_cover`).
3. **The locks** enter through the merge lemma (`finrank_chainSpace_insert`). Adding `h` to the
   `{μ, A}` side lowers the chain count by `1 − L1`; the same holds for `{μ, B}` and `L2`.
4. Euler (`TutteSides.euler_tri`), the side-edge and side-vertex counts, and linear arithmetic
   mod 8 (`f_arith`) finish the proof. `γ` cancels.

## Consequences (with `ChainMod4`'s formal Lemma W)

* `chainParityLaw_sphere`: **Theorem 6**, the chain-parity law.
* `rigid_isolation`: the `π`-image of a rigid state is never rigid.
* `remark7`: a link-free Kempe swap preserves `N + L1 + L2` mod 2.

All of these hold on every triangulated spherical map (`SphericalMap`, i.e. `Fills`) without
isolated vertices.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill Finset TutteSides

/-! ### Colour tables -/

/-- An antisymmetric weight on ordered colour pairs, depending on a marked colour `μ`, whose
coboundary is `σ − 4 + 4·#μ` on every proper triangle (found by search; checked below). -/
def omT : Fin 4 → Fin 4 → Fin 4 → ZMod 8 :=
  ![![![0, 0, 0, 0], ![0, 0, 7, 1], ![0, 1, 0, 7], ![0, 7, 1, 0]],
    ![![0, 0, 0, 0], ![0, 0, 7, 1], ![0, 1, 0, 3], ![0, 7, 5, 0]],
    ![![0, 0, 0, 0], ![0, 0, 7, 5], ![0, 1, 0, 7], ![0, 3, 1, 0]],
    ![![0, 0, 0, 0], ![0, 0, 3, 1], ![0, 5, 0, 7], ![0, 7, 1, 0]]]

/-- Indicator of a colour equality, in `ZMod 8`. -/
def eq8 (a b : Fin 4) : ZMod 8 := if a = b then 1 else 0

lemma omT_antisymm : ∀ m a b : Fin 4, omT m b a = - omT m a b := by decide

/-- **The face table** (Lemma 0 and 0′ in one): on a proper triangle `(a, b, e)`, the weight
sums to `2·[clockwise] − 5 + 4·#μ`. -/
lemma omT_face : ∀ m a b e : Fin 4, a ≠ b → b ≠ e → e ≠ a →
    omT m a b + omT m b e + omT m e a =
      2 * ind8 (isCW (fxor a b) (fxor b e) (fxor e a)) - 5 + 4 * (eq8 a m + eq8 b m + eq8 e m) := by
  decide

/-- **The link table**: around the pentagon `(α, μ, α, A, B)`, read in the face orientation `s`,
the weight sums to `5 − 2·hand`. -/
lemma omT_link : ∀ (a m A B : Fin 4) (s : Fin 5), (s = 1 ∨ s = 4) → m ≠ a → A ≠ a → B ≠ a →
    m ≠ A → m ≠ B → A ≠ B →
    ∑ k : Fin 5, omT m (![a, m, a, A, B] k) (![a, m, a, A, B] (k + s)) =
      5 - 2 * ind8 (if s = 1 then isCW (fxor a m) (fxor a A) (fxor a B)
        else !isCW (fxor a m) (fxor a A) (fxor a B)) := by
  decide

/-- Three distinct colours are not all in a pair. -/
lemma tri_out : ∀ p q x y z : Fin 4, x ≠ y → y ≠ z → z ≠ x →
    (x ≠ p ∧ x ≠ q) ∨ (y ≠ p ∧ y ≠ q) ∨ (z ≠ p ∧ z ≠ q) := by decide

/-- The complement of a colour pair, among four distinct colours. -/
lemma col_compl : ∀ a b d e x : Fin 4, a ≠ b → a ≠ d → a ≠ e → b ≠ d → b ≠ e → d ≠ e →
    (¬ (x = a ∨ x = b) ↔ (x = d ∨ x = e)) := by decide

/-- Consecutive link colours of `(α, μ, α, A, B)` are never both in `{μ, A}` nor both in
`{μ, B}`. -/
lemma link_pair : ∀ (a m A B : Fin 4) (k s : Fin 5), (s = 1 ∨ s = 4) → m ≠ a → A ≠ a → B ≠ a →
    m ≠ A → m ≠ B → A ≠ B →
    ((![a, m, a, A, B] k ≠ m ∧ ![a, m, a, A, B] k ≠ A) ∨
      (![a, m, a, A, B] (k + s) ≠ m ∧ ![a, m, a, A, B] (k + s) ≠ A)) ∧
    ((![a, m, a, A, B] k ≠ m ∧ ![a, m, a, A, B] k ≠ B) ∨
      (![a, m, a, A, B] (k + s) ≠ m ∧ ![a, m, a, A, B] (k + s) ≠ B)) := by decide

/-- Where the pairs `{μ, A}`, `{μ, B}`, `{A, B}` and `μ` sit on the link. -/
lemma link_pos : ∀ (a m A B : Fin 4) (k : Fin 5), m ≠ a → A ≠ a → B ≠ a →
    m ≠ A → m ≠ B → A ≠ B →
    ((![a, m, a, A, B] k = m ∨ ![a, m, a, A, B] k = A) ↔ (k = 1 ∨ k = 3)) ∧
    ((![a, m, a, A, B] k = m ∨ ![a, m, a, A, B] k = B) ↔ (k = 1 ∨ k = 4)) ∧
    ((![a, m, a, A, B] k = A ∨ ![a, m, a, A, B] k = B) ↔ (k = 3 ∨ k = 4)) ∧
    (![a, m, a, A, B] k = m ↔ k = 1) := by decide

/-- The side-edge count at one dart (both ends off `h`): the three sides `{μ,A}`, `{μ,B}`,
`{α,μ}` count the dart once for each `μ`-end. -/
lemma dart_sides : ∀ a m A B x y : Fin 4, m ≠ a → A ≠ a → B ≠ a → m ≠ A → m ≠ B → A ≠ B →
    x ≠ y →
    (if (x = m ∨ x = A) ∧ (y = m ∨ y = A) then 1 else 0) +
      (if (x = m ∨ x = B) ∧ (y = m ∨ y = B) then 1 else 0) +
      (if (x = a ∨ x = m) ∧ (y = a ∨ y = m) then 1 else 0) =
      (if x = m then 1 else 0) + (if y = m then (1 : ℕ) else 0) := by decide

/-- `μ` sits once on the link, and `{μ, A}`, `{μ, B}` twice each. -/
lemma link_counts : ∀ (a m A B : Fin 4), m ≠ a → A ≠ a → B ≠ a → m ≠ A → m ≠ B → A ≠ B →
    ∑ k : Fin 5, eq8 (![a, m, a, A, B] k) m = 1 ∧
    ∑ k : Fin 5, (if ![a, m, a, A, B] k = m ∨ ![a, m, a, A, B] k = A then (1 : ℤ) else 0) = 2 ∧
    ∑ k : Fin 5, (if ![a, m, a, A, B] k = m ∨ ![a, m, a, A, B] k = B then (1 : ℤ) else 0) = 2 := by
  decide

/-- Four distinct colours exhaust `Fin 4`. -/
lemma col_cover : ∀ a m A B x : Fin 4, m ≠ a → A ≠ a → B ≠ a → m ≠ A → m ≠ B → A ≠ B →
    x = a ∨ x = m ∨ x = A ∨ x = B := by decide

/-- The side-vertex count at one vertex off `h`. -/
lemma vertex_sides : ∀ a m A B x : Fin 4, m ≠ a → A ≠ a → B ≠ a → m ≠ A → m ≠ B → A ≠ B →
    (if x = m ∨ x = A then 1 else 0) + (if x = m ∨ x = B then 1 else 0) +
      (if x = a ∨ x = m then 1 else 0) = 1 + 2 * (if x = m then (1 : ℕ) else 0) := by decide

/-! ### The clockwise count mod 8 as a dart sum (any triangulated rotation system) -/

section general
variable {V : Type*} [Fintype V] [DecidableEq V] {G : SimpleGraph V} [DecidableRel G.Adj]

section core
variable (φ : Equiv.Perm G.Dart) (hφ : ∀ d, (φ d).fst = d.snd)
  (h3 : ∀ d, φ (φ (φ d)) = d)
variable {h : V}

/-- Darts avoiding `h`: subtract the five darts out of `h` and the five into `h`. -/
lemma sum_off_h {R : Type*} [AddCommGroup R] (P : Pent G h) (X : G.Dart → R) :
    ∑ d : G.Dart, (if d.fst ≠ h ∧ d.snd ≠ h then X d else 0) =
      ∑ d, X d - ∑ i : Fin 5, X ⟨(h, P.x i), P.adj_h i⟩ -
        ∑ i : Fin 5, X (Dart.symm ⟨(h, P.x i), P.adj_h i⟩) := by
  classical
  have pt : ∀ d : G.Dart, X d = (if d.fst ≠ h ∧ d.snd ≠ h then X d else 0) +
      (if d.fst = h then X d else 0) + (if d.snd = h then X d else 0) := by
    intro d
    have hne := d.adj.ne
    by_cases a : d.fst = h <;> by_cases b : d.snd = h
    · exact absurd (a.trans b.symm) hne
    · simp [a, b]
    · simp [a, b]
    · simp [a, b]
  have e2 : ∑ d : G.Dart, (if d.snd = h then X d else 0) =
      ∑ i : Fin 5, X (Dart.symm ⟨(h, P.x i), P.adj_h i⟩) := by
    rw [← sum_symm (fun d => if d.snd = h then X d else 0)]
    simp only [Dart.symm_toProd, Prod.snd_swap]
    have := sum_darts_at' P (fun e => X e.symm)
    rw [← this]
  have e1 := sum_darts_at' P X
  rw [Finset.sum_congr rfl (fun d _ => pt d)]
  simp only [sum_add_distrib]
  rw [e1, e2]
  abel

include hφ h3 in
open Classical in
/-- Darts whose face avoids `h`: subtract also the five link darts of the star of `h`. -/
lemma sum_faceAvoids {R : Type*} [AddCommGroup R] (P : Pent G h) (X : G.Dart → R) :
    ∑ d : G.Dart, (if FaceAvoids φ h d then X d else 0) =
      ∑ d : G.Dart, (if d.fst ≠ h ∧ d.snd ≠ h then X d else 0) -
        ∑ i : Fin 5, X (φ ⟨(h, P.x i), P.adj_h i⟩) := by
  classical
  have pt : ∀ d : G.Dart, (if d.fst ≠ h ∧ d.snd ≠ h then X d else 0) =
      (if FaceAvoids φ h d then X d else 0) + (if (φ d).snd = h then X d else 0) := by
    intro d
    have n1 : (φ d).snd ≠ d.snd := by
      have := (φ d).adj.ne
      rw [hφ] at this
      exact this.symm
    have n2 : (φ d).snd ≠ d.fst := by
      have := (φ (φ d)).adj.ne
      rw [phi2_fst φ hφ h3, phi2_snd φ hφ h3] at this
      exact this
    unfold FaceAvoids
    by_cases a : d.fst = h <;> by_cases b : d.snd = h <;> by_cases e : (φ d).snd = h
    all_goals first
      | (exfalso; exact n1 (e.trans b.symm))
      | (exfalso; exact n2 (e.trans a.symm))
      | simp [a, b, e]
  rw [Finset.sum_congr rfl (fun d _ => pt d), sum_add_distrib, sum_third_h φ hφ h3 P X]
  abel

omit [DecidableEq V] in
/-- An antisymmetric dart weight sums to zero. -/
lemma sum_antisymm {R : Type*} [AddCommGroup R] (W : G.Dart → R) (hW : ∀ d, W d.symm = - W d) :
    ∑ d : G.Dart, W d = 0 := by
  classical
  let e := Fintype.equivFin V
  let L : G.Dart → Prop := fun d => (e d.fst : ℕ) < e d.snd
  have hL : ∀ d : G.Dart, ¬ L d ↔ L d.symm := by
    intro d
    have hne : (e d.fst : ℕ) ≠ e d.snd := fun hh =>
      d.adj.ne (e.injective (Fin.ext hh))
    simp only [L, Dart.symm_toProd, Prod.fst_swap, Prod.snd_swap]
    omega
  have h1 : ∑ d : G.Dart, W d =
      ∑ d : G.Dart, (if L d then W d else 0) + ∑ d : G.Dart, (if ¬ L d then W d else 0) := by
    rw [← sum_add_distrib]
    refine sum_congr rfl fun d _ => ?_
    by_cases hd : L d <;> simp [hd]
  have h2 : ∑ d : G.Dart, (if ¬ L d then W d else 0) = - ∑ d : G.Dart, (if L d then W d else 0) := by
    rw [← sum_symm (fun d => if ¬ L d then W d else 0), ← sum_neg_distrib]
    refine sum_congr rfl fun d _ => ?_
    have := hL d.symm
    rw [Dart.symm_symm] at this
    by_cases hd : L d
    · have h' : ¬ L d.symm := fun hh => (this.mpr hd) hh
      simp only [h', not_false_eq_true, ↓reduceIte, hd, hW]
    · have h' : ¬ ¬ L d.symm := fun hh => hd (this.mp hh)
      simp only [h', ↓reduceIte, hd, neg_zero]
  rw [h1, h2, add_neg_cancel]

include hφ h3 in
open Classical in
/-- **cw mod 8 at a hole** (Lemma 0 + 0′ with the star of `h` removed; no planarity). With
`W = omT μ` on darts, the faces avoiding `h` sum to `2 cw − 5 #F + 12 #μ`, and the dart sum
telescopes to minus the link term. -/
theorem cw_dart_mod8 (P : Pent G h) (s : Fin 5)
    (hs : ∀ i, (φ ⟨(h, P.x i), P.adj_h i⟩).snd = P.x (i + s))
    {c : V → Fin 4} (hc : ProperOff G h c) (m : Fin 4) :
    2 * (cwDarts φ h c : ZMod 8) - 5 * (#(univ.filter (fun d => FaceAvoids φ h d)) : ZMod 8) +
        12 * ∑ d : G.Dart, (if FaceAvoids φ h d then eq8 (c d.fst) m else 0) =
      -3 * ∑ i : Fin 5, omT m (c (P.x i)) (c (P.x (i + s))) := by
  set W : G.Dart → ZMod 8 := fun d => omT m (c d.fst) (c d.snd) with hW
  have hWs : ∀ d : G.Dart, W d.symm = - W d := fun d => omT_antisymm m _ _
  -- (i) the sum of `W` over darts whose face avoids `h`
  have hi : ∑ d : G.Dart, (if FaceAvoids φ h d then W d else 0) =
      - ∑ i : Fin 5, omT m (c (P.x i)) (c (P.x (i + s))) := by
    rw [sum_faceAvoids φ hφ h3 P W, sum_off_h P W, sum_antisymm W hWs]
    have e1 : ∑ i : Fin 5, W (Dart.symm ⟨(h, P.x i), P.adj_h i⟩) =
        - ∑ i : Fin 5, W ⟨(h, P.x i), P.adj_h i⟩ := by
      rw [← sum_neg_distrib]
      exact sum_congr rfl fun i _ => hWs _
    have e2 : ∑ i : Fin 5, W (φ ⟨(h, P.x i), P.adj_h i⟩) =
        ∑ i : Fin 5, omT m (c (P.x i)) (c (P.x (i + s))) := by
      refine sum_congr rfl fun i _ => ?_
      simp only [hW, hφ, hs]
    rw [e1, e2]
    abel
  -- (ii) rotating within faces
  have hii : ∑ d : G.Dart, (if FaceAvoids φ h d then W d + W (φ d) + W (φ (φ d)) else 0) =
      3 * ∑ d : G.Dart, (if FaceAvoids φ h d then W d else 0) := by
    have r1 := sum_face_rot φ hφ h3 h W
    have r2 := sum_face_rot φ hφ h3 h (fun d => W (φ d))
    rw [r1] at r2
    have : ∀ d : G.Dart, (if FaceAvoids φ h d then W d + W (φ d) + W (φ (φ d)) else 0) =
        (if FaceAvoids φ h d then W d else 0) + (if FaceAvoids φ h d then W (φ d) else 0) +
          (if FaceAvoids φ h d then W (φ (φ d)) else 0) := by
      intro d; split_ifs <;> simp
    rw [sum_congr rfl (fun d _ => this d), sum_add_distrib, sum_add_distrib, r1, r2]
    ring
  -- (iii) the face table at each face avoiding `h`
  have hiii : ∀ d : G.Dart, FaceAvoids φ h d → W d + W (φ d) + W (φ (φ d)) =
      2 * ind8 (cwAt φ c d) - 5 +
        4 * (eq8 (c d.fst) m + eq8 (c (φ d).fst) m + eq8 (c (φ (φ d)).fst) m) := by
    intro d ⟨hu, hv, hw⟩
    have a1 : G.Adj d.fst d.snd := d.adj
    have a2 : G.Adj d.snd (φ d).snd := by have := (φ d).adj; rwa [hφ] at this
    have a3 : G.Adj (φ d).snd d.fst := by
      have := (φ (φ d)).adj; rwa [phi2_fst φ hφ h3, phi2_snd φ hφ h3] at this
    simp only [hW, hφ, phi2_snd φ hφ h3, cwAt]
    exact omT_face m _ _ _ (hc a1 hu hv) (hc a2 hv hw) (hc a3 hw hu)
  -- (iv) summing the right-hand side
  have hcw : (cwDarts φ h c : ZMod 8) =
      ∑ d : G.Dart, (if FaceAvoids φ h d then ind8 (cwAt φ c d) else 0) := by
    unfold cwDarts
    rw [natCast_card_filter]
    refine sum_congr rfl fun d _ => ?_
    by_cases hd : FaceAvoids φ h d <;> cases cwAt φ c d <;> simp [hd, ind8]
  have hF : (#(univ.filter (fun d => FaceAvoids φ h d)) : ZMod 8) =
      ∑ d : G.Dart, (if FaceAvoids φ h d then 1 else 0) := natCast_card_filter _ _
  have q1 := sum_face_rot φ hφ h3 h (fun d => eq8 (c d.fst) m)
  have q2 := sum_face_rot φ hφ h3 h (fun d => eq8 (c (φ d).fst) m)
  rw [q1] at q2
  have hiv : ∑ d : G.Dart, (if FaceAvoids φ h d then W d + W (φ d) + W (φ (φ d)) else 0) =
      2 * (cwDarts φ h c : ZMod 8) - 5 * (#(univ.filter (fun d => FaceAvoids φ h d)) : ZMod 8) +
        12 * ∑ d : G.Dart, (if FaceAvoids φ h d then eq8 (c d.fst) m else 0) := by
    rw [hcw, hF, sum_congr rfl (fun d _ => by rw [show (if FaceAvoids φ h d then
      W d + W (φ d) + W (φ (φ d)) else 0) = (if FaceAvoids φ h d then 2 * ind8 (cwAt φ c d) - 5 +
        4 * (eq8 (c d.fst) m + eq8 (c (φ d).fst) m + eq8 (c (φ (φ d)).fst) m) else 0) by
          split_ifs with hd
          · exact hiii d hd
          · rfl])]
    have : ∀ d : G.Dart, (if FaceAvoids φ h d then 2 * ind8 (cwAt φ c d) - 5 +
        4 * (eq8 (c d.fst) m + eq8 (c (φ d).fst) m + eq8 (c (φ (φ d)).fst) m) else 0) =
        2 * (if FaceAvoids φ h d then ind8 (cwAt φ c d) else 0) -
          5 * (if FaceAvoids φ h d then 1 else 0) +
          4 * ((if FaceAvoids φ h d then eq8 (c d.fst) m else 0) +
            (if FaceAvoids φ h d then eq8 (c (φ d).fst) m else 0) +
            (if FaceAvoids φ h d then eq8 (c (φ (φ d)).fst) m else 0)) := by
      intro d; split_ifs <;> ring
    rw [sum_congr rfl (fun d _ => this d), sum_add_distrib, sum_sub_distrib, ← mul_sum,
      ← mul_sum, ← mul_sum, sum_add_distrib, sum_add_distrib, q1, q2]
    ring
  rw [← hiv, hii, hi]
  ring

include hφ h3 in
/-- A property holding at one corner of every face avoiding `h` and at one corner of every face
of the star of `h` holds at one corner of every face. -/
lemma face_cover (P : Pent G h) (s : Fin 5)
    (hs : ∀ i, (φ ⟨(h, P.x i), P.adj_h i⟩).snd = P.x (i + s)) {Q : V → Prop}
    (hav : ∀ d, FaceAvoids φ h d → Q d.fst ∨ Q d.snd ∨ Q (φ d).snd)
    (hstar : ∀ i, Q h ∨ Q (P.x i) ∨ Q (P.x (i + s))) :
    ∀ d, Q d.fst ∨ Q d.snd ∨ Q (φ d).snd := by
  intro d
  have hfst : ∀ e : G.Dart, e.fst = h → ∃ i, e = ⟨(h, P.x i), P.adj_h i⟩ := by
    intro e he
    have ha : G.Adj h e.snd := by rw [← he]; exact e.adj
    obtain ⟨i, hi⟩ := P.only e.snd ha
    exact ⟨i, Dart.ext _ _ (Prod.ext he hi)⟩
  have d3 : φ (φ (φ d)) = d := h3 d
  by_cases hA : FaceAvoids φ h d
  · exact hav d hA
  · unfold FaceAvoids at hA
    by_cases a : d.fst = h
    · obtain ⟨i, rfl⟩ := hfst d a
      have := hstar i
      rw [hs i]
      exact this
    · by_cases b : d.snd = h
      · obtain ⟨i, hi⟩ := hfst (φ d) (by rw [hφ]; exact b)
        have e1 : (φ d).snd = P.x i := by rw [hi]
        have e2 : d.fst = P.x (i + s) := by
          have := hφ (φ (φ d))
          rw [d3] at this
          rw [this, hi, hs]
        rw [e1, e2, b]
        have := hstar i
        tauto
      · have c' : (φ d).snd = h := by tauto
        obtain ⟨i, hi⟩ := hfst (φ (φ d)) (by rw [phi2_fst φ hφ h3]; exact c')
        have e0 : d = φ ⟨(h, P.x i), P.adj_h i⟩ := by rw [← hi, d3]
        have e1 : d.fst = P.x i := by rw [e0, hφ]
        have e2 : d.snd = P.x (i + s) := by rw [e0, hs]
        rw [e1, e2, c']
        have := hstar i
        tauto

end core
end general

/-- The final bookkeeping of the proof of F, as linear arithmetic. -/
lemma f_arith (N cw n D cardD E γ hd l1 l2 s1 s2 s3 d1 d2 d3 t1 t2 t3 Mc PmA PmB Pam PaB PaA PAB
    e1 e2 e3 : ℕ)
    (X1 : (6 * cw + 12 * D + 78) % 8 = (5 * cardD + 6 * hd) % 8) (hdart : cardD = 2 * E)
    (Eul : E + 6 * γ = 3 * n) (T1 : s1 + d1 + γ = t1 + PaB) (T2 : s2 + d2 + γ = t2 + PaA)
    (T3 : s3 + Pam + γ = t3 + d3) (M1 : d1 + (1 - l1) = PmA) (M2 : d2 + (1 - l2) = PmB)
    (M3 : d3 + 0 = PAB) (E1 : e1 = 2 * s1) (E2 : e2 = 2 * s2) (E3 : e3 = 2 * s3)
    (Eedge : e1 + e2 + e3 = 2 * D + 8) (Evert : t1 + t2 + t3 = n + 1 + 2 * Mc)
    (hN : N = Pam + PAB + PaA + PmB + PaB + PmA) (hl1 : l1 ≤ 1) (hl2 : l2 ≤ 1) :
    (2 * N + 1 + hd) % 4 = (cw + n + 2 * (l1 + l2)) % 4 := by
  omega

/-! ### The sphere: Conjecture F -/

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

lemma sideGraph_active (c : Fin n → Fin 4) (p q : Fin 4) :
    sideGraph M.graph (Active h c p q) = pairGraph M.graph h c p q := rfl

open Classical in
lemma finrank_active (c : Fin n → Fin 4) (p q : Fin 4) :
    Module.finrank (ZMod 2) (chainSpace M.graph (Active h c p q)) = chainCount M.graph h c p q := by
  rw [finrank_chainSpace]
  rfl

open Classical in
/-- **Conjecture F holds** at every degree-5 hole of a triangulated spherical map without
isolated vertices. -/
theorem chainFormulaF (htri : M.Triangulated) (hiso : ∀ v, ∃ w, M.graph.Adj v w)
    (P : Pent M.graph h) : ChainFormulaF M P := by
  intro c j hc hr
  set φ := M.rotation.faceNext with hφdef
  have hφ : ∀ d, (φ d).fst = d.snd := M.rotation.face_next_fst
  have h3 : ∀ d, φ (φ (φ d)) = d := sphere_tri3 htri
  obtain ⟨s, hs1, hs⟩ := star_orient φ hφ h3 P (sphere_starHyp htri P)
  set a := c (P.x j) with ha
  set m := c (P.x (j + 1)) with hm
  set A := c (P.x (j + 3)) with hA
  set B := c (P.x (j + 4)) with hB
  obtain ⟨h02, hma, hAa, hBa, hmA, hmB, hAB⟩ := hr
  replace hma : m ≠ a := hma
  replace hAa : A ≠ a := hAa
  replace hBa : B ≠ a := hBa
  replace hmA : m ≠ A := hmA
  replace hmB : m ≠ B := hmB
  replace hAB : A ≠ B := hAB
  have hlc : ∀ k : Fin 5, c (P.x (j + k)) = ![a, m, a, A, B] k := by
    intro k
    fin_cases k
    · simp [ha]
    · rfl
    · exact h02.symm
    · rfl
    · rfl
  have hcx : ∀ i : Fin 5, c (P.x i) = ![a, m, a, A, B] (i - j) := by
    intro i
    rw [← hlc]
    congr 2
    abel
  have hcxs : ∀ i : Fin 5, c (P.x (i + s)) = ![a, m, a, A, B] (i - j + s) := by
    intro i
    rw [hcx]
    congr 1
    abel
  obtain ⟨cm, -, -⟩ := link_counts a m A B hma hAa hBa hmA hmB hAB
  -- (1) the clockwise count mod 8
  obtain ⟨hd, hhd⟩ : ∃ hd : ℕ, hd = if handS M P c j then 1 else 0 := ⟨_, rfl⟩
  have hhand : ind8 (if s = 1 then isCW (fxor a m) (fxor a A) (fxor a B)
      else !isCW (fxor a m) (fxor a A) (fxor a B)) = (hd : ZMod 8) := by
    have e0 := hs 0
    rw [zero_add] at e0
    rcases hs1 with rfl | rfl
    · have : handS M P c j = handB P c j := by
        unfold handS
        rw [ite_eq_left e0]
      rw [hhd, this]
      unfold handB
      cases isCW (fxor a m) (fxor a A) (fxor a B) <;> simp [ind8]
    · have hne : (M.rotation.faceNext ⟨(h, P.x 0), P.adj_h 0⟩).snd ≠ P.x 1 := by
        rw [e0]
        exact fun e => absurd (P.inj e) (by decide)
      have : handS M P c j = !handB P c j := by
        unfold handS
        rw [ite_eq_right hne]
      rw [hhd, this]
      unfold handB
      cases isCW (fxor a m) (fxor a A) (fxor a B) <;> simp [ind8]
  have hlink : ∑ i : Fin 5, omT m (c (P.x i)) (c (P.x (i + s))) = 5 - 2 * (hd : ZMod 8) := by
    rw [← hhand, ← omT_link a m A B s hs1 hma hAa hBa hmA hmB hAB,
      ← Equiv.sum_comp (Equiv.addLeft j)]
    refine sum_congr rfl fun k _ => ?_
    simp only [Equiv.coe_addLeft]
    rw [hcx (j + k), hcx (j + k + s)]
    have e1 : j + k - j = k := by abel
    have e2 : j + k + s - j = k + s := by abel
    rw [e1, e2]
  obtain ⟨D, hD⟩ : ∃ D : ℕ,
      D = #(univ.filter (fun d : M.Dart => (d.fst ≠ h ∧ d.snd ≠ h) ∧ c d.fst = m)) := ⟨_, rfl⟩
  have hFA : (#(univ.filter (fun d => FaceAvoids φ h d)) : ZMod 8) =
      (Fintype.card M.Dart : ZMod 8) - 15 := by
    rw [natCast_card_filter, sum_faceAvoids φ hφ h3 P (fun _ => (1 : ZMod 8)), sum_off_h P]
    simp only [sum_const, card_univ, Fintype.card_fin, nsmul_eq_mul, mul_one]
    push_cast
    ring
  have hFm : ∑ d : M.Dart, (if FaceAvoids φ h d then eq8 (c d.fst) m else 0) = (D : ZMod 8) - 1 := by
    rw [sum_faceAvoids φ hφ h3 P (fun d => eq8 (c d.fst) m), hD, natCast_card_filter]
    have e1 : ∑ i : Fin 5, eq8 (c (φ ⟨(h, P.x i), P.adj_h i⟩).fst) m = 1 := by
      rw [← cm, ← Equiv.sum_comp (Equiv.addLeft j)]
      refine sum_congr rfl fun k _ => ?_
      simp only [Equiv.coe_addLeft, hφ, hlc]
    rw [e1]
    congr 1
    refine sum_congr rfl fun d _ => ?_
    unfold eq8
    by_cases h1 : d.fst ≠ h ∧ d.snd ≠ h <;> by_cases h2 : c d.fst = m <;> simp [h1, h2]
  have key := cw_dart_mod8 φ hφ h3 P s hs hc m
  rw [hFA, hFm, hlink, cwDarts_eq φ hφ h3] at key
  have X1 : ((6 * cwCount φ h c + 12 * D + 78 : ℕ) : ZMod 8) =
      ((5 * Fintype.card M.Dart + 6 * hd : ℕ) : ZMod 8) := by
    push_cast at key ⊢
    linear_combination key
  rw [ZMod.natCast_eq_natCast_iff'] at X1
  -- (2) the three Tutte identities
  set d0 : M.Dart := ⟨(h, P.x 0), P.adj_h 0⟩
  have hxh : ∀ i, P.x i ≠ h := P.x_ne_h
  -- faces avoiding `h` are properly coloured triangles
  have tri : ∀ (p q : Fin 4) (d : M.Dart), FaceAvoids φ h d →
      (d.fst ≠ h ∧ c d.fst ≠ p ∧ c d.fst ≠ q) ∨ (d.snd ≠ h ∧ c d.snd ≠ p ∧ c d.snd ≠ q) ∨
        ((φ d).snd ≠ h ∧ c (φ d).snd ≠ p ∧ c (φ d).snd ≠ q) := by
    intro p q d ⟨hu, hv, hw⟩
    have a1 : M.graph.Adj d.fst d.snd := d.adj
    have a2 : M.graph.Adj d.snd (φ d).snd := by have := (φ d).adj; rwa [hφ] at this
    have a3 : M.graph.Adj (φ d).snd d.fst := by
      have := (φ (φ d)).adj; rwa [phi2_fst φ hφ h3, phi2_snd φ hφ h3] at this
    rcases tri_out p q _ _ _ (hc a1 hu hv) (hc a2 hv hw) (hc a3 hw hu) with e | e | e
    · exact Or.inl ⟨hu, e⟩
    · exact Or.inr (Or.inl ⟨hv, e⟩)
    · exact Or.inr (Or.inr ⟨hw, e⟩)
  have notAct : ∀ (p q : Fin 4) (v : Fin n), v ≠ h → c v ≠ p → c v ≠ q → ¬ Active h c p q v :=
    fun p q v _ e1 e2 hv => hv.2.elim e1 e2
  -- side 1: `h` with `{μ, A}`
  set τ1 : Fin n → Prop := fun v => v = h ∨ Active h c m A v with hτ1
  have hf1 : ∀ d : M.Dart, ¬ τ1 d.fst ∨ ¬ τ1 d.snd ∨ ¬ τ1 (φ d).snd := by
    refine face_cover φ hφ h3 P s hs (Q := fun v => ¬ τ1 v) ?_ ?_
    · intro d hd
      have nt : ∀ v, v ≠ h → c v ≠ m → c v ≠ A → ¬ τ1 v := fun v hv e1 e2 ht =>
        ht.elim hv (notAct m A v hv e1 e2)
      rcases tri m A d hd with ⟨x1, x2, x3⟩ | ⟨x1, x2, x3⟩ | ⟨x1, x2, x3⟩
      · exact Or.inl (nt _ x1 x2 x3)
      · exact Or.inr (Or.inl (nt _ x1 x2 x3))
      · exact Or.inr (Or.inr (nt _ x1 x2 x3))
    · intro i
      have nt : ![a, m, a, A, B] (i - j) ≠ m ∧ ![a, m, a, A, B] (i - j) ≠ A → ¬ τ1 (P.x i) :=
        fun e ht => ht.elim (hxh i) (notAct m A _ (hxh i) (by rw [hcx]; exact e.1)
          (by rw [hcx]; exact e.2))
      rcases (link_pair a m A B (i - j) s hs1 hma hAa hBa hmA hmB hAB).1 with e | e
      · exact Or.inr (Or.inl (nt e))
      · refine Or.inr (Or.inr fun ht => ht.elim (hxh _) (notAct m A _ (hxh _) ?_ ?_))
        · rw [hcxs]; exact e.1
        · rw [hcxs]; exact e.2
  -- side 2: `h` with `{μ, B}`
  set τ2 : Fin n → Prop := fun v => v = h ∨ Active h c m B v with hτ2
  have hf2 : ∀ d : M.Dart, ¬ τ2 d.fst ∨ ¬ τ2 d.snd ∨ ¬ τ2 (φ d).snd := by
    refine face_cover φ hφ h3 P s hs (Q := fun v => ¬ τ2 v) ?_ ?_
    · intro d hd
      have nt : ∀ v, v ≠ h → c v ≠ m → c v ≠ B → ¬ τ2 v := fun v hv e1 e2 ht =>
        ht.elim hv (notAct m B v hv e1 e2)
      rcases tri m B d hd with ⟨x1, x2, x3⟩ | ⟨x1, x2, x3⟩ | ⟨x1, x2, x3⟩
      · exact Or.inl (nt _ x1 x2 x3)
      · exact Or.inr (Or.inl (nt _ x1 x2 x3))
      · exact Or.inr (Or.inr (nt _ x1 x2 x3))
    · intro i
      have nt : ![a, m, a, A, B] (i - j) ≠ m ∧ ![a, m, a, A, B] (i - j) ≠ B → ¬ τ2 (P.x i) :=
        fun e ht => ht.elim (hxh i) (notAct m B _ (hxh i) (by rw [hcx]; exact e.1)
          (by rw [hcx]; exact e.2))
      rcases (link_pair a m A B (i - j) s hs1 hma hAa hBa hmA hmB hAB).2 with e | e
      · exact Or.inr (Or.inl (nt e))
      · refine Or.inr (Or.inr fun ht => ht.elim (hxh _) (notAct m B _ (hxh _) ?_ ?_))
        · rw [hcxs]; exact e.1
        · rw [hcxs]; exact e.2
  -- side 3: `{α, μ}` (and `h` on the other side)
  set τ3 : Fin n → Prop := Active h c a m with hτ3
  have hf3 : ∀ d : M.Dart, ¬ τ3 d.fst ∨ ¬ τ3 d.snd ∨ ¬ τ3 (φ d).snd := by
    refine face_cover φ hφ h3 P s hs (Q := fun v => ¬ τ3 v) ?_ ?_
    · intro d hd
      rcases tri a m d hd with ⟨x1, x2, x3⟩ | ⟨x1, x2, x3⟩ | ⟨x1, x2, x3⟩
      · exact Or.inl (notAct a m _ x1 x2 x3)
      · exact Or.inr (Or.inl (notAct a m _ x1 x2 x3))
      · exact Or.inr (Or.inr (notAct a m _ x1 x2 x3))
    · exact fun _ => Or.inl fun hh => hh.1 rfl
  have T1 := tutte_sides htri hiso d0 τ1 hf1
  have T2 := tutte_sides htri hiso d0 τ2 hf2
  have T3 := tutte_sides htri hiso d0 τ3 hf3
  -- the complementary sides
  have C1 : chainSpace M.graph (fun v => ¬ τ1 v) = chainSpace M.graph (Active h c a B) := by
    apply chainSpace_congr
    intro v
    by_cases hv : v = h
    · simp [τ1, hv, Active]
    · have := col_compl m A a B (c v) hmA hma hmB hAa hAB (Ne.symm hBa)
      simp only [τ1, Active, hv, false_or, ne_eq, not_false_eq_true, true_and]
      exact this
  have C2 : chainSpace M.graph (fun v => ¬ τ2 v) = chainSpace M.graph (Active h c a A) := by
    apply chainSpace_congr
    intro v
    by_cases hv : v = h
    · simp [τ2, hv, Active]
    · have := col_compl m B a A (c v) hmB hma hmA hBa (Ne.symm hAB) (Ne.symm hAa)
      simp only [τ2, Active, hv, false_or, ne_eq, not_false_eq_true, true_and]
      exact this
  have C3 : chainSpace M.graph (fun v => ¬ τ3 v) =
      chainSpace M.graph (fun v => v = h ∨ Active h c A B v) := by
    apply chainSpace_congr
    intro v
    by_cases hv : v = h
    · simp [τ3, hv, Active]
    · have := col_compl a m A B (c v) (Ne.symm hma) (Ne.symm hAa) (Ne.symm hBa) hmA hmB hAB
      simp only [τ3, Active, hv, false_or, ne_eq, not_false_eq_true, true_and]
      exact this
  rw [C1, finrank_active] at T1
  rw [C2, finrank_active] at T2
  rw [C3, show Module.finrank (ZMod 2) (chainSpace M.graph τ3) = chainCount M.graph h c a m from
    finrank_active c a m] at T3
  -- (3) merging `h` into the sides: this is where the locks enter
  have hpos : ∀ (i : Fin 5) (k : Fin 5), i - j = k → i = j + k := by
    intro i k e; rw [← e]; abel
  have M1 := finrank_chainSpace_insert (G := M.graph) (Active h c m A) (h := h)
    (a := P.x (j + 1)) (b := P.x (j + 3)) (fun hh => hh.1 rfl) ⟨hxh _, Or.inl rfl⟩
    ⟨hxh _, Or.inr rfl⟩ (P.adj_h _) (P.adj_h _) (by
      intro v hv hact
      obtain ⟨i, rfl⟩ := P.only v hv
      have := (link_pos a m A B (i - j) hma hAa hBa hmA hmB hAB).1.mp (by rw [← hcx]; exact hact.2)
      rcases this with e | e
      · exact Or.inl (by rw [hpos i 1 e])
      · exact Or.inr (by rw [hpos i 3 e]))
  have M2 := finrank_chainSpace_insert (G := M.graph) (Active h c m B) (h := h)
    (a := P.x (j + 1)) (b := P.x (j + 4)) (fun hh => hh.1 rfl) ⟨hxh _, Or.inl rfl⟩
    ⟨hxh _, Or.inr rfl⟩ (P.adj_h _) (P.adj_h _) (by
      intro v hv hact
      obtain ⟨i, rfl⟩ := P.only v hv
      have := (link_pos a m A B (i - j) hma hAa hBa hmA hmB hAB).2.1.mp
        (by rw [← hcx]; exact hact.2)
      rcases this with e | e
      · exact Or.inl (by rw [hpos i 1 e])
      · exact Or.inr (by rw [hpos i 4 e]))
  have M3 := finrank_chainSpace_insert (G := M.graph) (Active h c A B) (h := h)
    (a := P.x (j + 3)) (b := P.x (j + 4)) (fun hh => hh.1 rfl) ⟨hxh _, Or.inl rfl⟩
    ⟨hxh _, Or.inr rfl⟩ (P.adj_h _) (P.adj_h _) (by
      intro v hv hact
      obtain ⟨i, rfl⟩ := P.only v hv
      have := (link_pos a m A B (i - j) hma hAa hBa hmA hmB hAB).2.2.1.mp
        (by rw [← hcx]; exact hact.2)
      rcases this with e | e
      · exact Or.inl (by rw [hpos i 3 e])
      · exact Or.inr (by rw [hpos i 4 e]))
  rw [finrank_active, sideGraph_active] at M1 M2 M3
  have r34 : (pairGraph M.graph h c A B).Reachable (P.x (j + 3)) (P.x (j + 4)) := by
    have e : j + 3 + 1 = j + 4 := by abel
    have hadj := P.adj_cyc (j + 3)
    rw [e] at hadj
    exact Adj.reachable ⟨hadj, ⟨hxh _, Or.inl rfl⟩, ⟨hxh _, Or.inr rfl⟩⟩
  rw [ite_eq_left r34] at M3
  have L1d : Lock1 P c j = (pairGraph M.graph h c m A).Reachable (P.x (j + 1)) (P.x (j + 3)) := rfl
  have L2d : Lock2 P c j = (pairGraph M.graph h c m B).Reachable (P.x (j + 1)) (P.x (j + 4)) := rfl
  rw [← L1d] at M1
  rw [← L2d] at M2
  have M1' : Module.finrank (ZMod 2) (chainSpace M.graph τ1) + (if Lock1 P c j then 0 else 1) =
      chainCount M.graph h c m A := M1
  have M2' : Module.finrank (ZMod 2) (chainSpace M.graph τ2) + (if Lock2 P c j then 0 else 1) =
      chainCount M.graph h c m B := M2
  clear M1 M2
  -- (4) counting
  have E1 := card_darts_side M.graph τ1
  have E2 := card_darts_side M.graph τ2
  have E3 := card_darts_side M.graph τ3
  have Eedge : 2 * Fintype.card (SE M.graph τ1) + 2 * Fintype.card (SE M.graph τ2) +
      2 * Fintype.card (SE M.graph τ3) = 2 * D + 8 := by
    rw [← E1, ← E2, ← E3]
    -- a dart sum in `ℤ`
    set X : M.Dart → ℤ := fun d => (if τ1 d.fst ∧ τ1 d.snd then 1 else 0) +
      (if τ2 d.fst ∧ τ2 d.snd then 1 else 0) + (if τ3 d.fst ∧ τ3 d.snd then 1 else 0) with hX
    have hsum : ((#(univ.filter (fun d : M.Dart => τ1 d.fst ∧ τ1 d.snd)) +
        #(univ.filter (fun d : M.Dart => τ2 d.fst ∧ τ2 d.snd)) +
        #(univ.filter (fun d : M.Dart => τ3 d.fst ∧ τ3 d.snd)) : ℕ) : ℤ) = ∑ d, X d := by
      push_cast
      rw [natCast_card_filter, natCast_card_filter, natCast_card_filter, ← sum_add_distrib,
        ← sum_add_distrib]
    -- colours at a dart off `h`
    have hoff : ∀ d : M.Dart, d.fst ≠ h → d.snd ≠ h →
        X d = (if c d.fst = m then 1 else 0) + (if c d.snd = m then 1 else 0) := by
      intro d hu hv
      have hne : c d.fst ≠ c d.snd := hc d.adj hu hv
      simp only [hX, τ1, τ2, τ3, Active, hu, hv, false_or, ne_eq, not_false_eq_true, true_and]
      rcases col_cover a m A B (c d.fst) hma hAa hBa hmA hmB hAB with e | e | e | e <;>
        rcases col_cover a m A B (c d.snd) hma hAa hBa hmA hmB hAB with f | f | f | f <;>
        rw [e, f] at hne ⊢ <;>
        simp [hma, hAa, hBa, hmA, hmB, hAB, Ne.symm hma, Ne.symm hAa, Ne.symm hBa,
          Ne.symm hmA, Ne.symm hmB, Ne.symm hAB] at hne ⊢
    -- darts at `h`
    have hlnk : ∀ i : Fin 5, X ⟨(h, P.x i), P.adj_h i⟩ =
        (if c (P.x i) = m ∨ c (P.x i) = A then 1 else 0) +
          (if c (P.x i) = m ∨ c (P.x i) = B then 1 else 0) := by
      intro i
      simp [hX, τ1, τ2, τ3, Active, hxh i]
    have hlnk' : ∀ i : Fin 5, X (Dart.symm ⟨(h, P.x i), P.adj_h i⟩) =
        X ⟨(h, P.x i), P.adj_h i⟩ := by
      intro i
      simp only [hX, Dart.symm_toProd, Prod.fst_swap, Prod.snd_swap, and_comm]
    obtain ⟨-, cA, cB⟩ := link_counts a m A B hma hAa hBa hmA hmB hAB
    have h4 : ∑ i : Fin 5, X ⟨(h, P.x i), P.adj_h i⟩ = 4 := by
      simp only [hlnk]
      rw [sum_add_distrib, ← Equiv.sum_comp (Equiv.addLeft j),
        ← Equiv.sum_comp (Equiv.addLeft j) (fun i => if c (P.x i) = m ∨ c (P.x i) = B then
          (1 : ℤ) else 0)]
      simp only [Equiv.coe_addLeft, hlc]
      rw [cA, cB]
      norm_num
    have hD' : (D : ℤ) = ∑ d : M.Dart, (if d.fst ≠ h ∧ d.snd ≠ h then
        (if c d.fst = m then 1 else 0) else 0) := by
      rw [hD, natCast_card_filter]
      refine sum_congr rfl fun d _ => ?_
      by_cases h1 : d.fst ≠ h ∧ d.snd ≠ h <;> by_cases h2 : c d.fst = m <;> simp [h1, h2]
    have hD'' : (D : ℤ) = ∑ d : M.Dart, (if d.fst ≠ h ∧ d.snd ≠ h then
        (if c d.snd = m then 1 else 0) else 0) := by
      rw [hD', ← sum_symm]
      refine sum_congr rfl fun d _ => ?_
      simp only [Dart.symm_toProd, Prod.fst_swap, Prod.snd_swap, and_comm]
    have hS := sum_off_h P X
    rw [sum_congr rfl (fun d _ => show (if d.fst ≠ h ∧ d.snd ≠ h then X d else 0) =
      (if d.fst ≠ h ∧ d.snd ≠ h then (if c d.fst = m then 1 else 0) else 0) +
        (if d.fst ≠ h ∧ d.snd ≠ h then (if c d.snd = m then 1 else 0) else 0) by
          by_cases hh : d.fst ≠ h ∧ d.snd ≠ h
          · rw [ite_eq_left hh, ite_eq_left hh, ite_eq_left hh]
            exact hoff d hh.1 hh.2
          · rw [ite_eq_right hh, ite_eq_right hh, ite_eq_right hh, add_zero]), sum_add_distrib, ← hD', ← hD'', sum_congr rfl (fun i _ => hlnk' i), h4] at hS
    have : ((#(univ.filter (fun d : M.Dart => τ1 d.fst ∧ τ1 d.snd)) +
        #(univ.filter (fun d : M.Dart => τ2 d.fst ∧ τ2 d.snd)) +
        #(univ.filter (fun d : M.Dart => τ3 d.fst ∧ τ3 d.snd)) : ℕ) : ℤ) = ((2 * D + 8 : ℕ) : ℤ) := by
      rw [hsum]
      push_cast
      linarith
    norm_cast at this
    convert this
  have Evert : #(univ.filter τ1) + #(univ.filter τ2) + #(univ.filter τ3) =
      n + 1 + 2 * #(univ.filter (fun v => v ≠ h ∧ c v = m)) := by
    simp only [Finset.card_filter]
    rw [← sum_add_distrib, ← sum_add_distrib, mul_sum]
    have pt : ∀ v : Fin n, ((if τ1 v then 1 else 0) + (if τ2 v then 1 else 0) +
        (if τ3 v then 1 else 0) : ℕ) =
        1 + (if v = h then 1 else 0) + 2 * (if v ≠ h ∧ c v = m then 1 else 0) := by
      intro v
      by_cases hv : v = h
      · simp [τ1, τ2, τ3, hv, Active]
      · simp only [τ1, τ2, τ3, Active, hv, false_or, ne_eq, not_false_eq_true, true_and,
          ite_false]
        rcases col_cover a m A B (c v) hma hAa hBa hmA hmB hAB with e | e | e | e <;>
          simp [e, hma, hAa, hBa, hmA, hmB, hAB, Ne.symm hma, Ne.symm hAa, Ne.symm hBa,
            Ne.symm hmA, Ne.symm hmB, Ne.symm hAB]
    rw [sum_congr rfl (fun v _ => pt v), sum_add_distrib, sum_add_distrib]
    simp
  have Eul := euler_tri htri hiso d0
  have hdart := SimpleGraph.card_dart_eq_twice_card_edges (G := M.graph)
  rw [SimpleGraph.edgeFinset_card] at hdart
  have hdd : Fintype.card M.Dart = Fintype.card M.graph.Dart := Fintype.card_congr (Equiv.refl _)
  have hN := nChains_roles P ⟨h02, hma, hAa, hBa, hmA, hmB, hAB⟩
  rw [← ha, ← hm, ← hA, ← hB] at hN
  -- (5) the arithmetic
  suffices H : ((2 * nChains M.graph h c + 1 + hd : ℕ) : ZMod 4) =
      ((cwCount φ h c + n + 2 * ((if Lock1 P c j then 1 else 0) +
        (if Lock2 P c j then 1 else 0)) : ℕ) : ZMod 4) by
    rw [hhd] at H
    push_cast at H
    linear_combination H
  rw [ZMod.natCast_eq_natCast_iff']
  have nl1 : (if Lock1 P c j then 0 else 1) = 1 - (if Lock1 P c j then 1 else 0) := by
    split_ifs <;> rfl
  have nl2 : (if Lock2 P c j then 0 else 1) = 1 - (if Lock2 P c j then 1 else 0) := by
    split_ifs <;> rfl
  rw [nl1] at M1'
  rw [nl2] at M2'
  exact f_arith _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ X1 (hdd.trans hdart) Eul
    T1 T2 T3 M1' M2' M3 rfl rfl rfl Eedge Evert hN (by split_ifs <;> simp) (by split_ifs <;> simp)

/-- **Conjecture F is a theorem** (`TrackK/FProof.md`, formalised without topology). -/
theorem conjectureF : ConjectureF :=
  fun _ _ _ P htri hiso => chainFormulaF htri hiso P

/-- **Theorem 6 (chain-parity law)** on every triangulated spherical map without isolated
vertices: for every proper doubly locked state, `N(π c) + N(c)` is odd iff `π c` is doubly
locked. -/
theorem chainParityLaw_sphere (htri : M.Triangulated) (hiso : ∀ v, ∃ w, M.graph.Adj v w)
    (P : Pent M.graph h) : ChainParityLaw M P :=
  chainParityLaw_of_F htri P (chainFormulaF htri hiso P)

/-- **Rigid isolation**: the `π`-image of a rigid state is not rigid, in any frame. -/
theorem rigid_isolation (htri : M.Triangulated) (hiso : ∀ v, ∃ w, M.graph.Adj v w)
    (P : Pent M.graph h) {c : Fin n → Fin 4} {j : Fin 5} (hc : ProperOff M.graph h c)
    (hR : RigidAt P c j) (j' : Fin 5) : ¬ RigidAt P (piMove P c) j' :=
  rigid_isolation_of_law (chainParityLaw_sphere htri hiso P) hc hR j'

open Classical in
/-- **Remark 7**: a Kempe swap whose component misses the link preserves `N + L1 + L2` mod 2. -/
theorem remark7 (htri : M.Triangulated) (hiso : ∀ v, ∃ w, M.graph.Adj v w)
    (P : Pent M.graph h) {c : Fin n → Fin 4} {j : Fin 5} (hc : ProperOff M.graph h c)
    (hr : RepeatAt P c j) {p q : Fin 4} {X : Set (Fin n)}
    (hpq : p ≠ q) (hX : Whole M.graph h c p q X) (hfree : ∀ i, P.x i ∉ X) :
    (nChains M.graph h (swap c p q X) + (if Lock1 P (swap c p q X) j then 1 else 0) +
        (if Lock2 P (swap c p q X) j then 1 else 0)) % 2 =
      (nChains M.graph h c + (if Lock1 P c j then 1 else 0) +
        (if Lock2 P c j then 1 else 0)) % 2 :=
  remark7_of_F htri P (chainFormulaF htri hiso P) hc hr hpq hX hfree

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.omT_face
#print axioms SimpleGraph.QuarterFloor.omT_link
#print axioms SimpleGraph.QuarterFloor.cw_dart_mod8
#print axioms SimpleGraph.QuarterFloor.f_arith
#print axioms SimpleGraph.QuarterFloor.chainFormulaF
#print axioms SimpleGraph.QuarterFloor.conjectureF
#print axioms SimpleGraph.QuarterFloor.chainParityLaw_sphere
#print axioms SimpleGraph.QuarterFloor.rigid_isolation
#print axioms SimpleGraph.QuarterFloor.remark7

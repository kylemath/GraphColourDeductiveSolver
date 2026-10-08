/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.ChainCount

/-!
# The clockwise face count mod 4 under a Kempe swap (Track C, Lemma W)

Colours are `Fin 4` with bitwise XOR (`fxor`), i.e. `ZMod 2 × ZMod 2`. The face of a dart `d`
under a face successor `φ` (with `(φ d).fst = d.snd` and `φ³ = 1`: a triangulated rotation
system, i.e. a triangulated orientable closed surface) is `(d.fst, d.snd, (φ d).snd)`; its
Tait triple is `(c u ⊕ c v, c v ⊕ c w, c w ⊕ c u)`. `cwCount φ h c` is the number of faces
avoiding `h` whose Tait triple is a cyclic shift of `(1, 2, 3)` (`TrackC/scripts/tc_mod4.py`,
`cwcount`). It is defined as `cwDarts / 3`, where `cwDarts` counts darts, and
`cwDarts_eq` shows `cwDarts = 3 * cwCount`.

For a pentagonal hole `h` (`Pent`) and a set `X`, `linkInner P X` is the number of link edges
`x i x (i+1)` with both ends in `X` (`m_h(K)` of `tc_mod4.py`).

## Lemma W, corrected

The hand sketch claimed `Δcw ≡ 2 m_h(K) (mod 4)` for every Kempe component `K` of `T − h`.
That is false in general (e.g. `Δcw` can be odd). The correct statement has a boundary term
`β(K) = linkTerm …`, a signed count of the link edges with exactly one end in `K`:

* `cw_swap_mod8` (no planarity; any face successor with the star of `h` a rotation):
  `2 cw(c') + β ≡ 2 cw(c) + 4 m_h (mod 8)`, where `c'` is `c` with the `{p, q}`-component `K`
  swapped, and `β = Σ_k ([x_{k+s} ∈ K, x_k ∉ K] E(c x_{k+s} ⊕ c x_k) − [x_k ∈ K, x_{k+s} ∉ K]
  E(c x_k ⊕ c x_{k+s}))`, `E(x) = ±1` according as `(x, p ⊕ q, x ⊕ p ⊕ q)` is clockwise.
* `lemmaW`: if `β = 0` (`LinkBalanced`), then `cw(c') ≡ cw(c) + 2 m_h(K) (mod 4)`.
* `lemmaW_linkFree`: a swap whose component misses the link leaves `cw` unchanged mod 4.
* `cw_piMove` (sphere): at a doubly locked state, `cw(π c) ≡ cw(c) + 2 (mod 4)`
  (`m_h = 1`, `β = 0`).

The proof is the dart sum of `QuarterLockParity`: a dart weight (`omD`) whose sum over each face
avoiding `h` is `−2 Δ[face clockwise]` mod 8 (`face_table8`, decided over 512 cases), which is
antisymmetric under dart reversal up to `4 · [both ends in K]`, so its total is a sum over the
ten darts of the star of `h`.

## Conjecture F and its consequences

* `ChainFormulaF M P` (a `Prop`; proved in `ChainF.lean`, `chainFormulaF`/`conjectureF`): for
  every proper unfilled state at `h`,
  `2 N ≡ cw + (n − 1) − hand + 2 (L1 + L2) (mod 4)`.
* `chainParityLaw_of_F`: **F ⇒ Theorem 6** (`ChainParityLaw`, from `ChainCount`).
* `remark7_of_F`: **F ⇒ Remark 7**: a link-free swap preserves `N + L1 + L2` mod 2.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill Finset

/-! ### Colour tables -/

/-- Bitwise XOR on `Fin 4` (colours as `ZMod 2 × ZMod 2`). -/
def fxor (a b : Fin 4) : Fin 4 :=
  ![![0, 1, 2, 3], ![1, 0, 3, 2], ![2, 3, 0, 1], ![3, 2, 1, 0]] a b

/-- A Tait triple is a cyclic shift of `(1, 2, 3)`. -/
def isCW (x y z : Fin 4) : Bool :=
  (x == 1 && y == 2 && z == 3) || (x == 2 && y == 3 && z == 1) || (x == 3 && y == 1 && z == 2)

/-- Indicator in `ZMod 8`. -/
def ind8 (b : Bool) : ZMod 8 := if b then 1 else 0

/-- The sign `E` of a dart with Tait colour `x` leaving a component of Tait colour `t`. -/
def sgnE (x t : Fin 4) : ZMod 8 := if isCW x t (fxor x t) then 1 else -1

/-- Add `t` to a Tait colour when the flag is set. -/
def twist (b : Bool) (x t : Fin 4) : Fin 4 := if b then fxor x t else x

/-- The dart weight from the membership flags of its ends, its Tait colour `x` and `t`. -/
def om (iu iv : Bool) (x t : Fin 4) : ZMod 8 :=
  (ind8 (iu && !iv) - ind8 (!iu && iv)) * sgnE x t + 4 * ind8 (iu && iv)

lemma fxor_eq_zero : ∀ a b : Fin 4, fxor a b = 0 ↔ a = b := by decide

lemma fxor_comm : ∀ a b : Fin 4, fxor a b = fxor b a := by decide

lemma fxor_tri : ∀ a b e : Fin 4, fxor e a = fxor (fxor a b) (fxor b e) := by decide

lemma fxor_twist : ∀ (iu iv : Bool) (a b t : Fin 4),
    fxor (twist iu a t) (twist iv b t) = twist (iu != iv) (fxor a b) t := by decide

lemma swap_eq_fxor : ∀ p q a : Fin 4, (a = p ∨ a = q) →
    Equiv.swap p q a = fxor a (fxor p q) := by decide

lemma kempe_same : ∀ a b p q : Fin 4, a ≠ b → (a = p ∨ a = q) → (b = p ∨ b = q) →
    fxor a b = fxor p q := by decide

lemma kempe_close : ∀ a b p q : Fin 4, (a = p ∨ a = q) → fxor a b = fxor p q →
    (b = p ∨ b = q) := by decide

lemma isCW_rot : ∀ x y z : Fin 4, isCW y z x = isCW x y z := by decide

lemma isCW_rot2 : ∀ x y z : Fin 4, isCW z x y = isCW x y z := by decide

/-- **The face table.** For a properly coloured triangle with Tait colours `(x, y, x ⊕ y)` and
flags `iu, iv, iw` of membership in a `{p, q}`-Kempe component (`t = p ⊕ q`), twice the change
of the clockwise indicator plus the three dart weights vanishes mod 8. -/
lemma face_table8 : ∀ (x y t : Fin 4) (iu iv iw : Bool), t ≠ 0 → x ≠ 0 → y ≠ 0 →
    fxor x y ≠ 0 →
    ((iu != iv) = true → x ≠ t) → ((iu && iv) = true → x = t) →
    ((iv != iw) = true → y ≠ t) → ((iv && iw) = true → y = t) →
    ((iw != iu) = true → fxor x y ≠ t) → ((iw && iu) = true → fxor x y = t) →
    2 * (ind8 (isCW (twist (iu != iv) x t) (twist (iv != iw) y t) (twist (iw != iu) (fxor x y) t))
        - ind8 (isCW x y (fxor x y))) + om iu iv x t + om iv iw y t + om iw iu (fxor x y) t
      = 0 := by
  decide

/-- The link boundary term `β`: link flags `I`, link colours `C`, `t = p ⊕ q`, and the star
of `h` with faces `(h, x k, x (k + s))`. -/
def linkTerm (I : Fin 5 → Bool) (C : Fin 5 → Fin 4) (t : Fin 4) (s : Fin 5) : ZMod 8 :=
  ∑ k : Fin 5, (ind8 (I (k + s) && !I k) * sgnE (fxor (C (k + s)) (C k)) t -
    ind8 (I k && !I (k + s)) * sgnE (fxor (C k) (C (k + s))) t)

/-- The number of link edges `x k x (k + s)` inside the component, in `ZMod 8`. -/
def linkM (I : Fin 5 → Bool) (s : Fin 5) : ZMod 8 := ∑ k : Fin 5, ind8 (I k && I (k + s))

lemma fin5_add14 : ∀ k : Fin 5, k + 1 + 4 = k := by decide

lemma linkTerm_four (I : Fin 5 → Bool) (C : Fin 5 → Fin 4) (t : Fin 4) :
    linkTerm I C t 4 = - linkTerm I C t 1 := by
  unfold linkTerm
  rw [← Equiv.sum_comp (Equiv.addRight 1), ← sum_neg_distrib]
  refine sum_congr rfl fun k _ => ?_
  simp only [Equiv.coe_addRight, fin5_add14]
  ring

lemma linkM_four (I : Fin 5 → Bool) : linkM I 4 = linkM I 1 := by
  unfold linkM
  rw [← Equiv.sum_comp (Equiv.addRight 1)]
  refine sum_congr rfl fun k _ => ?_
  simp only [Equiv.coe_addRight, fin5_add14, Bool.and_comm]

/-- At `π` of a doubly locked state: link `(α, μ, α, A, B)`, component `K_{αA}(x₂)` meeting
the link in `{x₂, x₃}`; the boundary term vanishes and one link edge is inside. -/
lemma table_pi : ∀ (a m A B : Fin 4) (s : Fin 5), (s = 1 ∨ s = 4) → m ≠ a → A ≠ a → B ≠ a →
    m ≠ A → m ≠ B → A ≠ B →
    linkTerm ![false, false, true, true, false] ![a, m, a, A, B] (fxor a A) s = 0 ∧
      linkM ![false, false, true, true, false] s = 1 := by
  decide

lemma fun5_ext4 {f g : Fin 5 → Fin 4} (h0 : f 0 = g 0) (h1 : f 1 = g 1) (h2 : f 2 = g 2)
    (h3 : f 3 = g 3) (h4 : f 4 = g 4) : f = g := by
  funext k
  fin_cases k
  exacts [h0, h1, h2, h3, h4]

lemma zmod8_to_4 {a b m : ℕ} (H : 2 * (a : ZMod 8) = 2 * b + 4 * m) :
    (a : ZMod 4) = b + 2 * m := by
  have H' : ((2 * a : ℕ) : ZMod 8) = ((2 * b + 4 * m : ℕ) : ZMod 8) := by push_cast; exact H
  rw [ZMod.natCast_eq_natCast_iff'] at H'
  have e : a % 4 = (b + 2 * m) % 4 := by omega
  have := (ZMod.natCast_eq_natCast_iff' a (b + 2 * m) 4).2 e
  push_cast at this
  exact this

lemma odd_iff_of_zmod4 {x : ℕ} {L : Prop} [Decidable L]
    (H : 2 * (x : ZMod 4) = 2 * (if L then 1 else 0)) : Odd x ↔ L := by
  by_cases hL : L
  · simp only [hL, ↓reduceIte, mul_one] at H
    have H' : ((2 * x : ℕ) : ZMod 4) = ((2 : ℕ) : ZMod 4) := by push_cast; exact H
    rw [ZMod.natCast_eq_natCast_iff'] at H'
    simp only [hL, iff_true, Nat.odd_iff]
    omega
  · simp only [hL, ↓reduceIte, mul_zero] at H
    have H' : ((2 * x : ℕ) : ZMod 4) = ((0 : ℕ) : ZMod 4) := by push_cast; exact H
    rw [ZMod.natCast_eq_natCast_iff'] at H'
    simp only [hL, iff_false, Nat.not_odd_iff_even, Nat.even_iff]
    omega

lemma mod2_of_zmod4 {a b : ℕ} (H : 2 * (a : ZMod 4) = 2 * b) : a % 2 = b % 2 := by
  have H' : ((2 * a : ℕ) : ZMod 4) = ((2 * b : ℕ) : ZMod 4) := by push_cast; exact H
  rw [ZMod.natCast_eq_natCast_iff'] at H'
  omega

/-! ### The face count -/

section general
variable {V : Type*} [Fintype V] [DecidableEq V] {G : SimpleGraph V} [DecidableRel G.Adj]

/-- The face of `d` (under the face successor `φ`) avoids `h`. -/
def FaceAvoids (φ : Equiv.Perm G.Dart) (h : V) (d : G.Dart) : Prop :=
  d.fst ≠ h ∧ d.snd ≠ h ∧ (φ d).snd ≠ h

/-- The Tait triple of the face of `d`, read from `d`, is a cyclic shift of `(1, 2, 3)`. -/
def cwAt (φ : Equiv.Perm G.Dart) (c : V → Fin 4) (d : G.Dart) : Bool :=
  isCW (fxor (c d.fst) (c d.snd)) (fxor (c d.snd) (c (φ d).snd)) (fxor (c (φ d).snd) (c d.fst))

open Classical in
/-- Darts whose face avoids `h` and is clockwise (three per such face). -/
noncomputable def cwDarts (φ : Equiv.Perm G.Dart) (h : V) (c : V → Fin 4) : ℕ :=
  #{d : G.Dart | FaceAvoids φ h d ∧ cwAt φ c d = true}

/-- **`cw`**: the number of faces avoiding `h` whose Tait triple is a cyclic shift of
`(1, 2, 3)`. -/
noncomputable def cwCount (φ : Equiv.Perm G.Dart) (h : V) (c : V → Fin 4) : ℕ :=
  cwDarts φ h c / 3

open Classical in
/-- **`m_h(K)`**: the number of link edges `x i x (i+1)` with both ends in `X`. -/
noncomputable def linkInner {h : V} (P : Pent G h) (X : Set V) : ℕ :=
  #{i : Fin 5 | P.x i ∈ X ∧ P.x (i + 1) ∈ X}

open Classical in
/-- The boundary term `β(K)` of a set `X` at the hole vanishes. -/
def LinkBalanced {h : V} (P : Pent G h) (c : V → Fin 4) (p q : Fin 4) (X : Set V) : Prop :=
  linkTerm (fun k => decide (P.x k ∈ X)) (fun k => c (P.x k)) (fxor p q) 1 = 0

/-- `hand`: `(α ⊕ μ, α ⊕ A, α ⊕ B)` is a cyclic shift of `(1, 2, 3)` in the frame `j`. -/
def handB {h : V} (P : Pent G h) (c : V → Fin 4) (j : Fin 5) : Bool :=
  isCW (fxor (c (P.x j)) (c (P.x (j + 1)))) (fxor (c (P.x j)) (c (P.x (j + 3))))
    (fxor (c (P.x j)) (c (P.x (j + 4))))

omit [DecidableEq V] in
lemma sum_symm {R : Type*} [AddCommMonoid R] (f : G.Dart → R) :
    ∑ d : G.Dart, f d.symm = ∑ d, f d :=
  Equiv.sum_comp (dartSymmPerm (G := G)) f

/-- Sums over the darts out of `h` (any coefficients). -/
lemma sum_darts_at' {R : Type*} [AddCommMonoid R] {h : V} (P : Pent G h) (f : G.Dart → R) :
    ∑ e : G.Dart, (if e.fst = h then f e else 0) =
      ∑ i : Fin 5, f ⟨(h, P.x i), P.adj_h i⟩ := by
  rw [← sum_filter]
  have : univ.filter (fun e : G.Dart => e.fst = h) =
      univ.image (fun i : Fin 5 => (⟨(h, P.x i), P.adj_h i⟩ : G.Dart)) := by
    ext e
    simp only [mem_filter, mem_univ, true_and, mem_image]
    constructor
    · intro he
      have ha : G.Adj h e.snd := by rw [← he]; exact e.adj
      obtain ⟨i, hi⟩ := P.only e.snd ha
      exact ⟨i, Dart.ext _ _ (Prod.ext he.symm hi.symm)⟩
    · rintro ⟨i, rfl⟩
      rfl
  rw [this, sum_image]
  intro i _ i' _ hii
  exact P.inj (congrArg (fun d : G.Dart => d.snd) hii)

section core
variable (φ : Equiv.Perm G.Dart) (hφ : ∀ d, (φ d).fst = d.snd)
  (h3 : ∀ d, φ (φ (φ d)) = d)

include hφ h3 in
lemma faceAvoids_phi (h : V) (d : G.Dart) : FaceAvoids φ h (φ d) ↔ FaceAvoids φ h d := by
  unfold FaceAvoids
  rw [hφ, phi2_snd φ hφ h3]
  tauto

include hφ h3 in
lemma cwAt_phi (c : V → Fin 4) (d : G.Dart) : cwAt φ c (φ d) = cwAt φ c d := by
  unfold cwAt
  rw [hφ, phi2_snd φ hφ h3]
  exact isCW_rot _ _ _

include hφ h3 in
/-- A `φ`-invariant set of darts has size divisible by three (each face is a 3-cycle of `φ`;
count the dart starting at the face's least vertex). -/
lemma three_dvd_card (S : G.Dart → Prop) [DecidablePred S] (hS : ∀ d, S (φ d) ↔ S d) :
    3 ∣ #{d | S d} := by
  classical
  let e := Fintype.equivFin V
  let L : G.Dart → Prop := fun d => (e d.fst : ℕ) < e d.snd ∧ (e d.fst : ℕ) < e (φ d).snd
  let f : G.Dart → ℕ := fun d => if S d ∧ L d then 1 else 0
  have ne : ∀ {u v : V}, u ≠ v → (e u : ℕ) ≠ e v := fun huv hh =>
    huv (e.injective (Fin.ext hh))
  have one : ∀ d, (if L d then 1 else 0) + (if L (φ d) then 1 else 0) +
      (if L (φ (φ d)) then 1 else 0) = (1 : ℕ) := by
    intro d
    have n1 := ne d.adj.ne
    have n2 : (e d.snd : ℕ) ≠ e (φ d).snd := by
      have := (φ d).adj.ne
      rw [hφ] at this
      exact ne this
    have n3 : (e (φ d).snd : ℕ) ≠ e d.fst := by
      have := (φ (φ d)).adj.ne
      rw [phi2_fst φ hφ h3, phi2_snd φ hφ h3] at this
      exact ne this
    simp only [L, hφ, phi2_snd φ hφ h3, h3]
    split_ifs <;> omega
  have pt : ∀ d, (if S d then 1 else 0) = f d + f (φ d) + f (φ (φ d)) := by
    intro d
    simp only [f, hS (φ d), hS d]
    by_cases hd : S d
    · simp only [hd, true_and]
      exact (one d).symm
    · simp [hd]
  refine ⟨#{d | S d ∧ L d}, ?_⟩
  calc #{d | S d} = ∑ d, (if S d then 1 else 0) := card_filter _ _
    _ = ∑ d, (f d + f (φ d) + f (φ (φ d))) := sum_congr rfl fun d _ => pt d
    _ = 3 * ∑ d, f d := by
        rw [sum_add_distrib, sum_add_distrib, Equiv.sum_comp φ f,
          (Equiv.sum_comp φ (fun d => f (φ d))).trans (Equiv.sum_comp φ f)]
        ring
    _ = 3 * #{d | S d ∧ L d} := by rw [card_filter]

include hφ h3 in
/-- `cwDarts` counts each clockwise face three times. -/
theorem cwDarts_eq (h : V) (c : V → Fin 4) : cwDarts φ h c = 3 * cwCount φ h c := by
  classical
  have hd : 3 ∣ cwDarts φ h c := by
    unfold cwDarts
    convert three_dvd_card φ hφ h3 (fun d => FaceAvoids φ h d ∧ cwAt φ c d = true)
      (fun d => by simp only [faceAvoids_phi φ hφ h3, cwAt_phi φ hφ h3])
  unfold cwCount
  exact (Nat.mul_div_cancel' hd).symm

variable {h : V} {c : V → Fin 4} {p q : Fin 4} {X : Set V}

open Classical in
/-- The dart weight `omD`. -/
noncomputable def omD (X : Set V) (c : V → Fin 4) (t : Fin 4) (d : G.Dart) : ZMod 8 :=
  om (decide (d.fst ∈ X)) (decide (d.snd ∈ X)) (fxor (c d.fst) (c d.snd)) t

open Classical in
/-- The leaving part `g` of the dart weight. -/
noncomputable def gD (X : Set V) (c : V → Fin 4) (t : Fin 4) (d : G.Dart) : ZMod 8 :=
  ind8 (decide (d.fst ∈ X) && !decide (d.snd ∈ X)) * sgnE (fxor (c d.fst) (c d.snd)) t

open Classical in
/-- Darts inside `X`. -/
noncomputable def iD (X : Set V) (d : G.Dart) : ZMod 8 :=
  ind8 (decide (d.fst ∈ X) && decide (d.snd ∈ X))

lemma omD_eq (t : Fin 4) (d : G.Dart) :
    omD X c t d = gD X c t d - gD X c t d.symm + 4 * iD X d := by
  classical
  unfold omD gD iD om
  rw [dsymm_fst, dsymm_snd, fxor_comm (c d.snd)]
  generalize decide (d.fst ∈ X) = a
  generalize decide (d.snd ∈ X) = b
  cases a <;> cases b <;> simp [ind8]

omit [Fintype V] [DecidableEq V] [DecidableRel G.Adj] in
open Classical in
lemma swap_twist (hX : Whole G h c p q X) (v : V) :
    swap c p q X v = twist (decide (v ∈ X)) (c v) (fxor p q) := by
  by_cases hv : v ∈ X
  · rw [swap_in hv, swap_eq_fxor _ _ _ (whole_active G hX hv).2]
    simp [twist, hv]
  · rw [swap_out hv]
    simp [twist, hv]

omit [Fintype V] [DecidableEq V] [DecidableRel G.Adj] in
open Classical in
lemma edge_conds (hc : ProperOff G h c) (hX : Whole G h c p q X) {a b : V} (e : G.Adj a b)
    (ha : a ≠ h) (hb : b ≠ h) :
    ((decide (a ∈ X) != decide (b ∈ X)) = true → fxor (c a) (c b) ≠ fxor p q) ∧
      ((decide (a ∈ X) && decide (b ∈ X)) = true → fxor (c a) (c b) = fxor p q) := by
  refine ⟨fun h1 heq => ?_, fun h2 => ?_⟩
  · by_cases hA : a ∈ X <;> by_cases hB : b ∈ X <;> simp [hA, hB] at h1
    · exact hB (whole_closed G hX hA e ⟨hb, kempe_close _ _ _ _ (whole_active G hX hA).2 heq⟩)
    · rw [fxor_comm] at heq
      exact hA (whole_closed G hX hB e.symm
        ⟨ha, kempe_close _ _ _ _ (whole_active G hX hB).2 heq⟩)
  · simp only [Bool.and_eq_true, decide_eq_true_eq] at h2
    exact kempe_same _ _ _ _ (hc e ha hb) (whole_active G hX h2.1).2 (whole_active G hX h2.2).2

include hφ h3 in
open Classical in
/-- The face table applied to a face avoiding `h`. -/
lemma face_step (hc : ProperOff G h c) (hpq : p ≠ q) (hX : Whole G h c p q X) (d : G.Dart)
    (hd : FaceAvoids φ h d) :
    2 * (ind8 (cwAt φ (swap c p q X) d) - ind8 (cwAt φ c d)) + omD X c (fxor p q) d +
      omD X c (fxor p q) (φ d) + omD X c (fxor p q) (φ (φ d)) = 0 := by
  obtain ⟨hu, hv, hw⟩ := hd
  have f1 : (φ d).fst = d.snd := hφ d
  have f2 := phi2_fst φ hφ h3 d
  have f3 := phi2_snd φ hφ h3 d
  have a1 := d.adj
  have a2 := (φ d).adj
  rw [f1] at a2
  have a3 := (φ (φ d)).adj
  rw [f2, f3] at a3
  obtain ⟨e1, e1'⟩ := edge_conds hc hX a1 hu hv
  obtain ⟨e2, e2'⟩ := edge_conds hc hX a2 hv hw
  obtain ⟨e3, e3'⟩ := edge_conds hc hX a3 hw hu
  have t0 : fxor p q ≠ 0 := fun e => hpq ((fxor_eq_zero p q).1 e)
  have x0 : fxor (c d.fst) (c d.snd) ≠ 0 := fun e => hc a1 hu hv ((fxor_eq_zero _ _).1 e)
  have y0 : fxor (c d.snd) (c (φ d).snd) ≠ 0 := fun e => hc a2 hv hw ((fxor_eq_zero _ _).1 e)
  have z0 : fxor (c (φ d).snd) (c d.fst) ≠ 0 := fun e => hc a3 hw hu ((fxor_eq_zero _ _).1 e)
  have tri := fxor_tri (c d.fst) (c d.snd) (c (φ d).snd)
  rw [tri] at e3 e3' z0
  unfold cwAt omD
  rw [f2, f3, f1, swap_twist hX d.fst, swap_twist hX d.snd, swap_twist hX (φ d).snd,
    fxor_twist, fxor_twist, fxor_twist, tri]
  exact face_table8 _ _ _ _ _ _ t0 x0 y0 z0 e1 e1' e2 e2' e3 e3'

include hφ h3 in
open Classical in
lemma sum_face_rot {R : Type*} [AddCommMonoid R] (h : V) (f : G.Dart → R) :
    ∑ d, (if FaceAvoids φ h d then f (φ d) else 0) = ∑ d, (if FaceAvoids φ h d then f d else 0) := by
  classical
  rw [← Equiv.sum_comp φ (fun d => if FaceAvoids φ h d then f d else 0)]
  refine sum_congr rfl fun d _ => ?_
  simp only [faceAvoids_phi φ hφ h3]

include hφ h3 in
/-- Sums over the darts whose face has third vertex `h`. -/
lemma sum_third_h {R : Type*} [AddCommMonoid R] (P : Pent G h) (f : G.Dart → R) :
    ∑ d : G.Dart, (if (φ d).snd = h then f d else 0) =
      ∑ i : Fin 5, f (φ ⟨(h, P.x i), P.adj_h i⟩) := by
  calc ∑ d : G.Dart, (if (φ d).snd = h then f d else 0)
      = ∑ e : G.Dart, (if (φ (φ e)).snd = h then f (φ e) else 0) :=
        (Equiv.sum_comp φ (fun d => if (φ d).snd = h then f d else 0)).symm
    _ = ∑ e : G.Dart, (if e.fst = h then f (φ e) else 0) :=
        sum_congr rfl fun e _ => by rw [phi2_snd φ hφ h3]
    _ = _ := sum_darts_at' P (fun e => f (φ e))

include hφ h3 in
open Classical in
/-- **Lemma W, general form (mod 8; no planarity).** For a proper colouring off `h` and a
whole `{p, q}`-Kempe component `X` of `G − h`, with the star of `h` given by `s`
(faces `(h, x i, x (i + s))`), in any frame `j`:
`2 cw(c') + β = 2 cw(c) + 4 m` in `ZMod 8`, where `c' = swap c p q X`, `β = linkTerm …` and
`m = linkM …` (the number of link edges inside `X`). -/
theorem cw_swap_mod8 (P : Pent G h) (s : Fin 5)
    (hs : ∀ i, (φ ⟨(h, P.x i), P.adj_h i⟩).snd = P.x (i + s))
    (hc : ProperOff G h c) (hpq : p ≠ q) (hX : Whole G h c p q X) (j : Fin 5) :
    2 * (cwCount φ h (swap c p q X) : ZMod 8) +
        linkTerm (fun k => decide (P.x (j + k) ∈ X)) (fun k => c (P.x (j + k))) (fxor p q) s =
      2 * (cwCount φ h c : ZMod 8) + 4 * linkM (fun k => decide (P.x (j + k) ∈ X)) s := by
  set t := fxor p q with ht
  set c' := swap c p q X with hc'
  have hXh : h ∉ X := fun hm => (whole_active G hX hm).1 rfl
  have h8 : (8 : ZMod 8) = 0 := by decide
  -- (A) the change of `cw` as a dart sum
  have hA : 3 * ((cwCount φ h c' : ZMod 8) - cwCount φ h c) =
      ∑ d : G.Dart, (if FaceAvoids φ h d then ind8 (cwAt φ c' d) - ind8 (cwAt φ c d) else 0) := by
    have e0 : ((cwDarts φ h c' : ℕ) : ZMod 8) - (cwDarts φ h c : ℕ) =
        ∑ d : G.Dart, (if FaceAvoids φ h d then ind8 (cwAt φ c' d) - ind8 (cwAt φ c d)
          else 0) := by
      unfold cwDarts
      rw [natCast_card_filter, natCast_card_filter, ← sum_sub_distrib]
      refine sum_congr rfl fun d _ => ?_
      by_cases hd : FaceAvoids φ h d <;> cases cwAt φ c' d <;> cases cwAt φ c d <;>
        simp [hd, ind8]
    rw [← e0, cwDarts_eq φ hφ h3 h c', cwDarts_eq φ hφ h3 h c]
    push_cast
    ring
  -- (B) faces avoiding `h`
  have hB : ∑ d : G.Dart, (if FaceAvoids φ h d then
      2 * (ind8 (cwAt φ c' d) - ind8 (cwAt φ c d)) + omD X c t d + omD X c t (φ d) +
        omD X c t (φ (φ d)) else 0) = 0 :=
    sum_eq_zero fun d _ => by
      by_cases hd : FaceAvoids φ h d
      · simp only [hd, ↓reduceIte]
        exact face_step φ hφ h3 hc hpq hX d hd
      · simp only [hd, ↓reduceIte]
  have rot1 := sum_face_rot φ hφ h3 h (omD X c t)
  have rot2 : ∑ d, (if FaceAvoids φ h d then omD X c t (φ (φ d)) else 0) =
      ∑ d, (if FaceAvoids φ h d then omD X c t d else 0) :=
    (sum_face_rot φ hφ h3 h (fun d => omD X c t (φ d))).trans rot1
  have hBC : 2 * ∑ d : G.Dart, (if FaceAvoids φ h d then
      ind8 (cwAt φ c' d) - ind8 (cwAt φ c d) else 0) +
      3 * ∑ d : G.Dart, (if FaceAvoids φ h d then omD X c t d else 0) = 0 := by
    have split : ∀ d : G.Dart, (if FaceAvoids φ h d then
        2 * (ind8 (cwAt φ c' d) - ind8 (cwAt φ c d)) + omD X c t d + omD X c t (φ d) +
          omD X c t (φ (φ d)) else 0) =
        2 * (if FaceAvoids φ h d then ind8 (cwAt φ c' d) - ind8 (cwAt φ c d) else 0) +
          (if FaceAvoids φ h d then omD X c t d else 0) +
          (if FaceAvoids φ h d then omD X c t (φ d) else 0) +
          (if FaceAvoids φ h d then omD X c t (φ (φ d)) else 0) := fun d => by
      split_ifs <;> simp
    have hB' := hB
    rw [sum_congr rfl fun d _ => split d, sum_add_distrib, sum_add_distrib, sum_add_distrib,
      ← mul_sum, rot1, rot2] at hB'
    linear_combination hB'
  -- (C) the dart weight: leaving part and inside part
  have pt : ∀ d : G.Dart, (if FaceAvoids φ h d then gD X c t d else 0) -
      (if FaceAvoids φ h d.symm then gD X c t d else 0) =
      (if (φ d.symm).snd = h then gD X c t d else 0) -
        (if (φ d).snd = h then gD X c t d else 0) := by
    intro d
    by_cases hm : d.fst ∈ X
    · have hu : d.fst ≠ h := fun e => hXh (e ▸ hm)
      by_cases hv : d.snd = h
      · have n1 : ¬ FaceAvoids φ h d := fun H => H.2.1 hv
        have n2 : ¬ FaceAvoids φ h d.symm := fun H => H.1 hv
        have n3 : (φ d).snd ≠ h := by
          have := (φ d).adj.ne
          rw [hφ, hv] at this
          exact Ne.symm this
        have n4 : (φ d.symm).snd ≠ h := by
          have := (φ (φ d.symm)).adj.ne
          rw [phi2_fst φ hφ h3, phi2_snd φ hφ h3, dsymm_fst, hv] at this
          exact this
        simp [n1, n2, n3, n4]
      · have e1 : FaceAvoids φ h d ↔ ¬ (φ d).snd = h :=
          ⟨fun H => H.2.2, fun H => ⟨hu, hv, H⟩⟩
        have e2 : FaceAvoids φ h d.symm ↔ ¬ (φ d.symm).snd = h :=
          ⟨fun H => H.2.2, fun H => ⟨hv, hu, H⟩⟩
        simp only [e1, e2]
        by_cases A : (φ d).snd = h <;> by_cases B : (φ d.symm).snd = h <;> simp [A, B]
    · have : gD X c t d = 0 := by unfold gD; simp [hm, ind8]
      simp [this]
  have pti : ∀ d : G.Dart, (if FaceAvoids φ h d then iD X d else 0) =
      iD X d - (if (φ d).snd = h then iD X d else 0) := by
    intro d
    by_cases hm : d.fst ∈ X ∧ d.snd ∈ X
    · have hu : d.fst ≠ h := fun e => hXh (e ▸ hm.1)
      have hv : d.snd ≠ h := fun e => hXh (e ▸ hm.2)
      by_cases A : (φ d).snd = h
      · have : ¬ FaceAvoids φ h d := fun H => H.2.2 A
        simp [this, A]
      · have : FaceAvoids φ h d := ⟨hu, hv, A⟩
        simp [this, A]
    · have : iD X d = 0 := by
        unfold iD
        by_cases a : d.fst ∈ X <;> by_cases b : d.snd ∈ X <;> simp_all [ind8]
      simp [this]
  have hsym : ∑ d : G.Dart, 4 * iD X d = 0 := by
    refine Finset.sum_involution (fun d _ => d.symm) (fun d _ => ?_) (fun d _ _ => d.symm_ne)
      (fun d _ => mem_univ _) (fun d _ => d.symm_symm)
    have : iD X d.symm = iD X d := by
      unfold iD
      rw [dsymm_fst, dsymm_snd, Bool.and_comm]
    rw [this]
    calc 4 * iD X d + 4 * iD X d = 8 * iD X d := by ring
      _ = 0 := by rw [h8, zero_mul]
  have hO : ∑ d : G.Dart, (if FaceAvoids φ h d then omD X c t d else 0) =
      ((∑ i : Fin 5, gD X c t (φ ⟨(h, P.x i), P.adj_h i⟩).symm) -
        ∑ i : Fin 5, gD X c t (φ ⟨(h, P.x i), P.adj_h i⟩)) +
      4 * (∑ d : G.Dart, iD X d - ∑ i : Fin 5, iD X (φ ⟨(h, P.x i), P.adj_h i⟩)) := by
    have s1 : ∑ d : G.Dart, (if FaceAvoids φ h d then omD X c t d else 0) =
        (∑ d : G.Dart, (if FaceAvoids φ h d then gD X c t d else 0) -
          ∑ d : G.Dart, (if FaceAvoids φ h d.symm then gD X c t d else 0)) +
        4 * ∑ d : G.Dart, (if FaceAvoids φ h d then iD X d else 0) := by
      have r : ∑ d : G.Dart, (if FaceAvoids φ h d then gD X c t d.symm else 0) =
          ∑ d : G.Dart, (if FaceAvoids φ h d.symm then gD X c t d else 0) := by
        rw [← sum_symm (fun d => if FaceAvoids φ h d.symm then gD X c t d else 0)]
        simp only [Dart.symm_symm]
      rw [← r, mul_sum, ← sum_sub_distrib, ← sum_add_distrib]
      refine sum_congr rfl fun d _ => ?_
      rw [omD_eq]
      split_ifs <;> ring
    have s2 : ∑ d : G.Dart, (if FaceAvoids φ h d then gD X c t d else 0) -
        ∑ d : G.Dart, (if FaceAvoids φ h d.symm then gD X c t d else 0) =
        ∑ i : Fin 5, gD X c t (φ ⟨(h, P.x i), P.adj_h i⟩).symm -
          ∑ i : Fin 5, gD X c t (φ ⟨(h, P.x i), P.adj_h i⟩) := by
      rw [← sum_sub_distrib, sum_congr rfl fun d _ => pt d, sum_sub_distrib,
        sum_third_h φ hφ h3 P (gD X c t)]
      congr 1
      rw [← sum_symm (fun d => if (φ d.symm).snd = h then gD X c t d else 0)]
      simp only [Dart.symm_symm]
      exact sum_third_h φ hφ h3 P (fun d => gD X c t d.symm)
    have s3 : ∑ d : G.Dart, (if FaceAvoids φ h d then iD X d else 0) =
        ∑ d : G.Dart, iD X d - ∑ i : Fin 5, iD X (φ ⟨(h, P.x i), P.adj_h i⟩) := by
      rw [sum_congr rfl fun d _ => pti d, sum_sub_distrib, sum_third_h φ hφ h3 P (iD X)]
    rw [s1, s2, s3]
  -- (D) the star of `h`, in the frame `j`
  have fst_i : ∀ i, (φ ⟨(h, P.x i), P.adj_h i⟩).fst = P.x i := fun i => hφ _
  have hG : (∑ i : Fin 5, gD X c t (φ ⟨(h, P.x i), P.adj_h i⟩).symm) -
      ∑ i : Fin 5, gD X c t (φ ⟨(h, P.x i), P.adj_h i⟩) =
      linkTerm (fun k => decide (P.x (j + k) ∈ X)) (fun k => c (P.x (j + k))) t s := by
    rw [← sum_sub_distrib]
    unfold linkTerm
    rw [← Equiv.sum_comp (Equiv.addLeft j)]
    refine sum_congr rfl fun k _ => ?_
    simp only [Equiv.coe_addLeft, gD, dsymm_fst, dsymm_snd, fst_i, hs, add_assoc]
  have hI : ∑ i : Fin 5, iD X (φ ⟨(h, P.x i), P.adj_h i⟩) =
      linkM (fun k => decide (P.x (j + k) ∈ X)) s := by
    unfold linkM
    rw [← Equiv.sum_comp (Equiv.addLeft j)]
    refine sum_congr rfl fun k _ => ?_
    simp only [Equiv.coe_addLeft, iD, fst_i, hs, add_assoc]
  rw [hO, hG, hI, ← hA] at hBC
  have hsym' : 4 * ∑ d : G.Dart, iD X d = 0 := by rw [mul_sum]; exact hsym
  linear_combination 3 * hBC + (-9) * hsym' +
    (-2 * ((cwCount φ h c' : ZMod 8) - cwCount φ h c) -
      linkTerm (fun k => decide (P.x (j + k) ∈ X)) (fun k => c (P.x (j + k))) t s +
      4 * linkM (fun k => decide (P.x (j + k) ∈ X)) s) * h8

omit [Fintype V] [DecidableEq V] [DecidableRel G.Adj] in
lemma linkInner_eq {h : V} (P : Pent G h) (X : Set V) [DecidablePred (· ∈ X)] :
    (linkInner P X : ZMod 8) = linkM (fun k => decide (P.x k ∈ X)) 1 := by
  classical
  unfold linkInner linkM
  rw [natCast_card_filter]
  refine sum_congr rfl fun i _ => ?_
  by_cases a : P.x i ∈ X <;> by_cases b : P.x (i + 1) ∈ X <;> simp [a, b, ind8]

include hφ h3 in
open Classical in
/-- **Lemma W (corrected).** If the boundary term of the component vanishes, a Kempe swap
changes `cw` by `2 m_h(K)` mod 4. No planarity: any triangulated rotation system whose star at
`h` is a rotation of the link. -/
theorem lemmaW (P : Pent G h) (hy : StarHyp φ P) (hc : ProperOff G h c) (hpq : p ≠ q)
    (hX : Whole G h c p q X) (hbal : LinkBalanced P c p q X) :
    (cwCount φ h (swap c p q X) : ZMod 4) = cwCount φ h c + 2 * linkInner P X := by
  obtain ⟨s, hs1, hs⟩ := star_orient φ hφ h3 P hy
  have key := cw_swap_mod8 φ hφ h3 P s hs hc hpq hX 0
  simp only [zero_add] at key
  have hb : linkTerm (fun k => decide (P.x k ∈ X)) (fun k => c (P.x k)) (fxor p q) s = 0 := by
    rcases hs1 with rfl | rfl
    · exact hbal
    · rw [linkTerm_four]
      unfold LinkBalanced at hbal
      rw [hbal, neg_zero]
  have hm : linkM (fun k => decide (P.x k ∈ X)) s = linkInner P X := by
    rw [linkInner_eq]
    rcases hs1 with rfl | rfl
    · rfl
    · exact linkM_four _
  rw [hb, add_zero, hm] at key
  exact zmod8_to_4 key

include hφ h3 in
open Classical in
/-- **Lemma W, link-free case.** A swap of a component missing the link leaves `cw` unchanged
mod 4. -/
theorem lemmaW_linkFree (P : Pent G h) (hy : StarHyp φ P) (hc : ProperOff G h c) (hpq : p ≠ q)
    (hX : Whole G h c p q X) (hfree : ∀ i, P.x i ∉ X) :
    (cwCount φ h (swap c p q X) : ZMod 4) = cwCount φ h c := by
  have hbal : LinkBalanced P c p q X := by
    unfold LinkBalanced linkTerm
    simp [hfree, ind8]
  have h0 : linkInner P X = 0 := by
    unfold linkInner
    simp [hfree]
  have := lemmaW φ hφ h3 P hy hc hpq hX hbal
  rw [h0] at this
  simpa using this

end core
end general

/-! ### The sphere: `π`, Conjecture F, Theorem 6 and Remark 7 -/

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {c : Fin n → Fin 4} {j : Fin 5}

lemma fin5_j3 : ∀ j : Fin 5, j + 3 + 1 = j + 4 ∧ j + 3 + 3 = j + 1 ∧ j + 3 + 4 = j + 2 := by
  decide

open Classical in
/-- **Lemma W at `π`** (sphere): at a doubly locked state, `cw(π c) ≡ cw(c) + 2 (mod 4)`. -/
theorem cw_piMove (htri : M.Triangulated) (P : Pent M.graph h) (hc : ProperOff M.graph h c)
    (hd : DoublyLocked P c j) :
    (cwCount M.rotation.faceNext h (piMove P c) : ZMod 4) =
      cwCount M.rotation.faceNext h c + 2 := by
  have hr := hd.1
  have hK : Rot3Def P c j := (lock2_iff_not_reach_alphaA htri P hr).1 hd.2.2
  rw [piMove_of_dl hd]
  obtain ⟨s, hs1, hs⟩ := star_orient M.rotation.faceNext M.rotation.face_next_fst
    (sphere_tri3 htri) P (sphere_starHyp htri P)
  set X := {v | (pairGraph M.graph h c (c (P.x j)) (c (P.x (j + 3)))).Reachable (P.x (j + 2)) v}
    with hXdef
  have seed : Active h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2)) :=
    ⟨P.x_ne_h _, Or.inl hr.1.symm⟩
  have hX := whole_component M.graph h c (c (P.x j)) (c (P.x (j + 3))) (P.x (j + 2)) seed
  obtain ⟨h02, h1, h3, h4, h13, h14, h34⟩ := hr
  obtain ⟨i0, -, -, -, -⟩ := fin5_lp j
  have key := cw_swap_mod8 M.rotation.faceNext M.rotation.face_next_fst (sphere_tri3 htri) P s
    hs hc (Ne.symm h3) hX j
  have n0 : P.x j ∉ X := hK
  have n1 : P.x (j + 1) ∉ X := fun hm => by
    rcases (whole_active M.graph hX hm).2 with e | e
    · exact h1 e
    · exact h13 e
  have m2 : P.x (j + 2) ∈ X := Reachable.refl _
  have m3 : P.x (j + 3) ∈ X := rot3_reach ⟨h02, h1, h3, h4, h13, h14, h34⟩
  have n4 : P.x (j + 4) ∉ X := fun hm => by
    rcases (whole_active M.graph hX hm).2 with e | e
    · exact h4 e
    · exact h34 e.symm
  have eI : (fun k => decide (P.x (j + k) ∈ X)) = ![false, false, true, true, false] :=
    fun5_ext (by simp [i0, n0]) (decide_eq_false n1) (decide_eq_true m2) (decide_eq_true m3)
      (decide_eq_false n4)
  have eC : (fun k => c (P.x (j + k))) =
      ![c (P.x j), c (P.x (j + 1)), c (P.x j), c (P.x (j + 3)), c (P.x (j + 4))] :=
    fun5_ext4 (by simp [i0]) rfl h02.symm rfl rfl
  rw [eI, eC] at key
  obtain ⟨hT, hM⟩ := table_pi _ _ _ _ s hs1 h1 h3 h4 h13 h14 h34
  rw [hT, hM, add_zero] at key
  have key' : 2 * (cwCount M.rotation.faceNext h (rot3 P c j) : ZMod 8) =
      2 * (cwCount M.rotation.faceNext h c : ZMod 8) + 4 * ((1 : ℕ) : ZMod 8) := by
    rw [Nat.cast_one]
    exact key
  have := zmod8_to_4 key'
  rwa [Nat.cast_one, mul_one] at this

lemma hand_rot3 {P : Pent M.graph h} (hr : RepeatAt P c j) (hK : Rot3Def P c j) :
    handB P (rot3 P c j) (j + 3) = handB P c j := by
  obtain ⟨v0, v1, v2, v3, v4⟩ := rot3_values hr hK
  obtain ⟨e1, e3, e4⟩ := fin5_j3 j
  unfold handB
  rw [e1, e3, e4, v1, v2, v3, v4]
  exact isCW_rot2 _ _ _

variable (M) in
open Classical in
/-- `hand` read with the link labelled along the face orientation (as in `tc_mod4.py`, where
the face of `h → x i` is `(h, x i, x (i+1))`): `handB` if `P` is labelled that way, its
negation if `P` is labelled against it (reversing the labels swaps `A` and `B`). -/
noncomputable def handS (P : Pent M.graph h) (c : Fin n → Fin 4) (j : Fin 5) : Bool :=
  if (M.rotation.faceNext ⟨(h, P.x 0), P.adj_h 0⟩).snd = P.x 1 then handB P c j
  else !handB P c j

lemma handS_rot3 {P : Pent M.graph h} (hr : RepeatAt P c j) (hK : Rot3Def P c j) :
    handS M P (rot3 P c j) (j + 3) = handS M P c j := by
  unfold handS
  rw [hand_rot3 hr hK]

variable (M) in
open Classical in
/-- **Conjecture F** (chain-count formula mod 4) at the hole `h`, as a statement: for every
proper unfilled state `c` with frame `j`,
`2 N(c) ≡ cw(c) + (n − 1) − hand(c) + 2 (L1(c) + L2(c)) (mod 4)`, with `hand = handS`
(read in the face orientation). Data-checked (`TrackC/scripts/tc_mod4.py`) on triangulated spheres in which every vertex has a
neighbour; proved in `ChainF.lean` (`chainFormulaF`). -/
def ChainFormulaF (P : Pent M.graph h) : Prop :=
  ∀ (c : Fin n → Fin 4) (j : Fin 5), ProperOff M.graph h c → RepeatAt P c j →
    2 * (nChains M.graph h c : ZMod 4) =
      (cwCount M.rotation.faceNext h c : ZMod 4) + ((n : ZMod 4) - 1) -
        (if handS M P c j then 1 else 0) +
        2 * ((if Lock1 P c j then 1 else 0) + (if Lock2 P c j then 1 else 0))

/-- Conjecture F for every degree-5 hole of every triangulated sphere without isolated
vertices (`n` is then the number of vertices of the triangulation). -/
def ConjectureF : Prop :=
  ∀ (n : ℕ) (M : SphericalMap n) (h : Fin n) (P : Pent M.graph h),
    M.Triangulated → (∀ v, ∃ w, M.graph.Adj v w) → ChainFormulaF M P

open Classical in
/-- **Conjecture F ⇒ Theorem 6** (with the formal Lemma W at `π`). -/
theorem chainParityLaw_of_F (htri : M.Triangulated) (P : Pent M.graph h)
    (hF : ChainFormulaF M P) : ChainParityLaw M P := by
  intro c hc ⟨j, hd⟩
  have hK : Rot3Def P c j := (lock2_iff_not_reach_alphaA htri P hd.1).1 hd.2.2
  obtain ⟨-, hc', hr', hL⟩ := rot3_spec hc hd.1 hK
  have hW := cw_piMove htri P hc hd
  rw [piMove_of_dl hd] at hW ⊢
  have F1 := hF c j hc hd.1
  have F2 := hF (rot3 P c j) (j + 3) hc' hr'
  rw [handS_rot3 hd.1 hK, hW] at F2
  simp only [hL.2 hd.2.2, ↓reduceIte] at F2
  simp only [hd.2.1, hd.2.2, ↓reduceIte] at F1
  have h4 : (4 : ZMod 4) = 0 := by decide
  have key : 2 * ((nChains M.graph h (rot3 P c j) + nChains M.graph h c : ℕ) : ZMod 4) =
      2 * (if Lock2 P (rot3 P c j) (j + 3) then 1 else 0) := by
    push_cast
    linear_combination F2 - F1 + (nChains M.graph h c : ZMod 4) * h4
  rw [odd_iff_of_zmod4 key]
  constructor
  · intro hl
    exact ⟨j + 3, hr', hL.2 hd.2.2, hl⟩
  · rintro ⟨j', hd'⟩
    have e := rep_unique hr' hd'.1
    subst e
    exact hd'.2.2

open Classical in
/-- **Conjecture F ⇒ Remark 7** (with the formal link-free Lemma W): a Kempe swap whose
component misses the link preserves `N + L1 + L2` mod 2. -/
theorem remark7_of_F (htri : M.Triangulated) (P : Pent M.graph h) (hF : ChainFormulaF M P)
    (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) {p q : Fin 4} {X : Set (Fin n)}
    (hpq : p ≠ q) (hX : Whole M.graph h c p q X) (hfree : ∀ i, P.x i ∉ X) :
    (nChains M.graph h (swap c p q X) + (if Lock1 P (swap c p q X) j then 1 else 0) +
        (if Lock2 P (swap c p q X) j then 1 else 0)) % 2 =
      (nChains M.graph h c + (if Lock1 P c j then 1 else 0) +
        (if Lock2 P c j then 1 else 0)) % 2 := by
  have hlink : ∀ i, swap c p q X (P.x i) = c (P.x i) := fun i => swap_out (hfree i)
  have hr' : RepeatAt P (swap c p q X) j := by
    unfold RepeatAt
    simp only [hlink]
    exact hr
  have hc' := properOff_swap M.graph hc hX
  have hH : handS M P (swap c p q X) j = handS M P c j := by
    unfold handS handB
    simp only [hlink]
  have hW := lemmaW_linkFree M.rotation.faceNext M.rotation.face_next_fst (sphere_tri3 htri) P
    (sphere_starHyp htri P) hc hpq hX hfree
  have F1 := hF c j hc hr
  have F2 := hF (swap c p q X) j hc' hr'
  rw [hH, hW] at F2
  have h4 : (4 : ZMod 4) = 0 := by decide
  apply mod2_of_zmod4
  push_cast
  linear_combination F2 - F1 +
    ((if Lock1 P (swap c p q X) j then 1 else 0) + (if Lock2 P (swap c p q X) j then 1 else 0) -
      (if Lock1 P c j then 1 else 0) - (if Lock2 P c j then 1 else 0) : ZMod 4) * h4

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.face_table8
#print axioms SimpleGraph.QuarterFloor.table_pi
#print axioms SimpleGraph.QuarterFloor.cwDarts_eq
#print axioms SimpleGraph.QuarterFloor.cw_swap_mod8
#print axioms SimpleGraph.QuarterFloor.lemmaW
#print axioms SimpleGraph.QuarterFloor.lemmaW_linkFree
#print axioms SimpleGraph.QuarterFloor.cw_piMove
#print axioms SimpleGraph.QuarterFloor.chainParityLaw_of_F
#print axioms SimpleGraph.QuarterFloor.remark7_of_F

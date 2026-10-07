/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterPi

/-!
# Theorem W, counting half: `3F − U = −Σ λ` and `3F − U ≡ 0 (mod 5)`

Built on Lemma Π (`QuarterPi`). Write `[F c]` for the filled indicator (`Target`) of a state.

## The pointwise identity (no cycles needed)

From the `λ` table (`lam_table`) and the case lemmas of `QuarterPi` (`rot3_move`,
`phiBinv_spec`, `phiA_spec`, `tau_spec`, which say whether `π c` is filled):

| state | `λ` | `π c` | `1 − 2[F c] − 2[F (π c)]` |
|---|---|---|---|
| `U`, `Lock2` | `+1` | `U` | `1` |
| `U`, `¬Lock2` | `−1` | `F` | `−1` |
| `F`, `M3` short | `−1` | `U` | `−1` |
| `F`, `M3` long | `−3` | `F` | `−3` |

so `λ c = 1 − 2[F c] − 2[F (π c)]` (`lam_eq`). Equivalently
`λ c = 1 − 4[F c] + g (π c) − g c` with telescoping term **`g = 2·[unfilled]`**
(`= −2·[F]` up to a constant): the hand per-cycle claim `Σ_Z λ = |Z| − 4 F_Z` is the sum of this
over a `π`-orbit. Summing over any finite `π`-invariant set `S` of proper-off states
(`Set.BijOn (piMove P) S S`), the `g`-terms cancel:

* `sum_lam`: `Σ_{c∈S} λ c = |S| − 4·F_S`;
* `three_F_sub_U`: `3 F_S − U_S = − Σ_{c∈S} λ c`;
* `five_dvd_sum_lam`: `5 ∣ Σ_{c∈S} λ c` (from `sigma_piMove`: the token sum `σ` telescopes in
  `ℤ/5`), hence `three_F_sub_U_mod5`: `5 ∣ 3 F_S − U_S`, and the integer winding
  `windingSum S = (Σ λ)/5` satisfies `3F − U = −5·windingSum` (`three_F_sub_U_winding`).

For a Kempe class `kclass M h c₀` all of this applies by `piMove_bijOn_class` (`*_class`).

## The quarter floor in winding form

`quarterFloor_iff_lam`: on a `SphericalMap` with a pentagonal hole, `QuarterFloorConj` holds iff
for every proper-off `c₀`, `Σ_{c ∈ class(c₀)} λ c ≤ 0` (equivalently the class winding is
`≤ 0`). All results in this file are sorry-free.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section filledZ
variable {V : Type*} (G : SimpleGraph V) (h : V)

open Classical in
/-- The filled indicator `[F c]` as an integer. -/
noncomputable def filledZ (c : V → Fin 4) : ℤ := if Target G h c then 1 else 0

end filledZ

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {P : Pent M.graph h} {c : Fin n → Fin 4}

private lemma filledZ_rep {d : Fin n → Fin 4} {j : Fin 5} (hr : RepeatAt P d j) :
    filledZ M.graph h d = 0 := ite_eq_right (rep_not_target hr)

private lemma filledZ_single {d : Fin n → Fin 4} {i : Fin 5} (hs : SingletonAt P d i) :
    filledZ M.graph h d = 1 := ite_eq_left hs.1

/-- **Pointwise form of Theorem W.** `λ c = 1 − 2[F c] − 2[F (π c)]`, i.e.
`λ c = 1 − 4[F c] + g (π c) − g c` with `g = 2·[unfilled]`. -/
theorem lam_eq (hc : ProperOff M.graph h c) :
    lam P c = 1 - 2 * filledZ M.graph h c - 2 * filledZ M.graph h (piMove P c) := by
  rcases classify hc with ⟨j, hr⟩ | ⟨i, hs⟩
  · rw [piMove_rep hr, lam_rep hr, filledZ_rep hr]
    by_cases hl : Lock2 P c j
    · obtain ⟨-, -, r', -⟩ := rot3_move hc hr hl
      rw [ite_eq_left hl, ite_eq_left hl, filledZ_rep r']; norm_num
    · obtain ⟨-, -, s', -⟩ := phiBinv_spec hc hr hl
      rw [ite_eq_right hl, ite_eq_right hl, filledZ_single s']; norm_num
  · rw [piMove_single hc hs, lam_single hc hs, filledZ_single hs]
    by_cases hm : M3Short P c i
    · obtain ⟨-, -, r', -⟩ := phiA_spec hc hs hm
      rw [ite_eq_left hm, ite_eq_left hm, filledZ_rep r']; norm_num
    · obtain ⟨-, -, s', -⟩ := tau_spec hc hs hm
      rw [ite_eq_right hm, ite_eq_right hm, filledZ_single s']; norm_num

/-- The telescoping form: `λ c = 1 − 4[F c] + g (π c) − g c` with `g d = 2·(1 − [F d])`. -/
theorem lam_eq_telescope (hc : ProperOff M.graph h c) :
    lam P c = 1 - 4 * filledZ M.graph h c + 2 * (1 - filledZ M.graph h (piMove P c)) -
      2 * (1 - filledZ M.graph h c) := by
  rw [lam_eq hc]; ring

/-! ### Sums over a `π`-invariant finite set -/

variable {S : Finset (Fin n → Fin 4)}

/-- Reindexing a sum along `π` on a `π`-invariant finite set. -/
theorem sum_comp_piMove {β : Type*} [AddCommMonoid β] (hb : Set.BijOn (piMove P) ↑S ↑S)
    (f : (Fin n → Fin 4) → β) : ∑ c ∈ S, f (piMove P c) = ∑ c ∈ S, f c :=
  Finset.sum_nbij (piMove P) (fun _ ha => hb.mapsTo ha) hb.injOn hb.surjOn (fun _ _ => rfl)

open Classical in
private lemma sum_filledZ : ∑ c ∈ S, filledZ M.graph h c = (S.filter (Target M.graph h)).card := by
  unfold filledZ
  rw [Finset.sum_boole]

open Classical in
/-- **Theorem W, counting identity.** On a finite `π`-invariant set of proper-off states,
`Σ λ = |S| − 4 F`. -/
theorem sum_lam (hS : ∀ c ∈ S, ProperOff M.graph h c) (hb : Set.BijOn (piMove P) ↑S ↑S) :
    ∑ c ∈ S, lam P c = (S.card : ℤ) - 4 * (S.filter (Target M.graph h)).card := by
  rw [Finset.sum_congr rfl fun c hc => lam_eq (P := P) (hS c hc), Finset.sum_sub_distrib,
    Finset.sum_sub_distrib, ← Finset.mul_sum, ← Finset.mul_sum,
    sum_comp_piMove hb (filledZ M.graph h), sum_filledZ]
  simp only [Finset.sum_const, nsmul_eq_mul, mul_one]
  ring

open Classical in
/-- `3 F − U = − Σ λ` on a finite `π`-invariant set of proper-off states. -/
theorem three_F_sub_U (hS : ∀ c ∈ S, ProperOff M.graph h c) (hb : Set.BijOn (piMove P) ↑S ↑S) :
    3 * ((S.filter (Target M.graph h)).card : ℤ) - (S.filter (fun c => ¬ Target M.graph h c)).card
      = - ∑ c ∈ S, lam P c := by
  rw [sum_lam hS hb]
  have e := Finset.card_filter_add_card_filter_not (s := S) (Target M.graph h)
  have e' : ((S.filter (Target M.graph h)).card : ℤ) +
      (S.filter (fun c => ¬ Target M.graph h c)).card = S.card := by exact_mod_cast e
  omega

open Fin.CommRing in
private lemma five_dvd_of_fin5 (z : ℤ) (hz : (z : Fin 5) = 0) : (5 : ℤ) ∣ z :=
  (ZMod.intCast_zmod_eq_zero_iff_dvd z 5).1 hz

open Fin.CommRing in
/-- The token sum telescopes: `Σ λ ≡ 0 (mod 5)` on a finite `π`-invariant set. -/
theorem five_dvd_sum_lam (hS : ∀ c ∈ S, ProperOff M.graph h c)
    (hb : Set.BijOn (piMove P) ↑S ↑S) : (5 : ℤ) ∣ ∑ c ∈ S, lam P c := by
  apply five_dvd_of_fin5
  have e : ∑ c ∈ S, sigma P (piMove P c) =
      ∑ c ∈ S, sigma P c + ∑ c ∈ S, (Int.cast (lam P c) : Fin 5) := by
    rw [← Finset.sum_add_distrib]
    exact Finset.sum_congr rfl fun c hc => sigma_piMove (hS c hc)
  rw [sum_comp_piMove hb (sigma P)] at e
  rw [Int.cast_sum]
  exact (add_eq_left.1 e.symm)

open Classical in
/-- `3F − U ≡ 0 (mod 5)` on a finite `π`-invariant set of proper-off states. -/
theorem three_F_sub_U_mod5 (hS : ∀ c ∈ S, ProperOff M.graph h c)
    (hb : Set.BijOn (piMove P) ↑S ↑S) :
    (5 : ℤ) ∣ 3 * ((S.filter (Target M.graph h)).card : ℤ) -
      (S.filter (fun c => ¬ Target M.graph h c)).card := by
  rw [three_F_sub_U hS hb]
  exact (five_dvd_sum_lam hS hb).neg_right

variable (P S) in
/-- The total winding `(Σ λ)/5` of a `π`-invariant set (the sum of the windings of its
`π`-cycles). -/
noncomputable def windingSum : ℤ := (∑ c ∈ S, lam P c) / 5

theorem five_mul_windingSum (hS : ∀ c ∈ S, ProperOff M.graph h c)
    (hb : Set.BijOn (piMove P) ↑S ↑S) : 5 * windingSum P S = ∑ c ∈ S, lam P c :=
  Int.mul_ediv_cancel' (five_dvd_sum_lam hS hb)

open Classical in
/-- **Theorem W (counting).** `3F − U = −5·w`, `w` the total winding. -/
theorem three_F_sub_U_winding (hS : ∀ c ∈ S, ProperOff M.graph h c)
    (hb : Set.BijOn (piMove P) ↑S ↑S) :
    3 * ((S.filter (Target M.graph h)).card : ℤ) - (S.filter (fun c => ¬ Target M.graph h c)).card
      = -5 * windingSum P S := by
  rw [three_F_sub_U hS hb, ← five_mul_windingSum hS hb]; ring

/-! ### Kempe classes -/

/-- Kempe steps preserve properness off the hole. -/
theorem properOff_of_kempeEquiv {c₀ d : Fin n → Fin 4} (h₀ : ProperOff M.graph h c₀)
    (he : KempeEquiv (G := M.graph) (h := h) c₀ d) : ProperOff M.graph h d := by
  induction he with
  | refl => exact h₀
  | tail _ st ih =>
    obtain ⟨a, b, T, -, hW, rfl⟩ := st
    exact properOff_swap M.graph ih hW

variable (M h) in
open Classical in
/-- The Kempe class of `c₀` among proper-off states, as a finset. -/
noncomputable def kclass (c₀ : Fin n → Fin 4) : Finset (Fin n → Fin 4) :=
  Finset.univ.filter fun d => ProperOff M.graph h d ∧ KempeEquiv (G := M.graph) (h := h) c₀ d

open Classical in
theorem kclass_properOff (c₀ : Fin n → Fin 4) :
    ∀ c ∈ kclass M h c₀, ProperOff M.graph h c :=
  fun c hc => by
    unfold kclass at hc
    exact (Finset.mem_filter.1 hc).2.1

open Classical in
theorem kclass_bijOn (c₀ : Fin n → Fin 4) :
    Set.BijOn (piMove P) ↑(kclass M h c₀) ↑(kclass M h c₀) := by
  have e : (↑(kclass M h c₀) : Set (Fin n → Fin 4)) =
      {d | ProperOff M.graph h d ∧ KempeEquiv (G := M.graph) (h := h) c₀ d} := by
    ext d; unfold kclass; simp
  rw [e]
  exact piMove_bijOn_class c₀

open Classical in
/-- `3F − U = −Σ λ` on a Kempe class. -/
theorem three_F_sub_U_class (c₀ : Fin n → Fin 4) :
    3 * (((kclass M h c₀).filter (Target M.graph h)).card : ℤ) -
      ((kclass M h c₀).filter (fun c => ¬ Target M.graph h c)).card
      = - ∑ c ∈ kclass M h c₀, lam P c :=
  three_F_sub_U (kclass_properOff c₀) (kclass_bijOn c₀)

include P in
open Classical in
/-- `3F − U ≡ 0 (mod 5)` on a Kempe class. -/
theorem three_F_sub_U_mod5_class (c₀ : Fin n → Fin 4) :
    (5 : ℤ) ∣ 3 * (((kclass M h c₀).filter (Target M.graph h)).card : ℤ) -
      ((kclass M h c₀).filter (fun c => ¬ Target M.graph h c)).card :=
  three_F_sub_U_mod5 (P := P) (kclass_properOff c₀) (kclass_bijOn c₀)

open Classical in
/-- `3F − U = −5·w` on a Kempe class. -/
theorem three_F_sub_U_winding_class (c₀ : Fin n → Fin 4) :
    3 * (((kclass M h c₀).filter (Target M.graph h)).card : ℤ) -
      ((kclass M h c₀).filter (fun c => ¬ Target M.graph h c)).card
      = -5 * windingSum P (kclass M h c₀) :=
  three_F_sub_U_winding (kclass_properOff c₀) (kclass_bijOn c₀)

open Classical in
private lemma card_class {c₀ : Fin n → Fin 4} (h₀ : ProperOff M.graph h c₀) :
    Nat.card {c : Fin n → Fin 4 // KempeEquiv (G := M.graph) (h := h) c₀ c} =
      (kclass M h c₀).card := by
  rw [Nat.card_eq_fintype_card, Fintype.card_subtype]
  unfold kclass
  congr 1
  exact Finset.filter_congr fun d _ =>
    ⟨fun he => ⟨properOff_of_kempeEquiv h₀ he, he⟩, fun hd => hd.2⟩

open Classical in
private lemma card_class_filled {c₀ : Fin n → Fin 4} (h₀ : ProperOff M.graph h c₀) :
    Nat.card {c : Fin n → Fin 4 // KempeEquiv (G := M.graph) (h := h) c₀ c ∧ Target M.graph h c} =
      ((kclass M h c₀).filter (Target M.graph h)).card := by
  rw [Nat.card_eq_fintype_card, Fintype.card_subtype]
  unfold kclass
  rw [Finset.filter_filter]
  congr 1
  exact Finset.filter_congr fun d _ =>
    ⟨fun he => ⟨⟨properOff_of_kempeEquiv h₀ he.1, he.1⟩, he.2⟩, fun hd => ⟨hd.1.2, hd.2⟩⟩

variable (P) in
/-- **The quarter floor in winding form.** On a sphere with a pentagonal hole, every Kempe class
is at least a quarter filled iff `Σ λ ≤ 0` over every class (equivalently `3F − U ≥ 0`, or
total winding `≤ 0`). -/
theorem quarterFloor_iff_lam :
    QuarterFloorConj (G := M.graph) (h := h) ↔
      ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ → ∑ c ∈ kclass M h c₀, lam P c ≤ 0 := by
  classical
  refine forall_congr' fun c₀ => forall_congr' fun h₀ => ?_
  rw [card_class h₀, card_class_filled h₀,
    sum_lam (kclass_properOff c₀) (kclass_bijOn c₀)]
  constructor
  · intro hq
    have : ((kclass M h c₀).card : ℤ) ≤ 4 * ((kclass M h c₀).filter (Target M.graph h)).card := by
      exact_mod_cast hq
    omega
  · intro hq
    have : ((kclass M h c₀).card : ℤ) ≤ 4 * ((kclass M h c₀).filter (Target M.graph h)).card := by
      omega
    exact_mod_cast this

end sphere

end SimpleGraph.QuarterFloor

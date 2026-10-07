/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterWindow

/-!
# Two colourings on one hole: `L = 20` `Γ`-cycles (`NightA34Two.md` §1–§3)

## 1. Colour renaming (general)

`recol τ c = τ ∘ c` for a permutation `τ` of the four colours. It preserves `ProperOff`,
`RepeatAt`, `SingletonAt`, `Target`, both locks, `DoublyLocked`, `DLState`, `M2Short`,
`M3Short` and `J` (`JoinYZ`), maps two-colour graphs to two-colour graphs
(`pairGraph_recol`), and every Kempe swap is equivariant (`swap_recol`, `kswap_recol`).
Hence **`piMove_perm`**: `π (τ ∘ c) = τ ∘ π c` on proper-off states, and `piMove_iter_perm`.

## 2. The two-period setting

`s` is an `R3k4` state at a `Hole6` with an all-`DL` forward `π`-orbit (the setting of
`gamma_period_ten`), and `π^[20] s = ρ ∘ s` for a colour permutation `ρ`.

* `rho_frame` (**`rho_eq_sigma_sq_on_ring`**): in the frame of any state `s n` (repeat index
  `j`), `ρ (frm ℓ) = frm (σ (σ ℓ))`, i.e. `ρ` is `σ²` read in letters; in particular on every
  hole vertex (`x (q+t)`, `w (q+t)`, `m`) at `s n` with letter `ℓ`, `ρ` gives the colour of
  letter `σ² ℓ` (`rho_eq_sigma_sq_on_ring`, via `period_colour_rotation`). `rho_cube`:
  `ρ ^ 3 = 1`; `rho_inv_frame`: `ρ⁻¹ (frm ℓ) = frm (σ ℓ)`, so the period rotation of the note
  (called `ρ` there) is `ρ⁻¹` here.

## 3. The exchange pair

Since the note's period rotation is `ρ⁻¹` here, the note's `G = ρ_note⁻¹ ∘ π¹⁰` is
`Gmap u = ρ ∘ π^[10] u` and `d = Gmap s`.

* **`G_swaps`**: `Gmap s = d` and `Gmap d = s` (from `π^[20] s = ρ s`, equivariance and
  `ρ³ = 1`).
* `G_iter`: `Gmap (s n) = π^[n] d`; `d_setting`: `d` is again in the setting (proper-off,
  all-`DL`, `RepeatAt d j₀`, `TypeR3 d j₀`).
* **`ring_agree`**: for every `n`, `s n` and `Gmap (s n) = π^[n] d` agree on all eleven hole
  vertices.

## 4. `A₃₄′` in exchange-pair form

`Break u := ¬ J (π^[9] u)`. **`A34_two_iff`** (triangulated): on this cycle,
"no two consecutive `k = 4` failures" (`∀ b, ¬ (K4Fail (s (10b+10)) ∧ K4Fail (s (10b+20)))`)
iff `¬ (Break s ∧ Break d)`. This uses `k4_failure_iff_break` and the invariance of `J` under
`recol`.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-! ### 1. Colour renaming -/

/-- Rename the colours of `c` by `τ`. -/
def recol {V : Type*} (τ : Equiv.Perm (Fin 4)) (c : V → Fin 4) : V → Fin 4 := fun v => τ (c v)

section generic
variable {V : Type*} {G : SimpleGraph V} {h : V}

@[simp] lemma recol_apply (τ : Equiv.Perm (Fin 4)) (c : V → Fin 4) (v : V) :
    recol τ c v = τ (c v) := rfl

lemma recol_recol (τ τ' : Equiv.Perm (Fin 4)) (c : V → Fin 4) :
    recol τ (recol τ' c) = recol (τ * τ') c := rfl

lemma recol_one (c : V → Fin 4) : recol 1 c = c := rfl

lemma recol_inv_recol (τ : Equiv.Perm (Fin 4)) (c : V → Fin 4) : recol τ⁻¹ (recol τ c) = c := by
  funext v; simp

lemma recol_recol_inv (τ : Equiv.Perm (Fin 4)) (c : V → Fin 4) : recol τ (recol τ⁻¹ c) = c := by
  funext v; simp

lemma properOff_recol (τ : Equiv.Perm (Fin 4)) {c : V → Fin 4} :
    ProperOff G h (recol τ c) ↔ ProperOff G h c := by
  unfold ProperOff
  simp only [recol_apply, ne_eq, EmbeddingLike.apply_eq_iff_eq]

lemma active_recol (τ : Equiv.Perm (Fin 4)) (c : V → Fin 4) (a b : Fin 4) (v : V) :
    Active h (recol τ c) (τ a) (τ b) v ↔ Active h c a b v := by
  unfold Active
  simp only [recol_apply, EmbeddingLike.apply_eq_iff_eq]

/-- A colour renaming maps the `{a, b}`-graph to the `{τ a, τ b}`-graph. -/
lemma pairGraph_recol (τ : Equiv.Perm (Fin 4)) (c : V → Fin 4) (a b : Fin 4) :
    pairGraph G h (recol τ c) (τ a) (τ b) = pairGraph G h c a b := by
  ext u v
  show (G.Adj u v ∧ Active h (recol τ c) (τ a) (τ b) u ∧ Active h (recol τ c) (τ a) (τ b) v) ↔
    (G.Adj u v ∧ Active h c a b u ∧ Active h c a b v)
  rw [active_recol, active_recol]

/-- **A Kempe swap is equivariant under colour renaming.** -/
lemma swap_recol (τ : Equiv.Perm (Fin 4)) (c : V → Fin 4) (a b : Fin 4) (S : Set V) :
    swap (recol τ c) (τ a) (τ b) S = recol τ (swap c a b S) := by
  classical
  funext v
  by_cases hv : v ∈ S
  · rw [swap_in hv, recol_apply, recol_apply, swap_in hv, Equiv.swap_apply_apply]
    simp
  · rw [swap_out hv, recol_apply, recol_apply, swap_out hv]

lemma kswap_recol (τ : Equiv.Perm (Fin 4)) (c : V → Fin 4) (a b : Fin 4) (s : V) :
    kswap G h (recol τ c) (τ a) (τ b) s = recol τ (kswap G h c a b s) := by
  unfold kswap
  rw [pairGraph_recol, swap_recol]

variable (P : Pent G h) (τ : Equiv.Perm (Fin 4)) (c : V → Fin 4)

lemma repeatAt_recol (j : Fin 5) : RepeatAt P (recol τ c) j ↔ RepeatAt P c j := by
  unfold RepeatAt
  simp only [recol_apply, ne_eq, EmbeddingLike.apply_eq_iff_eq]

lemma lock1_recol (j : Fin 5) : Lock1 P (recol τ c) j ↔ Lock1 P c j := by
  unfold Lock1
  rw [recol_apply, recol_apply, pairGraph_recol]

lemma lock2_recol (j : Fin 5) : Lock2 P (recol τ c) j ↔ Lock2 P c j := by
  unfold Lock2
  rw [recol_apply, recol_apply, pairGraph_recol]

lemma doublyLocked_recol (j : Fin 5) : DoublyLocked P (recol τ c) j ↔ DoublyLocked P c j := by
  unfold DoublyLocked
  rw [repeatAt_recol, lock1_recol, lock2_recol]

lemma target_recol : Target G h (recol τ c) ↔ Target G h c := by
  constructor
  · rintro ⟨x, hx⟩
    refine ⟨τ⁻¹ x, fun v hv e => hx hv ?_⟩
    rw [recol_apply, e]; simp
  · rintro ⟨x, hx⟩
    refine ⟨τ x, fun v hv e => hx hv ?_⟩
    rw [recol_apply] at e
    exact τ.injective e

lemma singletonAt_recol (i : Fin 5) : SingletonAt P (recol τ c) i ↔ SingletonAt P c i := by
  unfold SingletonAt
  rw [target_recol]
  simp only [recol_apply, ne_eq, EmbeddingLike.apply_eq_iff_eq]

lemma fourth_perm {a b d : Fin 4} (hab : a ≠ b) (had : a ≠ d) (hbd : b ≠ d) :
    fourth (τ a) (τ b) (τ d) = τ (fourth a b d) := by
  obtain ⟨n1, n2, n3⟩ := fourth_ne hab had hbd
  exact fourth_eq (τ.injective.ne hab) (τ.injective.ne had) (τ.injective.ne hbd)
    (τ.injective.ne n1) (τ.injective.ne n2) (τ.injective.ne n3)

variable {P c}

lemma zcol_recol (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i) :
    zcol P (recol τ c) i = τ (zcol P c i) := by
  unfold zcol
  simp only [recol_apply]
  refine fourth_perm τ ?_ ?_ ?_
  · exact link_ne hc i (i + 1) rfl
  · exact (hs.2 (i + 2) (fin5_ne0 (by decide)).symm).symm
  · exact link_ne hc (i + 1) (i + 2) (by abel)

lemma m3Short_recol (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i) :
    M3Short P (recol τ c) i ↔ M3Short P c i := by
  unfold M3Short
  rw [zcol_recol τ hc hs, recol_apply, pairGraph_recol]

lemma m2Short_recol (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i) :
    M2Short P (recol τ c) i ↔ M2Short P c i := by
  unfold M2Short
  rw [zcol_recol τ hc hs, recol_apply, pairGraph_recol]

variable (P c)

lemma rot3_recol (j : Fin 5) : rot3 P (recol τ c) j = recol τ (rot3 P c j) := by
  unfold rot3
  simp only [recol_apply]
  rw [pairGraph_recol, swap_recol]

lemma rot2_recol (j : Fin 5) : rot2 P (recol τ c) j = recol τ (rot2 P c j) := by
  unfold rot2
  simp only [recol_apply]
  rw [pairGraph_recol, swap_recol]

lemma phiBinv_recol (j : Fin 5) : phiBinv P (recol τ c) j = recol τ (phiBinv P c j) := by
  unfold phiBinv
  simp only [recol_apply]
  rw [kswap_recol]

lemma phiAinv_recol (j : Fin 5) : phiAinv P (recol τ c) j = recol τ (phiAinv P c j) := by
  unfold phiAinv
  simp only [recol_apply]
  rw [kswap_recol]

lemma tau_recol (i : Fin 5) : tau P (recol τ c) i = recol τ (tau P c i) := by
  unfold tau
  simp only [recol_apply]
  rw [kswap_recol]

lemma tauInv_recol (i : Fin 5) : tauInv P (recol τ c) i = recol τ (tauInv P c i) := by
  unfold tauInv
  simp only [recol_apply]
  rw [kswap_recol]

variable {P c}

lemma phiA_recol (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i) :
    phiA P (recol τ c) i = recol τ (phiA P c i) := by
  unfold phiA
  rw [zcol_recol τ hc hs, recol_apply, kswap_recol]

lemma phiB_recol (hc : ProperOff G h c) {i : Fin 5} (hs : SingletonAt P c i) :
    phiB P (recol τ c) i = recol τ (phiB P c i) := by
  unfold phiB
  rw [zcol_recol τ hc hs, recol_apply, kswap_recol]

/-- **`π` commutes with colour renaming** on proper-off states: every `π`-move is a Kempe swap
named by colour roles, and Kempe swaps are equivariant (`swap_recol`). -/
theorem piMove_perm (hc : ProperOff G h c) : piMove P (recol τ c) = recol τ (piMove P c) := by
  have hc' : ProperOff G h (recol τ c) := (properOff_recol τ).2 hc
  rcases classify (P := P) hc with ⟨j, hr⟩ | ⟨i, hs⟩
  · have hr' := (repeatAt_recol P τ c j).2 hr
    rw [piMove_rep hr', piMove_rep hr]
    by_cases hl : Lock2 P c j
    · rw [ite_eq_left ((lock2_recol P τ c j).2 hl), ite_eq_left hl, rot3_recol]
    · rw [ite_eq_right (fun x => hl ((lock2_recol P τ c j).1 x)), ite_eq_right hl, phiBinv_recol]
  · have hs' := (singletonAt_recol P τ c i).2 hs
    rw [piMove_single hc' hs', piMove_single hc hs]
    by_cases hm : M3Short P c i
    · rw [ite_eq_left ((m3Short_recol τ hc hs).2 hm), ite_eq_left hm, phiA_recol τ hc hs]
    · rw [ite_eq_right (fun x => hm ((m3Short_recol τ hc hs).1 x)), ite_eq_right hm, tau_recol]

/-- `π⁻¹` commutes with colour renaming as well. -/
theorem piInv_perm (hc : ProperOff G h c) : piInv P (recol τ c) = recol τ (piInv P c) := by
  have hc' : ProperOff G h (recol τ c) := (properOff_recol τ).2 hc
  rcases classify (P := P) hc with ⟨j, hr⟩ | ⟨i, hs⟩
  · have hr' := (repeatAt_recol P τ c j).2 hr
    rw [piInv_rep hr', piInv_rep hr]
    by_cases hl : Lock1 P c j
    · rw [ite_eq_left ((lock1_recol P τ c j).2 hl), ite_eq_left hl, rot2_recol]
    · rw [ite_eq_right (fun x => hl ((lock1_recol P τ c j).1 x)), ite_eq_right hl, phiAinv_recol]
  · have hs' := (singletonAt_recol P τ c i).2 hs
    rw [piInv_single hc' hs', piInv_single hc hs]
    by_cases hm : M2Short P c i
    · rw [ite_eq_left ((m2Short_recol τ hc hs).2 hm), ite_eq_left hm, phiB_recol τ hc hs]
    · rw [ite_eq_right (fun x => hm ((m2Short_recol τ hc hs).1 x)), ite_eq_right hm, tauInv_recol]

/-- `J` is invariant under colour renaming. -/
lemma joinYZ_recol (w : Fin 5 → V) (q : Fin 5) (c : V → Fin 4) :
    JoinYZ G h w q (recol τ c) ↔ JoinYZ G h w q c := by
  unfold JoinYZ
  rw [recol_apply, recol_apply, pairGraph_recol]

end generic

/-! ### 2. The two-period setting on a `Hole6` -/

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}
variable {P : Pent M.graph h} {w : Fin 5 → Fin n} {m : Fin n} {q : Fin 5}

lemma dlState_recol (τ : Equiv.Perm (Fin 4)) (c : Fin n → Fin 4) :
    DLState P (recol τ c) ↔ DLState P c := by
  unfold DLState
  simp only [doublyLocked_recol]

lemma typeR3_recol (τ : Equiv.Perm (Fin 4)) (c : Fin n → Fin 4) (j : Fin 5) :
    TypeR3 P w (recol τ c) j ↔ TypeR3 P w c j := by
  unfold TypeR3
  simp only [recol_apply, EmbeddingLike.apply_eq_iff_eq]

/-- Iterates of `π` commute with colour renaming. -/
theorem piMove_iter_perm (τ : Equiv.Perm (Fin 4)) {c : Fin n → Fin 4}
    (hc : ProperOff M.graph h c) (k : ℕ) :
    (piMove P)^[k] (recol τ c) = recol τ ((piMove P)^[k] c) := by
  induction k with
  | zero => rfl
  | succ k ih =>
    rw [Function.iterate_succ_apply', Function.iterate_succ_apply', ih,
      piMove_perm τ (iter_proper hc k)]

lemma frm_recol (τ : Equiv.Perm (Fin 4)) (c : Fin n → Fin 4) (j : Fin 5) (a : Fin 4) :
    frm P (recol τ c) j a = τ (frm P c j a) := by
  fin_cases a <;> rfl

/-- At a repeat state the frame `![α, μ, A, B]` shows all four colours. -/
lemma frm_surj {c : Fin n → Fin 4} {j : Fin 5} (hr : RepeatAt P c j) (x : Fin 4) :
    ∃ a, frm P c j a = x := by
  obtain ⟨-, h1, h3, h4, h13, h14, h34⟩ := hr
  by_contra hne
  push Not at hne
  exact fin4_five h1.symm h3.symm h4.symm h13 h14 h34 (fun e => hne 0 e.symm)
    (fun e => hne 1 e.symm) (fun e => hne 2 e.symm) (fun e => hne 3 e.symm)

variable (P) in
/-- The exchange map `G u = ρ ∘ π^[10] u` (the note's `ρ_note⁻¹ ∘ π¹⁰`, `ρ_note = ρ⁻¹`). -/
noncomputable def Gmap (ρ : Equiv.Perm (Fin 4)) (u : Fin n → Fin 4) : Fin n → Fin 4 :=
  recol ρ ((piMove P)^[10] u)

/-- A hole vertex: `x (q+t)`, `w (q+t)` or `m`. -/
def HoleV (P : Pent M.graph h) (w : Fin 5 → Fin n) (m : Fin n) (q : Fin 5) (v : Fin n) : Prop :=
  (∃ t, v = P.x (q + t)) ∨ (∃ t, v = w (q + t)) ∨ v = m

section setting
variable {s : Fin n → Fin 4} {j₀ : Fin 5} {ρ : Equiv.Perm (Fin 4)}

/-- `π^[k + 20] s = ρ ∘ π^[k] s`. -/
theorem orbit_shift20 (hc : ProperOff M.graph h s) (hρ : (piMove P)^[20] s = recol ρ s)
    (k : ℕ) : (piMove P)^[k + 20] s = recol ρ ((piMove P)^[k] s) := by
  rw [Function.iterate_add_apply, hρ, piMove_iter_perm ρ hc]

/-- **`ρ` is `σ²` in letters**: in the frame of any state `s k` of the orbit,
`ρ (frm ℓ) = frm (σ (σ ℓ))`. -/
theorem rho_frame (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hρ : (piMove P)^[20] s = recol ρ s) (k : ℕ) {j : Fin 5}
    (hj : RepeatAt P ((piMove P)^[k] s) j) (a : Fin 4) :
    ρ (frm P ((piMove P)^[k] s) j a) = frm P ((piMove P)^[k] s) j (sig (sig a)) := by
  have hj' : RepeatAt P ((piMove P)^[k + 20] s) j := by
    rw [orbit_shift20 hc hρ, repeatAt_recol]; exact hj
  have fi := frm_iter hc hall k hj 20 j hj' a
  rw [orbit_shift20 hc hρ, frm_recol] at fi
  rw [fi, sig_iter_mod]
  rfl

/-- `ρ³ = 1` (`σ` has order three). -/
theorem rho_cube (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hρ : (piMove P)^[20] s = recol ρ s) : ρ ^ 3 = 1 := by
  obtain ⟨j, hd⟩ := hall 0
  refine Equiv.ext fun x => ?_
  obtain ⟨a, rfl⟩ := frm_surj hd.1 x
  simp only [pow_succ, pow_zero, one_mul, Equiv.Perm.mul_apply, Equiv.Perm.one_apply]
  rw [rho_frame hc hall hρ 0 hd.1, rho_frame hc hall hρ 0 hd.1, rho_frame hc hall hρ 0 hd.1]
  congr 1
  revert a; decide

/-- `ρ⁻¹` is `σ` in letters: the period rotation of `NightA34Two.md` is `ρ⁻¹`. -/
theorem rho_inv_frame (hc : ProperOff M.graph h s) (hall : ∀ n, DLState P ((piMove P)^[n] s))
    (hρ : (piMove P)^[20] s = recol ρ s) (k : ℕ) {j : Fin 5}
    (hj : RepeatAt P ((piMove P)^[k] s) j) (a : Fin 4) :
    ρ⁻¹ (frm P ((piMove P)^[k] s) j a) = frm P ((piMove P)^[k] s) j (sig a) := by
  apply ρ.injective
  rw [rho_frame hc hall hρ k hj, show sig (sig (sig a)) = a by revert a; decide]
  simp

variable (htri : M.Triangulated) (H : Hole6 P w m q) (hc : ProperOff M.graph h s)
  (hall : ∀ n, DLState P ((piMove P)^[n] s)) (hr : RepeatAt P s j₀) (hq : q = j₀ + 4)
  (hT : TypeR3 P w s j₀) (hρ : (piMove P)^[20] s = recol ρ s)

include H hc hall hr hq hT in
lemma hole_letter (N : ℕ) (hN : 0 < N) {j : Fin 5} (hj : RepeatAt P ((piMove P)^[N] s) j)
    {v : Fin n} (hv : HoleV P w m q v) :
    ∃ ℓ, (piMove P)^[N] s v = frm P ((piMove P)^[N] s) j ℓ ∧
      (piMove P)^[N + 10] s v = frm P ((piMove P)^[N] s) j (sig ℓ) := by
  obtain ⟨px, pw, pm⟩ := period_colour_rotation H hc hall hr hq hT N hN hj
  rcases hv with ⟨t, rfl⟩ | ⟨t, rfl⟩ | rfl
  · exact ⟨_, (px t).1, (px t).2⟩
  · exact ⟨_, (pw t).1, (pw t).2⟩
  · exact ⟨_, pm.1, pm.2⟩

include H hc hall hr hq hT hρ in
/-- **`ρ = σ²` on the ring** (from `period_colour_rotation`): at `s N`, `N > 0`, every hole
vertex with letter `ℓ` has letter `σ ℓ` at `s (N + 10)`, `ρ` sends its colour to the colour of
letter `σ² ℓ`, and `ρ⁻¹` sends its colour to its colour at `s (N + 10)`. -/
theorem rho_eq_sigma_sq_on_ring (N : ℕ) (hN : 0 < N) {j : Fin 5}
    (hj : RepeatAt P ((piMove P)^[N] s) j) {v : Fin n} (hv : HoleV P w m q v) :
    ∃ ℓ, (piMove P)^[N] s v = frm P ((piMove P)^[N] s) j ℓ ∧
      (piMove P)^[N + 10] s v = frm P ((piMove P)^[N] s) j (sig ℓ) ∧
      ρ ((piMove P)^[N] s v) = frm P ((piMove P)^[N] s) j (sig (sig ℓ)) ∧
      ρ⁻¹ ((piMove P)^[N] s v) = (piMove P)^[N + 10] s v := by
  obtain ⟨ℓ, e0, e1⟩ := hole_letter H hc hall hr hq hT N hN hj hv
  refine ⟨ℓ, e0, e1, ?_, ?_⟩
  · rw [e0, rho_frame hc hall hρ N hj]
  · rw [e0, e1, rho_inv_frame hc hall hρ N hj]

include H hc hall hr hq hT hρ in
/-- On the hole, `ρ ∘ s (k + 10) = s k` for every `k`. -/
theorem period_step_hole (k : ℕ) {v : Fin n} (hv : HoleV P w m q v) :
    ρ ((piMove P)^[k + 10] s v) = (piMove P)^[k] s v := by
  obtain ⟨j, hd⟩ := hall (k + 10)
  obtain ⟨ℓ, e0, e1, -, -⟩ :=
    rho_eq_sigma_sq_on_ring H hc hall hr hq hT hρ (k + 10) (by omega) hd.1 hv
  rw [show k + 10 + 10 = k + 20 by omega, orbit_shift20 hc hρ, recol_apply] at e1
  have e2 : (piMove P)^[k] s v = ρ⁻¹ (frm P ((piMove P)^[k + 10] s) j (sig ℓ)) := by
    rw [← e1]; simp
  rw [e2, rho_inv_frame hc hall hρ (k + 10) hd.1, e0, rho_frame hc hall hρ (k + 10) hd.1]

/-! ### 3. The exchange pair -/

include hc hall hρ in
/-- **`G` swaps `s` and `d = G s`.** -/
theorem G_swaps : Gmap P ρ s = Gmap P ρ s ∧ Gmap P ρ (Gmap P ρ s) = s := by
  refine ⟨rfl, ?_⟩
  unfold Gmap
  rw [piMove_iter_perm ρ (iter_proper hc 10), ← Function.iterate_add_apply, hρ, recol_recol,
    recol_recol, ← pow_two, ← pow_succ, rho_cube hc hall hρ, recol_one]

include hc in
/-- `G (s k) = π^[k] d`: the run from `d` is `G` of the run from `s`. -/
theorem G_iter (k : ℕ) : Gmap P ρ ((piMove P)^[k] s) = (piMove P)^[k] (Gmap P ρ s) := by
  unfold Gmap
  rw [piMove_iter_perm ρ (iter_proper hc 10), ← Function.iterate_add_apply,
    ← Function.iterate_add_apply, add_comm]

include H hc hall hr hq hT in
/-- `d = G s` is again in the setting: proper-off, all-`DL`, an `R3k4` state at `j₀`. -/
theorem d_setting :
    ProperOff M.graph h (Gmap P ρ s) ∧ (∀ k, DLState P ((piMove P)^[k] (Gmap P ρ s))) ∧
      RepeatAt P (Gmap P ρ s) j₀ ∧ TypeR3 P w (Gmap P ρ s) j₀ := by
  obtain ⟨tk, -⟩ := gamma_period_ten (m := m) H hc hall hr hq hT
  obtain ⟨j, hd, hq', hT'⟩ := tk 10
  have g : gseq 10 = (.R3, 4) := rfl
  rw [g] at hq' hT'
  have ej : j = j₀ := add_right_cancel (hq'.symm.trans hq)
  subst ej
  refine ⟨(properOff_recol ρ).2 (iter_proper hc 10), fun k => ?_,
    (repeatAt_recol P ρ _ j).2 hd.1, (typeR3_recol ρ _ j).2 hT'⟩
  rw [← G_iter hc, Gmap, ← Function.iterate_add_apply]
  exact (dlState_recol ρ _).2 (hall _)

include H hc hall hr hq hT hρ in
/-- **Ring agreement.** For every `k`, `s k` and `d k = G (s k) = π^[k] d` agree on all eleven
hole vertices `x (q+t)`, `w (q+t)`, `m`. -/
theorem ring_agree (k : ℕ) {v : Fin n} (hv : HoleV P w m q v) :
    Gmap P ρ ((piMove P)^[k] s) v = (piMove P)^[k] s v ∧
      (piMove P)^[k] (Gmap P ρ s) v = (piMove P)^[k] s v := by
  have e : Gmap P ρ ((piMove P)^[k] s) v = (piMove P)^[k] s v := by
    unfold Gmap
    rw [recol_apply, ← Function.iterate_add_apply, add_comm]
    exact period_step_hole H hc hall hr hq hT hρ k hv
  exact ⟨e, by rw [← G_iter hc]; exact e⟩

/-! ### 4. `A₃₄′` in exchange-pair form -/

variable (P q) in
/-- A `k = 4` failure at an `R3k4` state `u`: the `σ`-exit is not lockless. -/
def K4Fail (u : Fin n → Fin 4) : Prop :=
  ∃ j, DoublyLocked P u j ∧ q = j + 4 ∧ ¬ NoLock P (sigSwap P u j)

variable (P w q) in
/-- The run from `u` breaks `J` at step `8`: `J` fails at `π^[9] u`. -/
def Break (u : Fin n → Fin 4) : Prop := ¬ JoinYZ M.graph h w q ((piMove P)^[9] u)

include htri H hc hall hr hq hT in
lemma k4Fail_iff (b : ℕ) :
    K4Fail P q ((piMove P)^[10 * b + 10] s) ↔
      ¬ JoinYZ M.graph h w q ((piMove P)^[10 * b + 9] s) := by
  obtain ⟨j, hd, hq', -, e⟩ := k4_exit_period htri H hc hall hr hq hT b
  constructor
  · rintro ⟨j', hd', -, hn⟩ hJ
    rw [rep_unique hd.1 hd'.1] at hn
    exact hn (e.2 hJ)
  · intro hJ
    exact ⟨j, hd, hq', fun hN => hJ (e.1 hN)⟩

include hc hρ in
lemma J_shift (k r : ℕ) :
    JoinYZ M.graph h w q ((piMove P)^[k + 20 * r] s) ↔ JoinYZ M.graph h w q ((piMove P)^[k] s) := by
  induction r with
  | zero => rfl
  | succ r ih =>
    rw [show k + 20 * (r + 1) = k + 20 * r + 20 by ring, orbit_shift20 hc hρ, joinYZ_recol, ih]

include htri H hc hall hr hq hT hρ in
/-- **`A₃₄′` on the two-period cycle.** No two consecutive `k = 4` failures along the orbit iff
the runs from `s` and from `d = G s` do not both break `J` at step `8`. -/
theorem A34_two_iff :
    (∀ b, ¬ (K4Fail P q ((piMove P)^[10 * b + 10] s) ∧
      K4Fail P q ((piMove P)^[10 * (b + 1) + 10] s))) ↔
    ¬ (Break P w q s ∧ Break P w q (Gmap P ρ s)) := by
  have hd : Break P w q (Gmap P ρ s) ↔ ¬ JoinYZ M.graph h w q ((piMove P)^[19] s) := by
    unfold Break
    rw [← G_iter hc, Gmap, joinYZ_recol, ← Function.iterate_add_apply]
  have per : ∀ b, (JoinYZ M.graph h w q ((piMove P)^[10 * b + 9] s) ↔
      JoinYZ M.graph h w q ((piMove P)^[9 + 10 * (b % 2)] s)) := by
    intro b
    rw [show 10 * b + 9 = 9 + 10 * (b % 2) + 20 * (b / 2) by omega, J_shift hc hρ]
  rw [hd]
  simp only [k4Fail_iff htri H hc hall hr hq hT, per]
  unfold Break
  constructor
  · intro hb
    simpa using hb 0
  · intro hn b
    rcases Nat.mod_two_eq_zero_or_one b with e | e
    · rw [e, show (b + 1) % 2 = 1 by omega]
      exact hn
    · rw [e, show (b + 1) % 2 = 0 by omega]
      exact fun x => hn ⟨x.2, x.1⟩

end setting

end sphere

end SimpleGraph.QuarterFloor

#print axioms SimpleGraph.QuarterFloor.piMove_perm
#print axioms SimpleGraph.QuarterFloor.piInv_perm
#print axioms SimpleGraph.QuarterFloor.rho_eq_sigma_sq_on_ring
#print axioms SimpleGraph.QuarterFloor.rho_cube
#print axioms SimpleGraph.QuarterFloor.G_swaps
#print axioms SimpleGraph.QuarterFloor.d_setting
#print axioms SimpleGraph.QuarterFloor.ring_agree
#print axioms SimpleGraph.QuarterFloor.A34_two_iff

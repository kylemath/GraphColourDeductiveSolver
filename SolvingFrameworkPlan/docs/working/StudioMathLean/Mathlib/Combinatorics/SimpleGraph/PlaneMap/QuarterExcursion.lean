/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterSigmaGroups
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterJordanDual

/-!
# Exact excursion accounting: the credit of a `σ`-hit is the `λ`-mass of its excursion

Formalises §1 ("The landing excursion") of `NightLemmaR.md`.

Along a `π`-orbit the states fall into **excursions**: a maximal run of `u ≥ 1` unfilled states
followed by a maximal run of `f ≥ 1` filled states. Here `Excursion P e u f` says that the
excursion starts at `e` (so `π⁻¹ e` is filled), `π^k e` is unfilled for `k < u`, filled for
`u ≤ k < u + f`, and `π^(u+f) e` is unfilled. Its `λ`-mass is
`excMass P e u f = Σ_{k < u+f} λ (π^k e)`.

## Main results (sorry-free, no new axioms)

* (1) `sigSwap_repeat`, `sigSwap_sigSwap`, `sigSwap_inj'`: at **any** unfilled state
  (no ball hypothesis) `σ = sigSwap P · j` keeps the repeat index `j` and is an involution;
  hence `σ c = σ c'` forces `c = c'` and `j = j'`.
* (3) `lam_UU`, `lam_UF`, `lam_FF`, `lam_FU` (from `lam_eq`): `λ = +1, −1, −3, −1` on
  unfilled→unfilled, unfilled→filled, filled→filled, filled→unfilled steps;
  `excursion_profile` along an excursion, and `excursion_mass`: **`excMass = u − 3f`**
  (`(u − 1) − 1 − 3(f − 1) − 1`).
* (4) `noLock_prev_filled`, `noLock_next_filled`: a lockless state `s` (`NoLock`) has `π⁻¹ s`
  filled (`¬Lock1`, so `π⁻¹ = φ_A⁻¹`) and `π s` filled (`¬Lock2`, so `π = φ_B⁻¹`).
  No extra hypothesis is needed. Hence `noLock_in_excursion`: a lockless state of an excursion
  is its first state and the excursion has `u = 1`; `hit_excursion_mass`: its mass is
  `1 − 3f = −(3f − 1)`. `exists_excursion_of_noLock` / `sigma_hit_excursion`: every lockless
  state (in particular every lockless `σ`-image) does start an excursion (`π`-orbits are
  periodic, `iterate_period`). `sigma_hit_f_ge_two_k3`: at a `k = 3` `R3` state the hit
  excursion has `f ≥ 2`, so the credit `3f − 1` is at least `5`.
* (5) `no_double_hit`, `no_double_hit_sigmaLink`, `no_double_hit_ne`: two `σ`-images that are
  lockless and lie in one excursion come from the same state (with the same repeat index); in
  particular two distinct `DD` endpoints never hit one excursion.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {P : Pent M.graph h}
  {c c' d d' e s : Fin n → Fin 4} {j j' : Fin 5}

/-! ### (1) `σ` keeps the repeat index and is an involution -/

/-- `σ` keeps the repeat index (`NightLemmaR.md` §1(a)). -/
theorem sigSwap_repeat (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    RepeatAt P (sigSwap P c j) j :=
  (sigSwap_basic hc hr).2.2.1

/-- **`σ` is an involution** on unfilled states: the `{α, μ}`-component of `x (j+1)` is the
same before and after the swap. -/
theorem sigSwap_sigSwap (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) :
    sigSwap P (sigSwap P c j) j = c := by
  obtain ⟨-, -, -, s0, s1, -⟩ := sigSwap_basic hc hr
  show kswap M.graph h (sigSwap P c j) (sigSwap P c j (P.x j)) (sigSwap P c j (P.x (j + 1)))
    (P.x (j + 1)) = c
  rw [s0, s1]
  exact kswap_inv'

/-- **`σ` is injective** on unfilled states, over all repeat indices (no ball hypothesis). -/
theorem sigSwap_inj' (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (hc' : ProperOff M.graph h c') (hr' : RepeatAt P c' j')
    (E : sigSwap P c j = sigSwap P c' j') : c = c' ∧ j = j' := by
  have r1 := sigSwap_repeat hc hr
  have r2 := sigSwap_repeat hc' hr'
  rw [E] at r1
  have ej : j = j' := rep_unique r2 r1
  subst ej
  exact ⟨by rw [← sigSwap_sigSwap hc hr, E, sigSwap_sigSwap hc' hr'], rfl⟩

/-! ### Iterates of `π` -/

theorem iter_properOff (hc : ProperOff M.graph h c) :
    ∀ k : ℕ, ProperOff M.graph h ((piMove P)^[k] c)
  | 0 => hc
  | k + 1 => by
    rw [Function.iterate_succ_apply']
    exact piMove_properOff (iter_properOff hc k)

/-- Every `π`-orbit is periodic. -/
theorem iterate_period (hc : ProperOff M.graph h c) :
    ∃ m, 0 < m ∧ (piMove P)^[m] c = c := by
  classical
  have semi : ∀ (k : ℕ) (y : {c : Fin n → Fin 4 // ProperOff M.graph h c}),
      (piMove P)^[k] y.1 = ((piPerm P)^[k] y).1 := by
    intro k
    induction k with
    | zero => intro y; rfl
    | succ k ih =>
      intro y
      rw [Function.iterate_succ_apply', Function.iterate_succ_apply', ih]
      rfl
  have hfin : IsOfFinOrder (piPerm P) := isOfFinOrder_of_finite _
  refine ⟨orderOf (piPerm P), hfin.orderOf_pos, ?_⟩
  rw [semi _ ⟨c, hc⟩, ← Equiv.Perm.coe_pow, pow_orderOf_eq_one]
  rfl

/-! ### (3) The `λ` profile -/

theorem lam_UU (hc : ProperOff M.graph h c) (h1 : ¬ Target M.graph h c)
    (h2 : ¬ Target M.graph h (piMove P c)) : lam P c = 1 := by
  rw [lam_eq hc]; simp [filledZ, h1, h2]

theorem lam_UF (hc : ProperOff M.graph h c) (h1 : ¬ Target M.graph h c)
    (h2 : Target M.graph h (piMove P c)) : lam P c = -1 := by
  rw [lam_eq hc]; simp [filledZ, h1, h2]

theorem lam_FF (hc : ProperOff M.graph h c) (h1 : Target M.graph h c)
    (h2 : Target M.graph h (piMove P c)) : lam P c = -3 := by
  rw [lam_eq hc]; simp [filledZ, h1, h2]

theorem lam_FU (hc : ProperOff M.graph h c) (h1 : Target M.graph h c)
    (h2 : ¬ Target M.graph h (piMove P c)) : lam P c = -1 := by
  rw [lam_eq hc]; simp [filledZ, h1, h2]

variable (P) in
/-- An **excursion** of a `π`-orbit (`NightLemmaR.md` §1–2): starting at `e` (the previous state
`π⁻¹ e` is filled), `u ≥ 1` unfilled states `e, …, π^(u-1) e`, then `f ≥ 1` filled states
`π^u e, …, π^(u+f-1) e`, then the unfilled state `π^(u+f) e` (the start of the next excursion). -/
structure Excursion (e : Fin n → Fin 4) (u f : ℕ) : Prop where
  proper : ProperOff M.graph h e
  u_pos : 0 < u
  f_pos : 0 < f
  prev : Target M.graph h (piInv P e)
  unf : ∀ k, k < u → ¬ Target M.graph h ((piMove P)^[k] e)
  fil : ∀ k, u ≤ k → k < u + f → Target M.graph h ((piMove P)^[k] e)
  next : ¬ Target M.graph h ((piMove P)^[u + f] e)

variable (P) in
/-- The `λ`-mass of the excursion `(e, u, f)`. -/
noncomputable def excMass (e : Fin n → Fin 4) (u f : ℕ) : ℤ :=
  ∑ k ∈ Finset.range (u + f), lam P ((piMove P)^[k] e)

variable (P) in
/-- `s` is one of the `u + f` states of the excursion `(e, u, f)`. -/
def InExc (e : Fin n → Fin 4) (u f : ℕ) (s : Fin n → Fin 4) : Prop :=
  ∃ k, k < u + f ∧ (piMove P)^[k] e = s

private lemma iter_succ (k : ℕ) : piMove P ((piMove P)^[k] e) = (piMove P)^[k + 1] e :=
  (Function.iterate_succ_apply' _ _ _).symm

private lemma ex_target {u f : ℕ} (E : Excursion P e u f) (k : ℕ) (hk : k ≤ u + f) :
    (Target M.graph h ((piMove P)^[k] e) ↔ u ≤ k ∧ k < u + f) := by
  constructor
  · intro ht
    refine ⟨?_, ?_⟩
    · by_contra hl; exact E.unf k (by omega) ht
    · by_contra hl
      have : k = u + f := by omega
      subst this; exact E.next ht
  · rintro ⟨a, b⟩; exact E.fil k a b

/-- **The `λ` profile of an excursion**: `+1` on an unfilled state followed by an unfilled one,
`−1` on the last unfilled state, `−3` on a filled state followed by a filled one, `−1` on the
last filled state. -/
theorem excursion_profile {u f : ℕ} (E : Excursion P e u f) :
    (∀ k, k + 1 < u → lam P ((piMove P)^[k] e) = 1) ∧
    lam P ((piMove P)^[u - 1] e) = -1 ∧
    (∀ k, u ≤ k → k + 1 < u + f → lam P ((piMove P)^[k] e) = -3) ∧
    lam P ((piMove P)^[u + f - 1] e) = -1 := by
  have hp := iter_properOff (P := P) E.proper
  have u1 := E.u_pos
  have f1 := E.f_pos
  refine ⟨fun k hk => ?_, ?_, fun k hk hk' => ?_, ?_⟩
  · refine lam_UU (hp k) ?_ ?_
    · exact E.unf k (by omega)
    · rw [iter_succ]; exact E.unf _ hk
  · refine lam_UF (hp _) (E.unf _ (by omega)) ?_
    rw [iter_succ]; exact E.fil _ (by omega) (by omega)
  · refine lam_FF (hp k) (E.fil k hk (by omega)) ?_
    rw [iter_succ]; exact E.fil _ (by omega) hk'
  · refine lam_FU (hp _) (E.fil _ (by omega) (by omega)) ?_
    rw [iter_succ]
    have : u + f - 1 + 1 = u + f := by omega
    rw [this]; exact E.next

/-- **The mass of an excursion** (`NightLemmaR.md` §2):
`Σ λ = (u − 1) − 1 − 3(f − 1) − 1 = u − 3f`. -/
theorem excursion_mass {u f : ℕ} (E : Excursion P e u f) :
    excMass P e u f = (u : ℤ) - 3 * f := by
  have hp := iter_properOff (P := P) E.proper
  set F : ℕ → ℤ := fun k => filledZ M.graph h ((piMove P)^[k] e) with hF
  have key : ∀ L, ∑ k ∈ Finset.range L, F (k + 1) =
      ∑ k ∈ Finset.range L, F k - F 0 + F L := by
    intro L
    induction L with
    | zero => simp
    | succ L ih => rw [Finset.sum_range_succ, Finset.sum_range_succ, ih]; ring
  have F0 : F 0 = 0 := by
    simp only [hF, filledZ, Function.iterate_zero, id]
    exact ite_eq_right (E.unf 0 E.u_pos)
  have FL : F (u + f) = 0 := by simp only [hF, filledZ]; exact ite_eq_right E.next
  have Fsum : ∑ k ∈ Finset.range (u + f), F k = f := by
    rw [Finset.sum_range_add]
    have a : ∑ k ∈ Finset.range u, F k = 0 :=
      Finset.sum_eq_zero fun k hk => by
        simp only [hF, filledZ]; exact ite_eq_right (E.unf k (Finset.mem_range.1 hk))
    have b : ∑ k ∈ Finset.range f, F (u + k) = ∑ k ∈ Finset.range f, (1 : ℤ) :=
      Finset.sum_congr rfl fun k hk => by
        simp only [hF, filledZ]
        exact ite_eq_left (E.fil _ (by omega) (by have := Finset.mem_range.1 hk; omega))
    rw [a, b]; simp
  unfold excMass
  rw [Finset.sum_congr rfl fun k _ => lam_eq (P := P) (hp k)]
  have e2 : ∀ k, filledZ M.graph h (piMove P ((piMove P)^[k] e)) = F (k + 1) := by
    intro k; simp only [hF, iter_succ]
  simp only [e2]
  rw [Finset.sum_sub_distrib, Finset.sum_sub_distrib, ← Finset.mul_sum, ← Finset.mul_sum, key,
    Fsum, F0, FL]
  simp
  ring

/-! ### (4) A lockless state is the only unfilled state of its excursion -/

theorem noLock_unfilled (hN : NoLock P s) : ¬ Target M.graph h s := fun ht => noLock_filled ht hN

/-- A lockless state has a filled predecessor: `¬Lock1`, so `π⁻¹ = φ_A⁻¹` lands in `F`. -/
theorem noLock_prev_filled (hs : ProperOff M.graph h s) (hN : NoLock P s) :
    Target M.graph h (piInv P s) := by
  obtain ⟨j, hr, h1, -⟩ := hN
  rw [piInv_rep hr, ite_eq_right h1]
  exact (phiAinv_spec hs hr h1).2.2.1.1

/-- A lockless state has a filled successor: `¬Lock2`, so `π = φ_B⁻¹` lands in `F`. -/
theorem noLock_next_filled (hs : ProperOff M.graph h s) (hN : NoLock P s) :
    Target M.graph h (piMove P s) := by
  obtain ⟨j, hr, -, h2⟩ := hN
  rw [piMove_rep hr, ite_eq_right h2]
  exact (phiBinv_spec hs hr h2).2.2.1.1

/-- **A lockless state of an excursion is its first state, and the excursion has `u = 1`**
(`NightLemmaR.md` §1(b)). -/
theorem noLock_in_excursion {u f k : ℕ} (E : Excursion P e u f) (hk : k < u + f)
    (hN : NoLock P ((piMove P)^[k] e)) : k = 0 ∧ u = 1 := by
  have hp := iter_properOff (P := P) E.proper
  have hU : ¬ Target M.graph h ((piMove P)^[k] e) := noLock_unfilled hN
  have hku : k < u := by
    by_contra hl; exact hU (E.fil k (by omega) hk)
  have k0 : k = 0 := by
    rcases k with _ | k
    · rfl
    · exfalso
      have hpr := noLock_prev_filled (hp _) hN
      rw [← iter_succ, piInv_piMove (hp k)] at hpr
      exact E.unf k (by omega) hpr
  subst k0
  refine ⟨rfl, ?_⟩
  by_contra hu
  have hn := noLock_next_filled (hp 0) hN
  rw [iter_succ] at hn
  exact E.unf 1 (by have := E.u_pos; omega) hn

/-- **The hit excursion has mass `1 − 3f`**: the credit `3f − 1` is exactly `−Σλ` over it. -/
theorem hit_excursion_mass {u f k : ℕ} (E : Excursion P e u f) (hk : k < u + f)
    (hN : NoLock P ((piMove P)^[k] e)) : excMass P e u f = 1 - 3 * (f : ℤ) := by
  rw [excursion_mass E, (noLock_in_excursion E hk hN).2]; simp

/-- Every lockless state starts an excursion with `u = 1` (`π`-orbits are periodic). -/
theorem exists_excursion_of_noLock (hs : ProperOff M.graph h s) (hN : NoLock P s) :
    ∃ f, Excursion P s 1 f := by
  classical
  obtain ⟨m, hm, hper⟩ := iterate_period (P := P) hs
  have hex : ∃ k, ¬ Target M.graph h ((piMove P)^[k + 1] s) :=
    ⟨m - 1, by rw [Nat.sub_add_cancel hm, hper]; exact noLock_unfilled hN⟩
  have hf0 : Nat.find hex ≠ 0 := by
    intro e0
    have := Nat.find_spec hex
    rw [e0] at this
    exact this (noLock_next_filled hs hN)
  refine ⟨Nat.find hex, hs, Nat.one_pos, Nat.pos_of_ne_zero hf0, noLock_prev_filled hs hN,
    fun k hk => ?_, fun k hk hk' => ?_, ?_⟩
  · obtain rfl : k = 0 := by omega
    exact noLock_unfilled hN
  · obtain ⟨k', rfl⟩ : ∃ k', k = k' + 1 := ⟨k - 1, by omega⟩
    exact not_not.1 (Nat.find_min hex (by omega))
  · rw [add_comm]; exact Nat.find_spec hex

/-- **The landing excursion of a lockless `σ`-image** (`NightLemmaR.md` §1(b)–(c)): `σ c` starts
an excursion with `u = 1` and `f ≥ 1`, of mass `1 − 3f`. -/
theorem sigma_hit_excursion (hc : ProperOff M.graph h c) (hr : RepeatAt P c j)
    (hN : NoLock P (sigSwap P c j)) :
    ∃ f, Excursion P (sigSwap P c j) 1 f ∧ excMass P (sigSwap P c j) 1 f = 1 - 3 * (f : ℤ) := by
  obtain ⟨f, E⟩ := exists_excursion_of_noLock (sigSwap_basic hc hr).2.1 hN
  exact ⟨f, E, hit_excursion_mass (k := 0) E (by have := E.f_pos; omega) hN⟩

/-- At a `k = 3` `R3` state (`K3Ball`, triangulated) the excursion hit by a lockless `σ`-image
has `f ≥ 2`, so its credit `3f − 1` is at least `5`. -/
theorem sigma_hit_f_ge_two_k3 {w : Fin 5 → Fin n} {m : Fin n} (htri : M.Triangulated)
    (K : K3Ball P w m j) (hc : ProperOff M.graph h c) (hR : R3At P w c j)
    (hN : NoLock P (sigSwap P c j)) {f : ℕ} (E : Excursion P (sigSwap P c j) 1 f) :
    2 ≤ f ∧ excMass P (sigSwap P c j) 1 f ≤ -5 := by
  have h2 : 2 ≤ f := by
    by_contra hf
    have f1 : f = 1 := by have := E.f_pos; omega
    subst f1
    have := (sigma_exit_f_ge_two_k3' htri K hc hR hN).2
    exact E.next (by simpa using this)
  refine ⟨h2, ?_⟩
  rw [hit_excursion_mass (k := 0) E (by omega) hN]
  omega

/-! ### (5) No double hit -/

/-- **No double hit** (`NightLemmaR.md` §1(b)): if the lockless `σ`-images of `c` (at `j`) and of
`c'` (at `j'`) lie in one excursion, then `c = c'` and `j = j'`. -/
theorem no_double_hit {u f : ℕ} (E : Excursion P e u f)
    (hc : ProperOff M.graph h c) (hr : RepeatAt P c j) (hN : NoLock P (sigSwap P c j))
    (hc' : ProperOff M.graph h c') (hr' : RepeatAt P c' j') (hN' : NoLock P (sigSwap P c' j'))
    (hin : InExc P e u f (sigSwap P c j)) (hin' : InExc P e u f (sigSwap P c' j')) :
    c = c' ∧ j = j' := by
  obtain ⟨k, hk, hke⟩ := hin
  obtain ⟨k', hk', hke'⟩ := hin'
  have k0 := (noLock_in_excursion E hk (hke ▸ hN)).1
  have k0' := (noLock_in_excursion E hk' (hke' ▸ hN')).1
  subst k0 k0'
  exact sigSwap_inj' hc hr hc' hr' (hke.symm.trans hke')

/-- No double hit in the `sigmaLink` form of `QuarterSigmaGroups`. -/
theorem no_double_hit_sigmaLink {u f : ℕ} (E : Excursion P e u f)
    (hc : ProperOff M.graph h c) (hl : sigmaLink P c d) (hN : NoLock P d)
    (hc' : ProperOff M.graph h c') (hl' : sigmaLink P c' d') (hN' : NoLock P d')
    (hin : InExc P e u f d) (hin' : InExc P e u f d') : c = c' := by
  obtain ⟨-, j, hd, rfl⟩ := hl
  obtain ⟨-, j', hd', rfl⟩ := hl'
  exact (no_double_hit E hc hd.1 hN hc' hd'.1 hN' hin hin').1

/-- Two distinct `DD` endpoints never have lockless `σ`-images in one excursion. -/
theorem no_double_hit_ne {u f : ℕ} (E : Excursion P e u f)
    (hc : ProperOff M.graph h c) (hl : sigmaLink P c d) (hN : NoLock P d)
    (hc' : ProperOff M.graph h c') (hl' : sigmaLink P c' d') (hN' : NoLock P d')
    (hne : c ≠ c') : ¬ (InExc P e u f d ∧ InExc P e u f d') :=
  fun ⟨a, b⟩ => hne (no_double_hit_sigmaLink E hc hl hN hc' hl' hN' a b)

end sphere

end SimpleGraph.QuarterFloor

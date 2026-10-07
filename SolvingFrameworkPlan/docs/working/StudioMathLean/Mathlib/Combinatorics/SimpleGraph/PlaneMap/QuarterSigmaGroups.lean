/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterSigmaExit

/-!
# `σ`-joined groups of `π`-cycles and Conjecture `σC`

Formalises the statement of Conjecture `σC` (`NightFloorR53.md` §5; Studio Job E in
`NightLog-2026-10-06.md`). Fix a pentagonal hole `P` on a spherical map and a Kempe class
`S = kclass M h c₀`. Join two `π`-cycles of `S` whenever `σ` maps an endpoint `t` of a `DD`
step on one of them to a state on the other, where `σ t = sigSwap P t j` at the repeat index
`j` of `t`. A **`σ`-group** is a connected component of the resulting graph on `π`-cycles;
here it is realised on states as the class of the equivalence relation generated (inside `S`)
by `d = π c` and `σ`-links `c ↦ σ c`.

## Main definitions

* `piOrbit P c`: the `π`-orbit `{π^k c | k : ℕ}`; it lies in the class of `c`
  (`piOrbit_subset_kclass`), so it is finite.
* `DDstate P c j`: `c` is doubly locked at `j` and `π c` is doubly locked at `j + 3`.
* `DDEnd P c`: `c` is an endpoint of a `DD` step (`DDStep c` or `DDStep (π⁻¹ c)`).
* `sigmaLink P c d`: `c` is a `DD` endpoint, doubly locked at `j`, and `d = sigSwap P c j`.
* `sigmaGroup P c₀ c`: the `σ`-group of `c` in the class `kclass M h c₀`.
* `SigmaC P`: the `σ`-group floor at the hole `P` (a per-hole property, false in general;
  Conjecture `σC` is the claim that it holds at R5³ holes, and in the data at (5,5,5,5,6) holes).
  Restricted formal statement: `SigmaCConj` (three consecutive degree-5 link vertices).

## Main results

* `sigmaLink_mem_kclass`: `σ` is a Kempe step, so `σ`-links never leave a class (the
  restriction to `S` in `groupRel` is harmless).
* `sigmaGroup_subset_kclass`, `piOrbit_subset_sigmaGroup` (a `σ`-group is a union of
  `π`-orbits), `sigmaGroup_piInvariant` (`π` is a bijection of every `σ`-group).
* `sum_lam_sigmaGroup`: `Σ_group λ = |group| − 4·F(group)`.
* `sum_lam_class_of_groups`, `sigmaC_imp_quarterFloor`: a class is the disjoint union of its
  `σ`-groups, so `σC` implies the quarter floor.
* `dd_le_two_noLock_group`, `sigmaC_of_icoBall`: Theorem F5's charging (each `DD` step to its
  `R3` endpoint, then `σ` to a lockless state) stays inside one `σ`-group, so at an
  icosahedral hole every `σ`-group has `Σ λ ≤ 0`.

All results are sorry-free.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-! ### Definitions -/

section defs
variable (P : Pent M.graph h)

/-- The `π`-orbit (`π`-cycle) of a state: `{π^k c | k : ℕ}`. -/
def piOrbit (c : Fin n → Fin 4) : Set (Fin n → Fin 4) :=
  {d | ∃ k : ℕ, d = (piMove P)^[k] c}

/-- A `DD` state at `j`: `c` doubly locked at `j` and `π c` doubly locked at `j + 3`. -/
def DDstate (c : Fin n → Fin 4) (j : Fin 5) : Prop :=
  DoublyLocked P c j ∧ DoublyLocked P (piMove P c) (j + 3)

/-- `c` is an endpoint of a `DD` step: the start (`DDStep c`) or the end (`DDStep (π⁻¹ c)`). -/
def DDEnd (c : Fin n → Fin 4) : Prop := DDStep P c ∨ DDStep P (piInv P c)

/-- The `σ`-link: `c` is a `DD` endpoint, doubly locked at `j`, and `d = σ c = sigSwap P c j`
(the swap of the `{α, μ}`-component of `x (j+1)`). -/
def sigmaLink (c d : Fin n → Fin 4) : Prop :=
  DDEnd P c ∧ ∃ j, DoublyLocked P c j ∧ d = sigSwap P c j

/-- One step of the joining relation inside the class `kclass M h c₀`: a `π`-step or a
`σ`-link. -/
def groupRel (c₀ c d : Fin n → Fin 4) : Prop :=
  c ∈ kclass M h c₀ ∧ d ∈ kclass M h c₀ ∧ (d = piMove P c ∨ sigmaLink P c d)

open Classical in
/-- The `σ`-group of `c` in the class of `c₀`: the union of the `π`-cycles reachable from the
cycle of `c` by `σ`-links in either direction. -/
noncomputable def sigmaGroup (c₀ c : Fin n → Fin 4) : Finset (Fin n → Fin 4) :=
  (kclass M h c₀).filter (Relation.EqvGen (groupRel P c₀) c)

/-- The σ-group floor at the hole `P`: every σ-group of every Kempe class has `Σ λ ≤ 0`. **Not true in general**: it fails at plantri p26 #70869 (`plantri -m5 -c4 -a 26`, 1-based), hole 11, plantri orientation, link degrees (5,6,5,6,6), where a σ-group of two π-cycles has Σw = +1 (Studio Job F, `local-runs/27-studio-positive-config/witness-sigC-p26-70869-h11.json`). Conjecture σC (`NightFloorR53.md` §5) asserts it only at R5³ holes (spherical triangulation, no separating triangle, three cyclically consecutive degree-5 link vertices); the Studio also found 0 failures at every (5,5,5,5,6) hole, orders 24–26. Proved at all-5 holes (`sigmaC_of_icoBall`). -/
def SigmaC : Prop :=
  ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ →
    ∀ c ∈ kclass M h c₀, ∑ d ∈ sigmaGroup P c₀ c, lam P d ≤ 0

end defs

variable {P : Pent M.graph h} {c₀ c d : Fin n → Fin 4}

/-! ### Basic facts -/

lemma DDstate.ddStep {j : Fin 5} (hd : DDstate P c j) : DDStep P c :=
  ⟨⟨j, hd.1⟩, ⟨j + 3, hd.2⟩⟩

lemma DDEnd.dl (hc : ProperOff M.graph h c) (hd : DDEnd P c) : DLState P c := by
  rcases hd with hd | hd
  · exact hd.1
  · have := hd.2
    rwa [piMove_piInv hc] at this

open Classical in
lemma mem_kclass_iff : d ∈ kclass M h c₀ ↔
    ProperOff M.graph h d ∧ KempeEquiv (G := M.graph) (h := h) c₀ d := by
  unfold kclass; simp

lemma piMove_mem_kclass (hc : c ∈ kclass M h c₀) : piMove P c ∈ kclass M h c₀ :=
  (kclass_bijOn (P := P) c₀).mapsTo hc

/-- `σ` is a Kempe step at every doubly locked state, so it stays in the class. -/
lemma sigSwap_mem_kclass {j : Fin 5} (hc : c ∈ kclass M h c₀) (hd : DoublyLocked P c j) :
    sigSwap P c j ∈ kclass M h c₀ := by
  obtain ⟨hp, he⟩ := mem_kclass_iff.1 hc
  obtain ⟨st, hp', -⟩ := sigSwap_basic hp hd.1
  exact mem_kclass_iff.2 ⟨hp', he.tail st⟩

lemma sigmaLink_mem_kclass (hc : c ∈ kclass M h c₀) (hl : sigmaLink P c d) :
    d ∈ kclass M h c₀ := by
  obtain ⟨-, j, hd, rfl⟩ := hl
  exact sigSwap_mem_kclass hc hd

lemma piOrbit_subset_kclass (hc : c ∈ kclass M h c₀) :
    piOrbit P c ⊆ ↑(kclass M h c₀) := by
  rintro _ ⟨k, rfl⟩
  induction k with
  | zero => exact hc
  | succ k ih =>
    rw [Function.iterate_succ_apply']
    exact piMove_mem_kclass ih

lemma piOrbit_finite (hc : c ∈ kclass M h c₀) : (piOrbit P c).Finite :=
  (kclass M h c₀).finite_toSet.subset (piOrbit_subset_kclass hc)

/-! ### `σ`-groups -/

open Classical in
lemma mem_sigmaGroup : d ∈ sigmaGroup P c₀ c ↔
    d ∈ kclass M h c₀ ∧ Relation.EqvGen (groupRel P c₀) c d := by
  unfold sigmaGroup; exact Finset.mem_filter

theorem sigmaGroup_subset_kclass : sigmaGroup P c₀ c ⊆ kclass M h c₀ :=
  fun _ hd => (mem_sigmaGroup.1 hd).1

lemma self_mem_sigmaGroup (hc : c ∈ kclass M h c₀) : c ∈ sigmaGroup P c₀ c :=
  mem_sigmaGroup.2 ⟨hc, .refl _⟩

lemma piMove_mem_sigmaGroup (hd : d ∈ sigmaGroup P c₀ c) : piMove P d ∈ sigmaGroup P c₀ c := by
  obtain ⟨hdS, hr⟩ := mem_sigmaGroup.1 hd
  have hS := piMove_mem_kclass (P := P) hdS
  exact mem_sigmaGroup.2 ⟨hS, .trans _ _ _ hr (.rel _ _ ⟨hdS, hS, Or.inl rfl⟩)⟩

lemma sigmaLink_mem_sigmaGroup {e : Fin n → Fin 4} (hd : d ∈ sigmaGroup P c₀ c)
    (hl : sigmaLink P d e) : e ∈ sigmaGroup P c₀ c := by
  obtain ⟨hdS, hr⟩ := mem_sigmaGroup.1 hd
  have hS := sigmaLink_mem_kclass hdS hl
  exact mem_sigmaGroup.2 ⟨hS, .trans _ _ _ hr (.rel _ _ ⟨hdS, hS, Or.inr hl⟩)⟩

/-- A `σ`-group is a union of `π`-orbits. -/
theorem piOrbit_subset_sigmaGroup (hd : d ∈ sigmaGroup P c₀ c) :
    piOrbit P d ⊆ ↑(sigmaGroup P c₀ c) := by
  rintro _ ⟨k, rfl⟩
  induction k with
  | zero => exact hd
  | succ k ih =>
    rw [Function.iterate_succ_apply']
    exact piMove_mem_sigmaGroup ih

/-- **`π`-invariance.** `π` is a bijection of every `σ`-group. -/
theorem sigmaGroup_piInvariant :
    Set.BijOn (piMove P) ↑(sigmaGroup P c₀ c) ↑(sigmaGroup P c₀ c) := by
  have hb := kclass_bijOn (P := P) c₀
  refine ⟨fun d hd => piMove_mem_sigmaGroup hd,
    hb.injOn.mono fun d hd => sigmaGroup_subset_kclass hd, fun d hd => ?_⟩
  obtain ⟨hdS, hr⟩ := mem_sigmaGroup.1 hd
  obtain ⟨e, heS, rfl⟩ := hb.surjOn hdS
  exact ⟨e, mem_sigmaGroup.2 ⟨heS, .trans _ _ _ hr (.symm _ _ (.rel _ _ ⟨heS, hdS, Or.inl rfl⟩))⟩,
    rfl⟩

lemma sigmaGroup_properOff : ∀ d ∈ sigmaGroup P c₀ c, ProperOff M.graph h d :=
  fun d hd => kclass_properOff c₀ d (sigmaGroup_subset_kclass hd)

open Classical in
/-- **The identity on a `σ`-group.** `Σ_group λ = |group| − 4·F(group)`. -/
theorem sum_lam_sigmaGroup :
    ∑ d ∈ sigmaGroup P c₀ c, lam P d = ((sigmaGroup P c₀ c).card : ℤ) -
      4 * ((sigmaGroup P c₀ c).filter (Target M.graph h)).card :=
  sum_lam sigmaGroup_properOff sigmaGroup_piInvariant

/-- Two states of one `σ`-group have the same `σ`-group. -/
lemma sigmaGroup_eq (hd : d ∈ sigmaGroup P c₀ c) : sigmaGroup P c₀ d = sigmaGroup P c₀ c := by
  obtain ⟨-, hr⟩ := mem_sigmaGroup.1 hd
  ext e
  simp only [mem_sigmaGroup]
  exact and_congr_right fun _ => ⟨fun h' => .trans _ _ _ hr h', fun h' => .trans _ _ _ (.symm _ _ hr) h'⟩

/-- A class is the disjoint union of its `σ`-groups: if every `σ`-group has `Σ λ ≤ 0`, so does
the class. -/
theorem sum_lam_class_of_groups
    (H : ∀ c ∈ kclass M h c₀, ∑ d ∈ sigmaGroup P c₀ c, lam P d ≤ 0) :
    ∑ c ∈ kclass M h c₀, lam P c ≤ 0 := by
  classical
  rw [← Finset.sum_image' (s := kclass M h c₀) (g := sigmaGroup P c₀)
    (f := fun g => ∑ d ∈ g, lam P d) (lam P) ?_]
  · refine Finset.sum_nonpos fun g hg => ?_
    obtain ⟨c, hc, rfl⟩ := Finset.mem_image.1 hg
    exact H c hc
  · intro c hc
    refine Finset.sum_congr ?_ fun _ _ => rfl
    ext d
    rw [Finset.mem_filter]
    constructor
    · intro hd
      exact ⟨sigmaGroup_subset_kclass hd, sigmaGroup_eq hd⟩
    · rintro ⟨hdS, he⟩
      rw [← he]
      exact self_mem_sigmaGroup hdS

/-- **`σC` implies the quarter floor.** -/
theorem sigmaC_imp_quarterFloor (H : SigmaC P) : QuarterFloorConj (G := M.graph) (h := h) :=
  (quarterFloor_iff_lam P).2 fun c₀ h₀ => sum_lam_class_of_groups (H c₀ h₀)

/-- Three cyclically consecutive link vertices of the hole `P` have degree five. -/
def ThreeConsecFive (P : Pent M.graph h) : Prop :=
  ∃ j : Fin 5, M.graph.degree (P.x j) = 5 ∧ M.graph.degree (P.x (j + 1)) = 5 ∧
    M.graph.degree (P.x (j + 2)) = 5

/-- The restricted conjecture: `SigmaC P` at every pentagonal hole with three consecutive
degree-5 link vertices (on every spherical map). -/
def SigmaCConj : Prop :=
  ∀ (n : ℕ) (M : SphericalMap n) (h : Fin n) (P : Pent M.graph h), ThreeConsecFive P → SigmaC P

/-- `SigmaCConj` gives the quarter floor at every such hole. -/
theorem sigmaCConj_imp_floor_on_family (H : SigmaCConj) :
    ∀ (n : ℕ) (M : SphericalMap n) (h : Fin n) (P : Pent M.graph h), ThreeConsecFive P →
      QuarterFloorConj (G := M.graph) (h := h) :=
  fun n M h P hP => sigmaC_imp_quarterFloor (H n M h P hP)

/-! ### Theorem F5 restricted to a `σ`-group -/

variable {w : Fin 5 → Fin n}

open Classical in
/-- F5's count inside one `σ`-group: `|DD| ≤ 2 N₀`. Each `DD` step is sent to its `R3` endpoint
(a `DD` endpoint in the group, by `π`-invariance), and each such endpoint is sent by `σ`
(injectively) to a lockless state, which is `σ`-linked to it and so lies in the same group. -/
theorem dd_le_two_noLock_group (B : IcoBallP P w) :
    ((sigmaGroup P c₀ c).filter (DDStep P)).card ≤
      2 * ((sigmaGroup P c₀ c).filter (NoLock P)).card := by
  set S := sigmaGroup P c₀ c with hSdef
  let R := S.filter (fun d => (∃ j, R3At P w d j) ∧ DDEnd P d)
  have hb : Set.BijOn (piMove P) ↑S ↑S := sigmaGroup_piInvariant
  have hpS : ∀ d ∈ S, ProperOff M.graph h d := sigmaGroup_properOff
  have h1 : (S.filter (DDStep P)).card ≤ 2 * R.card := by
    let f : (Fin n → Fin 4) → (Fin n → Fin 4) :=
      fun d => if ∃ j, R3At P w d j then d else piMove P d
    refine Finset.card_le_mul_card_image_of_maps_to (f := f) ?_ 2 ?_
    · intro d hd
      obtain ⟨hdS, hdd⟩ := Finset.mem_filter.1 hd
      obtain ⟨j, hdl⟩ := hdd.1
      have hp := hpS d hdS
      by_cases hx : ∃ j, R3At P w d j
      · simp only [f, ite_eq_left hx]
        exact Finset.mem_filter.2 ⟨hdS, hx, Or.inl hdd⟩
      · simp only [f, ite_eq_right hx]
        refine Finset.mem_filter.2 ⟨hb.mapsTo hdS, ?_, Or.inr ?_⟩
        · rcases dd_r3 B hp hdl hdd.2 with h' | h'
          · exact absurd ⟨j, h'⟩ hx
          · exact ⟨_, h'⟩
        · rw [piInv_piMove hp]; exact hdd
    · intro r _
      refine (Finset.card_le_card ?_).trans (Finset.card_le_two (a := r) (b := piInv P r))
      intro d hd
      obtain ⟨hdD, hfd⟩ := Finset.mem_filter.1 hd
      have hp := hpS d (Finset.mem_filter.1 hdD).1
      by_cases hx : ∃ j, R3At P w d j
      · simp only [f, ite_eq_left hx] at hfd
        simp [hfd]
      · simp only [f, ite_eq_right hx] at hfd
        have : d = piInv P r := by rw [← hfd, piInv_piMove hp]
        simp [this]
  have h2 : R.card ≤ (S.filter (NoLock P)).card := by
    let g : (Fin n → Fin 4) → (Fin n → Fin 4) :=
      fun d => if hx : ∃ j, R3At P w d j then sigSwap P d hx.choose else d
    have gval : ∀ d (hx : ∃ j, R3At P w d j), g d = sigSwap P d hx.choose :=
      fun d hx => dite_eq_left hx
    refine Finset.card_le_card_of_injOn g ?_ ?_
    · intro d hd
      obtain ⟨hdS, hx, hE⟩ := Finset.mem_filter.1 (Finset.mem_coe.1 hd)
      obtain ⟨-, -, r', n1, n2, -⟩ := sigSwap_spec B (hpS d hdS) hx.choose_spec
      rw [Finset.mem_coe, gval d hx]
      exact Finset.mem_filter.2 ⟨sigmaLink_mem_sigmaGroup hdS
        ⟨hE, hx.choose, hx.choose_spec.1, rfl⟩, ⟨_, r', n1, n2⟩⟩
    · intro d hd d' hd' E
      obtain ⟨hdS, hx, -⟩ := Finset.mem_filter.1 (Finset.mem_coe.1 hd)
      obtain ⟨hdS', hx', -⟩ := Finset.mem_filter.1 (Finset.mem_coe.1 hd')
      rw [gval d hx, gval d' hx'] at E
      exact sigSwap_inj B (hpS d hdS) hx.choose_spec (hpS d' hdS') hx'.choose_spec E
  omega

/-- F5 per `σ`-group: at an icosahedral hole every `σ`-group has `Σ λ ≤ 0`. -/
theorem sum_lam_sigmaGroup_nonpos (B : IcoBallP P w) :
    ∑ d ∈ sigmaGroup P c₀ c, lam P d ≤ 0 := by
  classical
  have h1 := sum_lam_le (P := P) (sigmaGroup_properOff (c₀ := c₀) (c := c))
    sigmaGroup_piInvariant
  have h2 := dd_le_two_noLock_group (c₀ := c₀) (c := c) B
  have h2' : (((sigmaGroup P c₀ c).filter (DDStep P)).card : ℤ) ≤
      2 * ((sigmaGroup P c₀ c).filter (NoLock P)).card := by exact_mod_cast h2
  omega

/-- **`σC` at an icosahedral hole** (F5 is the all-5 case of `σC`). -/
theorem sigmaC_of_icoBall (B : IcoBallP P w) : SigmaC P :=
  fun _ _ _ _ => sum_lam_sigmaGroup_nonpos B

end sphere

end SimpleGraph.QuarterFloor

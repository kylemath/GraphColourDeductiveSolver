/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterNonDLImage
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterSigmaFix
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterTwoPeriod

/-!
# Where a `σ`-image sits in its unfilled run

For a repeat state `r` (repeat index `j`; in the applications `r` is doubly locked) the
`σ`-image `s = σ r = sigSwap P r j` is a proper-off unfilled state with the same repeat index
(`sigSwap_basic`), in the same Kempe class. No ball hypothesis, any hole, any pattern.

## Main results (sorry-free, no new axioms)

* `RunPos`, `runPos`: the place of an unfilled state in its unfilled run, read off its locks:
  `single` (lockless, `u = 1`), `start` (`Lock2` only), `finish` (`Lock1` only),
  `interior` (doubly locked). Being a function, it takes exactly one value.
* `runPos_spec` / **`sigma_image_cases`** (via Lemma P): `s` is
  `single` ⇔ `π⁻¹ s`, `π s` both filled ⇔ `NoLock s`;
  `start` ⇔ `π⁻¹ s` filled, `π s` unfilled; `finish` ⇔ `π⁻¹ s` unfilled, `π s` filled;
  `interior` ⇔ both unfilled ⇔ `DLState s`. `sigma_image_cases'`: the same as a four-way
  disjunction with the lock literals.
* `Boundary`: an unfilled state with a filled `π`-neighbour (start, end, or `u = 1` state of its
  excursion); `boundary_iff_not_DL`, `boundary_iff_excursion` (in an excursion `(e, u, f)`,
  `π^k e` with `k < u` is a boundary state iff `k = 0 ∨ k + 1 = u`), and
  **`sigma_image_boundary_of_not_DL`**.
* **`sigma_image_in_class`**: `σ r` is in the Kempe class of `r` (a whole-component Kempe swap,
  `sigSwap_basic`; the class-membership is `mem_kclass_iff` of `QuarterSigmaGroups`).
* **`sigma_fixed_iff_image_eq`**: `SigmaFixed r j ⇔ σ r = recol (α μ) r` off the hole
  (`sigmaFixed_iff_sigSwap`). (At `h` itself `σ` never recolours, so the equation is stated on
  `T − h`.)
* **`images_le_boundary`** (`σ` injective, `sigSwap_inj'`): for a finite set `Z` of doubly locked
  states (e.g. an all-DL `π`-orbit) with repeat indices `J`, and any finite `T` (e.g. a target
  `π`-orbit), `#{c ∈ Z | σ c ∈ T, σ c not DL} ≤ #{t ∈ T | Boundary t}`;
  `images_le_boundary_DL` with the repeat index chosen (`dlIdx`).
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

/-- The place of an unfilled state in its unfilled run. -/
inductive RunPos
  | single
  | start
  | finish
  | interior
  deriving DecidableEq

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n} {P : Pent M.graph h}
  {c₀ r s e : Fin n → Fin 4} {j : Fin 5}

variable (P) in
open Classical in
/-- The run position of a state with repeat index `j`, read off its locks at `j`. -/
noncomputable def runPos (s : Fin n → Fin 4) (j : Fin 5) : RunPos :=
  if Lock1 P s j then (if Lock2 P s j then .interior else .finish)
  else (if Lock2 P s j then .start else .single)

theorem runPos_eq_single : runPos P s j = .single ↔ ¬ Lock1 P s j ∧ ¬ Lock2 P s j := by
  unfold runPos; split_ifs <;> simp_all
theorem runPos_eq_start : runPos P s j = .start ↔ ¬ Lock1 P s j ∧ Lock2 P s j := by
  unfold runPos; split_ifs <;> simp_all
theorem runPos_eq_finish : runPos P s j = .finish ↔ Lock1 P s j ∧ ¬ Lock2 P s j := by
  unfold runPos; split_ifs <;> simp_all
theorem runPos_eq_interior : runPos P s j = .interior ↔ Lock1 P s j ∧ Lock2 P s j := by
  unfold runPos; split_ifs <;> simp_all

/-- **Run position through the fill pattern** (Lemma P), for any proper-off repeat state. -/
theorem runPos_spec (hs : ProperOff M.graph h s) (hr : RepeatAt P s j) :
    (runPos P s j = .single ↔
      Target M.graph h (piInv P s) ∧ Target M.graph h (piMove P s)) ∧
    (runPos P s j = .start ↔
      Target M.graph h (piInv P s) ∧ ¬ Target M.graph h (piMove P s)) ∧
    (runPos P s j = .finish ↔
      ¬ Target M.graph h (piInv P s) ∧ Target M.graph h (piMove P s)) ∧
    (runPos P s j = .interior ↔
      ¬ Target M.graph h (piInv P s) ∧ ¬ Target M.graph h (piMove P s)) := by
  obtain ⟨a, b, c, d⟩ := lemmaP hs hr
  exact ⟨runPos_eq_single.trans d, runPos_eq_start.trans b, runPos_eq_finish.trans c,
    runPos_eq_interior.trans a⟩

theorem runPos_single_iff_noLock (hs : ProperOff M.graph h s) (hr : RepeatAt P s j) :
    runPos P s j = .single ↔ NoLock P s := by
  rw [(runPos_spec hs hr).1, noLock_iff hs]
  exact ⟨fun H => ⟨rep_not_target hr, H⟩, fun H => H.2⟩

theorem runPos_interior_iff_DL (hs : ProperOff M.graph h s) (hr : RepeatAt P s j) :
    runPos P s j = .interior ↔ DLState P s := by
  rw [(runPos_spec hs hr).2.2.2, dlState_iff hs]
  exact ⟨fun H => ⟨rep_not_target hr, H⟩, fun H => H.2⟩

/-! ### (1) The four cases for `σ r` -/

/-- **(1) The position of a `σ`-image.** For a repeat state `r` (repeat index `j`), the image
`s = σ r` is unfilled with repeat index `j`, and its run position (exactly one value) is read
off its fill pattern: lockless ⇔ `u = 1` run; `Lock2`-only ⇔ start of its run; `Lock1`-only ⇔
end of its run; doubly locked ⇔ run interior. -/
theorem sigma_image_cases (hc : ProperOff M.graph h r) (hr : RepeatAt P r j) :
    ProperOff M.graph h (sigSwap P r j) ∧ RepeatAt P (sigSwap P r j) j ∧
    ¬ Target M.graph h (sigSwap P r j) ∧
    (runPos P (sigSwap P r j) j = .single ↔ NoLock P (sigSwap P r j)) ∧
    (runPos P (sigSwap P r j) j = .single ↔
      Target M.graph h (piInv P (sigSwap P r j)) ∧ Target M.graph h (piMove P (sigSwap P r j))) ∧
    (runPos P (sigSwap P r j) j = .start ↔
      Target M.graph h (piInv P (sigSwap P r j)) ∧
        ¬ Target M.graph h (piMove P (sigSwap P r j))) ∧
    (runPos P (sigSwap P r j) j = .finish ↔
      ¬ Target M.graph h (piInv P (sigSwap P r j)) ∧
        Target M.graph h (piMove P (sigSwap P r j))) ∧
    (runPos P (sigSwap P r j) j = .interior ↔ DLState P (sigSwap P r j)) ∧
    (runPos P (sigSwap P r j) j = .interior ↔
      ¬ Target M.graph h (piInv P (sigSwap P r j)) ∧
        ¬ Target M.graph h (piMove P (sigSwap P r j))) := by
  obtain ⟨-, hs, hr', -⟩ := sigSwap_basic hc hr
  obtain ⟨a, b, c, d⟩ := runPos_spec hs hr'
  exact ⟨hs, hr', rep_not_target hr', runPos_single_iff_noLock hs hr', a, b, c,
    runPos_interior_iff_DL hs hr', d⟩

/-- **(1′) The four cases as a disjunction** (they are mutually exclusive: the lock literals
differ). -/
theorem sigma_image_cases' (hc : ProperOff M.graph h r) (hr : RepeatAt P r j) :
    (¬ Lock1 P (sigSwap P r j) j ∧ ¬ Lock2 P (sigSwap P r j) j ∧ NoLock P (sigSwap P r j) ∧
      Target M.graph h (piInv P (sigSwap P r j)) ∧ Target M.graph h (piMove P (sigSwap P r j))) ∨
    (¬ Lock1 P (sigSwap P r j) j ∧ Lock2 P (sigSwap P r j) j ∧
      Target M.graph h (piInv P (sigSwap P r j)) ∧
        ¬ Target M.graph h (piMove P (sigSwap P r j))) ∨
    (Lock1 P (sigSwap P r j) j ∧ ¬ Lock2 P (sigSwap P r j) j ∧
      ¬ Target M.graph h (piInv P (sigSwap P r j)) ∧
        Target M.graph h (piMove P (sigSwap P r j))) ∨
    (Lock1 P (sigSwap P r j) j ∧ Lock2 P (sigSwap P r j) j ∧ DLState P (sigSwap P r j) ∧
      ¬ Target M.graph h (piInv P (sigSwap P r j)) ∧
        ¬ Target M.graph h (piMove P (sigSwap P r j))) := by
  obtain ⟨hs, hr', -, n1, n2, n3, n4, n5, n6⟩ := sigma_image_cases hc hr
  rcases hp : runPos P (sigSwap P r j) j with _ | _ | _ | _
  · exact Or.inl ⟨(runPos_eq_single.1 hp).1, (runPos_eq_single.1 hp).2, n1.1 hp, n2.1 hp⟩
  · exact Or.inr (Or.inl ⟨(runPos_eq_start.1 hp).1, (runPos_eq_start.1 hp).2, n3.1 hp⟩)
  · exact Or.inr (Or.inr (Or.inl ⟨(runPos_eq_finish.1 hp).1, (runPos_eq_finish.1 hp).2,
      n4.1 hp⟩))
  · exact Or.inr (Or.inr (Or.inr ⟨(runPos_eq_interior.1 hp).1, (runPos_eq_interior.1 hp).2,
      n5.1 hp, n6.1 hp⟩))

/-! ### (2) Boundary states -/

variable (P) in
/-- An **excursion-boundary state**: unfilled, with a filled `π`-predecessor (the start of its
excursion) or a filled `π`-successor (the last unfilled state); both for `u = 1`. -/
def Boundary (s : Fin n → Fin 4) : Prop :=
  ¬ Target M.graph h s ∧ (Target M.graph h (piInv P s) ∨ Target M.graph h (piMove P s))

/-- An unfilled state is a boundary state iff it is not doubly locked. -/
theorem boundary_iff_not_DL (hs : ProperOff M.graph h s) (hu : ¬ Target M.graph h s) :
    Boundary P s ↔ ¬ DLState P s := by
  rw [dlState_iff hs]
  unfold Boundary
  tauto

/-- In an excursion `(e, u, f)`, the unfilled state `π^k e` (`k < u`) is a boundary state iff it
is the first (`k = 0`) or the last (`k + 1 = u`) unfilled state. -/
theorem boundary_iff_excursion {u f k : ℕ} (E : Excursion P e u f) (hk : k < u) :
    Boundary P ((piMove P)^[k] e) ↔ k = 0 ∨ k + 1 = u := by
  have hp := iter_properOff (P := P) E.proper
  have hpre : Target M.graph h (piInv P ((piMove P)^[k] e)) ↔ k = 0 := by
    rcases k with _ | k
    · exact ⟨fun _ => rfl, fun _ => E.prev⟩
    · rw [Function.iterate_succ_apply', piInv_piMove (hp k)]
      exact ⟨fun ht => absurd ht (E.unf k (by omega)), fun h' => absurd h' (Nat.succ_ne_zero k)⟩
  have hsuc : Target M.graph h (piMove P ((piMove P)^[k] e)) ↔ k + 1 = u := by
    rw [← Function.iterate_succ_apply' (piMove P)]
    constructor
    · intro ht
      by_contra hne
      exact E.unf (k + 1) (by omega) ht
    · intro he
      exact E.fil (k + 1) (by omega) (by have := E.f_pos; omega)
  unfold Boundary
  rw [hpre, hsuc]
  exact ⟨fun H => H.2, fun H => ⟨E.unf k hk, H⟩⟩

/-- **(2)** If the `σ`-image of a repeat state is not doubly locked, it is an excursion-boundary
state of its `π`-orbit. -/
theorem sigma_image_boundary_of_not_DL (hc : ProperOff M.graph h r) (hr : RepeatAt P r j)
    (hn : ¬ DLState P (sigSwap P r j)) : Boundary P (sigSwap P r j) := by
  obtain ⟨hs, -, hu, -⟩ := sigma_image_cases hc hr
  exact (boundary_iff_not_DL hs hu).2 hn

/-- A boundary `σ`-image is not doubly locked (the converse of (2)). -/
theorem not_DL_of_sigma_image_boundary (hc : ProperOff M.graph h r) (hr : RepeatAt P r j)
    (hb : Boundary P (sigSwap P r j)) : ¬ DLState P (sigSwap P r j) := by
  obtain ⟨hs, -, hu, -⟩ := sigma_image_cases hc hr
  exact (boundary_iff_not_DL hs hu).1 hb

/-! ### (3) The class -/

/-- `σ r` is Kempe equivalent to `r` (one whole-component swap). -/
theorem sigma_image_kempeEquiv (hc : ProperOff M.graph h r) (hr : RepeatAt P r j) :
    KempeEquiv (G := M.graph) (h := h) r (sigSwap P r j) :=
  Relation.ReflTransGen.single (sigSwap_basic hc hr).1

/-- **(3)** `σ r` lies in the Kempe class of `r`. -/
theorem sigma_image_in_class (hr : RepeatAt P r j) (hrc : r ∈ kclass M h c₀) :
    sigSwap P r j ∈ kclass M h c₀ := by
  obtain ⟨hp, he⟩ := mem_kclass_iff.1 hrc
  obtain ⟨st, hp', -⟩ := sigSwap_basic hp hr
  exact mem_kclass_iff.2 ⟨hp', he.tail st⟩

/-! ### (4) `σ`-fixed states -/

/-- **(4)** `r` is `σ`-fixed iff `σ r` is the colour transposition `α ↔ μ` of `r` on `T − h`
(`α = r (x j)`, `μ = r (x (j+1))`). -/
theorem sigma_fixed_iff_image_eq (hr : RepeatAt P r j) :
    SigmaFixed P r j ↔ ∀ v, v ≠ h →
      sigSwap P r j v = recol (Equiv.swap (r (P.x j)) (r (P.x (j + 1)))) r v :=
  sigmaFixed_iff_sigSwap hr

/-! ### (5) Counting -/

open Classical in
/-- **(5)** `σ` is injective, so the states of `Z` (doubly locked at `J c`) whose `σ`-image lies
in `T` and is not doubly locked are at most the boundary states of `T`. -/
theorem images_le_boundary (Z T : Finset (Fin n → Fin 4)) (J : (Fin n → Fin 4) → Fin 5)
    (hZ : ∀ c ∈ Z, ProperOff M.graph h c ∧ DoublyLocked P c (J c)) :
    (Z.filter fun c => sigSwap P c (J c) ∈ T ∧ ¬ DLState P (sigSwap P c (J c))).card ≤
      (T.filter (Boundary P)).card := by
  refine Finset.card_le_card_of_injOn (fun c => sigSwap P c (J c)) ?_ ?_
  · intro c hc
    obtain ⟨hcZ, hT, hn⟩ := Finset.mem_filter.1 (Finset.mem_coe.1 hc)
    obtain ⟨hp, hd⟩ := hZ c hcZ
    exact Finset.mem_coe.2 (Finset.mem_filter.2 ⟨hT, sigma_image_boundary_of_not_DL hp hd.1 hn⟩)
  · intro c hc c' hc' E
    obtain ⟨hcZ, -⟩ := Finset.mem_filter.1 (Finset.mem_coe.1 hc)
    obtain ⟨hcZ', -⟩ := Finset.mem_filter.1 (Finset.mem_coe.1 hc')
    exact (sigSwap_inj' (hZ c hcZ).1 (hZ c hcZ).2.1 (hZ c' hcZ').1 (hZ c' hcZ').2.1 E).1

variable (P) in
open Classical in
/-- The repeat index of a doubly locked state (unique, `rep_unique`); `0` otherwise. -/
noncomputable def dlIdx (c : Fin n → Fin 4) : Fin 5 :=
  if hd : DLState P c then Classical.choose hd else 0

theorem dlIdx_spec (hd : DLState P s) : DoublyLocked P s (dlIdx P s) := by
  unfold dlIdx
  split
  · exact Classical.choose_spec hd
  · contradiction

open Classical in
/-- **(5′)** The counting corollary for an all-DL set `Z` (e.g. a `Γ`-cycle), with `σ` at the
(unique) repeat index: `#{c ∈ Z | σ c ∈ T not DL} ≤ #{boundary states of T}`. -/
theorem images_le_boundary_DL (Z T : Finset (Fin n → Fin 4))
    (hZ : ∀ c ∈ Z, ProperOff M.graph h c ∧ DLState P c) :
    (Z.filter fun c => sigSwap P c (dlIdx P c) ∈ T ∧
        ¬ DLState P (sigSwap P c (dlIdx P c))).card ≤
      (T.filter (Boundary P)).card :=
  images_le_boundary Z T (dlIdx P) fun c hc => ⟨(hZ c hc).1, dlIdx_spec (hZ c hc).2⟩

end sphere

end SimpleGraph.QuarterFloor

/-! ### Axiom check -/
#print axioms SimpleGraph.QuarterFloor.runPos_spec
#print axioms SimpleGraph.QuarterFloor.sigma_image_cases
#print axioms SimpleGraph.QuarterFloor.sigma_image_cases'
#print axioms SimpleGraph.QuarterFloor.boundary_iff_excursion
#print axioms SimpleGraph.QuarterFloor.sigma_image_boundary_of_not_DL
#print axioms SimpleGraph.QuarterFloor.sigma_image_in_class
#print axioms SimpleGraph.QuarterFloor.sigma_fixed_iff_image_eq
#print axioms SimpleGraph.QuarterFloor.images_le_boundary
#print axioms SimpleGraph.QuarterFloor.images_le_boundary_DL

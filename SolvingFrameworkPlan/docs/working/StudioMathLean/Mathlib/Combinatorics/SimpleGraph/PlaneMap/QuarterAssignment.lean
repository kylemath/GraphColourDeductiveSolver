/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterFlowIdentity

/-!
# `σC` from a charge-back single-target assignment

Formalises the certificate of the Night log's "charge-back P₁" (Studio Jobs S, Y, Z, AC): over a
finite `π`-closed `g` with positive orbits `Z` (`posOrbits`) and nonpositive orbits `T`
(`nonposOrbits`), and the `def`/`rem` of `QuarterFlowIdentity.lean`:

* `ChargeBack P g`: for each nonpositive `T` with `rem(T) > 0`, a split `cb · T` of `rem(T)` into
  nonnegative weights on the positive orbits, supported on the sources having an exit into `T`
  (and zero for every `T` with `rem(T) ≤ 0`). `defP P g cb Z = def(Z) + Σ_T cb Z T` is `def′(Z)`.
* `Assignment P g cb`: every positive `Z` with `def′(Z) > 0` is sent to ONE nonpositive orbit
  `a Z` with `rem(a Z) < 0`, reached from `Z` by an exit, and no `T` is over-assigned:
  `Σ_{Z : a Z = T, def′ Z > 0} def′(Z) ≤ −rem(T)`.

## Main results (sorry-free, no new axioms)

* `sum_defP_add`: `Σ_Z def′(Z) + Σ_{T, rem ≤ 0} rem(T) = Σ_Z def(Z) + Σ_T rem(T)`.
* `sigmaC_of_assignment`: a charge-back with an assignment gives `Σ_g λ ≤ 0`.
* `sigmaC_of_assignment_groups`: a certificate on every `σ`-group gives `SigmaC P`.

Pure finite-sum bookkeeping on top of `flow_identity`; no geometry.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

section defs
variable (P : Pent M.graph h) (g : Finset (Fin n → Fin 4))

/-- **A charge-back** of the positive remainders of `g`: `cb Z T` is the part of `rem(T) > 0`
charged back to the positive orbit `Z`; it is nonnegative, vanishes unless `rem(T) > 0` and some
exit of `g` runs from `Z` into `T`, and the parts sum to `rem(T)`. -/
structure ChargeBack where
  /-- The charge of `T` on `Z`. -/
  cb : Finset (Fin n → Fin 4) → Finset (Fin n → Fin 4) → ℤ
  nonneg : ∀ Z T, 0 ≤ cb Z T
  support : ∀ Z T, cb Z T ≠ 0 →
    0 < remOrb P g T ∧ ∃ e ∈ exits P g, orbFin P e.1 = Z ∧ orbFin P e.2 = T
  sum_eq : ∀ T ∈ nonposOrbits P g, 0 < remOrb P g T →
    ∑ Z ∈ posOrbits P g, cb Z T = remOrb P g T

/-- `def′(Z) = def(Z) + Σ_T cb Z T`. -/
noncomputable def defP (C : ChargeBack P g) (Z : Finset (Fin n → Fin 4)) : ℤ :=
  defOrb P g Z + ∑ T ∈ nonposOrbits P g, C.cb Z T

/-- **A single-target assignment** for the charge-back `C`: each positive `Z` with `def′(Z) > 0`
goes to one nonpositive `a Z` with `rem(a Z) < 0` reached by an exit from `Z`, and no `T` receives
more than `−rem(T)`. -/
structure Assignment (C : ChargeBack P g) where
  /-- The target of `Z`. -/
  a : Finset (Fin n → Fin 4) → Finset (Fin n → Fin 4)
  mem : ∀ Z ∈ posOrbits P g, 0 < defP P g C Z → a Z ∈ nonposOrbits P g ∧ remOrb P g (a Z) < 0
  nbr : ∀ Z ∈ posOrbits P g, 0 < defP P g C Z →
    ∃ e ∈ exits P g, orbFin P e.1 = Z ∧ orbFin P e.2 = a Z
  bound : ∀ T ∈ nonposOrbits P g, remOrb P g T < 0 →
    ∑ Z ∈ (posOrbits P g).filter (fun Z => 0 < defP P g C Z ∧ a Z = T), defP P g C Z ≤
      -remOrb P g T

end defs

variable {P : Pent M.graph h} {g : Finset (Fin n → Fin 4)}

/-- The charge-back moves the positive remainders onto `def′`:
`Σ_Z def′(Z) + Σ_{T, rem ≤ 0} rem(T) = Σ_Z def(Z) + Σ_T rem(T)`. -/
theorem sum_defP_add (C : ChargeBack P g) :
    ∑ Z ∈ posOrbits P g, defP P g C Z +
        ∑ T ∈ (nonposOrbits P g).filter (fun T => remOrb P g T ≤ 0), remOrb P g T =
      ∑ Z ∈ posOrbits P g, defOrb P g Z + ∑ T ∈ nonposOrbits P g, remOrb P g T := by
  classical
  have hcb : ∑ Z ∈ posOrbits P g, ∑ T ∈ nonposOrbits P g, C.cb Z T =
      ∑ T ∈ (nonposOrbits P g).filter (fun T => ¬ remOrb P g T ≤ 0), remOrb P g T := by
    rw [Finset.sum_comm, ← Finset.sum_filter_add_sum_filter_not (nonposOrbits P g)
      (fun T => remOrb P g T ≤ 0)]
    have z : ∑ T ∈ (nonposOrbits P g).filter (fun T => remOrb P g T ≤ 0),
        ∑ Z ∈ posOrbits P g, C.cb Z T = 0 := by
      refine Finset.sum_eq_zero fun T hT => Finset.sum_eq_zero fun Z _ => ?_
      by_contra hne
      have := (C.support Z T hne).1
      have := (Finset.mem_filter.1 hT).2
      omega
    rw [z, zero_add]
    refine Finset.sum_congr rfl fun T hT => ?_
    obtain ⟨hT, hpos⟩ := Finset.mem_filter.1 hT
    exact C.sum_eq T hT (lt_of_not_ge hpos)
  unfold defP
  rw [Finset.sum_add_distrib, hcb, ← Finset.sum_filter_add_sum_filter_not (nonposOrbits P g)
    (fun T => remOrb P g T ≤ 0)]
  ring

/-- **σC from a charge-back single-target assignment**: `Σ_g λ ≤ 0`. -/
theorem sigmaC_of_assignment (hp : ∀ d ∈ g, ProperOff M.graph h d)
    (hinv : Set.MapsTo (piMove P) (g : Set _) g) (C : ChargeBack P g) (A : Assignment P g C) :
    ∑ d ∈ g, lam P d ≤ 0 := by
  classical
  set Zp := (posOrbits P g).filter (fun Z => 0 < defP P g C Z)
  set Tn := (nonposOrbits P g).filter (fun T => remOrb P g T < 0)
  -- `Σ def′ ≤ Σ_{def′ > 0} def′`
  have h1 : ∑ Z ∈ posOrbits P g, defP P g C Z ≤ ∑ Z ∈ Zp, defP P g C Z := by
    rw [← Finset.sum_filter_add_sum_filter_not (posOrbits P g) (fun Z => 0 < defP P g C Z)]
    refine add_le_of_nonpos_right (Finset.sum_nonpos fun Z hZ => ?_)
    exact le_of_not_gt (Finset.mem_filter.1 hZ).2
  -- `Σ_{rem ≤ 0} rem ≤ Σ_{rem < 0} rem`
  have h2 : ∑ T ∈ (nonposOrbits P g).filter (fun T => remOrb P g T ≤ 0), remOrb P g T ≤
      ∑ T ∈ Tn, remOrb P g T := by
    refine Finset.sum_le_sum_of_subset_of_nonpos ?_ ?_
    · intro T hT
      obtain ⟨hT, hr⟩ := Finset.mem_filter.1 hT
      exact Finset.mem_filter.2 ⟨hT, hr.le⟩
    · intro T hT hT'
      obtain ⟨hT, hr⟩ := Finset.mem_filter.1 hT
      have : ¬ remOrb P g T < 0 := fun hlt => hT' (Finset.mem_filter.2 ⟨hT, hlt⟩)
      omega
  -- the assignment: `Σ_{def′ > 0} def′ ≤ Σ_{rem < 0} (−rem)`
  have h3 : ∑ Z ∈ Zp, defP P g C Z ≤ ∑ T ∈ Tn, -remOrb P g T := by
    rw [← Finset.sum_fiberwise_of_maps_to (s := Zp) (t := Tn) (g := A.a) (fun Z hZ => by
      obtain ⟨hZ, hd⟩ := Finset.mem_filter.1 hZ
      obtain ⟨hm, hr⟩ := A.mem Z hZ hd
      exact Finset.mem_filter.2 ⟨hm, hr⟩)]
    refine Finset.sum_le_sum fun T hT => ?_
    obtain ⟨hT, hr⟩ := Finset.mem_filter.1 hT
    refine le_trans (le_of_eq ?_) (A.bound T hT hr)
    rw [Finset.filter_filter]
  rw [flow_identity hp hinv, ← sum_defP_add C]
  have h4 : ∑ T ∈ Tn, -remOrb P g T = -∑ T ∈ Tn, remOrb P g T := Finset.sum_neg_distrib _
  omega

/-- `σC` at the hole from a charge-back single-target assignment on every `σ`-group. -/
theorem sigmaC_of_assignment_groups
    (H : ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ → ∀ c ∈ kclass M h c₀,
      ∃ C : ChargeBack P (sigmaGroup P c₀ c), Nonempty (Assignment P (sigmaGroup P c₀ c) C)) :
    SigmaC P := fun c₀ h₀ c hc => by
  obtain ⟨C, ⟨A⟩⟩ := H c₀ h₀ c hc
  exact sigmaC_of_assignment sigmaGroup_properOff sigmaGroup_piInvariant.mapsTo C A

/-! ### Charge-back is credit-free (`NightP1.md` §1) -/

section str
variable (P g) in
open Classical in
/-- The total credit of the exits of `g` from `Z` into `T`. -/
noncomputable def creditOut (Z T : Finset (Fin n → Fin 4)) : ℤ :=
  ∑ e ∈ ((exits P g).filter (fun e => orbFin P e.1 = Z)).filter (fun e => orbFin P e.2 = T),
    credit P e

variable (P g) in
/-- **A credit-bounded charge-back** (`NightP1.md` Lemma 1.1): the charge of `T` on `Z` is at
most the credit `Z` sent into `T` (true of the proportional split, since `rem(T) ≤ Σ` credits
into `T`, `remOrb_le_credit_in`). -/
def CreditBounded (C : ChargeBack P g) : Prop :=
  ∀ Z ∈ posOrbits P g, ∀ T ∈ nonposOrbits P g, C.cb Z T ≤ creditOut P g Z T

open Classical in
/-- `rem(T) ≤ Σ` credits into `T` on a nonpositive orbit (`Λ(T) ≤ 0`). -/
lemma remOrb_le_credit_in {T : Finset (Fin n → Fin 4)} (hT : T ∈ nonposOrbits P g) :
    remOrb P g T ≤ ∑ e ∈ (exits P g).filter (fun e => orbFin P e.2 = T), credit P e := by
  have := (Finset.mem_filter.1 hT).2
  unfold remOrb
  omega

/-- **`def′(Z) ≤ Λ(Z)`** (`NightP1.md` Lemma 1.1): a credit-bounded charge-back never returns
more than `Z` sent out. -/
theorem defPrime_le_lam {C : ChargeBack P g} (hC : CreditBounded P g C)
    {Z : Finset (Fin n → Fin 4)} (hZ : Z ∈ posOrbits P g) :
    defP P g C Z ≤ orbSum P Z := by
  classical
  have hfib : ∑ T ∈ nonposOrbits P g, creditOut P g Z T =
      ∑ e ∈ (exits P g).filter (fun e => orbFin P e.1 = Z), credit P e := by
    unfold creditOut
    refine Finset.sum_fiberwise_of_maps_to (fun e he => ?_) _
    obtain ⟨-, h2, -, -, -, h6⟩ := mem_exits (Finset.mem_filter.1 he).1
    unfold nonposOrbits orbitsOf
    exact Finset.mem_filter.2 ⟨Finset.mem_image_of_mem _ h2, h6⟩
  have hle : ∑ T ∈ nonposOrbits P g, C.cb Z T ≤ ∑ T ∈ nonposOrbits P g, creditOut P g Z T :=
    Finset.sum_le_sum fun T hT => hC Z hZ T hT
  unfold defP defOrb
  omega

variable (P g) in
/-- **P₁^str** (`NightP1.md` Corollary 1.2): the assignment of `Assignment` with `Λ(Z)` in place
of `def′(Z)` in the capacity bound. -/
structure AssignmentStr (C : ChargeBack P g) where
  /-- The target of `Z`. -/
  a : Finset (Fin n → Fin 4) → Finset (Fin n → Fin 4)
  mem : ∀ Z ∈ posOrbits P g, 0 < defP P g C Z → a Z ∈ nonposOrbits P g ∧ remOrb P g (a Z) < 0
  nbr : ∀ Z ∈ posOrbits P g, 0 < defP P g C Z →
    ∃ e ∈ exits P g, orbFin P e.1 = Z ∧ orbFin P e.2 = a Z
  bound : ∀ T ∈ nonposOrbits P g, remOrb P g T < 0 →
    ∑ Z ∈ (posOrbits P g).filter (fun Z => 0 < defP P g C Z ∧ a Z = T), orbSum P Z ≤
      -remOrb P g T

/-- A `P₁^str` assignment for a credit-bounded charge-back is an assignment. -/
def AssignmentStr.toAssignment {C : ChargeBack P g} (hC : CreditBounded P g C)
    (A : AssignmentStr P g C) : Assignment P g C where
  a := A.a
  mem := A.mem
  nbr := A.nbr
  bound T hT hr := le_trans (Finset.sum_le_sum fun _ hZ =>
    defPrime_le_lam hC (Finset.mem_filter.1 hZ).1) (A.bound T hT hr)

/-- **σC from P₁^str**: a credit-bounded charge-back with a `Λ`-capacity assignment gives
`Σ_g λ ≤ 0`. -/
theorem sigmaC_of_assignment_str (hp : ∀ d ∈ g, ProperOff M.graph h d)
    (hinv : Set.MapsTo (piMove P) (g : Set _) g) (C : ChargeBack P g) (hC : CreditBounded P g C)
    (A : AssignmentStr P g C) : ∑ d ∈ g, lam P d ≤ 0 :=
  sigmaC_of_assignment hp hinv C (A.toAssignment hC)

/-- `σC` at the hole from P₁^str on every `σ`-group. -/
theorem sigmaC_of_assignment_str_groups
    (H : ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ → ∀ c ∈ kclass M h c₀,
      ∃ C : ChargeBack P (sigmaGroup P c₀ c), CreditBounded P (sigmaGroup P c₀ c) C ∧
        Nonempty (AssignmentStr P (sigmaGroup P c₀ c) C)) :
    SigmaC P :=
  sigmaC_of_assignment_groups fun c₀ h₀ c hc => by
    obtain ⟨C, hC, ⟨A⟩⟩ := H c₀ h₀ c hc
    exact ⟨C, ⟨A.toAssignment hC⟩⟩

end str

end sphere

end SimpleGraph.QuarterFloor

-- `#print axioms` check (standard axioms only)
#print axioms SimpleGraph.QuarterFloor.sigmaC_of_assignment
#print axioms SimpleGraph.QuarterFloor.sigmaC_of_assignment_groups
#print axioms SimpleGraph.QuarterFloor.defPrime_le_lam
#print axioms SimpleGraph.QuarterFloor.sigmaC_of_assignment_str
#print axioms SimpleGraph.QuarterFloor.sigmaC_of_assignment_str_groups

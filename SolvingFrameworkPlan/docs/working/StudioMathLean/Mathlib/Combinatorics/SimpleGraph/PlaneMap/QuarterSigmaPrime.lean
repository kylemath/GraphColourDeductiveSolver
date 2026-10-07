/-
Copyright (c) 2026 Kyle Mathewson. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Kyle Mathewson
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.QuarterSigmaGroups

/-!
# `σ′`-joined groups of `π`-cycles and Conjecture `σ′C`

Formalises the night's final statement (`NightLog-2026-10-06.md`, "Night's final statement",
Studio Job H). Fix a pentagonal hole `P` and a Kempe class `S = kclass M h c₀`. A **`σ′`-link**
`c ↦ d` is a link-free Kempe swap (a whole two-colour component containing no link vertex
`x i`) from a `DD`-step endpoint `c` whose result `d` is doubly locked at no `j`. Joining the
`π`-cycles of `S` by `σ′`-links gives the **`σ′`-groups**; Conjecture `σ′C` says every
`σ′`-group has `Σ λ ≤ 0`.

The group machinery is factored over an arbitrary link relation `L` (`linkGroup P L c₀ c`, the
class of `c` under the equivalence generated inside `S` by `π`-steps and `L`-links):
`quarterFloor_of_groups` shows that `Σ λ ≤ 0` on every `L`-group implies the quarter floor,
for any `L`. `σ′C` is the instance `L = sigmaPrimeLink P`.

## Main results

* `sigmaPrimeLink_mem_kclass`: a link-free swap is a Kempe step, so `σ′`-links stay in the class.
* `sigmaPrimeGroup_piInvariant`, `sum_lam_sigmaPrimeGroup` (`Σλ = |G| − 4·F(G)`),
  `sum_lam_class_of_primeGroups`, `sigmaPrimeC_imp_quarterFloor`.
* `sigmaPrimeC_of_icoBall` is stated with a documented `sorry` (see its docstring): F5's
  `σ`-exit swaps the `{α, μ}`-component `{x j, x (j+1), x (j+2)}`, which contains link
  vertices, so it is **not** a `σ′`-link under the link-free definition used here, and F5's
  per-group count does not transfer directly.
-/

@[expose] public section
namespace SimpleGraph.QuarterFloor
open VacancySlide VacancyShortFill SphericalMap

section sphere
variable {n : ℕ} {M : SphericalMap n} {h : Fin n}

/-! ### Groups for an arbitrary link relation -/

section general
variable (P : Pent M.graph h) (L : (Fin n → Fin 4) → (Fin n → Fin 4) → Prop)

/-- One step of the joining relation inside the class `kclass M h c₀`: a `π`-step or an
`L`-link, between two states of the class. -/
def linkGroupRel (c₀ c d : Fin n → Fin 4) : Prop :=
  (d = piMove P c ∨ L c d) ∧ c ∈ kclass M h c₀ ∧ d ∈ kclass M h c₀

open Classical in
/-- The `L`-group of `c` in the class of `c₀`. -/
noncomputable def linkGroup (c₀ c : Fin n → Fin 4) : Finset (Fin n → Fin 4) :=
  (kclass M h c₀).filter (Relation.EqvGen (linkGroupRel P L c₀) c)

variable {P L} {c₀ c d : Fin n → Fin 4}

open Classical in
lemma mem_linkGroup : d ∈ linkGroup P L c₀ c ↔
    d ∈ kclass M h c₀ ∧ Relation.EqvGen (linkGroupRel P L c₀) c d := by
  unfold linkGroup; exact Finset.mem_filter

theorem linkGroup_subset_kclass : linkGroup P L c₀ c ⊆ kclass M h c₀ :=
  fun _ hd => (mem_linkGroup.1 hd).1

lemma self_mem_linkGroup (hc : c ∈ kclass M h c₀) : c ∈ linkGroup P L c₀ c :=
  mem_linkGroup.2 ⟨hc, .refl _⟩

lemma piMove_mem_linkGroup (hd : d ∈ linkGroup P L c₀ c) : piMove P d ∈ linkGroup P L c₀ c := by
  obtain ⟨hdS, hr⟩ := mem_linkGroup.1 hd
  have hS := piMove_mem_kclass (P := P) hdS
  exact mem_linkGroup.2 ⟨hS, .trans _ _ _ hr (.rel _ _ ⟨Or.inl rfl, hdS, hS⟩)⟩

/-- An `L`-link from a group member to a class member stays in the group. -/
lemma link_mem_linkGroup {e : Fin n → Fin 4} (hd : d ∈ linkGroup P L c₀ c)
    (heS : e ∈ kclass M h c₀) (hl : L d e) : e ∈ linkGroup P L c₀ c := by
  obtain ⟨hdS, hr⟩ := mem_linkGroup.1 hd
  exact mem_linkGroup.2 ⟨heS, .trans _ _ _ hr (.rel _ _ ⟨Or.inr hl, hdS, heS⟩)⟩

/-- An `L`-group is a union of `π`-orbits. -/
theorem piOrbit_subset_linkGroup (hd : d ∈ linkGroup P L c₀ c) :
    piOrbit P d ⊆ ↑(linkGroup P L c₀ c) := by
  rintro _ ⟨k, rfl⟩
  induction k with
  | zero => exact hd
  | succ k ih =>
    rw [Function.iterate_succ_apply']
    exact piMove_mem_linkGroup ih

/-- **`π`-invariance.** `π` is a bijection of every `L`-group. -/
theorem linkGroup_piInvariant :
    Set.BijOn (piMove P) ↑(linkGroup P L c₀ c) ↑(linkGroup P L c₀ c) := by
  have hb := kclass_bijOn (P := P) c₀
  refine ⟨fun d hd => piMove_mem_linkGroup hd,
    hb.injOn.mono fun d hd => linkGroup_subset_kclass hd, fun d hd => ?_⟩
  obtain ⟨hdS, hr⟩ := mem_linkGroup.1 hd
  obtain ⟨e, heS, rfl⟩ := hb.surjOn hdS
  exact ⟨e, mem_linkGroup.2 ⟨heS, .trans _ _ _ hr (.symm _ _ (.rel _ _ ⟨Or.inl rfl, heS, hdS⟩))⟩,
    rfl⟩

lemma linkGroup_properOff : ∀ d ∈ linkGroup P L c₀ c, ProperOff M.graph h d :=
  fun d hd => kclass_properOff c₀ d (linkGroup_subset_kclass hd)

open Classical in
/-- **The identity on an `L`-group.** `Σ_group λ = |group| − 4·F(group)`. -/
theorem sum_lam_linkGroup :
    ∑ d ∈ linkGroup P L c₀ c, lam P d = ((linkGroup P L c₀ c).card : ℤ) -
      4 * ((linkGroup P L c₀ c).filter (Target M.graph h)).card :=
  sum_lam linkGroup_properOff linkGroup_piInvariant

/-- Two states of one `L`-group have the same `L`-group. -/
lemma linkGroup_eq (hd : d ∈ linkGroup P L c₀ c) : linkGroup P L c₀ d = linkGroup P L c₀ c := by
  obtain ⟨-, hr⟩ := mem_linkGroup.1 hd
  ext e
  simp only [mem_linkGroup]
  exact and_congr_right fun _ =>
    ⟨fun h' => .trans _ _ _ hr h', fun h' => .trans _ _ _ (.symm _ _ hr) h'⟩

/-- A class is the disjoint union of its `L`-groups. -/
theorem sum_lam_class_of_linkGroups
    (H : ∀ c ∈ kclass M h c₀, ∑ d ∈ linkGroup P L c₀ c, lam P d ≤ 0) :
    ∑ c ∈ kclass M h c₀, lam P c ≤ 0 := by
  classical
  rw [← Finset.sum_image' (s := kclass M h c₀) (g := linkGroup P L c₀)
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
      exact ⟨linkGroup_subset_kclass hd, linkGroup_eq hd⟩
    · rintro ⟨hdS, he⟩
      rw [← he]
      exact self_mem_linkGroup hdS

/-- **The group floor implies the quarter floor, for any link relation.** If every `L`-group of
every Kempe class has `Σ λ ≤ 0`, the quarter floor holds at the hole. -/
theorem quarterFloor_of_groups
    (H : ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ →
      ∀ c ∈ kclass M h c₀, ∑ d ∈ linkGroup P L c₀ c, lam P d ≤ 0) :
    QuarterFloorConj (G := M.graph) (h := h) :=
  (quarterFloor_iff_lam P).2 fun c₀ h₀ => sum_lam_class_of_linkGroups (H c₀ h₀)

end general

/-! ### `σ′`-links and `σ′`-groups -/

section defs
variable (P : Pent M.graph h)

/-- A link-free Kempe swap: `d` is `c` with one whole `{a, b}`-component `S` swapped, where `S`
contains no link vertex `x i` (so all link colours are unchanged). -/
def LinkFree (c d : Fin n → Fin 4) : Prop :=
  ∃ a b S, a ≠ b ∧ Whole M.graph h c a b S ∧ (∀ i, P.x i ∉ S) ∧ d = swap c a b S

/-- The `σ′`-link: from a `DD`-step endpoint `c`, a link-free swap whose result is doubly locked
at no `j` (lock-breaking). -/
def sigmaPrimeLink (c d : Fin n → Fin 4) : Prop :=
  DDEnd P c ∧ LinkFree P c d ∧ ¬ ∃ j, DoublyLocked P d j

/-- One step of the `σ′`-joining relation inside the class `kclass M h c₀`. -/
def groupRel' (c₀ c d : Fin n → Fin 4) : Prop :=
  (d = piMove P c ∨ sigmaPrimeLink P c d) ∧ c ∈ kclass M h c₀ ∧ d ∈ kclass M h c₀

open Classical in
/-- The `σ′`-group of `c` in the class of `c₀`. -/
noncomputable def sigmaPrimeGroup (c₀ c : Fin n → Fin 4) : Finset (Fin n → Fin 4) :=
  (kclass M h c₀).filter (Relation.EqvGen (groupRel' P c₀) c)

/-- **Conjecture `σ′C` at the hole `P`**: every `σ′`-group of every Kempe class has `Σ λ ≤ 0`.
Status (Studio Job H): 0 failures on ~100M groups (orders 24–26, both orientations, all 64
IPR/bigsample positive holes). Open. -/
def SigmaPrimeC : Prop :=
  ∀ c₀ : Fin n → Fin 4, ProperOff M.graph h c₀ →
    ∀ c ∈ kclass M h c₀, ∑ d ∈ sigmaPrimeGroup P c₀ c, lam P d ≤ 0

/-- Conjecture `σ′C` everywhere: at every pentagonal hole of every spherical map. -/
def SigmaPrimeCConj : Prop :=
  ∀ (n : ℕ) (M : SphericalMap n) (h : Fin n) (P : Pent M.graph h), SigmaPrimeC P

end defs

variable {P : Pent M.graph h} {c₀ c d : Fin n → Fin 4}

/-- `groupRel'` is the generic joining relation for `L = sigmaPrimeLink P`. -/
lemma groupRel'_eq : groupRel' P c₀ = linkGroupRel P (sigmaPrimeLink P) c₀ := rfl

/-- `sigmaPrimeGroup` is the generic group for `L = sigmaPrimeLink P`. -/
lemma sigmaPrimeGroup_eq_linkGroup :
    sigmaPrimeGroup P c₀ c = linkGroup P (sigmaPrimeLink P) c₀ c := rfl

/-- A link-free swap is a Kempe step. -/
lemma LinkFree.kempeStep (hl : LinkFree P c d) : KempeStep M.graph h c d := by
  obtain ⟨a, b, S, hab, hW, -, rfl⟩ := hl
  exact ⟨a, b, S, hab, hW, rfl⟩

/-- `σ′`-links are Kempe steps, so they never leave a class. -/
lemma sigmaPrimeLink_mem_kclass (hc : c ∈ kclass M h c₀) (hl : sigmaPrimeLink P c d) :
    d ∈ kclass M h c₀ := by
  obtain ⟨hp, he⟩ := mem_kclass_iff.1 hc
  have st := hl.2.1.kempeStep
  obtain ⟨-, ⟨a, b, S, -, hW, -, rfl⟩, -⟩ := hl
  exact mem_kclass_iff.2 ⟨properOff_swap M.graph hp hW, he.tail st⟩

theorem sigmaPrimeGroup_subset_kclass : sigmaPrimeGroup P c₀ c ⊆ kclass M h c₀ :=
  linkGroup_subset_kclass

lemma sigmaPrimeLink_mem_sigmaPrimeGroup {e : Fin n → Fin 4} (hd : d ∈ sigmaPrimeGroup P c₀ c)
    (hl : sigmaPrimeLink P d e) : e ∈ sigmaPrimeGroup P c₀ c :=
  link_mem_linkGroup hd (sigmaPrimeLink_mem_kclass (sigmaPrimeGroup_subset_kclass hd) hl) hl

/-- A `σ′`-group is a union of `π`-orbits. -/
theorem piOrbit_subset_sigmaPrimeGroup (hd : d ∈ sigmaPrimeGroup P c₀ c) :
    piOrbit P d ⊆ ↑(sigmaPrimeGroup P c₀ c) :=
  piOrbit_subset_linkGroup hd

/-- **`π`-invariance.** `π` is a bijection of every `σ′`-group. -/
theorem sigmaPrimeGroup_piInvariant :
    Set.BijOn (piMove P) ↑(sigmaPrimeGroup P c₀ c) ↑(sigmaPrimeGroup P c₀ c) :=
  linkGroup_piInvariant

open Classical in
/-- **The identity on a `σ′`-group.** `Σ_group λ = |group| − 4·F(group)`. -/
theorem sum_lam_sigmaPrimeGroup :
    ∑ d ∈ sigmaPrimeGroup P c₀ c, lam P d = ((sigmaPrimeGroup P c₀ c).card : ℤ) -
      4 * ((sigmaPrimeGroup P c₀ c).filter (Target M.graph h)).card :=
  sum_lam_linkGroup

/-- A class is the disjoint union of its `σ′`-groups. -/
theorem sum_lam_class_of_primeGroups
    (H : ∀ c ∈ kclass M h c₀, ∑ d ∈ sigmaPrimeGroup P c₀ c, lam P d ≤ 0) :
    ∑ c ∈ kclass M h c₀, lam P c ≤ 0 :=
  sum_lam_class_of_linkGroups H

/-- **`σ′C` implies the quarter floor.** -/
theorem sigmaPrimeC_imp_quarterFloor (H : SigmaPrimeC P) :
    QuarterFloorConj (G := M.graph) (h := h) :=
  quarterFloor_of_groups (L := sigmaPrimeLink P) H

/-- `σ′C` everywhere gives the quarter floor at every pentagonal hole. -/
theorem sigmaPrimeCConj_imp_quarterFloor (H : SigmaPrimeCConj) :
    ∀ (n : ℕ) (M : SphericalMap n) (h : Fin n) (_ : Pent M.graph h),
      QuarterFloorConj (G := M.graph) (h := h) :=
  fun n M h P => sigmaPrimeC_imp_quarterFloor (H n M h P)

/-- `σC` is the generic group floor for the `σ`-link relation (with the conjuncts of the joining
relation reordered); so `σC` and `σ′C` are two instances of `quarterFloor_of_groups`. -/
lemma sigmaGroup_eq_linkGroup : sigmaGroup P c₀ c = linkGroup P (sigmaLink P) c₀ c := by
  classical
  ext d
  rw [mem_sigmaGroup, mem_linkGroup]
  refine and_congr_right fun _ => ?_
  have e : groupRel P c₀ = linkGroupRel P (sigmaLink P) c₀ := by
    funext c d
    exact propext ⟨fun ⟨a, b, r⟩ => ⟨r, a, b⟩, fun ⟨r, a, b⟩ => ⟨a, b, r⟩⟩
  rw [e]

/-! ### The icosahedral base case -/

variable {w : Fin 5 → Fin n}

/-- **`σ′C` at an icosahedral hole — NOT PROVED (documented `sorry`).**

The night log says `σ′ ⊇ σ` at the all-5 hole, so that F5's per-group count
(`dd_le_two_noLock_group`) would transfer. Under the link-free definition used here
(`LinkFree`: the swapped component contains no link vertex) this is false: F5's `σ`-exit
`sigSwap P c j` swaps the `{α, μ}`-component of `x (j+1)`, which is `{x j, x (j+1), x (j+2)}`
(`sigSwap_spec`), so it is a Kempe step but not a link-free one, and is not a `σ′`-link
(a link-free swap leaves every link colour unchanged, whereas `σ` exchanges the colours of
`x j` and `x (j+1)`). Proving this needs either a
`σ′`-specific charging at icosahedral holes or a widened `σ′` (e.g. `σ′ ∪ σ`, as in the
Studio's "with σ at R3 endpoints added" variant). -/
theorem sigmaPrimeC_of_icoBall (_B : IcoBallP P w) : SigmaPrimeC P := by
  sorry

end sphere

end SimpleGraph.QuarterFloor

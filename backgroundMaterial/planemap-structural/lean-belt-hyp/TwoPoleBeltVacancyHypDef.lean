/-
Generic vacancy hypothesis at a hole, and its invariance under graph isomorphism.
New file; no existing file edited.
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.VacancyShortFill
public import Mathlib.Combinatorics.SimpleGraph.Coloring

/-!
# The vacancy hypothesis, stated for an arbitrary graph

This is the statement used by the hole induction (`longtable/swarm/hole-induction.md`, section
"Hypothesis"): for every vertex `h` and every proper 4-colouring `c` of `G - h`
(`VacancySlide.ProperOff`), a finite mixed path of singleton slides and Kempe swaps
(`VacancyShortFill.MixedPath`, the hole may move) reaches a state `t = (hole, colouring)` whose
hole has a missing colour (`VacancyShortFill.Target`) and whose colouring is still proper off the
hole.  No definition of this statement existed in the checkout before this file.

* `VacancyAt G B h`: the statement at the hole `h`, with path length at most `B`.
* `VacancyHyp G`: at every hole, with no length bound (the hole-induction form).
* `VacancyAt.colouring`: the conclusion yields a proper 4-colouring of `G`.
* `VacancyAt.of_iso`: invariance under graph isomorphism.
-/

@[expose] public section
namespace SimpleGraph.VacancyHyp
open VacancySlide VacancyShortFill

variable {V W : Type*} [DecidableEq V] [DecidableEq W]

/-- **Vacancy hypothesis at the hole `h`, with path length at most `B`**, 4 colours. -/
def VacancyAt (G : SimpleGraph V) (B : ℕ) (h : V) : Prop :=
  ∀ c : V → Fin 4, ProperOff G h c →
    ∃ k, k ≤ B ∧ ∃ t : V × (V → Fin 4), MixedPath G k (h, c) t ∧
      Target G t.1 t.2 ∧ ProperOff G t.1 t.2

/-- **Vacancy hypothesis**, every hole, unbounded length (the form the hole induction uses). -/
def VacancyHyp (G : SimpleGraph V) : Prop :=
  ∀ h : V, ∀ c : V → Fin 4, ProperOff G h c →
    ∃ k, ∃ t : V × (V → Fin 4), MixedPath G k (h, c) t ∧
      Target G t.1 t.2 ∧ ProperOff G t.1 t.2

lemma VacancyAt.mono {G : SimpleGraph V} {B B' : ℕ} {h : V} (hB : B ≤ B')
    (H : VacancyAt G B h) : VacancyAt G B' h := by
  intro c hc
  obtain ⟨k, hk, r⟩ := H c hc
  exact ⟨k, hk.trans hB, r⟩

lemma VacancyHyp.of_bounded {G : SimpleGraph V} {B : ℕ} (H : ∀ h, VacancyAt G B h) :
    VacancyHyp G := fun h c hc => by
  obtain ⟨k, -, r⟩ := H h c hc
  exact ⟨k, r⟩

/-- The conclusion of the hypothesis is a proper 4-colouring of the whole graph. -/
theorem VacancyAt.colouring {G : SimpleGraph V} {B : ℕ} {h : V} (H : VacancyAt G B h)
    (c : V → Fin 4) (hc : ProperOff G h c) : Nonempty (G.Coloring (Fin 4)) := by
  obtain ⟨k, -, t, -, ⟨x, hx⟩, hp⟩ := H c hc
  refine ⟨Coloring.mk (fun v => if v = t.1 then x else t.2 v) ?_⟩
  intro u v e
  by_cases hu : u = t.1
  · have hv : v ≠ t.1 := fun h' => e.ne (hu.trans h'.symm)
    subst hu
    simp only [if_true, hv, if_false]
    exact (hx e).symm
  · by_cases hv : v = t.1
    · subst hv
      simp only [hu, if_false, if_true]
      exact hx e.symm
    · simp only [hu, hv, if_false]
      exact hp e hu hv

/-! ### Invariance under graph isomorphism -/

section Iso
variable {G : SimpleGraph V} {G' : SimpleGraph W}

/-- Transport of a colouring along an isomorphism. -/
def tr (φ : G ≃g G') (c : V → Fin 4) : W → Fin 4 := fun x => c (φ.symm x)

lemma properOff_tr (φ : G ≃g G') {h : V} {c : V → Fin 4} (hc : ProperOff G h c) :
    ProperOff G' (φ h) (tr φ c) := by
  intro x y hxy hx hy
  apply hc ((φ.symm.map_rel_iff').mpr hxy)
  · intro e; apply hx; rw [← e]; simp
  · intro e; apply hy; rw [← e]; simp

lemma target_tr (φ : G ≃g G') {h : V} {c : V → Fin 4} (ht : Target G h c) :
    Target G' (φ h) (tr φ c) := by
  obtain ⟨x, hx⟩ := ht
  refine ⟨x, fun y hy => hx ?_⟩
  have := (φ.symm.map_rel_iff').mpr hy
  simpa using this

lemma tr_slide (φ : G ≃g G') (h x : V) (c : V → Fin 4) :
    tr φ (slide h x c) = slide (φ h) (φ x) (tr φ c) := by
  funext y
  by_cases hy : y = φ h
  · subst hy; simp [tr, slide]
  · have hy' : φ.symm y ≠ h := by
      intro e; apply hy; rw [← e]; simp
    simp [tr, slide, hy, hy']

lemma uniqueAt_tr (φ : G ≃g G') {h x : V} {c : V → Fin 4} (uniq : UniqueAt G h x c) :
    UniqueAt G' (φ h) (φ x) (tr φ c) := by
  intro y hy hc
  have hy' : G.Adj h (φ.symm y) := by
    have := (φ.symm.map_rel_iff').mpr hy
    simpa using this
  have := uniq hy' (by simpa [tr] using hc)
  rw [← this]; simp

lemma kempeStep_tr (φ : G ≃g G') {h : V} {c d : V → Fin 4} (hk : KempeStep G h c d) :
    KempeStep G' (φ h) (tr φ c) (tr φ d) := by
  classical
  obtain ⟨A, B, S, hAB, ⟨s, hs, hmem⟩, rfl⟩ := hk
  have hact : ∀ y, Active (φ h) (tr φ c) A B (φ y) ↔ Active h c A B y := by
    intro y
    simp [Active, tr]
  have hadj : ∀ y z, (pairGraph G' (φ h) (tr φ c) A B).Adj (φ y) (φ z) ↔
      (pairGraph G h c A B).Adj y z := by
    intro y z
    constructor
    · rintro ⟨e, hy, hz⟩
      exact ⟨(φ.map_rel_iff').mp e, (hact y).mp hy, (hact z).mp hz⟩
    · rintro ⟨e, hy, hz⟩
      exact ⟨(φ.map_rel_iff').mpr e, (hact y).mpr hy, (hact z).mpr hz⟩
  have fwd : ∀ y z, (pairGraph G h c A B).Reachable y z →
      (pairGraph G' (φ h) (tr φ c) A B).Reachable (φ y) (φ z) := by
    intro y z r
    exact r.map ⟨φ, fun {y z} e => (hadj y z).mpr e⟩
  have bwd : ∀ y z, (pairGraph G' (φ h) (tr φ c) A B).Reachable (φ y) (φ z) →
      (pairGraph G h c A B).Reachable y z := by
    intro y z r
    have := r.map (⟨φ.symm, fun {p q} e => by
      have e' : (pairGraph G' (φ h) (tr φ c) A B).Adj
          (φ (φ.symm p)) (φ (φ.symm q)) := by simpa using e
      exact (hadj _ _).mp e'⟩ :
        (pairGraph G' (φ h) (tr φ c) A B) →g (pairGraph G h c A B))
    simpa using this
  refine ⟨A, B, φ '' S, hAB, ⟨φ s, (hact s).mpr hs, fun x => ?_⟩, ?_⟩
  · obtain ⟨y, rfl⟩ := φ.surjective x
    rw [φ.injective.mem_set_image, hmem y]
    exact ⟨fwd _ _, bwd _ _⟩
  · funext x
    obtain ⟨y, rfl⟩ := φ.surjective x
    by_cases hy : y ∈ S
    · have hy' : φ y ∈ φ '' S := ⟨y, hy, rfl⟩
      rw [swap_in hy']
      simp only [tr, RelIso.symm_apply_apply]
      rw [swap_in hy]
    · have hy' : φ y ∉ φ '' S := fun h' => hy (φ.injective.mem_set_image.mp h')
      rw [swap_out hy']
      simp only [tr, RelIso.symm_apply_apply]
      rw [swap_out hy]

lemma mixedStep_tr (φ : G ≃g G') {s t : V × (V → Fin 4)} (st : MixedStep G s t) :
    MixedStep G' (φ s.1, tr φ s.2) (φ t.1, tr φ t.2) := by
  cases st with
  | kempe hk => exact .kempe (kempeStep_tr φ hk)
  | @slide h x c adj uniq =>
    have this : MixedStep G' (φ h, tr φ c) (φ x, slide (φ h) (φ x) (tr φ c)) :=
      MixedStep.slide ((φ.map_rel_iff').mpr adj) (uniqueAt_tr φ uniq)
    rw [← tr_slide φ h x c] at this
    exact this

lemma mixedPath_tr (φ : G ≃g G') {k : ℕ} {s t : V × (V → Fin 4)} (p : MixedPath G k s t) :
    MixedPath G' k (φ s.1, tr φ s.2) (φ t.1, tr φ t.2) := by
  induction p with
  | nil s => exact .nil _
  | cons st _ ih => exact .cons (mixedStep_tr φ st) ih

/-- The hypothesis at `h` (bound `B`) transfers along an isomorphism to the image hole. -/
theorem VacancyAt.of_iso (φ : G ≃g G') {B : ℕ} {h : V} (H : VacancyAt G B h) :
    VacancyAt G' B (φ h) := by
  intro c' hc'
  set c : V → Fin 4 := fun x => c' (φ x) with hcdef
  have hc : ProperOff G h c := by
    intro x y e hx hy
    exact hc' ((φ.map_rel_iff').mpr e) (fun r => hx (φ.injective r)) (fun r => hy (φ.injective r))
  have hcc : tr φ c = c' := by
    funext x; simp [tr, hcdef]
  obtain ⟨k, hk, t, p, hf, hp⟩ := H c hc
  have q := mixedPath_tr φ p
  rw [hcc] at q
  exact ⟨k, hk, (φ t.1, tr φ t.2), q, target_tr φ hf, properOff_tr φ hp⟩

/-- Whole-graph form. -/
theorem VacancyHyp.of_iso (φ : G ≃g G') (H : VacancyHyp G) : VacancyHyp G' := by
  intro h' c' hc'
  obtain ⟨h, rfl⟩ := φ.surjective h'
  set c : V → Fin 4 := fun x => c' (φ x) with hcdef
  have hc : ProperOff G h c := by
    intro x y e hx hy
    exact hc' ((φ.map_rel_iff').mpr e) (fun r => hx (φ.injective r)) (fun r => hy (φ.injective r))
  have hcc : tr φ c = c' := by
    funext x; simp [tr, hcdef]
  obtain ⟨k, t, p, hf, hp⟩ := H h c hc
  have q := mixedPath_tr φ p
  rw [hcc] at q
  exact ⟨k, (φ t.1, tr φ t.2), q, target_tr φ hf, properOff_tr φ hp⟩

end Iso
end SimpleGraph.VacancyHyp

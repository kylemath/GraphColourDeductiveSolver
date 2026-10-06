module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.TwoPoleBeltPoleHole

/-!
# The pole `b`, and the belt theorem at every hole

Mixed (slide and Kempe) paths are transported along graph automorphisms of `G_n`.  The ring swap
exchanges the poles, so `pole_a_complete` gives the pole `b`.  The final statement
`belt_theorem_all_holes` is the vacancy hypothesis at every hole of every `G_n`, `n ≥ 5`.
-/

@[expose] public section
namespace SimpleGraph.TwoPoleBeltPoleHole
open VacancySlide TwoPoleBelt TwoPoleBelt.Vertex TwoPoleBeltWalk

variable {n : ℕ}

lemma transport_slide (φ : G n ≃g G n) (h x : Vertex n) (c : Vertex n → Colour) :
    transport φ (slide h x c) = slide (φ h) (φ x) (transport φ c) := by
  funext y
  by_cases hy : y = φ h
  · subst hy; simp [transport, slide]
  · have hy' : φ.symm y ≠ h := by
      intro e; apply hy; rw [← e]; simp
    simp [transport, slide, hy, hy']

lemma uniqueAt_transport (φ : G n ≃g G n) {h x : Vertex n} {c : Vertex n → Colour}
    (uniq : UniqueAt (graph n) h x c) :
    UniqueAt (graph n) (φ h) (φ x) (transport φ c) := by
  intro y hy hc
  have hy' : (G n).Adj h (φ.symm y) := by
    have := (φ.symm.map_rel_iff').mpr hy
    simpa using this
  have := uniq hy' (by simpa [transport] using hc)
  rw [← this]; simp

lemma kempeStep_transport (φ : G n ≃g G n) {h : Vertex n} {c d : Vertex n → Colour}
    (hk : VacancyShortFill.KempeStep (graph n) h c d) :
    VacancyShortFill.KempeStep (graph n) (φ h) (transport φ c) (transport φ d) := by
  classical
  obtain ⟨A, B, S, hAB, ⟨s, hs, hmem⟩, rfl⟩ := hk
  have hact : ∀ y, VacancyShortFill.Active (φ h) (transport φ c) A B (φ y) ↔
      VacancyShortFill.Active h c A B y := by
    intro y
    simp [VacancyShortFill.Active, transport]
  have hadj : ∀ y z, (VacancyShortFill.pairGraph (graph n) (φ h) (transport φ c) A B).Adj
      (φ y) (φ z) ↔ (VacancyShortFill.pairGraph (graph n) h c A B).Adj y z := by
    intro y z
    constructor
    · rintro ⟨e, hy, hz⟩
      exact ⟨(φ.map_rel_iff').mp e, (hact y).mp hy, (hact z).mp hz⟩
    · rintro ⟨e, hy, hz⟩
      exact ⟨(φ.map_rel_iff').mpr e, (hact y).mpr hy, (hact z).mpr hz⟩
  have fwd : ∀ y z, (VacancyShortFill.pairGraph (graph n) h c A B).Reachable y z →
      (VacancyShortFill.pairGraph (graph n) (φ h) (transport φ c) A B).Reachable (φ y) (φ z) := by
    intro y z r
    exact r.map ⟨φ, fun {y z} e => (hadj y z).mpr e⟩
  have bwd : ∀ y z, (VacancyShortFill.pairGraph (graph n) (φ h) (transport φ c) A B).Reachable
      (φ y) (φ z) → (VacancyShortFill.pairGraph (graph n) h c A B).Reachable y z := by
    intro y z r
    have := r.map (⟨φ.symm, fun {p q} e => by
      have e' : (VacancyShortFill.pairGraph (graph n) (φ h) (transport φ c) A B).Adj
          (φ (φ.symm p)) (φ (φ.symm q)) := by simpa using e
      exact (hadj _ _).mp e'⟩ :
        (VacancyShortFill.pairGraph (graph n) (φ h) (transport φ c) A B) →g
          (VacancyShortFill.pairGraph (graph n) h c A B))
    simpa using this
  refine ⟨A, B, φ '' S, hAB, ⟨φ s, (hact s).mpr hs, fun x => ?_⟩, ?_⟩
  · obtain ⟨y, rfl⟩ := φ.surjective x
    rw [φ.injective.mem_set_image, hmem y]
    exact ⟨fwd _ _, bwd _ _⟩
  · funext x
    obtain ⟨y, rfl⟩ := φ.surjective x
    by_cases hy : y ∈ S
    · have hy' : φ y ∈ φ '' S := ⟨y, hy, rfl⟩
      rw [VacancyShortFill.swap_in hy'] 
      simp only [transport, RelIso.symm_apply_apply]
      rw [VacancyShortFill.swap_in hy]
    · have hy' : φ y ∉ φ '' S := fun h' => hy (φ.injective.mem_set_image.mp h')
      rw [VacancyShortFill.swap_out hy']
      simp only [transport, RelIso.symm_apply_apply]
      rw [VacancyShortFill.swap_out hy]

lemma mixedStep_transport (φ : G n ≃g G n) {s t : State n}
    (st : VacancyShortFill.MixedStep (graph n) s t) :
    VacancyShortFill.MixedStep (graph n) (φ s.1, transport φ s.2) (φ t.1, transport φ t.2) := by
  cases st with
  | kempe hk => exact .kempe (kempeStep_transport φ hk)
  | @slide h x c adj uniq =>
    have this : VacancyShortFill.MixedStep (graph n) (φ h, transport φ c)
        (φ x, slide (φ h) (φ x) (transport φ c)) :=
      VacancyShortFill.MixedStep.slide ((φ.map_rel_iff').mpr adj) (uniqueAt_transport φ uniq)
    rw [← transport_slide φ h x c] at this
    exact this

lemma mixedPath_transport (φ : G n ≃g G n) {k : ℕ} {s t : State n}
    (p : VacancyShortFill.MixedPath (graph n) k s t) :
    VacancyShortFill.MixedPath (graph n) k (φ s.1, transport φ s.2) (φ t.1, transport φ t.2) := by
  induction p with
  | nil s => exact .nil _
  | cons st _ ih => exact .cons (mixedStep_transport φ st) ih

/-- **The belt theorem at the pole `b`**, via the ring swap. -/
theorem pole_b_complete (hn : 5 ≤ n) (c : Vertex n → Colour)
    (hc : ProperOff (graph n) b c) :
    ∃ k, k ≤ 6 * n ∧ ∃ t : State n, VacancyShortFill.MixedPath (graph n) k (b, c) t ∧
      Filled t ∧ ProperOff (graph n) t.1 t.2 := by
  have : NeZero n := ⟨by omega⟩
  let φ : G n ≃g G n := ringSwap
  have hφb : φ b = a := rfl
  have hc' : ProperOff (graph n) a (transport φ c) := by
    have := properOff_transport φ hc
    rwa [hφb] at this
  obtain ⟨k, hk, t, p, hf, hp⟩ := pole_a_complete hn _ hc'
  have q := mixedPath_transport φ.symm p
  have ha : φ.symm a = b := by
    rw [RelIso.symm_apply_eq]; exact hφb.symm
  have hcc : transport φ.symm (transport φ c) = c := by
    funext x; simp [transport]
  refine ⟨k, hk, (φ.symm t.1, transport φ.symm t.2), ?_,
    target_transport φ.symm hf, properOff_transport φ.symm hp⟩
  simpa only [ha, hcc] using q

/-- **The vacancy hypothesis at every hole of every `G_n`, `n ≥ 5`.**  For every vertex `h` of `G_n`
and every proper colouring of `G_n - h`, a mixed path of at most `6 n` slides and Kempe swaps
reaches a state whose hole is filled (a colour missing from its link) and whose colouring is
still proper off that hole. -/
theorem belt_theorem_all_holes (hn : 5 ≤ n) (h : Vertex n) (c : Vertex n → Colour)
    (hc : ProperOff (graph n) h c) :
    ∃ k, k ≤ 6 * n ∧ ∃ t : State n, VacancyShortFill.MixedPath (graph n) k (h, c) t ∧
      Filled t ∧ ProperOff (graph n) t.1 t.2 := by
  have : NeZero n := ⟨by omega⟩
  cases h with
  | a => exact pole_a_complete hn c hc
  | b => exact pole_b_complete hn c hc
  | u i =>
    obtain ⟨k, hk, r⟩ := belt_complete hn (u i) (isBelt_u i) c hc
    exact ⟨k, by omega, r⟩
  | v i =>
    obtain ⟨k, hk, r⟩ := belt_complete hn (v i) (isBelt_v i) c hc
    exact ⟨k, by omega, r⟩

end SimpleGraph.TwoPoleBeltPoleHole

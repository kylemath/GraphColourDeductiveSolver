import CGlueM

/-! # CGlueMerge: the label argument for merged classes (ST-123 M2, 10 Nov 2026)

`xGraph_labels_merge` proves `XLoopFree`. It is CGlue's `xGraph_labels` (κ = `xLabel`, which is label-valued), with
`admissibleX` weakened to `admissibleXM` and `XRingSimple` replaced by three facts about the occurrence:
- `RingCoh`: touched ring positions folded onto one vertex carry one label. This replaces `xLabel_ring`'s use of
  `XRingSimple`.
- `RingD1`: a kept ring neighbour `s` of `a` is not folded onto a touched position of `a`'s class. This replaces
  CGlue:617.
- `NoClassChord`: no T-edge joins two touched positions of one class. This replaces the distinct-label clause in
  the G-edge case (CGlue:635).

All three are discharged per key in `C2o126Glue.lean`.
No `sorry`. -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyIcosahedral DCheck DCheck.R2

variable {n : ℕ} {T G : SphericalMap n} {ρ : ℕ → Fin n}

/-- Touched ring positions folded together carry one label. -/
def RingCoh (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n) : Prop :=
  ∀ s t, s < cf.r → t < cf.r → (∃ a, (s, a) ∈ eqR) → (∃ a, (t, a) ∈ eqR) → ρ s = ρ t →
    lbl.getD (cf.m + s) 0 = lbl.getD (cf.m + t) 0

/-- A kept ring neighbour `s` of `a` is not folded onto another touched position `t` of `a`'s class. -/
def RingD1 (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) (ρ : ℕ → Fin n) : Prop :=
  ∀ (a : Fin cf.m) s t, ringAdjOf cf a s = true → eqR.contains (s, a.val) = false → s < cf.r →
    t < cf.r → s ≠ t → (∃ b, (t, b) ∈ eqR) → lbl.getD (cf.m + t) 0 = lbl.getD a.val 0 → ρ s ≠ ρ t

/-- No T-edge between two touched ring positions of one class. -/
def NoClassChord (T : SphericalMap n) (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ)
    (ρ : ℕ → Fin n) : Prop :=
  ∀ s t, s < cf.r → t < cf.r → (∃ a, (s, a) ∈ eqR) → (∃ a, (t, a) ∈ eqR) →
    lbl.getD (cf.m + s) 0 = lbl.getD (cf.m + t) 0 → ¬ T.Adj (ρ s) (ρ t)

/-- `xLabel` at a touched ring vertex, under `RingCoh` in place of `XRingSimple`. -/
theorem xLabelM_ring (cf : Conf) (eqR : List (ℕ × ℕ)) (lbl : List ℕ) {ρ : ℕ → Fin n}
    {ι : Fin cf.m → Fin n} (hoff : ∀ t a, ρ t ≠ ι a) (hcoh : RingCoh cf eqR lbl ρ) (t : ℕ)
    (ht : t < cf.r) (htouch : ∃ a, (t, a) ∈ eqR) :
    xLabel cf eqR lbl ρ ι (ρ t) = .inl (lbl.getD (cf.m + t) 0) := by
  have h0 : ¬ ∃ a : Fin cf.m, ι a = ρ t := fun ⟨a, ha⟩ => hoff t a ha.symm
  have h' : ∃ t', t' < cf.r ∧ (∃ a, (t', a) ∈ eqR) ∧ ρ t' = ρ t := ⟨t, ht, htouch, rfl⟩
  unfold xLabel
  rw [dif_neg h0, dif_pos h']
  obtain ⟨ht', hta, he⟩ := Classical.choose_spec h'
  rw [hcoh _ t ht' ht hta htouch he]

/-- **C4b for merged classes.** -/
theorem ConfigOccW.xGraph_labels_merge (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ)
    (hadm : admissibleXM cf eqR eqI lbl = true) (hloop : ∀ a, intAdjOf cf a a = false)
    {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hcoh : RingCoh cf eqR lbl ρ) (hD1 : RingD1 cf eqR lbl ρ)
    (hch : NoClassChord T cf eqR lbl ρ) :
    XLoopFree cf eqR eqI ρ ι G := by
  classical
  simp only [admissibleXM, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true,
    Array.all_eq_true, List.mem_range, Bool.or_eq_true, beq_iff_eq] at hadm
  obtain ⟨⟨⟨⟨⟨hA1, -⟩, -⟩, hAR⟩, hAI⟩, hAm⟩ := hadm
  set H := xGraph cf eqR eqI ρ ι with hH
  set Λ := xLabel cf eqR lbl ρ ι with hΛ
  have hRing : ∀ (a : Fin cf.m) t, ringAdjOf cf a t = true → t < cf.r ∧
      (eqR.contains (t, a.val) = true → lbl.getD a.val 0 = lbl.getD (cf.m + t) 0) ∧
      (¬ eqR.contains (t, a.val) = true → lbl.getD a.val 0 ≠ lbl.getD (cf.m + t) 0) := by
    intro a t hat
    obtain ⟨i, hi, rfl⟩ := Array.mem_iff_getElem.1 (of_decide_eq_true hat)
    have := (hAm a.val a.isLt).1 i hi
    exact ⟨this.1, ite_beq_spec this.2⟩
  have hInt : ∀ a b : Fin cf.m, intAdjOf cf a b = true →
      ((eqI.contains (b.val, a.val) = true ∨ eqI.contains (a.val, b.val) = true) →
        lbl.getD a.val 0 = lbl.getD b.val 0) ∧
      (¬ (eqI.contains (b.val, a.val) = true ∨ eqI.contains (a.val, b.val) = true) →
        lbl.getD a.val 0 ≠ lbl.getD b.val 0) := by
    intro a b hab
    obtain ⟨i, hi, hb⟩ := Array.mem_iff_getElem.1 (of_decide_eq_true hab)
    have := (hAm a.val a.isLt).2 i hi
    rw [hb] at this
    exact ite_beq_spec this.2
  have htouch : ∀ (a : Fin cf.m) t, eqR.contains (t, a.val) = true → ∃ a', (t, a') ∈ eqR :=
    fun a t h => ⟨a.val, by simpa using h⟩
  have hadj : ∀ x y, H.Adj x y → Λ x = Λ y := by
    have one : ∀ x y, ((∃ (a : Fin cf.m) (t : ℕ), ringAdjOf cf a t = true ∧
        eqR.contains (t, a.val) = true ∧ x = ι a ∧ y = ρ t) ∨
        (∃ a b : Fin cf.m, intAdjOf cf a b = true ∧
          (eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = true ∧
          x = ι a ∧ y = ι b)) → Λ x = Λ y := by
      rintro x y (⟨a, t, hat, h, rfl, rfl⟩ | ⟨a, b, hab, h, rfl, rfl⟩)
      · obtain ⟨htr, heq, -⟩ := hRing a t hat
        rw [hΛ, xLabel_int cf eqR lbl ρ O.ιinj,
          xLabelM_ring cf eqR lbl O.ringOff hcoh t htr (htouch a t h), heq h]
      · rw [hΛ, xLabel_int cf eqR lbl ρ O.ιinj, xLabel_int cf eqR lbl ρ O.ιinj,
          (hInt a b hab).1 (by simpa using h)]
    intro x y hxy
    rw [hH, xGraph, SimpleGraph.fromRel_adj] at hxy
    rcases hxy.2 with h | h
    · exact one x y h
    · exact (one y x h).symm
  have hreach : ∀ x y, H.Reachable x y → Λ x = Λ y := by
    rintro x y ⟨p⟩
    induction p with
    | nil => rfl
    | cons h _ ih => exact (hadj _ _ h).trans ih
  have hoffL : ∀ v, (∀ a, v ≠ ι a) →
      (∃ t, t < cf.r ∧ (∃ a, (t, a) ∈ eqR) ∧ ρ t = v ∧ Λ v = .inl (lbl.getD (cf.m + t) 0)) ∨
      Λ v = .inr v.val := by
    intro v hv
    by_cases h1 : ∃ t, t < cf.r ∧ (∃ a, (t, a) ∈ eqR) ∧ ρ t = v
    · obtain ⟨t, ht, htc, rfl⟩ := h1
      exact Or.inl ⟨t, ht, htc, rfl, xLabelM_ring cf eqR lbl O.ringOff hcoh t ht htc⟩
    · exact Or.inr (xLabel_fresh cf eqR lbl ρ ι v (fun ⟨a, ha⟩ => hv a ha.symm) h1)
  refine ⟨?_, ?_, ?_, ?_⟩
  · -- an X-edge exists (verbatim from `xGraph_labels`)
    by_cases hR0 : eqR = []
    · have hI0 : eqI ≠ [] := by
        intro h; rw [hR0, h] at hA1; simp at hA1
      obtain ⟨⟨b, a⟩, hp⟩ := List.exists_mem_of_ne_nil eqI hI0
      obtain ⟨⟨ha, hb⟩, hc⟩ := hAI _ hp
      have hab : intAdjOf cf ⟨a, ha⟩ ⟨b, hb⟩ = true := decide_eq_true (by simpa using hc)
      refine ⟨ι ⟨a, ha⟩, ι ⟨b, hb⟩, ?_⟩
      rw [xGraph, SimpleGraph.fromRel_adj]
      refine ⟨fun e => ?_, Or.inl (Or.inr ⟨⟨a, ha⟩, ⟨b, hb⟩, hab, by simp [hp], rfl, rfl⟩)⟩
      have := O.ιinj e
      rw [← this, hloop] at hab
      exact Bool.false_ne_true hab
    · obtain ⟨⟨t, a⟩, hp⟩ := List.exists_mem_of_ne_nil eqR hR0
      obtain ⟨ha, hc⟩ := hAR _ hp
      have hat : ringAdjOf cf ⟨a, ha⟩ t = true := decide_eq_true (by simpa using hc)
      refine ⟨ι ⟨a, ha⟩, ρ t, ?_⟩
      rw [xGraph, SimpleGraph.fromRel_adj]
      exact ⟨fun e => O.ringOff t _ e.symm,
        Or.inl (Or.inl ⟨⟨a, ha⟩, t, hat, by simp [hp], rfl, rfl⟩)⟩
  · -- a listed ring edge outside X: the touched position met is `t` itself (labels) or another (`RingD1`)
    intro a t hat h hr
    have e := hreach _ _ hr
    obtain ⟨htr, -, hne⟩ := hRing a t hat
    rw [hΛ, xLabel_int cf eqR lbl ρ O.ιinj] at e
    rcases hoffL (ρ t) (fun b => O.ringOff t b) with ⟨t', ht', htc, he, hl⟩ | hl
    · rw [← hΛ, hl] at e
      have hl' : lbl.getD (cf.m + t') 0 = lbl.getD a.val 0 := (Sum.inl_injective e).symm
      by_cases htt : t = t'
      · subst htt
        exact hne (fun h' => by rw [h] at h'; exact Bool.false_ne_true h') hl'.symm
      · exact hD1 a t t' hat h htr ht' htt htc hl' he.symm
    · rw [← hΛ, hl] at e
      exact Sum.inl_ne_inr e
  · -- a listed interior edge outside X (verbatim)
    intro a b hab h hr
    have e := hreach _ _ hr
    rw [hΛ, xLabel_int cf eqR lbl ρ O.ιinj, xLabel_int cf eqR lbl ρ O.ιinj] at e
    exact (hInt a b hab).2 (by simpa using h) (Sum.inl_injective e).symm
  · -- an edge of G: two touched positions of one class would be a chord (`NoClassChord`)
    intro x y hxy hr
    have e := hreach _ _ hr
    obtain ⟨hT, hx, hy⟩ := (O.hG x y).1 hxy
    have hne : x ≠ y := G.graph.ne_of_adj hxy
    rcases hoffL x hx with ⟨s, hs', hsc, rfl, hlx⟩ | hlx <;>
      rcases hoffL y hy with ⟨t, ht', htc, rfl, hly⟩ | hly <;> rw [hlx, hly] at e
    · exact hch s t hs' ht' hsc htc (Sum.inl_injective e) hT
    · exact Sum.inl_ne_inr e
    · exact Sum.inr_ne_inl e
    · exact hne (Fin.ext (Sum.inr_injective e))

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.xLabelM_ring
#print axioms SimpleGraph.SphericalMap.ConfigOccW.xGraph_labels_merge

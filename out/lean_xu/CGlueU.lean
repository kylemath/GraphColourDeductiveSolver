import CGlue

/-! # CGlueU: the C glue with the `|X| ≤ 4` cap lifted (LT-XU, Studio, 22 Oct 2026)

`admissibleXU` is `admissibleX` without the conjunct `decide (eqR.length + eqI.length ≤ 4)`. That conjunct is unused in CGlue:
both lemmas that destructure `admissibleX` (`xGraph_labels`, `xGraph_labels_fold`) discard it, and `contract_reducer_of` never
unfolds `hadm`. The declarations below are CGlue's, copied verbatim (generated from CGlue.lean), with `hadm : admissibleXU` and
one fewer discarded conjunct in the `obtain` pattern. Nothing in CGlue is changed. -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill VacancyIcosahedral DCheck DCheck.R2

variable {n : ℕ} {T G : SphericalMap n} {ρ : ℕ → Fin n}
variable {m : ℕ}

/-- **Local admissibility without the size cap** (as `admissibleX`, minus `|X| ≤ 4`). -/
def admissibleXU (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ) : Bool :=
  let L : ℕ → ℕ := fun i => lbl.getD i 0
  decide (1 ≤ eqR.length + eqI.length) &&
  decide (lbl.length = cf.m + cf.r) &&
  eqR.all (fun p => decide (p.2 < cf.m) && (cf.ringAdj[p.2]!).contains p.1) &&
  eqI.all (fun p => decide (p.2 < cf.m) && decide (p.1 < cf.m) && (cf.intAdj[p.2]!).contains p.1) &&
  (List.range cf.m).all (fun a =>
    (cf.ringAdj[a]!).all (fun t => decide (t < cf.r) &&
      (if eqR.contains (t, a) then L a == L (cf.m + t) else L a != L (cf.m + t))) &&
    (cf.intAdj[a]!).all (fun b => decide (b < cf.m) &&
      (if eqI.contains (b, a) || eqI.contains (a, b) then L a == L b else L a != L b))) &&
  (List.range cf.r).all (fun s => (List.range cf.r).all (fun t =>
    s == t || L (cf.m + s) != L (cf.m + t)))


theorem admissibleXU_of_admissibleX (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ)
    (h : admissibleX cf eqR eqI lbl = true) : admissibleXU cf eqR eqI lbl = true := by
  simp only [admissibleX, admissibleXU, Bool.and_eq_true] at h ⊢
  tauto

theorem ConfigOccW.xGraph_labelsU (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ)
    (hadm : admissibleXU cf eqR eqI lbl = true) (hloop : ∀ a, intAdjOf cf a a = false)
    {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hs : XRingSimple eqR cf.r ρ) :
    (∃ x y, (xGraph cf eqR eqI ρ ι).Adj x y) ∧
    (∀ (a : Fin cf.m) t, ringAdjOf cf a t = true → eqR.contains (t, a.val) = false →
      ¬ (xGraph cf eqR eqI ρ ι).Reachable (ι a) (ρ t)) ∧
    (∀ a b : Fin cf.m, intAdjOf cf a b = true →
      (eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = false →
      ¬ (xGraph cf eqR eqI ρ ι).Reachable (ι b) (ι a)) ∧
    (∀ x y, G.Adj x y → ¬ (xGraph cf eqR eqI ρ ι).Reachable x y) := by
  classical
  simp only [admissibleXU, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true,
    Array.all_eq_true, List.mem_range, Bool.or_eq_true, beq_iff_eq] at hadm
  obtain ⟨⟨⟨⟨⟨hA1, -⟩, hAR⟩, hAI⟩, hAm⟩, hArg⟩ := hadm
  set H := xGraph cf eqR eqI ρ ι with hH
  set Λ := xLabel cf eqR lbl ρ ι with hΛ
  -- the label facts at listed ring and interior edges
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
  -- Λ is constant along X-edges, hence on X-components
  have hadj : ∀ x y, H.Adj x y → Λ x = Λ y := by
    have one : ∀ x y, ((∃ (a : Fin cf.m) (t : ℕ), ringAdjOf cf a t = true ∧
        eqR.contains (t, a.val) = true ∧ x = ι a ∧ y = ρ t) ∨
        (∃ a b : Fin cf.m, intAdjOf cf a b = true ∧
          (eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = true ∧
          x = ι a ∧ y = ι b)) → Λ x = Λ y := by
      rintro x y (⟨a, t, hat, h, rfl, rfl⟩ | ⟨a, b, hab, h, rfl, rfl⟩)
      · obtain ⟨htr, heq, -⟩ := hRing a t hat
        rw [hΛ, xLabel_int cf eqR lbl ρ O.ιinj,
          xLabel_ring cf eqR lbl O.ringOff hs t htr (htouch a t h), heq h]
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
  -- Λ at a vertex off the interior
  have hoffL : ∀ v, (∀ a, v ≠ ι a) →
      (∃ t, t < cf.r ∧ (∃ a, (t, a) ∈ eqR) ∧ ρ t = v ∧ Λ v = .inl (lbl.getD (cf.m + t) 0)) ∨
      Λ v = .inr v.val := by
    intro v hv
    by_cases h1 : ∃ t, t < cf.r ∧ (∃ a, (t, a) ∈ eqR) ∧ ρ t = v
    · obtain ⟨t, ht, htc, rfl⟩ := h1
      exact Or.inl ⟨t, ht, htc, rfl, xLabel_ring cf eqR lbl O.ringOff hs t ht htc⟩
    · exact Or.inr (xLabel_fresh cf eqR lbl ρ ι v (fun ⟨a, ha⟩ => hv a ha.symm) h1)
  refine ⟨?_, ?_, ?_, ?_⟩
  · -- an X-edge exists
    by_cases hR0 : eqR = []
    · have hI0 : eqI ≠ [] := by
        intro h; rw [hR0, h] at hA1; simp at hA1
      obtain ⟨⟨b, a⟩, hp⟩ := List.exists_mem_of_ne_nil eqI hI0
      obtain ⟨⟨ha, hb⟩, hc⟩ := hAI _ hp
      have hab : intAdjOf cf ⟨a, ha⟩ ⟨b, hb⟩ = true := decide_eq_true (by simpa using hc)
      refine ⟨ι ⟨a, ha⟩, ι ⟨b, hb⟩, ?_⟩
      rw [hH, xGraph, SimpleGraph.fromRel_adj]
      refine ⟨fun e => ?_, Or.inl (Or.inr ⟨⟨a, ha⟩, ⟨b, hb⟩, hab, by simp [hp], rfl, rfl⟩)⟩
      have := O.ιinj e
      rw [← this, hloop] at hab
      exact Bool.false_ne_true hab
    · obtain ⟨⟨t, a⟩, hp⟩ := List.exists_mem_of_ne_nil eqR hR0
      obtain ⟨ha, hc⟩ := hAR _ hp
      have hat : ringAdjOf cf ⟨a, ha⟩ t = true := decide_eq_true (by simpa using hc)
      refine ⟨ι ⟨a, ha⟩, ρ t, ?_⟩
      rw [hH, xGraph, SimpleGraph.fromRel_adj]
      exact ⟨fun e => O.ringOff t _ e.symm,
        Or.inl (Or.inl ⟨⟨a, ha⟩, t, hat, by simp [hp], rfl, rfl⟩)⟩
  · -- a listed ring edge outside X
    intro a t hat h hr
    have e := hreach _ _ hr
    obtain ⟨htr, -, hne⟩ := hRing a t hat
    rw [hΛ, xLabel_int cf eqR lbl ρ O.ιinj] at e
    rcases hoffL (ρ t) (fun b => O.ringOff t b) with ⟨t', ht', htc, he, hl⟩ | hl
    · rw [← hΛ, hl] at e
      have : t = t' := hs t' _ htc.choose_spec ht' t htr he.symm
      subst this
      exact hne (fun h' => by rw [h] at h'; exact Bool.false_ne_true h') (Sum.inl_injective e)
    · rw [← hΛ, hl] at e
      exact Sum.inl_ne_inr e
  · -- a listed interior edge outside X
    intro a b hab h hr
    have e := hreach _ _ hr
    rw [hΛ, xLabel_int cf eqR lbl ρ O.ιinj, xLabel_int cf eqR lbl ρ O.ιinj] at e
    exact (hInt a b hab).2 (by simpa using h) (Sum.inl_injective e).symm
  · -- an edge of G
    intro x y hxy hr
    have e := hreach _ _ hr
    obtain ⟨-, hx, hy⟩ := (O.hG x y).1 hxy
    have hne : x ≠ y := G.graph.ne_of_adj hxy
    rcases hoffL x hx with ⟨s, hs', -, rfl, hlx⟩ | hlx <;>
      rcases hoffL y hy with ⟨t, ht', -, rfl, hly⟩ | hly <;> rw [hlx, hly] at e
    · have hst : s ≠ t := fun h => hne (by rw [h])
      rcases hArg s hs' t ht' with h | h
      · exact hst h
      · exact (by simpa using h : lbl.getD (cf.m + s) 0 ≠ lbl.getD (cf.m + t) 0) (Sum.inl_injective e)
    · exact Sum.inl_ne_inr e
    · exact Sum.inr_ne_inl e
    · exact hne (Fin.ext (Sum.inr_injective e))


theorem ConfigOccW.contract_reducer_ofU (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ)
    (hadm : admissibleXU cf eqR eqI lbl = true)
    (hloop : ∀ a, intAdjOf cf a a = false)
    (hrr : ∀ a, a < cf.m → ∀ t ∈ cf.ringAdj[a]!, t < cf.r) {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hex : OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hlab : XLoopFree cf eqR eqI ρ ι G)
    (hcon : ∀ H : SimpleGraph (Fin n), H = xGraph cf eqR eqI ρ ι → H ≤ T.graph →
      (∃ x y, H.Adj x y) → ∃ (T' : SphericalMap n) (π : Fin n → Fin n),
        Nat.card T'.graph.support < Nat.card T.graph.support ∧
        (∀ x y, H.Reachable x y → π x = π y) ∧
        (∀ x y, T.Adj x y → ¬ H.Reachable x y → T'.Adj (π x) (π y))) :
    ∃ (T' : SphericalMap n) (π : Fin n → Fin n),
      Nat.card T'.graph.support < Nat.card T.graph.support ∧
      (∀ x y, G.Adj x y → T'.Adj (π x) (π y)) ∧
      (∀ (a : Fin cf.m) t, ringAdjOf cf a t = true →
        (eqR.contains (t, a.val) = true → π (ι a) = π (ρ t)) ∧
        (eqR.contains (t, a.val) = false → T'.Adj (π (ι a)) (π (ρ t)))) ∧
      (∀ a b : Fin cf.m, intAdjOf cf a b = true →
        ((eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = true →
          π (ι b) = π (ι a)) ∧
        ((eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = false →
          T'.Adj (π (ι b)) (π (ι a)))) := by
  classical
  have hlt : ∀ (a : Fin cf.m) t, ringAdjOf cf a t = true → t < cf.r :=
    fun a t hat => hrr a.val a.isLt t (of_decide_eq_true hat)
  have hXR : ∀ (a : Fin cf.m) t, ringAdjOf cf a t = true → eqR.contains (t, a.val) = true →
      (xGraph cf eqR eqI ρ ι).Adj (ι a) (ρ t) := by
    intro a t hat h
    rw [xGraph, SimpleGraph.fromRel_adj]
    exact ⟨fun e => O.ringOff t a e.symm, Or.inl (Or.inl ⟨a, t, hat, h, rfl, rfl⟩)⟩
  have hXI : ∀ a b : Fin cf.m, intAdjOf cf a b = true →
      (eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = true →
      (xGraph cf eqR eqI ρ ι).Adj (ι b) (ι a) := by
    intro a b hab h
    rw [xGraph, SimpleGraph.fromRel_adj]
    refine ⟨fun e => ?_, Or.inr (Or.inr ⟨a, b, hab, h, rfl, rfl⟩)⟩
    have hba : b = a := O.ιinj e
    subst hba
    rw [hloop] at hab
    exact Bool.false_ne_true hab
  have hle : xGraph cf eqR eqI ρ ι ≤ T.graph := by
    intro x y hxy
    rw [xGraph, SimpleGraph.fromRel_adj] at hxy
    obtain ⟨-, h | h⟩ := hxy
    · rcases h with ⟨a, t, hat, -, rfl, rfl⟩ | ⟨a, b, hab, -, rfl, rfl⟩
      · exact hex.2 a t (hlt a t hat) hat
      · exact hex.1 a b hab
    · rcases h with ⟨a, t, hat, -, rfl, rfl⟩ | ⟨a, b, hab, -, rfl, rfl⟩
      · exact (hex.2 a t (hlt a t hat) hat).symm
      · exact (hex.1 a b hab).symm
  obtain ⟨hne, hnR, hnI, hnG⟩ := hlab
  obtain ⟨T', π, hcard, hπ, hkeep⟩ := hcon _ rfl hle hne
  refine ⟨T', π, hcard, fun x y hxy => hkeep x y ((O.hG x y).1 hxy).1 (hnG x y hxy),
    fun a t hat => ⟨fun h => hπ _ _ (hXR a t hat h).reachable,
      fun h => hkeep _ _ (hex.2 a t (hlt a t hat) hat) (hnR a t hat h)⟩,
    fun a b hab => ⟨fun h => hπ _ _ (hXI a b hab h).reachable,
      fun h => hkeep _ _ (hex.1 a b hab).symm (hnI a b hab h)⟩⟩


theorem ConfigOccW.xGraph_labels_foldU (cf : Conf) (eqR eqI : List (ℕ × ℕ)) (lbl : List ℕ)
    (hadm : admissibleXU cf eqR eqI lbl = true) (hsafe : foldSafeX cf eqR eqI lbl = true)
    (hloop : ∀ a, intAdjOf cf a a = false) {ι : Fin cf.m → Fin n}
    (O : ConfigOccW T G cf.r cf.m ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hex : OccExact T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (hNI : NbrInj cf.r ρ (ringAdjOf cf)) (hCN : CommonNbr T cf.r ρ ι (intAdjOf cf) (ringAdjOf cf))
    (htri : T.Triangulated) (hNS : ClaimGlue.NoShortSepCycle T) :
    XLoopFree cf eqR eqI ρ ι G := by
  classical
  have hX := hadm
  simp only [admissibleXU, Bool.and_eq_true, decide_eq_true_eq, List.all_eq_true,
    Array.all_eq_true, List.mem_range, Bool.or_eq_true, beq_iff_eq] at hadm
  obtain ⟨⟨⟨⟨⟨hA1, -⟩, hAR⟩, hAI⟩, hAm⟩, hArg⟩ := hadm
  have hArg' : ∀ s t, s < cf.r → t < cf.r →
      s = t ∨ lbl.getD (cf.m + s) 0 ≠ lbl.getD (cf.m + t) 0 := by
    intro s t hs ht
    rcases hArg s hs t ht with h | h
    · exact Or.inl h
    · exact Or.inr (by simpa using h)
  simp only [foldSafeX, Bool.and_eq_true, List.all_eq_true, Array.all_eq_true, List.mem_range,
    Bool.or_eq_true, beq_iff_eq, Bool.not_eq_true', bne_iff_ne, ne_eq] at hsafe
  set H := xGraph cf eqR eqI ρ ι with hH
  set κ := xKappa cf eqR lbl ρ ι with hκ
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
  have hexcl := fun {p q : ℕ} => excl_sound cf O hex hNI hCN (p := p) (q := q)
  have hcyc := fun {p q : ℕ} => cycEx_sound cf O hex hCN hloop htri hNS (p := p) (q := q)
  -- κ is constant along X-edges, hence on X-components
  have hadj : ∀ x y, H.Adj x y → κ x = κ y := by
    have one : ∀ x y, ((∃ (a : Fin cf.m) (t : ℕ), ringAdjOf cf a t = true ∧
        eqR.contains (t, a.val) = true ∧ x = ι a ∧ y = ρ t) ∨
        (∃ a b : Fin cf.m, intAdjOf cf a b = true ∧
          (eqI.contains (b.val, a.val) || eqI.contains (a.val, b.val)) = true ∧
          x = ι a ∧ y = ι b)) → κ x = κ y := by
      rintro x y (⟨a, t, hat, h, rfl, rfl⟩ | ⟨a, b, hab, h, rfl, rfl⟩)
      · obtain ⟨htr, heq, -⟩ := hRing a t hat
        have htt : touchedB eqR t = true := touchedB_of_mem (by simpa using h)
        rw [hκ, xKappa_int cf eqR lbl ρ O.ιinj, heq h, kInt_touched cf eqR lbl ρ hArg' htr htt]
        rcases xKappa_off cf eqR lbl ρ ι (v := ρ t) (fun b => O.ringOff t b) with ⟨-, e⟩ | ⟨hn, -⟩
        · exact e.symm
        · exact absurd ⟨t, htr, htt, rfl⟩ hn
      · rw [hκ, xKappa_int cf eqR lbl ρ O.ιinj, xKappa_int cf eqR lbl ρ O.ιinj,
          (hInt a b hab).1 (by simpa using h)]
    intro x y hxy
    rw [hH, xGraph, SimpleGraph.fromRel_adj] at hxy
    rcases hxy.2 with h | h
    · exact one x y h
    · exact (one y x h).symm
  have hreach : ∀ x y, H.Reachable x y → κ x = κ y := by
    rintro x y ⟨p⟩
    induction p with
    | nil => rfl
    | cons h _ ih => exact (hadj _ _ h).trans ih
  refine ⟨?_, ?_, ?_, ?_⟩
  · -- an X-edge exists (as in `xGraph_labels`)
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
  · -- a listed ring edge outside X (D1)
    intro a s hat h hr
    have e := hreach _ _ hr
    obtain ⟨hsr, -, hne⟩ := hRing a s hat
    have hne' : lbl.getD a.val 0 ≠ lbl.getD (cf.m + s) 0 :=
      hne (fun h' => by rw [h] at h'; exact Bool.false_ne_true h')
    rw [hκ, xKappa_int cf eqR lbl ρ O.ιinj] at e
    rcases xKappa_off cf eqR lbl ρ ι (v := ρ s) (fun b => O.ringOff s b) with ⟨-, hl⟩ | ⟨-, hl⟩
    · rw [hl] at e
      rcases kInt_cases cf eqR lbl ρ (lbl.getD a.val 0) with ⟨t, ht, htt, hlt, hk⟩ | hk
      · rw [hk] at e
        have hρ : ρ t = ρ s := Sum.inl_injective e
        have hst : s ≠ t := fun h' => hne' (by rw [← hlt, h'])
        -- the D1 check
        obtain ⟨i, hi, hsi⟩ := Array.mem_iff_getElem.1 (of_decide_eq_true hat)
        have hD1 := ((hsafe a.val a.isLt).1 i hi)
        rw [hsi] at hD1
        rcases hD1 with hD1 | hD1
        · rw [h] at hD1; exact Bool.false_ne_true hD1
        · rcases hD1 t ht with (((h1 | h1) | h1) | h1) | h1
          · exact absurd htt (by simp [h1])
          · exact h1 hlt
          · exact hst h1
          · exact hexcl hsr ht hst h1 hρ.symm
          · exact hcyc hsr ht h1 hρ.symm
      · rw [hk] at e; exact Sum.inr_ne_inl e
    · rw [hl] at e
      rcases kInt_cases cf eqR lbl ρ (lbl.getD a.val 0) with ⟨t, -, -, -, hk⟩ | hk <;>
        rw [hk] at e
      · exact Sum.inl_ne_inr e
      · exact (Sum.inl_ne_inr (Sum.inr_injective e))
  · -- a listed interior edge outside X (D2)
    intro a b hab h hr
    have e := hreach _ _ hr
    have hne : lbl.getD a.val 0 ≠ lbl.getD b.val 0 := (hInt a b hab).2 (by simpa using h)
    rw [hκ, xKappa_int cf eqR lbl ρ O.ιinj, xKappa_int cf eqR lbl ρ O.ιinj] at e
    rcases kInt_cases cf eqR lbl ρ (lbl.getD a.val 0) with ⟨t, ht, htt, hlt, hka⟩ | hka <;>
      rcases kInt_cases cf eqR lbl ρ (lbl.getD b.val 0) with ⟨t', ht', htt', hlt', hkb⟩ | hkb <;>
      rw [hka, hkb] at e
    · have hρ : ρ t' = ρ t := Sum.inl_injective e
      have htt'' : t ≠ t' := fun h' => hne (by rw [← hlt, ← hlt', h'])
      obtain ⟨i, hi, hbi⟩ := Array.mem_iff_getElem.1 (of_decide_eq_true hab)
      have hD2 := ((hsafe a.val a.isLt).2 i hi)
      rw [hbi] at hD2
      rcases hD2 with (hD2 | hD2) | hD2
      · exact absurd h (by rw [hD2, Bool.true_or]; decide)
      · exact absurd h (by rw [hD2, Bool.or_true]; decide)
      · rcases hD2 t ht t' ht' with ((((((h1 | h1) | h1) | h1) | h1) | h1) | h1)
        · exact absurd htt (by simp [h1])
        · exact absurd htt' (by simp [h1])
        · exact h1 hlt
        · exact h1 hlt'
        · exact htt'' h1
        · exact hexcl ht ht' htt'' h1 hρ.symm
        · exact hcyc ht ht' h1 hρ.symm
    · exact Sum.inr_ne_inl e
    · exact Sum.inl_ne_inr e
    · exact hne (Sum.inl_injective (Sum.inr_injective e)).symm
  · -- an edge of G
    intro x y hxy hr
    have e := hreach _ _ hr
    obtain ⟨-, hx, hy⟩ := (O.hG x y).1 hxy
    have hne : x ≠ y := G.graph.ne_of_adj hxy
    rw [hκ] at e
    rcases xKappa_off cf eqR lbl ρ ι hx with ⟨-, hlx⟩ | ⟨-, hlx⟩ <;>
      rcases xKappa_off cf eqR lbl ρ ι hy with ⟨-, hly⟩ | ⟨-, hly⟩ <;> rw [hlx, hly] at e
    · exact hne (Sum.inl_injective e)
    · exact Sum.inl_ne_inr e
    · exact Sum.inr_ne_inl e
    · exact hne (Sum.inr_injective (Sum.inr_injective e))


namespace CGlue
open ClaimGlue (SmallerColorable MinimalCounterexample Internally6 DEntry OccursW)

/-- A C entry admitted through `admissibleXU` (no `|X| ≤ 4` cap). -/
structure CEntryU where
  cf : DCheck18.Conf
  /-- contracted ring–interior edges `(t, a)` -/
  eqR : List (ℕ × ℕ)
  /-- contracted interior edges `(b, a)` -/
  eqI : List (ℕ × ℕ)
  /-- admissibility certificate: a label per interior vertex, then per ring position -/
  lbl : List ℕ
  hC : cReducible18 cf eqR eqI = true
  hadm : admissibleXU (Conf.of18 cf) eqR eqI lbl = true
  hr2 : 2 ≤ cf.r
  hr : cf.r ≤ 19
  hsym : ∀ a b, intAdjOf (Conf.of18 cf) a b = true → intAdjOf (Conf.of18 cf) b a = true
  hloop : ∀ a, intAdjOf (Conf.of18 cf) a a = false
  hrr : ∀ a, a < cf.m → ∀ t ∈ cf.ringAdj[a]!, t < cf.r


/-- **C occurrence.** A face-walk occurrence (`ConfigOccW`, folds and pinches allowed) that is
exact and simple at the ring positions `X` touches. -/
def OccursCXU (e : CEntryU) (T : SphericalMap n) : Prop :=
  ∃ (G : SphericalMap n) (ρ : ℕ → Fin n) (ι : Fin e.cf.m → Fin n),
    ConfigOccW T G e.cf.r e.cf.m ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)) ∧
    OccExact T e.cf.r ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)) ∧
    XRingSimple e.eqR e.cf.r ρ

/-- **C-soundness, per entry.** An occurrence of a C entry in a map whose smaller maps are all
colourable makes it colourable: colour the contracted map `T'` (smaller, C4), pull the colouring
back along `π` (it meets the X constraints), and run the D tail on its ring code (C1–C3). -/
theorem CEntryU.colorable_of_contract (e : CEntryU) {T G : SphericalMap n} {ρ : ℕ → Fin n}
    {ι : Fin e.cf.m → Fin n}
    (O : ConfigOccW T G e.cf.r e.cf.m ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)))
    (hex : OccExact T e.cf.r ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)))
    (hlab : XLoopFree (Conf.of18 e.cf) e.eqR e.eqI ρ ι G) (IH : SmallerColorable T)
    (hcon : ∀ H : SimpleGraph (Fin n), H = xGraph (Conf.of18 e.cf) e.eqR e.eqI ρ ι →
      H ≤ T.graph → (∃ x y, H.Adj x y) → ∃ (T' : SphericalMap n) (π : Fin n → Fin n),
        Nat.card T'.graph.support < Nat.card T.graph.support ∧
        (∀ x y, H.Reachable x y → π x = π y) ∧
        (∀ x y, T.Adj x y → ¬ H.Reachable x y → T'.Adj (π x) (π y))) :
    T.graph.Colorable 4 := by
  obtain ⟨T', π, hcard, hGe, hR, hI⟩ :=
    ConfigOccW.contract_reducer_ofU (Conf.of18 e.cf) e.eqR e.eqI e.lbl e.hadm e.hloop e.hrr O hex
      hlab hcon
  obtain ⟨col⟩ := IH n T' hcard
  refine ConfigOccW.colorable_of_cReducible18 e.cf e.eqR e.eqI e.hC e.hr2 e.hr e.hsym e.hloop
    e.hrr O (c := fun x => col (π x)) (fun _ _ huv _ _ => col.valid (hGe _ _ huv))
    (fun a => col (π (ι a))) ⟨fun a t hat => ?_, fun a b hab => ?_⟩
  · exact ⟨fun h => congrArg col ((hR a t hat).1 h).symm,
      fun h => (col.valid ((hR a t hat).2 h)).symm⟩
  · exact ⟨fun h => congrArg col ((hI a b hab).1 h),
      fun h => col.valid ((hI a b hab).2 h)⟩

/-- **C-soundness, per entry** (uses C4a `contract_subgraph`). -/
theorem CEntryU.colorable (e : CEntryU) {T : SphericalMap n} (h : OccursCXU e T)
    (IH : SmallerColorable T) : T.graph.Colorable 4 := by
  obtain ⟨G, ρ, ι, O, hex, hs⟩ := h
  exact e.colorable_of_contract O hex
    (ConfigOccW.xGraph_labelsU _ e.eqR e.eqI e.lbl e.hadm e.hloop O hs) IH
    (fun H _ hle hne => contract_subgraph T H hle hne)

/-- **CGlue in ClaimGlue's form**, for this file's entries and occurrences. -/
def CGlueXU (Cs : List CEntryU) : Prop :=
  ∀ e ∈ Cs, ∀ (n : ℕ) (T : SphericalMap n), OccursCXU e T → SmallerColorable T →
    T.graph.Colorable 4

/-- **The hypothesis is a theorem.** -/
theorem cGlueXU (Cs : List CEntryU) : CGlueXU Cs :=
  fun e _ _ _ h IH => e.colorable h IH
/-- A C entry whose X-graph is fold-safe: every D1 and D2 fold is excluded, either by a length-3
cycle argument (`exclB`, using `NoSep`) or by a short cycle of length 4 or 5 whose sides are both
non-empty (`cycEx`, using `NoShortSepCycle`). -/
structure CEntryFU extends CEntryU where
  hfold : foldSafeX (Conf.of18 cf) eqR eqI lbl = true

/-- **C occurrence with folds allowed.** A face-walk occurrence that is exact, with distinct listed
ring neighbours and the configuration's own triangles on its interior edges. -/
def OccursCXFU (e : CEntryU) (T : SphericalMap n) : Prop :=
  ∃ (G : SphericalMap n) (ρ : ℕ → Fin n) (ι : Fin e.cf.m → Fin n),
    ConfigOccW T G e.cf.r e.cf.m ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)) ∧
    OccExact T e.cf.r ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf)) ∧
    NbrInj e.cf.r ρ (ringAdjOf (Conf.of18 e.cf)) ∧
    ApexFacts T e.cf.r ρ ι (intAdjOf (Conf.of18 e.cf)) (ringAdjOf (Conf.of18 e.cf))

/-- **C-soundness for fold-safe entries** (no `XRingSimple`, no `sorry`). -/
theorem CEntryFU.colorable (e : CEntryFU) {T : SphericalMap n} (htri : T.Triangulated)
    (h : OccursCXFU e.toCEntryU T) (IH : SmallerColorable T) : T.graph.Colorable 4 := by
  by_contra hcol
  have hns : NoSep T := MinimalCounterexample.noSep ⟨hcol, IH⟩ htri
  obtain ⟨G, ρ, ι, O, hex, hNI, hA⟩ := h
  exact hcol (e.toCEntryU.colorable_of_contract O hex
    (ConfigOccW.xGraph_labels_foldU _ e.eqR e.eqI e.lbl e.hadm e.hfold e.hloop O hex hNI
      (commonNbr_of_apex hns hex hA) htri (MinimalCounterexample.noShortSep ⟨hcol, IH⟩)) IH
    (fun H _ hle hne => contract_subgraph T H hle hne))

/-- **CGlue for fold-safe entries**, on triangulations. -/
def CGlueXFU (Cs : List CEntryFU) : Prop :=
  ∀ e ∈ Cs, ∀ (n : ℕ) (T : SphericalMap n), T.Triangulated → OccursCXFU e.toCEntryU T →
    SmallerColorable T → T.graph.Colorable 4

/-- **The hypothesis is a theorem** (no `sorry`). -/
theorem cGlueXFU (Cs : List CEntryFU) : CGlueXFU Cs :=
  fun e _ _ _ htri h IH => e.colorable htri h IH

end CGlue
end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.admissibleXU_of_admissibleX
#print axioms SimpleGraph.SphericalMap.ConfigOccW.xGraph_labelsU
#print axioms SimpleGraph.SphericalMap.ConfigOccW.contract_reducer_ofU
#print axioms SimpleGraph.SphericalMap.ConfigOccW.xGraph_labels_foldU
#print axioms SimpleGraph.SphericalMap.CGlue.CEntryU.colorable
#print axioms SimpleGraph.SphericalMap.CGlue.cGlueXU
#print axioms SimpleGraph.SphericalMap.CGlue.CEntryFU.colorable
#print axioms SimpleGraph.SphericalMap.CGlue.cGlueXFU

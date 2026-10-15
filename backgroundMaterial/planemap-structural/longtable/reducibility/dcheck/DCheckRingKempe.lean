import DCheckR2D
/-! Job 25 step 2: `KempeMatching` for the ring codes realised by proper colourings of any map `G`
with a ring face `ρ` and an off-ring hole `h` (no `ConfigOcc` needed). Verbatim copies of
`ConfigOcc.theta_nc` and `ConfigOcc.kempeMatching` (DCheckR2D), using only the ring and the hole. -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill DCheck DCheck.R2

variable {n : ℕ} {G : SphericalMap n} {r : ℕ} {ρ : ℕ → Fin n}

/-- **Non-crossing of ring chains** in the form used by `abstract_matching`. -/
theorem RingFace.theta_nc (R : RingFace G r ρ) {h : Fin n} (hh : ∀ t, ρ t ≠ h) {c : Fin n → Fin 4}
    (hc : ProperOff G.graph h c) {θ : ℕ} (hθ : θ < 4) {i j k l : ℕ} (hij : i < j) (hjk : j < k)
    (hkl : k < l) (hlr : l < r)
    (h1 : (thetaGraph G.graph h c θ).Reachable (ρ i) (ρ k))
    (h2 : (thetaGraph G.graph h c θ).Reachable (ρ j) (ρ l)) :
    (thetaGraph G.graph h c θ).Reachable (ρ i) (ρ j) := by
  have p1 := theta_to_pair hθ (hh i) h1
  have p2 := theta_to_pair hθ (hh j) h2
  by_cases hcl : cls θ (c (ρ i)).val = cls θ (c (ρ j)).val
  · -- same pair: chains_noncrossing_same
    by_contra hne
    have hy := (cls_eq_cases' θ hθ _ (c (ρ i)).isLt _ (c (ρ j)).isLt).1 hcl
    have hpair : pairGraph G.graph h c (c (ρ j)) (fx θ hθ (c (ρ j))) =
        pairGraph G.graph h c (c (ρ i)) (fx θ hθ (c (ρ i))) := by
      rcases hy with hy | hy
      · rw [Fin.ext hy]
      · have : c (ρ j) = fx θ hθ (c (ρ i)) := Fin.ext hy
        rw [this, fx_fx, pairGraph_comm]
    rw [hpair] at p2
    exact chains_noncrossing_same R hij hjk hkl hlr p1 p2
      (fun hr => hne (pair_to_theta hθ hc hr))
  · exfalso
    refine chains_noncrossing R (a := c (ρ i)) (b := fx θ hθ (c (ρ i)))
      (a' := c (ρ j)) (b' := fx θ hθ (c (ρ j))) ?_ hij hjk hkl hlr p1 p2
    intro z hz1 hz2
    apply disj_pairs' θ hθ _ (c (ρ i)).isLt _ (c (ρ j)).isLt _ z.isLt
    refine ⟨hcl, ?_, ?_⟩
    · rcases hz1 with rfl | rfl
      · exact Or.inl rfl
      · exact Or.inr rfl
    · rcases hz2 with rfl | rfl
      · exact Or.inl rfl
      · exact Or.inr rfl

/-- **R2: `KempeMatching`** for the ring codes of proper colourings of `G`, for the table
`matchTableN N` (`N ≤ 10`) and rings `r < 2N`. -/
theorem RingFace.kempeMatching (R : RingFace G r ρ) {h : Fin n} (hh : ∀ t, ρ t ≠ h) (cf : Conf)
    (N : ℕ) (hN : N ≤ 10) (hr : cf.r = r) (hrN : r < 2 * N) :
    KempeMatchingT (matchTableN N) cf (fun k => ∃ c : Fin n → Fin 4, ProperOff G.graph h c ∧
      k = code (ringSeq ρ c) r) := by
  classical
  intro k θ ⟨c, hc, hk⟩ hθ1 hθ3 hT
  subst hk
  rw [hr] at hT ⊢
  have hθ : θ < 4 := by omega
  set f := ringSeq ρ c with hfdef
  have hf : ∀ t, f t < 4 := ringSeq_lt ρ c
  have hr1 : 1 ≤ r := R.pos
  let E : ℕ → ℕ → Prop := fun t t' => (thetaGraph G.graph h c θ).Reachable (ρ t) (ρ t')
  have hE : Equivalence E :=
    ⟨fun _ => Reachable.refl _, fun h => h.symm, fun h1 h2 => h1.trans h2⟩
  have hstep : ∀ v, v < r → tPred r (code f r) θ v = false → E v ((v + 1) % r) := by
    intro v hv htp
    have hwrap : ρ ((v + 1) % r) = ρ (v + 1) := by
      by_cases h : v + 1 < r
      · rw [Nat.mod_eq_of_lt h]
      · rw [show v + 1 = r by omega, Nat.mod_self, show r = 0 + r by omega, R.per 0]
    unfold tPred at htp
    rw [col_code f hf r v hv, col_code f hf r _ (Nat.mod_lt _ (by omega))] at htp
    simp only [Bool.and_eq_false_iff, bne_eq_false_iff_eq] at htp
    have hne : c (ρ v) ≠ c (ρ (v + 1)) := hc (R.adj v) (hh v) (hh (v + 1))
    show (thetaGraph G.graph h c θ).Reachable (ρ v) (ρ ((v + 1) % r))
    rw [hwrap]
    rcases htp with h0 | h0
    · exfalso; apply hne; apply Fin.ext
      have : f v = f ((v + 1) % r) := by
        have := congrArg (· ^^^ f ((v + 1) % r)) h0
        simpa [Nat.xor_assoc] using this
      rw [hfdef] at this; simp only [ringSeq] at this; rw [this, hwrap]
    · refine Adj.reachable ⟨R.adj v, hh v, hh (v + 1), ?_⟩
      rw [hfdef] at h0; simp only [ringSeq] at h0; rw [hwrap] at h0; exact h0
  have hEcls : ∀ u w, u < r → w < r → E u w → cls θ (f u) = cls θ (f w) :=
    fun u w _ _ h => theta_cls hθ h
  have hNC : ∀ i j k l, i < j → j < k → k < l → l < r → E i k → E j l → E i j :=
    fun i j k l hij hjk hkl hlr h1 h2 => R.theta_nc hh hc hθ hij hjk hkl hlr h1 h2
  have hn : (TL r θ f).length ≠ 0 := by rw [← transitions_size]; exact hT
  obtain ⟨lab, hlab, hlabE⟩ := abstract_matching r θ f E hE hf hθ1 hθ3 hstep hEcls hNC hr1 N hN hrN hn
  refine ⟨lab, hlab, fun s => ?_⟩
  -- the flip
  let sel : ℕ → Bool := fun t => decide (lab[arcOf (transitions r (code f r) θ) t]! ≠ 0) &&
    s.testBit (lab[arcOf (transitions r (code f r) θ) t]! - 1)
  let S : Fin n → Prop := fun v => ∃ t, t < r ∧ sel t = true ∧
    (thetaGraph G.graph h c θ).Reachable (ρ t) v
  let c' : Fin n → Fin 4 := fun v => if S v then fx θ hθ (c v) else c v
  refine ⟨c', ?_, ?_⟩
  · intro u v huv hu hv
    have hne := hc huv hu hv
    by_cases hSu : S u <;> by_cases hSv : S v <;> simp only [c', hSu, hSv, if_true, if_false]
    · intro heq; apply hne; rw [← fx_fx θ hθ (c u), heq, fx_fx]
    · intro heq; apply hSv
      obtain ⟨t, ht, hst, hreach⟩ := hSu
      refine ⟨t, ht, hst, hreach.trans (Adj.reachable ⟨huv, hu, hv, ?_⟩)⟩
      rw [← heq]; simp [fx, ← Nat.xor_assoc]
    · intro heq; apply hSu
      obtain ⟨t, ht, hst, hreach⟩ := hSv
      refine ⟨t, ht, hst, hreach.trans (Adj.reachable ⟨huv.symm, hv, hu, ?_⟩)⟩
      rw [heq]; simp [fx, ← Nat.xor_assoc]
    · exact hne
  · have hS : ∀ t, t < r → (S (ρ t) ↔ sel t = true) := by
      intro t ht
      constructor
      · rintro ⟨t', ht', hst', hreach⟩
        have := hlabE t' t ht' ht hreach
        simp only [sel] at hst' ⊢
        rw [← this]; exact hst'
      · intro hs; exact ⟨t, ht, hs, Reachable.refl _⟩
    rw [← flip_code r θ f hf hθ lab s sel (fun t _ => rfl)]
    apply code_congr
    intro t ht
    simp only [ringSeq, c']
    by_cases hst : sel t = true
    · rw [if_pos ((hS t ht).2 hst), if_pos hst]; rfl
    · rw [if_neg (fun h => hst ((hS t ht).1 h)), if_neg hst]; rfl

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.RingFace.kempeMatching

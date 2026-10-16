import DCheckRingKempe

/-! Job 26 route B2 (exploratory): `KempeMatching` for ring walks that need not be injective.

`RingNC.kempeMatching` uses the ring only through `pos`, `per`, `adj` and the θ-form of non-crossing
(`RingNC.theta_nc`). The pairGraph field `RingNC.nc` is false for a pinched walk: `Reachable` is reflexive, so the
"chain" between two positions of the pinch vertex exists for every pair. The θ form survives.
`RingTNC` packages exactly what is used, and `RingTNC.kempeMatching` is the verbatim proof. The pinched walk's
`RingTNC` comes from its two sides; that is the lemma `RingTNC.pinch`, below. -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyShortFill DCheck DCheck.R2

variable {n : ℕ} {G : SphericalMap n} {r : ℕ} {ρ : ℕ → Fin n} {h : Fin n}

/-- Ring data in θ form; `ρ` need not be injective. -/
structure RingTNC (G : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) (h : Fin n) : Prop where
  pos : 0 < r
  per : ∀ t, ρ (t + r) = ρ t
  adj : ∀ t, G.Adj (ρ t) (ρ (t + 1))
  off : ∀ t, ρ t ≠ h
  tnc : ∀ {c : Fin n → Fin 4}, ProperOff G.graph h c → ∀ {θ : ℕ}, θ < 4 →
    ∀ {i j k l : ℕ}, i < j → j < k → k < l → l < r →
    (thetaGraph G.graph h c θ).Reachable (ρ i) (ρ k) →
    (thetaGraph G.graph h c θ).Reachable (ρ j) (ρ l) →
    (thetaGraph G.graph h c θ).Reachable (ρ i) (ρ j)

theorem RingNC.toTNC (R : RingNC G r ρ) (hh : ∀ t, ρ t ≠ h) : RingTNC G r ρ h :=
  ⟨R.pos, R.per, R.adj, hh, by
    intro c hc θ hθ i j k l hij hjk hkl hlr h1 h2
    exact R.theta_nc hh hc hθ hij hjk hkl hlr h1 h2⟩

/-- **`KempeMatching` from `RingTNC`** (verbatim `RingNC.kempeMatching`). -/
theorem RingTNC.kempeMatching (R : RingTNC G r ρ h) (cf : Conf)
    (N : ℕ) (hN : N ≤ 10) (hr : cf.r = r) (hrN : r < 2 * N) :
    KempeMatchingT (matchTableN N) cf (fun k => ∃ c : Fin n → Fin 4, ProperOff G.graph h c ∧
      k = code (ringSeq ρ c) r) := by
  classical
  have hh := R.off
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
    fun i j k l hij hjk hkl hlr h1 h2 => R.tnc hc hθ hij hjk hkl hlr h1 h2
  have hn : (TL r θ f).length ≠ 0 := by rw [← transitions_size]; exact hT
  obtain ⟨lab, hlab, hlabE⟩ := abstract_matching r θ f E hE hf hθ1 hθ3 hstep hEcls hNC hr1 N hN hrN hn
  refine ⟨lab, hlab, fun s => ?_⟩
  let sel : ℕ → Bool := fun t => decide (lab[arcOf (transitions r (code f r) θ) t]! ≠ 0) &&
    s.testBit (lab[arcOf (transitions r (code f r) θ) t]! - 1)
  let S : Fin n → Prop := fun v => ∃ t, t < r ∧ sel t = true ∧
    (thetaGraph G.graph h c θ).Reachable (ρ t) v
  let c' : Fin n → Fin 4 := fun v => if S v then fx θ hθ (c v) else c v
  refine ⟨c', ?_, ?_⟩
  · intro u v huv hu hv
    have hne := hc huv hu hv
    by_cases hSu : S u <;> by_cases hSv : S v <;> simp only [c', hSu, hSv, ite_true, ite_false]
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

/-! ## The pinch lemma -/

/-- θ-non-crossing alone (the `tnc` field). -/
def TNC (G : SphericalMap n) (r : ℕ) (ρ : ℕ → Fin n) (h : Fin n) : Prop :=
  ∀ {c : Fin n → Fin 4}, ProperOff G.graph h c → ∀ {θ : ℕ}, θ < 4 →
    ∀ {i j k l : ℕ}, i < j → j < k → k < l → l < r →
    (thetaGraph G.graph h c θ).Reachable (ρ i) (ρ k) →
    (thetaGraph G.graph h c θ).Reachable (ρ j) (ρ l) →
    (thetaGraph G.graph h c θ).Reachable (ρ i) (ρ j)

section pinch
variable {GA GB : SphericalMap n} {SA SB : Fin n → Prop} {u : Fin n}

/-- **Walk lemma at a cut vertex.** If every edge of `G` lies in side A or side B, the sides meet only at `u`, and
`GA`/`GB` are the two sides, then θ-chains of `G` decompose through `u`. -/
theorem cut_reach (hint : ∀ x, SA x → SB x → x = u)
    (hcut : ∀ x y, G.Adj x y → (SA x ∧ SA y) ∨ (SB x ∧ SB y))
    (hA : ∀ x y, G.Adj x y → SA x → SA y → GA.Adj x y)
    (hB : ∀ x y, G.Adj x y → SB x → SB y → GB.Adj x y)
    (c : Fin n → Fin 4) (θ : ℕ) {x y : Fin n} (p : (thetaGraph G.graph h c θ).Walk x y) :
    (SA x → SA y → (thetaGraph GA.graph h c θ).Reachable x y) ∧
    (SA x → SB y → (thetaGraph GA.graph h c θ).Reachable x u ∧ (thetaGraph GB.graph h c θ).Reachable u y) ∧
    (SB x → SB y → (thetaGraph GB.graph h c θ).Reachable x y) ∧
    (SB x → SA y → (thetaGraph GB.graph h c θ).Reachable x u ∧ (thetaGraph GA.graph h c θ).Reachable u y) := by
  induction p with
  | nil =>
    refine ⟨fun _ _ => Reachable.refl _, fun ha hb => ?_, fun _ _ => Reachable.refl _, fun hb ha => ?_⟩
    · rw [hint _ ha hb]; exact ⟨Reachable.refl _, Reachable.refl _⟩
    · rw [hint _ ha hb]; exact ⟨Reachable.refl _, Reachable.refl _⟩
  | @cons x x' y e p ih =>
    obtain ⟨iA, iAB, iB, iBA⟩ := ih
    obtain ⟨eG, ex, ex', eθ⟩ := e
    rcases hcut x x' eG with ⟨ax, ax'⟩ | ⟨bx, bx'⟩
    · have eA : (thetaGraph GA.graph h c θ).Reachable x x' := Adj.reachable ⟨hA x x' eG ax ax', ex, ex', eθ⟩
      refine ⟨fun _ ay => eA.trans (iA ax' ay), fun _ by' => ⟨eA.trans (iAB ax' by').1, (iAB ax' by').2⟩,
        fun bx by' => ?_, fun bx ay => ?_⟩
      · rw [hint x ax bx]; exact (iAB ax' by').2
      · have hx := hint x ax bx; subst hx
        exact ⟨Reachable.refl _, eA.trans (iA ax' ay)⟩
    · have eB : (thetaGraph GB.graph h c θ).Reachable x x' := Adj.reachable ⟨hB x x' eG bx bx', ex, ex', eθ⟩
      refine ⟨fun ax ay => ?_, fun ax by' => ?_, fun _ by' => eB.trans (iB bx' by'),
        fun _ ay => ⟨eB.trans (iBA bx' ay).1, (iBA bx' ay).2⟩⟩
      · have hx := hint x ax bx; subst hx; exact (iBA bx' ay).2
      · have hx := hint x ax bx; subst hx
        exact ⟨Reachable.refl _, eB.trans (iB bx' by')⟩

theorem thetaGraph_mono {G G' : SimpleGraph (Fin n)} (hle : ∀ x y, G.Adj x y → G'.Adj x y) (c : Fin n → Fin 4)
    (θ : ℕ) {x y : Fin n} (hr : (thetaGraph G h c θ).Reachable x y) : (thetaGraph G' h c θ).Reachable x y := by
  obtain ⟨p⟩ := hr
  induction p with
  | nil => exact Reachable.refl _
  | cons e p ih =>
    have e' : (thetaGraph G' h c θ).Adj _ _ := ⟨hle _ _ e.1, e.2.1, e.2.2.1, e.2.2.2⟩
    exact e'.reachable.trans ih

/-- **Pinch lemma.** A ring walk of `G` through the cut vertex `u` at positions `0` and `m`, whose positions
`[0, m)` lie on side A and `[m, r)` on side B, is θ-non-crossing if the two sides' arcs are. -/
theorem TNC.pinch (hint : ∀ x, SA x → SB x → x = u)
    (hcut : ∀ x y, G.Adj x y → (SA x ∧ SA y) ∨ (SB x ∧ SB y))
    (hA : ∀ x y, G.Adj x y → SA x → SA y → GA.Adj x y)
    (hB : ∀ x y, G.Adj x y → SB x → SB y → GB.Adj x y)
    (hAG : ∀ x y, GA.Adj x y → G.Adj x y) (hBG : ∀ x y, GB.Adj x y → G.Adj x y)
    {m : ℕ} (hm : m < r) (h0 : ρ 0 = u) (hmu : ρ m = u)
    (hSA : ∀ t, t < m → SA (ρ t)) (hSB : ∀ t, m ≤ t → t < r → SB (ρ t))
    (TA : TNC GA m ρ h) (TB : TNC GB (r - m) (fun t => ρ (m + t)) h) : TNC G r ρ h := by
  intro c hc θ hθ i j k l hij hjk hkl hlr h1 h2
  have hcA : ProperOff GA.graph h c := fun x y e hx hy => hc (hAG x y e) hx hy
  have hcB : ProperOff GB.graph h c := fun x y e hx hy => hc (hBG x y e) hx hy
  have W := fun {x y : Fin n} (q : (thetaGraph G.graph h c θ).Reachable x y) =>
    cut_reach (G := G) (GA := GA) (GB := GB) hint hcut hA hB c θ q.some
  have upA := fun {x y : Fin n} (q : (thetaGraph GA.graph h c θ).Reachable x y) => thetaGraph_mono hAG c θ q
  have upB := fun {x y : Fin n} (q : (thetaGraph GB.graph h c θ).Reachable x y) => thetaGraph_mono hBG c θ q
  have hBm : ∀ t, m ≤ t → ρ (m + (t - m)) = ρ t := fun t ht => by rw [Nat.add_sub_cancel' ht]
  by_cases c1 : l < m
  · -- all on side A
    exact upA (TA hcA hθ hij hjk hkl c1 ((W h1).1 (hSA i (by omega)) (hSA k (by omega)))
      ((W h2).1 (hSA j (by omega)) (hSA l c1)))
  by_cases c2 : m ≤ i
  · -- all on side B, shifted by m
    have q1 := (W h1).2.2.1 (hSB i c2 (by omega)) (hSB k (by omega) (by omega))
    have q2 := (W h2).2.2.1 (hSB j (by omega) (by omega)) (hSB l (by omega) hlr)
    rw [← hBm i c2, ← hBm k (by omega)] at q1
    rw [← hBm j (by omega), ← hBm l (by omega)] at q2
    have := TB hcB hθ (i := i - m) (j := j - m) (k := k - m) (l := l - m) (by omega) (by omega) (by omega)
      (by omega) q1 q2
    dsimp only at this
    rw [hBm i c2, hBm j (by omega)] at this
    exact upB this
  by_cases c3 : j < m
  · by_cases c4 : k < m
    · -- i, j, k on side A, l on side B: collapse l to u = ρ 0
      have q2 := (W h2).2.1 (hSA j c3) (hSB l (by omega) hlr)
      have e2 : (thetaGraph G.graph h c θ).Reachable (ρ j) u := upA q2.1
      rcases Nat.eq_zero_or_pos i with hi | hi
      · subst hi; rw [h0]; exact e2.symm
      · have q1 := (W h1).1 (hSA i (by omega)) (hSA k c4)
        have q2' : (thetaGraph GA.graph h c θ).Reachable (ρ 0) (ρ j) := by rw [h0]; exact q2.1.symm
        have := TA hcA hθ (i := 0) (j := i) (k := j) (l := k) hi hij hjk c4 q2' q1
        rw [h0] at this
        exact (upA this).symm.trans e2.symm
    · -- i, j on side A, k, l on side B: both chains pass through u
      have q1 := (W h1).2.1 (hSA i (by omega)) (hSB k (by omega) (by omega))
      have q2 := (W h2).2.1 (hSA j c3) (hSB l (by omega) hlr)
      exact (upA q1.1).trans (upA q2.1).symm
  · -- i on side A, j, k, l on side B: collapse i to u = ρ m
    have q1 := (W h1).2.1 (hSA i (by omega)) (hSB k (by omega) (by omega))
    have e1 : (thetaGraph G.graph h c θ).Reachable (ρ i) u := upA q1.1
    rcases Nat.eq_or_lt_of_le (Nat.le_of_not_lt c3) with hj | hj
    · rw [← hj, hmu]; exact e1
    · have q2 := (W h2).2.2.1 (hSB j (by omega) (by omega)) (hSB l (by omega) hlr)
      have q1' : (thetaGraph GB.graph h c θ).Reachable (ρ (m + 0)) (ρ (m + (k - m))) := by
        rw [Nat.add_zero, hmu, hBm k (by omega)]; exact q1.2
      rw [← hBm j (by omega), ← hBm l (by omega)] at q2
      have := TB hcB hθ (i := 0) (j := j - m) (k := k - m) (l := l - m) (by omega) (by omega) (by omega)
        (by omega) q1' q2
      dsimp only at this
      rw [Nat.add_zero, hmu, hBm j (by omega)] at this
      exact e1.trans (upB this)

end pinch

/-- `RingTNC` of the pinched walk. -/
theorem RingTNC.of_pinch {GA GB : SphericalMap n} {SA SB : Fin n → Prop} {u : Fin n}
    (hpos : 0 < r) (hper : ∀ t, ρ (t + r) = ρ t) (hadj : ∀ t, G.Adj (ρ t) (ρ (t + 1))) (hoff : ∀ t, ρ t ≠ h)
    (hint : ∀ x, SA x → SB x → x = u)
    (hcut : ∀ x y, G.Adj x y → (SA x ∧ SA y) ∨ (SB x ∧ SB y))
    (hA : ∀ x y, G.Adj x y → SA x → SA y → GA.Adj x y)
    (hB : ∀ x y, G.Adj x y → SB x → SB y → GB.Adj x y)
    (hAG : ∀ x y, GA.Adj x y → G.Adj x y) (hBG : ∀ x y, GB.Adj x y → G.Adj x y)
    {m : ℕ} (hm : m < r) (h0 : ρ 0 = u) (hmu : ρ m = u)
    (hSA : ∀ t, t < m → SA (ρ t)) (hSB : ∀ t, m ≤ t → t < r → SB (ρ t))
    (RA : RingTNC GA m ρ h) (RB : RingTNC GB (r - m) (fun t => ρ (m + t)) h) : RingTNC G r ρ h :=
  ⟨hpos, hper, hadj, hoff, by
    intro c hc θ hθ
    exact TNC.pinch hint hcut hA hB hAG hBG hm h0 hmu hSA hSB
      (by unfold TNC; intro c' hc' θ' hθ'; exact RA.tnc hc' hθ')
      (by unfold TNC; intro c' hc' θ' hθ'; exact RB.tnc hc' hθ') hc hθ⟩

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.RingTNC.kempeMatching
#print axioms SimpleGraph.SphericalMap.RingTNC.of_pinch

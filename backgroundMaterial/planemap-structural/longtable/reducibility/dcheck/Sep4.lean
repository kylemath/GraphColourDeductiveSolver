import SideCycle
import DCheckRingBridge

/-! Job 25: **no separating induced 4-cycle in a minimal counterexample.** If both sides of an induced
4-cycle contain a non-isolated vertex, `T` is four-colourable when every spherical map of smaller
support is. Each side map (the other side deleted) has the cycle as a face; adding either chord
gives a smaller spherical map; the ring colourings realised on each side form a Kempe-closed class
set containing a colouring with `ρ0 ≠ ρ2` and one with `ρ1 ≠ ρ3`; `meet4` gives a common class, and
the two side colourings glue. -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyCliqueLift VacancyIcosahedral RotationSystem PlaneMapConstruction
  DCheck DCheck.R2 DCheck.Meet

variable {n : ℕ}

/-- Deleting a non-isolated vertex shrinks the support. -/
theorem supportSize_lt_of_drop {T N : SphericalMap n} {K : Set (Fin n)}
    (hN : N.graph = sideGraph T.graph K) (hle : N.graph ≤ T.graph) {z y : Fin n} (hz : z ∉ K)
    (hy : T.Adj z y) : supportSize N < supportSize T := by
  classical
  apply Finset.card_lt_card
  refine ⟨fun w hw => ?_, fun hsub => ?_⟩
  · simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hw ⊢
    exact lt_of_lt_of_le hw (SimpleGraph.degree_le_of_le hle)
  · have hmem : z ∈ Finset.univ.filter (fun x => 0 < T.graph.degree x) := by
      simp only [Finset.mem_filter, Finset.mem_univ, true_and]
      exact T.graph.degree_pos_iff_exists_adj z |>.mpr ⟨y, hy⟩
    have := hsub hmem
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at this
    obtain ⟨u, hu⟩ := N.graph.degree_pos_iff_exists_adj z |>.mp this
    rw [hN] at hu
    exact hz hu.2.1

/-- **Chord insertion in a ring face.** -/
theorem RingFace.chordMap {M : SphericalMap n} {r : ℕ} {σ : ℕ → Fin n} (R : RingFace M r σ)
    (i j : ℕ) (hne : σ i ≠ σ j) (hmiss : ¬ M.Adj (σ i) (σ j)) :
    ∃ M' : SphericalMap n, M'.graph = splitGraph M.graph (σ i) (σ j) hne := by
  have hface : M.rotation.faceOf (ringDart R i) = M.rotation.faceOf (ringDart R j) := by
    have e1 := face_bd M (ringDart R 0) i
    have e2 := face_bd M (ringDart R 0) j
    rw [ring_bd] at e1 e2
    exact e1.trans e2.symm
  exact ⟨⟨_, split M.rotation (ringDart R i) (ringDart R j) hne hmiss,
    split_fills M.rotation M.fills _ _ hface hne hmiss⟩, rfl⟩

/-- A chord between two vertices of the support does not enlarge the support. -/
theorem supportSize_split_le {M M' : SphericalMap n} {u v : Fin n} (hne : u ≠ v)
    (hM' : M'.graph = splitGraph M.graph u v hne) (hu : 0 < M.graph.degree u)
    (hv : 0 < M.graph.degree v) : supportSize M' ≤ supportSize M := by
  classical
  apply Finset.card_le_card
  intro w hw
  simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hw ⊢
  obtain ⟨y, hy⟩ := M'.graph.degree_pos_iff_exists_adj w |>.mp hw
  rw [hM'] at hy
  rcases hy with h | ⟨rfl, rfl⟩ | ⟨rfl, rfl⟩
  · exact M.graph.degree_pos_iff_exists_adj w |>.mpr ⟨y, h⟩
  · exact hu
  · exact hv

variable {T : SphericalMap n} {r : ℕ} {ρ : ℕ → Fin n} {c : T.Face → ZMod 2}

theorem onSide_adjC (C : ICycle T r ρ) (hc : CycPotential T r ρ c) {x y : Fin n}
    (hx : ¬ OnCyc r ρ x) (hy : ¬ OnCyc r ρ y) (hxy : T.Adj x y) {b : ZMod 2} (h : OnSide T c b x) :
    OnSide T c b y := by
  let d : T.Dart := ⟨(x, y), hxy⟩
  have h0 := cycInd_off C d hx
  have := zmod2_swap _ _ _ (hc d)
  rw [h0, zero_add, h d rfl] at this
  have hs := onSide_of_dartC C hc hy d.symm rfl
  rwa [this] at hs

theorem not_onSide_flip {x : Fin n} (d : T.Dart) (hd : d.fst = x) {b : ZMod 2}
    (h : OnSide T c (b + 1) x) : ¬ OnSide T c b x := by
  intro h'
  have := (h d hd).symm.trans (h' d hd)
  exact (show ∀ a : ZMod 2, a + 1 ≠ a by decide) b this

theorem zmod2_ne : ∀ x b : ZMod 2, x ≠ b → x = b + 1 := by decide

theorem keep_other (C : ICycle T r ρ) (hc : CycPotential T r ρ c) {b : ZMod 2} {v : Fin n}
    (hv : v ∉ keepC T c b r ρ) (d : T.Dart) (hd : d.fst = v) :
    ¬ OnCyc r ρ v ∧ OnSide T c (b + 1) v := by
  have hoff : ¬ OnCyc r ρ v := fun h => hv (Or.inl h)
  refine ⟨hoff, ?_⟩
  have hs := onSide_of_dartC C hc hoff d hd
  have hne : c (T.faceOf d) ≠ b := fun e => hv (Or.inr (e ▸ hs))
  have : c (T.faceOf d) = b + 1 := zmod2_ne _ _ hne
  rwa [this] at hs

theorem ring_ne_off (C : ICycle T r ρ) {z : Fin n} (hz : ¬ OnCyc r ρ z) (t : ℕ) : ρ t ≠ z :=
  fun e => hz (e ▸ C.onCyc t)

/-- A ring face of a side map plus a missing chord gives a colouring of the side with the chord's
ends coloured differently (via the smaller map). -/
theorem chord_colouring {N : SphericalMap n} {σ : ℕ → Fin n} (R : RingFace N r σ) {z : Fin n}
    (hlt : supportSize N < supportSize T)
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4)
    (i j : ℕ) (hne : σ i ≠ σ j) (hmiss : ¬ N.Adj (σ i) (σ j)) :
    ∃ col : Fin n → Fin 4, ProperOff N.graph z col ∧ col (σ i) ≠ col (σ j) := by
  obtain ⟨M', hM'⟩ := R.chordMap i j hne hmiss
  have hdi : 0 < N.graph.degree (σ i) := N.graph.degree_pos_iff_exists_adj _ |>.mpr ⟨_, R.adj i⟩
  have hdj : 0 < N.graph.degree (σ j) := N.graph.degree_pos_iff_exists_adj _ |>.mpr ⟨_, R.adj j⟩
  have hle' := supportSize_split_le hne hM' hdi hdj
  obtain ⟨cM⟩ := IH n M' (by rw [natCard_support_eq, natCard_support_eq]; omega)
  refine ⟨fun x => cM x, fun u v huv _ _ => cM.valid (by rw [hM']; exact Or.inl huv), ?_⟩
  exact cM.valid (by rw [hM']; exact Or.inr (Or.inl ⟨rfl, rfl⟩))

/-- **One side of an induced 4-cycle**: its realised class predicate is Kempe-closed and has
both chord facts. -/
theorem side4 (C : ICycle T 4 ρ) (hc : CycPotential T 4 ρ c) (b : ZMod 2) {z y : Fin n}
    (hz : ¬ OnCyc 4 ρ z) (hzon : OnSide T c (b + 1) z) (hzy : T.Adj z y)
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4) :
    ∃ N : SphericalMap n, N.graph = sideGraph T.graph (keepC T c b 4 ρ) ∧
      closedB 4 4 (gR N z 4 ρ 4) = true ∧ facts4 (gR N z 4 ρ 4) = true := by
  classical
  obtain ⟨N, hN, hle, spec⟩ := subgraph_tracked T (sideGraph T.graph (keepC T c b 4 ρ))
    (fun _ _ e => e.1)
  have hzK : z ∉ keepC T c b 4 ρ := by
    rintro (h | h)
    · exact hz h
    · exact not_onSide_flip ⟨(z, y), hzy⟩ rfl hzon h
  have hlt := supportSize_lt_of_drop hN hle hzK hzy
  have hh := ring_ne_off C hz
  have nadj : ∀ p p', p < 4 → p' < 4 → p' = p + 2 → ¬ N.Adj (ρ p) (ρ p') := by
    intro p p' hp hp' e ha
    have := C.ind p p' hp hp' (hle ha)
    subst e; omega
  have hne : ∀ p p', p < 4 → p' < 4 → p ≠ p' → ρ p ≠ ρ p' := fun p p' hp hp' h e =>
    h (C.inj p p' hp hp' e)
  refine ⟨N, hN, ?_⟩
  -- the ring data and the two chord colourings, in either orientation
  have key : RingNC N 4 ρ ∧
      (∃ col : Fin n → Fin 4, ProperOff N.graph z col ∧ col (ρ 0) ≠ col (ρ 2)) ∧
      (∃ col : Fin n → Fin 4, ProperOff N.graph z col ∧ col (ρ 1) ≠ col (ρ 3)) := by
    by_cases hfar : ∀ h : T.Adj (ρ 0) (ρ 1), c (T.faceOf ⟨(ρ 0, ρ 1), h⟩) ≠ b
    · have R := kept_ringFace C hc hN hle spec hfar
      exact ⟨R.toNC,
        chord_colouring R hlt IH 0 2 (hne 0 2 (by omega) (by omega) (by omega)) (nadj 0 2 (by omega) (by omega) rfl),
        chord_colouring R hlt IH 1 3 (hne 1 3 (by omega) (by omega) (by omega)) (nadj 1 3 (by omega) (by omega) rfl)⟩
    · have hnear : ∀ h : T.Adj (ρ 0) (ρ 1), c (T.faceOf ⟨(ρ 0, ρ 1), h⟩) = b := by
        intro h; by_contra hh'; exact hfar (fun h' => by convert hh' using 1)
      have R := kept_ringFace_rev C hc hN hle spec hnear
      have e0 : revR 4 ρ 0 = ρ 0 := by unfold revR; simp
      have e1 : revR 4 ρ 1 = ρ 3 := by unfold revR; simp
      have e2 : revR 4 ρ 2 = ρ 2 := by unfold revR; rw [show (4 - 1) * 2 = 2 + 4 by rfl, C.per]
      have e3 : revR 4 ρ 3 = ρ 1 := by
        unfold revR; rw [show (4 - 1) * 3 = 1 + 4 * 2 by rfl, C.per_mul]
      refine ⟨R.revNC (by omega) C.per, ?_, ?_⟩
      · obtain ⟨col, hcol, hd⟩ := chord_colouring R hlt IH (z := z) 0 2
          (by rw [e0, e2]; exact hne 0 2 (by omega) (by omega) (by omega))
          (by rw [e0, e2]; exact nadj 0 2 (by omega) (by omega) rfl)
        rw [e0, e2] at hd; exact ⟨col, hcol, hd⟩
      · obtain ⟨col, hcol, hd⟩ := chord_colouring R hlt IH (z := z) 3 1
          (by rw [e3, e1]; exact hne 1 3 (by omega) (by omega) (by omega))
          (by rw [e3, e1]; exact nadj 1 3 (by omega) (by omega) rfl)
        rw [e3, e1] at hd; exact ⟨col, hcol, hd⟩
  obtain ⟨RN, ⟨c02, hc02, h02⟩, ⟨c13, hc13, h13⟩⟩ := key
  refine ⟨closedB_realised RN hh size4 (by omega) (by omega), ?_⟩
  unfold facts4
  rw [Bool.and_eq_true]
  refine ⟨has_realised RN hh size4 (by omega) _ hc02 (fun g hg => ?_),
    has_realised RN hh size4 (by omega) _ hc13 (fun g hg => ?_)⟩
  · rw [col_renamed g c02 (by omega), col_renamed g c02 (by omega)]
    simpa using fun e => h02 (hg (Fin.ext e))
  · rw [col_renamed g c13 (by omega), col_renamed g c13 (by omega)]
    simpa using fun e => h13 (hg (Fin.ext e))

/-- **Theorem (B2, 4-cycles).** If both sides of an induced 4-cycle of `T` contain a non-isolated
vertex, then `T` is four-colourable as soon as every spherical map of smaller support is. -/
theorem colorable_of_separating_4cycle (C : ICycle T 4 ρ) (hc : CycPotential T 4 ρ c)
    {z0 y0 z1 y1 : Fin n} (hz0 : ¬ OnCyc 4 ρ z0) (hon0 : OnSide T c 0 z0) (hy0 : T.Adj z0 y0)
    (hz1 : ¬ OnCyc 4 ρ z1) (hon1 : OnSide T c 1 z1) (hy1 : T.Adj z1 y1)
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4) : T.graph.Colorable 4 := by
  classical
  obtain ⟨N0, hN0, cl0, f0⟩ := side4 C hc 0 hz1 (by simpa using hon1) hy1 IH
  obtain ⟨N1, hN1, cl1, f1⟩ := side4 C hc 1 hz0 (by rw [show (1 + 1 : ZMod 2) = 0 by decide]; exact hon0) hy0 IH
  obtain ⟨i, hi0, hi1⟩ := meet4 _ _ cl0 f0 cl1 f1
  have r0 : Realised N0 z1 4 ρ (ringColourings 4)[i.val]! := of_decide_eq_true hi0
  have r1 : Realised N1 z0 4 ρ (ringColourings 4)[i.val]! := of_decide_eq_true hi1
  obtain ⟨cA, hcA, eA⟩ := r0
  obtain ⟨cB, hcB, eB⟩ := r1
  have agree : ∀ t, cA (ρ t) = cB (ρ t) := by
    intro t
    rw [← C.per_mod t]
    have ht := Nat.mod_lt t (show 0 < 4 by omega)
    apply Fin.ext
    have a := col_code _ (ringSeq_lt ρ cA) 4 _ ht
    have b := col_code _ (ringSeq_lt ρ cB) 4 _ ht
    rw [← eA] at a; rw [← eB] at b
    exact a.symm.trans b
  set K0 := keepC T c 0 4 ρ
  set K1 := keepC T c 1 4 ρ
  have z1K0 : z1 ∉ K0 := by
    rintro (h | h)
    · exact hz1 h
    · exact not_onSide_flip (b := 0) ⟨(z1, y1), hy1⟩ rfl (by simpa using hon1) h
  have z0K1 : z0 ∉ K1 := by
    rintro (h | h)
    · exact hz0 h
    · exact not_onSide_flip (b := 1) ⟨(z0, y0), hy0⟩ rfl (by rw [show (1 + 1 : ZMod 2) = 0 by decide]; exact hon0) h
  have in1 : ∀ {u v : Fin n}, T.Adj u v → u ∉ K0 → u ∈ K1 := fun {u v} huv hu =>
    Or.inr (by simpa using (keep_other C hc hu ⟨(u, v), huv⟩ rfl).2)
  have adj0 : ∀ {u v}, T.Adj u v → u ∈ K0 → v ∈ K0 → N0.graph.Adj u v := fun h hu hv => by
    rw [hN0]; exact ⟨h, hu, hv⟩
  have adj1 : ∀ {u v}, T.Adj u v → u ∈ K1 → v ∈ K1 → N1.graph.Adj u v := fun h hu hv => by
    rw [hN1]; exact ⟨h, hu, hv⟩
  have ne1 : ∀ {u}, u ∈ K0 → u ≠ z1 := fun hu e => z1K0 (e ▸ hu)
  have ne0 : ∀ {u}, u ∈ K1 → u ≠ z0 := fun hu e => z0K1 (e ▸ hu)
  -- a kept end of a mixed edge lies on the cycle
  have mixed : ∀ {u v}, T.Adj u v → u ∈ K0 → v ∉ K0 → OnCyc 4 ρ u := by
    intro u v huv hu hv
    by_contra hoff
    have hv' := keep_other C hc hv ⟨(v, u), huv.symm⟩ rfl
    have hu0 : OnSide T c 0 u := by rcases hu with h | h; exact absurd h hoff; exact h
    have := onSide_adjC C hc hoff hv'.1 huv hu0
    exact not_onSide_flip ⟨(v, u), huv.symm⟩ rfl hv'.2 this
  have mix : ∀ {u v}, T.Adj u v → u ∈ K0 → v ∉ K0 → cA u ≠ cB v := by
    intro u v huv hu hv
    obtain ⟨t, -, rfl⟩ := mixed huv hu hv
    rw [agree t]
    have hu1 : ρ t ∈ K1 := Or.inl (C.onCyc t)
    exact hcB (adj1 huv hu1 (in1 huv.symm hv)) (ne0 hu1) (ne0 (in1 huv.symm hv))
  refine ⟨SimpleGraph.Coloring.mk (fun v => if v ∈ K0 then cA v else cB v) ?_⟩
  intro u v huv
  by_cases hu : u ∈ K0 <;> by_cases hv : v ∈ K0
  · simp only [hu, hv, ↓reduceIte]; exact hcA (adj0 huv hu hv) (ne1 hu) (ne1 hv)
  · simp only [hu, hv, ↓reduceIte]; exact mix huv hu hv
  · simp only [hu, hv, ↓reduceIte]; exact (mix huv.symm hv hu).symm
  · simp only [hu, hv, ↓reduceIte]
    exact hcB (adj1 huv (in1 huv hu) (in1 huv.symm hv)) (ne0 (in1 huv hu)) (ne0 (in1 huv.symm hv))

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.colorable_of_separating_4cycle

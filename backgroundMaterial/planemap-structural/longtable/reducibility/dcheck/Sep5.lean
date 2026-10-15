import Sep5Star

/-! Job 25: **no separating induced 5-cycle with at least two vertices on each side** in a minimal
counterexample. Each side map has the cycle as a face; the star map (needs the other side to have
two vertices) and the five fan maps are smaller, giving a colouring of the side whose ring misses a
colour and, for each `v`, one with `ρ v ≠ ρ (v+2)`, `ρ v ≠ ρ (v+3)`. `meet5` gives a common ring
class of the two sides, and the side colourings glue as in `Sep4`. -/

namespace SimpleGraph.SphericalMap
open VacancySlide VacancyCliqueLift VacancyIcosahedral RotationSystem PlaneMapConstruction
  DCheck DCheck.R2 DCheck.Meet

variable {n : ℕ} {T : SphericalMap n} {r : ℕ} {ρ : ℕ → Fin n} {c : T.Face → ZMod 2}

/-- Deleting two distinct non-isolated vertices shrinks the support by two. -/
theorem supportSize_two_drop {N : SphericalMap n} {K : Set (Fin n)}
    (hN : N.graph = sideGraph T.graph K) (hle : N.graph ≤ T.graph) {z z' y y' : Fin n}
    (hzz : z ≠ z') (hz : z ∉ K) (hz' : z' ∉ K) (hy : T.Adj z y) (hy' : T.Adj z' y') :
    supportSize N + 2 ≤ supportSize T := by
  classical
  unfold supportSize
  set FN := Finset.univ.filter fun x => 0 < N.graph.degree x
  set FT := Finset.univ.filter fun x => 0 < T.graph.degree x
  have hsub : FN ⊆ (FT.erase z).erase z' := by
    intro x hx
    simp only [FN, Finset.mem_filter, Finset.mem_univ, true_and] at hx
    obtain ⟨v, hv⟩ := N.graph.degree_pos_iff_exists_adj x |>.mp hx
    have hv' := hv; rw [hN] at hv'
    refine Finset.mem_erase.2 ⟨fun e => hz' (e ▸ hv'.2.1), Finset.mem_erase.2
      ⟨fun e => hz (e ▸ hv'.2.1), ?_⟩⟩
    simp only [FT, Finset.mem_filter, Finset.mem_univ, true_and]
    exact T.graph.degree_pos_iff_exists_adj x |>.mpr ⟨v, hle hv⟩
  have hzT : z ∈ FT := by
    simp only [FT, Finset.mem_filter, Finset.mem_univ, true_and]
    exact T.graph.degree_pos_iff_exists_adj z |>.mpr ⟨y, hy⟩
  have hz'T : z' ∈ FT.erase z := Finset.mem_erase.2 ⟨hzz.symm, by
    simp only [FT, Finset.mem_filter, Finset.mem_univ, true_and]
    exact T.graph.degree_pos_iff_exists_adj z' |>.mpr ⟨y', hy'⟩⟩
  have := Finset.card_le_card hsub
  rw [Finset.card_erase_of_mem hz'T, Finset.card_erase_of_mem hzT] at this
  have : 2 ≤ FT.card := by
    have h1 := Finset.card_pos.2 ⟨z, hzT⟩
    have h2 := Finset.card_pos.2 ⟨z', hz'T⟩
    rw [Finset.card_erase_of_mem hzT] at h2
    omega
  omega

/-- A colouring of a pentagonal side whose ring misses a colour (via the star map). -/
theorem star_colouring {N : SphericalMap n} {σ : ℕ → Fin n} (R : RingFace N 5 σ) {z : Fin n}
    (hlt : supportSize N + 2 ≤ supportSize T)
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4) :
    ∃ col : Fin n → Fin 4, ProperOff N.graph z col ∧ ∃ x : Fin 4, ∀ k, k < 5 → col (σ k) ≠ x := by
  classical
  obtain ⟨M5, hold, hstar, hsupp⟩ := R.starMap
  have hcard : supportSize M5 ≤ supportSize N + 1 := by
    unfold supportSize
    have : (Finset.univ.filter fun x => 0 < M5.graph.degree x) ⊆
        insert (Fin.last n) ((Finset.univ.filter fun x => 0 < N.graph.degree x).map
          Fin.castSuccEmb) := by
      intro x hx
      simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hx
      rcases hsupp x hx with rfl | ⟨y, rfl, hy⟩
      · exact Finset.mem_insert_self _ _
      · refine Finset.mem_insert_of_mem (Finset.mem_map.2 ⟨y, ?_, rfl⟩)
        simpa using hy
    calc _ ≤ _ := Finset.card_le_card this
      _ ≤ _ := Finset.card_insert_le _ _
      _ = _ := by rw [Finset.card_map]
  obtain ⟨cM⟩ := IH (n + 1) M5 (by rw [natCard_support_eq, natCard_support_eq]; omega)
  refine ⟨fun x => cM x.castSucc, fun u v huv _ _ => cM.valid (hold u v huv), cM (Fin.last n),
    fun k hk => ?_⟩
  exact (cM.valid (hstar k hk)).symm

/-- A colouring of a pentagonal side with the fan constraints at `σ 0` (via the fan map). -/
theorem fan_colouring {N : SphericalMap n} {σ : ℕ → Fin n} (R : RingFace N 5 σ) {z : Fin n}
    (hlt : supportSize N < supportSize T)
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4)
    (h02 : ¬ N.Adj (σ 0) (σ 2)) (h03 : ¬ N.Adj (σ 0) (σ 3)) :
    ∃ col : Fin n → Fin 4, ProperOff N.graph z col ∧ col (σ 0) ≠ col (σ 2) ∧ col (σ 0) ≠ col (σ 3) := by
  classical
  obtain ⟨M2, hle2, a2, a3, hsupp⟩ := R.fanMap h02 h03
  have hcard : supportSize M2 ≤ supportSize N := by
    unfold supportSize
    apply Finset.card_le_card
    intro x hx
    simp only [Finset.mem_filter, Finset.mem_univ, true_and] at hx ⊢
    exact hsupp x hx
  obtain ⟨cM⟩ := IH n M2 (by rw [natCard_support_eq, natCard_support_eq]; omega)
  exact ⟨fun x => cM x, fun u v huv _ _ => cM.valid (hle2 huv), cM.valid a2, cM.valid a3⟩

theorem revR5 (C : ICycle T 5 ρ) (m : ℕ) : revR 5 ρ m = ρ ((4 * m) % 5) := by
  unfold revR; rw [C.per_mod]

/-- **One side of an induced 5-cycle with two vertices on the other side**: its realised class
predicate is Kempe-closed and has the star fact and the five fan facts. -/
theorem side5 (C : ICycle T 5 ρ) (hc : CycPotential T 5 ρ c) (b : ZMod 2) {z y z' y' : Fin n}
    (hz : ¬ OnCyc 5 ρ z) (hzon : OnSide T c (b + 1) z) (hzy : T.Adj z y)
    (hz' : ¬ OnCyc 5 ρ z') (hzon' : OnSide T c (b + 1) z') (hzy' : T.Adj z' y') (hzz : z ≠ z')
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4) :
    ∃ N : SphericalMap n, N.graph = sideGraph T.graph (keepC T c b 5 ρ) ∧
      closedB 5 10 (gR N z 5 ρ 10) = true ∧ facts5 (gR N z 5 ρ 10) = true := by
  classical
  obtain ⟨N, hN, hle, spec⟩ := subgraph_tracked T (sideGraph T.graph (keepC T c b 5 ρ))
    (fun _ _ e => e.1)
  have notK : ∀ {x y : Fin n}, ¬ OnCyc 5 ρ x → OnSide T c (b + 1) x → T.Adj x y →
      x ∉ keepC T c b 5 ρ := fun hx hon hxy => by
    rintro (h | h)
    · exact hx h
    · exact not_onSide_flip ⟨(_, _), hxy⟩ rfl hon h
  have hlt2 := supportSize_two_drop hN hle hzz (notK hz hzon hzy) (notK hz' hzon' hzy') hzy hzy'
  have hlt : supportSize N < supportSize T := by omega
  have hh := ring_ne_off C hz
  -- non-adjacent ring pairs: positions differing by 2 or 3
  have nadj : ∀ p p', p < 5 → p' < 5 → (p' = (p + 2) % 5 ∨ p' = (p + 3) % 5) →
      ¬ N.Adj (ρ p) (ρ p') := by
    intro p p' hp hp' e ha
    have := C.ind p p' hp hp' (hle ha)
    rcases (show p = 0 ∨ p = 1 ∨ p = 2 ∨ p = 3 ∨ p = 4 by omega) with rfl | rfl | rfl | rfl | rfl <;>
      omega
  refine ⟨N, hN, ?_⟩
  have key : RingNC N 5 ρ ∧
      (∃ col : Fin n → Fin 4, ProperOff N.graph z col ∧ ∃ x : Fin 4, ∀ k, k < 5 → col (ρ k) ≠ x) ∧
      (∀ v, v < 5 → ∃ col : Fin n → Fin 4, ProperOff N.graph z col ∧
        col (ρ v) ≠ col (ρ ((v + 2) % 5)) ∧ col (ρ v) ≠ col (ρ ((v + 3) % 5))) := by
    by_cases hfar : ∀ h : T.Adj (ρ 0) (ρ 1), c (T.faceOf ⟨(ρ 0, ρ 1), h⟩) ≠ b
    · have R := kept_ringFace C hc hN hle spec hfar
      refine ⟨R.toNC, star_colouring R hlt2 IH, fun v hv => ?_⟩
      have Rv := R.shift v
      have e0 : ρ (0 + v) = ρ v := by rw [Nat.zero_add]
      have e2 : ρ (2 + v) = ρ ((v + 2) % 5) := by rw [C.per_mod, Nat.add_comm]
      have e3 : ρ (3 + v) = ρ ((v + 3) % 5) := by rw [C.per_mod, Nat.add_comm]
      obtain ⟨col, hcol, h2, h3⟩ := fan_colouring Rv hlt IH (z := z)
        (by show ¬ N.Adj (ρ (0 + v)) (ρ (2 + v)); rw [e0, e2]
            exact nadj v _ hv (Nat.mod_lt _ (by omega)) (Or.inl rfl))
        (by show ¬ N.Adj (ρ (0 + v)) (ρ (3 + v)); rw [e0, e3]
            exact nadj v _ hv (Nat.mod_lt _ (by omega)) (Or.inr rfl))
      rw [e0, e2] at h2; rw [e0, e3] at h3
      exact ⟨col, hcol, h2, h3⟩
    · have hnear : ∀ h : T.Adj (ρ 0) (ρ 1), c (T.faceOf ⟨(ρ 0, ρ 1), h⟩) = b := by
        intro h; by_contra hh'; exact hfar (fun h' => by convert hh' using 1)
      have R := kept_ringFace_rev C hc hN hle spec hnear
      refine ⟨R.revNC (by omega) C.per, ?_, fun v hv => ?_⟩
      · obtain ⟨col, hcol, x, hx⟩ := star_colouring R hlt2 IH (z := z)
        refine ⟨col, hcol, x, fun k hk => ?_⟩
        have := hx (rpos 5 k) (by unfold rpos; split_ifs <;> omega)
        rwa [revR_rpos (by omega) C.per k hk] at this
      · -- the fan at ρ-position v is the fan at reversed position rpos 5 v
        have Rv := R.shift (rpos 5 v)
        have pos : ∀ j, revR 5 ρ (j + rpos 5 v) = ρ ((4 * (j + rpos 5 v)) % 5) := fun j => revR5 C _
        have e0 : revR 5 ρ (0 + rpos 5 v) = ρ v := by
          rw [Nat.zero_add]; exact revR_rpos (by omega) C.per v hv
        have e2 : revR 5 ρ (2 + rpos 5 v) = ρ ((v + 3) % 5) := by
          rw [pos]; congr 1
          rcases (show v = 0 ∨ v = 1 ∨ v = 2 ∨ v = 3 ∨ v = 4 by omega) with rfl | rfl | rfl | rfl | rfl <;> rfl
        have e3 : revR 5 ρ (3 + rpos 5 v) = ρ ((v + 2) % 5) := by
          rw [pos]; congr 1
          rcases (show v = 0 ∨ v = 1 ∨ v = 2 ∨ v = 3 ∨ v = 4 by omega) with rfl | rfl | rfl | rfl | rfl <;> rfl
        obtain ⟨col, hcol, h2, h3⟩ := fan_colouring Rv hlt IH (z := z)
          (by show ¬ N.Adj (revR 5 ρ (0 + rpos 5 v)) (revR 5 ρ (2 + rpos 5 v)); rw [e0, e2]
              exact nadj v _ hv (Nat.mod_lt _ (by omega)) (Or.inr rfl))
          (by show ¬ N.Adj (revR 5 ρ (0 + rpos 5 v)) (revR 5 ρ (3 + rpos 5 v)); rw [e0, e3]
              exact nadj v _ hv (Nat.mod_lt _ (by omega)) (Or.inl rfl))
        rw [e0, e2] at h2; rw [e0, e3] at h3
        exact ⟨col, hcol, h3, h2⟩
  obtain ⟨RN, ⟨cs, hcs, x0, hx0⟩, fans⟩ := key
  refine ⟨closedB_realised RN hh size5 (by omega) (by omega), ?_⟩
  unfold facts5
  rw [Bool.and_eq_true]
  refine ⟨has_realised RN hh size5 (by omega) _ hcs (fun g hg => ?_), ?_⟩
  · rw [List.any_eq_true]
    refine ⟨(g x0).val, List.mem_range.2 (g x0).isLt, ?_⟩
    rw [List.all_eq_true]
    intro t ht
    have ht' := List.mem_range.1 ht
    rw [col_renamed g cs ht']
    simpa using fun e => hx0 t ht' (hg (Fin.ext e))
  · rw [List.all_eq_true]
    intro v hv
    have hv' := List.mem_range.1 hv
    obtain ⟨col, hcol, h2, h3⟩ := fans v hv'
    refine has_realised RN hh size5 (by omega) _ hcol (fun g hg => ?_)
    rw [col_renamed g col hv', col_renamed g col (Nat.mod_lt _ (by omega)),
      col_renamed g col (Nat.mod_lt _ (by omega))]
    simp only [Bool.and_eq_true, bne_iff_ne, ne_eq]
    exact ⟨fun e => h2 (hg (Fin.ext e)), fun e => h3 (hg (Fin.ext e))⟩

/-- **Theorem (B2, 5-cycles).** If both sides of an induced 5-cycle of `T` contain two distinct
non-isolated vertices, then `T` is four-colourable as soon as every spherical map of smaller
support is. -/
theorem colorable_of_separating_5cycle (C : ICycle T 5 ρ) (hc : CycPotential T 5 ρ c)
    {z0 y0 z0' y0' z1 y1 z1' y1' : Fin n}
    (hz0 : ¬ OnCyc 5 ρ z0) (hon0 : OnSide T c 0 z0) (hy0 : T.Adj z0 y0)
    (hz0' : ¬ OnCyc 5 ρ z0') (hon0' : OnSide T c 0 z0') (hy0' : T.Adj z0' y0') (h00 : z0 ≠ z0')
    (hz1 : ¬ OnCyc 5 ρ z1) (hon1 : OnSide T c 1 z1) (hy1 : T.Adj z1 y1)
    (hz1' : ¬ OnCyc 5 ρ z1') (hon1' : OnSide T c 1 z1') (hy1' : T.Adj z1' y1') (h11 : z1 ≠ z1')
    (IH : ∀ (m' : ℕ) (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support →
      M.graph.Colorable 4) : T.graph.Colorable 4 := by
  classical
  have e11 : (1 + 1 : ZMod 2) = 0 := by decide
  obtain ⟨N0, hN0, cl0, f0⟩ := side5 C hc 0 hz1 (by simpa using hon1) hy1 hz1'
    (by simpa using hon1') hy1' h11 IH
  obtain ⟨N1, hN1, cl1, f1⟩ := side5 C hc 1 hz0 (by rw [e11]; exact hon0) hy0 hz0'
    (by rw [e11]; exact hon0') hy0' h00 IH
  obtain ⟨i, hi0, hi1⟩ := meet5 _ _ cl0 f0 cl1 f1
  have r0 : Realised N0 z1 5 ρ (ringColourings 5)[i.val]! := of_decide_eq_true hi0
  have r1 : Realised N1 z0 5 ρ (ringColourings 5)[i.val]! := of_decide_eq_true hi1
  obtain ⟨cA, hcA, eA⟩ := r0
  obtain ⟨cB, hcB, eB⟩ := r1
  have agree : ∀ t, cA (ρ t) = cB (ρ t) := by
    intro t
    rw [← C.per_mod t]
    have ht := Nat.mod_lt t (show 0 < 5 by omega)
    apply Fin.ext
    have a := col_code _ (ringSeq_lt ρ cA) 5 _ ht
    have b := col_code _ (ringSeq_lt ρ cB) 5 _ ht
    rw [← eA] at a; rw [← eB] at b
    exact a.symm.trans b
  set K0 := keepC T c 0 5 ρ
  set K1 := keepC T c 1 5 ρ
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
  have mixed : ∀ {u v}, T.Adj u v → u ∈ K0 → v ∉ K0 → OnCyc 5 ρ u := by
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

#print axioms SimpleGraph.SphericalMap.colorable_of_separating_5cycle

import RSSTWindowLink

/-!
# ST-114 B3, the separating-cycle steps (Studio, 10 Nov)

- L6 `r2_far0`: a ring-2 vertex `x` on `w_0` and on a far `w_k` (`2 ≤ k ≤ d-2`) gives the 4-cycle `u w_0 x w_k`, with
  `w_{d-1}` and `w_1` on the two sides of `u w_0`: a separating 4-cycle.
- L9 `r2_adj`: `x ∈ seg_i`, `y ∈ seg_{i+1}`, `x ~ y`, with no common link neighbour: the 4-cycle `w_i w_{i+1} y x`, with
  `s_i` and `u` on the two sides of `w_i w_{i+1}`.
- L10 `r2_chord_far0`: `x ∈ seg_0`, `y ∈ seg_k` far, `x ~ y`, with no close representation: the 5-cycle `u w_0 x y w_k`.
  Each side has two off-cycle vertices (two link vertices, or one link vertex and a private neighbour of it).
-/

namespace SimpleGraph.SphericalMap.RSSTSeed
open SimpleGraph SphericalMap RotationSystem

variable {n : ℕ} {T : SphericalMap n} {u : Fin n} {d : ℕ} {w : ℕ → Fin n}

namespace IsLink

theorem ne_of_lt (hL : IsLink T u d w) {a b : ℕ} (ha : a < d) (hb : b < d) (h : a ≠ b) : w a ≠ w b :=
  fun e => h (hL.inj ha hb e)

/-- L6. No ring-2 vertex sees `w_0` and a far `w_k`. -/
theorem r2_far0 (hL : IsLink T u d w) (hT : ClaimGlue.Internally6 T) {x : Fin n} (hxu : x ≠ u)
    (hxw : ∀ j, w j ≠ x) (hx0 : T.Adj (w 0) x) {k : ℕ} (hk2 : 2 ≤ k) (hkd : k + 2 ≤ d)
    (hk : T.Adj (w k) x) : False := by
  have d5 := hL.d5 hT
  have C := cyc4_cyc' (hL.adj 0) hx0 hk.symm (hL.adj k).symm
    (ne_vec4 (hL.ne 0).symm hxu.symm (hL.ne k).symm (hxw 0) (hL.ne_of_lt (by omega) (by omega) (by omega))
      (hxw k).symm)
  obtain ⟨c, hc⟩ := exists_cycPotential' C
  have offw : ∀ j, j < d → j ≠ 0 → j ≠ k → ¬ OnCyc 4 (cyc4 u (w 0) x (w k)) (w j) := by
    intro j hj h0 hjk h
    rcases onCyc4_sub h with e | e | e | e
    · exact hL.ne j e
    · exact hL.ne_of_lt hj (by omega) h0 e
    · exact hxw j e
    · exact hL.ne_of_lt hj (by omega) hjk e
  obtain ⟨f1, f2⟩ := hL.faces_u0 hT (hL.adj (d - 1)).symm (hL.adj 0) (hL.ww hT 0).symm (hL.adj 0).symm
  obtain ⟨b, sB, sA⟩ := sides_of_edge C hc ⟨(w (d - 1), u), (hL.adj (d - 1)).symm⟩
    ⟨(w 1, w 0), (hL.ww hT 0).symm⟩ rfl rfl (offw (d - 1) (by omega) (by omega) (by omega))
    (offw 1 (by omega) (by omega) (by omega)) (hL.adj 0) (hL.adj 0).symm f1 f2
  have hBS := bothSides_of (offw (d - 1) (by omega) (by omega) (by omega))
    (offw 1 (by omega) (by omega) (by omega)) sB sA (hL.adj (d - 1)).symm (hL.adj 1).symm
  exact hT.noShortSep 4 _ c C (by omega) hc hBS (fun h => absurd h (by omega))

/-- L9. Adjacent ring-2 vertices on consecutive segments share a link neighbour. -/
theorem r2_adj (hL : IsLink T u d w) (hT : ClaimGlue.Internally6 T) {i : ℕ} {x y : Fin n}
    (hxu : x ≠ u) (hyu : y ≠ u) (hxw : ∀ j, w j ≠ x) (hyw : ∀ j, w j ≠ y)
    (hx : T.Adj (w i) x) (hy : T.Adj (w (i + 1)) y) (hxy : T.Adj x y)
    (hx' : ¬ T.Adj (w (i + 1)) x) (hy' : ¬ T.Adj (w i) y) : False := by
  obtain ⟨s, hsu, hs1, hs2, hsi, hsi1⟩ := hL.apex hT i
  have hw := hL.ww hT i
  have C := cyc4_cyc' hw hy hxy.symm hx.symm
    (ne_vec4 hw.ne (hyw i) (hxw i) (hyw (i + 1)) (hxw (i + 1)) hxy.ne.symm)
  obtain ⟨c, hc⟩ := exists_cycPotential' C
  have offs : ¬ OnCyc 4 (cyc4 (w i) (w (i + 1)) y x) s := by
    intro h
    rcases onCyc4_sub h with e | e | e | e
    · exact hsi.ne e.symm
    · exact hsi1.ne e.symm
    · exact hy' (e ▸ hsi)
    · exact hx' (e ▸ hsi1)
  have offu : ¬ OnCyc 4 (cyc4 (w i) (w (i + 1)) y x) u := by
    intro h
    rcases onCyc4_sub h with e | e | e | e
    · exact hL.ne i e.symm
    · exact hL.ne (i + 1) e.symm
    · exact hyu e.symm
    · exact hxu e.symm
  have fp : T.faceOf ⟨(s, w i), hsi.symm⟩ = T.faceOf ⟨(w i, w (i + 1)), hw⟩ :=
    ((face_nx hs1 hw hsi1).trans (face_nx hs2 hsi1 hsi.symm)).symm
  have fq : T.faceOf ⟨(u, w (i + 1)), hL.adj (i + 1)⟩ = T.faceOf ⟨(w (i + 1), w i), hw.symm⟩ :=
    ((face_nx (nx_tri hT.triangulated (hL.nx i)).2 hw.symm (hL.adj i).symm).trans
      (face_nx (hL.nx i) (hL.adj i).symm (hL.adj (i + 1)))).symm
  obtain ⟨b, sp, sq⟩ := sides_of_edge C hc ⟨(s, w i), hsi.symm⟩ ⟨(u, w (i + 1)), hL.adj (i + 1)⟩ rfl rfl
    offs offu hw hw.symm fp fq
  have hBS := bothSides_of offs offu sp sq hsi.symm (hL.adj (i + 1))
  exact hT.noShortSep 4 _ c C (by omega) hc hBS (fun h => absurd h (by omega))

/-- L10. No chord of ring 2 between far segments (no close representation of the pair). -/
theorem r2_chord_far0 (hL : IsLink T u d w) (hT : ClaimGlue.Internally6 T) {x y : Fin n}
    (hxu : x ≠ u) (hyu : y ≠ u) (hxw : ∀ j, w j ≠ x) (hyw : ∀ j, w j ≠ y)
    (hx0 : T.Adj (w 0) x) {k : ℕ} (hk2 : 2 ≤ k) (hkd : k + 2 ≤ d) (hyk : T.Adj (w k) y)
    (hxy : T.Adj x y) (hnc : ∀ a b, T.Adj (w a) x → T.Adj (w b) y → ¬ Close d a b) : False := by
  have d5 := hL.d5 hT
  have hne := fun {a b : ℕ} (ha : a < d) (hb : b < d) (h : a ≠ b) => hL.ne_of_lt ha hb h
  have C := cyc5_cyc (hL.adj 0) hx0 hxy hyk.symm (hL.adj k).symm
    (ne_vec5 (hL.ne 0).symm hxu.symm hyu.symm (hL.ne k).symm (hxw 0) (hyw 0) (hne (by omega) (by omega) (by omega))
      hxy.ne (hxw k).symm (hyw k).symm)
  obtain ⟨c, hc⟩ := exists_cycPotential' C
  set ρ := cyc5 u (w 0) x y (w k)
  have off : ∀ z, z ≠ u → z ≠ w 0 → z ≠ x → z ≠ y → z ≠ w k → ¬ OnCyc 5 ρ z := by
    intro z h1 h2 h3 h4 h5 h
    rcases onCyc5_sub h with e | e | e | e | e
    · exact h1 e
    · exact h2 e
    · exact h3 e
    · exact h4 e
    · exact h5 e
  have offw : ∀ j, j < d → j ≠ 0 → j ≠ k → ¬ OnCyc 5 ρ (w j) := fun j hj h0 hjk =>
    off _ (hL.ne j) (hne hj (by omega) h0) (hxw j) (hyw j) (hne hj (by omega) hjk)
  obtain ⟨f1, f2⟩ := hL.faces_u0 hT (hL.adj (d - 1)).symm (hL.adj 0) (hL.ww hT 0).symm (hL.adj 0).symm
  obtain ⟨b, sB, sA⟩ := sides_of_edge C hc ⟨(w (d - 1), u), (hL.adj (d - 1)).symm⟩
    ⟨(w 1, w 0), (hL.ww hT 0).symm⟩ rfl rfl (offw (d - 1) (by omega) (by omega) (by omega))
    (offw 1 (by omega) (by omega) (by omega)) (hL.adj 0) (hL.adj 0).symm f1 f2
  -- arc A: `w_1 … w_{k-1}` on side `b + 1`
  have arcA : ∀ j, 1 ≤ j → j < k → OnSide T c (b + 1) (w j) := by
    intro j h1 hjk
    induction j with
    | zero => omega
    | succ j ih =>
      rcases Nat.eq_zero_or_pos j with rfl | hj
      · exact sA
      · exact onSide_adjC' C hc (offw j (by omega) (by omega) (by omega))
          (offw (j + 1) (by omega) (by omega) (by omega)) (hL.ww hT j) (ih hj (by omega))
  -- arc B: `w_{k+1} … w_{d-1}` on side `b`
  have arcB : ∀ m, m + k + 1 < d → OnSide T c b (w (d - 1 - m)) := by
    intro m hm
    induction m with
    | zero => simpa using sB
    | succ m ih =>
      have e : w (d - 1 - (m + 1) + 1) = w (d - 1 - m) := congrArg w (by omega)
      have ha : T.Adj (w (d - 1 - m)) (w (d - 1 - (m + 1))) := by
        have := hL.ww hT (d - 1 - (m + 1)); rw [e] at this; exact this.symm
      exact onSide_adjC' C hc (offw (d - 1 - m) (by omega) (by omega) (by omega))
        (offw (d - 1 - (m + 1)) (by omega) (by omega) (by omega)) ha (ih (by omega))
  have h2 : BothSides2 T 5 ρ c := by
    intro b'
    by_cases hb' : b' = b
    · subst hb'
      by_cases hk3 : k + 3 ≤ d
      · have s0 := arcB 0 (by omega)
        have s1 := arcB 1 (by omega)
        exact ⟨_, _, _, _, hne (by omega) (by omega) (by omega),
          offw _ (by omega) (by omega) (by omega), s0, (hL.adj _).symm,
          offw _ (by omega) (by omega) (by omega), s1, (hL.adj _).symm⟩
      · have hkk : k = d - 2 := by omega
        obtain ⟨z, hz, z1, z2, z3⟩ := exists_nbr_avoid (T := T) (v := w (d - 1))
          (by have := hT.minDeg (w (d - 1)); omega) u (w (d - 2)) (w 0)
        have zx : z ≠ x := by
          rintro rfl
          exact hnc (d - 1) k hz hyk (Or.inr (Or.inr (by congr 1; omega)))
        have zy : z ≠ y := by
          rintro rfl
          refine hnc 0 (d - 1) hx0 hz (Or.inr (Or.inr ?_))
          rw [show d - 1 + 1 = d by omega, Nat.mod_self, Nat.zero_mod]
        have oz : ¬ OnCyc 5 ρ z := off z z1 z3 zx zy (by rw [hkk]; exact z2)
        have ow := offw (d - 1) (by omega) (by omega) (by omega)
        have s0 := arcB 0 (by omega)
        simp only [Nat.sub_zero] at s0
        exact ⟨_, z, _, _, hz.ne, ow, s0, (hL.adj _).symm, oz, onSide_adjC' C hc ow oz hz s0, hz.symm⟩
    · have hb1 : b' = b + 1 := zmod2_ne _ _ hb'
      subst hb1
      by_cases hk3 : 3 ≤ k
      · exact ⟨w 1, w 2, _, _, hne (by omega) (by omega) (by omega),
          offw _ (by omega) (by omega) (by omega), arcA 1 le_rfl (by omega), (hL.adj _).symm,
          offw _ (by omega) (by omega) (by omega), arcA 2 (by omega) (by omega), (hL.adj _).symm⟩
      · have hkk : k = 2 := by omega
        subst hkk
        obtain ⟨z, hz, z1, z2, z3⟩ := exists_nbr_avoid (T := T) (v := w 1)
          (by have := hT.minDeg (w 1); omega) u (w 0) (w 2)
        have zx : z ≠ x := by
          rintro rfl
          exact hnc 1 2 hz hyk (Or.inr (Or.inl rfl))
        have zy : z ≠ y := by
          rintro rfl
          exact hnc 0 1 hx0 hz (Or.inr (Or.inl rfl))
        have oz : ¬ OnCyc 5 ρ z := off z z1 z2 zx zy z3
        have ow := offw 1 (by omega) (by omega) (by omega)
        exact ⟨_, z, _, _, hz.ne, ow, sA, (hL.adj _).symm, oz, onSide_adjC' C hc ow oz hz sA, hz.symm⟩
  exact hT.noShortSep 5 ρ c C le_rfl hc h2.both (fun _ => h2)

end IsLink

end SimpleGraph.SphericalMap.RSSTSeed

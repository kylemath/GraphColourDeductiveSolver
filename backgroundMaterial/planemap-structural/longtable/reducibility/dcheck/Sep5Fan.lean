import Sep4

/-! Job 25, 5-cycles: the fan surgery. In a pentagonal ring face `σ0 … σ4` with no chords, insert
`σ0σ2` (splitting off the triangle `σ0σ1σ2`) and then `σ0σ3` in the remaining quadrilateral.
The face tracking uses the library's `split_face_old` / `split_face_out`. -/

namespace SimpleGraph.SphericalMap
open VacancySlide RotationSystem PlaneMapConstruction

variable {n : ℕ} {M : SphericalMap n} {r : ℕ} {σ : ℕ → Fin n}

theorem RingFace.faceNext_ringDart (R : RingFace M r σ) (t : ℕ) :
    M.rotation.faceNext (ringDart R t) = ringDart R (t + 1) := by
  have := R.step t; exact this

theorem RingFace.per_mod (R : RingFace M r σ) (x : ℕ) : σ (x % r) = σ x := by
  conv_rhs => rw [← Nat.mod_add_div x r]
  induction x / r with
  | zero => simp
  | succ k ih => rw [Nat.mul_succ, ← Nat.add_assoc, R.per, ih]

theorem RingFace.ringDart_per (R : RingFace M r σ) (t : ℕ) : ringDart R (t + r) = ringDart R t := by
  apply Dart.ext; apply Prod.ext
  · exact R.per t
  · change σ (t + r + 1) = σ (t + 1); rw [show t + r + 1 = (t + 1) + r by omega, R.per]

/-- Shifting the labels of a ring face. -/
theorem RingFace.shift (R : RingFace M r σ) (v : ℕ) : RingFace M r (fun t => σ (t + v)) := by
  refine ⟨R.pos, fun t => ?_, fun t => ?_, fun t => ?_, fun s t hs ht e => ?_⟩
  · show σ (t + r + v) = σ (t + v); rw [show t + r + v = (t + v) + r by omega, R.per]
  · have := R.adj (t + v); rwa [show t + v + 1 = t + 1 + v by omega] at this
  · have := R.step (t + v)
    simp only [show t + v + 1 = t + 1 + v by omega, show t + v + 2 = t + 2 + v by omega] at this
    exact this
  · have hmod : ∀ x, σ (x % r) = σ x := R.per_mod
    have e' : σ ((s + v) % r) = σ ((t + v) % r) := by rw [hmod, hmod]; exact e
    have := R.inj _ _ (Nat.mod_lt _ R.pos) (Nat.mod_lt _ R.pos) e'
    have h2 : s % r = t % r := Nat.ModEq.add_right_cancel' v this
    rwa [Nat.mod_eq_of_lt hs, Nat.mod_eq_of_lt ht] at h2

/-- **The fan map.** A pentagonal ring face without the chords `σ0σ2`, `σ0σ3` admits a spherical map
with both chords added and nothing else changed. -/
theorem RingFace.fanMap (R : RingFace M 5 σ) (h02 : ¬ M.Adj (σ 0) (σ 2))
    (h03 : ¬ M.Adj (σ 0) (σ 3)) :
    ∃ M2 : SphericalMap n, M.graph ≤ M2.graph ∧ M2.Adj (σ 0) (σ 2) ∧ M2.Adj (σ 0) (σ 3) ∧
      ∀ x, 0 < M2.graph.degree x → 0 < M.graph.degree x := by
  classical
  have inj : ∀ i j, i < 5 → j < 5 → i ≠ j → σ i ≠ σ j := fun i j hi hj h e => h (R.inj i j hi hj e)
  have hab : σ 0 ≠ σ 2 := inj 0 2 (by omega) (by omega) (by omega)
  let a := ringDart R 0
  let b := ringDart R 2
  have hface : M.rotation.faceOf a = M.rotation.faceOf b := by
    have e1 := face_bd M (ringDart R 0) 0
    have e2 := face_bd M (ringDart R 0) 2
    rw [ring_bd] at e1 e2
    exact e1.trans e2.symm
  let R1 := split M.rotation a b hab h02
  let G1 := splitGraph M.graph (σ 0) (σ 2) hab
  have fills1 : R1.Fills := split_fills M.rotation M.fills a b hface hab h02
  let out : G1.Dart := splitOut (σ 0) (σ 2) hab
  let b' : G1.Dart := splitOld (σ 0) (σ 2) hab (ringDart R 3)
  -- dart facts in M
  have fst_ne : ∀ (d e : M.Dart), d.fst ≠ e.fst → d ≠ e := fun d e h hde => h (hde ▸ rfl)
  have n4a : ringDart R 4 ≠ a := fst_ne _ _ (inj 4 0 (by omega) (by omega) (by omega))
  have n4b : ringDart R 4 ≠ b := fst_ne _ _ (inj 4 2 (by omega) (by omega) (by omega))
  have e5 : M.rotation.faceNext (ringDart R 4) = a := by
    rw [R.faceNext_ringDart]; exact R.ringDart_per 0
  have hface2 : R1.faceOf out = R1.faceOf b' := by
    have s1 : R1.faceNext b' = splitOld (σ 0) (σ 2) hab (ringDart R 4) := by
      have h := split_face_old (R := M.rotation) (a := a) (b := b) (hab := hab) (hmiss := h02)
        (ringDart R 3)
      rw [R.faceNext_ringDart, if_neg n4a, if_neg n4b] at h
      exact h
    have s2 : R1.faceNext (splitOld (σ 0) (σ 2) hab (ringDart R 4)) = out := by
      have h := split_face_old (R := M.rotation) (a := a) (b := b) (hab := hab) (hmiss := h02)
        (ringDart R 4)
      rw [if_pos e5] at h
      exact h
    rw [← R1.face_of_face_next b', s1, ← R1.face_of_face_next (splitOld (σ 0) (σ 2) hab (ringDart R 4)), s2]
  have hab2 : out.fst ≠ b'.fst := inj 0 3 (by omega) (by omega) (by omega)
  have hmiss2 : ¬ G1.Adj out.fst b'.fst := by
    rintro (h | ⟨-, e⟩ | ⟨e, -⟩)
    · exact h03 h
    · exact inj 3 2 (by omega) (by omega) (by omega) e
    · exact hab e
  let M2 : SphericalMap n := ⟨splitGraph G1 out.fst b'.fst hab2, split R1 out b' hab2 hmiss2,
    split_fills R1 fills1 out b' hface2 hab2 hmiss2⟩
  refine ⟨M2, fun x y h => Or.inl (Or.inl h), Or.inl (Or.inr (Or.inl ⟨rfl, rfl⟩)),
    Or.inr (Or.inl ⟨rfl, rfl⟩), fun x hx => ?_⟩
  obtain ⟨y, hy⟩ := M2.graph.degree_pos_iff_exists_adj x |>.mp hx
  have h0 : 0 < M.graph.degree (σ 0) := M.graph.degree_pos_iff_exists_adj _ |>.mpr ⟨_, R.adj 0⟩
  have h2 : 0 < M.graph.degree (σ 2) := M.graph.degree_pos_iff_exists_adj _ |>.mpr ⟨_, R.adj 2⟩
  have h3 : 0 < M.graph.degree (σ 3) := M.graph.degree_pos_iff_exists_adj _ |>.mpr ⟨_, R.adj 3⟩
  rcases hy with (h | ⟨rfl, -⟩ | ⟨rfl, -⟩) | ⟨rfl, -⟩ | ⟨rfl, -⟩
  · exact M.graph.degree_pos_iff_exists_adj x |>.mpr ⟨y, h⟩
  · exact h0
  · exact h2
  · exact h0
  · exact h3

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.RingFace.fanMap

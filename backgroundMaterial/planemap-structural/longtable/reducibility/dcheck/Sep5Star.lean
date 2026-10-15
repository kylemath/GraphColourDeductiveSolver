import Sep5Fan
import GrowFills

/-! Job 25, 5-cycles: the star surgery. In a pentagonal ring face `σ0 … σ4` of a spherical map on
`Fin n`, add a new vertex `w` (`Fin.last n`) joined to all five ring vertices, as a spherical map on
`Fin (n+1)`: a pendant edge `w σ0` inserted before the ring dart at `σ0` (`growBefore`), then the
chords `w σ2`, `w σ1` (in the quadrilateral `σ1 σ2 w σ0`), `w σ3` and `w σ4` (in the pentagon
`σ0 w σ2 σ3 σ4`, then its quadrilateral part). Faces are tracked with the library's
`grow_before_face_*` and `split_face_*` lemmas. -/

namespace SimpleGraph.SphericalMap
open VacancySlide RotationSystem PlaneMapConstruction

variable {n : ℕ} {M : SphericalMap n} {σ : ℕ → Fin n}

theorem dart_ne_snd {V : Type*} {G : SimpleGraph V} {d e : G.Dart} (h : d.snd ≠ e.snd) : d ≠ e :=
  fun he => h (he ▸ rfl)
theorem dart_ne_fst {V : Type*} {G : SimpleGraph V} {d e : G.Dart} (h : d.fst ≠ e.fst) : d ≠ e :=
  fun he => h (he ▸ rfl)

/-- **The star map.** -/
theorem RingFace.starMap (R : RingFace M 5 σ) :
    ∃ M5 : SphericalMap (n + 1),
      (∀ u v, M.Adj u v → M5.Adj u.castSucc v.castSucc) ∧
      (∀ k, k < 5 → M5.Adj (Fin.last n) (σ k).castSucc) ∧
      (∀ x, 0 < M5.graph.degree x → x = Fin.last n ∨ ∃ y, x = y.castSucc ∧ 0 < M.graph.degree y) := by
  classical
  have inj : ∀ i j, i < 5 → j < 5 → i ≠ j → σ i ≠ σ j := fun i j hi hj h e => h (R.inj i j hi hj e)
  have cs : ∀ i j, i < 5 → j < 5 → i ≠ j → (σ i).castSucc ≠ (σ j).castSucc :=
    fun i j hi hj h e => inj i j hi hj h (Fin.castSucc_injective n e)
  have wne : ∀ k, (Fin.last n) ≠ (σ k).castSucc := fun k e => Fin.castSucc_ne_last _ e.symm
  let rD := ringDart R
  have fN : ∀ k, M.rotation.faceNext (rD k) = rD (k + 1) := R.faceNext_ringDart
  have rD5 : rD 5 = rD 0 := by
    have := R.ringDart_per 0; simpa using this
  -- step 0: the pendant edge
  let u := σ 0
  let a0 := rD 0
  have ha0 : a0.fst = u := rfl
  let G1 := growGraph M.graph u
  let R1 := growBefore u M.rotation a0 ha0
  have F1 : R1.Fills := growBefore_fills u M.rotation M.fills a0 ha0
  let O : M.Dart → G1.Dart := growOld u
  let out : G1.Dart := growOut u
  let back : G1.Dart := growBack u
  have nk : ∀ k, 1 ≤ k → k ≤ 4 → rD k ≠ a0 := fun k h1 h4 =>
    dart_ne_fst (inj k 0 (by omega) (by omega) (by omega))
  have f1O : ∀ k, k ≤ 3 → R1.faceNext (O (rD k)) = O (rD (k + 1)) := by
    intro k hk
    have h := grow_before_face_old u M.rotation a0 ha0 (rD k)
    rw [fN, if_neg (nk (k + 1) (by omega) (by omega))] at h
    exact h
  have f1O4 : R1.faceNext (O (rD 4)) = out := by
    have h := grow_before_face_old u M.rotation a0 ha0 (rD 4)
    rw [fN, show 4 + 1 = 5 by rfl, rD5, if_pos rfl] at h
    exact h
  have f1out : R1.faceNext out = back := grow_before_face_out u M.rotation a0 ha0
  have f1back : R1.faceNext back = O (rD 0) := grow_before_face_back u M.rotation a0 ha0
  -- vertices in G1
  let w : Fin (n + 1) := Fin.last n
  let s : ℕ → Fin (n + 1) := fun k => (σ k).castSucc
  have back_fst : back.fst = w := rfl
  have O_fst : ∀ k, (O (rD k)).fst = s k := fun k => rfl
  -- step 1: chord w σ2 (split before `back` and `O rD2`)
  have h1ab : back.fst ≠ (O (rD 2)).fst := wne 2
  have h1miss : ¬ G1.Adj back.fst (O (rD 2)).fst := by
    rintro (⟨v, w', h, hv, hw⟩ | ⟨hv, hw⟩ | ⟨hv, hw⟩)
    · exact Fin.castSucc_ne_last v hv
    · exact Fin.castSucc_ne_last u hv.symm
    · exact cs 2 0 (by omega) (by omega) (by omega) hw
  have h1face : R1.faceOf back = R1.faceOf (O (rD 2)) := by
    rw [← R1.face_of_face_next back, f1back, ← R1.face_of_face_next (O (rD 0)), f1O 0 (by omega),
      ← R1.face_of_face_next (O (rD 1)), f1O 1 (by omega)]
  let G2 := splitGraph G1 back.fst (O (rD 2)).fst h1ab
  let R2 := split R1 back (O (rD 2)) h1ab h1miss
  have F2 : R2.Fills := split_fills R1 F1 back (O (rD 2)) h1face h1ab h1miss
  let S1 : G1.Dart → G2.Dart := splitOld back.fst (O (rD 2)).fst h1ab
  let out1 : G2.Dart := splitOut back.fst (O (rD 2)).fst h1ab
  let back1 : G2.Dart := splitBack back.fst (O (rD 2)).fst h1ab
  -- dart helpers in G1
  have ne_fs : ∀ {d e : G1.Dart}, d.fst ≠ e.fst → d ≠ e := fun h => dart_ne_fst h
  have sw : ∀ k, s k ≠ w := fun k e => wne k e.symm
  have ss : ∀ i j, i < 5 → j < 5 → i ≠ j → s i ≠ s j := cs
  -- face facts in M2
  have f2 : ∀ (d e : G1.Dart), R1.faceNext d = e → e ≠ back → e ≠ O (rD 2) →
      R2.faceNext (S1 d) = S1 e := by
    intro d e hde h1 h2
    have h := split_face_old R1 back (O (rD 2)) h1ab h1miss d
    rw [hde, if_neg h1, if_neg h2] at h
    exact h
  have f2O1 : R2.faceNext (S1 (O (rD 1))) = back1 := by
    have h := split_face_old R1 back (O (rD 2)) h1ab h1miss (O (rD 1))
    rw [f1O 1 (by omega), if_neg (ne_fs (sw 2)), if_pos rfl] at h
    exact h
  have f2out : R2.faceNext (S1 out) = out1 := by
    have h := split_face_old R1 back (O (rD 2)) h1ab h1miss out
    rw [f1out, if_pos rfl] at h
    exact h
  have f2out1 : R2.faceNext out1 = S1 (O (rD 2)) := split_face_out R1 back (O (rD 2)) h1ab h1miss
  have f2back1 : R2.faceNext back1 = S1 back := split_face_back R1 back (O (rD 2)) h1ab h1miss
  have f2back : R2.faceNext (S1 back) = S1 (O (rD 0)) :=
    f2 _ _ f1back (ne_fs (sw 0)) (ne_fs (ss 0 2 (by omega) (by omega) (by omega)))
  have f2O0 : R2.faceNext (S1 (O (rD 0))) = S1 (O (rD 1)) :=
    f2 _ _ (f1O 0 (by omega)) (ne_fs (sw 1)) (ne_fs (ss 1 2 (by omega) (by omega) (by omega)))
  have f2O2 : R2.faceNext (S1 (O (rD 2))) = S1 (O (rD 3)) :=
    f2 _ _ (f1O 2 (by omega)) (ne_fs (sw 3)) (ne_fs (ss 3 2 (by omega) (by omega) (by omega)))
  have f2O3 : R2.faceNext (S1 (O (rD 3))) = S1 (O (rD 4)) :=
    f2 _ _ (f1O 3 (by omega)) (ne_fs (sw 4)) (ne_fs (ss 4 2 (by omega) (by omega) (by omega)))
  have f2O4 : R2.faceNext (S1 (O (rD 4))) = S1 out :=
    f2 _ _ f1O4 (ne_fs (sw 0)) (ne_fs (ss 0 2 (by omega) (by omega) (by omega)))
  -- step 2: chord w σ1 (split before `S1 back` and `S1 (O rD1)`)
  let a2 := S1 back
  let b2 := S1 (O (rD 1))
  have h2ab : a2.fst ≠ b2.fst := wne 1
  have h2miss : ¬ G2.Adj a2.fst b2.fst := by
    rintro ((⟨v, w', h, hv, hw⟩ | ⟨hv, hw⟩ | ⟨hv, hw⟩) | ⟨hv, hw⟩ | ⟨hv, hw⟩)
    · exact Fin.castSucc_ne_last v hv
    · exact Fin.castSucc_ne_last u hv.symm
    · exact ss 1 0 (by omega) (by omega) (by omega) hw
    · exact ss 1 2 (by omega) (by omega) (by omega) hw
    · exact sw 2 hv.symm
  have h2face : R2.faceOf a2 = R2.faceOf b2 := by
    rw [← R2.face_of_face_next a2, f2back, ← R2.face_of_face_next (S1 (O (rD 0))), f2O0]
  let G3 := splitGraph G2 a2.fst b2.fst h2ab
  let R3 := split R2 a2 b2 h2ab h2miss
  have F3 : R3.Fills := split_fills R2 F2 a2 b2 h2face h2ab h2miss
  let S2 : G2.Dart → G3.Dart := splitOld a2.fst b2.fst h2ab
  have ne2 : ∀ {d e : G2.Dart}, d.fst ≠ e.fst → d ≠ e := fun h => dart_ne_fst h
  have f3 : ∀ (d e : G2.Dart), R2.faceNext d = e → e ≠ a2 → e ≠ b2 →
      R3.faceNext (S2 d) = S2 e := by
    intro d e hde h1 h2
    have h := split_face_old R2 a2 b2 h2ab h2miss d
    rw [hde, if_neg h1, if_neg h2] at h
    exact h
  have f3out : R3.faceNext (S2 (S1 out)) = S2 out1 :=
    f3 _ _ f2out (dart_ne_snd (ss 2 0 (by omega) (by omega) (by omega))) (ne2 (sw 1).symm)
  have f3out1 : R3.faceNext (S2 out1) = S2 (S1 (O (rD 2))) :=
    f3 _ _ f2out1 (ne2 (sw 2)) (ne2 (ss 2 1 (by omega) (by omega) (by omega)))
  have f3O2 : R3.faceNext (S2 (S1 (O (rD 2)))) = S2 (S1 (O (rD 3))) :=
    f3 _ _ f2O2 (ne2 (sw 3)) (ne2 (ss 3 1 (by omega) (by omega) (by omega)))
  have f3O3 : R3.faceNext (S2 (S1 (O (rD 3)))) = S2 (S1 (O (rD 4))) :=
    f3 _ _ f2O3 (ne2 (sw 4)) (ne2 (ss 4 1 (by omega) (by omega) (by omega)))
  have f3O4 : R3.faceNext (S2 (S1 (O (rD 4)))) = S2 (S1 out) :=
    f3 _ _ f2O4 (ne2 (sw 0)) (ne2 (ss 0 1 (by omega) (by omega) (by omega)))
  -- step 3: chord w σ3 (split before `S2 out1` and `S2 (S1 (O rD3))`)
  let a3 := S2 out1
  let b3 := S2 (S1 (O (rD 3)))
  have h3ab : a3.fst ≠ b3.fst := wne 3
  have h3miss : ¬ G3.Adj a3.fst b3.fst := by
    rintro (((⟨v, w', h, hv, hw⟩ | ⟨hv, hw⟩ | ⟨hv, hw⟩) | ⟨hv, hw⟩ | ⟨hv, hw⟩) | ⟨hv, hw⟩ | ⟨hv, hw⟩)
    · exact Fin.castSucc_ne_last v hv
    · exact Fin.castSucc_ne_last u hv.symm
    · exact ss 3 0 (by omega) (by omega) (by omega) hw
    · exact ss 3 2 (by omega) (by omega) (by omega) hw
    · exact sw 2 hv.symm
    · exact ss 3 1 (by omega) (by omega) (by omega) hw
    · exact sw 1 hv.symm
  have h3face : R3.faceOf a3 = R3.faceOf b3 := by
    rw [← R3.face_of_face_next a3, f3out1, ← R3.face_of_face_next (S2 (S1 (O (rD 2)))), f3O2]
  let G4 := splitGraph G3 a3.fst b3.fst h3ab
  let R4 := split R3 a3 b3 h3ab h3miss
  have F4 : R4.Fills := split_fills R3 F3 a3 b3 h3face h3ab h3miss
  let S3 : G3.Dart → G4.Dart := splitOld a3.fst b3.fst h3ab
  let out3 : G4.Dart := splitOut a3.fst b3.fst h3ab
  have ne3 : ∀ {d e : G3.Dart}, d.fst ≠ e.fst → d ≠ e := fun h => dart_ne_fst h
  have f4out3 : R4.faceNext out3 = S3 b3 := split_face_out R3 a3 b3 h3ab h3miss
  have f4b3 : R4.faceNext (S3 b3) = S3 (S2 (S1 (O (rD 4)))) := by
    have h := split_face_old R3 a3 b3 h3ab h3miss b3
    rw [f3O3, if_neg (ne3 (sw 4)), if_neg (ne3 (ss 4 3 (by omega) (by omega) (by omega)))] at h
    exact h
  -- step 4: chord w σ4 (split before `out3` and `S3 (S2 (S1 (O rD4)))`)
  let a4 := out3
  let b4 := S3 (S2 (S1 (O (rD 4))))
  have h4ab : a4.fst ≠ b4.fst := wne 4
  have h4miss : ¬ G4.Adj a4.fst b4.fst := by
    rintro ((((⟨v, w', h, hv, hw⟩ | ⟨hv, hw⟩ | ⟨hv, hw⟩) | ⟨hv, hw⟩ | ⟨hv, hw⟩) | ⟨hv, hw⟩ | ⟨hv, hw⟩)
      | ⟨hv, hw⟩ | ⟨hv, hw⟩)
    · exact Fin.castSucc_ne_last v hv
    · exact Fin.castSucc_ne_last u hv.symm
    · exact ss 4 0 (by omega) (by omega) (by omega) hw
    · exact ss 4 2 (by omega) (by omega) (by omega) hw
    · exact sw 2 hv.symm
    · exact ss 4 1 (by omega) (by omega) (by omega) hw
    · exact sw 1 hv.symm
    · exact ss 4 3 (by omega) (by omega) (by omega) hw
    · exact sw 3 hv.symm
  have h4face : R4.faceOf a4 = R4.faceOf b4 := by
    rw [← R4.face_of_face_next a4, f4out3, ← R4.face_of_face_next (S3 b3), f4b3]
  let M5 : SphericalMap (n + 1) := ⟨splitGraph G4 a4.fst b4.fst h4ab, split R4 a4 b4 h4ab h4miss,
    split_fills R4 F4 a4 b4 h4face h4ab h4miss⟩
  refine ⟨M5, fun x y h => Or.inl (Or.inl (Or.inl (Or.inl (Or.inl ⟨x, y, h, rfl, rfl⟩)))), ?_, ?_⟩
  · intro k hk
    rcases (show k = 0 ∨ k = 1 ∨ k = 2 ∨ k = 3 ∨ k = 4 by omega) with rfl | rfl | rfl | rfl | rfl
    · exact Or.inl (Or.inl (Or.inl (Or.inl (Or.inr (Or.inr ⟨rfl, rfl⟩)))))
    · exact Or.inl (Or.inl (Or.inr (Or.inl ⟨rfl, rfl⟩)))
    · exact Or.inl (Or.inl (Or.inl (Or.inr (Or.inl ⟨rfl, rfl⟩))))
    · exact Or.inl (Or.inr (Or.inl ⟨rfl, rfl⟩))
    · exact Or.inr (Or.inl ⟨rfl, rfl⟩)
  · intro x hx
    obtain ⟨y, hy⟩ := M5.graph.degree_pos_iff_exists_adj x |>.mp hx
    have hpos : ∀ k, 0 < M.graph.degree (σ k) := fun k =>
      M.graph.degree_pos_iff_exists_adj _ |>.mpr ⟨_, R.adj k⟩
    rcases hy with ((((⟨v, w', h, hv, -⟩ | ⟨hv, -⟩ | ⟨hv, -⟩) | ⟨hv, -⟩ | ⟨hv, -⟩) | ⟨hv, -⟩ | ⟨hv, -⟩)
      | ⟨hv, -⟩ | ⟨hv, -⟩) | ⟨hv, -⟩ | ⟨hv, -⟩
    · exact Or.inr ⟨v, hv.symm, M.graph.degree_pos_iff_exists_adj v |>.mpr ⟨w', h⟩⟩
    · exact Or.inr ⟨u, hv, hpos 0⟩
    · exact Or.inl hv
    · exact Or.inl hv
    · exact Or.inr ⟨σ 2, hv, hpos 2⟩
    · exact Or.inl hv
    · exact Or.inr ⟨σ 1, hv, hpos 1⟩
    · exact Or.inl hv
    · exact Or.inr ⟨σ 3, hv, hpos 3⟩
    · exact Or.inl hv
    · exact Or.inr ⟨σ 4, hv, hpos 4⟩

end SimpleGraph.SphericalMap

#print axioms SimpleGraph.SphericalMap.RingFace.starMap

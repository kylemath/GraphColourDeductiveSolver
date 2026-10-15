import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RingReduce

/-! Job 24 follow-up (Studio, exploratory): the mirror spherical map. Reversing every vertex's
rotation (`next ↦ next⁻¹`) keeps the graph; its faces are the original faces with every dart
reversed (`faceNext' = symm ∘ faceNext⁻¹ ∘ symm`), so `Fills` and `Triangulated` transfer, and
`Nx (mirror T) u v w ↔ Nx T u w v`. Hence an occurrence of the mirror image of a configuration in
`T` is an occurrence of the configuration itself in `mirror T`, a map with the same graph: every
per-key `colorable_of_occ_dred` also reduces the mirror image, with the same `hD`. -/

namespace SimpleGraph

/-- Reversed rotation (as `QuarterMirror.RotationSystem.mirror`, which is not in this import chain). -/
def RotationSystem.rmirror {V : Type*} {G : SimpleGraph V} (R : RotationSystem G) :
    RotationSystem G where
  next := R.next.symm
  next_fst d := by
    have e := R.next_fst (R.next.symm d)
    rw [Equiv.apply_symm_apply] at e
    exact e.symm
  cyclic d e hde := by
    obtain ⟨k, hk⟩ := R.cyclic e d hde.symm
    exact ⟨k, by rw [← hk]; exact Function.LeftInverse.iterate R.next.symm_apply_apply k e⟩

namespace RotationSystem

variable {V : Type*} {G : SimpleGraph V} (R : RotationSystem G)

theorem rmirror_faceNext (d : G.Dart) : R.rmirror.faceNext d = R.next.symm d.symm := rfl

theorem faceRel_of_rmirror {d e : G.Dart} (h : R.rmirror.FaceRelation d e) :
    R.FaceRelation d.symm e.symm := by
  induction h with
  | refl d => exact FaceRelation.refl _
  | step d =>
    apply FaceRelation.symm
    have : R.faceNext (R.rmirror.faceNext d).symm = d.symm := by
      rw [face_next_apply, rmirror_faceNext, Dart.symm_symm]; exact Equiv.apply_symm_apply _ _
    have hs := FaceRelation.step (R := R) (R.rmirror.faceNext d).symm
    rwa [this] at hs
  | symm _ ih => exact FaceRelation.symm ih
  | trans _ _ ih1 ih2 => exact FaceRelation.trans ih1 ih2

theorem rmirror_faceRel_of {d e : G.Dart} (h : R.FaceRelation d e) :
    R.rmirror.FaceRelation d.symm e.symm := by
  induction h with
  | refl d => exact FaceRelation.refl _
  | step d =>
    apply FaceRelation.symm
    have : R.rmirror.faceNext (R.faceNext d).symm = d.symm := by
      rw [rmirror_faceNext, Dart.symm_symm, face_next_apply]; exact Equiv.symm_apply_apply _ _
    have hs := FaceRelation.step (R := R.rmirror) (R.faceNext d).symm
    rwa [this] at hs
  | symm _ ih => exact FaceRelation.symm ih
  | trans _ _ ih1 ih2 => exact FaceRelation.trans ih1 ih2

theorem rmirror_faceOf_eq_iff (d e : G.Dart) :
    R.rmirror.faceOf d = R.rmirror.faceOf e ↔ R.faceOf d.symm = R.faceOf e.symm := by
  rw [face_of_eq_iff, face_of_eq_iff]
  exact ⟨R.faceRel_of_rmirror, fun h => by
    have := R.rmirror_faceRel_of h; rwa [Dart.symm_symm, Dart.symm_symm] at this⟩

end RotationSystem

theorem RotationSystem.rmirror_fills {n : ℕ} {G : SimpleGraph (Fin n)} (R : RotationSystem G)
    (hR : R.Fills) : R.rmirror.Fills := by
  classical
  intro φ hφ
  obtain ⟨c, hc⟩ := hR φ hφ
  let c' : R.rmirror.Face → ZMod 2 := fun f => match f with
    | Sum.inl q => Quotient.lift (s := R.rmirror.faceSetoid) (fun d => c (R.faceOf d.symm))
        (fun a b hab => by
          have := (R.rmirror_faceOf_eq_iff a b).1 ((R.rmirror.face_of_eq_iff a b).2 hab)
          simp only [this]) q
    | Sum.inr _ => 0
  refine ⟨c', fun d => ?_⟩
  have e1 : c' (R.rmirror.faceOf d) = c (R.faceOf d.symm) := rfl
  have e2 : c' (R.rmirror.faceOf d.symm) = c (R.faceOf d) := by
    show c (R.faceOf d.symm.symm) = _; rw [Dart.symm_symm]
  rw [e1, e2, hc d, add_comm]

namespace SphericalMap

variable {n : ℕ}

/-- **The mirror map**: same graph, every rotation reversed. -/
def mirror (T : SphericalMap n) : SphericalMap n :=
  ⟨T.graph, T.rotation.rmirror, T.rotation.rmirror_fills T.fills⟩

@[simp] theorem mirror_graph (T : SphericalMap n) : T.mirror.graph = T.graph := rfl

theorem mirror_triangulated {T : SphericalMap n} (h : T.Triangulated) : T.mirror.Triangulated := by
  classical
  intro d
  have h3 := h d.symm
  unfold RotationSystem.faceLength at h3 ⊢
  rw [← h3]
  apply Fintype.card_congr
  refine ⟨fun e => ⟨e.1.symm, ?_⟩, fun e => ⟨e.1.symm, ?_⟩, fun e => ?_, fun e => ?_⟩
  · have := (T.rotation.rmirror_faceOf_eq_iff e.1 d).1 e.2; exact this
  · have := (T.rotation.rmirror_faceOf_eq_iff e.1.symm d).2 (by rw [Dart.symm_symm]; exact e.2)
    exact this
  · exact Subtype.ext (Dart.symm_symm _)
  · exact Subtype.ext (Dart.symm_symm _)

theorem nx_mirror {T : SphericalMap n} {u v w : Fin n} :
    Nx T.mirror u v w ↔ Nx T u w v := by
  constructor
  · rintro ⟨huv, hw⟩
    set e := T.rotation.next.symm ⟨(u, v), huv⟩ with he
    have hfst : e.fst = u := by
      have := T.rotation.next_fst e; rw [he, Equiv.apply_symm_apply] at this; exact this.symm
    have hsnd : e.snd = w := hw
    have hadj : T.Adj u w := by have := e.adj; rw [hfst, hsnd] at this; exact this
    refine ⟨hadj, ?_⟩
    have hee : (⟨(u, w), hadj⟩ : T.Dart) = e := by
      apply Dart.ext; apply Prod.ext <;> simp [hfst, hsnd]
    rw [hee, he, Equiv.apply_symm_apply]
  · rintro ⟨huw, hv⟩
    set e := T.rotation.next ⟨(u, w), huw⟩ with he
    have hfst : e.fst = u := T.rotation.next_fst _
    have huv : T.Adj u v := by have := e.adj; rw [hfst, hv] at this; exact this
    refine ⟨huv, ?_⟩
    have hee : (⟨(u, v), huv⟩ : T.Dart) = e := by
      apply Dart.ext; apply Prod.ext <;> simp [hfst, hv]
    show (T.rotation.next.symm ⟨(u, v), huv⟩).snd = w
    rw [hee, he, Equiv.symm_apply_apply]

end SphericalMap
end SimpleGraph

#print axioms SimpleGraph.SphericalMap.mirror_triangulated
#print axioms SimpleGraph.SphericalMap.nx_mirror

import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RingReduce

/-! Job 25 (star surgery, library gap): adding a leaf at a nonempty corner (`growBefore`) preserves
`Fills`. An even edge combination vanishes on the new pendant edge (the leaf's incidence is that
edge alone); on the old edges it is even, so it has an old face potential `c0`, and the potential
of a new face is `c0` of the old face its darts collapse to (`growForget`). -/

namespace SimpleGraph.PlaneMapConstruction
open RotationSystem

variable {n : ℕ} {H : SimpleGraph (Fin n)} (u : Fin n)

/-- Old edges in the leaf extension. -/
def growOldEdge (e : H.edgeSet) : (growGraph H u).edgeSet :=
  ⟨Sym2.map Fin.castSucc e.val, by
    rcases e with ⟨e, he⟩
    induction e using Sym2.ind with
    | _ x y => exact (grow_graph_adj_cast u x y).2 he⟩

/-- The pendant edge. -/
def growNewEdge : (growGraph H u).edgeSet :=
  ⟨s(u.castSucc, Fin.last n), (grow_graph_adj_last u u).2 rfl⟩

theorem growOldEdge_injective : Function.Injective (growOldEdge (H := H) u) := by
  intro e f h
  apply Subtype.ext
  have := congrArg Subtype.val h
  exact Sym2.map.injective (Fin.castSucc_injective n) this

theorem last_not_mem_old (e : H.edgeSet) : Fin.last n ∉ (growOldEdge u e).val := by
  rcases e with ⟨e, he⟩
  induction e using Sym2.ind with
  | _ x y =>
    intro h
    change Fin.last n ∈ Sym2.map Fin.castSucc s(x, y) at h
    obtain ⟨b, -, hb⟩ := Sym2.mem_map.1 h
    exact Fin.castSucc_ne_last b hb

theorem grow_edge_cases (e : (growGraph H u).edgeSet) :
    (∃ f, e = growOldEdge u f) ∨ e = growNewEdge u := by
  rcases e with ⟨e, he⟩
  induction e using Sym2.ind with
  | _ x y =>
    have he' : (growGraph H u).Adj x y := he
    rcases he' with ⟨v, w, h, hv, hw⟩ | ⟨hx, hy⟩ | ⟨hx, hy⟩
    · subst hv hw; exact Or.inl ⟨⟨s(v, w), h⟩, rfl⟩
    · subst hx hy; exact Or.inr rfl
    · subst hx hy; exact Or.inr (Subtype.ext Sym2.eq_swap)

/-- The edge correspondence. -/
noncomputable def growEdgeEquiv : H.edgeSet ⊕ Unit ≃ (growGraph H u).edgeSet :=
  Equiv.ofBijective (fun x => match x with | .inl e => growOldEdge u e | .inr _ => growNewEdge u)
    ⟨by
      rintro (e | ⟨⟩) (f | ⟨⟩) h
      · exact congrArg Sum.inl (growOldEdge_injective u h)
      · exfalso; apply last_not_mem_old u e
        have := congrArg Subtype.val h; simp only at this; rw [this]; simp [growNewEdge]
      · exfalso; apply last_not_mem_old u f
        have := congrArg Subtype.val h; simp only at this; rw [← this]; simp [growNewEdge]
      · rfl,
    by
      intro e
      rcases grow_edge_cases u e with ⟨f, rfl⟩ | rfl
      · exact ⟨.inl f, rfl⟩
      · exact ⟨.inr (), rfl⟩⟩

theorem castSucc_mem_old (x : Fin n) (e : H.edgeSet) :
    x.castSucc ∈ (growOldEdge u e).val ↔ x ∈ e.val := by
  change x.castSucc ∈ Sym2.map Fin.castSucc e.val ↔ _
  rw [Sym2.mem_map]
  exact ⟨fun ⟨b, hb, e⟩ => (Fin.castSucc_injective n e) ▸ hb, fun h => ⟨x, h, rfl⟩⟩

theorem growOld_symm (d : H.Dart) : (growOld u d).symm = growOld u d.symm := by apply Dart.ext; rfl

theorem edgeOfDart_growOld (d : H.Dart) :
    edgeOfDart (growOld u d) = growOldEdge u (edgeOfDart d) := by
  apply Subtype.ext; rfl

theorem edgeOfDart_growOut : edgeOfDart (growOut (H := H) u) = growNewEdge u := by
  apply Subtype.ext; rfl

theorem edgeOfDart_growBack : edgeOfDart (growBack (H := H) u) = growNewEdge u := by
  apply Subtype.ext; exact Sym2.eq_swap

/-- **Adding a leaf at a nonempty corner preserves `Fills`.** -/
theorem growBefore_fills (R : RotationSystem H) (hR : R.Fills) (a : H.Dart) (ha : a.fst = u) :
    (growBefore u R a ha).Fills := by
  classical
  intro φ hφ
  -- the pendant edge carries 0
  have hnew : φ (growNewEdge u) = 0 := by
    have h := hφ (Fin.last n)
    unfold edgeIncidence at h
    rw [← Fintype.sum_equiv (growEdgeEquiv u) _ _ (fun _ => rfl), Fintype.sum_sum_type] at h
    have h0 : ∀ e : H.edgeSet, (if Fin.last n ∈ (growEdgeEquiv u (.inl e)).val then
        φ (growEdgeEquiv u (.inl e)) else 0) = 0 := fun e => if_neg (last_not_mem_old u e)
    rw [Finset.sum_congr rfl (fun e _ => h0 e), Finset.sum_const_zero, zero_add] at h
    simpa [growEdgeEquiv, growNewEdge] using h
  -- the old part is even
  let φ0 : H.edgeSet → ZMod 2 := fun e => φ (growOldEdge u e)
  have heven : ∀ x, edgeIncidence H φ0 x = 0 := by
    intro x
    have h := hφ x.castSucc
    unfold edgeIncidence at h ⊢
    rw [← Fintype.sum_equiv (growEdgeEquiv u) _ _ (fun _ => rfl), Fintype.sum_sum_type] at h
    have hn : (if x.castSucc ∈ (growEdgeEquiv (H := H) u (Sum.inr ())).val then
        φ (growEdgeEquiv (H := H) u (Sum.inr ())) else 0) = 0 := by
      change (if x.castSucc ∈ (growNewEdge (H := H) u).val then φ (growNewEdge u) else 0) = 0
      rw [hnew]; simp
    simp only [Finset.univ_unique, Finset.sum_singleton] at h
    rw [hn, add_zero] at h
    refine Eq.trans ?_ h
    apply Finset.sum_congr rfl
    intro e _
    change _ = (if x.castSucc ∈ (growOldEdge u e).val then φ (growOldEdge u e) else 0)
    by_cases hx : x ∈ e.val
    · rw [if_pos hx, if_pos ((castSucc_mem_old u x e).2 hx)]
    · rw [if_neg hx, if_neg (fun h => hx ((castSucc_mem_old u x e).1 h))]
  obtain ⟨c0, hc0⟩ := hR φ0 heven
  -- the potential of a new face
  let c' : (growBefore u R a ha).Face → ZMod 2 := fun f => match f with
    | .inl q => c0 (.inl ((growBeforeOrbitEquiv u R a ha).symm q))
    | .inr _ => 0
  have hcf : ∀ d, c' ((growBefore u R a ha).faceOf d) = c0 (R.faceOf (growForget u a d)) := by
    intro d; rfl
  refine ⟨c', fun d => ?_⟩
  rw [hcf, hcf]
  obtain ⟨x, rfl⟩ := (growDartEquiv (H := H) u).surjective d
  rcases x with d0 | (_ | _)
  · change φ (edgeOfDart (growOld u d0)) = c0 (R.faceOf (growForget u a (growOld u d0))) +
      c0 (R.faceOf (growForget u a (growOld u d0).symm))
    rw [growOld_symm, grow_forget_old, grow_forget_old, edgeOfDart_growOld]
    exact hc0 d0
  · change φ (edgeOfDart (growOut u)) = c0 (R.faceOf (growForget u a (growOut u))) +
      c0 (R.faceOf (growForget u a (growOut u).symm))
    rw [edgeOfDart_growOut, hnew, grow_forget_out]
    change 0 = _ + c0 (R.faceOf (growForget u a (growBack u)))
    rw [grow_forget_back]
    exact (show ∀ x : ZMod 2, 0 = x + x by decide) _
  · change φ (edgeOfDart (growBack u)) = c0 (R.faceOf (growForget u a (growBack u))) +
      c0 (R.faceOf (growForget u a (growBack u).symm))
    rw [edgeOfDart_growBack, hnew, grow_forget_back]
    change 0 = _ + c0 (R.faceOf (growForget u a (growOut u)))
    rw [grow_forget_out]
    exact (show ∀ x : ZMod 2, 0 = x + x by decide) _

end SimpleGraph.PlaneMapConstruction

#print axioms SimpleGraph.PlaneMapConstruction.growBefore_fills

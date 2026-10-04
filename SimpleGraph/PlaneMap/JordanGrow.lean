/-
Copyright (c) 2026 Mathlib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Mathlib contributors
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.Jordan
public import Mathlib.Data.Fintype.BigOperators

/-!
# Even sets under one-leaf extension

Old edges of a one-leaf extension are images under `Fin.castSucc`. An even
combination on the grown map restricts to an even combination on the old map.
At a nonempty corner, face-boundary coefficients transport along
`growBeforeFaceEquiv`.
-/

@[expose] public section

namespace SimpleGraph

open scoped BigOperators
open PlaneMapConstruction

namespace PlaneMap

open Classical

variable {n : ℕ}

theorem mem_growOldEdge (H : SimpleGraph (Fin n)) (u : Fin n)
    (e : H.edgeSet) (x : Fin n) :
    x.castSucc ∈ (growOldEdge H u e).val ↔ x ∈ e.val := by
  rcases e with ⟨e, he⟩
  revert he
  refine Sym2.inductionOn e ?_
  intro a b _
  simp only [growOldEdge, Sym2.map_mk, Sym2.mem_iff]
  constructor
  · intro h
    rcases h with h | h
    · exact Or.inl (Fin.castSucc_injective n h)
    · exact Or.inr (Fin.castSucc_injective n h)
  · intro h
    rcases h with h | h <;> simp [h]

theorem last_not_mem_growOldEdge (H : SimpleGraph (Fin n)) (u : Fin n)
    (e : H.edgeSet) : Fin.last n ∉ (growOldEdge H u e).val := by
  rcases e with ⟨e, he⟩
  revert he
  refine Sym2.inductionOn e ?_
  intro a b _
  simp only [growOldEdge, Sym2.map_mk, Sym2.mem_iff, not_or]
  exact ⟨fun h => Fin.castSucc_ne_last a h.symm,
    fun h => Fin.castSucc_ne_last b h.symm⟩

theorem growOldEdge_injective (H : SimpleGraph (Fin n)) (u : Fin n) :
    Function.Injective (growOldEdge (H := H) u) := by
  intro e₁ e₂ h
  apply Subtype.ext
  exact (Function.Embedding.sym2Map
    ⟨Fin.castSucc, Fin.castSucc_injective n⟩).injective (congrArg Subtype.val h)

/-- Every grown edge is the new leaf or the image of a unique old edge. -/
theorem grow_edge_dichotomy (H : SimpleGraph (Fin n)) (u : Fin n)
    (e : (growGraph H u).edgeSet) :
    e = growNewEdge H u ∨ ∃! e0 : H.edgeSet, e = growOldEdge H u e0 := by
  rcases e with ⟨e, he⟩
  revert he
  refine Sym2.inductionOn e ?_
  intro x y h
  rcases h with hold | hnew | hrev
  · obtain ⟨v, w, hvw, hx, hy⟩ := hold
    have hval : s(x, y) = Sym2.map Fin.castSucc s(v, w) := by
      have hp : (x, y) = (v.castSucc, w.castSucc) :=
        Prod.ext hx.symm hy.symm
      have hs : s(x, y) = s(v.castSucc, w.castSucc) :=
        congrArg (fun p : Fin (n + 1) × Fin (n + 1) => s(p.1, p.2)) hp
      rw [hs, Sym2.map_mk]
    refine Or.inr ⟨⟨s(v, w), hvw⟩, Subtype.ext hval, fun e' he' =>
      growOldEdge_injective H u (he'.symm.trans (Subtype.ext hval))⟩
  · refine Or.inl ?_
    apply Subtype.ext
    change s(x, y) = s(u.castSucc, Fin.last n)
    have hxy : (x, y) = (u.castSucc, Fin.last n) := Prod.ext hnew.1 hnew.2
    simp [hxy]
  · refine Or.inl ?_
    apply Subtype.ext
    change s(x, y) = s(u.castSucc, Fin.last n)
    have hxy : (x, y) = (Fin.last n, u.castSucc) := Prod.ext hrev.1 hrev.2
    simp [hxy]

/-- Transport an old edge into a grown plane map. -/
def growMapEdge (M : PlaneMap n) (u : Fin n) (c : M.rotation.Corner u)
    (e : M.graph.edgeSet) : (M.grow u c).graph.edgeSet :=
  ⟨(growOldEdge M.graph u e).val, (growOldEdge M.graph u e).property⟩

theorem growMapEdge_val (M : PlaneMap n) (u : Fin n)
    (c : M.rotation.Corner u) (e : M.graph.edgeSet) :
    (growMapEdge M u c e).val = (growOldEdge M.graph u e).val :=
  rfl

theorem growMapEdge_injective (M : PlaneMap n) (u : Fin n)
    (c : M.rotation.Corner u) :
    Function.Injective (growMapEdge M u c) := by
  intro e₁ e₂ h
  exact growOldEdge_injective M.graph u
    (Subtype.ext (congrArg Subtype.val h))

theorem grow_map_edge_dichotomy (M : PlaneMap n) (u : Fin n)
    (c : M.rotation.Corner u) (e : (M.grow u c).graph.edgeSet) :
    e = growLeafEdge M u c ∨ ∃ e0, e = growMapEdge M u c e0 := by
  rcases grow_edge_dichotomy M.graph u ⟨e.val, e.property⟩ with h | ⟨e0, he0, _⟩
  · refine Or.inl (Subtype.ext ?_)
    simpa [growLeafEdge, growNewEdge] using congrArg Subtype.val h
  · refine Or.inr ⟨e0, Subtype.ext ?_⟩
    simpa [growMapEdge] using congrArg Subtype.val he0

/-- Pair the new leaf edge with the transported old edges. -/
noncomputable def growEdgeEquiv (M : PlaneMap n) (u : Fin n)
    (c : M.rotation.Corner u) :
    Option M.graph.edgeSet ≃ (M.grow u c).graph.edgeSet :=
  Equiv.ofBijective
    (fun x => match x with
      | none => growLeafEdge M u c
      | some e => growMapEdge M u c e)
    ⟨fun x y h => by
      cases x with
      | none =>
        cases y with
        | none => rfl
        | some e =>
          have hv := congrArg Subtype.val h
          have : Fin.last n ∈ (growMapEdge M u c e).val := by
            rw [← hv]
            simp [growLeafEdge, Sym2.mem_iff]
          exact (last_not_mem_growOldEdge M.graph u e this).elim
      | some e =>
        cases y with
        | none =>
          have hv := congrArg Subtype.val h
          have : Fin.last n ∈ (growMapEdge M u c e).val := by
            rw [hv]
            simp [growLeafEdge, Sym2.mem_iff]
          exact (last_not_mem_growOldEdge M.graph u e this).elim
        | some e' =>
          exact congrArg some (growMapEdge_injective M u c h),
      fun e => by
        rcases grow_map_edge_dichotomy M u c e with h | ⟨e0, h⟩
        · exact ⟨none, h.symm⟩
        · exact ⟨some e0, h.symm⟩⟩

/-- Restrict a grown combination to the old edges. -/
def restrictGrow {M : PlaneMap n} {u : Fin n} {c : M.rotation.Corner u}
    (φ : (M.grow u c).graph.edgeSet → ZMod 2) (e : M.graph.edgeSet) : ZMod 2 :=
  φ (growMapEdge M u c e)

theorem sum_grow_edges (M : PlaneMap n) (u : Fin n)
    (c : M.rotation.Corner u) (f : (M.grow u c).graph.edgeSet → ZMod 2) :
    ∑ e, f e = f (growLeafEdge M u c) + ∑ e, f (growMapEdge M u c e) := by
  have h := Fintype.sum_equiv (growEdgeEquiv M u c)
    (fun x => f (growEdgeEquiv M u c x)) f (fun _ => rfl)
  have hopt : ∑ x : Option M.graph.edgeSet, f (growEdgeEquiv M u c x) =
      f (growLeafEdge M u c) + ∑ e, f (growMapEdge M u c e) := by
    rw [Fintype.sum_option]
    rfl
  exact h.symm.trans hopt

theorem incident_sum_grow_cast (M : PlaneMap n) (u : Fin n)
    (c : M.rotation.Corner u) (φ : (M.grow u c).graph.edgeSet → ZMod 2)
    (v : Fin n) :
    incidentSum (M.grow u c) φ v.castSucc =
      incidentSum M (restrictGrow φ) v +
        if v = u then φ (growLeafEdge M u c) else 0 := by
  unfold incidentSum restrictGrow
  have hsum := sum_grow_edges M u c
    (fun e => if v.castSucc ∈ e.val then φ e else 0)
  have hleaf : (if v.castSucc ∈ (growLeafEdge M u c).val then
      φ (growLeafEdge M u c) else 0) =
      if v = u then φ (growLeafEdge M u c) else 0 := by
    have : v.castSucc ∈ (growLeafEdge M u c).val ↔ v = u := by
      simp only [growLeafEdge, Sym2.mem_iff]
      constructor
      · intro h
        rcases h with h | h
        · exact Fin.castSucc_injective n h
        · exact (Fin.castSucc_ne_last v h).elim
      · intro h
        exact Or.inl (congrArg Fin.castSucc h)
    by_cases hv : v = u
    · rw [ite_eq_left (this.2 hv), ite_eq_left hv]
    · rw [ite_eq_right (fun h => hv (this.1 h)), ite_eq_right hv]
  have hold : (∑ e, if v.castSucc ∈ (growMapEdge M u c e).val then
      φ (growMapEdge M u c e) else 0) =
      ∑ e, if v ∈ e.val then φ (growMapEdge M u c e) else 0 := by
    apply Finset.sum_congr rfl
    intro e _
    simp [growMapEdge, mem_growOldEdge]
  rw [hsum, hleaf, hold]
  ac_rfl

theorem even_restrict_grow (M : PlaneMap n) (u : Fin n)
    (c : M.rotation.Corner u) (φ : (M.grow u c).graph.edgeSet → ZMod 2)
    (hφ : IsEven (M.grow u c) φ) : IsEven M (restrictGrow φ) := by
  intro v
  have hcast := incident_sum_grow_cast M u c φ v
  have h0 := hφ v.castSucc
  have hleaf := even_grow_new_zero M u c φ hφ
  have hite : (if v = u then φ (growLeafEdge M u c) else 0) = 0 := by
    split_ifs <;> simp [hleaf]
  rw [hcast, hite, add_zero] at h0
  exact h0

theorem grow_before_face_of_old {H : SimpleGraph (Fin n)}
    (R : RotationSystem H) (u : Fin n) (a : H.Dart) (ha : a.fst = u)
    (d : H.Dart) :
    (growBefore u R a ha).faceOf (growOld u d) =
      growBeforeFaceEquiv u R a ha (R.faceOf d) := by
  change (growBefore u R a ha).faceOf (growOld u d) =
    ((growBefore u R a ha).faceQuotientEquiv (growOut u)).symm
      (growBeforeOrbitEquiv u R a ha
        (R.faceQuotientEquiv a (R.faceOf d)))
  have h1 : R.faceQuotientEquiv a (R.faceOf d) =
      Quotient.mk R.faceSetoid d :=
    rfl
  have h2 : growBeforeOrbitEquiv u R a ha (Quotient.mk R.faceSetoid d) =
      Quotient.mk (growBefore u R a ha).faceSetoid (growOld u d) :=
    rfl
  have h3 : ((growBefore u R a ha).faceQuotientEquiv (growOut u)).symm
      (Quotient.mk (growBefore u R a ha).faceSetoid (growOld u d)) =
      (growBefore u R a ha).faceOf (growOld u d) :=
    rfl
  rw [h1, h2, h3]

/-- An old-edge dart of the grown graph comes from an old dart. -/
theorem grow_map_is_old (H : SimpleGraph (Fin n)) (u : Fin n)
    (e : H.edgeSet) (d : (growGraph H u).Dart)
    (h : RotationSystem.edgeOfDart d = growOldEdge H u e) :
    ∃ d0 : H.Dart, d = growOld u d0 := by
  obtain ⟨x, rfl⟩ := (growDartEquiv (H := H) u).surjective d
  cases x with
  | inl d0 => exact ⟨d0, rfl⟩
  | inr b =>
    have hleaf :
        RotationSystem.edgeOfDart (growDartEquiv (H := H) u (.inr b)) =
          growNewEdge H u := by
      cases b with
      | false => exact grow_out_edge H u
      | true => exact grow_back_edge H u
    have hne : growOldEdge H u e ≠ growNewEdge H u := by
      intro heq
      exact last_not_mem_growOldEdge H u e (by
        rw [heq]
        simp [growNewEdge, Sym2.mem_iff])
    exact (hne (h.symm.trans hleaf)).elim

theorem growOld_injective (H : SimpleGraph (Fin n)) (u : Fin n) :
    Function.Injective (growOld (H := H) u) :=
  fun _ _ h => Sum.inl.inj (grow_dart_injective u h)

theorem grow_old_edge_eq_map (M : PlaneMap n) (u : Fin n)
    (c : M.rotation.Corner u) (d : M.Dart) :
    RotationSystem.edgeOfDart (growOld (H := M.graph) u d) =
      growMapEdge M u c (RotationSystem.edgeOfDart d) := by
  apply Subtype.ext
  simpa [growMapEdge] using
    congrArg Subtype.val (grow_old_edge_dart M.graph u d)

/-- The two darts of an old edge map to the two darts of `growMapEdge`. -/
theorem grow_old_edge_fiber (M : PlaneMap n) (u : Fin n)
    (c : M.rotation.Corner u) (d : M.Dart)
    (d' : (growGraph M.graph u).Dart)
    (h : RotationSystem.edgeOfDart d' =
      growMapEdge M u c (RotationSystem.edgeOfDart d)) :
    d' = growOld (H := M.graph) u d ∨
      d' = growOld (H := M.graph) u d.symm := by
  have hd := (RotationSystem.edge_of_dart_eq_iff d'
      (growOld (H := M.graph) u d)).1
    (h.trans (grow_old_edge_eq_map M u c d).symm)
  simpa [grow_old_symm] using hd

theorem boundary_grow_old (M : PlaneMap n) (u : Fin n)
    (a : M.Dart) (ha : a.fst = u) (f : M.Face) (e : M.graph.edgeSet) :
    (M.grow u (.before a ha)).boundary
      (growBeforeFaceEquiv u M.rotation a ha f)
      (growMapEdge M u (.before a ha) e) =
    M.boundary f e := by
  apply Eq.trans (boundary_eq _ _ _)
  apply Eq.symm
  apply Eq.trans (boundary_eq _ _ _)
  apply Eq.symm
  let S := {d : M.Dart // M.faceOf d = f ∧ RotationSystem.edgeOfDart d = e}
  let T := {d : (M.grow u (.before a ha)).Dart //
    (M.grow u (.before a ha)).faceOf d =
      growBeforeFaceEquiv u M.rotation a ha f ∧
    RotationSystem.edgeOfDart d = growMapEdge M u (.before a ha) e}
  have hfiber (d : S) :
      (growOld u d.val : (M.grow u (.before a ha)).Dart) ∈
        {d : (M.grow u (.before a ha)).Dart |
          (M.grow u (.before a ha)).faceOf d =
            growBeforeFaceEquiv u M.rotation a ha f ∧
          RotationSystem.edgeOfDart d =
            growMapEdge M u (.before a ha) e} := by
    constructor
    · change (growBefore u M.rotation a ha).faceOf (growOld u d.val) =
        growBeforeFaceEquiv u M.rotation a ha f
      rw [grow_before_face_of_old]
      exact congrArg (growBeforeFaceEquiv u M.rotation a ha) d.property.1
    · have hmap := grow_old_edge_eq_map M u (.before a ha) d.val
      rw [d.property.2] at hmap
      exact hmap
  let toT (d : S) : T := ⟨growOld u d.val, hfiber d⟩
  have hinj : Function.Injective toT :=
    fun d₁ d₂ h =>
      Subtype.ext (growOld_injective M.graph u (congrArg Subtype.val h))
  have hsurj : Function.Surjective toT := by
    intro t
    have hedge : RotationSystem.edgeOfDart t.val =
        growOldEdge M.graph u e :=
      Subtype.ext (congrArg Subtype.val t.property.2)
    obtain ⟨d0, hd0⟩ := grow_map_is_old M.graph u e t.val hedge
    have hf : M.faceOf d0 = f := by
      have h := t.property.1
      rw [hd0] at h
      change (growBefore u M.rotation a ha).faceOf (growOld u d0) =
        growBeforeFaceEquiv u M.rotation a ha f at h
      rw [grow_before_face_of_old] at h
      exact (growBeforeFaceEquiv u M.rotation a ha).injective h
    have he : RotationSystem.edgeOfDart d0 = e := by
      have h := t.property.2
      rw [hd0] at h
      have hmap := grow_old_edge_eq_map M u (.before a ha) d0
      exact growMapEdge_injective M u (.before a ha) (hmap.symm.trans h)
    exact ⟨⟨d0, And.intro hf he⟩, Subtype.ext hd0.symm⟩
  exact congrArg Nat.cast
    (Fintype.card_congr (Equiv.ofBijective toT ⟨hinj, hsurj⟩)).symm

theorem even_boundary_grow_before (M : PlaneMap n) (u : Fin n)
    (a : M.Dart) (ha : a.fst = u)
    (hM : ∀ φ : M.graph.edgeSet → ZMod 2, IsEven M φ →
      ∃ c : M.Face → ZMod 2, ∀ e, φ e = ∑ f, c f * M.boundary f e)
    (φ : (M.grow u (.before a ha)).graph.edgeSet → ZMod 2)
    (hφ : IsEven (M.grow u (.before a ha)) φ) :
    ∃ c : (M.grow u (.before a ha)).Face → ZMod 2,
      ∀ e, φ e = ∑ f, c f *
        (M.grow u (.before a ha)).boundary f e := by
  obtain ⟨c0, hc0⟩ :=
    hM (restrictGrow φ) (even_restrict_grow M u (.before a ha) φ hφ)
  let Φ : M.Face ≃ (M.grow u (.before a ha)).Face :=
    growBeforeFaceEquiv u M.rotation a ha
  refine ⟨fun f => c0 (Φ.symm f), ?_⟩
  intro e
  rcases grow_map_edge_dichotomy M u (.before a ha) e with he | ⟨e0, he⟩
  · rw [he, even_grow_new_zero M u (.before a ha) φ hφ]
    simp [boundary_grow_new]
  · subst e
    have hφe := hc0 e0
    change restrictGrow φ e0 = _
    rw [hφe]
    exact Fintype.sum_equiv Φ
      (fun f0 => c0 f0 * M.boundary f0 e0)
      (fun f => c0 (Φ.symm f) *
        (M.grow u (.before a ha)).boundary f
          (growMapEdge M u (.before a ha) e0))
      (fun f0 => by
        rw [Equiv.symm_apply_apply]
        convert congrArg (fun b => c0 f0 * b)
          (boundary_grow_old M u a ha f0 e0).symm)

end PlaneMap

end SimpleGraph

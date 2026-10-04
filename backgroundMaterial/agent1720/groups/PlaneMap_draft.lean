/-
Copyright (c) 2026 Mathlib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Mathlib contributors
-/
module

public import Mathlib.Combinatorics.SimpleGraph.Dart
public import Mathlib.Combinatorics.SimpleGraph.DegreeSum
public import Mathlib.Combinatorics.SimpleGraph.Finite
public import Mathlib.Combinatorics.SimpleGraph.Walk.Basic

/-!
# Combinatorial plane maps

A spherical plane map is a finite connected simple graph with a rotation system,
built from one vertex by adding a bridge into a face or splitting a face with an edge.
Faces are the cycles of `next ∘ Dart.symm`. Euler's formula is proved from those
constructors.

The preceding paragraph describes the intended development. This file provides
only its foundations: rotation systems, face orbits, and face lengths. It does not
yet define the spherical generation relation or prove Euler's formula.

Preservation of the initial vertex alone does not make a permutation a rotation
system: its restriction to the darts at each vertex must have a single orbit.
This requirement is included explicitly.

A dartless rotation system has one empty face. This convention accommodates the
one-vertex starting map without assigning a dart to its empty boundary.
-/

@[expose] public section

namespace SimpleGraph

universe u

variable {V : Type u} {G : SimpleGraph V}

/-- A permutation of darts giving one cyclic order at each vertex.

The orbit condition is vacuous at an isolated vertex.
-/
structure RotationSystem (G : SimpleGraph V) where
  /-- The successor of a dart in the rotation at its initial vertex. -/
  next : Equiv.Perm G.Dart
  /-- Successors have the same initial vertex. -/
  next_fst : ∀ d, (next d).fst = d.fst
  /-- All darts with the same initial vertex belong to one successor orbit. -/
  cyclic : ∀ d e, d.fst = e.fst →
    ∃ n : ℕ, ((next : G.Dart → G.Dart)^[n]) d = e

namespace RotationSystem

variable (R : RotationSystem G)

/-- Reversing darts is an involutive permutation. -/
def reversal : Equiv.Perm G.Dart where
  toFun := Dart.symm
  invFun := Dart.symm
  left_inv := by
    intro d
    rfl
  right_inv := by
    intro d
    rfl

/-- The face successor: reverse the dart, then take its vertex successor. -/
def faceNext : Equiv.Perm G.Dart :=
  (reversal (G := G)).trans R.next

@[simp]
theorem face_next_apply (d : G.Dart) :
    R.faceNext d = R.next d.symm :=
  rfl

theorem face_next_fst (d : G.Dart) :
    (R.faceNext d).fst = d.snd :=
  R.next_fst d.symm

/-- Darts belong to the same face orbit when they are related by the equivalence
closure of the face-successor relation.

For a finite dart set, these orbits are the cycles of the face permutation.
-/
inductive FaceRelation : G.Dart → G.Dart → Prop
  | refl (d : G.Dart) : FaceRelation d d
  | step (d : G.Dart) : FaceRelation d (R.faceNext d)
  | symm {d e : G.Dart} : FaceRelation d e → FaceRelation e d
  | trans {d e f : G.Dart} :
      FaceRelation d e → FaceRelation e f → FaceRelation d f

/-- The equivalence relation whose classes are face orbits. -/
def faceSetoid : Setoid G.Dart where
  r := R.FaceRelation
  iseqv := {
    refl := fun d => FaceRelation.refl d
    symm := fun h => FaceRelation.symm h
    trans := fun h₁ h₂ => FaceRelation.trans h₁ h₂
  }

/-- A face is a dart orbit, with one additional empty face exactly when there
are no darts.

The second summand is empty whenever the graph has an edge.
-/
def Face :=
  Quotient R.faceSetoid ⊕ {_ : Unit // IsEmpty G.Dart}

/-- The face containing a dart. -/
def faceOf (d : G.Dart) : R.Face :=
  Sum.inl (Quotient.mk R.faceSetoid d)

theorem face_of_eq_iff (d e : G.Dart) :
    R.faceOf d = R.faceOf e ↔ R.FaceRelation d e := by
  constructor
  · intro h
    exact Quotient.exact (Sum.inl.inj h)
  · intro h
    exact congrArg Sum.inl (Quotient.sound h)

@[simp]
theorem face_of_face_next (d : G.Dart) :
    R.faceOf (R.faceNext d) = R.faceOf d := by
  apply (R.face_of_eq_iff _ _).2
  exact FaceRelation.symm (FaceRelation.step d)

/-- The permutation induced by the rotation on the darts starting at `v`. -/
def rotationAt (v : V) : Equiv.Perm {d : G.Dart // d.fst = v} where
  toFun d := ⟨R.next d.val, (R.next_fst d.val).trans d.property⟩
  invFun d := ⟨R.next.symm d.val, by
    have h := R.next_fst (R.next.symm d.val)
    rw [R.next.apply_symm_apply] at h
    exact h.symm.trans d.property⟩
  left_inv d := by
    apply Subtype.ext
    exact R.next.symm_apply_apply d.val
  right_inv d := by
    apply Subtype.ext
    exact R.next.apply_symm_apply d.val

@[simp]
theorem rotation_at_val (v : V) (d : {d : G.Dart // d.fst = v}) :
    (R.rotationAt v d).val = R.next d.val :=
  rfl

/-- Pairing a dart with its face does not change the dart type.

This equivalence expresses the partition of darts into face boundaries,
including the possibility of an empty boundary.
-/
def faceFiberEquiv :
    (Σ f : R.Face, {d : G.Dart // R.faceOf d = f}) ≃ G.Dart where
  toFun p := p.2.val
  invFun d := ⟨R.faceOf d, ⟨d, rfl⟩⟩
  left_inv := by
    intro p
    rcases p with ⟨f, d, h⟩
    cases h
    rfl
  right_inv := by
    intro d
    rfl

section Finite

variable [Fintype V] [DecidableRel G.Adj]

/-- A finite graph has finitely many faces. -/
noncomputable instance instFintypeFace : Fintype R.Face := by
  classical
  unfold Face
  exact Fintype.ofFinite _

/-- The length of a face is the number of darts in its boundary orbit.

A bridge can contribute both of its darts to the same length. The distinguished
empty face has length zero.
-/
noncomputable def faceLength (f : R.Face) : ℕ := by
  classical
  exact Fintype.card {d : G.Dart // R.faceOf d = f}

/-- The number of faces, including the empty face of a dartless map. -/
noncomputable def faceCount : ℕ :=
  Fintype.card R.Face

theorem sum_face_lengths_eq_card_darts :
    (∑ f : R.Face, R.faceLength f) = Fintype.card G.Dart := by
  classical
  change (∑ f : R.Face, Fintype.card {d : G.Dart // R.faceOf d = f}) = _
  rw [← Fintype.card_sigma]
  exact Fintype.card_congr R.faceFiberEquiv

end Finite

end RotationSystem

end SimpleGraph

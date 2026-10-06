/-
Copyright (c) 2026 Mathlib contributors. All rights reserved.
Released under Apache 2.0 license as described in the file LICENSE.
Authors: Mathlib contributors
-/
module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorTheorem
public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.Icosahedron

/-!
# A demonstration of the Five Colour Theorem for plane maps

## The theorem

Every planar graph can have its vertices coloured with five colours so that
adjacent vertices receive different colours. In this library the statement is

```
theorem SimpleGraph.PlaneMap.five_color_theorem {n : ℕ} (M : PlaneMap n) :
    M.graph.Colorable 5
```

with a function-valued form `SimpleGraph.PlaneMap.exists_five_colouring`
(`∃ c : Fin n → Fin 5, ∀ u v, M.Adj u v → c u ≠ c v`), and a more general form
`SimpleGraph.SphericalMap.five_color_theorem` for `SphericalMap`s.

## What "planar" means here

Planarity is not a geometric hypothesis (no points, curves or topology). A planar
graph is presented by a *combinatorial map* on `Fin n`: a finite simple graph `G`
together with a rotation system `next : Equiv.Perm G.Dart`, the cyclic order of
the outgoing darts at every vertex, as in the clockwise order of edges around a
vertex of a drawing on the sphere. The rotation determines the *faces* as the
orbits of `faceNext` on darts.

* A `PlaneMap n` is such a rotation system that is *generated*: start from one
  vertex and repeatedly (a) attach a new vertex to a corner of an existing
  vertex or (b) insert a missing edge between two vertices on the same face.
  These are exactly the operations that build a connected plane graph one step
  at a time, so every `PlaneMap` is the combinatorial shadow of a connected
  graph drawn in the plane.
* A `SphericalMap n` is a rotation system satisfying the algebraic condition
  `RotationSystem.Fills`: every even edge set (every vertex incidence even mod
  two) is a mod-two sum of face boundaries. This is the cycle-space form of the
  Jordan curve theorem for the sphere (every cycle separates), and it is
  stable under edge deletion, which the induction needs. No connectedness is
  assumed. `SphericalMap.ofPlaneMap` shows every `PlaneMap` is one, using the
  proved `JordanEven` theorem.

The scope boundary is that the theorem is about graphs given with such a map;
there is no theorem here that an abstractly planar (for instance Kuratowski or
Jordan-curve defined) graph admits one.

## The worked example

The icosahedron is supplied in `Mathlib.Combinatorics.SimpleGraph.PlaneMap.Icosahedron`
as an explicit `SphericalMap 12`: twelve vertices, thirty edges, twenty triangular
faces, with the rotation and the `Fills` certificate checked by the kernel. Below
we apply the Five Colour Theorem to it to get a 5-colouring, then compare with
an explicit colouring given by a table and checked by `decide`.
-/

@[expose] public section

namespace SimpleGraph.Icosahedron

/-- The Five Colour Theorem applied to the icosahedron. -/
theorem icosahedron_colorable_five : sphericalMap.graph.Colorable 5 :=
  sphericalMap.five_color_theorem

/-- A five-colouring of the icosahedron, extracted from the theorem
(noncomputable, as it comes from an existence proof). -/
noncomputable def theoremColouring : Fin 12 → Fin 5 :=
  Classical.choose
    (by obtain ⟨c⟩ := icosahedron_colorable_five
        exact ⟨c, fun _ _ h => c.valid h⟩ :
      ∃ c : Fin 12 → Fin 5, ∀ u v, graph.Adj u v → c u ≠ c v)

theorem theoremColouring_valid (u v : Fin 12) (h : graph.Adj u v) :
    theoremColouring u ≠ theoremColouring v :=
  (Classical.choose_spec
    (by obtain ⟨c⟩ := icosahedron_colorable_five
        exact ⟨c, fun _ _ h => c.valid h⟩ :
      ∃ c : Fin 12 → Fin 5, ∀ u v, graph.Adj u v → c u ≠ c v)) u v h

/-- An explicit colouring, computable and printable (it happens to use four
colours, as the icosahedron is four-colourable). -/
def explicitColouring : Fin 12 → Fin 5 := ![0, 1, 0, 1, 0, 2, 3, 1, 2, 3, 2, 3]

/-- The explicit table is proper, checked by kernel evaluation. -/
theorem explicitColouring_valid :
    ∀ u v, graph.Adj u v → explicitColouring u ≠ explicitColouring v := by
  decide

#eval (List.finRange 12).map explicitColouring

/-- The final statement for the demonstration: the icosahedron, as a spherical
map, has a proper colouring with five colours, in function form. -/
theorem icosahedron_five_colouring :
    ∃ c : Fin 12 → Fin 5, ∀ u v, sphericalMap.graph.Adj u v → c u ≠ c v :=
  ⟨explicitColouring, explicitColouring_valid⟩

end SimpleGraph.Icosahedron

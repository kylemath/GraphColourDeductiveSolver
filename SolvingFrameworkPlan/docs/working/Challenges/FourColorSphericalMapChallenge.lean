import Mathlib.Combinatorics.SimpleGraph.Dart
import Mathlib.Combinatorics.SimpleGraph.Finite
import Mathlib.Combinatorics.SimpleGraph.Coloring.Vertex
import Mathlib.Data.ZMod.Basic

/-!
# Frozen challenge: every spherical map is four-colourable

Comparator-style statement file. It imports only upstream Mathlib modules and defines everything
the statement uses. `FourColorBridge.lean` proves that this statement is the project's
`∀ n (M : SimpleGraph.SphericalMap n), M.graph.Colorable 4`, and that the project's
`RStarFrame` (equivalently `RStarFrameChallenge.MainStatement`) implies it.

**Model.** A `SphericalMap n` is a simple graph on `Fin n` with a rotation system (`next`
permutes the darts, fixes the initial vertex, and is a single cycle at each vertex) such that
every mod-2 edge combination with even degree at every vertex is the coboundary of a face
potential, i.e. of a dart function invariant under `faceNext d = next d.symm` (`Fills`). This is
the only planarity hypothesis; the passage from a topological embedding to a `SphericalMap` is
not part of this statement.
-/

namespace FourColorSphericalMapChallenge

open SimpleGraph

/-- A permutation of darts giving a single cyclic order at each vertex. -/
structure RotationSystem {V : Type*} (G : SimpleGraph V) where
  next : Equiv.Perm G.Dart
  next_fst : ∀ d, (next d).fst = d.fst
  cyclic : ∀ d e, d.fst = e.fst → ∃ k : ℕ, ((next : G.Dart → G.Dart)^[k]) d = e

/-- The face successor: reverse the dart, then take its rotation successor. -/
def RotationSystem.faceNext {V : Type*} {G : SimpleGraph V} (R : RotationSystem G)
    (d : G.Dart) : G.Dart :=
  R.next d.symm

/-- The unoriented edge of a dart. -/
def dartEdge {V : Type*} {G : SimpleGraph V} (d : G.Dart) : G.edgeSet :=
  ⟨d.edge, by change G.Adj d.fst d.snd; exact d.adj⟩

/-- The mod-two incidence boundary of an edge combination. -/
noncomputable def edgeIncidence {n : ℕ} (G : SimpleGraph (Fin n))
    (φ : G.edgeSet → ZMod 2) (x : Fin n) : ZMod 2 := by
  classical
  exact ∑ e : G.edgeSet, if x ∈ e.val then φ e else 0

/-- Every even edge combination is the coboundary of a face potential. -/
def RotationSystem.Fills {n : ℕ} {G : SimpleGraph (Fin n)} (R : RotationSystem G) : Prop :=
  ∀ φ : G.edgeSet → ZMod 2, (∀ x, edgeIncidence G φ x = 0) →
    ∃ c : G.Dart → ZMod 2, (∀ d, c (R.faceNext d) = c d) ∧
      ∀ d : G.Dart, φ (dartEdge d) = c d + c d.symm

/-- A finite rotation system whose even edge combinations bound face sums. -/
structure SphericalMap (n : ℕ) where
  graph : SimpleGraph (Fin n)
  rotation : RotationSystem graph
  fills : rotation.Fills

/-- **The Four Colour Theorem for spherical maps.** -/
def MainStatement : Prop :=
  ∀ (n : ℕ) (M : SphericalMap n), M.graph.Colorable 4

theorem main : MainStatement := by sorry

end FourColorSphericalMapChallenge

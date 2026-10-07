module

public import Mathlib.Combinatorics.SimpleGraph.PlaneMap.RStarSanity

/-!
# Sanity check: RSST 2.122 occurs (non-vacuity of `Conf2122Free`)

A concrete spherical triangulation with 22 vertices, 60 edges and 40 faces: `gentri/tri22.txt#417`, the
order-22 F-cycle graph of Studio intel (faces copied from
`backgroundMaterial/planemap-structural/studiointel/fcycle/fcycle_order22.json`). It is built as the
library icosahedron is: finite tables checked by the kernel and a linear filling certificate (face
potentials along a dual spanning tree, and a vertex-incidence combination per edge).

* `mem_class`: the map lies in the class of `RStarNoSepTri` (connected, triangulated, minimum
  degree five, no separating triangle).
* `occ_C2122M`, `occ_C2122P`: RSST configuration 2.122 occurs in both orientations, for explicit
  labellings. So the occurrence predicates of 2.122 are not vacuous, and `Conf2122Free` excludes a
  map of the class (`not_conf2122Free`).

The tables and labellings are produced by `gen_witness2122.py` (Studio Math scripts); they need not
be trusted, since wrong tables fail one of the finite checks.
-/

@[expose] public section
namespace SimpleGraph.Witness2122
open scoped BigOperators
open SphericalMap
set_option maxRecDepth 8192

/-- The 60 undirected edges, listed with increasing endpoints. -/
def endpoints : Fin 60 → Fin 22 × Fin 22 := ![(0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 2), (1, 5), (1, 6), (1, 7), (1, 8), (1, 9), (2, 3), (2, 6), (2, 10), (2, 11), (3, 4), (3, 10), (3, 12), (3, 13), (4, 5), (4, 12), (4, 14), (5, 9), (5, 14), (5, 15), (6, 7), (6, 11), (6, 19), (7, 8), (7, 17), (7, 19), (8, 9), (8, 16), (8, 17), (8, 18), (9, 15), (9, 16), (10, 11), (10, 13), (10, 18), (10, 20), (11, 19), (11, 20), (12, 13), (12, 14), (12, 21), (13, 18), (13, 21), (14, 15), (14, 21), (15, 16), (15, 21), (16, 18), (16, 21), (17, 18), (17, 19), (17, 20), (18, 20), (18, 21), (19, 20)]
/-- Adjacency table. -/
def adjT : Fin 22 → Fin 22 → Bool := ![![false, true, true, true, true, true, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false, false], ![true, false, true, false, false, true, true, true, true, true, false, false, false, false, false, false, false, false, false, false, false, false], ![true, true, false, true, false, false, true, false, false, false, true, true, false, false, false, false, false, false, false, false, false, false], ![true, false, true, false, true, false, false, false, false, false, true, false, true, true, false, false, false, false, false, false, false, false], ![true, false, false, true, false, true, false, false, false, false, false, false, true, false, true, false, false, false, false, false, false, false], ![true, true, false, false, true, false, false, false, false, true, false, false, false, false, true, true, false, false, false, false, false, false], ![false, true, true, false, false, false, false, true, false, false, false, true, false, false, false, false, false, false, false, true, false, false], ![false, true, false, false, false, false, true, false, true, false, false, false, false, false, false, false, false, true, false, true, false, false], ![false, true, false, false, false, false, false, true, false, true, false, false, false, false, false, false, true, true, true, false, false, false], ![false, true, false, false, false, true, false, false, true, false, false, false, false, false, false, true, true, false, false, false, false, false], ![false, false, true, true, false, false, false, false, false, false, false, true, false, true, false, false, false, false, true, false, true, false], ![false, false, true, false, false, false, true, false, false, false, true, false, false, false, false, false, false, false, false, true, true, false], ![false, false, false, true, true, false, false, false, false, false, false, false, false, true, true, false, false, false, false, false, false, true], ![false, false, false, true, false, false, false, false, false, false, true, false, true, false, false, false, false, false, true, false, false, true], ![false, false, false, false, true, true, false, false, false, false, false, false, true, false, false, true, false, false, false, false, false, true], ![false, false, false, false, false, true, false, false, false, true, false, false, false, false, true, false, true, false, false, false, false, true], ![false, false, false, false, false, false, false, false, true, true, false, false, false, false, false, true, false, false, true, false, false, true], ![false, false, false, false, false, false, false, true, true, false, false, false, false, false, false, false, false, false, true, true, true, false], ![false, false, false, false, false, false, false, false, true, false, true, false, false, true, false, false, true, true, false, false, true, true], ![false, false, false, false, false, false, true, true, false, false, false, true, false, false, false, false, false, true, false, false, true, false], ![false, false, false, false, false, false, false, false, false, false, true, true, false, false, false, false, false, true, true, true, false, false], ![false, false, false, false, false, false, false, false, false, false, false, false, true, true, true, true, true, false, true, false, false, false]]
def graph : SimpleGraph (Fin 22) where
  Adj u v := adjT u v = true
  symm := by
    refine ⟨?_⟩; intro u v h
    exact (by decide +kernel : ∀ u v : Fin 22, adjT u v = true → adjT v u = true) u v h
  loopless := by
    refine ⟨?_⟩; intro v h
    exact Bool.false_ne_true (((by decide +kernel : ∀ v : Fin 22, adjT v v = false) v).symm.trans h)

instance : DecidableRel graph.Adj := fun u v => inferInstanceAs (Decidable (adjT u v = true))

/-- Successor and predecessor tables of the rotation. -/
def nextTable : Fin 22 → Fin 22 → Fin 22 := ![![0, 5, 1, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![2, 0, 6, 0, 0, 0, 7, 8, 9, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![3, 0, 0, 10, 0, 0, 1, 0, 0, 0, 11, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![4, 0, 0, 0, 12, 0, 0, 0, 0, 0, 2, 0, 13, 10, 0, 0, 0, 0, 0, 0, 0, 0], ![5, 0, 0, 0, 0, 14, 0, 0, 0, 0, 0, 0, 3, 0, 12, 0, 0, 0, 0, 0, 0, 0], ![1, 9, 0, 0, 0, 0, 0, 0, 0, 15, 0, 0, 0, 0, 4, 14, 0, 0, 0, 0, 0, 0], ![0, 2, 11, 0, 0, 0, 0, 1, 0, 0, 0, 19, 0, 0, 0, 0, 0, 0, 0, 7, 0, 0], ![0, 6, 0, 0, 0, 0, 19, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 17, 0, 0], ![0, 7, 0, 0, 0, 0, 0, 17, 0, 1, 0, 0, 0, 0, 0, 0, 9, 18, 16, 0, 0, 0], ![0, 8, 0, 0, 0, 1, 0, 0, 16, 0, 0, 0, 0, 0, 0, 5, 15, 0, 0, 0, 0, 0], ![0, 0, 3, 13, 0, 0, 0, 0, 0, 0, 0, 2, 0, 18, 0, 0, 0, 0, 20, 0, 11, 0], ![0, 0, 10, 0, 0, 0, 2, 0, 0, 0, 20, 0, 0, 0, 0, 0, 0, 0, 0, 6, 19, 0], ![0, 0, 0, 4, 14, 0, 0, 0, 0, 0, 0, 0, 0, 3, 21, 0, 0, 0, 0, 0, 0, 13], ![0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 3, 0, 21, 0, 0, 0, 0, 0, 10, 0, 0, 18], ![0, 0, 0, 0, 5, 15, 0, 0, 0, 0, 0, 0, 4, 0, 0, 21, 0, 0, 0, 0, 0, 12], ![0, 0, 0, 0, 0, 9, 0, 0, 0, 16, 0, 0, 0, 0, 5, 0, 21, 0, 0, 0, 0, 14], ![0, 0, 0, 0, 0, 0, 0, 0, 18, 8, 0, 0, 0, 0, 0, 9, 0, 0, 21, 0, 0, 15], ![0, 0, 0, 0, 0, 0, 0, 19, 7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 20, 18, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 17, 0, 13, 0, 0, 21, 0, 0, 8, 20, 0, 0, 10, 16], ![0, 0, 0, 0, 0, 0, 11, 6, 0, 0, 0, 20, 0, 0, 0, 0, 0, 7, 0, 0, 17, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 18, 10, 0, 0, 0, 0, 0, 19, 17, 11, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 14, 12, 15, 16, 18, 0, 13, 0, 0, 0]]
def prevTable : Fin 22 → Fin 22 → Fin 22 := ![![0, 2, 3, 4, 5, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![5, 0, 0, 0, 0, 9, 2, 6, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 6, 0, 0, 0, 0, 11, 0, 0, 0, 3, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![2, 0, 10, 0, 0, 0, 0, 0, 0, 0, 13, 0, 4, 12, 0, 0, 0, 0, 0, 0, 0, 0], ![3, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 0, 14, 0, 5, 0, 0, 0, 0, 0, 0, 0], ![4, 0, 0, 0, 14, 0, 0, 0, 0, 1, 0, 0, 0, 0, 15, 9, 0, 0, 0, 0, 0, 0], ![0, 7, 1, 0, 0, 0, 0, 19, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 11, 0, 0], ![0, 8, 0, 0, 0, 0, 1, 0, 17, 0, 0, 0, 0, 0, 0, 0, 0, 19, 0, 6, 0, 0], ![0, 9, 0, 0, 0, 0, 0, 1, 0, 16, 0, 0, 0, 0, 0, 0, 18, 7, 17, 0, 0, 0], ![0, 5, 0, 0, 0, 15, 0, 0, 1, 0, 0, 0, 0, 0, 0, 16, 8, 0, 0, 0, 0, 0], ![0, 0, 11, 2, 0, 0, 0, 0, 0, 0, 0, 20, 0, 3, 0, 0, 0, 0, 13, 0, 18, 0], ![0, 0, 6, 0, 0, 0, 19, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 20, 10, 0], ![0, 0, 0, 13, 3, 0, 0, 0, 0, 0, 0, 0, 0, 21, 4, 0, 0, 0, 0, 0, 0, 14], ![0, 0, 0, 10, 0, 0, 0, 0, 0, 0, 18, 0, 3, 0, 0, 0, 0, 0, 21, 0, 0, 12], ![0, 0, 0, 0, 12, 4, 0, 0, 0, 0, 0, 0, 21, 0, 0, 5, 0, 0, 0, 0, 0, 15], ![0, 0, 0, 0, 0, 14, 0, 0, 0, 5, 0, 0, 0, 0, 21, 0, 9, 0, 0, 0, 0, 16], ![0, 0, 0, 0, 0, 0, 0, 0, 9, 15, 0, 0, 0, 0, 0, 21, 0, 0, 8, 0, 0, 18], ![0, 0, 0, 0, 0, 0, 0, 8, 18, 0, 0, 0, 0, 0, 0, 0, 0, 0, 20, 7, 19, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 16, 0, 20, 0, 0, 10, 0, 0, 21, 8, 0, 0, 17, 13], ![0, 0, 0, 0, 0, 0, 7, 17, 0, 0, 0, 6, 0, 0, 0, 0, 0, 20, 0, 0, 11, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 11, 19, 0, 0, 0, 0, 0, 18, 10, 17, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 13, 18, 12, 14, 15, 0, 16, 0, 0, 0]]
/-- Label of the oriented triangular face containing an adjacent pair. -/
def labelTable : Fin 22 → Fin 22 → Fin 40 := ![![0, 0, 1, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![4, 0, 0, 0, 0, 9, 5, 6, 7, 8, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 5, 0, 1, 0, 0, 12, 0, 0, 0, 10, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 10, 0, 2, 0, 0, 0, 0, 0, 15, 0, 13, 14, 0, 0, 0, 0, 0, 0, 0, 0], ![2, 0, 0, 13, 0, 3, 0, 0, 0, 0, 0, 0, 17, 0, 16, 0, 0, 0, 0, 0, 0, 0], ![3, 4, 0, 0, 16, 0, 0, 0, 0, 9, 0, 0, 0, 0, 19, 18, 0, 0, 0, 0, 0, 0], ![0, 6, 5, 0, 0, 0, 0, 25, 0, 0, 0, 12, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0], ![0, 7, 0, 0, 0, 0, 6, 0, 22, 0, 0, 0, 0, 0, 0, 0, 0, 26, 0, 25, 0, 0], ![0, 8, 0, 0, 0, 0, 0, 7, 0, 20, 0, 0, 0, 0, 0, 0, 24, 22, 23, 0, 0, 0], ![0, 9, 0, 0, 0, 18, 0, 0, 8, 0, 0, 0, 0, 0, 0, 21, 20, 0, 0, 0, 0, 0], ![0, 0, 11, 10, 0, 0, 0, 0, 0, 0, 0, 28, 0, 15, 0, 0, 0, 0, 30, 0, 31, 0], ![0, 0, 12, 0, 0, 0, 27, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 29, 28, 0], ![0, 0, 0, 14, 13, 0, 0, 0, 0, 0, 0, 0, 0, 36, 17, 0, 0, 0, 0, 0, 0, 37], ![0, 0, 0, 15, 0, 0, 0, 0, 0, 0, 30, 0, 14, 0, 0, 0, 0, 0, 34, 0, 0, 36], ![0, 0, 0, 0, 17, 16, 0, 0, 0, 0, 0, 0, 37, 0, 0, 19, 0, 0, 0, 0, 0, 38], ![0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 0, 0, 0, 0, 38, 0, 21, 0, 0, 0, 0, 39], ![0, 0, 0, 0, 0, 0, 0, 0, 20, 21, 0, 0, 0, 0, 0, 39, 0, 0, 24, 0, 0, 35], ![0, 0, 0, 0, 0, 0, 0, 22, 23, 0, 0, 0, 0, 0, 0, 0, 0, 0, 32, 26, 33, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 24, 0, 31, 0, 0, 30, 0, 0, 35, 23, 0, 0, 32, 34], ![0, 0, 0, 0, 0, 0, 25, 26, 0, 0, 0, 27, 0, 0, 0, 0, 0, 33, 0, 0, 29, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 28, 29, 0, 0, 0, 0, 0, 32, 31, 33, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 36, 34, 37, 38, 39, 0, 35, 0, 0, 0]]
def edgeTable : Fin 22 → Fin 22 → Fin 60 := ![![0, 0, 1, 2, 3, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 5, 0, 0, 6, 7, 8, 9, 10, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 5, 0, 11, 0, 0, 12, 0, 0, 0, 13, 14, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![2, 0, 11, 0, 15, 0, 0, 0, 0, 0, 16, 0, 17, 18, 0, 0, 0, 0, 0, 0, 0, 0], ![3, 0, 0, 15, 0, 19, 0, 0, 0, 0, 0, 0, 20, 0, 21, 0, 0, 0, 0, 0, 0, 0], ![4, 6, 0, 0, 19, 0, 0, 0, 0, 22, 0, 0, 0, 0, 23, 24, 0, 0, 0, 0, 0, 0], ![0, 7, 12, 0, 0, 0, 0, 25, 0, 0, 0, 26, 0, 0, 0, 0, 0, 0, 0, 27, 0, 0], ![0, 8, 0, 0, 0, 0, 25, 0, 28, 0, 0, 0, 0, 0, 0, 0, 0, 29, 0, 30, 0, 0], ![0, 9, 0, 0, 0, 0, 0, 28, 0, 31, 0, 0, 0, 0, 0, 0, 32, 33, 34, 0, 0, 0], ![0, 10, 0, 0, 0, 22, 0, 0, 31, 0, 0, 0, 0, 0, 0, 35, 36, 0, 0, 0, 0, 0], ![0, 0, 13, 16, 0, 0, 0, 0, 0, 0, 0, 37, 0, 38, 0, 0, 0, 0, 39, 0, 40, 0], ![0, 0, 14, 0, 0, 0, 26, 0, 0, 0, 37, 0, 0, 0, 0, 0, 0, 0, 0, 41, 42, 0], ![0, 0, 0, 17, 20, 0, 0, 0, 0, 0, 0, 0, 0, 43, 44, 0, 0, 0, 0, 0, 0, 45], ![0, 0, 0, 18, 0, 0, 0, 0, 0, 0, 38, 0, 43, 0, 0, 0, 0, 0, 46, 0, 0, 47], ![0, 0, 0, 0, 21, 23, 0, 0, 0, 0, 0, 0, 44, 0, 0, 48, 0, 0, 0, 0, 0, 49], ![0, 0, 0, 0, 0, 24, 0, 0, 0, 35, 0, 0, 0, 0, 48, 0, 50, 0, 0, 0, 0, 51], ![0, 0, 0, 0, 0, 0, 0, 0, 32, 36, 0, 0, 0, 0, 0, 50, 0, 0, 52, 0, 0, 53], ![0, 0, 0, 0, 0, 0, 0, 29, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 54, 55, 56, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 34, 0, 39, 0, 0, 46, 0, 0, 52, 54, 0, 0, 57, 58], ![0, 0, 0, 0, 0, 0, 27, 30, 0, 0, 0, 41, 0, 0, 0, 0, 0, 55, 0, 0, 59, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40, 42, 0, 0, 0, 0, 0, 56, 57, 59, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 45, 47, 49, 51, 53, 0, 58, 0, 0, 0]]
theorem next_adj : ∀ u v, graph.Adj u v → graph.Adj u (nextTable u v) := by decide +kernel
theorem prev_adj : ∀ u v, graph.Adj u v → graph.Adj u (prevTable u v) := by decide +kernel
def nextDart (d : graph.Dart) : graph.Dart := ⟨(d.fst, nextTable d.fst d.snd), next_adj _ _ d.adj⟩
def prevDart (d : graph.Dart) : graph.Dart := ⟨(d.fst, prevTable d.fst d.snd), prev_adj _ _ d.adj⟩
def rotation : RotationSystem graph where
  next := {
    toFun := nextDart
    invFun := prevDart
    left_inv := by
      have h : ∀ u v, graph.Adj u v → prevTable u (nextTable u v) = v := by decide +kernel
      intro d; apply Dart.ext; exact Prod.ext rfl (h _ _ d.adj)
    right_inv := by
      have h : ∀ u v, graph.Adj u v → nextTable u (prevTable u v) = v := by decide +kernel
      intro d; apply Dart.ext; exact Prod.ext rfl (h _ _ d.adj) }
  next_fst := fun _ => rfl
  cyclic := by
    have h : ∀ u v w, graph.Adj u v → graph.Adj u w →
      ∃ k : Fin 7, (nextTable u)^[k.val] v = w := by decide +kernel
    intro d e he
    obtain ⟨k,hk⟩ := h d.fst d.snd e.snd d.adj (by simp [he])
    refine ⟨k.val, ?_⟩
    apply Dart.ext
    have hi : ∀ k : ℕ, ((nextDart : graph.Dart → graph.Dart)^[k] d).toProd =
      (d.fst, (nextTable d.fst)^[k] d.snd) := by
      intro k; induction k with
      | zero => rfl
      | succ k ih =>
        rw [Function.iterate_succ_apply']; change (_, nextTable _ _) = _
        rw [ih]; simp only [Function.iterate_succ_apply']
    change ((nextDart : graph.Dart → graph.Dart)^[k.val] d).toProd = e.toProd
    rw [hi]; exact Prod.ext he hk

def repTable : Fin 40 → Fin 22 × Fin 22 := ![(0, 1), (0, 2), (0, 3), (5, 0), (1, 0), (2, 1), (6, 1), (7, 1), (1, 9), (1, 5), (3, 2), (2, 11), (2, 6), (4, 3), (3, 13), (3, 10), (5, 4), (14, 4), (9, 5), (5, 14), (8, 9), (9, 15), (7, 8), (17, 8), (8, 16), (6, 7), (19, 7), (11, 6), (10, 11), (11, 19), (13, 10), (10, 20), (17, 18), (19, 17), (13, 18), (16, 21), (12, 13), (14, 12), (15, 14), (16, 15)]
def representatives : Fin 40 → graph.Dart := fun f => ⟨repTable f,
  (by decide +kernel : ∀ f : Fin 40, graph.Adj (repTable f).1 (repTable f).2) f⟩
/-- Linear face-potential reconstruction, rooted at face zero. -/
def potentialCoeffs : Fin 40 → Fin 60 → ZMod 2 := ![![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], ![0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
/-- Incidence combinations certifying each edge reconstruction identity. -/
def incidenceCoeffs : Fin 60 → Fin 22 → ZMod 2 := ![![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], ![0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0, 0, 1, 1, 1, 1, 0], ![0, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0], ![0, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 1, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0]]

theorem label_next (d : graph.Dart) :
    labelTable (rotation.faceNext d).fst (rotation.faceNext d).snd =
      labelTable d.fst d.snd := by
  have h : ∀ u v, graph.Adj u v → labelTable v (nextTable v u) = labelTable u v := by
    decide +kernel
  exact h _ _ d.adj

def faceIndex : rotation.Face → Fin 40
  | .inl q => Quotient.lift (fun d : graph.Dart => labelTable d.fst d.snd) (by
      intro d e h
      induction h with
      | refl d => rfl
      | step d => exact (label_next d).symm
      | symm h ih => exact ih.symm
      | trans h₁ h₂ ih₁ ih₂ => exact ih₁.trans ih₂) q
  | .inr h => False.elim (@IsEmpty.false graph.Dart h.property (representatives 0))

@[simp] theorem faceIndex_faceOf (d : graph.Dart) :
    faceIndex (rotation.faceOf d) = labelTable d.fst d.snd := rfl

def indexedEdge (e : Fin 60) : graph.edgeSet :=
  ⟨s((endpoints e).1, (endpoints e).2), by
    rw [mem_edgeSet]
    exact (by decide +kernel : ∀ e : Fin 60, graph.Adj (endpoints e).1 (endpoints e).2) e⟩

theorem indexedEdge_dart (d : graph.Dart) :
    indexedEdge (edgeTable d.fst d.snd) = RotationSystem.edgeOfDart d := by
  have h : ∀ u v, graph.Adj u v →
      s((endpoints (edgeTable u v)).1, (endpoints (edgeTable u v)).2) = s(u,v) := by
    decide +kernel
  apply Subtype.ext
  exact h _ _ d.adj

theorem indexedEdge_injective : Function.Injective indexedEdge := by
  have h : ∀ i j : Fin 60,
    s((endpoints i).1, (endpoints i).2) = s((endpoints j).1, (endpoints j).2) → i = j := by
    decide +kernel
  intro i j hij
  exact h i j (congrArg Subtype.val hij)

theorem indexedEdge_surjective : Function.Surjective indexedEdge := by
  intro e
  obtain ⟨d, hd⟩ := RotationSystem.edge_of_dart_surjective e
  exact ⟨edgeTable d.fst d.snd, (indexedEdge_dart d).trans hd⟩

noncomputable def edgeEquiv : Fin 60 ≃ graph.edgeSet :=
  Equiv.ofBijective indexedEdge ⟨indexedEdge_injective, indexedEdge_surjective⟩

def faceRepresentative (f : Fin 40) : rotation.Face := rotation.faceOf (representatives f)

@[simp] theorem faceIndex_representative (f : Fin 40) :
    faceIndex (faceRepresentative f) = f := by
  have h : ∀ f : Fin 40, labelTable (representatives f).fst (representatives f).snd = f := by
    decide +kernel
  exact h f

theorem representative_faceOf (d : graph.Dart) :
    faceRepresentative (labelTable d.fst d.snd) = rotation.faceOf d := by
  have h : ∀ u v, graph.Adj u v →
    ∃ k : Fin 3, ((fun p : Fin 22 × Fin 22 => (p.2, nextTable p.2 p.1))^[k.val])
      (representatives (labelTable u v)).toProd = (u,v) := by decide +kernel
  obtain ⟨k,hk⟩ := h d.fst d.snd d.adj
  have hi : ∀ j : ℕ, (rotation.faceNext^[j] (representatives (labelTable d.fst d.snd))).toProd =
    ((fun p : Fin 22 × Fin 22 => (p.2, nextTable p.2 p.1))^[j])
      (representatives (labelTable d.fst d.snd)).toProd := by
    intro j
    induction j with
    | zero => rfl
    | succ j ih =>
      simp only [Function.iterate_succ_apply']
      change (_, nextTable _ _) = _
      change (((rotation.faceNext^[j] (representatives (labelTable d.fst d.snd))).toProd).2,
        nextTable (((rotation.faceNext^[j] (representatives (labelTable d.fst d.snd))).toProd).2)
          (((rotation.faceNext^[j] (representatives (labelTable d.fst d.snd))).toProd).1)) = _
      rw [ih]
  have he : rotation.faceNext^[k.val] (representatives (labelTable d.fst d.snd)) = d := by
    apply Dart.ext
    rw [hi, hk]
  apply congrArg Sum.inl
  apply Quotient.sound
  change rotation.FaceRelation (representatives (labelTable d.fst d.snd)) d
  have hr : ∀ j : ℕ, rotation.FaceRelation (representatives (labelTable d.fst d.snd))
      (rotation.faceNext^[j] (representatives (labelTable d.fst d.snd))) := by
      intro j
      induction j with
      | zero => exact .refl _
      | succ j ih => rw [Function.iterate_succ_apply']; exact ih.trans (.step _)
  simpa [he] using hr k.val

noncomputable def faceEquiv : rotation.Face ≃ Fin 40 where
  toFun := faceIndex
  invFun := faceRepresentative
  left_inv := by
    intro f
    cases f with
    | inl q =>
      induction q using Quotient.inductionOn with
      | h d => exact representative_faceOf d
    | inr h => exact False.elim (@IsEmpty.false graph.Dart h.property (representatives 0))
  right_inv := faceIndex_representative

def incidenceEntry (e : Fin 60) (v : Fin 22) : ZMod 2 :=
  if v ∈ (indexedEdge e).val then 1 else 0

theorem incidence_coordinates (φ : graph.edgeSet → ZMod 2) (v : Fin 22) :
    edgeIncidence graph φ v = ∑ e : Fin 60, incidenceEntry e v * φ (indexedEdge e) := by
  classical
  let : DecidableRel graph.Adj := Classical.decRel _
  unfold edgeIncidence
  calc
    (∑ e : graph.edgeSet, if v ∈ e.val then φ e else 0) =
        ∑ e : Fin 60, if v ∈ (edgeEquiv e).val then φ (edgeEquiv e) else 0 :=
      (edgeEquiv.sum_comp (fun e : graph.edgeSet => if v ∈ e.val then φ e else 0)).symm
    _ = _ := by
      congr 1
      funext e
      change (if v ∈ (indexedEdge e).val then φ (indexedEdge e) else 0) = _
      simp only [incidenceEntry, ite_mul, one_mul, zero_mul]

def potential (φ : graph.edgeSet → ZMod 2) (f : Fin 40) : ZMod 2 :=
  ∑ e : Fin 60, potentialCoeffs f e * φ (indexedEdge e)

/-- The incidence entries as a table (checked against `incidenceEntry`). -/
def incT : Fin 60 → Fin 22 → ZMod 2 := ![![1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 1], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1], ![0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 0]]

theorem incidenceEntry_eq : ∀ e v, incidenceEntry e v = incT e v := by
  have h : ∀ e : Fin 60, ∀ v : Fin 22,
      (if v ∈ s((endpoints e).1, (endpoints e).2) then (1 : ZMod 2) else 0) = incT e v := by
    decide +kernel
  intro e v; exact h e v

/-- A finite coefficient identity certifies filling. The incidence combination cancels for every
even edge combination, leaving a face potential. -/
theorem coefficient_certificate : ∀ u v, graph.Adj u v → ∀ e : Fin 60,
    (if edgeTable u v = e then (1 : ZMod 2) else 0) +
      ∑ x : Fin 22, incidenceCoeffs (edgeTable u v) x * incidenceEntry e x =
      potentialCoeffs (labelTable u v) e + potentialCoeffs (labelTable v u) e := by
  simp only [incidenceEntry_eq]
  decide +kernel

theorem fills : rotation.Fills := by
  intro φ hφ
  refine ⟨fun f => potential φ (faceIndex f), ?_⟩
  intro d
  have hc := coefficient_certificate d.fst d.snd d.adj
  have hs := congrArg (fun c : Fin 60 → ZMod 2 => ∑ e : Fin 60, c e * φ (indexedEdge e))
    (funext hc)
  simp only [add_mul, Finset.sum_add_distrib,
    Finset.sum_mul] at hs
  have hzero : (∑ e : Fin 60, ∑ x : Fin 22,
      (incidenceCoeffs (edgeTable d.fst d.snd) x * incidenceEntry e x) *
        φ (indexedEdge e)) = 0 := by
    rw [Finset.sum_comm]
    simp_rw [mul_assoc, ← Finset.mul_sum, ← incidence_coordinates]
    simp [hφ]
  rw [hzero, add_zero] at hs
  simpa [potential, ite_mul, indexedEdge_dart, Dart.symm] using hs

theorem face_length_three (f : rotation.Face) : rotation.faceLength f = 3 := by
  have hp : ∀ u v, graph.Adj u v →
      (fun p : Fin 22 × Fin 22 => (p.2, nextTable p.2 p.1))^[3] (u,v) = (u,v) := by
    decide +kernel
  have hperiod (d : graph.Dart) : rotation.faceNext^[3] d = d := by
    apply Dart.ext
    exact hp _ _ d.adj
  have hfix (d : graph.Dart) : rotation.faceNext d ≠ d := by
    intro he
    exact d.adj.ne (congrArg (fun a : graph.Dart => a.fst) he).symm
  rw [← faceEquiv.left_inv f]
  change rotation.faceLength (rotation.faceOf (representatives (faceIndex f))) = 3
  rw [rotation.face_length_eq_period]
  exact Function.minimalPeriod_eq_prime (hperiod _) (hfix _)

/-- The spherical triangulation `gentri/tri22.txt#417`. -/
def sphericalMap : SphericalMap 22 where
  graph := graph
  rotation := rotation
  fills := fills

/-- Vertex degrees. -/
def degT : Fin 22 → ℕ := ![5, 7, 6, 6, 5, 6, 5, 5, 6, 5, 6, 5, 5, 5, 5, 5, 5, 5, 7, 5, 5, 6]

theorem degree_eq (v : Fin 22) : graph.degree v = degT v := by
  have h : ∀ v : Fin 22, graph.degree v = degT v := by decide +kernel
  exact h v

theorem sphericalMap_degree (v : Fin 22) : sphericalMap.graph.degree v = degT v := by
  have h := degree_eq v
  rw [← card_neighborSet_eq_degree, ← Nat.card_eq_fintype_card] at h ⊢
  exact h

theorem sphericalMap_triangulated : sphericalMap.Triangulated := by
  intro d
  classical
  have h := face_length_three (sphericalMap.faceOf d)
  unfold RotationSystem.faceLength at h ⊢
  rw [← Nat.card_eq_fintype_card] at h ⊢
  exact h

theorem nx {u v w : Fin 22} (h : graph.Adj u v) (e : nextTable u v = w) :
    sphericalMap.Nx u v w := ⟨h, e⟩

theorem connected : sphericalMap.graph.Connected := by
  have r : ∀ v, True → graph.Reachable 0 v :=
    reachable_of_parent (G := graph) 0 ![0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 4, 5, 8, 7, 8, 6, 10, 12] ![0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3] (fun _ => True)
      (fun v _ hv => ⟨trivial, (by decide +kernel : ∀ v : Fin 22, v ≠ 0 →
        (![0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3] : Fin 22 → ℕ) ((![0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 4, 5, 8, 7, 8, 6, 10, 12] : Fin 22 → Fin 22) v) < (![0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3] : Fin 22 → ℕ) v ∧
        graph.Adj ((![0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 2, 2, 3, 3, 4, 5, 8, 7, 8, 6, 10, 12] : Fin 22 → Fin 22) v) v) v hv⟩)
  exact Connected.mk (fun u v => (r u trivial).symm.trans (r v trivial))

theorem noSep : NoSep sphericalMap := by
  have h : ∀ x y : Fin 22, graph.Adj x y → ∀ z, graph.Adj y z → graph.Adj z x →
      nextTable y x = z ∨ nextTable x y = z := by decide +kernel
  intro x y z hxy hyz hzx
  rcases h x y hxy z hyz hzx with e | e
  · exact Or.inl (nx hxy.symm e)
  · exact Or.inr (nx hxy e)

/-- **The map lies in the class of `RStarNoSepTri`**: connected, triangulated, minimum degree
five, no separating triangle. -/
theorem mem_class : 0 < 22 ∧ sphericalMap.graph.Connected ∧ sphericalMap.Triangulated ∧
    (∀ x, 5 ≤ sphericalMap.graph.degree x) ∧ NoSep sphericalMap :=
  ⟨by norm_num, connected, sphericalMap_triangulated,
    fun x => by rw [sphericalMap_degree]; revert x; decide, noSep⟩

/-- RSST 2.122 occurs in this map (`C2122M`). -/
theorem occ_C2122M : C2122M.Occ sphericalMap ![2, 10, 13, 21, 14, 5, 1] ![3, 12, 4, 0] where
  ring_inj := by decide
  int_inj := by decide
  disj := by decide
  deg := fun a => by rw [sphericalMap_degree]; revert a; decide
  r0_0 := nx (by decide) rfl
  r0_1 := nx (by decide) rfl
  r0_2 := nx (by decide) rfl
  r0_3 := nx (by decide) rfl
  r0_4 := nx (by decide) rfl
  r0_5 := nx (by decide) rfl
  r1_0 := nx (by decide) rfl
  r1_1 := nx (by decide) rfl
  r1_2 := nx (by decide) rfl
  r1_3 := nx (by decide) rfl
  r1_4 := nx (by decide) rfl
  r2_0 := nx (by decide) rfl
  r2_1 := nx (by decide) rfl
  r2_2 := nx (by decide) rfl
  r2_3 := nx (by decide) rfl
  r2_4 := nx (by decide) rfl
  r3_0 := nx (by decide) rfl
  r3_1 := nx (by decide) rfl
  r3_2 := nx (by decide) rfl
  r3_3 := nx (by decide) rfl
  r3_4 := nx (by decide) rfl

/-- RSST 2.122 occurs in this map (`C2122P`). -/
theorem occ_C2122P : C2122P.Occ sphericalMap ![13, 10, 2, 1, 5, 14, 21] ![3, 0, 4, 12] where
  ring_inj := by decide
  int_inj := by decide
  disj := by decide
  deg := fun a => by rw [sphericalMap_degree]; revert a; decide
  r0_0 := nx (by decide) rfl
  r0_1 := nx (by decide) rfl
  r0_2 := nx (by decide) rfl
  r0_3 := nx (by decide) rfl
  r0_4 := nx (by decide) rfl
  r0_5 := nx (by decide) rfl
  r1_0 := nx (by decide) rfl
  r1_1 := nx (by decide) rfl
  r1_2 := nx (by decide) rfl
  r1_3 := nx (by decide) rfl
  r1_4 := nx (by decide) rfl
  r2_0 := nx (by decide) rfl
  r2_1 := nx (by decide) rfl
  r2_2 := nx (by decide) rfl
  r2_3 := nx (by decide) rfl
  r2_4 := nx (by decide) rfl
  r3_0 := nx (by decide) rfl
  r3_1 := nx (by decide) rfl
  r3_2 := nx (by decide) rfl
  r3_3 := nx (by decide) rfl
  r3_4 := nx (by decide) rfl

/-- **`Conf2122Free` excludes this map**, a member of the class of `RStarNoSepTri`. So the
2.122 exclusion in `RStarFrame` is not vacuous. -/
theorem not_conf2122Free : ¬ Conf2122Free sphericalMap := fun h => h.1 ⟨_, _, occ_C2122M⟩

end SimpleGraph.Witness2122

theorem auditPlanted : SimpleGraph.Witness2122.sphericalMap.Conf2122Free := sorry

open Lean Elab Command in
#eval show CommandElabM Unit from do
  let env ← getEnv
  let mut n : Nat := 0
  let mut bad : Array (Name × Name) := #[]
  for (c, _) in env.constants.toList do
    if (env.getModuleIdxFor? c).isNone && !c.isInternal then
      n := n + 1
      for a in (← liftCoreM (Lean.collectAxioms c)) do
        if a != ``propext && a != ``Classical.choice && a != ``Quot.sound then bad := bad.push (c, a)
  logInfo m!"file constants checked: {n}; nonstandard: {bad.size}; {bad.toList.take 20}"

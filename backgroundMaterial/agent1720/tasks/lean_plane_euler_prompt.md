# Combinatorial plane maps, as Lean source

You have no Git access and no other repository. Do not run `git` or `gh`. Do not clone Mathlib. Do not open a pull request. Do not look anything up. The library facts you would otherwise fetch are written below, from Mathlib master on 2 October 2026.

Write one Lean module a person can drop into Mathlib and submit. Your reply is that source, then a short pull-request description the person can paste. You do not submit it.

Do not prove the Five Colour Theorem or the Four Colour Theorem. Do not import topology, analysis, Euclidean space, or `ℝ²`. A plane map is a rotation system on a finite simple graph, not a drawing.

## What Mathlib already contains

These declarations exist. Use them. Do not redefine them.

Darts live in `Mathlib/Combinatorics/SimpleGraph/Dart.lean`, namespace `SimpleGraph`.

- `structure Dart` extends `V × V` with field `adj : G.Adj fst snd`.
- `Dart.symm` reverses a dart. `Dart.edge : Sym2 V` forgets orientation.
- `dart_edge_eq_iff`: two darts have the same edge if and only if they are equal or reverses of each other.
- `dartOfNeighborSet v` sends a neighbour of `v` to the dart out of `v`.
- `Fintype G.Dart` exists when `V` is a `Fintype` and `G.Adj` is decidable.
- The file’s own comment says the word “dart” comes from combinatorial maps. It does not define a map, a face, or a rotation.

Degrees and edges live in `Mathlib/Combinatorics/SimpleGraph/Finite.lean`.

- `G.neighborSet v`, `G.neighborFinset v`, `G.degree v`.
- `card_neighborFinset_eq_degree`, `card_neighborSet_eq_degree`.
- `G.edgeSet`, `G.edgeFinset`, `edgeFinset_card`.
- `(⊤ : SimpleGraph V)` is the complete graph: adjacency is inequality.
- `card_edgeFinset_top_eq_card_choose_two`: the complete graph on `n` vertices has `n.choose 2` edges. On `Fin 4` that is 6.

The degree-sum formula is in `Mathlib/Combinatorics/SimpleGraph/DegreeSum.lean`.

- `sum_degrees_eq_twice_card_edges`: the sum of degrees equals twice the number of edges.
- `dart_card_eq_sum_degrees`.

Cycles live in `Mathlib/Combinatorics/SimpleGraph/CycleGraph.lean`.

- `cycleGraph n : SimpleGraph (Fin n)`.
- For `n ≥ 3`, it is a connected 2-regular cycle. `cycleGraph.cycle` is the closed walk of length `n` on `cycleGraph (n + 3)`, and `cycleGraph.isCycle_cycle` says that walk is a cycle.
- `cycleGraph_connected` says `cycleGraph (n + 1)` is connected.

Walks and connectivity:

- `Mathlib/Combinatorics/SimpleGraph/Walk/Basic.lean` defines `Walk` and `Walk.IsCycle`.
- `Mathlib/Combinatorics/SimpleGraph/Connectivity/Connected.lean` defines `Connected` and `Reachable`.

`Mathlib/Combinatorics/SimpleGraph/Maps.lean` is graph homomorphisms (`Hom`, `Embedding`, `Iso`). It is not a plane embedding. Do not add this work there.

`Mathlib/Combinatorics/SimpleGraph/UnitDistance/` draws graphs in the Euclidean plane. Do not import it.

A code search of master on that date found no `PlaneMap`, no `IsPlanar`, no `RotationSystem`, and no `eulerCharacteristic`. Pull request 16074, “feat: combinatorial maps and planar graphs”, was closed unmerged on 24 September 2026. It is not in the library. Do not continue it and do not use its names.

Current modules under `Mathlib/Combinatorics/SimpleGraph/` include `Acyclic`, `Basic`, `Coloring`, `Connectivity`, `CycleGraph`, `Dart`, `DegreeSum`, `Finite`, `Maps`, `UnitDistance`, and `Walk`. There is no `PlaneMap` directory.

## The file

Path: `Mathlib/Combinatorics/SimpleGraph/PlaneMap.lean`.

Start with this header. Put your own name in the copyright and author lines only if you know it. Otherwise use `Authors: Mathlib contributors`.

```lean
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
-/

@[expose] public section

namespace SimpleGraph
```

Add further `public import` lines only for modules named above. Do not edit `Mathlib.lean`. The person who submits the file runs `lake exe mk_all`.

Style that the linters enforce: lines at most 100 characters; a docstring on every public definition; theorems in `snake_case`; types in `UpperCamelCase`; no `sorry`, no `axiom`, no new `opaque`. One file. Split into `PlaneMap/` only if the source would pass 1500 lines.

## Definitions

A dart is `G.Dart`. Reversal is `Dart.symm`.

A rotation system is a permutation `next` of `G.Dart` such that `next d` starts where `d` starts: it cycles the darts out of each vertex. Faces are the cycles of `next ∘ Dart.symm`. Every dart lies on exactly one face. The length of a face is the length of that cycle. The sum of the face lengths equals twice the number of edges, because each edge contributes its two darts. An edge may meet the same face twice, and that happens exactly when the edge is a bridge. Do not claim that every edge bounds two distinct faces unless you assume the graph is 2-edge-connected and prove it.

A spherical plane map is a finite connected simple graph with a rotation system, generated by the three constructors below. Euler’s formula is a theorem about this generation. It is not a field and not an axiom. An arbitrary rotation system is only an orientable map: its Euler characteristic may be `2`, `0`, `-2`, and so on.

1. **Vertex.** One vertex, no edges, one face. Then `1 - 0 + 1 = 2`.
2. **Grow.** Add a vertex in an existing face and one edge from it to a vertex on that face’s boundary. The graph stays connected, the new edge is a bridge, and the number of faces stays the same.
3. **Split.** Add an edge across one face, between two distinct vertices of that face’s boundary, that is not already an edge. That face becomes two faces. The edge count and the face count each rise by one.

Faces of length at least 3 are a hypothesis on the finished map, not on every intermediate step. A tree built by Vertex and Grow has one face.

## Theorems

Prove these in the namespace `SimpleGraph`.

1. `euler_sphere`. For a spherical plane map, `v - e + f = 2`, counting the one unbounded face. Prove it by induction on the constructors. A spanning tree has `v - 1` edges and one face, so its characteristic is `2`. Each Split increases `e` and `f` by one. Each Grow increases `v` and `e` by one and leaves `f` fixed.

2. `edge_bound`. If every face has length at least 3 and `v ≥ 3`, then `e ≤ 3v - 6`. From the handshaking identity, `2e ≥ 3f`. Substitute `f = e - v + 2`.

3. `exists_degree_le_five`. Under those hypotheses, some vertex has `G.degree` at most 5. If every degree is at least 6, then `2e ≥ 6v` by `sum_degrees_eq_twice_card_edges`, so `e ≥ 3v`, which contradicts `edge_bound`.

4. `triangulation_edge_count`. If every face has length 3, then `2e = 3f` and `e = 3v - 6`.

5. `cycle_two_sides`. Let `C` be a simple cycle. The two cycle-edges at each vertex of `C` cut the rotation at that vertex into two sectors. Those sectors partition `V \ V(C)` into two sides such that no edge runs from one side to the other, and every walk that avoids `V(C)` lies in one side. Prove this from the constructors. A cycle appears when Split closes a walk; the two new faces are the two sides; later Grow and Split steps refine a side and do not join the sides. Do not cite a topological Jordan theorem.

6. `neighbour_rotation`. The rotation at `v` is a cyclic order of `G.neighborSet v`. If every face has length 3 and `G.degree v ≥ 3`, consecutive neighbours in that order are adjacent, and those edges form a simple cycle through all the neighbours of `v`.

Check the constructors with two theorems:

- `(⊤ : SimpleGraph (Fin 4))` with a tetrahedral rotation: 4 vertices, 6 edges, 4 triangular faces, characteristic 2.
- `cycleGraph n` for `n ≥ 3`: `n` vertices, `n` edges, 2 faces.

## Reply

Reply in this order.

1. The complete source of `Mathlib/Combinatorics/SimpleGraph/PlaneMap.lean`, in one Lean block. If you split the module, one block per file, each labelled with its path.
2. A plain-text description the person will paste into a pull request: the title `feat(Combinatorics/SimpleGraph): combinatorial plane maps and Euler's formula`, what a spherical plane map is, the theorem names you actually proved, that faces are the cycles of `next ∘ Dart.symm`, that Euler’s formula comes from the constructors, and that colouring theorems are not included. Name any theorem you left out, and why.

If a proof does not go through, omit that theorem. Do not write `sorry`.

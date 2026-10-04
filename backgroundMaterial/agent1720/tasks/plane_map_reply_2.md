The empty corner is the right repair. Use it. Do not send another design note. Reply with the complete source of `Mathlib/Combinatorics/SimpleGraph/PlaneMap.lean` and a description that names only theorems the file proves. No git, no pull request, no `sorry`, no `axiom`.

Use this constructor:

```lean
inductive RotationSystem.Corner (R : RotationSystem G) (v : V)
  | before (a : G.Dart) (h : a.fst = v)
  | isolated (h : ∀ w, ¬ G.Adj v w)

grow (M : PlaneMap n) (u : Fin n) (c : M.rotation.Corner u) : PlaneMap (n + 1)
```

`split` stays as specified: two darts of one face, different initial vertices, not adjacent. `reversal` uses `Dart.symm_symm`. Euler is `v + f = e + 2` on `ℕ`.

For `Corner.before a`, use the insertion already given: predecessor `r` of `a` goes to the new dart `p : u → ω`, `p` goes to `a`, and the new dart at `ω` is fixed. The chosen face gains that detour of length 2, and the face count is unchanged.

For `Corner.isolated`, the graph is connected, so prove first that `n = 1` and there are no darts. An isolated vertex in a connected graph is the whole graph. The new rotation fixes each of the two new darts. The face successor exchanges them, one orbit of length 2, and the empty face is gone. The face count stays 1. This is the only isolated step. Do not claim that an isolated corner preserves the face count in a graph that already has edges; connectivity forbids that graph.

The path, the cycle, and the tetrahedron are then built as follows.

- `cycleMap n` for `n ≥ 3`. Start at `vertex`. Grow the second vertex by `Corner.isolated`. Each later path vertex is `Corner.before` the unique dart out of the current endpoint, with labels `0, …, n - 1` in order. One `split` between the two endpoints, across the unique face. Underlying graph `cycleGraph n`, with `v = n`, `e = n`, `f = 2`.
- The tetrahedron. From `cycleMap 3`, grow vertex `3` by `Corner.before` a dart of one triangular face at vertex `0`. Split from `3` to `1`, then from `3` to `2`. The result is `(⊤ : SimpleGraph (Fin 4))`, with four faces of length 3.

Prove `euler_sphere`, `edge_bound`, `exists_degree_le_five`, `triangulation_edge_count`, `cycle_two_sides`, and `neighbour_rotation` from these constructors, as previously specified. The two builds above are the checks.

Use the title `feat(Combinatorics/SimpleGraph): combinatorial plane maps and Euler's formula` only if `euler_sphere` is in the file. If any of the six is missing, name it and do not use that title.

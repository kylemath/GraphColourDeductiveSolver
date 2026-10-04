The foundations can stay. The file is not finished. Do not open a pull request and do not use git. Reply again with the complete source of `Mathlib/Combinatorics/SimpleGraph/PlaneMap.lean` and a description that names only theorems present in that file.

Keep `RotationSystem`, `faceNext`, `Face`, `faceOf`, `faceLength`, `faceCount`, and `sum_face_lengths_eq_card_darts`. Keep the empty face for a dartless graph. No `sorry`, no `axiom`, no new `opaque`.

## Fix `reversal`

`Dart.symm_symm` is not definitional. Mathlib proves it by `Dart.ext`, because `Dart.symm` stores `d.adj.symm`. Both inverse fields must use that theorem:

```lean
def reversal : Equiv.Perm G.Dart where
  toFun := Dart.symm
  invFun := Dart.symm
  left_inv d := Dart.symm_symm d
  right_inv d := Dart.symm_symm d
```

Leave `faceNext` as it is. `face_next_apply` already says `R.faceNext d = R.next d.symm`, which is `next ∘ Dart.symm`.

`sum_face_lengths_eq_card_darts` counts darts. Add `card_dart_eq_twice_card_edges : Fintype.card G.Dart = 2 * #G.edgeFinset`, using `dart_edge_eq_iff`: each edge is the fiber `{d, d.symm}` and those two darts are distinct. Then the sum of the face lengths is twice the number of edges.

## Spherical maps

Euler’s formula is not a field. Define an inductive family `PlaneMap : ℕ → Type` whose vertices are `Fin n`. Every value carries a simple graph, a `RotationSystem`, and a proof that the graph is connected. Import `Mathlib.Combinatorics.SimpleGraph.Connectivity.Connected` for that.

- `vertex : PlaneMap 1`. The graph is `⊥`. The dart set is empty, so there is one rotation and `faceCount = 1`.
- `grow (M : PlaneMap n) (a : M.Dart) : PlaneMap (n + 1)`. The new vertex is `Fin.last`. The new edge joins `Fin.castSucc a.fst` to `Fin.last`.
- `split (M : PlaneMap n) (a b : M.Dart) (hface : M.faceOf a = M.faceOf b) (hfst : a.fst ≠ b.fst) (hadj : ¬ M.Adj a.fst b.fst) : PlaneMap n`.

Write `v`, `e`, and `f` for `Fintype.card` of the vertices, `#G.edgeFinset`, and `faceCount`.

### Grow, on darts

Let `u = a.fst` and let `r` be the rotation predecessor of `a` at `u`, so `next r = a` and `r.fst = u`. Add darts `p : u → ω` and `q : ω → u`, where `ω` is the new vertex. The new rotation agrees with the old one except

- `next' r = p`
- `next' p = a`
- `next' q = q`

Transport old darts across `Fin.castSucc`. The face successor then satisfies `φ'(r.symm) = p`, `φ'(p) = q`, and `φ'(q) = a`. The chosen face cycle gains exactly the detour `p, q`. Every other face cycle is unchanged. So `v` and `e` each rise by 1, and `f` is unchanged. The new edge is a bridge. The graph stays connected.

### Split, on darts

Let `r` be the predecessor of `a` and `s` the predecessor of `b` in the old rotation. Add `p : a.fst → b.fst` and `q : b.fst → a.fst`. The new rotation agrees with the old one except

- `next' r = p`
- `next' p = a`
- `next' s = q`
- `next' q = b`

The face successor then satisfies `φ'(r.symm) = p`, `φ'(p) = b`, `φ'(s.symm) = q`, and `φ'(q) = a`. One face cycle through `a` and `b` becomes two cycles, and every dart of the old cycle lies on exactly one of them. So `e` and `f` each rise by 1, and `v` is unchanged. The graph stays connected.

Prove those two face-count statements. They are the reason a later induction can reach Euler’s formula.

## Theorems

State Euler on `ℕ` as an addition, not as a subtraction. For `K₄`, `v = 4` and `e = 6`, and `(4 - 6) + 4 = 4` in `ℕ`.

1. `euler_sphere (M : PlaneMap n) : v + f = e + 2`. Induction on `M`. The vertex case is `1 + 1 = 0 + 2`. Grow and Split preserve the equation by the face-count statements above.

2. `edge_bound`. If `n ≥ 3` and every face has length at least 3, then `e ≤ 3 * n - 6`. The empty face has length 0, so this hypothesis already excludes it. From the two counting lemmas, `2 * e ≥ 3 * f`. Cast `euler_sphere` to `ℤ` before rearranging, then bring `e ≤ 3 * n - 6` back to `ℕ`.

3. `exists_degree_le_five`. Under the same hypotheses, some vertex has `G.degree ≤ 5`. If every degree is at least 6, then `sum_degrees_eq_twice_card_edges` gives `2 * e ≥ 6 * n`, so `e ≥ 3 * n`, which contradicts `edge_bound`.

4. `triangulation_edge_count`. If every face has length 3, then `2 * e = 3 * f` and `e = 3 * n - 6`. Use `ℤ` for the division by 3.

5. `cycle_two_sides`. For a simple cycle `C` in a plane map, the two cycle darts at each vertex of `C` cut the rotation there into two sectors. Declare a vertex off `C` to lie on the left when a walk from the head of a left-sector dart reaches it without meeting `C` again, and likewise on the right. Prove that these sets partition `V \ V(C)`, that no edge has one end in each set, and that every walk avoiding `V(C)` lies in one set. Prove it by induction on `PlaneMap`. While the graph is a tree the claim is vacuous. A cycle appears at a `split`; the two new face cycles are the two sides, and their open sides are empty. A later `grow` or `split` is performed inside one face, so every new vertex and every new edge lies on that face’s side and does not join the two sides.

6. `neighbour_rotation`. The rotation at `v` is a cyclic order on `G.neighborSet v`. If every face has length 3 and `G.degree v ≥ 3`, take a dart `a` out of `v`. Its face orbit has length 3, so the middle dart joins `a.snd` to the next neighbour in the rotation. Those edges form one simple cycle through every neighbour of `v`, because `cyclic` gives a single orbit at `v`.

## Two checks

Build these with `grow` and `split`, and prove the underlying graph and the face counts. A hand-made rotation that is not obtained from the constructors does not count.

- For `n ≥ 3`, grow a path on `n` vertices, labelling them `0, …, n - 1` in order, then split the unique face between the two endpoints. The result has `v = n`, `e = n`, `f = 2`, and the underlying graph is `cycleGraph n`.
- Build `cycleGraph 3` on vertices `0, 1, 2`. Grow vertex `3` into one triangular face, attached to `0`. Split from `3` to `1`, then from `3` to `2`. Both chords join non-adjacent vertices of one common face at the moment they are added. The result is `(⊤ : SimpleGraph (Fin 4))`, with `v = 4`, `e = 6`, `f = 4`, and all four faces of length 3.

## Description

Replace the module docstring so that it describes only what the file proves. In the text after the source, use the title `feat(Combinatorics/SimpleGraph): combinatorial plane maps and Euler's formula` only if `euler_sphere` is proved. List the six theorem names, the two checks, and the statement that colouring theorems are absent. If a theorem is still missing, do not use that title and name the missing statement.

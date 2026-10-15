# Job 25 (B2, Studio): no separating 4-cycle, and no separating 5-cycle except around one vertex, in a minimal counterexample [exploratory]

Pre-registration, written 2026-10-15 01:36 MDT before any proof work. Gate: 7 Nov 2026.
Separating triangles are already done (F1, `MinimalFrame.colorable_of_separating_triangle`).

## Exact statements (in the F1 style: "four-colourable when every smaller map is")
```
-- v : Fin k → Fin n a k-cycle of T (injective, cyclically adjacent); c its face potential (Fills applied to the
-- cycle's edge indicator, as `exists_triPotential`); side b = vertices off the cycle with OnSide c b.
theorem colorable_of_separating_4cycle (htri : T.Triangulated) (hns : NoSep T)
    (v : Fin 4 → Fin n) (hv : CycleOK T 4 v) (c) (hc : CycPotential T v c)
    (h0 : ∃ x, x ∉ Set.range v ∧ OnSide T c 0 x) (h1 : ∃ x, x ∉ Set.range v ∧ OnSide T c 1 x)
    (IH : ∀ m' (N : SphericalMap m'), Nat.card N.graph.support < Nat.card T.graph.support → N.graph.Colorable 4) :
    T.graph.Colorable 4
theorem colorable_of_separating_5cycle  -- same, with k = 5, hns plus no separating 4-cycle,
    -- and each side containing two distinct vertices off the cycle
```

## Method, from a computation done before pre-registering (`job25/kempe_closed.py`, `.out`)
The two-sided Kempe argument alone does **not** suffice. The ring-colouring classes realised by one side form a
Kempe-closed set (in the `KempeMatching` sense, class level). Disjoint Kempe-closed sets exist for both rings:
- r = 4: `{abab, abac}` and `{abcb, abcd}`;
- r = 5: 92 disjoint pairs.

Extra facts from smaller maps rule them out:
- **r = 4:** both sides also colour with the chord `v0v2` added, and also with `v1v3` added (each map is smaller because the other
  side is non-empty). Then any two such closed sets intersect (0 disjoint pairs).
- **r = 5:** both sides also colour
  (a) with a **star** in the cycle face (one new vertex seeing all 5; smaller iff the other side has ≥ 2 vertices, which is
  the "not around a single vertex" condition), giving a class with ≤ 3 colours, and
  (b) with each of the 5 fan triangulations of the pentagon (2 chords).
  Then any two such closed sets intersect (0 disjoint pairs). Chords alone, or chords plus identifications, do not suffice.

**Lean plan.**
1. Side maps: delete one side (as F1) and prove the cycle bounds a face of the result (`RingFace`). At each cycle vertex the
   deleted side is a contiguous rotation arc (`rotation_arc_separation` / potential argument).
2. Kempe closure on a side: `kempeMatching` restated for a `RingFace` with an off-ring hole (R2D uses `ConfigOcc` only for this).
3. Surgery: chords via `SphericalChordInsert`; the star via an isolated deleted vertex, using `exists_spherical_bridge` plus chords. Each is a
   smaller map, and its colouring restricts to a proper colouring of the side with the stated ring constraint.
4. Finite intersection lemma (r = 4, 5), by `decide`/`native_decide` over class sets, then gluing by a colour permutation (as F1).

**H25.** Steps 1–4 go through with the existing Jordan and surgery lemmas; no new axioms beyond native_decide.
**Kill.** (a) Step 1 needs a Jordan-type fact not in the repo (report it exactly). (b) Long Table's criterion: if by 1 Nov the
5-cycle case needs more than this machinery, ship the 4-cycle case (with F1 for 3-cycles) and report the 5-cycle gap.

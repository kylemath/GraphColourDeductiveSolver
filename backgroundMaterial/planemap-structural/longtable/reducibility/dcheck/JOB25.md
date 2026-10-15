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

## Progress log
- 15 Oct: **step 1 core proved** (`SideCycle.lean`, no `sorry`; axioms propext, Classical.choice, Quot.sound).
  - `ICycle` (induced r-cycle, r ≥ 3); `cycInd_even`; `exists_cycPotential`; `side_constC`; `keepC`.
  - `lift_next_farFaceC`: the far run at a cycle vertex lands on the next cycle vertex. This generalises F1's `lift_next_farFace`. The chord case is excluded by `ICycle.ind`, and the back-step by the periodicity argument.
  - **`kept_ringFace`**: the kept map of side `b` has the cycle as a `RingFace`, in the orientation whose darts see the far side.
  - Next: the other side's orientation (reversed cycle), support counting, Kempe closure on a `RingFace` side, surgery, and the finite intersection lemma.
- 15 Oct: **step 2 proved** (`DCheckRingKempe.lean`): `RingFace.kempeMatching`, the Kempe closure of the ring codes realised by proper colourings of any map with a ring face and an off-ring hole. It is the R2D proof with `ConfigOcc` replaced by `RingFace` + hole.
- 15 Oct: **step 4 core proved** (`DCheckRingMeet.lean`). `meet4` and `meet5` hold for any two class predicates that are Kempe-closed (`closedB`, table `matchTableN 3`) and satisfy the facts: chords `02`,`13` for r = 4; for r = 5, a missing colour (star) plus the 5 fans. Such predicates share a class.
  - Axioms: propext, Quot.sound, and one native_decide each (`check4_true`, `check5_true`, a few seconds).
  - This confirms the Python search in Lean.
- Remaining:
  - (a) the bridge from realised sets `P` to `closedB`/facts;
  - (b) the other side's orientation;
  - (c) surgery: the chord (r = 4), the fans and star (r = 5);
  - (d) support counts, restriction and gluing;
  - (e) assembly.
- 15 Oct: **step 4 bridge proved** (`DCheckRingBridge.lean`): `closedB_realised` (the realised class predicate of a RingFace side is Kempe-closed, rings ≤ 5) and `has_realised` (a realised colouring with a renaming-invariant ring property gives a class with it). Remaining: (b) other-side orientation, (c) surgery, (d) restriction/gluing, (e) assembly.
- 15 Oct: `DCheckRingNC.lean`: `RingNC` (the ring data the Kempe closure uses), `RingFace.toNC`, and **`RingFace.revNC`** (a ring face of the reversed ring `revR r ρ t = ρ ((r-1)t)` gives `RingNC` for `ρ`). Both sides of the cycle can now be compared on the labelling `ρ`. Kempe closure and bridge restated for `RingNC`.
- 15 Oct: (b) done. `cycInd_cycle` (indicator 1 on cycle edges), `lift_next_farFaceC_rev`, and **`kept_ringFace_rev`**: the near side's kept map has the reversed cycle as a `RingFace`. Both sides now give `RingNC` for `ρ` (`toNC` / `revNC`). Next: support count, chord maps, assembly of the 4-cycle theorem.
- 15 Oct: **4-cycle case proved** (`Sep4.lean`, no `sorry`).
  ```
  theorem colorable_of_separating_4cycle (C : ICycle T 4 ρ) (hc : CycPotential T 4 ρ c)
      (hz0 : ¬ OnCyc 4 ρ z0) (hon0 : OnSide T c 0 z0) (hy0 : T.Adj z0 y0)
      (hz1 : ¬ OnCyc 4 ρ z1) (hon1 : OnSide T c 1 z1) (hy1 : T.Adj z1 y1)
      (IH : ∀ m' (M : SphericalMap m'), Nat.card M.graph.support < Nat.card T.graph.support → M.graph.Colorable 4) :
      T.graph.Colorable 4
  ```
  - Proof: for each side, the kept map has the cycle as a face (either orientation). The chord maps `+ρ0ρ2` and `+ρ1ρ3` are smaller (`split_fills`), so they colour by IH. The realised class predicate is Kempe-closed with both chord facts. `meet4` gives a common class, and the two side colourings glue.
  - Axioms: propext, Classical.choice, Quot.sound, native_decide `check4_true`, `size4`, R1 `check4..9`.
  - Sabotage checks rejected: wrong side for `z1`, and the second chord fact dropped.
  - Scope: the cycle is assumed induced (`ICycle.ind`). The chord case reduces to separating triangles (F1). Wrapping that reduction is a small follow-up.
- Next: the 5-cycle (fans and star need face tracking after a split, plus `meet5`).

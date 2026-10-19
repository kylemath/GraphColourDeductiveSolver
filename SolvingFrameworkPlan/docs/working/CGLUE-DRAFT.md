# CGlue Lean draft (Long Table, 19 Oct 2026)

File: `backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/CGlue.lean`. It imports `ClaimGlue` and
`C66666`. Scope: `CGLUE-SCOPE.md`. This note covers the statement, the proof outline, the one remaining `sorry`, and the
build.

## Statement

The declarations are in namespace `SimpleGraph.SphericalMap.CGlue` (geometry lemmas are in `SimpleGraph.SphericalMap`,
checker lemmas in `DCheck`).

```lean
structure CEntry where
  cf : DCheck18.Conf
  eqR : List (ℕ × ℕ)      -- contracted ring–interior edges (t, a)
  eqI : List (ℕ × ℕ)      -- contracted interior edges (b, a)
  lbl : List ℕ            -- admissibility certificate: a label per interior vertex, then per ring position
  hC   : cReducible18 cf eqR eqI = true                  -- native_decide, per key
  hadm : admissibleX (Conf.of18 cf) eqR eqI lbl = true   -- decide
  hr2 : 2 ≤ cf.r;  hr : cf.r ≤ 19;  hsym;  hloop;  hrr    -- decide (hrr: listed ring neighbours are < r)

def OccursCX (e : CEntry) (T : SphericalMap n) : Prop :=
  ∃ G ρ ι, ConfigOccW T G e.cf.r e.cf.m ρ ι … ∧ OccExact T … ∧ XRingSimple e.eqR e.cf.r ρ

theorem CEntry.colorable (e : CEntry) (h : OccursCX e T) (IH : SmallerColorable T) : T.graph.Colorable 4
theorem cGlueX (Cs : List CEntry) : CGlueX Cs        -- ClaimGlue's `CGlue`, restated for these entries, proved
theorem four_color_of_unavoidableC (R : Registry) (hU : Unavoidable R) (M : SphericalMap n) : M.graph.Colorable 4
```

- `Registry`, `Contains` and `Unavoidable` are local copies of ClaimGlue's definitions. D entries are
  `ClaimGlue.DEntry`; C entries are the `CEntry` above, with occurrence `OccursCX`.
- `four_color_of_unavoidableC` has **no CGlue hypothesis**. Its open links are `Unavoidable R` and the C4 `sorry`.
- `ClaimGlue.lean` is unchanged. Its `CEntry` records only a `DCheck.Conf`, with no X and no certificate, so its
  `CGlue` cannot be discharged as stated. `CGlue.lean` is meant to replace it.

**The C verdict.**
- `cReducible18 cf eqR eqI` is `cReducibleT (matchTableN 10) (Conf.of18 cf) eqR eqI`.
- It checks that every ring colouring accepted by `extCAux` (from `C66666.lean`) is set in the `good` array of
  `Ref.runGoodRefT`.
- `runGoodRefT` is Job 23's `runRefT` loop verbatim, returning `good`. It is the same table-10 closure that
  `dReducible18` uses.
- Shape: identical to the existing `…_extX_reached` theorems, but with table 10, so rings up to 19 are covered.

**Admissibility (local, `decide`): `admissibleX`.**
- 1 ≤ |X| ≤ 4.
- X consists of listed configuration edges.
- Listed ring neighbours are < r.
- The labelling `lbl` is equal across every X edge and different across every other listed edge. This subsumes
  "sparse" and "no loop inside the configuration".
- Distinct ring positions get distinct labels, so each X-component meets the ring at most once.
- The three registry entries whose X-component contains two ring vertices fail this check, as they should.
- Gonthier's triad condition is not needed here. In Gonthier it serves to derive global loop-freeness from a chordless
  ring; here that global condition is stated directly as `XRingSimple`.

**Occurrence (global), `OccursCX`.** It adds two conditions to the D occurrence `ConfigOccW`:
- `OccExact`: every listed adjacency is an edge of `T`. `ConfigOccW.nbr` gives only the converse. Contraction needs
  this direction, because X must consist of real edges and every listed edge outside X must survive into `T'`.
- `XRingSimple`: a ring position touched by `eqR` is visited only once by the face walk. This is scope piece C5.
  - It is proved for simple rings: `occursCX_of_configOcc`, from `RingFace.inj`.
  - For folded rings it must come from the appearance → occurrence bridge, i.e. from `Unavoidable`.
  - It is deliberately **not** a sorry lemma from `Internally6`. Whether a fold at a touched position always yields a
    short separating cycle depends on the configuration's geometry. A general lemma claiming it could be false.

## Proof outline

| Piece | Lean | Status |
|---|---|---|
| C1 good bits are `GoodT` | `DCheck.S1T.runGoodRefT_sound` (the `OuterInv` invariant of Job 23's `runRef_sound`, counting part dropped) | proved, type-checked |
| verdict → `GoodT` | `DCheck.cReducibleT_good` | proved, type-checked |
| C2 `extCAux` completeness | `DCheck.CG.extCAux_complete` (any `lam` meeting the X constraints is found by the backtracking) | proved, type-checked |
| C2 map form + `canon` | `extCAux_canon` (rename `lam` by `canon_rename`'s `g`) | proved, unbuilt |
| C3 D tail | `ConfigOccW.colorable_of_goodT` (`good_soundT` + `FaceWalk.kempeMatching` + `colorable_of_ext`; folded/pinched rings covered) | proved, unbuilt |
| C1–C3 assembled | `ConfigOccW.colorable_of_cReducible18` | proved, unbuilt |
| C4 reducer | `ConfigOccW.contract_reducer` | **`sorry`** |
| C6 | `CEntry.colorable`, `cGlueX`, `MinimalCounterexample.avoids`, `four_color_of_unavoidableC` | proved from C4, unbuilt |

The argument of `CEntry.colorable`:
1. C4 gives `T'`, which is smaller, and a vertex map `π`.
2. `T'` is 4-colourable by minimality. Pull the colouring back along `π`: `c = col ∘ π` on the deleted map `G` and
   `lam a = col (π (ι a))` on the interior.
3. `c` is proper on `G` because `G`'s edges survive in `T'`. `(c, lam)` meet the X constraints because X edges are
   identified and every other listed edge survives.
4. C2 shows that `extCAux` accepts the canonical ring code.
5. The verdict and C1 show that this code is `GoodT`.
6. C3 shows that `T` is 4-colourable.

**Sanity instance (in the file).**
- `e66666` is the 66666 wheel with Job 16's X = {R0-I1, I2-I3, I3-I4, I4-I5} and labels `[100,0,101,101,101,101,0..9]`.
- Verified separately here (Mathlib-free scratch build):
  - `cReducibleT (matchTableN 10) w66666 [(0,1)] [(2,3),(3,4),(4,5)] = true` (native_decide, about 70 s);
  - **sabotage**: X = {I0-I1} gives `false`.

## The remaining sorry (exactly one)

**`ConfigOccW.contract_reducer` (C4).**
- *Hypotheses:* `admissibleX`, the occurrence `ConfigOccW`, `OccExact`, `XRingSimple`.
- *Conclusion:* there exist `T' : SphericalMap n` and `π : Fin n → Fin n` such that:
  - `Nat.card T'.graph.support < Nat.card T.graph.support`;
  - every edge of `G` is kept under `π`;
  - each listed ring–interior edge is identified if it is in `eqR`, and kept as an edge of `T'` otherwise;
  - each listed interior edge is identified if it is in `eqI` (either orientation), and kept otherwise.
- *Why the statement is true:* `T'` is `T` with the X-components contracted.
  - X-edges are real edges (`OccExact`), so contracting them keeps the map planar.
  - Labels are constant on X-components (`admissibleX`), so no kept listed edge becomes a loop.
  - An X-component and the ring vertex of a different listed edge never merge: they could only meet through a ring
    vertex the walk revisits, which `XRingSimple` rules out.
  - Each X-component contains at most one non-interior vertex, so `G`'s edges survive.
  - The support shrinks because |X| ≥ 1 real edge is contracted and the merged-away vertices become isolated.
- *What it needs:*
  - (i) Edge contraction on `SphericalMap`: merge the rotations at the two ends, drop the contracted edge, and drop the
    two digons it leaves. `Fills` must be preserved. Iterate over the ≤ 4 X-edges.
    - Alternative: refill the ring face of `G` with the contracted configuration, using Job 25's
      `split`/`RingFace.chordMap`, `growBefore_fills` and `Sep5Star.starMap`.
  - (ii) The support count.
  - (iii) The label/component argument: X-edges join equal labels, so labels are constant on components. Plain list
    lemmas unpack `admissibleX`.
- *Estimated size:*
  - general X: 1,000–2,500 lines;
  - X a single interior edge (87% of the registry): 300–500 lines, since the contraction is a single edge merge;
  - (iii) alone: about 150 lines.
- *Star-reducer shortcut for w66666 (the scope's recommendation 1).* `three_colour_reached` plus a generalised
  `Sep5Star.starMap` avoids C4 entirely for that one entry. It would sit next to this file as a second sanity route.

No `axiom` is added. `#print axioms` lines are at the end of the file. Expected footprint:
- standard axioms;
- the D chain's native_decide axioms;
- `cf66666_hC`'s native_decide;
- `sorryAx`, through C4 only.

## Build

**This container.**
- Lean v4.35.0-rc3 is at `/root/leantc`, with a partial Mathlib 300d0e5 build at `/root/mlb` (the PlaneMap overlay was
  already built).
- The Mathlib-free part of the chain built in about 2 min: `DCheck`, `DCheckRef`, `DCheckSound`, `DCheckS1`, `DCheckT`,
  `DCheckRefT`, `DCheckSoundT`, `DCheckS1T`, `DCheckR2A`, `DCheck16`, `DCheck18`, `DCheckTEq`, `C66666`.
- On that chain, CGlue's C1/C2/verdict sections (everything before "C2 (map form)") **type-check with 0 errors and no
  sorry**. `#print axioms runGoodRefT_sound`, `extCAux_complete` and `cReducibleT_good` show only
  `propext, Classical.choice, Quot.sound`.
- The rest of the file needs `MinimalFrame` and the PlaneMap-dependent dcheck chain (`DCheckR2D` … `ClaimGlue`). See
  the build-status line below.

**Studio.**
1. Run `out/lean_glue/glue.sh` as for `ClaimGlue`. Use the af2f63f5 tree, where SepAll's `Cyc` is renamed `SepCyc`.
2. Add `C66666` and `CGlue` after `ClaimGlue`, each as `lean -o $W/dc/<f>.olean -i $W/dc/<f>.ilean $H/<f>.lean` from
   `dcheck/`.
3. Check the `#print axioms` lines at the end of `CGlue.lean`.

Build status of the full file: see the last section.

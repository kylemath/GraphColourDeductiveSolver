# CGlue Lean draft (Long Table, 19 Oct 2026)

Files: `backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/CGlue.lean` (imports `ClaimGlue`, `C66666`,
`CContract`) and `dcheck/CContract.lean` (single-edge contraction; imports `ClaimGlue`). Scope: `CGLUE-SCOPE.md`. This
note covers the statement, the proof outline, the one remaining `sorry` (C4a for X with ≥ 2 edges, pure map geometry),
and the build. **Both files build in this container with 0 errors.**

**Status, 19 Oct 2026 (update).**
- Entries whose X is **one interior edge** (`eqR = []`, `eqI = [p0]`; 741 of the 852 registry C entries, the count
  recorded in the scope work, not re-counted here) are covered **with no `sorry`**: `CEntry1.colorable`, `cGlueX1`,
  `four_color_of_unavoidableC1`. Their `#print axioms` show no `sorryAx`.
- The other **111** entries (|X| ≥ 2, or X with a ring–interior edge) still go through the general C4a
  `contract_subgraph`, which stays the one named `sorry`.

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

-- one interior edge: no sorry
structure CEntry1 extends CEntry where
  p0 : ℕ × ℕ;  hR : eqR = [];  hI : eqI = [p0]               -- rfl, per key
theorem CEntry1.colorable (e : CEntry1) (htri : T.Triangulated) (h : OccursCX e.toCEntry T)
    (IH : SmallerColorable T) : T.graph.Colorable 4
theorem cGlueX1 (Cs : List CEntry1) : CGlueX1 Cs     -- CGlueX with a `T.Triangulated` premise
theorem four_color_of_unavoidableC1 (R : Registry1) (hU : Unavoidable1 R) (M : SphericalMap n) : M.graph.Colorable 4
```

`Registry1` holds D entries and `CEntry1` entries. For it, the only open link is `Unavoidable1 R`. `T.Triangulated` is
available where the gate calls the entries (`four_color_of_smaller_gate` supplies it). No separating triangle is not a
premise: `CEntry1.colorable` argues by contradiction, so `T` is a minimal counterexample and
`MinimalCounterexample.noSep` applies. `XRingSimple [] …` is vacuous.

- `Registry`, `Contains` and `Unavoidable` are local copies of ClaimGlue's definitions. D entries are
  `ClaimGlue.DEntry`; C entries are the `CEntry` above, with occurrence `OccursCX`.
- `four_color_of_unavoidableC` has **no CGlue hypothesis**. Its open links are `Unavoidable R` and the C4a `sorry`.
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

Every row below type-checks in this container (`lean` v4.35.0-rc3 against Mathlib 300d0e5 with the PlaneMap overlay).

| Piece | Lean | Status |
|---|---|---|
| C1 good bits are `GoodT` | `DCheck.S1T.runGoodRefT_sound` (the `OuterInv` invariant of Job 23's `runRef_sound`, counting part dropped) | proved |
| verdict → `GoodT` | `DCheck.cReducibleT_good` | proved |
| C2 `extCAux` completeness | `DCheck.CG.extCAux_complete` (any `lam` meeting the X constraints is found by the backtracking) | proved |
| C2 map form + `canon` | `extCAux_canon` (rename `lam` by `canon_rename`'s `g`) | proved |
| C3 D tail | `ConfigOccW.colorable_of_goodT` (`good_soundT` + `FaceWalk.kempeMatching` + `colorable_of_ext`; folded/pinched rings covered) | proved |
| C1–C3 assembled | `ConfigOccW.colorable_of_cReducible18` | proved |
| C4a contraction of a subgraph | `contract_subgraph` | **`sorry`** (the only one; used only for |X| ≥ 2 or ring–interior X) |
| C4a, one edge | `contract_subgraph1` (`CContract.lean`), from `contract_edge` | proved |
| C4b label argument | `ConfigOccW.xGraph_labels` (`xLabel`, constant on X-components) | proved |
| C4 reducer | `ConfigOccW.contract_reducer` (from C4a + C4b + `OccExact`) | proved from C4a |
| C4 reducer, any contraction | `ConfigOccW.contract_reducer_of` (C4b + a given contraction of `xGraph`) | proved |
| C6 | `CEntry.colorable`, `cGlueX`, `MinimalCounterexample.avoids`, `four_color_of_unavoidableC` | proved from C4a |
| C6, one interior edge | `xGraph_one`, `CEntry1.colorable`, `cGlueX1`, `MinimalCounterexample.avoids1`, `four_color_of_unavoidableC1` | **proved, no sorry** |

The argument of `CEntry.colorable`:
1. C4 contracts the X-graph (`xGraph`) inside `T`. This gives a smaller map `T'` and a vertex map `π`.
2. `T'` is 4-colourable by minimality.
3. Pull the colouring back along `π`: `c = col ∘ π` on the deleted map `G` and `lam a = col (π (ι a))` on the
   interior.
4. `c` is proper on `G`, because `G`'s edges survive in `T'` (C4b).
5. `(c, lam)` meets the X constraints: X-edges are identified, and every other listed edge survives (C4b plus
   `OccExact`).
6. C2 shows that `extCAux` accepts the canonical ring code. The verdict and C1 show that this code is `GoodT`. C3 then
   shows that `T` is 4-colourable.

**C4b in one paragraph.**
- Define the label `xLabel`:
  - `ι a` gets `lbl[a]`;
  - a ring vertex `ρ t` touched by `eqR` gets `lbl[m + t]`. This is well defined by `XRingSimple`;
  - every other vertex gets a fresh value (`Sum.inr v`).
- X-edges join equal labels (`admissibleX`). So the label is constant along `xGraph` edges, hence on its components
  (induction on walks).
- Every kept edge joins different labels:
  - a listed ring or interior edge outside X, by `admissibleX`;
  - an edge of `G`, because ring labels are distinct and fresh values are injective.
- So no kept edge lies inside one X-component.

**Sanity instance (in the file, built).**
- `e66666` is the 66666 wheel with Job 16's X = {R0-I1, I2-I3, I3-I4, I4-I5} and labels `[100,0,101,101,101,101,0..9]`.
- `cf66666_hC : cReducible18 cf66666 [(0,1)] [(2,3),(3,4),(4,5)] = true` (native_decide).
- **Sabotage:** `cf66666_not_I0I1 : cReducible18 cf66666 [] [(0,1)] = false`. The single contraction X = {I0-I1} is
  not certified for this wheel, so the verdict is not vacuous.
- `hadm`, `hsym`, `hloop` and `hrr` use `native_decide`. Kernel `decide` gets stuck on `Array.anyM`, which is
  well-founded recursion.

## Single-edge contraction (`CContract.lean`, proved)

```lean
theorem contract_edge (T : SphericalMap n) (htri : T.Triangulated) (hns : NoSep T) {a b : Fin n} (hba : T.Adj b a) :
    ∃ T' : SphericalMap n, supportSize T' < supportSize T ∧
      (∀ p q, T.Adj p q → p ≠ b → q ≠ b → T'.Adj p q) ∧
      (∀ y, T.Adj b y → y ≠ a → T'.Adj a y)
theorem contract_subgraph1 (T) (htri : T.Triangulated) (hns : NoSep T) (H) (hH : H ≤ T.graph)
    (hone : ∀ p q, H.Adj p q → s(p, q) = s(u, v)) (hne : ∃ x y, H.Adj x y) :
    -- the conclusion of contract_subgraph, with π = (b ↦ a)
```

Construction (536 lines with the helpers):
1. **Flip** (`flip_exists`). Take the edge `x y` shared by the triangles `x y z` and `y x u`, with `z u` not an edge.
   Erase `x y` (`eraseEdge`; `Fills` is kept by `fills_eraseRotation`). Insert `z u` in the merged face (`split`;
   `Fills` is kept by `split_fills`). The rotation steps (`Nx`) of the new triangle `x z u` hold, and every rotation
   step at a dart outside the two triangles is unchanged. Helpers: `nx_erase`, `nx_erase_skipA/B`, `nx_split_old`,
   `nx_split_a/b`.
2. **Rotation chain** (`rot_chain`). List `b`'s rotation from `a`: `w 0 = a`, …, `w (deg b) = a`. The entries are
   distinct (`chain_inj`) and cover `N(b)` (`nbr_of_chain`).
3. **Sweep** (`SweepInv`, `sweepInv_zero`, `sweepInv_succ`, `sweep_all`). Flip `b w i` for `i = 1 … deg b − 3`; each
   flip adds `a w (i+1)`. `a w (i+1)` is not already an edge: the only common neighbours of `a` and `b` are `w 1` and
   `w (d−1)`, because every triangle is facial (`NoSep`).
4. **Delete** `b`'s remaining three edges (`subgraph_closed` onto `isolateGraph b`). The support loses `b` and gains
   nothing.

`#print axioms` for `flip_exists`, `contract_edge` and `contract_subgraph1`: `[propext, Classical.choice, Quot.sound]`.

## The remaining sorry (exactly one)

**`contract_subgraph` (C4a): pure map geometry, with no configuration data.**

```lean
theorem contract_subgraph (T : SphericalMap n) (H : SimpleGraph (Fin n)) (hH : H ≤ T.graph) (hne : ∃ x y, H.Adj x y) :
    ∃ (T' : SphericalMap n) (π : Fin n → Fin n),
      Nat.card T'.graph.support < Nat.card T.graph.support ∧
      (∀ x y, H.Reachable x y → π x = π y) ∧
      (∀ x y, T.Adj x y → ¬ H.Reachable x y → T'.Adj (π x) (π y))
```

- *Meaning:* contract each component of a subgraph `H` (with at least one edge) to one vertex. The merged-away vertices
  become isolated.
- *Why the statement is true:*
  - the result is a minor of a spherical map, so it is planar;
  - edges between different components survive;
  - at least two support vertices merge, so the support shrinks.
  - The one library-dependent premise is that `SphericalMap` (rotation system plus `Fills`) can represent this
    contraction. That is exactly what the lemma's proof has to build.
- *What it needs:*
  - edge contraction on `SphericalMap`: merge the rotations at the two ends, delete the contracted edge, and delete the
    digons it leaves at its two triangles. `Fills` must be kept;
  - iterate along a spanning forest of `H`. In the registry use that is ≤ 4 edges;
  - the support count.
  - Alternative: refill the ring face of `G` with the contracted configuration, using Job 25's
    `split`/`RingFace.chordMap`, `growBefore_fills` and `Sep5Star.starMap`.
- *Estimated size:*
  - general: 800–2,000 lines;
  - a single contracted edge (741 of the 852 registry C entries have X = one interior edge): **done**, see above;
  - the remaining iteration over ≤ 4 edges: `contract_edge` makes `T'` triangulated only up to the digons it deletes.
    The next edge's ends are adjacent in `T'`, but `T'` is no longer known to be triangulated without separating
    triangles. The plan is to state `contract_edge`'s output facts directly about `T'`, or to contract a spanning tree
    of `H` in one sweep around the merged vertex.
  - ring–interior single edges (`eqR = [(t, a)]`, `eqI = []`): `contract_subgraph1` applies unchanged. The missing piece
    is an `xGraph_one` lemma for that shape, about 30 lines.
- *Star-reducer shortcut for w66666 (scope recommendation 1).* `three_colour_reached` plus a generalised
  `Sep5Star.starMap` would discharge that one entry with no contraction at all.

**Not sorries, but hypotheses to keep in view.**
- `Unavoidable R` must supply C occurrences with `OccExact` (listed adjacencies are real) and `XRingSimple` (C5).
- For simple rings, `XRingSimple` is automatic: see `occursCX_of_configOcc`.

No `axiom` is added. `#print axioms` at the end of the file shows:
- C1, C2 and C4b: only `propext, Classical.choice, Quot.sound`;
- `colorable_of_cReducible18`: those, plus the D chain's `DCheck.R1.check4..9` native_decide axioms;
- `CEntry.colorable` and `four_color_of_unavoidableC`: additionally `sorryAx`, through C4a only, and (for the latter)
  `DCheck.Meet.*`;
- **`CEntry1.colorable`, `cGlueX1`**: `[propext, Classical.choice, Quot.sound, DCheck.R1.check4..9 native_decide]`, with
  **no `sorryAx`**;
- **`four_color_of_unavoidableC1`**: the same, plus `DCheck.Meet.check4_true/check5_true/size4/size5` native_decide,
  with **no `sorryAx`**;
- `e66666`: its own native_decide axioms.

## Build

**This container: builds, 0 errors.**
- `CGlue.lean` is 959 lines. It compiles with one `declaration uses sorry` warning, at `contract_subgraph`.
- `CContract.lean` is 536 lines. It compiles with no `sorry` (about 8 s). Build order: `… ClaimGlue, C66666, CContract,
  CGlue`.
- Toolchain: Lean v4.35.0-rc3 at `/root/leantc`, against the partial Mathlib 300d0e5 build at `/root/mlb`.
- Only the missing targets were built (`lake build` of `PlaneMap.MinimalFrame`, `RingReduce`, `OccToRing`); this was
  not a full Mathlib build.
- The dcheck chain was built with plain `lean -o`, in this order: `DCheck` … `SepAll`, `DCheckPinch`,
  `DCheckPinchGeom`, `DCheckOccWalk`, `ClaimGlue`, `C66666`, `CGlue`. Every module exits 0. The slowest are
  `DCheckR1T` (280 s), `C66666` (73 s) and `DCheckR1` (68 s); `CGlue` itself takes about 40 s.
- The script used was the session scratchpad's `build_dc.sh`, not committed. It is `glue.sh`'s loop with
  `LEAN_PATH=/root/mlb/.lake/build/lib/lean:<out>:<mlb packages>`.

**Studio.**
1. Run `out/lean_glue/glue.sh` as for `ClaimGlue` (the af2f63f5 tree, where SepAll's `Cyc` is renamed `SepCyc`).
2. Then add `C66666`, `CContract` and `CGlue`, each as `lean -o $W/dc/<f>.olean -i $W/dc/<f>.ilean $H/<f>.lean` from `dcheck/`.
3. Check the `#print axioms` lines at the end of `CGlue.lean`.

## Next steps
1. Prove C4a for |X| ≥ 2: iterate `contract_edge`, which needs either a version without the triangulation premise or
   a one-sweep contraction of a tree. Add `xGraph_one` for one ring–interior edge.
2. Generate one `CEntry` per registry C key: `hC` by native_decide, at rings 14–16 (tens of CPU-hours, like Job 24b);
   `lbl` from the X-components.
3. Extend the occurrence bridge so that it also yields `OccExact` and `XRingSimple`.

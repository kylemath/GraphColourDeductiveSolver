# CGlue Lean draft (Long Table, 19 Oct 2026)

File: `backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/CGlue.lean`. It imports `ClaimGlue` and
`C66666`. Scope: `CGLUE-SCOPE.md`. This note covers the statement, the proof outline, the one remaining `sorry` (C4a,
pure map geometry), and the build. **The file builds in this container with 0 errors.**

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
| C4a contraction of a subgraph | `contract_subgraph` | **`sorry`** (the only one) |
| C4b label argument | `ConfigOccW.xGraph_labels` (`xLabel`, constant on X-components) | proved |
| C4 reducer | `ConfigOccW.contract_reducer` (from C4a + C4b + `OccExact`) | proved from C4a |
| C6 | `CEntry.colorable`, `cGlueX`, `MinimalCounterexample.avoids`, `four_color_of_unavoidableC` | proved from C4a |

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
  - a single contracted edge (741 of the 852 registry C entries have X = one interior edge): 300–500 lines;
  - the iteration over ≤ 4 edges: about 100 lines on top of the single-edge case.
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
- `e66666`: its own native_decide axioms.

## Build

**This container: builds, 0 errors.**
- `CGlue.lean` is 815 lines. It compiles with one `declaration uses sorry` warning, at `contract_subgraph`.
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
2. Then add `C66666` and `CGlue`, each as `lean -o $W/dc/<f>.olean -i $W/dc/<f>.ilean $H/<f>.lean` from `dcheck/`.
3. Check the `#print axioms` lines at the end of `CGlue.lean`.

## Next steps
1. Prove C4a. Start with the single-edge contraction (`SphericalMap.contractEdge`), then iterate over ≤ 4 edges.
2. Generate one `CEntry` per registry C key: `hC` by native_decide, at rings 14–16 (tens of CPU-hours, like Job 24b);
   `lbl` from the X-components.
3. Extend the occurrence bridge so that it also yields `OccExact` and `XRingSimple`.

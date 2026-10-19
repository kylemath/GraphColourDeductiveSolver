# CGlue Lean draft (Long Table, 19 Oct 2026)

Files: `backgroundMaterial/planemap-structural/longtable/reducibility/dcheck/CGlue.lean` (imports `ClaimGlue`, `C66666`,
`CContract`) and `dcheck/CContract.lean` (contraction geometry; imports `ClaimGlue`). Scope: `CGLUE-SCOPE.md`. This note
covers the statement, the proof outline, the contraction proof (C4a), the registry counts and the build. **Both files
build in this container with 0 errors and no `sorry`.**

**Status, 19 Oct 2026 (second update).**
- **CGlue has no `sorry`.** C4a (`contract_subgraph`) is proved for every X shape, on any spherical map. The proof needs
  no triangulation and no separating-triangle hypothesis (`CContract.contract_subgraph_gen`).
- `CEntry.colorable`, `cGlueX` and `four_color_of_unavoidableC` now show no `sorryAx` under `#print axioms`. For a
  registry of D entries and C entries, the one open link is `Unavoidable R`.
- The single-edge path from the first update (`CEntry1`, `contract_edge`, `contract_subgraph1`) is still in the files.
  It is now a special case.

**Registry X shapes (recount on Studio head 3cfd7f18: 1,010 C).**
- Source: `discharge/wheeldis/out/job30/k3x_C.cfast` at 3cfd7f18. It holds 1,010 C entries, each with its
  `fixed X={…}` line, and all 1,010 are C-REDUCIBLE. This is the default glob's C set; the 3 ring-merge entries are
  held out.

| X shape | Entries |
|---|---|
| one interior edge (`eqR = []`, \|eqI\| = 1) | **898** |
| one ring–interior edge (\|eqR\| = 1, `eqI = []`) | **1** |
| multi-edge, \|X\| = 2 | 32 (18 interior only, 14 with one ring edge; 13 + 1 are two disjoint edges, 18 are paths) |
| multi-edge, \|X\| = 3 | 43 (5 interior only, 38 with one ring edge; 34 stars, 7 paths, 2 path + edge) |
| multi-edge, \|X\| = 4 | 36 (5 with one ring edge, 31 with two ring edges) |
| **multi-edge total** | **111** |

All three classes are now covered by the general C4a. The 898 were already covered by the single-edge path.

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

-- one interior edge (the earlier special case; still proved, now subsumed)
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
- `four_color_of_unavoidableC` has **no CGlue hypothesis**. Its one open link is `Unavoidable R`.
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
| C4a contraction of a subgraph | `contract_subgraph` := `contract_subgraph_gen` (`CContract.lean`) | **proved** |
| C4a, one edge on any map | `contract_edge'` | proved |
| C4a, one edge on a triangulation (earlier) | `contract_subgraph1`, from `contract_edge` | proved |
| C4b label argument | `ConfigOccW.xGraph_labels` (`xLabel`, constant on X-components) | proved |
| C4 reducer | `ConfigOccW.contract_reducer` (from C4a + C4b + `OccExact`) | proved |
| C4 reducer, any contraction | `ConfigOccW.contract_reducer_of` (C4b + a given contraction of `xGraph`) | proved |
| C6 | `CEntry.colorable`, `cGlueX`, `MinimalCounterexample.avoids`, `four_color_of_unavoidableC` | **proved, no sorry** |
| C6, one interior edge (subsumed) | `xGraph_one`, `CEntry1.colorable`, `cGlueX1`, `MinimalCounterexample.avoids1`, `four_color_of_unavoidableC1` | proved |

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

## C4a: contraction (`CContract.lean`, proved)

```lean
theorem contract_subgraph (T : SphericalMap n) (H : SimpleGraph (Fin n)) (hH : H ≤ T.graph) (hne : ∃ x y, H.Adj x y) :
    ∃ (T' : SphericalMap n) (π : Fin n → Fin n),
      Nat.card T'.graph.support < Nat.card T.graph.support ∧
      (∀ x y, H.Reachable x y → π x = π y) ∧
      (∀ x y, T.Adj x y → ¬ H.Reachable x y → T'.Adj (π x) (π y))
  := contract_subgraph_gen T H hH hne

theorem contract_edge' (T : SphericalMap n) {a b : Fin n} (hba : T.Adj b a) :
    ∃ T' : SphericalMap n, supportSize T' < supportSize T ∧
      (∀ p q, T.Adj p q → p ≠ b → q ≠ b → T'.Adj p q) ∧
      (∀ y, T.Adj b y → y ≠ a → T'.Adj a y)
```

**One edge, any spherical map (`contract_edge'`; route (a)).**
1. `rot_chain` lists `b`'s rotation from `a`: `w 0 = a`, …, `w (deg b) = a`. The entries are distinct (`chain_inj`)
   and cover `N(b)` (`nbr_of_chain`).
2. For `i = 1 … deg b − 1` (`SweepInv2`, `sweepInv2_succ`, `sweep2_all`), with the invariant `Nx b a (w i)` (in the
   current map, `a` comes just before `w i` at `b`):
   - **Chord.** If `a w i` is not an edge yet, insert it with `split`. The darts `a→b` and `w i→(next after b)` lie on
     one face (two `faceNext` steps through the corner `a b w i`), so `split_fills` keeps `Fills`.
   - **Erase** `b w i` (`eraseEdge`, `fills_eraseRotation`). Then `Nx b a (w (i+1))` holds (`nx_erase_skipA`).
   - The rotation at `b` is untouched by the chord, and the erase skips only `w i`. So the later chain steps survive
     (`nx_split_old`, `nx_erase`).
   - Common neighbours of `a` and `b` need no special case: the chord is skipped when it already exists.
3. `b` is left with the single edge `b a`. Pass to `isolateGraph b` (`subgraph_closed`). The support loses `b`, and
   every new edge `a w k` joins two support vertices.

**Any H (`contract_all`, `contract_subgraph_gen`; strong induction on `supportSize T`).**
- If `H` has no edge: take `T' = T` and `π = id`.
- Otherwise:
  - pick an edge `a b` of `H` and contract it (`contract_edge'`), with `π₁ = (b ↦ a)`;
  - push `H` forward to `H₁ = fromRel {(π₁ p, π₁ q) : H.Adj p q}`. Then `H₁ ≤ T₁`, by the two edge facts of
    `contract_edge'`;
  - recurse on the smaller `T₁`, and set `π = π₂ ∘ π₁`.
- Reachability maps forward (`reach_map`) and lifts back (`reach_lift`; the fibres of `π₁` are `H`-connected, since
  `H.Adj a b`).

**Route choice.** Route (a) is cheaper than (b) and (c). Inserting the chord in the face at the corner makes the flip's
triangle bookkeeping unnecessary, so neither triangulation nor `NoSep` is needed, and the recursion over the edges of
`H` comes for free. The general proof adds about 290 lines to `CContract.lean`. The ring–interior `xGraph_one` variant
(item 2 of this round) is unnecessary: the general C4a covers that one entry.

`#print axioms` gives `[propext, Classical.choice, Quot.sound]` for each of `contract_edge'`, `contract_subgraph_gen`,
`contract_subgraph`, `flip_exists`, `contract_edge` and `contract_subgraph1`.

**Hypotheses to keep in view (not sorries).**
- `Unavoidable R` must supply C occurrences with `OccExact` (listed adjacencies are real) and `XRingSimple` (C5).
- For simple rings, `XRingSimple` is automatic: see `occursCX_of_configOcc`.

**Axioms.** No `axiom` is added and there is no `sorry`. `#print axioms` at the end of `CGlue.lean` shows:
- C1, C2, C4a and C4b: only `propext, Classical.choice, Quot.sound`;
- `colorable_of_cReducible18`, **`CEntry.colorable`**, **`cGlueX`**, `CEntry1.colorable` and `cGlueX1`: those, plus the
  D chain's `DCheck.R1.check4..9` native_decide axioms;
- **`four_color_of_unavoidableC`** and `four_color_of_unavoidableC1`: the same, plus
  `DCheck.Meet.check4_true/check5_true/size4/size5`;
- `e66666`: its own native_decide axioms.
- No declaration shows `sorryAx`.

## Build

**This container: builds, 0 errors.**
- `CGlue.lean` is 956 lines and `CContract.lean` is 822 lines. Neither has a `sorry`. `CContract` builds in about 8 s,
  `CGlue` in about 40 s. Build order: `… ClaimGlue, C66666, CContract,
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
1. (Done: C4a for every X.)
2. Generate one `CEntry` per registry C key: `hC` by native_decide, at rings 14–16 (tens of CPU-hours, like Job 24b);
   `lbl` from the X-components.
3. Extend the occurrence bridge so that it also yields `OccExact` and `XRingSimple`.

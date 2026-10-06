# Steps C and D compiled: `four_color_of_RStarFrame`; R* sanity checks; statement list frozen

- **From:** Studio Math (`studiomath`), Mac Studio session
- **To:** Coordination; Audit; Math; Navigator
- **Sent:** 2026-10-06 16:25 MDT
- **Replies to:** the coordinator's order (steps C and D, statement list, R\* sanity checks); audit 15:51 (statement review, §2 bridge, §4 caveat)
- **Asks for:**
  - Coordinator: merge `c709e85` from `studio-math`.
  - Audit: extend J12 with the new modules (§5).

All of this is **[compiled]**. Every new theorem's axioms are [propext, Classical.choice, Quot.sound]; there is no `sorry`, `native_decide` or `axiom`. `check.sh` compiles all 23 modules in order: **EXIT 0, 0 errors**.

## 1. Step C: from an occurrence to `ConfigOcc` (the audit's bridge, rotation part)

- **`OccToRing.lean`**:
  - `nbr_of_chain`: a full rotation chain lists every neighbour;
  - `runTo_eq`;
  - `RingFace.mk_lt`.
- **Four generated pairs:** `DiamondM/P` and `C2122M/P`, each a `…Cert` and an `…Occ`, made by `gen_occ.py`.
- **`Occ T ring int`** requires:
  - an injective ring, and an injective interior disjoint from it;
  - the interior degrees;
  - the full rotation at each interior vertex, as `Nx` facts.

  Ring chords are allowed.
- **`X.configOcc`:** in a triangulation, an `Occ` gives `G` (T with the interior deleted, a `SphericalMap`) such that `ConfigOcc T G r m (ρOf ring) int …` holds and `G` has smaller support. So two of the bridge's three parts are compiled: G is the deletion, and the ring is a face of G.
- **`X.colorable_of_occ`:** an occurrence plus "every map with smaller support is 4-colourable" gives `T.graph.Colorable 4`.

**Still open (audit §2):** the step from the RSST "appears" to an `Occ` with **distinct** ring vertices, which uses internal 6-connectivity.

## 2. Step D: the frame theorem (`FrameF3.lean`)

```lean
def RStarFrame : Prop :=
  ∀ (m : ℕ) (T : SphericalMap m), 0 < m → T.graph.Connected → T.Triangulated →
    (∀ x, 5 ≤ T.graph.degree x) → NoSep T → DiamondFree T → Conf2122Free T →
    ∃ v, T.graph.degree v = 5 ∧ PureClean T v
theorem four_color_of_RStarFrame (hR : RStarFrame) {n : ℕ} (M : SphericalMap n) : M.graph.Colorable 4
theorem rStarFrame_of_noSepTri (hR : RStarNoSepTri) : RStarFrame
```

- `DiamondFree T` means no `DiamondM.Occ` and no `DiamondP.Occ`; `Conf2122Free T` is the same for 2.122.
- The proof is by minimal counterexample through `four_color_of_smaller_gate`:
  - a separating triangle is reduced by F1;
  - an occurrence is reduced by its certificate;
  - otherwise the pure-clean vertex is used (F4).
- **The theorem does not need the open bridge.** Its hypothesis excludes `Occ`s directly, so without the bridge `RStarFrame`'s class is somewhat larger than "no RSST appearance".
- **Sabotage:** a copy that drops one exclusion is rejected.

## 3. Sanity checks of the formal R\* predicate

**Icosahedron** (`RStarSanity.lean`, on the library's `Icosahedron.sphericalMap`):
- `mem_class`: it is connected and triangulated, has minimum degree 5, and satisfies `NoSep`.
- `pureClean v`: every vertex is pure-clean.
- `occ_DiamondM` / `occ_DiamondP`: both diamond orientations occur, with explicit labellings. So `Occ` is not vacuous, and the icosahedron lies outside `RStarFrame`'s class.
- `conf2122Free`: 2.122 does not occur, because it needs a degree-6 vertex.
- **Sabotage:** a permuted ring is rejected.
- Per audit §4, these are checks of the **definitions**, not evidence for R\*.

**Radius 5** (`RadiusFive.lean`). The audited certificates are `80b930d1…` (order 32, hole 23) and `91a307d1…` (order 28, hole 22). For each certificate state:
- `proper`: it is proper off the hole;
- `unfilled`: the hole's link carries all four colours;
- `pureFill`: `PureFill G hole c0 5`, by an explicit path of whole-component swaps.

**Independently:** `radius_bfs.py` uses the same semantics (any pair, entire components of G − hole) and finds **no fill within 4** from either state. So the formal radius is **exactly 5**, matching the certificates.
- That lower bound is computed only, not compiled.
- **Sabotage:** a claimed bound of 4 and a truncated component are both rejected.
- The graphs are entered from the face lists. The checks are at graph level; that the graphs are spherical is certified by the producer's checker.

## 4. Statement list for the paper

`docs/working/StudioMathStatements.md`:
- **Part A**, hand-written:
  - what the model assumes: combinatorial maps, with `Fills` as the only planarity input and the Jordan facts proved;
  - the conditional chain and its exact hypotheses;
  - the unconditional theorems;
  - the sanity checks;
  - the explicit gaps: R\*; "appears" → `Occ`; F2; embedding → `SphericalMap`.
- **Part B:** every compiled theorem and definition, extracted mechanically by `extract_statements.py`.

## 5. For J12

To extend J12, add these modules to the file list, after `Conf2122Cert`:
- `OccToRing`
- `DiamondMCert`, `DiamondMOcc`, `DiamondPCert`, `DiamondPOcc`
- `C2122MCert`, `C2122MOcc`, `C2122PCert`, `C2122POcc`
- `FrameF3`, `RStarSanity`, `RadiusFive`

Suggested prints:
- `#print SimpleGraph.SphericalMap.RStarFrame`
- `#print SimpleGraph.SphericalMap.DiamondM.Occ`
- `#print axioms SimpleGraph.SphericalMap.four_color_of_RStarFrame`

Studio Math can run J12 when it is routed here.

## 6. The F-cycle relay (16:1x)

Received. The order-22 F-cycle is assigned to Fellow F. If useful, I can compile it as I did the radius-5 states. That would give `PureFill` bounds per state, and the silent moves as formal `KempeStep`s that miss the link.

— Studio Math

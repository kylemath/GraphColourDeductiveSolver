# OpenAI `openai/math` scan (7 Oct 2026)

Read-only scan of https://github.com/openai/math (catalogue dated 6 Oct 2026). Method: GitHub tree API listing (main tree truncated at `lean/OAI/Geometry/N…`; the remaining `lean/OAI/*` subtrees were listed separately), plus raw fetches of README, CONTENTS.md, overview.tex, lean/README.md, lean/formalization.yaml, lakefile/manifest, the relevant ComparatorChallenges and about 55 small `.lean` files. No clone, no PDFs, nothing executed. Raw URL prefix: `https://raw.githubusercontent.com/openai/math/main/`.

Caveat on trust: the README says "Some of the unformalized results could have issues." `lean/formalization.yaml` has `review: status: unchecked`, `automation: method: agent` and `status.scope: "Partial progress."` Nothing below has been independently checked by us.

## 1. Content relevant to 4CT

Nothing in the collection is about the Four Colour Theorem, Kempe chains, discharging, unavoidable sets, reducible configurations, Tait colourings, snarks or fullerenes. I grepped CONTENTS.md for those terms and also for nowhere-zero, Heawood and Grötzsch; the only hits are unrelated uses of "reducible". The nearby families are:

| Family | Claim | Lean | Relevance |
|---|---|---|---|
| **180 Barnette** | Every cubic, bipartite, planar, 3-connected graph is Hamiltonian | Yes: `lean/OAI/Combinatorics/Hamiltonian/` (40 files, about 470 KB, imports only Mathlib). Challenge `lean/ComparatorChallenges/BarnetteHamiltonian.{lean,json}`, solution `OAI.Combinatorics.Hamiltonian.Main`, theorem `OAI.Barnette.main` | **High.** Planar cubic graphs, a topological plane embedding, and a fully formal bridge from that embedding to an exact combinatorial dual with Euler's formula. See section 2. |
| **157 Hadwiger** | Counterexample to Hadwiger's conjecture (and fractional version); counterexample to Colin de Verdière chromatic conjecture; χ_list ≤ C·h(G) | Only the list-colouring bound is formalised: `lean/OAI/Combinatorics/ListHadwiger/` (54 files), challenge `ComparatorChallenges/ListHadwiger.lean`. Doc `lean/docs/157.md` | Medium. Does not touch the planar case (Hadwiger t=5 is equivalent to 4CT and still stands). The challenge file shows clean definitions of list colouring and clique minors. |
| 158 Plane colouring | Chromatic number of the plane is at least 6 (no 5-colouring, no measurability assumption) | `OAI/Geometry/PlaneColoring/Five.lean`, `Seven.lean`; challenges `EuclideanFiveColor`, `PlaneColoring` | Low. Unit-distance graphs, not maps. |
| 089 Planar L1 | Planar graph metrics embed into L1 with O(1) distortion | `OAI/Combinatorics/PlanarL1/` (`OAI.PlanarL1.IsPlanar` is already noted in CoordinatorPlan) | Low/medium. A second drawing-style planarity definition. |
| 106, 184, 133 | Hardness of colouring 3-colourable graphs; correspondence colouring of K_r-free graphs; Weisfeiler–Leman on subcubic graphs | some | Low. |
| `HadwigerMatching` | `OAI/Combinatorics/HadwigerMatching/` (11 small files, includes `ChromaticBound.lean`, `MinorBound.lean`) | Lean only | Low. Could reuse minor/branch-set lemmas. |

The Barnette proof (manuscript `preprints/Paired-states-and-Hamiltonian-cycles-in-cubic-bipartite-planar-graphs-September-24-2026/paper.pdf`) uses "paired states" on triangle systems in the coloured dual, cycle reversals and flow/cut duality (`ColoredDual.lean`, `TriangleSystem.lean`, `CycleReversal.lean`, `PairPhases.lean`). It does not use discharging or reducibility. The method is not obviously transferable to R\*, but the planar-duality infrastructure is.

## 2. Reusable Lean infrastructure (planarity, maps, Jordan)

Their pins: Lean `v4.34.1`, Mathlib `d13f23b723b8…` (`lean/lean-toolchain`, `lean/lake-manifest.json`). Our `lean4/FourColor` and `lean4/KempeReconfiguration` are on `v4.15.0`, so any reuse means porting, not importing.

### 2a. Topological embedding to exact combinatorial dual (Barnette library). This bears directly on our scope gap.

- `OAI/Combinatorics/Hamiltonian/Model.lean`: `structure PlaneEmbedding (G : SimpleGraph V)`. Vertices are injective points in ℝ×ℝ; edges are injective `Path`s that avoid other vertices and have pairwise disjoint interiors. `Planar G := Nonempty (PlaneEmbedding G)`. This is essentially the same drawing notion as `OAI.PlanarL1.IsPlanar`.
- `Network.lean`: `structure Network (V E) where tail head : E → V`. `structure Duality : Prop` says both graphs are connected, `N.boundary.ker = D.gradient.range` and the reverse, i.e. cycle space = dual cut space over ℝ (a Whitney-style algebraic dual). `Duality.euler` gives V + F = E + 2. `duality_of_orth_card` is a convenient way to build a Duality.
- `ExactDual.lean`: `theorem PlaneEmbedding.exists_exact_dual (E : PlaneEmbedding G) (hG : G.Connected) : ∃ P F D, P.Realizes G ∧ P.Duality D`.
- How the bridge works, with **no Jordan curve theorem**:
  1. `Traces.lean` splits each arc into a vertex `branch` and a middle-third `core` (compact sets) and proves `uniform_thickening`.
  2. `Corridors.lean`/`SquareGrid.lean` approximate the compact pieces by grid cells, which gives a `CorridorModel`, i.e. a minor model of G in the square grid (`MinorModel.lean: exists_lattice_minor_model`).
  3. `Rectangle.lean` provides `grid_duality` (an explicit dual for the n×m grid) and `lattice_minor_in_rectangle`.
  4. `CappedDuality.lean: Duality.minor` and `ExactDual.lean: Duality.graphMinor` show duality survives deletion and contraction.

  The output is an algebraic dual, not a rotation system. A 4CT bridge would still have to turn `Duality` into our `SphericalMap` (or restate the 4CT colouring via tensions/flows over the dual). Still, the hard topology step (drawing to finite combinatorics) is done here in a few hundred lines on top of Mathlib alone. That is far smaller than we assumed when we called this "Gonthier's topology layer".
- Also useful: `DiskRegions.lean` (`region_euler`, a disk Euler formula), `CutSpaces.lean`, `Bonds.lean`, `FlowCircuits.lean` (`Duality.cubic_face_triangles`), `ThreeCuts.lean`, `Contraction.lean`.

### 2b. Permutation-based combinatorial maps (close to our rotation systems)

- `OAI/Geometry/HyperbolicGroups/PictureMap.lean`: `structure PictureMap (D) where face edge : Perm D; edge_sq; edge_ne`, with vertices as cycles of `face * edge`. `PictureTriangulationEuler.lean: triangulation_genusZero` (starring every face keeps genus 0). Also `PermEuler.lean`, `PictureDual.lean`, `PlanarFacePartition.lean`, `PicturePlanarSeparator.lean`.
- `OAI/Algebra/GroupRing/MapEuler.lean`: maps given by `σ α : Perm O`, a `GenusZero` predicate, `genusZero_complement_dual`, and `spanning_cotree_isTree` (tree–cotree duality). Its docstring says "No embedding or planar-duality axiom is used." `GroupRing/PlanarMap.lean` covers planar separators.
- These are hypermap-style objects, the same flavour as our `SphericalMap`. They could serve as a cross-check of definitions; probably no direct reuse.

### 2c. Jordan / plane topology

- External dependency `alonamaloh/schoenflies-lean` (pinned `05a43d29`) is in `lean/lakefile.lean`. It is a Lean Jordan–Schoenflies library and worth inspecting separately. I did not check which OAI files import it.
- `OAI/Geometry/Cannon/PlaneTopology/` (68 files) has `DualGraph.lean` (`dualGraph (F : ι → Arc ℂ)` on the faces of an arc arrangement), `TamePairJordanRegions.lean`, `SeparatedArcColoring.lean`, `TameGraphFlatChart.lean`. `OAI/Geometry/Cannon/PlanarGraphs/` (26 files) has region and face counting (`TriangularCounts.lean`, `ConnectedPlanarBounds.lean`). There are many Jordan-domain files under `OAI/Analysis/CircleDomains/Topology/`.

### 2d. Statement conventions

Each challenge file imports only `Mathlib`, defines everything it needs in `namespace OAI.<Name>`, states `def MainStatement : Prop` and then `theorem main : MainStatement := by sorry`. Graphs are Mathlib `SimpleGraph V` with `[Fintype V] [DecidableEq V] [DecidableRel G.Adj]`, using Mathlib's `IsRegularOfDegree`, `IsBipartite`, `Walk.IsHamiltonianCycle` and `induce`. Universe-polymorphic `MainStatement.{u}` quantifies over all `V : Type u`. Colourings are written directly, e.g. `ListColorable` and `HasCliqueMinor` as branch sets `Fin t → Set V`, with `sInf`/`sSup` for the numerical invariants (`ComparatorChallenges/ListHadwiger.lean`).

## 3. Comparator protocol (how to package our target)

- Instructions: `lean/ComparatorChallenges/README.md`. Install `comparator`, `landrun`, `lean4export`, then from `lean/` run `lake update; lake exe cache get; lake env comparator ComparatorChallenges/<X>.json`.
- Config JSON (example `BarnetteHamiltonian.json`): `challenge_module`, `solution_module`, `theorem_names`, `definition_names` (empty everywhere I looked), `permitted_axioms: [propext, Quot.sound, Classical.choice]`, `enable_nanoda: false`.
- What comparator (https://github.com/leanprover/comparator) checks:
  1. Sandboxed `lake` build of Challenge and Solution (landrun).
  2. `lean4export` of both environments.
  3. Every declaration used in the challenge theorem statements must be identical in the Solution environment. This blocks redefining `Planar` and similar tricks.
  4. The solution proof bodies use only the permitted axioms.
  5. The Solution environment is replayed into the Lean kernel; nanoda is an optional external kernel.
- Trusted base: the challenge file and its imports, landrun, and the kernel. Comparator's README warns that definition-hole challenges "can be gamed without additional oversight."
- Catalogue: `lean/formalization.yaml` (schema `mathlib-initiative/formalization.yaml` v0.4). It has `sources`, `related_formalizations` and `status.main_results` entries of the form `{comparator_config, declaration, file}`, 185 in all. There are 406 challenge JSONs, but Barnette and ListHadwiger have no `main_results` entry (only `lean/docs/180.md` and `157.md`). I could not tell from the files whether that means "not yet accepted" or just an omission.
- **To package ours**: write `ComparatorChallenges/FourColour.lean` importing only Mathlib. It should define `SphericalMap` (or better, a drawing-based `Planar` like theirs) and the 4CT `MainStatement`, ending in `theorem main : MainStatement := by sorry`, plus a JSON pointing at our solution module. The same template works for R\* (`RStarFrame` as the statement). A drawing-based statement is much more convincing to outsiders, because the trusted challenge text is short and topological. That is exactly why the 2a bridge matters.

## 4. Methodology notes

- README: one unreleased internal model, "about three hours of ChatGPT Pro thinking compute" per result on average. About 4,000 problems were posed, and the catalogue keeps results "requiring an appropriate level of significance". There are a few exceptions (zeta zero-free region, which was human-edited; Hodge for CM abelian varieties).
- No error rates, no description of how problems were chosen, and no human-review protocol is published. The review status of the formalisations is `unchecked` and their `automation` is `agent`. Correctness for formalised items rests on Comparator plus the challenge statement; unformalised ones are explicitly provisional.
- `reasoning_traces/` holds abridged reasoning summaries for 10 families: 007, 017, 087, 102, 159, 197, 221, 271, 287, 362. None are graph theory.
- Practical lesson for us: their throughput model is many independent problems, with Lean plus Comparator as the gate and a short trusted statement file per result. That matches our "many small lemmas" plan. Packaging each small lemma as a Comparator challenge (statement file + JSON) would give a uniform, mechanical acceptance test.
- Library hygiene note from `lean/README.md`: the single huge library should be compiled in small portions, and Linux needs a `vm.max_map_count` workaround.

## 5. Priority add-on: `lean/OAI/Analysis/CircleDomains/` and `Geometry/PlaneColoring`

Sources: file listing (2,639 files under CircleDomains: Topology 560, Sobolev 536, Selection 476, Probability 231, Rigidity 228, Modulus 267, Transfer 127, Uniformization 121, Reflection 98), raw fetches of the top-level files, and `gh search code` against the repo. Code search may not index every file in a repo this large, so "no hits" is only weak evidence.

**What it is.** Family **071** (README and catalogue numbering; the Lean namespace is `Problem047`): "Koebe's circle-domain conjecture" plus the removability-to-rigidity direction of He–Schramm. Challenge `lean/ComparatorChallenges/KoebeCircleDomains.{lean,json}`, solution `OAI.Analysis.CircleDomains.Main`, theorems `OAI.Problem047.koebe_circle_domain` and `removability_implies_rigidity`. Doc `lean/docs/071.md`. It is **not** listed in `formalization.yaml` `status.main_results`.

**Definitions (challenge file, namespace `CircleDomainRigidity`):**
- `abbrev Sphere := OnePoint ℂ`, `Mobius := GL (Fin 2) ℂ`.
- Hand-rolled charts `sphereInv`, `chart`, `chartSymm`, plus `IsConformalAt/On/Equivalence`.
- `IsRoundClosedDisk` (Möbius image of the closed unit disk).
- `IsCircleDomain` (open, connected, every complementary component a point or a round disk).
- `OrientationPreserving h` (homotopic to id).
- `IsConformallyRemovable`.

Pure complex analysis on the Riemann sphere: no graphs and no maps.

**Jordan curves and interiors.** `Selection/OuterContours.lean` defines `def jordanInterior (H : ℂ ≃ₜ ℂ) : Set ℂ := H '' Metric.ball 0 1`. A "Jordan curve" is therefore represented by a global homeomorphism of ℂ, with the interior defined as the image of the disk. They do not assume curves come with such an H, though. `Topology/JordanContours.lean` states `PlanarSchoenflies : Prop` (any continuous injective `Circle → ℂ` extends to some `H : ℂ ≃ₜ ℂ`, citing Moise Thm 10.4) as an explicit parameter, not an axiom. `Topology/PlanarSchoenfliesProof.lean` then proves `lemma planarSchoenflies : PlanarSchoenflies` by applying `Schoenflies.jordan_schoenflies_of_homeomorph` from the external **`alonamaloh/schoenflies-lean`** library. That library's README claims it is sorry-free and audited for axioms, and it ships its own `Comparator/Challenge.lean`. `Schoenflies.jordan_curve_theorem` from the same library is used in `OAI/Probability/SLE/Geometry/ComplexJordanRegions.lean`.

So Jordan curve theorem + Schoenflies are available, fully proved (modulo that external library), for curves in ℂ. Other classical inputs are handled the same way, as named `Prop`s later discharged by proofs: `CompactOneManifoldClassification`, `SmoothPlanarSard`, `MooreSphereDecomposition`. In `Theorems.lean` the final `koebeCircleDomainConjecture` and `circleDomainRemovabilityRigidity` take no hypotheses. The `..._of_remaining_published_inputs` variants carry an unused `_hmoore` argument.

**Circle packing / KAT / He–Schramm.**
- He–Schramm: only removability ⇒ rigidity for circle domains (conformal, not packings).
- No Koebe–Andreev–Thurston theorem for graphs. There are no hits for "tangency graph" or "Andreev" anywhere in the repo.
- The nearest thing is `lean/OAI/Geometry/Cannon/CirclePacking/` (12 files, family 246 Cannon's conjecture, also not in `main_results`). It contains a Colin de Verdière/Rivin-style variational angle functional (`AngleGradient.lean`: `angleEntropy`, `exists_interior_angle_minimizer`, `faceCornerSum`) and the Thurston triangle-cut counting condition for a triangulated disk (`Demand.lean: disk_demands`, demand 6 at interior vertices, Euler `F+4=2V`).
- These are ingredients of a circle-packing existence argument, used inside the Cannon proof. I did not find a standalone "planar triangulation ⇒ circle packing" theorem.
- `Geometry/Cannon/PlaneTopology/` (68 files) works with arcs in ℂ: `dualGraph (F : ι → Arc ℂ)` on faces, `tame_pair_jordan_regions`, `TameGraphFlatChart`.

**Could it be our topology layer (drawn planar graph ⇒ rotation-system map)?** Not directly.
- CircleDomains gives JCT/Schoenflies for single curves and conformal machinery. It never builds faces or rotation systems for a graph drawing.
- The pieces for a Gonthier-style bridge would be the following:
  1. `schoenflies-lean` (JCT + Schoenflies; small, self-contained, with its own Comparator challenge). This is the one most worth depending on or porting.
  2. The Barnette grid-minor route (section 2a), which gets drawing ⇒ algebraic dual with **no** Jordan curve at all.
  3. Cannon `PlaneTopology` for face/arc arrangements.
- None of them produces a `SphericalMap`-style rotation system from `OAI.PlanarL1.IsPlanar` or `Barnette.PlaneEmbedding`. That last step (local cyclic order of arcs at each vertex, plus face tracing equal to the dual's vertices) is still unbuilt.
- The cheapest route I can see: Barnette's `exists_exact_dual` gives `(P, D)` with cycle space = cut space. From that, a rotation system can be recovered combinatorially, because each dual vertex star is a face boundary cycle (Whitney/Edmonds). That last step is pure combinatorics, so no further topology would be needed. Unverified idea.

**`Geometry/PlaneColoring` / `no_proper_five_coloring`.**
- In `formalization.yaml` `status.main_results`: `comparator_config: ComparatorChallenges/EuclideanFiveColor.json`, `declaration: OAI.EuclideanFiveColor.no_proper_five_coloring`, `file: OAI/Geometry/PlaneColoring/Five.lean`.
- The JSON permits only `propext, Quot.sound, Classical.choice`. It has `definition_names: ["OAI.EuclideanFiveColor.ProperColoring"]`, i.e. a definition hole, the case Comparator's README says needs human oversight. The definition is a one-liner, so the risk is low but nonzero.
- I downloaded all 46 `PlaneColoring/*.lean` files (868 KB). They contain no `sorry`, `admit`, `axiom`, `native_decide`, `implemented_by` or `extern`. Their only non-local imports are `Mathlib`, `OAI.Analysis.PlaneSpectrum.CircleOperator` and `OAI.Analysis.PlaneSpectrum.Ergodicity`. Code search finds no `sorry` in `Analysis/PlaneSpectrum` (weak evidence).
- The repo publishes no Comparator run logs, so I found no positive record of a passing run. The catalogue's own status is `review: unchecked`. The claim is plausibly sorry-free, but **unverified**: confirming it needs `lake env comparator ComparatorChallenges/EuclideanFiveColor.json` or `#print axioms`. We did not compile anything.

## Key URLs

- https://github.com/openai/math/blob/main/lean/ComparatorChallenges/BarnetteHamiltonian.lean
- https://github.com/openai/math/tree/main/lean/OAI/Combinatorics/Hamiltonian (`Model.lean`, `Network.lean`, `ExactDual.lean`, `Corridors.lean`, `Traces.lean`, `Rectangle.lean`, `Main.lean`)
- https://github.com/openai/math/blob/main/lean/ComparatorChallenges/ListHadwiger.lean
- https://github.com/openai/math/blob/main/lean/OAI/Geometry/HyperbolicGroups/PictureMap.lean
- https://github.com/openai/math/blob/main/lean/OAI/Algebra/GroupRing/MapEuler.lean
- https://github.com/openai/math/tree/main/lean/OAI/Geometry/Cannon/PlaneTopology
- https://github.com/openai/math/blob/main/lean/formalization.yaml
- https://github.com/openai/math/blob/main/lean/ComparatorChallenges/README.md and https://github.com/leanprover/comparator
- https://github.com/alonamaloh/schoenflies-lean
- https://github.com/openai/math/blob/main/lean/ComparatorChallenges/KoebeCircleDomains.lean, `lean/OAI/Analysis/CircleDomains/{Main,Theorems}.lean`, `Topology/{JordanContours,PlanarSchoenfliesProof}.lean`, `Selection/OuterContours.lean`
- https://github.com/openai/math/tree/main/lean/OAI/Geometry/Cannon/CirclePacking
- https://github.com/openai/math/blob/main/lean/ComparatorChallenges/EuclideanFiveColor.json, `lean/OAI/Geometry/PlaneColoring/Five.lean`

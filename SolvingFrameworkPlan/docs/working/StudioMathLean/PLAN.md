# Studio Math: Lean plan for the Euler lemma and Theorem H (6 Oct 2026)

Status (updated 1406 MDT): **Piece 1 compiled.** `EulerCounting.lean` (SHA-256 prefix 4a2f0fb67de7d1d6), theorem `StudioMath.good_card_ge_twelve`, no `sorry`, `#print axioms` = [propext, Classical.choice, Quot.sound]. Checked as a single file with Lean v4.35.0-rc3 against the read-only Mathlib oleans of `~/mathlib4-planemap-build` (Mathlib 300d0e5) via LEAN_PATH, at nice -n 10; nothing in that directory was written. Not yet audited. Pieces 2 and 3 not started.

## Finding from reading the library [hand, from source]
`SphericalMap.edge_card_bound` (PlaneMap/SphericalDegree.lean) gives only `E + 1 ≤ V_support + F`. For a triangulation (3F = 2E) this yields E ≤ 3V − 3, i.e. Σ(deg−6) ≤ −6. The accepted Euler lemma needs Σ(deg−6) = −12 (E = 3V − 6), because its threshold is 12. So the existing inequality is one step too weak: the library's current `exists_pos_degree_le_five` needs only Σ(deg−6) < 0. We need the full Euler identity V − E + F = 2 for a connected triangulation.

## Update 1609 MDT: steps C and D compiled; sanity checks; statement list frozen

**Step C.** `OccToRing.lean` plus the four generated pairs `DiamondM/P` and `C2122M/P` (each a `…Cert` and an `…Occ`, made by `gen_occ.py`).
- `X.configOcc`: an `Occ T ring int` in a triangulation gives the deleted map `G` with the ring as a face (`ConfigOcc`) and smaller support.
- `X.colorable_of_occ`: the occurrence is reducible.
- ε = −1 uses the identity ring order; ε = +1 uses the reversed order.

**Step D.** `FrameF3.lean`, `four_color_of_RStarFrame : RStarFrame → ∀ M, M.graph.Colorable 4`. `RStarFrame` asks R\* only for `NoSep` triangulations that are free of both orientations of the diamond and of 2.122. The proof:
- separating triangle → F1;
- occurrence → its certificate;
- otherwise → the pure-clean vertex (F4).

`rStarFrame_of_noSepTri` shows that `RStarFrame` is weaker than `RStarNoSepTri`.

**Sanity checks.**
- `RStarSanity.lean`, on the icosahedron:
  - it is in the R\* class, and every vertex is pure-clean;
  - both diamond orientations occur, so `Occ` is not vacuous and the icosahedron is outside `RStarFrame`'s class;
  - 2.122 does not occur.
- `RadiusFive.lean`: the two audited radius-5 certificate states (`80b930d1…` hole 23, `91a307d1…` hole 22) satisfy the formal `PureFill … 5`, by explicit whole-component paths. `radius_bfs.py` independently gives distance exactly 5 under the same semantics. That lower bound is computed only.

**Checks.**
- All new theorems have axioms [propext, Classical.choice, Quot.sound].
- Sabotaged copies are rejected: a dropped exclusion, a wrong ring order, a bound of 4, and a truncated component.
- `check.sh` compiles all 23 modules in order.

**Statement list:** `../StudioMathStatements.md`. Part A covers the model assumptions, the headline statements and the gaps. Part B is every theorem, extracted by `extract_statements.py`.

## Design 1518 MDT: one D-reducibility interface (the diamond and 2.122 are instances)

**Done:** F1 + frame + F4 (`MinimalFrame.lean`, commit 3db558c).

**Configuration data, finite and decidable.** `Config` consists of:
- ring size k and interior size m;
- an interior adjacency table `Fin m → Fin m → Bool`;
- a ring–interior adjacency table `Fin k → Fin m → Bool`;
- the ring order r_0 … r_(k−1) (a cycle).

The diamond has k = 6, m = 4. 2.122 has k = 7.

**Occurrence in T** (`Occurs T K ρ ι`):
- ρ : Fin k → Fin n and ι : Fin m → Fin n are jointly injective;
- consecutive ring vertices are adjacent;
- interior adjacencies equal the tables;
- every T-neighbour of an interior vertex is a ring or interior vertex, so the degrees are the table degrees;
- an orientation condition: the ring is the boundary walk of the disc that contains the interior.

The exact wording is to be agreed with the audit.

**Certificate: Birkhoff's D-reducibility, as a checked Boolean.**
- E₀ is the set of proper ring colourings κ : Fin k → Fin 4 that extend to the interior (a finite search).
- κ ∈ E_(t+1) if κ ∈ E_t, or for some pair partition π = {a,b}|{c,d} the following holds. For every **consistent chain structure** S, meaning partitions of the {a,b}- and {c,d}-coloured ring vertices that are jointly non-crossing and contain the ring edges, some union of S's {a,b}-classes (or {c,d}-classes) when flipped gives κ′ ∈ E_t.
- D-reducible means every proper ring colouring lies in E_N.
- This is the classical D (Birkhoff, Heesch). A `Bool` checker `dred K`, proved sound once and run by `decide`, makes each configuration a one-line instance: `theorem diamond_dred : dred diamond = true := by decide`. C-reducible configurations, with a reducer, would be a later extension of the same interface.

**Soundness** (`colorable_of_occurs`): Occurs T K ρ ι, `dred K`, and G := T − interior colourable together imply T colourable. Plug-in to the frame: G has smaller support, so the induction hypothesis gives the colouring of G. The proof needs four pieces:
- **G0 (ring face):** after deleting the interior with `subgraph_tracked`, the ring is a face boundary of G. This is the k-cycle version of D3's LB, and uses the same potential argument.
- **G1 (face Jordan):** disjoint walks in G joining alternating vertices of one face boundary meet. Proof: insert a star vertex in the face, using a freed interior label, a bridge and then chords via `split`, and apply the library's `alternating_walks_intersect` at the star. **F2 needs the same lemma for a 4-face**, so it is built first.
- **C1 (chain structure is consistent):** the actual Kempe components of a colouring of G, restricted to the ring, form a jointly non-crossing structure, by G1.
- **C2 (flip realisation):** flipping a union of ring classes is realised by swapping the corresponding whole components of G, with `KempeStep`s and `properOff`-style lemmas.

**Order.** G1, then G0, then C1/C2 with the checker and its soundness, then the instances: the diamond, then 2.122. F2 reuses G1 and the 4-cycle version of G0, plus the Birkhoff case analysis.

**Open with the audit and Math.**
- The occurrence definition, especially the orientation and whether ring chords are allowed.
- Whether 2.122 is D-reducible or only C-reducible. If only C-reducible, the reducer extension is needed.

## Plan 1513 MDT: the classical minimal-counterexample frame (coordinator's redirect)

**Goal.** `four_color_of_frame_Rstar`: R\* assumed only for connected triangulations with
- minimum degree ≥ 5,
- no separating triangle,
- no separating 4-cycle,
- no Birkhoff diamond

implies that every spherical map is 4-colourable.

**Design change: induct on colourability, not on clean vertices.** The current `four_color_of_core_Rstar` threads a protected face through a clean-vertex induction because R\* is stated relative to φ. For a frame that excludes reducible configurations, the natural proof is the classical one: strong induction on the support size, over all spherical maps.

**Step 0. Reduce to the hard class.** `four_color_of_triangulated_five_extension` already handles degree ≤ 4 and completion, so we may assume a connected triangulation T of minimum degree 5. Then dispatch:

| case | argument | library pieces | new work | difficulty |
|---|---|---|---|---|
| **F1** separating triangle F | Both kept sides `keep_b` and `keep_(b+1)` are smaller spherical maps (D3, already compiled for either b) and so are colourable by induction. Every edge of T lies on one side. Permute the second colouring to agree on F's three distinct colours, and glue. **No Kempe chains.** | D1–D3 (`subgraph_tracked`, `kept_*`), `supportTransport` | covering lemma, permutation, gluing | medium |
| **F2** separating 4-cycle abcd | Birkhoff: colour each side with a chord added in its 4-face (or with a pair identified). Match the ring patterns; a mismatch is repaired by one Kempe swap on one side, whose failure gives a Jordan separation of the other pair. | D2's potential generalises to any even cycle; `RotationSystem.split` / `SphericalChordInsert` to insert a chosen chord; Jordan across a face via `alternating_walks_intersect` after stellar insertion (`RotationInsert`) | sides of a 4-cycle (D2/D3 generalised to a 4-face), inserting a *chosen* chord, face Jordan lemma, the Kempe case analysis | **hard** (days) |
| **F3** Birkhoff diamond (ring 6, four interior vertices of degree 5) | D-reducibility: delete the 4 interior vertices, colour the remainder G − K (smaller), then show every ring-6 colouring that occurs can be Kempe-modified in G − K to one that extends into K. This is a finite enumeration over ring colourings × planar chain patterns. | `KempeStep`, the clique-lift style restriction, Jordan non-crossing of chains outside the ring | recognising the configuration; deleting K (isolate ×4); the ring-6 colouring table; the planar chain-matching lemma; the per-colouring Kempe certificates (decide-style) | **very hard** (a week or more) |
| **F4** otherwise | R\* gives a pure-clean degree-5 v. Colour T − v (smaller) and fill (`extend_of_pureClean`). | link A | none | easy |

**Order and honest estimate.**
1. F1 together with the colourability frame and F4. That gives `four_color_of_frame_Rstar_triangles`, with R\* asked only for triangulations with no separating triangle: an alternative to link D with no protected face.
2. F2.
3. F3.

Each piece is pushed as it compiles. F3 is the largest single formalisation in this project so far. The Lean design of a reusable "D-reducible configuration ⇒ minimal counterexample avoids it" interface (ring, ring colourings, chain patterns) should come first, because RSST-style lists would reuse it.

**Hypotheses to check with Math and the audit before F2/F3.**
- The precise definition of "Birkhoff diamond" in `Fin n` language. Proposal: four vertices u1..u4 of degree 5 forming two triangles u1u2u3 and u2u3u4 that share the edge u2u3, with a ring of 6 distinct vertices.
- Whether "no separating 4-cycle" should allow the trivial 4-cycles around a degree-4 vertex. They are excluded anyway by minimum degree 5.

## Update 1511 MDT: link D and the wrapper compiled. **R\* (four-connected core) ⇒ 4CT**

- **`SphericalMap.four_color_of_core_Rstar : RStarCore → ∀ M : SphericalMap n, M.graph.Colorable 4`**, plus `four_color_of_core_Rstar_planeMap` for the library's `PlaneMap`s.
- **`RStarCore`** (`PlaneMap/RStarCore.lean`, docstring) is the hand Lemma R\*. Take any spherical map T and vertices p, q, r such that:
  - T is connected and triangulated;
  - pq, qr, rp are edges and pqr bounds a face (the protected face φ);
  - every triangle bounds a face (`NoSep`, the four-connected core);
  - every vertex off φ has degree ≥ 5.

  Then ∃ v ∉ φ of degree 5 with `PureClean T v`.
- **Proof.**
  - D1 `subgraph_tracked`;
  - D2 sides via `Fills`;
  - D3 `kept_triangulated`, `kept_facial`, `kept_degree`, `kept_reach`;
  - D4 `pureClean_lift`;
  - D5 `cleanOff_of_RStarSupport` (strong induction on the support size) and `four_color_of_RStarSupport`;
  - the wrapper `rStarSupport_of_core` relabels onto the support (`supportTransport`): it transports the triangulation, faces, NoSep, degrees and connectivity, and pulls back pure-cleanness.
- **Checks.** Standard axioms only; no `sorry`, `admit` or `native_decide` in any module; sabotaged copies rejected. `check.sh` builds all five modules.
- **Notes for the audit.**
  1. The degree of the φ vertices is unconstrained in `RStarCore`. In the hand core class they have degree ≥ 4 automatically. The quantified class is the same, but that equality is **not** formalised.
  2. `Facial T p q r` := `Nx T q p r ∨ Nx T p q r`: r is the third vertex of one of the two faces on the edge pq.
  3. R\*'s conclusion is `PureClean` (every colouring of T − v fills by pure swaps). The hand form says every *doubly locked* state has finite radius. These are equivalent, and only the trivial direction is used (see the definitions table below).

## Update 1446 MDT: links A–C compiled (`PlaneMap/RStar.lean`)

- **A.** `extend_of_pureClean`: `PureClean T r` → (T − r 4-colourable → T 4-colourable).
- **`four_color_of_global_Rstar`.**
  - Hypothesis: **every** connected spherical triangulation of minimum degree 5 has a pure-clean vertex of degree 5.
  - Conclusion: every `SphericalMap` is 4-colourable.
  - **This assumes the clean-vertex property for all min-5 triangulations, not only for the 4-connected relative-class core.** The core version needs link D.
- **B.** `pureClean_iff_locked`: it suffices to check the colourings with no fill within one swap.
- **C.** `pureClean_of_theorem_H`, `pureClean_of_theorem_HP`. These hold only at holes of the H/HP classes. "Every min-5 triangulation has an H- or HP-class vertex" is **false** (the pentakis dodecahedron has only (6⁵) holes), so C is not a four-colour theorem.
- **Axioms:** standard only. `check.sh` now compiles the three modules in order into a copy-on-write clone of the built Mathlib tree.

**Definitions: library notion versus hand notion (for the audit).**

| hand | library / here | match |
|---|---|---|
| state at hole v | `c : Fin n → Fin 4` with `ProperOff G v c`; the value at v is ignored | same (an extra dummy value) |
| Kempe swap | `KempeStep`: a whole component of `pairGraph` (the two-colour subgraph of G − v), colours exchanged | same |
| fill F (link uses ≤ 3 colours) | `Target G v c`: some colour is missing on N(v) | same (4 colours) |
| radius r(s) ≤ m | `PureFill G v c m`: a pure swap path of length ≤ m to a `Target` state | same |
| pure-clean / KD(v) | `PureClean T v` | same |
| doubly locked | not defined. `pureClean_iff_locked` uses "no `PureFill` within 1" instead. By the hand Step 1 and the one-swap analysis, an unfilled state fails to fill within one swap exactly when both locks hold. **That equivalence is not formalised**, and is not needed: the hypothesis is stated as `PureClean`. | stated form is the stronger or equal one |
| R\*'s "finitely many swaps" | `∃ m, PureFill ... m` | same |

## Plan
1. **Piece 1: counting lemma** (`EulerCounting.lean`, compiled, `good_card_ge_twelve`). Pure `SimpleGraph` statement: min degree ≥ 5 and 2E + 12 ≤ 6V imply at least 12 degree-5 vertices with at most one neighbour of degree ≥ 12. Needs only Mathlib (handshake `sum_degrees_eq_twice_card_edges`, double counting). Can be built and checked in isolation with a single-file `lake env lean`, which is light.
2. **Piece 2: sharp Euler bound** for the `SphericalMap` carrier, all faces of length 3 and a connected graph: `2E + 12 ≤ 6V`. Two extra facts beyond `edge_card_bound`: rank(incidence) = V − 1 (connected graph) and dim ker(boundary) = 1 (dual connected, which follows from connectivity of the graph). Alternative: derive E ≤ 3V − 6 from a quadrangulation or girth argument. I have not chosen yet. This is the real work.
3. **Piece 3: Theorem H**, after the local combinatorics is stated: a `vacancy state` in the library's existing `SimpleGraph.Vacancy*` language (inspect `VacancySlide.lean` and `VacancyShortFill.lean`), hypothesis "the five link vertices have degree 5, rotation at v is the cyclic order, no chord in the link". The proof is a finite colour case analysis once the DL predicate and the swap are defined.

## Open decision for the coordinator
The hole-fill statements need the plane-map carrier (rotation, outer ring w_t) rather than a bare `SimpleGraph`. I will ask the Math team (Lean owner) how `Vacancy*` states it before writing Piece 3.

## Plan 1441 MDT: "R* implies the Four Colour Theorem" in Lean

**Finding that shortens the chain.** The library already compiles
`SphericalMap.four_color_of_triangulated_five_extension` (`SphericalFourContact.lean`, in the audited 8299419 set):
- **Gate hypothesis:** `TriangulatedFiveExtension`. Every connected spherical triangulation T of minimum degree 5 has a degree-5 vertex r with (T − r 4-colourable → T 4-colourable).
- **Conclusion:** every `SphericalMap` is 4-colourable.

R*'s conclusion at v is *every colouring of T − v reaches a fill by pure swaps*. That gives the gate's implication at r = v immediately: colour T − v, swap to a fill, then put the missing colour on v.

So for **R* ⇒ 4CT** the fan machinery is not needed: VH_C, φ-good fans, VH∃, T\*_τ, mixed moves and Theorem A. Those links (L1, L2, L4, L6 and vh-exists Theorem A) are needed only for VH∃ itself as a hypothesis, which is weaker than R*. The formal chain is:

| link | statement in the library's language | uses (compiled) | difficulty |
|---|---|---|---|
| **A. pure-clean ⇒ gate** | `PureClean T r` := ∀ c, `ProperOff T.graph r c` → ∃ m, `PureFill T.graph r c m`. Then `(∀ T conn. tri. min-5, ∃ r, deg r = 5 ∧ PureClean T r)` → every `SphericalMap` is 4-colourable. | `four_color_of_triangulated_five_extension`, `PureFill`/`Target` | easy (hours) |
| **B. DL form** | "every colouring with no fill within one swap fills eventually" ⇔ `PureClean`. This is L3, and trivial: a doubly locked state has radius ≥ 2, and the others fill in ≤ 1. | none | trivial |
| **C. light vertices are clean** | `theorem_H` / `theorem_HP` ⇒ `PureClean` at a degree-5 vertex with ≤ 1 neighbour of degree ≥ 6 and no separating triangle through it. Corollary: 4CT holds if every connected min-5 triangulation has such a vertex (conditional, but fully compiled). | this branch's `theorem_H`, `theorem_HP` | easy |
| **D. L5, separating-triangle reduction** | `RStar` := every connected triangulation T with a facial triangle φ, every vertex off φ of degree ≥ 5 and on φ of degree ≥ 4, and **no separating triangle** (`∀ triangle, facial`), has a degree-5 v ∉ φ with `PureClean T v`. Then `RStar` ⇒ every connected min-5 triangulation has a pure-clean degree-5 vertex. Proof: induction on order. At a separating triangle F, build the side A not containing φ as a `SphericalMap` with F as a face (isolate the far side's vertices and transport the support). Apply `RStar` to (A, F), using `relative_light_fives` only if the counting form is wanted. Lift pure-cleanness by `VacancyCliqueLift.interior_fill_lift`. | `isolate_closed`, `supportTransport`, `VacancyCliqueLift`, `JordanSides` | **hard** (days). The new content is the side map: after isolating B − F, the region face must be the triangle F. |
| **E. assembly** | `RStar` → every `SphericalMap` (and `PlaneMap`) is 4-colourable. | A + D | easy once D is done |
| (optional) **F. VH∃ ⇒ 4CT** | needs T\*_τ (isolate v, insert two chosen chords into the pentagon), mixed paths, and the containment lemma | `isolate_closed`, `RotationSystem.split`, `MixedPath` | medium–hard; not on the R* path |

**Hypothesis to settle with the audit before D.** "4-connected" for (T, φ) is stated as "every triangle of T is facial". This matches `NoSeparatingTriangleAt`, used globally. The relative class allows degree 4 on φ. Its Euler side is `relative_light_fives`, which is already compiled.

**Order of work.** A + B + C now, then D, then E. F only on request.

## Update 1438 MDT: Theorem HP compiled (same file, `VacancyIcosahedral.lean`)

- **`SphericalMap.theorem_HP`.**
  - Hypotheses: `M.Triangulated`; `degree h = 5`; a neighbour p of h; every other neighbour of h has degree 5; `NoSeparatingTriangleAt h`.
  - Conclusion: every proper 4-colouring of T − h has `PureFill ... 6`.
  - **Nothing is assumed about p**, not even degree ≥ 5.
- **Structure**, following `MathHighDegreeNeighbour.md` §2:
  - `HPBall`: the two-ball with free port k, the rotation included, plus a shift lemma.
  - `moveF_R1`, `moveF_R3`, `moveB_R1`, `moveB_R3` (Lemma 3): each image, read in the frame shifted by 3 or 2 after a colour renaming, has the other ring word. The free port moves to k − 3 or k − 2 (= k + 3).
  - `killB`, `killF` (B- and F-starvation) and `chainR3_34` (AB at k = 3, 4): Lemma 2.
  - `hp_cases`: Lemma 1 for every k, by `decide` over 5·4⁵ cases. It concludes R1, R3, B-killable (k ≠ 0) or F-killable (k ≠ 2).
  - Chains with the hand termination table's bounds:
    - `chainR3_34`: ≤ 2;
    - `chainR1_012`: ≤ 3;
    - `chainR3_02`: ≤ 4;
    - `chainR1_34`: ≤ 5;
    - `chainR3_1`: ≤ 6.
  - `hp_fill_normalized` → `hp_fill` (any colouring) → `hpBall_of_triangulated` → `theorem_HP`.
- **Non-vacuity:** `Icosahedron.theorem_HP_icosahedron`, at vertex 0 with p = 1.
- **Checks:** `#print axioms` lists propext, Classical.choice and Quot.sound only, and `hp_cases` uses propext only. No `sorry`. A sabotaged copy (wrong frame shift in `chainR3_1`) was rejected.

## Update 1429 MDT: relative-class Euler lemma (audit S1)

- `StudioMath.good_card_add_two_four`: the counting core with degree-4 vertices allowed, each costing two. It shows 12 ≤ good + 2·n₄. `good_card_ge_twelve` is now its corollary.
- `StudioMath.good_off_add_four`: let φ have at most 3 vertices, every vertex off φ degree ≥ 5, and every vertex on φ degree ≥ 4 (if 4, then it is on φ). Then 2E + 12 ≤ 6V implies **9 ≤ #(good off φ) + n₄**, where n₄ = #(degree-4 vertices on φ).
- `SphericalMap.relative_light_fives`: the same for spherical triangulations.
  - This is the audit's 13:25 repair: at least 9 − n₄ good vertices off φ, so ≥ 7 when n₄ ≤ 2.
  - It needs neither n₄ ≤ 2 nor 4-connectivity. φ is any vertex set of size ≤ 3; in the application it is the protected face.
- Non-vacuity: `Icosahedron.relative_light_fives_icosahedron`, with φ = {0,1,5} and n₄ = 0. **No instance with n₄ > 0 has been built.**
- `#print axioms`: propext, Classical.choice, Quot.sound only.

## Update 1427 MDT: the IcoBall derivation and non-vacuity (answers audit S3; derivation done)

- **Dedupe.** `EulerCounting.lean` is removed. Its content lives only in `PlaneMap/EulerSharp.lean`, so each declaration exists exactly once.
- **`SphericalMap.theorem_H`** in `PlaneMap/VacancyIcosahedral.lean`, now with **no `IcoBall` hypothesis**.
  - Hypotheses: `M.Triangulated`; `degree h = 5`; every neighbour of h has degree 5; `M.NoSeparatingTriangleAt h`.
  - Conclusion: every proper 4-colouring of T − h has `PureFill ... 3`.
  - `NoSeparatingTriangleAt h` means: if two neighbours u, v of h are adjacent, then they are consecutive in the rotation at h. On a triangulation, that is exactly the statement that every triangle through h is a face.
  - It is used only to exclude the chord x_t x_{t+3}, i.e. w_t = x_{t+3}.
- **`icoBall_of_triangulated`** derives `IcoBall` from those hypotheses.
  - Triangle law `nx_tri`: three `faceNext` steps close a face.
  - `orbit5` / `chain5`: at a degree-5 vertex the rotation is one 5-cycle of darts. So the rotation at x_t reads w_t → x_{t+1} → h → x_{t−1} → w_{t−1} and lists every neighbour exactly once.
- **Non-vacuity**, on the library's `Icosahedron.sphericalMap`:
  - `Icosahedron.theorem_H_icosahedron`: every hypothesis of `theorem_H` holds at vertex 0, for an explicit colouring `sampleColouring` that is proper off 0 and **not** already filled (`sampleColouring_unfilled`).
  - `Icosahedron.twelve_light_fives_icosahedron`: the hypotheses of the Euler lemma hold.
- **Axioms.** `#print axioms` for all of these lists propext, Classical.choice and Quot.sound only. No `sorry`.
- **Note.** The icosahedron has no doubly locked state, so the sample exercises the statement, not the R1–R3 branches.

## Compiled 1419 MDT (single-file checks, read-only against the built snapshot 8299419; not yet audited)

Reproduce with `check.sh`. Hashes are in `SHA256SUMS`. No file contains `sorry`. `#print axioms` lists only propext, Classical.choice and Quot.sound; `ring_cases` uses only propext. A deliberately broken copy was rejected, which confirms that the check really elaborates the proofs.

| file | main theorem | statement |
|---|---|---|
| (in `EulerSharp.lean`) | `StudioMath.good_card_ge_twelve` | finite simple graph, every degree ≥ 5, 2E + 12 ≤ 6V ⇒ ≥ 12 degree-5 vertices with ≤ 1 neighbour of degree ≥ 12 |
| `PlaneMap/EulerSharp.lean` | `SphericalMap.edge_card_bound_sharp` | any `SphericalMap` with a dart: E + 2 ≤ n + F (no connectivity hypothesis) |
| | `SphericalMap.twice_edges_add_twelve_le` | all faces of length 3 ⇒ 2E + 12 ≤ 6n |
| | `SphericalMap.twelve_light_fives` | **Euler lemma:** spherical triangulation (a dart, all faces of length 3), every vertex of degree ≥ 5 ⇒ ≥ 12 degree-5 vertices with ≤ 1 neighbour of degree ≥ 12. The file repeats the counting lemma so that it is self-contained. |
| `PlaneMap/VacancyIcosahedral.lean` | `SphericalMap.ico_fill` | **Theorem H:** hole h with `FiveLink` L in rotation order, and `IcoBall` (see below) ⇒ every proper 4-colouring of T − h has `PureFill ... 3` (a filled hole within ≤ 3 whole-component Kempe swaps) |
| | `VacancyIcosahedral.ico_fill_normalized` | the same on any `SimpleGraph`, for link word 0,1,0,2,3, given the library's `Alternation` |

**What `IcoBall` assumes, for the auditor.** `IcoBall G h L w` is an explicit hypothesis. It is not derived from "triangulation and degree 5". It requires:
- each `L.port t` has neighbour set exactly {h, port(t−1), port(t+1), w(t−1), w(t)};
- w(t) ~ w(t+1);
- w(t) is neither a port nor h.

In a triangulation with no separating triangle through h, these follow from the five link vertices having degree 5. That derivation is **not** formalised. The statement is therefore Theorem H over the local data, which is how `MathRadiusGeometry.md` states it. The conclusion is stronger than "radius ≤ 3 for doubly locked states": it covers every colouring.

**Not done:** Theorem HP; the derivation of `IcoBall` from triangulation and degree hypotheses; the R* links.

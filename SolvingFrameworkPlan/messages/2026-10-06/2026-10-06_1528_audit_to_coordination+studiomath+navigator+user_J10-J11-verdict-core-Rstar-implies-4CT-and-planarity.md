# J10 and J11 verdict: PASSED. "R\* in the four-connected core ⇒ every spherical map is 4-colourable" is compiled and audited. What "planar" means in this Lean development (no planarity axioms; one bridge not formalised)

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Proof Navigator; the user (planarity question from the outside advisor)
- **Sent:** 2026-10-06 15:28 MDT
- **Replies to:** the coordinator's J10 and J11 note; the evidence on `main`:
  - `backgroundMaterial/planemap-structural/longtable/lean-studiomath-audit-6/` (J10, `f0f7005`);
  - `lean-studiomath-audit-7/` (J11, `ef83ddb`), at worktree `dcb7818`
- **Asks for:**
  - Navigator: record the wording in §2.
  - Coordinator: the bounty (§2).
  - Severn and the user: §3 is the sentence to use when anyone asks what "compiled" means.

Nothing was run on the MacBook. The audit read the evidence (`git show`, plus a diff of the compiled copies against `main`) and the library sources in the live checkout.

## 1. The check (J11 supersedes J10: same procedure, plus MinimalFrame)

- **Files.** `shasum -c` OK for six files: EulerSharp, MinimalFrame (`08cf33da…`), RStar, RStarCore, SideTriangle and VacancyIcosahedral. **All six compiled copies equal the current `main` files** (997, 264, 228, 109, 1,571 and 325 lines), checked by diff.
- **Grep and builds.** The escape-hatch grep is empty. The folder's `check.sh` (into a copy-on-write clone of the base build, as in J9) ends `exit 0`, and every audit copy ends `exit 0`. Warnings are linter-only: unused section variables and unused names.
- **Axioms.** Per-file sweeps: SideTriangle 64, RStarCore 14, MinimalFrame 9, RStar 8, VacancyIcosahedral 76 and EulerSharp 19 constants, all **0 nonstandard**. The headline theorems print `[propext, Classical.choice, Quot.sound]`:
  - `four_color_of_core_Rstar`;
  - `four_color_of_core_Rstar_planeMap`;
  - `four_color_of_RStarSupport`;
  - `four_color_of_RStar_noSepTri`;
  - `rStarNoSepTri_of_core`.
- **Negative control.** The planted `sorry` is reported as `sorryAx`.
- **J11's discarded first attempt** (a script slip that dropped the prints, everything compiled) is recorded in its README. Accepted.

## 2. The statements, read against the hand results

- **`RStarCore`.** For every spherical map T and vertices p, q, r:
  - T is connected and `Triangulated`;
  - pq, qr and rp are edges, and pqr is `Facial` (the protected face φ);
  - `NoSep` holds (every triangle is facial, so there is no separating triangle, which is the four-connected core);
  - every vertex off φ has degree ≥ 5.

  Then `CleanOff`: there is a v ∉ φ of degree 5 that is `PureClean` (every proper colouring of T − v reaches a filled state by finitely many pure Kempe swaps).
  - **This is the hand Lemma R\*** (`2026-10-06_1325`, the audit's chain read). "Every DL state has finite radius" and "pure-clean" are equivalent by link L3, because a non-DL unfilled state fills in one swap.
  - The φ-vertices may have any degree. Under `NoSep` they have degree ≥ 4.
- **`four_color_of_core_Rstar : RStarCore → ∀ M : SphericalMap n, M.graph.Colorable 4`.** This is the core-class reduction, with link D included. Together with J9 it compiles **all six links of the hand chain**, now in the core form.
- **`MinimalFrame`.**
  - `RStarNoSepTri`: every connected, triangulated, `NoSep`, minimum-degree-5 spherical map has a degree-5 `PureClean` vertex.
  - `four_color_of_RStar_noSepTri : RStarNoSepTri → 4CT`.
  - `rStarNoSepTri_of_core : RStarCore → RStarNoSepTri`.
  - So the **minimal-counterexample frame F1 is compiled**: it is enough to prove R\* for four-connected minimum-degree-5 triangulations, with no protected face.
- **Verdict: PASSED.** The hypotheses are open statements. The theorems are conditional.

**Ledger wording.** "Compiled and audited (J10, J11): Lemma R\* for the four-connected core (`RStarCore`) implies that every spherical map is 4-colourable. The same holds for R\* restricted to four-connected minimum-degree-5 triangulations (`RStarNoSepTri`). Both hypotheses are open."

**Bounty.** The 300-point condition ("the R\* reduction compiled in Lean, no sorry, standard axioms, in an audit") is **met** by Studio Math's work, in the audit's view. The audit takes no share.

## 3. What the Lean development assumes about planarity (for the outside advisor)

- **No planarity axiom, and no axiom of any kind beyond Lean's three standard ones.** Every module in the audited set and in J5–J11 was swept constant by constant (1,903 constants in the 79-module snapshot, plus the per-file sweeps above), with negative controls. There is no `sorry`, `axiom`, `native_decide`, `implemented_by` or `extern`.
- **Planarity is a definition, carried as data.** `SphericalMap n` (`PlaneMap/SphericalMap.lean`) is a structure: a simple graph on `Fin n`, a rotation system (a cyclic order of darts at every vertex, so the faces are determined), and a proof of `RotationSystem.Fills`. `Fills` says that **every mod-2 even edge set (cycle-space element) is a sum of face boundaries**.
  - For the surface a rotation system defines, this says that mod-2 first homology vanishes, which for a connected graph means the surface is a **sphere**. This is the standard topological reading, not a Lean theorem.
  - So `SphericalMap` is a faithful combinatorial definition of a graph embedded in the sphere, each component on its own sphere.
- **All Jordan-type facts are theorems from that definition.** They include:
  - `JordanEven`;
  - `JordanCycle`;
  - `vacancy_alternation`, whose docstring reads "all separation inputs … are discharged from the native spherical rotation and face-sum theory";
  - the clique and side-triangle lifts.

  The Lean theorems use them as proved lemmas, not as hypotheses.
- **What is not formalised: the bridge to "planar graph" in the usual sense.**
  - The library proves that every `PlaneMap` (a map built by the planar vertex and edge insertions) is a `SphericalMap` (`ofPlaneMap`, via JordanEven).
  - It does **not** prove that every abstractly planar graph, whether defined by a drawing in ℝ² or by Kuratowski's theorem, admits a `SphericalMap` structure. That is the combinatorial embedding theorem: standard mathematics, but not in this development, and not in Mathlib as far as the audit knows.
  - So the honest statement of what is compiled is: **"every graph presented with a spherical rotation system is 4-colourable, provided R\* holds"**. The Five Colour demo's docstring already states this scope boundary.
- **One limit of the audit's own reading.** The audit read the `SphericalMap` and `Fills` definitions directly. It did **not** re-read `RotationSystem`'s face construction (`faceOf`, `faceNext`) line by line. That construction is in the audited 105-module set, and the faces are the orbits of the face permutation, as standard.

— Independent audit

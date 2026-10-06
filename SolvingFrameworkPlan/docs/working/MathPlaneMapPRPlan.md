# PlaneMap to Mathlib: pull request plan

Date: 6 October 2026. Author: Math Lean worker (read-only survey; nothing was edited, staged or committed in the checkout). Checkout: `/Users/fulkanjou/mathlib4-planemap`, branch `master`, HEAD `7d79788`, Lean `leanprover/lean4:v4.35.0-rc3`.

## 0. Facts that change the commission's numbers

- The directory `Mathlib/Combinatorics/SimpleGraph/PlaneMap/` holds 86 files on disk but only **49 are tracked** (git ls-files). 37 are untracked. Together with `PlaneMap.lean` (338 lines) and the 6 `Coloring/*Kempe*` files that the PlaneMap proofs import, the tracked set is **56 modules, 13,336 lines**. This table covers those 56. Tests: 27 tracked `MathlibTest/PlaneMap*.lean`.
- Excluded (untracked, 38 files incl. `PlaneMap/FiveColorDemo.lean`): BeltCapsMath BeltDWalkTeamA BeltOpeningWords BeltVacancyTeamA FiveColorDemo PoleStarEscape SphericalVacancyEasy TheoremPPole{Basic,Chain,Cut,Degen,Flip,Moves,NoSingleton,Rules} TwoPoleBelt{,AllRoots,Caps,EqualPoles,PoleB,PoleHole,TeamB,Transport,VacancyHyp,VacancyHypDef,Walk} VacancyCliqueLift VacancyEasyNeighbour VacancyLemmaL4 VacancyMobility{,General,Triangulated} VacancyPotential VacancyProtectedLift VacancyShortFill{,TeamA,TeamB} VacancyThreeMoveObstruction. Of these, 14 are in the 105-module audit (BeltOpeningWords, TwoPoleBelt, TwoPoleBeltAllRoots, TwoPoleBeltCaps, TwoPoleBeltTransport, TwoPoleBeltWalk, VacancyCliqueLift, VacancyMobility, VacancyMobilityGeneral, VacancyMobilityTriangulated, VacancyPotential, VacancyProtectedLift, VacancyShortFill, VacancyThreeMoveObstruction); 24 are not (including every *TeamA/*TeamB, BeltCapsMath, and FiveColorDemo). Only these 14 are candidates for the "later" series, after they are committed.
- The 105-module audit = 6 `Coloring` modules + 99 PlaneMap modules. Of the 56 tracked modules, **55 are in the audit; `RankPortfolio` is not**.
- No `sorry`, `admit`, `native_decide`, `unsafe` or `axiom` declaration in any of the 56 (comment-stripped grep; the table shows `-` throughout).

## 1. Table of the 56 tracked modules

Columns: lines; layer (0 = no in-set imports); direct imports within the set (prefix `Mathlib.Combinatorics.SimpleGraph.` dropped); in the 105 audit; banned tokens; Mathlib copyright header present (first line `/-` then `Copyright`).

| Module | Lines | Layer | Direct imports in set | Audited | sorry/native_decide/axiom | Header |
|---|---|---|---|---|---|---|
| Coloring.Kempe | 396 | 0 | - | Y | - | N |
| PlaneMap.BreadcrumbWarning | 105 | 0 | - | Y | - | Y |
| PlaneMap.ErasePermutation | 75 | 0 | - | Y | - | N |
| PlaneMap.RotationSystem | 644 | 0 | - | Y | - | Y |
| Coloring.FiniteReachability | 122 | 1 | Coloring.Kempe | Y | - | N |
| Coloring.FiveColorExtension | 249 | 1 | Coloring.Kempe | Y | - | N |
| Coloring.KempeMass | 247 | 1 | Coloring.Kempe | Y | - | N |
| Coloring.KempeRepartition | 170 | 1 | Coloring.Kempe | Y | - | N |
| PlaneMap.Construction | 1065 | 1 | PlaneMap.RotationSystem | Y | - | Y |
| PlaneMap.FaceCorner | 87 | 1 | PlaneMap.RotationSystem | Y | - | N |
| PlaneMap.InsertPermutation | 294 | 1 | PlaneMap.ErasePermutation | Y | - | N |
| PlaneMap.SharedHub | 105 | 1 | PlaneMap.RotationSystem | Y | - | Y |
| Coloring.KempeBoundary | 137 | 2 | Coloring.FiniteReachability, Coloring.KempeMass | Y | - | N |
| PlaneMap | 338 | 2 | PlaneMap.Construction | Y | - | Y |
| PlaneMap.RotationInsert | 136 | 2 | PlaneMap.Construction | Y | - | Y |
| PlaneMap.Examples | 552 | 3 | PlaneMap | Y | - | Y |
| PlaneMap.Jordan | 629 | 3 | PlaneMap | Y | - | Y |
| PlaneMap.SingletonExterior | 48 | 3 | Coloring.KempeBoundary | Y | - | N |
| PlaneMap.JordanFace | 189 | 4 | PlaneMap.Jordan | Y | - | Y |
| PlaneMap.JordanGrow | 56 | 4 | PlaneMap.Jordan | Y | - | Y |
| PlaneMap.JordanSides | 1104 | 4 | PlaneMap.Examples | Y | - | Y |
| PlaneMap.JordanSplit | 390 | 5 | PlaneMap.Jordan, PlaneMap.JordanFace | Y | - | Y |
| PlaneMap.JordanEven | 450 | 6 | PlaneMap.Jordan, PlaneMap.JordanSplit, PlaneMap.JordanFace | Y | - | Y |
| PlaneMap.JordanCycle | 320 | 7 | PlaneMap.Jordan, PlaneMap.JordanSides, PlaneMap.JordanEven | Y | - | Y |
| PlaneMap.JordanTwoSides | 96 | 8 | PlaneMap.JordanCycle | Y | - | N |
| PlaneMap.JordanWalkParity | 110 | 8 | PlaneMap.JordanCycle | Y | - | N |
| PlaneMap.SphericalMap | 90 | 8 | PlaneMap.JordanCycle | Y | - | N |
| PlaneMap.FiveColorSeparation | 226 | 9 | PlaneMap.JordanWalkParity | Y | - | N |
| PlaneMap.Icosahedron | 365 | 9 | PlaneMap.SphericalMap | Y | - | Y |
| PlaneMap.RotationBoundary | 309 | 9 | PlaneMap.SphericalMap | Y | - | Y |
| PlaneMap.RotationDelete | 106 | 9 | PlaneMap.SphericalMap, PlaneMap.ErasePermutation | Y | - | N |
| PlaneMap.SphericalDegree | 189 | 9 | PlaneMap.SphericalMap | Y | - | N |
| PlaneMap.SphericalFiveColor | 413 | 9 | PlaneMap.SphericalMap, Coloring.FiveColorExtension | Y | - | N |
| PlaneMap.FaceChord | 249 | 10 | PlaneMap.SphericalFiveColor, PlaneMap.FaceCorner | Y | - | N |
| PlaneMap.FiveColor | 105 | 10 | PlaneMap.FiveColorSeparation, Coloring.FiveColorExtension | Y | - | N |
| PlaneMap.FourColorExtension | 306 | 10 | PlaneMap.SphericalFiveColor | Y | - | N |
| PlaneMap.RotationSplit | 286 | 10 | PlaneMap.RotationInsert, PlaneMap.RotationBoundary | Y | - | Y |
| PlaneMap.SphericalDelete | 222 | 10 | PlaneMap.RotationDelete | Y | - | N |
| PlaneMap.SphericalSmallOrder | 204 | 10 | PlaneMap.SphericalDegree | Y | - | N |
| PlaneMap.DegreeFiveOutside | 168 | 11 | PlaneMap.SphericalSmallOrder | Y | - | Y |
| PlaneMap.DeleteVertex | 51 | 11 | PlaneMap.FiveColor | Y | - | N |
| PlaneMap.FiniteFourExtension | 282 | 11 | PlaneMap.FourColorExtension, Coloring.FiniteReachability | Y | - | N |
| PlaneMap.FiveColorTheorem | 58 | 11 | PlaneMap.SphericalFiveColor, PlaneMap.SphericalDelete, PlaneMap.SphericalDegree | Y | - | N |
| PlaneMap.FourColorSmallOrder | 87 | 11 | PlaneMap.FourColorExtension, PlaneMap.SphericalSmallOrder, PlaneMap.SphericalDelete | Y | - | N |
| PlaneMap.RotationSplitFills | 153 | 11 | PlaneMap.RotationSplit | Y | - | Y |
| PlaneMap.SupportTransport | 243 | 11 | PlaneMap.SphericalMap, PlaneMap.SphericalDelete | Y | - | N |
| PlaneMap.VacancySlide | 108 | 11 | PlaneMap.SphericalDelete | Y | - | Y |
| PlaneMap.FiveColorExamples | 34 | 12 | PlaneMap.DeleteVertex | Y | - | N |
| PlaneMap.FourEliminationOrder | 86 | 12 | PlaneMap.FourColorSmallOrder | Y | - | N |
| PlaneMap.RotationBridgeFills | 224 | 12 | PlaneMap.RotationSplitFills | Y | - | Y |
| PlaneMap.SphericalChordInsert | 53 | 12 | PlaneMap.FaceChord, PlaneMap.RotationSplitFills | Y | - | Y |
| PlaneMap.SphericalCompletion | 122 | 13 | PlaneMap.SphericalChordInsert, PlaneMap.RotationBridgeFills | Y | - | Y |
| PlaneMap.SphericalFourContact | 90 | 14 | PlaneMap.SphericalCompletion, PlaneMap.SupportTransport, PlaneMap.FourColorExtension | Y | - | Y |
| PlaneMap.SphericalMassContact | 128 | 15 | PlaneMap.SphericalFourContact, PlaneMap.BreadcrumbWarning, Coloring.KempeBoundary | Y | - | Y |
| PlaneMap.SphericalRankedContact | 161 | 16 | PlaneMap.SphericalMassContact | Y | - | Y |
| PlaneMap.RankPortfolio | 104 | 17 | PlaneMap.SphericalRankedContact | N | - | Y |

Total 13,336 lines. 29 of 56 files have **no copyright header** (all 6 Coloring files, and 23 PlaneMap files; list in section 4). 2 files have no `/-! ... -/` module docstring: `FaceChord`, `SupportTransport`. 1 line over 100 characters (`SupportTransport`). No trailing whitespace. No `#guard_msgs` anywhere in the library files (the tests use guarded axiom reports in MathlibTest, not `#guard_msgs`). Every file uses `module` / `public import` / `@[expose] public section` (new Mathlib module system).

## 2. Import DAG and layering

Layers are the longest-path depth in the table (column "Layer"). Summary, 18 layers (0 to 17):

- L0: Coloring.Kempe, ErasePermutation, RotationSystem, BreadcrumbWarning
- L1: Coloring.{FiniteReachability, FiveColorExtension, KempeMass, KempeRepartition}, Construction, FaceCorner, InsertPermutation, SharedHub
- L2: Coloring.KempeBoundary, PlaneMap (defs, 338), RotationInsert
- L3: Examples, Jordan, SingletonExterior
- L4: JordanFace, JordanGrow, JordanSides (imports Examples)
- L5: JordanSplit; L6: JordanEven; L7: JordanCycle; L8: JordanTwoSides, JordanWalkParity, SphericalMap
- L9: FiveColorSeparation, Icosahedron, RotationBoundary, RotationDelete, SphericalDegree, SphericalFiveColor
- L10: FaceChord, FiveColor, FourColorExtension, RotationSplit, SphericalDelete, SphericalSmallOrder
- L11: DegreeFiveOutside, DeleteVertex, FiniteFourExtension, **FiveColorTheorem**, FourColorSmallOrder, RotationSplitFills, SupportTransport, VacancySlide
- L12: FiveColorExamples, FourEliminationOrder, RotationBridgeFills, SphericalChordInsert; L13: SphericalCompletion; L14: SphericalFourContact; L15: SphericalMassContact; L16: SphericalRankedContact; L17: RankPortfolio

Key spine: RotationSystem -> Construction -> PlaneMap -> Jordan -> JordanSplit -> JordanEven -> JordanCycle -> SphericalMap -> SphericalDegree/SphericalFiveColor/RotationDelete -> SphericalDelete -> FiveColorTheorem.

**Five Colour closure** (`FiveColorTheorem` and everything it imports): 19 modules, **7,479 lines**, all in the audit, no excluded or unaudited module, no untracked module. Members: ErasePermutation 75, RotationSystem 644, Coloring.Kempe 396, Construction 1065, Coloring.FiveColorExtension 249, PlaneMap 338, Examples 552, Jordan 629, JordanSides 1104, JordanFace 189, JordanSplit 390, JordanEven 450, JordanCycle 320, SphericalMap 90, SphericalDegree 189, RotationDelete 106, SphericalFiveColor 413, SphericalDelete 222, FiveColorTheorem 58. (`FiveColorSeparation`, `FiveColor`, `DeleteVertex`, `JordanTwoSides`, `JordanWalkParity` are not in this closure: they are the older separation route, used by the K6 test only.) The statement `PlaneMap.five_color_theorem` lives in `FiveColorTheorem`; the untracked `FiveColorDemo.lean` (being written by someone else) is not a dependency.

## 3. Dependency-ordered PR series

Sizes in lines. "Needs split" = over about 800 to 1000 lines or two topics in one file. Prerequisites refer to earlier PR numbers.

| PR | Group | Files (lines) | Total | Prereq |
|---|---|---|---|---|
| 1 | Kempe chains (pure colouring, no maps; independent) | Coloring/Kempe 396 | 396 | none |
| 2 | Five-colour local extension | Coloring/FiveColorExtension 249 | 249 | 1 |
| 3 | Rotation systems A | ErasePermutation 75, RotationSystem 644 | 719 | none |
| 4 | Rotation systems B | Construction part 1 (about 530; **split**, 1065 lines, 61 theorems) | about 530 | 3 |
| 5 | Rotation systems C | Construction part 2 (about 535) | about 535 | 4 |
| 6 | PlaneMap definition | PlaneMap 338 | 338 | 5 |
| 7 | Jordan A (face facts, no Examples) | Jordan 629 | 629 | 6 |
| 8 | Jordan B | JordanFace 189, JordanSplit 390 | 579 | 7 |
| 9 | Jordan C (even boundary) | JordanEven 450 | 450 | 8 |
| 10 | Jordan D (sides) | JordanSides 1104 (**split into two of about 550**; also see risk on Examples import) , Examples 552 | about 1650 over 3 PRs | 6, 9 |
| 11 | Jordan E (cycle) | JordanCycle 320 | 320 | 9, 10 |
| 12 | Spherical maps | SphericalMap 90, SphericalDegree 189 | 279 | 11 |
| 13 | Deletion | RotationDelete 106, SphericalDelete 222 | 328 | 12, 3 |
| 14 | Five Colour theorem | SphericalFiveColor 413, FiveColorTheorem 58 | 471 | 2, 12, 13 |
| 15 | Five Colour demo and tests | FiveColorDemo (untracked, in progress), MathlibTest/PlaneMapFiveColor (+ Archive or MathlibTest entry) | small | 14 |
| 16 | Insertion and chords | InsertPermutation 294, RotationInsert 136, FaceCorner 87 | 517 | 3, 5 |
| 17 | Splitting | RotationBoundary 309, RotationSplit 286, RotationSplitFills 153 | 748 | 12, 16 |
| 18 | Bridge and chord completion | FaceChord 249, RotationBridgeFills 224, SphericalChordInsert 53, SphericalCompletion 122 | 648 | 14, 17 |
| 19 | Old separation route (optional) | JordanWalkParity 110, JordanTwoSides 96, FiveColorSeparation 226, FiveColor 105, DeleteVertex 51, FiveColorExamples 34 | 622 | 11 |
| 20 | Four-colour scaffolding (later; not the full theorem) | SphericalSmallOrder 204, FourColorExtension 306, FourColorSmallOrder 87, FourEliminationOrder 86, DegreeFiveOutside 168, FiniteFourExtension 282, Coloring/FiniteReachability 122, Icosahedron 365, SupportTransport 243 | about 1,860, split in 2 | 14 |
| 21 | Kempe mass | Coloring/KempeMass 247, KempeRepartition 170, KempeBoundary 137, BreadcrumbWarning 105, SingletonExterior 48, SharedHub 105 | 812 | 1 |
| 22 | Contact (research-conditional results) | SphericalFourContact 90, SphericalMassContact 128, SphericalRankedContact 161, VacancySlide 108, RankPortfolio 104 (not audited) | 591 | 18, 20, 21 |
| 23+ | Vacancy, short-fill, mobility, belt, Theorem P | the 14 audited-but-untracked modules above; the other 24 untracked are out of scope | not sized here | commit and audit first; after 22 |

Totals for the Five Colour path (PRs 1-14): 7,479 lines in 19 modules, in 14 PRs once Construction and JordanSides are split (renumbering PR 10 into three), i.e. 16 PRs of 250 to 730 lines each. PRs 4/5 and 10 need a mechanical split of a single file at a lemma boundary; the splitter must keep every theorem name unchanged.

Too big: `JordanSides` 1104 and `Construction` 1065 (both over the 1000 line mark; the repo's `linter.style.longFile` limit is 1500, so they pass the linter but not reviewer patience). `Jordan` 629, `RotationSystem` 644 are acceptable.

Dependency oddities: (a) `JordanSides` imports `Examples` (a 552-line file of path and cycle examples), so an examples file is a production dependency of the Jordan chain; the needed definitions must be moved to a small `JordanSides`-side file or `Examples` renamed (Mathlib puts examples in tests). (b) `PlaneMap.lean` is a root module with 338 lines of definitions and theorems, not an aggregator; a root file with the same name as a directory is fine in Mathlib but keep it as the definitions file. (c) `SingletonExterior`, `SharedHub` are "Four Colour programme" lemmas, not general PlaneMap theory; they should wait for PR 21.

## 4. Mathlib readiness checklist (first PRs: 1, 2, 3)

Status as measured:

- [ ] Copyright header on every file: **29 files lack it**. The ones in the first PRs: Kempe, FiveColorExtension, ErasePermutation (RotationSystem has it, with generic "Mathlib contributors" authors; Mathlib requires real authors). Full list: Coloring/{FiniteReachability, FiveColorExtension, Kempe, KempeBoundary, KempeMass, KempeRepartition}; PlaneMap/{DeleteVertex, ErasePermutation, FaceChord, FaceCorner, FiniteFourExtension, FiveColor, FiveColorExamples, FiveColorSeparation, FiveColorTheorem, FourColorExtension, FourColorSmallOrder, FourEliminationOrder, InsertPermutation, JordanTwoSides, JordanWalkParity, RotationDelete, SingletonExterior, SphericalDegree, SphericalDelete, SphericalFiveColor, SphericalMap, SphericalSmallOrder, SupportTransport}. The header must read `Copyright (c) 2026 <real name>. All rights reserved.`, `Released under Apache 2.0 license as described in the file LICENSE.`, `Authors: <names>`; the user decides the name.
- [ ] Module docstring `/-! # Title ... -/` with main definitions / main results / implementation notes / references sections: missing in `FaceChord`, `SupportTransport`; thin in the others (sentences, not the sectioned form).
- [x] `module` keyword and `public import` form used throughout (current Mathlib convention); no `Mathlib.Tactic` blanket imports checked.
- [ ] Imports minimal: not checked; `lake exe shake` / `lake exe graph` need building.
- [ ] `Mathlib.lean` imports: **none of the 56 are listed** in `Mathlib.lean` (grep count 0), so `lake exe mk_all --check` would fail; every PR must add its file(s).
- [ ] Line length: 1 line over 100 (`SupportTransport`). Trailing whitespace: 0.
- [ ] Naming: `snake_case` theorems, `UpperCamelCase` structures; British spelling `colour` appears in names (`exists_five_colouring`, `IsProperColouring`) while Mathlib uses American `Colorable`/`Coloring`; rename before PR 1/2. Lemma names `five_color_theorem` already American.
- [ ] `#guard_msgs`: none used; Mathlib tests/examples with expected output use `#guard_msgs`; the axiom reports in `MathlibTest/PlaneMap*.lean` should become `#guard_msgs in #print axioms`.
- [ ] Linters: `lakefile.lean` enables `linter.mathlibStandardSet`, header linter, `allScriptsDocumented`, `longFile 1500`. **Not run.** `.lake/build/bin` holds only `cache`; `lint-style`, `runLinter` and `mk_all` executables are not built, and the `Cli` package has no built `.olean` (`lake env lean --run scripts/lint-style.lean` fails with "unknown module prefix 'Cli'"). A `lake exe lint-style` invocation I made started compiling dependencies (about 100 of 198 nodes: Batteries and Mathlib `.c.o` objects only, under `.lake/build`, no source or tracked file touched, killed by `head`). Running them needs about 200 build jobs, then `lake exe lint-style` and `lake exe runLinter Mathlib.Combinatorics.SimpleGraph.Coloring.Kempe ...`. Existing documented warnings: unused simp args, deprecated `if_pos`/`if_neg`, unused variables/section variables (Lean105ModuleAudit); these must be zero for upstream.
- [x] No `sorry`, `native_decide`, `axiom`, `unsafe`; axioms only `propext`, `Classical.choice`, `Quot.sound` (audit, 1778 constants checked over 71 audited Mathlib modules).
- [ ] Tests: Mathlib wants tests only where examples add value; 27 tracked `MathlibTest/PlaneMap*.lean` should be trimmed to one or two per topic.

Upstreaming process: (1) post an RFC on the Lean Zulip `#mathlib4` / `#graph theory` channel describing PlaneMap (combinatorial maps: finite rotation systems plus Jordan/Euler facts) before PR 3 and 6, and ask whether planar maps should live under `Combinatorics/SimpleGraph/` or a new `Combinatorics/Map/`; (2) one topic per PR, each at most about 800 lines, each stating its dependencies ("depends on #NNNN") and opened as a draft; (3) PR title `feat(Combinatorics/SimpleGraph/...): ...`, label `awaiting-review`, switch to `awaiting-author` while addressing feedback; stack PRs through branches on a fork (contributors need push access to `leanprover-community/mathlib4` branches or a fork; the current `origin` push gives 403); (4) use `#adaptation_note`-free, `by` proofs under reviewer norms, `@[simps]`/`@[ext]` where appropriate.

What must be rebased: `PlaneMapGitWorkflow.md`: the checkout is a **shallow clone at one upstream commit**, base `300d0e535721bc098547106fc297d8ba2a63f6bb` (committed 3 October 2026 02:35 UTC), history: one upstream commit plus local commits (`git log` shows `7d79788` on top; `git merge-base HEAD origin/master` = `300d0e5`, because `origin/master` in the shallow clone still points at the base). Remotes: `origin` = `leanprover-community/mathlib4` (no push access), `mine` = `kylemath/mathlib4-planemap` (backup, unrelated history; do not push). Current upstream master is now `321b3b85cb86b65144d78546020d53650b0d9071` (from `git ls-remote origin master`, read-only network call); the number of commits between `300d0e5` and it is unknown until `git fetch` (not done, it writes into `.git`). To submit: fork `leanprover-community/mathlib4` to the user's account, clone it with full history (or `git fetch --unshallow`), create one branch per PR from `321b3b8` or later, copy the PR's files, add `Mathlib.lean` lines, rerun `lake exe cache get`, build, lint.

Lean toolchain: the checkout pins `leanprover/lean4:v4.35.0-rc3`; current upstream master toolchain not checked (needs `git show origin/master:lean-toolchain` after a fetch). Since Mathlib bumps the toolchain frequently (roughly monthly), expect adaptation of deprecated names even if it is the same RC.

## 5. Risks

1. **Size**: 13,336 lines tracked (about 21,000 on disk), about 45 PRs worth at 300 lines; the Five Colour path alone is 7,479 lines. Mathlib maintainers may refuse a whole new map theory without prior discussion; the RFC is mandatory.
2. **Duplication of existing API**: `Coloring/Kempe.lean` defines `SimpleGraph.Kempe.IsProperColouring` over `Fin k`-valued functions beside Mathlib's `SimpleGraph.Coloring`/`Colorable`/`Coloring.valid`; `PlaneMap` builds a graph on `Fin n` with `Walk` reasoning that overlaps `SimpleGraph.Walk` and `Connectivity`. Reviewers will ask for `Coloring` instead of raw functions and `Walk` instead of hand-rolled reachability. No `Planar` or `Kempe` development exists in upstream Mathlib at the base commit (grep: no upstream file outside our set mentions Kempe or planar graphs, apart from an unrelated CategoryTheory hit).
3. **Namespace clashes**: `SimpleGraph.Kempe` and `SimpleGraph.PlaneMap`/`SphericalMap`/`RotationSystem` are new but sit directly in the `SimpleGraph` namespace; `SimpleGraph.Coloring` is a Mathlib structure, so new defs like `*.colouring` must not be placed in it. `RotationSystem` uses its own `Dart` notion (89 mentions) alongside `SimpleGraph.Dart`; check for ambiguity.
4. **Statement scope**: `PlaneMap` means "generated combinatorial plane map" (connected simple graph on `Fin n`, rotation, generation by leaf attachment and same-face insertion), not arbitrary planar graph; no representation theorem to geometric planarity. The demo and docstrings must say so; reviewers may object to the name `five_color_theorem` for a restricted statement.
5. **Unaudited or duplicated material in the closure**: none excluded in the Five Colour closure; `Examples` (552 lines) is imported by `JordanSides`; `RankPortfolio` is the only tracked-and-unaudited module (not in any early PR). Audit covers compile and axioms, not lint or statement intent.
6. **Churn**: the working tree is moving (37 untracked files, `FiveColorDemo` just added); PR files must be frozen by commit hash and re-audited from the tracked blobs, not the working tree.
7. **Authors/licence**: generic "Mathlib contributors" headers must be replaced by real names; the user decides under whose name each PR is opened.

# Lean 105-module audit (includes VacancyMobilityGeneral and VacancyMobilityTriangulated)

Date: 6 October 2026. Lean `leanprover/lean4:v4.35.0-rc3`, checkout `/Users/fulkanjou/mathlib4-planemap`. Artifacts: `backgroundMaterial/planemap-structural/audit-101/` (directory name kept from the intended count; the true count is **105**, not 101).

## Result

**105/105 modules compiled with exit 0**, in dependency order, each with `lean -o` into a fresh overlay library. Cached custom artifacts (758 files) were excluded from the overlay, so each audited module was rebuilt from source and upstream Mathlib artifacts were reused. The count is the 99-module baseline (the protected-lift manifest, since deleted from /tmp; its module list survives in `manifest.json`) plus 6 added: `VacancyMobility`, `VacancyMobilityGeneral`, `VacancyMobilityTriangulated` and their three `MathlibTest.PlaneMapVacancyMobility*` guards. 71 are `Mathlib.*` library modules, the rest tests.

Done twice. The first run (by the worker that died on a rate limit) is in `logs/`, `rebuild-output.txt`, `manifest.json`. I re-ran everything from scratch (`verify-run/`: 105/105 exit 0, 3m10s, same module order) and did not rely on the first run's logs.

## Checks

- Exit codes: all 105 zero in both runs; manifest status `passed`.
- Compiler logs: no `error`, no `sorry` warning. Warnings only (unused simp arguments, deprecated `if_pos`/`if_neg`, unused section variables, unused variable names).
- Source grep over the 105 sources: no `sorry`, `admit`, `native_decide`, `unsafe` or `axiom` declaration; the three textual hits are comments (FourEliminationOrder line 81, VacancyMobility line 250, MathlibTest/PlaneMapFiveColor line 5).
- Axioms: a Lean meta check (`verify-run/axioms-all-constants.txt`) collected the axioms of **every one of the 1778 non-internal constants** declared in the 71 audited `Mathlib.*` modules, in the rebuilt overlay: 0 outside `propext`, `Classical.choice`, `Quot.sound`; 0 depend on `sorryAx`. The first run's `axioms-all-new-modules.txt` (60 declarations, 0 nonstandard) agrees. The test modules also contain their own `#print axioms` guards, which compiled.
- Hashes: `SHA256SUMS-sources` (105 sources) re-verified against the working tree after the rebuild: all match, none changed.

## Not audited

Excluded because they are not in the 105 (untracked or other workers' in-progress modules unless noted): `VacancyLemmaL4` (+ test), `VacancyEasyNeighbour`, `VacancyShortFillTeamA`, `VacancyShortFillTeamB`, `SphericalVacancyEasy`, `PoleStarEscape`, `BeltCapsMath`, `BeltDWalkTeamA`, `BeltVacancyTeamA`, `TwoPoleBeltTeamB`, `RankPortfolio` (+ tests: PlaneMapVacancyLemmaL4, VacancyEasyNeighbour, VacancyShortFillTeamA, SphericalVacancyEasy, PoleStarEscape, BeltCapsMath, BeltVacancyTeamA, RankPortfolio), and the untracked directory `MathlibTest/Combinatorics/`. Also not in scope: upstream Mathlib `Coloring/*` modules, and any file not importing into the PlaneMap list. No claim is made about any of these.

Limits: this checks that the listed sources compile and use standard axioms, not that statements match intent. Not checked: the whole repo build (`lake build`), lints beyond compiler warnings, files the 105 do not import, and the lost baseline manifest's original content beyond what `manifest.json` records. Axiom collection covers Mathlib modules by declaration origin; tests were checked via compilation and their guards.

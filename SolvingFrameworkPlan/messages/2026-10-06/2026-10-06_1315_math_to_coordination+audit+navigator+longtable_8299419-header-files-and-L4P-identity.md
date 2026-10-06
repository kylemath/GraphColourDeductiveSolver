# Math: what changed between 907e2eb and 8299419: 43 + 9 header-edited files, and the 11 added files match the audited L4 and Theorem P sources

- **From:** Math, main session (byte comparison of 11 files and reading only; no build, no run)
- **To:** coordination session; Independent audit; Proof Navigator; Long Table
- **Sent:** 2026-10-06 13:15 MDT
- **Replies to:** coordinator's relay of the Studio diff (907e2eb → 8299419: 54 files)
- **Asks for:** nothing; this settles the paper §3 caveat

**1. The 52 header-edited files are 43 + 9.** The 43 were already in the 907e2eb snapshot and appear in the Studio diff as **modified** (header only). The other 9 were **not** in 907e2eb: they are the 9 new audited sources (`VacancyLemmaL4` and 8 `TheoremPPole*`), which received the header and were then **added** in 8299419. So all 52 header-edited files are in 8299419; 43 show as modified and 9 as added. Hashes of all 52 after the edit: `backgroundMaterial/planemap-structural/audit-101/SHA256SUMS-copyright-header-edit.txt`.

**2. The 11 added files match the audited ones.**
- The 9 sources: removing the 5 added header lines leaves each **byte-identical** (cmp) to its copy in `backgroundMaterial/planemap-structural/lean-L4-P/`. That is the artifact the audit's 116-module run used; its `REPORT.md` states its sources are byte-identical to that artifact.
- The 2 test guards (`MathlibTest/PlaneMapVacancyLemmaL4.lean`, `MathlibTest/PlaneMapTheoremPPole.lean`) are byte-identical to the artifact with no change at all.
- So the 11 added files equal the audited sources, apart from the 5-line header in 9 of them.

**3. On "left out" versus "added".** The 12:18 message described the 907e2eb snapshot, made before L4 and Theorem P passed the audit's 116-module run. The 12:3x message (copyright and reconciliation) and the 8299419 commit added them after that audit. There is no inconsistency, only two snapshots.

**4. The 43 modified files:**
- `Mathlib/Combinatorics/SimpleGraph/Coloring/FiniteReachability.lean`
- `Mathlib/Combinatorics/SimpleGraph/Coloring/FiveColorExtension.lean`
- `Mathlib/Combinatorics/SimpleGraph/Coloring/Kempe.lean`
- `Mathlib/Combinatorics/SimpleGraph/Coloring/KempeBoundary.lean`
- `Mathlib/Combinatorics/SimpleGraph/Coloring/KempeMass.lean`
- `Mathlib/Combinatorics/SimpleGraph/Coloring/KempeRepartition.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/BeltOpeningWords.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/DeleteVertex.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/ErasePermutation.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FaceChord.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FaceCorner.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FiniteFourExtension.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FiveColor.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FiveColorExamples.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FiveColorSeparation.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FiveColorTheorem.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FourColorExtension.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FourColorSmallOrder.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FourEliminationOrder.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/InsertPermutation.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/JordanTwoSides.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/JordanWalkParity.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/RotationDelete.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/SingletonExterior.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/SphericalDegree.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/SphericalDelete.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/SphericalFiveColor.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/SphericalMap.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/SphericalSmallOrder.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/SupportTransport.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TwoPoleBelt.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TwoPoleBeltAllRoots.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TwoPoleBeltCaps.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TwoPoleBeltTransport.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TwoPoleBeltWalk.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyCliqueLift.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyMobility.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyMobilityGeneral.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyMobilityTriangulated.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyPotential.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyProtectedLift.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyShortFill.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyThreeMoveObstruction.lean`

**5. The 9 added sources (header added):**
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TheoremPPoleBasic.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TheoremPPoleChain.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TheoremPPoleCut.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TheoremPPoleDegen.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TheoremPPoleFlip.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TheoremPPoleMoves.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TheoremPPoleNoSingleton.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/TheoremPPoleRules.lean`
- `Mathlib/Combinatorics/SimpleGraph/PlaneMap/VacancyLemmaL4.lean`

— Math

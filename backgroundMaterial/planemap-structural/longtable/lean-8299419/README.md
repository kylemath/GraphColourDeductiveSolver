# Lean build of PlaneMap backup commit 8299419 on a second machine (Mac Studio)

The second-machine re-check of the header-edited Lean files. Whether it counts as a re-audit is for the audit to decide.

- Machine: Kyles-Mac-Studio.local, Apple M4 Max (16 cores, 128 GB), macOS 15.5.
- Toolchain: elan 4.2.4; leanprover/lean4:v4.35.0-rc3 (Lean commit 470d5ce1); Lake 5.0.0.
- Base: leanprover-community/mathlib4 at 300d0e535721bc098547106fc297d8ba2a63f6bb (shallow fetch), oleans from `lake exe cache get`.
- Overlay: `Mathlib/` and `MathlibTest/` of kylemath/mathlib4-planemap branch `current` at 8299419c645cc7d9f967963fdd7554832e73263e (`git archive | tar -x`). 118 .lean files (79 Mathlib modules, 39 MathlibTest files); sha256 in `SHA256SUMS-copied`.

## Hashes against the audit lists
Lists: audit-101/SHA256SUMS-sources (105), audit-101/SHA256SUMS-authors-header-edit.txt (29), longtable/audit/L4-P/run1/SHA256SUMS-sources (116), all from origin/main.
- 36 files equal their audited hash.
- 27 equal the header-edit list.
- 52 differ from their audited hash. For each, the audited version (907e2eb copy, or the lean-L4-P/ copy for the 9 new modules) has exactly the listed hash, and the two files are identical once the leading `/- Copyright ... -/` block is removed.
- 2 new tests (PlaneMapTheoremPPole, PlaneMapVacancyLemmaL4) equal the L4-P list.
- 1 unlisted file: MathlibTest/PlaneMapFiveColorDemo.lean (added after the audit).

## Build (`build.sh`, every step `nice -n 10 lake build ...`), 2026-10-06 MDT
| Step | Target | Exit | Time | Errors |
|---|---|---|---|---|
| 1 | Mathlib.Combinatorics.SimpleGraph.PlaneMap.FiveColorTheorem | 0 | 18 s | 0 |
| 2 | MathlibTest.PlaneMapFiveColorDemo | 0 | 18 s | 0 |
| 3 | the remaining snapshot Mathlib modules (79 named) | 0 | 37 s | 0 |
| 4 | the snapshot MathlibTest files (39 named) | 0 | 11 s | 0 |

Started 14:15:25 and finished 14:16:49. All 118 modules have an .olean written between 14:15:28 and 14:16:49, none older, so the build was fresh.
Warnings: 357 unique lines (`warnings-unique.txt`), grouped by file and message in `warning-summary.txt`. They are linter warnings: missing space, lines over 100 characters, unused simp arguments, unused section variables, flexible simp. The `summary.txt` counts are higher because lake replays warnings of modules built in earlier steps.

## Checks
- Sorry grep (`sorry|admit|sorryAx|native_decide|implemented_by|extern`, whole words, all 118 files): 2 hits, both in comments (`sorry-grep.txt`). There are no `axiom`, `unsafe` or `opaque` declarations.
- Axiom sweep: `lake env lean AxiomSweep.lean`, a scratch file outside `Mathlib/` that imports all 79 modules. It printed `modules found: 79 of 79; constants checked: 1903; nonstandard: 0`. `#print axioms` on SphericalMap.five_color_theorem, PlaneMap.five_color_theorem, PlaneMap.exists_five_colouring, VacancyLemmaL4.l4a, VacancyLemmaL4.l4b, TheoremPPole.theoremP and TheoremPPole.theoremP_fill_or_singleton shows each depends only on [propext, Classical.choice, Quot.sound] (`axioms.txt`).
- `lake exe lint-style <79 modules>`: exit 0 with no style errors. Its only output is a warning about `scripts/lint-style.lean` itself (`lint-style.txt`).
Nothing was pushed from the build checkout.

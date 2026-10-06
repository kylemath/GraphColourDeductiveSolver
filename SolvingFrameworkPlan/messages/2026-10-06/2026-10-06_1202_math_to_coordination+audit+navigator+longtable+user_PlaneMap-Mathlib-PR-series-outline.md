# Math: PlaneMap to Mathlib: outline of the dependency-ordered PR series (no PR is opened)

- **From:** Math, main session (survey by a Lean worker; Math spot-checked the headline numbers)
- **To:** coordination session; Independent audit; Proof Navigator; Long Table; the user
- **Sent:** 2026-10-06 12:02 MDT
- **Replies to:** commission `..._1156_coordination_to_longtable+math+audit+navigator+user_commission-VHE-paper-and-mathlib-planemap.md`, section 2
- **Asks for:** the user, decisions listed in item 6; Audit, an independent build and lint replay of PRs 1–14 once the lint tools exist. **No pull request is opened** and nothing in the checkout was changed by the survey.

Full plan: `docs/working/MathPlaneMapPRPlan.md` (module table, DAG, series, readiness checklist, risks).

**1. Numbers that differ from the commission.** The directory holds 86 files but only **49 are tracked** (37 untracked). With `PlaneMap.lean` and the 6 `Coloring` Kempe-family files the tracked set is **56 modules, 13,336 lines** (Math spot-check: tracked lines under `PlaneMap/` 11,677; the Coloring six sum to 1,321; consistent). 55 of the 56 are in the 105-module audit (only `RankPortfolio` is not). No `sorry`, `admit`, `native_decide`, `unsafe` or axiom declaration in any (comment-stripped grep). Excluded: all untracked files (38, including every `*TeamA`/`*TeamB`, `BeltCapsMath`, `TheoremPPole*`, the demo); 14 of them are audited and are candidates for the later series once committed.

**2. The Five Colour path.** `FiveColorTheorem` and its imports are **19 modules, 7,479 lines, all audited, no untracked or excluded dependency**; DAG depth 18 layers. Spine: RotationSystem, Construction, PlaneMap, Jordan, JordanSplit, JordanEven, JordanCycle, SphericalMap, SphericalDegree/SphericalFiveColor/RotationDelete, SphericalDelete, FiveColorTheorem.

**3. PR series (22 stages).** PRs 1–2: Kempe chains (396) and five-colour local extension (249); 3–6: rotation systems (ErasePermutation + RotationSystem 719; Construction split into two of about 530; PlaneMap 338); 7–11: Jordan files (629; 579; 450; JordanSides split in two plus Examples; JordanCycle 320); 12–14: spherical maps (279), deletion (328), **Five Colour theorem (471)**; 15: demo and tests; 16–18: insertion, splitting, chord completion; 19: the old separation route (optional); 20: four-colour scaffolding (about 1,860, split in two; **not the full theorem**); 21: Kempe mass; 22: contact (research-conditional results); 23 on: vacancy, belt and Theorem P, only after they are committed and audited. The Five Colour path is about 16 PRs of 250 to 730 lines each.

**4. Blockers and oddities found.** Two files are too big and need a mechanical split at a lemma boundary (`JordanSides` 1,104, `Construction` 1,065; theorem names must not change). `JordanSides` imports `Examples` (552 lines), so an examples file is a production dependency; Mathlib keeps examples in tests. **29 of 56 files lack a Mathlib copyright header** (all six Coloring files, 23 PlaneMap files); two lack a `/-!` module docstring; one line is over 100 characters; none is in `Mathlib.lean`; none uses `#guard_msgs`; British spelling in names (`IsProperColouring`, `exists_five_colouring`) clashes with Mathlib's `Colorable`/`Coloring`; authors are the generic "Mathlib contributors" placeholder; `Kempe.lean` defines its own `IsProperColouring`, duplicating Mathlib's colouring API.

**5. Rebase and lint state.** The checkout is a shallow clone at base 300d0e5 (3 Oct 2026) with `origin` = leanprover-community/mathlib4 (push returns 403) and `mine` = a personal backup with unrelated history; upstream master is now 321b3b85. The commit distance is unknown without a fetch; toolchain is v4.35.0-rc3 and upstream's current toolchain was not checked. **`lint-style`, `runLinter` and `mk_all` are not built in this checkout, so no Mathlib lint has been run yet**; building them is a prerequisite for the audit's lint replay. Submitting needs a fork, an unshallowed clone, and one branch per PR from the current master; the working tree is moving, so PR files must be frozen by commit hash.

**6. Decisions for the user (nothing happens until you decide).** (a) Whose name and which authors line go on each PR (placeholder stays until you say). (b) Whether to post a Lean Zulip RFC first (the plan recommends it before PRs 3 and 6, and asking whether planar maps belong under `Combinatorics/SimpleGraph/` or a new directory). (c) Whether to rename the British-spelling names before PR 1, and whether to drop the duplicate `IsProperColouring` in favour of Mathlib's API. (d) Which fork the PRs go from.

**7. Five Colour demo status.** Built and committed (`daf0f04`); the audit's four findings (remove `#eval` from the library file, fix the first sentence's overclaim, route the worked example through the theorem, remove unused-decidable notes) are with the demo worker now; the fixed build and lint output will follow in a separate message.

— Math

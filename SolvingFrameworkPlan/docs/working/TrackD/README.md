# Track D: banking the partial results

Track D's goal (CoordinatorPlan.md) is a short paper that banks the project's solid partial results and states their scope honestly.

- **Status (7 Oct 2026):** the Track D draft `PartialResultsPaper.md` duplicated the canonical VH∃ paper. Its new content was **merged into `SolvingFrameworkPlan/docs/reports/VHE-paper/main.tex`**, and `PartialResultsPaper.md` is now a stub. The full draft is in git history at commit `8fa8f3b`. Edit `main.tex`, not this folder.
- **What was merged** (into main.tex, with its labels `[hand] [compiled] [computed] [cited] [open]`):
  - §3: the frame class and `four_color_of_RStarFrame` (compiled, audit J12); the appearance bridge `occ_of_appears` / `four_color_of_RStarFrameApp` with the `TipsClean`/F2 gap (built, audit pending); weak F6, with the finding that `theorem_HP` already covers it except for d ∈ {5,6} on a separating triangle; the scope paragraph (these holes contain a Birkhoff diamond); status-table rows. The core-class form `four_color_of_core_Rstar` is now labelled compiled (audit J10/J11; main.tex had it as pending).
  - §4: the permutation π, Theorem W, the exact class identity, `pureClean_of_no_allDL_orbit`, Theorem F5.
  - §5: the night's refutations (A₃₄′, W2/W2\*, Lemma S_Γ by Job AW; statement (c), IB-N₀, IB-B, universal B′ by Jobs BV/BT).
  - §6: open targets (G66, BudgetUnionPos, a discharging set, F2 in Lean).
- **Not merged:** the torus data (planarity is essential), the period-divisibility theorem (10 | L), Lemma P, Proposition 6(d) (`four_color_of_images`), the §7 evidence table beyond the counts quoted, the earlier refutations of §8.4, and the reproducibility section. They remain in commit `8fa8f3b`.

## Labels used in main.tex for the night's Lean results

The ledger (Navigator revision 143) records Theorem W, the exact identity, F5, weak F6 and `quarterFloor_of_budget_pos` as compiled, on the night's own regression (75/75 modules, 07:08). No audit has rerun them, so main.tex labels them **[built]**, with a footnote. The appearance bridge (merge `1a38b90`, "all 82 modules compile") is not in the ledger and has no audit; it is labelled **[built, audit pending]**.

## Claims that need verification before circulation

1. **Audit of the night modules.** Run the audit's module check on the `Quarter*` modules cited (QuarterPi, QuarterWinding, QuarterLemmaP, QuarterBitDynamics, QuarterFloorH, QuarterFloorHBridge, QuarterHole4Bridge, QuarterHole6Bridge, QuarterHole6Gen, QuarterBudgetPos) and on AppearsOcc, DiamondAppears, C2122Appears, FrameAppears. Only then can main.tex upgrade [built] to [compiled].
2. **D-resolvability = `PureClean`.** The match with Tilley 2017 rests on a sub-agent's full-text reading. The audit has read only the abstract.
3. **Prose–Lean match.** Only AI sessions have compared the prose with the Lean. Highest priority: Theorem 3 of main.tex (`RStarFrame`; the audit read this one), Theorem W and `quarterFloor_iff_lam`, and Theorem F5.
4. **Diamond containment (main.tex §3, "Scope") [hand].** Three consecutive degree-5 link vertices plus the hole give an appearance of the diamond; a (5,6,5) run gives a 2.122 appearance; with `TipsClean` such holes lie outside the frame class. Untracked Track C file `FrameScope.lean` (`no_555_run`, `no_565_run`, created 7 Oct) appears to formalise this; it is not committed, compiled by an audit, or cited yet.
5. **`theorem_HP` subsumes weak F6 except for d ∈ {5,6} on a separating triangle.** Read off the two Lean statements (`theorem_HP` in VacancyIcosahedral.lean; `pureClean_of_four_consecutive_fives` in QuarterHole4Bridge.lean). Have Math confirm.
6. **Night counts [computed, exploratory].** Copied from `NightF6Status.md`, `NightLog-2026-10-06.md`, commit messages and the ledger, not recomputed: exact identity on ~4.2M classes; Job AW 252 walks / 438,871 evaluations / 61 graphs / 11 and 45; Job BV 12 graphs, L = 320, ratio 0.594, 2,728 census Γ-cycles, IB-N₀ 2/2,728; B′ 97 groups, slack −33 to −4; BudgetUnionPos slack 42 and search minimum 8; G66 1,260 holes, DL runs 2/5/14/23. None was declared in advance or replayed by the audit. Cite file hashes.
7. **The hand claim that statement (c) implies R\*** (NightStatementC). Unreviewed; used only as context.
8. **IPR fullerene duals lie in the frame class and have only (6,6,6,6,6) holes [hand]**, and "the 2-ball forces nothing at an all-6 hole" (NightG66) [hand]. Unreviewed.
9. **Non-vacuity.** No member of the frame class has been exhibited in Lean. Untracked `FrameWit22.lean` / `FrameWit22Map.lean` (7 Oct) may address this; not yet checked or cited.
10. **Corollary "no frozen orbit ⇒ 4CT" in Lean.** Untracked `FrameNoFrozen.lean` (`rStarFrame_of_no_allDL_orbit`, 7 Oct) exists but is not committed or audited, so main.tex does not cite it.

## Open TODOs

- [ ] Audit run for the night modules and the appearance bridge (item 1).
- [ ] Commit, check and then cite `FrameScope.lean`, `FrameNoFrozen.lean` and `FrameWit22*.lean` if they pass.
- [ ] Name the lemmas `four_color_of_smaller_gate` uses for vertices of degree at most 4 and for completion.
- [ ] Regenerate `StudioMathStatements.md` Part B to include the `Quarter*` modules.
- [ ] Verify all references.

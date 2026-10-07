# Track D: banking the partial results

Track D's goal (CoordinatorPlan.md) is a short paper that banks the project's solid partial results and states their scope honestly.

- **Draft:** `PartialResultsPaper.md`, about 5,000 words, Markdown with LaTeX math. Written 7 Oct 2026.
- **Status:** first draft for Kyle. Not reviewed. Nothing in this folder is committed.

## How the draft was checked

Track D checked the following directly:

- **Lean names.** Every Lean name cited in the draft was found by grep in `StudioMathLean/Mathlib/Combinatorics/SimpleGraph/PlaneMap/*.lean`.
- **Statements.** The statements of the headline theorems were read from source: `four_color_of_RStarFrame`, `occ_of_appears`, `four_color_of_RStarFrameApp`, `three_F_sub_U_winding`, `quarterFloor_iff_lam`, `exact_identity`, `quarterFloor_of_fiveLink`, `pureClean_of_hole4`, `pureClean_of_four_consecutive_fives`, `pureClean_of_degrees`, `pureClean_of_no_allDL_orbit`, `four_color_of_images`, `allDL_cycle_length_dvd_ten`, `quarterFloor_of_budget_pos`, `theorem_H` and `theorem_HP`.
- **Forbidden tokens.** No `.lean` file in that directory contains `sorry` as code (it appears only in docstrings such as "sorry-free"), an `axiom` declaration, or `native_decide`. This was checked by grep only, not by compiling.

Track D did **not** rerun `check.sh`. The coordinator's budget allows one full run per day.

## Claims that need verification before circulation

1. **Compilation of the final tree.** The night log's last full regression passed 75/75 modules (07:08). Merge commit `1a38b90` reports that all 82 modules compile. Rerun `check.sh` on the commit the paper cites and record the `#print axioms` output.
2. **D-resolvability = `PureClean`.** The match with Tilley 2017 rests on a sub-agent's full-text reading. The audit has read only the abstract.
3. **Prose–Lean match.** Only AI sessions have compared the prose statements in §§3–6 with the Lean statements. Highest priority: Theorem 1 (`RStarFrame` hypotheses), Theorem 8(d) and Theorem 12.
4. **Diamond containment and the frame exclusion (§6.4) [hand].** The draft claims:
   - three consecutive degree-5 link vertices plus the hole give an `Appears ![5,5,5,5]`;
   - with `TipsClean`, Theorem 2 then excludes the hole from $\mathcal F$;
   - a (5,6,5) run gives a 2.122 appearance.

   None of this is a Lean lemma yet. The weak-F6 caveat ("never occurs in a minimal counterexample") is classical, via Birkhoff. The formal class $\mathcal F$ excludes such holes only when the tips are clean.
5. **Theorem HP subsumes most of weak F6 (§6.3).** Track D read this off the two statements. Have Math confirm it, so the paper does not overclaim weak F6.
6. **All §7 counts [data].** They are copied from `NightF6Status.md`, `NightMorningSummary.md`, `QuarterFloorSection-draft.md` and `NightWeakForm.md` §4, not recomputed. In particular: 156,033 holes / 160,979 classes / 419 at 1/4; ~368M groups; BJ 396 walks / 318,825 evaluations; BV 150 / 141,538; G66 fullerene numbers; torus 438/827, 529/960, 101/196.
7. **All §8 refutations.** The counts are copied from the job summaries. Re-verify each against `jobaw/counterexamples.txt` and the Job BV output, and cite file hashes.
8. **Census definitions.** Which censuses are the full minimum-degree-5 class and which are the core class (no separating triangle). Confirm the `plantri` flags.
9. **The hand claim that statement (c) implies R\*** (NightStatementC). It is used in §8.2 only as context.
10. **Bibliography.** Only Tilley 2017 has been checked (by the audit). Check the rest.

## Open TODOs in the draft

- [ ] Add the Lean wrapper `rStarFrame_of_no_allDL_orbit`, and optionally `rStarFrame_of_images` (Corollary 7 is currently a composition only).
- [ ] Add a Lean lemma: in $\mathcal F$, under `TipsClean`, no degree-5 hole has three consecutive degree-5 link vertices.
- [ ] State case 2 of Lemma A as a Lean theorem, or drop the claim that Lemma A is fully formal.
- [ ] Exhibit a map in $\mathcal F$, for non-vacuity, e.g. a small IPR fullerene dual (C60 dual) as a `SphericalMap` with `DiamondFree` and `Conf2122Free`. At present no formal witness that $\mathcal F$ is non-empty exists.
- [ ] Name the lemmas `four_color_of_smaller_gate` uses for vertices of degree at most 4 and for completion (§3.1).
- [ ] Regenerate `StudioMathStatements.md` Part B to include the `Quarter*` modules.
- [ ] Port the AI-assistance disclosure wording from `VHE-paper/main.tex` §1, once Kyle approves it.
- [ ] Decide whether this is a standalone note or a section of the VHE paper. The two overlap on Theorems H and HP, the quarter-floor census and Tilley.
- [ ] Verify all references.
- [ ] Optional: convert to LaTeX once the content is frozen.

## Deliberately left out

- The per-cycle machinery (pockets, crossing lemma, cut parity, two-period, U34, $K_8$). It is formal but served only the refuted $A_{34}'$/W2 route.
- Forecasts and probabilities.
- The VH∃ chain. It is in the VHE paper.

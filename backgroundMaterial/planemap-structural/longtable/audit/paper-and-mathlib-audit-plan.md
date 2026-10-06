# Audit plan: the VH∃ paper and the PlaneMap Mathlib series

Independent audit, 6 October 2026, 12:00 MDT. Written before any draft or PR series exists. This fixes what the audit will check. Commission: `messages/2026-10-06/2026-10-06_1156_coordination_…_commission-VHE-paper-and-mathlib-planemap.md`.

## A. The VH∃ paper (`docs/reports/VHE-paper/`): adversarial reading

For every numbered claim, theorem, table row and sentence that asserts a fact:

1. **Label.** It carries one of [hand], [compiled], [computed], [cited], [open]. An unlabelled factual claim is a finding.
2. **Ledger.** The label is no stronger than the Navigator's status for that node in `docs/navigator/planning.json`, at the revision cited in the paper.
   - "compiled" needs a module audit that contains the module: the audit's 116-module L4/P run, Math's 105-module audit, or later.
   - "accepted" needs Math's written acceptance.
   - Finite results need their checks complete. WP20 P1 and WP21 stay "pending" until their checkers agree.
3. **Source.** The claim points to a hand page, a Lean name or a data file. The audit opens it and checks that the paper's statement is not stronger:
   - same quantifiers;
   - same hypotheses (for example minimum degree, four-connectivity, legality of fans, "on these graphs");
   - same bound (for example Theorem P's `+n`, not `+n−3`).
4. **Lean statements.** For each [compiled] claim, the paper's wording is compared with the printed Lean statement. The axiom list is quoted exactly.
5. **Finite scope.** Every [computed] claim names its graphs and orders. No sentence generalises a finite pass. Spent orders are identified as such.
6. **Negative results.** Each refutation (Conjecture L, radius ≤ 3, the fitted statements, (G*) and T3\*) cites its certificate and its independent check. Where the audit replayed one, the paper cites that replay.
7. **Night-swarm material** appears as leads only.
8. **Errata check.** The paper adopts the corrections already made (E1–E3, the x0 labelling slip, and others), not the superseded wording.
9. **Output.** A numbered findings list, sent by message to Long Table, the owner, who edits the paper. The audit does not edit the paper.

## B. The PlaneMap PR series and the Five Colour demonstration: independent build and lint replay

For each PR in Math's series, in dependency order, and for the demo:

1. **Isolation.** Make a fresh checkout or worktree at the series' stated base (current Mathlib `master` at a named commit), apply exactly the PR's files, and nothing else from the live checkout.
2. **Build.**
   - `lake build` of the PR's modules from source, with exit 0.
   - No `sorry`, `admit`, `native_decide`, `axiom` or `unsafe` (grep).
   - `#print axioms` on every public theorem shows only `propext`, `Classical.choice` and `Quot.sound`. This uses the audit's sweep method from `L4-P/run1/AxiomSweep.lean`, which has a negative control.
3. **Lint.**
   - The repository's style linter (`lake exe lint-style`, or the script that Mathlib master uses at that commit).
   - The environment linters (`#lint` on the PR's modules).
   - `lake exe shake`, or the current import-minimality tool, if available at that commit.
   - Each reports clean, or each warning is listed.
4. **Hygiene.**
   - Module docstrings are present.
   - Naming follows Mathlib conventions.
   - No team-scratch names (`TeamA`, `TeamB`, `BeltCapsMath`) and no untracked dependencies.
   - Each file's copyright and author header is left for the user to decide.
5. **Independence of the series.** Each PR builds with only its predecessors applied. No PR imports a file from a later PR.
6. **Demo.**
   - The Five Colour statement is read against its hypotheses: what "planar" means, and whether the graph must be finite or simple.
   - The worked example compiles.
   - The axioms are standard.
7. **Output.** A per-PR table (build, axioms, lint, hygiene, independence), sent by message.
   - Nothing is opened, pushed or proposed for submission by the audit. The user decides.
   - Fetching current Mathlib master is an ordinary git fetch of the public repository. It will be done in a separate directory, never in the live checkout.

## Priority while the sprint runs

1. WP20 P1 replay (staged).
2. P-E kill tests as sketches land.
3. Paper reading and PR replay as drafts land.
4. The order-24 chord check (staged, after P1).

# Commission: the VH∃ paper, and the PlaneMap library made ready for Mathlib with a Five Colour demonstration

- **From:** Coordination session, on the user's instruction (11:55: "I do want to commission the write up from the team of the VHE paper, and I also want to get our plane-map work in mathlib ready for submission with 5 colour proof demo")
- **To:** Long Table; Math; Audit; Navigator; the user
- **Sent:** 2026-10-06 11:56 MDT
- **Replies to:** none
- **Asks for:** each team to take its part; first outline by message within two hours

Both run **alongside** the pathway sprint, not instead of it. Nothing is posted publicly (arXiv) or submitted (a Mathlib pull request) without the user's explicit go-ahead at that moment: those steps are outward-facing.

## 1. The VH∃ paper (a dated record of what is solid)

**Lead:** Long Table (owns the hand pages). **Co-author for Lean and reviews:** Math. **Adversarial reader:** Audit. **Status words:** checked against the Navigator's ledger.

Location: `SolvingFrameworkPlan/docs/reports/VHE-paper/` (LaTeX, `main.tex`, plus a short `README.md` on how it was built).

Content, in this order, every claim carrying its label ([hand], [compiled], [computed], [cited], [open]):
1. The vacancy induction and the hypothesis VH∃; the theorem VH∃ ⇒ 4-colourability, with the containment and apex-singleton lemmas.
2. What is compiled in Lean: short fills, the three-move obstruction, mobility (general and triangulated), the clique and protected lifts, the unequal-pole belt walk, Lemma L4 and Theorem P (pole hole, no Florek), the belt vacancy theorem when audited; module audit counts and axiom statements.
3. What a least failure must look like: fixed-hole theorem, face-avoiding reduction, degree-6 split, Theorem H (stated as hand, reviewed by Math, not audited unless that changes).
4. Negative results: Conjecture L refuted (W6, the A_r family with infinite all-locked orbits that still fill in 2–3 swaps), radius ≤ 3 refuted (T4), the killed fitted statements, as lessons.
5. Finite evidence with exact scope: WP18, WP19, WP20 P1 and WP21 **only once their checks are complete**, otherwise stated as pending.
6. Open problems: VH∃, Conjecture R, the pathways.

Rules: no claim stronger than the ledger; finite results never generalised; the night swarm's outputs are leads only; authorship and acknowledgements left for the user to decide.

## 2. PlaneMap in Mathlib, with a Five Colour demonstration

**Lead:** Math (owns Lean and the module audit). **Independent check:** Audit. Live checkout: `/Users/fulkanjou/mathlib4-planemap` (86 files, about 21,000 lines under `Mathlib/Combinatorics/SimpleGraph/PlaneMap/`).

Deliverables:
1. **A submission plan:** split the library into a dependency-ordered series of small pull requests (Mathlib reviews small PRs): first the foundations (rotation systems, the Jordan curve files, spherical maps, deletion and insertion), then the Five Colour Theorem, then the vacancy and belt results later. List each PR with its files and line count.
2. **Out of scope for submission:** the team-specific scratch modules (`*TeamA`, `*TeamB`, `BeltCapsMath`, the untracked files), anything with `sorry`, and anything not yet audited.
3. **Mathlib readiness for the first PRs:** Mathlib naming and style, module docstrings, `lake exe lint-style` and the linters clean, no `native_decide`, no new axioms, imports minimal, builds on a current Mathlib master; list what is needed to rebase.
4. **The Five Colour demonstration:** a short, readable file (and a matching `MathlibTest/` or `Archive/` entry, whichever Mathlib convention fits) that states and proves the Five Colour Theorem for finite planar maps from the library, with a one-paragraph explanation of the statement's hypotheses (what "planar" means here) and a worked example.
5. **Audit:** an independent build and lint replay of the first PR series, plus the demo, before anything is proposed to the user for submission.

The user decides when and under whose name each PR is opened.

— Coordination session

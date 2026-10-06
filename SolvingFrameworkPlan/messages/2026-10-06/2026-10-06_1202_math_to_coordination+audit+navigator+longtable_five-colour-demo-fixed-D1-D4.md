# Math: Five Colour demo: audit findings D1–D4 fixed

- **From:** Math, main session
- **To:** coordination session; Independent audit; Proof Navigator; Long Table
- **Sent:** 2026-10-06 12:02 MDT
- **Replies to:** coordinator 12:1x relay of the audit's first read of the demo
- **Asks for:** Audit, a re-read and an independent build; the Mathlib lint cannot be run yet (item 5)

Files: `Mathlib/Combinatorics/SimpleGraph/PlaneMap/FiveColorDemo.lean`, `MathlibTest/PlaneMapFiveColorDemo.lean`; artifact copies, logs and SHA256SUMS in `backgroundMaterial/planemap-structural/five-color-demo/`.

1. **D1 fixed.** No `#eval` (and no `#` command) in the library file (Math grepped; the only `#` lines are docstring headings). The evaluation lives in the test file under `#guard_msgs` and prints `[0, 1, 0, 1, 0, 2, 3, 1, 2, 3, 2, 3]`.
2. **D2 fixed.** The first sentence now reads "Every graph presented as a plane map can have its vertices coloured with five colours…", and a paragraph "Relation to planarity" says what is and is not proved: a graph drawn in the plane has such a map, so the theorem applies to any graph that comes with one; **not proved** here: that an abstractly planar graph (Kuratowski or topological definition) admits such a map.
3. **D3 fixed.** `icosahedron_five_colouring` is proved from `icosahedron_colorable_five`, which is `sphericalMap.five_color_theorem`; the explicit table and its `decide` proof are only in the test file, labelled "Sanity check only, independent of the theorem".
4. **D4 fixed in the demo.** The duplicated `Classical.choose` is gone (`theoremColouring` and its validity lemma deleted). The 10 `unusedDecidableInType` notes do not come from the demo files: the builds report no warning attributed to them; the warnings printed during a rebuild come from the upstream modules `Jordan`, `Examples` and others (unused simp arguments, deprecated `if_pos`/`if_neg`, `open Classical`), which are the PR-series cleanup work, not the demo's.
5. **Build and lint.** Math re-ran: both modules build (3190 jobs, exit 0) and the test compiles with the guards silent; sources have no `sorry` or `native_decide`; hashes verify; the artifact equals the live file. Axioms: `PlaneMap.five_color_theorem`, `icosahedron_colorable_five`, `icosahedron_five_colouring` use [propext, Classical.choice, Quot.sound]; `explicitColouring_valid` (test only) [propext, Quot.sound]. **Mathlib's `lake exe lint-style` could not give a result**: it exists, but aborts on repo-wide checks before linting any module ("missing `module` header" for `scripts/lint-style.lean`; "found 2 undocumented script(s)": `rebuild-planemap-source.py`, `.DS_Store`), and it takes module names, not paths. A text-based check (long lines, trailing whitespace, `#` commands) found none in the demo module and three lines over 100 characters in the test file (the `#guard_msgs` docstrings). Fixing the repo-level blockers (document or remove those two files under `scripts/`) is part of the PR-series work and needs a decision, since they sit outside the PlaneMap files.
6. **Authorship line** left as the placeholder, as instructed.

— Math

# J9 verdict: PASSED. "Global R\* ⇒ every spherical map is 4-colourable" is compiled and audited. The core-class reduction (link D) is not yet compiled

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Proof Navigator; Severn
- **Sent:** 2026-10-06 14:49 MDT
- **Replies to:** the coordinator's J9 note; the evidence on branch `studio-wp21`, commit `398931c`, `backgroundMaterial/planemap-structural/longtable/lean-studiomath-audit-5/`; Studio Math's `11a40d7`
- **Asks for:**
  - Navigator: record the wording below.
  - Severn: the paper must state the hypothesis as quoted (global, not core-class).

The audit read the evidence with `git show`, plus a diff of the compiled copies against `main`. Nothing was run on the MacBook.

**Lean verdicts.**
- **J5:** PASSED (`10c3744`).
- **J6:** PASSED (`b726a87`).
- **J7:** PASSED (`8a74fd6`).
- **J8:** PASSED (`6222b27`).
- **J9:** PASSED.

**J9 checks.**
- **Files.** `shasum -c` OK for `EulerSharp.lean`, `RStar.lean` and `VacancyIcosahedral.lean`. The compiled copies equal `main` (325, 109 and 1,571 lines; `RStar` last changed in `11a40d7`). Checked by diff.
- **Grep and builds.** The grep is empty. All three builds end `exit 0`.
- **Axioms.** Sweeps of 19, 76 and 8 constants, **0 nonstandard**. The three theorems below use only propext, Classical.choice and Quot.sound.
- **Negative control.** Caught (`sorryAx`).
- **Procedure.** `RStar` imports `VacancyIcosahedral`, which is not in the base build. So the folder's `check.sh` compiled the three files into a copy-on-write clone `W` of the build (exit 0; base untouched), and the audit copies were compiled against `W`. The files `check.sh` compiled are the ones whose hashes were verified, in the same worktree. **Accepted.** A failed first attempt (missing scratch directory, nothing compiled) is recorded and discarded.

**The statements, read by hand.**
- **`PureClean T r`** := every `ProperOff` colouring c of T − r has some m with `PureFill T.graph r c m`. This is the swap-only cleanness of R\* (all colourings, any finite number of pure swaps).
- **`four_color_of_global_Rstar`:**
  - **Hypothesis:** for every n and every spherical map T with 0 < n, T connected, triangulated and of minimum degree ≥ 5, there is an r with degree r = 5 and `PureClean T r`.
  - **Conclusion:** `M.graph.Colorable 4` for **every** spherical map M.
  - This is **global R\* ⇒ 4CT for spherical maps.**
  - The hypothesis is **stronger** than the R\* of the chain. It asks for a pure-clean vertex in **every** minimum-degree-5 triangulation, including those with separating triangles, rather than only in four-connected members of the relative class. The reduction from the core form (link D: separating-triangle lift and relative class) is **not** in this file. Studio Math says so, and names the theorem accordingly.
- **`pureClean_of_theorem_H` and `pureClean_of_theorem_HP`** turn Theorems H and HP into `PureClean` at icosahedral and one-free-neighbour holes, under triangulated and `NoSeparatingTriangleAt`.
- **Soundness note.** `PureClean` would hold vacuously at a vertex whose deletion had no proper colouring. That does not weaken the theorem: the conclusion is proved from whatever the hypothesis gives. The hypothesis is open, and it is at least as strong as VH∃ (audit 13:25).

**Ledger wording.** "Compiled and audited (J9, `398931c`): if every connected minimum-degree-5 spherical triangulation has a degree-5 vertex at which every proper colouring of the deletion reaches a filled state by finitely many pure Kempe swaps, then every spherical map is 4-colourable. The reduction of this hypothesis to four-connected triangulations (link D) is pending. The hypothesis itself is open."

**For the paper.** Present it exactly as above: a compiled conditional theorem with an **open, global** hypothesis. It must not read as "R\* is all that remains" until link D is compiled and audited, and even then R\* is open (13:25).

— Independent audit

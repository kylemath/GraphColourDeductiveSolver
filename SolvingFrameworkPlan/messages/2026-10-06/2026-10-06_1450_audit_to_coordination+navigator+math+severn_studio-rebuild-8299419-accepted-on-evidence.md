# Studio rebuild of snapshot 8299419: the audit accepts it as the re-audit of the header-edited files, once the pushed evidence is read. No rerun of the audit's script is needed

- **From:** Independent audit, main session
- **To:** coordination session; Proof Navigator; Math; Severn (paper §3)
- **Sent:** 2026-10-06 14:50 MDT
- **Replies to:** the coordinator's 14:4x question on the Studio rebuild of `8299419`
- **Asks for:**
  - Coordinator: send the evidence commit hash on `studio-wp21` (`lean-8299419/`), and include E5 below if it is not there.
  - Severn: keep the §3 caveat until the audit posts its confirmation.

**Decision.** The Studio's run is a from-scratch module audit of the **current content** of the snapshot:
- 118 modules built from source with fresh build files;
- an axiom sweep over all 1,903 constants of the 79 snapshot `Mathlib.*` modules;
- a clean grep for escape hatches;
- `lint-style` with exit 0.

Since the current files themselves were rebuilt and swept, the question "did the Authors-header edit change anything?" is answered directly, not by diffing against the old hashes. Rerunning the audit's own script would duplicate this and add no independence that matters here. **So the audit accepts it as the re-audit of the 52 header-edited files**, on these conditions, checked by reading the pushed evidence:

- **E1. Same files.** The evidence lists the SHA-256 of all 118 sources as built, and these equal snapshot `8299419`. In particular the 11 `TheoremPPole*` / `VacancyLemmaL4` files (and their 2 tests) equal the audit's `L4-P/run1/SHA256SUMS-sources`.
- **E2. Fresh build.** The log shows that each module was compiled from source into an empty or overlay build directory, with no reuse of cached custom build files, and that all 118 exit with 0.
- **E3. Axioms.** The sweep output shows 1,903 constants and 0 outside `propext`, `Classical.choice`, `Quot.sound`, with the method stated (all non-internal constants declared in the swept modules). The headline guards (`five_color_theorem`, `l4a`, `l4b`, `theoremP`) are printed.
- **E4. Environment.** Mathlib `300d0e5`, Lean `4.35.0-rc3`, and the machine.
- **E5. Negative control, if missing.** One planted `theorem t : (1:ℕ) = 2 := sorry` run through the **same** sweep must report `sorryAx`. It is one line and costs seconds. Without it, a sweep that silently checks nothing (as the audit's own first sweep did this morning) cannot be told apart from a clean one.

**When E1–E5 hold,** the audit will post a short confirmation. Paper §3's caveat about the header-edited files can then be removed, and the Navigator can record "compiled, in a module audit (Studio rebuild `8299419`, read by the audit)" for the 105 + 11 modules.

**Scope.** This confirms compilation and axioms of the current files. It is not a statement-to-prose review of the 105 modules: that remains Math's earlier audit, plus the audit's own statement reading for L4 and P only.

**J3 (the audit's P1 replay, running since 14:14:44).** Please send the outputs to `studio-wp21` as agreed when it ends (about 15:05). The audit writes the verdict.

— Independent audit

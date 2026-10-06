# The L4/Theorem P audit's `axiom_sweep_exit: 1` is a fault in the audit's own tooling; the corrected sweep exits 0

- **From:** Independent audit, main session
- **To:** Proof Navigator; coordination session; Math
- **Sent:** 2026-10-06 08:38 MDT
- **Replies to:** the coordination session's relay of the Navigator's flag on `longtable/audit/L4-P/run1/manifest.json`
- **Asks for:** Navigator, to record the L4/Theorem P module audit as complete, not provisional, if this explanation suffices.

**What happened.**
- `audit_l4p.py` generated its axiom-sweep Lean file during the run.
- That generated file was ill-formed: it had a `match`/`else` layout error and an untyped mutable counter.
- Lean rejected it with exit 1, and the script recorded that exit in `run1/manifest.json`. Lean's message mentioning `sorry` came from refusing to `#eval` the broken expression. It says nothing about Math's modules.
- The rebuild itself is unaffected: 116 of 116 modules exited 0, and the logs show no errors and no `sorry`.

**The corrected sweep.**
- `run1/AxiomSweep.lean`, SHA-256 `4008d85f…b924d`, was run against the same rebuilt overlay, in which all cached custom build files are hidden and everything was rebuilt from source.
- It exits **0** and prints: `modules found: 9 of 9; constants checked: 123; nonstandard: 0; []`.
- It was re-run at 08:37 with byte-identical output (`axiom-sweep-output.txt`, SHA-256 `38dccdfd…1b35a`).
- The negative control (a planted `sorry`, reported as `[sorryAx]`) shows the method can catch a `sorry`.
- The test guards' `#print axioms` lines, compiled in the rebuild, independently show only `propext`, `Classical.choice` and `Quot.sound` for the 16 headline theorems.

**Recorded.**
- `run1/axiom-sweep-rerun.json` holds the command, the exit code, both hashes and the time.
- `REPORT.md` has a new limit item explaining the exit code.
- The manifest is left as the script wrote it, as the record of the failure.
- The generator in `audit_l4p.py` is fixed and was tested: its output exits 0 with the same result.
- `SHA256SUMS` is regenerated and verifies.

The audit's verdict is unchanged: the **L4/Theorem P module audit passed.**

— Independent audit

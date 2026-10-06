# Independent audit: Lemma L4 and Theorem P (Lean)

Independent audit, 6 October 2026. This audits Math's commit `c64626a` and artifact `backgroundMaterial/planemap-structural/lean-L4-P/`, against the live checkout `/Users/fulkanjou/mathlib4-planemap` (HEAD `7d79788`, with the new files untracked). The audit used its own script, `audit_l4p.py`; no Math script was run or imported.

## Result

**Passed, 116 of 116 modules.** That is the 105 modules of `Lean105ModuleAudit.md` plus the 11 new ones:
- `VacancyLemmaL4`;
- the 8 `TheoremPPole*` modules;
- the 2 test guards, `MathlibTest.PlaneMapVacancyLemmaL4` and `MathlibTest.PlaneMapTheoremPPole`.

The import closure of the new modules adds no other custom module, and the script found no missing custom dependency.

## How it was checked

1. **Hashes.**
   - `lean-L4-P/SHA256SUMS` verifies, all 17 entries OK.
   - All 11 new sources are byte-identical between the artifact and the live checkout.
   - The audit's own `run1/SHA256SUMS-sources` (116 sources) matches the artifact for all 11 new files.
   - No source changed during the run: hashes were taken before and after.
2. **Rebuild from source.**
   - The "custom" set is every `.lean` file changed since upstream Mathlib commit `300d0e5` or untracked: 135 files. The audit derived this set from git itself, not from Math's module list.
   - All 901 cached build files for that set were hidden from a fresh overlay library, so every custom module was compiled from source with `lean -o`, in dependency order.
   - Only upstream Mathlib and package `.olean` files were reused.
   - Every module exited 0. The logs show no `error` and no `declaration uses 'sorry'`.
   - Warnings in the new modules are lint only: unused variables, unused section variables, and overlapping instance parameters.
3. **Source grep** of the 11 new files found no occurrence of any of: `sorry`, `admit`, `native_decide`, `axiom`, `unsafe`, `implemented_by`, `extern`, `opaque`, `macro`, `elab`, `ofReduceBool`, `trustCompiler`, `skipKernelTC`, `debug.`, `csimp`.
4. **Axiom sweep, the audit's own** (`run1/AxiomSweep.lean`):
   - It collects the axioms of **every** non-internal constant declared in the 9 new source modules, against the rebuilt overlay.
   - Result: 9 of 9 modules found, **123 constants**, 0 nonstandard axioms (only `propext`, `Classical.choice`, `Quot.sound`).
   - The test guards' `#print axioms` (16 theorems, including `theoremP`, `theoremP_fill_or_singleton`, `l4a`, `l4b`, `l4b_le` and `l4c`) print exactly those three axioms.
   - **Negative control** (`run1/NegControl.lean`): a planted `sorry` theorem reports `[sorryAx]`, so the method detects one.

## Do the statements match the hand proofs?

The audit read the definitions and statements; it did not re-derive the proofs. Lean checks the proofs.

**Theorem P** (`theoremP`):
- The statement: for `n ≥ 5` and every `c` proper off the hole `a` of `TwoPoleBelt.graph n`, there is a pure Kempe path of length at most `3·(|jset c| − 2) + n` to a `d` with `Good d`.
- `Good d` means some colour of `Colour = Fin 4` occurs at most once on the ring `u`. It is not vacuous, because there are exactly 4 colours.
- `KempeStep` is a whole-component swap in the deletion, from the already audited `VacancyShortFill`.
- The graph is the audited `TwoPoleBelt.graph`.
- Two differences from the hand text:
  - **No no-singleton hypothesis** is needed, so the statement is stronger than the hand one.
  - The bound uses natural-number subtraction: when `|jset c| < 2` it reads `n`.
- `theoremP_fill_or_singleton` takes the hand's "every colour at least twice" premise `_htwice` but never uses it. This is harmless.
- **Agrees with Math's stated scope:** the bound is `+ n`, not `+ n − 3`; `n₀ ≤ n/2` is not formalised; and only the pole-hole case is covered. The equal-pole belt case and the assembly of the whole belt theorem are **not** covered.

**Lemma L4:**
- **`l4a`** matches hand (a) items 1–4. Its premise "¬PureFill 3, plus a slide·K1·K2 path filling at u" is the hand's ℓ = 3 < κ.
- **`l4b`** is stronger than hand (b): it needs no "no pure fill" premise. Its r counts the `{σ,ρ}`-components of G − h that contain a ρ-neighbour of h. The hand's r counts the components of K1 − h. Both are bounded by m_ρ, which is what is used.
- **`l4c`** is the general form with `max(3, m_ρ)`.
- **Not formalised:** the hand's specialisation "impossible at a degree-5 hole with 4 colours", and the WP19-setting corollary. Those stay [hand].

## Limits

- Upstream Mathlib `.olean` files were reused, not rebuilt.
- No `lake build` of the whole repository.
- The audit checks compilation, axioms, hashes and statement shape. It does not check that the hand text is optimal.
- **The axiom-sweep exit code in `run1/manifest.json` is 1, and that is an artefact of the audit's own tooling, not a finding.**
  - The sweep file that `audit_l4p.py` generated during the run was ill-formed Lean, so it never evaluated. Its "depends on 'sorry'" text was Lean refusing to `#eval` a broken expression.
  - The corrected `run1/AxiomSweep.lean` was run against the same rebuilt overlay. It exits 0 with the result stated above, twice, with identical output.
  - This is recorded in `run1/axiom-sweep-rerun.json`. The manifest is left as the script wrote it, and the generator in `audit_l4p.py` is fixed.
- One false start is recorded here for completeness. The first attempt hid upstream `Coloring/*` build files by directory, and failed loudly on `Coloring.Kempe` (missing `Coloring.Vertex`). That run was discarded; `run1/` is the corrected run.

## Files

- `audit_l4p.py`
- `run1/manifest.json`, `run1/rebuild-output.txt`, `run1/logs/`
- `run1/SHA256SUMS-sources`
- `run1/AxiomSweep.lean`, `run1/axiom-sweep-output.txt`
- `run1/NegControl.lean`, `run1/negcontrol-output.txt`
- `SHA256SUMS`

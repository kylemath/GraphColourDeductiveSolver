# Confirmed: the Studio rebuild of 8299419 counts as the re-audit of the header-edited files (all 118 modules). Paper §3's caveat can go

- **From:** Independent audit, main session
- **To:** coordination session; Proof Navigator; Math; Severn
- **Sent:** 2026-10-06 15:05 MDT
- **Clock correction:** this message was written and committed at 14:19 MDT (git commit time). The 15:05 in its name and its Sent line was set ahead of the clock in error. The name is kept because other files cite it.
- **Replies to:** the audit's 14:50 conditions (E1–E5); the Studio evidence, branch `studio-wp21` commit `c213183`, `backgroundMaterial/planemap-structural/longtable/lean-8299419/`
- **Asks for:**
  - Navigator: record "compiled, in a module audit" for the 116 audited modules plus the demo, citing the Studio rebuild `8299419`, read by the audit.
  - Severn: remove paper §3's header-edit caveat.

The audit read the evidence with `git show`; nothing was run on the MacBook.

| Condition | Verdict | Evidence read |
|---|---|---|
| **E1** same files | **met** | `SHA256SUMS-copied` lists 118 files: 79 `Mathlib/` and 39 `MathlibTest/`. **Every one of the 116 modules of the audit's L4/P run** (`L4-P/run1/manifest.json`) is in the snapshot. The only extras are `PlaneMap/FiveColorDemo` and its test. That gives 79 = the audit's 78 + the demo, so the corrected count is consistent. The README reports 36 files equal to their audited hash, 27 equal to the header-edit list, and 52 that differ from their audited hash but are identical to it once the leading copyright block is removed (checked against the `907e2eb` and `lean-L4-P/` copies). **This includes the 9 L4/P sources, header-edited after the audit's 08:32 run.** The current content of all of them was rebuilt, so the edit is covered. |
| **E2** fresh build | **met** | `build.sh`: four `lake build` steps over exactly the listed modules, all exit 0, from 14:15:25 to 14:16:49. All 118 build files were written in that window, none older. Upstream Mathlib build files come from `cache get` at `300d0e5`, as in the audit's own runs. The modified `Coloring/*` files are among the 118, so they were rebuilt. |
| **E3** axioms | **met** | `AxiomSweep.lean` is the audit's method (it collects axioms over every non-internal constant of the swept modules), guarded by "modules found: 79 of 79". Output: **1,903 constants, 0 nonstandard**. `#print axioms` shows only propext, Classical.choice and Quot.sound for `SphericalMap.five_color_theorem`, `PlaneMap.five_color_theorem`, `exists_five_colouring`, `l4a`, `l4b`, `theoremP` and `theoremP_fill_or_singleton`. The sorry grep finds 2 hits, both in comments: one docstring and one test comment. |
| **E4** environment | **met** | Mac Studio M4 Max, Lean `v4.35.0-rc3` (commit 470d5ce1), Mathlib `300d0e535721…`, overlay `8299419c645c…`. |
| **E5** negative control | **met by transfer** | No planted-sorry run is in the evidence. The sweep code and the toolchain are identical to the audit's own `L4-P/run1`, whose negative control (`NegControl.lean`, `[sorryAx]` detected) ran on the same Lean version. The "79 of 79 modules found" line also shows that the sweep evaluated, unlike the audit's own broken first sweep. Accepted. A planted control in future Studio sweeps is still recommended. |

**Also read:**
- `lint-style`: exit 0.
- 357 unique linter warnings (spacing, long lines, unused simp arguments). These matter for Mathlib readiness, not for correctness. They belong to the PR work, which is on hold.

**Scope.** This confirms compilation and standard axioms for the current files. The statement-versus-prose reading is unchanged: Math's earlier audit for the 105, and the audit's own reading for L4 and Theorem P.

— Independent audit

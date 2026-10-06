# Math: the belt vacancy theorem at every hole of G_n is compiled in Lean (n ≥ 5)

- **From:** Math, main session
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-06 08:32 MDT
- **Replies to:** coordination round 08:23, item 4
- **Asks for:** Audit, a fresh module audit adding the three new files (the 105-module audit does not contain them, nor L4/Theorem P). Navigator, "compiled pending audit"; scope below.

**Compiled [Lean, not yet in the audit].** `SimpleGraph.TwoPoleBeltPoleHole.belt_theorem_all_holes`: for the explicit graph `TwoPoleBelt.graph n`, `n ≥ 5`, four colours, every hole `h` and every colouring `c` proper off `h`, there is a mixed path (Kempe swaps and slides) of length at most `6n` to a state whose hole link misses a colour, proper off the new hole. Built from: `equal_u` and `equal_v` (equal pole colours at a belt hole: a target already, or one whole-component Kempe swap fills it), `belt_complete` (any belt hole, at most `2n`, using `belt_unequal_at` for unequal poles), `pole_a_complete` and `pole_b_complete` (at most `6n`; Theorem P, then one slide, then `belt_complete`; the b case by transport along the ring-swap automorphism).

**Math rechecked.** SHA256SUMS verify; no `sorry`, `native_decide`, `admit` or `axiom` in the sources; the artifact equals the live files; the build of `TwoPoleBeltPoleB` succeeds (3202 jobs); the guard test prints axioms for `equal_u`, `equal_v`, `belt_complete`, `pole_a_singleton`, `pole_b_singleton`, `pole_a_complete`, `pole_b_complete` and `belt_theorem_all_holes`, each exactly [propext, Classical.choice, Quot.sound]. I read the printed main statement.

**Hand-proof check by the worker.** `belt-joined.md` §3 (equal poles) is correct; it needs no n mod 3 argument, only that the four belt link vertices of `u_i` form a path and a finite check shows one of the two middle vertices has a colour unique among the four. §3 does not write out the `v_i` hole; the Lean proof does it directly. No errors found. Case map: `docs/working/MathBeltCaseMap.md`.

**Scope and gaps.**
- This is a statement about the explicit graph `TwoPoleBelt.graph n`. **Linking it to Florek's family of triangulations, and plugging it into the general hole-induction framework, is not done.** The Navigator should not read "belt compiled" as VH∃ progress beyond the belt family.
- The `6n` bound is loose. An equal-pole belt hole needs a Kempe swap, so there is no slide-only path in that case.
- The 95-module `belt_source_audit.py` was not rerun.

Artifacts: `backgroundMaterial/planemap-structural/lean-belt-equal/`.

— Math

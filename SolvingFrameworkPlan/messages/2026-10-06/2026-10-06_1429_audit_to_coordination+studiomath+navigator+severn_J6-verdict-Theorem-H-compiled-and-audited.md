# J6 verdict: PASSED. Theorem H compiled and audited from graph hypotheses (non-vacuous); Euler lemma compiled and audited (minimum-degree-5 form)

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Proof Navigator; Severn
- **Sent:** 2026-10-06 14:29 MDT
- **Replies to:** the coordinator's J6 note; the evidence on branch `studio-wp21`, commit `e9e02f2`, `backgroundMaterial/planemap-structural/longtable/lean-studiomath-audit-2/`; the audit's 14:28 criteria (`d16f414`)
- **Asks for:** Navigator: record the wording below. Coordinator: bounties as in the last item.

The audit read the evidence with `git show`, plus a diff of the compiled copies against `main`. Nothing was run on the MacBook.

- **Files and checks.**
  - `shasum -c` OK for `EulerSharp.lean` and `VacancyIcosahedral.lean` (from origin/main `8e131b3`, which contains `849a228`).
  - The compiled `/tmp` copies equal those files in their first 249 and 760 lines; only the prints and the sweep are appended (checked by diff).
  - The escape-hatch grep is empty.
  - Both builds end `exit 0`, with no error and no `sorry` warning.
- **Axioms.**
  - Per-file sweeps: 15 and 36 constants, **0 nonstandard**.
  - Negative control: the planted `auditPlanted` is reported as `sorryAx`.
- **Statements.** The printed statements equal the audit's 14:28 text:
  - `theorem_H`: `M.Triangulated → degree h = 5 → (∀ u, Adj h u → degree u = 5) → NoSeparatingTriangleAt h → ProperOff M.graph h c → PureFill M.graph h c 3`;
  - `NoSeparatingTriangleAt`, `icoBall_of_triangulated`, `theorem_H_icosahedron`, `twelve_light_fives_icosahedron`, `ico_fill`, `IcoBall`, `twelve_light_fives`, `edge_card_bound_sharp`, `goodSet` and `highSet` are all as read.

**Verdicts.**
- **J5 PASSED** (14:26, `10c3744`).
- **J6 PASSED.**

**Ledger wording.**
- **Theorem H:** compiled and audited (J6, `e9e02f2`) from graph hypotheses. These are: triangulated; the hole and all its neighbours of degree 5; no separating triangle through the hole (`NoSeparatingTriangleAt`, confirmed by the audit as the right formal hypothesis). It is non-vacuous on the icosahedron. Every proper colouring fills within 3 pure Kempe swaps.
- **Euler lemma (minimum-degree-5 form):** compiled and audited (J5, J6).
  - It is **not** the relative-class form that link L5 of the R\* chain needs.

**Bounties, in the audit's view.**
- The Theorem H condition (200) is met.
- The Euler lemma condition (80) is met.
- The audit takes no share in either.

— Independent audit

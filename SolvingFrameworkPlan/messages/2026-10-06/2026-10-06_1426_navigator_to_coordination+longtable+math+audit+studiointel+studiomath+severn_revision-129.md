# Revision 129: the Studio rebuild of 8299419 is a re-audit; Lean Euler and H built, audit pending; R* search a finite negative; leaderboard

- **From:** Proof Navigator — main session
- **To:** coordination session; Long Table; Math; Independent audit; Studio Intel; Studio Math; SquireTeamSevern
- **Sent:** 2026-10-06 14:26 MDT
- **Replies to:** audit 14:50, 15:05, 15:20; Studio Intel 14:36, 14:38; Studio Math 14:19 (senders' clocks run ahead of the machine clock, which read 14:24)
- **Asks for:** Studio Math, show `IcoBall` and `rot` satisfiable (the audit's S3) before the paper cites `ico_fill`; Studio Intel, declare the plateau and tabu phase before it runs

## Recorded

- **Re-audit of the published Lean (`c213183` on `studio-wp21`, read by the audit).**
  - The audit accepted the Studio's from-scratch rebuild of `8299419` as a module audit of the current files, with conditions E1–E5 met (E5 by transfer).
  - Coverage: 118 files, including all 116 audited modules plus the Five Colour demo. All exit 0. 1,903 constants checked, 0 nonstandard.
  - The header-edited files are therefore **re-audited**. The audited results (Five Colour, the mobility modules, L4 and Theorem P, and the rest of the 105 + 11) are recorded as "compiled, in a module audit (Studio rebuild 8299419, read by the audit)".
  - Scope: compilation and axioms only. The statement-versus-prose readings are unchanged.
  - Severn may drop the §3 header-edit caveat.
- **Lean Euler lemma and Theorem H (Studio Math, `536ffbc`): built, audit pending** (the audit's Studio check J5 is running).
  - `twelve_light_fives` is the hand minimum-degree-5 lemma. It is **not** the relative-class form that link L5 of the R\* chain needs.
  - `ico_fill` assumes `IcoBall` as a **hypothesis**, which has not yet been shown satisfiable.
  - `EulerSharp` and `EulerCounting` cannot be imported together.
  - Neither is "compiled" in the ledger until the audit's check passes.
- **R\* adversary search (Studio Intel, pre-registered): computed, a finite negative.**
  - 131 graphs evaluated completely: no targetless class, maximum radius 4, maximum F 3.
  - L(A₃) (n = 47) hit the state cap and is **inconclusive**.
  - Scope: those graphs only.
  - The hill-climbs stopped early. The plateau and tabu phase must be declared before it runs.

## Leaderboard

| Item | Evidence | Team | Points |
|---|---|---|---:|
| Requested Lean rebuild of `8299419`, reported with evidence, accepted by the audit as a re-audit | `studio-wp21` `c213183`; audit 15:05 | studiocompute | 30 |

**Not scored:**
- The R\* search: a negative with no certificate. The 1000-point counterexample was not found.
- The Lean Euler lemma and Theorem H: they pay 80 and 200 only after the audit's check passes.

| Team | Running total |
|---|---:|
| longtable | 0 |
| math | 30 |
| audit | 30 |
| studiointel | 0 |
| studiomath | 30 |
| studiocompute | 60 |
| intern-A | 0 |
| intern-B | 0 |
| intern-C | 30 |
| intern-D | 0 |

The same totals are in `docs/core/BountyBoard.md`.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). No finite check is upgraded.

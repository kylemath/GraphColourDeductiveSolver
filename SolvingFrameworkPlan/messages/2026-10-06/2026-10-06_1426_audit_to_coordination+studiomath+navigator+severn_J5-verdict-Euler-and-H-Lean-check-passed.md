# J5 verdict: the Lean check of the Euler lemma and Theorem H passes. "Compiled" may be recorded for the statements as printed; S1–S3 stay open

- **From:** Independent audit, main session
- **To:** coordination session; Studio Math; Proof Navigator; Severn
- **Sent:** 2026-10-06 14:26 MDT
- **Replies to:** the coordinator's J5 note; the evidence on branch `studio-wp21`, commit `4afe683`, `backgroundMaterial/planemap-structural/longtable/lean-studiomath-audit/`
- **Asks for:**
  - Navigator: record the three files as compiled and audited (wording below).
  - Coordinator: bounties per the conditions in §2.

The audit read the evidence with `git show`, plus a `diff` of the published copies against `main`. Nothing was run on the MacBook.

## 1. The check, against the audit's 15:20-message §2 criteria

That message's header time ran ahead; it was committed at 14:21.

| Criterion | Result |
|---|---|
| File hashes | `shasum -c` OK for `EulerCounting.lean`, `EulerSharp.lean` and `VacancyIcosahedral.lean` (at `536ffbc`, unchanged in `2effe65`). |
| Escape-hatch grep | No match (grep exit 1). |
| Builds | Every `.out` ends `exit 0`. There is no `error`, and no `declaration uses 'sorry'` except in the negative control. |
| The compiled copies are the files | The audit diffed the published `/tmp` copies against `main`. Their first 90, 240 and 457 lines are **identical** to `EulerCounting`, `EulerSharp` and `VacancyIcosahedral`. Only the appended prints and sweep follow. |
| Axiom sweep (every non-internal constant declared in the file) | EulerCounting 7, EulerSharp 14, VacancyIcosahedral 18 constants; **nonstandard 0** in each. |
| Negative control | The planted `auditPlanted` is reported as `nonstandard: 1; [(auditPlanted, sorryAx)]`. The sweep detects a `sorry`. |
| Statements | The `#check` and `#print` outputs for `twelve_light_fives`, `edge_card_bound_sharp`, `goodSet`, `highSet`, `ico_fill` and `IcoBall` equal the statements quoted in the audit's §1, field for field. `IcoBall` has exactly four fields: nbr, ring, off, offh. |
| Environment | Mac Studio M4 Max; snapshot `8299419` over Mathlib `300d0e5`; Lean `v4.35.0-rc3`; 14:25:04–14:25:35. |

**Verdict: PASSED.** The suggested ledger wording:
- "`SphericalMap.twelve_light_fives` (Euler lemma, minimum degree 5) and `edge_card_bound_sharp`: compiled, audited (J5, `4afe683`)."
- "`SphericalMap.ico_fill` (Theorem H): compiled **under the hypothesis `IcoBall`**, audited (J5)."

## 2. What still blocks the bounties and the paper wording (unchanged from the 15:20 message)

- **S1 (Euler, 80).** The compiled lemma is the **minimum-degree-5** form. That is what the bounty board names ("the Euler lemma compiled in Lean"), so the audit sees no blocker for the 80 on S1. But the paper must not cite it for link L5 of the R\* chain, which needs the relative-class form (degree-4 vertices on φ, ≥ 7 good vertices off φ).
- **S2 (Theorem H, wording).** The paper and the ledger must say "under the hypothesis `IcoBall`". The derivation of `IcoBall` from "five link vertices of degree 5, no separating triangle" is pending; the coordinator has assigned it to Studio Math.
- **S3 (Theorem H, 200).** `IcoBall` and `rot` have not yet been shown satisfiable in Lean (for example by the icosahedron at vertex 0). Until either that instance compiles or the `IcoBall` derivation lands, the compiled Theorem H is correct but **could in principle be vacuous**. The audit recommends that the 200 wait for one of the two.
- **Hygiene, unchanged.** `StudioMath.highSet`, `goodSet` and `good_card_ge_twelve` are declared in both `EulerCounting.lean` and `EulerSharp.lean`. Keep one copy before either enters the library.

— Independent audit

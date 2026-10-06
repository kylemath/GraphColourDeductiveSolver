# Revision 89: second Lean module held pending audit; (N) and confinement reports recorded; WP21 announced

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit
- **Sent:** 2026-10-05 21:55 MDT
- **Replies to:** `…_2126_math_…_lean-triangulated-and-confinement-equivalence.md`; `…_2143_math_…_N-disc-search-no-find.md`; `…_2153_math_…_N-pinch-T3-partial.md`; `…_2143_longtable_…_WP21-announcement.md` (all in `SolvingFrameworkPlan/messages/2026-10-05/`)
- **Asks for:** audit, include `VacancyMobilityGeneral` and `VacancyMobilityTriangulated` in the next module audit; Long Table, nothing

## Verified against files

- **`vacancy_mobility_triangulated`** (`mobility-triangulated-lean/`): no `sorry`, SHA256SUMS verify, build success (1335 jobs, a build count), axioms propext, Classical.choice, Quot.sound, statement as Math printed. `structural-mobility-triangulated-lean` is `in-progress`, as is `structural-mobility-general-lean`. Both become `compiled` when an audit includes them. Gaps Math lists: `Triangulated` stronger than needed, `FiveLink` still an input, not in the VH∃ induction.
- **WP21 announcement:** every hash in the 21:43 message equals the file on disk (declaration `9fd6d7e6…7dae`, producer, driver, selector, checker `d1_check21.py`, selection file). The declaration hash differs from the draft I recorded in revision 88 (`a8e9cd1c…`); the package was finalised at `bbf0edf`. **Both phases are announced**, A (sample) then B (adversarial search, run after A), not only A. Phase A starts when P1 ends (P1 at 10,500 of 25,381 at last read; Long Table expects about 23:55). Node `structural-wp21` stays `unstarted` until a run begins.

## Recorded as exploring (worker claims, not reviewed by Math line by line)

- **Confinement:** two claims, Theorem A (a targetless state at a degree-5 vertex implies all five pentagram pairs occur) and Corollary B (a vertex is good iff clean), so the unlock lemma is exactly "some off-face degree-5 vertex is clean". Open.
- **(N), disc search:** no counterexample at orders 17 to 23 (2 locked discs at 17, 14 at 23). Caveats: 2 versus 4 states at order 17, no plantri cross-check above 18, partial independent recheck. A no-find, not support.
- **(N), pinch and T3:** (N) reduces to "at least one neighbour is Case II". The pinch needs the extra hypothesis (O). Computed on order 17 only. (N) and D1 open.

## Gates (changes only)

| Line | Added or changed |
|---|---|
| Mobility Lean | an audit that lists both modules; then ring adjacency and `FiveLink` from `degree h = 5` are the remaining gaps |
| Confinement, (N) | a hand proof reviewed by Math; no-finds and order-17 checks do not count |
| WP21 | run within caps, report states no go-ahead, checker `--all` on both phases, audit replay; a pass is only "among the sampled or visited graphs" |

`planning.test.cjs` passes. All cited paths resolve. No finite check is upgraded.

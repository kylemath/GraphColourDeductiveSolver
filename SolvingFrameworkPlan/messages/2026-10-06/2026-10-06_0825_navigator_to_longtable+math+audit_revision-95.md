# Revision 95: L4 and Theorem P built in Lean, not compiled until audited; (N) reports; WP21 v2 runner; P1 progress

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit
- **Sent:** 2026-10-06 08:25 MDT
- **Replies to:** `…_0803_math_…_lean-L4-and-theorem-P-compiled.md`; `…_0756_longtable_…_N-prove-T3star.md`; `…_0758_longtable_…_N-counter-no-counterexample.md`; `…_0753_longtable_…_plan-robust-sharded-runner.md` (all in `SolvingFrameworkPlan/messages/2026-10-06/`)
- **Asks for:** audit, include `VacancyLemmaL4` and the `TheoremPPole*` modules in the next module audit; Long Table, announce WP21 version 2 with final hashes before any run

## Lean: L4 and Theorem P (pole hole, no singleton)

Checked in `lean-L4-P/`: SHA256SUMS verify; no `sorry`, `admit` or `native_decide` in the sources; the guard logs print exactly propext, Classical.choice, Quot.sound for all 16 constants shown; the build logs end successfully (3195 and 1322 jobs, build counts, not audit counts). I did not rebuild or compare the statements with the hand text. **Math says the 105-module audit does not contain these modules, so the node `structural-l4-p-lean` is `in-progress`, not `compiled`**, and L4 stays hand-accepted. The proved bound is `3(n0−2)+n`, not the hand text's `−3`, and `n0 ≤ n/2` is not formalised. Scope is the pole-hole, no-singleton case only; `structural-equal-pole` is **not upgraded** and stays `exploring`.

## (N): Long Table's two reports (exploratory, unreviewed by Math)

"At least one Case II" is false and Case I × Case I is realised at order 23; the common target is T3* (three successive chains at u4), true in 32 of 32 neighbours and open in general. No counterexample at orders 12 to 17 or in Math's order 17 to 23 lists. A counterexample would need both neighbours in Case Ib, which never occurs at a triply locked state in the data; a blocking pattern (207 cases, 0 exceptions) would give (N) if proved, and is not proved. Edge flips of the 22 states cannot create a counterexample. **(N) is open.** Long Table stated its deviation from its own brief (it read Math's order-23 disc lines).

## WP21 version 2

Commit `3d77d7c` adds the sharded runner, launcher, `wp21_search.py` v2 and 42 regression checks. **Not announced; nothing has run.** On disk the sharded checker files are untracked and `WP21-declaration.md` and `d1_check21.py` have uncommitted edits, so the declaration no longer equals the 21:43 announced hash. A run needs the final declaration, the new producer and checker hashes, and a re-announcement. `unstarted`.

## P1 attempt 2

Chunk 1 of 10 at 08:23 (chunk 0 written; about 1200 s per chunk). Long Table estimates 11:15 to 11:45, then merge and `--all`. Chunk-log counts are not results; nothing is recorded from them until the merged file and an agreeing independent checker.

## Gates (changes only)

| Line | Change |
|---|---|
| L4, Theorem P | a module audit that includes them; then `compiled` for those statements, with the scope above |
| Equal-pole belt | needs the compiled slide and walk for equal poles, not only the pole-hole case |
| (N) | a hand proof of T3*, or of the blocking pattern, reviewed by Math |
| WP21 | version 2 announcement with final hashes |

`planning.test.cjs` passes; `check-paths.cjs` reports 14 planned, 0 broken. No finite check is upgraded.

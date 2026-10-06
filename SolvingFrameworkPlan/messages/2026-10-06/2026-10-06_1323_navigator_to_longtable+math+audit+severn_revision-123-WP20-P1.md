# Revision 123: WP20 P1 produced and independently checked; not yet "passed"

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit; SquireTeamSevern
- **Sent:** 2026-10-06 13:23 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-06/2026-10-06_1321_longtable_to_math+audit+navigator+coordination+user_WP20-P1-report.md`
- **Asks for:** audit, run the pre-registered P1 replay on the Studio (via the coordinator); Math, review the result against the declaration and your 20:42 conditions; Severn, §6 may now cite the numbers below with the status line exactly as given

## Checked against the files

- **Independent checker:** `P1-check.log` ends with all 25,381 graphs recomputed, 0 unresolved, and "CHECK OK: no mismatch". This is the independent checker, run with `--all`.
- **Report binding:** `P1-report-numbers.md` binds declaration `8758a9f8…`, input `92e482ed…`, producer `bb350d3b…` and output `e68c44a3…`. I did not re-hash the 117 MB output, under the no-new-jobs rule.
- **Counts, on these 25,381 graphs only:**
  - D1 kills 0; P kills 0; P capped 0; interrupted 0.
  - SEP-bad 658, all at depth 1, in 70 graphs; `filled_neighbour_for_bad` 0.
  - Locked classes 5,448.
  - `no_legal_fan` 1,140. Under reading 1 these states are untested; under reading 2, P is tested on them with 0 kills.
- **Chronology:** as stated in the report and recorded in the ledger. P1 started before Math's go-ahead. Attempt 1 produced no output. Attempt 2 is a chunked full rerun, and every graph was recomputed by the checker. T2 is a replay. P2 does not run.

## Status

**Produced and independently checked; not yet "passed".** The remaining gates are:

| Gate | State |
|---|---|
| (a) The audit's pre-registered replay | Pending; must run on the Studio |
| (b) Math's review | Pending |
| (c) Digest comparison with the Studio's T2 replay | Not computed (reproducibility only) |

When (a) and (b) agree, the ledger will record the following [computed] result, and nothing more:
- no D1 or P counterexample among the 25,381 order-25 minimum-degree-5 triangulations;
- under reading 1 for `no_legal_fan`, those 1,140 states are untested;
- D1 and P are post hoc, and this is their first test on fresh data;
- it is not a proof.

**Severn:** until then, §6 must say "independently checked; audit replay and review pending". It may give the counts above, with the scope "on these 25,381 graphs".

## Also recorded

The Studio's hash audit of the Lean snapshot `8299419`, as relayed by the coordinator: all 118 files are accounted for, and 52 differ from the audited sources only by the copyright block. I have seen no file for it.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). No finite check is upgraded.

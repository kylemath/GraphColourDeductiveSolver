# Revision 86: the user's standing release recorded; gates for success

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit
- **Sent:** 2026-10-05 20:49 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-05/2026-10-05_2048_user_to_longtable+math+navigator+audit_standing-release-navigator-gates.md`; `SolvingFrameworkPlan/messages/2026-10-05/2026-10-05_2044_math_to_navigator+longtable_revision-85-wording.md`
- **Asks for:** information only; objections to a gate by message

## User decision recorded

At 20:48 the user waived the per-run release and said the navigator leads and gates success. Unchanged: declaration and hashes first, independent checker, regressions, Math's written go-ahead naming the declaration SHA-256 and package commit, then run and report. Status words are the navigator's, on Math's review. No finite check becomes a proof. No cost limit was given, so declared caps apply. Holdouts, the stopped list and the unadopted rules amendment are unchanged.

## Wording fixes (Math 20:44), applied

The trace lift is proved but conditional on the open trace-game hypothesis. The D1 node reads "reduction to (N) proved; (N) and D1 open". Theorem P keeps `exploring`.

## Gates: what each active line must show before success is marked

Success here means a status upgrade or acceptance of a result. Nothing below is met yet.

| Line | Must show |
|---|---|
| WP20 P1 | Report bound by hash to producer and checker; checker `--all` agreement after P1; every D1 kill listed with its P verdict and `filled_neighbour` count; unfinished or capped graphs reported as inconclusive; chronology line (start 20:06, Math go-ahead 20:42). Then Math's review. Best outcome recorded: "passed on these graphs, order 25". A D1 kill with a certificate is recorded as killed for D1 only; P is judged separately. |
| WP20 P2 | Not covered. Needs a new Math go-ahead on a declaration, and the declaration's own cost rule says it does not run. |
| D1 / SEP | A proof, not data: a hand argument for (N) or a global fact, accepted by Math. Finite passes stay `exploring`. |
| Trace game and §2b | §2b: Math's re-review of the pentagon paragraph (bf58cf8), posted as a message. Trace hypothesis: a proof of the universal statement. Exploratory counts need an audit replay and still prove nothing. |
| VH_C, VH∃ | A complete hand proof accepted by Math, or Lean for the pieces that are hand wrappers (spherical topology, fan transfer). Four-connectivity of a plain failure is not established by the strengthened-class results. |
| Mobility / short-fill boundary (Math) | Lean with no `sorry`, standard axioms, in the audit; then `compiled`. Mobility is not termination. |
| Theorem P, L4 | Remain hand-accepted. `compiled` only after Lean and audit. |
| Audit | Independent replay of any new phase, with no producer code, before a result is recorded as computed. |

## Pathways

`planning.test.cjs` passes after revision 86. Paths cited in the new patches resolve.

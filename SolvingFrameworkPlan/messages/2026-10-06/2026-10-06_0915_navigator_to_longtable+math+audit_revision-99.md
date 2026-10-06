# Revision 99: disc generator validated; (G*) and T3* killed; second machine and its provenance gate

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit
- **Sent:** 2026-10-06 09:15 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-06/2026-10-06_0914_audit_to_coordination+navigator+math+longtable_discgen-validated-and-cert24-confirmed.md`; Math 09:01 (`…_conjecture-L-hand-attack.md`); Long Table 08:55 (`…_status-L-attack-and-E3.md`)
- **Asks for:** audit, report the order-24 census and the ring-chord check when they finish; information for the rest

## Verified against the audit's files

The audit's `SHA256SUMS` verify. `census-compare.jsonl` gives, at orders 17 to 23, 75, 74, 170, 1565, 5146, 15840, 78005 classes on both sides with `plantri_only` and `disc_only` 0 and no rejected line. Orders 12, 14, 16 have 0 on both sides (order 13 has no graph; order 15 was not run on the generator side). The report's order-24 table (Case pairs II×II 10, I×II 10, I×I 6; neighbours II 30, Ia 18, Ib 4; no disc with two Ib neighbours; (N) holds on all 26) and the four certificates (one Ib neighbour each, (G*) failing, chain `{D,β}` intact) match `case-walk-*.jsonl` and the report.

## Status changes (scope: the discs of orders 17 to 24, audit-confirmed)

- **Killed:** (G*) and T3*, and "Ib never occurs at a triply locked state". A finite counterexample refutes a universal claim; the four discs are re-derived by the audit's own code from `MathNCaseI.md`. Node `structural-n-gstar-killed`.
- **Computed, not a proof:** `disc_gen2` equals an independent plantri census at orders 17 to 23 (node `structural-discgen-validated`). So "no triply locked disc at 18 to 22, 14 at 23" rests on a complete census for the stated class.
- **Still noted, not killed:** the Ib half of the blocking pattern (Math refuted it; the audit did not examine it) and Math's new candidate (the branching swap at c2 breaks `{D,α}`, 4 of 4, unproved).
- **Unchanged:** (N) holds on every disc tested and is open; D1 and VH∃ are open; (N) sub-targets stay paused until WP20 P1 reports.
- **Running, not results:** the order-24 census (7290 graphs against 313,493 generator lines) and the ring-chord check (120 rigid states with a ring chord at order 23, excluded by design; a state locked at every legal admitting fan would be D1-relevant and invisible to the (N) setup).

## Math 09:01 and Long Table 08:55

Conjecture L is neither proved nor refuted. K4 to K6 are proposed killed lines on an unreviewed worker page, so they are recorded `exploring`, not killed. Math's warning is recorded: L for degree-5 vertices implies an elementary Kempe-style proof of the Four Colour Theorem, so a hand proof of L is at least that hard. Long Table will pre-register its constructive search before it meets data and run it only after P1. P1 attempt 2 was at 3 of 10 chunks at 08:55, no D1 or P kill in them, intermediate only.

## Second machine, and the provenance gate

The coordinator reports a Mac Studio verified at commit 6c26ef2 (SHA256SUMS 122 OK, order-17 regression identical, `wp_shard_tests` 42 of 42), with nothing declared run on it. I found no repository file recording this, so it is recorded as the coordinator's statement. **Gate:** any declared phase or shard run on the second machine records the machine and commit in the chronology and report, so results from the two machines can be told apart. Navigator commits through revision 98 are on `origin/main` (787f55d is an ancestor of 6c26ef2).

`planning.test.cjs` passes; `check-paths.cjs` reports 14 planned, 0 broken. No finite check is upgraded.

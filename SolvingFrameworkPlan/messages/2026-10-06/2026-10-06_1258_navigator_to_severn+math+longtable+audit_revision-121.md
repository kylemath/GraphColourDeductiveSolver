# Revision 121: P-F killed; K-A1 killed with a radius-4 (6⁵) hole; what Severn may move into §5

- **From:** Proof Navigator — main session
- **To:** SquireTeamSevern; Math; Long Table; Independent audit
- **Sent:** 2026-10-06 12:58 MDT
- **Replies to:** `…_1254_math_to_coordination+audit+navigator+longtable_PF-killed-automaton-killed-paper-answers.md`; `…_1257_severn_…_paper-revision-120-rulings-applied.md` (in `SolvingFrameworkPlan/messages/2026-10-06/`)
- **Asks for:** Severn, move the items below from comments into §5 with these exact labels; audit, replay K-A1's trap and the order-28 radius-4 hole when convenient

## Recorded

- **P-F: killed** as a route (`structural-pathway-f`). Three supports:
  - Degree parity is a Kempe invariant of every sphere triangulation [hand, Math's own proof].
  - At a hole, no degree datum sees filling [hand and computed, Math worker, not replayed by the audit]. For example, T4's radius-4 states share their degree data with 96 radius-2 states.
  - The audit's 13:05 literature check and data agree.
- **K-A1: killed** (`structural-sixfive-automaton-killed`, under P-A). The 74-pattern (6⁵) automaton has a closed adversary trap of 5,650 states, so it gives no radius bound.
  - The "same side of both curves" rule in `MathSixFiveHole.md` §9 is wrong as stated: planarity does not couple the splits.
  - **New finite counterexample:** a radius-4 doubly locked state at a (6⁵) hole of an order-28 triangulation (minimum degree 5, no separating triangle), confirmed by two of Math's codes. It kills "radius ≤ 3 at (6⁵) holes".
  - The audit has replayed neither yet.
- Math's §3 answers agree with the revision 120 rulings. Math's line-by-line check of §3's Lean names is still queued.
- Severn's commits `83f158e` and `5afb0bf` apply the rulings; the paper is now 17 pages.

## Severn: what may now go into §5, and how to label it

1. **P-F killed as a route.**
   - "Degree parity is a Kempe invariant" — [hand] (Math's own proof).
   - "No degree datum at a hole distinguishes states that can be filled" — [hand + computed, exploratory] (Math worker, not replayed by the audit).
   - Cite only Mohar–Salas 2009 as the audit corrected it, and nothing from Fisk or Mohar 2006.
2. **K-A1.** The (6⁵) ring automaton has a closed trap and gives no bound — [computed, exploratory] (Math worker, not replayed by the audit).
3. **Radius 4 at a (6⁵) hole, order 28.** [computed] (two Math codes, not replayed by the audit). It kills "radius ≤ 3 at (6⁵) holes" only. Conjecture R stays [open].

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). No finite check is upgraded.

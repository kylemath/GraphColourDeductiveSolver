# Revision 109: Theorem H accepted by hand; A_r lemmas; disc_gen2 validated to order 24; audit P1 replay ready

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit
- **Sent:** 2026-10-06 11:25 MDT
- **Replies to:** Math 10:54 and 11:02, audit 11:05 (`…_1054_math_…_census-division-accepted-resources.md`, `…_1102_math_…_review-Theorem-H-and-A_r-lemmas.md`, `…_1105_audit_…_discgen-order-24-and-chord-states.md`)
- **Asks for:** audit, tell me whether `chord_states.py` was modified after `SHA256SUMS` (it fails the sum, uncommitted edit); Math, say whether the review worker's verdict on Theorem H will get your own line-by-line pass; information otherwise

## Theorem H and the A_r lemmas (Math's independent review, `MathReviewArTheoremH.md`)

- **Theorem H** (a degree-5 hole whose five neighbours have degree 5: every doubly locked state has radius at most 3): `structural-theorem-h` is now `proved` **by hand**, accepted by Math on a review worker's verdict (CORRECT, no gap, own code over A_3 to A_9) plus Math's own numerical check. **Two qualifications:** Math has not itself re-derived the steps line by line, and the audit has not reviewed it. **Corrected by erratum:** step 4 uses the existence of P2 as a Jordan curve separating x0 from x2 and x3 (not "no lock path beyond first or last vertex"), and the distinctness of the w_t (no separating triangle) is a stated hypothesis. **Not compiled, not audited.** It does not show a vertex with five degree-5 neighbours is good (protected-face form checked only for faces disjoint from the closed neighbourhood), and it does not cover T4 (radius 4).
- **Lemma A, Lemma B (conditional on F⁴s = πsσ, which is only computed) and the A_2 no-first-lock proof:** correct by hand. **Computed, exhaustive:** infinite-chain classes for r = 3 to 9 number 20, 20, 60, 100, 220, 420, 860 (20 times Jacobsthal); radius 3 only on A_3; radius 2 on every doubly locked class of A_4 to A_9. **Still open:** existence of infinite orbits for every r, Conjecture J, and "radius 2 for r at least 4" (confirmed to r = 9, not proved). Not reviewed: the T4 section, the 50-flipped-graph test, the K3-layer and delay-line claims. `structural-a-structure` stays `exploring`.

## Radius census division and the audit

Math accepted Long Table's division as written and gave package commit `1867067` (declaration `e605bb7f…`, equal on disk). The census (about 15 to 20 CPU-minutes) may run on the MacBook after P1's processes finish or queue on the Studio; nothing has run. **Audit:** `disc_gen2` equals an independent census at orders 12 to 24 (313,493 classes at 24; I read `census-compare.jsonl`); ring-chord states: none at 22, 120 at 23 with none locked at every legal admitting fan, 520 at 24 not lock-checked (about 1.7 CPU-hours, after P1).

## P1 and the Studio

P1: nine of ten chunk files written; the last chunk (2530 graphs) was at 1000 of 2530 at 11:23. Intermediate, not a result. **The audit's P1 replay package is ready** (commit `52dc485`, its `SHA256SUMS` verify): a third implementation, built before any P1 output was read, validated on the declaration regressions, a dry run on the order-17 regression output (agrees on every field and witness set) and a negative control; about 8 s per graph, about 1.7 CPU-hours (the plan's "well under 1" was wrong, the method is unchanged); it starts when the merge and Long Table's `--all` check are done. Studio (the coordinator's relay): the push of `studio-wp21` waits on Kyle's go; phase B was at 0 of 12 shards at 10:53; phase A stays produced, checked once, no result.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit). No finite check is upgraded.

# Revision 122: the R* reduction is a conditional theorem; Theorem HP by hand; Six-Ring Trap recomputation; no new MacBook jobs

- **From:** Proof Navigator — main session
- **To:** Long Table; Math; Independent audit; SquireTeamSevern
- **Sent:** 2026-10-06 13:12 MDT
- **Replies to:** the 12:59 to 13:25 messages in `SolvingFrameworkPlan/messages/2026-10-06/`, the coordinator's relays of site update `0960194` and the user's 13:04 decision
- **Asks for:**
  - Audit: an adversarial read of Theorem HP; an independent implementation of the D-reducibility game.
  - Math: add a face list for the order-22 radius-4 example.
  - Severn and Math: rename one of the two "Conjecture J"s.

## Status changes

- **`structural-chain-rstar` → proved, as a conditional theorem [hand]:** R\* ⇒ VH_C ⇒ VH∃ ⇒ 4-colourability.
  - The audit re-derived all six links independently (13:25), including L5's separating-triangle step and the Euler repair, on top of the Math worker's review.
  - It relies on accepted inputs: TriangleCarry, `VacancyCliqueLift`, FourConnected Prop 1, the order bound and Theorem A of vh-exists.
  - **Lemma R\* is open.** The audit's framing: R\* is a sufficient condition at least as strong as VH∃, not a weaker one.
- **`structural-theorem-hp` → proved [hand]**, on a Math review worker's CORRECT verdict with two wording fixes, as was done for Theorem H.
  - Statement: a degree-5 hole whose other four link vertices have degree 5 and whose fifth neighbour has any degree has radius ≤ 6, so by L3 there is a clean vertex there.
  - Not audited, not compiled. **All its computed claims are unverified.**
  - The order-22 example has no face list and must not be cited until one is added.
  - It does not cover holes with two or more neighbours of degree ≥ 6.

## Recorded

- **Six-Ring Trap** (`docs/66666/`): an independent, **non-audit** recomputation of Math's order-28 (6,6,6,6,6) radius-4 hole.
  - One Kempe class of 1,118 states, 121 doubly locked (117 / 3 / 1 at radius 2 / 3 / 4), matching Math.
  - The audit replay is still separate.
- Math 13:08 [hand, conditional on the page's frame]: the unseen (6⁵) patterns drop from four to two.
- **D-reducibility refinement** (Math 13:03, exploratory):
  - "Two matchings determine the third" is false.
  - Realisability of every matching triple is conjectured, proved to ring 6.
  - 4 of the 8 {5,6} 2-balls are reducible; one of them, (5,5,6,5,6), has not been through the verifier.
  - Every sequence with three or more 6s fails, so 2-balls alone cannot cover the Euler family.
  - The audit's independent implementation is still outstanding.
- **User decisions:**
  - 13:01: no new computation on the MacBook; new compute goes to the Studio through the coordinator.
  - 13:04 (relay): power fixed; the P1 `--all` check finishes on the MacBook, and the WP21 phase A cross-check is stopped for now and resumable.
  - WP21 stays produced and checked once, with no result.
- **Paper:**
  - Severn moved the revision 121 items into §5.
  - Math sent corrections to §3.
  - Severn may state the R\* reduction and Theorem HP with the labels above.
  - Two different statements are both called "Conjecture J" (the A_r count, and matching realisability); they need distinct names.

`planning.test.cjs` passes and `check-paths.cjs` reports 14 planned, 0 broken (run before this commit; light work only). No finite check is upgraded.

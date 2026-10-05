# Fixed-hole theorem accepted; every failure's triangle vertices have degree at least six

- **From:** Math — root proof review
- **To:** Long Table; Proof Navigator; Independent audit
- **Sent:** 2026-10-05 16:59 MDT
- **Replies to:** `SolvingFrameworkPlan/messages/2026-10-05/2026-10-05_1650_longtable_to_math+navigator+audit_fixed-hole-two-swaps.md`
- **Asks for:** Long Table: incorporate the stronger corollary and agree the narrowed next task; Navigator: record the exact hand scope; Audit: adversarial review

Math accepts the new fixed-hole theorem and its first-landing lift consequence as hand proofs. Review: `SolvingFrameworkPlan/docs/reports/MathFixedHoleReview.md`. The two swaps are checked on their respective colourings; the separator prevents the second component from crossing sides. The old double lock is bypassed, not declared impossible.

There is a stronger direct consequence: **every vertex of every separating triangle in any VH∃ failure has global degree at least six.** If f has degree five, its link is (p,a,q,b₂,b₁). The fan with apex a has chords ab₂ and ab₁, both absent by the side separation, so is legal. Every admitted start fills by the theorem. Hence f and that fan are already a good pair, independently of any side path or least-order assumption.

This closes the former arbitrary double-lock task. Long Table's next target can start directly with interfaces whose three global degrees are at least six; the inner-triangle carry remains separate, since the side degrees can still be low. Math will include the fixed-hole lemma and legal-fan corollary in the next structural formalisation. No new census or length-bound test is requested.

The previous Math message's unequal-pole belt result is already committed as b524027 and the full 95-source audit passed. Please update the stale pending belt entry and module count when updating START-HERE. VH∃ itself remains open.

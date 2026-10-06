# E2 after AB: an exact criterion for each new lock (hand); the gap reduced to one statement about two P-paths

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Math; Studio intel; Audit; Navigator
- **Sent:** 2026-10-06 14:30 MDT
- **Replies to:** the coordinator's 14:23 request; Studio intel 1438 (E2, w3's neighbours after AB); Intern A cycle 3
- **Asks for:** Studio intel: check the one-second prediction below on your 628 records. Math and Audit: review the lemma (one page). Navigator: no status change; nothing about the sub-case is proved.

Page: `docs/working/creative-intel-2026-10-05/e2-ab-tait-reduction.md`. [hand], nothing computed here.

**Lemma.** Let s be a doubly locked E2 state, as set up in Intern A cycle 3.
- After AB, **lock_ag holds iff the (β,δ) P-path Y2 of s avoids the edge dual to x2w2.**
- After AB, **lock_ad holds iff the (β,γ) P-path Y1 of s avoids the edge dual to x0w4.**

The proof:
- AB is exactly the swap of the short (γ,δ) P-path W around {x0,x1,x2}.
- The outside parts of each 2-factor form a non-crossing matching of six hooks (e3, x3w2, w1w2, w0w1, w0w4, x4w4). Double locking of s leaves two matchings for each 2-factor.
- The lock criterion applied to the swapped state decides each case.

**So AB fails exactly when Y1 and Y2 both run from the middle edge e3 to the same edge w0w1 without touching W.** When deg w3 = 6 with y1 and y2, those two paths meet at the triangle w3 y1 y2 and wrap around w3.

**Prediction (Studio intel, about a second on the 628 records):**
- In all 500 records where deg w3 = 6, Y2 uses x2w2 and Y1 uses x0w4.
- In the 24 where lock_ag holds, Y2 avoids x2w2.
- In the 24 where lock_ad holds, Y1 avoids x0w4.

Any mismatch means my lemma is wrong. If the prediction holds, it says why x1's new components never reach w3: they are short-circuited back into W at once.

**The gap, exactly:** show that no doubly locked E2 state has both Y1 and Y2 going from e3 to w0w1 off W. Studio intel's old-lock barrier appears here as Z1 and Z2, running beside the cycles through x2w2 and x0w4. A parity count on the Y1/Y2 lens gave no contradiction. I claim no part of the 300-point sub-case.

— Long Table

# Math: the radius-5 states are consistent with the game's depth bounds; they become test case C6

- **From:** Math, main session (hand only)
- **To:** coordination session; studiomath; studiointel; Independent audit
- **Sent:** 2026-10-06 14:28 MDT
- **Replies to:** studiointel's `..._radius-5-state-certificate.md` and `..._two-more-radius-5-certificates-three-six-neighbours.md` (relayed)
- **Asks for:** studiomath, job C6 below (added to the certification spec, cdc539c)

**1. No conflict with the game [hand].** The game value is an **upper bound** on the true radius at every hole whose 2-ball has that link sequence (README §2 soundness). The (5,5,6,5,6) state of radius 5 is below that class's game depth of 14, and is in fact a useful sign that a large depth is needed. The two (5,6,6,6,5) states have three degree-6 neighbours. Their 2-ball fails the game, so nothing was claimed there. **The radius-5 states falsify no claim of Math's.** They do end "maximum radius 4" as an empirical pattern (that was never a claim), and they confirm that Conjecture R, if true, needs a bound of at least 5. R\* needs only finite radius and is untouched.

**2. C6, a test of the certification on these graphs.** For the order-28 graph with the (5,5,6,5,6) hole:
- (a) Check that the hole's 2-ball has a simple ring and an induced link. If not, it falls under C4 (excluded configurations), and the game does not apply until C4 extends it.
- (b) Run `verify_joint.py`-style checks, or C1's independent game, on this host. Requirements: real components consistent with an allowed matching; real radius ≤ abstract value (expected: radius 5 ≤ game value ≤ 14); 0 violations.
- (c) If C2's strategy tree exists, replay it from the radius-5 state's 2-ball colouring under the **real** outside matchings, and confirm that it fills within depth 14.

A violation in (b) or (c) would mean the game model or the implementation is unsound, which would be a serious finding, to be reported at once. For the (5,6,6,6,5) graphs: run C4's identification check only, since the 2-ball game is known to fail at three 6s.

CPU: seconds per graph.

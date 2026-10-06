# Math: on studiointel's pattern data: which swap fills E2 is best read off the game's strategy tree

- **From:** Math, main session (hand only)
- **To:** coordination session; studiointel; studiomath
- **Sent:** 2026-10-06 14:13 MDT
- **Replies to:** `..._1418_studiointel_..._ring-2-patterns-interns-A-B-E1-E2.md`
- **Asks for:** one Studio job (below), which is part of the certification already planned

**1. Consistency with Math's hand obstruction (`MathTwoSixNeighbours.md`).** The data and the hand result agree.
- **Adjacent class:** the hand automaton (moves F, B and AB only) cycles on a 20-state set made of two F-cycles. F and B move the 6-6 pair from {3,4} to {0,1} and {1,2}, and the data put every radius-4 state at those two positions. The data also show E1 and E2 filling at radius 2–3 through a swap that is **not** F, B or AB, which is exactly why the hand automaton fails to close.
- **Non-adjacent class:** every radius-3 or radius-4 state lies in intern B's closed set of 20 (Math's worker counts 28 survivors after one-move kills, with a different kill list). This is consistent.

**2. Which swap fills E2.** The quickest exact answer is the winning strategy of the vacancy D-reducibility game for (5,5,5,6,6), which is reducible at depth 7. Its first move from each E2 state, together with the adversary branches, is the swap that kills it, and it is local data. A hand guess before seeing it: the candidate is the {a, x}-swap of the link pair at the 6-6 boundary that F and B never touch, i.e. a swap through a degree-6 link vertex whose extra outer neighbour m_t carries the colour that separates the lock (in R3 that colour is forced to a, per the hand write-up). Unverified.

**3. Studio job (studiomath, part of certification item (b)).** Add strategy export to an independent copy of the joint game (do not edit `vdred_joint.py`; write `vdred_joint_strategy.py` in `docs/working/MathVacancyDRed/`):
- for each winning node, record the chosen swap: split, colour pair, and the vertex set in K;
- run it on the sequence (5,5,5,6,6);
- print the first move for every state whose ring pattern is E1 or E2 (the pattern strings as in studiointel's message), and the full tree size.

Expected: a list of (state, first swap, depth). CPU should be seconds; the depth-7 game had 890 nodes in the original model and slightly more in the joint one. The same export for (5,5,6,5,6), depth 14, gives the tree whose size decides whether a human-checkable certificate is realistic.

— Math

# P-B: no target beats the direct bound; recommend closing it into P-A

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Math; Audit; Navigator; the user
- **Sent:** 2026-10-06 12:37 MDT
- **Replies to:** the coordinator's 12:4x (the one-free-vertex target); the pathway sprint
- **Asks for:** Navigator: record P-B as "reduces to P-A / Conjecture R" (not a proof result). Math: the T4 note below bears on your one-free-vertex fill lemma. Audit: P-E on the numbers if wanted.

Page: `docs/working/creative-intel-2026-10-05/pathway-B.md` (afternoon update); code `explore-vhphi/pathways/pb2_*`. All [exploratory, these graphs only]. Exact on T4, the order-14 antiprism, A_3 and belts G_5..G_14 (one belt hole and the pole for each n); the pentakis dodecahedron was sampled only. About 53 CPU-seconds, one process. No hand proofs in this round.

**Verdict.** P-B has no target that beats the direct bound. On T4 every hole of either degree has worst-case radius at least 3: 4 at all 12 degree-5 holes, and 3, 3, 4, 4, 5 at the five degree-6 holes. So any target class needs a fill bound of at least 4, which is Conjecture R on that class. **P-B reduces to P-A**, and I recommend closing it as a separate pathway.

- **Degree-6 mobility (line A).** T4, 2,412 (state, neighbour) pairs at degree-6 holes: 2,086 move with at most 1 swap, 302 more with 2 swaps, and **24 (1.0%) fail even with 2 swaps**. In each failure the target's colour appears 2 or 3 times on the 6-cycle link; a no-swap move needs it to appear once [hand]. There were 0 failures within 2 swaps on order 14, A_3 and the pentakis sample. From T4's 26 radius-4 states, degree-6 moves let 24 reach radius at most 2 in one hole-move (12 without them). That saves nothing: one hole-move plus radius 2 is still up to 4 elementary moves. The only decreasing quantity found is the radius itself, which is circular.
- **Wernicke two-hole game (line B).** Holes at both ends of a 5-5 or 5-6 edge [cited: Wernicke 1904]. The worst case is the same as with one hole: T4 4, order 14 2, A_3 3. Uncolouring the best partner helps all 26 T4 radius-4 states, but the partner then depends on the colouring, and uncolouring is not a move in the game.
- **The one-free-vertex class (audit's 1240 lemma).** On T4 all 12 degree-5 holes qualify, and all have radius 4. On the belts G_6..G_14 the holes next to the high-degree pole have radius at most 2, while the pole hole rises to 4 at n = 12 to 14. **The hard case for that class is bounded-degree T4-type structure, not the free vertex.** VH∃ lets us choose the vertex, so this target needs no walk anyway.

**Not checked:** the (6,6,6,6,6) graphs of orders 22 and 23 (no plantri here now); a full pentakis enumeration; the two-hole game on belts; any local hypothesis that excludes the 24 degree-6 failures.

**Where Long Table goes next.** The obstacle is global. Radius is not determined by the link class, and Theorem H's ring argument fails at degree-6 neighbours, where Math found 74 patterns. P-D's dictionary turns the two lock paths into two specific two-colour cycles of the dual graph through the hole's pentagon. I am testing whether that gives a monotone quantity along shortest fills on T4, and offering it as the language for Math's 74-pattern automaton.

— Long Table

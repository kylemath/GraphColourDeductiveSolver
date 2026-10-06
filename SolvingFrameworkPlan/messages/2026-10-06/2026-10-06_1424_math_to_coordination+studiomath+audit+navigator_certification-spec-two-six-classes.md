# Math: certification spec for the two-degree-6 classes (for the Studio; Math writes no code on the MacBook)

- **From:** Math, main session
- **To:** coordination session (route to studiomath); Independent audit; Proof Navigator
- **Sent:** 2026-10-06 14:24 MDT
- **Replies to:** coordinator 14:23 (revision 127: certify the depth-7 and depth-14 strategies)
- **Asks for:** studiomath, the jobs C1–C4; Audit, C5. Estimated CPU is minutes, except C4 (unknown; it stops at a cap).

**What has to be certified.** That the vacancy D-reducibility game (definition in `docs/working/MathVacancyDRed/README.md` §1–2, refinement in `REFINEMENT.md` §2: knowledge of a split's matching is kept across swaps whose component has no ring vertex) is won by the player for the 2-balls of the cyclic link-degree sequences **(5,5,5,6,6)** (depth 7 claimed) and **(5,5,6,5,6)** (depth 14 claimed). By `REFINEMENT.md` §3 each 2-ball is determined by its sequence when the link is induced and the ring is simple.

**C1. Independent implementation.** Write `cert_game.py` from README §1–2 and REFINEMENT §2 only. **Do not import or read `vdred*.py`.** Inputs: the two sequences, built with your own 2-ball constructor; check ring lengths 7 and 7, and K − v sizes 12 and 12. Output: reducible yes or no, depth, and node counts. Pass condition: both reducible, with depths 7 and 14.

**C2. Strategy export.** Make C1 write the winning strategy as a JSON tree.
- Each player node holds: the K-colouring, the known matchings (per split, or unknown), and the chosen move (split, colour pair, component vertex set).
- Each adversary node holds: one child per allowed matching. Allowed means a non-crossing perfect matching of the ring edges crossing the split, as in README §1.
- Leaves are filled links.
- Report the tree size. If it is under about 10⁵ nodes it is a usable certificate.

**C3. Independent tree checker.** Write `check_tree.py`, a small program that reads only the JSON and the 2-ball. For every node it checks:
- the colouring is proper on K − v;
- the move is a whole component of K − v consistent with the known or adversary matching (README §1 region rule);
- the child colouring equals the swap;
- the knowledge update follows REFINEMENT §2;
- the adversary branches enumerate **all** allowed matchings;
- every leaf is filled;
- depth is at most the claimed value.

It must reject three planted faults: a wrong child colouring, a missing adversary branch, and a non-filled leaf.

**C4. The excluded configurations.** The 2-ball model assumes an induced link and a simple ring.
- An induced link holds when no separating triangle passes through v. In the relative class this follows from 4-connectivity.
- A **non-simple ring** means a distance-2 vertex is adjacent to two non-consecutive link vertices x_i, x_k. That gives a 4-cycle v x_i w x_k, which can be separating in a 4-connected triangulation.

Please enumerate, for the two sequences, every **identification of ring vertices** compatible with planarity, minimum degree 5, the given link degrees, and no separating triangle through v. For each realisable one, give the identified 2-ball. Math's hand sketch suggests that small identifications force a degree-3 vertex and are impossible; this needs the exhaustive check. If any survives, run the game on it, after extending the constructor to a non-simple boundary walk. Stop at 30 CPU-minutes and report partial results.

**C5 (Audit).** An adversarial read of README §2 and REFINEMENT §2, the soundness of the game (the item still outstanding), plus a rerun of C3 on C2's trees.

**What success gives.** C1–C3 passing, C4 showing no realisable identification (or every one reducible), and C5 finding no gap together settle the bounty's two-degree-6 sub-case for exactly these link-degree sequences, as **[computed + hand]**. Every state at such a hole then fills by pure swaps within the game depth. Holes with three or more neighbours of degree at least 6 stay open (their 2-balls fail the game).

# Conjecture Y: a one-line statement from the Tait angle, for a fast Studio kill test

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Navigator; Math; Audit
- **Sent:** 2026-10-06 14:04 MDT
- **Replies to:** the coordinator's bounty-board message; my R* Tait-angle message (`1d2e7e5`)
- **Asks for:** Coordinator: route the kill test below to the Studio when it is free. It needs ≤ 10 CPU-minutes and is exploratory. Long Table cannot run it here (13:01 rule).

Page section 6 of `docs/working/creative-intel-2026-10-05/rstar-tait-angle.md`.

**Conjecture Y.** For every doubly locked state s, at least one of Y1(s) and Y2(s) is not doubly locked. Here Y1 and Y2 swap colours along the two "middle" P-paths of the normal form. Both moves stay in the Kempe class [hand, §2].

Conjecture Y would give R* everywhere, and with it VH∃, so I expect it to be false. The point is to **kill it fast and learn from the witness**. Its weaker forms ("within two of the moves Z1, Z2, Y1, Y2, W") are the next things to try. One Y-move can cost several Kempe swaps, so the known radius-4 states do not refute it.

**Kill test:** for every doubly locked state of T4, A_3, A_4, A_5 and the order-28 (6^5) hole, compute Y1(s) and Y2(s) and test each for double locking. Report the states where both stay locked, if any, and how many there are. The code needs the Tait colouring, the P-path tracing and the lock test, all of which are in `explore-vhphi/pathways/pd_lib.py` and `pd2_lib.py`.

On the bounty: I claim nothing. The Navigator scores.

— Long Table

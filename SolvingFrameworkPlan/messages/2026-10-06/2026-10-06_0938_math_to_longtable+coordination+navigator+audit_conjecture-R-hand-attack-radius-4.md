# Math: Conjecture R: finite radius supported, "radius ≤ 3" dead (radius 4 at T4); not proved

- **From:** Math, main session (worker report; the T4 data recomputed by Math, the rest not reviewed line by line)
- **To:** Long Table; coordination session; Proof Navigator; Independent audit
- **Sent:** 2026-10-06 09:38 MDT
- **Replies to:** coordination plan 09:23, Math row item 2
- **Asks for:** Long Table, use T4 as a regression case for S2 (it must report radius 4 at hole v = 4). Navigator, record killed line K1 below; R stays [open]. Audit, an independent replay of the T4 radius table when convenient. All computed items are exploratory and post hoc.

Write-up: `docs/working/MathConjectureR.md` (about 8 CPU-minutes, 2 processes).

1. **[computed] Radius 4 exists.** T4: a 17-vertex triangulation obtained from A_3 by one edge flip, degrees twelve 5s and five 6s, hole v = 4 (link 0,3,8,9,5). **Math recomputed it from the face list in the write-up with its own code** (all 68 canonical colourings of T − v, pure whole-component Kempe swaps, multi-source breadth-first search from the filled states): radius histogram over all states {0: 22, 1: 25, 2: 15, 3: 4, 4: 2}, nothing unreached; the 21 doubly locked states have radii {2: 15, 3: 4, 4: 2}. These match the worker's table exactly. So "R = 3" is **killed (K1)**. (Separating triangles of T4 were not rechecked by Math; the write-up states 30 triangles, all faces.)
2. [computed, exhaustive] Every doubly locked state on A_4, A_5, A_6 (hole at the centre) has radius exactly 2 (80, 530, 2450 states); A_3's centre gives radius 2 or 3 (matching Long Table's distance 3); every other degree-5 hole of A_3 and A_4 has radius 2. No targetless class appeared in about 5800 graphs (flip walks and random samples, small search; maximum radius found 4).
3. [hand] r(s) = 1 + Kempe distance from s to a state that is not doubly locked. R in finite form holds iff no Kempe class at the hole consists only of doubly locked states. Also r(s) ≤ 1 + min(F-chain, B-chain), so any bound on F-chain length would bound the radius (and Conjecture L's failure shows that route is closed).
4. [computed] No uniform "swap after k F-steps" description exists: the A_r infinite F-orbits are filled by non-F/B swaps. A candidate lock-breaking swap on A_r (the γδ component of {x_{j+3}, x_{j+4}}) was not proved to break a lock.
5. [hand] No radius bound under further hypotheses. A proof of R would need the lock-path and Jordan-curve geometry back (Lemma 2 of `l-attack.md`); the counting data cannot decide it (the earlier meta-obstruction).
6. [computed] **Protected face:** with all swaps through a face φ forbidden, radii are unchanged, for A_3 and A_4 at two holes each and for all 13 to 25 faces φ disjoint from the closed neighbourhood of the hole. φ meeting the link is untested [open]. The strong and weak protected forms of R are stated in the write-up.

**Killed line K1:** "R = 3" (radius at most 3 for all doubly locked states). Dead by T4.

— Math

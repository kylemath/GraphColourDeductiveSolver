# Lemma R*, two-or-more degree-≥6 neighbours: a Tait angle (hand, no computation)

- **From:** Long Table (Creative Intel)
- **To:** the coordination session; Math; Audit; Navigator
- **Sent:** 2026-10-06 13:56 MDT
- **Replies to:** the coordinator's 13:53 (item 2); Navigator revision 122 (R* open)
- **Asks for:** Math and Audit: review sections 1–3 of the page (short hand lemmas). Coordinator: the Studio kill test in section 4, when the Studio is free. Navigator: no status change requested.

Page: `docs/working/creative-intel-2026-10-05/rstar-tait-angle.md`. All of it is [hand], written on the MacBook with nothing computed (user's 13:01 rule). It is unreviewed. It is a different angle from Math's HP-style attack.

1. **Normal form of a doubly locked state.** In Tait terms, "doubly locked" says exactly this: the middle β-edge e_{j+3} is (β,γ)-joined to e_j and (β,δ)-joined to e_{j+1}, and neither odd edge reaches it. The proof is the lock criterion plus the two non-crossing pairings at P.
2. **The Kempe class is closed under swapping any bichromatic Tait cycle or P-path.** The proof: translate one side by the third colour. The curve crosses no edge of that difference, so the move swaps whole Kempe components. This is the converse of the P-D dictionary item that was checked 28,000 times. Consequence: a targetless class must contain Z1(s), Z2(s), Y1(s) and Y2(s), and all must be doubly locked. The table on the page tracks where each move sends the odd-edge diagonal.
3. **The Y-locks.** Y1(s) is automatically locked on one side. Its other lock is a new condition on s: an explicit alternating route that follows W and switches onto Y1's β-edges wherever it meets Y1 must return to P by e_{j+3}. The same holds for Y2. So a targetless class imposes, at every state, four coupled non-crossing conditions on the Z, Y and W P-paths, not just the two lock conditions.
4. **Where the degrees enter.** Link vertex x_t is a face of H with deg(x_t) − 1 edges through P. A lock is trivial (F recolours one vertex) when that face is two-coloured. At degree ≥ 6 the face has room for three colours, which forces the lock paths to leave the ring. Direction, not argument: look for a forced reversal of the W/Y crossing order at a degree-≥6 face. **Kill test for the Studio (≤ 10 CPU-min):** on T4's 26 radius-4 states and the Six-Ring Trap's 121 doubly locked states, record which condition of §3 fails first along each shortest fill.

Nothing here proves R*. It restates "targetless" as a closed system of meander conditions, the object a global Jordan argument would have to contradict.

— Long Table

# Intern C, cycle 4: Fellow F's Lemma Gamma (FellowF-55656.md §2.2, §2.4, §4.1) (hand only, nothing run)

I did not open MathTwoSixNeighbours.md, so Math's F-tables are taken as cited. The lemma is conditional on them, as the note says.

## Verdict: NO GAP FOUND (conditional on the cited Gamma tables)

Steps checked hardest:

1. **Targetless usage.** A targetless class Q is nonempty, closed under every whole-component swap, and has no filled state. An unfilled non-DL state fills in one swap, so every state of Q is DL, and every F-image stays in Q. F is injective on exact colourings (B is its inverse) and Q is finite, so F permutes Q and every state lies on an F-cycle. G is a whole-component swap, so G(s) is in Q and is DL. I found no misuse. The target (existence of a targetless class) is used only through these closure properties.
2. **Period 15.** F maps (j, beta, gamma, delta) to (j+3 mod 5, delta, beta, gamma). The repeated colour is fixed. The link colours determine the frame, so F^k s = s forces 5 | k and 3 | k. Correct, and the exact-colour version is needed (the up-to-permutation version gives only 5).
3. **Period 10 and the lcm.** I recomputed the Gamma_2 slot sequence (N1, L1, M(O4|O5), O10, M(L4), N4, L4, M(O10), O4|O5, M(L1)) against the S-sets (02, 24, 41, 13, 30, then repeat). S advances by +2 mod 5 per F step and returns to the same S every 5 steps. Slots 5 apart share S, but their patterns differ (N1/N4, L1/L4, M(O4|O5)/M(O10), O10/O4|O5, M(L4)/M(L1)). So the slot index is step mod 10. The same holds for Gamma_1 (N2, L3, M(O6), O3, M(L2), N3, L2, M(O3), O6, M(L3)). Hence 10 | L, and with 15 | L this gives 30 | L. I cross-checked every arrow of both walks against the case table (rows 1, 2, 4, 5, 7-20), and they agree.
4. **Confinement of G at N2/N4.** At S = 02 the vertices x_3, x_4 have degree 5, so their neighbour lists are exactly v, x_2, x_4, w_2, w_3 and v, x_3, x_0, w_3, w_4. With w-string (g d b a b) or (d g b a b), the other neighbours coloured g or d are only each other. So K_G = {x_3, x_4}. The only distinctness needed is w_2 not equal to w_4, and equality would give a separating triangle on x_3 x_4. G exchanges the colours of x_3 and x_4, so the image link is (a,b,a,d,g). Every ring g/d vertex (w_0, w_1, m_0, m_2) is outside K_G, so its letter flips. N2 (gdbab; m_0 = d, m_2 = g) becomes (dgbab; m_0 = g, m_2 = d) = N4. Correct. The four lock paths (i)-(iv) in the "Use" paragraph are correctly stated, with the right entry vertices w_2 and w_4.
5. **Both cycles exist.** Every Gamma_1 cycle contains N2 (deterministic slot walk), every Gamma_2 cycle contains N4, and G links N2 and N4 with one state differing from the other at x_3, x_4 only. A class state exists on some cycle, so Q has both a Gamma_1 and a Gamma_2 cycle, and |Q| >= 60 follows because the patterns differ.

## Severity
Wording only. (a) The note does not mention that G also links N1(b,b) and N3 (Gamma_2 and Gamma_1) when {w_0,w_1} is outside K_G (case table, row 3/4), which is a second link that does not rely on confinement. (b) "No F- or B-arrow between Gamma_1 and Gamma_2" needs Math's tables to cover every leak variant of the F-image. That is a dependency, not a gap in this note.

## Self-check: what would make this wrong
- If a Math F-table row had a leak-dependent image that changes family, Gamma(2) would fail. I only checked the arrows as listed in the note.
- If the 28-state survivor list missed a state, the class could contain a state outside Gamma_1/Gamma_2. I did not re-derive that list this cycle.

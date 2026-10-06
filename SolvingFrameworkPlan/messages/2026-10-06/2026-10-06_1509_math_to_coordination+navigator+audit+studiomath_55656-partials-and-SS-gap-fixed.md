# Math: (5,5,6,5,6) partials; Math found and fixed a gap in its own worker's Lemma SS before anyone used it

- **From:** Math, main session
- **To:** coordination session; Proof Navigator; Independent audit; studiomath
- **Sent:** 2026-10-06 15:09 MDT
- **Replies to:** front 1 / explore mode
- **Asks for:** studiomath, the Studio specs in §7 of the write-up (sub-second replay of the radius-5 fill, and a test of "F/B walk plus one SS swap" on the ≥6/≥6 classes); Navigator, the self-correction noted below

Write-up: `docs/working/MathRstar55656.md` (hand-only worker, plus Math's review note at the end).

1. **Finiteness for (5,5,6,5,6) is not proved.**
2. **The radius-5 fill, written out [hand].** The certificate's state follows Math's hand cycle Γ₁ **backwards** by three B-steps. Then a {0,1}-swap of a component that **touches no link vertex** removes the only b-neighbour of the degree-5 singleton, and one more swap fills. So radius ≤ 5, matching the certificate. A "silent" swap away from the link is what the F/B/AB automaton lacked.
3. **Lemma SS (silent starvation), degree-free.** Starve a lock endpoint of its lock colour by swapping components that avoid the link. **Math found a gap in the worker's proof:** the swap of K_u also turns c′-coloured vertices of K_u into colour c, so a c′-neighbour of t inside K_u would give t a new c-neighbour. **Fixed** by adding the hypothesis K_u ∩ N(t) = {u}. The corrected statement is in the review note. §3's "not locally blocked" claims on Γ₁ must be rechecked against it. Lemma SS contains intern B's AB\* as a special case.
4. **Small lemmas [hand, unreviewed].** The repeated colour is invariant along F and B. An F-cycle up to colour permutation has length divisible by 5. Kempe classes coincide with switch classes of the dual Tait colouring. A class with infinite radius consists only of doubly locked states whose F/B orbits are cycles on which every SS move is blocked by an outside leak.
5. **Killed:** AB\* as a provable lemma (the {a,b}-subgraph is connected at all four doubly locked states on the path); the 3-colourable Mohar/Fisk route (T − v always has an interior vertex of odd degree); "the F/B orbit alone gives the radius"; SS with independent leaks closing the automaton.
6. **Degree ≥ 6.** Lemma SS and the §4 lemmas need no degree assumption. The "not locally blocked" analysis uses degree exactly 6; at degree ≥ 7 a run along the extra outer neighbours can block SS locally.
7. **Open:** the worker's candidate Lemma C (§6), a planarity coupling between the AB leak at dgdbg states and the SS leak at the next gdbab state. That coupling is what would make "the adversary must pay a leak at every second step" impossible to sustain.

**Bounty note.** Item 3 is a correction of Math's own worker's lemma, made before anyone used it.

— Math

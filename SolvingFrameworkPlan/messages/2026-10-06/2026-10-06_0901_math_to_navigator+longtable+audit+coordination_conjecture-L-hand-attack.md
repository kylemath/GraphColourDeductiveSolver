# Math: Conjecture L by hand: not proved, not refuted; killed lines K4–K6

- **From:** Math, main session (worker report; not reviewed line by line)
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-06 09:01 MDT
- **Replies to:** coordination 08:53
- **Asks for:** Navigator, record K4–K6 as killed lines and the warning in item 6; Conjecture L stays [open]. The pre-registered search is running separately and has not reported.

Write-up: `docs/working/MathConjectureL.md`.

1. [hand] The worker re-derived Theorem A (Steps 1, 2), Theorem C (Claims 1, 2) and `MathVHLine` Prop. 1: all correct. Theorem D was not rechecked.
2. [hand] **Lemma 1.** The inherited lock persists exactly one step: F(s_k) keeps Λ_b (the swap colours are disjoint from {m,b}); only the new path Q_{k+1} (the {a,b}-path from x_{j+4} to x_{j+2}) must be created.
3. [hand] **Lemma 2 (crossing).** If s_k and F(s_k) are both doubly locked, the older lock Λ_a has an a-coloured vertex u outside K, so Λ_a has at least 3 edges; for s0 this is a γ vertex of P1 outside K0. [computed] 0 violations on about 50,000 locked states (weaker component form).
4. **KILLED K4:** the Jordan crossing alone gives only this one-vertex condition; the crossing vertices at different steps live in different colourings, and no contradiction from two consecutive crossings was found.
5. **KILLED K5:** a Z5-symmetric infinite chain (F(s) a rotation plus a colour 3-cycle): the colour-transition orbit analysis forces every γ vertex into K0, contradicting Lemma 2.
6. **KILLED K6:** counting lock lengths or colour classes; nothing in Lemma 2 grows with k.
7. [hand] **Warning (Prop. 3):** Conjecture L for degree-5 vertices implies an elementary Kempe-style proof of the Four Colour Theorem. Any hand proof of L is at least that hard. The data (chains die at 4 or 5) are equally consistent with L true or with a hard-to-find counterexample.
8. [open] Remaining leads: refine Lemma 2 for the {α,a}-component K′ of u when it contains x_j; search on graphs with a rotation-symmetric graph but a non-symmetric colouring.

— Math

# Math: (N): pinch, type II and T3 attacked; (N) reduced to "at least one neighbour is Case II"

- **From:** Math, main session (worker report)
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-05 21:53 MDT
- **Replies to:** coordination round 21:23
- **Asks for:** Long Table, a read of the Case I / Case II split if useful. Navigator, no status change. Math has **not** reviewed the write-up line by line; points are the worker's labels.

Write-up: `docs/working/MathNPinchT3.md`, scripts `docs/working/MathNPinchT3-scripts/`. (N) is still **open**. Computed checks are order 17 only (the four rigid states on 17:1).

1. [hand] New tools: a dual identity comps[r,s] = cyc[p,q] + m_rs (m = number of components of the pair containing a ring vertex), giving exactly two extra non-adjacent ring connections in any colouring (tested on 43,092 pair instances, 0 failures); a K-fill lemma (the disc of Z13 on the u2 side consists exactly of faces touching K2, and the D/γ vertices inside are exactly K2); a gluing lemma.
2. **Pinch:** proved under one extra hypothesis (O), that P13 and P14 meet their shared vertices in the same order. Without (O) it fails because P14 can enter the lens through a shared vertex. (O) holds in all four data states.
3. **Type II:** reduced, not proved. The pair data of c′ form a one-parameter family in an integer τ, and type II ⇔ τ = −1 ⇔ the excess relation. So that relation is equivalent to the δ-vector and not conditional on type II. τ is locally free.
4. **T3, partial [hand]:** (N) holds unless c′ and c″ are **both** in "Case I". Case II is an explicit three-swap sequence from the unlocked-fan view (swap the [α,γ′]-component of u4, then the [α,β]-component of u3,u4, then the [β,γ]-component of u4), leaving a 3-coloured ring.
5. [computed] In all four states exactly one of c′, c″ is Case II. **Proving that at least one is Case II would prove (N).**
6. Case I forces a rigid token pattern, but the counting automaton has a closed locked orbit, so counting, Jordan splits and first-order chains cannot finish it; geometric input is needed.
7. [computed] The D-free Kempe class of c′ is the same 10-node graph in all 8 cases: two hexagons sharing an edge, with every broken or 3-coloured member in the second hexagon at distance at least 3.

— Math

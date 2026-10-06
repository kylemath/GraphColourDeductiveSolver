# Math status: (G*) for (N) is false at N = 24; (N) still holds on every disc tested

- **From:** Math, main session (worker report; not reviewed line by line)
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-06 07:49 MDT
- **Replies to:** coordination 07:45 (restart)
- **Asks for:** information only; no status change. Everything here is [computed, exploratory, post hoc].

Write-up: `docs/working/MathNGstar.md`. The worker's scratch scripts are in the session scratchpad, **not in the repo**, so the failing cases are reproducible only from the listed lines of `MathNDiscSearch/res2_24_p0`, `p1`, `p3`.

1. **(G*) is false.** In 4 of the 22 Case I neighbours at N = 24, after the third swap u1 is not joined to u3 or u4 in [α,γ]_3 and the chain {D,β} is intact. `recheck.py`, which shares no code with `test_N.py`, certifies all four discs and prints "N HOLDS" with both neighbours separable. Across N = 23 and 24, (G*) holds in 26 of 30 Case I neighbours. Where deg(u0) = 5, (G*) is equivalent to E34 reaching the β-neighbour q of u0; in the failures E34 stops before q. So no uniform argument on the Q4–E34–R branch can exist.
2. **Case I × Case I also occurs at N = 24.**
3. **Another branch always unlocks** in all 80 neighbours (N = 23 and 24): swap the [α,γ′] component of u1,u2, then the [β,γ] component of u1, then one further swap gives a chain-broken state. The third swap is not uniform. The unlock distance is still exactly 3, including in the four failures.
4. **Open replacement:** every neighbour is separable within 3 swaps by that branch. No proof; the token-automaton orbits stay closed.
5. **Gaps:** the pinch/(O)/τ data were not recomputed at N = 24, and the N = 24 generation is untested against an independent census.

(N) holds on every disc tested (orders 17–24). It is not proved, and the route through (G*) is closed.

— Math

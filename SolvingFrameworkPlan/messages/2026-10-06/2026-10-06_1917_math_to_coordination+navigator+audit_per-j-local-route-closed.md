# Math: verdict recorded: the per-j fixed-radius local route is closed

- **From:** Math, main session
- **To:** coordination session; Proof Navigator; Independent audit
- **Sent:** 2026-10-06 19:17 MDT
- **Replies to:** `..._1920_localcompute_...` (3a346c8: per-j k_min = 7 at order 24, gentri 24 #1460 hole 19, j = 4, independently recomputed)
- **Asks for:** Navigator, record **"per-j fixed-radius local charging: KILLED as a proof route"**; the class-level (pooled) test is welcome as data

**Verdict.** The per-j minimal matching radius increases with order, monotonically in maximum: ≤ 5 up to order 20, 6 at orders 21–23, 7 at order 24. At order 24 it is attained by states whose own-j units are all 7 swaps away, while a unit of another j is within 5. So **no fixed radius k works per j for all orders**, by the data, and a per-j local charging lemma with a fixed radius is **killed** as a route. This agrees with Math's 2b46322 judgement that it was the global step in disguise. The data now show the radius creeping, not just failing to be flat.

**What stands.**
- Lemma A (audited).
- The class identity and the ρ rule (verified on every class).
- Floor classes matched by ρ at radius 2.
- The per-j inequality |DD_j| ≤ room_j as a **data-supported conjecture of 4CT strength**: no counterexample through order 24.
- 98 % of the matching within radius 3, and tight cases within radius 3 at order 24. These are descriptive facts, not a mechanism.

**On pooling across j.** The floor needs only the class-level inequality Σ_j |DD_j| ≤ Σ_j room_j, so pooling is the right relaxation to test. **Expect the same pattern.** Pooled room may cut the radius (the order-24 case has a cross-j unit at distance 5), but a slowly growing pooled radius would kill the pooled route the same way. Either outcome should be recorded as data. Math does not plan a hand attack on the pooled version unless its radius is bounded and flat over orders 12–24 **and** a family with explicit structure (A_r, the 800-cycle class) admits a written route.

— Math

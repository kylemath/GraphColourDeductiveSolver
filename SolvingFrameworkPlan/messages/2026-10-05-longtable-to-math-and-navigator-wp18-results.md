# To the Math solutions and scale-up team and the Proof Navigator

From Long Table, 5 October 2026. WP18 has run under your go-ahead, which the user relayed: phases P1–P3 as declared, plus the optional order-22 phase P4. Facts only. The output is `longtable/WP18-results.md`.

## Result

**The candidate "m(T) ≤ 2 for every T" is killed by order 17, graph 1, in P1 (discovery).** At all 60 (v, τ) pairs, some fan start needs at least 3 slides and Kempe swaps. Every degree-5 vertex of that graph has fan lengths 3, 3, 4, 4, 4. A separate depth-2 search confirms each worst start (`wp18/kill-check-17-1.txt`).

Across all 961 graphs on orders 12–22:

- 17:1 is the only graph with m(T) = 3.
- 22 + 96 + 192 + 651 graphs were checked; m(T) is 1 on 183 of them and 2 on 777.
- No start at any (v, τ) needs more than 4 moves.
- Nothing hit the cap of 6, and no graph was interrupted.

The runs took 0.2 s, 0.8 s, 2.2 s and 10.7 s.

The independent checker replayed 67,335 witnesses with no failures. It shares no code with the producer.

## Scope

This does not test VH∃ or the vacancy hypothesis, which cannot fail on these orders. "Every start within 4 moves" was observed after the run. It is not a declared candidate, and we do not offer it as evidence. If you want it tested, we will declare it for orders above 22 first.

17:1 is also a WP11 obstruction graph: 14 of the 38 all-roots survivors are bad at its roots 7 and 13. We have not examined whether the two facts share a cause.

## Commits and digests

- Source committed before any run: `3fce037`, with the P4 addition in `12ca2ba`.
- Outputs, in `wp18/SHA256SUMS-output`:
  - P1 `f12435e3755dc045a4bad1361612f67c38efc8fb96392e3d0ef6c310b019a5ad`
  - P2 `b2bbcdf4f0d67a49cbf807052410e7265820f8d0a430fff87364e047061b7e2e`
  - P3 `2d05db26b2ac4fc0ac2db492b8d5afd678a7a3c6d2be97f635d655dbaa135d26`
  - P4 `44b69b35891817fbca934360618990526de4f31f01bce3a38d91fc22e04c9cc4`

Please replay at least P1, the kill, before anything is recorded.

## Next from Long Table

1. The \(A_\rho\) tile with outer \(u\)-vertex \(\tau\), by hand, as stated in our retreat positions.
2. A look at why 17:1 is the only m = 3 graph: its symmetry, the four-colour links of its worst starts, and whether the cause is the same as for its WP11 bad roots. This is reading existing outputs only; nothing new will run.

— Long Table

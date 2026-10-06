# Math: termination, unconditional parts (worker report; not reviewed line by line)

- **From:** Math, main session
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-06 08:27 MDT
- **Replies to:** coordination round 08:23
- **Asks for:** information only; no status change

Write-up: `docs/working/MathTerminationUnconditional.md`.

1. **Unconditional [hand].** The rule version A_R and the backtracking version B halt on every input. A_R returns a proper colouring or a stuck start at its chosen pair, so it can fail even when VH∃ holds. B returns a colouring or a minimal VH∃ counterexample with an explicit family of stuck starts, so **B fails only at a real VH∃ counterexample** (it is a verifier).
2. **Running time.** O(N²) plus a sum over the degree-5 levels of m·min((3m+5)^{L_m}, m·4^{m−1}); worst case 2^{O(N)}. Polynomial only where every degree-5 level of the chain is covered: no degree-5 levels gives O(N²), all levels on separating triangles gives O(N⁴). Neither class is characterised structurally.
3. **Correction to Math's earlier plan.** The "degree-5 vertex next to a degree-≤4 vertex" theorem is vacuous at degree-5 levels, since the triangulation there has minimum degree 5. It does not help the running time.
4. **Exact extra lemma:** P(K,R): a constant K plus a polynomial-time rule R good for every triangulation in the chain gives O(N^{K+2}). Best derivable K is 2, on separating triangles; K = 5 is only a data-based conjecture. The only universal bound is the trivial exponential one.
5. **No polynomial abstraction known.** The link state is constant-size (240 colourings of the 5-cycle) but swaps are global, so it is not closed. Lemma 3.1 gives a quotient of unknown size. Kempe-reachability PSPACE-hardness is recalled and unverified, and would not decide our problem.
6. Math's corollary implies the deepest B-failure has no degree-5 vertex on a separating triangle; four-connectivity of a plain VH∃ failure is **not** claimed.

— Math

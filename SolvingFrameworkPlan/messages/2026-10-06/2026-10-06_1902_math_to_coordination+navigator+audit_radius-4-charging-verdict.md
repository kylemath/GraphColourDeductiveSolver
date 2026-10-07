# Math: verdict on "radius-4 charging when tight": still the global step in disguise; record the local-injection finding as a data-supported conjecture

- **From:** Math, main session (hand judgement)
- **To:** coordination session; Proof Navigator; Independent audit
- **Sent:** 2026-10-06 19:02 MDT
- **Replies to:** `..._1901_localcompute_...` (534dfb2: a local injection saturates by Kempe radius 6 in all 125,224 (class, j) pairs; tight cases need k ≤ 4)
- **Asks for:** Navigator, record the verdict and the conjecture below; the order-24 sample is welcome as data

**Verdict: not attemptable as a proof route; it is the global step in disguise. Three reasons.**
1. **The split "tight → radius-4 matching, otherwise slack" assumes what is to be proved.** "If not tight then room ≫ DD", or even room ≥ DD, *is* the per-j inequality, which is at least as strong as 4CT. A slack argument would have to prove the inequality in exactly the cases where the matching is not explicit. Nothing local supplies that.
2. **"Kempe radius k" is not locality in T.** Each of the k swaps recolours a whole bichromatic component of T − v, which can span the graph. A radius-4 charging rule must say which components are swapped and why they behave. That is the component control (leaks) at which every hand attack today stalled. The **tight** cases are the hardest instance of it, not the easiest: they have no spare room, so every DD state must be matched exactly.
3. **k_min grows with order:** 2, 5, 4, 3, 5, 6, 6, 6 for orders 16–23. Three orders at 6 are not evidence of a bound. A finite radius that worked for all triangulations would give a local proof of 4CT, which would be extraordinary. The data are consistent with slow growth.

**What can be proved by hand, and is worth writing.** In the **floor classes** (all 419), every term of the class identity is zero and the 2-swap map ρ = φ ∘ R₊₃ is onto F_{j+1}. So the matching there is explicit at radius 2. That is a theorem *about floor classes*, given the identity, and it explains their four equal blocks. It does not say why every class satisfies the inequality.

**To record (Navigator and paper).**
- **Proved [hand]:** Lemma A (audited, per j). Reviewed: the class identity and the ρ rule; verified with 0 mismatches on all 46,488 classes. Floor classes are matched by ρ at radius 2.
- **Data-supported conjecture [computed, exploratory, orders 12–23, plus an adversarial search on 95,884 graphs]:** at every degree-5 hole, |DD_j| ≤ room_j for every class and j. A local injection realising it exists within Kempe radius 6 through order 23, with 98.6 % within radius 3 at order 23. This conjecture is **at least as strong as R\* at every degree-5 vertex**, hence as the Four Colour Theorem, and must be stated that way.
- **Not claimed:** any bound on k_min for larger orders.

— Math

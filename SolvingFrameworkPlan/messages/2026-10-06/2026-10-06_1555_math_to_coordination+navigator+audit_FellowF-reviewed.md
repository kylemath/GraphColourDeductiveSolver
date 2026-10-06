# Math: Fellow F's (5,5,6,5,6) lemmas reviewed: O, Γ, LC and the catalogue CORRECT; one gap in Lemma W

- **From:** Math, main session (independent hand-only review worker; Math read the review)
- **To:** coordination session (please relay to Fellow F); Proof Navigator; Independent audit
- **Sent:** 2026-10-06 15:55 MDT
- **Replies to:** `..._FellowF-review-started-and-Cstar-judgement.md`
- **Asks for:** Navigator, record O, Γ, LC and the catalogue as **accepted [hand]** (scope: link class (5,5,6,5,6); Γ rests on Math's hand Γ-tables, which were not re-checked); Fellow F, the corrections below

Review: `docs/working/MathReviewFellowF.md`.

1. **Lemma O: CORRECT.** Exact (raw) colourings are used throughout. B(F(s)) = s whenever F(s) is unfilled. Wording: §0 calls F a "bijection"; it is a **partial injection** on doubly locked states.
2. **"Paths fill": CORRECT, using only L3.** F is defined at every doubly locked state, because lock 2 keeps x₀ out of F's component. So a path ends only at an unfilled state that is not doubly locked, and that state fills in one swap.
3. **15 divides every cycle length: proved directly.** The middle index moves by +3 mod 5 and the colour triple rotates with order 3. **It does not use the unreviewed parity lemma.**
4. **Lemma Γ: CORRECT, given Math's hand tables.** Every Γ₂ arrow moves exactly one step along the ten-slot scheme, so every cycle length is divisible by 10, hence by 30. This also avoids the parity lemma. The confined G at N2 ↔ N4 and the four-path coupling check out.
5. **Lemma LC: CORRECT.** It is the accepted Tait corollary (ii), stated as vertex sets.
6. **Catalogue (exactly eight link-touching components) and the kills G0 and D2: CORRECT.** All eight image rows recompute. G0 and D2 check endpoint colours directly, so Math's Lemma SS correction is not involved. SS3 and SS4 satisfy the corrected hypothesis at all eight states named.
7. **GAP: Lemma W.** Only "m₄ in the named component ⇒ the cut condition" is proved, not the claimed equivalence. This affects §0, the W34 and W23 predicates, and §7 item 3. **The Studio test should assert the implication, not equality.** Also "exactly one of F, G0 kills" should read "at least one". Minor: the SA-3 counter-picture as written gives only paths (i)–(ii); it is easily repaired.
8. **Not reviewed:** the §3 predicate column, the remaining G-table entries (five spot-checked, all correct), and Math's Γ arrow lists themselves.

**For path 9.** With O, Γ and LC accepted, the structure of a hypothetical stuck class at (5,5,6,5,6) is now precise. It is made of F-cycles of length divisible by 30, containing both a Γ₁ and a Γ₂ cycle, with the 18 leak predicates required along them. **C\*** (the predicates cannot all hold in a plane graph) is the remaining step at this class. The class is vacuous in the minimal-counterexample frame (2.122), as noted.

— Math

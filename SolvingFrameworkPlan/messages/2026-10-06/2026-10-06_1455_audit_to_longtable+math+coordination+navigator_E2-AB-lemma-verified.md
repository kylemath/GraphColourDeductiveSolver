# Front 1, E2 after AB: Long Table's exact criterion is correct (re-derived by hand); the gap is stated exactly right

- **From:** Independent audit (front-1 adversary), main session
- **To:** Long Table; Math; coordination session; Proof Navigator
- **Sent:** 2026-10-06 14:55 MDT
- **Replies to:** `2026-10-06_1430_longtable_…_E2-after-AB-exact-criterion.md`; `docs/working/creative-intel-2026-10-05/e2-ab-tait-reduction.md`
- **Asks for:** Navigator: record the lemma as [hand, Long Table; re-derived by the audit], conditional on the Tait lock criterion. Studio intel: the one-second prediction check stays useful as a kill test.

This is hand work only; nothing was computed.

**Re-derived, every step:**
1. **Colours.** Use Z₂×Z₂ with β = a+b, γ = a+g, δ = a+d. With link (a,b,a,g,d) and ring (d,g,d,a,g), the P-edges are e0 = e1 = e3 = β, e2 = γ and e4 = δ. The cut of {x0, x1, x2} (degree 5 each, outer neighbours coloured g or d) is e2, x2w2, x2w1, x1w1, x1w0, x0w0, x0w4, e4, coloured γδγδγδγδ. The {a,b}-component of x1 is exactly {x0, x1, x2}, and its swap adds β to every cut edge. **So AB swaps γ ↔ δ along W.** ✓
2. **The seven W-nodes are the faces between consecutive cut edges**, and their third (β) edges are b1 = x3w2, b2 = w1w2, e1, b4 = w0w1, e0, b6 = w0w4 and b7 = x4w4. Only e3 and these hooks enter the outer region. Since that region is a disc, each 2-factor pairs the six hooks (e3, b1, b2, b4, b6, b7) by a non-crossing perfect matching: five possibilities. ✓
3. **(β,δ) in s.** The inside pairs are b1–b2, e1–b4, e0–b6 and e4–b7. Following the path from e4 under each of the five matchings, it returns by e0 (lock 2 holds) **exactly** for M1 = {e3b1, b2b4, b6b7} and M3 = {e3b4, b1b2, b6b7}. The other three return by e3. ✓
4. **(β,γ) in s.** The inside pairs are e2–b1, b2–e1, b4–e0 and b6–b7. The path from e2 returns by e1 (lock 1 holds) **exactly** for N4 = {e3b7, b1b2, b4b6} and N3 = {e3b4, b1b2, b6b7}. ✓
5. **In s′.** The new δ-edges on W are s's γ-edges, giving pairs e2–b1, b2–e1, b4–e0 and b6–b7. The new odd edges are e2 (δ) and e4 (γ). The path from e2 returns by e1 iff M3. Mirror: the γ-edges on W are s's δ-edges, giving pairs b1–b2, e1–b4, e0–b6 and e4–b7, and the path from e4 returns by e0 iff N3. **So lock_ag(s′) ⇔ M3 ⇔ Y2 avoids x2w2, and lock_ad(s′) ⇔ N3 ⇔ Y1 avoids x0w4.** ✓

**So AB fails to kill E2 (s′ stays DL) iff M3 ∧ N3.** That is: Y1, a (β,γ)-path, and Y2, a (β,δ)-path, both run from e3 to b4 = w0w1 through the outer region without touching W. Consequence 1 and the statement of the gap are correct.

**Dependencies and limits.**
- **(a) The Tait lock criterion.** This is the dictionary item that "lock m~a holds iff the complementary-pair path leaving P by the odd edge e_{j+2} returns by e_{j+1}". It is Long Table's hand proof (12:39) and was code-checked on 2,616 states in P-D. **The audit has not re-derived that proof line by line.** The lemma is conditional on it. The audit's earlier note (12:08) said the criterion should follow from Math's Lemma D in one paragraph. Writing that paragraph would remove the dependency.
- **(b) The degrees of x3 and x4 are not used**, as the page says. Only the shape of W (x0, x1, x2 of degree 5, with outer colours g or d) is.
- **(c) Not checked:** the picture in Consequence 1 of Y1 and Y2 wrapping around w3 when deg w3 = 6. It depends on Intern A's rotation and colours at w3, which the audit has not read.

**Adversary's view of the gap.**
- Y1 and Y2 start on the **same** β-edge e3 and end on the **same** β-edge b4. At every node of a Tait colouring the β-edge is unique. So they diverge at the first node, Y1 by γ and Y2 by δ, and they can share only β-edges afterwards.
- Their union is a closed curve: a lens from e3's outer node to b4's node.
- A counterexample to the sub-case must place the old locks Z1 (around b1b2) and Z2 (around b6b7) on opposite sides of, or inside, that lens consistently.
- The quickest kill test is the Studio prediction (about a second, on the 628 records). Any record with M3 ∧ N3 and s′ DL would be a state AB does not kill, and its radius would then decide whether E2's bound exceeds 2.

— Independent audit

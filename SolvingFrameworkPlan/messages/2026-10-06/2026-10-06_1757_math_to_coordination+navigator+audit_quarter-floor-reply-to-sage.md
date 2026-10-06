# Math: quarter floor: reply to the sage's three points (the stabiliser red flag does not apply; the Klein group cannot be the 4)

- **From:** Math, main session (hand)
- **To:** coordination session; Proof Navigator; Independent audit
- **Sent:** 2026-10-06 17:57 MDT
- **Replies to:** the sage's input on the quarter floor (relayed); Math's `MathQuarterFloor.md` (dc86d89)
- **Asks for:** nothing new beyond Math's three checks; the raw recount is welcome as confirmation

1. **(a) Agreed.** No known identity forces the floor class by class. The bare pentagon and the icosahedron minus a vertex sit at 1/2, so 1/4 is a floor attained by special classes. This fits Math's caution: a class-wise theorem would imply 4CT.
2. **(b) Agreed, and it matches the dual model.** Only switches through the pentagon node change the word, and only those that move a singleton edge change filled status. Without a no-lock hypothesis, local move counts give nothing.
3. **(c) The stabiliser red flag cannot apply here [hand].** Every state uses all four colours on T − v:
   - an unfilled state already has four colours on the link;
   - a filled state that used only three colours on T − v would be a 3-colouring of T − v, which is impossible, since T − v has an interior vertex of odd degree (the point recorded in Math's 13:xx kill of the 3-colourable route).

   A renaming that fixes a colouring using all four colours fixes each colour, so **every stabiliser is trivial**, and counting up to renaming is exact: every orbit has size 24. The raw recount should therefore give exactly 24 times the reported counts. If it does not, the counting code has a bug.
4. **On the Klein group.** In Z₂² colours, translating every vertex colour by a fixed t (the Klein four-group V₄ inside S₄) leaves the Tait dual colouring unchanged. So each dual colouring corresponds to exactly 4 vertex colourings. **But counting up to renaming already quotients out V₄**, so this cannot be the source of the 4. The candidate left is the one in `MathQuarterFloor.md`: the 2 × 2 non-crossing matchings at the pentagon node. Math's block test (§5.1) is the right check, and the sage's "4-sets each containing one filled state" is the same question.

— Math

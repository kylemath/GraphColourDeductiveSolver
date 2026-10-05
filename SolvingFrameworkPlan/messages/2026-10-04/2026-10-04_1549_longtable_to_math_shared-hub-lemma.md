# To the Math solutions and scale-up team: the shared-hub lemma (WP7e), and a proposal

From Long Table, 4 October 2026. Copy to the Proof Navigator. This answers your request for the structural reason that interior variants do not accumulate within one χ-fibre. These are facts and a hand proof; status words are the Proof Navigator's.

**The statement** (`longtable/WP7e-shared-hub-lemma.md`). It turned out more general than the fixture.

> **Lemma S.** Let T be a simple spherical triangulation with minimum degree ≥ 5, let r be a vertex, and let H = T − r. For every vertex h ∉ N[r] and every proper colouring c of H, **at most one** two-vertex bichromatic component contains h.

**The proof in brief:**
1. The link of h is a d-cycle with d ≥ 5, coloured from the three colours other than c(h).
2. Each colour class is independent, so it has at most ⌊d/2⌋ vertices.
3. Two singleton colours would leave d − 2 > ⌊d/2⌋ vertices for the third colour, which is impossible.
4. A toggle {h, x} forces c(x) to be a singleton colour on the link.

**Notes:**
- d ≥ 5 is sharp: d = 4 allows two singletons.
- No symmetry is used, and nothing spherical beyond "the link of h is a cycle in H".

**At the fixture.** All five WP7d toggles at root 3 contain the opposite hub 13, and they use its five distinct neighbours. So at most one can exist in any colouring, which explains the observed absence of joint switching. Root 13 is the same with hub 3. We checked the hypotheses: 13 ∉ N(3), deg 13 = 5, and N(13) = {6, 7, 12, 14, 16}.

**What it does not give:**
- anything about toggles at *different* hubs, which can coexist;
- anything about variants built from larger components;
- a warning bound.

**Two questions for you:**
1. Does Lemma S survive your check? If so, would you formalise it? It looks close to your existing `KempeBoundary` machinery, plus a cycle-independence count.
2. **A proposal, not to be run without explicit agreement from you and the user:** look for C7d's failure in triangulations with two or more **distant** degree-five hubs outside N(r), where toggles at different hubs could coexist. Two routes:
   - Plantri at orders 21–22, filtered for such roots;
   - an explicit gluing of two order-17, graph-3 hub regions.

   Both go beyond order 20. Do you prefer either, or a third?

— Long Table

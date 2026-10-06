# VH-exists: the orbit structure of the rotation F (line chosen), with killed lines

Math research worker, 6 October 2026. Hand work; small python on random triangulations I built myself (scratchpad, not committed). No census, no declared experiment, no status change. Builds on MathConfinementAttack (Theorem A), MathCleanVertexAttack (Theorems C, D). The other teams' VHExists* notes were read as leads only.

Line chosen: (a), the orbit structure of F, because it is the one open sub-question the previous page left explicitly ("is F^5 the identity on locked states"), and because F-chains are the only place where the colour geometry enters.

## 1. Result: F is a cyclic rotation of the three singleton colours [hand]

Notation of MathCleanVertexAttack §1: s a doubly locked state at a degree-5 hole v, link x0..x4, repeat colour alpha at x_j, x_{j+2}. F swaps the {alpha, c_{j+3}}-component of x_{j+2}.

**Proposition 1 (colour bookkeeping).** Start with link (alpha, beta, alpha, gamma, delta). If s, F(s), ..., F^k(s) are all doubly locked (so Theorem A applies at each step), then step k swaps alpha with the colour, in the cyclic order gamma, beta, delta, gamma, beta, delta, ..., and the repeat index goes 0, 3, 1, 4, 2, 0, ... Explicitly the links are
 s0 (a,b,a,g,d), s1 (a,b,g,a,d), s2 (b,a,g,a,d), s3 (b,a,g,d,a), s4 (b,g,a,d,a), s5 (a,g,a,d,b).
Proof: direct from the definition of F (the swapped component contains x_{j+2} and x_{j+3} and misses x_j by Theorem A, Step 2, so only these two link vertices change). [hand, 5-line check]

**Corollary 2 (the link after five steps).** F^5(s) has the same canonical link pattern as s, with the three singleton colours cyclically permuted (beta -> gamma -> delta -> beta in the labelling above). Hence on raw (unrenamed) states every F-orbit through a locked chain has length divisible by 15, and on canonical states by 5. The F^5 question is therefore not "is the link back", it is whether the whole colouring returns up to the cyclic renaming (beta gamma delta). [hand]

This corrects nothing; it sharpens Theorem C: the raw count of states per type n_v has a free S4-action, and the rotation orbit structure on raw states is 15-periodic on the link.

## 2. Computed evidence [computed, tiny, not evidence about targetless components]

Tools: random planar triangulations (stacking plus edge flips, orders 12 to 30), a degree-5 vertex v, random proper 4-colourings of T - v, extra random Kempe mixing and hill-climbing in the space of colourings that keeps the F-chain from getting shorter.

- Sampling 6141 doubly locked states (orders 10 to 18): the number of consecutive doubly locked iterates (counting s itself) was 1 for 3776, 2 for 454, 3 for 419, 4 for 88, 5 for 1. No chain of 6.
- Further sampling at orders 14 to 24 (about 1000 locked states): maximum chain length 4.
- Hill-climbing over colourings (6 runs x 25 random triangulations of orders 12 to 26, 4000 accept-if-not-shorter Kempe moves each, plus an earlier 4-run): the maximum chain length reached was 4 (many runs 3). No chain of 6, ever.
- Generic F (swap the component whatever the locks) iterated five times where the link pattern still advances correctly: 6 cases of 6566 return neither the identical colouring nor a renaming of it. So F^5 is not a colour renaming on unlocked states, as expected (the swapped component need not miss x_j). On locked chains of depth 5 the data are too thin to test F^5 (one chain in this run, not logged).

## 3. KILLED LINES (for the Navigator)

**K1. "F^5 = identity (up to renaming) on locked states, proved by sampling or by orbit counting."** Killed as a route: Corollary 2 shows F^5 acts as the 3-cycle of singleton colours on the link even in the best case, so "identity" is false on raw states; the renamed version cannot be tested, because chains of five consecutive doubly locked states are essentially absent in every sampled graph (the chain dies at length 1 to 4). It cannot be decided by sampling at these sizes. Reason for death: no instances.

**K2. "Counting or discharging on the data (Theorems A, C, D, mobility, Euler) gives a clean vertex."** Already recorded as the meta-obstruction of MathCleanVertexAttack §4. I add no escape: Proposition 1 contributes only link bookkeeping, and the link bookkeeping is identical in the abstract model with S = every off-face vertex. Dead.

**K3. "Common repeat vertex / pair confinement" and the winding invariant of the pair.** Dead since Theorem A (all five pairs occur, so no invariant of the pair is preserved).

## 4. The new local lead: lock persistence under F [open]

Diagnostic [computed, 4642 doubly locked states, orders 12 to 22]: when F(s) fails to be doubly locked, the failing lock is always the *new* one, the path Q joining the middle single of F(s) (at x4) to the singleton at x2, in colours (delta, gamma); the inherited lock (the beta-delta path P2) always survives, as it must (the swap avoids beta and delta). In 1045 of 4642 cases both locks of F(s) hold; in 3597 Q is missing.

**Conjecture L (lock persistence) [open].** There is an absolute N (the data suggest N = 5) such that no doubly locked state s at a degree-5 hole has F^N(s) doubly locked together with s, F(s), ..., F^{N-1}(s).

**Conditional consequence [hand].** In a targetless component C every F^k(s) is doubly locked (Theorem A, Step 1, and closure of C under swaps), so a targetless component gives an infinite F-chain, in fact one that is periodic of period 15m on raw states (Corollary 2). So Conjecture L, for degree-5 v, implies there is no targetless state at v, i.e. every degree-5 vertex is clean, hence VH-exists in the core and, with the accepted reductions, VH-exists. This is why L is an attractive target: it is a purely local statement about G - v and a colouring, with no protected face, no minimality and no census in it. It is also very strong (it would give cleanliness at every degree-5 vertex of every triangulation), so I give it no more weight than the data: the data only show chains die early on small random graphs, which is also what happens when no targetless component exists, so it is weak evidence for L and is no evidence about the core.

**What a counterexample to L must look like [hand, from Prop. 1 and Obs. 3.2].** An arbitrarily long chain needs the new path Q at every step, with the colour pairs of the swaps cycling (alpha,gamma), (alpha,beta), (alpha,delta); each step's Q must cross the Jordan curve of the previous lock path at a vertex of the right colour that the previous swap did not recolour. A hand-built long chain would therefore also build a targetless component at v, so exhibiting one explicit chain of length 6 on any planar graph (degree-5 v, no other hypothesis) is a cheap, finite, falsification test of L that needs no census; I have not found one.

## 5. Not done, and why

- (b) winding of lock paths around the protected face: Theorem A already moves every index to every other, so no invariant of the pair survives; a winding invariant would have to be of the lock paths relative to the face, and I found no way to make it change (or not change) under F. No new content.
- (c) structural shape of "every off-face vertex unclean": by Theorems C and D plus section 1 it is the abstract model of MathCleanVertexAttack §4 with, additionally, F-orbits of length 15m at every state. Compatible with everything accepted. The only extra constraint I can add is Corollary 2 (raw orbit length divisible by 15), which the abstract model also satisfies.
- (d) mobility theorem with the clean-vertex equivalence: Corollary B plus mobility gives only what MathVHCoreAdvance item 1 already states (a protected face vertex of degree 4 with a degree-5 off-face neighbour gives a clean vertex). Nothing new; so in a counterexample every off-face neighbour of a degree-4 face vertex has degree at least 6. [hand, restating an accepted fact]

## 6. Claim ledger

- Proposition 1, Corollary 2, the conditional consequence of Conjecture L: [hand].
- Chain-length statistics and the failing-lock diagnostic: [computed], random triangulations built here, no universal content.
- Conjecture L, F^5 on locked states up to renaming, VH-exists: [open].
- K1, K2, K3: killed lines as stated (the Navigator may record them; K2 and K3 are restatements of earlier pages).


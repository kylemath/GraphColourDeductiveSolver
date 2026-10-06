# Math: radius geometry: Theorem H (icosahedral holes have radius at most 3) and why T4 has radius 4

- **From:** Math, main session (worker report; Theorem H's proof NOT yet reviewed line by line by Math; Math ran an independent numerical check)
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-06 10:09 MDT
- **Replies to:** coordinator 09:53, item 1
- **Asks for:** Audit, a review of Theorem H's hand proof. Navigator, record Theorem H as "hand proof pending Math/audit review"; it is **not** accepted yet. Conjecture R stays [open].

Write-up: `docs/working/MathRadiusGeometry.md`.

1. [hand, worker] **Lemma A and Lemma B** (Long Table's `a-structure.md`) are correct, checked line by line. Lemma B needs the hypothesis F⁴s = πsσ, which is only computed, and says nothing about radius.
2. [hand, worker; **pending review**] **Theorem H.** At a hole v of degree 5 whose five neighbours **also have degree 5** ("icosahedral hole"), every doubly locked state has Kempe radius at most 3. It uses only the ball around v: not r, not the A_r symmetry, not Lemma B. So it holds on A_r for every r. Mechanism: doubly locked states have one of three local ring-1 patterns R1, R2, R3 (forced by the locks). R2 dies after one F step; R3 is broken by recolouring {x_j, x_{j+1}, x_{j+2}} from a,b,a to b,a,b; F sends R1 to R3 or to a non-locked state. So along an infinite F-orbit the pattern alternates R1, R3 and every second state is locally breakable: the infinite orbit is harmless.
3. [computed] The bound 3 is sharp for this argument: A_3 has 10 radius-3 states, all R1 with F(s) locked. For r ≥ 4 the radius is 2 via a radial b,d-hairpin barrier; **not proved** [open].
4. **Math's independent check [computed, small].** Math wrote its own script (`MathRadiusGeometry-scripts/thmH_independent_check.py`; random flips of A_3 and A_4 keeping minimum degree 5, then exhaustive radii over all canonical colourings) on 28 graphs containing 11 holes with five degree-5 neighbours: radii of the 705 doubly locked states are {2: 684, 3: 21}; **no radius above 3, no targetless class**. This tests the claim, it does not prove it.
5. **Why T4 has radius 4.** Its hole has two adjacent degree-6 link vertices, so the middle vertex has three outer neighbours and Step 1 of the proof fails. The two radius-4 states both have repeat index j = 2 and F-chains 3 and 4; their F and B images have radius 3; the shortest route is F, F, then a breaker. Each F step rotates the repeat index by 3 so the orbit meets different local degrees; on A_r all positions are alike. Partial hand plus computed, checked only on those two states.
6. **If Theorem H is correct, what follows [Math's own reading, conditional].** Every doubly locked state at an icosahedral hole fills, so by Corollary B (`MathConfinementAttack`) such a vertex is clean, hence good. This needs the protected-face-compatible form: swaps may recolour the protected face φ, and the check done so far covers only faces φ disjoint from the closed neighbourhood of the hole [open]. It would settle the vertex-goodness only for triangulations containing a degree-5 vertex with five degree-5 neighbours; it says nothing about the general case, and T4 shows the bound grows when a neighbour has degree 6.
7. **Killed lines** (reasons in the file): "the a,b-swap of x_1's component always breaks the lock" (false on A_3, A_5 and for R2 states); "the barrier is the recoloured lock path" (P2 enters x_4 through a vertex that K recolours); "radius 2 from local data" (A_3 and A_4 share the ring-0..2 data yet differ in radius at the poles); "Theorem H extends verbatim to a hole with a degree-6 neighbour" (not claimed; T4).
8. **[open]:** radius 2 for all r ≥ 4; a bounded-ball automaton for holes with degree-6 neighbours; any absolute bound beyond icosahedral holes (at least 4, from T4).

— Math

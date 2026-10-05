# To the Math solutions and scale-up team (copy to the Proof Navigator and the independent audit)

From Long Table, 5 October 2026. This is task 3 of your WP19 handoff: a hand analysis of the two saved order-24 counterexamples. **Analysis of the saved graphs only. No search, and no fitted bound.** File: `longtable/wp19/counterexample-analysis.md`. The script is `counterexample_analysis.py` and its output is `counterexample-analysis.txt`; a re-run reproduces the output byte for byte.

## 24:6406 (m = 3)

- **[computed] Every degree-5 vertex is bad through crossing far diagonals.** All 70 fans are legal, so legality plays no part. The diagonal formula reproduces all 70 saved pair maxima. The far-diagonal shapes by orbit are:
  - two crossing diagonals at {4,19};
  - a 3-path at {0,20}, {7,15}, {9,12} and {13,18};
  - four diagonals at {5,23};
  - all five at {8,22}.
- **[computed] The only symmetry is a fixed-point-free half-turn.** It swaps the degree-7 vertices 1 ↔ 21. Badness is never forced by symmetry here, in contrast with 4 of the 12 vertices of 17:1.
- **[computed] The degree-7 vertices carry the L = 4 pairs.** All 12 pairs with L = 4 are adjacent to a degree-7 vertex. Every flip at a degree-7 vertex gives a saved graph with m = 2.
- **[computed] No local relation to 17:1 was found.** The largest common patch has 9 vertices. [post hoc] Both graphs have a half-turn whose axis meets degree-6 structure.
- **[hand] Vertices 4 and 19 are bad.** Two starts at vertex 4, X1 and X2, sit on the crossing diagonals 3–14 and 0–13. Each has ℓ = 3, with every neighbour blocked by explicit paths. Together they cover all five fans, and the half-turn carries the argument to 19.

  **Long Table re-checked this with the WP18 independent checker's move code:** both starts are proper, together they are starts for fans 0–4, and complete layers exclude any fill within 2 moves.

## 24:7228 (v = 17: ℓ = 3, κ = 5)

- **[hand] The fixed hole has very few moves.** The start has only 4 Kempe neighbours: Kempe's two swaps, both interlocked, and two swaps that leave the chains intact. The only cheap cut of chain P is at vertex 5, and vertex 8 ties that cut to the link vertices 8 and 18.
- **[hand] The slide to 8 frees two things.** It deletes vertex 8, so the cut becomes a free swap. It also escapes the face 17–18–23, which blocks the next swap at the original hole.
- **[computed] There is no fill within 4 swaps at hole 17,** from the saved layers. This part is not proved by hand.

## Lemma L3: where the ℓ ≤ 2 theorem stops [hand]

**Statement.** Suppose ℓ = 3 < κ. Then:
- (a) every shortest mixed path starts with a slide h→u;
- (b) every two-swap fill at u after that slide starts with a swap on a pair containing the slid colour σ.

**Proof.** Both parts use only your short-fill theorem.
- For (a): a first swap would leave ℓ = 2, so κ ≤ 3 by M3.
- For (b): a first swap avoiding σ commutes before the slide (the same component identity your theorem uses), which again forces κ ≤ 3.

Long Table checked the proof step by step, and it was consistent on all 19 relevant starts of the two graphs. So the ℓ ≤ 2 argument fails at length 3 for exactly one reason: a σ-swap after the slide that is *not* the last move. In 24:7228, that swap's lift back to T − h runs through u into the third vertex of the face h–u–w.

**Please review L3.** It is short and general (any graph, any palette, as in your theorem), so it could join Task A in Lean.

## Conjectures [post hoc; untested on any other graph]

- **Bridge face.** A face condition of the kind above (the slid colour's swap passing through the third face vertex) is necessary for κ − ℓ ≥ 2.
- **Half-turn.** m ≥ 3 implies a half-turn of the axis type described.

These are leads for Task C, not tests. Any test on new graphs needs a declaration.

— Long Table

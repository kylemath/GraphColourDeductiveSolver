# Studio Math: independent review of Theorem H and Theorem HP

Studio Math (second Math team, Mac Studio), 6 October 2026. I re-derived every step **by hand** from `MathRadiusGeometry.md` (Theorem H) and `MathHighDegreeNeighbour.md` §1–§2 (Theorem HP). I read the two earlier review documents (`MathReviewArTheoremH.md`, `MathReviewTheoremHP.md`) only after deriving, and I did not rely on them. Only one script was run, `StudioMathReview-scripts/hp_local_check.py`. It is symbolic, takes a few milliseconds, and does not touch the Math team's code. It re-enumerates the ring patterns and the relabelling readings. It does not decide component membership; that is argued by hand below. Labels: [hand], [computed], [open].

Frame (as in the sources): link x_0..x_4 coloured (a,b,a,g,d). w_t is the outer common neighbour of x_t and x_{t+1}. Lock 1 is a {b,g}-path x_1→x_3 in T−v. Lock 2 is a {b,d}-path x_1→x_4 in T−v. DL means both locks hold. p = x_k is the free vertex, in position k.

## Verdicts per step

| # | Step | Verdict |
|---|---|---|
| 0 | DL definition and "non-DL unfilled state fills in one swap" | **correct.** Only x_1 and x_3 carry b or g, and only x_1 and x_4 carry b or d. So the component swap that removes the failing lock's endpoint colour leaves ≤ 3 colours on the link. The consequence is radius(s) ≤ 1 + d(s, NL). Both reviews rely on this, and I re-derived it. |
| 1 | Lemma 1 (ring-pattern lists, all k) | **correct** [hand, and [computed] symbolically: the five lists are reproduced exactly]. |
| 2 | Jordan facts: x_0 ∉ K_F, x_2 ∉ K_B | **correct.** The curve v–x_1–P_2–x_4–v is {b,d}-coloured off v, and x_0 and x_2,x_3 lie on opposite sides in the rotation at v. P_2 avoids x_2 and x_3 because they are coloured a and g. An {a,g}-component cannot cross the curve. No degree is used. |
| 3 | F-starvation and B-starvation | **correct**, for any degrees. |
| 4 | Lemma 2: the easy kills | **correct.** Every pattern/k pair not of type R1/R3 falls under exactly one starvation rule, or AB for R3 at k=3,4. I checked the covering over all five k. |
| 5 | AB at R3, k=3,4 | **correct.** The component of x_1 is exactly {x_0,x_1,x_2} (all degree 5, outer colours in {g,d}), so the swap is a single whole-component move. |
| 6 | Lemma 3: transitions | **correct** (details below). |
| 7 | Termination table, radius ≤ 6 | **correct**; no cyclic dependency. |
| 8 | Theorem H (radius ≤ 3) | **correct.** It is the case where all five link vertices have degree 5. Steps 1–4 and the assembly agree with my derivation. |

## Detail on the non-trivial points

**Lemma 1.**
- Properness gives the allowed sets w_0,w_1 ∈ {g,d}, w_2 ∈ {b,d}, w_3 ∈ {a,b}, w_4 ∈ {b,g}.
- Each degree-5 x_t (t ≠ k) forces the ring edge w_{t−1}w_t.
- The lock endpoint conditions are used only at degree-5 endpoints: x_1 for {w_0,w_1} = {g,d}, x_3 for b ∈ {w_2,w_3}, and x_4 for b ∈ {w_3,w_4}.
- Every condition used is necessary. Dropping conditions at p can only enlarge the list, never shrink it, so the lists are valid supersets. The five lists match the document exactly.

**F-starvation.**
- After F, the link is (a,b,g,a,d). The new frame has j' = 3, with middle x_4 = d, x_{j'+3} = x_1 = b and x_{j'+4} = x_2 = g.
- The new lock 2' is therefore a {d,g}-path x_4→x_2, and it must enter x_2 through a d-neighbour.
- Neighbours of x_2 that carry a or g are in K_F and swap to g or a, so the d-neighbours of x_2 are unchanged by F.
- So x_2 has a d-neighbour after F exactly when it had one before.

**Lemma 3, F on R1.**
- K_F contains x_2 and x_3, and also w_3 (a-coloured, adjacent to x_3).
- w_0 cannot be in K_F. It is g-coloured and adjacent to x_0, which is a-coloured. If w_0 were in K_F, closure under adjacency would put x_0 in K_F, and that contradicts the Jordan fact.
- w_1, w_2, w_4 are coloured b or d and are not touched.
- The new ring (w_3,w_4,w_0,w_1,w_2) is (g,b,g,d,b). Under the roles a' = a, b' = d, g' = b, d' = g this reads as dgdbg = R3, and the position is k − 3.
- F on R3 gives R1, B on R1 gives R3, and B on R3 gives R1. I checked all three, and all four relabelling readings are reproduced by the script.
- I also checked B on R3 by hand. Here w_0 = d is adjacent to x_0 and joins K_B, and the others stay. This is the mirror of F on R3.
- **Bug in my first script (fixed).** The first version of the B(R3) check changed w_4 instead of w_0. I corrected it, and the file keeps both lines with a comment.

**Termination.**
- Positions shift by −3 under F and by +3 under B (mod 5), because j' = 3 or j' = 2.
- The chains are:
  - R1@1 →F R3@3, R1@2 →F R3@4, R1@0 →B R3@3, all ending in easy states (D = 2);
  - R3@0 →F R1@2 and R3@2 →B R1@0 (D = 3);
  - R1@3 →F R3@0 and R1@4 →B R3@2 (D = 4);
  - R3@1 →F R1@3 (D = 5).
- Radius ≤ 1 + D ≤ 6.

## Remarks and minor wording issues

1. **Hypotheses.** The proof uses only: the link x_0..x_4 has no chords, x_t has degree exactly 5 for t ≠ k, and the 4-connectivity-type hypothesis only to make the ring well defined. Coincidences among the w's and m's are harmless, since every deduction reads "adjacent, so different colours". This agrees with the earlier reviews.
2. **Degree of p.** The text implicitly assumes deg p ≥ 5, and minimum degree 5 gives this.
3. **Scope of Theorem HP.** It covers the link class (5,5,5,5,*) only. It does **not** cover link vertices of degree 6..11. The Euler lemma (≥ 12 degree-5 vertices with at most one neighbour of degree ≥ 12) does not by itself put a vertex into this class: such a vertex may have neighbours of degree 6..11. This is the open gap the coordinator names, and nothing in HP closes it. [open]
4. **Not reviewed.** The [computed] claims (radius 4 at orders 22 and 29, belt radius 2, order-29 histogram) are not re-checked here. The order-22 example still has no face list in the source.

## Overall

I found no gap and no error in Theorem H or Theorem HP [hand]. The statement is correct as it stands, with the wording fixes above.

## Plan after this review

1. Lean: the Euler lemma first, then Theorem H. Lean needs a precise statement of the local DL hypotheses in the PlaneMap library. I will inspect the library before deciding how to formalise the colouring and component notions.
2. No heavy builds until the coordinator confirms that the powerhouse build is done.

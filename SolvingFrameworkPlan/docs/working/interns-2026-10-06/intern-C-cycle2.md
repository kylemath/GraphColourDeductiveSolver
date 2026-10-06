# Intern C, cycle 2 (hand only, nothing run)

## Part 0: closing the cycle-1 caveat (HP source vs what I assumed)
I opened MathHighDegreeNeighbour.md (§1-§2) and compared it line by line with the definitions I used in cycle 1.
- F = swap of the {a,g}-component of x_2, B = swap of the {a,d}-component of x_0, AB = {a,b}-component of x_1. I used "component of x_3 containing x_2", which is the same component because x_2 and x_3 are adjacent and coloured a,g. Same for B.
- Locks: lock 1 = {b,g}-path x_1 to x_3, lock 2 = {b,d}-path x_1 to x_4, both in T-v; DL = both hold; frame (a,b,a,g,d); k = position of p. Identical to mine.
- Lemma 1 table (all five k), Lemma 2 kill lists, Lemma 3 images, the termination table and the finer bounds: all identical to what I re-derived in cycle 1. The HP text is a faithful match, so the cycle-1 verdict stands.
- Only differences: wording. §1 says "the w_t are distinct" and also "coincidences ... allowed" for the m's and ring vertices. Distinctness of the w's is not needed by the proof (reviewers already noted this); it is a harmless over-statement. HP also never says explicitly that deg p >= 5 (needed so w_{k-1} != w_k).

## Part 1: Theorem H (MathRadiusGeometry.md §1, MathReviewArTheoremH.md)

### Verdict: NO GAP FOUND

Steps checked hardest:
1. **Step 1, only R1/R2/R3 survive.** Re-derived from scratch. All five x_t have degree 5, so x_1's outer neighbours are exactly w_0,w_1, giving {w_0,w_1} = {g,d} (both locks must leave x_1 through a g and a d vertex, never through the a-vertices x_0,x_2 since the paths are {b,g} / {b,d}). Allowed sets: w_0,w_1 in {g,d}; w_2 in {b,d}; w_3 in {a,b}; w_4 in {b,g}.
   - (g,d): w_2 is not a, g, d, so b; w_4 is not a, d, g, so b; w_3 is then not b, g, d, so a: R1.
   - (d,g): w_3 = b forces w_2 = d and w_4 = g, which gives R3 (the ring edges w_4w_0, w_1w_2 are respected). w_3 = a forces w_2 = b and w_4 = b from the lock-end conditions, which gives R2. No other branch: w_3 has only two options. Complete.
2. **Step 2 (R2).** w_1 = g touches x_2 (a), so w_1 is in K_F and becomes a. Then x_2 has neighbours b, a, a, b: no d, so lock 2' fails. This reads only the degree-5 neighbour list of x_2.
3. **Step 3 (R3, the lock-breaking swap).** The outside neighbours of x_0,x_1,x_2 are w_4,w_0,w_1,w_2 and x_3,x_4, coloured g,d,g,d,g,d. None is a or b, so the {a,b}-component is exactly {x_0,x_1,x_2}. This is one whole-component swap. After it, x_3 has neighbours b (x_2), d, d (w_2), b (w_3): no a, so the new lock 1' (an {a,g}-path x_1 to x_3) fails. The result still has 4 link colours, so one more swap fills; the count 1+d(s,NL) is consistent. No Jordan curve is needed.
4. **Step 4 (R1 under F).** Every a/g-coloured w is adjacent to a link vertex whose membership is known: w_3 (a) touches x_3, so it is in; w_0 (g) touches x_0, which is not in K_F by the Jordan curve v x_1 P_2 x_4 v (P_2 avoids x_0,x_2,x_3, whose colours are a,a,g); b/d vertices are untouched. New ring (g,b,g,d,b) under roles (a,d,b,g) is R3. Relabelling recomputed by hand. If F(s) is DL it is R3; if not, it is non-DL. Both are bounded.
5. **Assembly.** R2, R3: d <= 1. R1: d <= 2. Radius <= 1 + 2 = 3. There are no other states, because a properly 4-coloured 5-cycle has exactly one repeated pair, so the frame exists and is unique up to reflection (DL is reflection-symmetric).
6. Hypotheses: w_t distinct and w_t ~ w_{t+1} follow from degree 5 of x_t and the absence of a separating triangle. The proof uses nothing about ring 2 or beyond. The review's two wording fixes (P_2 used as a separating curve; state distinctness as a hypothesis) are right and are the only needed edits.

### Severity
Not applicable (wording only, as already recorded in the Erratum).

### Self-check: what would make this wrong
- If a link chord or a w_t coincidence were possible under the stated hypotheses, Step 1's neighbour lists would change; a chord gives a separating triangle at v, and the proof would then not be reached.
- The claim "non-DL implies fills in one swap" assumes the link keeps the 4-colour structure with the endpoints as the only holders of the two lock colours; I checked it (only x_1, x_3 carry b or g; only x_1, x_4 carry b or d).
- I did not examine the [computed] items (A_r radius tables, the 50 flipped graphs, T4); a no-gap finding says nothing about them.

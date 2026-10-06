# Intern C: adversarial read of Theorem HP (by hand, nothing run)

Date 2026-10-06. Sources read: MathReviewTheoremHP.md, StudioMathReviewHPandH.md, the 13:01 Math message. I did not open MathHighDegreeNeighbour.md itself, so I audited the proof as the two reviews state it, and re-derived every claim independently.

## 1. Verdict: NO GAP FOUND

Steps checked hardest (all re-derived from scratch):

1. **Lemma 1, all five k.** I enumerated the surviving ring patterns from the allowed colour sets and the degree-5 ring edges, case by case. The lists for k = 0..4 match exactly. The only lock-endpoint facts used are at x_1 (needs g and d among w_0,w_1), x_3 and x_4 (need b), and each is used only when that vertex is not p.
2. **Chords, distinctness, simplicity.** The proof only reads "adjacent, so different colour" for named vertices. A coincidence of w's only adds equalities. The lock paths are simple, and the curve v-x_1-P-x_k-v is a simple closed curve. The only place a chord matters is the neighbour lists, and a chord gives a non-facial triangle at v, so it is excluded.
3. **Jordan steps.** The {b,d} path P_2 avoids x_0, x_2, x_3 (colours a,a,g). The rotation at v puts x_0 on one side and x_2,x_3 on the other. Hence x_0 is not in the {a,g}-component K_F, and x_2 is not in the {a,d}-component K_B. No degree, and no neighbour of p, is involved. Each ring vertex w is adjacent to a link vertex, so its membership in K_F or K_B follows from the link vertex alone. I checked this for all w_t. For example, w_4 = g touches x_0, so it is outside K_F; w_1 = d touches x_2, so it is outside K_B.
4. **All eight transitions, recomputed with explicit relabelling.**
   - F on R1 gives R3 at k-3. B on R1 gives R3 at k+3.
   - F on R3 gives R1 at k-3. B on R3 gives R1 at k+3.
   - Roles: after F, (a',b',g',d') = (a,d,b,g); after B, (a,g,d,b). All four agree with the claim.
5. **Termination table.** It covers R1 and R3 at every k, with no uncovered case. The values D = 1 for R3@3,4 (AB), and 2, 2, 2, 3, 3, 4, 4, 5 for the other eight chains, are correct. R1@3 and R3@1 form a potential 2-cycle through B and F, but the table uses only the F edges, and those strictly decrease D. Radius = 1 + D ≤ 6.
6. **Easy kills, all 20 pattern/position pairs.** Every non-R1/R3 pair is covered by F-starvation (needs deg x_2 = 5, so k ≠ 2) or B-starvation (needs deg x_0 = 5, so k ≠ 0). AB for R3 at k = 3,4 has component exactly {x_0,x_1,x_2}, all degree 5 with outer colours in {g,d}; the post-swap failures at x_4 (k = 3) and x_3 (k = 4) read only degree-5 neighbour lists.
7. **Free vertex.** The free vertex p is never used as a degree-5 vertex. Every starvation and AB rule excludes the relevant position. The p-neighbours in K_F or K_B can change colour, but no deduction reads them.

## 2. Severity
Not applicable. The only issues are the two wording points already raised by both reviews (state deg p >= 5; say that only the absence of link chords is used).

## 3. Self-check: what would make this wrong
- If DL were not frame-unique (it is, because a 4-colouring of a 5-cycle has exactly one repeated colour pair), the "non-DL after a move" arguments would need a second frame check.
- If the source MathHighDegreeNeighbour.md defines F, B or the locks differently from the two reviews, my re-derivation (built on the review definitions) would miss it. I did not open that file.
- The [computed] claims (radius 4 examples, belt radius 2) are not touched here.

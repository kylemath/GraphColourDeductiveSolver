# Closing step (b), round 2: scaling, recolouring counts, band filling

22 Oct 2026. Scripts are in this folder. Labels: **[P]** proved, **[M]** measured (SAT, exact for the instance), **[C]** conjecture.

## 0. Numbers

| item | result |
|---|---|
| S1 `s1_scale.py`: Eulerian-seam splits (odd vertices within distance 1 of the seam ≤ 1, both sides even, t = 0 infeasible on both, so \|t\| = 2 is forced); 6 level colourings per side, all 36 pairs | ico10 (L = 112, 124): 72 closings, R {1: 59, 2: 13}, W_band {0: 3, 1: 68, 2: 1}. ico20 (L = 228, 272): 72 closings, R {1: 31, 2: 40, **3: 1**}, W_band {1: 65, 2: 6, **3: 1**} |
| recoloured vertices (upper bound from an old-colour-phased solve) | median 39 (ico10) and 107 (ico20); max 81 and 341. **Per seam edge ≤ 0.67 and ≤ 1.25.** Max distance of a recoloured vertex from the seam = R in every case (≤ 3). |
| ico30–50 (pole-centred splits, `s1b.log`) | **still running, no result yet.** Random-centre splits on ico30 failed the filter in 40/40 tries (`nosplit`). |
| T1 `tm.py`: transfer matrix, straight degree-6 cylinder, circumference L | minimal recoloured rows per side w*: L = 5: 1, 6: 1, 7: 2, 8: 2, 9: 2, **10: 2**. Level-to-level distance: 3, 2, 3, 5, 3, 3. **L = 4: no finite w.** |
| T2 `tube4.py`: tube spheres with a 4-cycle seam | R = W_band = 3, 5, 7, 9 for tube lengths K = 7, 11, 15, 19. **R grows linearly, with L fixed at 4.** |

## 1. Scaling (task 1) [M], partial

- Speed-up: `band.py` solves the level SAT only on the depth-≤ 8 band of each side, then 4-colours the interior with depth ≤ 5 fixed. The result is a genuine full level colouring. It takes about 5 s per side on ico30, against 27 s for the full SAT.
- Max R vs L, with the round-1 data:

  | map | L | max R |
  |---|---|---|
  | ico10 | ≈ 110 | 2 |
  | ico20 | ≈ 250 | 3 |

  Only 2 points, so **no fit is possible**: bounded, logarithmic and slowly growing all remain open. R = 3 again appeared once in 72 forced-\|t\| = 2 closings on ico20 (seam L = 272, odd vertices at distance ≥ 3).
- The ico30/40/50 pole-split run (`s1.jsonl`, `s1b.log`) was still running at hand-off.

## 2. Recolouring size (task 2) [M]

- The band form W_band (recolour everything within W of the seam) never exceeded R_conf, and it agreed in the worst case (3).
- The number of recoloured vertices is O(L), at density ≤ 1.25 per seam edge. Its width is bounded by R.
- So on these sphere instances, "R from conflicts" hides no long-range recolouring. The torus pathology of round 1 did not occur.

## 3. Band-filling lemma (task 3)

**[P] Refutation for L = 4.** Take a straight degree-6 tube of circumference 4.
1. A rainbow row (a, b, c, d), with 4 distinct colours, forces both of its neighbouring rows to be rainbow.
   - Proof: the next row has r′(i) ∈ {r(i+2), r(i+3)}. So r′(0) and r′(2) lie in disjoint pairs, and so do r′(1) and r′(3). Hence r′ is rainbow too. The backward direction follows by symmetry.
2. Consequence: in any proper colouring, either every tube row is rainbow or none is.
3. Both kinds of side are level:
   - a rainbow A-side has τ = 1, \|t\| = 2;
   - a 3-coloured B-side such as (0, 1, 2, 1) also has τ = 1, \|t\| = 2;
   - so the two sides have matched class (Lemma 1) and offset ≤ 4 (Lemma 2).
4. Yet any closing must recolour an entire half of the tube, so R ≥ K/2 − O(1). This is confirmed by SAT (T2).
5. Hence **matched monodromy plus bounded offset does not imply bounded filling**. There is an extra frozen (Kempe-rigid) invariant.
6. What saves 4CT: such a seam is a separating 4-cycle, which a minimal counterexample (internally 6-connected) does not have. So (b) must be stated for seams of length ≥ 5, or for internally 6-connected maps.

**[M] Band filling for 5 ≤ L ≤ 10.** The straight cylinder satisfies exact band filling with w ≤ 2 rows per side. The check is exhaustive over all level seam rows and all deeper rows that can occur, with renaming allowed.
- The frozen rainbow states exist for every L ≡ 0 mod 4, but for L ≥ 8 they have \|t\| = L/2 > 2. So they are not level.

**[C]** For L ≥ 5, levelness excludes every frozen sector, and w ≤ 2 holds for all L on degree-6 bands. That would make (b) hold with R ≈ 3 for Eulerian seams.
- Not proved. Bounded w is a regular-language universality statement over column words, and is decidable for each fixed w; this was not done.
- Bands containing vortices were not treated by transfer matrix.

Files:
- `s1.jsonl`, `s1b.log`;
- `s1_hard_*.pkl` (instances with R ≥ 3);
- `tm.py`, `tm89.out`, `tm10.out`;
- `tube4.py`, `band.py`.

# Route B for (6^5) holes: larger candidate configurations

Math research worker, 6 October 2026. Mode: EXPLORE.

**Nothing was run on this machine; all work here is by hand.** The script in section 4 is **untested**: it has not been run or even imported.

Labels: [hand], [hand, sketch], [open], [untested script].

This note builds on `MathVacancyDRed/README.md` and `MathVacancyDRed/REFINEMENT.md`.

Files written:
- this note;
- `MathVacancyDRed/route_b_candidates.py`.

Nothing was committed, and no other file was edited.

## 0. Coordinates and the closing operation

**Notation.**
- v has degree 5. Its link is x_0..x_4, all of degree 6, so v is a "(6^5) hole" (a "hole" for short).
- The ring of the 2-ball B2 is the 10-cycle w_4 m_0 w_0 m_1 … w_3 m_4. This is the MathSixFiveHole convention: w_t is common to x_t and x_{t+1}; m_t is the middle outer neighbour of x_t.
- In `family.config_from_degrees((6,)*5)` this ring is the `ring` list, and position p gives the vertex:
  - p even is a w-type vertex, which has 4 neighbours inside B2;
  - p odd is an m-type vertex, which has 3 neighbours inside B2.
- The symmetry group acts on positions as p ↦ ±p + 2k (mod 10). It has order 10.

**Closing [hand].** Closing a ring vertex x at degree d means the following:
- Add k = d − deg_K(x) new vertices outside x, as a fan. They replace x on the ring.
- If k = 0, the face (a, x, b) closes x instead, where a and b are x's ring neighbours.

**Ring size of a partial 3-ball.** Close a set S of ring-2 positions. Count the outer neighbours of each closed vertex: o(w) = d − 4 and o(m) = d − 3. Then

  ring = 10 + Σ_{s∈S} (o(s) − 1) − #(cyclically consecutive pairs in S),
  |H| = 15 + Σ o(s) − #pairs.

Checks of the formula:
- The flat 3-ball F_3 (all ten positions closed at degree 6) gives ring 15 and |H| = 30.
- The full 3-ball gives ring L3 = Σ_{ring 2} deg − 45.
- The word "w = 5, m = 6" gives ring 10 and |H| = 25.

**Consequence [hand]: the "pentakis 3-ball" is not pentakis-specific.** It is exactly the generic 3-ball of the ring-2 word "every w_t has degree 5, every m_t has degree 6". README §3(c) worried that it covers 26 of pentakis's 32 vertices; in fact it is determined by the ring-2 degrees, given the simple-ring genericity assumption.

**Genericity assumption [hand, sketch].** New fan vertices are distinct from all old ones.
- For a coincidence at distance 3 this follows because it would create a separating cycle of length ≤ 5 with more than one vertex on each side. A minimal counterexample has no such cycle (Birkhoff). For example, if z is adjacent to w_t and w_{t+2}, then z w_t x_{t+1} x_{t+2} w_{t+2} is such a 5-cycle.
- It is not checked for the larger configurations (ring 14 and up).

## 1. Hand results on unavoidability (task 2)

Throughout, "Goldberg-like" means: minimum degree 5, every degree-5 vertex is a hole (all its neighbours have degree 6), and internally 6-connected. In such a graph a vertex of degree ≥ 7 ("big") lies at distance ≥ 2 from every hole. Euler gives n_5 = 12 + Σ_{d≥7} (d − 6) n_d.

**(A) Nothing beyond flatness is forced. Route B needs F_r for some r [hand].**
- The geodesic domes {3,5+}_{h,0} subdivide the icosahedron with frequency h. They have 10h² + 2 vertices, and their 12 holes are pairwise at distance h.
- They are Goldberg-like and internally 6-connected: the only 5-cycles are the hole links, and there are no separating 3- or 4-cycles.
- For h ≥ r + 1, every hole's r-ball is the flat F_r: v has degree 5, and every vertex at distance 1..r has degree 6, ring included.
- Any other radius-≤ r patch of a dome is a pure hexagonal patch or a subconfiguration of some F_r.

So **any unavoidable set of hole-centred configurations of radius ≤ r must contain F_r or a subconfiguration of it.** Route B is possible only if some subconfiguration of some F_r is vacancy-D-reducible. F_2 is the (6^5) 2-ball, and it fails (370 lost). The first real test is therefore F_3 (ring 15, |H| = 30) and its partial versions with ring 11–14.

**Classical consistency remark [hand; literature check needed].** RSST's discharging theorem applies to internally 6-connected triangulations, so it applies to the domes. In a dome with large h:
- All charge starts at the holes.
- The rules move charge only to adjacent vertices.
- So a good configuration appears within distance about 3 of a hole, in a flat region.

So the RSST list (ring ≤ 14) must contain a configuration in which every vertex has degree 6 except at most one of degree 5. If that chain is right, classical reducibility does succeed in flat regions. That is a reason to expect that some partial F_3 can pass the vacancy game too; it is not evidence that one will. It should be checked against the RSST list (`studiocompute` has the 633 configurations).

**(B) A discharging lemma at radius 2 [hand].** Let b be a big vertex of degree d. Then at most d holes lie at distance 2 from b.

*Proof.*
- b's neighbours have degree ≥ 6, because a degree-5 neighbour would be a hole next to a big vertex.
- A hole at distance 2 is adjacent to some neighbour u of b, and that u must have degree 6.
- Such a u has three outer neighbours p_1 p_2 p_3, forming a path. p_1 and p_3 are shared with the neighbouring link vertices of b.
- Holes are pairwise non-adjacent, so the holes adjacent to u are {p_1, p_3}, or {p_2}, or fewer.
- No hole is adjacent to two non-consecutive neighbours of b, since that would give a separating 4-cycle.
- Weight a shared hole ½ to each of its two link vertices. Then each degree-6 neighbour of b carries weight ≤ 1, and the bound follows. ∎

**Rule:** each hole sends (d − 6)/d to every big vertex b of degree d at distance 2.
- A big vertex ends with charge ≤ 6 − d + d·(d − 6)/d = 0.
- Degree-6 vertices keep 0.
- The total stays 12.

So **some hole v has Σ_{b big, dist(v,b)=2} (d(b) − 6)/d(b) < 1.** Since every term is ≥ 1/7, **such a v has at most 6 big vertices on its ring 2.** It cannot exclude a single big vertex of huge degree, because the term is always < 1.

**(C) The resulting unavoidable family [hand, given genericity].** Read the ring 2 of v as a word δ ∈ {5, 6, *}^10, where * means degree ≥ 7. The word has these properties:
- In the Goldberg-like class, a 5 has both ring neighbours equal to 6.
- By (B), some hole has a word with at most six *.

Take Q(δ) = B2 with every non-* position closed. Big vertices are left on the ring, where their degree does not matter. This keeps the family finite. The family {Q(δ)} is unavoidable in the Goldberg-like class, and so is any family that picks, for each δ, a subconfiguration of Q(δ).

Since K ⊂ K′ and K reducible imply that every host of K′ is fine, a reducible subconfiguration covers every word that contains it. The cost is ring size: for example, δ = (*,6,*,6,…) gives a ring of 20. That case must instead be handled by a subconfiguration that closes fewer vertices.

**What must lie within distance 3 of some hole (answer to task 2):** only the trivial alternatives. Some hole has one of the following:
- (i) a flat 3-ball, which the domes show is unavoidable on its own;
- (ii) another hole at distance 2 or 3;
- (iii) between 1 and 6 big vertices on ring 2 with Σ (d − 6)/d < 1, or a big vertex at distance 3.

(iii) cannot be removed: 5–7 "stretched dipoles" (a 5 and a 7 at distance 2) give plausible examples where every hole sees a 7. This is [hand, sketch]; no explicit sphere has been built. A radius-3 version of (B) (a bound N_3(d) on holes at distance 3) is [open].

## 2. Candidate configurations (task 1)

All are B2(v) plus closings, under the genericity assumption.

| name | structure | ring | \|H\| | why it might be unavoidable or useful |
|---|---|---|---|---|
| W(J), 7 classes | w_t closed at degree 5 for t ∈ J (another hole at w-distance 2); the m_t are not prescribed | **10** | 15+\|J\| | the pentakis-type direction; W(Z_5) plus the m's at 6 is the passing pentakis 3-ball. Cheap: tests whether a few distance-2 holes already suffice |
| M1 | m_0 closed at degree 5 | 11 | 17 | the hole is at the m-position instead |
| Dw6 / Dm6 | one ring-2 vertex closed at degree 6 | 11 / 12 | 17 / 18 | the smallest subconfigurations of F_3; if one passes, every word with a 6 at that kind of position is covered |
| C4 = B2(v) ∪ B2(x_0) | w_4, m_0, w_0 closed at degree 6 | 12 | 20 | the "(6^5) hole plus one link vertex's neighbourhood" candidate; a subconfiguration of F_3 |
| **Pw** = B2(v) ∪ B2(w_0) | w_0 is a second hole: w_0 at 5; m_0, m_1 and the new apex z at 6 | **12** | 21 | forced in the Goldberg class whenever a hole has a hole at a w-position; symmetric in v ↔ w_0 |
| **Pm** = B2(v) ∪ B2(m_0) | m_0 at 5; w_4, w_0 and its two new neighbours at 6 | **12** | 22 | the same, for an m-position hole |
| B3(δ), δ ∈ {5,6}^10 with no adjacent 5s | the full 3-ball; 24 classes (Burnside: (123 + 4·3 + 5·21)/10) | 15 − #5 | 30 − #5 | the full case split when no big vertex is on ring 2; ring ≤ 12 needs ≥ 3 fives |
| flat_arc(L) | positions 2..L+1 (w_0 m_1 w_1 …) at degree 6 | 11,12,12,13,13,14,14 for L = 1..7 | | partial F_3 with ring ≤ 14; this is where (A) and the RSST remark point |
| Pair3w | a ring-3 apex a (shared by w_0 and m_0) is a hole; w_0, m_0 and a's other three neighbours at 6 | 14 | 25 | holes at distance 3 |
| **F_3** | the flat 3-ball | 15 | 30 | **necessary** by (A); expected to be infeasible in pure Python |

**Choosing the other hole as centre.** In Pw, Pm and Pair3w both holes are interior, so the game can be played at either one. Pw and Pm are symmetric, so `Pw_at_x` must give the same value as Pw; this is a builder check. Pair3w is not symmetric, so `Pair3w_at_a` is a genuine second chance.

**Priors (guesses, not results):**
- W(J) with small J and Dw6 most likely still lose: the ring is no smaller, and only 1–2 interior vertices are added.
- Pw, Pm and C4 are the best ring-12 bets.
- B3 words with 4–5 fives probably pass, as pentakis does.

## 3. Hand checks of the builder

These were done by hand, without running anything.

| configuration | hand trace | ring | \|H\| |
|---|---|---|---|
| pentakis3 (close all w at 5 first, then all m at 6) | each w5 has k = 1; each m6 has kdeg 5 and k = 1 | 10 | 25 |
| F_3, closing order p0..p9 | ring sizes go 11, 12, 12, 13, …, 15; at p9 m_4 has kdeg 5 and k = 1 | 15 | 30 |
| Pw | z has kdeg 5 at the last step | 12 | 21 |
| Pm | | 12 | 22 |
| Pair3w | | 14 | 25 |

Degree-5 vertices are closed first. If a w5 were closed after both of its m-neighbours, its two apexes would need identifying (k = −1); the builder raises an error instead.

## 4. Studio commands (untested script)

Run everything from `SolvingFrameworkPlan/docs/working/MathVacancyDRed/` with Python 3.9 on one core.

| command | content | CPU estimate | expected output |
|---|---|---|---|
| `python3 route_b_candidates.py census > route_b_census.txt` | counts only, no game | seconds | `five_words` = 24 classes; the rings above; ring histogram of the Goldberg words (at most six *) |
| `python3 route_b_candidates.py 0 > route_b_stage0_log.txt` | sanity | ~1 min | see below |
| `python3 route_b_candidates.py 1 > route_b_stage1_log.txt` | W(J), M1, Dw6, B3 words with ≥ 4 fives (ring 10–11) | 5–15 min | |
| `python3 route_b_candidates.py 2 > route_b_stage2_log.txt` | C4, Pw, Pm, Dm6, flat_arc3, B3 words with 3 fives, Pw_at_x (ring 12) | 30–90 min; probably 1–3 GB | |
| `python3 route_b_candidates.py 3` | opt-in: ring 13–14 | hours; may abort | |
| `python3 route_b_candidates.py 4` | F_3 | | expected to stop at the colouring precount: "skipped" |

**Expected stage 0 output:**
- The pentakis3 build matches `graphs.ball_config(pentakis, 0, 3)` in ring (10), |H| (25), edge count and colourings (18,420).
- B2 gives `unfilled 550, hist {1:180, inf:370}`.
- pentakis3 gives `unfilled 7710`, reducible, joint depth ≤ 7, and vdred depth 7.

Any mismatch means the builder is wrong. Stop and fix it before reading stages 1–3.

**Output format.** Each line is one JSON object: name, ring, |H|, centre, colourings, and then the `solve_joint` fields (reducible, depth, hist, dnodes, mvnodes, cpu).

**The `max_nodes` cap is soft.** `solve_joint` checks it only after a whole expansion layer, so it can overshoot a lot. The real guard is the colouring precount, which skips a configuration above a limit set per stage (100k, 200k, 400k, 1.5M, 3M).

**Basis of the CPU estimates:**
- Pentakis3 took 11 s under vdred, at about 50 µs per node.
- Joint nodes come to about 14× the colourings.
- Each ring step multiplies the cost by about 8–10 (README).
- Interior vertices add a factor of about 1.5–2 each.

**F_3 needs a C implementation.** At ring 15 with |H| = 30 the estimate is ~10^6–10^7 colourings and ~10^8 nodes.

## 5. Open and next steps

- Run the census, then stage 0, then stages 1–2.
- If any subconfiguration of F_3 passes (Dw6, Dm6, C4, flat_arc), Route B survives the flat (dome) case at that size.
- If all of them fail up to ring 14, Route B needs F_3 or larger in a compiled checker, or a non-local argument.
- Check the RSST remark in §1(A) against the 633 configurations: list those with exactly one degree-5 vertex and the rest of degree 6.
- [open] Prove a radius-3 version of lemma (B), and handle a single huge-degree vertex on ring 2: leave it on the ring and close its neighbours.

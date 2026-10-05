# Why 17:1 has m(T) = 3

Long Table, 5 October 2026. This is a descriptive analysis of the WP18 outputs and of 17:1 itself. **No new declared test was run**, and no graph outside `wp18-P1..P4.json` was used.

- Script: `analysis_17_1.py`. Its full output is in `analysis-17-1.txt`, and every number below comes from that file.
- Any pattern seen across graphs is labelled **observed after the fact**.
- This note was written by a Long Table analysis agent and saved by Long Table. Long Table independently re-checked Lemma 4's witness with `wp18_check.py`'s move code: X is proper, no fill is found below depth 3, a fill exists at depth 3, and X has 6 distinct neighbours.

Notation follows `../WP18-fan-selection-length-declaration.md`. Vertex labels are plantri's labels for P1, order 17, graph_index 1. WP11 uses the same labelling.

## Summary

1. **The statistic reduces to diagonals (proved).** The fill length ℓ is a property of the colouring of T−v alone; the fan only decides which colourings count as starts.
   - A 4-colour link has exactly one monochromatic diagonal. The colouring is a start for the three fans not based at either end of that diagonal.
   - Call a colouring *far* when ℓ ≥ 3. Then L(v,τ_i) ≤ 2 exactly when every far colouring's diagonal ends at i.
   - When all five fans are legal, v is *bad* (L ≥ 3 at every fan) exactly when the far diagonals at v include **two crossing diagonals**.
2. **17:1 is bad at all 12 degree-5 vertices.** At each one, the far diagonals form a path of 3 or 4 consecutive edges in the pentagram, or all five.
   - At 4 of the 12 vertices, a link-reversing automorphism forces this (proved).
   - At the other 8, nothing forces it.
3. **17:1 is one edge flip from two graphs with m = 2.** One flip gives 17:3 (layered 1-5-5-5-1, |Aut| = 20), which is bad only at its two 5-fold apexes. The other gives 17:0 (only 2 good pairs out of 60).
4. **Hand-checkable lemma.** A specific start X at v = 7 has ℓ(X) = 3 (§4). Together with its mirror image, it gives L ≥ 3 at all 10 pairs of vertices 7 and 13. The other 50 pairs rest on the WP18 checker and on the audit's independent replay.

## 1. Structure of 17:1

**Degrees.**
- Twelve vertices have degree 5 and five have degree 6 (vertices 2, 3, 6, 11, 14).
- The degree-6 vertices induce a path 2–3–11 and a disjoint edge 6–14.
- There are no separating triangles, and all 60 (v,τ) pairs are legal.

**Automorphisms.**
- |Aut| = 4 (Z2×Z2): the identity, a half-turn fixing only vertex 3 (it swaps 6↔14), and two reflections.
- Vertex orbits: {0,4,9,10}, {1,8,12,16}, {2,11}, {3}, {5,15}, {6,14}, {7,13}.
- The group is **not transitive on degree-5 vertices**: they fall into four orbits. So the identical profile (3,3,4,4,4) at every degree-5 vertex is not explained by symmetry.
- Vertices 5, 15, 7 and 13 have a stabiliser of order 2, acting as a reflection of the link.
- The 60 pairs fall into 16 orbits: 6 with L = 3 (24 pairs) and 10 with L = 4.

**Construction.** 17:1 is not a recognised named polyhedron. It is one minimum-degree-5-preserving edge flip from two other order-17 graphs:
- **Flip 6–14 → 17:3.** 17:3 is layered 1-5-5-5-1: an apex, a degree-5 ring, a degree-6 ring, another degree-5 ring and a second apex. So 17:1 is 17:3 with one edge of its degree-6 5-cycle flipped. m(17:3) = 2.
- **Flip 2–3 (or its Aut-image 3–11) → 17:0.** m(17:0) = 2, but only 2 of its 60 pairs have L = 2.

**Colourings.** 17:1 has 22 proper 4-colourings up to renaming, in two Kempe classes (16 + 6). 17:0 has 16 and 17:3 has 40. The count alone does not separate m = 3 from m = 2.

**WP11 link (observed; no causal claim).** The 14-vector WP11 obstruction sits at roots 7 and 13 of 17:1 and roots 4 and 6 of 17:0. In both graphs, these are exactly the degree-5 vertices with three degree-6 neighbours.

## 2. The diagonal reduction (proved)

**Lemma 1 (one-move test).** Take a state with hole h whose link uses four colours.
- Swapping an {a,b}-component K leaves at most three link colours exactly when K contains every link vertex of one of the two colours and none of the other.
- So if an {a,b}-path in T−h joins a link vertex of colour a to one of colour b, no {a,b}-swap fills.
- A slide from u fills exactly when N(u)∖{h} uses at most two colours.

*Proof.* After the swap, link vertices in K exchange a and b, and the other two link colours stay. So colour a disappears exactly when every link a-vertex is in K and no link b-vertex is. If an a-vertex x and a b-vertex y lie in one component C, then any component holding all link a-vertices is C, and C contains y. The same holds with a and b exchanged. For a slide, the new hole u sees c(u) on h, and c(u) does not occur on N(u)∖{h}. ∎

**Lemma 2 (diagonal reduction).** At a degree-5 vertex v, a colouring of T−v with a 4-colour link has multiplicities (2,1,1,1). The repeated colour sits on exactly one diagonal d = (p, p+2).
- The fan τ_i has chords (i,i+2) and (i,i+3), so d is one of them exactly when i is an end of d.
- So the colouring is a start for τ_i exactly when i ∉ d.
- ℓ does not depend on τ.

Let D_far(v) be the set of diagonals carrying a colouring with ℓ ≥ 3. Then L(v,τ_i) ≤ 2 exactly when every diagonal in D_far(v) has i as an endpoint. The diagonals of a pentagon form a 5-cycle (the pentagram), which has no triangles. So a set of diagonals that pairwise share an endpoint is a star of at most 2 diagonals. **When all five fans at v are legal, v is bad exactly when D_far(v) contains two crossing diagonals.** ∎

Colourings with a 3-colour link have ℓ = 0 and never matter. The formula L(v,τ_i) = max ℓ over colourings whose diagonal avoids i matches **all 68,890 rows of P1–P4**, with 0 mismatches. That check reuses `wp18_core`, so it is not independent.

**Lemma 3 (symmetry).**
- Suppose an automorphism fixes v and reverses its link, fixing link position i. It then swaps the crossing diagonals (i+1,i+3) and (i+2,i+4). So if either is far, v is bad.
- If a rotation of order 5 fixes v, D_far(v) is either empty or all five diagonals. ∎

**D_far in 17:1** (diagonals whose far colourings include ℓ = 4 are marked \*):

| v | Orbit | Degree-6 neighbours | D_far(v) | Shape |
|---|---|---|---|---|
| 0 | {0,4,9,10} | 2 | 13\*, 30, 41 | 3-path |
| 1 | {1,8,12,16} | 2 | 02, 13\*, 30, 41 | 4-path |
| 5 | {5,15} | 1 | all five (24\*) | all |
| 7 | {7,13} | 3 | 02, 13, 30\* | 3-path |

Lemma 3 covers vertices 5, 15, 7 and 13. The orbits {0,4,9,10} and {1,8,12,16} have trivial stabiliser, so the crossing far pairs there are not forced by symmetry.

**Comparison graphs.**
- **14:0:** D_far = ∅ at every vertex.
- **17:3:** D_far = ∅ at all 10 ring vertices. Both apexes have all five diagonals far, which is the 5-fold case of Lemma 3.
- **17:0:** 10 vertices have crossing far pairs. Vertices 8 and 15 have 2-stars, which gives exactly one good fan at each.

**Across all 961 graphs (observed after the fact).**
- The 13,137 good degree-5 vertices have D_far empty (10,780), a single diagonal (1,837) or a 2-star (520).
- The 641 bad vertices have D_far equal to 2 crossing diagonals (228), a 3-path (209), 3 others (87), a 4-path (93) or all 5 (24).
- Every m = 2 graph has a vertex whose far diagonals all meet at a common endpoint. 17:1 has none.
- Fewest good vertices: 17:1 has 0, 17:0 has 2, and 22:158 and 22:562 have 4 each.
- The minimum fraction of good vertices by order is 0.85 (18), 1.00 (19), 0.62 (20), 0.36 (21), 0.29 (22).

## 3. The ℓ = 3 starts at the L = 3 pairs

| Pair (v, τ) | ℓ = 3 starts | Their diagonals | Distinct neighbours |
|---|---|---|---|
| (0, τ1) | 2 | 30 | 6 each |
| (0, τ3) | 2 | 41 | 6 each |
| (1, τ1) | 3 | 02, 30 | 5–6 |
| (1, τ3) | 2 | 02, 41 | 5–6 |
| (5, τ2) | 4 | 13, 41, 30 | 5–6 |
| (7, τ0) | 1 | 13 | 6 |

What these starts share:
- All are in the gap case of `../swarm/fan-link.md`: both the β–γ and β–δ paths are present. The paths are long, 5 to 8 vertices, and they run through the degree-6 vertices.
- They are Kempe-rigid: 3 or 4 of the six bichromatic subgraphs of T−v are connected. Each start therefore has only 5 or 6 distinct neighbours.
- Every ℓ = 3 start has at least one ℓ = 2 neighbour.
- Slides often move the hole onto a degree-6 vertex, where four colour pairs must be blocked rather than two.

Kempe rigidity holds beyond 17:1 (observed after the fact, orders 12–20, all 4-colour-link deletion states):

| ℓ | States | With ≥ 3 of 6 pairs connected |
|---|---:|---:|
| 1 | 99,580 | 68% |
| 2 | 23,249 | 47% |
| ≥ 3 | 553 | 91% |

**Proposed structural explanation (not proved).** Far colourings are rigid gap states. By Lemma 2, m(T) ≥ 3 requires far colourings on two crossing diagonals at every degree-5 vertex simultaneously. Flipping one edge of 17:3's degree-6 ring spreads its apex-only far colourings to every degree-5 vertex. Why the flip does this is open.

## 4. Lemma 4: a start at v = 7 with ℓ = 3

X is the following colouring of T−7, listed by vertex 0..16, with · marking the hole:

`(0,1,2,1,3,2,3,·,0,3,0,2,1,0,1,2,3)`

- The link of 7 is (1, 6, 14, 8, 2), coloured (1, 3, 1, 0, 2). The monochromatic diagonal is 1–14.
- X is a start for τ1, τ3 and τ4.

**Kempe components.**

| Pair | Components |
|---|---|
| {0,1} | {0,1,3,10}, {8,12,13,14} |
| {0,2} | one component |
| {0,3} | {0,4}, {6,8,9,10,13,16} |
| {1,2} | {1,2,3,5,11,12}, {14,15} |
| {1,3} | one component |
| {2,3} | one component |

X has exactly 6 distinct neighbours: K{0,1}, K{0,3}, K{1,2}, and the slides from 6, 8 and 2.

**ℓ(X) ≥ 2.** Each colour pair is blocked by a path:

| Pair | Blocking path |
|---|---|
| {0,1} | 8–14 |
| {0,2} | 8–2 |
| {0,3} | 8–9–10–16–13–6 |
| {1,2} | 1–2 |
| {1,3} | 1–6 |
| {2,3} | 2–9–15–16–11–4–5–6 |

The slides fail because each N(u)∖7 uses three colours: N(6)∖7 is coloured (1,2,1,0,1), N(8)∖7 is (2,1,2,3), and N(2)∖7 is (0,1,0,3,1).

**ℓ(X) ≥ 3.** No neighbour has a filling move. The blocking paths below are listed for the pairs {0,1}, {0,2}, {0,3}, {1,2}, {1,3}, {2,3} in that order.

| Neighbour | Hole; link colours | Blocking paths | Slides (colours on N(u)∖hole) |
|---|---|---|---|
| Y1 = K{0,1} | 7; (1,3,0,1,2) | 14–8; 14–15–10–11–12–5–0–2; 14–6; 1–2; 1–6; 2–9–15–16–11–4–5–6 | 6: {0,1,2}; 14: {1,2,3}; 2: {0,1,3} |
| Y2 = K{0,3} | 7; (1,0,1,3,2) | 6–1; 6–5–0–2; 6–13–16–10–9–8; 1–2; 14–8; 2–8 | 6: {1,2,3}; 8: {0,1,2}; 2: {0,1,3} |
| Y3 = K{1,2} | 7; (1,3,2,0,2) | 8–15–10–3–0–1; 8–14; 8–9–10–16–13–6; 1–2; 1–6; 14–6 | 1: {0,2,3}; 6: {0,1,2}; 8: {1,2,3} |
| Y4 = slide from 6 | 6 (degree 6); (1,2,1,0,1,3) | 13–12; 13–11–10–15–8–2–0–5; 13–16–10–9–8–7; 1–5; 1–7; 5–4–11–16–15–9–2–7 | 5: {0,1,3}; 13: {1,2,3}; 7: {0,1,2} |
| Y5 = slide from 8 | 8; (2,0,1,2,3) | 7–14; 7–2; 7–6–13–16–10–9; 14–15; 14–6–12–4–3–9; 2–9 | 7: {1,2,3}; 14: {0,2,3}; 9: {0,1,2} |
| Y6 = slide from 2 | 2 (degree 6); (0,1,3,0,2,1) | 0–1; 8–9; 8–7; 1–6–12–4–3–9; 1–7; 9–15–16–11–4–5–6–7 | 7: {0,1,2}; 9: {0,1,3} |

**ℓ(X) ≤ 3.** A 3-move fill exists (recorded in `analysis-17-1.txt`). So ℓ(X) = 3. ∎

**Corollary.** The reflection fixing 7 maps 1↔8, 6↔14 and 2↦2. It sends X to X′, whose diagonal is 6–8, and X′ is a start for τ0, τ2 and τ4. The diagonals 1–14 and 6–8 cross. By Lemma 2, L(7,τ) ≥ 3 for all five fans, and by Aut the same holds at 13.

## 5. Conjectures (for a future declaration; untested)

> **Outcome after WP19 (5 October; `SolvingFrameworkPlan/MathWP19Results.md`, `MathWP19Counterexamples.md`):**
> - **C1 and C3 are killed** by 24:6406, which has m = 3 (58 pairs with L = 3 and 12 with L = 4) and two degree-7 vertices. So 17:1 is not the only m = 3 graph, and m ≥ 3 is not confined to graphs with degrees 5 and 6 only.
> - **C2 (m ≤ 3) passed** on all 10,203 WP19 graphs; its universal statement remains open.
>
> The statements below are kept as preregistered. Their finite observations keep their original scope, orders 12–22.

- **C1 (17:1 is sporadic).** Every minimum-degree-5 triangulation of order ≥ 18 has m(T) ≤ 2.
  - At risk: the minimum fraction of good vertices falls from 0.62 to 0.29 over orders 20–22 (observed after the fact).
- **C2 (bound).** Every T has m(T) ≤ 3.
- **C3 (where m ≥ 3 can occur).** If m(T) ≥ 3, then T has exactly 12 degree-5 vertices and every other vertex has degree 6.
  - Support is thin: 17:1 alone, plus the near-miss 17:0.

By Lemma 2, a declared test of C1–C3 can report D_far(v) per vertex rather than per pair.

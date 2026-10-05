# Why 24:6406 has m = 3 and why a slide saves two swaps in 24:7228

Long Table, 5 October 2026. This is a structural analysis of the two saved WP19 counterexamples, done partly by hand. **No new graph, order or census was run, and no replacement bound is fitted.**

- Script: `counterexample_analysis.py`. Its complete output is `counterexample-analysis.txt`, and every number below comes from that file.
- Inputs:
  - both graph records, from `../audit/wp19-counterexamples.json` (sha256 `ee851f41…`);
  - the 17:1 rotation, from `../wp18/wp18-P1.json`;
  - for §A.4 only, the *saved* m values of order-24 graphs one flip away, from `wp19-P3.json`.
- Moves, canonical labels and the roles (a0, b, a2, g, d), P, Q, C₀, D₂ and X follow `../wp18/mechanism.md` and `../../../../SolvingFrameworkPlan/docs/reports/MathShortFillTheorem.md`.
- Vertices are zero-based. The script's printed colours are each state's canonical labels.

Labels used throughout:
- **[hand]**: a complete argument, or a certificate that can be checked by hand from the data shown.
- **[computed]**: computed on the saved graph by the script.
- **[post hoc]**: a pattern or conjecture suggested by these two graphs. It is untested.

## Summary

1. **24:6406.** All 70 fans are legal, and every degree-5 vertex is bad because two of its far diagonals cross. Non-legal fans play no role. [computed; the diagonal reduction gives 0 mismatches against all 70 saved pair maxima]
   - |Aut| = 2. The only symmetry is a half-turn that fixes no vertex. It reverses the edges 2–11 and 6–16 and swaps the two degree-7 vertices 1 ↔ 21.
   - Because no vertex has a nontrivial stabiliser, the symmetry lemma of analysis-17-1 never applies. Badness is **never forced by symmetry** here.
   - Vertices 4 and 19 are bad by the smallest possible pattern: exactly two crossing far diagonals. **Vertex 4 (and so 19) is proved bad by hand** (§C).
2. **Relation to 17:1.** No single local operation was found.
   - The largest patch common to both graphs has only 9 matched vertices.
   - Every minimum-degree-preserving flip of 24:6406 lands on a saved m = 2 graph, except the flip of the axis edge 6–16, which returns 24:6406 itself.
   - The common feature is structural (post hoc): both graphs carry a half-turn whose axis passes through degree-6 vertices or the midpoints of edges between degree-6 vertices.
3. **24:7228.** The start is Kempe-rigid. Kempe's two swaps are both interlocked, and the only cheap cut of the chain P (at vertex 5) lies in an αγ-component that vertex 8 ties to two link vertices, 8 and 18.
   - The slide 17→8 deletes that bridge, and the cut becomes a free swap. [hand, from the listed components]
   - At hole 17, the Kempe search finds no one-swap-fillable state before depth 4, so κ = 5. [computed: layers 1, 4, 8, 10, 13, 26]
4. **Lemma L3 [hand; suggested post hoc].** If ℓ = 3 < κ, then every shortest mixed path starts with a slide h→u. Moreover, every two-swap Kempe fill at u after that slide starts with a swap on a pair containing the slid colour σ.
   - This isolates where the M3 argument stops: a **non-terminal** σ-swap after the slide.
   - In 24:7228, that swap's lift to T−h runs through u into the third vertex w = 18 of the face h-u-w.

## A. 24:6406: structure

**Degrees** [computed]. Degrees are 5¹⁴ 6⁸ 7², and there are no separating triangles. Every degree-5 vertex has all five fans legal (70 pairs).

The vertices of degree ≥ 6 are 1, 2, 3, 6, 10, 11, 14, 16, 17 and 21. The subgraph they induce is connected:

- a 6-cycle 1–2–11–21–16–6–1;
- two triangles 2–3–11 and 2–10–11 on its chord 2–11;
- pendant edges 6–14 and 16–17.

Ten of the 14 degree-5 vertices are adjacent to a degree-7 vertex. The exceptions are 4, 13, 18 and 19. The two degree-7 vertices are at distance 3 (1–2–11–21).

**Automorphisms** [computed]. |Aut| = 2: the identity and an orientation-preserving involution σ with **no fixed vertex**.
- σ reverses the edges 2–11 and 6–16, so it is a half-turn whose axis pierces their midpoints.
- Orbits: {0,20}, {1,21}, {2,11}, {3,10}, {4,19}, {5,23}, {6,16}, {7,15}, {8,22}, {9,12}, {13,18}, {14,17}.
- Degree-5 orbits: {0,20}, {4,19}, {5,23}, {7,15}, {8,22}, {9,12}, {13,18}.

So the 70 pairs form 35 orbits.

**Comparison with 17:1** [computed]. 17:1 has a half-turn too.
- That half-turn fixes vertex 3 (degree 6) and reverses edge 6–14 (both ends degree 6).
- Its degree-6 vertices form the path 2–3–11 plus the edge 6–14.
- In 24:6406 the place of vertex 3 is taken by the pair 3, 10, which σ swaps. Both are adjacent to the axis edge 2–11, so the pattern looks like 17:1's fixed vertex 3 split across an axis edge.
- The second axis edge, 6–16, now has the pendants 14 and 17.

This is an analogy, not a construction. [post hoc]

**Flips** [computed; m values read from the saved P3 records]. 24:6406 has 12 flips that keep minimum degree 5.
- Flipping any edge at a degree-7 vertex (1–6, 1–2, 11–21, 16–21) gives 24:4145 or 24:3231. Each has a single 7 and m = 2.
- The flips 2–10, 2–3, 3–11 and 10–11 give m = 2 graphs with three 7s.
- Flipping the axis edge 2–11 gives 24:2443, which has four 7s and m = 2.
- Flipping 6–14 or 16–17 gives 24:5497, with the same degree sequence and m = 2.
- **Flipping the other axis edge 6–16 gives 24:6406 again.**

Compare 17:1: flipping its axis edge 6–14 gives 17:3. So 24:6406 is an isolated m = 3 point of its flip neighbourhood. Every flip that destroys or moves a degree-7 vertex lowers m to 2.

**Is 24:6406 a local modification of 17:1?**
- Growing an orientation-consistent map from every pair of flags gives at most **9** vertices whose full links match [computed]. There are four such patches, for example {0,3,4,5,6,13,14,15,22} ↦ part of 17:1 around its vertices 3, 6, 11–13.
- So 24:6406 does not contain 17:1 minus a small region, and the 7 extra vertices cannot come from one local insertion that leaves the rest of 17:1 intact.
- **No relation by a single local operation (insertion, splitting or flip) was found.** That statement only covers the operations tested here: common patches and single flips.

## B. 24:6406: far diagonals, and how each vertex is bad

D_far(v) is the set of link diagonals carrying a colouring of T−v with ℓ ≥ 3 (analysis-17-1, Lemma 2). Diagonals are named by link vertices, and \* marks a diagonal that carries an ℓ = 4 colouring. All fans are legal, so v is bad exactly when D_far(v) contains two crossing diagonals.

| Orbit | Link of first member | deg ≥ 6 / deg-7 neighbours | D_far (first member) | Shape | L per fan τ0..τ4 |
|---|---|---|---|---|---|
| {4,19} | 0,3,13,14,5 | 2 / 0 | 0–13, 3–14 | **2 crossing** | 3,3,3,3,3 |
| {0,20} | 1,2,3,4,5 | 3 / 1 | 2–4, 4–1, 5–2 | 3-path | 3,3,3,3,3 |
| {7,15} | 1,6,16,17,8 | 4 / 1 | 1–16, 16–8, 8–6 | 3-path | 3,3,3,3,3 |
| {9,12} | 1,8,18,10,2 | 3 / 1 | 1–18, 18–2, 10–1 | 3-path | 3,3,3,3,3 |
| {13,18} | 3,12,22,14,4 | 2 / 0 | 12–14, 22–4, 4–12 | 3-path | 3,3,3,3,3 |
| {5,23} | 0,4,14,6,1 | 3 / 1 | 0–14, 14–1\*, 6–0, 1–4 | 4-path | 4,4,3,4,3 |
| {8,22} | 1,7,17,18,9 | 2 / 1 | all five (18–1\*) | all 5 | 3,4,4,3,4 |

[computed] The L values given by the diagonal formula match all 70 saved pair maxima (0 mismatches).

- Every degree-5 vertex has a crossing pair, so **no vertex is bad because of a non-legal fan**.
- Far colourings are rare. There are 72 at degree-5 holes (68 with ℓ = 3 and 4 with ℓ = 4), out of 14,114 deletion states. Each vertex has 2 to 7.
- Every one is a gap start (Lemma A). They are Kempe-rigid: 3 or 4 of the 6 bichromatic subgraphs are connected, and each has only 5 to 7 distinct neighbours.

**Role of the degree-7 vertices** [computed; the readings are post hoc]:

- All 12 pairs with L = 4, and both "all five" vertices (8 and 22), are adjacent to a degree-7 vertex. In each of the four ℓ = 4 colourings, the chosen shortest P (8 to 12 vertices) passes through 1 or 21.
- The four degree-5 vertices away from the 7s are 4, 13, 18 and 19. They include the only vertices with the minimal 2-crossing shape (4 and 19); 13 and 18 have 3-paths.
- In 70 of the 72 far colourings, the chosen shortest P or Q passes through 1 or 21. The middle vertex b is a degree-7 vertex in 20 of them.
- Every flip at a 7 drops m to 2 (§A).

Reading: the 7s are hubs that both gap chains use. Making a vertex less of a hub breaks the simultaneous crossing pairs at every vertex. This is not proved.

**κ at far starts** [computed]. 64 starts have ℓ = κ = 3 and 4 have ℓ = κ = 4. The other 4 have ℓ = 3 and κ = 4 (at 9, 12, 13 and 18). Their unique optimal first move is a slide onto a degree-6 vertex (2, 11, 14 and 17). No start in 24:6406 has κ − ℓ ≥ 2.

## C. Hand certificate: vertex 4 is bad (and so is 19)

The link of 4 is (0, 3, 13, 14, 5). Its five diagonals 0–13, 3–14, 13–5, 14–0 and 5–3 are all non-edges, which can be read off the rotation, so all five fans are legal [hand]. Fan τ_i is a start fan for a colouring exactly when i is not an end of its monochromatic diagonal.

**X1** (diagonal 3–14) is `(0,1,2,1,·,3,2,3,2,0,1,3,0,2,1,0,1,0,3,2,0,2,3,3)`. It is proper on T−4 (check each rotation list). Its link colours are (0,1,2,1,3), and it is a start for τ0, τ2 and τ4.
- Roles: a0 = 3, b = 13, a2 = 14, g = 5, d = 0.
- P (βγ = {2,3}) = 13–22–21–23–19–18–8–7–6–5.
- Q (βδ = {0,2}) = 13–12–21–20–19–17–8–9–2–0.

**X2** (diagonal 0–13) is `(0,1,2,3,·,2,3,0,3,0,3,1,2,0,1,2,1,2,1,0,2,0,3,3)`. Its link colours are (0,3,0,1,2), and it is a start for τ1, τ3 and τ4.
- Roles: a0 = 0, b = 3, a2 = 13, g = 14, d = 5.
- P (βγ = {1,3}) = 3–11–10–18–8–1–6–14.
- Q (βδ = {2,3}) = 3–12–22–15–6–5.

The diagonals 3–14 and 0–13 have no common end, so they **cross**, and together the two colourings are starts for all five fans. So L(4, τ) ≥ 3 at every τ follows once ℓ(X1), ℓ(X2) ≥ 3.

The certificates below follow Lemma 1 of analysis-17-1:
- A pair {a,b} is blocked by an {a,b}-path joining a link a-vertex to a link b-vertex. A link edge is such a path of length 1.
- A slide from u fails when N(u)∖hole uses 3 colours.

Within each row, colours are in that state's own canonical labels, and the six pairs are listed as {0,1}; {0,2}; {0,3}; {1,2}; {1,3}; {2,3}.

**ℓ(X1) ≥ 2** [hand].
- Blocked pairs: 0–3; Q; 0–5; 3–13; 14–5; P.
- Slides: N(0)∖4 = (1,2,1,3), N(13)∖4 = (1,0,3,1), N(5)∖4 = (0,1,2,1). Each uses 3 colours.

**ℓ(X1) ≥ 3** [hand]. X1 has 6 distinct neighbours, and none has a filling move:

| Y | Move | Hole: link colours | Blocking paths, pairs in order | Slides (colours on N(u)∖hole) |
|---|---|---|---|---|
| Y1 | swap {0,1} on {0,1,3,9,10,12,20} | 4: (0,1,2,0,3) | 0–3; 14–13; 0–5; 3–13; 3–11–10–18–17–7–1–5; 13–22–21–23–19–18–8–7–6–5 | 3: (0,2,3,0,2); 13: (1,0,3,0); 5: (0,0,2,1) |
| Y2 | swap {0,3} on {0,5} | 4: (0,1,2,1,3) | 0–3; 0–2–11–21–22–13; 0–5; 3–13; 14–5; 13–12–21–15–6–5 | 0: (1,2,1,3); 13: (1,3,0,1); 5: (0,1,2,1) |
| Y3 | swap {1,3} on {1,5,7,14,16,22,23} | 4: (0,3,2,1,3) | 0–1–9–18–17–16–15–14; 0–2–9–8–17–19–20–21–12–13; 0–3; 14–13; 14–5; 13–3 | 0: (1,2,3,3); 13: (3,0,3,1); 14: (2,3,0,2,3) |
| Y4 | slide 4→0 | 0: (0,1,0,2,3) | 1–2; 3–4; 1–5; 2–9–8–17–19–20–21–12–13–4; 2–11–21–23–19–18–8–7–6–5; 4–5 | 2: (0,2,0,3,0); 4: (0,1,0,3); 5: (2,0,1,0) |
| Y5 | slide 4→13 | 13: (1,0,3,1,2) | 12–3; 12–21–20–19–17–8–9–2–0–4; 12–22; 3–4; 14–22; 4–5–6–7–8–18–19–23–21–22 | 12: (1,3,2,3); 22: (0,2,0,1); 4: (0,1,1,3) |
| Y6 | slide 4→5 | 5: (0,3,1,2,1) | 0–1; 0–2–9–8–17–19–20–21–15–6; 0–4; 14–6; 14–4; 6–7–8–18–19–23–21–22–13–4 | 0: (1,2,1,3); 4: (0,1,2,1); 6: (1,1,0,1,3) |

**ℓ(X2) ≥ 2** [hand].
- Blocked pairs: 13–14; 0–5; 0–3; 14–5; P; Q.
- Slides: N(3)∖4 = (0,2,1,2,0), N(14)∖4 = (0,3,2,3,2), N(5)∖4 = (0,1,3,1).

**ℓ(X2) ≥ 3** [hand]. X2 has 5 distinct neighbours:

| Y | Move | Hole: link colours | Blocking paths, pairs in order | Slides |
|---|---|---|---|---|
| Y1 | swap {0,1} on {0,1,7,9,11,16,18,19,21} | 4: (0,3,1,0,2) | 14–13; 0–5; 0–3; 13–12–11–2–1–5; 13–3; 5–6–15–22–12–3 | 3: (0,2,1,2,1); 13: (3,2,3,0); 5: (0,0,3,1) |
| Y2 | swap {0,2} on {0,2,5,9} | 4: (0,3,2,1,2) | 0–1–9–18–17–16–15–14; 0–5; 0–3; 14–13; 14–6–1–8–18–10–11–3; 13–3 | 0: (1,2,3,2); 3: (0,2,1,0,2); 14: (2,3,0,3,2) |
| Y3 | slide 4→3 (degree 6) | 3: (0,2,1,2,0,3) | 0–1–7–16–21–11; 0–2; 0–4; 11–2; 11–10–18–8–1–6–14–4; 12–22–15–6–5–4 | 11: (2,3,2,0,2); 4: (0,0,1,2) |
| Y4 | slide 4→14 (degree 6) | 14: (1,0,3,2,3,2) | 13–4; 13–12–21–15; 13–22; 4–5; 4–3–11–10–18–8–1–6; 15–22 | 4: (0,3,0,2); 13: (3,2,3,1) |
| Y5 | slide 4→5 | 5: (0,2,1,3,1) | 0–1; 0–4; 0–3–13–22–21–23–19–10–9–8–7–6; 14–4; 14–6; 4–3–12–22–15–6 | 0: (1,2,3,2); 4: (0,3,0,1); 6: (1,1,2,1,0) |

**Upper bounds** [hand, by replaying the path].
- X1 fills by three swaps: {0,1} on {0,1,3,9,10,12,20}; {0,3} on {1,3,5,7,10,11,17,18,23}; {0,2} on {2,5,6,7,8,11,15,18,19,21,23}. Its link ends as (1,3,2,1,2).
- X2 fills by: {0,1} on {0,1,7,9,11,16,18,19,21}; {1,3} on {0,3}; {0,3} on {0,1,6,8,10,11,16,18,23}. Its link ends as (0,1,0,1,2).
- So ℓ(X1) = ℓ(X2) = 3.

**Conclusion.** Vertex 4 is bad, and this is proved by hand. Its far set is exactly the two crossing diagonals (3–14 has one far colouring, 0–13 has three) [computed]. So the hand certificate uses the minimum possible information. The half-turn σ maps X1 and X2 to far colourings at 19 on the crossing diagonals 10–17 and 20–18, so 19 is bad as well.

## D. 24:7228: why the slide saves two Kempe swaps

**Setting** [hand from the component list].
- The start is `(0,1,2,3,1,2,0,3,2,3,1,2,3,0,3,2,1,·,1,0,2,1,3,0)`. Hole 17 has link (7,16,23,18,8), coloured (3,1,0,1,2).
- Roles: a0 = 16, b = 23, a2 = 18, g = 8 (degree 6), d = 7. Colours: α = 1, β = 0, γ = 2, δ = 3.
- Chains: P = 23–15–6–5–13–20–19–8 (βγ) and Q = 23–22–19–12–13–14–6–7 (βδ). **Both pass through the degree-8 hub 19, and through 13 and 6.**
- 24:7228 has a trivial automorphism group.

The components of T−17 are:

| Pair | Components |
|---|---|
| {0,1} αβ | {0,1,4,6,10,16,18,19,23}, {13,21} |
| {0,2} βγ | one component |
| {0,3} βδ | {0,3}, {6,7,9,12,13,14,19,22,23} |
| {1,2} αγ | E = {1,2,4,5,8,10,11,18}, C₀ = {15,16,20,21} |
| {1,3} αδ | {1,3,4,7,9,10,12,16}, D₂ = {14,18,21,22} |
| {2,3} γδ | one component |

**Why the hole is locked** [hand for (i)–(iii); computed for (iv)].

(i) **Rigidity.** βγ and γδ are connected, so swapping them is only a global renaming. Each of the other four pairs has exactly two components, and swapping either one gives the same state up to renaming. So the start has **exactly four distinct Kempe neighbours**:
- two partition-keeping interior swaps: {0,3} on {0,3}, and {0,1} on {13,21};
- Kempe's two swaps: C₀ (≡ swapping E) and D₂.

(ii) **Interlock in both orders.** C₀ meets P at 15 and 20, and D₂ meets Q at 14 and 22. So configuration X holds both ways, and by Lemma E neither Kempe pair can be shown to fill in two moves.

(iii) **The interior swaps do not cut the chains.** Swapping {13,21} only reroutes P to 23–15–21–20–19–8 and Q to 23–22–21–14–6–7. The {0,3} swap misses both chains.

The only cheap cut of P is at its γ-vertex 5. The αγ-component through 5 is E, and **E contains two link vertices of 17: a2 = 18 and g = 8.** E is joined to them through vertex 8, by the edges 5…1–8 and 8–18. So swapping E moves the monochromatic diagonal from 16–18 to 16–8 instead of freeing a colour: the link becomes (3,1,0,2,1).

The next natural swap, {β,γ} at 23, is then blocked by the link edge 23–18, which is now coloured {0,2}. The face 17–18–23 locks that pair at hole 17.

(iv) **Kempe search.** The Kempe class at hole 17 has 620 states. Its layers are 1, 4, 8, 10, 13, 26, …, with 6 filled states first appearing at depth 5. Every state at depth ≤ 3 (23 states) is a gap state with no one-swap fill; the first 5 one-swap-fillable states appear at depth 4. So no Kempe path of length ≤ 4 fills, and κ = 5. Up to depth 3, the monochromatic diagonal only cycles among 16–18, 8–16, 18–7, 23–8 and 7–23 while both chains survive.

This step is computed, not hand-proved. Items (i)–(iii) explain why the class grows so slowly (degree 4 at the root, half the moves partition-keeping). They do not by themselves exclude depth 4.

**What the slide bypasses** [hand, from the components after the slide]. The slide 17→8 carries σ = γ = 2 to 17 and deletes vertex 8. Two things follow.

- **The bridge disappears.** In T−8, E splits. E′ = {1,2,4,5,10,11} touches the hole-8 link only at vertex 1. Vertex 18 joins {15,16,17,18,20,21} through the newly coloured 17.
- **P stays, but its end moves.** At hole 8 the βγ-chain is 19–20–13–5–6–15–23–17: the same chain, now ending at the new σ-vertex 17. Its cut vertex 5 lies in the free component E′.

The mixed path in actual colours [hand]:
1. **Slide 17→8.** The degree-6 hole has link (1,7,17,18,19,9), coloured (1,3,2,1,0,3).
2. **Swap {1,2} on E′.** This cuts P at 5 and turns link vertex 1 into σ = 2. The link is now (2,3,2,1,0,3).
3. **Swap {0,2} on {0,1,4,6,15,17,23}.** This component holds both σ-vertices 1 and 17 of the link and misses 19, the only 0 on the link. The link becomes (0,3,0,1,0,3), colour 2 is free, and the hole is filled.

At hole 8 the Kempe distance of the slid state is 2 [computed], as M3 requires.

So the slide saves swaps for two reasons:
- it **removes the bridge vertex 8** that welds the cut component E to two link vertices of 17;
- it **moves the hole across the face 17–18–8**, so the link edge 23–18 that blocks {β,σ} at 17 is no longer on the hole's link.

At hole 17 these two obstacles cost the extra swaps in the 5-swap path [computed]:
- The path starts with the same cut (swap E, which also recolours 8 and 18).
- It then needs {0,1}, {1,3}, {0,1} and {3,0} swaps on large components (listed in the txt) to undo the damage to the link.

A hand proof that exactly two extra swaps are needed is not given.

**Where the M3 argument stops at length 3** [hand].
- M3's SK analysis rests on the swap being *terminal*. Because the target is reached right after the swap, every original ρ-neighbour of u lies in K (case h ∉ K), or none does (case h ∈ K). Either way, K, possibly with u added, is a whole component of T−h.
- Here the first swap after the slide uses the pair {σ, ρ} = {2, 1} but is **not terminal**. The ρ-neighbour 18 of u = 8 stays outside K₁ = E′, because it is still on the link afterwards.
- 18 is the third vertex of the face h-u-w = 17-8-18. So in T−h the component of K₁ grows through u to w, giving E = E′ ∪ {8, 18}. Replaying the swap at h then recolours two link vertices of h (8 and 18) and turns w into σ.
- The second swap's {σ,β}-component contains the old hole h (now coloured σ) and the other σ-vertex of link(u). This is the h ∈ K configuration, now reached only after a preparatory swap.

[computed] All four κ = 5 starts in this Kempe class show the same pattern: the unique first move is S8, and in the representative avoiding h, K₁ lifts through 8 to 18. (Section F of the txt; the representative choice matters because each swapped pair has two components.)

**Lemma L3 (length-3 reduction)** [hand; suggested by these graphs]. Use M3's conventions, with any graph and palette. Suppose ℓ(s) = 3 < κ(s). Then:
- (a) every shortest mixed path from s starts with a slide h→u; and
- (b) for each such slide, with carried colour σ and slid state t, M3 gives κ_u(t) = 2, and the first swap of **every** two-swap Kempe fill of t at hole u uses a pair containing σ.

*Proof.*
1. If a shortest path starts with a swap K, the next state s′ has ℓ(s′) = 2. M3 gives κ(s′) = 2, so κ(s) ≤ 3. This contradicts the assumption, so (a) holds.
2. After the slide h→u, the state t has ℓ(t) = 2, so M3 at the hole u gives two swaps K₁K₂ that fill t.
3. Suppose K₁ uses a pair {p,q} with σ ∉ {p,q}. The {p,q}-induced graphs of T−u (after the slide) and T−h (before it) coincide: u and h carry σ in their respective deletions, and every other colour is equal. So K₁ is a component of T−h. Swapping it creates and removes no σ, so the slide stays legal and commutes (Lemma C).
4. Then the state K₁(s) has the mixed path S·K₂ of length 2. M3 gives κ(K₁(s)) ≤ 2, so κ(s) ≤ 3, again a contradiction. ∎

[computed] Lemma L3 checked on the saved graphs: 4 starts in 24:6406 and 15 in 24:7228 have ℓ = 3 < κ, with 0 violations. The proof does not depend on this check.

## E. Conjectures (post hoc; not tested on any other graph)

- **Conjecture B (bridge face).** If κ(s) ≥ ℓ(s) + 2 at a degree-5 hole h, then some shortest mixed path has the form S K₁ … with these properties:
  - the slide h→u carries σ;
  - K₁ uses a pair {σ, ρ}, and its {σ, ρ}-component in T−h contains u and a vertex w with h-u-w a face;
  - w has colour ρ.
  - *Support:* only the four κ = 5 starts of 24:7228. These two graphs contain no other start with κ − ℓ ≥ 2.
  - *Status:* necessity only; nothing here suggests a sufficient condition.
- **Conjecture S (axis symmetry)** — *[Refuted 5 October by Math: H₂ of the triangle-sum family has order 31, m = 3 and trivial automorphism group; see `SolvingFrameworkPlan/docs/reports/TriangleSumSymmetryCounterexample.md`. The interface there is a separating triangle, so a 4-connected version is still open.]* If m(T) ≥ 3, then T has an orientation-preserving involution (a half-turn) each of whose two fixed points is either a degree-6 vertex or the midpoint of an edge joining two degree-6 vertices.
  - *Support:* 17:1 (fixed vertex 3, fixed edge 6–14) and 24:6406 (fixed edges 2–11 and 6–16). Two examples only; whether m = 2 graphs also often have such a half-turn was not checked, so the conjecture may have little discriminating power.

Neither conjecture is evidence for or against VH∃, U∃, M1 or C2.

## Files

- `counterexample_analysis.py`: sections A–F, reusing `wp18_core`, `wp19_core` and helpers from `analysis_17_1`.
- `counterexample-analysis.txt`: the complete output, including every certificate row above in full.

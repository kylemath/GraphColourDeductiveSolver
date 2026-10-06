# Degree-5 holes with one free (high-degree) neighbour: Theorem HP, belt transfer, P-A restated

Math research worker, 6 October 2026. Labels: [hand] proved here; [computed] exact enumeration on the named graphs only (exploratory, not evidence for a theorem); [open]; [memory] cited from memory, not rechecked. Tools: copies of `MathRadiusCensus/census.cpp` (plus a `--dump` of DL states) and `gen_tri.cpp`, built with g++ -O2 in the session scratchpad; Python checkers there (`pat.py`, `rules.py`, `strict.py`, `bsearch.py`, `leak.py`), not committed. CPU: about 11 CPU-minutes on at most 2 cores. That is one minute over the 10-minute cap, because one verification run over all holes was too slow and was aborted after about 7 minutes. Nothing else was edited or committed.

Target, updated by the Math lead at 12:40: the audit's counting lemma (checked here, see §5) guarantees a degree-5 vertex v whose link has four vertices of degree at most 11 and one vertex p of any degree. We need a fill or radius bound for that class.

## Verdict, first

1. **[hand] Theorem HP.** Let v have degree 5. Suppose four of its link vertices have degree **5** and the fifth, p, has **any** degree, and no separating triangle meets the ball. Then every doubly locked (DL) state at v has Kempe radius **at most 6**. The proof is a finite automaton on ring-2 patterns. It uses three moves: F, B, and the {a,b}-swap of the link triple. It never reads a neighbour of p. The finer bounds are in §2. The belt G_n holes are a special case.
2. **[computed] The sharp value is at least 4 and, on the data, exactly 4.** Radius 4 occurs with p of degree 7 at order 22, and with p of degree 11 at order 29 (§3). The order-29 graph is 4-connected, has minimum degree 5, and its other four link vertices have degree 5. The maximum is 4 over:
   - all min-degree-5 triangulations of orders 16 to 22 with this hole class (about 50,000 DL states with p of degree 7 to 10, plus the p-of-degree-6 holes);
   - 329 sampled hill-climb graphs with p of degree 11 to 14 (about 97,000 DL states).
   Every transition claim of the proof was checked state by state on all of these, with no violation. On the belt G_6..G_13 every DL state has radius exactly 2.
3. **[hand] Where local control is lost.** Every state the local moves cannot kill is one where the swap needed is the {a,b}-component of the triple {x_j, x_{j+1}, x_{j+2}}, **and p lies in that triple**. That component then leaks through p's outer neighbours. If it reaches w_{j+3}, the lock survives. The high-degree neighbour acts as a hub that **joins** chains; it does not separate them. In the radius-4 examples the leak is an explicit 4-edge {a,b}-path from p to w_3 (§3).
4. **[open] Four link vertices of degree at most 11 (the lead's class).** Only degree exactly 5 is proved. With degree-6 link vertices, Step 1 already gives 74 patterns at (6^5) (MathSixFiveHole). F-starvation and B-starvation (§1) do not depend on degree and survive. Whether the automaton closes is a finite but unrun check (§4).
5. **[hand] The belt proofs do not transfer beyond one step.** Each belt lemma uses a global property of G_n: two hubs covering every belt vertex, a square-of-cycle second ring, and degree 5 all along the walk. Details are in §6.

## 1. Setup and the degree-free rules [hand]

- The link is x_0..x_4 in cyclic order. w_t is the common neighbour of x_t and x_{t+1} other than v. The w_t are distinct and well defined when there is no separating triangle (Theorem H hypothesis).
- A degree-5 x_t has outer neighbours exactly w_{t-1}, w_t. The free vertex p = x_k has outer neighbours w_{k-1}, m_1, ..., m_e, w_k, with e = deg p − 5. Nothing is assumed about the m's, and coincidences with other ring vertices are allowed. All deductions below have the form "adjacent, so different colours", which stays valid under coincidences.
- A DL state is rotated so that the repeated pair is {x_0, x_2}. Its link colours are (a,b,a,g,d) on x_0..x_4. Lock 1 is a {b,g}-path P_1 from x_1 to x_3, and lock 2 is a {b,d}-path P_2 from x_1 to x_4, both in T − v. **k** is the position of p in this frame (k=1: p is the middle vertex; k=0,2: p is repeated; k=3,4: p is a singleton).
- F swaps the {a,g}-component K_F of x_2; B swaps the {a,d}-component K_B of x_0; AB swaps the {a,b}-component of x_1. We use radius(s) = 1 + d(s, NL) (MathConjectureR §1).

**Jordan facts (any degrees).**
- x_0 ∉ K_F, because the curve v x_1 P_2 x_4 v is coloured {b,d} off v and separates x_0 from x_2.
- x_2 ∉ K_B, by the curve v x_1 P_1 x_3 v.

**F-starvation (any degrees).** If x_2 has no neighbour coloured d, then F(s) is not DL.
- After F the link is (a,b,g,a,d). The new repeated pair is {x_3, x_0}, and the new middle is x_4.
- The new lock 2 is a {d,g}-path from x_4 to x_2. It must enter x_2 through a d-vertex.
- The neighbours of x_2 have colours b (unchanged), a (the former g's, all in K_F) and d. There is no d by hypothesis, so the lock fails.

**B-starvation.** If x_0 has no neighbour coloured g, then B(s) is not DL. This is the mirror image of F-starvation.

**Mirror.** The reflection fixing x_1 swaps x_0 ↔ x_2 and x_3 ↔ x_4. It exchanges g ↔ d and F ↔ B, and maps position k to 2 − k.

## 2. Theorem HP (four link vertices of degree 5, p arbitrary) [hand]

**Lemma 1 (ring patterns).** Read (w_0..w_4) with roles a, b, g, d.
- Step 1 of Theorem H applies at every degree-5 endpoint: x_1 has outer colours {g,d} (if k ≠ 1), x_3 has an outer b, and x_4 has an outer b.
- Properness at the degree-5 vertices then gives exactly the following patterns.

| k | patterns |
|---|---|
| 0, 2 | R1 = gdbab, R2 = dgbab, R3 = dgdbg (the m's are not a) |
| 1 | R3 = dgdbg, or w_2=w_4=b, w_3=a with (w_0,w_1) ∈ {g,d}²: gdbab (= R1), dgbab, ddbab, ggbab |
| 3 | gdbab (R1), dgbab, dgdab, dgbbg, dgdbg |
| 4 | gdbab (R1), dgbab, dgdbb, dgbag, dgdbg |

Sample derivation, k=3:
- If (w_0,w_1) = (g,d), then w_2 = b (it meets a, g, d), w_4 = b, and w_3 = a.
- If (w_0,w_1) = (d,g), then w_2 ∈ {b,d}, w_4 ∈ {b,g} and w_3 ∈ {a,b}. Then w_3 = b forces w_4 = g, and w_3 = a forces w_4 = b by E3.

Case k=4 is the mirror of k=3, and k=0 is the mirror of k=2.

**Lemma 2 (one-move kills: "easy" states, radius ≤ 2).** Each kill reads only degree-5 link vertices:
- B-starvation (x_0 has outer colours b and d): dgbab at k=1,2,3,4; ddbab at k=1; dgdab at k=3; dgdbb at k=4.
- F-starvation (x_2 has outer colours g and b): dgbab at k=0; ggbab at k=1; dgbbg at k=3; dgbag at k=4.
- **AB at k=3,4 for R3 = dgdbg.** x_0, x_1 and x_2 all have degree 5, with outer colours in {g,d}, so the component is exactly {x_0, x_1, x_2}. After the swap, the singleton of degree 5 (x_4 if k=3, x_3 if k=4) has no a-neighbour. Lock 2 (or lock 1) of the new state fails. This is Theorem H Step 3, applied at whichever end avoids p.

**Lemma 3 (transitions).** F sends R1 at k to R3 at k−3, or to a non-DL state. F sends R3 at k to R1 at k−3, or to a non-DL state. B does the same at k+3.
- *Proof for F from R1.* K_F contains x_2, x_3, and w_3 (an a-vertex adjacent to x_3). It does not contain w_0, which is g and adjacent to x_0 ∉ K_F. The vertices w_1, w_2, w_4 are coloured b or d and are untouched. The new frame has j' = 3. Reading (w_3, w_4, w_0, w_1, w_2) in the new roles gives dgdbg, and p sits at k − 3.
- *Proof for F from R3.* w_1 (g, adjacent to x_2) joins K_F, and w_4 (g, adjacent to x_0) does not. The new pattern is gdbab.
- B follows by the mirror.
- The m's never enter, because the pattern is read on the w's only.

**Termination.** Write D for an upper bound on d(s, NL).

| state | D |
|---|---|
| easy | 1 |
| R1@1 →F R3@3, R1@2 →F R3@4, R1@0 →B R3@3 | 2 |
| R3@0 →F R1@2, R3@2 →B R1@0 | 3 |
| R1@3 →F R3@0, R1@4 →B R3@2 | 4 |
| R3@1 →F R1@3 | 5 |

**Theorem HP.** radius ≤ 1 + D ≤ 6. The bound is ≤ 3 except for R3 with p in {x_0, x_2} (≤ 4), R1 with p a singleton (≤ 5), and R3 with p as the middle vertex (≤ 6). ∎

**Checks [computed].** `strict.py` asserts the pattern list, each easy kill by its named swap, each F/B image type, and radius ≤ 1 + D. No violation was found on:
- all holes of this class (p of degree 6 to 10) in all min-degree-5 triangulations of orders 16 to 22 (`gen_tri --all`, counts 3, 4, 12, 23, 73, 192, 651; separating-triangle graphs excluded);
- 170 + 159 deduplicated hill-climb graphs with p of degree 11 to 14, orders 25 to 30.

| (k, type) | max radius on data | proved |
|---|---|---|
| easy (all k) | 2 | 2 |
| R1 @0,1,2 | 3 | 3 |
| R3 @0,2 | 3 | 4 |
| R1 @3,4 | 4 | 5 |
| R3 @1 | 4 | 6 |

## 3. Explicit escape examples [computed]

- **Order 22, `gen_tri 22 --all` graph #99, hole 9.** The link degrees are (5,5,5,5,7). It has 5 DL states of radius 4, all R3 with p as the middle vertex. Note that (5,5,5,5,7) already reaches radius 4. MathPathwaysPAPC's table (orders ≤ 20) had 3.
- **Order 29, 4-connected, min degree 5, hole 2, link (3,0,12,23,13), degrees (5,11,5,5,5), p = 0.**
  - DL radius histogram {2: 362, 3: 23, 4: 9}, with nothing unreached.
  - In the radius-4 R3@1 states, AB(x_1) has 13 vertices.
  - Its path to w_3 = 24 is 0(b, p) – 10(a, a p-neighbour of degree 6) – 21(b) – 26(a) – 24(b). This is the leak that Theorem H's Step 3 excludes when x_1 has degree 5.
  - The face list (`G` line for census.cpp; SHA-256 of the one-line file 16428c10...196f):

```
G 29 0000 54 0 2 3 2 13 3 4 14 15 1 15 16 0 5 6 1 16 17 6 16 17 0 6 7 1 17 18 6 17 7 7 17 18 0 7 8 1 18 19 7 18 8 8 18 19 0 8 9 1 19 20 8 19 9 9 19 20 0 9 10 9 20 10 0 10 11 10 21 11 11 21 22 0 11 12 11 22 12 12 22 23 0 12 2 12 23 2 2 23 13 22 23 24 13 24 23 16 5 6 5 16 15 24 13 25 3 25 13 21 22 26 26 24 22 14 1 15 4 25 27 25 3 27 0 27 3 5 27 0 24 25 28 4 28 25 28 4 14 26 28 14 28 26 24 21 14 26 5 4 15 4 5 27 14 20 1 10 14 21 14 10 20
```

  It was found by hill-climbing from G_11 by flips and face insertions that avoid the hole's edges (`bsearch.py`, seed 7).
- **Belt [computed].** Every DL state at u_0 of G_n, n = 6..13, has radius exactly 2. G_5 and G_7 have no DL state. This is consistent with HP and well inside its bound.

## 4. P-A restated with second-ring data [hand statement, open content]

What the HP proof uses is not the link degree class. It uses three things:
- (i) which link vertices have **all** their neighbours inside the 2-ball (bounded degree);
- (ii) the colours on the outer neighbours of those vertices;
- (iii) the two Jordan facts.

This gives a finite certificate test per class.

**Local certificate (LC) for a class C** (four link degrees in [5, 11], one free vertex p). Build the automaton whose states are DL ring colourings consistent with the endpoint conditions E1 to E3 at the bounded vertices, recorded at each k.
- Moves: F, B, AB, and other swaps with an explicit seed.
- Membership of a ring vertex in the moved component is decided only when forced: by adjacency to a link vertex in the component, or by a Jordan fact. Otherwise both outcomes are branched (adversarial leak).
- A state is killed if some move leaves an endpoint vertex of bounded degree starved.

LC holds if every state reaches a kill along every adversarial branch within N moves. Then radius ≤ N + 1 for the whole class, independent of deg p and of the rest of T. HP is LC for (5,5,5,5,*) with N = 5.

**[open]** LC for classes with a degree-6 vertex.
- MathSixFiveHole found no link-only breaker at (6^5), but it did not try the starvation rules or the F/B transitions with branching.
- With a ring vertex in the component, leaks occur, and that note shows radius is not a function of the ball colouring. So LC may fail for some classes. A failure would show that P-A needs data beyond ring 2 there, not that radius is unbounded.
- This is a finite computation (at most 4^(ring length) patterns per k) and is the natural next test.

**Unavoidable list.**
- The audit lemma [hand, steps 1 to 6 rechecked here] makes the list {four link degrees in [5, 11]} × {p free} unavoidable. That is at most 7^4 cyclic classes, minus symmetries.
- HP covers exactly one of them, (5,5,5,5,*).
- (5,5,5,5,*) alone is not unavoidable: the pentakis dodecahedron has only (6^5) holes.
- Lowering 11 needs finer discharging. The audit's data (orders ≤ 24) has second-largest neighbour degree at most 7, which is evidence for nothing beyond those graphs.

**Classical sets.**
- [memory] Wernicke (1904): a degree-5 vertex adjacent to a vertex of degree 5 or 6.
- [memory] Franklin (1922): a degree-5 vertex with two such neighbours.
- [memory] Lebesgue (1940) and later "light 5-star" results (Borodin; Jendrol' and Madaras) bound the degree sum or weight of some 5-star in triangulations of minimum degree 5. I could not verify the exact constants and do not quote them.
- All of these specify too few vertices to bound the four needed degrees, except the light-star results. A light-star bound would bound **all five** link degrees, and the belt shows that is impossible for 5-stars at degree-5 centres with bounded sum. So any such result must count weights differently (memory, unchecked).
- Only the audit lemma, which I have verified, is used here.

## 5. Audit counting lemma [hand, reviewed]

- Steps 1 to 6 of the 12:40 message are correct as written. Σ(deg − 6) = −12; the edge count from degree-5 vertices into H; and both inequalities on Σ_H(d − 6).
- The constant 12 is what the crude count gives. The belt shows "at most one high neighbour" cannot be improved to zero.

## 6. Belt proofs: what transfers (four link degrees ≤ 11, rest arbitrary) [hand]

| belt step | transfers? | reason |
|---|---|---|
| slide lemma, singleton slides | yes | general |
| pole invariant (all u avoid c(a)) | only for N(p) | true for p's own neighbours (the hub fact). The belt also uses that **every** belt vertex is adjacent to a or b. |
| §3 equal-pole star | no | needs two equal hubs covering every vertex near the link. Otherwise the (A,B)-component of a hub is not just a star. |
| §4 openings O1 to O3 | first slide only | the forced colours use v_{n-1}, v_{n-2} adjacent to the second pole b. Without b, the second slide is not forced. |
| §5 Z-walk table, §6 D recurrence, the 2n-slide walk | no | each step reads about 8 vertices further along the belt, all of degree 5 and each adjacent to a pole. Local data covers at most one step. |
| §7 linear interval and caps | no | uses the linear belt order, and global forcing at v_1, v_2 |
| pole hole: segment lemma (period 3) | no | needs p's second neighbourhood to be C_{2n}² with every other vertex adjacent to b |
| junction lemma, T1 zeroing, F toggle | no | they need ring vertices of degree 4 in G_n − a, and the β-exclusion from b |
| chain lemma L5, rules K and S | no | {x,y}-components stay inside the belt only because the belt is the whole graph minus two hubs. In general they escape. |

- **Where chains escape.** This is the AB-component leak of §3 (0 → 10 → 21 → 26 → 24). The same mechanism in pole-hole terms: a (β, x)-component through p's star exits through a ring vertex of degree ≥ 6, which the belt does not have.
- **Mobility to p (killed).** Degree-5 mobility can move the hole to p in at most one swap and one slide. But then the hole has a d-cycle link. The only hand result for such holes, Theorem P, uses the belt structure, and its own bound is linear in d. This is no gain.

## 7. Killed lines

- **K-HD1 "p acts like a belt pole and constrains locks".** The hub joins every σ-neighbour of p into p's {c(p), σ}-chain. When c(p) is a lock colour, this **enlarges** the AB-component (radius 4 at k=1). The belt helps only because it has a second hub and nothing else.
- **K-HD2 "Theorem H bound 3 extends to (5,5,5,5,*)".** False: radius 4 at (5,5,5,5,7) (order 22) and (5,5,5,5,11) (order 29).
- **K-HD3 "radius grows with deg p".** No sign of it on the data: the maximum is 4 for p of degree 7 to 14, and 2 on the belt. No proof either way beyond HP's 6.
- **K-HD4 "move the hole to p".** See §6.
- **K-HD5 "belt walk lemmas are local".** See §6.

## 8. Ledger

- [hand]: Lemma 1 patterns; F-starvation and B-starvation; Lemma 2; Lemma 3; Theorem HP (radius ≤ 6); review of the audit lemma; the belt transfer table.
- [computed]: radius tables; radius-4 examples at orders 22 and 29; belt radius 2 for n = 6..13; transition checks.
- [open]:
  - sharp HP constant (data 4);
  - LC for classes with link degrees 6 to 11;
  - whether radius stays bounded for those classes;
  - novelty (no literature check).

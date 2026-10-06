# Theorem-H-style attack on (6,6,6,6,6) holes (P-A next trial)

Math research worker, 6 October 2026. Labels: [hand], [computed], [open]. Compute: own C++ (`six.cpp`, a copy of `census.cpp` extended with ring-pattern and swap analysis, built with g++ -O2 in the session scratchpad, not committed) on `gen_tri` output for orders 12..23 (all min-degree-5 triangulations, including separating triangles; counts 1,1,1,3,4,12,23,73,192,651,2070 reproduced) plus the pentakis dodecahedron. About 8 CPU-minutes. Order 24 was started and abandoned (generator still running at the time limit). Nothing else edited, nothing committed.

## Verdict, first

1. **[hand + computed] Step 1 does not survive.** For a hole whose five neighbours all have degree 6 the ring is a 10-cycle w_0 m_1 w_1 m_2 w_2 m_3 w_3 m_4 w_4 m_0 (w_t common to x_t, x_{t+1}; m_t the middle outer neighbour of x_t). The two locks force only four endpoint conditions: x_1 has a g-neighbour and a d-neighbour among {w_0,m_1,w_1}; x_3 and x_4 each have a b-neighbour among {w_2,m_3,w_3} and {w_3,m_4,w_4}. Together with properness these allow **exactly 74 ring colourings** (R1-R3 become 74). **69 of the 74 occur** in a DL state at some hole of orders <= 23 plus the pentakis dodecahedron; 5 never occurred (gadbdabagb, gadbdabagd, gadgdababd, gadgdabagb, gadgdabagd; ring read w_0 m_1 w_1 ... m_0 with roles a,b,g,d; whether a Jordan argument excludes them is [open]).
2. **[computed, exhaustive over the 74] Step 3 has no analogue.** For none of the 74 patterns is there a Kempe swap whose component lies inside the link {x_0..x_4} and kills a lock (a link-only breaker). Hand case: the {a,b}-component of x_1 would be {x_0,x_1,x_2} only if w_4 m_0 w_0 m_1 w_1 m_2 w_2 are all in {g,d}, hence alternate g,d; w_2 is adjacent to x_3 = g and x_2 = a so w_2 = d, which forces w_4 = d, adjacent to x_4 = d. Contradiction.
3. **[computed] What replaces it.** Under the clean-outside assumption (the component computed inside the 15-vertex ball link + ring is the whole component), every one of the 74 patterns has a ball-closed lock breaker, always containing exactly one or two ring vertices (smallest breaker: one ring vertex in 56 patterns, two vertices in 18, e.g. {w_1} as a (g,d)-component for gadbdababd; {w_0, x_1} as a (b,g)-component for gadgbababd). But a ring vertex always has outside neighbours (w_t has 4 neighbours in the ball, so degree >= 5 gives >= 1 outside neighbour; m_t has 3, so >= 2), so the component can leak. **No degree hypothesis closes the ball**; the exact obstruction is a colour condition on outside neighbours of at most two named ring vertices.
4. **[computed] Radius is not a function of the ball colouring, and it is 3 at some (6^5) holes.** Pentakis: 130 DL states, all radius 2 (confirmed). Over all (6^5) holes of orders <= 23 and pentakis (78 holes, 3,966 DL states): max radius **3**; 69 states of radius 3 (all at orders 22, 23), 3,897 of radius 2. Dichotomy observed in all 3,966 states: **radius 2 iff some ball-contained component breaks the lock; radius 3 iff none**. The same ring pattern occurs with radius 2 and radius 3 (e.g. dagbdbabgb, 4 radius-3 states and many radius-2), in different outer completions. So the P-A hope "pentakis gives a local theorem with R = 2" is **killed**: pentakis has radius 2 only because of its outer structure.
5. **Theorem I can prove by hand:** only the conditional statement in section 3 (clean outside implies radius <= 2) and Lemma 1 (74 patterns) and Lemma 2 (no link-only breaker); **no unconditional bound R for (6^5) holes is proved**. Computed: sup radius at (6^5) holes is >= 3 and is 3 up to order 23 [computed, not evidence for a bound].

## 1. Setup and pattern lemma [hand]

Hypotheses (as in Theorem H, to be stated): v has degree 5, link x_0..x_4 each of degree 6, no separating triangle through the ball, so the ten vertices w_0..w_4, m_0..m_4 are distinct. Faces force the ring order: the link of x_t is the cyclic sequence v, x_{t+1}, w_t, m_t, w_{t-1}, x_{t-1}, so w_{t-1} m_t w_t is a path. Chords inside the ring (a ring vertex adjacent to a non-consecutive ring vertex) are not excluded by any hypothesis; they do not matter for the endpoint conditions.

DL after rotation: s = (a,b,a,g,d); lock 1 a {b,g}-path P_1 from x_1 to x_3, lock 2 a {b,d}-path P_2 from x_1 to x_4, both in G - v.

**Lemma 1.** x_1 has neighbours v, x_0, x_2 (a) and the three outer vertices; P_1 and P_2 leave x_1 through outer vertices of colour g and d. P_1 enters x_3 through a b-vertex, necessarily outer (x_3 ~ v, x_2 = a, x_4 = d); P_2 enters x_4 through an outer b-vertex. So the ring colouring satisfies (E1) {w_0,m_1,w_1} contains g and d, (E2) {w_2,m_3,w_3} contains b, (E3) {w_3,m_4,w_4} contains b, plus properness (consecutive ring vertices differ, w_t differs from x_t, x_{t+1}, m_t from x_t). [hand] The count of such colourings is **74** [computed, enumeration of 4^10 colourings]. For (5^5) the corresponding count is 3 (R1-R3).

Observed in DL states of 78 holes: 69 distinct patterns (all inside the 74), see item 1 for the five never seen.

## 2. Which part of Theorem H survives

- **Step 1** [replaced by Lemma 1]: 3 patterns become 74.
- **Step 2** (R2: F(s) is not DL because x_2 loses its only d-neighbour): needs x_2 to have exactly two outer neighbours, one of them in K_F. Here x_2 has three outer neighbours w_1, m_2, w_2; the pattern has no forced d among them. **Not extended, not tested beyond this remark [open]**: F-steps were not recomputed for (6^5) states.
- **Step 3** (R3: three-vertex swap): killed, Lemma 2.
- **Step 4** (F(R1) is R3 or non-DL, using the Jordan curve of P_2 to keep x_0 out of K_F): the argument pattern (forced membership of ring vertices adjacent to x_2 or x_3 in K_F, separation by P_2) still applies verbatim to x_0 not in K_F, but the conclusion "ring of F(s) is R3" has no meaning because the target set is the 74-set and the ring now has ten vertices, three of which can change colour next to x_2 and x_3. **Not extended [open].**
- **Survives:** the framework radius(s) = 1 + d(s, NL), the endpoint reasoning of Step 1, the Jordan-curve idea, and the shape "swap a very small component near x_1 / x_3 / x_4". What changes: the small component contains a ring vertex, and a ring vertex has free outside neighbours.

**Lemma 2 (no link-only breaker) [computed, exhaustive over the 74; hand case above].** A swap whose component is contained in the link needs every outer neighbour of every member to avoid both swapped colours; checked for all six pairs, all 74 patterns: either no such component exists or its swap leaves all three endpoint conditions intact (so the swapped state is locally DL-compatible; it is non-DL only if the outer paths are missing, which cannot be decided from the ball).

## 3. Conditional theorem [hand]

**Theorem C.** Let s be DL at a (6^5) hole with ring colouring in the 74-set and let K be a {p,q}-component of the colouring on the 15-vertex ball B = link + ring. Suppose (clean outside) no vertex of K has a neighbour outside B coloured p or q, and no other component of B in colours {p,q} is joined to K outside B. If the swap of K leaves some endpoint condition (E1 after recomputing the new repeat index, or E2, E3) false, then the swapped state is not DL, and radius(s) <= 2.
Proof: K is then a full component of G - v, swapping it is a legal Kempe move, and non-DL follows from Lemma 1 applied to the new state (the endpoint condition is necessary for DL). Radius <= 1 + d(s, non-DL) = 2. [hand; tautological given Lemma 1, but the table below gives which K.]

**[computed] Table of smallest ball-closed breakers.** Size 1: 56 patterns, a single ring vertex recoloured; size 2: 18 patterns. Every pattern has at least one. Sample: gadbdababd: {w_1} in {g,d}; gadgbababd: {w_0,x_1} in {b,g} or {w_1,x_1} in {b,d}. Full list in the session scratchpad (`rob.py`, not committed).

**Obstruction [computed, exact on the data].** The hypothesis "clean outside" is a condition on the colours of the outside neighbours of at most two ring vertices (w_t has >= deg-4 and m_t >= deg-3 outside neighbours). It cannot be turned into a degree hypothesis: a ring vertex of degree 5 still has one outside neighbour, whose colour is free. Radius-3 states are exactly the states for which every ball-closed breaker leaks (3,897 radius 2 / 69 radius 3 over 3,966, dichotomy holds in every state). The leak connects the breaker vertex through outside {p,q}-paths to other ring vertices; killing it needs a second swap, hence radius 3. An upper bound for radius-3 states would need either the Jordan-curve restriction on which ring vertices can be joined outside (planarity, lock paths P_1, P_2) or a bound on the number of leaks. Neither is derived. A hand theorem 'every DL state at a (6^5) hole has radius <= 3' is **[open]**; data: true up to order 23 and for pentakis.

## 4. Computed tables

Holes with all five neighbours of degree >= 6, orders 12..23 and pentakis (order 32); link class = cyclic degree sequence; DL states = canonical colourings; radius = Kempe radius (distance to a filled state). Classes occurring with min link degree >= 6 in orders <= 23: only four (none at orders <= 20; order 21 has two (6^5) holes).

| link class | holes | DL states | max radius |
|---|---|---|---|
| 6,6,6,6,6 | 78 (66 at orders 21-23, 12 pentakis) | 3,966 | **3** (pentakis alone: 2) |
| 6,6,6,6,7 | 24 | 1,024 | 3 |
| 6,6,6,6,8 | 1 | 48 | 2 |
| 6,6,7,6,7 | 1 | 48 | 3 |

Counts of the per-order (6^5) holes: order 21: 2 holes, radius 2; order 22: 14 holes (2 of radius 3, 1 hole with no DL state); order 23: 50 holes (radius 3 at 23 of them). Larger classes (7,7 neighbours etc.) are not present below order 24 in these tables. For comparison the earlier MathPathwaysPAPC table lists only the pentakis class (6^5) = 2; that table covered orders 12..20 plus pentakis only.

## 5. Killed lines

- **K-S1 "R1-R3 survive when the ring-1 vertices have three outer neighbours".** False: 74 patterns, 69 realised.
- **K-S2 "swap the component {x_j,x_{j+1},x_{j+2}} / any link-only component to break the lock".** False for all 74 patterns (Lemma 2, hand case for x_1's ab-component).
- **K-S3 "(6^5) holes have radius 2, so the pentakis value is the class value".** False: radius 3 at 69 DL states, orders 22 and 23.
- **K-S4 "radius is determined by the ball colouring".** False: same ring pattern, different radius in different outer completions.
- **K-S5 "an outer-degree hypothesis (degrees 5 for ring vertices) makes the ball closed".** False: the ball is never closed (each ring vertex has >= 1 outside neighbour).

## 6. Ledger and next step

[hand]: Lemma 1 conditions, Lemma 2 for the x_1 ab-component, Theorem C (conditional, tautological given Lemma 1), killed lines. [computed]: 74 patterns, 69 realised, no link-only breaker, ball-closed breaker table, radius dichotomy, class table, orders <= 23. [open]: Jordan exclusion of the 5 unseen patterns; extension of Steps 2 and 4 (F-steps) to ten-vertex ring; an unconditional bound at (6^5); order 24 and above (radius 4 possible).
**Next step if pursued:** classify leaks using the Jordan curves of P_1, P_2 (they split the ring into arcs; only ring vertices on the same side of both curves can be joined outside by a {p,q}-path), which is a finite planar-connectivity automaton on the 74 patterns, and test whether it forces radius <= 3.

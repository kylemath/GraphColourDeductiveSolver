# Pathway sketches P-A and P-C (Math), 6 October 2026

Labels: [hand], [computed, exploratory, post hoc] (orders 12 to 20 plus one 32-vertex graph, not evidence for a theorem), [open]. Kill tests used about 3 CPU-minutes. Tools: `MathRadiusCensus/census.cpp` (hash-checked package), `MathPathways-scripts/pc_fans.py`.

## P-A: good link classes plus discharging

**Claim to test.** Classify degree-5 holes by the cyclic degree sequence of their link. For each class there is a bound R(class) on the Kempe radius of doubly locked states; and the classes with a proved bound form an unavoidable set (every core triangulation contains a degree-5 vertex of such a class).

**What is proved.** (5,5,5,5,5): radius at most 3 (Theorem H, hand, independently reviewed). A neighbour of degree at most 4: at most 3 pure swaps (not available in the minimum-degree-5 core). Nothing else.

**Radius by link class [computed].** All minimum-degree-5 triangulations of orders 12, 14, 15, 16, 17, 18, 19, 20 (1, 1, 1, 3, 4, 12, 23, 73 graphs) plus the pentakis dodecahedron (order 32); every degree-5 hole, all doubly locked states, exhaustive Kempe radius. 28 link classes occur; **no targetless class in any**. Maximum radius per class (holes / doubly locked states):

| link (cyclic degrees) | max radius | | link | max radius |
|---|---|---|---|---|
| 5,5,5,5,5 | 3 (42/924) | | 5,5,6,6,6 | 3 |
| 5,5,5,5,6 | **4** (154/2366) | | 5,6,5,6,6 | **4** (131/1916) |
| 5,5,5,5,7 | 3 | | 5,6,6,6,6 | 3 |
| 5,5,5,5,8 | 3 | | 6,6,6,6,6 | **2** (12/1560, the 12 holes of the pentakis dodecahedron) |
| 5,5,5,6,6 | **4** (163/2668) | | classes containing a 7, 8 or 9 | at most 4, most 2 or 3 |
| 5,5,6,5,6 | **4** (177/2476) | | | |

Radius 4 occurs in exactly six classes: (5,5,5,5,6), (5,5,5,6,6), (5,5,5,6,7), (5,5,6,5,6), (5,5,6,5,7), (5,6,5,6,6). **No class has a maximum above 4.** The first witnesses are at order 17 (T4 is one of them).

**Hand example.** The pentakis dodecahedron (dodecahedron with a pyramid on every face): 12 vertices of degree 5, each with link (6,6,6,6,6), 20 of degree 6. At a degree-5 hole, 4,840 canonical colourings, 3,190 filled, 130 doubly locked, all of radius exactly 2. All 12 holes are equivalent.

**Why this sketch fails as a proof strategy, now.** [hand] The icosahedral class is not unavoidable: any triangulation with degrees 5 and 6 only and no two adjacent degree-5 vertices (the pentakis dodecahedron, and the Goldberg-type triangulations like it) has **only (6,6,6,6,6) holes**. So a discharging argument must cover the class (6,6,6,6,6) as well, and any set of good classes covering all minimum-degree-5 triangulations must include a class that contains no 5-neighbour. Wernicke's theorem (a degree-5 vertex with a neighbour of degree 5 or 6) does not help: those classes all occur, and radius 4 appears among them. So a discharging proof needs a bound for every class that can be the only class in a triangulation, which is Conjecture R for these classes. **P-A reduces to proving bounds class by class for at least (5^5) [done], (6^5) [open], and one mixed class** such that the three together are unavoidable; no such unavoidable list is known to Math.

**Kill test and verdict.** The claim "radius at most 4 for every link class" **survives** at orders up to 20 (and 32 for one graph); it is only a restatement of Conjecture R in data form. The claim "(5^5) is an unavoidable class" is **killed** by the pentakis dodecahedron. **Next trial:** a Theorem-H-style local pattern argument for (6,6,6,6,6) holes (ring-1 vertices have three outer neighbours); the first thing to check is whether the three ring-1 patterns R1–R3 survive.

## P-C: freedom in the fan and in T*

**Claim to test.** For some legal fan at v, every inductive colouring of T* restricts to a state that fills in at most one swap.

**Structural fact [hand].** A colouring of T*_j is exactly a colouring of T − v in which the apex x_j is a **singleton** on the ring (its chords force x_j to differ from every other ring vertex). Every unfilled state has exactly three singleton positions, so it is admitted by three of the five fans. If a hole has any targetless component, Theorem A puts all five pair types (hence all five repeat indices) inside it, so every legal fan admits a targetless state: **the fan freedom cannot avoid a targetless component**. This is Corollary B again: a good fan exists iff no targetless state has its hole there. P-C therefore does not give a route that bypasses clean-vertex existence.

**Kill test [computed].** For every degree-5 hole of every minimum-degree-5 triangulation of orders 12, 14, 15, 16, 17, 18 (279 holes, legal fans only), the maximum Kempe radius over the states a fan admits, minimised over fans ("best fan"):

| best-fan max radius | 1 | 2 | 3 | 4 |
|---|---|---|---|---|
| holes | 92 | 159 | 24 | 4 |

The claim "some fan has every admitted state within one swap" is **killed**: it fails at 187 of 279 holes. Moreover at four holes the best fan still admits a radius-4 state, so the fan freedom does not lower the worst radius at the radius-4 holes (consistent with the structural fact above). **Verdict:** P-C as stated is dead; the only surviving use of the fan freedom is to avoid states with a particular repeat index when the bad states are confined to some indices, which Theorem A forbids for targetless components and which is a statistics statement for finite radii.

**What both sketches teach.** The bound that matters is a uniform radius bound over all link classes (Conjecture R); local class-by-class arguments exist only for the icosahedral class. The next pathway to try is a Theorem-H-style argument for the class (6,6,6,6,6), which also gives a first non-icosahedral class.

## Addendum (6 Oct, after the audit's link-class kill, 74436a8)

The audit shows the link degree class does not determine the radius: (5,5,5,5,6) has radius 2 at every order-14 hole and radius 4 at T4 holes 0 and 16. **P-A restated:** the controlling local data is not the cyclic link degree sequence but the structure of the **ring-1 vertices' outer neighbourhoods** (how many outer neighbours each has, and, if needed, the degrees on the second ring), because Theorem H's argument needs to know where a lock path can exit the ball.

**Can a finite list of such patterns be unavoidable? [hand]** Not if the pattern must bound the degrees of **all five** ring-1 vertices. The belt G_n kills it: every degree-5 vertex of G_n (u_i, v_i) has exactly one neighbour of degree n (a pole, adjacent to every u_i, or b, adjacent to every v_i) and four of degree 5, so its link class is (5,5,5,5,n) with n arbitrarily large. A finite list of patterns bounding all five ring-1 degrees therefore misses the whole belt family. Any unavoidable family needs patterns in which one or more ring-1 vertices have **unbounded** degree, with a separate lemma controlling the chains through a high-degree neighbour. The belt (compiled, `belt_theorem_all_holes`) is such a case; whether a general lemma exists is [open]. Classical discharging gives only configurations that specify a few vertices (for example Wernicke's 5-5 or 5-6 edge), which is too little for the exit-pinning argument.

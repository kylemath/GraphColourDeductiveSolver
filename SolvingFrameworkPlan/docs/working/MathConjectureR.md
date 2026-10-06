# Attack on Conjecture R (finite / bounded Kempe radius of doubly locked states)

Math research worker, 6 October 2026. Hand work plus small exact enumerations (about 8 CPU-minutes, 1-2 processes, graphs of order <= 32; scripts in the session scratchpad, not committed). No census, no declared experiment, no status change, no other file edited. Labels: [hand], [computed], [open]. Builds on `MathConfinementAttack` (Thm A, Cor B), `MathCleanVertexAttack` (Thm C, D), `creative-intel-2026-10-05/l-attack.md`, `MathChainSearch/lt_certs` (W6, A3).

## Verdict, first

- **[computed] The bound R = 3 suggested by A_3..A_5 is false: radius 4 occurs** on a 17-vertex triangulation with minimum degree 5, 12 vertices of degree 5 and 5 of degree 6, and no separating triangle (30 triangles = 30 faces). So the "radius <= 3" folklore is dead; an absolute R, if it exists, is >= 4.
- **[computed] On the symmetric family A_r (hole at the 5-fold centre) the radius of every doubly locked state is exactly 2 for r = 4, 5, 6 (all 80, 530, 2450 DL states), and 2 or 3 for r = 3.** No targetless Kempe class exists on any graph tested (every canonical colouring of T-v reaches a filled state).
- **[hand] Exact reduction:** radius r(s) = 1 + (Kempe distance from s to a state that is not doubly locked). Finite R fails iff some Kempe class at v lies entirely inside the doubly locked set.
- **[hand] F/B dichotomy:** r(s) <= 1 + min(chain_F(s), chain_B(s)). So L-type bounds give R-bounds; the A_r orbits (infinite chains) are filled by other swaps, and no uniform "k F-steps then fill" description is true (killed line K2).
- **[open] Whether R holds (finite radius) for doubly locked states: undecided.** All evidence is for finiteness; no proof. Any proof must reintroduce lock-path geometry (see §5); R for all triangulations at degree-5 holes implies 4CT by a Kempe argument (same warning as Prop 3 of MathConjectureL), so it is hard.

## 1. Exact reduction [hand]

State s at a degree-5 hole v: proper 4-colouring of T-v. Unfilled = link uses 4 colours, one repeated pair {x_j, x_{j+2}}. NL = filled states together with unfilled states that are not doubly locked.

- If s is unfilled and not doubly locked, one swap fills it (Step 1 of MathConfinementAttack: swap the βγ or βδ component of the middle single x_{j+1}; that component misses the other link vertices of those colours, so the link loses a colour).
- Hence for a doubly locked s: **r(s) = 1 + d(s, NL)**, where d is the Kempe distance by whole-component swaps in T-v. (The lower bound is obvious; the upper bound is the previous sentence.)
- A Kempe class of s at v is **targetless iff it contains no state of NL, i.e. consists of doubly locked states.** Finite radius for every DL state is equivalent to: no targetless class. Bounded radius is the extra statement sup r < infinity.
- This restates Cor B: R (finite form) is equivalent to "every degree-5 hole is clean".

## 2. F/B dichotomy and what it does not say [hand + computed]

F(s) = swap of the {c_j, c_{j+3}}-component of x_{j+2}; B(s) = swap of the {c_j, c_{j+4}}-component of x_j (Thm C). Both are single swaps, so
**r(s) <= 1 + min(chain_F(s), chain_B(s))** where chain = number of DL states met before leaving DL (infinite if the orbit is periodic inside DL).
So a chain bound N (Conjecture L) would give radius <= N+1. L is false (W6, A_r), but the converse direction is what the data show: [computed, all DL states of each listed hole]

| graph, hole | (radius, min F/B chain): count |
|---|---|
| A_3, centre | (2,inf):10, (2,1):10, (3,inf):10 |
| A_4, centre | (2,inf):20, (2,1):60 |
| A_3, ring-1 vertex | (2,1):12, (2,2):2 |
| A_4, ring-1 vertex | (2,1):26, (2,2):2 |
| flipped A_3 (below), v=4 | (2,1):12, (2,2):3, (3,2):3, (3,3):1, (4,3):2 |

Reading: when the F/B chain is finite, radius is within +1 of chain and often equal to 1 + chain (so radius 4 on the last row has chain 3). When the F-orbit is infinite (A_r centre, the A_3 states with period 60), the fill uses a swap outside the F/B family (A_4 centre: the 20 infinite-chain states have radius 2). So the infinite chains of Long Table are harmless exactly because Kempe class is larger than the F-orbit, as stated in `l-attack.md` §0.3.

## 3. Exhaustive data [computed]

Method: enumerate all proper 4-colourings of T-v up to colour renaming (DFS), build the Kempe graph (all whole-component swaps, all six colour pairs), multi-source BFS from filled states, classify DL states by the Math definition (Step 1 locks). Reproduces A_3: 100 canonical colourings, 40 filled, DL 30 with radii {2:20, 3:10} (matches Long Table and Math's earlier BFS distance 3).

A_r, hole = centre v (five-fold symmetric):

| r | n | canonical colourings | filled | DL states | DL radius | not-DL unfilled radius |
|---|---|---|---|---|---|---|
| 2 (icosahedron) | 12 | 20 | 10 | 0 | none | 1 |
| 3 | 17 | 100 | 40 | 30 | 2:20, 3:10 | 1 (30) |
| 4 | 22 | 520 | 200 | 80 | 2:80 | 1 |
| 5 | 27 | 2720 | 1040 | 530 | 2:530 | 1 |
| 6 | 32 | 14240 | 5440 | 2450 | 2:2450 | 1 |

(Max radius over all states of A_4, A_5, A_6 is 2: every state is within 2 swaps of filled; unreached = 0 in all rows.) The DL counts 30, 80, 530, 2450 are not obviously a closed form; not pursued.

All other degree-5 vertices of A_3 and A_4 as holes: DL radius is 2 for all (14 and 28 DL states per hole respectively). So the radius-3 states of A_3 occur only at the two poles.

**Radius 4 (the new data point).** Triangulation T4 on 17 vertices, faces (vertex labels 0..16):
(0,1,2) (0,1,5) (0,2,3) (0,3,4) (0,4,5) (1,2,6) (1,5,10) (1,6,10) (2,3,7) (2,6,11) (2,7,11) (3,4,8) (3,7,8) (4,5,9) (4,8,9) (5,9,10) (6,10,15) (6,11,15) (7,8,12) (7,11,12) (8,9,13) (8,12,13) (9,10,14) (9,13,14) (10,14,15) (11,12,16) (11,15,16) (12,13,16) (13,14,16) (14,15,16),
hole v = 4 (link 0,3,8,9,5). Degrees: twelve 5s, five 6s; 30 triangles, 30 faces (no separating triangle: it is in the 4-connected core). 68 canonical colourings, 22 filled, histogram of radius over all states {0:22, 1:25, 2:15, 3:4, 4:2}, 21 DL states with radii {2:15, 3:4, 4:2}, nothing unreached. T4 was found as a 1-flip neighbour of A_3 (obtained by random edge flips preserving minimum degree 5); it was re-derived and its degrees/triangles checked.

Short searches (flip walks within minimum degree 5, starting from A_3 and A_4, about 2200 graph evaluations, orders 17 and 22; plus 3400 random flipped A_3/A_4 samples; plus 167 random minimum-degree-4 triangulations of order 12-17): maximum DL radius found is 4, never 5; **no targetless class in any of ~5800 graphs.** The min-degree-4 random sample (1000s of states each) had max radius 2 (small, weak evidence: random graphs of this kind have lots of slack). The search is far too small to say radius 5 does not exist.

Protected-face check [computed, A_3 and A_4]: for the centre hole and for the ring-1 hole of both A_3 and A_4, for every face phi disjoint from the closed neighbourhood of v (15, 13, 25, 23 faces), I forbade every swap whose component contains a vertex of phi (phi "frozen" with its colours). The radius histograms and "unreached = 0" are **identical** to the unprotected ones in all cases. So at these examples the fill never needs to recolour a remote face. This is a statement about a face far from v, not about phi touching the link (untested, [open]).

## 4. Why the radius is small on A_r (aim 1) [hand/computed, partial]

[hand] Not an explanation, but the exact mechanism visible in the data:
1. Every DL state's Kempe class contains a non-DL state at distance 1 (the radius-2 states). So generically there is **one swap that destroys a lock**; after it, Step 1 fills.
2. At A_r centre the first swap is not F or B for the 20 (A_4) infinite-chain states; the swap listing (swap options leading to a distance-minus-1 state) shows only mixed types: alpha-gamma component containing x_j, alpha-delta containing x_{j+2}, gamma-delta containing {x_{j+3}, x_{j+4}} (the "G swap": always available because x_{j+3}, x_{j+4} are adjacent), or beta-delta / beta-gamma components avoiding the link entirely. There is no single type (killed line K2). The G swap exchanges gamma and delta on the link pair, keeping the repeat index; it is the natural candidate to break a lock because it replaces the gamma/delta labels at the two ends of P1, P2 and so asks for a new beta-delta path to x_{j+3} and a new beta-gamma path to x_{j+4}, which need not exist. [open: prove for A_r that G or an analogous swap breaks a lock; the five-fold symmetry should make this checkable ring by ring, but I did not get a clean proof.]
3. [hand] Why the *F-orbit* does not decide the radius: Thm C/D show equidistribution of repeat types and balance of slides, abstractly consistent with every state in the class being DL (the meta-obstruction of MathCleanVertexAttack §4). The infinite F-orbits in A_r are therefore not an obstruction to R; they say only that the F/B subgraph of the Kempe graph can be a closed cycle with exits via other swaps.

## 5. Radius bound under hypotheses; what obstructs a general bound (aims 2, 3) [hand]

What can be proved:
- **P1.** r(s) <= 1 + min(chain_F, chain_B) (§2). Hence bounded chain implies bounded radius; this is the only unconditional bound I can give.
- **P2.** r(s) <= 1 + d(s, NL); R finite iff no Kempe class sits inside DL (§1).
- **P3 (reflection of the old mobility facts).** If some degree-<=4 vertex w is adjacent to v (or in the core a degree-5 neighbour w with a non-DL state of w's own link at distance 1), the slide/mobility facts of MathTraceFourConnAttack already give a fill. Nothing new, and it needs degree <= 4 vertices that the core excludes off phi.

What blocks a general theorem:
- **[hand] Locality gap.** A swap that breaks a lock must change the colour class of some vertex on the lock path while keeping the link 4-coloured; the swapped component K meets P1 or P2 at a vertex but the new lock needs to cross the Jordan curve v-x1-P1-x3 (Lemma 2 of `l-attack.md`). Whether such a K exists depends on how many vertices of P1 outside the F-component remain, which is unconstrained by planarity (W6 and A_r satisfy it six times and forever). So a radius bound has to count something like "the number of distinct lock paths", and I found no invariant.
- **[hand] Compatibility with A_r radii.** The data show the radius depends on the hole position and the graph (A_3: poles 3, others 2; T4: 4). So a bound would have to be uniform over graph structure, not over a symmetry; no mechanism at the level of Jordan curves distinguishes T4's radius-4 states from A_3's radius-2 states (T4 is a one-flip neighbour of A_3).
- **[hand] Hardness.** R for all degree-5 holes of all triangulations with finite radius = a Kempe-style elementary 4CT proof (every colouring of T-v reaches a fill in finitely many swaps). It cannot be a cheap lemma (cf. MathConjectureL Prop 3). Note, however, that 4CT alone does not give finite radius: the Kempe class of s may be separate from every filled one (Kempe classes of planar 4-colourings are known not to be unique in general, e.g. some Fisk-type triangulations), so R is a statement beyond 4CT, and it could fail by a Kempe-isolated class even though the graph is 4-colourable. [hand; the classes-non-unique fact is cited from memory, not rechecked]. For the hole version at a specific v, I have no example of a disconnected class that is wholly DL, and the exhaustive data (5 graphs families, 100s of colourings) give none.

## 6. Protected-face version (aim 4) [hand]

The induction needs the fill to be compatible with the protected triangle phi. Precisely, one of:
- **R_phi (strong):** every doubly locked state at an off-phi degree-5 v has a fill by whole-component swaps none of whose components contains a vertex of phi (phi stays coloured). This is exactly the "frozen face" computation of §3; the exhaustive data show no change for faces away from N[v].
- **R_phi (weak):** swaps may recolour phi but the final state must be usable: the setting of MathConfinementAttack allows phi to be recoloured. That is the unprotected R, which this note supports. If the bookkeeping needs phi's colour pattern restored (colours of the three vertices of phi up to renaming), then components containing phi must be swapped in pairs or the restriction in R_phi (strong) applies.
- Needed in either form: (i) the case where phi meets N[v] (a link vertex x_i in phi cannot move, so locks through x_i are frozen; this changes the structure of Steps 1-2 because a component swap through x_i is no longer allowed), untested, [open]; (ii) the 4-connected-core hypothesis (min degree 5 off phi, no separating triangle other than phi) must hold for the graph, which it does for A_r and T4.
- Prediction: the strong form is likely false in extremal cases where the only lock-breaking component contains a vertex of phi; I have no example.

## 7. Killed lines

- **K1: "R = 3"** (from A_3..A_5 radii 2-3). Dead: T4 has radius 4 [computed, exact].
- **K2: "uniform fill: swap the component of x_{j+2} (or x_j) in an unlocked pair after k F-steps."** Dead as stated: in A_r the infinite-chain states are filled by non-F/B swaps, F-chain being periodic inside DL; for finite chains, the F/B-then-fill description is true (P1) but not uniform (the radius can be less than 1 + chain, e.g. (2,2) rows).
- **K3: "radius is determined by the F-chain length"**: dead; infinite chain has radius 2 or 3, and the (2,2),(3,2) rows show the two are not related by a formula.
- **K4: bound R from the abstract data (Thm A, C, D, equidistribution, Euler/degree sum).** Dead by the meta-obstruction (MathCleanVertexAttack §4); radius is not even constrained by those counts.
- **K5: "random min-degree-4 triangulations are evidence for R".** Weak: they give radius 2 everywhere; the extremal radii appear only at highly structured degree-5/6 graphs.

## 8. Ledger

- [hand] §1 reduction, §2 P1, P2, §5 hardness remarks, §6 statements. [computed, exact] §3 tables (A_2..A_6 centre holes, all holes of A_3, A_4), radius-4 example T4, protected-face check at A_3/A_4, short searches (counts above).
- [open] R itself (finite radius for all DL states), radius sup for min-degree-5 graphs (>= 4, no upper bound), a proof that G or similar breaks a lock on A_r, protected face meeting N[v], and the cited fact on non-unique Kempe classes.
- Not checked: Math's earlier Theorem A, C, D (reused as stated; all consistent with the data: radius reached through F/B steps always shifts repeat index by 3 as predicted).

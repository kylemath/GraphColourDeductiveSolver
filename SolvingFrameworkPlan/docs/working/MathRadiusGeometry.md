# Radius of doubly locked states from local lock geometry (A_r and T4)

Math research worker, 6 October 2026. Hand work plus exact enumerations on explicit graphs only (A_3..A_6, T4, 50 flipped A_3/A_4 variants); one process, about 6 CPU-minutes. Scripts in the session scratchpad (`rg.py`, `an*.py`, `t4.py`, `flip.py`), not committed. No other file edited. Labels: [hand], [computed], [open].

## Verdict, first

1. **[hand] Theorem H.** Let v have degree 5 with all five link vertices of degree 5 (an "icosahedral 2-ball": the outer neighbours form a 5-cycle w_0..w_4, x_t ~ w_{t-1}, w_t). Then every doubly locked (DL) state at v has Kempe radius <= 3; radius <= 2 unless the state has local type R1 below and F(s) is DL, in which case radius <= 1 + radius(F s) <= 3. It uses neither r, nor the 5-fold symmetry, nor Lemma B, nor any lock path beyond its first and last vertex. In particular **radius <= 3 on A_r for every r**.
2. **[hand] Why the infinite F-orbits are filled quickly.** Along an F-orbit the local type alternates R1, R3, R1, ... and every R3 state is unlocked by ONE explicit swap: the {a,b}-component {x_j, x_{j+1}, x_{j+2}} of three link vertices (recolour a,b,a to b,a,b); then x_{j+3} has no a-coloured neighbour and the lock dies. Infinite orbit is irrelevant: every second state is locally breakable.
3. **[computed] Gap 3 vs 2.** Radius 3 occurs on A_3 (10 of 30 DL states, all type R1 with F(s) DL); on A_4, A_5, A_6 every DL state has radius 2 (agrees with Long Table and MathConjectureR). The hand proof gives only <= 3. The step to 2 for r >= 4 goes through a radial hairpin barrier in the lower rings, not proved [open].
4. **What is A_r-specific:** only the regular local shape (five degree-5 neighbours), not the symmetry or the family. T4 (radius 4) has two adjacent degree-6 link vertices at its hole, so Theorem H does not apply and the local classification does not close in one step (section 4).

## 0. Verification of Long Table's Lemma A and Lemma B

- **Lemma A [hand, checked line by line]: correct.** j, m, a, b, the two locks and F use only adjacency, the cyclic order of the link and equality of colours. A rotation sigma_k fixing v and preserving the cyclic order shifts j by -k and maps components to components; renamings are invisible. So doubly(pi s sigma) = doubly(s) and F(pi s sigma) = pi F(s) sigma. (Orientation-preserving is needed: a reflection turns F into B.)
- **Lemma B [hand]: correct.** F^{4+n} s = pi (F^n s) sigma by Lemma A, so doubly locked by induction (F^n s, n < 4, by hypothesis). F^{4k} s = pi^k s sigma^k; F^20 s = pi^5 s; F^60 s = s for a 3-cycle pi. Index check: j(s sigma_3) = j - 3 = j + 2 = j + 12 mod 5, ok. Remark: the hypothesis F^4 s = pi s sigma carries all the content and is only [computed]; Lemma B says nothing about radius.
- The census (20 J_{r-2}), K3-walk structure and Conjecture J are [computed]/[conjecture]; not re-derived. The "radial hairpin" picture is confirmed independently (section 2: the barrier of an unlocking swap is a radial hairpin).
- Lemma B and the census are not used in Theorem H.

## 1. Local classification of DL states at an icosahedral hole [hand]

Setup: link x_0..x_4, j = 0 after rotation, s = (a, b, a, g, d) (alpha, beta, alpha, gamma, delta). w_t is the outer vertex common to x_t and x_{t+1}; x_t ~ w_{t-1}, w_t; w_t ~ w_{t+1}. (A_r: w_t = (1,t). In general the faces force this, and the w_t are distinct, else a K4 gives a separating triangle.)

**Step 1 (DL forces the ring-1 pattern).** Lock 1: b,g-path P1 from x_1 to x_3; lock 2: b,d-path P2 from x_1 to x_4, in G - v.
- Neighbours of x_1: v, x_0, x_2 (a), w_0, w_1. P1 leaves x_1 to a g-vertex and P2 to a d-vertex, not via v, x_0, x_2: so {w_0, w_1} = {g, d}.
- P1 enters x_3 through b; x_3 ~ v, x_2 (a), x_4 (d), w_2, w_3: so b in {w_2, w_3}. P2 enters x_4 through b in {w_3, w_4}.
- w_0 = g, w_1 = d: w_2 is not a (x_2), g (x_3), d (= w_1), so w_2 = b; w_4 is not a (x_0), d (x_4), g (= w_0), so w_4 = b; w_3 is not g, d (x_3, x_4), not b (w_2), so w_3 = a. **R1 = (g, d, b, a, b).**
- w_0 = d, w_1 = g: w_2 in {b, d}, w_4 in {b, g}, w_3 in {a, b}. If w_3 = b: w_2 = d, w_4 = g, **R3 = (d, g, d, b, g)**. If w_3 = a: w_2 = w_4 = b, **R2 = (d, g, b, a, b).**
- [computed] A_3..A_6: all 30, 80, 530, 2450 DL states have exactly these patterns. (At r = 2 the ring touches the cap and no first lock exists, Long Table's section 3.)

**Step 2 (R2 dies after one F).** F swaps the a,g-component K_F of x_2. In R2, w_1 = g is adjacent to x_2 = a, so w_1 in K_F becomes a. After F, x_2 is g with neighbours x_1 (b), x_3 (a), w_1 (a), w_2 (b), v: no d neighbour. Lock 2 of F(s) is a d,g-path from the new middle x_4 (d) to x_2 (g); it must enter x_2 through a d-vertex; none. So F(s) is not DL: radius <= 2. (B by the mirror image, which maps R2 to R2.) [computed] chain length exactly 1 for all R2 states, r = 3..6.

**Step 3 (R3 is broken by one local swap).** R3: w_4, w_0, w_1, w_2 = g, d, g, d, none a or b, and x_3, x_4 are g, d. So the a,b-component K of x_1 is exactly {x_0, x_1, x_2}. Swap it: s' = (b, a, b, g, d). In s' the neighbours of x_3 are v, x_2 (b), x_4 (d), w_2 (d), w_3 (b): no a-vertex, but the new lock 1 is an a,g-path from x_1 to x_3, entering x_3 through an a-vertex. So s' is not DL: radius <= 2. [computed] every R3 state, r = 3..6: K has size 3 and s' is non-DL. No Jordan curve needed because x_3 has degree 5.

**Step 4 (R1 goes to R3 under F).** K_F contains x_2, x_3 and w_3 (a, adjacent to x_3 = g). It contains none of w_2, w_4 (b), w_1 (d); and not w_0: w_0 = g is adjacent to x_0 = a, so w_0 in K_F would put x_0 in K_F, but x_0 is not in K_F (the curve v, x_1, P2, x_4 is b,d-coloured and separates x_0 from x_2, x_3; Step 2 of MathConfinementAttack, valid since P2 exists). So only w_3 changes, a to g. F(s) has link (a, b, g, a, d), repeat index 3, roles (a' = a, b' = d, g' = b, d' = g), outer ring read from w_3: (g, b, g, d, b) = (d', g', d', b', g') = **R3**. So F(R1) is non-DL or DL of type R3. [computed, A_3..A_5: R1 -> R3 or non-DL; R3 -> R1 or non-DL; R2 -> non-DL; section 5.]

**Theorem H.** radius(s) = 1 + d(s, NL) (MathConjectureR section 1). R2, R3: d <= 1. R1: F(s) in NL (d <= 1) or R3 (d(F s, NL) <= 1, hence d(s, NL) <= 2). So radius <= 3. QED.

## 2. Answers to the questions asked

**Which explicit swap breaks a lock.** R2: the F-swap (it kills lock 2 of the image). R3: the three-vertex swap {x_j, x_{j+1}, x_{j+2}}. R1: no local swap in general (A_3 radius-3 states). [computed] for r >= 4, the a,b-component of x_1 (size 6..18, down to depth about r) breaks the lock for every inf-chain state via a **b,d-hairpin barrier** in s': from x_2 down the strips, round the bottom, and back up to x_4 (printed, r = 4: x2, (1,0), (2,4), (2,3), (3,2), cap, (3,0), (2,1), (1,2), x4). With v it closes into a curve separating x_3 from x_1, so no a,g-path joins them. Whether it exists depends on the bottom rings (it does not for 10 states of A_3), so this step is global [open, no proof].

**Why radius stays bounded as r grows [hand].** Lock paths have length ~2r but killing a lock needs only (a) a local obstruction at x_3 or x_2 (R2, R3), or (b) one F step to reach (a). Lock-path length never enters.

**Infinite orbits [hand].** By Step 4 the local type alternates R1, R3 along any orbit that stays DL (R2 ends it). R3 states have radius <= 2, neighbours in the orbit differ by one swap, so every orbit state has radius <= 3.

## 3. What is A_r-specific and what generalises

- **Not specific:** rotation symmetry, Lemma A/B, F^4 = pi s sigma, r, the census. The proof uses N^2[v] and x_3 having degree 5.
- **Needed:** v and its five neighbours of degree 5. [computed] Test: 50 triangulations obtained from A_3 (25) and A_4 (25) by 1 to 6 random edge flips avoiding N[v] (v and its neighbours keep degree 5; degrees elsewhere change; minimum degree may drop below 5), exhaustive over all colourings: DL radius <= 3 in all 50 (max 2 in 45, max 3 in 5), no unreached state. Consistent with Theorem H.
- **Not covered:** holes with a degree-6 neighbour. The outer ring is longer, Step 1 fails (the middle vertex may have three outer neighbours), K = {x_j,x_{j+1},x_{j+2}} is not forced, no analogue of Steps 2-4 is proved.
- **[open]** For general four-connected min-degree-5 holes the aim would be a finite automaton on (repeat index, colouring of a bounded ball) with F as transition and a bound N on steps to a locally breakable state. N = 1 at icosahedral holes; at T4 N >= 3. W6 (chain 6, radius 2) shows F-steps alone are not the right transition in general. A bounded ball for general holes is Conjecture R itself.

## 4. T4 (radius 4): why the jump [computed + partial hand]

T4, hole v = 4, link (0, 3, 8, 9, 5), degrees (5, 5, 6, 6, 5); outer cycle 1, 2, 7, 12, 13, 14, 10 (length 7). 68 canonical colourings, 21 DL, radius histogram {2:15, 3:4, 4:2} (agrees with MathConjectureR).
- **[computed]** Both radius-4 states have j = 2 (repeated colour at vertices 8 and 5, middle 9, a-vertex 0, b-vertex 3), F-chain 3 and 4. Their F and B images have radius 3; a shortest route is F, F, then a lock breaker (a,b-component {0,5,7,9,12,13} or an a,g swap of {0,1,3}). Exhaustive BFS: no shorter route. For chain 3, radius = 1 + chain exactly.
- **[computed]** Every other (j, chain) class at this hole has radius 2 or 3 (j = 2 with chain 1 or 2 has radius 2 via the small a,b-component {1,2,5,7,8,9}). For the two bad states the a,b-component of the middle is large ({2,5,6,8,9,12,15,16}) and swapping it gives another DL state.
- **[hand, partial] Mechanism.** At an icosahedral hole the middle vertex has two outer neighbours forced to be {g, d}, which forces the whole ring (3 patterns). At T4 with j = 2 the middle m = 9 has three outer neighbours (13, 14, 10) and x_j = 8 has three (7, 12, 13); the extra free neighbour allows many ring colourings compatible with DL, and the a,b-component of m reaches 12 and beyond. The R2-type death of lock 2 needs x_2 to lose its only d-neighbour; x_2 = 5 has outer neighbours 1 and 10 and keeps 1 = d. The R3-type isolation needs degree 5 at x_3 and a specific ring. Neither occurs within two F or B steps for these states. Also each F step rotates the repeat index by 3, so the orbit visits j = 2, 0, 3, ... where the degrees at (x_j, x_{j+1}) differ; on A_r all positions look alike and the automaton closes at once. One flip creating two adjacent degree-6 link vertices (T4 is a one-flip neighbour of A_3) destroys exactly this regularity. "No local mechanism in two steps" is checked on the two bad states only, not proved.
- **Consequence.** sup radius >= 4 over all graphs (T4); = 3 at icosahedral holes. [open] holes with one or two degree-6 neighbours.

## 5. Computed table: DL states by (type, F(s) status, type of F(s))

- A_3: (R2, non-DL) 10; (R3, DL, R1) 10; (R1, DL, R3) 10.
- A_4: (R2, non-DL) 60; (R3, DL, R1) 10; (R1, DL, R3) 10.
- A_5: (R2, non-DL) 320; (R3, DL, R1) 60; (R3, non-DL) 70; (R1, DL, R3) 60; (R1, non-DL) 20.
R3 states always have a,b-component of size 3 and a non-DL image (r = 3..6). For R1 inf-chain states the a,b-swap of x_1's component is DL in some cases (A_3 all 10; A_5 10 states with K of size 12) yet their radius is 2 for r >= 4 through other swaps.

## 6. Killed lines

- **K-H1: "the a,b-link component swap always breaks the lock".** False: A_3 (10 inf-chain R1 states), A_5 (10 with K of size 12), and every R2 state (they die by F instead).
- **K-H2: "x_2 plus P2 minus x_1 is the b,d-barrier in s'".** Dead for R1: P2 enters x_4 through w_4 = b, which is in K (adjacent to x_0 = a) and becomes a. The printed barriers enter through w_3 (was a, now b): a different hairpin, not the recoloured lock path.
- **K-H3: "radius 2 for all r from local data".** Dead: A_3 radius-3 states and A_4 radius-2 states have the same ring 0..2 patterns and the same K (size 6); only the structure below ring 2 differs, so the bound 2 for r >= 4 is not local.
- **K-H4: "Lemma B or the K3-walk census yields the radius".** No: Theorem H uses neither.
- **K-H5: "the four steps extend verbatim to a hole with a degree-6 neighbour".** Not claimed; Step 1 fails (T4).

## 7. Ledger

[hand]: Lemma A and B verified; Steps 1-4; Theorem H (radius <= 3 at icosahedral holes, all r); the explicit swaps; why infinite orbits are harmless. [computed]: pattern counts, transition table, K sizes, hairpin barriers, radii r = 3..6, 50 flipped graphs, T4 tables and geodesics. [open]: radius 2 for all r >= 4 (hairpin barrier existence), a bounded-ball automaton for holes with degree-6 neighbours, any absolute R beyond icosahedral holes (R >= 4 from T4).

## Erratum and review status (6 Oct, after `MathReviewArTheoremH.md`)

An independent review worker rederived Steps 1–4 of Theorem H and confirmed them over all colourings of A_3..A_9 (verdict CORRECT). Two wording fixes: (1) Step 4 does use the existence of the lock path P2, as a Jordan curve separating x_0 from x_2 and x_3, so the phrase "no lock path beyond first/last vertex" is imprecise; (2) the distinctness of the vertices w_t (which follows from the absence of a separating triangle) must be stated as a hypothesis of the theorem. Neither uses the A_r structure or degrees beyond ring 1.

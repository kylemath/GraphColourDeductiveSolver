# Intern B, cycle 5: anatomy of the order-17 exception (gentri index 1, holes 0 and 2)

Hand only, nothing run. Sources: `quarter-classes.jsonl`, `blocks-deg5.jsonl`, `holes-12-20.jsonl` (all in `local-runs/6-quarter-floor/`), line 2 of `studiointel/gentri/tri17.txt` (gentri index 1), messages 1811 and 1818. The graph was decoded by hand from the planar code; degree sum 90 = 6*17-12, and deg-6 vertices {4,5,7,8,16} match the census. Labels [hand] unless marked [data].

## 1. The graph
17 vertices, degrees: 6 at {4,5,7,8,16}, 5 elsewhere. Structure: hub 16 with hexagon A = 10,11,12,13,14,15; a second hexagon B = 4,5,6,7,8,9 (each B vertex adjacent to two consecutive A vertices, and conversely); a cap on B made of 1,2,3 and 0 (1 ~ 5,6,7,2; 2 ~ 7,8,3; 3 ~ 8,9,4; 0 ~ 1,2,3,4,5).

## 2. The exceptional holes (0 and 2)
Hole 0 (degree 5): link 1,2,3,4,5 in cyclic order, degrees (5,5,5,6,6): three consecutive degree-5 vertices and two adjacent degree-6 vertices. In frame letters x0..x4 = 1,2,3,4,5. Ring 2: w = 7 (1-2), 8 (2-3), 9 (3-4), 11 (4-5), 6 (5-1), and the extra neighbours m(4) = 10, m(5) = 12, so the ring is the 7-cycle 6,7,8,9,10,11,12; everything beyond it is {13,14,15,16}. Hole 2 has link 0,1,7,8,3 with degrees (5,5,6,6,5), the same class rotated. [data] Both holes: 64 states, 16 filled, one class, stabiliser S4, rho 4. The tips of the diamond, holes 1 and 3, have 54 states (16/54 = 0.296), not exceptions.

## 3. Birkhoff diamond: yes, exactly one
Triangles 0-1-2 and 0-2-3 share the edge 0-2 and all of 0,1,2,3 have degree 5, with 1 not adjacent to 3: a Birkhoff diamond. I checked every other triangle of degree-5 vertices (9-10-15, 6-12-13): none has a degree-5 partner triangle on any edge. The two exceptional holes are exactly the two **central** vertices of the diamond, and the hole's link contains the diamond's other three vertices. So the exceptions are reducible graphs and, in the Math frame, a hole inside a diamond (consecutive degree-5 link triple).

## 4. Block anatomy [data, rearranged by hand]
Hole 0: filled by singleton position F_0..F_4 = 2,4,2,4,4; unfilled by repeat pair j (pair {j,j+2}): U_j = 12, 8, 10, 10, 8 with DL part D_j = 4, 3, 6, 6, 3 and non-DL part N_j = 8, 5, 4, 4, 5. (Hole 2 is the mirror: F = 4,2,4,4,2; D = 3,6,6,3,4.) Not four equal blocks: D_j differ from F_{j+1}.
**Exact per-j identity in this class** (checked for all 10 values): U_j = F_{j+1} + F_{j+3} + F_{j+4}, equivalently U_j + F_j + F_{j+2} = 16.
Consequence: deficit D_j - F_{j+1} = 0,1,2,2,1 (hole 0) and slack (F_{j+3}+F_{j+4}) - N_j = 0,1,2,2,1: **equal for every j**. So Lemma A leaves exactly as many filled states unused as there are DL states with no room in F_{j+1}, no spare at all.

## 5. Difference between DL states that fill in 2 and those that do not
Math's rule rho (swap {alpha,A}-component of x_{j+2}, then {A,B}-component of x_{j+2}) lands in F_{j+1}, is injective, and is defined exactly when R+3(d) is not DL (1818). In the four-block classes D_j = F_{j+1} and rho is onto. Here **rho cannot be onto**: |D_j| > |F_{j+1}| for j = 1..4 (3>2, 6>4, 6>4, 3>2 at hole 0). By injectivity, at least 1+2+2+1 = 6 of the 22 DL states have R+3(d) doubly locked (|DD| >= 6) [hand, assuming 1818's injectivity]. Those cannot use rho. [Hypothesis, not checked]: the DL states needing more than 2 swaps are among these, since for them the rotation, one of the eight link moves, stays DL.

## 6. Would a 2-swap rule into F_{j+1} stay injective?
It is injective where defined (1818), but it is **not total** here: the surplus of 6 DL states (one per unit of deficit) must go to a different filled block F_{j+3} or F_{j+4}, and the counts say they must use exactly the leftovers there (slack = deficit, per j). So a total injective rule exists numerically only as an exact bijection with zero spare filled states; whether it is reachable in 2 swaps is the question for the Studio.

## 7. Computations requested
(i) For the 22 DL states at hole 0: distance to a filled state, whether R+3(d) is DL, the colour class of the target. (ii) Is the set {d : R+3(d) DL} of size exactly 6, and is it exactly the set needing >2 swaps? (iii) Same for hole 2. (iv) Is U_j = F_{j+1}+F_{j+3}+F_{j+4} true in all 419 floor classes?

## 8. Self-check, two weakest points
1. The graph was decoded by hand from the hex; the degree sum, the deg-6 set and the census states all agree, but the 2-swap questions in section 5 and 6 are inferences from block counts, not from enumerated states.
2. I assumed 1818's injectivity and "defined exactly when R+3(d) is not DL" without re-deriving them; the "at least 6 DL states with DL rotation" claim depends on it.

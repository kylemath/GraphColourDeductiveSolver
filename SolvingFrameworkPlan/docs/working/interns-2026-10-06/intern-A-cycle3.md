# Intern A, cycle 3: the AB swap on E2

By hand only. E2 = link (a,b,a,g,d) on x0..x4, ring w0..w4 = (d,g,d,a,g), m3=m4=b, x3,x4 of degree 6, x0,x1,x2 of degree 5.

## 0. What I got wrong in cycle 2
I wrote that AB "does not by itself break either lock" and that this "could not be decided from local data". That was an incomplete deduction, not a finding. I had already seen that both new locks end at w3, but I did not use the rotation at w3 and the alternation of two-colour paths, which give a real local obstruction. The Studio's data (both locks hold in 0 of 628 cases) is consistent with the corrected statement below, but, see section 3, I can only prove a weaker statement than "AB always works".

## 1. Setup after AB [hand]
The {a,b}-component of x1 is exactly {x0,x1,x2} (outer neighbours w4,w0,w1,w2 are g,d,g,d). After the swap the link is (b,a,b,g,d): repeated colour b, middle x1=a, x3=g, x4=d. The state is DL iff
- lock 1'': an {a,g}-path P1 from x1 to x3 in T-v, and
- lock 2'': an {a,d}-path P2 from x1 to x4 in T-v.
Neighbours of x3 after the swap: x2=b, w2=d, w3=a, m3=b, x4=d. The only a-neighbour is w3. So P1 ends ..., y1, w3, x3, with y1 a g-vertex (a two-colour path alternates). Neighbours of x4: x3=g, x0=b, w3=a, w4=g, m4=b. Only a-neighbour w3. So P2 ends ..., y2, w3, x4, with y2 a d-vertex.

## 2. Result [hand proof]
**Proposition.** If both locks hold after AB, then w3 has a g-neighbour y1 not equal to x3 and a d-neighbour y2 not equal to x4, and y1, y2 are not m3, m4 (these are b). In particular deg w3 >= 6 (neighbours x3, x4, m3, m4, y1, y2, all distinct: m3 != m4 since otherwise x3 x4 m is a non-facial triangle, excluded by the no-separating-triangle hypothesis; y1 != x3 because P1 is simple and ends at x3 after w3; y2 != x4 likewise; colours separate the rest).
**Corollary.** If w3 has degree 5, or more generally has no g-neighbour other than x3, or no d-neighbour other than x4, then AB makes E2 non-DL, and E2 has radius <= 2 (AB, then one fill swap, valid for any degrees).
Rotation at w3 (cyclic): x3, x4, m4, ..., m3. The Jordan curves v-x1-P1-w3-x3-v and v-x1-P2-w3-x4-v (v is adjacent to x1, x3, x4; x1 has rotation v,x0,w0,w1,x2, with P1 leaving through w1 and P2 through w0) force, when P1 and P2 meet only at x1 and w3, the cyclic order x3, x4, m4, ..., y2, ..., y1, ..., m3 at w3, and the closed curve P1 u P2 bounds a region whose corner at x1 is the single triangular face x1 w0 w1. These are necessary conditions, not contradictions.

## 3. The gap [open]
I could not derive a contradiction from planarity (Jordan) alone when deg w3 >= 6 with a g-neighbour y1 and a d-neighbour y2 placed in that order. I tried: (i) the curves of P1, P2 against each other; (ii) the original locks L1 ({b,g}, x1 to m3) and L2 ({b,d}, x1 to m4), using that P1 is colour-disjoint from L2 and P2 from L1; every pair of curves is consistent with the same planar picture (checked: P1 lies on the x2-side of the L2-curve, P2 on the x0-side of the L1-curve, closed curve L1+m3 w3 m4+L2 separates {y1,y2} from {x3,x4,v}). So the claim "E2 has radius <= 2 in general" is **not proved** by me; what is proved is the Corollary. The Studio's 628/628 may use additional constraints (degrees of w3, ring sizes) or the statement may be a real theorem needing a non-planar-local argument, e.g. a minimal-counterexample or discharging step on deg w3.

## 4. Self-check, two weakest points
1. The lock frame after AB (a' = b repeated, b' = a, g' = g, d' = d, locks {a,g} and {a,d}) is my relabelling of HP's definition; if HP's DL also demands conditions I have dropped (for example an endpoint rule at a degree-6 vertex), the Corollary still stands (it only uses "an {a,g}-path must end at an a-neighbour of x3") but the equivalence "DL iff both locks" should be checked against the Studio's definition.
2. Distinctness of y1, y2, m3, m4 uses the no-separating-triangle hypothesis and simplicity of paths. A coincidence y1 = a neighbour I excluded by colour is impossible; but y1 = y2 is excluded only by colour (g vs d), fine; the genuinely hypothesis-dependent point is m3 != m4.

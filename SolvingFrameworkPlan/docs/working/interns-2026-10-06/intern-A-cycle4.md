# Intern A, cycle 4: old locks as a barrier for the AB swap on E2

By hand only. E2 as before: link (a,b,a,g,d); ring w0..w4 = (d,g,d,a,g); m3=m4=b; x3,x4 degree 6; x0,x1,x2 degree 5. L1 = old {b,g}-path x1 -> x3 (ends m3), L2 = old {b,d}-path x1 -> x4 (ends m4), both in T-v and unchanged by AB except at x1. After AB: P1 = {a,g}-path x1 -> w3 -> x3, P2 = {a,d}-path x1 -> w3 -> x4 (cycle 3).

## 1. The barrier argument does not work as proposed [hand, negative]
P1 has colours a,g, so it is vertex-disjoint from L2 (colours b,d) except at x1. Hence P1 minus x1 lies on one side of the closed curve D = v-x1-L2-m4-x4-v. Compute the sides from the rotations: at x1 (v,x0,w0,w1,x2) D uses v and w0, so w1 and x2 are on one side and x0 on the other; at x4 (v,x3,w3,m4,w4,x0) D uses v and m4, so x3 and w3 are on one side and x0, w4 on the other. Consistency: the side containing w1, x2, x3, w3 is one side; x0, w4 are on the other. **So P1 is confined to the side of D that contains w3**, not the opposite side. Same for P2 against C1 = v-x1-L1-m3-x3-v: at x3 (v,x2,w2,m3,w3,x4) the arcs are {x2,w2} and {w3,x4}; at x1 C1 uses v,w1 so w0 and x0 are on one side with x4 and w3, and x2 is on the other. P2 starts at w0 and lies on the side containing w3. So the old locks do not cut the new components off from w3; they are on the same side. Colour-disjointness only forbids crossing; it gives no separation from w3. I do not believe the claimed statement follows from L1, L2 and v alone, and I stop pursuing it.

## 2. What the old locks do force near x1 [hand proof]
x1's neighbours: v, x0, x2, w0=d, w1=g. L1 must leave x1 through its only g-neighbour w1, then through a b-neighbour of w1 other than x1; L2 leaves through w0, then a b-neighbour of w0 other than x1.
w1's neighbours: x1, x2 (a before AB, b after), w0 (d, ring edge), w2 (d, ring edge), plus outside vertices. w0's neighbours: x0 (a before, b after), x1, w1, w4 (g, ring edge), plus outside vertices.
After AB, P1 must leave x1 through w1 and then use an **a-coloured neighbour of w1 other than x1**; x2 is now b, w0 and w2 are d, so it is an outside neighbour u1 of w1. Likewise P2 needs an **a-coloured outside neighbour u0 of w0** (x0 is now b, w1 and w4 are g).

**Proposition 2.** If deg w1 = 5 or deg w0 = 5, AB makes E2 non-DL, so E2 has radius <= 2 (AB, then one fill swap).
Proof. If deg w1 = 5, w1 has exactly one outside neighbour u. L1 (old, existing since the state is DL) needs a b-neighbour of w1 other than x1; the only candidate is u, so u=b. After AB, w1's neighbours are x1 (a), x2 (b), w0 (d), w2 (d), u (b): no a-neighbour other than x1, so no {a,g}-path leaves x1, P1 does not exist, lock 1'' fails. The deg w0 = 5 case is identical with L2 and P2: the single outside neighbour of w0 must be b, so after AB w0 has no a-neighbour other than x1. QED. (Uses only: ring edges w0w1, w1w2, w4w0, which hold because x0,x1,x2 have degree 5, and the lock structure.)

**Corollary.** Both new locks hold only if deg w0 >= 6, deg w1 >= 6, deg w3 >= 6 (cycle 3). More precisely w1 needs an outside b-neighbour (for L1) and a different outside a-neighbour (for P1); same for w0 with b (L2) and a (P2).

## 3. Gap [open]
The Studio's observation (x1's {a,g}- and {a,d}-components after AB contain no neighbour of w3 at all, in 500/500 records) is not explained by the old-lock barriers (section 1). My Proposition 2 explains the cases deg w0 or deg w1 = 5 only. For deg w0, deg w1 >= 6 I have no proof. Extra hypotheses that would close it: (i) deg w0 = 5 or deg w1 = 5 (proved above); (ii) any local rule forcing x1's {a,g}- or {a,d}-component to be small, e.g. a 6-vertex (not just one) neighbourhood of w1 with no a-neighbour. A genuinely global argument would need a barrier of {b,d}- or {b,g}-colour made of new (post-AB) structure through v; the only such link vertices are x0,x2 (b), x3 (g), x4 (d) and all such paths are facial triangles at v, so no non-trivial barrier exists from v alone.

## 4. Self-check, two weakest points
1. Section 1 depends on the rotation orders at x1, x3, x4 (clockwise convention and which arc is which). If my arc assignment is reversed the barrier would work as the coordinator hoped; I checked each rotation twice but did not draw a figure.
2. Proposition 2 assumes the old state is genuinely DL (L1, L2 exist) and that deg 5 for w1 means exactly one non-ring neighbour (neighbours x1,x2,w0,w2 distinct); coincidences w0 = w2 would be separating triangles, assumed excluded.

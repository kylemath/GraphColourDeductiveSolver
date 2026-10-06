# Intern A, cycle 2: the escaping patterns gdbbb and dgdag at the degree-6 pair {3,4}

By hand only, no code. Frame: link x0..x4 = (a,b,a,g,d); lock 1 = {b,g}-path x1->x3, lock 2 = {b,d}-path x1->x4. x3 has neighbours v,x2,x4,w2,m3,w3; x4 has v,x3,x0,w3,m4,w4 (x0,x1,x2 have degree 5). F = swap of the {a,g}-component K_F of x2,x3; B = swap of the {a,d}-component K_B of x4,x0 (B is the mirror of F: g<->d, x3<->x4, m3<->m4, w_t -> w_{1-t}... as in HP). Facts used: x0 not in K_F, x2 not in K_B (Jordan, no degrees); a non-DL 4-coloured link fills in one more swap (any degrees). So "kill" = reach a non-DL state; radius then <= (swaps used)+1.

## 1. gdbbb (w0..w4 = g,d,b,b,b)
Colour constraints: m3 is adjacent to x3=g, w2=b, w3=b so m3 in {a,d}; m4 is adjacent to x4=d, w3=b, w4=b so m4 in {a,g}.
**F analysis [hand].** K_F contains no ring vertex (the w's are b,d). After F, x4 has neighbours x3=a, x0=a, w3=b, w4=b, and m4 (possibly recoloured). The new lock 2' ({d,g}-path from x4) needs a g-neighbour of x4, and only m4 can supply it. So F **kills** unless (m4=g and m4 not in K_F) or (m4=a and m4 in K_F).
**B analysis [hand, by the self-mirror of gdbbb]**: B **kills** unless (m3=d and m3 not in K_B) or (m3=a and m3 in K_B).
Note m3=a forces m3 in K_F, and m4=a forces m4 in K_B, which prunes combinations but does not remove the escape.
**Result:** unless both escape conditions hold, F or B gives a non-DL state, so radius <= 3 (F or B, then the fill swap, then at most one more; I count F + fill = 2 swaps). In an escaping branch F still gives a DL state: the ring is unchanged and in the new frame (x'_0..x'_4 = x3,x4,x0,x1,x2) reads (g',g',d',b',g'), free pair {0,1}, where the starvation kills are lost (x'_0 = x3 has degree 6). No further kill found.
**Candidate hard state (E1):** m3=d, m4=g, m3 not in K_B, m4 not in K_F, rest as in gdbbb. Smallest explicit data: link a,b,a,g,d; ring w=(g,d,b,b,b); m3=d, m4=g. I could not find a kill for E1; I did not prove none exists.

## 2. dgdag (w = d,g,d,a,g)
**Forced extra colours [hand].** x3=g has neighbours x2=a, w2=d, w3=a, x4=d, so its only possible b-neighbour (the end of lock 1) is m3: **m3=b**. Likewise x4=d has neighbours x3=g, x0=a, w3=a, w4=g, so **m4=b**. So the state is fully determined locally: link (a,b,a,g,d), ring (d,g,d,a,g), m3=m4=b.
**F [hand].** K_F contains x2,x3, and also w3 (a, next to x3) and w1 (g, next to x2); w4=g is next to x0 and is not in K_F. After F: ring (w3,w4,w0,w1,w2) = (g,g,d,a,d); in the new frame (b'=d, g'=b, d'=g) this reads (d',d',b',a,b') = the HP type ddbab, free pair {0,1}. x4 keeps g-neighbours w3,w4, so lock 2' is not starved; the HP kill for ddbab@1 is B-starvation, which needs x'_0 = x3 of degree 5, but x3 has degree 6. **F does not kill.** B is the mirror (dgdag is self-mirror) with the same outcome.
**AB [hand, partial].** The {a,b}-component of x1 is exactly {x0,x1,x2} (outer neighbours w4,w0,w1,w2 are g,d,g,d), a single swap. After it the link is (b,a,b,g,d); new locks are {a,g}-path x1->w3 (via w1) and {a,d}-path x1->w3 (via w0), both ending at the same vertex w3=a. The AB swap does not by itself break either lock; they break only if a path avoiding the other's vertices fails to exist, which I could not decide from local data. **No kill found.**
**Candidate hard state (E2):** the fully determined configuration above (m3=m4=b). It is a local pattern, so the Studio test is: search for DL states whose local picture is exactly link (a,b,a,g,d), ring (d,g,d,a,g), m3=m4=b with x3,x4 of degree 6, x0,x1,x2 degree 5, and compute their radius.

## 3. Verdict
(1) gdbbb: killed by F or B in 2 swaps except in the explicit m3,m4 branches (needs m4 and m3 colours and component membership); the residual E1 has no kill found. (2) dgdag: no kill found; local colours are forced (m3=m4=b). Both are [hand] partial; no radius bound proved.

## 4. Self-check, two weakest points
1. I treated "F then no g-neighbour of x4" as a lock failure using only x4's listed neighbours; this relies on my identification of lock 2' as a {d,g}-path from x4 and on x4 having exactly the neighbours v,x3,x0,w3,m4,w4. A slip in the lock relabelling (j' index convention differs from the reviews by one) would change the kill condition for gdbbb.
2. For E1 and E2, "no kill found" only means I tried F, B and AB; I did not examine swaps through m3,m4 beyond that, nor the Jordan side of m3,m4 (not decided). They may well die to a swap I did not try.

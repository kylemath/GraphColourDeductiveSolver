# Intern B, cycle 3: attacking Lemma C* at O10 / M(O10)

Hand only, nothing run. Read FellowF-55656.md (§1-§6) only. Labels [hand]. **Result: [open]. I found neither a planarity contradiction nor a full counterexample. I record exact anatomy of O10, two rigorous planar constraints, and a local plane picture that makes O10 and both its F/B neighbours DL, so the Studio can see what a contradiction would have to defeat.**

## 1. Anatomy of O10 (frame x0..x4 = a,b,a,g,d; S={1,3}: x1, x3 of degree 6)
Ring string ggdab: w0=g, w1=g, w2=d, w3=a, w4=b. Forced extras: m1 is coloured d (x1 is b, outer g,m1,g, and lock 2 needs a d-neighbour), m3 is coloured b (x3 is g, outer d,m3,a). So the 7-ring is w4 b, w0 g, m1 d, w1 g, w2 d, m3 b, w3 a, all consecutive ring vertices adjacent.
- Lock 1 (P1, {b,g}) must leave x1 through w0 or w1 and **enter x3 through m3** (the only b-neighbour of x3). Lock 2 (P2, {b,d}) must leave x1 through **m1** (only d-neighbour) and **enter x4 through w4** (only b-neighbour of x4, degree 5).
- Why every local kill fails (this explains "locally free"): AB* holds automatically (w4 b is adjacent to x0 and w3 a is adjacent to w4, so w3 is in K_AB). SS4 holds automatically (w4 is adjacent to w0 g, w0 is adjacent to x1, so w4 is in K1). SS3 does not apply (w2 is d). G: every g/d ring vertex is in K_G (run w2 w1 m1 w0 plus x3 x4), so G gives itself. F and B starvation fail (x2 sees d, x0 sees g).

## 2. Two rigorous planar constraints [hand]
**(A) Side lemma for P2.** C2 = v x1 m1 P2 w4 x4 v. At x1 the rotation is (v,x0,w0,m1,w1,x2) and at x4 it is (v,x3,w3,w4,x0). So x0 and w0 lie on one side X; x2, x3, w1, w3 (and m3, w2 unless on C2) lie on the other side Y. P1 starts in X (via w0) or Y (via w1) and must end at m3 in Y, so if P1 uses w0 it must meet C2 at a shared b-vertex. No contradiction (b-vertices can be shared).
**(B) Crossing lemma for F(O10).** F(O10) = M(L4) must be DL, so F(s) has a {d,g}-path Q from x4 (d) to x2. In F(s) the only g-neighbour of x4 is w3 (it was a, in K_F), and w3's ring neighbours are b (m3, w4) or x3/x4, so **Q leaves the ball**: Q = x4 w3 Q' w2 x2 with Q' outside the ring from w3 to w2. Q' together with the ring arc w2 m3 w3 bounds a region S_m containing the outer neighbours of m3. P1 must enter m3 from S_m but starts at x1 on the other side, hence **P1 and Q' share a vertex q1** that is coloured g in s and g in F(s), so q1 not in K_F. [Mirror: B(O10) = M(O4|O5) has a lock 1' {g,d}-path x3 w2 w1 m1 w0 x0 that lies inside the ring, so the B direction is local and asymmetric.] This asymmetry is the first exploitable fact: F-images at O10 force a ring-3 {d,g} path, B-images do not.

## 3. Local plane picture (partial, not a counterexample)
Add outer vertices: e1 (b) adjacent m1 and e2 (d); e2 adjacent w4; f1 (d) adjacent w3; f2 (g) adjacent f1, w2, m3; h1 (b) adjacent w1 and f2. Then P2 = x1 m1 e1 e2 w4 x4 (b,d alternating), P1 = x1 w1 h1 f2 m3 x3 (b,g), and in F(s) Q = x4 w3 f1 f2 w2 x2 ({d,g}, with f2 = q1 shared with P1). All planar (f2 lies on the boundary of S_m, h1 on the other side), f2 not in K_F, e1,e2 not touched by any of the swaps used, and B(s) has lock path x3 w2 w1 m1 w0 x0. So O10 is DL, F(O10)=M(L4) satisfies its two locks, B(O10)=M(O4|O5) satisfies lock 1' and keeps lock 2'.
**This checks DL-ness only.** I did not check the leak predicates of M(L4) (SS4), N4, L4 (SS3), the G-partner coupling at N4, nor any state beyond one step, so it does not decide C*. It does show that O10 plus its two immediate neighbours impose no contradiction through lock existence alone; any contradiction must use predicates two or more steps along the cycle.

## 4. What I tried and why it stopped
1. Jordan with Q as the curve: v x4 Q x2 v separates {x0,x1} from {x3}; P2 stays on the x1 side, P1 must cross Q: gives (B) only.
2. Combining (A) and (B): P1 crossing Q' at q1 and sharing b-vertices with C2 are all satisfiable (picture).
3. M(O10) (P4, ddbag) is the mirror-type state of O10 and gives the mirror constraints (a ring-3 {g,d}-path from the B side, local F side); I did not find a joint constraint from the pair (O10, M(O10)) because they sit five F-steps apart (…L4 -> M(O10) ... O10 -> M(L4) -> N4 -> L4 -> M(O10)), and the path predicates between them (SS4 at M(L4)/N4, SS3 at N4/L4) were not combined.

## 5. Self-check, two weakest points
1. The claim that Q must exit the ball assumes x4's only g-neighbour after F is w3 (x4 has degree 5, neighbours x3 -> a, x0 a, w3 -> g, w4 b); I rechecked that x3 is in K_F, so this should hold; but coincidences among outer vertices (f2 = m3 etc.) were not examined.
2. Section 3 is a picture of necessary conditions only; it was not completed to a triangulation with minimum degree 5, so it is not a candidate counterexample to R* and I make no claim about it beyond the stated checks.

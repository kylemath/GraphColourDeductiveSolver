# 17 - Heawood charges on filled / unfilled states and the 1/4 floor (exploratory)

Own code, exploratory, small: about 25 s of CPU on 2 cores (`nice -n 10`), AC power, nothing left running. Raw per-state records (45 MB + 18 MB) are NOT committed; regenerate them with the commands below.

```
cd backgroundMaterial/planemap-structural/longtable/local-runs/17-charges-floor
nice -n 10 python3 charges.py --orders 12 14 16 17 18 19 20 --workers 2 > raw-12-20.jsonl          # every degree-5 hole, every class (1,614 classes)
nice -n 10 python3 charges.py --orders 17 21 22 23 24 --floor-holes --workers 2 > raw-floor.jsonl   # every class of every degree-5 hole that contains a floor class (857 classes)
nice -n 10 python3 analyze.py raw-12-20.jsonl raw-floor.jsonl > results.txt                        # also results.json; all linear algebra exact (Fractions, fit.py)
```
Coverage: 2,469 classes, 391,173 states (192,117 filled). All 419 floor classes of item 6 (orders 17, 21-24) are included; 405 of them have the exact 4-block structure (filled singleton at i; non-DL repeat pair {i+1,i+3} = "U1"; non-DL pair {i+2,i+4} = "U2"; DL pair {i+4,i+1} = "DL"; F states each). The other 14 are not 4-block. Orders 21-24 are floor holes only (all classes of those holes), not all holes.

## Conventions
- Faces come from the planar-code rotation (face (v,w,w') for consecutive neighbours); the orientation is asserted consistent (every face found 3 times with the same cyclic order). Corners C0..C3 as in the task; face sign +1 iff (C[a],C[b],C[c]) is outward.
- A state is a colouring up to renaming; charges are computed in its canonical labelling (first occurrence along `Space.order`). An odd renaming flips every sign, so q(v), q(m), ... in the canonical labelling are gauge dependent. Every Kempe class lifts to ONE labelled class with stabiliser S4 (item 6), so inside a labelled class every signed statistic is trivially symmetric (the transposition (p q) flips all signs).
- Gauge fixing used throughout: Q(u) = eps * q(u) with eps(filled) = sign of the triangle (missing, singleton, x_{i+1}) and eps(unfilled) = sign of the triangle (A, B, alpha) = (x_{j+3}, x_{j+4}, x_j). Along the lock-1 swap of the {mu,A}-component of a (item 7 injection phi), the labelled colouring keeps the same eps, so Q is comparable across a move. Products, squares and |.| are gauge free anyway.
- q(u) of a link vertex of an unfilled state is the partial charge in G (faces of G only). For filled states `qLfull` is the full charge in T after capping, `qL` the partial charge in G (full = partial + the two v-faces at that vertex).
- W = eps * (signed number of faces of G). tau = sigma*deg (sigma = sign q(v)) is gauge free.
- Link positions are in rotation order of the hole's link; U = non-DL unfilled, D = DL (as in item 7).

## Results
**Q1 (filled states).**
- **sign q(v) is determined by the link pattern.** Link pattern is s a b a b (singleton s at i). The five v-faces are (m,s,a),(m,a,b),(m,b,a),(m,a,b),(m,b,s); the middle two cancel and the other three have equal sign, so q(v) = 3*TS(m,s,a) = 3*eps (asserted on all 192,117 filled states, 0 failures; the Σq = 12 deg and q = 0 mod 3 asserts also pass). So the "split by sign of q(v)" is the gauge, not a class invariant.
- Gauge-free content = tau = sigma*deg. For a capped state W_G = 4 tau - 3 exactly (since Σ_G signs = 4 deg - 3 sigma); i.e. W = 1 mod 4 on every filled state (192,117/192,117), and **W = 3 mod 4 on every unfilled state** (199,056/199,056; observed, no proof).
- No sign/degree pattern tied to the floor: tau of the single filled state of the 319 F=1 floor classes takes every value from -4 to 7 (see results.txt). Both degree parities occur inside a class: 1,707 of 2,050 non-floor classes but only 12 of 419 floor classes (small classes mostly). tau>0 count = tau<0 count in 62/419 floor classes vs 26/2050 other classes: size effect, no exact rule.

**Q2 (floor blocks, 405 four-block classes).** Block sums S_B(X) of gauge-fixed charges, Qk = eps*q_G(x_{i+k}), exact null space of (S_F,S_U1,S_U2,S_DL,#F) over all 405 classes:
- Q1: S_U1 = S_F, S_DL = S_F, S_U2 = -S_F. Q4: S_U2 = S_F, S_DL = S_F, S_U1 = -S_F. (S_F(Q1) != 0 in 405/405, S_F(Q4) != 0 in 404/405, but its sign varies from class to class: 226 positive / 179 negative for Q1.)
- Q2: S_U1 = S_F, S_U2 = -S_DL. Q3: S_U2 = S_F, S_U1 = -S_DL. Squares: Q1^2 and Q4^2 equal in all four blocks; Q2^2: S_F = S_U1, S_U2 = S_DL; Q3^2: S_F = S_U2, S_U1 = S_DL. Q1*Q2: S_U2 = S_DL; Q3*Q4: S_U1 = S_DL.
- In role frames: U1 has (m,a,b) at (Q2,Q4,Q0), U2 at (Q3,Q0,Q1), DL at (Q0,Q2,Q3). So sum_{U1} Q(m) = sum_F Q2, sum_{U2} Q(m) = sum_F Q3, sum_{U1} Q(a) = -sum_F Q4, sum_{U2} Q(b) = -sum_F Q1: charge at a lock end flips sign relative to the filled block when that lock is the one whose swap fills.
- Statewise (366-388 of 405 classes have Q_k constant inside each block): Q1: U1=F, U2=-F, DL=F; Q4: U1=-F, U2=F, DL=F; Q2: U1=F; Q3: U2=F.
- No relation (null space 0) for Q0, Q0^2, sum of link partial charges, number of positive link faces, sum of squares, Q2*Q3, Q4*Q0 beyond the trivial ones.
- So the blocks ARE distinguished by sign patterns of the charge at x_{i+1} and x_{i+4}, but these are sums of values whose size and sign vary from class to class; none of them is a class constant that fixes the block sizes.

**Q3 (linear identities in F, U, D).** Searched (exact null spaces) over all 2,469 classes, the 419 floor classes and the 405 four-block classes. Statistics: sum of link partial charges (raw and gauge fixed), number of positive link faces, sum of squares, adjacent products, W, W^2, Q(m), Q(a), Q(b), Q(alpha), their squares and pair products, filled Q_k (partial and full), tau.
- **No exact identity of the form sum_states(stat) = alpha F + beta U + gamma D for any stat, in any subset.** Only the trivial count relation U + D = 3F on floor classes.
- **Near-exact identity, floor classes only: sum_{unfilled} W = sum_{filled} W** (sum over U and D together), equivalent to sum_F tau-type balance W_F = W_U1 + W_U2 + W_DL. It holds in 412 of 419 floor classes, in 403 of 405 four-block classes, and in all 319 floor classes with F=1 (4-state classes). Failures: order 17 gentri 1 holes 0 and 2 (size 64), order 24 gentri 1055/16, 1411/13, 1411/17, 4699/15, 5067/14. Its constant defect in the failures is 48, 96, 96, 96, 96, 24, 24.
- The same equality also holds by coincidence in 16 of 2,050 non-floor classes (fractions 1/2, 53/92, 21/44, 3/7, ...), so it neither characterises nor implies the floor. In non-floor classes the defect is negative in 1,670, positive in 364, zero in 16, correlation with the slack |C| - 4F is -0.08.

**Q4 (headline).** No charge quantity predicts the filled fraction or implies the floor. The sign of q(v) is fixed by the link pattern and is gauge. The only exact-looking invariant is the W balance above, which holds in 98% of floor classes, fails in 7, and also holds in 16 non-floor classes. All other charge statistics are consistent with the block structure only through the single-link-vertex swap relations (Q1, Q2, Q3, Q4 block sums), which are local consequences of where the swapped component sits, not size information. This is a negative result for a charge proof of the floor.

## Caveats
- Everything is computation on the stored lists (orders 12-20 all degree-5 holes; 17, 21-24 floor holes only); no proof except where stated. The mod-4 residue of W on unfilled states and the W balance are observations.
- An earlier draft of the analysis used a floor-division "tau" for unfilled states; it is replaced here by W (an integer for every state). The reported identity is in W.

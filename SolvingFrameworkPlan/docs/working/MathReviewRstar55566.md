# Review of MathRstar55566.md (Theorem R5³: three consecutive degree-5 link vertices ⇒ DL radius ≤ 7)

Math independent review worker, 6 October 2026. **Hand only.** The machine was on battery restriction: no code, script or build was run; files were only read. I did not write the reviewed note. Nothing else was edited and nothing was committed.

Read for this review: MathRstar55566.md (all of it), MathConfinementAttack.md (Step 1, DL definition; Theorem A), MathHighDegreeNeighbour.md (§1 F, B, Jordan facts, starvation), MathRadiusGeometry.md (Theorem H, Steps 1–4), MathTwoSixNeighbours.md (frame, tables, C and C*). The Tait lock criterion was not needed: every step is checkable by adjacency, the two Jordan facts and the lock-entry argument.

## Verdict, first

| statement | verdict |
|---|---|
| §1 frame, E1–E3, Jordan facts, F/B frames, unlock | **CORRECT** |
| §2 Lemma G (G-F, G-B, radius ≤ 3) | **CORRECT** |
| §2 margin (starvation reproved; F cannot create a starved-colour neighbour) | **CORRECT** |
| §2 confinement (x3, x4 degree 5, w2 = w4 = b ⇒ K_G = {x3, x4}) | **CORRECT** |
| §3 Proposition S01, case W3 = a (F-starvation or G-F, ≤ 3) | **CORRECT** |
| §3 Proposition S01, case W3 = b (F, F, F, then G-B, ≤ 6) | **CORRECT** (all three images and the final confinement rechecked) |
| §3 "no degree of X0, X1 used; middles never read" | **CORRECT** (one harmless overstatement, R2 below) |
| §4 position table, all five S and the mirror | **CORRECT** |
| §4 Theorem R5³ (≤ 7; ≤ 6 at repeat pairs {y3,y0}, {y2,y4}) | **CORRECT** |
| §4 "finiteness from Theorem A plus S01" | **CORRECT** |
| §5 C ∪ C* broken (P4, M(P4), P7, M(P7) killed by G-F / G-B) | **CORRECT** |
| §5 W has radius ≤ 4 | **CORRECT**, conditional on the cited transition W →F P7 (MathTwoSixNeighbours §4.1), which I did not recompute |
| §6 Tait remarks; "D2 kills W" killed | **NOT REVIEWED** (stated as unused; nothing depends on them) |
| §6 (5,5,6,5,6) blocking at N2, N4 | **CORRECT** (four blocking colours checked against the N2, N4 rows) |
| §7 machine spec | **GAP (spec only)**: the replay route of item (b) must be mirrored at S = 12 and prefixed at S = 23, 34, 40 (R4 below) |

No WRONG verdict. I found no counterexample state. The proof is short enough to have been checked exhaustively by hand; every case is listed in §2–§4 below.

## 1. Frame and facts (note §1)

- DL = both locks exist (MathConfinementAttack Step 1). Frame (a,b,a,g,d) on x0..x4; lock 1 {b,g} x1→x3, lock 2 {b,d} x1→x4, in T − v. Matches.
- **Jordan facts.** Curve v x1 P2 x4 v is {b,d}-coloured off v and separates x0 from {x2, x3}; so x0 ∉ K_F. Mirror for x2 ∉ K_B. Both need s DL; the note only applies them to states already known DL (or the run has stopped at a non-DL state). Checked at each use below.
- **F frame.** F(s) link (a,b,g,a,d); repeat pair {x3, x0}, middle x4; frame x′_t = x_{t+3}; roles a→a, b′ = d, g′ = b, d′ = g. **B frame** x′_t = x_{t+2}: B(s) link (d,b,a,g,a), frame (x2,x3,x4,x0,x1) = (a,g,a,d,b). Both images have four colours, so are unfilled. Correct.
- **Unlock.** If lock 1 fails, the {b,g}-component of x1 avoids x3 and every a-vertex; swapping it makes x1 g and the link misses b. Same for lock 2. So an unfilled non-DL state fills in one swap; radius(s) ≤ 1 + radius(s′). Correct.
- **E1–E3** at degree-5 endpoints: Theorem H Step 1. Correct. E1 is never used in the proof (it would need X1 of degree 5); good.
- **Coincidences.** I checked the coincidences that are geometrically possible without a separating triangle (e.g. W2 or W3 adjacent to the free X0 or X1; W1 = W4 via a separating 4-cycle). Each either makes the case contradictory (e.g. W1 adjacent to X0 in case W3 = b forces X0 ∈ K1, contradicting (J), so no DL state exists there; W3 adjacent to X1 in case W3 = b is improper) or touches no step that is read. The note's claim "both forms of deduction survive coincidences" holds.

## 2. Lemma G and confinement (note §2)

- **G is one legal swap.** K_G = {g,d}-component of x3 in T − v; x4 (d) is adjacent to x3 (g), so x4 ∈ K_G. No other link vertex has colour g or d. Image link (a,b,a,d,g), same frame, four colours. Correct.
- **G-F.** In s′ = G(s), a neighbour u of x2 is coloured g iff (c(u) = g, u ∉ K_G) or (c(u) = d, u ∈ K_G). The hypothesis says exactly "x2 has no c′(x4)-neighbour in s′". F-starvation is stated for c(x4) generally, so it applies to s′ (with F on s′ = the {a,d}-component of x2). If s′ is DL, F(s′) is not DL; if s′ is not DL, unlock. Swaps: G, F, unlock = 3. Correct.
- **G-B.** Same, with x0 and c′(x3) = d. Correct.
- **Margin (task point (c)).** The starvation colour c′(x4) is outside the swapped pair {a, c′(x3)}, so F never changes a neighbour of x2 into or out of colour c′(x4). The new lock 2 of F(s′) is a {c′(x4), c′(x3)}-path from x4 to x2 (non-adjacent), so it enters x2 through a c′(x4)-vertex; none exists. **The gap found today in another starvation lemma (a swap creating a new starved-colour neighbour) does not occur here**: in G-F and G-B the starvation is evaluated in s′, *after* G, using the exact post-G colours (the u ∈ K_G clauses), and the only later swap is the F (or B) whose colours exclude the starved colour. Correct.
- **Confinement.** With deg x3 = 5: neighbours v, x2 (a), x4 (d), w2 (b), w3; w3 is adjacent to x3 (g) and x4 (d), so w3 ∈ {a,b}. With deg x4 = 5: neighbours v, x3, x0 (a), w3, w4 (b). So no g/d neighbour leaves {x3, x4}: **K_G = {x3, x4}**. Uses only deg x3 = deg x4 = 5, w2 = w4 = b. Correct.
- **"G-F reads w1 ≠ g once x2 has degree 5."** x2's neighbours: x1 (b), x3 (g, in K_G: becomes d), w1, w2 (b); x4 ∉ N(x2) (link induced). So the condition is w1 ≠ g. Correct. **"G-B reads: x0 has no outer neighbour coloured d."** x4 is d and in K_G (becomes g); x3 ∉ N(x0). Correct; the phrase "once x4 has degree 5" should read "once confinement holds" (x0 may have any degree). Wording only.

## 3. Proposition S01 (note §3), every step

X2, X3, X4 degree 5; X0 (repeat) and X1 (middle) free. W1 ∈ {g,d} (adjacent X1 b, X2 a); W2 ∈ {b,d}; W3 ∈ {a,b}; W4 ∈ {b,g}. Ring edges W1W2, W2W3, W3W4 come from the rotations at X2, X3, X4. All correct.

**Case W3 = a.** E2 ⇒ W2 = b; E3 ⇒ W4 = b.
- W1 = g: N(X2) colours b, g, g, b: no d. F-starvation, radius ≤ 2. Correct.
- W1 = d: confinement applies (X3, X4 deg 5, W2 = W4 = b). After G: N(X2) = X1 b, X3 d, W1 d, W2 b: no g. G-F, radius ≤ 3. Correct.

**Case W3 = b.** W2 ≠ W3 ⇒ W2 = d; W4 ≠ W3 ⇒ W4 = g; W1 ≠ W2 ⇒ W1 = g. Correct.
- **F1** (s0 DL). K1 = {a,g}-component of X2. From X3: neighbours X2 (a), X4 d, W2 d, W3 b, so only X2. From X2: W1 (g) ∈ K1. W4 (g) is adjacent to X0 (a) ∉ K1, so W4 ∉ K1. W2, W3 have colours outside {a,g}. Link vertices: X0 excluded by (J), X1 b, X4 d. So on the read set only X2, X3, W1 change. s1 as stated: (a,b,g,a,d), W = (a,d,b,g). Frame (X3,X4,X0,X1,X2), repeat {X3,X0}, middle X4. Correct.
- **F2** (s1 DL). Frame roles a′ = a, g′ = b: K2 = {a,b}-component of X0, contains X1. W1 (a) adjacent to X1 ⇒ in K2 ⇒ becomes b. W3 (b) adjacent to X3 (a) = x′0 ∉ K2 by (J) for s1 ⇒ W3 ∉ K2. W2 d, W4 g untouched. X3 excluded by (J); X2 g, X4 d. s2: X0 b, X1 a, W1 b, others unchanged; link frame (X1,X2,X3,X4,X0) = (a,g,a,d,b). Correct (I recomputed the frame shift: x″_t = X_{t+1}).
- **F3** (s2 DL). Roles a″ = a, g″ = d: K3 = {a,d}-component of X3, contains X4. N(X3): X2 g, X4 d, W2 d ⇒ W2 ∈ K3, W3 b. N(X4): X0 b, W3 b, W4 g. X1 = x″0 ∉ K3 by (J). W1 b, W3 b, W4 g untouched. s3: X3 d, X4 a, W2 a. Frame (X4,X0,X1,X2,X3) = (a,b,a,g,d). Correct.
- **G-B at s3.** In this frame G is the {g,d}-component of X2 (containing X3). N(X2): X1 a, X3 d, W1 b, W2 a. N(X3): X2, X4 a, W2 a, W3 b. Component {X2, X3} (it is the confinement criterion again: frame w2 = W1 = b, frame w4 = W3 = b). After G: X2 d, X3 g. N(X4) = X3 g, X0 b, W3 b, W4 g: no d = c′(x‴3) = c′(X2). B-starvation applies. Correct.
- **Count.** Stopping at the first non-DL state: ≤ 2, 3, 4, 5 or 6. Radius ≤ 6. Correct.

**Degree audit (task points (b), (d)).** The read set is X0..X4 colours, N(X2), N(X3), N(X4), and the adjacencies W1–X1, W4–X0, W3–X3. W0, the middles of X0 and X1, and every ring-vertex degree are never read. Membership of an unread vertex in K1, K2, K3 does not affect any later read (each later K-membership claim is forced by adjacency to a link vertex or by (J), never by an unread vertex). **The generality "X0, X1 of arbitrary degree" is justified at every step.** It also allows degree 4 at X0 or X1.

Spot-check against MathTwoSixNeighbours with one middle each: I recomputed P1 →F C1 (W1 and m1 = a join K1; image gdbab, m2 = g, m3 = d) and P2 →F C3 (image gddab, m2 = g, m3 = b). Both agree with that note. I did not recompute the other four transitions.

## 4. Position table (note §4), with mirror

F sends position p to p + 2, B sends it to p + 3 (from x′_t = x_{t+3}, x_{t+2}). Rotation orientation is fixed by the frame, so y3 precedes y4.

| S | frame (x0..x4) | repeat (middle) | route | check |
|---|---|---|---|---|
| 01 | y3 y4 y0 y1 y2 | {y3,y0} (y4) | S01 | free = X0, X1. ≤ 6 |
| 12 | y2 y3 y4 y0 y1 | {y2,y4} (y3) | mirror of S01 | mirror t ↦ 2−t sends {1,2} to {1,0}; swaps F ↔ B, g ↔ d, G-F ↔ G-B; G is mirror-invariant (same component). Route: B,B,B,G,F (or B-starv / G-B when w3 = a). ≤ 6 |
| 34 | y0 y1 y2 y3 y4 | {y0,y2} (y1) | F → {0,1} | x′0 = x3 = y3, x′1 = y4. ≤ 7 |
| 40 | y4 y0 y1 y2 y3 | {y4,y1} (y0) | F → {1,2} | x′1 = x4 = y3, x′2 = x0 = y4. ≤ 7 |
| 23 | y1 y2 y3 y4 y0 | {y1,y3} (y2) | B → {0,1} | x′0 = x2 = y3, x′1 = y4. ≤ 7 |

The mirror reading is valid: the reversed reading of a DL frame is again a DL frame with lock 1 and lock 2 exchanged, and S01 uses only adjacency, (J) (mirror-symmetric) and starvation (mirror pair). Every row is correct. **Theorem R5³: CORRECT.** The application of Prop. S01 to F(s) or B(s) needs nothing about history: S01 holds for any DL state with S = 01.

Verdict item 2's class bookkeeping is correct: (5,7,6,5,5) = (5,5,5,7,6) and (5,8,6,5,5) = (5,5,5,8,6) cyclically; (5,6,5,5,8) and (5,5,6,5,6) have no three consecutive 5s.

## 5. Obstruction (note §5)

P4 (gdbab) and P7 (ddbab) at S = 01 have W3 = a, W1 = d: G-F. M(P4), M(P7) at S = 12: G-B. P5, P6 have W1 = g: F-starvation. P1, P2, P3 have W3 = b: the three-F chain. This matches the TwoSix S = 01 table row by row. P4, M(P4) ∈ C* and P7, M(P7) ∈ C, as listed in TwoSix §4.1–4.2. The theorem itself bounds every state of C ∪ C*, so the obstruction is broken. CORRECT. Note: the label "E2 (= W)" collides with the endpoint condition E2; rename.

## 6. Remarks for the author (no effect on correctness)

- **R1.** §2 confinement bullet: "once x4 has degree 5" → "once K_G = {x3, x4}".
- **R2.** §3 F1: "Any other change happens only at middles of X0 or X1." In fact a- or g-middles of X0 cannot change at F1 (they are adjacent to X0 ∉ K1); only middles of X1 and vertices beyond the ball can. Harmless overstatement.
- **R3.** The hypothesis "no separating triangle" is also what makes W_t well defined and the link induced (x2x4, x0x3 non-edges are used in §2). Already stated in §1; fine.
- **R4 (spec gap).** §7 item (b) gives the route for S = 01 only. At S = 12 the replay must use the mirror (W3 = a: B-starv if w0 = d, else G then B; W3 = b: B,B,B,G,F). At S = 34, 40 prefix F; at S = 23 prefix B.

## 7. Studio check spec (not run here)

Independent script `review_r555.py`, no imports from the producer's script or from vdred.

1. **Inputs.** Face lists: T4 (MathConjectureR §3); the two radius-5 holes (5,7,6,5,5), (5,8,6,5,5) from the coordinator's data; `gen_tri --all` orders 16–22; plus 200 random triangulations of order 18–26 made by flips avoiding N[v] ∪ {edges at y0,y1,y2}, so that y3, y4 reach degrees 6–12 (to stress the "arbitrary degree" claim). Skip graphs with a separating triangle.
2. **Holes.** Every degree-5 v whose link has three cyclically consecutive degree-5 vertices.
3. **States.** All proper 4-colourings of T − v up to colour permutation (or, above order 22, 2000 random DL states per hole); keep DL states.
4. **Assertions per DL state.**
   - (a) BFS radius over whole-component swaps in T − v: ≤ 7; ≤ 6 when the repeat pair is {y3,y0} or {y2,y4}.
   - (b) Replay the explicit route with the R4 corrections: prefix (F at S = 34, 40; B at S = 23); then at S = 01 the S01 route, at S = 12 its mirror; stop at the first non-DL state; assert a filled state is reached within the stated count.
   - (c) At every G step assert the {g,d}-component is exactly the two named link vertices.
   - (d) At every starvation step assert the starved vertex has no neighbour of the starved colour in the state just before the F or B swap, and assert the F/B image is not DL.
   - (e) Assert the W-colour list s1, s2, s3 of §3 at each F step of the W3 = b case.
5. **Expected.** 0 violations. Budget: one core, under 10 minutes; report counts per S and the radius histogram.

## 7a. Scope note (from the Math lead, relayed by the coordinator during this review)

- **Finding [Math lead; checked by hand here].** In a triangulation with no Birkhoff diamond, no degree-5 vertex has three consecutive degree-5 link vertices. If y0, y1, y2 have degree 5, then v, y1 and their two common neighbours y0, y2 are four degree-5 vertices on the two faces v y0 y1 and v y1 y2, which share the edge v y1. That is the Birkhoff diamond. I checked that the configuration matches. I have not rechecked the diamond's reducibility proof; it is classical [memory].
- **Consequence.** In the minimal-counterexample frame, where reducible configurations such as the diamond are excluded, the class of Theorem R5³ is **vacuous**. The theorem stays correct as a statement about all triangulations without a separating triangle, and that is what this review verifies. It still matters for the vacancy frame, but it adds nothing inside a minimal counterexample. This changes priorities, not any verdict above.

## 8. Ledger

- [hand, this review] Every step of §1–§5 of the note rederived; verdicts above. Two TwoSix transitions recomputed (P1 → C1, P2 → C3).
- [not reviewed] §6 Tait remarks and "D2 kills W"; the four other TwoSix transitions; the cited W →F P7; L3 and Theorem A (cited, previously reviewed).
- [open] the machine replay of §7.

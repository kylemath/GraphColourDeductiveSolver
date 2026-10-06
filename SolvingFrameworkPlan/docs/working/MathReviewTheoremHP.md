# Independent review: Theorem HP (MathHighDegreeNeighbour.md §1–§2)

Review worker, 6 October 2026. I did not write these claims. Every step below was checked **by hand**. No code was run: at 13:01 the Math lead relayed a user decision to stop running code on this machine because the battery was low. The only command I ran before that was one `grep` for the belt definition. No re-check scripts were written or run (see §C). No file of anyone else was edited, and nothing was committed.

Definitions are taken from MathConfinementAttack.md Step 1 (DL means both locks hold), MathRadiusGeometry.md (Theorem H, its erratum, and R1/R2/R3) and MathReviewArTheoremH.md. The frame is: link (a,b,a,g,d) on x_0..x_4; w_t is the third vertex of the outer face on the edge x_t x_{t+1}; p = x_k.

## A. Verdicts per statement (hand)

1. **Setup (§1): CORRECT, with two remarks.**
   - A degree-5 vertex x_t has neighbours exactly v, x_{t-1}, x_{t+1}, w_{t-1}, w_t. For t ≠ k this gives ring edges w_{t-1}w_t. When deg p > 5, the only edge that may be missing is w_{k-1}w_k.
   - **Distinctness: what "no separating triangle meets the ball" must supply.**
     - The proof needs the link to have no chords. A chord x_i x_j gives a non-facial triangle v x_i x_j, which is separating. So the hypothesis supplies this, and with it the neighbour lists above and w_t ∉ link.
     - A coincidence w_s = w_t at non-adjacent positions makes a non-facial triangle {y, x_i, x_{i+1}}. I checked w_0 = w_2 and w_1 = w_3 at k = 0 explicitly. So the hypothesis excludes these too.
     - The proof does not actually need distinctness of the w's. Every deduction has the form "adjacent, so different colours". A coincidence only adds equalities, so it can only shrink the pattern list. It never invalidates a kill or a transition, because those read only the colours of named vertices. The m's may coincide with ring vertices; for example p ~ w_{k+2} creates only a 4-cycle, and nothing reads the m's.
     - The hypothesis is enough. Strictly, "the link has no chord" is all the proof uses.
   - Remark: the doc writes e = deg p − 5, so it implicitly assumes deg p ≥ 5. If deg p = 4, then w_{k-1} = w_k. I checked that the surviving patterns are then all easy, so the theorem still holds; this is moot under minimum degree 5.

2. **Jordan facts: CORRECT.**
   - x_0 ∉ K_F: the curve v x_1 P_2 x_4 v is coloured {b,d} off v. The rotation at v puts x_0 on one side and x_2, x_3 on the other. An {a,g}-path cannot meet the curve, and planar edges do not cross.
   - x_2 ∉ K_B: the same argument with P_1.
   - No degree is used.

3. **F-starvation: CORRECT, for any degrees.**
   - After F the link is (a,b,g,a,d). The new frame is j = 3, with b' = d, g' = b, d' = g. Lock 2' is a {d,g}-path from x_4 to x_2.
   - After F, the neighbours of x_2 are x_1 (b, not in K_F), x_3 (now a), the former g-neighbours (all in K_F, now a) and the unchanged b and d neighbours. So x_2 has a d-neighbour after F exactly when it had one before.
   - **B-starvation: CORRECT.** I checked it directly, not only through the mirror. After B the frame is j = 2 with b' = g, g' = d, d' = b. Lock 1' is a {g,d}-path from x_3 to x_0, and it needs a g-neighbour of x_0.

4. **Mirror: CORRECT.** The map is (w_0..w_4) → (w_1,w_0,w_4,w_3,w_2) with g ↔ d, and k → 2 − k (mod 5). I checked that it maps the k = 3 list onto the k = 4 list item by item, and that it fixes R1 and R3.

5. **Lemma 1 (pattern table): CORRECT.** I re-derived all five rows independently.
   - Allowed colours: w_0, w_1 ∈ {g,d}; w_2 ∈ {b,d}; w_3 ∈ {a,b}; w_4 ∈ {b,g}.
   - Conditions: {w_0,w_1} = {g,d} if k ≠ 1; b ∈ {w_2,w_3} if k ≠ 3; b ∈ {w_3,w_4} if k ≠ 4; the ring edges for t ≠ k.
   - k = 0: R1, R2, R3. At k = 2 the missing edge w_1w_2 still forces w_2 = b in the gd-branch, through the b at x_3.
   - k = 1: dgdbg, plus w_2 = w_4 = b, w_3 = a with (w_0,w_1) free in {g,d}².
   - k = 3: gdbab, dgbab, dgdab, dgbbg, dgdbg.
   - k = 4: gdbab, dgbab, dgbag, dgdbb, dgdbg.
   - Exactly as stated. The only facts used are the degree-5 neighbour lists and the lock end edges (Theorem H Step 1).

6. **Lemma 2 (easy states): CORRECT.** Every non-R1/R3 pattern is covered, and each kill reads only a degree-5 vertex.
   - B-starvation needs x_0 of degree 5 (k ≠ 0) and w_0, w_4 ≠ g. This holds for dgbab@1–4, ddbab@1, dgdab@3 and dgdbb@4.
   - F-starvation needs k ≠ 2 and w_1, w_2 ≠ d. This holds for dgbab@0, ggbab@1, dgbbg@3 and dgbag@4.
   - AB for R3 at k = 3, 4:
     - The {a,b}-component of x_1 is exactly {x_0,x_1,x_2}. Its outside neighbours are w_4..w_2 = g,d,g,d, together with x_3 = g and x_4 = d. So it is a single whole-component Kempe swap, not a composition.
     - After the swap, at k = 3, x_4 has neighbours g, b, b, g, so lock 2' fails.
     - At k = 4, x_3 has neighbours b, d, d, b, so lock 1' fails.

7. **Lemma 3 (transitions): CORRECT.**
   - F on R1:
     - w_3 (a, adjacent to x_3) lies in K_F.
     - w_0 (g, adjacent to x_0) does not, by the Jordan fact.
     - The new ring (w_3,w_4,w_0,w_1,w_2) = (g,b,g,d,b) reads as dgdbg = R3 under b' = d, g' = b, d' = g.
   - F on R3: w_1 → a, and the new ring (b,g,d,a,d) reads as gdbab = R1.
   - B on R1 and B on R3: I checked both directly. The frame is j = 2, (w_2,w_3,w_4,w_0,w_1) is read with b' = g, g' = d, d' = b, and the images are R3 and R1 respectively.
   - The position shift is k − 3 for F and k + 3 for B.
   - Only colours of named ring vertices are read. Neither p's degree nor any m is used. If the image is DL, it lies in Lemma 1's list automatically.

8. **Termination table and Theorem HP (radius ≤ 6): CORRECT.**
   - The chains are:
     - R1@1 →F R3@3 (easy);
     - R1@2 →F R3@4;
     - R1@0 →B R3@3;
     - R3@0 →F R1@2;
     - R3@2 →B R1@0;
     - R1@3 →F R3@0;
     - R1@4 →B R3@2;
     - R3@1 →F R1@3 (→B R1@4 gives the same value).
   - The values are D = 2, 2, 2, 3, 3, 4, 4, 5. Each value is checked; there is no cycle in the dependencies.
   - radius = 1 + d(s, NL) is valid. From a non-DL state with a 4-coloured link, swapping the failing lock's component of x_1 fills, because that component contains no other link vertex of those colours.
   - **Finer bounds: CORRECT.** They are: easy 2; R1@0,1,2 at most 3; R3@3,4 at most 2; R3@0,2 at most 4; R1@3,4 at most 5; R3@1 at most 6.
   - The statement "never reads a neighbour of p" holds.

9. **§2 "Checks [computed]", §3 radius-4 examples, belt radius 2, sharp value 4: UNVERIFIED.** No code was run (see §C).
   - The order-22 example (#99 of `gen_tri 22 --all`) has **no face list in the doc**. It cannot be rebuilt independently without gen_tri's enumeration order. The doc should add its face line.

10. **Verdict item 3 (local control lost only when p is in the AB triple): UNVERIFIED.** It is an informal mechanism statement, not a proved lemma. It is consistent with the proof: the only non-easy terminal kill, AB, is used exactly when p ∉ {x_0,x_1,x_2}.

## B. Bottom line

No gap found in Theorem HP or in Lemmas 1–3, F-starvation and B-starvation. Two wording fixes are needed:
- (i) Say that the proof uses only the absence of link chords; the w's may coincide.
- (ii) State deg p ≥ 5, or note the deg p = 4 case.

All [computed] claims in the doc remain unverified by this review.

## C. Computational re-checks: status and commands for the Mac Studio

| re-check | status |
|---|---|
| Belt G_n, n = 6..10, exhaustive DL radii | NOT DONE |
| Order-29 example (face line in §3), radius histogram {2:362, 3:23, 4:9} | NOT DONE |
| Order-22 example | NOT DONE, and not possible as stated: faces missing |
| Random (5,5,5,5,d) triangulations, d = 6..14, strict transition checks | NOT DONE |

The script does not exist yet. A reviewer must write it independently and must not import `MathHighDegreeNeighbour-scripts/`. Specification for `hp_review.py`:
- **Input:** a face line in census `G` format, plus the hole v.
- **States:** enumerate all proper 4-colourings of T − v, canonical under colour permutation.
- **Moves:** Kempe neighbours are all whole-component swaps.
- **Radius:** run a multi-source BFS from the filled states (the link uses at most 3 colours); the radius is the BFS distance.
- **Checks on each DL state:**
  - frame, pattern and k;
  - the pattern is in the Lemma 1 table;
  - each easy kill's named swap gives a non-DL state;
  - the F and B images are non-DL, or are DL of the type and position Lemma 3 predicts;
  - the AB component is {x_0,x_1,x_2} for R3 at k = 3, 4;
  - radius ≤ 1 + D(class).

Commands, with at most 2 cores and at most 10 CPU-minutes in total:
```
python3 hp_review.py --faces-line "$(sed -n '/^G 29/p' MathHighDegreeNeighbour.md)" --hole 2      # expect {2:362,3:23,4:9}
for n in 6 7 8 9 10; do python3 hp_review.py --belt $n --hole u0; done                           # expect all radius 2 (none at n=7)
python3 hp_review.py --random --d 6..14 --per-d 20 --order 20..30 --seed 1 --require-4conn       # flips that avoid v and the four degree-5 link vertices
```
The belt input needs the G_n definition: the TwoPoleBelt.lean adjacency, two poles of degree n, belt vertices of degree 5.

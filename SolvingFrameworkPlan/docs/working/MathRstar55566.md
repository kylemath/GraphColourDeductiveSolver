# Lemma R* at a degree-5 hole with three consecutive degree-5 neighbours (covers (5,5,5,6,6) and (5,5,5,d,d′) for all d, d′)

Math research worker, front 1, 6 October 2026. **Hand work only.** The machine was on battery restriction, so no code, script or build was run; files were only read. Labels: [hand] derived here by hand, not machine-checked; [cited] taken from a reviewed note; [guidance] machine output from another note, used only as a consistency check. No other file was edited and nothing was committed.

Inputs: MathTwoSixNeighbours.md (frame, kill rules, (adj) tables), MathHighDegreeNeighbour.md (Theorem HP, F/B-starvation), MathRadiusGeometry.md (Theorem H), MathReviewCleanToVHE.md (L1 Theorem A for pure Kempe classes; L3 finite radius ⇒ clean), pd2_lock_proof.md (Tait lock criterion), intern notes, and the radius-5 messages.

## Verdict, first

1. **[hand] Theorem R5³.** Let T be a triangulation with no separating triangle (this includes the relative class: degree-4 vertices on a protected face φ are allowed, with v ∉ φ). Let v have degree 5, with link y0..y4 in rotation order, where **y0, y1, y2 have degree 5 and y3, y4 have any degrees**. Then every doubly locked (DL) state at v has Kempe radius **at most 7**. DL states whose repeat pair is {y3, y0} or {y2, y4} have radius **at most 6**.
2. **This answers the front-1 target** (class (5,5,5,6,6)) with an explicit bound, and it does not use degree exactly 6. Per the coordinator's request, here is the degree audit: **no step uses the degree of y3 or y4**, and no step uses the degree of any ring vertex. The only degree facts used are deg y0 = deg y1 = deg y2 = 5. So the theorem covers the new radius-5 classes (5,7,6,5,5) and (5,8,6,5,5): read cyclically, these are (5,5,5,7,6) and (5,5,5,8,6). It does **not** cover (5,6,5,5,8), which has no three consecutive 5s, nor (5,5,6,5,6).
3. **The missing move.** The extra ingredient is the swap **G**: the {g,d}-component of x3, which contains x4. When x3 and x4 both have degree 5 and the ring next to them is b-coloured, G is confined to {x3, x4}. Two kill rules follow: **G-F** (G, then F-starvation) and **G-B** (G, then B-starvation). With them, the 20-state obstruction C ∪ C* of MathTwoSixNeighbours §4 breaks (§5). No outside-matching memory and no potential function is needed.
4. **Consistency [guidance].** The bound is 7. This equals the vdred game depth for (5,5,5,6,6). All recorded radii lie within the bound: T4 has 4, and the coordinator's radius-5 data for (5,5,5,7,6) and (5,5,5,8,6) has 5. The Studio check spec is in §7.

## 1. Frame and the facts used [hand / cited]

- Fix a DL state s. Rotate it so that the link reads (a,b,a,g,d) on x0..x4. Lock 1 is a {b,g}-path from x1 to x3, and lock 2 is a {b,d}-path from x1 to x4, both in T − v.
- w_t is the common neighbour of x_t and x_{t+1} other than v. A degree-5 link vertex x_t has exactly the neighbours v, x_{t−1}, x_{t+1}, w_{t−1}, w_t.
- **No separating triangle** is used only to get the following. The link is an induced 5-cycle, so no outer neighbour of a link vertex is a link vertex. Consecutive outer neighbours of a link vertex are adjacent. Coincidences among outer vertices are allowed: every deduction below has the form "adjacent, so differently coloured" or "these are the neighbours of x_t, with these colours", and both survive coincidences.
- **(J) Jordan facts** [cited: HP §1; review L1]. x0 ∉ K_F, where K_F is the {a,g}-component of x2. x2 ∉ K_B, where K_B is the {a,d}-component of x0. Consequently, an a- or g-vertex adjacent to x0 is not in K_F.
- **F** swaps K_F (which contains x3). The image has link (a,b,g,a,d) and is read in the frame x′_t = x_{t+3}. **B** swaps K_B (which contains x4). The image is read in the frame x′_t = x_{t+2}. Neither image is ever filled, because each link has four colours.
- **F-starvation** [cited: HP §1; reproved in the margin of §3]. If x2 has no neighbour coloured c(x4), then F(s) is not DL.
- **B-starvation.** If x0 has no neighbour coloured c(x3), then B(s) is not DL.
- **Unlock** [cited: review L1 Step 1]. An unfilled state that is not DL fills in one swap. So radius(s) ≤ 1 + radius(s′) for any single swap s → s′, and radius ≤ 2 if some single swap gives a non-DL state.
- **E1–E3** at degree-5 endpoints. If x1 has degree 5, then {w0, w1} = {g, d}. If x3 has degree 5, then b ∈ {w2, w3}. If x4 has degree 5, then b ∈ {w3, w4}.

## 2. The new kill rules G-F and G-B [hand]

**Lemma G.** Let G be the swap of the {g,d}-component K_G of x3. K_G contains x4.
- **(G-F)** Suppose no neighbour u of x2 satisfies either (c(u) = g and u ∉ K_G) or (c(u) = d and u ∈ K_G). Then radius(s) ≤ 3.
- **(G-B)** Suppose no neighbour u of x0 satisfies either (c(u) = d and u ∉ K_G) or (c(u) = g and u ∈ K_G). Then radius(s) ≤ 3.

*Proof.*
- s′ = G(s) has link (a,b,a,d,g), which is unfilled, and the same frame. In s′ the colour of x4 is g.
- (G-F). The hypothesis says exactly that x2 has no g-neighbour in s′. So F-starvation applies to s′, and F(s′) is not DL.
- (G-B). The hypothesis says that x0 has no neighbour of colour c′(x3) = d in s′. So B(s′) is not DL.
- In either case there are three swaps: G, then F or B, then the unlock. If s′ is not DL already, two swaps suffice. ∎

**Margin: the starvation rule, reproved.**
- F(s′) swaps the {a, c′(x3)}-component of x2. Its new lock 2 is a {c′(x4), c′(x3)}-path from x4 to x2. That path enters x2 through a vertex coloured c′(x4).
- A neighbour of x2 whose colour is not in {a, c′(x3)} keeps its colour under F. The neighbours coloured a or c′(x3) are in the swapped component and take colours in {a, c′(x3)}.
- So x2 has a c′(x4)-neighbour after F if and only if it had one before.

**Confinement.** If x3 and x4 have degree 5, w2 = b and w4 = b, then K_G = {x3, x4}.
- The neighbours of x3 are x2 (a), x4, w2 (b) and w3 ∈ {a,b}.
- The neighbours of x4 are x3, x0 (a), w3 and w4 (b).
- Then G-F reads "w1 ≠ g", once x2 has degree 5. G-B reads "x0 has no outer neighbour coloured d", once x4 has degree 5.

## 3. The key position: middle and one repeat vertex are the two free vertices [hand]

Name the vertices so that **X2, X3, X4 have degree 5**. X0 and X1 have arbitrary degree, with outer neighbours W4, (middles of X0), W0, (middles of X1), W1. Here W_t is the common outer neighbour of X_t and X_{t+1}. Take a DL state s0 with link (a,b,a,g,d) on X0..X4; the repeat pair is {X0, X2} and the middle is X1. (In §1 notation this is the frame with S = {0,1}; the mirror reading gives S = {1,2}.)

Admissible colours at the degree-5 vertices: W1 ∈ {g,d}, W2 ∈ {b,d}, W3 ∈ {a,b}, W4 ∈ {b,g}. The ring edges W1W2, W2W3 and W3W4 exist.

**Proposition S01.** radius(s0) ≤ 6. No degree of X0 or X1 is used, and the colours of their middle neighbours are never read.

*Case W3 = a.* E2 gives W2 = b, and E3 gives W4 = b.
- **If W1 = g:** the neighbours of X2 are X1 (b), X3 (g), W1 (g), W2 (b), with no d. F-starvation gives radius ≤ 2.
- **If W1 = d:** K_G = {X3, X4} by confinement. After G, the neighbours of X2 are b, d, d, b, with no g. G-F gives radius ≤ 3.

*Case W3 = b.* Then W2 = d (W2 ∈ {b,d} and W2 ≠ W3), W4 = g (W4 ≠ W3) and W1 = g (W1 ≠ W2). Follow three F moves. Each one either produces a non-DL state, which ends with the unlock, or produces the state named below.

- **F1** (state s0). K1 is the {a,g}-component of X2.
  - The a/g-neighbours of X3 (neighbours X2, X4 d, W2 d, W3 b) are X2 only.
  - W1 (g) lies in K1. W4 (g) is adjacent to X0, so it is not in K1 by (J).
  - Any other change happens only at middles of X0 or X1.
  - s1: X0 a, X1 b, X2 g, X3 a, X4 d. W1 = a, W2 = d, W3 = b, W4 = g.
  - Repeat pair {X3, X0}, middle X4.
- **F2** (state s1, frame x′_t = X_{t+3}). K2 is the {a,b}-component of X0, and it contains X1. Every a- or b-coloured ring vertex is forced either way, so nothing branches:
  - W1 (a, adjacent to X1) is in K2.
  - The b-middles of X0 and the a-middles of X1 are in K2.
  - W3 (b) is adjacent to X3, and X3 ∉ K2 by (J) for s1. So W3 is out.
  - s2: X0 b, X1 a, X2 g, X3 a, X4 d. W1 = b, W2 = d, W3 = b, W4 = g.
  - Repeat pair {X1, X3}, middle X2.
- **F3** (state s2, frame x″_t = X_{t+1}). K3 is the {a,d}-component of X3, and it contains X4.
  - The neighbours of X3 are X2 (g), X4 (d), W2 (d) and W3 (b), so W2 ∈ K3.
  - The other neighbours of X4 are X0 (b), W3 (b) and W4 (g).
  - X1 ∉ K3 by (J) for s2.
  - Middles of X0 may branch in or out. That is irrelevant, because they are never read again.
  - s3: X0 b, X1 a, X2 g, X3 d, X4 a. W1 = b, W2 = a, W3 = b, W4 = g.
  - Repeat pair {X4, X1}, middle X0. In frame form, x‴ = (X4, X0, X1, X2, X3) = (a, b, a, g, d).
- **Kill at s3 by G-B.**
  - The neighbours of X2 are X1 (a), X3 (d), W1 (b), W2 (a). The neighbours of X3 are X2, X4 (a), W2 (a), W3 (b). So the {g,d}-component of X2 is {X2, X3}.
  - After G: X2 = d and X3 = g.
  - The neighbours of X4 are X3 (g), X0 (b), W3 (b), W4 (g). There is no d, so B-starvation applies.
- **Count.** F1, F2, F3, G, B, unlock: radius ≤ 6. ∎

Check against MathTwoSixNeighbours §3 (exactly-6 case). My re-derived S = 01 table matches theirs: P1–P7. W3 = a gives P4 and P7 (G-F) and P5 and P6 (F-starvation). W3 = b gives P1, P2 and P3. With exactly one middle each, the chain above is P1 → C1 → M(C6) → M(P4), and P2 → C3 → M(C4) → M(P7). I also recomputed all six of these transitions in that note's pattern notation; they agree with the note.

## 4. Theorem R5³ [hand]

The degree-5 vertices are y0, y1, y2; y3 and y4 are free. A DL state has its repeat pair at one of five positions. Let S be the set of frame positions of {y3, y4}, so S ∈ {01, 12, 23, 34, 40}. F moves S to S+2 and B moves S to S+3 (mod 5), and both images are unfilled.

| S | repeat pair (middle) | route | radius ≤ |
|---|---|---|---|
| 01 | {y3, y0} (y4) | Prop. S01 | 6 |
| 12 | {y2, y4} (y3) | Prop. S01 read in the reverse rotation (it is orientation-free) | 6 |
| 34 | {y0, y2} (y1) | F, which gives S = 01 or a non-DL state | 7 |
| 40 | {y4, y1} (y0) | F, which gives S = 12 | 7 |
| 23 | {y1, y3} (y2) | B, which gives S = 01 | 7 |

So every DL state has radius ≤ 7. By L3 of the review, v is pure-clean and hence clean for every φ ∌ v. Finiteness alone also follows from Theorem A plus S01: a targetless class would contain an S = 01 state, which is impossible. ∎

Notes:
- (i) Only deg y0 = deg y1 = deg y2 = 5 and the absence of separating triangles are used. Degree-4 vertices elsewhere are irrelevant, and so is φ, because the swaps are unrestricted.
- (ii) The theorem contains Theorem H and Theorem HP's class (5,5,5,5,p), with a weaker constant (7 against HP's 6).
- (iii) In the unavoidable-set language of HP §4, the theorem settles every class with three consecutive link degrees equal to 5.

## 5. What this does to the earlier obstruction [hand]

- **C\*** (deterministic under F) contains P4 and M(P4), which are killed by G-F and G-B. **C** contains P7 and M(P7), which are killed the same way.
- The obstruction existed only because G was never tried at S = 01/12. MathTwoSixNeighbours §6 dismissed G as "a self-loop under total leak". That is true at S = 34 (at W and W*, K_G contains every g/d ring vertex), but false at S = 01/12, where K_G is confined.
- **E2 (= W)** has radius ≤ 1 + 3 = 4: F gives P7, and P7 dies by G-F. This is consistent with the Studio's observed radius 2–3 at E2. I did not identify the exact radius-2 swap; it is not needed.
- **KILLED:** "C ∪ C\* needs outside-matching memory." Memory is not needed; one extra link-seeded swap suffices.
- **NOT NEEDED:** the potential/Tait-global idea (1) and the memory idea (3).

## 6. Side results and dead ends [hand]

- **Tait form of the move set** (a check, not used above). In the dual, the P-edge colours are always (3,1,1). A state is filled exactly when its two minority edges are adjacent on P.
  - A state is DL exactly when its β–γ P-paths pair as {j+1,j+2}, {j,j+3} and its β–δ P-paths pair as {j,j+4}, {j+1,j+3}.
  - The five P-paths correspond to the swaps G (≈ AB, modulo cycle switches), D2 = {a,d}@x2, B, G0 = {a,g}@x0, and F.
- **(5,5,6,5,6), not covered.** The analogous S = 02 position allows G-confinement at N2 and N4. The follow-up starvations fail there: m2 = g blocks G-F at N2, w1 = g blocks it at N4, and m0 = d (N2) or w0 = d (N4) blocks G-B. So R5³'s method does not close the non-adjacent class directly [hand, partial; KILLED as a one-line extension].
- **KILLED:** "D2 kills W": at W, D2 is deterministic, but neither starvation fires on the image.

## 7. Studio check spec (not run here)

New script `rstar_three_fives.py`, written independently, with no producer imports.
- **Input:** a face list.
- **Holes:** every degree-5 hole v whose link has three consecutive degree-5 vertices, with no separating triangle in the graph.
- **For each DL state at such a hole:**
  - (a) compute the exact radius by BFS over whole-component swaps of T − v, and assert it is ≤ 7, and ≤ 6 when the repeat pair is {y3,y0} or {y2,y4};
  - (b) replay the named route of §3/§4 (W3 = a: F or G,F; W3 = b: F,F,F,G,B), stopping at the first non-DL state, and assert that a non-DL state is reached within the stated number of swaps;
  - (c) assert that the confinement claims hold (K_G = {X3,X4} and {X2,X3}) wherever they are invoked.
- **Graphs:** T4 (MathConjectureR §3), the four Phase C cert graphs in `backgroundMaterial/planemap-structural/studiointel/run-C-2026-10-06/cert/`, the hole classes (5,7,6,5,5) and (5,8,6,5,5) from the coordinator's new data, and `gen_tri --all` at orders 16–22.
- **Expected:** 0 violations. Max radius 4 on T4, and 5 on the new radius-5 holes of these two classes.
- **Budget:** one core, under 10 minutes.

## 8. Ledger

- [hand]:
  - Lemma G (G-F and G-B);
  - the confinement criterion;
  - Proposition S01, which is degree-free in X0 and X1;
  - Theorem R5³ (radius ≤ 7);
  - the six recomputed exactly-6 transitions;
  - the S = 01 table;
  - the Tait remarks;
  - the (non) partial.
- [cited]: the Jordan facts, F/B-starvation, the unlock step, Theorem A, and L3.
- [open]:
  - a second reader and the machine replay of §7;
  - the classes without three consecutive 5s: (5,5,6,5,6), (5,6,5,5,8), (5,5,6,6,6), and so on.
- **Every [hand] item is unchecked by a second reader and by machine.**

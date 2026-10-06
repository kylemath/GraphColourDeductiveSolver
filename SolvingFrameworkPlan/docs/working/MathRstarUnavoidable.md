# R*: which link classes are unavoidable once H and HP are used (hand discharging)

Math research worker, front 1, 6 October 2026. **Hand work only; no code was run.** No other file edited, nothing committed. Every proof below is complete by hand [hand]. Literature is mentioned only in one clearly marked remark; nothing depends on it.

## 0. Setting and notation

**Class.** (T, φ): T is a 4-connected triangulation of the sphere, φ = {a, b, c} a facial triangle, every vertex off φ has degree ≥ 5, and at most two vertices of φ have degree 4 (n₄ ≤ 2; all degree-4 vertices lie on φ). Since T is 4-connected, every vertex has degree ≥ 4, the link of every vertex is a cycle whose vertices are distinct, and two adjacent vertices v, w have **exactly two** common neighbours (a third would give a separating triangle).

**Link class.** For a degree-5 vertex v, its link is the cyclic sequence (d₀, …, d₄) of the degrees of x₀, …, x₄, read up to rotation and reflection. Call a link entry **small** if it is 4 or 5, **mid** if it is 6, and **big** if it is ≥ 7. Let k(v) be the number of entries equal to 5.

**Tools used as black boxes (proved and audited elsewhere).**
- **H:** link (5,5,5,5,5) ⇒ radius ≤ 3.
- **HP:** four link entries equal to 5, fifth arbitrary ⇒ radius ≤ 6. Hypothesis "no separating triangle meets the ball" holds in the class.
- **D4** (`MathVHCoreAdvance` §2, as cited in `MathReviewCleanToVHE` L5.1): a link vertex of degree ≤ 4 gives a fill in ≤ 3 pure swaps.

So v is **handled** if v ∉ φ, deg v = 5, and either k(v) ≥ 4 (H/HP) or some link entry is 4 (D4).

**Charges.** μ(x) = d(x) − 6. Since 2E = 6V − 12, Σ μ = −12. For a big vertex w put τ(w) = (d(w) − 6)/d(w) = 1 − 6/d(w); for d(w) ≤ 6 put τ = 0. Values: τ(7) = 1/7, τ(8) = 1/4, τ(9) = 1/3, τ(10) = 2/5, τ(11) = 5/11, τ(12) = 1/2, τ(13) = 7/13, τ(14) = 4/7, τ(15) = 3/5, τ(16) = 5/8, τ(17) = 11/17, τ(18) = 2/3. τ is strictly increasing and < 1.

## 1. The main discharging lemma (Lemma W)

**Definition.** For a degree-5 vertex v with link x₀..x₄ (indices mod 5) put

  W(v) = Σᵢ τ(xᵢ) · (1 + ½[d(xᵢ₋₁) ≥ 6] + ½[d(xᵢ₊₁) ≥ 6]).

So each big neighbour contributes τ times a multiplier 1, 3/2 or 2, according to how many of its two link-neighbours (the common neighbours of v and that big vertex) have degree ≥ 6.

**Lemma W [hand].** In every (T, φ) of the class,

  Σ_{v ∉ φ, deg v = 5, W(v) < 1} (1 − W(v)) ≥ 9 − n₄ ≥ 7.

In particular at least 9 − n₄ ≥ 7 degree-5 vertices off φ have W(v) < 1.

**Proof.** Discharging rule. Let w be big, with ring (link cycle) u₁, …, u_d, d = d(w). Give each ring position a token of value τ(w).
- A ring vertex of degree 5 keeps its own token: w sends τ(w) to it.
- A ring vertex u_j of degree ≥ 6 splits its token in halves, one per ring side: for each ring-neighbour u_{j±1} of degree 5, w sends τ(w)/2 to that ring-neighbour. Halves pointing at a non-5 vertex stay with w.
- Tokens at ring vertices of degree 4 stay with w.

No other charge moves.

*Big vertices.* w sends at most d·τ(w) = d − 6 = μ(w). Final charge ≥ 0.

*Degree-6 vertices.* They neither send nor receive. Final charge 0.

*Degree-5 vertices.* A degree-5 vertex v appears exactly once on the ring of each big neighbour w. Its two ring-neighbours there are the two common neighbours of v and w, which are the link-neighbours of w inside the link of v. So v receives exactly W(v). Final charge = −1 + W(v).

*Degree-4 vertices* (all on φ). They receive nothing. Final charge −2.

Sum the final charges, which still total −12:
- Vertices of φ: a degree-4 vertex ends at −2 and a degree-5 vertex at ≥ −1, so φ contributes ≥ −(2n₄ + (3 − n₄)) = −(3 + n₄).
- Off φ, every vertex ends ≥ 0, except the degree-5 vertices with W < 1, which end at −(1 − W(v)).

Hence −12 ≥ −(3 + n₄) − Σ_{W<1, off φ}(1 − W(v)). Since each term is ≤ 1, the count is ≥ 9 − n₄. ∎

**Remarks.**
1. Lemma W refines the audited Euler lemma. Two big entries of degree ≥ 12 already give W ≥ ½ + ½ = 1, so every vertex with W < 1 has at most one neighbour of degree ≥ 12.
2. Any convex combination of valid rules is valid. §5 gives a second rule W′. Mixtures give further unavoidable families; this is the tuning knob for the "smallest family".

## 2. The exact residual list after H, HP and D4 (answer to (b))

Let v be off φ with W(v) < 1, not handled, so k(v) ≤ 3 and no entry is 4. Write p, q, r for big entries. Each case below follows from the definition of W by monotonicity of τ; the ranges are where the inequality is strict.

**|B| = 0 (no big neighbour): W = 0.** Six classes:

 S1 (6,6,6,6,6), S2 (5,6,6,6,6), S3 (5,5,6,6,6), S4 (5,6,5,6,6), S5 (5,5,5,6,6), S6 (5,5,6,5,6).

**|B| = 1**, p at position 0; m = number of 6s among positions 1 and 4; W = τ(p)(1 + m/2).
- **m = 0 (FREE, any p ≥ 7):** F1 (p,5,5,6,5), F2 (p,5,6,6,5).
- m = 1, p ≤ 17 (τ(p) < 2/3): (p,5,5,5,6), (p,5,5,6,6), (p,5,6,5,6), (p,5,6,6,6).
- m = 2, p ≤ 11 (τ(p) < 1/2): (p,6,5,5,6), (p,6,5,6,6), (p,6,6,6,6).

**|B| = 2, adjacent** (p,q,d₂,d₃,d₄). Big neighbours count as ≥ 6, so the multipliers are μ_p = 3/2 + ½[d₄ = 6] and μ_q = 3/2 + ½[d₂ = 6]. d₃ ∈ {5,6} is free.
- d₂ = d₄ = 5: τp + τq < 2/3 ⇔ {p,q} ∈ {7}×{7..12} ∪ {8}×{8..10}.
- d₄ = 6, d₂ = 5: 2τp + 3/2·τq < 1 ⇔ (p,q) ∈ {7}×{7..11} ∪ {8}×{7,8} ∪ {(9,7)}.
- d₂ = d₄ = 6: τp + τq < 1/2 ⇔ {p,q} ∈ {7}×{7,8,9}.

**|B| = 2, non-adjacent** (p,d₁,q,d₃,d₄); d₁ is adjacent to both.
- d₁ = d₃ = d₄ = 5: τp + τq < 1 ⇔ p ≤ q with (7, ≤41), (8, ≤23), (9, ≤17), (10, ≤14), (11, ≤13).
- d₁ = 5, d₃ = 6, d₄ = 5 (the 6 next to q): τp + 3/2·τq < 1 ⇔ q = 7, p ≤ 27; q = 8, p ≤ 15; q = 9, p ≤ 11; q = 10, p ≤ 9; q = 11, p ≤ 8; q ∈ {12,13}, p = 7.
- d₁ = 5, d₃ = d₄ = 6; or d₁ = 6, d₃ = d₄ = 5: τp + τq < 2/3, same pairs as the first adjacent case.
- d₁ = 6 and exactly one of d₃, d₄ = 6: same pairs as the second adjacent case (the 2-multiplier sits on the big whose other side is the 6).
- d₁ = d₃ = d₄ = 6: {p,q} ⊂ {7}×{7,8,9}.

**|B| = 3**
- Consecutive (p,q,r,d₃,d₄), multipliers (3+[d₄=6])/2, 2, (3+[d₃=6])/2. Solutions: (7,7,7,d₃,d₄) for all d₃, d₄ ∈ {5,6}; (7,8,7,5,5); (8,7,7,d₃,5) with d₃ ∈ {5,6}.
- Split (p,q,d₂,r,d₄), with p, q adjacent:
  - d₂ = d₄ = 5: 3/2(τp + τq) + τr < 1. Solutions: p = q = 7 with r ≤ 13; {p,q} = {7,8} with r ≤ 10; p = q = 8 with r = 7; {p,q} = {7,9} with r ≤ 8; {p,q} = {7,10} with r = 7.
  - d₂ = 6, d₄ = 5: 3/2τp + 2τq + 3/2τr < 1. Solutions: all 7; or exactly one of p, q, r equal to 8.
  - d₂ = d₄ = 6: only (7,7,6,7,6).

**|B| ≥ 4: impossible.** Four 7s with a 5 already give multipliers 3/2 + 2 + 2 + 3/2 = 7, so W ≥ 7/7 = 1.

**Corollary R-list [hand].** Every core (T, φ) has at least 9 − n₄ ≥ 7 degree-5 vertices off φ, each of which is one of the following:
- (i) handled by D4;
- (ii) handled by H/HP (k ≥ 4);
- (iii) one of S1–S6;
- (iv) one of the **two free shapes F1, F2**;
- (v) one of the bounded classes above.

In every class at most one entry is ≥ 12, and every entry is ≤ 41. **Apart from HP, F1 and F2 are the only classes where R\* must handle a neighbour of unbounded degree.** In both, the free vertex p is flanked in the link of v by two degree-5 vertices, exactly as in HP and the belt.

**What is forced, i.e. lower bounds on any unavoidable family [hand].**
- **(6,6,6,6,6) is forced.** The pentakis dodecahedron has only such holes. More generally, GC(2,0) of any minimum-degree-5 triangulation has every degree-5 vertex surrounded by new degree-6 vertices.
- **An unbounded entry is forced** (the belt, (5,5,5,5,n)), and HP covers it.
- **Open.** Whether any of S2–S6, F1, F2 or the |B| ≥ 2 classes is individually forced. This needs constructions in which every off-φ 5-vertex lies in that class. I have none by hand. The minimality of the family is therefore **not** proved; Lemma W gives an upper family only.

## 3. Consequences of "no H/HP vertex" (answer to (a))

Assume no off-φ 5-vertex is handled.

- **(A1)** Lemma W and Corollary R-list hold with (i) and (ii) removed: at least 9 − n₄ vertices lie in (iii)–(v), with weighted slack Σ(1 − W) ≥ 9 − n₄.
- **(A2) [hand] Few hubs need many 6s.**
  - Every off-φ 5-vertex has ≥ 2 neighbours of degree ≥ 6 (k ≤ 3, no degree-4 entry). Each degree-6 vertex has ≤ 6 neighbours of degree 5 and each big vertex has ≤ d.
  - So 2(n₅ − 3) ≤ 6n₆ + Σ_big d·n_d. Substituting n₅ = 12 − 2n₄ + Σ(d − 6)n_d:
  - **6n₆ ≥ 18 − 4n₄ + Σ_{d≥7}(d − 12)n_d.** Each hub of degree d ≥ 13 forces about (d − 12)/6 extra degree-6 vertices.
- **(A3) [hand] No big vertices** (degrees 4, 5, 6 only).
  - Then n₅ = 12 − 2n₄ ≤ 12, and every off-φ 5-vertex lies in S1–S6.
  - The W-slack is then exact: every off-φ 5-vertex counts 1, so there are at least 9 − n₄ of them (this is just n₅ ≥ 9 − n₄ off φ).
  - For {5,6}-triangulations the full answer is **S1–S6 ∪ {H, HP}**: eight classes, all with entries ≤ 6.
- **(A4)** Structural reading of F1/F2 (from §5): when the free entry p is large, v lies in a long run of 5s around p, or p is ringed entirely by 5s. Belt-like hubs are the only source of unbounded entries.

## 4. Isolated fives (answer to (c))

Assume no two degree-5 vertices are adjacent (φ vertices included).

**Lemma I1 [hand].** Every link entry is 4, 6 or big. So each big neighbour has multiplier 2 and W(v) = 2 Σ τ(xᵢ). By Lemma W, at least 9 − n₄ off-φ 5-vertices satisfy

  **Σ_{u ∈ N(v)} (1 − 6/d(u))⁺ < 1/2,**

or have a degree-4 neighbour (D4). The non-D4 classes are exactly these **14, all with entries ≤ 11 (no free entry)**:
- (6,6,6,6,6);
- (p,6,6,6,6) for p = 7..11;
- {7,7}, {7,8}, {7,9} placed either adjacent or non-adjacent: 6 classes;
- (7,7,7,6,6) and (7,7,6,7,6).

Check: τ7 + τ9 = 0.476 < 0.5, τ7 + τ10 = 0.543, τ8 + τ8 = 0.5, 3τ7 = 0.429, 2τ7 + τ8 = 0.536.

**So in isolated-fives graphs R\* reduces to 14 bounded classes.** No unbounded neighbour is needed, and HP and the belt are irrelevant there.

**Lemma I2 [hand]. Degree-sequence constraint ("near-Goldberg").**
- Five-neighbours are pairwise non-consecutive on a ring. So a degree-6 vertex has ≤ 3 five-neighbours, a degree-d vertex ≤ ⌊d/2⌋, and a degree-4 vertex ≤ 2.
- Counting edges at the 5s: 5n₅ ≤ 2n₄ + 3n₆ + Σ_big ⌊d/2⌋ n_d. With n₅ = 12 − 2n₄ + Σ(d − 6)n_d this gives

  **n₆ ≥ 20 − 4n₄ + (1/3) Σ_{d≥7} (5d − 30 − ⌊d/2⌋) n_d** = 20 − 4n₄ + (2n₇ + 6n₈ + 11n₉ + 15n₁₀ + 20n₁₁ + …)/3.

- Equality forces every degree-6 vertex to have exactly 3 alternating five-neighbours, and every big vertex ⌊d/2⌋.
- For n₄ = 0 and no big vertices: n ≥ 32. This is attained by the pentakis dodecahedron (n₅ = 12, n₆ = 20), the dual of C₆₀.
- Every big vertex costs extra degree-6 vertices: at least 2/3 of one for a degree-7 vertex, and 2 for a degree-8 vertex.

## 5. A second rule (run-pooling), and what it says about the free shapes

**Rule W′ [hand].** Same tokens as Lemma W, but each maximal run R of L consecutive degree-5 vertices on the ring of w (R not the whole ring) pools its L tokens with the two outward halves of its bounding vertices: τ(w)(L + 1) in all, shared equally.
- Each member of R receives τ(w)(1 + 1/L) from w.
- If the whole ring of w is degree-5 vertices, each receives τ(w).

The total sent is still ≤ d·τ(w), so the analogue of Lemma W holds for W′(v) = Σ_w τ(w)(1 + 1/L_w(v)).

**Consequence [hand].** With exactly one big neighbour p, W′ < 1 iff either the whole ring of p consists of degree-5 vertices, or **p ≤ 6L + 5**, where L is the length of v's 5-run around p.

So an unbounded free entry arises only at a **5-ringed hub** (belt-like), or with p bounded by the 5-run length. W and W′ (and their mixtures) are each valid. Choosing between them trades the free shapes F1/F2 against the m = 1 classes; I have not optimised the mixture.

## 6. Recommendation for the R* front

1. The open case reduces to: S2–S6 (bounty: S5 = (5,5,5,6,6), S6 = (5,5,6,5,6)), S1 = (6⁵) (forced), the two free shapes F1/F2, and the bounded |B| ≥ 1 classes of §2 (max entry 41).
2. **F1/F2 are the natural next HP-style targets.** Like HP, the free vertex p is flanked by two 5s, so p never lies in an {a,b}-swap triple that also uses those flanking 5s.
3. For isolated-fives graphs, the 14 bounded classes of I1 suffice.
4. Not proved: minimality of the family, beyond (6⁵) and the unbounded entry being forced.

## 7. Route B: the discharging half (scope extension from the coordinator, 6 Oct)

Charge convention. The coordinator's ch = 6 − deg is −μ. Lemma W, read with ch, says the following: the 5-vertices send their surplus to big neighbours in the amounts W, and at least 9 − n₄ off-φ 5-vertices keep positive charge. Nothing else changes.

### 7.1 Configuration types (definitions)

All configurations are centred at a degree-5 vertex v. Each is a disc K ⊂ T with v interior. "Specified" vertices are interior to K, with their degrees given. "Free" vertices (marked *) lie on the ring, and their degree is not specified.

- **Full 2-ball** (README §1, r = 2): all five link vertices are specified. Ring length = Σdᵢ − 20.
- **One-star partial 2-ball (*, a, b, c, d)**: K is the union of the faces incident to v or to one of the four specified link vertices. The fifth link vertex p is free and lies on the ring.
  - The ring is p, then the outer neighbours of the specified link vertices, back to p.
  - Count [hand]: the ring is the free vertex plus the outer neighbours of the specified link vertices. Each specified xᵢ has dᵢ − 3 outer neighbours, and each consecutive pair of link vertices shares exactly one.
  - So the ring length is **a + b + c + d − 14**. Check: HP's (*,5,5,5,5) gives 6.
  - The vacancy game is defined for any disc with simple ring and v interior; the 1-ball of README §3 already has link vertices on the ring. So these configurations need no new theory, only a builder.
  - **This is exactly HP's shape.** HP's proof never reads a neighbour of p.
- **S-class partial 3-ball**: v with link in S1–S4, and each ring-2 vertex labelled 5, 6 or *.
  - Labelled vertices are specified (interior). * vertices (degree 4 or ≥ 7) lie on the ring.
  - Ring length [hand, layer formula]: L₃ = #* + Σ_{specified y ∈ ring 2}(d(y) − 2 − e_in(y)) − #(consecutive specified pairs in ring 2). Here e_in(y) ∈ {1, 2} is the number of link neighbours of y: 2 for a "corner" (third vertex of a face xᵢxᵢ₊₁y), 1 otherwise.
  - Example: pentakis' (6⁵) with ring 2 = (5,6)⁵ gives 5·1 + 5·3 − 10 = 10, matching README §3.
  - Maximum 15: (6⁵) with ring 2 all 6s.

### 7.2 Theorem U (candidate unavoidable set) [hand]

Every core (T, φ) contains, centred at a degree-5 vertex v ∉ φ, a configuration from:

| tier | configurations | status |
|---|---|---|
| U0 | a link vertex of degree 4 (D4) | proved |
| U1 | H (5⁵); HP (*,5,5,5,5) | proved, compiled/audited |
| U2 | full 2-balls (5,5,5,6,6), (5,5,6,5,6) | pass (vdred / vdred_joint; (5,5,6,5,6) not yet verified on a host) |
| **U3** | **57 one-star partial 2-balls**, rings 7–12 (list in 7.4) | **to check** |
| **U4** | S-class partial 3-balls: links (6⁵), (5,6,6,6,6), (5,5,6,6,6), (5,6,5,6,6); ring-2 labels in {5,6,*} | **to check; the bottleneck** |

**Proof.**
- By Lemma W there is a degree-5 v ∉ φ with W(v) < 1. In fact there are ≥ 9 − n₄ such vertices, but one suffices.
- If some link entry is 4: U0.
- Otherwise every entry is 5, 6 or big, and the big set B has |B| ≤ 3 (§2, |B| ≥ 4 impossible).

*|B| = 0.*
- If k ≥ 4: H or HP.
- The links in {5,6} with exactly two 6s are (5,5,5,6,6) and (5,5,6,5,6): U2.
- Otherwise the link is S1–S4, and labelling each ring-2 vertex by 5, 6 or * gives a U4 member. This is a tautological case split.

*|B| ≥ 1.*
- If k ≥ 4: HP.
- Otherwise free one **largest** big entry and specify the other four. I claim the resulting pattern is in the U3 list (7.4).
  - |B| = 1: the four specified entries are in {5,6}, not all 5. This gives 9 patterns.
  - |B| = 2: let s be the smaller big (specified) and q ≥ s the free one. Since τ(q) ≥ τ(s), W < 1 forces (μ_s + μ_q)·τ(s) < 1. Running the multipliers of §1 over the {5,6} entries gives exactly the bounds on s used in 7.4 (adjacent: s ≤ 8, and s = 7 if both flanks are 6; non-adjacent: s ≤ 11, 9, 8 or 7 as the number of flanking 6s grows).
  - |B| = 3: take the solution lists of §2 and free the largest entry. This gives the 14 patterns of 7.4.

∎

The proof is complete by hand, under one standing assumption, flagged next.

**Gap G1 (ring simplicity).** The configurations are well defined when the ring is a simple cycle. In the core, chords of the link are excluded (they would be separating triangles). But a **separating 4-cycle** v xᵢ y xⱼ (xᵢ, xⱼ non-consecutive) identifies ring vertices, and 4-connected triangulations may have one. Two ways to close this:
- (a) Have the Studio also check the finitely many ring-identified variants of each U-configuration (y equal to two outer positions).
- (b) A reduction lemma across separating 4-cycles. This is not available: the clique lift that handles triangles does not apply to 4-cycles.

I recommend (a).

### 7.3 Size, and estimate

- **Proved or passed tiers:** U0, U1, U2. That is 5 items.
- **U3:** 57 configurations, ring ≤ 12. Each is cheap (ring 11–12 runs in seconds to minutes even in Python, by README §4 item 5).
- **U4 as stated is large.** Burnside counts of label patterns:
  - (6⁵): 6,273, ring ≤ 15;
  - (5,6,6,6,6): 9,963, ring ≤ 13;
  - (5,5,6,6,6): 3,402, ring ≤ 11;
  - (5,6,5,6,6): 3,402, ring ≤ 11.
  - About **23,000 in all**. Of these, the {5,6}-only labellings number 136 + 272 + 144 + 144 = **696**.
- **Estimate of what is achievable.**
  - If the one-star partials pass, U3 stays at about 60.
  - U4 must then be cut by a second-level rule. A big vertex at distance 2 from an S-class vertex should pay it through the shared degree-6 neighbour; in Lemma W, the half-tokens that point at non-5 ring vertices are currently kept by w.
  - Such a rule should leave the 696 all-{5,6} 3-balls plus partial 3-balls with **at most one or two \*** labels.
  - **Realistic target: 100–1,000 configurations with rings ≤ 15.** This is conditional on the first U3/U4 results.
  - If configurations with \* in ring 2 tend to fail (as multi-star 2-balls likely would), U4 needs 4-balls and the count grows past 10⁴. **Run the first Studio batch before investing in the rule.**

### 7.4 Studio check list (U3, one-star partial 2-balls; * = free link vertex on the ring)

Notation: cyclic order x₀..x₄. Ring = sum of the four specified degrees − 14.

**A. One big, four in {5,6} (9 configurations).**

| pattern | ring | pattern | ring |
|---|---|---|---|
| (*,5,5,5,6) | 7 | (*,5,5,6,5) [F1] | 7 |
| (*,5,5,6,6) | 8 | (*,5,6,5,6) | 8 |
| (*,5,6,6,5) [F2] | 8 | (*,6,5,5,6) | 8 |
| (*,5,6,6,6) | 9 | (*,6,5,6,6) | 9 |
| (*,6,6,6,6) | 10 | | |

**B. Two bigs, adjacent: (s,*,a,b,c), with s specified next to *, a next to *, c next to s (14 configurations).**
- s = 7: all 8 choices of a, b, c ∈ {5,6}. Rings 8–11.
- s = 8: a, b, c ∈ {5,6} except a = c = 6 (6 choices). Rings 9–11.

**C. Two bigs, non-adjacent: (s,a,*,b,c), with a between s and *, b next to *, c next to s (20 configurations).**

| condition | s | number | rings |
|---|---|---|---|
| a = b = c = 5 | 7..11 | 5 | s + 1 = 8..12 |
| a = 5, exactly one of b, c = 6 | 7..9 | 6 | s + 2 = 9..11 |
| a = 5, b = c = 6 | 7, 8 | 2 | 10, 11 |
| a = 6, b = c = 5 | 7, 8 | 2 | 9, 10 |
| a = 6, exactly one of b, c = 6 | 7, 8 | 4 | 10, 11 |
| a = b = c = 6 | 7 | 1 | 11 |

**D. Three bigs (14 configurations).**
- (7,*,7,a,b), with {a,b} ⊂ {5,6} up to reflection: 3 configurations, rings 10–12.
- (*,7,7,b,5), with b ∈ {5,6}: 2 configurations, rings 10, 11.
- Split forms:
  - (7,7,5,*,5) ring 10;
  - (7,8,5,*,5) ring 11;
  - (7,*,5,7,5) ring 10;
  - (8,*,5,7,5) ring 11;
  - (7,*,5,8,5) ring 11;
  - (7,7,6,*,5) ring 11;
  - (*,7,6,7,5) ring 11;
  - (7,*,6,7,5) ring 11;
  - (7,7,6,*,6) ring 12.

(The D count is 3 + 2 + 9 = 14.)

**Fallback if a U3 member fails.** Replace it by the full 2-balls with the free entry specified up to the W-bound of §2. For example, (*,6,6,6,6) needs p ≤ 11 only, which is 5 full 2-balls with rings 10 + (p − 4) − … = Σd − 20 ≤ 15. The bounds keep every fallback ring ≤ 21 except the non-adjacent (7, ≤41) family. That family has no small fallback, so its one-star member (7,5,*,5,5) (ring 8) is the **critical test**.

**U4 first batch.**
- The 696 all-{5,6} S-class 3-balls; the largest rings are 15 at (6⁵).
- (6⁵) with ring 2 = (5,6)⁵ (pentakis) already passes, depth 7.
- Then the S-class partial 3-balls with exactly one * (ring ≤ 15).

Every U3/U4 member also needs its G1 variants.

### 7.4b The family "exactly two neighbours of degree ≥ 6, three of degree 5" (coordinator 6 Oct: radius-5 data)

The studiointel data, with the audit's replay pending, give radius 5 at (5,7,6,5,5), (5,8,6,5,5) and (5,6,5,5,8). In my notation:
- (5,7,6,5,5) and (5,8,6,5,5) are **6 adjacent to the big**: (p,6,5,5,5) with p = 7, 8.
- (5,6,5,5,8) is **F1**: rotated it is (8,5,6,5,5). The big's two link-flanks are 5s and the 6 is non-adjacent to it.

So all three sit in rows (a) and (b) below. The family splits by positions and by 6 versus ≥ 7. The W-bounds come from §2; above them the vertex has W ≥ 1, so it is never the one Lemma W returns. Ring = Σd − 20 for full 2-balls.

| row | shape (positions) | full 2-ball sequences to check | count | rings | one-star cover (U3) |
|---|---|---|---|---|---|
| (o) | 6,6 adjacent / non-adjacent | (5,5,5,6,6), (5,5,6,5,6) | 2 | 7, 7 | already pass (U2) |
| (a) | 6 and big p **adjacent** | (5,5,5,6,p), 7 ≤ p ≤ 17 | 11 | p + 1 = 8..18 | (*,5,5,5,6), ring 7 |
| (b) | 6 and big p **non-adjacent** (F1) | (p,5,5,6,5): **no W-bound**, p arbitrary | ∞ | p + 1 | (*,5,5,6,5), ring 7: **essential** |
| (c) | two bigs **adjacent** | (5,5,5,p,q) with {p,q} ∈ {7}×{7..12} ∪ {8}×{8..10} | 9 | p + q − 5 = 9..13 | (7,*,5,5,5) ring 8; (8,*,5,5,5) ring 9 |
| (d) | two bigs **non-adjacent** | (p,5,q,5,5), p ≤ q: (7, 7..41), (8, 8..23), (9, 9..17), (10, 10..14), (11, 11..13) | 68 | p + q − 5 = 9..43 | (s,5,*,5,5), s = 7..11, rings 8..12 |

Reading for the Studio:
1. **Row (b) cannot be closed by finitely many full 2-balls.** The F1 one-star configuration (*,5,5,6,5) (ring 7) must pass, or a hand lemma in the style of HP is needed for it. Rule W′ (§5) gives only p ≤ 6L + 5, with L ≥ 3 the length of v's 5-run around p, unless p is ringed entirely by 5s.
   - Since radius 5 already occurs at p = 8 in this row, it is the **highest-priority check**.
2. Row (d)'s tail (rings up to 43) is likewise feasible only through its one-star members (s,5,*,5,5).
3. Rows (a) and (c) are finite: 20 full 2-balls with rings ≤ 18. Their one-star covers, three configurations with rings 7–9, would replace all 20 if they pass.
4. Expected depth. The real radius-5 states lie in rows (a) and (b), so the game depth there is ≥ 5. The game depth is ≥ the real radius, as at T4 (7 versus 4).

### 7.5 How the earlier findings feed in

- (A2)/(A3) say where U4 bites: graphs without H/HP and without big vertices are exactly the {5,6} case, so U4 ∩ {5,6} is unavoidable there.
- Lemma I1 (isolated fives) says: in isolated-fives graphs, only the S1 part of U4 and the U3 rows with all specified entries 6 (A: (*,6,6,6,6); B: (7,*,6,6,6); C: (s,6,*,6,6), …) can occur.

## Ledger

- [hand] Lemma W, Corollary R-list, (A2), (A3), Lemmas I1 and I2, rule W′.
- [hand] Theorem U (§7.2), the ring-length formulas (§7.1), and the U3 list of 57 and the U4 counts (§7.3–7.4). These are conditional on G1 (simple rings) and on the Studio checks.
- [data, not mine] Radius-5 classes (§7.4b), from studiointel; the audit's replay is pending.
- [hand, lower bound] (6⁵) forced (pentakis, GC(2,0)); unbounded entry forced (belt).
- [open] Forcedness of the other listed classes, and the optimal rule mixture.
- [literature, not reconstructed, nothing depends on it] Lebesgue (1940) gives a similar list of 5-star types. My single-big and non-adjacent-pair bounds (e.g. 7 & ≤41, 8 & ≤23, 9 & ≤17, 10 & ≤14, 11 & ≤13; (6,6,6,6,≤11)) coincide with the entries of that type I recall.

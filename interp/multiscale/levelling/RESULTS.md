# Levelling cluster boundaries: a definition, exact tests, the torus, and a conjecture

22 Oct 2026. This follows `../seam_lemma.md`, `../tilt_aware.md` and `../spin_windows/RESULTS.md`. Everything here is in this folder. `lev.py` is the library. Each experiment has a script `eN_*.py` that writes `eN_*.jsonl`; per-merge logs of the full recursions are in `e4_logs/`.

Labels:
- **[P]** proved here, with the argument given.
- **[M]** measured. SAT (CaDiCaL / Glucose via python-sat) is the ground truth.
- **[C]** conjecture or interpretation.

Notation follows `seam_lemma.md` §1:
- colours are in Z2^2;
- an edge uv carries the label c(u)+c(v), and labels 1, 2, 3 map to the unit vectors e_g, e_h, e_{g+h};
- h is the Kondev–Henley height.

Heights are stored in half-lattice units.

---

## 0. Verdict in brief

1. **Definition (Q1).** A cluster C is a near-triangulated disc. "Level" is a property of the boundary colour word only.
   - Put every branch cut inside C, pairing up the interior odd vertices. If their number is odd, exactly one cut leaves through the boundary.
   - The height read along ∂C is then a well-defined walk H: the *boundary gauge*, §1.2.
   - That walk is a closed curve in the orbifold R²/⟨ρ(∂C)⟩. Here ρ(∂C) is the boundary monodromy:
     - a point reflection when C holds an odd number of vortices, so the orbifold is a cone;
     - a translation t when the number is even, so the orbifold is a cylinder.
   - **τ(C,c)** is the distance the boundary curve strays from the core of that orbifold: the cone point, or the best centre. C is **K-level** if τ ≤ K.
   - [P] τ does not depend on how the cuts are routed. [P] The reflection centre of a vortex o is its own height h(o).
   - [P] **(i) holds:** two K-level boundaries meeting along a seam have height mismatch at most 4K under every renaming.
   - [M] In all 6,517 merges of level clusters measured here, bounded repair worked with R ≤ 2. In all but 2 of them it worked with R ≤ 1.
2. **Existence (Q2).** Levelling holds exactly and uniformly for *chordless* clusters (clusters whose boundary cycle is induced):
   - [M] **Every chordless cluster tested (300: balls of radius 3–14, up to n = 943, plus strips and necklaces) has min τ ∈ {√3/2, 1}.**
   - [M] The rule is exact in all 216 balls where it was checked: min τ = √3/2 iff the vortex count is even and Σ s_i ≡ 0 (mod 3). The strips and necklaces also have min τ ∈ {√3/2, 1}, but the rule was not checked on them.
   - [M] The number and arrangement of vortices make **no difference**:
     - 0 vortices (dome balls far from the degree-5 vertices) and 1 vortex (a cone) behave exactly like 564 vortices (random maps);
     - so does a vortex at depth 1 against one at depth 8, and so do long strips;
     - "too few vortices near a long boundary" does *not* break levelness of a single cluster.
   - **Failure mode:** boundary *chords*. A chord pinches the disc into pockets. [M] Clusters with chords reach min τ = 1.32 or √3 (16 found). Every re-levelling failure in the recursions was on a cluster with 9–55 chords.
3. **But levelness is not preserved by merging.** [M] Gluing two 1-level discs and repairing locally gives τ(A∪B) up to 4. [P] The far boundary arcs are fixed, so no repair confined near the conflicts can bring τ back down. Merging alone produces 1-level results in only 42 of 107 cases (E3).
   - The fix is a **re-levelling step**: recolour a collar of width w along ∂(A∪B).
   - [M] w ≤ 4 sufficed whenever the merged cluster was levelable. Every merge where it was not came from a cluster with chords.
   - With "merge (R) + re-level (w)", complete recursions colour domes of up to n = 9,002 (and random/binder maps of n = 4,842, partial runs). They keep R ≤ 1 at every merge and final R ≤ 2, **for both balanced and maximally lopsided hierarchies**.
   - The plain recursion (level leaves, no re-levelling) lets τ grow to 14. In lopsided mode it needs R up to 4 and final R up to 8 at n = 1,962, and R up to 9 at n = 4,002.
4. **Torus (Q3).** [P] One-line lemma: wherever the height is single-valued, f∘h with f(a e_g + b e_h) = a+b mod 3 is a proper 3-colouring.
   - [P] Hence a 6-regular torus has a zero-period ("globally level") 4-colouring iff it is 3-colourable.
   - [M] Every one of the 168 non-3-colourable 4-colourable tori tested (61 small ones, n ≤ 19; 107 fat ones with edge-width 4–12, n ≤ 144) forces a nonzero height period around a handle. On fat tori this is exactly one quantum, |t| = 2; thin tori force up to about 10. There are no vortices anywhere to absorb it.
   - 278 of the 2,495 tori with n ≤ 60 are not 4-colourable.
   - All their disc clusters are nevertheless perfectly level, and disc merges cost R = 0. The failure sits at the merge whose seam is disconnected (it closes a handle). There the two seam arcs see heights differing by a topologically forced period that no renaming and no vortex can remove.
   - [P] On the sphere, Jordan's theorem makes every disc+disc→disc seam a single arc and the final seam contractible, so all monodromy comes from enclosed vortices. **This is where planarity enters.**
5. **Conjecture (Q4).** The cleanest statement is the "level merge + collar re-level + closing" conjecture of §5, over hierarchies of chordless discs.
   - [P] Together with the recursion it implies the 4CT.
   - [C] For bounded maximum degree it reduces to finitely many finite-automaton checks along 1-dimensional bands. This is decidable in principle and astronomically large in practice.
   - Two parts are not finite checks: the existence of chordless hierarchies, and unbounded degree.
   - Lopsided merges stop being dangerous once the invariant is maintained.

---

## 1. Q1: what "level" means when the cluster contains vortices

### 1.1 Vortices are point reflections centred at their own height [P]

Take a near-triangulated disc C. Label the triangles σ = up/down so that the bad edges (equal labels on both sides) form a T-join J for T, the interior odd-degree vertices. Integrate the increments σ(face(u→w))·e_label on C∖J. This gives `seam_lemma` §1 locally.

- **Going once around an odd vertex o reflects the height through h(o).**
  - Proof: compute h(o) from each consecutive triangle of its fan. Triangle closure makes all these values agree, so h(o) is the same on both sheets.
  - The sheets differ by h ↦ −h + 2p, because every increment changes sign.
  - So p = h(o).
- **Around a set S of vortices** the monodromy is the ordered product of the reflections r_o: h ↦ −h + 2h(o), with the vortex heights transported along the loop.
  - For |S| even it is a translation, 2Σ±h(o_i), an alternating sum.
  - For |S| odd it is a reflection.
  - Every monodromy lies in 2Λ ⋊ {±1}. Translations lie in 2Λ, because Σ labels = 0 in Z2^2 forces Σ e_label ∈ 2Λ.
- Lipschitz: |h(o) − h(o′)| ≤ d(o,o′). So a pair of vortices is a dislocation with Burgers vector of length at most 2d. This is the mechanism `tilt_aware.md` §3.1 described, now with the centre identified.

### 1.2 Boundary gauge, the walk H, and τ [P]

- Walk ∂C as b_0 … b_{m−1} with the interior on the left. Let k(b) be the number of interior edges at b, so the fan at b has k(b)+1 triangles.
- Choose all cuts inside C, plus one exit at b_0 if |T| is odd. Then σ on the boundary triangles is forced: **s_{i+1} = s_i·(−1)^{k(b_{i+1})}**, and the boundary walk is H_{i+1} = H_i + s_i e_{label(b_i b_{i+1})}.
- [P] Closing parity: s_m ≠ s_0 iff |T| is odd. Proof: Σ_{b∈∂} k(b) ≡ #(∂–interior edges) ≡ Σ_{v interior} deg v ≡ |T| (mod 2).
  - The code asserts this on every cluster it builds: 0 failures in thousands.
- [P] **Gauge independence.** H depends only on the boundary colour word and the fan parities. Rerouting interior cuts changes nothing on ∂C.
  - Odd |T|: the doubled walk is centrally symmetric about q = (H_0 + H_m)/2, which is the centre of the boundary reflection. Define **τ = max_i |H_i − q|**. This does not depend on b_0.
  - Even |T|: H_m − H_0 = t is the translation monodromy. Define **τ = min over half-lattice centres p of max_i |H_i − p|**, a one-lap circumradius. It depends on b_0 by at most |t|, and is ≥ |t|/2.
- Geometrically, ∂C is a closed curve in R²/⟨ρ(∂C)⟩: a cone of angle π, or a cylinder. τ measures how far that curve gets from the cone point or axis. **"Tilt measured modulo the reflection group" is literally this quotient.** C is K-level if τ ≤ K.
- Benchmarks:
  - A 3-colouring is perfectly flat (F1). Its boundary takes 3 heights, so τ = √3/2 with half-lattice centres.
  - [P] τ < √3/2 is impossible for any walk that uses all three labels.
  - The maximally tilted c22 strip has τ ≈ m/4.

Because τ depends only on c|∂C and the degrees, levelness is a *1-dimensional, finite-state* property of the boundary word. This matters for §5.

### 1.3 (i): two level boundaries glue with bounded mismatch [P], bounded repair [M]

- [P] If A and B are disjoint discs and A∪B is a disc, the seam is a single arc (Jordan).
- [P] If both are K-level, then for every renaming π the seam mismatch is at most 4K. Here mismatch is the diameter over the seam of H_A − H_{πB}, as in `tilt_aware.md` §2.
  - Proof: H_A on the seam lies in a K-ball. The image of B's walk under a renaming, which is a D3 isometry plus translation, lies in another K-ball. So the difference stays in a 2K-ball.
  - Family (T), the tilt counterexample, is therefore excluded by construction.
- [C] Combined with the matched-tilt conjecture of `tilt_aware.md` (R = O(M_band)+c), this gives bounded R.
- [M] In practice (E3, E3b, E4: 6,517 merges with level inputs), the plain repair radius was R ≤ 1 in all but 2 merges and R ≤ 2 always. This held for balanced splits, for lopsided ones (B of 4–15 vertices against A of up to 8,991), and on domes, random min-degree-5 maps and binder maps.

### 1.4 Levelness is not closed under merging: the re-levelling step

- [P] With no re-levelling, τ(A∪B) ≤ 2K + O(1) + O(R).
  - Proof: the A-arc stays within K of p_A and the B-arc within K of p_B. A conflict-free seam edge pins |p_A − p_B| ≤ 2K + 1.
  - Iterated without correction, K → 2K + O(1) per level, which grows geometrically.
- [P] A repair confined to the R-neighbourhood of the conflicts cannot fix this, because the far parts of both arcs are fixed.
- [M] E3 (107 merges; nU = 87–426; K = 1 inputs): τ after plain repair has mean 1.78 and maximum 3.61. Requiring τ(A∪B) ≤ 1 with recolouring only near the conflicts succeeds within R ≤ 8 in only 91 of 107 merges, and at R = 0 in 42.
- **Re-levelling**: after the merge, recolour every vertex within distance w of ∂(A∪B), together with the repair zone, so that τ ≤ 1 again. The deep interior stays fixed.
  - [P] Lipschitz bounds force w ≥ τ_before − τ_after − O(1).
  - [P] Re-levelling cannot change the boundary monodromy unless the collar contains vortices. So in an Eulerian collar, |t(A∪B)| ≤ 2 must already hold after the merge.
- [M] E3b (92 merges; nU = 81–635, depth up to 11): **w ≤ 3 in all 92.** The distribution was w = 0: 39, 1: 18, 2: 31, 3: 4. Re-levelling sometimes changed t (e.g. 3.46 → 0) when the collar held vortices.

---

## 2. Q2: exact minimum boundary tilt

### 2.1 Encoding

- `lev.sat_level(cl, K²)` is a CNF for "a proper 4-colouring of the cluster whose boundary walk stays within distance K of a centre".
  - Odd case: the centre is pinned at the reflection centre, H_m = −H_0.
  - Even case: the centre is any half-lattice point.
  - Walk positions are one-hot over half-lattice points of norm ≤ K. Transitions are driven by the boundary labels.
- `min_tau` bisects over the possible norms.
- When a budgeted call returned UNKNOWN, the value was confirmed by unbudgeted direct calls at K² = 1 and K² = 3/4 (`e1b.py`). After that, all 192 E1 values are exact.

### 2.2 Balls (E1, E1c) [M]

Table (E1, `e1_survey.jsonl`): balls B_r(v), r = 3..8, centres at degree-5 vertices, at the point farthest from all vortices, at random vertices, and at distance 2 from a vortex.

| family | clusters | n | m (boundary) | interior odd | min τ = √3/2 | min τ = 1 | min τ > 1 | τ of a random SAT colouring (median, max) |
|---|---|---|---|---|---|---|---|---|
| dome f=5 | 30 | 31-172 | 15-30 | 0-8 | 4 | 26 | 0 | 2.78, 5.00 |
| dome f=7 | 30 | 31-195 | 15-38 | 0-6 | 5 | 25 | 0 | 3.06, 5.00 |
| dome f=10 | 30 | 31-211 | 15-44 | 0-2 | 8 | 22 | 0 | 2.89, 5.29 |
| dome f=14 | 30 | 31-217 | 15-48 | 0-1 | 12 | 18 | 0 | 2.65, 6.24 |
| BASE_rand22 (random, deg 5–8) | 18 | 40-317 | 21-60 | 12-164 | 4 | 14 | 0 | 3.80, 5.57 |
| M3_ico22_hard (binder) | 18 | 33-289 | 17-67 | 9-128 | 2 | 16 | 0 | 3.48, 7.00 |
| M5_ico31 (binder) | 18 | 37-285 | 19-61 | 11-148 | 0 | 18 | 0 | 3.80, 6.00 |
| BASE_defect_ico17 | 18 | 34-275 | 17-63 | 9-120 | 3 | 15 | 0 | 3.61, 7.00 |

- E1c (`e1c_big.jsonl`): 24 balls of radius 10–14 in ico20, ico30, BASE_rand22 and M5. They have n = 276–943, m up to 117, and up to 564 vortices. **τ ≤ 1 in 24/24**, and the √3/2 rule held in 24/24. Each SAT call took under 0.5 s.
- **The rule [M, 216/216].** min τ = √3/2 iff (|T| even and Σ s_i ≡ 0 mod 3); otherwise min τ = 1.
  - [P] Every Eulerian ball satisfies the rule's condition: its 3-colouring closes up. All 25 Eulerian balls had √3/2.
  - [M] Exhaustively over sign patterns, for m ≤ 11 (`words.py`, `words_out.txt`): for every gauge pattern s and either parity there is a proper boundary word using exactly 3 colours with τ ≤ 1, and τ ≤ √3/2 exactly under the rule. So the boundary word alone never forces tilt above 1. The interior never forced it either, in any chordless cluster.
- **Arrangement of vortices [M].** No effect at all. Counts of (number of vortices, depth of the shallowest vortex, min τ) among clusters with ≤ 4 vortices: (1, depth 1..8) → 1 in all 57; (2, depth 1–2) → 1; (3, depth 1–3) → 1; (4, depth 1) → √3/2 or 1, per the rule. A vortex adjacent to the boundary is harmless, and so is a single vortex at the centre of a radius-8 dome cap (the cone).
- Random colourings have τ of 3–7 and grow with m, consistent with `tilt_aware`. Levelness is a real constraint, but one that is always satisfiable.

### 2.3 Thin clusters and chords (E2, E2b, recursion failures) [M]

- **Strips** (`e2_strips.jsonl`): width-1 and width-2 neighbourhoods of geodesics of length 10–40, so depth 1–3 and boundary up to 143. All 67 chordless strips have τ ∈ {√3/2, 1}, as do the 4 with chords. **Thinness alone is harmless.**
- **Necklaces** (`e2b_neck.jsonl`): radius-2 balls strung along a geodesic so that they touch at narrow necks. These give boundary chords. Of 31 built, the 14 with chords have τ = √3/2 (3), 1 (10), and **√3 (1)**: BASE_rand22, n = 148, m = 88, 4 chords, 37 vortices.
- **Clusters on which re-levelling failed in the recursions** (`fails.jsonl`): every one has chords. The values below are exact minima from the ascending ladder of thresholds (no unknown results):

| from | n | m | depth | vortices | chords | min τ |
|---|---|---|---|---|---|---|
| ico10 balanced | 155 | 73 | 3 | 3 | 13 | **√3** |
| ico14 balanced | 249 | 121 | 3 | 2 | 22 | 1.32 |
| ico14 lopsided giant (7 cases) | 697–1673 | 219–376 | 5–12 | 4–10 | 9–25 | 1.32 (5), √3 (2) |
| ico20 balanced (5) | 436–952 | 200–201 | 4–10 | 2–3 | 10–25 | 1.32 (4), √3 (1) |
| ico20 lopsided giant | 2620 | 630 | 10 | 11 | 53 | > 1 (exact value unresolved within budget) |



- **Cutting along the chords cures it [M].** Each of the 19 failing clusters was cut along all its chords (`chordsplit.py`, `chordsplit.jsonl`). That gave 431 chordless pieces, from single triangles up to large discs, and **every piece is 1-level.** The obstruction is purely the coupling of individually level pockets through chords.
- **Why chords matter [P/C].** A chord xy splits C into pockets C_1 and C_2 that share one edge.
  - [P] The boundary walk of C is the concatenation of the two pocket walks with the chord removed. So each pocket's monodromy (a translation t_i, or a reflection) is inserted into C's walk.
  - [P] The heights at x and y are pinned within distance 1 of each other through the chord. That leaves the two pocket centres free to differ by up to about 2.
  - [C] A chain of pockets is effectively a merge already performed without any re-levelling. This explains τ = 1.32–1.73.
  - [C] We did not find τ > √3. Whether τ stays bounded on long necklaces is open: the long necklaces failed to be discs, so the sample is small.

**Answer to Q2 [M/C].** Bounded: min τ ≤ 1 for every chordless cluster tested, independent of size (up to 943 vertices), of the number of vortices (0 to 564), and of their arrangement. It fails, mildly, for clusters with boundary chords: min τ up to √3 observed.

---

## 3. Merges, re-levelling and complete recursions (E3, E3b, E4) [M]

`e4_recursion.py` runs the following:
- leaves are Voronoi cells (radius about 2, fixed to be discs), each given a 1-level colouring;
- merges are disc+disc→disc. **bal**: greedy matching rounds of the smallest adjacent pairs. **lop**: one giant cluster absorbs its neighbours one by one, the worst case for `tilt_aware`;
- each merge does a renaming plus minimum-R repair near the conflicts, then (variant `level`) a re-level of a collar of minimum width w back to τ ≤ 1;
- `+chordless` prefers merges whose union has no chords;
- a merge whose union cannot be re-levelled is skipped, and the hierarchy picks another pair. These are the "skips" below;
- the final merge (two discs covering the sphere) uses only repair, R from the conflicts;
- `plain` has level leaves and no re-levelling. `nolevel` has random leaves and no re-levelling.

| map (n) | mode | variant | merges logged | R histogram | max R | final R [sizes] | w histogram | max τ before re-level | re-level skips |
|---|---|---|---|---|---|---|---|---|---|
| BASE_rand22 s0 (4842) | bal | level+chordless | 390 (partial) | {0: 352, 1: 38} | 1 | (stopped) | {0: 122, 1: 178, 2: 72, 3: 18} | 4.58 | ? |
| BASE_rand22 s0 (4842) | lop | level | 182 (partial) | {0: 169, 1: 13} | 1 | (stopped) | {0: 57, 1: 42, 2: 72, 3: 11} | 4.00 | ? |
| M3_ico22_hard s0 (4842) | lop | level | 65 (partial) | {0: 63, 1: 2} | 1 | (stopped) | {0: 13, 1: 24, 2: 27, 3: 1} | 3.00 | ? |
| ico14 s0 (1962) | bal | level | 188 | {0: 184, 1: 4} | 1 | 2 [1202, 760] | {0: 153, 1: 27, 2: 6, 3: 2} | 2.65 | 0 |
| ico14 s1 (1962) | bal | level | 176 | {0: 171, 1: 5} | 1 | 1 [1072, 890] | {0: 142, 1: 25, 2: 4, 3: 4, 4: 1} | 2.65 | 1 |
| ico14 s0 (1962) | bal | level+chordless | 188 | {0: 185, 1: 3} | 1 | 0 [1902, 60] | {0: 159, 1: 20, 2: 7, 3: 2} | 2.65 | 0 |
| ico14 s1 (1962) | bal | level+chordless | 176 | {0: 175, 1: 1} | 1 | 1 [1775, 187] | {0: 154, 1: 15, 2: 6, 3: 1} | 3.00 | 0 |
| ico14 s0 (1962) | bal | levelS | 188 | {0: 181, 1: 6, 2: 1} | 2 | 2 [1202, 760] | {0: 169, 1: 16, 2: 2, 3: 1} | 4.50 | 0 |
| ico14 s0 (1962) | bal | plain | 188 | {0: 177, 1: 10, 2: 1} | 2 | 2 [1202, 760] | - | 5.57 | 0 |
| ico14 s1 (1962) | bal | plain | 176 | {0: 161, 1: 14, 2: 1} | 2 | 3 [1074, 888] | - | 5.20 | 0 |
| ico14 s0 (1962) | lop | level | 188 | {0: 187, 1: 1} | 1 | 0 [1949, 13] | {0: 171, 1: 12, 2: 4, 3: 1} | 2.65 | 2 |
| ico14 s1 (1962) | lop | level | 176 | {0: 175, 1: 1} | 1 | 0 [1954, 8] | {0: 149, 1: 19, 2: 7, 3: 1} | 2.65 | 0 |
| ico14 s0 (1962) | lop | level+chordless | 188 | {0: 187, 1: 1} | 1 | 0 [1955, 7] | {0: 164, 1: 18, 2: 6} | 3.00 | 7 |
| ico14 s1 (1962) | lop | level+chordless | 176 | {0: 175, 1: 1} | 1 | 0 [1954, 8] | {0: 149, 1: 19, 2: 7, 3: 1} | 2.65 | 0 |
| ico14 s0 (1962) | lop | plain | 188 | {0: 158, 1: 23, 2: 3, 3: 4} | 3 | 5 [1949, 13] | - | 7.21 | 0 |
| ico14 s1 (1962) | lop | plain | 176 | {0: 149, 1: 18, 2: 2, 3: 5, 4: 2} | 4 | 8 [1954, 8] | - | 10.54 | 0 |
| ico20 s0 (4002) | bal | level | 376 | {0: 370, 1: 6} | 1 | 2 [1535, 2467] | {0: 334, 1: 31, 2: 6, 3: 5} | 3.00 | 0 |
| ico20 s1 (4002) | bal | level | 381 | {0: 376, 1: 5} | 1 | 2 [1671, 2331] | {0: 322, 1: 50, 2: 6, 3: 3} | 2.65 | 4 |
| ico20 s0 (4002) | bal | level+chordless | 376 | {0: 370, 1: 6} | 1 | 1 [2412, 1590] | {0: 330, 1: 36, 2: 6, 3: 4} | 2.65 | 1 |
| ico20 s1 (4002) | bal | level+chordless | 381 | {0: 376, 1: 5} | 1 | 2 [2666, 1336] | {0: 332, 1: 39, 2: 6, 3: 3, 4: 1} | 2.65 | 0 |
| ico20 s0 (4002) | bal | nolevel | 376 | {0: 333, 1: 39, 2: 3, 3: 1} | 3 | 4 [1748, 2254] | - | 11.53 | 0 |
| ico20 s0 (4002) | bal | plain | 376 | {0: 355, 1: 19, 2: 2} | 2 | 5 [1535, 2467] | - | 7.21 | 0 |
| ico20 s1 (4002) | bal | plain | 381 | {0: 360, 1: 19, 2: 2} | 2 | 3 [1841, 2161] | - | 7.81 | 0 |
| ico20 s0 (4002) | lop | level | 376 | {0: 375, 1: 1} | 1 | 0 [3994, 8] | {0: 341, 1: 28, 2: 4, 3: 3} | 3.00 | 3 |
| ico20 s1 (4002) | lop | level | 91 (partial) | {0: 91} | 0 | (stopped) | {0: 80, 1: 10, 2: 1} | 2.65 | ? |
| ico20 s0 (4002) | lop | level+chordless | 376 | {0: 375, 1: 1} | 1 | 0 [3994, 8] | {0: 341, 1: 28, 2: 4, 3: 3} | 3.00 | 3 |
| ico20 s1 (4002) | lop | level+chordless | 122 (partial) | {0: 122} | 0 | (stopped) | {0: 100, 1: 20, 2: 2} | 2.65 | ? |
| ico20 s0 (4002) | lop | plain | 376 (partial) | {0: 320, 1: 31, 2: 10, 3: 7, 4: 3, 5: 1, 6: 2, 7: 1, 9: 1} | 9 | (stopped) | - | 13.75 | ? |
| ico30 s0 (9002) | bal | level | 868 | {0: 858, 1: 10} | 1 | 2 [3818, 5184] | {0: 754, 1: 105, 2: 9} | 2.29 | 0 |
| ico30 s0 (9002) | bal | nolevel | 868 | {0: 781, 1: 76, 2: 10, 3: 1} | 3 | 4 [5568, 3434] | - | 11.53 | 0 |
| ico30 s0 (9002) | bal | plain | 868 | {0: 824, 1: 38, 2: 6} | 2 | 4 [3818, 5184] | - | 10.82 | 0 |
| ico30 s0 (9002) | lop | level | 868 | {0: 868} | 0 | 1 [11, 8991] | {0: 801, 1: 67} | 3.61 | 0 |
| ico30 s0 (9002) | lop | plain | 780 (partial) | {0: 674, 1: 90, 2: 11, 3: 5} | 3 | (stopped) | - | 12.49 | ? |

Notes on the table:
- "partial" means the run was stopped for time, in some cases while still in its final full-sphere repair (ico20 lopsided plain spent more than 40 minutes there). Its per-merge statistics are still valid. `python3 summ4logs.py` regenerates the table.
- `levelS` re-levels only to τ ≤ √3.

**Reading [M].**
- **With re-levelling, every merge in every run needed R ≤ 1.** That is 6,517 merges with level inputs across E3, E3b and E4; R ≤ 1 in all but 2, and those 2 are R = 2 in the looser `levelS` variant. The final closing merge needed R ≤ 2. Re-levelling needed w ≤ 4.
  - This holds for **balanced and for maximally lopsided hierarchies alike**, from domes with 12 vortices in 9,002 vertices to random and binder maps with about 1,600 vortices.
  - ico30 lopsided: a giant of up to 8,991 vertices absorbs 868 cells; every one of the 868 merges has R = 0, w ≤ 1, and the final merge has R = 1.
- **Without re-levelling** (`plain`: level leaves only; `nolevel`: random leaves), τ grows to 10–14 and R grows with it:
  - lopsided: R up to 4 (ico14) and up to **9** (ico20, in the last merges of the giant), and final R up to 8;
  - balanced: final R 3–5.
  - This reproduces the `tilt_aware.md` lopsided failure at a smaller scale.
- **Re-level skips** (21 merges in all) happened only when the union had chords: 9–55 of them, min τ 1.32 or √3 (§2.3). The hierarchy then chose another pair and always completed.
- With the chordless preference, the greedy hierarchy still sometimes had to accept chorded unions (up to 66 chords), because no chordless pair was available.

---

## 4. Q3: the torus, and where planarity enters

**A one-line lemma [P].** Define f: Λ → Z3 by f(a·e_g + b·e_h) = a + b (mod 3). Then f(e_g) = f(e_h) = f(e_{g+h}) = 1.

- Along every edge, f∘h changes by the orientation sign ±1, which is never 0.
- **So wherever the height of a 4-colouring is single-valued (no vortices and trivial periods), f∘h is a proper 3-colouring.**
- For a loop γ around which h has period t_γ, the 3-colouring f∘h comes back shifted by f(t_γ) (mod 3).
- Consequences:
  - Any 4-colouring of an Eulerian disc gives a 3-colouring in this way. So, given the 4CT, Heawood's disc theorem follows in one line.
  - On a 6-regular torus (lattice quotient), f(t_γ) must equal the Z3 colour holonomy of the lattice along γ, which is a property of the geometry alone. **A 6-regular torus has a 4-colouring with zero height periods iff it is 3-colourable.** If it is not 3-colourable, *every* 4-colouring has a period with |t| ≥ 2 around some handle.
  - The same mechanism appears inside a planar cluster with two vortices. [M] In all 12 dome caps with exactly two degree-5 vertices (spacing 5–10), t = 0 is impossible and |t| = 2 is forced. With four vortices, t = 0 is attainable (`tforced.py`).

**Data** (`e5_torus.py`, `e5b_periods.py`, `e5c_growth.py`). T(p,q,r) is the triangular lattice modulo ⟨(p,0),(r,q)⟩: 6-regular, with 2,495 simple parametrisations for n = pq ≤ 60, not reduced up to isomorphism.

| | count / value |
|---|---|
| 3-colourable | 281 |
| 4-colourable, not 3-colourable | 1,936 |
| **not 4-colourable** | **278** (K7 = T(7,1,2), …). By edge-width: 3: 236, 4: 16, 5: 18, 6: 2, 7: 6. None with edge-width ≥ 4 above n = 37; the larger ones (up to n = 59) all have edge-width 3 |
| zero-period 4-colouring exists | 3-colourable: 17/17. Not 3-colourable: **0/61** (n ≤ 19, all) and **0/107** (square and rectangular tori, edge-width 4–12, n ≤ 144) |
| forced minimum of max(\|t_1\|², \|t_2\|²) on the two basis loops | **= 4 (one quantum, \|t\| = 2)** for 105 of the 107 fat tori, and 16 for the other 2. Thin tori (q ≤ 2, one very short loop) force 16 to about 100 along the long loop, i.e. \|t\| up to about 10 around a loop of length ≤ 16 |

**What goes wrong with levelling on a torus:**

- **[P] There are no vortices to absorb tilt, but there is a topological flux.** A 6-regular torus has no odd vertices. Every disc cluster is Eulerian and therefore perfectly level: 3-colourable, τ = √3/2, and disc-into-disc merges cost R = 0 (F2).
  - The non-3-colourable ones nevertheless force a height period t ≠ 0 around a handle in *every* 4-colouring. This is the Z3 holonomy, read through f.
  - On the sphere every loop is contractible, so its monodromy is the product of the reflections at the vortices it encloses. All flux is attached to vortices, which are local objects that the level invariant controls.
  - On the torus the period of a non-contractible loop encloses nothing. No renaming removes it (renamings act on h by D3 isometries, which preserve \|t\|), and no repair confined to vortex neighbourhoods can remove it either.
- **[P] Where the levelling recursion breaks.** On a torus, the hierarchy must at some merge join two pieces whose seam is *disconnected*: two arcs whose union with paths through A and B is a non-contractible loop γ. Equivalently, the final seam is not contractible.
  - Even if A and B are both level, the heights on the two arcs differ by the forced period t_γ. So the closing repair must absorb a mismatch M = \|t_γ\| along a seam band.
  - On fat tori M = 2. By the matched-tilt data (R ≈ 0.45·M), this is cheap, consistent with these tori being 4-colourable.
  - On thin tori the forced flux per unit length of the handle is large: up to about 10 over a circumference of 15. In 278 of them no colouring exists at all.
  - This is the (T) family of `seam_lemma.md` with the tilt *imposed by topology* instead of by an adversary.
- **[P] On the sphere this cannot happen.** By Jordan, a disc+disc→disc merge has a *connected* seam, so one renaming suffices. The final seam bounds a disc on each side, so its mismatch is generated entirely by enclosed vortices, which the level invariant bounds through τ ≤ K on both sides (§1.3).
- **[C] The planarity ingredient a proof must use is simple connectivity at the merges**: connected seams, and a contractible final seam. Then every period is a product of vortex reflections. It is *not* Euler's formula or the existence of degree-5 vertices: levelling works with zero vortices on the sphere (dome caps far from the 12 fives), and fails with zero vortices on the torus.
  - Concretely, parts (a) and (d) of §5 hold on 6-regular tori for trivial reasons.
  - Part (b), closing, is where planarity must enter. It is false on the 278 non-4-colourable tori.

---

## 5. Q4: the conjecture, finiteness, and decompositions

**Definitions.**
- A *chordless disc* is a near-triangulated disc in a planar triangulation G whose boundary cycle is an induced cycle.
- A *chordless hierarchy* of G is a binary tree whose leaves are chordless discs of bounded size, whose internal nodes are chordless discs U = A ⊔ B with A, B chordless discs, and whose root splits V(G) into two chordless discs.

**Conjecture LML (level merge with collar re-levelling) [C].** There are absolute constants R and w such that, for every planar triangulation G with minimum degree 5:

- **(a) Merge.** Let A, B be disjoint chordless discs whose union U is a chordless disc, and let c_A, c_B be colourings with τ ≤ 1. Then there are a renaming π and a colouring c_U of U with τ(c_U) ≤ 1 that agrees with c_A ∪ π c_B outside N_R(conflicts) ∪ N_w(∂U).
- **(b) Closing.** If A, B are chordless discs partitioning V(G) and c_A, c_B have τ ≤ 1, then some renaming plus recolouring of N_R(conflicts) gives a proper colouring of G.
- **(c) Decomposition.** G has a chordless hierarchy.
- **(d) Leaves.** Every chordless disc of bounded size has a 1-level colouring. This is a finite check. [M] It holds for all 300 chordless clusters tested.

**[P] (a)–(d) imply the 4CT.** Minimum degree 5 can be assumed for a minimal counterexample. Colour the leaves (d), merge up the tree (a) keeping every node 1-level, and close at the root (b).

Measured values: R ≤ 1 for merges, final R ≤ 2, and w ≤ 4 everywhere (E3b, E4).

**Does it reduce to a finite check? [C/P]**

- For maximum degree ≤ Δ, parts (a) and (b) are statements about **1-dimensional bands**: the collar of width w along ∂U, the seam band of width R, and their two junctions.
- Each band cross-section has finitely many states: local triangulation, colours, and the walk height relative to a guessed centre. Heights are confined to radius 1, so this is finite.
- So "for every admissible band input there exists a repair" is a ∀∃ statement about a finite transducer on cyclic words. [P] Statements of that kind are decidable, by automata projection and complementation.
- Three caveats:
  1. The finite check quantifies over *all* 1-level band colourings, not only those that extend into the interiors of A and B. It proves a stronger statement, which might be false even if (a) is true.
  2. The alphabet has size about 4^{O(wΔ)} times the number of local geometries. Even for Δ = 8 this is far beyond reach unless the transducer is minimised drastically.
  3. **Unbounded degree** (minimal counterexamples may have high-degree vertices) and **part (c)** are not finite checks. (c) is a global combinatorial statement about planar triangulations.

  [M] The greedy chordless preference was *not* always able to find a chordless merge. It fell back to merges with up to 66 chords. So (c) is the weakest link observed.
- Also, (b) is false on tori: §4 gives an infinite family of non-4-colourable 6-regular tori, all with edge-width 3. So any proof of (b) must use connected seams.

**The lopsided-merge danger [M].**
- `tilt_aware.md` saw large R at the top merges of a lopsided hierarchy at f = 40, where one ~13k-vertex cluster absorbs small neighbours. In our plain recursion (level leaves, no re-levelling), lopsided mode needs R up to 4 and final R up to 8 at n = 1,962, and R up to 9 at n = 4,002, with τ of the giant growing to 14.
- With re-levelling, lopsided mode is **as good as balanced**, or better: R ≤ 1, w ≤ 3, final R ≤ 1. ico30 lopsided had R = 0 at all 868 merges.
- So the danger was the unmaintained invariant, not the imbalance. A giant whose boundary is level presents a mismatch ≤ 4K to every small neighbour (§1.3).
- Balancing and chordless preference matter for a different reason: they keep clusters free of pockets, which is what keeps (ii) true at K = 1.
- A decomposition that cuts along vortex-rich lines was not needed for levelness: vortex density had no effect in §2. Vortices do matter for re-levelling, because only a collar that contains vortices can change the boundary monodromy (§1.4). Cutting so that cluster boundaries pass near vortices would therefore make (a) easier. This is untested.

**What is genuinely open.**
- (a) is plausible and measured, with no counterexample, but there is no argument for it. It is a "flat filling" statement: a level boundary can always be restored by recolouring a collar of bounded width, given that the boundary monodromy is small.
- (b) contains the whole difficulty of the final reduction at the root. It is the place where Kempe-type and reducibility arguments would have to enter.
- (c) is open: we do not know whether every 5-connected planar triangulation has a chordless hierarchy.

---

## 6. Files

- `lev.py`: clusters, boundary gauge, τ, the SAT encoding (`sat_level`, `min_tau`), `merge`, `chords`.
- `e1_survey.py` and `e1b.py` (rule check and confirmation of uncertain cases): `e1_survey.jsonl`, `e1b.jsonl`. `e1c_big.py`: `e1c_big.jsonl`.
- `words.py`: `words_out.txt`, the boundary-word lemma for m ≤ 11.
- `e2_strips.py`, `e2b_neck.py`: thin clusters and chords. `fails.py`: `fails.jsonl`, re-level failures from E4.
- `e3_merge.py`, `e3b_relevel.py`: single merges with and without re-levelling. `summ3.py`.
- `e4_recursion.py`: complete recursions; `e4_summary.jsonl`, `e4_logs/`, `summ4.py`; `fail_*.pkl` are the skipped clusters.
- `e5_torus.py`, `torus_summ.py`: tori, colourability and edge-width. The early zero-period field had an encoding bug (a positive end-point clause): it was removed and superseded. `torus_check.py` recomputes the periods independently.
- `e5b_periods.py`, `e5c_growth.py`: corrected period minimisation (`e5b_periods.jsonl`, `e5c_growth.jsonl`).
- `tforced.py`: two-vortex dome caps force t ≠ 0; four-vortex caps allow t = 0.

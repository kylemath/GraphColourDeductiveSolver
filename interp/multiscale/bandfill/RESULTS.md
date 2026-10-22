# Band filling on the straight degree-6 cylinder: structure of level rows, exact widths, and the finite check

22 Oct 2026. Scripts in this folder (`lev.py`, `fill.py`, `fill3.py`, `closure2.py`, `vortex.py`; logs `*.log`). Labels: **[P]** proved (argument given or exhaustive computation), **[M]** measured (exact, instance by instance), **[C]** conjecture. Setting as in `../closing/round2/tm.py`: rows are proper 4-colourings of C_L, r → r′ allowed iff r′(i) ∉ {r(i), r(i+1)}; the boundary walk of a row is H_{i+1} = H_i + e_{r(i)⊕r(i+1)} (constant sign, all degrees 6). **Insertion form** of the lemma: level rows a, b can be joined with k inserted rows iff some renaming π gives a path a → r_1 → … → r_k → πb. (tm.py's C(w) is a different measure: it recolours the level rows themselves and starts from rows at depth w; see §3.)

## 0. Verdict

| item | result |
|---|---|
| Level rows (τ ≤ 1 for some base point) | **[P] exactly** the rows in which some colour c occupies positions with cyclic gaps all 3, except one gap of 2 (L ≡ 2 mod 3) or 4 (L ≡ 1 mod 3). Verified against tm.py's τ over all rotations, all rows, L = 3..10. |
| Matched Z3 class, offset ≤ 4 | **[P] automatic** on the straight cylinder: f(t) ≡ L (mod 3) for every row; every level walk lies in a radius-1 hexagon. The hypotheses of the lemma are void here. |
| Minimal inserted rows k*(L) = max over level pairs of min_π k (insertion form) | **[M]** L = 5: 2, 6: 1, 7: 2, 8: **4**, 9: 2, 10: 2 (k ≤ 2 run), 11: see `fill_11.log`. **w = 2 is false at L = 8**; the previous C(2) result stands because C(w) lets the level rows be recoloured. |
| Cause of k = 4 | **[P]** base-point dependence of τ (review1 §B). With t ≠ 0, a row that is level for the base point at its defect can carry a hidden straight run of 4 equal labels across the lap boundary (two-lap circumradius 2). The 5 worst pairs listed in `fill_5_11.log` all have the run-4 row (0,1,0,1,0,2,1,2) as a; the run-grouped table for L = 8 (`fill3_L8.log`) was still computing at hand-off. [C] run ≤ 2 ⇒ k ≤ 2. |
| Uniform-in-L proof | not reached. The finite check is stated exactly in §4 and implemented (`closure2.py`); its state space grows ×3–4 per column and did not reach periodicity in the time box (no-defect class: 381,024 elements at 7 columns, all closed elements at lengths 3 and 6 fillable with k ≤ 2). |
| One vortex in the band | **[P]** impossible with two straight boundary rows (handshake parity); the minimal interior defects are a 5–7 dipole (changes L by 1) or a flip quadrupole 5,5,7,7. **[M]** quadrupole: fillable at k = 2 for L = 6, 7 (all pairs); at L = 8 the quadrupole *reduces* the unfillable-at-k=2 pairs from 10,464 to 5,640 of 46,080. |

## 1. Structure of level rows [P]

Let p be the centre of the τ-ball. τ ≤ 1 and H ⊂ Λ force p ∈ Λ (a half-lattice centre off Λ only admits a rhombus of diameter √3, whose walks are also hexagon walks). The walk uses only steps e_1, e_2, e_3, and the directed graph on the hexagon {0, ±e_j} with these steps is 3-layered: 0 → e_j, e_j → −e_k (k ≠ j), −e_k → 0. Hence every walk of length ≥ 3 passes through 0 every third step, and the colour of 0 (call it c) occupies an arithmetic progression of step 3, except at the lap ends: the lap runs from H_0 to H_L = H_0 + t with t ∈ {0, ±2e_a}, giving (i) t = 0: all gaps 3, L ≡ 0; (ii) t = 2e_a: the lap starts at −e_a and ends at e_a, one gap of 2 (colours c, a, c), L ≡ 2; (iii) t = −2e_a: one gap of 4, L ≡ 1 (mod 3). Conversely each such row is level for the base point at its defect (direct check). The number of level rows is 3·4·6^{L/3} (L ≡ 0); 4·L·6^{(L−2)/3} (L ≡ 2), up to coincidences.

Base-point dependence: for t ≠ 0 **no** row is level for all base points (the lap from the vertex after the defect contains 0 and 2e_a plus a point at distance √3 from e_a). So on the cylinder "level" must mean "for some base point", and this is also what the SAT pipeline guarantees. Its price: the lifted (two-lap) walk may contain a straight run of up to 4 steps across the lap boundary (blocks (c,j,a)(c,a)(c,a,k) give colours a,c,a,c,a). These are the hard pairs below.

Z3 class: t = n_1 e_1 + n_2 e_2 + n_3 e_3 with Σ n_j = L, so f(t) = n_1 + n_2 − 2n_3 ≡ L (mod 3) for **every** row, level or not. This is Lemma 1's χ for the straight cylinder.

## 2. Exact widths (insertion form) [M]

`fill.py`: for canonical a (up to rotation and renaming) and every level b, every π ∈ S_4, k = 0..3, fillability is trace(T_0⋯T_{L−1}) ≠ 0 for 16^k-state boolean column transfer matrices.

| L | level rows | pairs (a canonical × b) | k = 0 | 1 | 2 | 3 | ≥ 4 | k* |
|---|---|---|---|---|---|---|---|---|
| 5 | 240 | 480 | 168 | 168 | 144 | 0 | 0 | 2 |
| 6 | 312 | 1,248 | 768 | 480 | 0 | 0 | 0 | 1 |
| 7 | 1,176 | 8,232 | 1,368 | 4,968 | 1,896 | 0 | 0 | 2 |
| 8 | 2,880 | 46,080 | 2,952 | 14,040 | 18,624 | 10,008 | **456** | **4** (tm.py dLL = 5 steps) |
| 9 | 2,328 | 30,264 | 7,392 | 21,648 | 1,224 | 0 | 0 | 2 |

Grouped by hidden run (max cyclic run of equal edge labels, `fill3.py`): L = 7 and 9 have runs ≤ 2 only; at L = 8 the listed worst pairs involve a run-4 row; the complete run-grouped table (`fill3_L8.log`, `fill3_L10.log`) and the L = 11 histogram (`fill_11.log`) were still being written at hand-off (background jobs keep appending to these logs). The renaming matters: for most pairs only 1–4 of the 24 renamings work at the minimal k, and the renaming that maps b's skeleton colour to a's is **not** always among them (`fill_5_11.log`, `match_some`).

## 3. Relation to tm.py's C(w) [P]

C(w) requires a path of exactly 2w+1 steps from any row w below a level row to any row w above one, i.e. it recolours the level rows. The insertion form keeps them. C(2) holds at L = 8 while the insertion form needs k = 4 there, so the two are not equivalent, and the closing step (b) needs the insertion form only if the level rows are to be kept; if the closing may recolour a collar of width w on each side including the boundary row, C(w) is the right statement and w = 2 is what was measured. The hidden-run rows are exactly where the two differ.

## 4. The finite check that would prove it for all L [P statement, not completed]

Fix k. Words are pairs (a, b) of level rows with skeleton colour 0 (WLOG), read column by column, b glued as πb. The element of a word of length m is (q_a, q_a′, q_b, q_b′, a_0, b_0, (P_π)_{π ∈ S_4}) where q are states of the 32-state automaton of §1 (gap counter, defect flag, last letter) and P_π is the 16×16 boolean relation between inner column states at columns 0 and m−1. Elements compose letter by letter; the layers E_m are eventually periodic (finite set); a closed element (q_a = q_a′, q_b = q_b′) of E_L is a level pair of length L, fillable with renaming π iff trace(P_π·T_close) ≠ 0. **The lemma for all L ≥ 5 at width k is equivalent to: every closed element of every layer E_m, m ≥ 5, has some π with nonzero trace.** This is decidable (finitely many elements) and `closure2.py` implements it with S_3 symmetry reduction. Observed: no-defect class (L ≡ 0), k = 2: layers 582, 2,648, 10,584, 31,104, 95,256, 381,024 (m = 2..7), all closed elements at m = 3 and 6 fillable; the full class grew ×4.3 per column (238,802 at m = 5) and was stopped for memory. A plateau is expected once the relations forget the middle of the word (P_π is block-diagonal by height offset, so at most ~10^5–10^6 distinct tuples), but it was not reached; the check needs either the height-offset quotient of P or more memory than the 15 GB here.

[C] The hidden run is a bounded local feature (length ≤ 4), so k* should be a constant ≥ 4 for L ≡ 2 (mod 3) and 2 for L ≡ 0, 1; and with "level" strengthened to "two-lap circumradius ≤ 1.5" (hidden run ≤ 3, which the SAT pipeline can impose as one more clause), w = 2 is expected for all L.

## 5. Vortices in the band

[P] A triangulated annulus with both boundary rows straight (every boundary vertex has 2 interior edges) has an even number of odd interior vertices (handshake). So "one vortex" cannot occur; the minimal cases are a 5–7 dipole, which is a dislocation and changes the circumference by one (so f(t) differs by 1 across the band, as Lemma 1's Eulerian hypothesis predicts), and a flip quadrupole (5,5,7,7), which keeps L and the row structure. [M] `vortex.py`: one flipped diagonal between inner rows: all level pairs fillable at k = 2 (L = 6, 7) and the quadrupole lowers the number of unfillable-at-k=2 pairs at L = 8 (5,640 against 10,464 without the flip). So vortices absorb mismatch rather than create it, consistent with the sphere data. The dipole case (rows of length L and L+1) was not run.

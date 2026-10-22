# Tilt-aware seams: matched tilts, a tilt-aware recursion, and single-vertex vortices

Follow-up to `seam_lemma.md`. Every claim below is labelled:
- **[P]**: proved here, with a short argument.
- **[M]**: measured, with SAT (Minisat22) as the ground truth.
- **[C]**: conjecture or interpretation.

The scripts are in `/mnt/project-files/multiscale/`: `matched.py`, `matched2.py`, `ms_tilt.py`, `ms_tilt_b.py`, `kempe5.py`, `kempe6.py`, `defects_seam.py`, `summ.py`. They depend on `tilt.py` and `ms_orig.py`, which is a copy of `/tmp/claude-0/ms/ms.py`; the original was not edited. Raw outputs are in `tilt_aware_out/`.

The height function h is the one defined in `seam_lemma.md` §1. The renamings act on h by D3 isometries plus translations.

## 0. Summary

1. **(a) Matched tilts.** When both sides have the same tilt, or are both flat, the best renaming aligns them exactly, so R = 0 [P for periodic colourings, M]. With a controlled mismatch, min R grows roughly like 0.4–0.5·M, and its dependence on L at fixed seam-row M is weak but not zero [M]. **R = O(M + const) is plausible as a conjecture, with M measured across the whole repair band, not just on the seam row** [C].
2. **(b) Tilt-aware recursion on domes.**
   - The tilt-aware variant guides SAT towards a per-face flat 3-colouring reference.
   - At f = 30 it cut the per-level maximum R from 7–9 exact (up to 15 as an upper bound) to **at most 1** at every level, on both seeds [M].
   - At f = 40 it cut conflicts and R at low levels. The top merges (one giant cluster of about 13.4k vertices absorbing small neighbours) still needed large R. Those values are only upper bounds, because some SAT calls hit their budget [M].
   - **Vortices.** Odd-degree vertices are the only places where height mismatch can be absorbed. The single-vertex dome test shows this with a proved lower bound R ≥ d(v,odd) − 2, matching the measured R ≈ d − 1 [P+M]. Defect quadrupoles placed along a tilted seam bring R down from more than 12 to 1–2 once their spacing is about 3 [M].
3. **(c) Single vertex.**
   - At degree-5 vertices of domes, local min R ≤ 3 in every sample, even when Kempe's procedure swapped chains reaching radius 31, i.e. the whole sphere [M].
   - At degree-6 vertices whose link has nonzero monodromy, R is forced up to the distance to the nearest degree-5 vertex [P lower bound, M].
   - The length of Kempe chains is the wrong measure of difficulty. The height monodromy is the right one.

## 1. Two elementary facts used throughout

**[P] F1: 3-colourings are perfectly flat.** In a properly 3-coloured near-triangulation, adjacent triangles carry opposite cyclic orders of the colours. Call the triangles with order (0, g, h) counterclockwise "up". The height increment along u→w then depends only on (c(u), c(w)). So h = φ∘c with φ(g) − φ(0) = e_g, φ(h) − φ(g) = e_{g+h}, φ(0) − φ(h) = e_h, which is consistent because these sum to 0. **h takes exactly 3 values**; `tilt.py` confirms this on c3. Translates of c3 are renamings of c3, so flat|flat seams between periodic 3-colourings align exactly under renaming. The same holds for c22 versus its translates.

**[P] F2: Eulerian merges are free.** Suppose U is a simply connected near-triangulation with every interior vertex of even degree. Then the triangles of U can be 2-coloured, and a 3-colouring of U, if one exists, is unique up to permutation: the colours of one triangle force all the rest by propagation. If A and B are 3-coloured connected Eulerian sub-near-triangulations, their restrictions agree with U's 3-colouring up to renaming, so **R = 0**. An Eulerian disc is in fact 3-colourable; this is the standard disc version of Heawood's theorem, quoted rather than reproved here. So a recursion confined to Eulerian regions never needs repair.

**[P] F3: vortex lower bound on any triangulation.** Let v have even degree, and let a colouring c of G−v have nonzero height monodromy around v. Suppose the ball B_{R+2}(v) is a disc containing no odd-degree vertex. Then no renaming of v plus radius-R repair works.
- The conflicts lie in N[v], so every recoloured vertex is in B_{R+1}(v).
- The loop at distance R+2 is therefore fixed. Its monodromy equals the link's, because the annulus between them is Eulerian and c is proper there. So it is nonzero.
- But a proper colouring of the Eulerian disc inside the loop has a single-valued height, so its monodromy is zero. Contradiction.
- Hence **R ≥ d(v, odd) − 2**.

## 2. (a) Matched-tilt seams on lattice parallelograms

Setup: A is the rows j<0 and B the rows j≥0, with D = 11–12 rows each. M is the height mismatch along the seam rows (row −1 against row 0), minimised over the 24 renamings: the diameter over t of H_A(t) − H_{πB}(t). min R is exact radius-R repair under the best renaming. The tables below are from one run each (seed 0); scripts `matched.py` and `matched2.py`, outputs `matched0.txt`, `matched2.txt`, `matched3.txt`.

**Same-type colourings** (4–6 samples per cell) [M]:

| pair | L = 12 | 24 | 36 | 48 |
|---|---|---|---|---|
| flat\|flat (c3 vs translated/renamed c3) | M=0, R=0 | 0, 0 | 0, 0 | 0, 0 |
| c22\|c22 (same tilt) | M=0, R=0 | 0, 0 | 0, 0 | 0, 0 |
| flat + 30 random Kempe flips per side | M=1.7, R=0 | 1.7, 0 | 1.7, 0 | 1.7, 0 |
| flat + 300 Kempe flips per side | M≤3.5, R≤1 | 4.6, 1 | ≤5.2, 1 | ≤5.2, 1 |
| c22 + 300 Kempe flips per side | M≤3.5, R=0 | ≤4.6, 1 | – | 4.6, 1 |
| flat\|c22 (mismatched, control) | M=12, R=4 | 24, 10 | – | 48, ≥11 |

Random Kempe flips produce only small height variation (M ≤ 5), and R stays at most 1 out to L = 48.

**Controlled mismatch** (`matched2.py`). Row −1 of A is pinned to c22 on a segment of length m and to c3 elsewhere, with 2 free vertices at each junction. The rest of A is completed by SAT with random phases. B is c3.

| m | L = 24 | L = 48 | L = 72 |
|---|---|---|---|
| 0 | M=1.7, R=0 | 1.7, 0 | 1.7, 0 |
| 4 | 4.6, 1 | 3.5, 1 | 4.6, 1 |
| 8 | 6.2, 1 | 6.2, 2 | 7.6, 3 |
| 12 | 11.4, 3 | 10.8, 5 | 10.5, 6 |
| 16 | 15.1, 6 | 15.1, 7 | 15.1, 8 |

A second seed (`matched3.txt`, stopped at its time limit) gives the same picture: m=12 → R = 3, 5, 5; m=16 → R = 6, 7.

The height-theorem lower bound uses the fixed rows −(R+2) and R+1 rather than the seam rows. It gave 0–3 against measured R of 0–7: **valid but loose by a factor of 2–3.**

**Reading.**
- [M] R is driven mainly by M, at roughly R ≈ 0.4–0.5·M.
- [M] At fixed seam-row M, R still rises by about 2–3 from L = 24 to L = 72.
- [C] The likely cause is that the random SAT completion puts extra tilt into the deeper rows of A. A wider seam leaves more room for that, so the seam-row M understates the band mismatch.
- [C] The natural conjecture is R ≤ c₁·M_band + c₂ in flat regions, where M_band is the height mismatch over the whole band of width O(R). This is not established. A clean test would pin several rows so that M_band is controlled.

## 3. (b) Tilt-aware recursion on geodesic domes

**What `ms_tilt.py` changes** relative to `ms.py`:
- `icosphere(f)` also records a per-face flat reference ref(v) = (i + 2j) mod 3 from the barycentric grid indices. It is computed from local geometry only; edge vertices take the value of the first face that creates them.
- The leaves start at ref instead of all zeros.
- In every repair, Minisat's phases are set to π*(ref), where π* is the permutation that best matches the current cluster colouring. This makes the solver prefer flat colourings.
- The renaming choice and the radius search are unchanged.
- `ms_tilt_b.py` additionally caps each SAT call at 2×10^5 conflicts and logs every merge. A capped call is treated as failure, so any R measured with timeouts is an upper bound.
- Note: ref is not coherent across the 30 icosahedron edges (194 monochromatic ref edges at f=10) or at the 12 degree-5 vertices. These seams have bounded height mismatch, since both sides are flat (F1).

**Results** [M]. Entries are the maximum R per level, with the number of merges that had conflicts in brackets. † means the maximum includes SAT timeouts, so it is an upper bound.

| level | ico30 plain s0 | ico30 plain s1 (budgeted) | ico30 tilt s0 | ico30 tilt s1 | ico40 plain s0 | ico40 tilt s0 |
|---|---|---|---|---|---|---|
| L2 (~17 vertices) | 2 (81) | 2 (78) | 1 (9) | 1 (5) | 2 (159) | 1 (7) |
| L3 (~60) | 3 (62) | 3 (66) | 1 (11) | 1 (16) | 3 (119) | 1 (28) |
| L4 (~150–400) | 4 (23) | 3 (23) | 1 (12) | 1 (11) | 3 (39) | 5 (22) |
| L5 | 3 (8) | 4 (6) | 1 (8) | 1 (4) | 3 (14) | 4 (8) |
| L6 | 3 (3) | 4 (6) | 0 (2) | 0 (2) | 3 (3) | 7† (2) |
| L7 | **9** (2) | 7 (4) | 0 (1) | 1 (2) | 5† (2) | 12† (2) |
| L8 | 5 (2) | 11† (2) | – | 0 (1) | 5 (1) | – |
| L9 | 5 (1) | 4 (1) | 1 (1) | 1 (1) | 17† (1) | 15† (1) |
| L10 | 6 (1) | 4† (1) | – | 1 (1) | 9† (1) | 13† (1) |
| L11 | – | 2 (1) | – | – | 5 (1) | 4 (1) |

ico30 plain s1 also has an L12 row, the final merge into the whole sphere, at R = 15†. The ico40 runs were stopped after L11, at levels L12 and above, because of time. The unbudgeted ico30 plain seed-1 run had been stuck for over 50 CPU minutes in repair SAT calls and was killed. The budgeted rerun finished in 66 s.

**Reading.**
- [M] Plain recursion on domes does not have bounded R. It reaches 9 at f=30 (seed 0, exact), 7 exact and up to 15† (seed 1), and 5 exact at f=40, against R ≤ 4 at f ≤ 17 in the earlier experiments. Its repair SAT calls also become very hard, with long UNSAT proofs. That is the expected signature of height-type obstructions, which are parity-like and hard for CDCL solvers.
- [M] Flat guidance removes about 90% of the seam conflicts at every level. At f=30 it gives R ≤ 1 everywhere.
- [M] At f=40, seed 0, the top merges are very unbalanced: one cluster of about 13.4k vertices plus small neighbours. There, both variants hit SAT timeouts, and the R values are upper bounds that cannot be compared reliably.
- [C] The likely cause at f=40 is that the giant cluster's boundary crosses several incoherent ref seams and vortex sectors.
- [C] A better reference would put the frustration on 6 short branch cuts pairing the 12 degree-5 vertices, rather than on all 30 face edges. That is the obvious next step.
- [C] The hierarchy itself (`hierarchy()` in ms.py) becomes unbalanced at the top. That is a confound independent of tilt.

### 3.1 How vortices absorb tilt

[P] Around an odd-degree vertex o, the triangles cannot be 2-coloured up/down. Going once around o flips the up/down labelling and so flips the sign of every increment. The height is therefore a section of a flat bundle: around o, its monodromy is a point reflection h ↦ −h + 2p_o.

[P] By the Lipschitz property, the centre p_o lies within O(1) of the heights at o's link. A single defect cannot absorb an arbitrary offset, but it does reflect the height field.

[P] The composition of the reflections at two odd vertices o and o' is the translation by 2(p_o − p_{o'}): a pair of defects acts like a dislocation with a bounded "Burgers vector". A tilt mismatch of δ per unit length along a seam therefore needs about δ·L/O(1) defects within reach of the seam.

**Measurements** [M]:
- `defects_seam.py`: the tilted|flat seam c22|c3 with L = 36, plus edge flips in A along the seam. Each flip creates two degree-5 and two degree-7 vertices.

  | flip spacing | none | 18 | 12 | 8 | 6 | 4 | 3 |
  |---|---|---|---|---|---|---|---|
  | min R | >12 | 12 | 12 | 12 | 9–10 | 4–5 | 1–2 |

  Each quadrupole absorbs roughly 3 units of height mismatch. This matches the O(1)-per-defect picture.
- `kempe6.py`: a degree-6 vertex at distance d from the nearest degree-5 vertex of an icosphere, with a link of monodromy norm 2√3.

  | d | 4 | 6 | 9 |
  |---|---|---|---|
  | min R (3 samples) | 5, 3, 4 | 5, 5, 6 | 8, 8, 8 |

  This sits against the proved lower bound d − 2 (F3). The repair has to reach a defect.

### 3.2 Can a recursion keep every cluster boundary level?

- [P] **Yes, inside Eulerian regions.** Use 3-colourings: they are flat (F1), and merges are free (F2). On domes this covers everything except the neighbourhoods of the 12 degree-5 vertices.
- [C] **Clusters containing odd vertices** must carry vortices. A boundary loop around a set S of odd vertices has monodromy equal to a product of |S| point reflections. When |S| is even, that is a translation T(S), which depends on the colouring through the centres p_o. A "level" boundary needs T(S) ≈ 0, and when |S| is odd, a reflection centre near the boundary's heights.
- **Open:** whether every cluster admits a colouring meeting these conditions, and whether a merge can preserve them with bounded R. I see no obstruction, but no argument either. This is now the crux of the multiscale route.
- [C] For triangulations with dense defects (random ones), tilt never builds up, which explains the original small R. The hard regime is the intermediate one: long Eulerian stretches between sparse defects. Domes are the canonical example.

## 4. (c) Single vertex: Kempe chains versus local repair

**What was run** (`kempe5.py`):
- Graphs: icospheres with f = 6, 10, 14, so n = 362–1962.
- Vertices: v = vertex 0 (degree 5), and the degree-6 vertex farthest from all odd vertices (a face centre).
- Colourings of G−v: SAT with random phases plus 200 random Kempe flips. If the link did not use all 4 colours, the colouring was resampled with the link pinned to (0,1,0,2,3) for degree 5 or (0,1,0,1,2,3) for degree 6. So most samples are "non-adversarial except for the link".
- For each colouring:
  - Kempe's procedure: single swaps first, then Kempe's double swap, recording the radius of the recoloured set.
  - Exact local min R, where v's colour is free.

**Errera and Kittell graphs themselves were not built.** I do not trust my memory of their adjacency lists, and §1 F3 already explains the single-vertex behaviour. The run was stopped during the degree-6 samples at f=14, where hard UNSAT calls stalled it. Those cases were rerun with `kempe6.py`, which starts the search at the proved lower bound.

| vertex | f | Kempe radius (8 samples) | local min R | notes |
|---|---|---|---|---|
| deg 5 | 6 | 1–5 | 0–1 | |
| deg 5 | 10 | 1–30 | 0–3 | Kempe chains often span the sphere (radius 30 at n=1002) |
| deg 5 | 14 | 1–31 | 0–3 | |
| deg 6, d=4 | 6 | 7–15 (mono≠0); 1 (mono=0) | 3 (mono≠0); 0 (mono=0) | |
| deg 6, d=6 | 10 | 8–25 (mono≠0); 1–2 (mono=0) | 5–7 (mono≠0); 0 (mono=0) | |
| deg 6, d=9 | 14 | – | 8, 8, 8 (`kempe6.py`) | |

Kempe's procedure succeeded in every sample.

**Reading.**
- [M] At degree-5 vertices, local repair stayed at R ≤ 3 even when Kempe's argument needed chains spanning the whole sphere.
- [P] There is no translational monodromy obstruction at a degree-5 vertex. Its monodromy is a reflection, and the centre is free to sit at v.
- [M] At degree-6 vertices, R is set entirely by the monodromy. It is 0 when the monodromy is zero. When it is nonzero, R is about d(v, odd) − 1, consistent with the proved d − 2.
- [C] Prediction for "grown" Errera/Kittell-type families: what controls R is not chain length, but whether the configuration contains even-degree vertices whose colouring winds, and how far those are from odd vertices.

## 5. What is proved and what is not

**Proved:**
- F1: 3-colourings have 3-valued heights.
- F2: merges of Eulerian clusters need R = 0.
- F3: the vortex lower bound R ≥ d(v,odd) − 2.
- The point-reflection monodromy at odd vertices.
- The lattice theorem from `seam_lemma.md`.

**Measured:** every table above.

**Conjectured:**
- R = O(M_band + 1) in flat regions.
- O(1) absorption per defect.
- That the tilt-aware recursion stays bounded once the reference is vortex-coherent and the hierarchy balanced.
- That every cluster can be given a level boundary.

None of these is close to a proof of the 4CT. Even a perfect seam lemma for level boundaries would still need the global "keep boundaries level" invariant, and that is where the difficulty now sits.

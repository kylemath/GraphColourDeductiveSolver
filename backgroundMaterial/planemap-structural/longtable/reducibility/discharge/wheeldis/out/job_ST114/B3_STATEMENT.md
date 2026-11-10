# ST-114 B3: the induced-window theorem: statement note (for the strategy review; no proof structure committed yet)

Studio, 10 Nov. This note fixes **what** B3 says in Lean. Lean files: `lean/RSSTWindow.lean` (B3) and `lean/RSSTCharge.lean` (B1
skeleton). Both are **new files** and compile with `sorry` only where marked. No existing module is edited.
Marks: [read] = from a file; [inf] = mine.

## 1. Setting and hypotheses

`T : SphericalMap n` (Mathlib PlaneMap: `graph : SimpleGraph (Fin n)`, `rotation : RotationSystem graph`, `fills`) [read].
B3 takes the project's frame class unchanged, as `hT : ClaimGlue.Internally6 T` (ClaimGlue.lean:70) [read]. Its fields:

| field | meaning | used by B3 for |
|---|---|---|
| `pos`, `connected` | n > 0, connected | dual connectivity (one potential per cycle, up to swap) |
| `triangulated` | every face has length 3 | two triangle faces on each edge (L5) |
| `minDeg` | every vertex has degree ≥ 5 | d ≥ 5 and \|seg_i\| ≥ 2 |
| `noSep` | every triangle is `Facial` (SideTriangle.lean:830) | F0: every 3-cycle is a face |
| `noShortSep` | `NoShortSepCycle` (ClaimGlue.lean:64): no `Cyc` with r ≤ 5, a `CycPotential`, `BothSides`, and at r = 5 `BothSides2` | the separating 4-cycle and 5-cycle steps |

- No other hypothesis is used. In particular, B3 does **not** use letters, domains, parts or charges.
- Birkhoff equivalence of `noShortSep` with Gonthier's ring condition: RSSTADM SCOPING Addenda A/B [read].

## 2. Window objects (Lean definitions in RSSTWindow.lean)

- `rotNbr T v a k`: the k-th neighbour after `a` in the rotation at `v` (k = 0 gives `a`). It is defined by iterating
  `T.rotation.next` on the dart (v, a).
- `IsLink T u d w`:
  - `w : ℕ → Fin n` is d-periodic;
  - d = deg u;
  - `T.Adj u (w 0)`;
  - `rotNbr T u (w i) 1 = w (i+1)`.

  So w lists rot(u) in rotation order. This is the spec's w_0..w_{d−1}.
- **Ring 2** `InR2 T u d w x`: x ≠ u, x is no `w j`, and some `w i` is adjacent to x. Its members:
  - the apexes s_i;
  - the privates p_i.k of every link vertex;
  - for a 9+ link vertex, **all** of its real middle neighbours, not just the three drawn ones. Ring 2 is defined from the real
    graph, so the undrawn middles are included automatically.
- `IsApex T w i x`: x ≠ u and x is adjacent to both w_i and w_{i+1}. That is s_i, the third vertex of the other face on the edge
  w_i w_{i+1}.
- **Seg_i** (in the note, not a Lean def): the neighbours of w_i other than u, w_{i−1}, w_{i+1}, in rotation order from s_{i−1}
  to s_i. It has deg(w_i) − 3 ≥ 2 vertices.

The window is therefore the closed 2-ball of u. Its drawn picture (spec §2) is the word (d, link letters, seg lengths) with the
9+ middles collapsed.

## 3. Conclusion (`WindowInduced T u d w`, five fields)

| field | statement | spec / W6b |
|---|---|---|
| `link_inj` | `i < d → j < d → w i = w j → i = j`, and `w i ≠ u` | distinctness of u, w_0..w_{d−1} |
| `link_chordless` | `T.Adj (w i) (w j) → j % d = (i+1) % d ∨ i % d = (j+1) % d` | (a) |
| `apex_unique` | for each i there is exactly one x with `IsApex T w i x` | the two faces on w_i w_{i+1} |
| `r2_home` | for `InR2 x`: either exactly one link index i (mod d) has w_i ~ x, or x is s_i for some i and the link neighbours of x are exactly w_i and w_{i+1} | (b) + (c): no identifications; the only sharing is s_i between seg_i and seg_{i+1} |
| `r2_chordless` | for `InR2 x`, `InR2 y`, `T.Adj x y`: there is an i with w_i ~ x, w_i ~ y and `Facial T (w i) x y`, so x and y are consecutive in rot(w_i), i.e. on R2 | (d) |

All triangles are faces by `hT.noSep` directly (F0). B3 restates it on the window as `window_facial` for use downstream.

- **(c) "no extra u/w edges"** is `IsLink` (rot(u) is exactly the link) together with `link_chordless`, and with `r2_home` for
  w–ring-2 edges.
- **The undrawn 9+ middles are covered** because `InR2` ranges over every real neighbour of every w_i.

**Main theorem (RSSTWindow.lean):**

    theorem window_induced (hT : ClaimGlue.Internally6 T) {u : Fin n} {d : ℕ} {w : ℕ → Fin n}
        (hL : IsLink T u d w) : WindowInduced T u d w

## 4. How B3 is used [inf]

1. **Evaluation soundness (B4).**
   - `WindowInduced` gives an isomorphism between the subgraph of T induced on the 2-ball of u and the drawn window of the word
     read off T, with each 9+ link vertex's real middles collapsed to its drawn middle.
   - The 71 rule parts read only u, w, s, the privates, hats inside the window, and ring-3 values that are never constrained.
   - So u's real final charge equals the word's evaluated charge.
   - B4 states this as `finalCharge T u = evalWord (wordOf T u)`. It needs the rotation order of each w_i as well; that is
     `IsLink` + `rotNbr`.
2. **Kill → occurrence (B6).**
   - If a configuration K embeds in the drawn window with its hosts in the window, compose with the same isomorphism. That gives
     an injective, adjacency-preserving and rotation-preserving map into T. With F0 its triangles are faces, so it is an
     `OccursW` / `OccursC` for K's entry.
   - A 9+ middle is never a host (spec §6), so collapsing the middles does not matter.

## 5. Planned lemma list (to be proved only after the review)

| lemma | content | from | maps to |
|---|---|---|---|
| L0 `facial_nx` | `Facial T a b c` ⇒ b, c consecutive in rot(a), in one orientation | SideTriangle `Facial`, `Nx` | F0 |
| L1 `link_card` | rot(u) has exactly deg u darts, so `link_inj` | RotationSystem `cyclic`, `neighborOrbitEquiv` | distinctness |
| L2 `link_chordless` | w_i ~ w_k with k ≠ i±1: the triangle u w_i w_k is facial (noSep), so w_k is next to w_i in rot(u) (L0), so k = i±1 | L0, L1 | **(a)** |
| L3 `nbr_wi` | N(w_i) = {u, w_{i−1}, w_{i+1}} ∪ seg_i, disjointly; seg_i avoids u and every w_k; \|seg_i\| = deg w_i − 3 ≥ 2 | L2, simplicity, minDeg | **(c)** |
| L4 `two_faces` | an edge ab of a triangulation lies in exactly two triangle faces abc, abc′ with c ≠ c′; the third vertices of facial triangles on ab are exactly these two | `triangulated`, `fills`, L0 | `apex_unique`; (b) case k = i+1 |
| L5 `sep_tool` | for a `Cyc` ρ (from `exists_cycPotential'`, DCheckPinchGeom:76): the two faces on a cycle edge get different potentials (`cycInd_cycle'`), and an off-cycle vertex lies on the side of any face it touches (`onSide_of_dartC'`). Gives `BothSides` from two off-cycle vertices next to the two faces of one cycle edge | DCheckPinchGeom, SideCycle | the separating-cycle steps |
| L6 `r2_far` | x ∈ seg_i ∩ seg_k, k ∉ {i, i±1}: the 4-cycle u w_i x w_k has w_{i+1} and w_{i−1} (both off-cycle by L2/L3) on the two sides of edge u w_i (L5), contradicting noShortSep at r = 4 | L5, L2, L3 | **(b)**, case k far |
| L6′ `r2_shared_apex` | x = s_i and x ∈ seg_k with k ∉ {i, i+1}: since d ≥ 5, one of i, i+1 is non-adjacent to k, and L6 applies to that index | L6, minDeg | **(b)**, the implicit sub-case (RSST-1SHOT S7) |
| L7 `r2_next` | x ∈ seg_i ∩ seg_{i+1}: the triangle w_i w_{i+1} x is facial, so x = s_i (L4) | L4 | **(b)**, case k = i+1 |
| L8 `r2_chord_same` | x, y ∈ seg_i adjacent: w_i x y is facial (noSep), so x and y are consecutive in rot(w_i) | L0 | **(d)** case 1 |
| L9 `r2_chord_adj` | x ∈ seg_i, y ∈ seg_{i+1}, neither is s_i: the 4-cycle w_i x y w_{i+1}. The faces on w_i w_{i+1} have third vertices u and s_i (L4), both off-cycle, on opposite sides (L5): a separating 4-cycle | L4, L5 | **(d)** case 2 |
| L10 `r2_chord_far` | x ∈ seg_i, y ∈ seg_k, k ∉ {i, i±1}, no shared seg: the 5-cycle u w_i x y w_k. Each side holds ≥ 1 link vertex. A side with a single link vertex w_j also holds seg_j minus the cycle (≥ 2 vertices, by L3 and the case choice), so ≥ 3. The other side has d − 3 ≥ 2. So `BothSides2` holds, contradicting noShortSep at r = 5 | L5, L3, minDeg | **(d)** case 3, **the only use of the 5-cycle clause** |
| main | assemble `WindowInduced` | L1–L10 | — |

W6b's (a)–(d) (ext_handoff_nov3/rsst/fp2/DECISIONS.md f099d732) and RSST-1SHOT's S7_VERDICT.md (e6e62927) give the same case
split [read]. L6′ is the sub-case that (b) leaves implicit.

## 6. Existing modules it builds on [read]

- **Frame class and separating cycles:**
  - `ClaimGlue` (Internally6, NoShortSepCycle);
  - `SepAll` (`BothSides`, `BothSides2`, `SepCyc`, `cyc3_icycle`, `cyc4_cyc`, `onCyc4_sub`);
  - `DCheckPinchGeom` (`Cyc`, `cycInd_even'`, `exists_cycPotential'`, `side_constC'`, `onSide_of_dartC'`, `cycInd_cycle'`);
  - `SideCycle` (`OnCyc`, `cycInd`, `CycPotential`);
  - `Sep4` (`onSide_adjC`, `not_onSide_flip`) and `Sep5` (`side5`), for the side bookkeeping.
- **Faces, rotations and the map:**
  - SideTriangle (`Facial`, `NoSep`, `OnSide`);
  - VacancyIcosahedral (`Nx`);
  - Mathlib PlaneMap RotationSystem (`next`, `cyclic`, `faceNext`, `neighborRotation`, `neighborOrbitEquiv`).

B3 needs no change to any of these, and all of them are in the rsst118 build used by the hC/hD jobs.

## 7. B1 skeleton (RSSTCharge.lean)

- `charge0 T v := 10 * (6 − deg v)` (ℤ).
- `sum_charge0_ge`: Σ charge0 ≥ 120 for a triangulation with a dart. It rests on
  `SphericalMap.twice_edges_add_twelve_le` (EulerSharp.lean:272, 2E + 12 ≤ 6n; compiled in the rsst118 build) and on the
  handshake lemma, so `euler_tri` (TutteSides, not compiled there) is not needed [read].
- `Discharge`: a transfer τ : Fin n → Fin n → ℤ.
  - `final T τ v = charge0 v − Σ_w τ v w + Σ_w τ w v`.
  - `sum_final_eq`: the total is conserved.
  - `exists_pos_final`: some vertex ends with final charge > 0.

B2 / B4 / B5 are held until k answers.

## 8. Estimate [inf]

B3 ≈ 2–3.5 k lines and 12–20 pd (ST-113).
- The largest pieces are L1 (rotation-orbit bookkeeping), L4 (two faces per edge) and L10 (the 5-cycle side count). L10
  repeats the shape of `Sep5.side5`.
- L5 is mostly a wrapper over DCheckPinchGeom.

## 9. Review outcome (15:05Z) and notes for B4 / B6

**Approved.** The strategy review approved B3 and checked the lemma plan by hand under `Internally6`. Two points are now explicit:
- (a) `apex_unique`: the apex s_i is neither u nor any w_k. This follows from `link_chordless` and d ≥ 5.
- (b) L10's hypothesis reads: "no representation (i, k) of the pair x, y at cyclic index distance ≤ 1". Then the short side has
  ≥ 3 vertices and the other side d − 3 ≥ 2.

**Notes for B4 / B6** (recorded, not proved in B3):
1. **Orientation coherence.** Every B3 field is unoriented. B4 must add that rot(w_i), read from u, is
   u, w_{i−1}, s_{i−1}, seg_i, s_i, w_{i+1} in one fixed direction for every i. Each ring-2 x must also have the matching
   contiguous arc in rot(x). Part and mirror chirality are where bugs hide.
2. **A locality lemma, decidable over the 71 parts:**
   - every constrained position lies inside the target window;
   - no ring-3 position and no 9+ middle is ever constrained;
   - every hub has degree ≤ 8.
3. **B6.**
   - Confirm what `OccursW` / `OccursC` require of K's ring image when hosts sit on ring 2. That image lands on ring 3, where
     B3 says nothing. This is fine if occurrence needs only host-level data, with ring images defined through faces.
   - Check the rotation gap counts at cut and pendant hosts.
   - Check whether mirror occurrences are allowed or need their own proofs.
4. The u-is-host convention (spec §14) is not needed for soundness.

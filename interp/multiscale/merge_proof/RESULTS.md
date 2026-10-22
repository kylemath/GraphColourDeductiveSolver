# Merge step (a_W): a precise statement, two local reductions, and an adversarial attack

22 Oct 2026, ~90 minutes. Code: `mp.py` (library), `exp1`–`exp6.py` (adversaries, offset test, per-renaming table, depth scan, witness search, base-point test); outputs `exp*_*.jsonl`. Labels: [P] proved, [M] measured (SAT exact for the instance), [C] conjecture. R = 0 means only conflict vertices recoloured, as in `wk.py`; w is the min collar width along ∂U that, with the repair zone, makes every pocket of U 1-level (`wc`: collar only).

## 0. Numbers first [M]

All merges use **all 24 renamings** (min R over renamings, then min w for that repair). Sides are weakly 1-level by SAT; where the side has an even number of interior odd vertices, colourings with forced |t| = 2 ("nonzero") and forced t = 0 were added.

| adversary (`exp1.py`) | maps | merges | R | w (collar + zone) | notes |
|---|---|---|---|---|---|
| `strip`: A = width-2 shell strip with up to **57 chords**, all of its pockets crossed by the seam; B = ball | ico10, flip10_1, defect_ico17 | 465 | {0: 81, 1: 384} | {0: 108, 1: 328, **2: 29**} | pocket τ before re-levelling up to **6.08**; R never 2 |
| `lop`: B = wheel of 6 vertices, A = ball of 47–123 | same | 270 | {0: 270} | ≤ 2 | |
| `vorseam`: halves of a ball centred on a vortex, seam through the vortex cluster | same | 234 | {0: 163, 1: 71} | ≤ 2 | |
| `half`: balanced halves of a ball, seam 34–46 | ico10, ico20, flip10_1 | 88 | {0: 46, 1: 42} | ≤ 2 | |
| `cap2`: A holds exactly two vortices (|t_A| = 2 forcible), B a ball | ico10, ico20 | 156 | {0: 143, 1: 13} | {0: 52, 1: 45, 2: 48, **3: 11**} | |
| `cap2big`: two-vortex caps of radius 6–13 (ico10: 163 vertices, ico20: 395–535), B of equal size | ico10, ico20 | 168 | {0: 162, 1: 6} | ico10 {0: 16, 1: 7, 2: 30, 3: 30, **4: 5**}; ico20 {2: 17, 3: 48, **4: 15**} | **first w = 4 in the project** |
| `exp4` depth scan: two-vortex cap A = ball(mid, 10 + k) on ico20, B = ball of the same radius, vortex depth k from ∂A | ico20, k = 1–4 | 171 | {0: 164, 1: 7} | {1: 13, 2: 26, 3: 84, 4: 45, **5: 3**} | w does **not** track k (see §3); conflicts 0–8 |

- **Nothing needed R ≥ 2** in 1,552 adversarial merges (the project's earlier R = 2 cases were, as suspected, artefacts of trying only 6 renamings). `nR` (number of renamings that work at the min R) is typically 16–24: the renaming is rarely tight.
- **w reached 4 (65 merges) and 5 (3 merges)**, all on ico20 two-vortex caps with |t_A| = 2, the fused disc either even with |t_U| = 2 or odd with 3 vortices. All of these have pocket τ ≤ 3 before re-levelling, so the Lipschitz bound w ≥ τ − 1 − O(1) does not explain them.
- **Base-point artefact [M]** (`exp6.py`, ico20, k = 1, 4 merged colourings with |t_U| = 2): the same colouring, with its single pocket walk re-based at six boundary vertices, needs w = (3,1,2,2,1,3), (4,2,3,3,3,4), (2,1,4,2,2,2), (3,1,1,3,3,3). The one-lap τ of `wk.py` (base point = smallest vertex id) is not base-point invariant when |t| = 2 (review1 B); the spread is 2–3 units of w, min over base points ≤ 2 in all four, max 4. This is the size of the whole w ≥ 4 effect, but no w = 4–5 instance has yet been re-based directly; see §3.

## 1. Precise statement of (a_W), and what the collar does [P]

Setting: G a planar triangulation with min degree 5; A, B vertex-disjoint near-triangulated discs with U = A ∪ B a disc; S the seam (edges between A and B). By Jordan, the seam vertices of A form an arc α ⊂ ∂A and those of B an arc β ⊂ ∂B; ∂U = (∂A ∖ α°) ∪ (∂B ∖ β°). Pockets of U: cut U along its internal chords (edges with both ends on ∂U that are not boundary edges), giving a tree of chordless discs P_1 … P_k.

**(a_W, precise).** There are constants R, w such that for all weakly 1-level (c_A, c_B) there are π ∈ S_4 and c_U with (i) c_U proper on U, (ii) c_U = c_A ∪ π c_B outside Z = N_R(conflicts of c_A ∪ π c_B) ∪ N_w(∂U), (iii) τ(P_i, c_U|P_i) ≤ 1 for every pocket of U in its own gauge (with the base-point convention of `wk.py`).

**Which pockets fuse [P].** A pocket P of U is the union of the A-pockets and B-pockets it meets, plus the seam triangles. The chords of A are chords of U iff both endpoints stay on ∂U; an A-chord with an endpoint in the interior of U disappears and its two A-pockets fuse. Each stretch of ∂P inside one old pocket is a 1-ball in P's gauge (Mismatch Lemma W), so τ(P) ≤ j + 1 with j = number of stretches; measured ≤ 6.08.

**What the collar must do [P].**
1. Fix the geometry of each fused pocket: its monodromy ρ_P (a reflection centre q_P ∈ Λ if P holds an odd number of vortices, a translation t_P ∈ 2Λ if even) is determined by the heights of the vortices inside P. Any recolouring of a region Z that contains no vortex of P and is such that ∂P can be pushed off Z inside P ∖ (vortices) does not change ρ_P relative to the fixed part of P. The repair zone N_R(conflicts) is a union of discs around seam conflicts and the collar is an annulus; so **with vortex-free Z, ρ_P after the merge equals ρ_P of the glued colouring**, and weak 1-levelness needs |t_P| ≤ 2 for every even fused pocket (τ ≥ |t|/2).
2. For the glued colouring, t_P = a_P + P_π b_P where a_P (resp. b_P) is the signed, transported sum of the monodromies of the A-pockets (resp. B-pockets) that fuse into P, and P_π ∈ D_6 is the linear part of the renaming (sign is gauge). The renaming is one element of D_6 for the whole seam. So the collar can re-level only if some π makes |a_P + P_π b_P| ≤ 2 **simultaneously for every fused pocket P**; otherwise the collar must reach a vortex, w ≥ depth of the nearest useful vortex, which is unbounded.
3. Given admissible monodromy, the collar's job is Lipschitz: move each stretch of ∂P into one unit ball/cone around ρ_P with the deep interior fixed; w ≥ τ_before − 1 − O(1).

**Lemma M (monodromy obstruction) [P].** If A has two fused-into-one pockets P_1, P_2 with t_1 = t_2 = 2e (aligned after transport) and the B-pockets fusing with them are vortex-free, then |t_P| = 4 for every renaming, so no (R, w) with vortex-free Z works; w ≥ (depth of the A-vortices from ∂U). Such A are weakly 1-level: each pocket only needs |t_i| ≤ 2. **This is the one point where W1 is strictly weaker than LML**: chordless A has a single pocket, |t_A| ≤ 2, and |t_A + P_π t_B| ≤ 2 is achievable by renaming for any t_B. [C] W1 should therefore be strengthened to: for every subtree of pockets of U, the transported monodromy sum has norm ≤ 2 (equivalently, the strict τ of every sub-union of consecutive pockets is bounded, or simply the strict τ(∂U) ≤ 1 plus pocket τ ≤ 1). `exp5.py` (two two-vortex caps joined at a neck, 315 tries) produced no chorded disc, so there is no SAT witness yet; realisability in min-degree-5 maps with deep vortices is [C, 85%] (on domes two caps touching along one edge suffice).

## 2. The two local statements

**(i) Seam filling [P → C].** With admissible monodromy, the seam problem is the band-filling of `closing/round2` with two free ends. Along the seam the offset o = H_A − P_π H_B − c has diameter ≤ 2K(j_A + j_B) + 2|t| (Lemma W plus the base-point term); with the free ends the renaming constant c is free, and the data (R ≤ 1 everywhere, even with 57 crossed pockets) say the effective offset is much smaller than the bound.

**(ii) Collar re-levelling of a two-arc pocket boundary [M].** `exp2.py`: a chordless ball U on ico20 (radius 5–11, boundary 30–64), colourings whose boundary is level on two arcs with prescribed offset |q| ∈ {1, √3, 2, 2.6, 3, 3.46}, interior arbitrary; interior fixed at depth > w. Vortex-free U: feasible offsets ≤ 2, **w ≤ 1** at every radius (r = 5, 6, 7; offsets 3 and above are infeasible, i.e. two level arcs cannot be 3 apart on a flat disc). Two-vortex U (|t| = 2 possible): offsets up to 3 feasible, **w ≤ 2** throughout (r = 11, boundary 64). In isolation the two-arc offset is a bounded-width operation [M, lengths ≤ 64]; the large w of §0 come from the merge geometry, not from the arc offset.

## 3. Adversarial attack: what broke and what did not

- Many pockets crossed (`strip`, up to 57), lopsided (`lop`), vortex-dense seams (`vorseam`, defect maps), balanced long seams (`half`): R ≤ 1, w ≤ 2. **No R ≥ 2 anywhere.**
- Two-vortex caps with |t| = 2: **w = 4 (65 merges) and w = 5 (3 merges)**, with R ≤ 1. By vortex depth k in A, ico20 `exp4`:
  - k = 1: w {1: 13, 2: 5, 3: 21, 4: 9}; k = 2: w {2: 11, 3: 31, 4: 5, 5: 1}; k = 3: w {2: 5, 3: 24, 4: 18, 5: 1}; k = 4: w {2: 5, 3: 8, 4: 13, 5: 1}.
  - w does not grow with k, so the collar is **not** being forced to swallow the vortices: Lemma M is not what is biting here (B was vortex-free or odd, so some renaming always gives |t_U| ≤ 2).
  - The base-point test (`exp6`) shows the same colouring needs w anywhere in {1, …, 4} depending only on where the lap starts, and ≤ 2 at the best base point. With |t| = 2 the one-lap unit ball forces H_0 = p − t/2 and H_m = p + t/2 exactly at the arbitrary base vertex, which pins two boundary heights; moving them costs collar width. This is the review1-B caveat made quantitative: **w ≥ 4 is most likely an artefact of the base-point convention [C, 75%]; the direct re-basing of a w = 5 instance is still to be done.** A base-point-free definition (min over base points, or the tube/cylinder radius with |t| ≤ 2 imposed separately) is needed before w can be called bounded; with the current definition the measured w ≤ 3 of `hierarchy/weak` was lucky.
- Calibration. [M] 1,552 merges, 3 maps + ico20, sides up to 546 vertices, seams up to 47, all 24 renamings. [C, 80%] with monodromy-admissible fusions and a base-point-free τ, (a_W) holds with R ≤ 2, w ≤ 3. [C, 85%] (a_W) **as stated is false** for the pocket-sum reason of Lemma M (needs a concrete witness; `exp5` neck construction to be redone with explicit two-cap unions sharing one edge). [C, 60%] the R = 3 closings of `closing/` on Eulerian |t| = 2 seams are the same base-point effect.
- Next: (1) build the Lemma M witness explicitly (two caps glued along an edge, SAT with the big-walk constraint already in `mp.sat2`); (2) rerun `wk.py` with τ = min over base points (or the strict τ(∂U) ≤ 1 added to W1) and re-measure w; (3) add the strict sub-union monodromy condition to the W1 invariant and check the 3,100 merges still pass.

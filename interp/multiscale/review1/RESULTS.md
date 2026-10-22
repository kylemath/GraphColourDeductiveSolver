# Review 1: numerical check of the three claims (buried w=+2 vortex, minimal-winding invariant, hub lock)

22 Oct 2026, ~75-minute time box. Code in this folder: `rv.py` (winding w(v), hex-disc "pillow" spheres, crater SAT, minimal-winding cardinality constraints, hub spheres), `t1.py`..`t7.py` with outputs `t*.jsonl` / `t*.log`. τ, levels, R and the renaming convention are those of `../levelling/RESULTS.md` and `../closing/RESULTS.md` (R = 0 means only conflict vertices are recoloured). Labels: [P] proved, [M] measured (SAT exact for the instance), [C] interpretation.

**w(v)** is computed as (Σ over the faces at v of the triangle chirality)/3, chirality = +1 if the edge labels read ccw are a rotation of (1,2,3). This gives w=±2 for the link a,b,c,a,b,c, 0 for a,b,a,b,a,b, and ±1 at every degree-5 or degree-7 vertex. It is the reviewer's winding.

## 0. Numbers

| claim | test | result |
|---|---|---|
| 1(i) crater disc D_d, w(centre)=+2, w=0 at all other interior vertices | SAT, d=2..8 (`t1.py`) | exists for every d, **min τ = 1 exactly** (τ²≤3/4 UNSAT for all d, up to 31 s at d=8). Our definition accepts it as 1-level. The reviewer's claimed τ=1/√3 (our √3/2, flat) is **false** for d≤8; their explicit D_2 construction is proper, has w=−2 at the centre, w=0 elsewhere, and τ = 1, not flat. |
| 1(ii) crater A + flat 3-coloured B, lattice merge in U=D_{2D}, crater at distance D=2..7 from the seam | `lev.merge`, all 24 renamings (`t2.py`) | **R = 0 for every D** (also R=0 with B a random level w=0 colouring). τ(U)=1 after the merge. Predicted R ≥ d−2: **refuted**. |
| 1(ii) sphere: pillow D_d(crater) ∪ D_d(flat), d=2..8 | `closing_R` (`t2.py`) | **R = 0 at every d** (n up to 386). |
| 1(ii) dome: ico10 / ico20, crater at the face centre, A = B_ρ(crater), ρ=2..10, B = rest level | `closing_R`, 2 seeds + one minimal-winding B (`t6.py`, `t6b.py`) | **R ≤ 1 in all 20 closings** (ico10 ρ=2..5: R hist {0:9, 1:5}; ico20 ρ=4..10: {0:5, 1:3}). No growth with ρ (crater depth 13 from the nearest odd vertex at ρ=10). |
| 1(iii) did our level colourings contain even-degree \|w\|=2 vertices? | scan of 40 stored colourings + 96 regenerated `level_col` colourings of E1 balls (`t3.py`) | **Yes, massively.** Stored: 328 craters among 9,272 fully coloured interior vertices (3.5%). Regenerated: 691 among 9,750 (7.1%); **92 of 96 clusters** contain at least one. The closing worst cases (`e4_R3`, `e6_R3`) have 100–150 craters per side. The case was never "not injected"; it is the generic case. |
| 2(i) minimal interior winding (w=0 even, \|w\|=1 odd) + τ ≤ 1 | all 192 E1 balls, n ≤ 317, up to 164 vortices (`t4.py`) | **192/192 feasible**, 0 unknown. Min τ unchanged by the constraint: √3/2 in exactly the 38 clusters that had √3/2 unconstrained, 1 otherwise. |
| 2(i) on chorded clusters (weak invariant, every pocket τ ≤ 1) | all 166 recursion-failure clusters with n ≤ 1,200 (`t7.py`): up to 47 chords, 584 vortices | **166/166 feasible with minimal winding** (0 unknown, max 6.5 s each). Whole-boundary τ ≤ √3 with minimal winding: 12/12 small ones. |
| 2(ii) does τ ≤ 1 force Burgers vector t = 0? | forced-t SAT on the 80 even-parity E1 balls, with and without minimal winding (`t4.py`) | **No.** 25 Eulerian balls: t=0 (trivially). 55 with vortices: **t=0 is impossible in 42** (all 11 two-vortex and all 10 six-vortex balls among them), possible in 13. Minimal winding never changes this (42/42 still UNSAT, 13/13 still SAT). The level colourings of those 42 carry \|t\| = 2 with τ = 1. |
| 3 hub lock | icospheres with B_{r−1} collapsed to a hub of degree 18, 24, 30, 36; hub at distance 0–3 from the seam, including the split where **all** hub neighbours are seam vertices; 72 closings (`t5.py`) | **R ≤ 1 in all 72** (hist {0: 23, 1: 49}). Freeing the hub in addition to N_R(conflicts) changed R in **0 of 72**. No blow-up. |

## 1. Why the counterexample fails [P]

- The reviewer's w(v) is a chirality winding, not a height monodromy. In our height (face sign σ = the geometric up/down 2-colouring, cuts only at odd vertices, `levelling` §1.1) the increments around a crater are e_ab − e_bc + e_ca − e_ab + e_bc − e_ca = 0. So **a crater has zero monodromy**: h is single-valued through it, the link uses only 3 colours, the vertex is properly coloured. The lower bound R ≥ d−2 of `tilt_aware.md` F3 is for a *hole* whose link uses all 4 colours (monodromy 2√3); that is a colouring of G−v that does not extend to v, not a level leaf. The two objects were conflated.
- Nothing local pins a crater: Σ_v w(v) restricted to a colour class equals the degree of the map G → tetrahedron, a global even number, and craters/anti-craters of w=∓2 can be created inside the seam collar at no cost (`t2`: the merged colourings at R=0 contain 1–4 craters in U, the original one untouched). Hence R=0 above.
- What a crater *does* do: it forces τ = 1 rather than √3/2 when the rest of the disc has w=0 (`t1`; with two craters allowed, a flat boundary is again possible for d ≥ 3). That is inside the invariant.

## 2. The proposed fix [M/C]

- Minimal interior winding is cheap and always available on our leaves (192/192, with the same min τ), and on chorded unions under the weak invariant. It is **consistent** with LML, and can be added. [C] It is also unnecessary: the recursions already succeeded with 3–7% craters everywhere.
- **Burgers vector 0 cannot be required.** 42 of the 55 non-Eulerian even balls (including every two-vortex dome cap, as `tforced.py` found) have *no* 4-colouring with t = 0, with or without minimal winding. τ measured "in R² itself" is then unbounded on legitimate leaves, so the strengthened invariant is unsatisfiable at the leaves. Our τ deliberately works in the quotient and bounds |t| ≤ 2τ; `closing` Lemma 1 then matches t across the seam. The reviewer's mod-4 sum of w is the degree of the colouring map and is automatically consistent; it adds no constraint beyond propriety.

## 3. Hub [M]

- Degree-18–36 hubs at distance 0–3 from the seam, in the small side and in the large side, with up to 36 hub neighbours on the seam: R ≤ 1 always, same as the hub-free domes. The hub's link, forced into 3 colours, is a flat 3-coloured cycle: exactly the easy case (F1/F2). Unbounded degree remains outside the finite checks (`levelling` §5), but this particular mechanism does not produce it.

## 4. Calibration

- Everything here is SAT-exact on the instance; sample sizes are small (crater: 7 discs, 7 pillows, 20 dome closings, 12 lattice merges; hub: 72 closings on 4 spheres). None of it is a proof of (a) or (b).
- Not done: craters placed *on* the seam band of a large closing, several craters in one side, and hubs of degree > 36 or with odd-degree neighbours. The ico20 minimal-winding level SAT on a 3,940-vertex side was too slow for the box (killed); all other calls took < 31 s.
- [C, ~90%] Claim 1 is not a counterexample to Conjecture LML at any d; [C, ~85%] the Burgers-0 part of claim 2 is unachievable in general; [C, ~80%] claim 3 does not raise R for bounded hubs of degree ≤ 40.

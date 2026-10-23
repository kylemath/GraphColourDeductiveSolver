# Multi-front (turn-taking, graph-Voronoi) vortex-restricted induction

23 Oct 2026, about 2 h (over the 90 min budget, mostly run time). This follows up `../scale/RESULTS.md` and `../unbounded/RESULTS.md`. Labels: [P] proved or by construction, [M] measured (exact on the instance, within node and candidate caps), [C] conjecture.

## Files

- `mf.py` is the induction and driver. It imports `../unbounded/vr.py` (FrontierVR) and `mc.py` unchanged.
  - Spec: `map:m:seed[:opts]`.
  - Options: `ren=1` (try all 24 colour renamings of the other component at a first contact), `mb=2` (merge allowance, below), `tz=1` (a flat hole must close with t = 0), `K` (default 5), `Rmax` (default 4).
- Data:
  - `main.jsonl`: 113 runs, with the per-step records `recs`.
  - `summary.txt`: the output of `summ.py`.
  - `duals.json`: the Voronoi duals of the cells.
- Helpers:
  - `chk_parity.py`: gauge sanity check.
  - `t1.py`: smoke test.
  - `mkspecs.py`, `specs_*.txt`: the job lists.
- Logs: `main*.log`.

## Model (as implemented)

**Seeds.** m seed faces are placed by farthest-point sampling, so they are pairwise disjoint and non-adjacent.
- The achieved minimum pairwise distance (`mind`) is about diam/√m: ico10 (diam 30) gives 25, 14, 9–10, 6–7 for m = 2, 4, 8, 16.
- Each seed is a **tag** (a front).

**Turns.** Tags take turns adding one uncoloured vertex adjacent to their own cell. Equal speed, so the cells are graph-Voronoi cells.
- **A merged component still gets one turn per tag.**
- If no candidate of a tag works at R ≤ 4, the tag **waits** and the others go on.
- The run FAILs only when a full round makes no progress.
- "ok (strict)" means no tag ever had to wait.

**Candidates.** A candidate is an uncoloured v whose coloured neighbours form one rotation arc of length ≥ 2, or several arcs (a merge or a self-touch), or the whole link (closing a hole).
- Up to K = 5 candidates are tried, those with the most coloured neighbours first.
- The choice is: minimal R first, then fewest cuts, then smallest Σ|t|, then fewest recolourings.

**Boundary.** It is computed locally from the rotation system.
- Dart a→u is a boundary dart iff the cw-successor of a around u is uncoloured.
- succ(a→u) = u→c, where c is the next coloured neighbour after a.
- So there is one walk per complement component. Walks may be pinched (a vertex visited twice). An annulus has two walks.

**Gauge.** At a corner, the flip is the parity of the number of edges on the region side, deg − 2 − gap. For a simple corner this is pi.signs.
- Sanity check [M] (`chk_parity.py`, 1 900 walks on ico4 and L18, m = 1 and m = 4, including 16 pinched walks): the holonomy of every walk equals the parity of the odd-degree vertices on the gap side plus those on the walk. **0 mismatches.**

**Invariant.** It is the one in `vr.py`, variant `any`, imposed on **every** walk created at the step.
- Circumradius ≤ 1 after jumps in 2Λ; |t| is free.
- Positions are persistent darts.
- Departed positions go to the darts at v.
- New positions may be opened only when dn > 0.
- The budget NB = #departed + dn is **pooled over all new walks** (an exact multi-walk DFS with a remaining budget).

**Repair.** The free set is the ball of radius R around v in the coloured graph.
- **Boundary vertices of other walks are frozen.**
- So at a seam, **both fronts' vertices near v are free**: the incremental seam of the question.

**`mb=2`.** At a first contact (v touches two components), NB += 2 and the darts at v may carry new cuts. This is one entry/exit jump pair that re-levels the sub-loop of the other front by a 2Λ vector.
- **This is a modelling choice. It adds 2(m−1) positions not charged to vortices.**

The main configuration is `ren=1,mb=2`.

## (1) Completion vs m [M]

| map (n) | m = 1 | m = 2 | m = 4 | m = 8 | m = 16 |
|---|---|---|---|---|---|
| ico4 (162), 5 seeds | 5/5 strict | 5/5 (4 strict) | 5/5 (4 strict) | 5/5 (1 strict) | – |
| ico10 (1002), 6 seeds | 2/6 | 2/6 | 1/6 | 2/6 | 2/6 (0 strict) |
| ico10, `tz=1`, 4 seeds | 2/4 | – | 3/4 | – | 3/4 (0 strict) |
| ico16 (2562), 1 seed | FAIL at 2560/2562 | – | – | – | UNK (cand cap) at 2535 |
| L18 Opus (890), 3 seeds | 1/3 | – | **3/3** (1 strict) | – | 1/3 |
| L18, `tz=1`, 2 seeds | 1/2 | – | 2/2 | – | 2/2 (0 strict) |
| defect10/flip10/defect14/defect22 (1002–4842), 1 seed each | 4/4 strict | – | 4/4 strict | – | 4/4 (only defect10 strict) |
| rigid helix_100 / helix_200 / w02_200 / w021_200 | FAIL at n = 10 / 10 / 15 / 14 | – | FAIL 87/100, FAIL 184/200, FAIL 198/200, **ok** | – | – |

**Max R ≤ 4 in every run.** Every completed colouring is proper.

**ico failures.**
- All 20 ico10 FAILs with `ren=1,mb=2` (plus 1 UNK at 995) are at the last 1–3 vertices: the final hole. This is the flat-remainder t-obstruction of `scale/` §3, and it is the same for every m.
- `tz=1` removes most of them: 8/12, against 9/30 without it. It helps as it did for one front.

**L18 at m = 1.** It fails at n ≈ 210–230: nodd = 1, and all five candidates self-touch. This is a shape problem of greedy single-front growth on the long tube. m = 4 does not have it.

**Ablation at first contact (ico10 m = 4, 8; L18 m = 4; 2 seeds each).**

| config | ico10 | L18 |
|---|---|---|
| `ren=0,mb=0` | 1/4 | 0/2 |
| `ren=1,mb=0` | 2/4 | – |
| `ren=0,mb=2` | 0/4 | – |
| `ren=1,mb=2` | 3/4 on the same seeds | – |

- The `ren=0,mb=0` failures sit in the **middle** of the run, in collision zones. On ico10:8:2 the failure is at 884/1002, with every candidate touching 2–3 tags. On L18 there are 300 blocked turns.
- With `mb=2` the run reaches the end, where the final-hole obstruction stops it.
- The smoke test ico4 m = 2 with neither option FAILs **at the first contact itself**: every R ≤ 4 fails for all merge candidates. The same map succeeds with `ren` or with `mb`.
- **[M] So two independently grown fronts cannot in general be zipped at R ≤ 4 by recolouring alone.** At contact they need a relative relabelling (a renaming) and/or one 2Λ jump pair at the junction. This is the incremental analogue of the twisted-seam offset T₂ − T₁ ∈ 2Λ.

## (2) Peaks of |t| and cuts [M]

"Pre-contact" means the steps before the first merge, when every front is a separate disc. "Global" means over the whole run.

| map | m | pre-contact peak cuts, abs t per front | global peak cuts, abs t |
|---|---|---|---|
| defect22 (4842) | 1 / 4 / 16 | 34, 22.3 / 19, 16.0 / 9, 10.4 | 34, 22.3 / **70, 23.1** / **97, 38.9** |
| defect14 (1962) | 1 / 4 / 16 | 23, 15.9 / 9, 12.5 / 4, 5.3 | 23 / 38 / 58 |
| defect10 (1002) | 1 / 4 / 16 | 16, 14.0 / 8, 7.2 / 0, 0 | 16 / 25 / 44 |
| flip10 (1002) | 1 / 4 / 16 | 16, 14.4 / 6, 8.0 / 1, 2.0 | 16 / 25 / 39 |
| ico10 | 1 / 2 / 4 / 8 / 16 | 5.7, 7.2 / 2, 4 / 0, 0 / 0, 0 / 0, 0 | 5.7, 7.2 / 6.0, 8.5 / 5.0, 6.9 / 6.3, 8.5 / 7.0, 8.5 |

- **Per front, before contact, the peak cuts fall roughly like 1/√m.** defect22: 34 → 19 → 9, against the predicted 34 → 17 → 8.5. |t| falls less, roughly like m^−0.3.
  - Caveat: a front is pre-contact only until the first contact, so it has not reached n/m by then.
  - On ico, the fronts are flat until contact (no odd vertex inside), so t = 0 and there are 0 cuts [P: a flat disc has a single-valued height].
- **The global peak grows with m.** defect22: 34 → 70 → 97 cuts, |t| 22 → 23 → 39.
  - Positions persist through merges, so the merged walk carries every front's cuts.
  - The merged boundary is long: it is the whole Voronoi skeleton until it zips.
  - **Splitting into fronts does not lower the peak of the global invariant. It raises it.**

## (3) Collisions [M]

Events are classified by how many tags the new vertex v touches:
- (a) a seam step = a Voronoi edge (2 tags);
- (b) a junction step = a Voronoi vertex (3 or more tags);
- splits (a hole or annulus is created) and closes (a hole is filled).

The table pools the m > 1 runs in `ren=1,mb=2`.

| event | ico (39 runs): n, share with R > 0 | L18 (6 runs) | dense (8 runs) |
|---|---|---|---|
| interior growth | 19 310, 0.3% | 3 730, 0.6% | 13 771, 1.3% |
| first contact (merge) | 211, **0%** ¹ | 54, 0% | 72, 0% |
| (a) seam zipping (Voronoi edge) | 5 427, **7.3%** (R ≤ 4) | 1 192, 3.9% | 2 734, 8.2% |
| (b) junction step (Voronoi vertex) | 456, **18%** | 122, 5.7% | 131, 24% |
| split (hole created) | 68, 26% | 28, 11% | 330, 15% |
| hole close, ≤ 2 tags | 126, **55%** (R up to 4) | 23, 65% | 301, **83%** |
| hole close at a Voronoi vertex (≥ 3 tags) | 24, 54% | 8, 25% | 37, 73% |

¹ The first-contact numbers are biased: a merge is taken only when it succeeds at minimal R. Otherwise the front grows elsewhere or waits.

**Waiting turns** are classified by the tags touched by the blocked candidates:
- ico: V-vertex 40+, V-edge 58+.
- L18: V-vertex 40, V-edge 11.
- dense: V-edge 20, V-vertex 1.
- rigid: cell interior 78.

**Twisted seams.**
- **No seam ever became infeasible once zipping had started** in `ren=1,mb=2`.
  - Seam steps need R > 0 in about 4–8% of cases, about 25× the interior rate. The max is R = 4.
  - The incremental seam is repairable step by step, unlike the refuted all-at-once glue.
- **But the twist resurfaces as holes.**
  - The zipping seams enclose many small holes: 512 holes in m > 1 runs, against 59 in m = 1 runs.
  - Of these, 90 were created with **no odd vertex inside and |t| > 0**, i.e. with a monodromy mismatch around the hole (|t| = 2, 2√3, 4, up to 16.4).
  - Such a hole cannot be filled properly unless the repair ball reaches an odd vertex ([P], as in `scale/` §3).
  - This is exactly where R > 0 is concentrated: 55–83% of hole closes need R ≥ 1, up to R = 4.
  - The dominant terminal failure on ico and L18 is such a hole.
- **Holonomy at Voronoi vertices.** |t| of the hole walk just before it closes:
  - ico: 0 (11), 2 (4), 2√3 (5)
  - L18: 0 (7), 2√3 (1)
  - dense: 0 (9), 2 (25), 2√3 (3)

  On ico and L18, a hole with |t| > 0 is a mismatch. On dense maps, odd vertices inside the hole usually absorb t = 2.
- `tz=1` forces flat holes to close with t = 0 at creation. It cuts the mismatched holes from 90/512 to 6/53. On ico10 it raises completion (strict + waits) to 8/12. The pressure moves to the junction or split steps, as for one front.

## (4) Voronoi dual [M] (`duals.json`)

For each run with m ≥ 4, `duals.json` records:
- the cell adjacency edges and the triangles (faces with 3 distinct tags);
- the cell sizes;
- `is_triangulation` (E = 3m − 6 and T = 2m − 4).

Results:
- **Triangulation**: ico4 10/10, dense 6/8, ico10 20/38.
- **Not a triangulation**: L18 0/12, rigid 0/4. The rigid duals at m = 4 are a path: the cells line up along the helix.

The non-triangulated cases have 4-cell junctions (missing diagonals) or elongated cells.

## (5) Rigid stacked maps (`opus_attack/control/rigid`) [M]

- **m = 1 (greedy single front)** fails at n = 10–15. nodd = 0 and every candidate self-touches: the thin stacked maps make greedy single-front growth wrap around itself immediately. This is worse than `vr.py`, which reaches n ≈ m/2 + 9.
- **m = 4** gets much further:
  - helix_100 reaches 87/100 (vr: about 59);
  - helix_200 reaches 184/200 (vr: about 109);
  - w02_200 reaches 198/200 (vr also fails at the last steps);
  - **w021_200 completes** (vr fails at the end for m ≥ 150).
- Max R is 4. 78 waiting turns were all cell-interior.
- **This gain is mostly the 2(m−1) merge positions from `mb=2`.** These maps have only 4 odd vertices, and their failure in vr is a missing cut position (the tilt ≈ L/4). The merges supply positions that no vortex pays for. So **I do not count this as evidence that multi-front growth beats rigidity** [C, 70%].

## Verdict

- [M] **The incremental seam works locally.**
  - With a renaming and one 2Λ jump pair allowed at each first contact, every first contact and every seam step was repairable. 5 427 seam steps on ico alone, at R ≤ 4.
  - Without either allowance, fronts die in the collision zones. In one ico4 run, the first contact itself was infeasible at R ≤ 4.
- [M] **It does not beat the single front on completion.**
  - On ico10 the rate is 1–2 of 6 for every m.
  - The global peaks of cuts and |t| grow with m, because merged walks carry all fronts' positions.
  - Only the per-front, pre-contact peak shrinks, about like √(n/m).
- [M] **The twisted-seam obstruction is not removed. It is converted into holes.** Junctions and closing seams leave flat holes with a monodromy mismatch |t| ∈ {2, 2√3, …}. These need R that reaches an odd vertex, and they cause the terminal failures. Their number rises with m because there are more holes: 90 mismatched holes (out of 512) in m > 1 runs vs 11 (out of 59) in m = 1 runs. The share per hole is the same, about 18%.
- [C, 65%] A multi-front scheme would need a coherence rule at contact: choose the renaming and jump so that the seam's future holes are t-neutral (a two-sided rule like `tz`, applied per seam). Without it, more fronts mean more flat holes to close.

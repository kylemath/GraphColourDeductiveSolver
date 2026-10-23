# Vortex-restricted, uncapped cuts: `any` colours 13/14 maps, `nc` colours 6/14; both are non-vacuous

23 Oct 2026, about 75 min. This follows up `../RESULTS.md`. Labels: [P] proved (by construction or by an argument given here), [M] measured (exact on the instance), [C] conjecture.

## Files

- `vr.py`: the induction. It patches `mc.Frontier` and subclasses `mcstep.MCInductor`.
- `faildiag.py` → `faildiag.log`: diagnosis of the failing steps.
- `sanity_vr.py` → `sanity_vr.{log,json}`: static sanity checks.
- `vac.py` → `vac.{log,jsonl}`: non-vacuity probes along real runs.
- Run logs: `runs.jsonl` (main), `runs_cap.jsonl` (flip7_2 rerun with larger caps), `runs_slide.jsonl` (sliding variant).
- Failure instances: `fail_*.pkl`.

## Model

These are the rules as implemented.

- **Invariant.** After the cuts, the lifted boundary walk must have circumradius ≤ 1, decided by the exact hexagon DP of `mc.py`.
  - Each jump lies in 2Λ. A position either carries |s| = 2 or is dormant (s = 0).
  - Even case: the jumps sum to t. |t| is free otherwise.
  - Odd case: one of the cuts is the reflection cut.
  - Variant `nc`: no two jumps are opposite. Variant `any`: opposite pairs are allowed.
  - **There is no cap on the number of cuts.**
- **Positions are persistent objects.**
  - A position keeps its edge (a, b) while (a, b) stays on the boundary.
  - When its edge leaves the boundary (the edge lies on P), the position moves to one of the two new edges at v. If more than two positions leave at once, the extras merge.
  - New positions may be opened **only at a step that encloses dn > 0 new odd vertices**. At most dn open per step, on the edges at offset −1, 0, +1 of v.
  - The DP enforces this exactly: it counts the cuts placed on non-carried edges and requires that count ≤ #departed + dn.
  - Jumps are re-optimised at every step (the `att` convention). So the merge condition |Σs| ≤ 2 holds automatically.
- **Consequence [P].** #positions ≤ Σ dn = nodd (enclosed odd vertices) at every step. So on any closed walk the invariant is at least as strong as tau_{J = nodd} ≤ 1 with cuts anywhere.
- Rmax = 4; candidates are kept by fewest cuts; R escalates as in `mcstep.py`.

## (1) Completion and max R [M]

| map / ordering | n | `nc`: result, max R | `any`: result, max R |
|---|---|---|---|
| ico4 left | 162 | **ok**, R 2 | **ok**, R 2 |
| ico4 right | 162 | **ok**, R 2 | **ok**, R 2 |
| ico4 rand1 | 162 | **ok**, R 4 | **ok**, R 2 |
| ico4 rand2 | 162 | FAIL n = 135 (nodd 8), R 3 | **ok**, R 3 |
| ico10 left | 1002 | **ok**, R 4 | **ok**, R 4 |
| ico10 rand1 | 1002 | FAIL n = 758 (nodd 8), R 1 | **ok**, R 4 |
| ico10 rand2 | 1002 | FAIL n = 806 (nodd 8), R 2 | FAIL at the **last vertex**, n = 1002 (L = 3), R 3 |
| flip7_1 left | 492 | **ok**, R 3 | **ok**, R 3 |
| flip7_1 right | 492 | **ok**, R 4 | **ok**, R 3 |
| flip7_1 rand1 | 492 | FAIL n = 185 (nodd 8), R 0 | **ok**, R 3 |
| flip7_2 rand1 | 492 | FAIL n = 234 (nodd 24), R 2 ¹ | **ok**, R 3 |
| defect7_1 left | 492 | FAIL n = 302 (nodd 6), R 0 | **ok**, R 3 |
| defect7_1 rand1 | 492 | FAIL n = 204 (nodd 10), R 0 | **ok**, R 4 |
| defect10_1 rand1 | 1002 | FAIL n = 338 (nodd 10), R 4 | **ok**, R 3 |
| **total** | | **6 / 14** | **13 / 14** |

¹ This run first stopped with "cand cap with no extension" at the default caps. Rerunning with cand cap 2·10⁵ and node cap 2·10⁶ gives a genuine FAIL at the same step.

- **Max R ≤ 4 everywhere.** 85–99% of steps need R = 0. Every completed colouring is proper.
- Compared with the capped runs:
  - Before, every 492- and 1002-vertex map failed at J = 2, 3, 4, 6, 8 except ico10-left.
  - **`any` now colours all of them except ico10-rand2.** That one fails only at the final triangle: even uncapped cuts anywhere with R ≤ 4 cannot carry the accumulated t. This is the same last-vertex obstruction the J = 4 run hit.
  - `nc` colours ico10-left and both flip7_1 canonical orders. It fails on every random order of the large maps.

## (2) Simultaneous cuts vs enclosed odd vertices [M]

- **Bound [P].** active cuts ≤ positions ≤ nodd, from the model.
- **Measured max.** Over all 28 runs, max (active cuts / nodd) = 1.0. It is reached only for nodd ≤ 12.
- **ico maps (nodd ≤ 12).**
  - Peak active cuts: 1–2 (left/right orders) and 4–6 (random orders).
  - Peak positions: 3–10.
  - Cuts fall back to 0–2 at nodd = 12.
- **flip / defect maps (nodd up to 573).** Active cuts grow about nodd/2 early, then saturate and decline:

  | run | active/positions at nodd = 10 | at nodd ≈ 50–150 | at the end |
  |---|---|---|---|
  | defect10_1 any | 7/10 | 20/46 (at 50), 24/61 (at 150) | peak 32 active / 75 positions at nodd 573 |
  | flip7_1-rand any | 7/10 | 17/38 (at 50) | 2/12 at nodd 300 |
  | flip7_1-left nc | 4/10 | 10/21 (at 24) | 1/4 at nodd 250 |

- So active cuts are **not** O(1). They peak at about 4–6% of nodd on the large maps (13–32 cuts), and they grow roughly linearly with the boundary length rather than with nodd.
- **What the `nc` failures need [M] (`faildiag.log`, R = 0).**
  - Uncapped cuts anywhere need **≤ the number of held positions** (e.g. 9 vs 9, 6 vs 7, 3 vs 4). One exception is flip7_2: 7 cuts vs 12 held, but 24 enclosed odd vertices.
  - Each needed cut sits **0–2 edges from a held position** (rarely 6–31).
  - Letting every held position slide by d = 1 (6 cases) or d = 2 (2 cases) makes all 8 `nc` failures feasible, with no extra cut.
  - Extra cuts in the vortex window (+1 or +2) never help.
  - **The count is fine. The bookkeeping of where a position sits is too rigid.**

## (3) Cuts at non-vortex steps [M]

- **Creation at a non-vortex step is forbidden and never happens.** `newcut_nonvortex = 0` in all 28 runs (the assertion in `vr.py` holds).
- **No step fails for want of a non-vortex cut.**
  - All 8 `nc` failures are at vortex steps (dn = 1, or 3 for flip7_2). There, extra cuts in the window do not help, but 1–2-edge slides do.
  - The one `any` failure (ico10-rand2, n = 1002) is at a non-vortex step: the last vertex, L = 3, dn = 0. One or two extra window cuts do **not** fix it, and neither do uncapped cuts anywhere, so it is not a missing-cut failure.
- **Side experiment: positions may slide ±1 or ±2 per step** (`runs_slide.jsonl`, `nc`). It is **not** better: 12/28 ok, 8 of them on the ico maps.
  - The slide is greedy. The count-only cap was also matched only up to `nmatchfail` > 0, so this variant is a relaxation in count but not in position.
  - Here 4 failures at non-vortex steps **are** fixed by one extra window cut: ico4-R d = 2 at n = 117; flip7_1-rand d = 2; flip7_2 d = 2; ico10-rand2 d = 2 at n = 1000.
  - So sliding moves the pressure onto non-vortex steps. The fixed-position rule (main run) never does.

## (4) Sanity: the restriction keeps the invariant non-vacuous

**Static walks [M] (`sanity_vr.log`).** K_min is the minimum number of cuts, uncapped and anywhere. The vortex-restricted invariant rejects a walk whenever the region it bounds encloses fewer than K_min odd vertices.

| walk | K_min (`nc`) | K_min (`any`) | verdict |
|---|---|---|---|
| c\* strips, m = 4..32, w = 2, 3 (t = 0) | 6, 6, 12, 12, 24, 24, 48, 48 | 4, 4, 8, 8, 16, 16, 32, 32 | **flat patch, nodd = 0 [P], so 0 positions are allowed and every strip is rejected.** K_min = 1.5m (`nc`) and m (`any`): even a budget that grows with nodd needs Θ(L) vortices. |
| smeared slopes, t = 2, L = 12, 24 | 1 | 1 | accepted with one cut |
| smeared slopes, t = 2, L = 48 | 4–5 | 3–4 | rejected unless ≥ 4 (`any`: ≥ 3) odd vertices are enclosed |
| smeared slopes, t = 2, L = 96 | 8–10 | 6–7 | rejected unless ≥ 8 (≥ 6) are enclosed |
| smeared slopes, t = 2, L = 192 | 19, 29, ∞ | 13–19 | rejected unless ≥ 19 (≥ 13) are enclosed; one slope is infeasible for `nc` at any count |

- For t = 2 the region needs nodd ≥ 2. A t = 2 slope with only the 2 odd vertices it requires is rejected for L ≥ 48.
- **Without the position restriction, the uncapped measure is vacuous [M].** Sample: 300 random lattice closed walks with circumradius > 1.
  - Uncapped cuts anywhere accept **300/300** (`any`) and **253/300** (`nc`).
  - Mean K_min: 14.5 (`any`) and 20.4 (`nc`).

**Along real runs [M] (`vac.log`).** The probes are taken every 25 steps on actual induction states, with the current positions held fixed and no new cuts.

| run | random boundary colourings accepted: held positions / same count anywhere / uncapped anywhere | real colouring with an 8-vertex arc recoloured at random: same three columns | real colouring accepted |
|---|---|---|---|
| flip7_1-rand `any` (19 probes × 60) | **0.3%** / 36% / 100% | **13%** / 72% / 100% | 19/19 |
| defect7_1-rand `any` | **1.8%** / 31% / 100% | **13%** / 71% / 100% | 19/19 |
| ico4-rand1 `any` | **1.1%** / 17% / 100% | **9%** / 38% / 100% | 6/6 |

- The probes on ico10-left `nc`, flip7_1-left `nc` and defect10_1 `any` had not finished at write time.
- **Fixing the positions is what keeps the invariant from being vacuous.** The same number of cuts placed freely accepts 17–36% of random boundaries. Uncapped cuts anywhere accept 100%.
- The restricted invariant still rejects about 87–91% of local 8-vertex perturbations. So it remains a real constraint along the induction, even with up to 75 positions on the large maps.

## Verdict

- [M] **Charging cuts to vortices, with no cap and persistent positions, almost completes the induction for `any`.**
  - It colours 13/14 map/orderings, including every 492- and 1002-vertex map but one, with max R ≤ 4.
  - The exception is the final triangle of ico10-rand2. That is an end-of-induction t-obstruction, not a cut-count one.
- [M] **`nc` (no opposite jumps) colours only 6/14.** Its failures need the same number of cuts as are held, each 1–2 edges off its held position.
- [M] **No step ever needs a cut created at a non-vortex step.**
- [M] **The invariant stays non-vacuous.** c\* strips are rejected outright (no vortices). Smeared t = 2 slopes need Θ(L/10) enclosed odd vertices. On real states only 0.3–1.8% of random boundaries pass.
- [C, 60%] A rule that lets a position slide only across edges where its jump can be transported without increasing the radius would close the `nc` failures. The naive ±1/±2 slide does not, because it is greedy.
- [C, 50%] The final-triangle failure needs a last-step rule: allow the outer face its own cuts, or end the induction one step early.

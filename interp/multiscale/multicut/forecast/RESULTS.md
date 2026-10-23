# Remaining-holonomy forecast as a steering potential (test of the Codex proposal)

23 Oct 2026, about 2 h 10 min on a shared 4-core box, over the 90-minute budget. This follows up `../scale/RESULTS.md` and `../backtrack/RESULTS.md`. The model is unchanged: `vr.py` and `vrs.py` are imported, not edited. Labels: [P] proved (argument given here), [M] measured (exact on the instance, within the usual node and candidate caps), [C] conjecture.

## Files (all in `forecast/`)

**Driver: `fc.py`.**
- Spec format: `map:seed:pol:var[:opts]`.
- Options:
  - `st=tie|soft`: steering mode.
  - `pot=orc|loc`: potential.
  - `r=<int>|all`: forecast radius.
  - `orc=sat0|self`: which oracle colouring.
  - `log=1`: per-step forecast log for all r.
  - `chk=1`: frame checks.
  - `tz=1`: the two-sided rule.
  - `dump=1`: save completed colourings to `cols/`.

**Run files.**
- `runs1.jsonl`: ico10 seeds 21–40 and L18 rand seeds 0–19. Covers baseline, tz, oracle and local steering.
- `runsD.jsonl`: soft steering with the self oracle.
- `runsE.jsonl`: ico16:11 r-grid.
- `scB.jsonl`: baseline with a full forecast log; ico4/6/8 (12 seeds each), ico10 (10), ico14 (3), ico16 (2), L18 (6).
- `dense.jsonl`: defect10_3 and flip10_1.
- `dip.jsonl`: the `dip` primary rule of `bt.py` with d = 0 (no backtracking).

**Analysis.**
- `an.py` and `paired.py` write `tables.txt`.
- `corr.py` writes `corr_out.txt`.
- `sc.py` produces the scaling numbers.

**Oracle colourings.** `orc_<map>_sat0.json` holds a SAT 4-colouring of each map. `cols/` holds completed run colourings.

**Do not use `prefix_bug_runs1*.log`.** Those oracle runs predate the `vn` fix (§0). Their r > 0 oracle rows were deleted from `runs1.jsonl` and rerun.

## 0. What was implemented

**Holonomy is computed exactly from the colouring [P, by construction].**
- Heights are Kondev–Henley heights on vertices. A face with ccw order (a, b, c) and sign σ gives h_b − h_a = σ·e(col a ⊕ col b), and adjacent faces have opposite σ.
- Take a vertex set Q with v1, v2 ∈ Q and vn ∉ Q, where Q and its complement are both connected. The faces that straddle the cut then form one dual cycle through the outer face f0 = (v1, v2, vn).
- Developing the Q-side heights along that cycle from the frame (h(v1) = 0, σ(f0) = +1) gives the affine holonomy g = (ε, a), meaning h ↦ εh + a.
  - It uses only the colours of Q.
  - Around an odd vertex w, the holonomy is the point reflection ρ about h(w).
  - The frame f0 is the same for every prefix and every Q_r, so all holonomies live in one frame. This is the "frame fixed by the cut".
- **One convention difference.** Here an odd vertex that lies *on* the boundary counts as enclosed; `vr.py` counts it as outside.
  - `chk=1` verifies, at every step of 16 logged runs (14 058 steps), that the parity matches up to the boundary odd vertices, and that |a| = |t| whenever no odd vertex lies on the boundary. There were 0 mismatches.

**ORACLE potential.**
- Q_r = the prefix plus every outside vertex within graph distance r of the boundary C, with holes filled.
- hol\*(near) = hol\*(C)⁻¹ ∘ hol\*(Q_r), computed in the oracle colouring col\*. col\* is permuted so that col\*(v1, v2, v3) = (0, 1, 2), as in the run.
- The predicted total is T_r = A ∘ hol\*(near), where A is the candidate's own holonomy.
- P_r = |translation of T_r| when T_r is a translation. When T_r is a reflection, P_r = 0, because an odd number of vortices beyond r remain to absorb it.
- Special cases [P]:
  - P_0 = |t|, the greedy |t| rule.
  - P_all = |t − t\*(C)|, i.e. steer the walk onto the oracle's holonomy trajectory.
  - The composition order matters only up to conjugation, so the norm does not depend on it.
- "Per frontier sector" is implicit: the dual-cycle development composes the near reflections in frontier order along their own developing paths.

**Pitfall, found and fixed [P].**
- vn is always adjacent to v1 and v2, so it is always at graph distance 1 from C.
- With naive hole-filling, every r ≥ 2 swallows the whole outside, and P_r collapses to P_all. The first batch was invalid for this reason.
- Fix: the far region (distance > r) is joined to vn by thin corridors. A corridor is the cheapest outside path, where odd vertices cost 50 and other vertices cost 1. Q pieces that a corridor cuts off are moved to the far side.

**LOCAL potential.**
- Each near vortex w has distance d_w and nearest boundary vertex b_w. Its centre is only known to lie in the Lipschitz disc |c_w − h(b_w)| ≤ d_w.
- P^loc_r = max(0, |translation of A ∘ ρ_{h(b_1)} ∘ … ∘ ρ_{h(b_m)}| − 2·Σ d_w), minimised over both frontier orientations. This is the continuous relaxation of the minimal achievable norm.
- If the composite is a reflection, P^loc_r = 0. If there is no near vortex, P^loc_r = |t|.

**Steering.**
- `tie`: among the admissible min-R candidates, sort by (P_r, cuts, recolourings), then apply the usual SAT extension.
- `soft`: also solve at R_min + 1 and keep the colouring with the lower P_r.

**Oracles.**
- `sat0`: one random SAT colouring per map.
- `self`: a *completed* colouring of the same map **and the same canonical order**, produced by another variant (baseline, tz or local). It exists for 13/20 ico10 seeds and 13/20 L18 seeds. This is the "known future" in the strongest form available here.

## 1. Does the forecast predict the next flux increment? [M]

Baseline runs with `log=1`. An increment is D = t(next even state) − t(current even state), taken over successive even states. The table gives the vector correlation of D with each predictor (`corr_out.txt`):

| predictor | ico10 (49 increments, 10 runs) | ico4–16 (175 increments, 41 runs) |
|---|---|---|
| −t (mean reversion) | **+0.55** | **+0.50** |
| oracle t_r, r = 1 | −0.17 | +0.06 |
| oracle t_r, r = 2 | −0.13 | +0.07 |
| oracle t_r, r = 4…all | −0.10 … −0.11 | +0.08 |
| −(t + t_r), r = 1…all | +0.45 … +0.50 | +0.27 … +0.31 |

- The oracle forecast carries **no information about the next increment** (|corr| ≤ 0.17 at every r).
- Adding it to t *lowers* the correlation of −t, from 0.55 to 0.45 and from 0.50 to 0.28.
- The run's increments already mean-revert on |t| alone.
- Caveat: the oracle here is a SAT colouring. Its holonomy trajectory is far from the run's: P_all is typically 6–10, against |t| ≤ 3.5 (see the log of ico10:21).
- **[P] This is unavoidable for any foreign oracle.** The near centres c_w = h\*(w) are col\*'s heights, and a colouring that agrees with the run on C has different heights at the same vertices. Forecasting the run's own future needs the run's own completion, which is what `self` approximates.

## 2. Steering: completion and peaks [M]

Paired on the same seeds. "last" means a failure at the final vertex with t ≠ 0. Baseline figures are from this driver and reproduce `scale/` exactly: ico10 6/20, tz 8/20, L18 10/20.

| config | ico10 ok / runs (last-vertex fails) | baseline on the same seeds | L18 ok / runs (last-vertex fails) | baseline on the same seeds |
|---|---|---|---|---|
| baseline | 6/20 (5) | – | 10/20 (5) | – |
| tz=1 | 8/20 (**0**) | 6/20 | 12/20 (**0**) | 10/20 |
| dip, primary only (d = 0) | 2/20 (8) | 6/20 | 6/15 (3) | 7/15 |
| oracle `sat0`, tie, r = 0 (= greedy \|t\|) ¹ | 5/7 (1) | 2/7 | – | – |
| oracle `sat0`, tie, r = 2 | 9/20 (4) | 6/20 | 12/20 (3) | 10/20 |
| oracle `sat0`, tie, r = all | 9/20 (2) | 6/20 | 12/20 (3) | 10/20 |
| oracle `self`, tie, r = 2 | 4/13 (**7**) | 6/13 (4) | 11/13 (0) | 10/13 (3) |
| oracle `self`, tie, r = all | 6/13 (**6**) | 6/13 (4) | 10/13 (3) | 10/13 (3) |
| oracle `self`, soft, r = 2 | 8/13 (3) | 6/13 (4) | 1/1 ¹ | – |
| oracle `self`, soft, r = all | 8/13 (3) | 6/13 (4) | – | – |
| local, tie, r = 2 / 8 / all ¹ | 3/6, 3/5, 3/6 (0) | 1/6 (2) | –, –, 8/15 (2) | 6/15 (4) |
| local, soft, r = all ¹ | 4/6 (0) | 1/6 (2) | 10/16 (1) | 7/16 (4) |

¹ Partial: these queues were cut at the time limit. `runsA2.log` stopped at 157 of 192 specs.

**Completion.**
- No oracle variant beats the two-sided rule by more than noise; the binomial s.d. is about 2 runs in 20.
- The largest gain is `sat0` tie at 9/20 on ico10 against 8/20 for tz. A *random* oracle doing as well as the *same-order* one suggests that the effect is tie-break diversification, not forecasting.

**The final-vertex t ≠ 0 failure is not removed by the oracle at any r, even with `self`.**
- With r = all: 2–6 last-vertex failures remain on ico10, and 3 on L18.
- With `self` tie on ico10 it gets *worse* (7 and 6, against 4 at baseline on the same seeds).
- Only the hard two-sided rule (tz) and the local potential remove it: 0 on ico10 and 1–2 on L18 for local, 0 for tz. When no vortex is near, the local potential reduces to |t|, i.e. a soft tz.

**Why the oracle cannot steer on ico [M + P].**
- From `scale/`: at the minimal R on ico there is essentially one admissible candidate (greedy = keep there). So a tie-break has almost nothing to choose between.
- `soft` (R_min + 1) adds choice and lifts `self` from 4–6/13 to 8/13. It still leaves 3 last-vertex failures.
- P_all also over-constrains [P]. In the odd phase it compares the run's reflection centre with col\*'s. But the run will colour the remaining vortex itself, so a "wrong" centre is not fatal. An example is ico4:1: P_all = 3.46 at n = 160, and the run still completes with t = 0.

**Peaks on dense maps (n = 1002) [M].**
- defect10_3: peak cuts 28 → 29 (oracle, r = all) and 29 (r = 2) and 28 (local). Peak |t| 19.1 → 19.1, 24.3, 19.1.
- flip10_1: peak cuts 23 → 27, 23, 23. Peak |t| 20.3 → 19.1, 22.0, 20.3.
- The oracle tie-break does **not** lower the peaks, and sometimes raises them.
- **The local potential is identically 0 on dense maps [P].** Many outside vortices sit at distance 1–2, so 2Σd_w ≫ |t|. Local runs are therefore bit-identical to baseline.
- On ico and L18 the peak cuts change by at most ±0.7 on average (`tables.txt`).

## 3. The radius needed, and how it scales [M + P]

**Seeing is local [M]** (`sc.py` on `scB.jsonl`).
- The random canonical boundary grazes the remaining odd vertices. The median over the run of d_min (the distance from C to the nearest not-yet-enclosed odd vertex) is **1 on every size**: ico4, 6, 8, 10, 14, 16 and L18.
- When only one odd vertex is left outside, its distance to C is 1–2 (median 1) at every size.
- The maximum of d_min over a run is 2, 2, 3, 3.5, 6, 4.5 for ico4, 6, 8, 10, 14, 16 (and 8 on L18). This grows slowly, far below L/3.5 or the vortex spacing (about F/√3, i.e. 8 on ico14).
- **So r = 1–2 already contains the vortices that decide the end.** The forecast radius is not a locality obstruction.

**But no r fixes the failure by steering [M].**

| run | baseline | r = 1 | r = 2 | r = all | local, r = all, tie / soft | tz |
|---|---|---|---|---|---|---|
| ico16:11 (`runsE`) | ok, but t = 3.46 at full enclosure | ok, t = 0 | FAIL at the last vertex | FAIL at 2499 | ok / ok (soft: t = 0) | FAIL at 2404 |
| ico10, 13 seeds, `self` oracle | – | – | 7 last-vertex fails | 6 last-vertex fails | – | – |

- ico8, ico14 and ico22 r-grids were queued (`specsE.txt`) but not run within the time.
- Small icos (ico4, ico6: 24/24 ok) have no last-vertex failures to fix.
- **Answer to (3) [M, ico10 / ico16 only]: there is no smallest r.** The oracle tie-break fixes the final-vertex failure on some seeds at every r and breaks it on others. There is no monotone threshold, so a scaling exponent cannot be fitted.
- [C, 70%] The obstruction is **control authority, not forecast radius**. Few admissible candidates exist at bounded R, and the forecast sees the decisive vortices from r = 1–2 at every size. So enlarging r cannot help; what helps is a hard constraint at the enclosure step (tz) or more choice there (`soft` or larger R, or backtracking).

## Verdict

- [P] The proposed P_r is well defined and computable exactly. Its frame is the outer face (v1, v2, vn), and the near holonomy is hol\*(C)⁻¹ ∘ hol\*(Q_r). Special cases: P_0 = |t| and P_all = |t − t\*(C)|.
  - The outer vertex vn is always at distance 1 from the cut, so a naive radius-r region degenerates to r = all for r ≥ 2. Corridors are needed.
- [M] The oracle forecast does not predict flux increments: |corr| ≤ 0.17 against +0.5 for −t itself.
- [M] Oracle steering does not beat tz and does not remove the last-vertex t ≠ 0 failure at any r, even with a completed colouring of the same order (ico10: 6–7 last-vertex fails out of 13). It does not lower peak cuts or |t| on dense maps.
- [M] The local (Lipschitz) potential is 0 whenever vortices are near. It is therefore a no-op on dense maps, and a soft tz near the end on ico and L18: 0 last-vertex fails on ico10 (6 runs) and 1–2 on L18.
- [M + C] Locality is not the obstruction: the decisive vortices sit at distance 1–2 from C at every ico size. The bottleneck is the lack of admissible alternatives at bounded R.
- [C, 65%] The useful part of the proposal is its **local, necessary-condition** form, a "Lipschitz tz" rule: |base| ≤ 2·Σ d_w over the remaining vortices. Used as a hard constraint at vortex steps, it may move the tz pressure earlier. That was not tested.

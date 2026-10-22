# Step detrend (tau_step = colleague's tau_loc): it clears every canonical first-pair failure; the induction then dies at the second flux

22 Oct 2026, ~75 min. Code: `ld.py` (measures), `measures.py` (→ `measures_fail.json/.log`), `leaves_ld.py` (→ `leaves_ld.jsonl`), `opus_check.py`, `pi_step.py` (induction, cut modes `min`/`att`, run cap `k0`), `run_step.py` (→ `runs_step.jsonl`, `runs_att.jsonl`, `fail_*.pkl`), `twocut.py` (diagnostic). Labels: [P] proved, [M] measured exactly on the instance, [C] conjecture.

## 0. Numbers

| item | result |
|---|---|
| 13 even canonical failures (L = 39–659), best over R ≤ 1 recolourings with \|t\| ≤ 2 | **tau_step ≤ 1 on 13/13** (values 0.58–1.00, at R = 0 already); tau_Hodge 1.16–1.87 on 13/13; tau_strip 0.43–0.87 [M] |
| 3 odd canonical failures (3 interior odd, fixed-point radius 2.0) | odd step measure (reflection undone after a cut, §3) = **1.0 at R ≤ 1 on 3/3**; fixed-point radius stays 2.0 [M] |
| leaves/pockets set (88 discs of `hodge/leaves_pair.py`, colourings = Hodge-pair SAT at T = 1): 70 even walks, 32 odd | tau_step ≤ 1 on 49/70 (max 1.5; 41 walks have step > Hodge, 1 has step < Hodge); strip ≤ 1 on 70/70; odd: step_odd = fp = 1.0 on 32/32. [M] On small discs the uniform ramp is the better fit; the measures are not nested. |
| Opus bandfill rows (16) | t = 0 rows (8): Hodge = strip = step on 8/8 [P, M]. t = 2 rows (8): tau_step = **1.00 exactly** (tau_Hodge 0.97–1.47): the step radius does not reject a two-colour slope; only \|t\| ≤ 2 and the run cap do. |
| canonical induction, invariant \|t\| ≤ 2 + tau_step ≤ 1 (odd: step_odd ≤ 1), Rmax 4, policy keep, cut = min (28 runs, all finished) | **whole map coloured: ico4-left (n = 162, R ≤ 2) and ico10-left (n = 1002, R ≤ 3; Rhist {0: 887, 1: 90, 2: 20, 3: 2})**, 12 vortices each. ico4-right / rand1 / rand2, ico10 rand1 / rand2, flip7_1 left / right / rand: **all pass the first pair** (where tau_Hodge failed) at R = 0 and fail at the **next** flux: nodd = 3 (ico4-right n = 110, ico4-rand n = 104, ico10-rand1 n = 500) or nodd = 4 (ico4-rand1 n = 112, ico10-rand2 n = 570, flip7_1 n = 87, 146). Max R before failure: 1. |
| cut at attachment (`att`, colleague's transition rule; 10 runs, all finished) | same failure step as `min` on 7/9 comparable runs; ico10-rand2 fails **earlier** under `att` (n = 531, nodd = 3, against n = 570, nodd = 4 under `min`); values differ only at 2 steps per completed run (min 0.866 vs att 1.000, same R). **Exception: ico4-right completes under `att`** (R ≤ 4, one R = 4 step) while `min` fails at n = 110: restricting the cut changes which colourings `keep` picks, and that choice decided the run [M, 1 instance]. |
| run cap k0 = 3, 4 (invariant + tie-break among min-R colourings; 18 runs) | R ≤ 3 on every run except ico4-left k0 = 3 (one R = 4 step; completes). The cap was **never unrestorable at a step the pair itself survived** (every `capfail` record coincides with the pair failure step; the `inherited` flag there is an artefact of how the pre-step run is computed). ico4-left completes with k0 = 3 (R ≤ 4) and k0 = 4 (R ≤ 2). The cap costs R: R > 0 at 5–30% of steps vs 0–10% without it. Side effect: with k0 = 3, ico10-rand1 fails already at the first pair (n = 442, tau_step = 2.0 at R ≤ 1): the cap-shaped boundary is no longer two-disc decomposable [M, 1 instance]. |

**Verdict [M].** tau_step removes the smearing artefact exactly as predicted: the first vortex pair costs R = 0 everywhere, and 3 runs (ico4-left, ico10-left, ico4-right/att) colour the whole map at R ≤ 4. On the other orderings it does not make the pair inductive: the next vortex enters at a different place, the boundary then carries two localised fluxes, and one cut cannot undo both (tau_step ≥ 1.5 at R ≤ 1 on ico4-right, nodd = 3). The two-cut diagnostic `twocut.py` (one translation cut, one reflection cut) gives 1.0 / 1.0 / 0.87 on the three odd failures at R ≤ 1 [M], i.e. the obstruction is again representational, not a colouring obstruction [C, 80%].

## 1. The proposed invariant, precisely

Boundary cycle b_0..b_{L-1}, gauge signs s_i, lifted walk H_0 = 0, H_{i+1} = H_i + s_i e(c(b_i) ⊕ c(b_{i+1})), unit steps at 120°; holonomy H_L = g(H_0) with g = T_t (even number of interior odd vertices) or g = r_q, q = (H_0+H_L)/2 (odd).

- **Pair_step**: even: \|t\| ≤ 2 and tau_step ≤ 1 where tau_step = min_{0 ≤ j < L} circumradius( {H_i : i ≤ j} ∪ {g^{-1}(H_i) : j < i < L} ), g^{-1}(x) = x − t.
  Odd: tau_step_odd ≤ 1 with the same formula and g^{-1}(x) = 2q − x (this generalises the fixed-point radius max\|H_i − q\|, which is the special case "centre = q"; step_odd ≤ fp always [P]).
- **Base-point free [P].** Moving the base point from b_0 to b_1 replaces the lift by {H_1, …, H_{L-1}, g(H_0)}; the family of cut sets of the new lift, j' = 0..L−1, is the family of the old lift (j = j'+1, with j' = L−1 ↔ j = 0 up to applying g, an isometry). Circumradius is isometry-invariant, so the min over j is the same number. Checked numerically on the fail instances (shift 1, 5, 40: equal to 1e-10).
- **Transition (colleague's rule, mode `att`)**: the state carries the flux edge (b_j, b_{j+1}) of the chosen cut; at a step the admissible cuts are that edge (if it is still a boundary edge) and the two boundary edges at the new vertex v. The invariant is still checked with the min over all cuts and the value of both is recorded.
- **Run cap**: maxrun(B) ≤ k0, maxrun = longest cyclic block of consecutive boundary vertices using two colours (in vertices). Enforced on every candidate; if no candidate within Rmax meets it, the step falls back to the pair alone and is logged in `capfails`.

## 2. Why tau_step ≤ 1 at R = 0 on the failure instances [P sketch]

Before the step the boundary is flat: t = 0, circumradius ≤ 1 around a centre c, and the long fixed arc is a subset. After the step the walk has \|t\| = 2; the free vertices (v, or v and the path ends) lie between the two ends of the fixed arc, so the cut can be placed at v: the fixed arc is one piece (radius ≤ 1 around c), the free piece is 1–3 points that must land in disc(c, 1) after the shift by t. That is a local condition on O(1) points, independent of L, which is what the min over j buys. The Hodge ramp instead spreads the shift over the fixed arc.

## 3. Calibration / open

- [M] 13 even + 3 odd failures, 9 orderings × 3 maps for the induction; all exact (DFS over the free boundary colours with the two-piece prune, exact tau_step, SAT extension).
- [C, 80%] A k-cut version with k = number of flux clusters makes the pair pass further but is not bounded; the honest next invariant is "level up to the fluxes of the enclosed odd vertices", which is a different object from the pair.
- Not done: SAT encoding of tau_step (leaves set is evaluated on Hodge-pair colourings only, so "49/70" is a lower bound on satisfiability); the hub/defect maps.

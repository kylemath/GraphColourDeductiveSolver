# Bounded backtracking ("turning back") in the vortex-restricted canonical induction

23 Oct 2026, about 90 min, on a shared 4-core box. This follows up `../scale/RESULTS.md` and `../unbounded/RESULTS.md`. The model is unchanged: `vr.py` and `vrs.py` are imported, not edited. Labels: [P] proved (argument given here), [M] measured (exact on the instance, within node/candidate caps and search budgets), [C] conjecture.

## Files (all in `backtrack/`)

- `bt.py` is the driver. Spec format: `map:seed:pol:var:opts`.
  - It reuses `vrs.py` for maps, orderings and faces, and `vr.py` for FrontierVR and the position rules.
  - The step is split into enter / candidates / commit / undo, so undo is exact. `solve_step` is patched into `solve_all`, which returns every admissible colouring up to the caps.
- Output files:

  | file | runs | contents |
  |---|---|---|
  | `runs.jsonl` / `runs.log`, `runs2.log` | 451 lines; later lines supersede earlier ones for the same spec. The queue was stopped at the time limit. | ico, L18 and control |
  | `rigid.jsonl` / `rigid.log` | 190 | Opus rigid maps |

- `an.py` → `an_out.txt` is the analysis.
- Spec lists: `specs_all.txt`, `specs_r2.txt`, `specs_rigid.txt`.
- Sanity check: with `d=0,guard=0` the driver reproduces `scale/` exactly. Examples: ico10:21 FAIL at the last vertex, ico10:24 FAIL at n = 897, ico10:22 ok, helix_100 FAIL at 64, w02_150 FAIL at 149. Baseline completion is 6/20 (ico10 seeds 21–40) and 22/40 (L18), the same as before.

## What is implemented

Each step offers its **alternatives**: the admissible colourings at R ∈ [Rmin, Rmin+1] (Rmax = 4; 6 on the rigid maps). They are deduplicated by signature (t, cut set) and capped at 8. The first one is always the old `keep` choice.

Backtracking is triggered by three events:

- **F (failure):** no admissible colouring at R ≤ 4.
- **G (guard, `guard=1`):** a vortex step whose chosen colouring would push active cuts or |t| above the running peak.
  - First, another alternative at the same step is tried (depth 0).
  - Then undo δ = 1..d steps. This is iterative deepening, so **the minimal depth is found**.
  - At step k−δ, re-choose among its alternatives, ordered to turn back: smallest |t| first, then fewest cuts.
  - Replay steps k−δ+1..k with the primary rule.
  - A G event that cannot be resolved is accepted, and the peak rises.
- **D (dead state, `dead=1`, my addition):** all odd vertices are enclosed and t ≠ 0.
  - [P] The uncoloured remainder is then a disc with every degree even. The final walk must close. A ball of radius ≤ 4 can only change t if it reaches an enclosed odd vertex (`scale/` §3).
  - So the state is doomed, and D treats it as a failure at the step where it arises, instead of waiting for the last vertex.

Two variants:

- **`ord=dip` (dipole rule):** at every vortex step, the primary choice prefers a t-increment opposite to the most recent uncancelled one. A stack holds the increments; an exactly cancelling increment pops the top.
- **Search limit:** the search changes **one** earlier choice and replays greedily. It is a DFS over the stored lists at the top level only. Budget: 6000 step solves for F/D and 300 for G (20 000 for the rigid d = 160 runs).
  - Every unresolved F/D event used ≤ 930 solves, so for F/D **the search was exhausted, not truncated**. 45 G events stopped at the 300-solve budget.

## 1. Completion vs d [M]

| config | ico10 (20) | L18 rand (20) | L18 prioB seam (20) | ico + L18 total |
|---|---|---|---|---|
| d = 0 (baseline) | 6 | 10 | 12 | 28/60 |
| d = 5, F+G | 5 | 11 | 14 | 30/60 |
| d = 10, F+G | 6 | 13 | 14 | 33/60 |
| d = 20, F+G | 8 | 12 | 14 | 34/60 |
| d = 40, F+G | **9** | **13** | **15** | **37/60** |
| d = 10, F+D | (queued, not run) | | | |
| d = 40, F+D | 9 | 11 | 15 | 35/60 |
| **d = 20, F+G+D, `dip`** | 8/20 | **17/20** | **15/17** ² | **40/57** (the same 57 at baseline: 27) |

² Only 17 of the 20 prioB seeds ran before the time limit. On those 17 the baseline scores 11, F+D d = 40 scores 14, and F+G d = 40 scores 13.

**The dipole rule is the strongest variant on L18 [M].**
- L18: 32/37 ok against 21/37 at baseline on the same seeds; F+G d = 40 scores 26/37.
- Dead states fall from 11 (F+D d = 40) to 4.
- The gain comes from the **primary** choice. Steering each new vortex jump against the last uncancelled one keeps t near 0, so the last odd vertex is usually enclosed with t = 0. Its resolved F/D/G depths are ≤ 18.
- On ico10 it gives no gain over plain backtracking (8/20 against 9/20). There the 12 odd vertices are far apart, and the dead states remain (7 D).

The larger ico maps were run only with F+D, d = 40 [M]:

| map | ok | failures |
|---|---|---|
| ico14 | 1/8 | 5 D, 1 F, 1 UNK |
| ico16 | 1/6 | 3 D, 2 F |
| ico22 | 0/3 | 3 D |

Baselines from `scale/`: ico14 0/2, ico16 1/2, ico22 0/5.

- Backtracking helps modestly: **28 → 37 of 60** at d = 40. It does not converge to 100%.
  - The gain from d = 20 to d = 40 is 3 runs. Two of them are last-vertex failures repaired at depth 27 and 37 (§3).
- **Last-vertex failures stay at 13–14 of 60 for every d ≤ 40 under F+G** (ico10 5–6, L18 8).
- With D they turn into D failures. **D at d = 40 resolves only 6 of 34 dead states.**
  - Resolved depths: 1, 4, 5, 23, 32, 35.
  - Every unresolved one exhausted its search, with all single re-choices within 40 steps tried.
- On ico14/16/22, F+D at d = 40 completes 2/17. **Bounded single-change backtracking does not fix the few-defect families.**

## 2. Backtrack depth actually used [M]

Pooled over the ico10 + L18 runs, resolved events only:

| config | event | resolved / events | depth max | depth mean | depth histogram (bin lower edges) |
|---|---|---|---|---|---|
| d = 5 | G | 40/284 | 5 | 0.7 | 0:31, 1:2, 2:3, 3:1, 5:3 |
| d = 5 | F | 2/31 | 3 | – | – |
| d = 10 | G | 50/286 | 10 | 1.7 | – |
| d = 10 | F | 5/32 | 8 | – | 1, 3, 5, 5, 5 |
| d = 20 | G | 212/677 ¹ | 19 | 3.7 | 0:97, 1–4:44, 5–9:39, 10–19:32 |
| d = 20 | F | 11/37 | 18 | 7.2 | – |
| d = 40 | G | 67/292 | 38 | 6.6 | 0:35, 1–4:6, 5–9:8, 10–19:9, 20–39:9 |
| d = 40 | F | 15/38 | 37 | 16.5 | 3–4:2, 5–9:5, 10–19:3, 20–39:5 |
| d = 40, F+D | D | 6/34 | 35 | 16.7 | – |

¹ The d = 20 G row includes the control runs.

- **Most G events cannot be resolved at any depth ≤ d.** Only 23% are resolved at d = 40, and about half of those at depth 0. The peaks then simply rise.
- **The depth needed for F events grows with the d allowed.** The mean is 2 at d = 5 and 16.5 at d = 40. Each extra 2× in d resolves a few more events. There is no characteristic small depth.
- **Where the changed choice lies.** Over 232 resolved events with depth > 0:
  - The graph distance from the failing vertex v_k to the re-chosen vertex v_{k−δ} has median 9 and 90th percentile 21. The maximum is 57.
  - It is **uncorrelated with step depth** (r = 0.11). The random canonical order jumps around the boundary.
  - For F events the median graph distance is 4: the failing spot is usually within the old R ≤ 4 reach, but the needed change was made several steps earlier.
- The re-chosen step was a vortex step in only 2/15 F repairs (d = 40). For G repairs it was 97/115 (d = 20) and 16/32 (d = 40).
  - So failures are mostly repaired by recolouring at a *non-vortex* step, which shifts held positions or interior colours.
  - The turning-back of a *jump* is what the guard does.

## 3. The final-vertex t ≠ 0 failure: needs depth growing with n

**Lower bound [P].** Let k_full be the step that encloses the last odd vertex, with t ≠ 0. Every later step lies in the flat remainder. At such a step v the walk's t can change only if ball(v, R) reaches an enclosed odd vertex (`scale/` §3). So a repair started at the last vertex needs depth ≥ n − k_full, up to the few late steps whose balls touch an odd vertex.

**Measured n − k_full on the failing runs [M].**

| map | n − k_full |
|---|---|
| ico10 | 5, 15, 26, 29, 30, 53 (median 2.4% of n) |
| ico14 | 69 |
| ico16 | 158 (an ok run) |
| ico22 | 58, 223, 256, 259 (median 5% of n) |
| L18 (n = 890) | 20–377 |

- Log-log fit over ico: **slope 1.45 ± large error**, i.e. at least linear in n. With d ≤ 40 this exceeds the bound on every ico14/16/22 run.
- **The two last-vertex repairs that did succeed** (F+G, d = 40) were ico10:23 (k_full = 976, depth 27) and ico10:25 (k_full = 972, depth 37). Both re-chose a step **just before** the enclosure step, which confirms the bound.
- **Starting the repair at the dead state instead (`dead=1`)** removes the n − k_full term. The search then starts at k_full. But it succeeds only 6/34 times within 40 steps; the resolved depths were 1, 4, 5, 23, 32, 35.
  - So even from the right place, turning t back to 0 needs either more than one changed choice or more than 40 steps.
  - Its ok-rate on ico22 is 0/3.
- **Verdict [M + P].**
  - Bounded backtracking from the last vertex cannot fix this failure. The needed depth is ≥ n − k_full, which grows about linearly.
  - Early detection (D) plus d = 40 fixes a minority (6/34).
  - [C, 75%] It needs either the two-sided rule (`tz`/`face=odd` of `scale/`) or multi-change search whose depth grows with the distance between consecutive odd vertices (about √n on icoF).

## 4. Peaks vs n: does backtracking flatten the growth? [M, partial]

- **ico (d = 40, F+D):** peak cuts 6.1, 6.3, 6.3, 6.3 and peak |t| 6.5, 7.2, 7.8, 6.7 at n = 1002, 1962, 2562, 4842. Both are bounded, as in the baseline (cuts 6–7).
- **L18:** peak cuts 2.3 → 1.9 and peak |t| 3.6 → 2.9 with the guard (d = 10 and 40).
- **Control** (dense defect, guard d = 20; base values from `scale/walk.jsonl`, same seeds):

  | map | n | status | peak cuts (base → guard) | peak abs t (base → guard) |
  |---|---|---|---|---|
  | defect10_3 | 1002 | ok | 25 → 22 | 17.4 → 15.6 |
  | flip10_1 | 1002 | ok | 26 → 26 | 21.2 → 17.3 |
  | defect14_1 | 1962 | ok | 30 → 25 | 19.3 → 17.8 |
  | defect10_1 | 1002 | UNK at 932 | 28 → 22 (partial) | – |
  | defect10_2 | 1002 | UNK at 784 | – | – |
  | flip16_1 | 2562 | UNK at 957 | – | – |
  | defect14_2 | 1962 | timeout at 1102 (700 s) | – | – |
  | defect16_1 | 2562 | timeout at 1101 (700 s) | – | – |

  - The guard lowers the peaks by about 10–20% where it completes.
  - **But it costs completion.** 3 of 8 hit the node cap on the primary path: the alternative paths reach states with larger free boundaries. The baseline completed all 8 of these seeds (`scale/walk.jsonl`).
  - Each G event costs up to 300 solves; there are 35–71 G events per run, and only about 25% are resolved.
- **The n^0.65 / n^0.45 growth fit could not be redone.** The 4842-vertex controls did not run in the time, and 1962–2562 timed out.
  - Two points (n = 1002 and 1962, 4 runs) give slopes 0.11 (cuts) and 0.27 (|t|). That is not a reliable fit.
  - [C, 65%] The guard reduces the constant, not the exponent. Unresolved G events are 75% at d = 20 and do not fall with d (77% at d = 40 on ico/L18), so the peak still ratchets up with the boundary.

## 5. Add-on: Opus rigid stacked maps (`rigid.jsonl`, Rmax = 6, F only) [M]

Each cell is ok, or FAIL@n. The depth used per resolved F event is in brackets. "Unres." means unresolved. left and rand(seed 1) give identical results.

| map | d = 0 | d = 10 | d = 40 | d = 160 | depth needed | graph distance of the changed vertex |
|---|---|---|---|---|---|---|
| w02_150 | FAIL@149 | FAIL | ok [36] | ok [36] | 36 | 27 |
| w02_200 | FAIL@199 | FAIL | FAIL | ok [54] | 54 | 41 |
| w02_300 | FAIL@299 | FAIL | FAIL | ok [76] | 76 | 57 |
| w02_400 | FAIL@399 | FAIL | FAIL | ok [108] | 108 | 81 |
| w02_600 | FAIL@600 | FAIL | FAIL | ok [43] | 43 | 33 |
| w021_150 | FAIL@150 | FAIL | FAIL | ok [124] | 124 | 10 |
| w021_300 | FAIL@300 | FAIL | FAIL | ok [75] | 75 | 75 |
| w021_400 | FAIL@400 | FAIL | FAIL | ok [108] | 108 | 108 |
| w021_600 | FAIL@600 | FAIL | FAIL | ok [44] | 44 | 44 |
| w02/w021_100, w021_200 | ok | ok | ok | ok | – | – |
| helix_50 / 70 (left) | ok / FAIL@44 | ok [1, 2] / ok [4, 7, 1] | same | same | ≤ 7 | 4–7 |
| helix_70 (rand) | FAIL@56 | FAIL | FAIL@61 | FAIL@61 (unres.) | – | – |
| helix_100 … 400 | FAIL@64 … 230 | FAIL@65 … 233 | same | **FAIL, same step** | **unresolvable** | – |

- **w02/w021: one changed choice repairs the rigid snap, but at depth Θ(m).**
  - For w02 at m = 150–400, depth ≈ 0.27 m (36, 54, 76, 108). The graph distance of the changed vertex is 27, 41, 57, 81, which tracks Rext of `rigid/REPORT.md` (9–30) to within a factor of about 2–3.
  - m = 600 needs only 43–44. That ordering reaches its snap at the last step, in a different way.
  - The changed step was always a vortex step.
  - So **d must scale linearly with m** [M, 9 instances]. No fixed d works: d = 40 recovers only w02_150.
- **Tetrahelix: bounded backtracking never recovers it.**
  - On helix_100…400, two to three F events are repaired at depth 4 and 7. Then a failure about 2 steps later is **unresolvable even with d = 160 > k**: every single re-choice over the whole history was tried (130–290 solves, all fail).
  - So the failure needs ≥ 2 simultaneous changes, or none suffices [M].
  - This matches the `rigid/` finding: a colouring passing the invariant at every step may not exist (R = 0 is refuted). [C, 60%] No bounded-depth search fixes it.

## Verdict

- [M] Bounded backtracking (F + G, alternatives at R ≤ Rmin + 1, one changed choice) raises completion on the failing families from **28/60 to 37/60 at d = 40**. The gains from d = 5, 10 and 20 are 30, 33 and 34 out of 60. The F-repair depth used grows with the depth allowed, with no plateau.
- [P + M] **The final-vertex t ≠ 0 failure needs depth ≥ n − k_full**, measured at 2–5% of n, fit exponent ≥ 1 on ico.
  - Bounded d fixes it only when the last odd vertex was enclosed fewer than d steps before the end (2 cases).
  - Detecting the dead state early helps 6/34 at d = 40. So the fix is not local in the step order.
- [M] Changed choices lie at graph distance median 9 (p90 21) from the failure, uncorrelated with step depth. F repairs mostly re-choose a non-vortex step.
- [M] The guard trims peak cuts and |t| by 10–20% on dense maps. But 75% of guard events cannot be resolved within d, and node caps rise. [C, 65%] It does not change the growth exponent; the 4842-vertex points are missing.
- [M] Rigid maps:
  - w02/w021 are recovered by a single re-choice at depth about 0.27 m, i.e. **d ∝ m**.
  - The tetrahelix is not recovered by any single re-choice over the whole history.
- [M] **The dipole primary rule (`dip`, with F+G+D at d = 20) is the best variant: 40/57 against 27/57 at baseline.**
  - It is best on L18 (32/37), where it largely prevents the t ≠ 0 dead state rather than repairing it.
  - On ico10 it does not help beyond plain backtracking (8/20).
- [C, 70%] "Turning back" is real but not local. The jump that has to change is Θ(distance between odd vertices) steps back on few-defect maps, and Θ(m) steps back on rigid strips. A bounded-R, bounded-d controller therefore still needs a two-sided (outside-aware) constraint, not just backtracking.

## Not done (time)

- d = 10 with F+D, ico14/16/22 with F+G, all 4842-vertex controls, and the baseline/dip controls. These are left in `specs_all.txt` / `specs_r2.txt`.
- `dip` on ico14/16/22 and on the dense controls, and 3 prioB seeds.

# Bounded-cut detrend tau_J: no fixed J completes the 492- and 1002-vertex maps; the number of cuts grows with the vortex count

23 Oct 2026, about 75 min. Code: `mc.py` (exact tau_J test and value), `mcstep.py` (induction, cut modes `min`/`att`, run cap, repair), `run_mc.py`, `summ.py` (→ `summary.txt`), `diag.py`, `sanity_j1.py`, `sanity2.py`/`sanity3.py` (→ `.log`). Run logs: `runs*.jsonl`. Failure instances: `fail_*.pkl`. Labels: [P] proved, [M] measured (exact on the instance), [C] conjecture.

## 0. Numbers

| item | result |
|---|---|
| exactness | J = 1 reproduces tau_step on 797/797 even and 1184/1184 odd random walks. Shifting the base point leaves the min cut count unchanged on 2840/2840 checks (J = 1..4, both variants). The J = 1 induction reproduces the old traces exactly. [M] |
| lattice fact used by the test | A set of lattice points has circumradius ≤ 1 iff it lies in one closed hexagon (a lattice point plus its 6 neighbours). The 7 such hexagons that contain 0 are the only maximal sets. This is the hexagon retract of Dvořák et al. [P by exhaustive candidate-centre enumeration] |
| induction, \|t\| ≤ 2, tau_J ≤ 1, cuts anywhere (`nc`), 14 map/orderings: ico4 ×4, ico10 ×3, flip7_1 ×3, flip7_2, defect7_1 ×2, defect10_1 | **whole map coloured: J=2: 2/14, J=3: 3/14, J=4: 4/14** (ico4 L, R, rand2, plus ico10-rand2 at J = 4). Max R = 4. 95–99% of steps need R = 0. ico10-left: timeout at J = 3, 4. |
| same with \|t\| free (only the J jumps bound t) | **ico4: 4/4 orderings at J = 3 and at J = 4** (R ≤ 2). Every 492- and 1002-vertex map fails at J = 2, 3, 4: J = 4 fails at nodd = 6–15. ico10-rand2 at J = 4 reaches the **last vertex** (n = 1002) and fails there: the outer triangle cannot carry the accumulated \|t\| = 2√3. |
| J = 6, 8 (\|t\| free; flip7_1-L, defect7_1-rand, flip7_2-rand) | all fail. J = 6: nodd 14 / 10 / 45. J = 8: nodd 25 / 16 / 51. |
| cuts in use over time | **Climb to J in every failing run, then fail at the next vortex.** Example (flip7_1-L, J = 8), (nodd, cuts): (2,1) (4,2) (6,3) (7,4) (10,4) (11,5) (12,6) (15,8) … fail at nodd 25. Roughly nodd/2 to nodd/6 cuts. |
| what the failing step needs (diag, 6 instances) | **J + 1 cuts at R = 0 suffice** in 6/6. The extra cut sits at v (offset 0 or ±1). The other cuts lie 20–80 boundary steps apart. In the \|t\| ≤ 2 runs at J = 2, the binding constraint is \|t\|: every colouring at R ≤ 1 has \|t\| ≥ 2√3. [M] |
| cut at attachment (`att`, J = 2, 3) | ico10-left **completes** at J = 2 and J = 3 (R ≤ 4, 1 cut), the only large map to complete. Every other large map fails at nodd 4–24, the same as `min`. |
| run cap k0 = 4 | **Worse.** 3/42 runs complete. Most fail at nodd = 2–4. The cap forces cuts at non-vortex steps. |
| variant `any` (cancelling pairs allowed), J = 2 | 3/14 complete (ico4 L, R, rand2); the others fail at nodd 4–17. |
| repair: merge two cuts within d = 8 or 16 by recolouring radius-2 balls (J = 3, 18 runs) | 3 merges in total, all on ico4. **No failure step moved.** The lumps are too far apart to merge locally. [M] |

## 1. Sanity (part 2)

- **c\* parallelogram (t = 0) [M].** m ≥ 8: tau_J > 2.5 for every J ≤ 4 and both variants. m = 4, w = 2: nc stays ≥ 1.5, but any4 = 0.58 accepts it.
- **Smeared slopes, t = 2 [M].**
  - L = 96 and 192: tau_J ≥ 1.35 for every J ≤ 4 (tau_step 1.5), so all are rejected.
  - L = 48: any3, nc4 and any4 accept (1.0); nc2 and nc3 reject.
- **t = 0 loosening.** Sample: 889 random closed walks with circumradius > 1.
  - **nc, J = 2: accepts 0, so no loosening [P: on t = 0 two jumps must cancel].**
  - any, J = 2: accepts 349.
  - nc, J = 3 or 4: accepts 418, through the triple 2 + 2ω + 2ω² = 0 [M].
  - any, J = 4: accepts 568 [M].
  - The 8 Opus t = 0 rows are already accepted at J = 1 (value 1.0), so their accept status cannot change.
- So **only nc with J = 2 is a strict refinement on t = 0.** From J = 3 on, nc admits a "vortex triangle" of three jumps on flat rows.

## 2. Verdict

- **No J completes every map with bounded R [M].** R is not the issue: max R ≤ 4, and at the failure point R = 0 plus one more cut suffices. The issue is that **the number of active cuts grows without bound**, about one new cut per 2–6 enclosed odd vertices. Cuts are created only at vortex steps:
  - all runs without the run cap: 0 non-vortex cut creations, with one exception (ico10-left, J = 2);
  - every recorded failure except 2 happens at a step that encloses a new odd vertex. These are the coordinator's hexagon-retract columns `fail_at_vortex` and `cut+@nonvortex` in `summary.txt`.
- **Between vortex insertions the boundary stays in one hexagon modulo the existing cuts [M]:** no new cut is ever needed there.
- **Local merging (d ≤ 16) does not cancel lumps, because they sit 20–80 steps apart.**
- [C, 75%] Any bounded-J invariant along canonical orderings needs a **non-local cancellation**: pair each new flux with an existing lump of the opposite sign, for example by Kempe-type recolouring along the boundary. Alternatively, the count must be charged to enclosed vortices, giving a level relative to the fluxes rather than a bounded number of lumps.

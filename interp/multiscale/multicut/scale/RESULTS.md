# Vortex-restricted uncapped cuts: scale and adversarial tests

23 Oct 2026, about 2 h. This follows up `../unbounded/RESULTS.md`, and the model is unchanged (`../unbounded/vr.py` is imported, not edited). Labels: [P] proved (argument given here), [M] measured (exact on the instance, within node/candidate caps), [C] conjecture.

## Files (all in `scale/`)

- `vrs.py` is the driver. Spec format: `map:seed:policy:variant[:opts]`.
  - Extra map: `L18`, the Opus 890-vertex sphere.
  - Policies `prioA` / `prioB` peel one side first. With `face=seam`, the prefix boundary becomes exactly the length-18 seam row.
  - Options:
    - `face=odd`: the outer face sits at an odd vertex, which becomes the last vertex v_n.
    - `seedA=1`: the prefix A is overwritten with Opus's adversarial `colA`.
    - `Rlast`, `lastk`: larger R on the final steps.
    - `win=W`: departed and new positions may land within ±W of v. The count budget is unchanged.
    - `tz=1`: two-sided rule; once no odd vertex remains outside, the walk must close (t = 0).
    - `U12=1`: also allow jumps of norm 2√3.
    - `greedy=1`: among min-R candidates, minimise (cuts, |t|).
    - `walk=1`: per-step log.
- Run logs:
  - `l18.jsonl`: 36 runs.
  - `final.jsonl`: 240 runs, the final-step and L18 options.
  - `scale.jsonl`: 6 runs, ico22 and flip22.
  - `walk.jsonl`: 60 runs, 1k–5k vertices, with per-step walk logs.
  - In total, **342 valid runs**.
- Analysis scripts: `summ.py`, `walkan.py`, `lastfix.py` / `lastdiag.py` (final step), `faildiag2.py` (probe a failing state).
- Failure states: `fails/*.pkl`.
- `contaminated/` holds a first `final`/`u12` batch. **It is invalid**: a module-global `tz` flag leaked between jobs in the same pool worker, so plain runs were silently run with t = 0 forced. It was fixed (per-job reset) and everything was rerun. Do not use it.

## Headline [M]

| family | `any`, plain options | `nc` |
|---|---|---|
| flip / defect, n = 1002–4842 (random min-deg 5, max-deg 9) | **36/41 ok, 0 genuine FAIL**, 5 node-cap UNK | 0/6 (vortex steps, only "cuts anywhere" saves) |
| ico10/14/16/22 (12 odd vertices) | **8/40 ok** | – |
| L18 Opus sphere | **23/40 ok**, 1 UNK | 3/8 |

- Every completed colouring is proper (172 ok runs).
- Max R over all 342 runs:

  | max R | 0 | 1 | 2 | 3 | 4 | 5 |
  |---|---|---|---|---|---|---|
  | runs | 3 | 39 | 74 | 107 | 115 | 4 |

  The four R = 5 runs all use the `Rlast` option. No ok run without `Rlast` needed R > 4.
- New positions were never created at a non-vortex step: `newcut_nonvortex` = 0 in all 342 runs (the rule forbids it, and an assertion checks it).
  - But **non-vortex steps do fail for lack of a correctly placed cut** on ico and L18 (table in §3).
  - So the earlier claim "no step fails for want of a non-vortex cut" (13/14) does **not** survive scale.
- The earlier 13/14 for `any` was optimistic on few-defect maps. ico10 random orders: earlier 1/2; now 6/20 on seeds 21–40.

## 1. Adversarial: the Opus L18 sphere (n = 890, 12 degree-5, seam length 18)

**Orderings tested.**
- rand / left / right with random outer faces.
- `prioB` + `face=seam`: v1 and v2 in A's seam row, v_n in B; B is peeled first. In every prioB run, at n = 445 the prefix is **exactly A** and the boundary is **exactly the 18-cycle seam row** (`Ahit`: 18/18 seam vertices on the boundary). `prioA` is the mirror image.
- `seedA=1`: at that moment, A's colouring is replaced by Opus's `colA`, the level colouring whose deep rows defeat R ≤ 3 closing.

**Results [M].**
- **Crossing the seam needs no large R.** At the seam step and just after it, R ∈ {0, 1, 2} in every prioB run.
- The adversarial `colA` is accepted by the invariant with **zero cuts** (t = 0, τ ≤ 1).
- After seeding, the induction continues at **R ≤ 4**: 4/5 seeded runs complete, max R 2, 2, 2, 4.
- **Why the R ≥ 4 closing bound does not apply [P].** The obstruction is about fixed colourings on *both* sides. Here B is coloured by the induction itself, one vertex at a time, so the Opus pair never arises.
- **One prioB seed (3) fails exactly at the seam-closing step** (n = 445: L = 18, dn = 0, no held positions survive). Each of the following saves it at R = 2:
  - one cut 1 edge from v, on window offset +1, which departed positions may not use;
  - `extra1_window`;
  - cuts anywhere.

  This is a window-shape problem, not a count problem.
- **The dominant L18 failure is the final-step obstruction (§3)**: 18 of the 40 L18 `any` failures are at the last vertex, all with t = 2√3 once all 12 odd vertices are enclosed.
- When the prefix is exactly A, the seam walk has t = 0 or 2√3 (2 cuts). A t = 2√3 seam is carried through B without trouble, but then it reaches the end with t ≠ 0 and fails at the last vertex.

| L18 group (10 runs each) | ok | last-vertex FAIL | other FAIL |
|---|---|---|---|
| rand | 5 | 3 | 2 |
| rand, face=odd | **7** | 0 | 2 (+1 UNK) |
| rand, tz=1 | 6 | 0 | 4 |
| rand, win=2 | 4 | 5 | 1 |
| rand, win=2, tz=1 | 6 | 0 | 3 (+1 UNK) |
| prioB seam | 5 | 4 | 1 |
| prioB seam, win=2, tz=1 | **7** | 0 | 3 |

**merge/.** `opus_attack/merge/REPORT.md` states that its instances are flat discs inside one icosahedron face, and that the closed sphere was not built (§6 there). Skipped, as instructed.

## 2. Scale: 1k–5k vertices (`walk.jsonl`, `scale.jsonl`)

**flip / defect `any` [M].**
- 36/41 ok and 0 genuine failures. The 5 UNK are node caps at R = 3 with |FB| ≥ 17.
- Max R is 3–4 in every run, and stays at that level from n = 1002 to n = 4842.
- **Active cuts are not O(1).**
  - Peak cuts grow as about n^0.65: means 24, 32, 44, 67 (defect) and 27, 41, 44, 83 (flip) at n = 1002, 1962, 2562, 4842.
  - Peak cuts / √n stays at 0.6–1.2. Peak cuts / final nodd is 0.025–0.05 and falls with n.
- Active cuts ≤ nodd always (`cuts_le_nodd`).

**ico `any` [M].**
- Peak cuts stay at 5–7, independent of n (slope 0.04).
- But only 1/7 complete in the walk set and 0/5 on ico22 (`scale.jsonl`). Failures:
  - last vertex: ico10-11, ico14-11, ico22 ×2;
  - just before the end, with t ≠ 0 and nothing odd left outside: ico22-12, ico22-11;
  - position failures at non-vortex steps, saved only by cuts anywhere: ico10-12, ico14-12, ico16-12, and ico22-left at L = 1916.

**`nc`.** 0/6 on flip/defect. All failures are at vortex steps, and cuts anywhere save them. This matches the earlier finding.

## 3. The final step (task 3)

**Diagnosis of ico10-rand2 [P + M].**
- The final boundary is the outer triangle. For **every** proper colouring of a triangle, the walk is closed (t = 0) with radius 1/√3 (`lastdiag.py`). So the invariant never blocks the last step. Properness does.
- **Mechanism [P].** Once the last odd vertex is enclosed, the uncoloured remainder D′ is a disc with every degree even (here all degree 6).
  - In any proper colouring, the Kondev–Henley height on a flat disc is single-valued.
  - So the boundary walk must close: t = 0.
  - Recolouring a ball N_R(v) cannot change the monodromy of the loop just outside the ball, unless the ball contains a coloured odd vertex.
- **On ico10-rand2 [M].**
  - The last odd vertex is enclosed at n = 991. From then on t = 2√3, and it stays there until n = 1001.
  - v = 979 is at distance 4 from the nearest degree-5 vertex.
  - Exact SAT ball refill (`lastfix.py`): R = 0–4 infeasible, **R = 5 feasible**, the first ball that contains an odd vertex in its interior. `Rlast=6` completes the run with R = 5.
- **It is generic.**
  - In ok runs that enclosed the last odd vertex before the end, t was 0 at that moment in 92 cases and nonzero in 12 (those 12 were rescued later or by Rlast).
  - Every last-vertex failure (30 ico, 18 L18) has t_full = 2√3 (a few have 6 or 9.2).
  - On icoF the distance from v_n to the nearest degree-5 vertex grows like F/√3. So **"R up to 6 on the last step" is not a bounded fix [P]**: it works on ico10 by luck of distance. ico22 needs about 12.

**Remedies tested (ico10 seeds 21–40, 20 runs each) [M].**

| option | ok | last-vertex FAIL | other FAIL |
|---|---|---|---|
| plain | 6 | 5 | 9 |
| Rlast=6 on the last 20 steps | 7 | 5 | 8 |
| face=odd (v_n is a degree-5 vertex) | **11** | **0** | 9 |
| tz=1 (two-sided rule) | 8 | **0** | 12 |
| win=2 | 7 | 8 | 5 |
| win=2 + tz=1 | **11** | **0** | 9 |
| U12 (and U12 + win=2 + tz=1) | identical to plain (and to win=2 + tz=1) | | |

- `face=odd` and `tz=1` both **remove the last-vertex failure completely** (0/40 on ico, 0/20 on L18).
- But they do not raise completion to 100%. The pressure moves earlier:
  - With `tz`, failures move to the vortex step that encloses the last odd vertex (dn = 1). That step must reach t = 0, and at R ≤ 4 it often cannot. Cuts anywhere save some of these, not all.
  - With `face=odd`, failures are position failures at non-vortex steps with nodd = 8–11. These are mostly saved by `extra1_window` or by cuts anywhere.
- **[C, 65%]** The right last-step rule is two-sided: the invariant must also bound |t| by what the *outside* odd vertices can absorb, not only by the inside count. This matters only on low-defect maps (ico, L18). On flip/defect maps, odd vertices are dense, the outside is never flat until the very end, and no final failure was ever seen (0/41).

**Non-vortex failures on ico and L18 [M]**, from the `diag` field of the failing step:

| family | non-vortex: window+1 saves | non-vortex: only anywhere saves | non-vortex: nothing at R ≤ 4 | vortex: window+1 / anywhere / nothing |
|---|---|---|---|---|
| ico | 28 | 24 | 11 | 5 / 3 / 10 |
| L18 | 9 | 3 | 0 | 8 / 2 / 0 |

- In the probed cases, the needed cut sits 0–2 edges from v but outside the allowed window. Alternatively, a held position must slide by 1–3 (`faildiag2.py`: L18-0 slide 3; L18-1 cut at distance 2 from v; L18-4 slide 1).
- The count of cuts is always within the budget. **The bookkeeping of positions, not the count, fails.** `win=2` alone does not help (7/20), because it moves failures to the end.

## walk (coordinator request)

The model, per step (`walk.jsonl`, `walk=1`): n, nodd, active cuts, |t|, R, L, plus Lyapunov fields.
- Every active jump has |s| = 2, so Σ|s_k| = 2 · cuts.
- In the even case, t = Σ s_k.

**(a) Scaling of peak cuts and peak |t| [M]** (fit over n = 1002, 1962, 2562, 4842):

| family | peak cuts (means) | log-log slope vs n | peak abs t (means) | slope | peak Σ abs s / peak abs t |
|---|---|---|---|---|---|
| defect | 24, 32, 44, 67 | **0.66** | 16.3, 19.9, 26.3, 33.1 | **0.47** | about 4 |
| flip | 27, 41, 44, 83 | **0.65** | 17.8, 22.1, 24.7, 37.2 | **0.42** | about 4.5 |
| ico | 6, 6, 6, 7 | 0.04 (bounded) | 6.5, 7.2, 8.0, 6.9 | 0.09 | about 2 |

- On defect-rich maps both quantities grow without bound.
  - Peak cuts grow about √n or slightly faster.
  - Peak |t| grows about √n (slope 0.42–0.47). That is like a random walk of about n^0.65 jumps of length 2 with partial cancellation: 2√84 ≈ 18 against 37 observed, so there is some drift.
  - Relative to the enclosed odd count, peak cuts fall: cuts / nodd drops from 0.05 to 0.025.
- On ico both stay bounded (≤ 7 cuts, |t| ≤ 9.2). But there t ≠ 0 kills the final step (§3).
- **[C, 70%]** The walk is not self-bounding. A proof would need a charging argument (cuts ≤ c·√(enclosed odd) or similar), not O(1).

**(b) Lyapunov / drift test [M].**
- Steps tested: those where active cuts ≥ the run's 75th percentile (top quartile; flip/defect `any`, 39 runs, about 300–1400 such steps per run).
- **A non-increasing candidate exists in about 75% of top-quartile steps.** Non-increasing means cuts ≤ previous and |t| ≤ previous, at the minimal R, before SAT extension. Examples: flip22: 964/1274; defect22: 950/1233; flip10: about 190/255.
  - In the other about 25%, every boundary candidate at the minimal R increases cuts or |t|. Larger R was not explored.
- **The chosen colouring increased cuts in about 19%** of top-quartile steps and **|t| in about 23%**.
  - In about 8% (for example 105/1274 on flip22) it increased one of them although a non-increasing boundary candidate existed.
  - Those are almost all candidates that fail the SAT extension of the interior ball, or ties broken by `keep` (fewest recolourings) without regard to |t|.

**Greedy policy (`greedy=1`) [M].** Among min-R candidates, it orders by (cuts, |t|, #recoloured).
- It **does not bound the walk.** Peak cuts on paired runs:

  | run | keep | greedy |
  |---|---|---|
  | flip22 | 84 | 83 |
  | defect22 | 66 | 69 |
  | flip14 | 51 | 50 |
  | defect14 | 37 | 39 |

  Peak |t| is within ±3 of keep. Completion is the same: 12/14 vs 12/14 paired, the same UNKs.
- On ico, greedy is **identical** to keep: at the minimal R there is essentially one admissible candidate. So it does **not** fix the final-triangle failure (ico10-11, ico14-11 and ico22-11 still fail at the last vertex or just before it).
- Only the two-sided rules (`tz`, `face=odd`) remove that failure. Greedy minimisation of the inside quantities cannot see the obstruction, which lives outside.

## Verdict

- [M] **Dense-defect maps (flip/defect, 1k–5k): the `any` induction completes every run that is not capped (36/36), at R ≤ 4.** Active cuts and |t| grow about √n, with cuts ≤ nodd always.
- [M] **Few-defect maps (ico, Opus L18) fail often.**
  - ico: 8/40 plain. L18: 23/40.
  - The causes are (i) the flat-remainder / last-vertex t-obstruction and (ii) position-window failures at non-vortex steps, where the count is fine but the place is wrong.
- [M] **The Opus sphere does not force large R in the induction.** Crossing the length-18 seam, and even restarting from Opus's adversarial `colA`, stays at R ≤ 4. One seam step needed a cut at window offset +1, which is a window-shape issue.
- [P] **The final-step failure is topological.** A flat remainder forces t = 0. A fix by enlarging R at the end needs R ≈ the distance to the nearest odd vertex, which is unbounded on icoF.
  - [M] Making v_n an odd vertex, or adding a two-sided t = 0 rule, removes it entirely (0 last-vertex failures in 80 ico/L18 runs). The failures then move earlier.
- [C, 60%] Bounded R needs both (1) a two-sided |t| constraint tied to the odd vertices outside, and (2) a position rule that lets held positions slide by 1–3 when the jump can be transported.

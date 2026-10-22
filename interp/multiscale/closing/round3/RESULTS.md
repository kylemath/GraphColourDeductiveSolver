# Closing step (b), round 3: R vs seam length, ico10 to ico50

22 Oct 2026. Labels: **[M]** measured (SAT, exact for the instance), **[P]** proved, **[C]** conjecture.

## 0. Numbers [M]

Setup:
- Pole-centred half splits (`pole`, plus wiggle 0.3 `polew`), 6 poles on each side.
- Seams are chordless and Eulerian: no odd vertex within distance 1.
- t = 0 is UNSAT on both sides, so |t| = 2 is forced on both.
- 5 level colourings per side give 25 closings per split, and 4 splits per size give **100 closings per size, 700 in total**.

| F | L (4 seams) | R = 1 / 2 / 3 | mean R | W_band = 1 / 2 / 3 | max recoloured / L | seam-to-pole distance |
|---|---|---|---|---|---|---|
| 10 | 100–110 | 74 / 26 / 0 | 1.26 | 92 / 4 / 0 (4 cases had W = 0) | 1.55 | 3–4 |
| 14 | 146–170 | 50 / 50 / 0 | 1.50 | 84 / 16 / 0 | 0.88 | 5–6 |
| 20 | 206–226 | 27 / 71 / 2 | 1.75 | 68 / 32 / 0 | 1.17 | 7–9 |
| 25 | 254–288 | 22 / 75 / 3 | 1.81 | 66 / 33 / 1 | 0.92 | 7–12 |
| 35* | 362–404 | 8 / 87 / 5 | 1.97 | 48 / 50 / 2 | 1.49 | 12–15 |
| 40* | 404–466 | 4 / 94 / 2 | 1.98 | 42 / 56 / 2 | 1.20 | 14–18 |
| 50* | 504–572 | 1 / 91 / 8 | 2.07 | 25 / 73 / 2 | 1.12 | 18–23 |

- **Max R = 3 at every size from L ≈ 206 up to L = 572. No closing had R ≥ 4 out of 700.**
- The R distribution moves up with L: P(R = 1) goes from 0.74 to 0.01, and the mean rises from 1.26 to 2.07. P(R = 3) stays small (0 to 0.08) and noisy.
- **Adversary.** Local search re-solved one side's level colouring inside a random seam window of radius 3–6, keeping levelness and accepting non-decreasing moves.
  - The score was (R, number of renamings that fail at R).
  - ico50 (L = 538): 56 steps. It went from R = 2 to R = 3 at step 48, ending at score (3, 22), so only 2 of 24 renamings still repair at R = 3. **It did not reach R = 4.**
  - ico25, started from an R = 3 instance: 20 steps, stuck at (3, 16). No R = 4.
  - The search was short (about 10 min each). This is weak evidence.

\* For F ≥ 35 the colourings are **band-only**: proper on depth ≤ 6, level on the whole walk. I did not check that they extend to the interior, because the Cadical interior solve stalled. All repairs stay within depth ≤ 5, so R is exact *given* the band colouring. If a band colouring has no extension, that sample would be invalid. For F ≤ 25 the colourings are full.

## 1. Why ico30 failed [M]

The round-2 generator had no bug. The obstruction is arithmetic (`diag.py`, `diag.log`).
- On a 6/6-pole half of icoF, exactly one translation class is level-feasible.
- For F ≡ 0 mod 3 that class is **t = 0**: tested on 3 pole and 3 ball splits each for ico15 and ico30, all with t = 0 feasible and t = (±4, 0) infeasible.
- For F ≢ 0 mod 3 it is the |t| = 2 orbit. All 28 splits at F = 10, 14, 20, 25, 35, 40, 50 passed on the first attempt.
- So the forced-|t| = 2 regime does not exist on ico15 or ico30 with 6/6 splits. Splits with 4 or 6 poles per side at F = 10 and 20 also allowed t = 0.

**[C]** The feasible class is fixed by the poles' positions mod the 3-sublattice.

Two engineering fixes:
1. The t = 0 exclusion is now Cadical with one boundary edge's colours fixed. It is sound because t = 0 is invariant under renaming, and band-UNSAT implies full-UNSAT. It takes 1–2 s on ico50, where the Glucose UNSAT proof had stalled for more than 10 min.
2. The nonzero orbit is read off one SAT colouring.

## 2. Do the R = 3 cases share a structure? Mostly no [M, weak]

`analyse2.py` was run on 6 R = 3 instances (ico20 and ico25, plus the round-2 one); the output is in `analyse2.log`.
- In every case **only 6–8 of the 24 renamings are repairable at R = 3**; the others need R ≥ 4.
- In the repair, the changes at distance 3 sit in **9–26 separate spots** along the seam, all at distance ≥ 5 from every pole (except the round-2 wig case).
- Near those spots the rate of seam "corners" (A-vertices without exactly 2 B-neighbours) equals the seam average: 0.10–0.20 against 0.15, and 0.35–0.43 against 0.37.
- So I found no local motif. R = 3 behaves like an extensive effect: the more seam there is, the more chances some spot needs radius 3 under each good renaming.
- Caveat: the repair is phase-guided, not minimum-change, so the spot counts are upper bounds.

All 20 instances with R or W_band ≥ 3 are saved as `hard_F_kind_seed_i_j.pkl` (keys adj, A, colA, colB, out). The adversary's best ico50 instance is in `adv50_best.pkl`.

## 3. Reading [C]

- Max R stays 3 over a 5.7× range of L (100 to 572), under the random and the adversarial sampler. This fits **bounded R (≈ 3) for Eulerian, internally regular seams**. Growth as slow as log L is not excluded: the mean is still creeping up, from 1.26 to 2.07.
- Confound: the seam-to-pole distance grows about 0.4F, so larger L also means poles further from the seam.
- Not tested: seams near odd vertices, non-icosphere maps, and a longer or smarter adversary for R = 4.

Files: `s3_scale.py` (driver), `fastcol.py`, `tcheck.py`, `adv.py`, `analyse2.py`, `agg.py`, `s3.jsonl`, `s3.log`, `s3big.log`, `adv25.log`, `adv50.log`, `diag.log`. `analyse.py` is a slow exact per-cluster variant that was not completed.

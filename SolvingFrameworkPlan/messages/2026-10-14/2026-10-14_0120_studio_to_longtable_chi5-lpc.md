# Studio report: Job 6, the χ = 5 surface test of LPC

- **From:** Studio session
- **To:** Long Table
- **Sent:** 2026-10-14 01:20 MDT
- **Label:** exploratory data
- **Details:** `backgroundMaterial/planemap-structural/longtable/chi5/README.md`

## Result

0 parity-clean Kempe classes at good holes: no counterexample to surface-general LPC.

1. **Existing TrackF data.**
   - It contains 630 non-4-colourable triangulations: torus, Klein bottle, RP², genus 2 and rp2x3.
   - They have 1,132 good holes (degree 5, T − h 4-colourable). Two independent colouring checks agree: SAT and DSATUR.
   - The 3,045 classes there contain 0 all-DL π-cycles and 0 parity-clean classes.
   - The median violator fraction is 1.0. The minimum is 0.22 on the Klein bottle and on rp2x3.
2. **Annealing walks vs power control.**
   - **χ = 5 walks:** 20,534 walks and 30.8M flips (n = 12–40) that keep T non-4-colourable.
     - 0 all-DL π-cycles at good holes;
     - max DL π-run 5 (RP²) to 12 (Klein, rp2x3);
     - min violator fraction 0.22–0.40.
   - **Control:** the same objective on 4-colourable triangulations, 7,234 walks and 10.6M flips. It reaches all-DL
     π-cycles in 0.5% (genus 2) to 12% (RP²) of walks, median 365–791 flips to hit, max DL π-run up to 171.
3. **Reading.**
   - The null is meaningful against the control: same search, larger budget, never reaching the cycle region at
     χ = 5 holes.
   - Caveat: T − h at a good hole is near-critical, with few colourings and mostly frozen singletons. So the absence of
     cycles may be rigidity rather than a law.
   - n ≤ 40; this is evidence, not proof.

## Status of other Studio work

- Job 7 (boundary solvability, census orders 22–33) started at 01:10 on 12 workers. Its report follows when it is done.

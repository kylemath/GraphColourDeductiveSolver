# Studio report: Job 7, boundary solvability (plan A2) at scale

- **From:** Studio session
- **To:** Long Table
- **Sent:** 2026-10-14 03:00 MDT
- **Label:** exploratory data
- **Details:** `backgroundMaterial/planemap-structural/longtable/boundary/studio/README.md`

## Results

1. **Census, orders 22–33 (1,337,323 holes).**
   - Holes with a failing region: faceMax 67,882 (from order 25), face3 140,399, shell1 402,705, shell2 776 (from order
     30), dist3 0.
   - Max extra par where solvable: dist3 5, shell2 8, faceMax 17.
   - The dist3 region is 0.32–0.39 of n at the minimum, and 0.53 on average at order 33.
   - Counterexamples are confirmed by 3 engines: far face at p25#2111 h1 (confirmed on the MacBook too); shell2 at
     p30.r29#66366 h18.
2. **Rim statistic (faceMax).** 77.6% of dR-lowering R-moves meet the link, and 11.5% of states with dR > 0 have no
   rim-touching lowering move. Far chains do real work.
3. **Far-threshold scan, R = {d ≥ r}** (monotone in r everywhere):
   - **Fullerene C20–C46 and Goldberg C20/C60/C80:** the last one or two shells always suffice (dmax − rmax ≤ 1). Min
     |R|/n is 0.04; on the C80 dual, {d ≥ 5} (6/42) suffices.
   - **IPR duals (4,125 holes):** dmax − rmax ≤ 1 except ipr#243 h20, where it is 2: {d ≥ 5} (9/49) fails and
     {d ≥ 4} (20/49) solves.
   - **Job 2 glued graphs (300 sampled, 4,220 holes):** dmax − rmax reaches 3 (10 holes) and **4** (gglue4_1754 =
     p26#78654@21-22+p26#5298@9-10/q0, h44). There {d ≥ 4} (25/48) fails a state with dF = 1 (R-closure of 6 states),
     and only {d ≥ 3} solves.
4. **Reading.**
   - The far-field form holds on internally 6-connected maps (census, fullerene, IPR), with the last 1–2 shells.
   - It fails on maps with separating 4- and 5-cycles.
   - Only dist3 survives everywhere, and it is not genuinely far at these sizes.

## Studio state

Jobs 6 and 7 are done. Nothing is running.

# Seam-band tetrahedral SDP: twist or snap?

22 Oct 2026, about 60 min. Code: `tw.py` (SDP and low-rank solver), `run.py` (per-instance analysis), `shape.py` (profiles along the seam), `gen.py` (new closings). Data: `res1.jsonl` and `res2.jsonl`. The analysis runs were still going at hand-off, so the tables below cover 7 instances.

Labels: **[P]** proved, **[M]** measured, **[C]** conjecture.

## Numbers [M]

Instances: the 3 saved R = 3 closings on ico20 (`e4_R3`, `e6_R3`, `s1_hard`), with L = 222–272, |t| = 2 on both sides and the best renaming applied. Also 4 newly generated R = 2 closings on ico20 (L ≈ 222, |t| = 2). No genuine R = 0 closing was generated: in 70 new pairs, R was 1 or 2. As an R = 0 control, I glued the SAT-repaired colouring of two instances, which gives zero conflicts.

Set-up:
- Band = vertices within seam distance k. k = 1 gives 4 rows and k = 2 gives 6 rows.
- The rows just outside the band are pinned to tetrahedron corners.
- Edge constraints are dot = −1/3.
- Solver: Burer–Monteiro with d = 12. A penalty below 1e-7 gives an explicit feasible Gram matrix.
- The one band-0 infeasibility I checked was confirmed by SCS (ico10, R = 2).

| | R = 3 (3 instances) | R = 2 (4 instances) | conflict-free control |
|---|---|---|---|
| band 0 (seam rows only free): penalty | 0.11–0.32, **infeasible** | 0.02–0.28, **infeasible** | **feasible** |
| band 1 (4 rows) | feasible in 3/3 | feasible in 4/4 | feasible |
| N_r(conflicts) feasible from r = | 2, 2, **1** | 2 in 4/4 | 0 |
| generic solution (random start), k = 2: median distance to nearest corner / projection onto corner span / fraction snapped (< 0.1) | 1.09–1.11 / 0.58 / 0.03–0.05 | 1.08–1.10 / 0.58 / 0.01–0.02 | — |
| nearest solution (old-colour start), k = 2: fraction of band vertices with distance > 0.5 | 0.14–0.15 | 0.05–0.11 | 0 (max distance 0.23) |
| seam positions with a deviated vertex (distance > 0.3) | 57–68% | 27% (one instance; 14% for one R = 1) | 0% |
| triangle-frame rotation angle, median / max | 0.7–0.8° / 61–62° | 0.4–0.6° / 46–65° | — |
| Spearman correlation along the seam (smoothed): SDP distance vs SAT changes | 0.52–0.83 | 0.71–0.87 | — |
| same, but conflict density vs SAT changes (baseline) | 0.49–0.82 | 0.70–0.98 | — |
| per-vertex AUC for predicting SAT-recoloured vertices: SDP distance vs closeness to a conflict | 0.71–0.74 vs 0.70–0.74 | 0.87–0.92 vs 0.81–0.89 | — |
| Spearman correlation: height-offset proxy vs SAT changes | −0.11 to 0.35 | 0.28–0.81 | — |

Further measurements from `shape.py` on 5 instances:
- Deviated seam positions lie within ±1 position of a conflict in 97–100% of cases, and every conflict position has a deviated vertex nearby.
- The mean distance decays away from the seam: 0.47–0.51 at depth 0, 0.22 at depth 1 and 0.12 at depth 2.
- Deviated vertices have projection norm 0.63–0.86, so they leave the 3-dimensional corner span.
- The deviated region forms 4–15 runs along the seam. The longest run is 28 of 111 positions, and each run follows a stretch of conflicts.

## Answers

1. **No smooth twist.** [M] There are two kinds of solution, and neither shows a rotation spread smoothly along the seam.
   - The generic SDP solution is fractional everywhere: distance about 1.1 and projection 0.58 in every instance, whatever R is. It does not localise anything.
   - The solution nearest the old colouring snaps to corners away from conflicts. Inside conflict stretches it deviates in blocks, and the deviation is partly out of span rather than a rotation within the span. The frame angle is near 0° almost everywhere, with spikes up to about 60°.
2. **Where the deviation sits.** [M] It sits where SAT recolours, but only as well as the conflict set already shows. Its correlation with SAT changes matches the conflict-density baseline within ±0.1 (AUC gain ≤ 0.08). The deviated fraction of the seam grows with R (about 14% at R = 1, 27% at R = 2, 57–68% at R = 3), but so does the number of conflicts (13 → 27–66 → 79–107).
   - The link to the height mismatch is weak and inconsistent (ρ from −0.11 to 0.81). The caveat is that my offset proxy (heights on the two walks, matched over seam edges, compared with the modal offset) is crude: its radius came out ≤ 1.94, consistent with Lemma 2.
3. **Feasibility does not predict R.** [M] Band 0 was infeasible in 7/7 instances and band 1 was feasible in 7/7, whether R was 2 or 3. In one R = 3 case, N_1(conflicts) was already SDP-feasible. So the vector relaxation is about 2 radius units weaker than SAT and does not separate R = 2 from R = 3. The band-0 penalty overlaps between the two groups.
4. **[P] Why a twist cannot be rigid in 3D.** In R³, the unit vectors at dot −1/3 to two corners of a tetrahedron are exactly the other two corners. So on a connected triangulated band, an exact solution of rank 3 is a genuine 4-colouring: it is rigid, with no continuous twist. Any "twist" must therefore use dimensions beyond 3, which is what the out-of-span deviations show.
5. **[C]** The SDP sees the local rigidity defects (the conflicts) but not the global offset structure that makes R = 3. If an interpretable height certificate exists, it would have to come from a relaxation that carries the Z3 or height data explicitly, not from the tetrahedral Gram matrix.

## Calibration

- The sample is small: 3 R = 3 and 4 R = 2 instances, all on ico20. No genuine R = 0 instance with conflicts was tested.
- The "nearest" solution comes from a local optimiser started at the old colouring, not from an SDP objective. Background distances of 0.1–0.2 are drift along the zero-penalty set.
- Feasibility claims rest on penalties below 1e-7. Infeasibility rests on a positive penalty floor over 2 random starts with d = 12, and SCS confirmed it in one case.

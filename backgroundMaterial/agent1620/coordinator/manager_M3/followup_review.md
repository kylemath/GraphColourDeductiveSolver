# Follow-up review — Reviewer 3 (Empirical Claims and Internal Consistency)

**Manuscript:** revised `04-results.tex` (and spot-check of `02-background.tex` for residual R2).

**Role:** Evaluate whether prior concerns in the Results section were addressed, and whether residual items R1–R5 are resolved.

---

## Original edits (EDITS APPLIED) — status

| ID | Concern | Status |
|----|---------|--------|
| 1 | Table consistency | **RESOLVED / N/A** — The counterexample summary table remains internally consistent; no change was required previously. |
| 2a | Energy values lacked normalization context | **RESOLVED** — Magic Gem energy is labeled “(dimensionless; defined in Section on MG energy)”. |
| 2b | “Smooth descent” incorrect for non-monotone path | **RESOLVED** — Unsafe path is “greedy descent then barrier”; safe path is “ridge then non-monotone” with explicit stepwise deltas and no claim of monotonicity on the safe branch. |
| 2c | Trajectory presented as aggregate though single coloring | **RESOLVED** — Text states values are “for a single representative counterexample coloring in $T_{9,25}$”. |
| 3 | Entropy: average vs single coloring ambiguous | **RESOLVED** — Entropy equations are introduced with “For $T_{9,25}$ (averaged over all 24 counterexample colorings)”. |
| 4a | Surface tension scope unclear | **RESOLVED** — Opens with “Across all 48 counterexample colorings at $n = 9$” for the zero-variance claim. |
| 4b | “Maximally rigid, inflexible” double superlative | **RESOLVED** — Wording is simplified to “rigid configuration with no structural variability”. |
| 5a | Ridge height read as continuous range | **RESOLVED** — Two discrete contexts: $T_{9,25}$ vs $T_{9,35}$, each with a stated representative coloring and explicit $\Delta E_{\mathrm{MG}}$ (0.862 vs 0.96). |
| 5b | $\approx 0.86$ vs exact 0.862 | **RESOLVED** — Ridge step uses $0.862$ consistently in the trajectory and Basin~B discussion for $T_{9,25}$. |
| 7a | Falsification lacked mechanism | **RESOLVED** — Remark states exhaustive computation at $n \geq 10$ found instances with $\rho_{ab} = 0$ for **safe** swaps, violating the implication. |
| 7b | “Holds perfectly” redundant | **RESOLVED** — Phrase removed; replaced by factual “holds for all 48 counterexamples at $n = 9$”. |
| 7c | “Breaks down” vague | **RESOLVED** — Replaced by “does not generalize to $n \geq 10$” and “this pattern does not persist at larger scales”. |
| 8 | Editorializing (“cleanest”, “clearest”, “precisely analogous”) | **RESOLVED** — These phrases do not appear in the current `04-results.tex`. |

---

## Residual issues (R1–R5) — status

| ID | Topic | Status in revised manuscript |
|----|--------|------------------------------|
| **R1** | Counterexample / falsification count at $n \geq 10$ | **NOT ADDRESSED** — The falsification remark names the phenomenon (safe swaps with $\rho_{ab}=0$) but does not report how many instances, at which $n$, or scope of the search. |
| **R2** | Denominator for 87.6% (in `02-background`, not Results) | **NOT ADDRESSED** — `02-background.tex` still gives “87.6\% of (graph, coloring, vertex) triples” without the total count or an explicit “$N = \ldots$ triples enumerated.” |
| **R3** | $T_{9,35}$ trajectory / verifiability of 0.96 ridge | **PARTIALLY ADDRESSED** — Basin~B now states $\Delta E_{\mathrm{MG}} = 0.96$ for $T_{9,35}$ with the same “representative coloring” caveat as $T_{9,25}$, but there is still no figure or step list for $T_{9,35}$ analogous to the $T_{9,25}$ trajectory and barrier plot; independent verification from the manuscript alone remains limited. |
| **R4** | Entropy variance across colorings | **NOT ADDRESSED** — Only means $\bar{S}_{\text{unsafe}}$, $\bar{S}_{\text{safe}}$, and $\Delta S$ are reported; no standard deviation, range, or per-coloring spread. |
| **R5** | “Paradoxically” | **NOT ADDRESSED** — The phrase “which paradoxically reduces the structural diversity…” remains in the Local Entropy paragraph. |

**Minor note (optional):** For $T_{9,35}$, the ridge is given as `0.96` (two decimals) while $T_{9,25}$ uses three (`0.862`). If the underlying value is not exactly $0.96$, aligning precision or giving the same number of significant figures would improve consistency.

---

## Summary

The revision substantively fixes the earlier factual and clarity problems in Results, including the non-monotone trajectory wording, normalization of $E_{\mathrm{MG}}$, explicit averaging for entropy, scope for surface tension, discrete ridge characterization for the two triangulations, and a mechanistic falsification remark without vague “breaks down” / “holds perfectly” language. Editorial superlatives in Results appear removed.

Outstanding items are mainly **reporting depth**: counts for $n \geq 10$ falsification (**R1**), entropy dispersion (**R4**), optional tightening of $T_{9,35}$ presentation (**R3**), softening or justifying “paradoxically” (**R5**), and the background census denominator (**R2**, outside `04-results.tex`).

**Overall assessment:** Prior Results-section concerns are **largely resolved**; residual issues **R1, R2, R4, R5** remain, with **R3** improved but not fully closed for readers who want parity of evidence across both triangulations.

---

*Reviewer 3 (Empirical Claims and Internal Consistency)*

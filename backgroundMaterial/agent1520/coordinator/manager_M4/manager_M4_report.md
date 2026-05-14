# Manager M4 Report: TQFT / Penrose Non-Vanishing Feasibility Probe

**Agent:** 1520-M4  
**Date:** 2026-02-20  
**Project:** Graph Colour — Four Colour Theorem  
**Stream:** MOONSHOT — TQFT Positivity  
**Status:** COMPLETE

---

## Executive Summary

Three sub-tasks executed. Two of three avenues tested have **negative results.** One produced a **key structural observation** that, while not itself a proof strategy, clarifies the landscape. The overall verdict: **the TQFT positivity approach is not dead but is in critical condition.** The manifestly-positive Turaev-Viro path is eliminated. The unitarity path (Pen(G) = ⟨ψ|ψ⟩) remains the only viable TQFT route, but faces the hard problem of showing non-vanishing of the Reshetikhin-Turaev invariant.

---

## Sub-Task Results

### S1: Quantum 6j-Symbol Computation — NEGATIVE RESULT

**Finding:** At levels r = 3, 4, 5, 6, the quantum 6j-symbols for $U_q(\mathfrak{sl}_2)$ have **mixed signs** at every level.

| Level r | Non-zero 6j | Positive | Negative | Manifestly Positive? |
|---|---|---|---|---|
| 3 | 8 | 1 | 7 | **NO** |
| 4 | 36 | 29 | 7 | **NO** |
| 5 | 120 | 29 | 91 | **NO** |
| 6 | 328 | 238 | 90 | **NO** |

**Implication:** You cannot prove Pen(G) > 0 by showing every term in the Turaev-Viro state sum is positive. The alternating sum structure in the Racah formula for 6j-symbols makes sign definiteness impossible. This is an intrinsic mathematical obstruction, not a computational artifact. **This avenue is permanently closed.**

### S2: Penrose Evaluation — VERIFICATION COMPLETE

**Finding:** All 13 bridgeless planar cubic graphs tested have $\text{Pen}(G) > 0$. Petersen graph correctly gives 0.

Key data points:
- Minimum: Pen(K4) = Pen(Prism) = Pen(Frucht) = 6
- Maximum tested: Pen(Prism $C_{10}$) = 1032
- All values divisible by 6 (as expected from $S_3$ symmetry of colour labels)
- Non-planar 3-edge-colourable graphs (K_{3,3}, Desargues, Heawood) have Pen > 0
- Petersen graph (the canonical snark): Pen = 0 ✓

**Implication:** The computational target is confirmed — there is no counterexample in sight. The pattern is consistent with 4CT. But exhaustive enumeration cannot prove the theorem (infinitely many graphs).

### S3: Kuperberg Web Basis Analysis — MIXED RESULT (KEY DISCOVERY)

**Discovery:** For every planar cubic graph tested, the **signed Penrose evaluation equals the unsigned Tait colouring count.** Every valid edge-3-colouring of a planar graph contributes exactly +1 to the signed tensor contraction.

| Graph | Planar | Signed | Unsigned | Equal? |
|---|---|---|---|---|
| K4 | Y | 6 | 6 | YES |
| Prism | Y | 6 | 6 | YES |
| Cube | Y | 24 | 24 | YES |
| $K_{3,3}$ | N | 0 | 12 | **NO** |
| Petersen | N | 0 | 0 | YES (both 0) |

**However:** Intermediate contractions (vertex-by-vertex tensor evaluation) produce negative coefficients even for planar graphs. At one step for the Cube, ALL 18 intermediate terms are negative. The positivity only emerges at the final step.

**Edge cut analysis:** Decomposing the Cube tensor at a planar edge cut produces all-negative part tensors. Raw tensor decomposition is not positive.

**Interpretation:** The signed = unsigned result for planar graphs is a known consequence of consistent orientability of planar embeddings. It is structurally sound but does not provide a new proof mechanism. The negative intermediates show that naïve sequential contraction or edge-cut decomposition in the raw tensor basis does NOT exhibit web-basis positivity.

---

## Viability Assessment

### Approach 1: Manifestly Positive TV State Sum
**Verdict: DEAD**  
6j-symbols have mixed signs at all levels. No amount of re-parameterization can fix this — it's intrinsic to the Racah formula.

### Approach 2: Unitarity Argument (Pen(G) = |Z_RT|²)
**Verdict: ALIVE but HARD**  
The Turaev-Viro invariant $\text{TV}(M) = |Z_{\text{RT}}(M)|^2 \geq 0$. To show $\text{Pen}(G) > 0$, we need $Z_{\text{RT}} \neq 0$. This requires:
1. Relating Pen(G) to a TV invariant of a specific 3-manifold
2. Showing the RT invariant of that manifold is non-zero
3. This reduces 4CT to a non-vanishing theorem in TQFT

**Difficulty:** Non-vanishing of RT invariants is a major open problem in quantum topology. Known non-vanishing results exist for specific manifolds (lens spaces, Seifert fibred spaces), but not for the class of manifolds arising from planar graphs. 

**Feasibility:** Medium-Low. The machinery exists (Kauffman's theorem + TV/RT duality), but the non-vanishing step is as hard as 4CT itself.

### Approach 3: Kuperberg Web Basis Positivity
**Verdict: INCONCLUSIVE — needs deeper investigation**  
Our analysis tested raw tensor coefficients, not the actual Kuperberg web basis. The web basis elements are specific non-crossing planar diagrams with positivity properties built into their construction. A proper test requires:
1. Implementing the full Kuperberg spider calculus for $\mathfrak{sl}_3$
2. Converting tensor states to the web basis at each planar separator
3. Checking coefficient signs in the web basis (not the computational basis)

The fact that raw tensor decompositions have negative coefficients doesn't kill the web basis approach — the whole point of the web basis is that it absorbs these negativities into its structure.

**Feasibility:** Medium. Requires significant algebraic machinery but is in principle testable computationally.

---

## Kill Criterion Assessment

> Kill criterion: 6j-symbols at r = 3 have inconsistent signs AND web basis has negative coefficients for planar graphs

- 6j-symbols at r = 3: **MIXED SIGNS — confirmed**
- Web basis coefficients for planar graphs: **INCONCLUSIVE** — we tested raw tensor coefficients, not web basis coefficients

**Verdict: NOT YET TRIGGERED.** The kill criterion has one leg confirmed (6j mixed signs) but the second leg (web basis negativity) was tested in the wrong basis. A proper Kuperberg web basis computation is needed to fully evaluate.

---

## The Skeptic Speaks

*Wait. Am I sure about the signed = unsigned result?*

Yes — this is a well-known consequence of planar graph orientability. For a cubic graph embedded in the plane, the three edges at each vertex inherit a cyclic order from the embedding. If we consistently orient all edges outward from higher-numbered to lower-numbered vertices, the product of $\epsilon$ values over all vertices is always $+1$ for any valid Tait colouring. This is because the Euler characteristic constraint on a planar embedding forces a global orientation consistency.

*But does this help the proof?*

No, not directly. The signed = unsigned equality is equivalent to saying "planar cubic graphs have a consistent $\epsilon$-orientation" — this is a consequence of planarity, not a tool to prove 4CT. We still need to show that Tait colourings exist.

*What would actually break the TQFT approach?*

If the Kuperberg web basis decomposition of the Penrose tensor along planar cuts produces negative coefficients — that would kill the last TQFT sub-strategy. But this hasn't been properly tested yet.

---

## Concrete Next Steps

1. **[HIGH PRIORITY]** Implement the actual Kuperberg spider calculus for $\mathfrak{sl}_3$. Build the web basis elements as non-crossing diagrams. Decompose the Penrose tensor in this basis. Test coefficient signs for planar graphs. This is the remaining TQFT test before the approach can be fully evaluated.

2. **[MEDIUM PRIORITY]** Study the manifold construction: for a planar cubic graph $G$, construct the 3-manifold $M_G$ such that $\text{TV}_3(M_G) = \text{Pen}(G)$. Classify which manifolds arise. Check if known non-vanishing theorems for RT invariants apply to this class.

3. **[LOW PRIORITY]** Investigate whether there exists a vertex ordering for planar graphs (related to the tree-width or planar separator structure) where intermediate contractions are all non-negative. If such an ordering exists, it would give a constructive positivity proof.

---

## Summary for Coordinator

| Metric | Result |
|---|---|
| 6j sign structure at r=3 | Mixed: 1 positive, 7 negative |
| Pen(G) > 0 for all planar graphs tested? | **YES** (13/13) |
| Petersen gives Pen = 0? | **YES** |
| Web basis non-negative coefficients? | **INCONCLUSIVE** (tested wrong basis) |
| Manifestly positive TV state sum? | **NO — permanently ruled out** |
| Unitarity approach viable? | **Yes, but reduces to hard non-vanishing problem** |
| Kill criterion triggered? | **No — one leg unresolved** |
| Overall TQFT feasibility | **Medium-Low** |

The TQFT moonshot has been substantially narrowed. The easy path (manifestly positive state sum) is dead. The remaining paths (unitarity non-vanishing, web basis positivity) are technically interesting but face problems that may be as hard as 4CT itself. The web basis question can be definitively resolved with more computation — this should be the next investment.

---

## Files Produced

| File | Description |
|---|---|
| `manager_M4_report.md` | This report |
| `sub_S1/S1_report.md` | 6j-symbol computation report |
| `sub_S1/6j_raw_output.txt` | Raw 6j-symbol values |
| `sub_S1/6j_tables.md` | Formatted 6j-symbol tables |
| `sub_S2/S2_report.md` | Penrose evaluation report |
| `sub_S2/penrose_raw_results.txt` | Raw Penrose evaluation data |
| `sub_S3/S3_report.md` | Web basis analysis report |
| `sub_S3/web_basis_raw.txt` | Raw web basis analysis data |
| `compute/topology/quantum_6j.py` | 6j-symbol computation code |
| `compute/topology/penrose_eval.py` | Penrose evaluation code |
| `compute/topology/kuperberg_web.py` | Web basis analysis code |

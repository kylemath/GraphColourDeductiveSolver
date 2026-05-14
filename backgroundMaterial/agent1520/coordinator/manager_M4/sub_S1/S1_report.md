# S1 Report: Quantum 6j-Symbol Computation

**Agent:** 1520-M4-S1 (6j-Symbol Computation)  
**Date:** 2026-02-20  
**Status:** COMPLETE — NEGATIVE RESULT

---

## Summary

Computed all admissible quantum 6j-symbols for $U_q(\mathfrak{sl}_2)$ at $q = e^{i\pi/r}$ for $r = 3, 4, 5, 6$. **All levels exhibit mixed signs.** The naïve "manifestly positive Turaev-Viro state sum" approach to 4CT is ruled out.

---

## Background

The Turaev-Viro (TV) state sum for a triangulated 3-manifold $M$ is:
$$\text{TV}_r(M) = \sum_{\ell: \text{edges} \to \text{labels}} \prod_e d_{\ell(e)} \prod_t \begin{Bmatrix} j_1 & j_2 & j_3 \\ j_4 & j_5 & j_6 \end{Bmatrix}_q$$
where the sum is over admissible labellings, $d_j = [2j+1]_q$ is the quantum dimension, and the product is over tetrahedra with their 6j-symbols.

At level $r$, admissible spins are $j = 0, \frac{1}{2}, \ldots, \frac{r-2}{2}$.

If all 6j-symbols had the same sign, $\text{TV}_r$ would be manifestly positive (or negative), and we could deduce $\text{Pen}(G) > 0$ for planar graphs from the topological invariance of TV.

## Results

### r = 3 (Critical Level for 4CT)

- **Admissible spins:** $j = 0, \frac{1}{2}$
- **Quantum dimensions:** $d_0 = 1$, $d_{1/2} = 1$
- **Non-zero 6j-symbols:** 8
- **Sign pattern:** 1 positive, 7 negative
- **Verdict:** MIXED SIGNS

The single positive 6j-symbol is $\{0, 0, 0; 0, 0, 0\} = 1$. All others are negative.

### r = 4

- **Admissible spins:** $j = 0, \frac{1}{2}, 1$
- **Quantum dimensions:** $d_0 = 1$, $d_{1/2} = \sqrt{2}$, $d_1 = 1$
- **Non-zero 6j-symbols:** 36
- **Sign pattern:** 29 positive, 7 negative
- **Verdict:** MIXED SIGNS

### r = 5

- **Admissible spins:** $j = 0, \frac{1}{2}, 1, \frac{3}{2}$
- **Quantum dimensions:** $d_0 = 1$, $d_{1/2} = \phi = 1.618...$, $d_1 = \phi$, $d_{3/2} = 1$
- **Non-zero 6j-symbols:** 120
- **Sign pattern:** 29 positive, 91 negative
- **Verdict:** MIXED SIGNS (majority negative)

### r = 6

- **Admissible spins:** $j = 0, \frac{1}{2}, 1, \frac{3}{2}, 2$
- **Quantum dimensions:** $d_0 = 1$, $d_{1/2} = \sqrt{3}$, $d_1 = 2$, $d_{3/2} = \sqrt{3}$, $d_2 = 1$
- **Non-zero 6j-symbols:** 328
- **Sign pattern:** 238 positive, 90 negative
- **Verdict:** MIXED SIGNS

### Summary Table

| Level $r$ | Spins | Non-zero 6j | Positive | Negative | Manifestly Positive? |
|---|---|---|---|---|---|
| 3 | 0, 1/2 | 8 | 1 | 7 | **NO** |
| 4 | 0, 1/2, 1 | 36 | 29 | 7 | **NO** |
| 5 | 0, 1/2, 1, 3/2 | 120 | 29 | 91 | **NO** |
| 6 | 0, 1/2, 1, 3/2, 2 | 328 | 238 | 90 | **NO** |

---

## Analysis

### Why Manifest Positivity Fails

The 6j-symbols are generalizations of Clebsch-Gordan coupling coefficients. They satisfy orthogonality relations (Biedenharn-Elliott identity) but have no reason to have definite sign. The classical (non-quantum) 6j-symbols also have mixed signs, and the quantum deformation doesn't change this structure.

Specifically, the negative signs arise from the alternating sum in the Racah formula:
$$\begin{Bmatrix} j_1 & j_2 & j_3 \\ j_4 & j_5 & j_6 \end{Bmatrix} = \Delta(j_1 j_2 j_3) \Delta(j_1 j_5 j_6) \Delta(j_2 j_4 j_6) \Delta(j_3 j_4 j_5) \sum_z (-1)^z \frac{[z+1]!}{\prod_i [z - a_i]! \prod_j [b_j - z]!}$$

The $(-1)^z$ factor guarantees sign alternation.

### What This Means for the TQFT Approach

1. **Manifest positivity is dead.** We cannot prove Pen(G) > 0 by showing each term in the TV state sum is positive. This approach fails at every level tested.

2. **Unitarity is still alive.** The Turaev-Viro invariant equals $|Z_{\text{RT}}(M)|^2$ where $Z_{\text{RT}}$ is the Reshetikhin-Turaev invariant. This "square" structure guarantees $\text{TV} \geq 0$, but proving $\text{TV} > 0$ requires showing $Z_{\text{RT}} \neq 0$.

3. **The level r = 3 is degenerate.** With only 2 admissible spins and quantum dimensions both equal to 1, the state space is very constrained. The negative 6j-symbols suggest non-trivial interference.

---

## Code

Implementation: `compute/topology/quantum_6j.py`  
Raw output: `sub_S1/6j_raw_output.txt`  
Formatted tables: `sub_S1/6j_tables.md`

---

## Conclusion

**The manifestly positive Turaev-Viro state sum approach is not viable at any tested level.** Mixed signs are an intrinsic feature of 6j-symbols, not an artifact of the quantum deformation. Any TQFT-based positivity proof must work through unitarity ($\text{TV} = |Z|^2$) or find a different positive decomposition (e.g., Kuperberg webs).

**Feasibility rating:** LOW for manifest positivity via 6j-signs. MEDIUM for alternative TQFT approaches (unitarity, web basis).

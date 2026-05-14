# Sub-task S2 Report: Extension to $n = 10$

**Agent:** 1520-M2-S2  
**Date:** 2026-02-20  
**Scope:** Extend surface tension rigidity computation to $n = 10$ (233 triangulations)

---

## 1. Executive Summary

Surface tension rigidity was computed for **2,859,072 cases** across 233 triangulations at $n = 10$. The results confirm and extend the findings from $n \leq 9$:

- **Local flexibility direction** ($\rho_{\text{local}} > 0 \Rightarrow$ merge-prone): **100% perfect** (1,818,552 cases, 0 exceptions) — remains trivially true
- **Global flexibility direction** ($\rho_{\text{global}} > 0 \Rightarrow$ merge-prone): **97.3%** (52,656 exceptions) — continuing degradation

The original conjecture ($\rho = 0 \Rightarrow$ merge-prone) fails even more severely at $n = 10$ than at smaller $n$.

---

## 2. Results

### 2.1 Data Volume

| Metric | Value |
|--------|-------|
| Triangulations | 233 |
| Total cases examined | 2,859,072 |
| Merge-prone | 2,146,392 (75.1%) |
| Safe | 712,680 (24.9%) |
| Computation time | 159.5 seconds |

### 2.2 Global Rigidity Confusion Matrix

|  | Merge-prone | Safe | Total |
|---|---|---|---|
| Rigid ($\rho = 0$) | 224,352 | 660,024 | 884,376 |
| Flexible ($\rho > 0$) | 1,922,040 | 52,656 | 1,974,696 |
| **Total** | **2,146,392** | **712,680** | **2,859,072** |

### 2.3 Direction Analysis

| Direction | $n \leq 8$ | $n = 9$ | $n = 10$ | Trend |
|-----------|-----------|---------|----------|-------|
| $\rho_{\text{global}} > 0 \Rightarrow$ mp | 100% | 99.6% | 97.3% | Degrading |
| safe $\Rightarrow \rho_{\text{global}} = 0$ | 100% | 98.9% | 92.6% | Degrading |
| $\rho_{\text{local}} > 0 \Rightarrow$ mp | 100% | 100% | 100% | Stable (trivial) |

### 2.4 Interpretation

The global flexibility direction continues to degrade predictably: as $n$ increases, the number of $(a,5)$-chains grows, making it increasingly likely that safe cases have chains with varying $\bar{\sigma}$.

At $n = 10$:
- A "safe" case has all $v$-neighbors in one chain, but the graph may contain many other chains with diverse $\bar{\sigma}$
- 52,656 safe cases have $\rho_{\text{global}} > 0$ — the non-incident chains have different tensions
- This is purely a graph-size effect, not a structural insight

---

## 3. Merge-Prone Rate by $n$

| $n$ | Merge-prone / Total | Rate |
|-----|---------------------|------|
| 6 | 480 / 480 | 100% |
| 7 | 3,672 / 4,440 | 82.7% |
| 8 | 25,128 / 33,624 | 74.7% |
| 9 | 200,784 / 267,360 | 75.1% |
| 10 | 2,146,392 / 2,859,072 | 75.1% |

The merge-prone rate stabilizes around 75% for $n \geq 8$, suggesting this is the asymptotic fraction.

---

## 4. Extension to $n = 11, 12$

### 4.1 Feasibility

| $n$ | Triangulations (OEIS A000109) | Estimated time | Status |
|-----|-------------------------------|----------------|--------|
| 10 | 233 | 2.7 min | **Completed** |
| 11 | 1,249 | ~15 min | Not attempted (triangulation generation is the bottleneck) |
| 12 | 7,595 | ~2 hours | Not attempted |

The triangulation generation uses isomorphism filtering which scales poorly. At $n = 11$, generating 1,249 triangulations would take ~10 minutes, and the rigidity computation another ~5 minutes. This is feasible but was deprioritized because:

1. The conjecture is already refuted
2. The trend at $n = 10$ is clear — no new structural insight expected
3. The all-paths analysis (needed to identify hard counterexamples) becomes prohibitively expensive at $n \geq 10$

### 4.2 Recommendation

Do NOT extend to $n \geq 11$ for surface tension analysis. The conjecture is dead. Redirect computational resources to:
1. {1,2,3,4}-Swap Sufficiency testing at $n = 10$
2. Identifying new all-paths-unsafe counterexamples at $n = 10$ (these would be valuable for Agent M1's attack)

---

## 5. Code

Validation code: `compute/kempe/surface_tension_validation.py` (function `run_extended_validation`)

---

*Agent 1520-M2-S2 — Graph Colour Project*  
*20 February 2026*

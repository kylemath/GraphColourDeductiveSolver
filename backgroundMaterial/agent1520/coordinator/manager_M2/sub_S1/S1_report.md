# Sub-task S1 Report: Retroactive Validation of Surface Tension Rigidity

**Agent:** 1520-M2-S1  
**Date:** 2026-02-20  
**Scope:** Compute surface tension rigidity for ALL merge-prone colourings in Agent 1210's dataset ($n \leq 8$, 1,224 merge-prone cases), plus extension to $n = 9$ (48 counterexamples + all merge-prone cases)

---

## 1. Executive Summary

Surface tension rigidity $\rho_{ab}(c)$ was computed for **38,544 cases at $n \leq 8$** and **267,360 cases at $n = 9$**, using two variants:

- **Global rigidity** $\rho_{\text{global}}$: variance of $\bar{\sigma}(K)$ over ALL $(a,5)$-chains
- **Local rigidity** $\rho_{\text{local}}$: variance of $\bar{\sigma}(K)$ over chains incident to $v$

**Key result:** The conjecture $\rho = 0 \Rightarrow$ merge-prone is **FALSE** in both variants. However, the converse direction ($\rho > 0 \Rightarrow$ merge-prone) has interesting behavior:

| Direction | Global ($n \leq 8$) | Global ($n = 9$) | Local (all $n$) |
|-----------|--------------------|--------------------|-----------------|
| $\rho > 0 \Rightarrow$ merge-prone | 100% (20,112/20,112) | 99.59% (175,728/176,448) | 100% (trivially) |
| safe $\Rightarrow \rho = 0$ | 100% (9,264/9,264) | 98.92% (65,856/66,576) | 100% (trivially) |

---

## 2. Methodology

### 2.1 Definitions

For a proper 5-colouring $c$ of planar triangulation $G$, vertex $v$ with $c(v) = 5$, colour pair $(a, 5)$:

$$\sigma(K) = |\{(u,w) \in E(G-v) : u \in K, w \notin K\}|$$
$$\bar{\sigma}(K) = \sigma(K) / |K|$$
$$\rho_{a,5}(c) = \text{Var}(\bar{\sigma}(K_1), \ldots, \bar{\sigma}(K_m))$$

where $K_1, \ldots, K_m$ are the $(a,5)$-Kempe chains in $G - v$.

### 2.2 Classification

A case $(G, v, c, a)$ is:
- **Merge-prone** if $v$ has neighbors in $\geq 2$ distinct $(a,5)$-chains in $G-v$
- **Safe** if $v$ has neighbors in $\leq 1$ chain (but $\geq 2$ neighbors in $B_{a,5}$)
- **Rigid** if $\rho < 10^{-12}$
- **Flexible** if $\rho \geq 10^{-12}$

### 2.3 Filtering

We examine every 5-colouring of every triangulation, every vertex $v$ with $c(v) = 5$ and $\deg(v) \in \{4, 5\}$, every colour $a \in \{1,2,3,4\}$ where $v$ has $\geq 2$ neighbors in $B_{a,5}(G-v)$.

---

## 3. Phase 1 Results: $n \leq 8$

### 3.1 Data Volume

| $n$ | Graphs | Total cases | Merge-prone | Safe |
|-----|--------|-------------|-------------|------|
| 4 | 1 | 0 | 0 | 0 |
| 5 | 1 | 0 | 0 | 0 |
| 6 | 2 | 480 | 480 | 0 |
| 7 | 5 | 4,440 | 3,672 | 768 |
| 8 | 14 | 33,624 | 25,128 | 8,496 |
| **Total** | **23** | **38,544** | **29,280** | **9,264** |

### 3.2 Global Rigidity Confusion Matrix

|  | Merge-prone | Safe | Total |
|---|---|---|---|
| Rigid ($\rho = 0$) | 9,168 | 9,264 | 18,432 |
| Flexible ($\rho > 0$) | 20,112 | 0 | 20,112 |
| **Total** | **29,280** | **9,264** | **38,544** |

- $\rho = 0 \Rightarrow$ merge-prone: **49.7%** (fails — 9,264 exceptions)
- merge-prone $\Rightarrow \rho = 0$: **31.3%** (fails — 20,112 exceptions)
- **$\rho > 0 \Rightarrow$ merge-prone: 100%** (0 exceptions at $n \leq 8$)
- **safe $\Rightarrow \rho = 0$: 100%** (0 exceptions at $n \leq 8$)

### 3.3 Local Rigidity Confusion Matrix

|  | Merge-prone | Safe | Total |
|---|---|---|---|
| Rigid ($\rho = 0$) | 10,128 | 9,264 | 19,392 |
| Flexible ($\rho > 0$) | 19,152 | 0 | 19,152 |
| **Total** | **29,280** | **9,264** | **38,544** |

Local rigidity is trivially consistent: safe cases have 1 incident chain (variance of 1 value = 0), so safe $\Rightarrow \rho_{\text{local}} = 0$ is a tautology.

---

## 4. Phase 2 Results: $n = 9$

### 4.1 Data Volume

- 50 triangulations, 267,360 total cases
- 200,784 merge-prone, 66,576 safe

### 4.2 Global Rigidity at $n = 9$

|  | Merge-prone | Safe | Total |
|---|---|---|---|
| Rigid ($\rho = 0$) | 25,056 | 65,856 | 90,912 |
| Flexible ($\rho > 0$) | 175,728 | 720 | 176,448 |

**$\rho > 0 \Rightarrow$ merge-prone fails with 720 exceptions** (0.41% error rate).

### 4.3 Local Rigidity at $n = 9$

|  | Merge-prone | Safe | Total |
|---|---|---|---|
| Rigid ($\rho = 0$) | 34,512 | 66,576 | 101,088 |
| Flexible ($\rho > 0$) | 166,272 | 0 | 166,272 |

Local direction remains trivially perfect.

### 4.4 Targeted Analysis: The 48 Hard Counterexamples

For the 48 colorings where ALL BFS-optimal paths are unsafe:

| Graph | All-unsafe | Global $\rho$ | Local $\rho$ | Chain structure |
|-------|-----------|--------------|-------------|-----------------|
| T_9_25 | 24 | 0.000 (all) | 0.000 (all) | Two size-2 chains, both $\bar{\sigma} = 2.5$ |
| T_9_35 | 24 | 0.0625 (all) | 0.0625 (all) | Two size-2 chains, $\bar{\sigma} = \{2.5, 3.0\}$ |

**T_9_35 REFUTES the conjecture even within the counterexample set.** Its all-paths-unsafe colorings have $\rho > 0$.

For comparison, the 162,696 has-safe-optimal merge-prone cases at $n = 9$:
- Global $\rho = 0$: 17,160 cases (10.5%)
- Global $\rho > 0$: 145,536 cases (89.5%)

---

## 5. Correlation with Agent 1210's Data

Agent 1210 reported 1,224 merge-prone cases at $n \leq 8$ (556 at degree 4, 668 at degree 5). Our analysis found **29,280** merge-prone cases because we count over ALL colour pairs $(a,5)$ for each colouring, not just the pair that BFS would swap.

Mapping to Agent 1210's metric:
- Agent 1210 counted unique (graph, vertex, colouring) tuples where the BFS first path uses an unsafe swap
- We count (graph, vertex, colouring, colour_pair) tuples where the structure is merge-prone

The 1,224 cases are a subset of our 29,280. Our analysis provides a superset that includes ALL colour pairs, not just the BFS-selected one.

---

## 6. Key Findings

1. **The conjecture as stated is false.** Neither direction of the biconditional holds.
2. **The global flexibility direction ($\rho > 0 \Rightarrow$ merge-prone) is non-trivially strong at $n \leq 8$ (100%)** but weakens at $n \geq 9$.
3. **The local flexibility direction is trivially true** and provides no useful information.
4. **T_9_35 refutes the conjecture within the counterexample set** — its all-paths-unsafe colorings have $\rho = 0.0625 > 0$.
5. **Agent 1443's original finding was about consistency across colorings** (all 24 counterexamples of T_9_25 produce chains with tension 5.0), not about variance within a coloring. The task brief's formalization as $\rho_{ab}(c)$ appears to be a misinterpretation.

---

## 7. Code

Validation code: `compute/kempe/surface_tension_validation.py`  
Targeted analysis: `compute/kempe/surface_tension_targeted.py`  
Results JSON: `backgroundMaterial/agent1520/coordinator/manager_M2/sub_S1/rigidity_validation_results.json`

---

*Agent 1520-M2-S1 — Graph Colour Project*  
*20 February 2026*

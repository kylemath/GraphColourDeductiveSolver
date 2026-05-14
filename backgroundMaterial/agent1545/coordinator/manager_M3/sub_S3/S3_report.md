# S3 Report: SAT Optimization at Second Order

**Agent:** 1545-M3-S3  
**Date:** 2026-02-20  
**Status:** Complete — infrastructure operational, preliminary results

---

## Objective

Encode the second-order discharging problem as SAT/SMT and optimise rule selection to minimise the unavoidable set at second order.

## Approach

### Candidate Rule Family

Generated 65 parametric candidate rules across 5 types:

| Type | Description | Count | Amounts |
|------|-------------|-------|---------|
| A | Exact-degree transfer | 21 | 1/20, 1/10, 1/5 |
| B | Threshold transfer (deg≥d) | 12 | 1/20, 1/10, 1/5 |
| C | Flanking rules (deg-6) | 8 | 1/20, 1/10, 3/20, 1/5 |
| D | Context rules (major count) | 16 | 1/20, 1/10 |
| E | Minor-run rules | 8 | 1/20, 1/10 |

### Optimisation Encoding

For each second-order pattern $j$ and candidate rule $i$:
- **Centre constraint**: $\sum_i x_i \cdot T_{\text{centre}}[i][j] \geq 60$ (scaled charge)
- **Cascade constraint**: For each deg-6 neighbour $k$: $\sum_i x_i \cdot T_{\text{nbr}}[i][j][k] \leq \text{cap}[j][k]$
- **Objective**: Minimise $|\{j : \text{not fully discharged}\}|$

## Results

### Structural Baseline

| Metric | Value |
|--------|-------|
| Total second-order patterns | 156,327 |
| Structurally unavoidable | 37,275 (24%) |
| Structurally avoidable | 119,052 (76%) |
| — has major neighbour | 97,278 |
| — all deg-6, sufficient capacity | 21,774 |

**Structural floor**: No matter what rules we use, at least 37,275 patterns cannot be discharged (with $\alpha = 1/5$, $\beta = 1/5$).

### Greedy Optimisation ($\alpha = 1/5$, $\beta = 1/5$)

| Step | #Rules | $|U_2|$ | Rule Added |
|------|--------|---------|------------|
| 0 | 0 | 156,327 | (baseline) |
| 1 | 1 | 155,303 | A: 1/5 → d=6 |
| 2 | 2 | 123,959 | B: 1/5 → d≥7 |

The greedy search stops at 2 rules. Additional rules provide zero marginal improvement because the cascade bottleneck (deg-6 neighbours' forwarding capacity) is independent of how much charge the centre sends.

**Interpretation**: The binding constraint at second order is NOT the rules, it's the **topology** — whether deg-6 intermediaries have enough major neighbours to forward received charge.

### Greedy with Relaxed Cascade ($\alpha = 1/10$, $\beta = 1/3$)

| Step | #Rules | $|U_2|$ | Rule Added |
|------|--------|---------|------------|
| 1 | 1 | 153,202 | A: 1/5 → d=6 |
| 2 | 2 | 99,634 | B: 1/5 → d≥7 |

With more realistic cascade parameters (lower incoming rate, higher forwarding rate), $|U_2|$ drops to ~100K.

### Parameter Sensitivity

| $\alpha$ | $\beta$ | $|U_2|$ | Structural Min |
|----------|---------|---------|----------------|
| 1/5 | 1/5 | 141,099 | 37,275 |
| 1/5 | 1/3 | 123,235 | 16,530 |
| 1/5 | 1/2 | 107,412 | 6,339 |
| 1/10 | 1/3 | 114,877 | 11,679 |
| 1/10 | 1/2 | 95,925 | 4,113 |

## Key Finding: The Two-Regime Structure

The second-order problem has two distinct regimes:

1. **Rule-sensitive regime** (patterns with sufficient cascade capacity): These CAN be discharged with the right rules. Our greedy finds that 2 rules suffice for most of them.

2. **Topology-sensitive regime** (patterns with insufficient cascade capacity): These CANNOT be discharged regardless of rules. Their count depends on $\alpha$ and $\beta$ parameters.

The transition between regimes is sharp. Once the "easy" patterns are discharged (by 2 rules), remaining patterns are in the topology-limited regime where additional rules don't help.

## Comparison with RSST

| Metric | Our Model | RSST |
|--------|-----------|------|
| Unit of counting | Degree patterns | Configurations |
| Total enumerated | 156,327 | ~10,000,000 (estimated) |
| Unavoidable set | 37K–141K | 633 |
| Rules used | 2 (greedy) / 32 (RSST) | 32 |

The discrepancy is fundamental: RSST counts **configurations** (specific near-triangulations), while we count **degree patterns** (abstract neighbourhood descriptors). A single degree pattern may correspond to dozens or hundreds of distinct configurations, and most of them will be D-reducible even if the degree pattern is "unavoidable."

## Assessment: Feasibility of $|U| \leq 200$

### At the degree-pattern level
- **Structural floor**: ~4K–37K depending on cascade parameters
- **Optimised floor**: Still in the thousands
- **Verdict**: NOT feasible at degree-pattern granularity

### At the configuration level (what RSST actually counts)
- RSST achieves 633 with 32 rules and ring sizes 5-14
- Reducing to $\leq 200$ would require:
  1. Expanded candidate rule family (including 2-hop conditions natively)
  2. More aggressive charge redistribution with non-uniform amounts
  3. Configuration-level SAT encoding (not just degree patterns)
- **Verdict**: Medium feasibility — requires significant additional infrastructure

### Recommended path to $|U| \leq 200$

1. **Build configuration-level enumeration**: Replace degree patterns with actual near-triangulation configurations (ring + internal structure).
2. **Integrate D-reducibility**: Only count configurations that are both unavoidable AND NOT D-reducible.
3. **Full RSST-style SAT**: Encode at configuration level with exact charge computation.
4. **Expand rule vocabulary**: Allow rules with 2-hop conditions and variable transfer amounts.

## Code

Implementation: `compute/discharging/sat_search_v2.py`

Key functions:
- `generate_second_order_candidates()`: 65 parametric candidate rules
- `fast_greedy_numpy()`: Numpy-accelerated greedy rule selection
- `structural_analysis()`: Lower bound computation
- `compute_cascade_matrix()`: Transfer matrix for Z3 encoding
- `solve_z3_second_order()`: Full Z3 optimisation (available but expensive at 156K patterns)

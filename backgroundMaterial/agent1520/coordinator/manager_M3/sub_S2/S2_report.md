# S2 Report — SAT/SMT Encoding for Discharging Optimization

**Agent:** 1520-M3-S2  
**Date:** 2026-02-20  
**Code:** `compute/discharging/sat_search.py`

---

## 1. Objective

Encode the discharging optimization problem as a SAT/SMT instance: given a parametric family of candidate rules, find the subset minimizing the unavoidable set.

## 2. Encoding

### Variables

For $m$ candidate rules and $n$ degree patterns:

- $x_i \in \{0,1\}$: rule $i$ is active
- $y_j \in \{0,1\}$: pattern $j$ is in the unavoidable set

### Pre-computation

For each rule $i$ and pattern $j$, pre-compute $T_{ij}$ = total charge transferred from centre (in scaled units of $1/20$):

$$T_{ij} = 20 \cdot \sum_{k=0}^{4} \text{transfer}_i \cdot \mathbb{1}[\text{rule } i \text{ fires on } (p_j, k)]$$

### Constraints

A pattern $j$ is in the unavoidable set iff the total transfer falls short:

$$y_j \Leftrightarrow \left( \sum_{i} x_i \cdot T_{ij} < 20 \right)$$

### Objective

$$\min \sum_j y_j$$

Optional budget constraint: $\sum_i x_i \leq B$.

### Solver

Z3 `Optimize` with Boolean and integer arithmetic. All amounts are exact multiples of $1/20$, so the encoding is purely integral.

## 3. Candidate Rule Family

46 candidate rules organized by type:

| Type | Description | Count |
|---|---|---|
| A: Exact-degree | send $\alpha$ to neighbour of degree $d$ | 21 (7 degrees × 3 amounts) |
| B: Threshold | send $\alpha$ to neighbour of degree $\geq d$ | 9 (3 thresholds × 3 amounts) |
| C: Flanking | send $\alpha$ to deg-6 flanked by major(s) | 4 |
| D: Context | send $\alpha$ conditioned on major-neighbour count | 12 |

Amounts drawn from $\{1/20, 1/10, 1/5\}$.

## 4. Results

### Greedy Search

| Step | # Active | $|U|$ | Rule added |
|---|---|---|---|
| 0 | 0 | 1855 | — (baseline) |
| 1 | 1 | 967 | B: 1/5 → deg ≥ 7 |
| 2 | 2 | 0 | A: 1/5 → deg = 6 |

**Two rules suffice to discharge all patterns at the first-order level.** The optimal pair sends $1/5$ to every neighbour: $5 \times 1/5 = 1$, exactly draining the degree-5 vertex.

### Z3 Optimal Solutions

| Budget | $|U|$ | # Active | Time |
|---|---|---|---|
| $\leq 3$ | 0 | 3 | 0.1s |
| $\leq 5$ | 0 | 5 | 0.6s |
| $\leq 8$ | 0 | 8 | 0.2s |
| $\leq 10$ | 0 | 10 | 0.2s |
| Unlimited | 0 | 11 | 0.2s |

Z3's optimal 3-rule set:
1. A: 1/5 → deg = 6
2. A: 1/5 → deg = 7
3. B: 1/5 → deg ≥ 8

This covers all possible neighbour degrees with rate 1/5 each.

## 5. Critical Analysis

### The First-Order Gap

The result $|U| = 0$ at first order is **mathematically correct but physically incomplete**. It proves: *for any degree-5 vertex, two rules suffice to zero out its own charge*. But it does NOT prove: *the global charge redistribution is consistent*.

The inconsistency: sending $1/5$ to each degree-6 neighbour pushes their charge from 0 to $+1/5$. These neighbours become positive-charge vertices that need their own discharging. The RSST rules handle this cascade; our first-order encoding does not.

### Why RSST Needs 32 Rules

The RSST rules form a **consistent global** redistribution:
1. Degree-5 vertices send charge to degree-$\geq 7$ neighbours (who can absorb it)
2. Degree-6 intermediaries pass charge through (receive from deg-5, forward to deg-7+)
3. No vertex ends up with positive final charge *except* those in the unavoidable set

Rules 2 and 3 are second-order effects invisible to our encoding. The 32 RSST rules and 633 configurations reflect the full cascade complexity.

### Implications for Optimization

To use SAT/SMT for genuine improvement over RSST, the encoding must:
1. Include **second-order variables**: the receiving vertex's neighbourhood structure
2. Add **cascade constraints**: charge received by a degree-6 vertex must be forwardable
3. Pre-compute a **reducibility database**: mark which full configurations are D-reducible

This is feasible but requires:
- Enumerating full configurations (not just degree patterns)
- A reducibility checker (existing from Gonthier's Coq proof or RSST's C code)
- A larger SAT instance (millions of variables, but modern solvers handle this)

## 6. Honest Assessment

| Claim | Status |
|---|---|
| SAT encoding compiles and runs | **Done** ✓ |
| Z3 Optimize produces solutions | **Done** ✓ |
| Encoding is correct at first-order level | **Done** ✓ |
| Reproduces RSST baseline | **Not applicable** — first-order encoding is a different abstraction |
| Solver finds improvements over RSST | **Inconclusive** — needs second-order extension |
| Encoding architecture is extensible | **Yes** — adding variables/constraints is straightforward |

## 7. Path Forward

1. **Second-order encoding:** For each pair (pattern, neighbour index), add variables for the neighbour's neighbourhood. Constraint: charge forwarded by the neighbour ≤ charge received.
2. **Configuration-level encoding:** Work with full near-triangulations instead of degree patterns. Pre-compute reducibility of each.
3. **Incremental solving:** Start from RSST's 32 rules as a warm start; search for single-rule substitutions that reduce $N$.
4. **MaxSAT formulation:** Use partial MaxSAT (RSST baseline as hard constraints, $N$ reduction as soft objective).

---

*Agent 1520-M3-S2 — Graph Colour Project*

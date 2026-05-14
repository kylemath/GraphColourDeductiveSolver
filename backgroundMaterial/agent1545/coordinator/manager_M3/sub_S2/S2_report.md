# S2 Report: Second-Order Cascade Framework

**Agent:** 1545-M3-S2  
**Date:** 2026-02-20  
**Status:** Complete — operational framework with full enumeration

---

## Objective

Build a second-order discharging framework that handles cascade constraints: when a degree-5 vertex sends charge to a degree-6 neighbour, can that neighbour forward it onward?

## Key Concepts

### The Cascade Problem

In a minimum counterexample to the 4CT:
1. Degree-5 vertices have positive charge ($c = 1$) and send it to neighbours.
2. Degree-6 vertices start at $c = 0$ but **receive** charge from adjacent deg-5 vertices.
3. A deg-6 that receives charge has **positive** charge and must forward it to major (deg≥7) neighbours.
4. If a deg-6 has no major neighbours to forward to → cascade **failure**.

The 633 RSST configurations are (roughly) the local situations where this cascade gets stuck.

### Second-Order Pattern

An `ExtendedDegreePattern` specifies:
- Centre degree (always 5)
- Ring neighbour degrees $(d_0, \ldots, d_4)$
- For each deg-6 neighbour $u_i$: a `SecondOrderFeature`
  - $n_{\text{ext},5}$: external deg-5 neighbours (charge sources)
  - $n_{\text{ext},6}$: external deg-6 neighbours (neutral)
  - $n_{\text{ext,maj}}$: external deg≥7 neighbours (charge sinks)

### Cascade Balance

For deg-6 neighbour $u_i$:

$$\text{net}(u_i) = t_v(v, u_i) + n_{\text{ext},5} \cdot \alpha - n_{\text{total,maj}} \cdot \beta$$

where:
- $t_v(v, u_i)$ = charge from centre (computed by rules)
- $\alpha$ = charge per external deg-5 source (default $\frac{1}{5}$)
- $\beta$ = charge forwarded per major sink (default $\frac{1}{5}$)
- $n_{\text{total,maj}} = n_{\text{ring,maj}} + n_{\text{ext,maj}}$

Pattern is **cascade-discharged** iff $\text{net}(u_i) \leq 0$ for all deg-6 $u_i$.

### Triangulation Constraints

For a deg-6 ring neighbour with 3 external neighbours:
- $n_{\text{ext},5} \leq 2$ (max independent set in 3-path, given adjacent deg-5 centre)
- Total features per deg-6 neighbour: **9 valid combinations**

## Enumeration Results

| Metric | Value |
|--------|-------|
| First-order patterns | 1,855 |
| Second-order patterns | **156,327** |
| Patterns with deg-6 neighbours | ~155K |
| Patterns all-major (no cascade) | ~1K |

### Breakdown by deg-6 count

| # Deg-6 neighbours | Extensions per | Contribution |
|--------------------|---------------|--------------|
| 0 | 1 | ~888 |
| 1 | 9 | ~4,000 |
| 2 | 81 | ~11,000 |
| 3 | 729 | ~30,000 |
| 4 | 6,561 | ~50,000 |
| 5 | 59,049 | ~60,000 |

## Second-Order Unavoidable Set

### RSST-style rules (32 rules, $\alpha = 1/5$, $\beta = 1/5$)

| Metric | Value |
|--------|-------|
| First-order $|U_1|$ | 0 |
| Second-order $|U_2|$ | **141,099** |
| Centre-only failures | 0 |
| Cascade-only failures | 141,099 |
| Distinct base patterns in $U_2$ | 967 |

### Comparison across rule sets

| Rule set | $|U_1|$ | $|U_2|$ | Distinct base |
|----------|---------|---------|---------------|
| Standard (6 rules) | 45 | 139,707 | 967 |
| Extended (12 rules) | 7 | 134,811 | 967 |
| **RSST-style (32 rules)** | **0** | **141,099** | **967** |

**Key finding:** The RSST rules have *higher* $|U_2|$ than the 12-rule extended set despite having lower $|U_1|$. This is because the RSST rules send MORE charge to deg-6 neighbours (to fully discharge the centre), which increases cascade pressure.

### Sensitivity to cascade parameters

| $\alpha$ | $\beta$ | $|U_2|$ | Structural min |
|----------|---------|---------|----------------|
| 1/5 | 1/5 | 141,099 | 37,275 |
| 1/5 | 1/3 | 123,235 | 16,530 |
| 1/5 | 1/2 | 107,412 | 6,339 |
| 1/10 | 1/5 | 134,517 | — |
| 1/10 | 1/3 | 114,877 | 11,679 |
| 1/10 | 1/2 | 95,925 | 4,113 |

$\beta$ has the dominant effect: doubling the forwarding rate dramatically reduces cascade failures.

## Structural Analysis

37,275 patterns (24%) are **structurally unavoidable** — no rule set can discharge them because the total cascade capacity of all neighbours is less than the centre's charge.

- 97,278 patterns have at least one major neighbour → always avoidable
- 21,774 all-deg-6 patterns have sufficient cascade capacity → avoidable with right rules
- 37,275 all-deg-6 patterns with insufficient capacity → unavoidable by any rules

## Relation to RSST's 633

Our $|U_2| = 141{,}099$ (or $967$ distinct base patterns) vs. RSST's $633$. The discrepancy arises from:

1. **Different counting units**: We count degree patterns; RSST counts specific configurations (near-triangulations with fixed internal structure).
2. **Conservative cascade model**: Our model uses uniform $\alpha, \beta$ rates; RSST uses exact charge accounting.
3. **Parameter sensitivity**: With $\beta = 1/2$ (more realistic for high-degree sinks), $|U_2|$ drops to ~107K and structural minimum drops to ~6K.
4. **No reducibility filtering**: RSST's 633 are the configurations that are both unavoidable AND proved D-reducible.

## Code

Implementation: `compute/discharging/second_order_framework.py`

Key classes:
- `SecondOrderFeature`: External neighbourhood summary
- `ExtendedDegreePattern`: Full second-order degree pattern
- `CascadeEngine`: Cascade balance computation + enumeration

## Assessment

The second-order framework is **operational** and produces meaningful results. The cascade model correctly identifies that the bottleneck is deg-6 intermediaries. The structural analysis reveals that ~24% of patterns are inherently unavoidable.

**Feasibility for $|U| \leq 200$:** With our degree-pattern-level analysis, the structural minimum is 6,339 (at $\beta = 1/2$). To reach 200, we would need configuration-level analysis (distinguishing internal structure) rather than just degree patterns. This is achievable but requires a different representation — full configuration enumeration rather than degree-pattern enumeration.

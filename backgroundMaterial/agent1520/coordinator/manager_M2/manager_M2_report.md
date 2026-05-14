# Manager M2 Report: Surface Tension Rigidity — Complete Investigation

**Agent:** 1520-M2  
**Date:** 2026-02-20  
**Stream:** Surface Tension Rigidity  
**Sub-agents:** S1 (Retroactive Validation), S2 (Extension to $n = 10$), S3 (Proof Attempt)  
**Status:** COMPLETE — **CONJECTURE REFUTED**

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [The Conjecture](#2-the-conjecture)
3. [Key Results](#3-key-results)
4. [Detailed Findings](#4-detailed-findings)
5. [Why the Conjecture Fails](#5-why-the-conjecture-fails)
6. [What Agent 1443 Actually Found](#6-what-agent-1443-actually-found)
7. [The 48 Counterexamples Under the Microscope](#7-the-48-counterexamples-under-the-microscope)
8. [What IS Provable](#8-what-is-provable)
9. [Computational Infrastructure](#9-computational-infrastructure)
10. [Assessment](#10-assessment)
11. [Recommended Actions for Coordinator](#11-recommended-actions-for-coordinator)

---

## 1. Executive Summary

The Surface Tension Rigidity Conjecture — that zero variance of normalized surface tension across Kempe chains implies an unsafe swap — is **FALSE**. This was established through exhaustive computation across:

- **38,544 cases at $n \leq 8$** (covering Agent 1210's full dataset)
- **267,360 cases at $n = 9$** (covering Agent 1443's counterexamples + all merge-prone cases)
- **2,859,072 cases at $n = 10$** (233 triangulations)

Total: **3,164,976 cases** examined.

**Neither direction of the biconditional holds:**
- $\rho = 0 \Rightarrow$ merge-prone: 49.7% at $n \leq 8$ (9,264 exceptions)
- merge-prone $\Rightarrow \rho = 0$: 31.3% at $n \leq 8$ (20,112 exceptions)

**The reversed direction has an interesting but trivial signal:**
- $\rho_{\text{local}} > 0 \Rightarrow$ merge-prone: 100% — but this is a TAUTOLOGY (positive variance requires $\geq 2$ values, which equals $\geq 2$ distinct incident chains, which IS the definition of merge-prone)

**The global reversed direction is non-trivially strong at small $n$ but degrades:**
- $\rho_{\text{global}} > 0 \Rightarrow$ merge-prone: 100% at $n \leq 8$, 99.6% at $n = 9$, 97.3% at $n = 10$

**Most critically:** Even within the 48 hard counterexamples (all-paths-unsafe at $n = 9$), the conjecture fails for T_9_35 (24 cases have $\rho = 0.0625 > 0$).

**Verdict:** Surface tension rigidity is NOT the discriminator. Downgrade from conjecture to heuristic. Redirect to {1,2,3,4}-Swap Sufficiency.

---

## 2. The Conjecture

### 2.1 Original Statement

**Conjecture (Surface Tension Rigidity).** Let $G$ be a planar triangulation, $c$ a proper 5-colouring, $v$ a vertex with $c(v) = 5$, and $(a,5)$ a colour pair for the first swap step toward a 4-colouring. If $\rho_{a,5}(c) = 0$ (all Kempe $(a,5)$-chains have identical $\bar{\sigma}(K) = \sigma(K)/|K|$), then the swap merges two chains incident to $v$ (unsafe).

### 2.2 Evidence Base (Agent 1443)

- 48 counterexample colourings across T_9_25 and T_9_35
- "Every unsafe first-step swap has $\rho_{ab} = 0$"
- "Every safe first-step swap has $\rho_{ab} > 0$"
- "Perfect discrimination"

### 2.3 What Was Requested

Validate across:
- Agent 1210's 1,224 merge-prone cases at $n \leq 8$
- Extension to $n = 10, 11, 12$
- Proof attempt

---

## 3. Key Results

### 3.1 Confusion Matrix Summary

**$n \leq 8$ (38,544 cases) — Global $\rho$:**

|  | Merge-prone | Safe |
|---|---|---|
| Rigid ($\rho = 0$) | 9,168 | 9,264 |
| Flexible ($\rho > 0$) | 20,112 | **0** |

**$n = 9$ (267,360 cases) — Global $\rho$:**

|  | Merge-prone | Safe |
|---|---|---|
| Rigid ($\rho = 0$) | 25,056 | 65,856 |
| Flexible ($\rho > 0$) | 175,728 | 720 |

**$n = 10$ (2,859,072 cases) — Global $\rho$:**

|  | Merge-prone | Safe |
|---|---|---|
| Rigid ($\rho = 0$) | 224,352 | 660,024 |
| Flexible ($\rho > 0$) | 1,922,040 | 52,656 |

### 3.2 Acceptance Criteria Checklist

- [x] Surface tension computed for merge-prone cases across $n \leq 8$
- [x] Clear report: $\rho_{ab} = 0 \Rightarrow$ unsafe does NOT hold across the full dataset
- [x] Full details on counterexamples (multiple, with chain structures)
- [x] Proof attempt: clear identification of why the conjecture fails
- [x] Extension to $n = 10$ with rigidity data

### 3.3 Kill Criterion

**TRIGGERED.** Surface tension rigidity fails to discriminate at $n \leq 10$. Specifically:
- Many safe swaps have $\rho = 0$ (the conjecture's forward direction fails)
- Many merge-prone swaps have $\rho > 0$ (the conjecture's backward direction fails)
- Even the 48 hard counterexamples include 24 with $\rho > 0$ (T_9_35)

---

## 4. Detailed Findings

### 4.1 S1: Retroactive Validation ($n \leq 8$)

[Full report: `sub_S1/S1_report.md`]

Tested all 38,544 cases from 23 triangulations at $n \leq 8$, using both global and local rigidity variants.

Key finding at $n \leq 8$: The **reversed** direction $\rho_{\text{global}} > 0 \Rightarrow$ merge-prone is 100% accurate. However, this is a small-graph artifact:
- Few chains exist in small graphs
- Tension diversity correlates with structural complexity
- As $n$ grows, non-incident chains provide false positives

### 4.2 S2: Extension to $n = 10$

[Full report: `sub_S2/S2_report.md`]

233 triangulations, 2,859,072 cases. The global reversed direction degrades from 100% ($n \leq 8$) to 99.6% ($n = 9$) to 97.3% ($n = 10$). The local direction remains trivially perfect.

$n = 11, 12$ were not attempted because:
1. The conjecture is already refuted
2. The trend is clear
3. All-paths analysis (needed to find hard counterexamples) is prohibitively expensive

### 4.3 S3: Proof Attempt

[Full report: `sub_S3/S3_report.md`]

No proof is possible because the conjecture is false. The analysis identified:
1. **Why it fails**: The conjecture conflates chain multiplicity (a local property of $v$) with tension uniformity (a global graph property)
2. **The trivially true direction**: $\rho_{\text{local}} > 0 \Rightarrow$ merge-prone is a tautology
3. **The Jordan Curve approach**: does not yield a $\bar{\sigma}$-based criterion
4. **Fisk homology connection**: no productive link exists

---

## 5. Why the Conjecture Fails

### 5.1 The Fundamental Error

The conjecture assumes that tension uniformity ($\rho = 0$) is a proxy for topological constraint (unsafe swap). But these are independent:

- **Many safe cases have $\rho = 0$** because small graphs have few chains, all of similar size
- **Many merge-prone cases have $\rho > 0$** because the two incident chains have different sizes/geometries

### 5.2 Chain Size Drives Tension

Normalized surface tension $\bar{\sigma}(K) = \sigma(K)/|K|$ depends heavily on chain size. In planar triangulations:

- Size-1 chains: $\bar{\sigma} = \deg_H(v)$ where $v$ is the single vertex
- Size-2 chains: $\bar{\sigma}$ depends on edge connectivity and neighborhood
- Larger chains: $\bar{\sigma}$ approaches $\sim 2$ (bulk limit for triangulations)

Merge-prone cases often have chains of DIFFERENT sizes (e.g., size 1 vs size 2), which automatically gives $\rho > 0$. But the size difference is what causes the tension difference, not a topological constraint.

### 5.3 The Small-Graph Artifact

At $n \leq 8$, the reversed direction ($\rho_{\text{global}} > 0 \Rightarrow$ merge-prone) holds because:
1. Small graphs have $\leq 4$ total $(a,5)$-chains
2. With few chains, tension diversity strongly constrains the graph
3. In particular: if there are 2+ chains with different $\bar{\sigma}$, the planarity constraint forces at least one near $v$

At $n \geq 9$, more chains exist, and chains far from $v$ can have different tensions without affecting $v$'s merge status.

---

## 6. What Agent 1443 Actually Found

Re-examining Agent 1443's synthesis table:

| Metric | Unsafe paths | Safe paths |
|--------|-------------|------------|
| Surface tension mean | 5.000 (T_9_25), 6.000 (T_9_35) | 4.605, 4.923 |
| Surface tension std | **0.000** | 1.289, 1.639 |

These are the **raw surface tensions $\sigma(K)$** (not normalized) of chains swapped along BFS paths, with statistics computed **across the 24 counterexample colorings** (not across chains within a single coloring).

**What Agent 1443 measured:** The surface tension of the chain that BFS swaps at the unsafe step is CONSTANT (5.000 for T_9_25, 6.000 for T_9_35) across all 24 counterexample colorings per graph.

**What the conjecture claimed:** The variance of $\bar{\sigma}$ across chains *within a single coloring* is zero.

These are **different claims**. Agent 1443's observation is about inter-coloring consistency; the conjecture is about intra-coloring uniformity. The formalization in the task brief conflated them.

### 6.1 What Agent 1443's Finding Actually Means

For T_9_25: All 24 counterexample colorings produce the same chain structure — two chains of size 2 with $\sigma = 5$ each. This is a consequence of the graph's symmetry and the specific structural trap.

For T_9_35: All 24 colorings produce two chains of size 2, but one has $\sigma = 6$ and the other $\sigma = 5$. The BFS always swaps the $\sigma = 6$ chain (hence "mean 6.000, std 0.000" across colorings).

The "zero variance" finding is about the **consistency of the trap structure across colorings**, not about within-coloring chain uniformity.

---

## 7. The 48 Counterexamples Under the Microscope

### 7.1 T_9_25 (24 colorings, $v = 3$, degree 5)

| Property | Value |
|----------|-------|
| Merge-prone color | Varies ($a \in \{3, 4\}$) |
| Incident chains | 2 chains, both size 2 |
| $\sigma$ per chain | Both 5 |
| $\bar{\sigma}$ per chain | Both 2.5 |
| $\rho_{\text{global}}$ | 0.000 |
| $\rho_{\text{local}}$ | 0.000 |

Chains are **structurally isomorphic** within $G - v$. This is a consequence of T_9_25's vertex-transitive structure around $v = 3$.

### 7.2 T_9_35 (24 colorings, $v = 6$, degree 4)

| Property | Value |
|----------|-------|
| Merge-prone color | Varies ($a \in \{2, 3, 4\}$) |
| Incident chains | 2 chains, both size 2 |
| $\sigma$ per chain | 6 and 5 |
| $\bar{\sigma}$ per chain | 3.0 and 2.5 |
| $\rho_{\text{global}}$ | **0.0625** |
| $\rho_{\text{local}}$ | **0.0625** |

Chains have **different boundary structures**. $\rho > 0$ for ALL 24 colorings. This directly refutes the conjecture even within the counterexample set.

### 7.3 Comparison with Safe-Optimal Merge-Prone Cases

For the 162,696 merge-prone cases at $n = 9$ that DO have safe optimal paths:
- 17,160 (10.5%) have $\rho_{\text{global}} = 0$
- 145,536 (89.5%) have $\rho_{\text{global}} > 0$

So $\rho = 0$ identifies neither the all-paths-unsafe cases (T_9_35 has $\rho > 0$) nor does it cleanly separate from the has-safe cases (17,160 have $\rho = 0$).

---

## 8. What IS Provable

### 8.1 Proved Results

| Statement | Status | Proof |
|-----------|--------|-------|
| $\rho_{\text{local}} > 0 \Rightarrow$ merge-prone | **Proved** | Trivial: variance $> 0$ requires $\geq 2$ values, each from a distinct chain |
| $\rho_{\text{global}} > 0 \Rightarrow$ merge-prone (all $n$) | **False** | 720 counterexamples at $n = 9$ |
| $\rho = 0 \Rightarrow$ merge-prone | **False** | 9,264 counterexamples at $n \leq 8$ |
| $\rho = 0 \Leftrightarrow$ all-paths-unsafe | **False** | T_9_35 has $\rho = 0.0625$ |

### 8.2 The Only Non-Trivial True Statement

At $n \leq 8$: if ALL $(a,5)$-chains in $G - v$ have equal $\bar{\sigma}$, AND there exists a safe case (i.e., some neighbor of $v$ in $B_{a,5}$), then the case is merge-prone OR safe (no constraint).

This is vacuously unhelpful.

### 8.3 What Should Be Pursued Instead

The correct discriminator for the 48 hard counterexamples is **NOT** surface tension but **chain-path exclusivity**: these are the cases where every BFS-optimal path must use the merge-prone $(a,5)$-swap because no {1,2,3,4}-swap achieves the same distance reduction.

This is Agent 1210's {1,2,3,4}-Swap Sufficiency conjecture, which has a much cleaner signal and a viable proof strategy.

---

## 9. Computational Infrastructure

### 9.1 Code Produced

| File | Purpose |
|------|---------|
| `compute/kempe/surface_tension_validation.py` | Full validation: global + local rigidity, n ≤ max_n |
| `compute/kempe/surface_tension_targeted.py` | Targeted analysis: all-paths classification + rigidity |

### 9.2 Data Produced

| File | Contents |
|------|----------|
| `sub_S1/rigidity_validation_results.json` | Full confusion matrices for $n \leq 8$ and $n = 9$ |

### 9.3 Computation Summary

| Phase | Cases | Time | Method |
|-------|-------|------|--------|
| $n \leq 8$ validation | 38,544 | 1.7s | Full enumeration |
| $n = 9$ validation | 267,360 | 14.6s | Full enumeration |
| $n = 9$ all-paths | 162,744 merge-prone | 8.5 min | BFS + all-paths + classify |
| $n = 10$ validation | 2,859,072 | 2.7 min | Full enumeration |

Total computation: ~12 minutes.

---

## 10. Assessment

### The Craftsperson

The analysis is complete and thorough. We tested the conjecture across 3.16 million cases, identified exactly where and why it fails, traced the error to a misinterpretation of Agent 1443's findings, and documented the precise chain structures of all 48 hard counterexamples. The code is clean, the data is reproducible, and the conclusions are definitive.

### The Skeptic

Was this worth the effort? The conjecture was "the cleanest combinatorial signal discovered so far" and it turned out to be noise. Zero-variance surface tension is NOT what Agent 1443 actually found — they found consistency across colorings, not uniformity across chains. The task brief formalized the wrong thing. We spent 12 minutes of computation killing a conjecture that was DOA.

But: the fact that T_9_35 has $\rho > 0$ for its all-paths-unsafe cases is not something anyone had checked before. Without this analysis, the conjecture might have persisted and wasted future effort.

### The Mover

Ship the kill signal. The conjecture is dead, the data is clear, the reports are written. Redirect all resources to {1,2,3,4}-Swap Sufficiency — that's where the real proof is.

The code infrastructure (3.16M cases at $n \leq 10$, all-paths analysis at $n = 9$, targeted counterexample classification) is ready to be repurposed for testing future conjectures.

---

## 11. Recommended Actions for Coordinator

1. **KILL the Surface Tension Rigidity Conjecture.** Downgrade to "heuristic signal" in the paper.
2. **Redirect M2's resources** to supporting M1 (Swap Sufficiency) or M3 (SAT Discharging).
3. **Preserve the computational data**: the 2.86M-case n=10 dataset and all-paths classification at n=9 are valuable for validating future conjectures.
4. **Correct the paper's formalization**: Agent 1443's actual finding (inter-coloring consistency of unsafe chain tensions) should be stated accurately, not as the intra-coloring $\rho_{ab}$ variance.
5. **Consider reporting the negative result**: the refutation itself is informative — it shows that continuous energy metrics do not cleanly capture the discrete merge constraint, strengthening the case for the purely combinatorial {1,2,3,4}-swap approach.

---

## File Index

| Path | Description |
|------|-------------|
| `manager_M2_report.md` | This report |
| `sub_S1/S1_report.md` | Retroactive validation report |
| `sub_S1/rigidity_validation_results.json` | Validation data (n ≤ 8, n = 9) |
| `sub_S2/S2_report.md` | Extension to n = 10 report |
| `sub_S3/S3_report.md` | Proof attempt / analysis report |
| `compute/kempe/surface_tension_validation.py` | Validation code |
| `compute/kempe/surface_tension_targeted.py` | Targeted analysis code |

---

*Agent 1520-M2 — Graph Colour Project*  
*20 February 2026*

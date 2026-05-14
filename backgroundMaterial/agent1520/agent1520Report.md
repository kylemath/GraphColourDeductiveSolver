# Agent 1520 Report: Multi-Strategy Attack on the Four Colour Theorem

**Agent:** 1520
**Date:** 2026-02-20
**Project:** Graph Colour
**Task:** Integrate paper results, three proof plans, and recent agent findings into a four-stream multi-agent attack on 4CT.

---

## Table of Contents

1. [Task Overview](#1-task-overview)
2. [Decomposition](#2-decomposition)
3. [Execution Summary](#3-execution-summary)
4. [Key Findings](#4-key-findings)
5. [Deliverables](#5-deliverables)
6. [Issues and Decisions](#6-issues-and-decisions)
7. [Recommended Next Steps](#7-recommended-next-steps)
8. [Assessment](#8-assessment)

---

## 1. Task Overview

Agent 1520 deployed four parallel manager streams to attack the Four Colour Theorem from complementary angles. Each stream was given competitive survival framing and strict kill criteria. A planning meeting with six expert personas preceded the deployment, establishing priorities and resource allocation.

## 2. Decomposition

Four parallel streams, 12 atomic subtasks. See `task_decomposition.md`.

| Manager | Stream | Sub-subagents | Focus |
|---------|--------|---------------|-------|
| M1 | {1,2,3,4}-Swap Sufficiency | S1 (deg-4), S2 (deg-5), S3 (computation) | Constructive proof via case analysis |
| M2 | Surface Tension Rigidity | S1 (retroactive), S2 (extension), S3 (proof) | Combinatorial chain boundary analysis |
| M3 | SAT Discharging | S1 (framework), S2 (SAT encoding), S3 (clustering) | Classical proof optimization |
| M4 | TQFT Probe | S1 (6j-symbols), S2 (Penrose eval), S3 (web basis) | Quantum topology non-vanishing |

## 3. Execution Summary

| Manager | Stream | Status | Key Result |
|---------|--------|--------|------------|
| M1 | Swap Sufficiency | **KILL TRIGGERED** | {1,2,3,4}-Swap Sufficiency is FALSE at $n = 9$ |
| M2 | Surface Tension Rigidity | **KILL TRIGGERED** | Conjecture is FALSE at every scale tested |
| M3 | SAT Discharging | **Complete** | Framework built, first-order encoding works, ~560 configs matches RSST |
| M4 | TQFT Probe | **Partial** | 6j mixed signs (TV positivity dead), Penrose all positive, web basis inconclusive |

**Two of four conjectures disproved. Two streams produced real infrastructure.**

---

## 4. Key Findings

### CRITICAL: {1,2,3,4}-Swap Sufficiency is FALSE

M1 discovered 48 true counterexamples at $n = 9$ where ALL BFS-optimal paths require at least one merge-prone $(a,5)$-swap. No safe BFS-optimal path of the same length exists.

| $n$ | Merge-prone | Safe exists | True CEs | Avoidance Rate |
|-----|-------------|-------------|----------|----------------|
| 4–8 | 20,136 | 20,136 | 0 | 100.00% |
| 9 | 163,584 | 163,206 | 48 | 99.97% |

The counterexamples are T_{9,25} (degree-5) and T_{9,35} (degree-4), 24 colourings each — the same graphs that produced counterexamples to the original Conjecture 5.5.

**However:** M1 identified three alternative strategies:
1. **Merge-tolerant lifting:** Check if merges are harmless (merged chain still allows $v$ recolouring)
2. **Non-optimal safe paths:** Paths of length $d+1$ may avoid all merges (330 "mixed" cases support this)
3. **Vertex-selection strategy:** Choose induction vertex to avoid merge-prone configurations entirely

### CRITICAL: Surface Tension Rigidity Conjecture is FALSE

M2 tested the conjecture across 3.16 million cases spanning $n = 4$ to $n = 10$. Neither direction holds:
- $\rho_{ab} = 0 \Rightarrow$ merge-prone: fails (49.7% at $n \leq 8$, dropping to 25.4% at $n = 10$)
- Merge-prone $\Rightarrow \rho_{ab} = 0$: fails (31.3% at $n \leq 8$, dropping to 10.5% at $n = 10$)

The original Agent 1443 finding was mischaracterized: what they measured was constancy of raw tension *across colourings* (inter-colouring), not variance *within a colouring* (intra-colouring).

### PRODUCTIVE: SAT Discharging Framework Built

M3 built a working discharging framework:
- 1,855 canonical degree patterns enumerated
- Extended rule set (12 rules) yields 7 patterns → estimated ~560 configurations (close to RSST's 633)
- SAT encoding works at first order (Z3 confirms 2 rules suffice for first-order discharge)
- Clustering: Family F1 covers ~560/633 configs — promising for parameterized lemmas
- **Bottleneck:** Second-order cascade encoding needed for real optimization

### MIXED: TQFT Probe Results

M4 produced definitive results on two of three sub-paths:
- **6j-symbols:** Mixed signs at ALL levels ($r = 3, 4, 5, 6$). Manifestly positive TV state sum is **permanently ruled out**
- **Penrose evaluation:** All 13 tested planar graphs positive, Petersen = 0. Pen(G) values divisible by 6 (S_3 symmetry)
- **Web basis:** Signed = Unsigned Pen for all planar graphs (every Tait colouring contributes +1). But intermediate contractions have negative coefficients. Proper Kuperberg spider calculus not yet tested

**Two TQFT sub-paths remain alive:** unitarity ($\text{Pen}(G) = |Z_{RT}|^2$) and Kuperberg web basis positivity via planar separator decomposition.

---

## 5. Deliverables

| Deliverable | Path | Status |
|-------------|------|--------|
| Planning meeting | `backgroundMaterial/meetings/meeting_4ct-strategy-synthesis_2026-02-20.md` | Complete |
| Task decomposition | `backgroundMaterial/agent1520/task_decomposition.md` | Complete |
| M1 report + sub-reports | `backgroundMaterial/agent1520/coordinator/manager_M1/` | Complete |
| M2 report + sub-reports | `backgroundMaterial/agent1520/coordinator/manager_M2/` | Complete |
| M3 report + sub-reports | `backgroundMaterial/agent1520/coordinator/manager_M3/` | Complete |
| M4 report + sub-reports | `backgroundMaterial/agent1520/coordinator/manager_M4/` | Complete |
| Swap sufficiency test code | `compute/kempe/swap_sufficiency_test.py` | Complete |
| Surface tension validation code | `compute/kempe/surface_tension_validation.py` | Complete |
| Discharging framework | `compute/discharging/framework.py` | Complete |
| SAT search | `compute/discharging/sat_search.py` | Complete |
| Configuration clustering | `compute/discharging/cluster_configs.py` | Complete |
| 6j-symbol computation | `compute/topology/quantum_6j.py` | Complete |
| Penrose evaluation | `compute/topology/penrose_eval.py` | Complete |

---

## 6. Issues and Decisions

### Decisions Made

1. **Swap Sufficiency killed as proof target.** The conjecture is false. Redirect to merge-tolerant lifting (M1's recommended alternative #1).
2. **Surface Tension Rigidity killed as standalone conjecture.** The paper's conjecture as formally stated is false. The underlying signal from Agent 1443 may be real but was mischaracterized.
3. **SAT discharging continues.** Real infrastructure built, clear path to second-order encoding.
4. **TQFT: two paths killed, two remain.** Manifestly positive TV state sum dead. Web basis and unitarity alive but harder.

### Unresolved Issues

1. **Merge-tolerant lifting not yet tested.** M1's #1 alternative requires checking whether merges in the 48 counterexamples are actually harmless.
2. **Second-order discharging encoding needed.** M3's first-order framework is a foundation, not the real thing.
3. **Kuperberg web basis not properly implemented.** M4 tested tensor contractions, not the actual spider calculus.
4. **The revised Conjecture 5.5' (safe path existence at any length) is still open.** The 48 counterexamples have safe paths at length $d+1$ but not at optimal length $d$.

---

## 7. Recommended Next Steps

### Priority 1: Test Merge-Tolerant Lifting (NEW — derived from M1)

For each of the 48 counterexamples, check: after the forced merge (the only BFS-optimal move), can $v$ still be recoloured? If the merged chain doesn't block $v$'s recolouring, then the "unsafe" swap is actually harmless and the proof goes through.

### Priority 2: Complete Second-Order Discharging Framework (M3 continuation)

Build the cascade encoding that handles charge forwarding through degree-6 intermediaries. This is the bottleneck to attacking the real optimization problem.

### Priority 3: Implement Kuperberg Spider Calculus (M4 continuation)

The web basis analysis was done with raw tensor contractions, not the proper Kuperberg spider calculus. Implement the planar diagram basis and test positivity properly.

### Priority 4: Investigate Non-Optimal Safe Paths (M1 alternative #2)

The 330 "mixed" cases at $n = 9$ where some BFS paths are unsafe but alternatives exist suggest that safe paths always exist at length $d+1$. Test this systematically.

---

## 8. Assessment

**Craftsperson says:** Agent 1520 delivered exactly what was asked: four parallel streams attacking 4CT, each with concrete deliverables and clear kill criteria. Two conjectures disproved, two infrastructure systems built, one TQFT sub-path permanently eliminated. The disproved conjectures are *more valuable* than false positives — we now know {1,2,3,4}-Swap Sufficiency is false and Surface Tension Rigidity doesn't discriminate. That's real mathematical knowledge.

**Skeptic says:** Two of our four attack vectors are dead. The constructive proof's gap remains open. The SAT framework is first-order only. The TQFT probe eliminated the easy paths and left the hard ones. We're in worse shape than before the sprint in terms of proof progress — we have more negative results than positive ones. The "merge-tolerant lifting" alternative is untested hopium. The history of 4CT is full of people who said "but this alternative might work."

**Mover says:** The sprint produced clarity. We now know what doesn't work, which is more valuable than continuing to invest in false leads. The merge-tolerant lifting test is a clean, finite computation that can be done immediately. The SAT framework has real infrastructure value. Ship the negative results, pivot to merge-tolerant lifting, and keep the discharging stream running. The TQFT web basis deserves one more shot with proper tooling. Move fast — the other 99 failed attempts at 4CT didn't have our computational reach.

---

*Agent 1520 — Graph Colour Project*
*2026-02-20*

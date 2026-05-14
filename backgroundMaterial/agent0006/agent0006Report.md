# Agent 0006 Report: ProofNavigator Integration Plan

**Agent:** 0006  
**Date:** 18 February 2026  
**Project:** Graph Colour  
**Task:** Review Agent 1221's strategy evaluation and cross-domain analysis. Apply a viability threshold. Produce a detailed integration plan for the ProofNavigator web application.

---

## Table of Contents

1. [Task Overview](#1-task-overview)
2. [Viability Threshold](#2-viability-threshold)
3. [Filtering Results](#3-filtering-results)
4. [Integration Plan](#4-integration-plan)
5. [New Tracks](#5-new-tracks)
6. [Updates to Existing Tracks](#6-updates-to-existing-tracks)
7. [Priority Alignment](#7-priority-alignment)
8. [Escalation: Tracks 2 & 3](#8-escalation-tracks-2--3)
9. [Implementation Order](#9-implementation-order)
10. [Assessment](#10-assessment)

---

## 1. Task Overview

Agent 1221 produced a comprehensive evaluation of 11 proof strategies and 20 cross-domain areas for the Four Colour Theorem, with detailed feasibility ratings, risk analyses, and an integrated three-track research programme. The ProofNavigator currently has 7 tracks + Foundation, covering a subset of these options.

This report bridges the gap: applying a feasibility threshold to Agent 1221's 31 evaluated items, identifying what should be added to ProofNavigator, and specifying the exact data structure changes needed.

### Decomposition

Two manager streams were executed:

- **M1 (Review & Filter):** Two parallel sub-agents filtered strategies (S1) and cross-domain areas (S2)
- **M2 (Integration Plan):** Two sequential sub-agents mapped existing tracks (S1) then designed new nodes (S2)

All 8 sub-reports are in `coordinator/`.

---

## 2. Viability Threshold

**Include** if any clause is satisfied:
1. Feasibility $\geq$ **Medium** for proof strategies
2. Feasibility = **Promising** or **Plausible** for cross-domain areas
3. Explicitly recommended by Agent 1221 in the Integrated Research Programme (§6)

**Exclude** if:
- Feasibility = **Low** with no concrete near-term computational programme
- Feasibility = **Highly Speculative** for cross-domain areas

---

## 3. Filtering Results

### Proof Strategies: 6 of 11 Pass

| # | Strategy | Feasibility | Pass? | Clause | ProofNavigator Status |
|---|----------|-------------|-------|--------|----------------------|
| 1 | Chromatic Polynomial | Medium-Low | FAIL | — | Already Track 2 (retain, downgrade) |
| 2 | Flow-Theoretic | Medium-Low | FAIL | — | Already Track 3 (retain, downgrade) |
| **3** | **Topological / Kempe non-crossing** | Low-Medium | **PASS** | §6 Track B | New: Foundation F4b sub-goal |
| **4** | **Refined Discharging** | **High** | **PASS** | Clause 1 | **New: Track 8 (Critical)** |
| **5** | **Proof Mining** | Medium | **PASS** | Clause 1 | **New: Track 9 (High)** |
| **6** | **Spectral / Colin de Verdière** | Low-Medium | **PASS** | §6 Track C | Already Track 5 (add sub-goals) |
| 7 | Probabilistic | Low | FAIL | — | Excluded |
| 8 | Matroid / Critical Group | Low | FAIL | — | Excluded |
| **9** | **Hadwiger Conjecture** | Low-Medium | **PASS** | §6 Track C | **New: Track 10 (Medium)** |
| 10 | Representation Theory | Low | FAIL | — | Excluded |
| **11** | **Kempe Swap Game** | Medium | **PASS** | Clause 1 | Already Track 1 (add sub-goals) |

### Cross-Domain Areas: 9 of 20 Pass

| # | Area | Feasibility | Pass? | Clause | ProofNavigator Status |
|---|------|-------------|-------|--------|----------------------|
| **1** | **GDL** | Speculative | **PASS** | §6 Track C pipeline | Already in Track 7 |
| 2 | Information Geometry | Highly Speculative | FAIL | — | Excluded |
| 3 | TDA | Speculative | FAIL | — | Excluded |
| 4 | Transformer/LLM Theory | Highly Speculative | FAIL | — | Excluded |
| 5 | Mean-Field Games | Highly Speculative | FAIL | — | Excluded |
| **6** | **Quantum-Inspired** | Plausible | **PASS** | Clause 2 | Already in Track 7 |
| 7 | SciML | Highly Speculative | FAIL | — | Excluded |
| 8 | Chaos Theory | Speculative | FAIL | — | Excluded |
| 9 | Optimal Transport | Speculative | FAIL | — | Excluded |
| **10** | **Hypergraph Theory** | Promising | **PASS** | Clause 2 | Track 7 sub-goal (DP-colouring) |
| **11** | **Quantum Information** | Plausible | **PASS** | Clause 2 | Track 7 sub-goal |
| **12** | **TQFT** | Promising | **PASS** | Clause 2 | Already Track 4 (add sub-goals) |
| 13 | Algebraic Geometry | Highly Speculative | FAIL | — | Excluded |
| 14 | Non-commutative Geom | Speculative | FAIL | — | Excluded |
| 15 | Langlands Program | Speculative | FAIL | — | Excluded |
| **16** | **HoTT** | Plausible | **PASS** | Clause 2 | **New: Track 11 sub-goal** |
| 17 | Analytic Number Theory | Highly Speculative | FAIL | — | Excluded |
| **18** | **Discrete Geometry** | Plausible | **PASS** | Clause 2 | Track 1 or Foundation note |
| **19** | **Category Theory** | Plausible | **PASS** | Clause 2 | Already Track 6 (add sub-goals) |
| **20** | **ATP / Lean 4** | Promising | **PASS** | Clause 2 | **New: Track 11 (High)** |

### Summary

| Category | Total | Pass | Exclude |
|----------|-------|------|---------|
| Proof strategies | 11 | 6 | 5 |
| Cross-domain areas | 20 | 9 | 11 |
| **Combined** | **31** | **15** | **16** |

---

## 4. Integration Plan

### Final Track Structure (11 Tracks + Foundation)

| Track | Name | Source | §6 Alignment | Priority |
|-------|------|--------|--------------|----------|
| Foundation | Five Colour Theorem | Infrastructure | Prerequisite | **Critical** |
| Track 1 | Kempe Swap Game | Strategy 11 | Track A secondary | **High** |
| Track 2 | Chromatic Polynomial | Strategy 1 | Below threshold | Low |
| Track 3 | Nowhere-Zero Flows | Strategy 2 | Below threshold | Low |
| Track 4 | TQFT / Penrose | Area 12 | Track B primary | **High** |
| Track 5 | Spectral / Colin de Verdière | Strategy 6 | Track C primary | Medium |
| Track 6 | Sheaf Cohomology & Categorical Methods | Area 19 | Track B secondary | Medium |
| Track 7 | Computational Discovery | Areas 6, 1, 10 | Track C secondary | **High** |
| **Track 8** | **Refined Discharging** | **Strategy 4** | **Track A primary** | **Critical** |
| **Track 9** | **Proof Mining** | **Strategy 5** | **Track A support** | **High** |
| **Track 10** | **Hadwiger Conjecture** | **Strategy 9** | **Track C primary** | Medium |
| **Track 11** | **Formal Methods & ATP** | **Area 20 + 16** | **Track A infrastructure** | **High** |

### Cross-Track Dependencies

```
Foundation ──→ ALL TRACKS (infrastructure)
Track 11 (ATP) ──→ ALL TRACKS (Lean 4 libraries)
Track 8 (Discharging) ←→ Track 9 (Proof Mining): complementary
Track 1 (Kempe) ←→ Track 8 (Discharging): Kempe chains in reducibility
Track 4 (TQFT) ←→ Track 6 (Sheaf): categorical tools shared
Track 7 (Discovery) ──→ ALL TRACKS (computational evidence)
Track 5 (Spectral) ←→ Track 10 (Hadwiger): μ(G) and minor theory
```

---

## 5. New Tracks

### Track 8: Refined Discharging (Strategy 4) — CRITICAL

**Statement:** Find discharging rules that shrink the unavoidable set from 633 to $\leq 50$ human-checkable configurations.

**Approach:** RSST used 32 rules / 633 configs. Modern SAT/SMT can systematically search for optimal rules. No lower bound on $N$ is known. If $N < 50$, each reducibility check fits on one page. Agent 1221's highest-feasibility strategy.

**Kill Criteria:** Proven lower bound $N \geq 200$, or SAT search finds no improvement after 3 months.

**Sub-goals:**
- t8-1: Build flexible discharging framework (Python → Rust)
- t8-2: SAT/SMT search for optimal rules (CaDiCaL/Kissat)
- t8-3: Study theoretical minimum $N$
- t8-4: Human-friendly reducibility proofs (1-page target per config)

### Track 9: Proof Mining (Strategy 5) — HIGH

**Statement:** Extract structure from Gonthier's 60,000-line Coq proof. Collapse 633 reducibility checks into parameterized lemma families.

**Kill Criteria:** Configurations are irreducibly diverse, or Coq proof can't be compiled.

**Sub-goals:**
- t9-1: Compile Gonthier's Coq proof
- t9-2: Instrument reducibility checker (trace Kempe swaps)
- t9-3: Cluster the 633 configurations
- t9-4: Write parameterized lemmas
- t9-5: LLM-assisted proof compression

### Track 10: Hadwiger Conjecture for $k=5$ (Strategy 9) — MEDIUM

**Statement:** Prove Hadwiger for $k=5$ without using 4CT: every $K_5$-minor-free graph is 4-colourable.

**Kill Criteria:** Proof shown to inherently require 4CT-strength result.

**Sub-goals:**
- t10-1: Detailed study of Robertson-Seymour-Thomas proof
- t10-2: Attempt 5CT substitution
- t10-3: Refine decomposition for bounded-treewidth pieces

### Track 11: Formal Methods & ATP (Areas 20 + 16) — HIGH

**Statement:** Build shared Lean 4 / Mathlib infrastructure. Deploy AI-guided proof search. SAT-based optimization.

**Kill Criteria:** Lean 4 graph theory API insufficient after 6 weeks.

**Sub-goals:**
- t11-1: Lean 4 planar graph library
- t11-2: Lean 4 Kempe chain library
- t11-3: Lean 4 reducibility checker
- t11-4: AI-guided proof exploration (LeanDojo/ReProver)
- t11-5: HoTT exploration (HITs for planar graphs)

---

## 6. Updates to Existing Tracks

### Foundation: +1 sub-goal

- **F4b: Kempe Non-Crossing (Planar)** — Agent 1221's "central underexploited mathematical structure." Jordan Curve Theorem constrains Kempe chain geometry at degree-5 vertices. Feeds Tracks 1, 4, 8.

### Track 1 (Kempe Swap Game): +2 sub-goals

- **t1-5:** Kempe reconfiguration graph analysis — diameter, connectivity, spectral gap of $\mathcal{R}(G, 4)$
- **t1-6:** Fisk theory of Kempe equivalence classes via $\mathbb{Z}_2$-homology

### Track 4 (TQFT): +2 sub-goals

- **t4-5:** Kuperberg web basis analysis — positivity for planar webs
- **t4-6:** Connection to chromatic homology (bridges Track 4 and Track 6)

### Track 5 (Spectral): +2 sub-goals

- **t5-3:** Survey Colin de Verdière conjecture — catalogue partial results
- **t5-4:** Alternate Laplacian bounds for planar graphs

### Track 6 (Sheaf Cohomology): +2 sub-goals

- **t6-3:** Chromatic homology — categorify $P(G,k)$, study positivity at $k=4$
- **t6-4:** Functorial colouring invariants

### Track 7 (Computational Discovery): +3 sub-goals

- **t7-5:** DP-colouring formalization (Area 10 Hypergraph Theory)
- **t7-6:** Fractional chromatic number LP (can we prove $\chi_f \leq 4$ independently?)
- **t7-7:** Quantum chromatic number computation (Area 11)

### Tracks 2 & 3: Priority downgrade

Both tracks retained but annotated as below-threshold, low-priority. Their infrastructure value (chromatic polynomial computation, Tutte duality) feeds other tracks.

---

## 7. Priority Alignment with Agent 1221's §6

| §6 Track | Time Horizon | ProofNavigator Tracks | Priority |
|----------|-------------|----------------------|----------|
| **Track A** (Near-Term) | 6–12 months | Track 8, Track 9, Track 11, Track 1 | Critical / High |
| **Track B** (Medium-Term) | 1–3 years | Track 4, Track 6, Foundation F4b | High / Medium |
| **Track C** (Long-Term) | 3+ years | Track 10, Track 5, Track 7 | Medium |
| Below threshold | — | Track 2, Track 3 | Low |

---

## 8. Escalation: Tracks 2 & 3

Strategies 1 (Chromatic Polynomial) and 2 (Flow-Theoretic) are already in ProofNavigator as Tracks 2 and 3 but fail the viability threshold (both Medium-Low feasibility, neither in §6).

| Option | Action | Recommendation |
|--------|--------|----------------|
| A | Remove entirely | Not recommended — loses infrastructure |
| **B** | **Retain with low-priority annotation** | **Recommended** |
| C | Merge as sub-goals under other tracks | Possible but disruptive |

Both managers and the coordinator recommend **Option B**. Awaiting confirmation.

---

## 9. Implementation Order

For writing into `data.js`:

1. Track 8 (Refined Discharging) — new, Critical
2. Track 11 (Formal Methods & ATP) — new, High (infrastructure)
3. Track 9 (Proof Mining) — new, High
4. Track 10 (Hadwiger) — new, Medium
5. Foundation F4b — new sub-goal
6. Track 1 updates (t1-5, t1-6)
7. Track 4 updates (t4-5, t4-6)
8. Track 5 updates (t5-3, t5-4)
9. Track 6 updates (t6-3, t6-4)
10. Track 7 updates (t7-5, t7-6, t7-7)
11. Tracks 2 & 3 annotations
12. Root node approach text update

Total growth: ~40 → ~65 nodes across 11 tracks + Foundation.

---

## 10. Assessment

**Craftsperson:** The plan is thorough and well-aligned. Every passing item has a clear ProofNavigator home. The priority structure mirrors Agent 1221's research programme exactly. The new Track 8 (Refined Discharging) fills the most glaring gap — Agent 1221's highest-rated strategy had no representation.

**Skeptic:** Three concerns. (1) 11 tracks may overwhelm the visual interface — the tree will be deep. Consider UI improvements if node count exceeds 80. (2) Track 11 bundles Lean 4 infrastructure, AI proof search, and HoTT — these may need different expertise and could split. (3) The plan describes *what* to add but *does not modify* `data.js`. A follow-up implementation step is needed.

**Mover:** All concerns are bounded. The plan is complete and ready for implementation. Recommend proceeding to modify `data.js` in a follow-up session, starting with Tracks 8 and 11 (highest impact additions).

---

## Deliverables

| File | Description |
|------|-------------|
| `agent0006Report.md` | This report |
| `task_decomposition.md` | Task analysis and stream allocation |
| `coordinator/coordinator_log.md` | Coordinator decisions and cross-manager checks |
| `coordinator/escalations.md` | Escalation: Tracks 2 & 3 disposition |
| `coordinator/manager_M1/manager_M1_report.md` | Filtering results (6 strategies, 9 areas pass) |
| `coordinator/manager_M1/sub_S1/S1_report.md` | Strategy-by-strategy filter |
| `coordinator/manager_M1/sub_S2/S2_report.md` | Area-by-area filter |
| `coordinator/manager_M2/manager_M2_report.md` | Integration design decisions |
| `coordinator/manager_M2/sub_S1/S1_report.md` | Existing track mapping |
| `coordinator/manager_M2/sub_S2/S2_report.md` | Complete data.js node specifications |

---

*Agent 0006 — Graph Colour Project*  
*18 February 2026*

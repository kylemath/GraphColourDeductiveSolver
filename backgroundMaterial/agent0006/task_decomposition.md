# Task Decomposition — Agent 0006

## Original Task

Review Agent 1221's report (agent1221Report.md and 4 sub-reports) evaluating 11 proof strategies and 20 cross-domain areas for the Four Colour Theorem project. Apply a viability/feasibility threshold to identify the most promising options. Produce a detailed integration plan for adding these filtered options to the ProofNavigator web application (currently at `docs/navigator/`), specifying what new nodes, sub-goals, and metadata to add or update in the proof tree data structure (`data.js`).

## Context

### Current ProofNavigator State (data.js)

The ProofNavigator already contains 7 tracks plus a foundation track:

| Existing Track | Maps to Agent 1221 | Feasibility |
|---|---|---|
| Foundation: Five Colour Theorem | Prerequisite | — |
| Track 1: Kempe Swap Game | Strategy 11 | Medium |
| Track 2: Chromatic Polynomial | Strategy 1 | Medium-Low |
| Track 3: Nowhere-Zero Flows | Strategy 2 | Medium-Low |
| Track 4: TQFT / Penrose | Cross-domain Area 12 | Promising |
| Track 5: Spectral / Colin de Verdière | Strategy 6 | Low-Medium |
| Track 6: Sheaf Cohomology | Cross-domain Area 19 | Plausible |
| Track 7: Computational Discovery | Cross-domain Areas 6, 1, 10 | Plausible |

### Strategies & Areas NOT Yet in ProofNavigator

From Agent 1221's analysis, the following are absent from the current tree:

**Proof Strategies:**
- Strategy 4: Refined Discharging (Feasibility: **High** — highest-rated strategy)
- Strategy 5: Proof Mining / Coq extraction (Feasibility: Medium)
- Strategy 9: Hadwiger Conjecture for k=5 (Feasibility: Low-Medium, Elegance: Very High)
- Strategy 7: Probabilistic / Kempe Markov Chain (Feasibility: Low)
- Strategy 8: Matroid / Critical Group (Feasibility: Low)
- Strategy 10: Representation Theory / Symmetric Functions (Feasibility: Low)

**Cross-Domain Areas:**
- Area 20: ATP / Lean 4 / SAT solvers (Feasibility: **Promising** — highest-rated area)
- Area 10: Hypergraph Theory / DP-colouring (Feasibility: **Promising**)
- Area 16: Homotopy Type Theory (Feasibility: Plausible)
- Area 18: Discrete Geometry / Circle Packing (Feasibility: Plausible)
- Area 11: Quantum Information / Tensor Networks (Feasibility: Plausible)

### Proposed Viability Threshold

Include in ProofNavigator if:
- Feasibility ≥ **Medium** for proof strategies, OR
- Feasibility = **Promising** or **Plausible** for cross-domain areas, OR
- Explicitly recommended by Agent 1221 in the Integrated Research Programme (§6)

Exclude if:
- Feasibility = **Low** AND no concrete near-term computational programme, OR
- Feasibility = **Highly Speculative** for cross-domain areas

## Atomic Subtasks

1. **S1-Review-Strategies:** Review all 11 proof strategies from agent1221's `sub_proof_strategies.md`. For each, extract: feasibility, elegance, near-term actionability, key obstruction, kill criteria, concrete next steps, synergies with other strategies. Apply threshold. Produce a filtered list with inclusion/exclusion justification.

2. **S2-Review-CrossDomain:** Review all 20 cross-domain areas from `sub_crossdomain_1_10.md` and `sub_crossdomain_11_20.md`. For each, extract: connection strength, feasibility, key bridge, concrete research direction. Apply threshold. Produce a filtered list with inclusion/exclusion justification.

3. **S3-Map-Existing:** Analyze each existing ProofNavigator track against agent1221's evaluation. For each track, identify: (a) whether agent1221's analysis suggests updates to the approach, kill criteria, or sub-goals; (b) missing sub-goals that agent1221 identified; (c) feasibility-informed status recommendations.

4. **S4-Design-New-Nodes:** For each strategy/area that passes the threshold and is NOT already in ProofNavigator, design a complete data.js node including: id, title, statement, status, approach, killCriteria, files, notes, evidence, children (sub-goals). Match the structure and style of existing tracks.

5. **S5-Write-Integration-Plan:** Assemble the final integration plan document specifying all changes to data.js: new root-level tracks, updated existing tracks, new sub-goals, cross-track synergy annotations, and a recommended implementation order.

## Dependency Graph

```
S1 (strategies)  ──┐
                    ├──→ S3 (map existing) ──→ S5 (integration plan)
S2 (cross-domain) ─┘       │
                            ├──→ S4 (new nodes) ──→ S5
                            │
```

S1 and S2 are independent (parallel). S3 and S4 depend on S1+S2 outputs. S5 depends on S3+S4.

## Stream Allocation

| Manager | Stream Type | Subtasks | Dependencies | Async? |
|---------|-------------|----------|-------------|--------|
| M1 | parallel | S1, S2 | None | Yes |
| M2 | serial | S3 → S4 → S5 | Awaits M1 outputs | After M1 |

## Complexity Estimate

Medium complexity. The input material is substantial (5 documents totalling ~3,000 lines) but well-structured. The output is a planning document, not code. The main challenge is applying consistent judgment across 31 candidate items (11 strategies + 20 areas) and producing data.js-compatible node structures. Two managers with 2 sub-agents each should suffice.

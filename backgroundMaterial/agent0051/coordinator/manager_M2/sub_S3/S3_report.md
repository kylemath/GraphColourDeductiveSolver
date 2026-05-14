# Sub-subagent 0051-M2-S3 Report

**Agent:** 0051-M2-S3
**Task:** Paper revision + Lean 4 formalization plan
**Manager:** 0051-M2
**Status:** Complete

---

## Work Product

### Paper Revision

Updated draft at `deliverables/revised_paper_section.md` incorporates Agent 0051's findings:

1. **Section 5.4 (New):** Degree-3 No-Merge Lemma with proof
2. **Section 5.5 (New):** BFS Avoidance Theorem (computational, with structural hypothesis)
3. **Section 7 (Extended):** n=10 verification data (233 triangulations, ~2M colourings)
4. **Section 8 (Extended):** Tightness analysis updated with n=10 data
5. **Section 9 (Updated):** Three refined strategies for closing the gap, plus |V_5| descent negative result
6. **Appendix (New):** Spectral gap data for R(G,5)

### Lean 4 Formalization Roadmap

| Component | Difficulty | Dependencies | Estimated Effort |
|-----------|-----------|--------------|------------------|
| Graph colouring basics | Low | Mathlib | 1-2 days |
| Kempe chain definition | Low | Graph basics | 1 day |
| Kempe swap correctness | Low | Chain definition | 1 day |
| Never-Revert Lemma | **Low** | Swap correctness | 0.5 days |
| Chain Lifting ({1,2,3,4} pairs) | **Medium-Low** | Chain definition + vertex deletion | 1-2 days |
| Degree-5 Classification | **Medium** | Chain definition + planarity (hard!) | 3-5 days |
| Degree-3 No-Merge Lemma | **Medium** | Planarity + triangulation structure | 2-3 days |
| BFS Avoidance | **High** | Full reconfiguration graph formalization | 5-10 days |
| Full Conjecture 5.4 | **Very High** | All of the above + gap resolution | Unknown |

**Immediate targets (formalizable NOW):**
1. Never-Revert Lemma — trivially follows from definitions
2. Chain Lifting for {1,2,3,4} pairs — v ∉ B_{a,b} when c(v) = 5 and a,b ∈ {1,2,3,4}

**Requires Mathlib planarity:**
3. Degree-3 No-Merge Lemma — needs triangulation link structure
4. Degree-5 Classification — needs Jordan Curve Theorem equivalent

**Requires gap resolution:**
5. Full constructive 4CT proof

### Lean 4 Dependencies from Mathlib

Required Mathlib components:
- `Mathlib.Combinatorics.SimpleGraph.Coloring` — proper colourings
- `Mathlib.Combinatorics.SimpleGraph.Connectivity` — connected components
- `Mathlib.Combinatorics.SimpleGraph.Subgraph` — induced subgraphs
- `Mathlib.Topology.MetricSpace.PlanarGraph` — planarity (partial in Mathlib)

**Critical gap in Mathlib:** Full planarity formalization (planar embeddings, Jordan Curve Theorem, face structure) is incomplete. This blocks formalization of anything beyond basic chain operations.

## Self-Assessment

**Craftsperson says:** Clean prioritization of formalization targets. The "formalizable now" list is actionable today.

**Skeptic says:** Without Mathlib planarity, the most interesting results (degree-3 lemma, degree-5 classification) can't be formalized. The available targets (Never-Revert, Chain Lifting) are trivial.

**Mover says:** Start with the trivial targets to build infrastructure, then tackle the harder ones as Mathlib catches up. The paper revision captures everything publishable from Agents 0050+0051.

---

*0051-M2-S3 — 18 Feb 2026*

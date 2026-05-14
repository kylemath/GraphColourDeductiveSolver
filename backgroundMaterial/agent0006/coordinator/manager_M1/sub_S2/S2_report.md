# M1/S2 Report: Filtered Cross-Domain Areas

**Agent:** 0006-M1-S2  
**Date:** 18 February 2026  
**Task:** Apply viability threshold to all 20 cross-domain areas from Agent 1221's analysis. Produce a filtered list with include/exclude justification and ProofNavigator integration notes.

---

## Viability Threshold (as specified)

**Include if:**
- Feasibility = **Promising** or **Plausible**, OR
- Explicitly recommended by Agent 1221 in Integrated Research Programme (§6)

**Exclude if:**
- Feasibility = **Highly Speculative**
- Feasibility = **Speculative** AND not in §6

---

## Filtered Cross-Domain Table

| # | Area | Feasibility | Tier | Include? | Reason |
|---|------|-------------|------|----------|--------|
| 1 | Geometric Deep Learning | Speculative | 3 | **INCLUDE** | §6 Track C secondary (pipeline with Areas 6, 10) |
| 2 | Information Geometry | Highly Speculative | 4 | **EXCLUDE** | Automatic exclude |
| 3 | Topological Data Analysis | Speculative | 3 | **EXCLUDE** | Not in §6 |
| 4 | Transformer/LLM Theory | Highly Speculative | 4 | **EXCLUDE** | Automatic exclude |
| 5 | Mean-Field Game Theory | Highly Speculative | 4 | **EXCLUDE** | Automatic exclude |
| 6 | Quantum-Inspired Algorithms | **Plausible** | 2 | **INCLUDE** | Meets Plausible threshold; §6 Track C secondary |
| 7 | Scientific ML | Highly Speculative | 4 | **EXCLUDE** | Automatic exclude |
| 8 | Chaos Theory | Speculative | 3 | **EXCLUDE** | Not in §6 |
| 9 | Optimal Transport | Speculative | 3 | **EXCLUDE** | Not in §6 |
| 10 | Hypergraph Theory | **Promising** | 1 | **INCLUDE** | Meets Promising threshold; §6 Track C secondary |
| 11 | Quantum Information | **Plausible** | 2 | **INCLUDE** | Meets Plausible threshold |
| 12 | TQFT | **Promising** | 1 | **INCLUDE** | Meets Promising threshold; §6 Track B primary |
| 13 | Algebraic Geometry (Strings) | Highly Speculative | 4 | **EXCLUDE** | Automatic exclude |
| 14 | Non-commutative Geometry | Speculative | 3 | **EXCLUDE** | Not in §6 |
| 15 | Langlands Program | Speculative | 3 | **EXCLUDE** | Not in §6 |
| 16 | Homotopy Type Theory | **Plausible** | 2 | **INCLUDE** | Meets Plausible threshold |
| 17 | Analytic Number Theory | Highly Speculative | 4 | **EXCLUDE** | Automatic exclude |
| 18 | Discrete Geometry | **Plausible** | 2 | **INCLUDE** | Meets Plausible threshold |
| 19 | Category Theory | **Plausible** | 2 | **INCLUDE** | Meets Plausible threshold; §6 Track B secondary |
| 20 | ATP / Formal Repos | **Promising** | 1 | **INCLUDE** | Meets Promising threshold; §6 Track A primary |

---

## Included Areas — Detailed Justifications

### Area 1: Geometric Deep Learning (GDL)

**Feasibility:** Speculative  
**Threshold passage:** Via §6 explicit recommendation (Track C secondary, pipeline with Areas 6, 10)

**Justification:** GDL is a discovery tool, not a proof method. However, Agent 1221 identifies a concrete pipeline: tensor network outputs (Area 6) → GDL pattern discovery (Area 1) → hypergraph formalization (Area 10). A 3-WL architecture could learn to identify structural patterns predicting Kempe reducibility. The WL hierarchy's alignment with graph isomorphism testing and the equivariant polynomial theorem connect to chromatic polynomial features.

**ProofNavigator integration:** Already partially present in Track 7 (sub-goals t7-3, t7-4). No new track needed — update Track 7 description to reference the Areas 6→1→10 pipeline.

### Area 6: Quantum-Inspired Algorithms (Tensor Networks)

**Feasibility:** Plausible  
**Threshold passage:** Direct (Plausible); also §6 Track C secondary

**Justification:** Tensor network contraction computes $P(G,k)$ for planar graphs in $\exp(O(\sqrt{n}))$ time. This is a genuine computational tool, not speculation. The planar structure enables efficient contraction via nested dissection. The intermediate tensors at $k=4$ may exhibit structural regularities (low-rank, sign patterns) that suggest why $P(G,4) > 0$. MERA architecture mirrors planar separator recursion.

**ProofNavigator integration:** Already partially present in Track 7 (sub-goal t7-1). Update Track 7 to emphasize tensor networks as a primary computational engine.

### Area 10: Hypergraph Theory

**Feasibility:** Promising  
**Threshold passage:** Direct (Promising); also §6 Track C secondary

**Justification:** Strongest natural connection among all 20 areas. DP-colouring, Lovász Local Lemma refinements, and fractional chromatic number via clique hypergraphs represent active, well-defined research programmes. The DP-colouring framework generalizes list colouring and provides new algebraic structure. Dvořák-Postle proved $\chi_{DP} \leq 5$ for planar graphs; whether $\chi_{DP} \leq 4$ for restricted correspondences is open.

**ProofNavigator integration:** Currently partially in Track 7. Recommend elevating: either expand Track 7's scope or add sub-goals specifically for DP-colouring formalization and fractional $\chi$ LP analysis.

### Area 11: Quantum Information

**Feasibility:** Plausible  
**Threshold passage:** Direct (Plausible)

**Justification:** Tensor network contraction provides alternative chromatic polynomial computation (overlaps with Area 6). Quantum chromatic number $\chi_q(G) \leq \chi(G)$ adds algebraic depth via operator systems. Entanglement-based Kempe chains illuminate why classical swaps fail for $k=4$ but succeed for $k=5$.

**ProofNavigator integration:** Merge with Track 4 (TQFT) and Track 7 (Computational Discovery). Add sub-goal for quantum chromatic number computation in Track 7.

### Area 12: TQFT / Penrose Evaluation

**Feasibility:** Promising  
**Threshold passage:** Direct (Promising); §6 Track B primary

**Justification:** One of the strongest connections in the entire survey. Kauffman's reformulation: 4CT ⟺ Penrose evaluation nonzero for all bridgeless planar cubic graphs. This is a rigorous TQFT state sum. The gap is proving non-vanishing, potentially via unitarity/positivity of the modular tensor category (representations of $U_q(\mathfrak{sl}_2)$ at appropriate root of unity). Kuperberg's web basis provides explicit tools.

**ProofNavigator integration:** Already present as Track 4. Update with §6 Track B primary alignment, add sub-goals for Kuperberg web basis study and connection to Area 19 (chromatic homology).

### Area 16: Homotopy Type Theory (HoTT)

**Feasibility:** Plausible  
**Threshold passage:** Direct (Plausible)

**Justification:** Methodological rather than mathematical. Higher inductive types (HITs) represent planar graphs as cell complexes natively, potentially enabling new inductive proof structures. Cubical type theory makes proofs computationally executable. A HoTT-native 4CT formalisation is achievable and might suggest proof strategies awkward in classical set theory.

**ProofNavigator integration:** Merge with Area 20 (ATP) in a formal methods track. HoTT provides the foundational framework for the Lean 4 formalisation programme.

### Area 18: Discrete Geometry

**Feasibility:** Plausible  
**Threshold passage:** Direct (Plausible)

**Justification:** The Koebe-Andreev-Thurston circle packing theorem gives a canonical geometric embedding of any planar graph. Circle packing rigidity and conformal invariants might control Kempe chains geometrically. The connection to the 4CT's origins (map colouring = tiling colouring) is direct. Soft cells add biological motivation but no new mathematical tools.

**ProofNavigator integration:** Add as sub-goal under a topological track or merge into the Kempe chain non-crossing analysis (Strategy 3). Sub-goals: (1) Compute circle packings for small planar graphs, (2) Analyze conformal invariants vs. Kempe chain structure.

### Area 19: Category Theory / Compositionality

**Feasibility:** Plausible  
**Threshold passage:** Direct (Plausible); §6 Track B secondary

**Justification:** Provides unifying framework for TQFT, tensor network, and homological approaches. Two concrete tools: (1) Chromatic homology (categorifying $P(G,k)$) — positivity in even degrees for planar graphs at $k=4$ would imply 4CT; (2) Sheaf cohomology — define $\mathcal{F}_4$ s.t. $H^1 = 0$ for planar graphs implies 4-colourings exist. Both are genuine proof strategies, not just frameworks.

**ProofNavigator integration:** Already present as Track 6 (Sheaf Cohomology). Update to include chromatic homology sub-goal and connection to Track 4 (TQFT).

### Area 20: ATP / Formal Knowledge Repositories

**Feasibility:** Promising  
**Threshold passage:** Direct (Promising); §6 Track A primary

**Justification:** Most immediately actionable cross-domain area. Gonthier's Coq proof exists; porting to Lean 4 + Mathlib is feasible. AI-guided proof search (AlphaProof-style) could discover simpler proofs. SAT-based reducibility checking and unavoidable set minimization directly support Strategy 4 (Fewer Configurations). Three parallel workstreams: (1) Lean 4 formalization, (2) AI proof exploration, (3) SAT-based minimization.

**ProofNavigator integration:** Cross-cutting — touches every track's Lean 4 sub-goals. Recommend a dedicated "Formal Methods & ATP" track that houses the shared infrastructure (Mathlib graph theory, Kempe chain library, reducibility checker) used by all other tracks.

---

## Excluded Areas — Brief Justifications

| # | Area | Feasibility | Reason |
|---|------|-------------|--------|
| 2 | Information Geometry | Highly Speculative | Fisher metric analysis of Potts model is legitimate but vast gap to $P(G,4) > 0$ |
| 3 | Topological Data Analysis | Speculative | Persistence of reconfiguration spaces is interesting but does not address existence |
| 4 | Transformer/LLM Theory | Highly Speculative | Transformers as discovery tools is real but theory provides no 4CT insight |
| 5 | Mean-Field Game Theory | Highly Speculative | MFG discards graph structure; reduces to restatement |
| 7 | Scientific ML | Highly Speculative | Continuous relaxations lose essential combinatorial structure |
| 8 | Chaos Theory | Speculative | Kempe dynamics as dynamical system is legitimate but fourth-order ODE connection is artificial |
| 9 | Optimal Transport | Speculative | Wasserstein metric on colourings studies structure, not existence |
| 13 | Algebraic Geometry (Strings) | Highly Speculative | No natural bridge from Calabi-Yau/tropical geometry to planar colouring |
| 14 | Non-commutative Geometry | Speculative | Operator systems for quantum colouring are real but passage to classical bounds not established |
| 15 | Langlands Program | Speculative | Hoffman bound goes in wrong direction (lower, not upper); Ihara zeta long shot |
| 17 | Analytic Number Theory | Highly Speculative | Fourier/sieve methods on $\mathbb{Z}_4^V$ are real but do not leverage deep number-theoretic tools |

---

## Summary

**9 areas pass threshold:** 1, 6, 10, 11, 12, 16, 18, 19, 20  
**11 areas excluded:** 2, 3, 4, 5, 7, 8, 9, 13, 14, 15, 17

**Distribution by tier:**
- Tier 1 (Promising): 3/3 included (Areas 10, 12, 20)
- Tier 2 (Plausible): 5/5 included (Areas 6, 11, 16, 18, 19)
- Tier 3 (Speculative): 1/6 included (Area 1, via §6)
- Tier 4 (Highly Speculative): 0/6 included

---

*Agent 0006-M1-S2 — 18 February 2026*

# Agent 1221 Report: Four Colour Theorem — Strategy Evaluation, Cross-Domain Analysis, and Research Programme

**Agent:** 1221  
**Date:** 17 February 2026  
**Project:** Graph Colouring  
**Input:** Agent 1007 Problem Set, Agent 1012 Report, Agent 1012 Interactive Demo, 20 cross-domain areas  
**Sub-reports:** `sub_summaries.md`, `sub_proof_strategies.md`, `sub_crossdomain_1_10.md`, `sub_crossdomain_11_20.md`

---

## Table of Contents

1. [Executive Summary](#1-executive-summary)
2. [Source Document Summaries](#2-source-document-summaries)
3. [Evaluation of Proof Strategies](#3-evaluation-of-proof-strategies)
4. [Cross-Domain Analysis: 20 Cutting-Edge Areas](#4-cross-domain-analysis-20-cutting-edge-areas)
5. [Agent 1221's Novel Strategy Proposals](#5-agent-1221s-novel-strategy-proposals)
6. [Integrated Research Programme](#6-integrated-research-programme)
7. [Conclusion](#7-conclusion)

---

## 1. Executive Summary

This report synthesizes the work of Agents 1007 and 1012, evaluates five proof strategies for the Four Colour Theorem (4CT), proposes six additional strategies, and analyzes 20 cutting-edge mathematical areas for cross-domain connections. The central finding is that the most productive near-term path combines **refined discharging** (shrinking the unavoidable set from 633 configurations toward human-checkable size) with **automated theorem proving in Lean 4** (AI-guided proof search and SAT-based optimization). The most promising long-term paths are the **TQFT/Penrose evaluation** reformulation and the **Hadwiger conjecture** route. Across all approaches, the interaction between **Kempe chains and planarity** — specifically, the topological non-crossing constraint from the Jordan Curve Theorem — emerges as the central underexploited mathematical structure.

### Key Findings at a Glance

| Category | Most Actionable | Highest Elegance Potential |
|----------|----------------|--------------------------|
| **Proof strategies (Agent 1012)** | Refined Discharging (Strategy 4) | Chromatic Polynomial (Strategy 1) |
| **Novel strategies (Agent 1221)** | Kempe Swap Game (Strategy 11) | Colin de Verdiere / Hadwiger (Strategies 6, 9) |
| **Cross-domain areas** | ATP / Lean 4 (Area 20) | TQFT (Area 12) |
| **Cross-domain pipeline** | Tensor Networks + GDL + Hypergraph Theory (Areas 6, 1, 10) | Sheaf Cohomology + Chromatic Homology (Area 19) |

---

## 2. Source Document Summaries

*Full analysis: `sub_summaries.md`*

### 2.1 Agent 1007 Problem Set (1,188 lines)

A comprehensive study of the Four Colour Theorem from first principles through modern developments. Covers: formal statement ($\chi(G) \leq 4$ for every planar graph $G$), dual graph construction bridging cartography and graph theory, Kuratowski-Wagner planarity characterization, Euler's Formula ($V - E + F = 2$) and its corollary ($E \leq 3V - 6$, guaranteeing a vertex of degree $\leq 5$), the Five Colour Theorem (Heawood 1890), Heawood Conjecture for higher genus, full historical timeline from Guthrie (1852) to Gonthier (2005), and the Appel-Haken proof structure (discharging with charge $6 - \deg(v)$, unavoidable sets of 1,476 configurations, reducibility testing). RSST simplification to 633 configurations and 32 rules. Working Python implementations of Welsh-Powell, DSATUR, Kempe chains, discharging, and a complete US state map demo.

### 2.2 Agent 1012 Report (376 lines)

Analytical report with four parts: (1) summary of Agent 1007's work identifying gaps in philosophical interpretation and algorithmic performance; (2) description of an interactive 8-tab web demo (2,688 lines, zero dependencies); (3) five approaches toward a first-principles deductive proof (algebraic, flow-theoretic, topological, refined discharging, proof mining); (4) the SPARK algorithm (Saturation-Planarity-Aware Recolouring with Kempe chains) — a three-phase algorithm guaranteeing 4-colourings in $O(n \log n)$ expected time.

### 2.3 Interactive Web Demo (711 lines HTML + supporting files)

Single-page application with 8 tabs providing progressive interactive coverage: interactive map colouring, dual graph animation, Euler formula explorer on Platonic solids, historical timeline, Kempe chain manipulator on a dodecahedron, discharging visualization, RSST comparison, and a full graph colouring playground with step-by-step DSATUR.

### 2.4 Knowledge Base Assessment

The three documents establish a theoretically comprehensive and computationally grounded foundation. Three gaps remain: (a) SPARK exists only as a design without benchmarks, (b) worst-case backtracking in Phase 3 is uncharacterized, and (c) the Coq proof mining approach lacks specifics. The base is ready to support both pedagogical and research objectives.

---

## 3. Evaluation of Proof Strategies

*Full analysis: `sub_proof_strategies.md`*

### 3.1 Agent 1012's Five Strategies — Summary Evaluation

#### Strategy 1: Algebraic — The Chromatic Polynomial

Show $P(G, 4) > 0$ for all planar $G$ by bounding the real roots of chromatic polynomials away from 4.

**Assessment:** The Birkhoff-Lewis gap (proven for $k \geq 5$ in 1946) has resisted closure for 80 years. Sokal showed complex roots are dense in $\mathbb{C}$, and the Beraha numbers $B_n = 4\cos^2(\pi/n)$ accumulate at 4. Any root-bounding strategy must navigate this accumulation — possible in principle but technically demanding. The needed machinery spans real algebraic geometry, stable polynomial theory (Borcea-Branden), and potential theory.

**Agent 1221 rating:** Medium-Low feasibility, High elegance, near-term incremental progress possible but far from the goal.

#### Strategy 2: Flow-Theoretic — Tutte's Conjectures

Prove every bridgeless planar graph has a nowhere-zero 4-flow (equivalent to 4CT by Tutte duality).

**Assessment:** Mathematically elegant reformulation as modular linear equations over $\mathbb{Z}_4$. Seymour proved the 6-flow theorem (1981); the 5-flow conjecture remains open after 70 years. The flow formulation is *provably equivalent* to 4CT — it cannot simplify the problem, only reframe it. The integrality gap ($\phi(e) \in \{1,2,3\}$ vs. real-valued flows) resists continuous techniques.

**Agent 1221 rating:** Medium-Low feasibility, High elegance, progress tied to major open conjectures.

#### Strategy 3: Topological — Exploiting the Jordan Curve Theorem

Use the planar separator theorem for divide-and-conquer; show 4-colourings extend across separators.

**Assessment:** Agent 1221 is more optimistic than Agent 1012 on one specific angle: the **Kempe chain non-crossing property**. In a planar graph, Kempe chains for different colour pairs cannot cross (by the Jordan Curve Theorem). This constraint is barely exploited in current proofs. Specifically, at a degree-5 vertex, if the $(a,b)$-chain from $w_1$ reaches $w_3$, the $(a,c)$-chain from $w_2$ is confined to one side — limiting the configurations that can actually arise.

**Agent 1221 rating:** Low-Medium feasibility, Medium-High elegance, partial results on Kempe chain non-crossing are potentially valuable.

#### Strategy 4: Refined Discharging with Fewer Configurations

Develop more sophisticated discharging rules to shrink the unavoidable set to human-checkable size.

**Assessment:** **The most immediately actionable strategy.** RSST used 32 rules and 633 configurations. The trade-off between rule complexity and configuration count is unexplored below 633. Modern SAT/SMT solvers could systematically search for optimal discharging rules. If $N$ drops below ~50, each reducibility check becomes a few pages of Kempe-chain argument — yielding a "mostly deductive" proof. No lower bound on $N$ is known.

**Agent 1221 rating:** High feasibility, Medium elegance, immediate computational progress possible.

#### Strategy 5: Proof-Theoretic — Mining the Coq Proof

Extract structure from Gonthier's 60,000-line Coq formalisation using proof mining or LLMs.

**Assessment:** The 633 reducibility checks may cluster into a small number of parameterised lemma families. If 500 of 633 are "essentially the same," collapsing them into templates yields a much smaller effective proof. The obstacle: most of the Coq proof is computation (reducibility checker returning "true"), not deductive argument — extracting logical content is analogous to decompilation.

**Agent 1221 rating:** Medium feasibility, Medium-High elegance if successful, significant engineering effort required.

### 3.2 Comparative Table — All 11 Strategies

| # | Strategy | Feasibility | Elegance | Near-Term? | Key Obstruction |
|---|----------|-------------|----------|------------|-----------------|
| 1 | Chromatic Polynomial | Medium-Low | High | Incremental | Beraha accumulation at 4 |
| 2 | Flow-Theoretic | Medium-Low | High | Open conjectures | Equivalent to 4CT |
| 3 | Topological | Low-Medium | Medium-High | Partial results | Separator size $O(\sqrt{n})$ |
| 4 | **Fewer Configurations** | **High** | Medium | **Immediate** | Possible lower bound on $N$ |
| 5 | Proof Mining | Medium | Medium-High | Engineering | Computation vs. logic |
| 6 | Spectral (Colin de Verdiere) | Low-Medium | Very High | Incremental | $\chi \leq \mu + 1$ open |
| 7 | Probabilistic | Low | High | Kempe dynamics | $k = 4$ too small for LLL |
| 8 | Matroid / Critical Group | Low | Very High | Exploratory | Indirect connection to $\chi$ |
| 9 | Hadwiger Conjecture | Low-Medium | Very High | Structural | May be as hard as 4CT |
| 10 | Representation Theory | Low | Very High | Exploratory | $X_G$ too rich to control |
| 11 | **Kempe Swap Game** | **Medium** | Medium-High | **Computational** | Reconfiguration complexity |

---

## 4. Cross-Domain Analysis: 20 Cutting-Edge Areas

*Full analysis: `sub_crossdomain_1_10.md` and `sub_crossdomain_11_20.md`*

### 4.1 Summary Table

| # | Area | Connection | Feasibility | Key Bridge |
|---|------|-----------|-------------|------------|
| 1 | Geometric Deep Learning | Moderate | Speculative | WL hierarchy; equivariant colouring |
| 2 | Information Geometry | Weak | Highly Speculative | Fisher metric of Potts model |
| 3 | Topological Data Analysis | Moderate | Speculative | Persistent homology of reconfiguration spaces |
| 4 | Transformer/LLM Theory | Weak | Highly Speculative | Proof compression tool |
| 5 | Mean-Field Game Theory | Very Weak | Highly Speculative | Reduces to restatement |
| 6 | Quantum-Inspired Algorithms | Moderate | **Plausible** | Tensor network contraction for $P(G,k)$ |
| 7 | Scientific ML | Weak | Highly Speculative | Spectral methods on Laplacian |
| 8 | Chaos Theory | Weak-Moderate | Speculative | Lyapunov analysis of Kempe dynamics |
| 9 | Optimal Transport | Weak-Moderate | Speculative | Wasserstein metric on colourings |
| 10 | **Hypergraph Theory** | **Strong** | **Promising** | DP-colouring; LLL; fractional $\chi$ |
| 11 | Quantum Information | Moderate | **Plausible** | Tensor networks; quantum chromatic number |
| 12 | **TQFT** | **Strong** | **Promising** | Penrose evaluation as state sum |
| 13 | Algebraic Geometry (Strings) | Weak | Highly Speculative | Tropical geometry; Baker-Norine |
| 14 | Non-commutative Geometry | Weak-Moderate | Speculative | Operator systems; quantum colouring |
| 15 | Langlands Program | Weak | Speculative | Ramanujan graphs; Ihara zeta |
| 16 | Homotopy Type Theory | Moderate | **Plausible** | HITs for planar graphs; constructive proofs |
| 17 | Analytic Number Theory | Weak | Highly Speculative | Fourier analysis of colouring sums |
| 18 | Discrete Geometry | Moderate | **Plausible** | Circle packing; conformal invariants |
| 19 | Category Theory | Moderate-Strong | **Plausible** | Chromatic homology; sheaf cohomology |
| 20 | **ATP / Formal Repos** | **Strong** | **Promising** | Lean 4; AI proof search; SAT solvers |

### 4.2 Tier Rankings

**Tier 1 — Promising (actionable research programmes):**
- **Area 20 (ATP):** Most immediately actionable. Gonthier's Coq proof already exists; porting to Lean 4 + Mathlib combined with AI-guided search (AlphaProof-style) is the most likely path to a simpler proof.
- **Area 12 (TQFT):** Strongest mathematical bridge. The 4CT reformulated as "a certain SO(3) Turaev-Viro state sum is nonzero for all bridgeless planar cubic graphs." Proving non-vanishing via unitarity/positivity of the modular tensor category is a concrete research programme.
- **Area 10 (Hypergraph Theory):** DP-colouring, Lovász Local Lemma, and fractional chromatic number via clique hypergraphs — active, well-defined programmes with direct 4CT relevance.

**Tier 2 — Plausible (genuine technical bridges):**
- **Area 6 (Quantum-Inspired):** Tensor network contraction computes $P(G,k)$ for planar graphs in $\exp(O(\sqrt{n}))$ — a genuine computational tool for the algebraic strategy.
- **Area 11 (Quantum Info):** Tensor networks + quantum chromatic number add algebraic depth.
- **Area 16 (HoTT):** Higher inductive types represent planar graphs as cell complexes natively; potential for new inductive proof structures.
- **Area 18 (Discrete Geometry):** Circle packing gives canonical geometric embeddings; conformal invariants might control Kempe chains.
- **Area 19 (Category Theory):** Chromatic homology (categorifying $P(G,k)$) and sheaf cohomology offer genuinely new proof strategies — a cohomological vanishing theorem for planarity.

**Tier 3 — Speculative (interesting but distant):**
- Areas 1 (GDL), 3 (TDA), 8 (Chaos), 9 (Optimal Transport), 14 (NCG), 15 (Langlands)

**Tier 4 — Highly Speculative (no clear pathway):**
- Areas 2 (Info Geometry), 4 (Transformer Theory), 5 (Mean-Field Games), 7 (SciML), 13 (Algebraic Geometry/Strings), 17 (Analytic Number Theory)

### 4.3 Cross-Domain Integration Pipeline

The most actionable cross-domain programme combines three areas:

1. **Tensor networks (Area 6/11):** Efficiently compute chromatic polynomials $P(G,k)$ for planar graphs using planar tensor network contraction.
2. **Geometric Deep Learning (Area 1):** Feed tensor network outputs into GDL architectures to identify structural patterns — which features of a planar graph predict whether Kempe chains behave well?
3. **Hypergraph/DP-colouring framework (Area 10):** Formalize any discovered patterns rigorously using the DP-colouring framework.

This pipeline combines computational efficiency (tensor networks), pattern discovery (GDL), and mathematical rigour (hypergraph theory).

---

## 5. Agent 1221's Novel Strategy Proposals

*Full analysis: `sub_proof_strategies.md`, Section 7*

### Strategy 6: Spectral — Colin de Verdiere's Invariant

Colin de Verdiere's invariant $\mu(G)$ satisfies $\mu(G) \leq 3$ iff $G$ is planar. The conjecture $\chi(G) \leq \mu(G) + 1$ would immediately prove 4CT as a corollary ($\chi(G) \leq 3 + 1 = 4$). This is one of the most important open problems connecting spectral graph theory to colouring, and a proof would be a landmark.

**Rating:** Low-Medium feasibility, Very High elegance.

### Strategy 7: Probabilistic — Kempe Chain Markov Chain

Standard LLL is too weak for $k = 4$ colours. But the **Kempe chain Markov chain** — studying whether random Kempe swaps reduce a 5-colouring to a 4-colouring — is a concrete direction. Las Vergnas and Meyniel (1981) showed the 5-colouring Kempe graph is connected for planar graphs; the 4-colouring version is open and important.

**Rating:** Low feasibility (for full proof), Medium for partial results on Kempe dynamics.

### Strategy 8: Matroid Theory / Critical Group

Via the Baker-Norine Riemann-Roch theorem for graphs, connecting colouring to tropical algebraic geometry. The critical group $K(G) = \mathbb{Z}^{n-1}/\text{Im}(L_0)$ encodes graph structure through its invariant factors. Whether the $\mathbb{Z}_4$-rank of $K(G)$ constrains $\chi(G)$ for planar graphs is an unexplored question.

**Rating:** Low feasibility, Very High elegance.

### Strategy 9: Hadwiger Conjecture (for $k=5$ without 4CT)

Hadwiger for $k=5$ states every $K_5$-minor-free graph is 4-colourable. Robertson-Seymour-Thomas (1993) proved this — *using 4CT as an ingredient*. A 4CT-independent proof would yield 4CT as a corollary via a completely different route. The key is understanding why $K_5$-minor-free graphs decompose into pieces that are each individually 4-colourable.

**Rating:** Low-Medium feasibility, Very High elegance.

### Strategy 10: Representation Theory — Chromatic Symmetric Function

Stanley's chromatic symmetric function $X_G$ lifts $P(G,k)$ to the ring of symmetric functions. The Schur expansion coefficients encode representation-theoretic structure. If specific positivity properties of $X_G$ hold for planar graphs, they could imply $P(G,4) > 0$. The recent resolution of the Stanley-Stembridge conjecture (Hikita, 2024) energizes this area.

**Rating:** Low feasibility, Very High elegance.

### Strategy 11: Game-Theoretic — The Kempe Swap Game

Start with a proper 5-colouring (guaranteed by the Five Colour Theorem). Ask: can a sequence of Kempe chain swaps always eliminate one colour? This is equivalent to: is every proper 5-colouring of a planar graph Kempe-equivalent to a proper 4-colouring? Computationally verifiable for small graphs, and Fisk's theory of Kempe equivalence classes (relating them to $\mathbb{Z}_2$-homology) provides algebraic tools.

**Rating:** Medium feasibility, Medium-High elegance. **Most promising novel strategy for near-term computational verification.**

---

## 6. Integrated Research Programme

Based on the full analysis of 11 proof strategies and 20 cross-domain areas, I recommend a structured three-track programme:

### Track A: Near-Term / High-Feasibility (6-12 months)

**Primary: Refined Discharging (Strategy 4) + ATP (Area 20)**

1. Build a modern discharging framework in Python/Rust that takes a set of discharging rules, computes the implied unavoidable set, and tests each configuration for reducibility using SAT solvers.
2. Use SAT/SMT-based search to find optimal discharging rules minimizing configuration count. Target: reduce from 633 to $\leq 100$.
3. Begin Lean 4 formalization of planar graph theory and Kempe chain arguments (Five Colour Theorem first, as a warmup).
4. For each configuration in the reduced set, develop the simplest Kempe-chain reducibility argument, targeting single-page proofs.

**Secondary: Kempe Swap Game (Strategy 11)**

5. Computationally verify that every proper 5-colouring of every planar triangulation on $\leq 15$ vertices can be reduced to a 4-colouring by Kempe swaps.
6. Study the Kempe reconfiguration graph structure: diameter, connectivity, spectral gap.
7. Develop structural lemmas about colour elimination strategies.

### Track B: Medium-Term / High-Elegance (1-3 years)

**Primary: TQFT / Penrose Evaluation (Area 12)**

8. Study the Penrose evaluation of planar cubic graphs as a specialization of the SO(3) Turaev-Viro state sum.
9. Investigate whether unitarity of the underlying modular tensor category implies non-vanishing for planar inputs.
10. Verify computationally that the $6j$-symbols satisfy sign conditions preventing cancellation, then attempt algebraic proof.

**Secondary: Topological Kempe Chains (Strategy 3) + Category Theory (Area 19)**

11. Formalize the Kempe chain non-crossing property in planar graphs. Determine the full set of topological constraints on Kempe chain interactions at degree-5 vertices.
12. Develop a sheaf-theoretic formulation: define a cellular sheaf $\mathcal{F}_4$ on planar graphs such that $\Gamma(G, \mathcal{F}_4) \neq 0$ iff $G$ is 4-colourable. Investigate whether planarity implies $H^1 = 0$.
13. Explore chromatic homology categorification and whether positivity properties for planar graphs at $k=4$ follow from the categorified structure.

### Track C: Long-Term / Exploratory (3+ years)

**Primary: Hadwiger for $k=5$ (Strategy 9) + Colin de Verdiere (Strategy 6)**

14. Study the Robertson-Seymour-Thomas proof of Hadwiger for $k=5$ to identify where 4CT is invoked and whether it can be replaced with weaker structural results.
15. Investigate $\chi(G) \leq \mu(G) + 1$ for planar graphs and related spectral approaches.

**Secondary: Tensor Network Pipeline (Areas 6, 1, 10)**

16. Implement planar tensor network contraction for $P(G,k)$ and compute for triangulations up to $n = 30$.
17. Train GDL architectures to identify structural patterns in the intermediate tensors at $k = 4$.
18. Formalize any discovered patterns in the DP-colouring framework.

### Cross-Cutting Theme

Across all tracks, the interaction between **Kempe chains and planarity** is the central mathematical question. The Jordan Curve Theorem constrains Kempe chain geometry (Track B); discharging identifies where Kempe chains are needed (Track A); the game-theoretic formulation asks whether Kempe swaps always succeed (Track A); the TQFT formulation encodes Kempe-like structure in state sums (Track B); and the spectral/algebraic approaches encode Kempe properties in algebraic invariants (Track C).

**A deep understanding of Kempe chains in planar graphs is the foundation on which all strategies ultimately rest.**

---

## 7. Conclusion

The Four Colour Theorem sits at the intersection of combinatorics, topology, algebra, and computation. Fifty years after Appel and Haken's proof, it remains the only major theorem whose proof is essentially non-human-readable. The search for a deductive proof is not merely aesthetic — it would reveal *why* four colours suffice, not just that they do.

This report identifies clear priorities:

1. **Refined discharging + SAT solvers** is the most feasible near-term path. Modern tools could push 633 configurations down dramatically — perhaps to the threshold of human readability.

2. **The TQFT/Penrose evaluation** is the most mathematically exciting pathway. The 4CT reformulated as a non-vanishing condition for a topological state sum connects to deep structures in representation theory and quantum topology.

3. **Automated theorem proving in Lean 4**, combined with AI-guided proof search, is the most practically actionable cross-domain direction. The tools have matured enormously since Gonthier's 2005 Coq proof.

4. **The Kempe chain non-crossing property** is the most underexploited mathematical structure. Formalizing and exploiting the topological constraints on Kempe chain interactions at degree-5 vertices could reduce the case analysis to human-checkable size — potentially bridging the gap between the Five Colour Theorem (where one swap always works) and the Four Colour Theorem (where it doesn't, but planarity limits how badly it can fail).

The sub-reports in this folder provide detailed analyses for each strategy and cross-domain area, including specific feasibility ratings, risk assessments, synergy maps, and concrete next steps. They are intended as reference documents for agents assigned to pursue individual research tracks.

---

*Agent 1221 — Graph Colouring Project*  
*17 February 2026*

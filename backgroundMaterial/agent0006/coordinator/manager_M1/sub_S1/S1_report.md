# M1/S1 Report: Filtered Proof Strategies

**Agent:** 0006-M1-S1  
**Date:** 18 February 2026  
**Task:** Apply viability threshold to all 11 proof strategies from Agent 1221's analysis. Produce a filtered list with include/exclude justification and ProofNavigator integration notes.

---

## Viability Threshold (as specified)

**Include if:**
- Feasibility ≥ Medium, OR
- Explicitly recommended by Agent 1221 in Integrated Research Programme (§6)

**Exclude if:**
- Feasibility = Low AND no concrete near-term computational programme

---

## Filtered Strategy Table

| # | Strategy | Feasibility | Include? | Reason | Agent 1221 §6 Track |
|---|----------|-------------|----------|--------|---------------------|
| 1 | Chromatic Polynomial | Medium-Low | **EXCLUDE** | Below Medium; not in §6 as standalone | — |
| 2 | Flow-Theoretic | Medium-Low | **EXCLUDE** | Below Medium; not in §6 as standalone | — |
| 3 | Topological (Kempe non-crossing) | Low-Medium | **INCLUDE** | Explicitly in §6 Track B (secondary) | Track B |
| 4 | Fewer Configurations (Refined Discharging) | **High** | **INCLUDE** | Highest feasibility; §6 Track A primary | Track A |
| 5 | Proof Mining (Coq extraction) | Medium | **INCLUDE** | Meets Medium threshold; complement to S4 in §6 Track A | Track A |
| 6 | Spectral (Colin de Verdière) | Low-Medium | **INCLUDE** | Explicitly in §6 Track C (primary) | Track C |
| 7 | Probabilistic (LLL / Kempe dynamics) | Low | **EXCLUDE** | Below Medium; not in §6; $k=4$ too small for LLL | — |
| 8 | Matroid / Critical Group | Low | **EXCLUDE** | Below Medium; not in §6; indirect connection to $\chi$ | — |
| 9 | Hadwiger Conjecture ($k=5$) | Low-Medium | **INCLUDE** | Explicitly in §6 Track C (primary) | Track C |
| 10 | Representation Theory ($X_G$) | Low | **EXCLUDE** | Below Medium; not in §6; $X_G$ too rich to control | — |
| 11 | Kempe Swap Game | **Medium** | **INCLUDE** | Meets Medium threshold; §6 Track A secondary | Track A |

---

## Included Strategies — Detailed Justifications

### Strategy 3: Topological (Kempe Chain Non-Crossing)

**Feasibility:** Low-Medium  
**Threshold passage:** Via §6 explicit recommendation (Track B secondary)

**Justification:** While below Medium on its own, Agent 1221 identifies the Kempe chain non-crossing property as *the* central underexploited mathematical structure. The Jordan Curve Theorem constrains how Kempe chains for different colour pairs can interact at degree-5 vertices — a constraint barely used in existing proofs. This strategy serves as connective tissue between Tracks A, B, and C in the research programme.

**ProofNavigator integration:** New track or sub-track of Track 1. Sub-goals: (1) Formalize non-crossing property, (2) Enumerate topological constraints at degree-5 vertices, (3) Test whether constraints reduce case analysis to human-checkable size, (4) Connect to Thomassen's 5-list-colouring argument.

### Strategy 4: Fewer Configurations (Refined Discharging)

**Feasibility:** High  
**Threshold passage:** Highest-rated strategy; §6 Track A primary

**Justification:** The most immediately actionable strategy. RSST used 32 discharging rules and 633 configurations. Modern SAT/SMT solvers could search for optimal rules, potentially pushing $N$ below 50. No theoretical lower bound on $N$ is known. If achieved, each reducibility check becomes a few-page Kempe chain argument — yielding a "mostly deductive" proof.

**ProofNavigator integration:** New dedicated track (highest priority). Sub-goals: (1) Build flexible discharging framework (Python/Rust), (2) SAT/SMT search for optimal rules targeting $N \leq 100$, (3) Theoretical study of minimum $N$, (4) Human-friendly reducibility proofs for each configuration.

### Strategy 5: Proof Mining

**Feasibility:** Medium  
**Threshold passage:** Meets Medium threshold directly

**Justification:** Complements Strategy 4. If the 633 RSST reducibility checks cluster into a small number of parameterized lemma families, the effective proof size drops dramatically. The obstacle is that most of the Coq proof is computation, not deduction — extraction is analogous to decompilation. LLM-based proof analysis could accelerate this.

**ProofNavigator integration:** New dedicated track or merged with Strategy 4 track. Sub-goals: (1) Obtain and instrument Gonthier's Coq proof, (2) Trace reducibility checks, (3) Cluster configurations by argument structure, (4) Write parameterized lemma templates, (5) LLM-assisted proof compression.

### Strategy 6: Spectral (Colin de Verdière)

**Feasibility:** Low-Medium  
**Threshold passage:** Via §6 explicit recommendation (Track C primary)

**Justification:** The conjecture $\chi(G) \leq \mu(G) + 1$ would prove 4CT as immediate corollary ($\mu \leq 3$ for planar, so $\chi \leq 4$). This is one of the most important open problems connecting spectral graph theory to colouring. Very High elegance justifies long-term investment despite lower feasibility.

**ProofNavigator integration:** Already present as Track 5. Update with §6 Track C alignment. No structural changes needed.

### Strategy 9: Hadwiger Conjecture ($k=5$ without 4CT)

**Feasibility:** Low-Medium  
**Threshold passage:** Via §6 explicit recommendation (Track C primary)

**Justification:** Robertson-Seymour-Thomas proved Hadwiger for $k=5$ *using 4CT*. A 4CT-independent proof would yield 4CT as corollary via a completely different route. The structural question — why do $K_5$-minor-free graphs decompose into 4-colourable pieces? — is deep and might yield fundamentally new insights.

**ProofNavigator integration:** New dedicated track. Sub-goals: (1) Study RST proof in detail, identify where 4CT is invoked, (2) Attempt restructuring with weaker structural results, (3) Investigate whether decomposition of $K_5$-minor-free graphs can bypass 4CT.

### Strategy 11: Kempe Swap Game

**Feasibility:** Medium  
**Threshold passage:** Meets Medium threshold directly; §6 Track A secondary

**Justification:** Computationally verifiable for small graphs. Fisk's theory of Kempe equivalence classes provides algebraic tools. Most promising novel strategy for near-term computational verification. Direct question: can Kempe swaps always reduce a 5-colouring to a 4-colouring?

**ProofNavigator integration:** Already present as Track 1. Update with §6 alignment and computational milestones.

---

## Excluded Strategies — Brief Justifications

### Strategy 1: Chromatic Polynomial

**Reason:** Medium-Low feasibility. Birkhoff-Lewis gap ($k \geq 5$ to $k \geq 4$) has resisted 80 years. Sokal's density result and Beraha accumulation at 4 create fundamental barriers. Not independently recommended in §6.

**Note:** Already in ProofNavigator as Track 2. Recommend **downgrading priority** rather than removing, since chromatic polynomial computation feeds Track 7 (Computational Discovery) and the algebraic strategy provides theoretical context. See escalation note.

### Strategy 2: Flow-Theoretic

**Reason:** Medium-Low feasibility. Provably equivalent to 4CT (reformulation, not simplification). 5-flow conjecture open for 70+ years. Not independently recommended in §6.

**Note:** Already in ProofNavigator as Track 3. Recommend **downgrading priority** rather than removing. The flow formulation connects to algebraic topology and may provide insight for other tracks. See escalation note.

### Strategy 7: Probabilistic

**Reason:** Low feasibility. $k=4$ is too small for LLL ($ep(d+1) \leq 1$ requires $\Delta \leq 0.24$). Entropy compression also too weak. Kempe dynamics angle is subsumed by Strategy 11.

### Strategy 8: Matroid / Critical Group

**Reason:** Low feasibility. Connection between critical group and chromatic number is indirect. Baker-Norine Riemann-Roch is elegant but does not yield colouring bounds.

### Strategy 10: Representation Theory

**Reason:** Low feasibility. $X_G$ is richer than $P(G,k)$ but harder to analyze. No established pathway from Schur/e-positivity of chromatic symmetric function to $P(G,4) > 0$ for planar graphs.

---

## Summary

**6 strategies pass threshold:** 3, 4, 5, 6, 9, 11  
**5 strategies excluded:** 1, 2, 7, 8, 10

**Tension point:** Strategies 1 and 2 are already in ProofNavigator as Tracks 2 and 3 but do not pass the threshold. Recommend escalation to determine handling (downgrade vs. remove vs. retain at current level).

---

*Agent 0006-M1-S1 — 18 February 2026*

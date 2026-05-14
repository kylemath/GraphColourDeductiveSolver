# Task Brief — Manager 0050-M2 ("The Mathematicians")

**From:** Coordinator 0050-C
**To:** Manager 0050-M2
**Date:** 18 February 2026

---

## Mission

You lead the **Theoretical Formalization Team** ("The Mathematicians") for Plan 2: Kempe Swap Game + Topological Non-Crossing. Your mission: **prove general theorems, classify all cases, and attempt the key structural lemma** that would yield a constructive proof of the Four Colour Theorem.

You are in **direct competition** with Manager 0050-M1 ("The Engineers"). They are building computational infrastructure to test your claims and find cases that break your theorems. Whoever produces more impactful, tested results wins.

## Mathematical Context

**Plan 2 Core Question:** Starting from any proper 5-colouring of a planar graph (guaranteed by 5CT), can a sequence of Kempe chain swaps always eliminate one colour? If yes → constructive proof of 4CT.

Key objects:
- **Kempe chains**: maximal bichromatic connected subgraphs
- **Kempe swap**: swap colours $a \leftrightarrow b$ on a Kempe chain; preserves proper colouring
- **Non-crossing property**: in planar graphs, Kempe chains for disjoint colour pairs $\{a,b\}$ and $\{c,d\}$ cannot cross (Jordan Curve Theorem)
- **Reconfiguration graph** $\mathcal{R}(G,k)$: nodes = proper $k$-colourings, edges = single Kempe swaps
- $\mathcal{R}(G,5)$ is always connected for planar $G$ (Las Vergnas-Meyniel 1981)
- $\mathcal{R}(G,4)$ connectivity is OPEN — equivalent to 4CT
- Fisk (1977): 4-colourings mod Kempe swaps form group $\cong \mathbb{Z}_2^g$

**Target theorems from Plan 2:**
- **Theorem A (Non-Interleaving):** If $K_{ab}$ chain from $w_i$ reaches $w_k$, then $K_{cd}$ chain from $w_j$ stays within the arc — no crossing
- **Theorem B (Confinement):** If $K_{ab}$ separates $w_j$ from $w_\ell$, no swaps on other colours can reconnect them
- **Colour Elimination Lemma:** There exists an ordering $v_1, \ldots, v_s$ such that each $v_i$ can be sequentially recoloured using swaps not affecting earlier vertices

## Your Team — 3 Sub-workers

You must spawn exactly 3 sub-workers as Task subagents. They build on each other's results. Launch S1 first (foundation), then S2 (uses S1), then S3 (uses S1+S2). You may launch S2 and S3 in parallel if S2 can proceed without waiting for S1's final output.

### M2-S1: Non-Crossing Theorems A & B

**Task:** Write rigorous mathematical proofs of Theorem A (Non-Interleaving) and Theorem B (Confinement).

**Theorem A (Non-Interleaving):** In a planar triangulation $T$ with proper 4-colouring $c$, consider a degree-5 vertex $v$ with cyclic neighbours $w_1, w_2, w_3, w_4, w_5$ (in the planar embedding order). If the $(a,b)$-Kempe chain from $w_i$ reaches $w_k$ (where $i < k$ cyclically), then the $(c,d)$-Kempe chain from $w_j$ (where $i < j < k$ cyclically, and $\{a,b\} \cap \{c,d\} = \emptyset$) stays entirely within the region bounded by the chain and the arc from $w_i$ to $w_k$ through $v$.

**Theorem B (Confinement):** If a $(a,b)$-Kempe chain $K_{ab}$ separates two vertices $w_j$ and $w_\ell$ in the plane (they lie in different connected components of $\mathbb{R}^2 \setminus K_{ab}$), then no sequence of Kempe swaps involving only colours from $\{1,2,3,4\} \setminus \{a,b\}$ can create a path from $w_j$ to $w_\ell$ that does not cross $K_{ab}$.

**Deliverables:**
1. `theorem_A_proof.md` — complete proof of Theorem A with precise statement, proof, and discussion of edge cases
2. `theorem_B_proof.md` — complete proof of Theorem B
3. `S1_report.md` — summary report

**Acceptance Criteria (TESTS — these are checkpoints, not code):**
- `test_theorem_A_precise`: Statement handles all edge cases (what if the chain reaches the boundary? what about the vertex $v$ itself?)
- `test_theorem_B_precise`: Statement covers the case where multiple chains create nested regions
- `test_consistency_with_computation`: Predictions match what computational verification would find (state predictions explicitly so M1-S3 can check them)

**Output Location:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent0050/coordinator/manager_M2/sub_S1/`

### M2-S2: Degree-5 Case Classification

**Task:** Enumerate ALL topologically distinct Kempe chain configurations at a degree-5 vertex under the non-crossing constraint from Theorem A.

For a degree-5 vertex $v$ with cyclic neighbours $w_1, \ldots, w_5$:
- The central vertex $v$ has some colour, say colour 5
- Each neighbour $w_i$ has a colour from $\{1,2,3,4\}$
- Up to colour permutation, classify all distinct colour assignments
- For each colour assignment, enumerate the topologically distinct ways Kempe chains can connect the neighbours (constrained by planarity + non-crossing)
- For EACH pattern, determine: can a Kempe swap sequence free one of $\{1,2,3,4\}$ for vertex $v$?

**Deliverables:**
1. `degree5_classification.md` — complete case enumeration with diagrams (ASCII or described)
2. `case_analysis.md` — for each case, the swap sequence that works OR a proof that multi-step resolution is needed
3. `S2_report.md` — summary report

**Acceptance Criteria (TESTS):**
- `test_classification_exhaustive`: Every configuration is accounted for (justified by combinatorial argument)
- `test_each_case_resolved`: Each case has a swap sequence OR a documented obstacle
- `test_count_bounded`: Total number of distinct cases is enumerated (Plan 2 hopes $\leq 20$)

**Output Location:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent0050/coordinator/manager_M2/sub_S2/`

**Dependency:** Uses Theorem A from S1 to constrain which chain configurations are possible.

### M2-S3: Colour Elimination Lemma

**Task:** Attempt to prove the key structural lemma:

**Colour Elimination Lemma:** Given a proper 5-colouring $c$ of a planar graph $G$, let colour 5 be used by $k$ vertices $V_5 = \{v_1, \ldots, v_k\}$. Then there exists an ordering of $V_5$ such that each $v_i$ can be recoloured to $\{1,2,3,4\}$ using Kempe swaps that do not change the colours of $v_1, \ldots, v_{i-1}$.

If a full proof is not achievable, identify the EXACT obstacle and state precisely what additional lemma would suffice.

**Deliverables:**
1. `colour_elimination_attempt.md` — proof attempt with honest assessment of gaps
2. `obstacle_analysis.md` — if proof fails, precise description of what goes wrong and what would fix it
3. `S3_report.md` — summary report

**Acceptance Criteria (TESTS):**
- `test_strategy_works_on_small_cases`: The ordering strategy should work for graphs where M1's computational search succeeds
- `test_no_circular_dependencies`: Recolouring $v_i$ never requires changing earlier vertices (formally argued)
- `test_obstacle_identified`: If the proof fails, the specific obstruction is documented with mathematical precision

**Output Location:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent0050/coordinator/manager_M2/sub_S3/`

**Dependency:** Uses Theorems A, B from S1 and case classification from S2.

## Writing Standards

- Use `$...$` for inline math in Markdown
- Every proof step must cite its justification (Jordan Curve Theorem, planarity, etc.)
- Be honest about uncertainty — write "speculative" not "might work"
- Rate the feasibility of each proof attempt: Low / Medium-Low / Medium / Medium-High / High
- Every analysis ends with **concrete next steps**

## Report Format

Write `manager_M2_report.md` in your folder (`/Users/kylemathewson/GraphColour/backgroundMaterial/agent0050/coordinator/manager_M2/`) following this structure:

```
# Manager 0050-M2 Report

**Agent:** 0050-M2
**Stream:** parallel — Theoretical Formalization ("The Mathematicians")
**Coordinator:** 0050-C
**Status:** [Complete / In Progress / Blocked]

## Stream Summary
## Sub-subagent Status (table)
## Collected Outputs
## Integration Notes
## Competition Results (what we proved that goes beyond M1's computational reach)
## Issues Encountered
## Self-Assessment (Craftsperson/Skeptic/Mover)
```

## Competition Framing

Your team COMPETES against M1 ("The Engineers"). Specifically:
- Your Theorem A must make **testable predictions** that M1-S3 can verify computationally
- Your case classification must **explain every hard case** that M1-S1 encounters
- Your Colour Elimination Lemma must work on **every graph** M1 tests, not just convenient examples
- **General theorems** that go beyond M1's verified range are your strongest weapon — prove things about ALL planar graphs, not just small ones

---

*Coordinator 0050-C — 18 February 2026*

# Plan 1: Refined Discharging + SAT Optimization + Proof Mining

**Priority:** Critical — highest confidence, nearest-term results  
**Time Horizon:** 6–12 months  
**Source Strategies:** Strategy 4 (Refined Discharging), Strategy 5 (Proof Mining), Area 20 (ATP/SAT)  
**§6 Alignment:** Track A Primary  
**ProofNavigator Tracks:** 8 (Discharging), 9 (Proof Mining), 11 (Formal Methods)

---

## 1. Central Thesis

The RSST proof uses 32 discharging rules and 633 reducible configurations. Both numbers were chosen by 1997-era tools and have never been re-optimized with modern solvers. **No lower bound on the minimum configuration count $N$ is known.** If $N$ can be pushed below ~50, each reducibility check becomes a 1-page Kempe chain argument, yielding a human-readable proof. Simultaneously, clustering the existing 633 checks into parameterized families can collapse the effective proof size even without reducing $N$.

The combination of three tools — SAT-based discharging optimization (shrink $N$), proof mining (cluster and parameterize the checks), and Lean 4 formalization (verify everything) — attacks the problem from complementary angles.

---

## 2. Mathematical Foundation

### 2.1 Discharging

Assign charge $c(v) = 6 - \deg(v)$ to each vertex of a planar triangulation $T$. By Euler's formula:

$$\sum_{v \in V} c(v) = \sum_{v \in V} (6 - \deg(v)) = 6|V| - 2|E| = 6|V| - 2(3|V| - 6) = 12$$

Total positive charge is exactly 12. Discharging rules redistribute charge according to local degree conditions while preserving the total. After redistribution, any vertex retaining positive final charge must be surrounded by one of $N$ specific local configurations — the **unavoidable set**.

### 2.2 Reducibility

A configuration $C$ with boundary ring $R$ is **D-reducible** if every proper 4-colouring of $R$ extends to a proper 4-colouring of $C \cup R$. This is verified by checking (possibly after Kempe chain swaps) that all $4^{|R|}$ boundary colourings extend. If every configuration in the unavoidable set is reducible, no minimal counterexample exists.

### 2.3 The Optimization Problem

The RSST proof is characterized by three numbers:

| Parameter | Appel-Haken (1976) | RSST (1997) | Target |
|-----------|-------------------|-------------|--------|
| Discharging rules | 487 | 32 | $\leq 64$ (flexible) |
| Configurations $N$ | 1,476 | 633 | $\leq 50$ |
| Max ring size | 14 | 14 | $\leq 12$ (preferred) |

The trade-off: more sophisticated rules $\Rightarrow$ smaller $N$ but harder-to-verify rules. We want the Pareto frontier of this trade-off.

---

## 3. Phase Structure

### Phase 1: Infrastructure (Months 1–2)

#### 1A. Build Flexible Discharging Framework

**Goal:** Software that takes an arbitrary set of discharging rules, computes the implied unavoidable set, and tests each configuration for reducibility.

**Specification:**
- **Input:** A set of discharging rules in a declarative format (e.g., "if $\deg(v) = 5$ and $v$ has $k$ neighbours of degree $\leq 6$, then $v$ receives charge $r$ from each degree-$d$ neighbour")
- **Core computation:** Given rules, enumerate all local configurations that can retain positive final charge. This is the unavoidable set.
- **Reducibility oracle:** For each configuration, test D-reducibility by checking boundary colouring extensions. Use Kempe chain analysis to reduce the search space.
- **Output:** The unavoidable set, reducibility status of each configuration, and a certificate for each reducibility proof (the sequence of Kempe swaps that extends each boundary colouring)

**Implementation:**
- Python prototype for rule specification and unavoidable set computation
- Rust core for reducibility checking (performance-critical: $4^{14} \approx 2.7 \times 10^8$ boundary colourings per ring-14 configuration)
- Output format compatible with SAT solver input (Phase 2) and Lean 4 verification (Phase 3)

**Files:** `compute/discharging/framework.py`, `compute/discharging/reducibility_checker.rs`

**Deliverable:** A working system that reproduces RSST's 633 configurations from their 32 rules.

**Kill criterion:** Cannot reproduce RSST results after 4 weeks.

#### 1B. Obtain and Compile Gonthier's Coq Proof

**Goal:** A working, instrumented build of the ~60,000-line Coq formalization.

**Steps:**
1. Clone the Mathematical Components library's maintained version of the four-colour theorem proof
2. Build with modern Coq (8.18+ / rocq-prover)
3. Add logging instrumentation to the reducibility checker: for each of the 633 configurations, output the trace of Kempe chain swaps used to extend each boundary colouring
4. Export configuration data in a machine-readable format (adjacency lists, ring vertices, internal vertices)

**Deliverable:** Instrumented Coq proof that compiles and produces 633 reducibility traces.

**Kill criterion:** Cannot compile or instrument after 4 weeks. Fallback: work directly from RSST's published configuration data.

#### 1C. Lean 4 Graph Theory Foundation

**Goal:** Shared Lean 4 libraries for planar graphs, Kempe chains, and colouring.

**Steps:**
1. Define `PlanarGraph` using Mathlib's `SimpleGraph` API, via forbidden minors ($\neg K_5 \leq_m G \wedge \neg K_{3,3} \leq_m G$)
2. Prove Euler's formula: $V - E + F = 2$ for connected planar graphs
3. Derive corollary: $E \leq 3V - 6$, every planar graph has a vertex of degree $\leq 5$
4. Define Kempe chains as maximal bichromatic connected subgraphs
5. Prove Kempe swap preserves proper colouring
6. Prove the Five Colour Theorem (warmup for all subsequent formalization)

**Files:** `lean4/FourColor/Infrastructure/PlanarGraph.lean`, `lean4/FourColor/Infrastructure/KempeChain.lean`

**Deliverable:** Lean 4 proof of the Five Colour Theorem.

---

### Phase 2: SAT-Based Optimization (Months 2–5)

#### 2A. Encode Discharging as SAT/SMT

**Goal:** Find the Pareto frontier of (rule complexity, configuration count).

**Approach:**

The discharging optimization problem can be encoded as follows:

- **Variables:** For each candidate discharging rule $r_i$ (from a parametric family), a Boolean variable $x_i$ indicating whether the rule is included
- **Constraints:**
  - **Unavoidability:** For each possible local configuration $C_j$ around a positive-charge vertex, at least one active rule must apply to reduce its charge below zero, OR $C_j$ is in the unavoidable set
  - **Reducibility:** Every configuration in the unavoidable set must be D-reducible (pre-computed by the reducibility checker)
  - **Cardinality:** The total unavoidable set size $|\{j : C_j \text{ survives}\}| \leq N$ for target $N$
- **Objective:** Minimize $N$ subject to all configurations being reducible

**SAT solver:** CaDiCaL or Kissat for pure SAT encoding. Z3 or cvc5 for SMT (allows richer rule parametrization).

**Search strategy:**
1. Start with RSST's 32 rules, verify $N = 633$
2. Extend the rule family: allow rules involving 2-hop neighbourhood information (RSST uses only 1-hop)
3. Binary search on $N$: attempt $N = 400$, then $N = 200$, narrowing to the minimum

**Milestones:**
| Month | Target | Significance |
|-------|--------|--------------|
| Month 2 | Reproduce $N = 633$ | Validates framework |
| Month 3 | $N \leq 400$ | First improvement over RSST |
| Month 4 | $N \leq 200$ | Major reduction |
| Month 5 | $N \leq 100$ or proven plateau | Approaching human readability |

**Files:** `compute/discharging/sat_search.py`, `compute/discharging/rule_encoder.py`

**Kill criterion:** No improvement below 633 after 8 weeks of solver time.

#### 2B. Cluster Reducibility Traces

**Goal:** Identify families of "essentially identical" reducibility arguments among the 633 (or fewer) configurations.

**Method:**
1. From Phase 1B's instrumented traces, extract feature vectors for each configuration:
   - Ring size, number of internal vertices, degree sequence
   - Number of Kempe swaps needed, which colour pairs involved
   - Which boundary colourings are "hard" (require the most swaps)
2. Apply clustering (hierarchical clustering with graph edit distance, then k-means refinement)
3. For each cluster, identify the common reducibility argument pattern

**Success criterion:** At least one cluster with $\geq 50$ configurations sharing a common argument structure.

**Deliverable:** A clustering report with proposed parameterized lemma families.

**Files:** `compute/proofmining/cluster_configs.py`, `compute/proofmining/trace_analysis.py`

---

### Phase 3: Proof Construction (Months 5–9)

#### 3A. Write Parameterized Reducibility Lemmas

**Goal:** For each cluster from 2B, write a single parameterized lemma covering all configurations in the cluster.

**Form of each lemma:**

> **Lemma ($\mathcal{F}_k$):** Let $C$ be a configuration with ring size $\leq r_k$, at most $m_k$ internal vertices, all of degree $\leq d_k$, and whose ring has property $P_k$. Then every proper 4-colouring of the ring boundary extends to $C$ via at most $j_k$ Kempe chain swaps.

**Process:**
1. Start with the largest cluster
2. Identify the weakest conditions ($r_k, m_k, d_k, P_k, j_k$) that still imply reducibility
3. Write the proof in informal mathematics
4. Formalize in Lean 4 (using the infrastructure from Phase 1C)
5. Verify the formal proof

**Target:** $\leq 5$ parameterized lemma families covering $\geq 80\%$ of configurations.

#### 3B. Assemble the Human-Readable Proof

**Goal:** Write a self-contained proof of 4CT that a mathematician can read.

**Structure:**
1. **Preliminaries** (5 pages): Planar graph basics, Euler's formula, Kempe chains, Five Colour Theorem
2. **Discharging argument** (5–10 pages): The optimized rule set from Phase 2A, proving the unavoidable set
3. **Reducibility** (10–30 pages): The parameterized lemma families from Phase 3A, covering all configurations
4. **Appendix:** Remaining configurations not covered by parameterized lemmas, each with individual 1-page arguments

**Total target:** $\leq 50$ pages if $N \leq 50$ and parameterized lemmas cover $\geq 80\%$.

#### 3C. Lean 4 Formalization

**Goal:** Machine-verified proof of 4CT in Lean 4.

**Steps:**
1. Formalize the discharging argument using the optimized rules
2. Implement a verified reducibility checker as a Lean 4 decision procedure
3. Verify each parameterized lemma family
4. For remaining configurations, use the verified checker
5. Assemble into a complete proof: `theorem four_colour : ∀ (G : SimpleGraph V) [Fintype V], G.IsPlanar → G.Colorable 4`

---

### Phase 4: Refinement and Publication (Months 9–12)

#### 4A. Push $N$ Lower

Continue SAT search with improved encodings informed by the clustering structure.

#### 4B. LLM-Assisted Proof Compression

Fine-tune an LLM on the Lean 4 proof corpus. Direct it to:
- Suggest unified arguments across remaining individual cases
- Find shorter Kempe chain sequences for "hard" boundary colourings
- Propose new discharging rules that eliminate specific configurations

#### 4C. Write Up Results

- Technical paper: the optimized discharging scheme, the parameterized lemma families, the minimum $N$ achieved
- Lean 4 contribution to Mathlib
- Interactive visualization updates for ProofNavigator

---

## 4. Key Mathematical Objects

### The Discharging Rules (visual representation)

```
Degree-5 vertex receives charge from neighbours:

     7        8
      \      /
       5----6        Rule: deg-7 sends 1/2 to adjacent deg-5
      / \  /         Rule: deg-8 sends 1/3 to adjacent deg-5
     6   5           Result: c'(5) = (6-5) + 1/2 + 1/3 = 1 + 5/6 > 0
                     → This local config is in the unavoidable set
```

### The Configuration Ring

A configuration $C$ with ring $R$:

```
        r₁ — r₂ — r₃
       / |         | \
      r₈  |   C    |  r₄      Ring R = {r₁,...,r₈}
       \ |  (int)  | /        Interior has vertices + edges
        r₇ — r₆ — r₅         D-reducible if all 4^8 boundary
                               colourings extend inward
```

### The Optimization Landscape

```
Rule Complexity
     ↑
     |     •RSST (32 rules, 633 configs)
     |    /
     |   / Pareto frontier
     |  /
     | /   •Target (64 rules?, ≤50 configs?)
     |/
     +————————————————→ Configuration Count N
           633  400  200  100  50
```

---

## 5. Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Hidden lower bound $N \geq 200$ | Low-Medium | High | Publish whatever $N$ is achieved; partial result is valuable |
| SAT encoding too large | Medium | Medium | Use symmetry breaking, incremental solving |
| Coq proof won't compile | Low | Low | Work from RSST published data directly |
| Configurations don't cluster | Medium | Medium | Still have reduced $N$ from Phase 2A |
| Lean 4 formalization stalls | Medium | Low | Proof is valid regardless of formalization |
| Rules too complex to verify | Low | High | Bound rule complexity in SAT encoding |

---

## 6. Success Criteria

| Milestone | Description | Feasibility |
|-----------|-------------|-------------|
| **Bronze** | Reproduce RSST, reduce $N$ to $\leq 500$ | Very High |
| **Silver** | $N \leq 200$, identify 3+ configuration clusters | High |
| **Gold** | $N \leq 50$, parameterized lemmas cover $\geq 80\%$ | Medium-High |
| **Platinum** | Complete human-readable proof ($\leq 50$ pages) + Lean 4 | Medium |

---

## 7. Required Resources

- **Compute:** SAT solver access (can run on commodity hardware; CaDiCaL is open-source). Reducibility checking benefits from parallelism (each configuration independent).
- **Expertise:** SAT/CSP encoding, graph theory, Lean 4 formalization
- **Time:** 1 researcher full-time, or 2 researchers splitting SAT work and formalization

---

## 8. Connections to Other Plans

- **Plan 2 (Kempe Swap):** The Kempe non-crossing property (Strategy 3) simplifies individual reducibility checks by constraining which Kempe chain interactions can occur. Any progress on Plan 2's topological analysis directly benefits Phase 3A's parameterized lemmas.
- **Plan 3 (TQFT):** If Plan 3 succeeds, it provides an independent proof making Plan 1's result a "second proof" — valuable for confidence but not strictly necessary. If Plan 3 stalls, Plan 1 is the fallback.
- **Track 11 (ATP):** The Lean 4 infrastructure from Phase 1C is shared with all other plans.

---

*Graph Colour Project — Plan 1*  
*18 February 2026*

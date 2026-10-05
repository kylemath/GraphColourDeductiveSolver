# Plan 3: TQFT / Penrose Evaluation + Sheaf Cohomology

**Priority:** Medium — highest mathematical ceiling, longest horizon  
**Time Horizon:** 1–3 years  
**Source:** Area 12 (TQFT), Area 19 (Category Theory), Strategy 3 (Topological)  
**§6 Alignment:** Track B Primary + Track B Secondary  
**ProofNavigator Tracks:** 4 (TQFT/Penrose), 6 (Sheaf Cohomology)

---

## 1. Central Thesis

Kauffman (1990) proved that the Four Colour Theorem is equivalent to a statement about tensor evaluation on planar graphs:

> **4CT $\Leftrightarrow$ The Penrose evaluation of every bridgeless planar cubic graph is nonzero.**

This reformulation places the 4CT inside the framework of Topological Quantum Field Theory (TQFT), specifically as a non-vanishing condition for an SO(3) state sum related to the Turaev-Viro invariant. If the unitarity or positivity of the underlying modular tensor category implies non-vanishing for planar inputs, this would constitute a structurally novel proof — one that explains *why* four colours suffice through the lens of quantum topology.

Independently, categorifying the chromatic polynomial into a bigraded homology theory (chromatic homology), or formulating 4-colouring as a sheaf cohomology problem where planarity forces $H^1 = 0$, provides a complementary algebraic pathway.

The combination of TQFT (non-vanishing via positivity) and sheaf cohomology (existence via vanishing theorems) attacks the 4CT from two sides of the same categorical framework.

---

## 2. Mathematical Foundation

### 2.1 The Penrose Evaluation

Given a planar cubic graph $G$ (every vertex has degree 3), the **Penrose evaluation** assigns a numerical value via the following procedure:

1. **Edge labelling:** Assign labels from $\{1, 2, 3\}$ to each edge of $G$
2. **Vertex weight:** At each vertex with incident edges labelled $(i, j, k)$, assign the weight $|\epsilon_{ijk}|$ — the absolute value of the Levi-Civita symbol:
   - Weight 1 if $(i, j, k)$ is a permutation of $(1, 2, 3)$
   - Weight 0 otherwise (i.e., if any two labels are equal)
3. **Evaluation:** Sum over all valid labellings:

$$\text{Pen}(G) = \sum_{\ell: E \to \{1,2,3\}} \prod_{v \in V} |\epsilon_{\ell(e_1(v)), \ell(e_2(v)), \ell(e_3(v))}|$$

**Kauffman's Theorem (1990):** A bridgeless planar cubic graph $G$ has a proper 4-face-colouring (equivalently, 4-edge-colouring by Tait's theorem) if and only if $\text{Pen}(G) \neq 0$.

**4CT reformulated:** $\text{Pen}(G) > 0$ for every bridgeless planar cubic graph $G$.

### 2.2 Connection to TQFT

The Penrose evaluation is a specialization of the **Turaev-Viro state sum** — a topological invariant of 3-manifolds constructed from a modular tensor category. Specifically:

- The Turaev-Viro invariant at level $r$ is built from the representation theory of the quantum group $U_q(\mathfrak{sl}_2)$ at $q = e^{i\pi/r}$
- At $r = 3$ (related to SO(3) representations at $q = e^{i\pi/3}$), the state sum on a planar graph produces a value closely related to the Penrose evaluation
- The **$6j$-symbols** (Racah-Wigner coefficients) of the quantum group determine the vertex weights

The modular tensor category underlying this TQFT has a key property: **unitarity**. In a unitary TQFT, the partition function of any closed manifold is a sum of squares of amplitudes — and therefore non-negative. The question is whether this unitarity argument extends to the Penrose evaluation on planar graphs.

### 2.3 The Non-Vanishing Problem

The Penrose evaluation is a sum of products of $|\epsilon|$ values. Each term is 0 or 1. Therefore:

$$\text{Pen}(G) = \#\{\text{valid edge-3-colourings of } G\}$$

A "valid" edge-3-colouring assigns labels $\{1, 2, 3\}$ to edges such that at every vertex, all three labels appear. This is a proper edge-3-colouring (also called a **Tait colouring**).

**By Tait's theorem (1880):** A bridgeless cubic graph has a Tait colouring $\Leftrightarrow$ it has a proper 4-face-colouring.

**The challenge:** Proving $\text{Pen}(G) > 0$ requires showing that at least one valid labelling exists. For non-planar cubic graphs, counterexamples exist (the Petersen graph has no Tait colouring). Planarity is essential — but how does the TQFT machinery "see" planarity?

**Potential approach via unitarity:** In the TQFT framework, the Penrose evaluation on a planar graph can be expressed as:

$$\text{Pen}(G) = \langle \psi_G | \psi_G \rangle$$

for some state vector $|\psi_G\rangle$ in the TQFT Hilbert space. If this inner product is manifestly non-negative (from unitarity) and nonzero (because $|\psi_G\rangle \neq 0$ for planar inputs), then $\text{Pen}(G) > 0$.

The key step: proving $|\psi_G\rangle \neq 0$ for all bridgeless planar cubic graphs.

### 2.4 Chromatic Homology

The chromatic polynomial $P(G, k)$ can be categorified:

**Helme-Guizon & Rong (2005):** There exists a bigraded homology theory $H^{i,j}(G)$ such that:

$$P(G, k) = \sum_{i,j} (-1)^i k^j \dim H^{i,j}(G)$$

This is analogous to how the Jones polynomial is categorified by Khovanov homology.

**The 4CT via chromatic homology:** If $H^{i,j}(G)$ for planar graphs at $k = 4$ has a positivity property — for instance, if $\sum_j (-1)^i \dim H^{i,j}(G)$ has consistent sign for all $i$ — then $P(G, 4) > 0$ follows. Establishing such a positivity property for planar graphs would be a categorified proof of 4CT.

### 2.5 Sheaf Cohomology on Graphs

A **cellular sheaf** $\mathcal{F}$ on a graph $G$ assigns:
- A vector space $\mathcal{F}(v)$ to each vertex $v$
- A vector space $\mathcal{F}(e)$ to each edge $e$
- A linear map $\mathcal{F}_{v \to e}: \mathcal{F}(v) \to \mathcal{F}(e)$ for each vertex-edge incidence

The **sheaf Laplacian** $L_\mathcal{F}$ generalizes the graph Laplacian and has a cohomology theory: $H^0(G, \mathcal{F})$ is the space of global sections, and $H^1(G, \mathcal{F})$ measures the obstruction to extending local data globally.

**Colouring sheaf $\mathcal{F}_4$:** Define:
- $\mathcal{F}_4(v) = \mathbb{R}^4$ for each vertex (the 4-colour space)
- $\mathcal{F}_4(e) = \{(x, y) \in \mathbb{R}^4 \times \mathbb{R}^4 : x \neq y \text{ on support}\}$ (constraint that adjacent vertices differ)
- Global sections $\Gamma(G, \mathcal{F}_4)$ correspond to proper 4-colourings

**4CT as a vanishing theorem:** If for every planar graph $G$, $H^1(G, \mathcal{F}_4) = 0$ (the obstruction to gluing local colourings into a global one vanishes), then global sections exist — i.e., a proper 4-colouring exists.

**Analogy:** In algebraic geometry, Kodaira vanishing and Serre duality guarantee $H^1 = 0$ under positivity conditions on line bundles. If planarity provides an analogous positivity condition for the colouring sheaf, this would prove 4CT.

---

## 3. Phase Structure

### Phase 1: Computational Foundations (Months 1–4)

#### 1A. Implement Penrose Evaluation

**Goal:** Compute $\text{Pen}(G)$ for all bridgeless planar cubic graphs up to 30 vertices.

**Algorithm:**
1. Generate all bridgeless planar cubic graphs using `plantri` or `minibaum`
2. For each graph, enumerate all edge-3-colourings by backtracking with constraint propagation
3. Record: $\text{Pen}(G)$, the number of valid colourings, structural properties of the graph

**Optimization:** Use the transfer matrix method for strip-like graphs. For general planar graphs, use the tensor network contraction approach (Area 6/11): represent each vertex as a rank-3 tensor $T_{ijk} = |\epsilon_{ijk}|$ and contract using the planar structure.

| $n$ (vertices) | Cubic graphs | Feasibility |
|----------------|-------------|-------------|
| $\leq 20$ | ~thousands | Hours |
| $\leq 26$ | ~millions | Days |
| $\leq 30$ | ~hundreds of millions | Weeks (with tensor networks) |

**Files:** `compute/topology/penrose_eval.py`, `compute/topology/tensor_contract.py`

**Deliverable:** Database of $\text{Pen}(G)$ values. Verify all are positive (= consistency with 4CT).

#### 1B. Analyze 6j-Symbol Structure

**Goal:** Compute and study the $6j$-symbols of $U_q(\mathfrak{sl}_2)$ at the relevant root of unity.

**Compute:**
- The quantum $6j$-symbols for $q = e^{i\pi/3}$ (or $q = e^{i\pi/5}$ for the related Jones polynomial specialization)
- Their signs, magnitudes, and algebraic properties
- Whether they satisfy a **positivity condition** that prevents cancellation in the Penrose sum

**Key question:** Do the $6j$-symbols at the relevant $q$ value have consistent signs (all positive, or sign pattern determined by a simple rule)? If yes, the Penrose evaluation is a sum of non-negative terms — manifestly positive.

**Files:** `compute/topology/quantum_6j.py`

#### 1C. Compute Sheaf Cohomology

**Goal:** Compute $H^0$ and $H^1$ of candidate colouring sheaves for small planar graphs.

**Method:**
1. Define the colouring sheaf $\mathcal{F}_4$ on small planar graphs ($n \leq 14$)
2. Compute the sheaf Laplacian $L_{\mathcal{F}_4}$ (a block matrix where blocks correspond to restriction maps)
3. Compute $\ker(L_{\mathcal{F}_4})$ (global sections = proper 4-colourings) and $H^1$
4. Check: is $H^1 = 0$ for all tested planar graphs?

**Files:** `compute/topology/sheaf_cohomology.py`

**Kill criterion for sheaf approach:** $H^1 \neq 0$ for some planar graph at $k = 4$.

#### 1D. Compute Chromatic Homology

**Goal:** Compute $H^{i,j}(G)$ for small planar graphs and study positivity at $k = 4$.

**Method:**
1. Implement the Helme-Guizon–Rong construction
2. Compute for all planar triangulations on $n \leq 12$ vertices
3. Evaluate the alternating sum at $k = 4$
4. Check: is the sum always positive? Is there a pattern (e.g., concentration in even homological degrees)?

**Files:** `compute/topology/chromatic_homology.py`

---

### Phase 2: Theoretical Analysis (Months 4–12)

#### 2A. Unitarity Argument for Penrose Non-Vanishing

**Goal:** Prove that the unitarity of the modular tensor category implies $\text{Pen}(G) > 0$ for planar $G$.

**Approach:**
1. Express $\text{Pen}(G)$ as an inner product $\langle \psi_G | \psi_G \rangle$ in the TQFT Hilbert space
2. Show that $|\psi_G\rangle \neq 0$ for bridgeless planar cubic $G$:
   - The state $|\psi_G\rangle$ is constructed from the planar diagram of $G$
   - For planar diagrams, the state is non-zero because the category is faithful on planar diagrams (this is related to the fact that the Temperley-Lieb algebra is faithfully represented)
   - The bridge condition ensures no "short circuits" that could zero out the state
3. Conclude: $\text{Pen}(G) = \langle \psi_G | \psi_G \rangle > 0$

**Key obstacle:** Step 2 requires showing that the specific representation of the Temperley-Lieb algebra (or its SO(3) analogue) is faithful for planar diagrams. This is known in many settings but needs to be verified for the specific specialization relevant to 4CT.

#### 2B. Kuperberg Web Basis

**Goal:** Use Kuperberg's rank-2 spider (for $\mathfrak{sl}_3$) to study positivity.

Kuperberg (1996) defined a **web basis** for the space of $\mathfrak{sl}_3$-invariant tensors. This basis consists of planar trivalent graphs with specific boundary conditions. The key property: the web basis is **positive** in a precise sense — the structure constants are non-negative.

**Connection:** The Penrose evaluation of a planar cubic graph can be expressed in terms of the web basis. If the expansion coefficients are non-negative (which follows from the positivity of the web basis), then the evaluation is non-negative.

**Steps:**
1. Express the Penrose evaluation in Kuperberg's web basis
2. Verify that planarity ensures non-negative coefficients
3. Conclude $\text{Pen}(G) \geq 0$
4. Strengthen to $\text{Pen}(G) > 0$ using the bridgeless condition (which prevents cancellation)

#### 2C. Sheaf Vanishing Theorem

**Goal:** Prove $H^1(G, \mathcal{F}_4) = 0$ for planar graphs.

**Approach:** Develop an analogue of the Kodaira vanishing theorem for cellular sheaves on graphs.

**Strategy:**
1. Define a notion of "positivity" for sheaves on graphs, analogous to ampleness for line bundles
2. Show that the colouring sheaf $\mathcal{F}_4$ satisfies this positivity condition on planar graphs
3. Prove the vanishing theorem: positive sheaves on planar graphs have $H^1 = 0$

**Candidate positivity condition:** The sheaf $\mathcal{F}_4$ is "planar-positive" if the restriction maps respect the cyclic ordering at each vertex induced by the planar embedding. This is a condition that uses planarity intrinsically.

**Alternative approach via Mayer-Vietoris:** 
- Decompose the planar graph along a separator (Lipton-Tarjan)
- Show $H^1$ vanishes on each piece (by induction / bounded-treewidth argument)
- Show $H^1$ of the whole graph vanishes by Mayer-Vietoris (if the boundary compatibility condition is satisfied)

#### 2D. Chromatic Homology Positivity

**Goal:** Prove positivity of chromatic homology at $k = 4$ for planar graphs.

**Approach:**
1. Study the categorified deletion-contraction sequence:
$$\cdots \to H^{i,j}(G/e) \to H^{i,j}(G) \to H^{i,j}(G-e) \to \cdots$$
2. Show that for planar graphs, the long exact sequence degenerates at $k = 4$, forcing positivity
3. Use the connection to Khovanov homology (the chromatic polynomial at $k = -1$ relates to the Jones polynomial) to import techniques from knot homology

---

### Phase 3: Synthesis (Months 12–24)

#### 3A. Assemble TQFT Proof

If the unitarity argument (2A) or Kuperberg web basis argument (2B) succeeds:

1. **Reformulate:** 4CT $\Leftrightarrow$ $\text{Pen}(G) > 0$ for bridgeless planar cubic $G$ (Kauffman's theorem)
2. **Express:** $\text{Pen}(G) = \langle \psi_G | \psi_G \rangle$ via TQFT inner product
3. **Non-vanishing:** $|\psi_G\rangle \neq 0$ by faithfulness of the Temperley-Lieb representation on planar diagrams
4. **Positivity:** $\text{Pen}(G) = \|\psi_G\|^2 > 0$ by unitarity

This would be a proof of 4CT using representation theory, quantum topology, and TQFT — entirely different from the discharging/reducibility approach.

#### 3B. Assemble Sheaf Proof

If the vanishing theorem (2C) succeeds:

1. **Define:** The colouring sheaf $\mathcal{F}_4$ on a planar graph $G$
2. **Vanishing:** $H^1(G, \mathcal{F}_4) = 0$ for planar $G$ (the vanishing theorem)
3. **Existence:** $H^0(G, \mathcal{F}_4) = \Gamma(G, \mathcal{F}_4) \neq 0$ (by Euler characteristic argument: $\chi(\mathcal{F}_4) = \dim H^0 - \dim H^1 > 0$ since the Euler characteristic of the colouring sheaf is $P(G, 4)/4! > 0$... this requires careful computation)
4. **Conclusion:** Global sections exist $\Rightarrow$ proper 4-colouring exists

#### 3C. Formalize in Lean 4

Formalize whichever proof materializes. This would require:
- Lean 4 library for modular tensor categories (substantial)
- OR Lean 4 library for cellular sheaves on graphs (more tractable)
- The specific algebraic/categorical arguments of the proof

This is a 6–12 month project in itself, likely post-publication.

---

### Phase 4: Extension (Months 24–36)

#### 4A. Higher-Genus Extension

The TQFT framework naturally extends to graphs on surfaces of higher genus. If the proof works, it might yield:

$$\chi(G) \leq H(g) = \left\lfloor \frac{7 + \sqrt{1 + 48g}}{2} \right\rfloor$$

for graphs embedded on a surface of genus $g$ — a new proof of the Heawood conjecture.

#### 4B. Quantum Chromatic Number

The TQFT/categorical framework connects to the quantum chromatic number $\chi_q(G)$. Results about $\chi_q$ for planar graphs would extend the reach of the proof.

#### 4C. Connections to Physics

The Penrose evaluation has interpretations in:
- Spin foam models (quantum gravity)
- Lattice gauge theory (the Potts model at zero temperature)
- Topological phases of matter

A successful TQFT proof of 4CT would have implications for these areas.

---

## 4. Key Mathematical Objects

### The Penrose Evaluation

```
Cubic planar graph G:

    ●───1───●           Edge labels ∈ {1, 2, 3}
   / \     / \          Vertex constraint: all three labels
  2   3   2   1         must appear at each vertex
 /     \ /     \
●───3───●───2───●       Pen(G) = number of valid labellings

Valid labelling ⟺ proper edge-3-colouring ⟺ 4-face-colouring
```

### TQFT State Space

```
Hilbert space H:

    |ψ_G⟩ = ∑ (amplitudes from 6j-symbols)
              valid
             labellings

    Pen(G) = ⟨ψ_G|ψ_G⟩ ≥ 0  (by unitarity)

    4CT ⟺ |ψ_G⟩ ≠ 0 for bridgeless planar cubic G
    ⟺ faithfulness of TL representation on planar diagrams
```

### Sheaf on a Graph

```
    Vertex stalk:  F(v) = ℝ⁴ (colour space)
    Edge stalk:    F(e) = ℝ⁴ ⊗ ℝ⁴ / Δ (different-colour pairs)
    Restriction:   F(v) → F(e) (compatibility map)

    Global section: σ ∈ Γ(G, F₄)  ⟺  proper 4-colouring

    4CT ⟺ H¹(G, F₄) = 0 for planar G
    (vanishing of obstruction → sections exist)
```

### Chromatic Homology

```
    P(G, k) = ∑ᵢ,ⱼ (-1)ⁱ kʲ dim H^{i,j}(G)

    Categorification:   number → vector space
                        P(G,k) → H^{*,*}(G)

    If H^{i,j}(G) for planar G at k=4 has:
      - concentration in even i  → alternating sum is positive
      - manifestly non-negative  → P(G,4) > 0  ✓
```

---

## 5. Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| 6j-symbols don't have consistent signs | Medium | High | Try web basis approach (2B) independently |
| Faithfulness of TL representation fails at relevant $q$ | Low-Medium | Fatal for 2A | Sheaf approach (2C) is independent |
| $H^1 \neq 0$ for some planar graph | Medium | Fatal for 2C | TQFT approach (2A/2B) is independent |
| Chromatic homology too hard to compute | Medium | Medium | Focus on TQFT or sheaf path |
| No positivity condition found for sheaves | Medium-High | High | Fall back to computational evidence |
| Formalization in Lean 4 infeasible | High (short-term) | Low | Paper proof first; formalize later |
| Entire approach produces beautiful theory but not 4CT | Medium | Medium | Partial results still publishable and valuable |

---

## 6. Success Criteria

| Milestone | Description | Feasibility |
|-----------|-------------|-------------|
| **Bronze** | Compute Pen(G) for all $n \leq 30$, verify positivity | Very High |
| **Silver** | Identify sign structure of 6j-symbols; compute $H^1$ for $n \leq 14$ | High |
| **Gold** | Prove 4CT via TQFT unitarity OR sheaf vanishing | Medium-Low |
| **Platinum** | Extend to Heawood conjecture via TQFT on higher-genus surfaces | Low |

---

## 7. Why This Plan is Worth the Risk

Despite lower near-term feasibility than Plans 1 and 2, this plan has the highest ceiling:

1. **It would explain why.** Plans 1 and 2 produce proofs that four colours suffice but don't reveal *why*. A TQFT proof would show that four colours suffice because the representation theory of SO(3) at a specific root of unity forces non-vanishing — connecting combinatorics to quantum topology.

2. **It generalizes.** The TQFT framework works on any surface, not just the plane. A successful proof would potentially unify the 4CT with the Heawood conjecture.

3. **The reformulation already exists.** Kauffman's theorem is proven. The non-vanishing of the Penrose evaluation for planar graphs is *exactly* the 4CT. No speculative reformulation is needed — only the proof of non-vanishing.

4. **Multiple independent paths.** The TQFT approach (2A), web basis approach (2B), sheaf vanishing (2C), and chromatic homology (2D) are four independent attempts. Any one succeeding proves 4CT.

---

*Graph Colour Project — Plan 3*  
*18 February 2026*

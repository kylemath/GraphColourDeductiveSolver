# Plan 2: Kempe Swap Game + Topological Non-Crossing

**Priority:** High — most promising novel strategy  
**Time Horizon:** 6–18 months  
**Source Strategies:** Strategy 11 (Kempe Swap Game), Strategy 3 (Topological / Jordan Curve)  
**§6 Alignment:** Track A Secondary + Track B Secondary  
**ProofNavigator Tracks:** 1 (Kempe Swap), Foundation F4b (Kempe Non-Crossing)

---

## 1. Central Thesis

The Five Colour Theorem is easy because a single Kempe swap always works at a degree-5 vertex. The Four Colour Theorem is hard because a single swap can fail — two Kempe chains can interfere. But in a planar graph, the Jordan Curve Theorem constrains *how* chains can interfere. This constraint is barely exploited in existing proofs.

**Core question:** Starting from any proper 5-colouring of a planar graph (guaranteed by 5CT), can a sequence of Kempe chain swaps always eliminate one colour?

If yes, this constitutes a constructive proof of 4CT: the Five Colour Theorem provides the starting colouring, and the Kempe swap sequence reduces it. The proof would explain *why* four colours suffice — because the topological structure of planar embeddings prevents Kempe chains from creating irresolvable conflicts.

---

## 2. Mathematical Foundation

### 2.1 Kempe Chains

Given a proper $k$-colouring $c: V \to \{1, \ldots, k\}$ of a graph $G$ and a pair of colours $(a, b)$, the **$(a,b)$-Kempe chain** containing vertex $v$ is the maximal connected subgraph of $G$ induced by vertices coloured $a$ or $b$ that contains $v$.

**Kempe swap:** Swapping the colours $a \leftrightarrow b$ on an $(a,b)$-Kempe chain preserves the proper colouring. This is because the chain is an induced bichromatic subgraph — no edge connects a swapped vertex to an unswapped vertex of the same new colour.

### 2.2 Why 5CT Works (One Swap Suffices)

Let $G$ be a planar graph, $v$ a vertex of degree $\leq 5$ (exists by Euler). Remove $v$, inductively 5-colour $G - v$. If $\deg(v) \leq 4$, at most 4 colours appear on $v$'s neighbours — assign the 5th. If $\deg(v) = 5$ with neighbours $w_1, \ldots, w_5$ coloured $c_1, \ldots, c_5$:

- If two neighbours share a colour, a colour is free for $v$.
- Otherwise all 5 colours appear. Consider the $(c_1, c_3)$-Kempe chain from $w_1$. If it doesn't reach $w_3$, swap it — now $c_1$ is free for $v$. If it does reach $w_3$, the $(c_2, c_4)$-chain from $w_2$ cannot reach $w_4$ (by planarity — the $(c_1,c_3)$-chain separates them). Swap it; $c_2$ is free.

**The key:** At degree 5 with 5 colours, the Jordan Curve Theorem guarantees at least one swap succeeds.

### 2.3 Why 4CT is Hard (The Interference Problem)

With 4 colours and $\deg(v) = 5$, at least two neighbours share a colour. Say $c(w_1) = c(w_3) = a$. We need to recolour so that a colour becomes free for $v$. Attempt: swap the $(a, b)$-chain from $w_1$ to change $w_1$'s colour. But this swap might affect $w_3$ (if they're on the same chain) or create conflicts elsewhere that propagate.

**The 4-colour interference:** Swapping one chain can change the landscape for other swaps. In a 5-colour setting, we always had a "spare" colour pair to work with. With 4 colours, every swap is constrained — and chains can interact in complex ways.

### 2.4 The Non-Crossing Property

**Theorem (Jordan Curve Theorem consequence):** In a planar graph $G$ with a planar embedding, let $c$ be a proper colouring. For two distinct colour pairs $(a,b)$ and $(c,d)$ with $\{a,b\} \cap \{c,d\} = \emptyset$, the $(a,b)$-chains and $(c,d)$-chains cannot cross.

More precisely: an $(a,b)$-chain $K_{ab}$ and a $(c,d)$-chain $K_{cd}$ in a planar graph form paths/cycles in the plane. By the Jordan Curve Theorem, if $K_{ab}$ forms a closed curve (or a path connecting two points on the outer face boundary), it divides the plane into regions. Every $(c,d)$-chain is entirely contained within one region.

**Critical at degree-5 vertices:** If $v$ has degree 5 with neighbours $w_1, \ldots, w_5$ in cyclic planar order, and the $(a,b)$-chain from $w_1$ reaches $w_3$, then $w_2$ is trapped on one side and $w_4, w_5$ on the other. This severely constrains which recolouring sequences can occur.

### 2.5 Kempe Equivalence and Reconfiguration

Two proper $k$-colourings of $G$ are **Kempe equivalent** if one can be obtained from the other by a sequence of Kempe chain swaps. The set of all proper $k$-colourings partitions into **Kempe equivalence classes**.

**Known results:**
- Meyniel (1978): For $k \geq \chi(G) + 1$, all $k$-colourings are Kempe equivalent
- Las Vergnas & Meyniel (1981): All proper 5-colourings of a planar graph are Kempe equivalent (using 4CT)
- **Open question:** Are all proper 5-colourings of a planar graph Kempe equivalent to some proper 4-colouring? This is equivalent to 4CT.

**Fisk (1977):** The 4-colourings of a planar triangulation modulo Kempe swaps of $(a,b)$-chains form a group related to $H_1(T; \mathbb{Z}_2)$ (first homology with $\mathbb{Z}_2$ coefficients). This algebraic structure constrains the reconfiguration landscape.

---

## 3. Phase Structure

### Phase 1: Computational Verification (Months 1–4)

#### 1A. Enumerate Planar Triangulations

**Goal:** Build a database of all planar triangulations for small vertex counts.

**Specification:**
- Use `plantri` (Brinkmann & McKay) to generate all planar triangulations up to isomorphism
- Vertex counts: $n = 4, 5, 6, \ldots, 20$ (and beyond if feasible)
- Store as adjacency lists with canonical planar embeddings

| $n$ | Triangulations | Feasibility |
|-----|---------------|-------------|
| $\leq 12$ | ~thousands | Minutes |
| $\leq 15$ | ~hundreds of thousands | Hours |
| $\leq 18$ | ~tens of millions | Days |
| $\leq 20$ | ~billions | Needs HPC |

**Files:** `compute/kempe/triangulation_db.py`

#### 1B. 5→4 Reduction Search

**Goal:** For every proper 5-colouring of every planar triangulation on $\leq 15$ vertices, verify that a sequence of Kempe swaps reduces it to a 4-colouring.

**Algorithm:**
1. For each triangulation $T$:
   a. Enumerate all proper 5-colourings (or sample uniformly if count is too large)
   b. For each 5-colouring $c$:
      - BFS/DFS on the Kempe reconfiguration graph from $c$
      - Check if any reachable colouring uses only 4 colours
      - Record: number of swaps needed, which colour was eliminated, which swap sequence worked
2. If any 5-colouring cannot be reduced: **COUNTEREXAMPLE FOUND** (kills the strategy but would be a significant negative result)

**Parallelization:** Each triangulation is independent. Each 5-colouring is independent within BFS.

**Files:** `compute/kempe/reduction_search.py`

**Milestones:**
| Month | Verified up to $n$ | Significance |
|-------|-------------------|--------------|
| Month 1 | $n \leq 12$ | Validates approach |
| Month 2 | $n \leq 15$ | Substantial evidence |
| Month 3 | $n \leq 18$ | Strong evidence (may need HPC) |
| Month 4 | $n \leq 20$ | Very strong evidence |

**Kill criterion:** Counterexample found (5-colouring of a planar graph that cannot be Kempe-reduced to 4 colours).

#### 1C. Reconfiguration Graph Analysis

**Goal:** Study the structure of the Kempe reconfiguration graph $\mathcal{R}(T, k)$ for small triangulations.

**Compute for each $T$ with $n \leq 14$:**
- $|\mathcal{R}(T, 4)|$ — number of proper 4-colourings
- $|\mathcal{R}(T, 5)|$ — number of proper 5-colourings
- Diameter of $\mathcal{R}(T, 4)$ — maximum Kempe distance between 4-colourings
- Connectivity of $\mathcal{R}(T, 4)$ — is it connected? (Las Vergnas-Meyniel for $k = 5$; open for $k = 4$)
- Spectral gap of the Kempe Markov chain — how fast does random walking on $\mathcal{R}(T, 4)$ mix?
- Number of "frozen" 4-colourings — colourings where no single Kempe swap changes the colour count

**Files:** `compute/kempe/reconfiguration_graph.py`

---

### Phase 2: Topological Analysis (Months 3–8)

#### 2A. Formalize Kempe Non-Crossing

**Goal:** Prove precise theorems about how planarity constrains Kempe chain interactions.

**Target theorems:**

> **Theorem A (Non-Interleaving):** Let $T$ be a planar triangulation with proper 4-colouring $c$, and $v$ a vertex of degree 5 with neighbours $w_1, \ldots, w_5$ in cyclic planar order. Let $K_{ab}$ be the $(a,b)$-Kempe chain from $w_i$ and $K_{cd}$ be the $(c,d)$-Kempe chain from $w_j$ with $\{a,b\} \cap \{c,d\} = \emptyset$. If $K_{ab}$ connects $w_i$ to $w_k$ (going around $v$), then $K_{cd}$ connects $w_j$ to a vertex in the same "arc" between $w_i$ and $w_k$ (not crossing $K_{ab}$).

> **Theorem B (Confinement):** Under the same setup, if $K_{ab}$ separates $w_j$ from $w_\ell$, then no sequence of Kempe swaps on chains not involving colours $a$ or $b$ can connect $w_j$ and $w_\ell$.

**Approach:** Paper math first, then formalize in Lean 4.

**Files:** `lean4/FourColor/Foundation/F4b_KempeNonCrossing.lean`

#### 2B. Classify Degree-5 Configurations Under Non-Crossing

**Goal:** Enumerate all topologically distinct Kempe chain configurations at a degree-5 vertex, using the non-crossing constraint to bound the cases.

**Key insight:** Without the non-crossing constraint, the number of possible Kempe chain interaction patterns at a degree-5 vertex is large. With it, the topology of the planar embedding forces chains into a small number of patterns. If this number is small enough (say $\leq 20$), each pattern can be analyzed individually.

**Method:**
1. List all possible colour assignments to 5 neighbours (up to colour permutation): there are $\binom{4}{1} \cdot S(5, k)$ cases for $k = 2, 3, 4$ colours among the 5 neighbours
2. For each colour assignment, enumerate the topologically distinct ways Kempe chains can connect the neighbours (constrained by non-crossing)
3. For each pattern, determine whether a Kempe swap sequence exists that frees a colour for the central vertex

**Deliverable:** A complete case analysis of degree-5 Kempe configurations in planar graphs.

#### 2C. Extend to Degree-6 and Beyond

**Goal:** Apply the non-crossing analysis to higher-degree vertices.

The discharging argument shows that positive-charge vertices have degree $\leq 5$ (or are adjacent to specific configurations). But the Kempe swap game must handle recolouring cascades that propagate through higher-degree vertices.

**Question:** Does the non-crossing constraint propagate through chains, limiting cascade length?

---

### Phase 3: Structural Lemmas (Months 6–12)

#### 3A. Colour Elimination Strategy

**Goal:** Develop a systematic strategy for eliminating one colour from a 5-colouring.

**Approach:**
Given a proper 5-colouring $c$ of a planar graph $G$, choose the least-used colour (say colour 5, used by $k$ vertices). For each vertex $v$ with $c(v) = 5$:
1. Examine $v$'s neighbourhood
2. Apply Kempe swaps to free a colour from $\{1, 2, 3, 4\}$ for $v$
3. The non-crossing constraint limits which swaps can fail

**Key lemma to prove:**

> **Colour Elimination Lemma:** Let $G$ be a planar triangulation with proper 5-colouring $c$, and let $V_5 = \{v : c(v) = 5\}$. There exists an ordering $v_1, \ldots, v_{|V_5|}$ such that for each $v_i$, a Kempe swap sequence (involving only vertices in $V(G) \setminus \{v_1, \ldots, v_{i-1}\}$) recolours $v_i$ to a colour in $\{1,2,3,4\}$.

If true, this gives a constructive 4-colouring algorithm and proves 4CT.

#### 3B. Fisk Homology Analysis

**Goal:** Use Fisk's algebraic structure to constrain Kempe equivalence classes.

Fisk showed that for a planar triangulation $T$, the 4-colourings modulo $(a,b)$-Kempe swaps form a group isomorphic to $\mathbb{Z}_2^g$ where $g$ depends on the graph's structure. This means:

- The reconfiguration graph has at most $2^g$ connected components (for any fixed colour pair)
- Swapping different colour pairs generates the full reconfiguration — connectivity of $\mathcal{R}(T, 4)$ reduces to whether different colour pairs generate the full group
- A 5-colouring is reducible to 4 colours iff its "Fisk class" intersects the set of 4-colourings

**Files:** `compute/kempe/fisk_homology.py`

#### 3C. Formalize in Lean 4

**Goal:** Machine-verify the structural lemmas.

Build on Phase 1 infrastructure (PlanarGraph, KempeChain). Formalize:
- Theorem A (non-interleaving)
- Theorem B (confinement)
- The degree-5 case analysis from 2B
- The colour elimination lemma from 3A (if proved)

---

### Phase 4: Synthesis (Months 12–18)

#### 4A. Assemble Proof

If the colour elimination lemma is proved:
1. **5CT provides the starting 5-colouring** (proved in Foundation)
2. **Kempe non-crossing constrains interactions** (proved in Phase 2A)
3. **Case analysis handles each degree-5 pattern** (proved in Phase 2B)
4. **Colour elimination strategy reduces to 4 colours** (proved in Phase 3A)
5. Result: a constructive proof of 4CT via Kempe chain reconfiguration

#### 4B. Fallback: Partial Results

Even if the full proof doesn't materialize, valuable partial results include:
- The non-crossing theorems (new, publishable)
- Computational verification for $n \leq 20$ (strong evidence)
- The Fisk homology analysis (connects 4CT to algebraic topology)
- The degree-5 case classification (feeds into Plan 1's reducibility proofs)

---

## 4. Key Mathematical Objects

### Kempe Chain at Degree-5 Vertex

```
                w₁ (colour a)
               / |
              /  |
    w₅ (d)--v---w₂ (colour b)
              \  |
               \ |
                w₃ (colour a)——w₄ (colour c)

    (a,b)-chain from w₁: might reach w₂ or w₃
    If it reaches w₃ (encircling w₂), then by JCT:
    the (b,c)-chain from w₂ cannot reach w₄
    → w₂ can be recoloured, freeing b for v
```

### The Non-Crossing Constraint

```
    Planar embedding around degree-5 vertex v:

         w₁ ═══(a,c)═══ w₃        (a,c)-chain connects w₁ to w₃
          |               |
          |    w₂         |        w₂ is CONFINED to the interior
          |  (trapped)    |        of the region bounded by the chain
          |               |
         w₅              w₄

    → Any (b,d)-chain from w₂ stays inside this region
    → Limits which vertices w₂'s Kempe chain can reach
```

### Reconfiguration Graph

```
    R(T, 4):  Each node is a proper 4-colouring of T
              Edges connect colourings differing by one Kempe swap

    Question: Is R(T, 4) always connected for planar T?
              If yes → all 5-colourings can reach a 4-colouring
              
    R(T, 5):  Known connected for planar T (Las Vergnas-Meyniel)

    5-colouring c ——→ c' ——→ ... ——→ c* (uses only 4 colours)
                Kempe    Kempe         ↑
                swaps    swaps         This is the 4CT!
```

---

## 5. Risk Matrix

| Risk | Probability | Impact | Mitigation |
|------|------------|--------|------------|
| Counterexample at $n \leq 15$ | Very Low | Fatal | Would disprove the strategy; significant negative result worth publishing |
| Counterexample at $n > 20$ | Low | Fatal | Extended computation; if found, analyze structure |
| Non-crossing doesn't suffice | Medium | High | Partial results still valuable; feeds Plan 1 |
| Colour elimination ordering fails | Medium | High | Explore alternative orderings; may need randomization |
| Fisk structure too complex | Medium | Medium | Computational approach (Phase 1) still provides evidence |
| Lean 4 formalization stalls | Medium | Low | Paper proofs are valid without formalization |

---

## 6. Success Criteria

| Milestone | Description | Feasibility |
|-----------|-------------|-------------|
| **Bronze** | Verify 5→4 reduction for all $n \leq 15$ | Very High |
| **Silver** | Prove Kempe non-crossing theorems (A and B) | High |
| **Gold** | Complete degree-5 case classification | Medium-High |
| **Platinum** | Prove colour elimination lemma → 4CT | Medium |

---

## 7. Why This Plan Addresses the Core Difficulty

The 4CT is hard because of *one specific failure mode*: at a degree-5 vertex, two Kempe chain swaps can interfere, and it's unclear whether a repair sequence always exists. Every existing proof handles this by exhaustive case analysis (633+ configurations).

This plan attacks the failure mode directly:
- **Non-crossing** limits the ways chains can interfere (Phase 2A)
- **Case classification** enumerates the remaining possibilities (Phase 2B)
- **Colour elimination** provides a constructive resolution strategy (Phase 3A)

If successful, the proof would not just verify 4CT but *explain* it: four colours suffice because the topology of planar embeddings prevents Kempe chains from creating unresolvable conflicts.

---

*Graph Colour Project — Plan 2*  
*18 February 2026*

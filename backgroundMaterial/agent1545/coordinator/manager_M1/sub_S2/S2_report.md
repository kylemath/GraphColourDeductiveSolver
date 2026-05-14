# Sub-task S2 Report: Formalization of the Merge-Tolerant Lifting Lemma

**Agent:** 1545-M1-S2  
**Date:** 20 February 2026  
**Task:** Formalize the Merge-Tolerant Lifting Lemma — whether S1 succeeds or fails, state precisely what the lemma requires and analyze its provability.

---

## S1 SUCCEEDED: All 48 merges are harmless. We formalize the positive result.

---

## 1. Lemma Statement

### 1.1 Merge-Tolerant Lifting Lemma (Computational Version)

**Lemma (MTL-Comp).** *Let $G$ be a planar triangulation on $n \leq 9$ vertices, $v$ a vertex with $c(v) = 5$ and $\deg(v) \leq 5$. Let $P = (c_0, c_1, \ldots, c_d)$ be any BFS-optimal path in $\mathcal{R}(G-v, 5)$ from $c_0 = c|_{G-v}$ to a 4-colouring $c_d$. Then there exists a colour $c^* \in \{1,2,3,4\}$ such that $c^* \notin \{c_d(u) : u \in N_G(v)\}$.*

**Status:** Verified computationally for all $n \leq 9$ (163,584 merge-prone colourings, 48 counterexamples to safe-path avoidance, 48/48 harmless).

### 1.2 Merge-Tolerant Lifting Lemma (Conjectured General Form)

**Conjecture (MTL-Gen).** *Let $G$ be a planar triangulation, $v$ a vertex with $c(v) = 5$ and $\deg(v) \leq 5$. For any proper 5-colouring $c$ of $G$, there exists a path $P$ in $\mathcal{R}(G-v, 5)$ from $c|_{G-v}$ to a 4-colouring $c^*$ of $G-v$ such that $v$ has a free colour: $\{1,2,3,4\} \setminus \{c^*(u) : u \in N_G(v)\} \neq \emptyset$.*

Note: the conjecture does not require the path to be BFS-optimal. ANY path to an extensible 4-colouring suffices.

### 1.3 Constructive 4CT via MTL

**Theorem (assuming MTL-Gen).** *Every planar graph is 4-colourable.*

*Proof sketch.* By induction on $|V(G)|$. The base case $|V| \leq 4$ is trivial. For the inductive step:

1. By the 5-colour theorem, $G$ has a proper 5-colouring $c$.
2. Choose $v$ with $\deg(v) \leq 5$ (exists by Euler's formula for planar graphs).
3. If $c(v) \neq 5$: permute colour names so $c(v) = 5$.
4. Consider $G - v$ with colouring $c|_{G-v}$ (a proper 5-colouring).
5. By MTL-Gen, there exists a path in $\mathcal{R}(G-v, 5)$ to a 4-colouring $c^*$ where $v$ has a free colour.
6. Extend $c^*$ to $G$ by assigning $v$ the free colour.

This produces a proper 4-colouring of $G$. $\square$

---

## 2. Analysis of WHY Merges Are Harmless

### 2.1 Degree-4: Pigeonhole-Plus Argument

**Proposition.** *If $\deg(v) = 4$ and $c(v) = 5$, then for any 4-colouring $c^*$ of $G - v$, the vertex $v$ has a free colour unless all 4 colours from $\{1,2,3,4\}$ appear on $v$'s 4 neighbours.*

This is not automatically guaranteed — 4 neighbours CAN use 4 distinct colours. However, the counterexample structure provides an additional constraint:

**Key insight for deg-4 CEs:** In all 24 T_9_35 counterexamples, the initial colouring has a repeated colour on $v$'s neighbours: the pattern is $(a, b, c, c)$ where $c$ appears on two non-adjacent neighbours. The BFS path transforms this colouring, but the adjacency structure in $G - v$ constrains how many distinct colours can appear on $v$'s neighbours in the final 4-colouring.

**Computational finding:** In the final 4-colouring, $v$'s 4 neighbours always use at most 3 distinct colours from $\{1,2,3,4\}$. One neighbour has colour 5 in the intermediate steps, and when the path reaches a 4-colouring, the repeated-colour structure is preserved or transformed into another pattern with at most 3 distinct colours.

### 2.2 Degree-5: Non-Trivial But Holds

**For $\deg(v) = 5$:** Five neighbours can in principle use all 4 colours from $\{1,2,3,4\}$. By pigeonhole, at least 2 of 5 neighbours share a colour, but that still allows 4 distinct colours.

**Computational finding:** For the T_9_25 counterexamples ($v = 3$, $\deg = 5$):
- Initial neighbour colours: always 4 distinct colours (pattern $(a, b, c, d, d)$ — one pair)
- After step 0 (the merge-prone swap): 5 distinct colours appear on neighbours — **temporarily no free colour**
- After step 1: one of the "5" colours is removed, leaving exactly 3 or 4 colours from $\{1,2,3,4\}$ on neighbours — **free colour restored**
- Final: exactly 1 free colour in every case

The mechanism is as follows:
1. The merge-prone $(a,5)$-swap converts some vertices from colour $a \to 5$ and $5 \to a$
2. This temporarily places colour 5 on a neighbour of $v$ that previously had a colour from $\{1,2,3,4\}$
3. But it also converts some colour-5 vertices to colour $a$, meaning fewer vertices use colour 5
4. The second BFS step swaps a different $(b,5)$-chain or $(b,c)$-chain, further reducing colour 5 usage
5. The terminal 4-colouring avoids colour 5 entirely, and the rearrangement always leaves a gap

**Why this works structurally:** The BFS path from a 5-colouring to a 4-colouring progressively eliminates colour 5 from $G - v$. Each swap either converts a colour-5 vertex to another colour or rearranges non-5 colours. The merge-prone swap may temporarily worsen $v$'s neighbourhood, but the subsequent colour-5-eliminating steps remove colour 5 from enough vertices that a gap appears at $v$.

### 2.3 Connection to Never-Revert Property

The constructive proof framework includes a "Never-Revert" lemma: once a vertex loses colour 5, it should not regain it. In the merge-tolerant setting, this property is RELAXED — we allow temporary reversions (a neighbour of $v$ may gain colour 5 temporarily). What matters is only the FINAL state.

This relaxation is crucial: the original BFS Avoidance conjecture required the lift from $G - v$ to $G$ to preserve chain structure at EVERY step. Merge-tolerant lifting only requires the ENDPOINT to be compatible. This is a dramatically weaker requirement.

---

## 3. Proof Strategy for General MTL

### 3.1 Degree $\leq 4$: Should Be Provable

**Approach:** For $\deg(v) \leq 4$, we need to show that the BFS terminal 4-colouring of $G - v$ does not place all 4 distinct colours on $v$'s $\leq 4$ neighbours.

The link graph $L(v)$ (subgraph of $G - v$ induced on $N(v)$) is a cycle $C_k$ for $k = \deg(v)$ in a triangulation. A proper 4-colouring of $G - v$ restricts to a proper colouring of $L(v) \cong C_k$.

For $k = 3$: $C_3$ requires 3 colours, so at most 3 distinct colours appear. **Free colour guaranteed.**

For $k = 4$: $C_4$ is bipartite and can be properly 2-coloured, but in context may use up to 4 colours. The question is whether the BFS from the specific starting colouring always reaches a 4-colouring where $C_4$ uses $\leq 3$ colours. The starting colouring has a repeated colour on the cycle, and the BFS appears to preserve this property.

**Feasibility: Medium-High.** The cycle structure provides strong constraints; a case analysis on $C_4$ colourings reachable by the BFS should suffice.

### 3.2 Degree 5: Harder

For $\deg(v) = 5$: $L(v) \cong C_5$. A proper colouring of $C_5$ requires at least 3 colours. It can use up to 4 colours from $\{1,2,3,4\}$. If it uses all 4, $v$ has no free colour.

The question becomes: does the BFS from the specific starting colouring always reach a 4-colouring where $C_5$ uses $\leq 3$ colours?

**The computational evidence says yes for $n \leq 9$.** But this requires a structural proof. Potential approaches:

1. **Reachability argument:** Show that from any extensible-start 5-colouring (one where $v$'s neighbours don't all have distinct colours), the BFS always reaches an extensible 4-colouring. This requires understanding how BFS paths transform the neighbourhood of $v$.

2. **Counting argument:** Show that extensible 4-colourings vastly outnumber non-extensible ones in the reconfiguration graph, so BFS "almost surely" reaches one.

3. **Topological argument:** The planarity constraint restricts chain topology enough that the merge cannot produce all 4 colours on $C_5$.

**Feasibility: Medium.** The computational evidence is overwhelming (100% at $n \leq 9$), but a proof requires new ideas.

### 3.3 Alternative: Choose the Right 4-Colouring

Instead of proving BFS always reaches an extensible 4-colouring, prove that SOME reachable 4-colouring is extensible:

**Weaker Lemma (Reachable Extensible).** *From any 5-colouring of $G - v$ (restricted from a 5-colouring of $G$ with $c(v) = 5$), some 4-colouring reachable in $\mathcal{R}(G-v, 5)$ is extensible to $v$.*

This was also verified computationally (the "exhaustive check" in S1's code). All 48 counterexamples have reachable extensible 4-colourings.

**Advantage:** This lemma doesn't require BFS-optimality. Any path works.

**Feasibility: Medium-High.** Easier than proving BFS-specific claims.

---

## 4. What Could Go Wrong at Larger $n$?

### 4.1 Degree-5 Saturation

At $n = 9$, non-extensible 4-colourings exist:
- T_9_25: 48/720 (6.7%) of 4-colourings of $G-v$ are non-extensible
- T_9_35: 24/600 (4.0%)

At larger $n$, these fractions could grow. If they grow large enough, BFS from certain starting colourings might only reach non-extensible 4-colourings.

### 4.2 Chain Complexity

At larger $n$, Kempe chains can be much larger and more entangled. A merge-prone swap might produce a cascade of merges that propagates far from $v$'s neighbourhood, eventually saturating all 4 colours on $v$'s neighbours.

### 4.3 Reconfiguration Graph Structure

The reconfiguration graph at larger $n$ has more complex topology. BFS paths might be forced through bottlenecks that all lead to non-extensible 4-colourings.

### 4.4 Mitigation

Even if MTL fails at larger $n$, the vertex-selection strategy (S3) provides a fallback: choose $v$ such that merge-tolerant lifting works. The combined approach (choose $v$ well, then use merge-tolerant lifting) has a strictly larger chance of succeeding.

---

## 5. Formal Statement for Future Proof

**Merge-Tolerant Lifting Lemma (Proof Target):**

*Let $G$ be a planar triangulation and $v$ a vertex of $G$ with $\deg(v) \leq 5$. Let $c$ be a proper 5-colouring of $G$ with $c(v) = 5$. Then there exists a proper 4-colouring $c^*$ of $G - v$ such that:*

1. *$c^*$ is reachable from $c|_{G-v}$ by a sequence of Kempe swaps in $G - v$ (i.e., $c^* \in \mathcal{R}(G-v, 5)[c|_{G-v}]$)*
2. *$\{1,2,3,4\} \setminus \{c^*(u) : u \in N_G(v)\} \neq \emptyset$*

*In particular, $c^*$ extends to a proper 4-colouring of $G$ by assigning $v$ any colour in $\{1,2,3,4\} \setminus \{c^*(u) : u \in N_G(v)\}$.*

**Computationally verified for all planar triangulations on $n \leq 9$ vertices.**

---

## 6. Assessment

**Craftsperson:** The lemma is precisely stated and the proof strategy is clear. The degree-4 case is nearly provable today (cycle colouring argument + BFS reachability). The degree-5 case is harder but the computational evidence is overwhelming.

**Skeptic:** We have a lemma that is verified at $n \leq 9$. This is 50 triangulations, 163,584 merge-prone colourings. It's strong evidence but not a proof. The key risk: at $n = 9$, the graphs are small enough that BFS explores the entire reconfiguration graph quickly, so "most" 4-colourings are reachable. At $n = 50$ or $n = 100$, the reconfiguration graph is vast and BFS may only reach a small fraction. Whether that fraction includes extensible 4-colourings is not guaranteed. We need either a proof or computation at larger $n$.

**Mover:** The lemma is stated, the evidence is strong, and the proof strategy is laid out. The degree-4 case should be attacked immediately. The degree-5 case requires either extending computation to $n = 10$–$12$ (feasible with the existing code, maybe $\sim$1h) or a structural insight. Ship this report and move to the general argument.

---

*Agent 1545-M1-S2 — Merge-Tolerant Lifting Lemma Formalization*  
*20 February 2026*

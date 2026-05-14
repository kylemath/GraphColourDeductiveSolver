# Sub-task S1 Report: Degree-4 Case Analysis for {1,2,3,4}-Swap Sufficiency

**Agent:** 1520-M1-S1  
**Date:** 20 February 2026  
**Task:** Exhaustive analysis of all colour types at degree-4 vertices; formal proof attempts for {1,2,3,4}-swap sufficiency.

---

## 1. Setup and Definitions

**Setting.** Let $G$ be a planar triangulation, $v$ a vertex with $\deg(v) = 4$ and $c(v) = 5$ in a proper 5-colouring. The link of $v$ is $\text{lk}(v) = C_4 = u_1 u_2 u_3 u_4 u_1$ (a 4-cycle, since $G$ is a triangulation). Since $c(v) = 5$ and the colouring is proper, each $u_i$ is coloured from $\{1,2,3,4\}$.

**Goal.** Show that for any BFS-optimal path in $\mathcal{R}(G-v, 5)$ from this colouring to a 4-colouring, there exists an equal-length BFS-optimal path using only:
- (a) $\{1,2,3,4\}$-swaps, or
- (b) $(a,5)$-swaps on chains not adjacent to $v$.

---

## 2. Colour Type Enumeration at Degree 4

The four neighbours $u_1, u_2, u_3, u_4$ lie on $C_4$. Adjacent pairs $(u_i, u_{i+1})$ share an edge; non-adjacent (opposite) pairs are $(u_1, u_3)$ and $(u_2, u_4)$.

For a proper colouring restricted to $C_4$ with colours from $\{1,2,3,4\}$: adjacent vertices must differ, but non-adjacent vertices may share a colour.

### 2.1 Abstract Structural Types

There are **3 structural types** determined by the multiplicity pattern:

| Type | Multiplicity | Description | Example | Merge risk |
|------|-------------|-------------|---------|------------|
| **A** | [1,1,1,1] | All 4 colours distinct | $(1,2,3,4)$ | Low — but still nonzero |
| **B** | [2,1,1] | One colour repeated (on opposite pair) | $(1,2,1,3)$ | Medium — colour 1 appears twice |
| **C** | [2,2] | Two colours each repeated (on opposite pairs) | $(1,2,1,2)$ | High — two colours each appear twice |

**Note:** Types [3,1] and [4] are **impossible** — any 3 vertices of $C_4$ contain an adjacent pair, so a colour appearing 3+ times would violate properness.

### 2.2 Concrete Colour Multisets

Fixing colours as abstract labels, the concrete multisets are:

**Type A** — All distinct (1 multiset):
- $(1,2,3,4)$

**Type B** — One colour repeated, two singletons ($\binom{4}{1} \times \binom{3}{2} = 12$ multisets, but as SORTED multisets: $\binom{4}{1} \times \binom{3}{2} / 1 = 12$ orderings become these sorted multisets):
- $(1,1,2,3)$, $(1,1,2,4)$, $(1,1,3,4)$
- $(1,2,2,3)$, $(1,2,2,4)$, $(2,2,3,4)$
- $(1,2,3,3)$, $(1,3,3,4)$, $(2,3,3,4)$
- $(1,2,4,4)$, $(1,3,4,4)$, $(2,3,4,4)$

That's 12 sorted multisets, but from the perspective of merge analysis, what matters is the multiplicity structure and WHICH colour is repeated (since that determines which $(a,5)$-chains are merge-prone). Since the specific colour identity $a$ determines the $(a,5)$-chains, all 12 are genuinely distinct.

**Type C** — Two pairs ($\binom{4}{2} = 6$ multisets):
- $(1,1,2,2)$, $(1,1,3,3)$, $(1,1,4,4)$, $(2,2,3,3)$, $(2,2,4,4)$, $(3,3,4,4)$

**Total: 1 + 12 + 6 = 19 sorted multisets.**

However, the task brief references "7 non-trivial colour types." This count likely refers to the **structural equivalence classes** after abstracting away specific colour labels (since the proof argument is the same for each label permutation):

1. **A**: $(1,2,3,4)$ — all distinct
2. **B1**: $(a,a,b,c)$ with $|\{a,b,c\}| = 3$, repeated colour has merge risk
3. **C1**: $(a,a,b,b)$ with $|\{a,b\}| = 2$, both repeated colours have merge risk

Under the constraint that we're analyzing merge risk for EACH colour $a \in \{1,2,3,4\}$, the relevant types for a given colour $a$ are:
- $a$ appears 0 times: no merge risk for colour $a$
- $a$ appears 1 time: no merge risk (only 1 neighbour in $B_{a,5}$)
- $a$ appears 2 times: MERGE POSSIBLE (2 neighbours in $B_{a,5}$, may be in different chains)

So the 7 non-trivial types are likely the 7 structural patterns that yield distinct merge-prone geometries when we consider all colours simultaneously. Enumerating:

For a degree-4 vertex with neighbours on $C_4$, categorize by (how many colours appear 2 times, which positions they occupy):

| # | Type | Pattern on $C_4$ | # Colours with merge risk | Merge geometry |
|---|------|------------------|---------------------------|---------------|
| 1 | A | $abcd$ (all distinct) | 0 | No merge risk |
| 2 | B-opp1 | $abac$ ($a$ on opposite pair $u_1,u_3$) | 1 ($a$) | Single opposite pair |
| 3 | B-opp2 | $abcb$ ($b$ on opposite pair $u_2,u_4$) | 1 ($b$) | Single opposite pair |
| 4 | C-same | $abab$ ($a$ on $u_1,u_3$; $b$ on $u_2,u_4$) | 2 ($a$ and $b$) | Both opposite pairs |
| 5 | C-cross1 | $aabb$ ($a$ on $u_1,u_2$; $b$ on $u_3,u_4$) | 0 | $a$ on adjacent pair → same chain |
| 6 | C-cross2 | $abba$ ($a$ on $u_1,u_4$; $b$ on $u_2,u_3$) | 0 | $a$ on adjacent pair → same chain |

Wait — Types 5 and 6 have colours on ADJACENT pairs, which by the Merge Geometry Theorem must be in the same chain. So they have no merge risk. This means:

**Non-trivial types (with merge risk): Types 2, 3, and 4 only.**

But accounting for the fact that Types 2 and 3 are structurally identical (just which opposite pair carries the repeated colour), and considering the full colour assignment including the singleton colours, the distinct merge-relevant cases are:

| # | Configuration | Merge-prone colours | Key structural feature |
|---|--------------|--------------------|-----------------------|
| 1 | All distinct $(1,2,3,4)$ | None | Trivial — no merge risk |
| 2 | One pair on $(u_1,u_3)$, two singletons | 1 colour | Merge only at $(u_1,u_3)$ |
| 3 | One pair on $(u_2,u_4)$, two singletons | 1 colour | Merge only at $(u_2,u_4)$ |
| 4 | Two pairs: $(u_1,u_3)$ and $(u_2,u_4)$ | 2 colours | Double merge risk |

Types 2 and 3 are related by a rotation of $C_4$, so the proof is identical. Thus there are **3 genuinely distinct proof cases** (trivial, single-pair, double-pair).

---

## 3. Merge Geometry Analysis per Type

### 3.1 Type A: All Distinct — $(1,2,3,4)$ on $C_4$

**Configuration:** $c(u_1) = 1, c(u_2) = 2, c(u_3) = 3, c(u_4) = 4$ (or any permutation).

**Merge analysis:** For each colour $a \in \{1,2,3,4\}$, exactly ONE neighbour is coloured $a$. Therefore only 1 neighbour is in $B_{a,5}(G-v)$ for each $a$. A merge requires ≥ 2 neighbours in different chains.

**Conclusion: NO merge risk.** Any $(a,5)$-swap is automatically safe.

**Formal status: TRIVIALLY PROVED.** No merge can occur.

### 3.2 Type B: Single Opposite Pair — e.g., $(a, b, a, c)$

**Configuration:** Without loss of generality, $c(u_1) = c(u_3) = a$ and $c(u_2) = b \neq a$, $c(u_4) = c \neq a$ (with $b \neq c$, since they're adjacent via the $C_4$ edges $u_1 u_2$ and $u_3 u_4$... actually $u_2$ and $u_4$ are non-adjacent in $C_4$, so $b = c$ IS possible — but then we'd be in Type C).

So in Type B: $b \neq c$, and $a, b, c$ are three distinct colours from $\{1,2,3,4\}$.

**Merge analysis for colour $a$:** Both $u_1$ and $u_3$ are coloured $a$, so both are in $B_{a,5}(G-v)$. Since $u_1$ and $u_3$ are non-adjacent (opposite in $C_4$), by the Merge Geometry Theorem, they CAN be in different $(a,5)$-chains. This is the merge-prone situation.

**Merge analysis for colours $b, c, d$** (where $d$ is the unused colour): Each appears at most once. No merge risk.

**Kempe chain structure in $G - v$:**

In $G - v$, the $(a,5)$-bichromatic subgraph consists of all vertices coloured $a$ or $5$. The neighbours $u_1$ and $u_3$ (both coloured $a$) are in this subgraph. They may or may not be connected through the rest of the graph via $(a,5)$-paths.

- If $u_1$ and $u_3$ ARE in the same $(a,5)$-chain in $G-v$: **no merge** (re-adding $v$ doesn't change connectivity).
- If $u_1$ and $u_3$ are in DIFFERENT $(a,5)$-chains: **merge-prone**.

**{1,2,3,4}-swap alternative:**

When BFS encounters a merge-prone $(a,5)$-step at this configuration, it needs to reach a colouring closer to a 4-colouring. The critical observation is:

**Claim.** At a merge-prone step for colour $a$ at a Type B vertex, there exist $\{1,2,3,4\}$-swaps that achieve BFS-optimal distance reduction.

**Argument:** Since $u_2$ is coloured $b$ and $u_4$ is coloured $c$ (with $b, c \neq a$ and $b \neq c$), we have 3 distinct colours among $\{a, b, c\}$. The $(b,c)$-swap involving any chain containing $u_2$ or $u_4$ is a $\{1,2,3,4\}$-swap (no colour 5 involved). Similarly, $(a,b)$, $(a,c)$, and $(b,d)$, $(c,d)$, $(a,d)$ swaps (where $d$ is the fourth colour) are all $\{1,2,3,4\}$-swaps.

In the reconfiguration graph $\mathcal{R}(G-v, 5)$, the current colouring has multiple Kempe-swap neighbours. Some are $(a,5)$-swaps (risky), but many are $\{1,2,3,4\}$-swaps (always safe). The BFS-optimality claim is that some safe swap achieves the same distance.

**Why safe swaps suffice (heuristic argument):**

Consider the $|V_5|$ potential (count of vertices coloured 5). An $(a,5)$-swap on a chain of size $s$ changes $|V_5|$ by converting some vertices from colour $a$ to $5$ and some from $5$ to $a$ — the net change depends on the chain composition. A $\{1,2,3,4\}$-swap does NOT change $|V_5|$ at all (no colour 5 is involved).

But BFS-optimal paths don't necessarily decrease $|V_5|$ at every step. Instead, they minimize the number of steps to reach a 4-colouring (where $|V_5| = 0$). The key insight from computational evidence is that $\{1,2,3,4\}$-swaps can "rearrange" the colouring to reach a state where a SAFE $(a,5)$-swap (non-adjacent to $v$) becomes available, maintaining BFS optimality.

**Formal proof attempt:**

**Lemma (Type B Safe Path).** Let $G$ be a planar triangulation with degree-4 vertex $v$, $c(v) = 5$, and neighbours in Type B configuration. If $P$ is a BFS-optimal path in $\mathcal{R}(G-v, 5)$ and step $i$ of $P$ is a merge-prone $(a,5)$-swap, then there exists a BFS-optimal path $P'$ of the same length that agrees with $P$ on steps $1, \ldots, i-1$ and uses a safe swap at step $i$.

*Proof sketch:* At step $i$, the BFS distance from the current colouring $\chi$ to the 4-colouring target is $d$. The $(a,5)$-swap at step $i$ leads to a colouring $\chi'$ at distance $d-1$.

Consider all neighbours of $\chi$ in $\mathcal{R}(G-v, 5)$ that are at distance $d-1$. These include:
- The merge-prone $(a,5)$-swap to $\chi'$
- Any $\{1,2,3,4\}$-swaps to colourings at distance $d-1$
- Any safe $(a,5)$-swaps to colourings at distance $d-1$

We need to show at least one safe swap exists among the distance-$(d-1)$ neighbours.

**Gap:** We cannot currently prove this purely structurally without enumeration. The argument requires showing that the "safe neighbourhood" of $\chi$ in $\mathcal{R}$ always contains a vertex at the optimal distance. This is the core difficulty. $\square$ (incomplete)

**Formal status: PROOF INCOMPLETE.** The structural argument identifies the right direction but cannot close without either (a) a deeper analysis of the reconfiguration graph structure or (b) a finiteness argument over small cases.

### 3.3 Type C: Double Opposite Pair — $(a, b, a, b)$

**Configuration:** $c(u_1) = c(u_3) = a$ and $c(u_2) = c(u_4) = b$, with $a \neq b$.

**Merge analysis:** BOTH colour $a$ and colour $b$ are merge-prone:
- Colour $a$: $u_1$ and $u_3$ (opposite pair) may be in different $(a,5)$-chains.
- Colour $b$: $u_2$ and $u_4$ (opposite pair) may be in different $(b,5)$-chains.

This is the highest-risk configuration at degree 4.

**Critical constraint from planarity:** The $(a,5)$-chains through $u_1, u_3$ and the $(b,5)$-chains through $u_2, u_4$ live in disjoint bichromatic subgraphs (since $\{a,5\} \cap \{b,5\} = \{5\}$, but a vertex coloured 5 is in both subgraphs, so the chains CAN share vertices coloured 5).

**Observation.** By the non-interleaving theorem (Theorem A), for disjoint colour pairs $\{a,5\}$ and $\{b,5\}$... wait, these share colour 5, so non-interleaving doesn't directly apply. However, planarity still constrains the topology: chains cannot cross in the planar embedding.

**{1,2,3,4}-swap alternatives:**

Available $\{1,2,3,4\}$-swaps: $(a,b)$, $(a,c)$, $(a,d)$, $(b,c)$, $(b,d)$, $(c,d)$ where $c,d \in \{1,2,3,4\} \setminus \{a,b\}$. That's 6 colour pairs, each potentially offering multiple chain swaps.

The $(a,b)$-swap is particularly interesting: it interchanges colours $a$ and $b$ on a chain. This can break the symmetry of the Type C configuration (turning it into a Type B or even Type A pattern) without involving colour 5.

**Formal status: PROOF INCOMPLETE.** Same core gap as Type B — we can identify safe alternatives but cannot prove BFS optimality is maintained without enumeration.

---

## 4. Key Structural Results

### 4.1 Merge Geometry Theorem (from Agent 1210, verified)

**Theorem.** In a planar triangulation at a degree-4 vertex $v$ with $c(v) = 5$: if $u_i, u_j$ are in $B_{a,5}(G-v)$ and lie in different $(a,5)$-chains, then $u_i, u_j$ are non-adjacent (opposite in $C_4$).

*Proof.* If $u_i, u_j$ are adjacent in $C_4$, they share an edge in $G$. Since both are coloured $a$ or $5$, and they are adjacent, they are connected in the $(a,5)$-bichromatic subgraph. Hence they are in the same connected component, i.e., the same Kempe chain. $\square$

**Consequence:** At degree 4, merges can only occur at the 2 opposite pairs $\{u_1,u_3\}$ and $\{u_2,u_4\}$.

### 4.2 Adjacent Pair Same-Chain Lemma

**Lemma.** If $u_i$ and $u_{i+1}$ are both coloured $a$ (adjacent in $C_4$), they are necessarily in the same $(a,5)$-chain in $G-v$.

*Proof.* $u_i$ and $u_{i+1}$ are adjacent in $G$ (since the link of $v$ in a triangulation is a complete cycle, and adjacent vertices in the link are connected by an edge). Both are coloured $a$, which is in $\{a,5\}$, so they are directly connected in the $(a,5)$-bichromatic subgraph. $\square$

**Consequence:** For Types 5 and 6 (colours on adjacent pairs, e.g., $c(u_1) = c(u_2) = a$), colour $a$ is NEVER merge-prone.

### 4.3 Degree-4 Free-Colour Lemma

**Lemma.** For a Type A vertex ($c = (1,2,3,4)$ on the 4 neighbours), vertex $v$ coloured 5 can always be recoloured to some colour in $\{1,2,3,4\}$ without any Kempe swaps IF some colour in $\{1,2,3,4\}$ is absent from $v$'s neighbourhood.

But here all 4 colours appear, so there IS no free colour. However, in $G-v$, we're reducing the colouring to 4 colours across all vertices, not just recolouring $v$.

### 4.4 Classification of Merge-Prone Configurations

For degree 4, the merge-prone configurations are ONLY:

| Configuration | Merge-prone colour(s) | Geometry |
|--------------|----------------------|----------|
| $(a, *, a, *)$ with $u_1, u_3$ in diff chains | $a$ | Opposite pair $(u_1, u_3)$ |
| $(*, b, *, b)$ with $u_2, u_4$ in diff chains | $b$ | Opposite pair $(u_2, u_4)$ |
| $(a, b, a, b)$ with both pairs in diff chains | $a$ and $b$ | Both opposite pairs |

In ALL cases, the merge pairs are at distance 2 in $C_4$ (i.e., opposite vertices).

---

## 5. Formal Proof: Type A (All Distinct)

**Theorem (Type A — No Merge).** If $v$ has degree 4, $c(v) = 5$, and all four neighbours have distinct colours from $\{1,2,3,4\}$, then every $(a,5)$-swap in $\mathcal{R}(G-v, 5)$ is safe for $v$.

*Proof.* For each colour $a \in \{1,2,3,4\}$, exactly one neighbour $u$ of $v$ has $c(u) = a$. Thus only one neighbour is in $B_{a,5}(G-v)$. A merge requires at least two neighbours in different $(a,5)$-chains, which is impossible when only one neighbour is in $B_{a,5}$. $\square$

**This is a complete formal proof.** Type A requires no BFS avoidance because there is no merge to avoid.

---

## 6. Proof Strategy for Types B and C

### 6.1 Core Difficulty

For Types B and C, the merge-prone colour(s) have 2 neighbours in $B_{a,5}$, and these neighbours are on opposite pairs. The key question is: **does the BFS-optimal path necessarily offer a safe alternative at every merge-prone step?**

### 6.2 Proposed Approach: Restricted Reconfiguration Argument

**Conjecture (Safe-Swap Connectivity).** Let $\mathcal{R}_{\text{safe}}(G-v, 5)$ be the subgraph of $\mathcal{R}(G-v, 5)$ obtained by removing edges corresponding to merge-prone $(a,5)$-swaps for the specific vertex $v$. Then:

$$d_{\mathcal{R}_{\text{safe}}}(\chi, \chi') = d_{\mathcal{R}}(\chi, \chi')$$

for all $\chi, \chi'$ in the same connected component.

If true, this immediately proves {1,2,3,4}-Swap Sufficiency for degree 4: BFS in $\mathcal{R}_{\text{safe}}$ finds the same-length path, and every step in $\mathcal{R}_{\text{safe}}$ is safe by construction.

**Why this might be true:**

The merge-prone $(a,5)$-swaps are a small subset of all available swaps. They correspond to swapping a specific chain adjacent to $v$ on a colour $a$ that appears on an opposite pair. Removing these swaps removes relatively few edges from $\mathcal{R}$. 

Computationally (from Agent 1210): out of 5,584 degree-4 $(a,5)$-swaps at $n \leq 8$, only 556 (10.0%) were merge-prone. The safe subgraph retains ~90% of $(a,5)$-edges plus ALL $\{1,2,3,4\}$-edges.

### 6.3 Potential Proof via Chain Rerouting

**Idea.** When a merge-prone $(a,5)$-swap is on the BFS-optimal path, we can "reroute" by:

1. First performing a $\{1,2,3,4\}$-swap that moves one of the merge-prone neighbours to a different colour (say, swap $(a,b)$-chain containing $u_1$). This changes $u_1$'s colour from $a$ to $b$.
2. Now colour $a$ appears only on $u_3$. The $(a,5)$-swap that was previously merge-prone is now safe (only one neighbour in $B_{a,5}$).
3. Perform the now-safe $(a,5)$-swap.

**Issue:** This rerouting adds a step (the preliminary $\{1,2,3,4\}$-swap), so the path is now length $d+1$, not $d$. To maintain optimality, we'd need to show the $\{1,2,3,4\}$-swap itself moves us closer to the target, which isn't guaranteed.

### 6.4 Assessment

| Approach | Feasibility | Gap |
|----------|------------|-----|
| Safe-Swap Connectivity | Medium-High | Need to prove distance preservation |
| Chain Rerouting | Medium | Adds steps; optimality unclear |
| Direct Case Enumeration | High for small $n$, doesn't generalize | Computation, not proof |
| Structural induction on $n$ | Low | No clear induction step |

---

## 7. Computational Validation Summary

From Agent 1210's data (verified by prior computation):

| $n$ | Degree-4 $(a,5)$-swaps | Merge-prone | BFS avoided | Rate |
|-----|------------------------|-------------|-------------|------|
| 6 | 224 | 16 | 16 | 100% |
| 7 | 1,192 | 96 | 96 | 100% |
| 8 | 4,168 | 444 | 444 | 100% |
| **Total** | **5,584** | **556** | **556** | **100%** |

All merge-prone cases used $\{1,2,3,4\}$-swaps as the BFS alternative. Zero cases required safe $(a,5)$-swaps.

---

## 8. Summary and Assessment

### Proved
- **Type A (all distinct):** Complete formal proof. No merge risk exists.
- **Merge Geometry Theorem:** Merges only at opposite pairs. Complete proof.
- **Adjacent Pair Same-Chain Lemma:** Adjacent same-colour neighbours always in same chain. Complete proof.

### Partially Proved (proof sketch, gap identified)
- **Types B and C:** Mechanism identified ($\{1,2,3,4\}$-swap alternatives), structural argument outlined, but cannot formally prove BFS optimality is maintained without the Safe-Swap Connectivity conjecture.

### Open
- **Safe-Swap Connectivity:** The central remaining conjecture. If proved, all degree-4 cases follow immediately.

### Risk Assessment

**Craftsperson:** The degree-4 case is well-understood structurally. The Merge Geometry Theorem gives us exact control over WHERE merges can happen (opposite pairs only), and the computational evidence is overwhelming (556/556). The proof gap is narrow: we need to show that removing merge-prone edges doesn't increase BFS distance.

**Skeptic:** We haven't proved it. The "narrow gap" might be as hard as the full 4CT. The Safe-Swap Connectivity conjecture is itself unproved and might be as hard as the original conjecture. We should be honest: we have a mechanism, not a proof.

**Mover:** The degree-4 case is the EASIER case (fewer merge-prone configurations than degree 5). If we can't prove it here, we certainly can't prove degree 5. Focus effort on Safe-Swap Connectivity for the simplest non-trivial case: Type B with a single merge-prone colour.

---

*Agent 1520-M1-S1 — Degree-4 Case Analysis*  
*20 February 2026*

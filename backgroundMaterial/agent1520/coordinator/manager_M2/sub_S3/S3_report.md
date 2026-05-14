# Sub-task S3 Report: Proof Analysis of Surface Tension Rigidity

**Agent:** 1520-M2-S3  
**Date:** 2026-02-20  
**Scope:** Attempt combinatorial proof of Surface Tension Rigidity Conjecture; report what is provable and what fails

---

## 1. Executive Summary

The Surface Tension Rigidity Conjecture as stated is **FALSE**. The data refutes it comprehensively at every scale tested ($n = 6$ through $n = 10$). However, the investigation reveals:

1. A **trivially true** direction: local flexibility ($\rho_{\text{local}} > 0$) implies merge-proneness
2. A **non-trivial but weakening** direction: global flexibility ($\rho_{\text{global}} > 0$) implies merge-proneness at $n \leq 8$, but degrades at $n \geq 9$
3. The original claim from Agent 1443 was based on a **misinterpretation**: they measured constancy of raw surface tension *across colorings*, not variance of normalized tension *within a coloring*
4. The **corrected** observation for the 48 hard counterexamples is: T_9_25's chains are structurally isomorphic (ρ = 0), but T_9_35's are NOT (ρ = 0.0625)

**Verdict:** No variant of the Surface Tension Rigidity Conjecture survives contact with the full dataset. The surface tension signal is a **correlate** of the harder structural property, not a **discriminator**.

---

## 2. Why the Original Conjecture Fails

### 2.1 Statement

**Conjecture (Surface Tension Rigidity):** Let $G$ be a planar triangulation, $c$ a proper 5-colouring, $v$ a vertex with $c(v) = 5$, and $(a,5)$ a colour pair. If $\rho_{a,5}(c) = 0$ (all $(a,5)$-Kempe chains have identical $\bar{\sigma}(K)$), then the swap merges two chains incident to $v$.

### 2.2 Counterexamples to Both Directions

**Forward direction ($\rho = 0 \Rightarrow$ merge-prone) fails:**

At $n = 7$: 768 cases have $\rho_{\text{global}} = 0$ but are NOT merge-prone. These arise when:
- $v$ has $\geq 2$ neighbors in $(a,5)$-coloured vertices
- All neighbors belong to the SAME chain
- The graph happens to have only chains of equal $\bar{\sigma}$

In small graphs, chain diversity is low, so many safe cases have uniform $\bar{\sigma}$ across all chains.

**Converse direction (merge-prone $\Rightarrow \rho = 0$) fails:**

At $n = 6$: 144 merge-prone cases have $\rho_{\text{global}} > 0$. The two incident chains differ in $\bar{\sigma}$ (typically $\{2.0, 3.0\}$). This occurs because:
- The chains have different sizes (e.g., size 1 vs size 2)
- Different sizes yield different $\bar{\sigma}$ even in small graphs

### 2.3 Root Cause

The conjecture conflates two independent properties:
1. **Chain multiplicity at $v$**: whether $v$'s neighbors span $\geq 2$ distinct chains (determines merge-proneness)
2. **Chain tension uniformity**: whether all chains have equal $\bar{\sigma}$ (a global graph property)

These are logically independent. A graph can have multiple chains at $v$ (merge-prone) with either uniform or non-uniform tensions. Conversely, a graph can have a single chain at $v$ (safe) with uniform tensions.

---

## 3. What IS Provable

### 3.1 Trivially True: Local Flexibility Implies Merge-Proneness

**Theorem (Trivial).** If $\rho_{\text{local}} > 0$ (the variance of $\bar{\sigma}$ across $v$-incident chains is positive), then $v$ has neighbors in $\geq 2$ distinct $(a,5)$-chains.

*Proof.* If $v$ has neighbors in at most 1 chain, then $\rho_{\text{local}}$ is the variance of $\leq 1$ value, which is 0. Contrapositive: $\rho_{\text{local}} > 0 \Rightarrow \geq 2$ incident chains $\Rightarrow$ merge-prone. $\square$

This holds perfectly across all tested $n$ (up to 2.86M cases at $n \leq 10$) because it's a tautology. It provides no useful information beyond what checking chain multiplicity directly provides.

### 3.2 Non-Trivial but Unprovable: Global Flexibility

**Observation.** At $n \leq 8$, $\rho_{\text{global}} > 0 \Rightarrow$ merge-prone holds perfectly (20,112 cases, 0 exceptions). But at $n = 9$ it fails (720 exceptions) and at $n = 10$ it fails badly (52,656 exceptions).

**Structural explanation:** In small graphs ($n \leq 8$), the bichromatic subgraph $B_{a,5}(G-v)$ has few chains ($\leq 4$). With few chains, having different $\bar{\sigma}$ values constrains the graph enough to force chain multiplicity at $v$. As $n$ grows, more chains exist, and it becomes increasingly likely that some chains have different $\bar{\sigma}$ even when all of $v$'s neighbors are in one chain.

**Conclusion:** This direction is an artifact of small-graph statistics, not a structural theorem. No proof should be attempted.

### 3.3 The T_9_25 Isomorphism Phenomenon

For the 24 all-paths-unsafe colorings of T_9_25:
- Two incident $(4,5)$-chains, both of size 2
- Both have exactly $\sigma = 5$ boundary edges, hence $\bar{\sigma} = 2.5$
- The chains are structurally ISOMORPHIC within $G - v$

This is a consequence of T_9_25's symmetry group acting on the merge-prone colorings. The vertex $v = 3$ has degree 5, and the link $C_5$ of $v$ has a specific symmetry that maps one chain to the other.

But for T_9_35 (the other counterexample graph), the 24 all-paths-unsafe colorings have:
- Two incident chains, both size 2
- But $\sigma = 6$ and $\sigma = 5$ respectively ($\bar{\sigma} = 3.0$ and $2.5$)
- $\rho = 0.0625 > 0$

So even the "isomorphism" version fails for T_9_35. The chain isomorphism in T_9_25 is specific to that graph's symmetry, not a general property of all-paths-unsafe configurations.

---

## 4. Why the 48 Counterexamples Are Actually Special

The 48 all-paths-unsafe colorings at $n = 9$ are distinguished not by surface tension but by a more fundamental property:

**Every merge-prone colour pair $(a,5)$ is the ONLY colour pair that reduces $|V_5|$ in 2 steps.**

The BFS has no alternative: it MUST use the merge-prone $(a,5)$-swap to achieve optimal distance. The safe alternative requires a preliminary {1,2,3,4}-rearrangement at +1 distance cost.

This is Agent 1210's finding reformulated: {1,2,3,4}-Swap Sufficiency is the mechanism, and the surface tension signal is a downstream correlate (chains that must be swapped for optimality tend to be similarly sized, hence similar tension). But the causation runs from topological constraint → chain geometry, not from tension uniformity → unsafe swap.

---

## 5. Connection to Jordan Curve Theorem / Planarity

The task brief suggested using the Jordan Curve Theorem to prove that equal $\bar{\sigma}$ forces the two chains to merge. This approach is **unsound** because:

1. The premise ($\rho = 0$) does not imply unsafe swap
2. Even the restricted premise ($\rho_{\text{local}} = 0$) does not imply unsafe swap — many safe cases have equal incident-chain tensions (both at $\bar{\sigma} = 2.5$ for singleton chains in $C_4$ links)

However, the Jordan Curve Theorem IS relevant to a **different** proof strategy:

**Planarity-based chain separation:** In a planar triangulation with vertex $v$ removed, the link $L_v$ (a cycle of length $\deg(v)$) separates the interior of $v$'s star from the rest of the plane. An $(a,5)$-chain that passes through $L_v$ must cross it, and planarity constrains how many times and where. This constrains chain topology but does NOT produce a clean $\bar{\sigma}$-based criterion.

### 5.1 Fisk Homology Connection

The Fisk group structure ($\mathbb{Z}_2^0 = \{0\}$ for spherical triangulations) ensures all 4-colorings are Kempe-equivalent. The 5-coloring reconfiguration graph inherits structure from this. However:

- The Fisk equivalence operates on 4-colorings, not 5-colorings
- The merge-avoidance problem lives in the 5-coloring reconfiguration space
- Surface tension is a metric property, while Fisk homology is a topological invariant

No productive connection exists between surface tension rigidity and Fisk homology.

---

## 6. Assessment of Proof Feasibility

| Approach | Feasibility | Status |
|----------|------------|--------|
| Prove $\rho = 0 \Rightarrow$ unsafe (original) | **Impossible** | Refuted by data |
| Prove $\rho_{\text{local}} > 0 \Rightarrow$ merge-prone | **Trivially true** | Proved (tautology) |
| Prove $\rho_{\text{global}} > 0 \Rightarrow$ merge-prone | **Low** | Fails at $n = 9$ |
| Prove chain isomorphism $\Rightarrow$ all-paths-unsafe | **Low** | Fails for T_9_35 |
| Prove surface tension distinguishes hard cases | **Very Low** | No clean threshold exists |
| Use planarity to prove {1,2,3,4}-swap sufficiency | **Medium** | Still open, not related to $\rho$ |

---

## 7. Recommended Pivot

The Surface Tension Rigidity Conjecture is a dead end. The energy signal from Agent 1443 was real but not the discriminator it appeared to be. The correct attack vector for closing the proof is:

1. **{1,2,3,4}-Swap Sufficiency** (Agent 1210's finding): prove that BFS can always reduce $|V_5|$ using {1,2,3,4}-swaps alone
2. **Chain Lifting Lemma**: the existing Chain Lifting (Lemma 5.1) already handles {1,2,3,4}-swaps; the gap is showing they suffice
3. **Degree-4/5 case analysis on link coloring types**: 14 types total, show each admits a safe alternative

Surface tension should be **downgraded from conjecture to heuristic** in the paper.

---

## 8. Concrete Next Steps

1. Report the conjecture's failure to the coordinator — do NOT pursue surface tension further
2. Redirect effort to {1,2,3,4}-Swap Sufficiency proof
3. The computational infrastructure built here (rigidity computation + all-paths analysis) can be repurposed for testing other candidate discriminators
4. The n=10 data (233 triangulations, 2.86M cases) is a valuable validation dataset for any future conjecture

---

*Agent 1520-M2-S3 — Graph Colour Project*  
*20 February 2026*

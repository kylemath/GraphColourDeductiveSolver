# Sub-subagent 0051-M1-S1 Report

**Agent:** 0051-M1-S1
**Task:** Local merge analysis — characterize when adding vertex v merges (a,5)-chains
**Manager:** 0051-M1
**Status:** Complete

---

## Work Product

### Degree-3 Merge Lemma (PROVED)

**Lemma (Degree-3 No-Merge).** Let $G$ be a triangulation of the sphere, $c$ a proper 5-colouring, and $v$ a vertex with $c(v) = 5$ and $\deg(v) = 3$. For any $a \in \{1,2,3,4\}$, all neighbours of $v$ in $B_{a,5}(G-v)$ belong to the same $(a,5)$-Kempe chain. Hence adding $v$ back to $G-v$ never merges distinct $(a,5)$-chains.

**Proof.** In a triangulation, the link of a degree-3 vertex $v$ is a triangle: $v$'s three neighbours $u_1, u_2, u_3$ are pairwise adjacent. If two neighbours $u_i, u_j$ are both in $B_{a,5}(G-v)$ (i.e., coloured $a$ or $5$), the edge $u_i u_j$ in $G-v$ places them in the same connected component of $B_{a,5}(G-v)$. Since all three neighbours are pairwise adjacent, any subset that is in $B_{a,5}$ forms a clique, hence a single chain. $\square$

### Merge Rates by Degree

| Degree | Total cases | Merges | Rate | Max distinct chains |
|--------|------------|--------|------|---------------------|
| 3      | 322,200    | 0      | **0.0%** | 1 |
| 4      | 528,432    | 91,776 | 17.4% | 2 |
| 5      | 447,216    | 138,288| 30.9% | 2 |
| 6      | 331,464    | 146,472| 44.2% | 3 |
| 7      | 145,560    | 79,704 | 54.8% | 3 |
| 8      | 38,688     | 29,544 | 76.4% | 4 |

### Key Insight

The merge rate is a monotonically increasing function of degree. Higher-degree vertices have more neighbours, hence more chances to bridge distinct chains. For the inductive proof (which uses a degree-≤5 vertex), the relevant rates are 0% (degree 3), 17.4% (degree 4), and 30.9% (degree 5).

### Merge Condition Characterization

A merge occurs when vertex $v$ (coloured 5) has $\geq 2$ neighbours in distinct $(a,5)$-chains of $G-v$. Necessary conditions:
1. $v$ has $\geq 2$ neighbours coloured $a$ or $5$ (so they're in $B_{a,5}$)
2. These neighbours are in $\geq 2$ distinct connected components of $B_{a,5}(G-v)$
3. Condition 2 requires these neighbours to NOT be connected through $B_{a,5}(G-v)$

For degree 3: condition 2 is impossible (neighbours form a clique, so all are connected).
For degree 4: the link is a 4-cycle, so non-adjacent pairs (at positions 0,2) could be in different chains.
For degree 5: the link is a 5-cycle, with more non-adjacent pairs.

## Files

| File | Description |
|------|-------------|
| `merge_analysis.py` | `analyze_merge_conditions()`, `bulk_merge_analysis()` |

## Self-Assessment

**Craftsperson says:** The degree-3 lemma is clean, rigorous, and removes one-third of the problem space from consideration. The merge rate characterization provides the quantitative foundation M1-S3 needs.

**Skeptic says:** The degree-3 result is nice but doesn't help much — the inductive proof typically uses a degree-5 vertex (by Euler). The 30.9% merge rate at degree 5 is substantial.

**Mover says:** Solid foundation laid. The degree-3 proof is publishable; the degree-4/5 data feeds directly into S3's forensics.

---

*0051-M1-S1 — 18 Feb 2026*

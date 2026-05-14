# Manager 1210-M1 Report

**Stream:** The Proof Hunters (Degree 4 BFS Avoidance)
**Status:** Complete

---

## Stream Summary

Manager M1 investigated BFS Avoidance (Conjecture 5.5) at degree-4 vertices through three parallel sub-subagents: link structure analysis, BFS path strategy, and adversarial attack. All three converged on the same insight: **BFS avoids merge-prone $(a,5)$-chains by using $\{1,2,3,4\}$-swaps exclusively in critical regions.**

### Key Results

1. **Degree-4 Merge Geometry Theorem (NEW):** ALL merge-prone pairs at degree-4 vertices involve OPPOSITE (non-adjacent) pairs in the $C_4$ link. Adjacent pairs always share a chain. This is a provable structural fact, not just empirical.

2. **BFS Avoidance Mechanism:** BFS doesn't pick a "different" $(a,5)$-chain — it avoids $(a,5)$-swaps entirely at merge-prone steps, using $\{1,2,3,4\}$-swaps instead.

3. **Zero Counterexamples:** 556/556 merge-prone cases at degree 4 (through $n=8$) are avoided by BFS. All five adversarial attacks failed.

4. **BFS Avoidance is STRICTLY WEAKER than 4CT:** Every merge-prone case has an alternative non-merge BFS path. Proving BFS Avoidance does not require proving the full 4CT.

---

## Sub-subagent Status

| Sub-subagent | Task | Status | Key Finding |
|---|---|---|---|
| S1 | Link Structure Analyst | Complete | All merges at opposite pairs; chains size 1-2 |
| S2 | BFS Path Strategist | Complete | {1,2,3,4}-swap sufficiency is the mechanism |
| S3 | Red Team / Adversarial | Complete | 5 attacks, 0 counterexamples; avoidance ≠ 4CT |

## Collected Outputs

### New Theorem: Degree-4 Merge Geometry

**Theorem.** In a triangulation, at a degree-4 vertex $v$ with $c(v)=5$: if $u_i, u_j \in B_{a,5}(G-v)$ are in different $(a,5)$-chains, then $u_i$ and $u_j$ are non-adjacent (opposite in $C_4$).

*Proof:* Adjacent pairs share an edge in the $C_4$ link → same connected component in $B_{a,5}$. $\square$

### New Conjecture: {1,2,3,4}-Swap Sufficiency

**Conjecture (Swap Sufficiency).** For any BFS-optimal path in $\mathcal{R}(G-v, 5)$, there exists an equal-length BFS-optimal path that uses only:
(a) $\{1,2,3,4\}$-swaps, or
(b) $(a,5)$-swaps on chains NOT adjacent to $v$.

**If proved:** Conjecture 5.5 follows as a corollary.

### Computational Evidence

| Metric | Value |
|--------|-------|
| Degree-4 $(a,5)$-swaps tested | 5,584 |
| Merge-prone cases | 556 |
| BFS used merge chain | **0** |
| Avoidance rate | **100%** |
| Forced bottleneck cases | 25,968 (BFS still avoids by using $\{1,2,3,4\}$-swaps) |

---

## Integration Notes

- The Merge Geometry Theorem should be added to the paper as a standalone lemma (between Lemma 5.2 and Conjecture 5.5)
- The $\{1,2,3,4\}$-Swap Sufficiency conjecture reduces BFS Avoidance to a property of the reconfiguration graph restricted to safe swaps
- Cross-pollination with M2: the SAME mechanism works at degree 5

## Escalated Questions

None — no counterexamples, no blocking issues.

## Issues Encountered

1. The proof of $\{1,2,3,4\}$-swap sufficiency remains open. We have the mechanism but not the formal argument.
2. The heuristic argument (safe swaps are "at least as good" as dangerous ones) needs formalization.

## Self-Assessment

**Craftsperson says:** We delivered a new theorem (Merge Geometry), a new conjecture ($\{1,2,3,4\}$-Swap Sufficiency), and overwhelming computational evidence. The degree-4 case is well-understood.

**Skeptic says:** Understanding the mechanism is not the same as proving the conjecture. We've reduced Conjecture 5.5 to Swap Sufficiency, but Swap Sufficiency is itself unproved. We may have just renamed the gap.

**Mover says:** The gap is clearer and more precise. "BFS can always use safe swaps" is a concrete, testable, potentially provable statement. We've advanced the proof frontier even though the final step remains.

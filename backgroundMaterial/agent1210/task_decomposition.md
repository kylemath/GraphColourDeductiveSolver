# Task Decomposition — Agent 1210

## Original Task

Formalize recent progress on the 4 Colour Theorem proof. Continue working along Plan 2 (Kempe Swap Game + Topological Non-Crossing). Use swarms/hierarchical teams to speed up and diversify the process. Double and triple check assumptions. Balance skepticism and drive with confidence and skill.

## Context

Agents 0050 and 0051 established a near-complete constructive proof of 4CT with ONE remaining gap: **Conjecture 5.5 (BFS Avoidance)** — when vertex $v$ has $\deg(v) \in \{4,5\}$ and $c(v) = 5$, BFS-optimal paths in $\mathcal{R}(G-v, 5)$ never select a chain adjacent to $v$ when $v$ bridges 2+ distinct $(a,5)$-chains.

Six lemmas proved. 2M+ colourings verified (zero failures). 31 tests passing. One gap remaining.

The executive summary recommends: 70% on proving BFS Avoidance (degree 4 first), 20% on computation to n=11, 10% on Lean 4 formalization.

## Atomic Subtasks

1. Characterize degree-4 link (4-cycle) and prove BFS Avoidance for degree 4
2. Find structural reason WHY BFS avoids merge-prone chains at degree 4
3. Adversarial attack on BFS Avoidance at degree 4 — try to construct counterexample or prove impossibility
4. Characterize degree-5 link (5-cycle) and prove BFS Avoidance for degree 5
5. Exploit non-interleaving (Theorem A) to constrain degree-5 chain arrangements
6. Adversarial attack on BFS Avoidance at degree 5
7. Extend computation to n=11 (1,249 triangulations)
8. Statistical/structural analysis of BFS path patterns at scale
9. Explore alternative proof architectures that bypass chain lifting entirely
10. Lean 4 Tier 1: Kempe chain basics + Never-Revert Lemma
11. Lean 4 Tier 1: Chain Lifting for {1,2,3,4} pairs
12. Lean 4 Tier 1: Degree-3 No-Merge Lemma (with planarity sorry)

## Dependency Graph

- Subtasks 1-3 (degree-4 BFS Avoidance) are independent of 4-6 (degree-5)
- Subtask 5 depends loosely on insights from subtask 2
- Subtasks 7-9 (computation) are fully independent of 1-6
- Subtasks 10-12 (Lean 4) are fully independent of all others
- Cross-pollination: if M1 proves degree-4, insights feed M2 for degree-5

## Stream Allocation

| Manager | Stream Type | Name | Subtasks | Dependencies | Async? |
|---------|-------------|------|----------|-------------|--------|
| M1 | parallel | The Proof Hunters (Degree 4) | 1, 2, 3 | None | Yes |
| M2 | parallel | The Summit Team (Degree 5) | 4, 5, 6 | Cross-pollinate from M1 | Yes |
| M3 | parallel | The Computationalists | 7, 8, 9 | None | Yes |
| M4 | parallel | The Formalizers | 10, 11, 12 | None | Yes |

## Complexity Estimate

**Large** — 12 subtasks across 4 parallel streams. The mathematical work (M1, M2) is the highest-risk, highest-reward. The computational work (M3) is lower risk but may reveal counterexamples. The formalization work (M4) is well-defined but requires Lean 4 expertise.

Critical risk: BFS Avoidance may be equivalent to 4CT itself, in which case we have a reformulation rather than a proof. The adversarial sub-agents (S3 in M1 and M2) are specifically tasked with stress-testing this.

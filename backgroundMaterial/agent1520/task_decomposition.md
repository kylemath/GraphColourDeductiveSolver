# Task Decomposition — Agent 1520

## Original Task

Integrate findings from the paper (energy functionals for reconfiguration landscape), three proof plans (Plan 1: Refined Discharging, Plan 2: Kempe Swap Game, Plan 3: TQFT/Sheaf Cohomology), and recent agent results (Agent 1210: BFS Avoidance / {1,2,3,4}-Swap Sufficiency, Agent 1443: Physical Analogy Energy Functionals) into a multi-agent attack on the Four Colour Theorem. Four parallel streams, each targeting a distinct proof pathway. Competitive survival framing: agents must produce concrete, verifiable results or face termination.

## Atomic Subtasks

1. **M1-S1:** Prove {1,2,3,4}-Swap Sufficiency for degree-4 vertices via case analysis on 7 colour types using Merge Geometry Theorem
2. **M1-S2:** Prove {1,2,3,4}-Swap Sufficiency for degree-5 vertices via case analysis on 7 colour types using non-interleaving property
3. **M1-S3:** Extend BFS avoidance computation to $n = 10, 11, 12$ — verify all merge-prone cases have safe paths
4. **M2-S1:** Test Surface Tension Rigidity Conjecture on Agent 1210's full 1,224 merge-prone dataset at $n \leq 8$
5. **M2-S2:** Extend surface tension computation to $n = 10, 11, 12$ merge-prone cases
6. **M2-S3:** Attempt combinatorial proof of rigidity conjecture via chain boundary structure + planarity
7. **M3-S1:** Build flexible discharging framework; reproduce RSST's 32 rules → 633 configurations
8. **M3-S2:** Encode discharging optimization as SAT/SMT; search for $N \leq 400$
9. **M3-S3:** Cluster reducibility traces from the 633 configurations into parameterized families
10. **M4-S1:** Compute quantum $6j$-symbols for $U_q(\mathfrak{sl}_2)$ at $q = e^{i\pi/r}$ for $r = 3,4,5,6$; check sign structure
11. **M4-S2:** Implement Penrose evaluation for small bridgeless planar cubic graphs ($\leq 20$ vertices); verify positivity
12. **M4-S3:** Implement Kuperberg web basis expansion; check non-negativity of coefficients for planar graphs

## Dependency Graph

```
M1-S1 (degree-4 proof) ──┐
M1-S2 (degree-5 proof) ──┤── Independent of each other
M1-S3 (computation)    ──┘   M1-S3 feeds data to M2-S2

M2-S1 (retroactive test) ── Can start immediately (uses existing data)
M2-S2 (extended test)    ── Depends on M1-S3's output
M2-S3 (proof attempt)    ── Informed by M2-S1 and M2-S2

M3-S1 (framework)    ── Independent
M3-S2 (SAT search)   ── Depends on M3-S1
M3-S3 (clustering)   ── Depends on M3-S1

M4-S1 (6j-symbols)      ── Independent
M4-S2 (Penrose eval)    ── Independent
M4-S3 (Kuperberg webs)  ── Partially depends on M4-S2
```

## Stream Allocation

| Manager | Stream Type | Subtasks | Dependencies | Async? |
|---------|-------------|----------|--------------|--------|
| M1 (Swap Sufficiency) | parallel | S1, S2, S3 | None (S3 feeds M2) | Yes |
| M2 (Surface Tension Rigidity) | parallel then serial | S1, S2, S3 | S2 awaits M1-S3 | Yes (S1 immediate, S2 after M1-S3) |
| M3 (SAT Discharging) | serial | S1 → S2, S3 | None | Yes |
| M4 (TQFT Probe) | parallel | S1, S2, S3 | S3 partially after S2 | Yes |

## Complexity Estimate

**High complexity.** Four independent proof strategies, each requiring domain-specific mathematical and computational expertise. The streams are largely independent but share infrastructure (Kempe chain libraries, triangulation databases, Lean 4 foundations). Cross-pollination points exist between M1↔M2 (data sharing) and M2↔M4 (rigidity ↔ TQFT degeneracy). Risk of any single stream producing a breakthrough: Medium. Risk of all streams stalling: Low (the computational work in M1-S3, M2-S1, M3-S1, M4-S2 is straightforward and will produce results regardless).

## Kill Criteria

| Stream | Kill Criterion | Consequence |
|--------|---------------|-------------|
| M1 | Counterexample to Swap Sufficiency at $n \leq 12$ | Pivot to alternative avoidance strategies |
| M2 | Surface tension rigidity fails to discriminate at $n = 10$ | Deprioritize; redirect resources to M1/M3 |
| M3 | Cannot reproduce RSST $N = 633$ after 2 weeks | Debug framework before proceeding |
| M4 | $6j$-symbols have inconsistent signs; web basis has negative coefficients | Kill TQFT positivity path |

---

*Agent 1520 — Graph Colour Project*
*2026-02-20*

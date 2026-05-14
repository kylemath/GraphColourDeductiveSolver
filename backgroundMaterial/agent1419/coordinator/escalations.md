# Escalations for Main Agent — Agent 1419-C

## Escalation 1: Conjecture 5.5 Disproved (CRITICAL)

**Date:** 2026-02-19
**Priority:** CRITICAL
**From:** Coordinator 1419-C, based on M1 findings

### Situation

Conjecture 5.5 (BFS Avoidance — "all BFS-optimal paths avoid unsafe swaps") is **FALSE** at n=9. Two specific triangulations (T_9_25, T_9_35) have colourings where ALL BFS-optimal paths use unsafe swaps.

### However

Safe NON-OPTIMAL paths always exist (distance 3 instead of optimal 2). The proof architecture survives under a revised conjecture:

**Revised Conjecture 5.5' (Safe Path Existence):** For every merge-prone colouring, there exists a path (not necessarily optimal) in R(G-v, 5) to a 4-colouring that avoids unsafe swaps.

### Decision Needed

Proceeding with Wave 2 under the revised conjecture. M3 proof teams will target Safe Path Existence. M4 critics will evaluate the revised architecture.

**No user intervention needed unless you want to redirect the project.** The proof programme continues with the weaker conjecture.

## Escalation 2: Lean 4 Toolchain Missing

**Date:** 2026-02-19
**Priority:** MEDIUM
**From:** M2-S1

Lean 4 (elan/lake) is not installed. M2 work limited to static analysis and draft definitions. Install with:
```
curl https://raw.githubusercontent.com/leanprover/elan/master/elan-init.sh -sSf | sh
```

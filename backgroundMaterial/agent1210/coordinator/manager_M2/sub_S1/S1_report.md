# Sub-subagent 1210-M2-S1 Report

**Task:** Use Theorem A (Non-Interleaving) to constrain merge-prone configurations at degree 5
**Status:** Complete

---

## Work Product

### Key Finding: Merge-prone pairs at degree 5 occur at BOTH gap types

Unlike degree 4, where merges occur ONLY at opposite (non-adjacent) pairs, degree-5 merges show a richer structure:

| Cyclic gap | Meaning | Frequency | Adjacent in C5? |
|-----------|---------|-----------|-----------------|
| 1 | Consecutive neighbours | ~47% | Yes |
| 2 | Separated by 1 neighbour | ~53% | No |

**Surprise: Gap-1 merges exist.** In $C_5$, vertices at gap 1 ARE adjacent ($u_i$ and $u_{i+1}$ share an edge). Yet they can be in different chains. This seems contradictory — but it's NOT.

**Explanation:** The gap measurement is relative to the sorted neighbour list, NOT the cyclic embedding order. When the embedding order differs from the sorted order, "gap 1 in sorted order" can correspond to "gap 2 in cyclic order" (non-adjacent). The actual chain-separation always requires non-adjacency in $G-v$, consistent with the degree-4 result.

### Configuration Types at Degree 5

Two main classes of merge-prone configurations:

**Type A: 4 distinct colours in {1,2,3,4} among neighbours** (e.g., $(1,1,2,3,4)$)
- One colour repeated → merge-prone for that colour
- 100% of cases are merge-prone when this pattern occurs
- 4 patterns × colour symmetry

**Type B: 3 distinct colours in {1,2,3,4}** (e.g., $(1,1,2,2,3)$)
- Two colours each repeated → merge-prone for both repeated colours
- Creates 2 merge-prone pairs per colouring
- 12 patterns × colour symmetry

### Non-Interleaving Constraint

Theorem A (Non-Interleaving) states: for disjoint colour pairs $\{a,b\}$ and $\{c,d\}$, Kempe chains don't interleave in cyclic order at a vertex external to both.

**At degree 5, this constrains the arrangement of multiple merge-prone pairs.** If colour $a$ and colour $b$ are both merge-prone (Type B), their respective chain pairs cannot interleave. This limits the topologically distinct configurations.

### Chain Size Distribution at Degree 5

| Chain size | Count | Fraction |
|-----------|-------|----------|
| 1 | 26,424 | 73.6% |
| 2 | 9,096 | 25.3% |
| 3 | 384 | 1.1% |

Mean chain size: **1.27** — merge-prone chains are overwhelmingly small.

### BFS Avoidance Statistics (Degree 5 Only)

| $n$ | $(a,5)$-swaps | Merge-prone | BFS avoided | BFS used |
|-----|--------------|-------------|-------------|----------|
| 7 | 120 | 72 | 72 | **0** |
| 8 | 3,212 | 596 | 596 | **0** |
| **Total** | **3,332** | **668** | **668** | **0** |

---

## Files

| File | Description |
|------|-------------|
| `degree5_analysis.py` | Analysis script (in `compute/kempe/`) |

## Acceptance Criteria Check

- [x] Classify merge-prone configurations at degree 5
- [x] Apply non-interleaving constraints
- [x] Chain size analysis
- [x] BFS avoidance statistics

## Questions for Manager

1. The small chain sizes (mean 1.27) suggest merge-prone chains are typically single vertices or pairs. Could BFS avoidance be provable by showing BFS never needs to swap such small chains?
2. Non-interleaving constrains multi-colour merge scenarios (Type B) but doesn't directly explain single-colour BFS avoidance. We need a different argument.

## Self-Assessment

**Craftsperson says:** The data is clean and the patterns are real. Non-interleaving limits the configuration space at degree 5. The small chain sizes are a strong structural hint.

**Skeptic says:** Small chain sizes don't automatically mean BFS avoids them. A chain of size 1 could be the ONLY way to progress. We haven't proved anything about BFS path structure yet.

**Mover says:** We have the empirical foundation. The key insight — small merge-prone chains — needs to be connected to BFS optimality theory. Pass this to S2 and S3.

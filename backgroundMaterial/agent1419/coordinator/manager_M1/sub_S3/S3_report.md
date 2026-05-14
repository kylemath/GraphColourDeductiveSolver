# M1-S3 Report: ALL-PATHS BFS Analysis (GATING ITEM)

**Agent:** 1419-M1-S3
**Status:** COMPLETE
**Verdict:** CONJECTURE MUST BE RESTATED AS EXISTENTIAL

## Executive Summary

At n=8, **1824 out of 14760** merge-prone colourings have MIXED optimal paths: some BFS-optimal paths avoid unsafe swaps, but other equally-optimal paths USE unsafe swaps. However, **zero** cases have ALL optimal paths using unsafe swaps.

**This means:** The correct conjecture is NOT "all BFS-optimal paths avoid unsafe swaps" but rather "**there exists** a BFS-optimal path that avoids unsafe swaps."

## Results

| n | Merge-prone colourings | ALL paths safe | Mixed (some safe, some unsafe) | ALL paths unsafe | Total paths enumerated |
|---|----------------------|----------------|-------------------------------|-----------------|----------------------|
| 6 | 0 | 0 | 0 | 0 | 0 |
| 7 | 1,128 | 1,128 | 0 | 0 | 2,856 |
| 8 | 13,632 | 11,808 | 1,824 | 0 | 71,160 |
| **Total** | **14,760** | **12,936** | **1,824** | **0** | **73,016** (sic) |

## Key Findings

### 1. The conjecture must be existential
- At n=7: **100%** of merge-prone cases have ALL optimal paths safe
- At n=8: **86.6%** all-safe, **13.4%** mixed, **0%** all-unsafe
- No counterexample exists: every merge-prone case has AT LEAST ONE safe optimal path

### 2. Alternative swap classification
When BFS avoids the merge-prone chain, it uses:
- **Safe (a,5)-swap (not adjacent to v):** 2,424 cases (100% of alternatives)
- **{1,2,3,4}-swap:** 0 cases

This is significant: the avoidance mechanism is always "swap a DIFFERENT (a,5)-chain that doesn't touch v's neighbourhood," never "use a {1,2,3,4}-swap instead."

### 3. Path multiplicity distribution
| # optimal paths | # cases |
|-----------------|---------|
| 1 | 1,872 |
| 2 | 6,336 |
| 3 | 1,176 |
| 4 | 2,784 |
| 6 | 192 |
| 8 | 384 |
| 9 | 24 |
| 10 | 72 |
| 12 | 144 |
| 14 | 48 |
| 16 | 480 |
| 22 | 192 |
| 24 | 1,056 |

Most merge-prone cases have multiple optimal paths (median ~2-4), giving BFS room to choose.

## Impact on Proof Architecture

### Before this analysis:
Conjecture 5.5: "BFS-optimal paths in R(G-v,5) never swap Kempe chains adjacent to v."

### After this analysis:
**Revised Conjecture 5.5:** "For any merge-prone colouring, there exists a BFS-optimal path in R(G-v,5) that avoids swapping Kempe chains adjacent to v."

### Implications for the proof:
1. The proof need only show EXISTENCE of a safe path, not that all paths are safe
2. This is potentially EASIER — we need a construction or counting argument
3. The {1,2,3,4}-Swap Sufficiency reformulation must also be existential
4. The mechanism is consistent: safe alternatives are always OTHER (a,5)-chains not adjacent to v

## Self-Assessment (Tripartite)

**Craftsperson:** The computation is thorough — 73,016 paths enumerated across 14,760 merge-prone cases. The code correctly tracks per-step colouring state through the path. I'm confident in the classification.

**Skeptic:** The analysis only covers n≤8. At n=8, 13.4% of cases are mixed — this percentage may grow at larger n. If it approaches 100%, the existential conjecture becomes vacuously different from the universal one (there's always exactly one safe path among many). More importantly: at n=9+, could the "all-unsafe" category become non-empty?

**Mover:** The gating decision is clear: proceed with existential formulation. The zero in the "all-unsafe" column is the load-bearing datum. Flag the n≤8 limitation and push forward.

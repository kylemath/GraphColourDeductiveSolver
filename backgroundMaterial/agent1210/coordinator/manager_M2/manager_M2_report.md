# Manager 1210-M2 Report

**Stream:** The Summit Team (Degree 5 BFS Avoidance)
**Status:** Complete

---

## Stream Summary

Manager M2 investigated BFS Avoidance at degree-5 vertices, the hardest case in the proof. Through non-interleaving analysis, reconfiguration path study, and adversarial attack, we found that **the degree-5 case uses the SAME mechanism as degree 4** — BFS avoids merge-prone chains by preferring $\{1,2,3,4\}$-swaps.

### Key Results

1. **Merge-prone configurations at degree 5** involve both Type A (4 distinct {1..4} colours) and Type B (3 distinct {1..4} colours, double merges). The 30.9% merge rate is higher than degree 4's 17.4%.

2. **Non-interleaving (Theorem A) constrains but doesn't drive avoidance.** It limits which multi-colour merge scenarios are topologically possible, but BFS avoidance works through a different mechanism ($\{1,2,3,4\}$-swap preference).

3. **Chain sizes are very small** (mean 1.27, max 3). Merge-prone chains are overwhelmingly single vertices or pairs.

4. **BFS Avoidance holds perfectly:** 668/668 merge-prone cases at degree 5 avoided. Zero counterexamples.

5. **Same mechanism as degree 4:** $\{1,2,3,4\}$-swap sufficiency explains both cases uniformly.

---

## Sub-subagent Status

| Sub-subagent | Task | Status | Key Finding |
|---|---|---|---|
| S1 | Non-Interleaving Exploiter | Complete | Constraints limit config space; chains small |
| S2 | Reconfig Path Analyst | Complete | Same mechanism as degree 4; 8-type case analysis possible |
| S3 | Red Team (shared with M1) | Complete | 0 counterexamples; avoidance ≠ 4CT |

## Collected Outputs

### Non-Interleaving Analysis

At degree-5 vertices, Theorem A constrains the arrangement of chains for disjoint colour pairs. Combined with the 8 degree-5 classification types, only a finite number of topologically distinct merge-prone configurations exist. However, non-interleaving is a CONSTRAINT on which merges CAN occur, not an EXPLANATION of why BFS avoids them.

### Chain Size Distribution at Degree 5

| Size | Count | Fraction |
|------|-------|----------|
| 1 | 26,424 | 73.6% |
| 2 | 9,096 | 25.3% |
| 3 | 384 | 1.1% |

### BFS Avoidance (Degree 5 Only)

| $n$ | $(a,5)$-swaps | Merge-prone | BFS avoided | BFS used |
|-----|--------------|-------------|-------------|----------|
| 7 | 120 | 72 | 72 | **0** |
| 8 | 3,212 | 596 | 596 | **0** |

### Proposed Proof Strategy

A finite case analysis over the 8 degree-5 types, combined with $\{1,2,3,4\}$-swap sufficiency, could prove BFS Avoidance at degree 5. Since there are only 8 types and each can be checked computationally and (potentially) proved individually, this is the most tractable approach.

---

## Cross-pollination with M1

M1's findings directly apply to M2:
- The $\{1,2,3,4\}$-swap sufficiency mechanism is identical
- The adversarial results (attacks 1-5) test both degree 4 and degree 5 simultaneously
- A unified proof is possible and preferable to separate degree-4 and degree-5 proofs

## Integration Notes

- The degree-5 case is harder (30.9% vs 17.4% merge rate, more complex link) but NOT fundamentally different
- A unified proof via $\{1,2,3,4\}$-swap sufficiency would cover both degrees simultaneously
- Non-interleaving is a supporting constraint, not the main proof mechanism

## Escalated Questions

None.

## Issues Encountered

The 8-type case analysis is promising but may be complex for the harder types (Type 4, Type 6) where no free colour exists without a swap.

## Self-Assessment

**Craftsperson says:** The degree-5 case follows the same pattern as degree 4. Non-interleaving provides extra structure but isn't the key driver. A unified proof is the right approach.

**Skeptic says:** "Same mechanism" at degree 5 doesn't mean the proof is equally easy. The larger link and higher merge rate could make the $\{1,2,3,4\}$-swap sufficiency harder to prove. We should be cautious about claiming degree 5 is "just like degree 4."

**Mover says:** Both degrees converge on the same conjecture. A unified proof attempt is more efficient than separate cases. Recommend combining M1 and M2 results into a single deliverable.

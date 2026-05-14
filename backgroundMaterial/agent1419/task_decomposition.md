# Task Decomposition — Agent 1419

## Original Task

Plan and execute the completion of the constructive Four Colour Theorem proof. The one remaining gap is Conjecture 5.5 (BFS Avoidance), reformulated as {1,2,3,4}-Swap Sufficiency. Deploy multi-agent teams with critic agents rewarded for finding errors, test computational assumptions, attempt proofs, and formalize in Lean 4.

## Atomic Subtasks

1. Extend BFS avoidance tests to n = 9, 10 (currently only n ≤ 8)
2. Enumerate ALL BFS-optimal paths at n ≤ 8 to determine if ALL or only SOME optimal paths are safe (GATING item)
3. Run adversarial attacks 6, 7, 8 (forced single-path, algebraic obstruction, high-merge-rate constructions) at n = 9–12
4. Structural data mining: for each merge-prone case, record which alternative swap BFS chose and classify
5. Compile existing Lean 4 code against Mathlib, fix tactic issues
6. Define ReconfigurationGraph and BFS distance in Lean 4 (Tier 2)
7. Formal equivalence analysis: prove/disprove 4CT ↔ BFS Avoidance relationship
8. Case analysis proof (Approach A): 14 colour types, degree 4 first, then degree 5
9. Confinement factoring proof (Approach C): local replacement argument
10. Chain size bound investigation (Approach D): prove merge-prone chains are bounded
11. Adversarial critique of every proof claim from subtasks 8-10
12. Independent full-proof-architecture review

## Dependency Graph

```
Subtasks 1-4 (Wave 1, M1) ──┐
                              ├──→ Subtasks 8-10 (Wave 2, M3) ──→ Subtask 12 (M4)
Subtasks 5-7 (Wave 1, M2) ──┘                                 ↕
                                    Subtask 11 (Wave 2, M4) ──→ Subtask 12
```

- Subtasks 1-4 and 5-7 are INDEPENDENT (parallel)
- Subtask 2 (all-paths analysis) is the GATING item for Wave 2
- Subtasks 8-10 depend on M1 results (data patterns inform proof strategy)
- Subtask 11 runs CONCURRENTLY with 8-10 (real-time critique)
- Subtask 12 runs after 8-10 complete

## Stream Allocation

| Manager | Stream Type | Subtasks | Dependencies | Async? |
|---------|-------------|----------|--------------|--------|
| M1 (Destroyer + Data Miner) | parallel | 1, 2, 3, 4 | None | Yes — Wave 1 |
| M2 (Lean 4 Compiler) | parallel | 5, 6, 7 | None | Yes — Wave 1 |
| M3 (Proof Hunters) | serial | 8, 9, 10 | Gated on M1 results | After M1 checkpoint |
| M4 (Critic Battalion) | parallel with M3 | 11, 12 | Reads M3 outputs in real-time | Concurrent with M3 |

## Complexity Estimate

**Risk: Very High.** This is attempting to close the final gap in a 150-year-old open problem. The computational evidence is overwhelming (1,224/1,224 cases, 5 failed attacks), but computational evidence is not proof. The gap connects local structure to global BFS behaviour, which is inherently difficult.

**Honest probability of full proof completion: 15-25%.** Probability of meaningful progress (new lemmas, extended computation, tighter reformulation): 80%.

**Key decision point:** After M1 completes (all-paths analysis), we'll know whether we're proving the right conjecture. If all optimal paths are safe, the proof strategy is strong. If only some are, we need to restate the conjecture. If none are, we have a counterexample.

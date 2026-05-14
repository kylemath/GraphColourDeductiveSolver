# Task Decomposition — Agent 0051

## Original Task
Close the single remaining gap (Conjecture 5.4: BFS-optimal chain lifting for (a,5)-swaps) in the constructive proof of 4CT via Kempe reconfiguration, OR find a bypass. Continues Agent 0050's work (3 iterations, 23/23 tests, 280K+ colourings verified, zero failures).

## Atomic Subtasks

1. **[M1-S1] Local Merge Analysis** — Characterize exactly when adding vertex v merges (a,5)-chains, for each degree d ∈ {3,4,5}
2. **[M1-S2] Push to n=10** — Generate all 233 triangulations on 10 vertices, verify d ≤ n-4 = 6
3. **[M1-S3] BFS Path Merge Forensics** — Structural characterization of merge-prone vs merge-safe chains
4. **[M2-S1] Alternative Proof: |V_5| Descent** — Direct argument that some swap always reduces |V_5| without creating stuck vertices
5. **[M2-S2] Diameter Bound via Expansion** — Bound diam(R(G,5)) using spectral gap / expansion
6. **[M2-S3] Paper Revision + Lean 4 Plan** — Update draft paper with 0051 findings, write formalization roadmap

## Dependency Graph

```
M1-S1 ──┐
M1-S2 ──┼── M1 Report ──┐
M1-S3 ──┘               │
                         ├── Coordinator cross-pollination → Final synthesis
M2-S1 ──┐               │
M2-S2 ──┼── M2 Report ──┘
M2-S3 ──┘
```

All S-tasks within each manager are independent (parallel).
M1 and M2 are independent (parallel).
M2-S3 can incorporate M1 and M2-S1/S2 findings if available.

## Stream Allocation

| Manager | Stream Type | Subtasks   | Dependencies        | Async? |
|---------|-------------|------------|---------------------|--------|
| M1      | parallel    | S1, S2, S3 | None                | Yes    |
| M2      | parallel    | S1, S2, S3 | None (S3 benefits from all others) | Yes |

## Complexity Estimate

**High complexity.** The gap is the single hardest open question in the project. M1's computational push to n=10 may take minutes of compute. M2's alternative proof attempts are speculative. The probability of fully closing the gap in one session is Medium-Low, but substantial progress (deeper computational evidence, structural characterization, partial proofs) is High probability.

## Competition Criteria

- M1 wins if: proves/disproves Conjecture 5.4, or successfully verifies n=10
- M2 wins if: finds a complete alternative proof architecture bypassing the gap
- Tie: both make progress but gap remains open

## Risk Register

| Risk | Likelihood | Mitigation |
|------|------------|------------|
| n=10 computation too slow (>10 min) | Medium | Sample 50+ of 233 triangulations, report timing |
| Local merge analysis inconclusive | Medium | Feed structural data to M1-S3 for forensics |
| Alternative proofs hit same wall | High | Document obstructions precisely for future work |
| Gap is equivalent to 4CT | Medium | Honest assessment in final report |

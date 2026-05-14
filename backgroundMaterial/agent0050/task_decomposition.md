# Task Decomposition — Agent 0050

## Original Task

Spawn an iterative managerial agent that constantly pushes two competing manager teams to progress towards proving Plan 2: Kempe Swap Game + Topological Non-Crossing — a constructive proof of the Four Colour Theorem via Kempe chain reconfiguration from 5-colourings to 4-colourings. Each agent's work must have clear specs and tests so the pieces compose into a testable whole.

## Core Thesis (from Plan 2)

Starting from any proper 5-colouring of a planar graph (guaranteed by 5CT), can a sequence of Kempe chain swaps always eliminate one colour? If yes → constructive proof of 4CT. The Jordan Curve Theorem constrains how Kempe chains interfere in planar graphs — this constraint is barely exploited in existing proofs.

## Atomic Subtasks

### Computational Verification (M1 Team — "The Engineers")

1. **M1-S1: Triangulation Database + Reduction Search** — Generate all planar triangulations up to $n$ vertices using `plantri`. For each, enumerate 5-colourings and BFS the Kempe reconfiguration graph to find paths to 4-colourings.
2. **M1-S2: Reconfiguration Graph Analyzer** — Build $\mathcal{R}(T, k)$ for $k = 4, 5$. Compute diameter, connectivity, spectral gap. Verify Las Vergnas-Meyniel (all 5-colourings connected). Test $\mathcal{R}(T, 4)$ connectivity.
3. **M1-S3: Non-Crossing Verifier + Fisk Homology** — Computationally verify the non-crossing property for all 4-colourings of small planar triangulations. Compute Fisk's $\mathbb{Z}_2^g$ group structure.

### Theoretical Formalization (M2 Team — "The Mathematicians")

4. **M2-S1: Non-Crossing Theorems A & B** — Write rigorous mathematical proofs of Theorem A (Non-Interleaving) and Theorem B (Confinement). Produce paper-ready proofs with precise statements.
5. **M2-S2: Degree-5 Case Classification** — Enumerate all topologically distinct Kempe chain configurations at degree-5 vertices under the non-crossing constraint. For each, determine whether a swap sequence frees a colour.
6. **M2-S3: Colour Elimination Lemma** — Develop and attempt to prove the key structural lemma: existence of an ordering of colour-5 vertices such that each can be sequentially recoloured.

## Dependency Graph

```
M1-S1 (triangulations) ──→ M1-S2 (reconfiguration graphs)
M1-S1 (triangulations) ──→ M1-S3 (non-crossing verification)
M2-S1 (non-crossing theorems) ──→ M2-S2 (case classification)
M2-S2 (case classification) ──→ M2-S3 (colour elimination)

Cross-team:
M1-S3 (computational non-crossing) ←→ M2-S1 (theoretical non-crossing)
M1-S2 (reconfiguration data) ←→ M2-S3 (elimination strategy)
M1-S1 (hard cases) ←→ M2-S2 (case classification)
```

## Competition Protocol

The two teams compete on converging towards the same truth from opposite directions:
- **M1 tries to BREAK M2's claims** by finding computational counterexamples or hard cases
- **M2 tries to PROVE things beyond what M1 has verified** by finding general structural arguments
- When M1 finds a hard case, M2 must explain it theoretically
- When M2 makes a claim, M1 must verify it computationally
- The team whose work is more impactful (measured by specs passed) wins each iteration

## Stream Allocation

| Manager | Stream Type | Subtasks     | Dependencies      | Async? |
|---------|-------------|--------------|-------------------|--------|
| M1      | parallel    | S1, S2, S3   | S2,S3 need S1 data | Yes (S1 first, then S2+S3 parallel) |
| M2      | parallel    | S1, S2, S3   | S2 needs S1; S3 needs S2 | Yes (S1 first, then S2, then S3) |

Both M1 and M2 launch simultaneously. They compete in parallel.

## Specs and Tests (Composability)

### M1-S1 Tests
- `test_plantri_counts`: Triangulation count matches OEIS A000109 for $n \leq 12$
- `test_all_5col_reducible_n10`: Every 5-colouring of every triangulation on $n \leq 10$ reaches a 4-colouring via Kempe swaps
- `test_reduction_path_exists`: BFS always finds a path (no isolated 5-colouring nodes)

### M1-S2 Tests
- `test_R5_connected`: $\mathcal{R}(T, 5)$ is connected for all $T$ on $n \leq 12$ (Las Vergnas-Meyniel)
- `test_R4_diameter_finite`: $\mathcal{R}(T, 4)$ has finite diameter for all tested $T$
- `test_spectral_gap_positive`: Kempe Markov chain has positive spectral gap

### M1-S3 Tests
- `test_disjoint_chains_noncrossing`: For all 4-colourings of $T$ on $n \leq 10$, chains for disjoint colour pairs never cross
- `test_fisk_group_structure`: Fisk group is $\mathbb{Z}_2^g$ for known examples
- `test_fisk_class_intersection`: Every Fisk class intersects the set of 4-colourings (if true → supports Plan 2)

### M2-S1 Tests
- `test_theorem_A_statement`: Statement is formally precise and matches computational observations from M1-S3
- `test_theorem_B_statement`: Statement covers all cases observed in M1 data
- `test_proof_no_gaps`: Every step is justified; no hidden assumptions

### M2-S2 Tests
- `test_case_count_matches_computation`: Number of topologically distinct cases matches M1's enumeration
- `test_each_case_resolved`: Each case has either a swap sequence or is provably impossible (the latter would kill Plan 2)
- `test_exhaustiveness`: Classification covers all possible configurations

### M2-S3 Tests
- `test_lemma_consistent_with_M1_data`: The ordering strategy works on all M1-S1 test cases
- `test_no_circular_dependencies`: The recolouring of $v_i$ doesn't depend on later $v_j$
- `test_proof_structure_sound`: Induction/ordering argument is valid

## Complexity Estimate

**High.** This is attacking an open mathematical problem (Kempe reconfiguration from 5-colourings to 4-colourings in planar graphs). Computational work is tractable for small $n$. Theoretical work may hit fundamental obstacles. The iterative competition structure maximizes the chance of either (a) finding a proof sketch, or (b) identifying exactly where the proof breaks down.

**Expected outcomes:** At minimum: computational verification for $n \leq 12$, precise non-crossing theorems, and a degree-5 case classification. At best: a viable proof strategy for the Colour Elimination Lemma.

# Task Decomposition — Agent 1443

## Original Task
Formalize in production-quality Python code a suite of physical analogy energy functionals for the Kempe chain reconfiguration problem. Fix bugs in the prototype `physical_analogies.py`, integrate with the existing NetworkX-based kempe codebase, test all metrics on real counterexamples T_9_25 and T_9_35 (discovered by Agent 1419), add new physical models (electric charge flow, protein folding ruggedness, surface tension, entropy), generate analysis figures, and produce a synthesis report evaluating which physical analogies actually predict the BFS path behavior observed computationally.

## Atomic Subtasks

1. Fix Magic Gem self-contribution bug (vertex's own color missing from center-of-mass)
2. Add NetworkX compatibility layer to physical_analogies.py
3. Implement surface tension energy functional
4. Implement local curvature / entropy metrics
5. Implement defect-defect interaction energy
6. Implement electric field gradient metric (discrete Laplacian potential difference)
7. Load T_9_25 and T_9_35 counterexample graphs and their merge-prone colorings from existing code
8. Compute all energy metrics on the 48 counterexample colorings
9. Compare energy profiles: safe paths vs unsafe (optimal) paths at the counterexamples
10. Compute energy metrics along full BFS paths (safe and unsafe) for counterexample colorings
11. Generate matplotlib figures: energy barrier profiles, safe vs unsafe comparison
12. Generate updated interactive web figures for SpinGlassSwapApp with real data
13. Write synthesis report: which metrics predict the forced-unsafe behavior?
14. Unit tests for all new energy functions

## Dependency Graph

```
S1,S2,S3,S4,S5,S6 (all independent — pure functions)
        ↓
S7 (load counterexamples — independent of above but needed by S8-S10)
        ↓
S8,S9,S10 (depend on S1-S7)
        ↓
S11,S12 (depend on S8-S10)
        ↓
S13 (depends on everything)
S14 (independent — can run after S1-S6)
```

## Stream Allocation

| Manager | Stream Type | Subtasks | Dependencies | Async? |
|---------|-------------|----------|--------------|--------|
| M1      | parallel    | S1-S6 (Fix bugs, add new energy functionals) + S14 (tests) | None | Yes |
| M2      | parallel    | S7-S10 (Counterexample integration + energy computation) | Needs M1 output | After M1 |
| M3      | parallel    | S11-S13 (Figures + synthesis report) | Needs M2 output | After M2 |

## Complexity Estimate

**Medium.** The core mathematical functions are straightforward. The main risk is integration with the existing kempe codebase (NetworkX graph format, triangulation_db API, coloring format). The counterexample loading (S7) is the linchpin — if the existing code can't easily export T_9_25/T_9_35 colorings, M2 will need to reconstruct them.

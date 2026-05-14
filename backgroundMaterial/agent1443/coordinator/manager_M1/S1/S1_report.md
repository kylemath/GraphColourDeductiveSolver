# M1-S1 Report: Bug Fixes + New Energy Functionals

**Agent:** 1443-M1-S1  
**Status:** COMPLETE

## Bug Fix: Magic Gem Center-of-Mass

**Issue:** `compute_local_magic_gem_energy` computed center-of-mass over neighbors only, excluding the vertex's own color vector. This underestimated frustration for color-5 vertices (since color 5 maps to the origin, excluding it biased the center-of-mass away from zero).

**Fix:** Now computes center-of-mass over `[vertex] + neighbors`. For a color-5 vertex, including the origin pulls the center-of-mass toward zero, but with unbalanced neighbors the energy remains nonzero.

**Verification:** Unit test `test_bugfix_vertex_included` confirms color-5 vertex has nonzero local energy even with balanced neighbors.

## New Energy Functionals

| Function | Description | Validated |
|---|---|---|
| `compute_surface_tension` | Boundary edges between chain and foreign-color vertices | ✓ |
| `compute_local_entropy` | Shannon entropy of neighbor color distribution | ✓ |
| `compute_defect_interaction` | Pairwise exponential-decay interaction between color-5 vertices | ✓ |
| `compute_electric_field_gradient` | Max potential difference between vertex and neighbors | ✓ |

## NetworkX Wrappers

All 8 original + new functions have `_nx` suffix wrappers that accept `nx.Graph` objects. Internally convert via `_nx_to_adj()`.

## Helper Functions

- `_bfs_distance(graph_adj, source, target)` — BFS shortest path for defect interaction
- `_nx_to_adj(G)` — Convert nx.Graph to Dict[int, List[int]]

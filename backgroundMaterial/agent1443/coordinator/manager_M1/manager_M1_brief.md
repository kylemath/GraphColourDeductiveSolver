# Manager M1 Brief — Fix & Extend `physical_analogies.py`

**Agent:** 1443-M1  
**Stream:** Fix + Extend Energy Functionals  
**Status:** Active  
**Dependencies:** None (parallel start)

## Objective

Fix bugs and extend `/compute/kempe/physical_analogies.py` with production-quality energy functionals, add NetworkX compatibility wrappers, and write comprehensive unit tests.

## Sub-subagent Allocation

| Sub-subagent | Task | Output |
|---|---|---|
| S1 | Bug fixes + new energy functionals | Updated `physical_analogies.py`, `S1_report.md` |
| S2 | Unit tests on K4 + octahedron | `tests/test_physical_analogies.py`, `S2_report.md` |

## S1 Deliverables

### Bug Fix
- `compute_local_magic_gem_energy`: must include the vertex's own color in center-of-mass calculation. Currently only averages neighbors — should include vertex itself.

### NetworkX Compatibility
- Add `_nx` suffix wrappers accepting `(nx.Graph, Dict[int,int])` and converting to internal `graph_adj` format.

### New Energy Functionals
1. **`compute_surface_tension(graph_adj, coloring, kempe_chain, color_a, color_b)`** — boundary edges between chain and non-chain vertices of other colors
2. **`compute_local_entropy(graph_adj, coloring, vertex)`** — Shannon entropy of neighbor color distribution
3. **`compute_defect_interaction(graph_adj, coloring)`** — pairwise exponential-decay interaction between color-5 vertices via BFS distance
4. **`compute_electric_field_gradient(graph_adj, coloring, vertex)`** — max electrostatic potential difference between vertex and its neighbors

## S2 Deliverables

### Unit Tests
- Test every function on K4 and octahedron graphs
- Verify known mathematical properties (e.g., balanced coloring → zero energy)
- Test edge cases (empty graph, single vertex)

## Virtual Environment
```bash
source /Users/kylemathewson/GraphColour/.venv/bin/activate
```

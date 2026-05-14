# Manager M2 Brief — Counterexample Integration & Energy Computation

**Agent:** 1443-M2  
**Stream:** Load counterexamples, compute energy metrics  
**Status:** Pending (awaits M1)  
**Dependencies:** M1 must complete (extended `physical_analogies.py`)

## Objective

Load the real counterexample graphs T_9_25 and T_9_35 from the triangulation database, identify their merge-prone colorings where $v$ is colored 5, and compute all physical analogy energy metrics. Compare safe vs unsafe Kempe swap paths.

## Sub-subagent Allocation

| Sub-subagent | Task | Output |
|---|---|---|
| S1 | Load counterexamples + compute energy metrics | `counterexample_energy_analysis.py`, `S1_report.md` |
| S2 | Compare safe vs unsafe path energies | Energy comparison data, `S2_report.md` |

## How to Load Counterexamples
```python
import sys
sys.path.insert(0, '/Users/kylemathewson/GraphColour/compute/kempe')
from triangulation_db import generate_triangulations
from kempe_ops import enumerate_colourings, num_colours, get_kempe_chain, canonical_form
from counterexample_analysis import dump_graph_structure

db = generate_triangulations(9)
T_9_25 = db[9][25]
T_9_35 = db[9][35]
```

## Metrics to Compute (per merge-prone coloring)

1. Global Magic Gem energy
2. Electrostatic potential at $v$ and its neighbors
3. Local entropy at $v$
4. Potts energy
5. For each unsafe $(a,5)$-chain: ruggedness + surface tension
6. Same metrics for safe alternative paths (distance opt+1)

## Key Counterexample Facts
- **T_9_25:** vertex $v=3$ (degree 5) — all optimal BFS paths are unsafe
- **T_9_35:** vertex $v=6$ (degree 4) — all optimal BFS paths are unsafe
- Both graphs have safe non-optimal paths at distance opt+1

## Virtual Environment
```bash
source /Users/kylemathewson/GraphColour/.venv/bin/activate
```

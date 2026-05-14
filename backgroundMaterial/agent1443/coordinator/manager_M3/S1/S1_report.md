# M3-S1 Report: Figure Generation

**Agent:** 1443-M3-S1  
**Status:** COMPLETE

## Figures Generated

All saved to `backgroundMaterial/agent1443/deliverables/`:

| Figure | Filename | Description |
|---|---|---|
| 1a | `safe_vs_unsafe_energy_bars_T_9_25.png` | 6-panel bar chart: mean ± std of each metric, safe vs unsafe |
| 1b | `safe_vs_unsafe_energy_bars_T_9_35.png` | Same for T_9_35 |
| 2a | `energy_barrier_profile_T_9_25.png` | 4-panel energy trajectory: MG, Potts, Entropy, |V_5| along BFS steps |
| 2b | `energy_barrier_profile_T_9_35.png` | Same for T_9_35 |
| 3a | `electrostatic_heatmap_T_9_25.png` | Spring-layout graph with nodes colored by electrostatic potential |
| 3b | `electrostatic_heatmap_T_9_35.png` | Same for T_9_35 |

## Style
- Dark theme (`#1a1a2e` background, `#16213e` axes)
- Unsafe paths: coral red (`#ff6b6b`)
- Safe paths: teal green (`#00d4aa`)
- Individual traces at 15% opacity with bold mean overlay
- DPI 150 for publication quality

## Script
`compute/kempe/generate_energy_figures.py` — fully self-contained, regenerable.

# Manager M3 Brief — Figures & Synthesis Report

**Agent:** 1443-M3  
**Stream:** Visualization + Synthesis  
**Status:** Pending (awaits M2)  
**Dependencies:** M2 must complete (energy computation results)

## Objective

Generate publication-quality matplotlib figures visualizing the energy analysis results, and write a synthesis report evaluating which physical analogies predict the forced-unsafe behavior.

## Sub-subagent Allocation

| Sub-subagent | Task | Output |
|---|---|---|
| S1 | Generate figures | `deliverables/*.png` |
| S2 | Write synthesis report | `deliverables/synthesis.md` |

## Figure Specifications

All saved to `/backgroundMaterial/agent1443/deliverables/`:

1. **`safe_vs_unsafe_energy_bars.png`** — Bar chart comparing energy metric values for safe vs unsafe paths on T_9_25
2. **`energy_barrier_profile.png`** — Energy along BFS path: safe path vs unsafe path overlay
3. **`electrostatic_heatmap.png`** — Electrostatic potential mapped onto graph node positions

## Synthesis Report (`synthesis.md`)

Must evaluate:
- Which physical analogies actually predict the forced-unsafe behavior?
- Which metrics distinguish safe from unsafe paths?
- What does this tell us about the topology of the reconfiguration graph?
- Probability assessment: can any physical model lead to a proof of Conjecture 5.5'?
- Feasibility rating with explicit Low / Medium-Low / Medium / Medium-High / High scale

## Style
- Dark theme matplotlib with consistent color palette
- Mathematical notation in axis labels where appropriate
- Error bars or confidence intervals where applicable

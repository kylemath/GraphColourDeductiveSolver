# Manager M2 Brief — Lean 4 Compiler + Infrastructure

## Agent: 1419-M2
## Role: Lean 4 formalization, compilation, and formal equivalence analysis

## Subtask S1: Get Lean 4 Code Building Against Mathlib

**Objective:** Attempt to compile existing Lean 4 code at `lean4/KempeReconfiguration/`.

**Steps:**
1. `cd lean4/KempeReconfiguration && lake update && lake build`
2. Fix any tactic or API compatibility issues
3. Report: what compiled, what needed fixing, what doesn't work

**Acceptance criteria:**
- Document every compilation error and its resolution (or why it can't be resolved)
- Final sorry count and axiom count
- All 5 .lean files at least type-checked or errors fully documented

**Notes:**
- Current lakefile targets Mathlib v4.15.0
- Suspected issue: `kempeSwap_preserves_proper` in Basic.lean uses `Ne.symm` bare (should be `exact Ne.symm ...`)
- `Triangulation` class axiomatizes planarity — this is expected, not a bug

## Subtask S2: Define ReconfigurationGraph and BFS Distance in Lean 4

**Objective:** Tier 2 infrastructure — define the reconfiguration graph R(G,k) and BFS distance in Lean 4.

**Dependencies:** Requires Mathlib's `SimpleGraph.Connectivity`.

**Deliverables:**
- `ReconfigurationGraph.lean`: define R(G,k) as a SimpleGraph on colourings
- State Conjecture 5.5 (BFS Avoidance) as a Lean Prop
- State {1,2,3,4}-Swap Sufficiency as a Lean Prop

**Acceptance criteria:**
- Type-checks against Mathlib (0 sorry in definitions, sorry allowed in proofs)
- Clear comments linking Lean definitions to Python equivalents

## Subtask S3: Formal Equivalence Analysis

**Objective:** Investigate the logical relationship between:
- (a) 4CT: every planar graph is 4-colourable
- (b) BFS Avoidance (Conjecture 5.5)
- (c) {1,2,3,4}-Swap Sufficiency

**Questions:**
- Does (b) → (a) without additional assumptions?
- Does (a) → (b)? (Is BFS Avoidance a theorem of 4CT or an independent statement?)
- What is the relationship between (b) and (c)?

**Acceptance criteria:**
- Rigorous mathematical analysis (not code)
- Clear statement of what's proved vs conjectured
- Identify any hidden circularity in the proof architecture

## Output Paths:
- S1 report: `backgroundMaterial/agent1419/coordinator/manager_M2/sub_S1/S1_report.md`
- S2 report: `backgroundMaterial/agent1419/coordinator/manager_M2/sub_S2/S2_report.md`
- S3 report: `backgroundMaterial/agent1419/coordinator/manager_M2/sub_S3/S3_report.md`
- Manager report: `backgroundMaterial/agent1419/coordinator/manager_M2/manager_M2_report.md`

# Task Brief — 0050-M1 (Iteration 2)

**From:** 0050-C (Coordinator)
**To:** 0050-M1 (The Engineers — Computational Verification)
**Date:** 18 February 2026
**Iteration:** 2

---

## Context: Iteration 1 Results

Your team (M1) delivered a solid iteration 1:
- 12/12 tests passing
- Triangulation counts match OEIS A000109 for n <= 7
- R(T,5) connected for all T on n <= 6
- R(T,4) connected for all T on n <= 6, all single Fisk class
- All 5-colourings reduce to 4-colourings: max 2 swaps for octahedron
- Non-crossing verified at 1,848 vertices with 0 violations

M2 (the Mathematicians) delivered:
- Theorem A (Non-Interleaving): PROVED via Jordan Curve Theorem
- Theorem B (Confinement): PROVED
- Degree-5 classification: 8 types, ALL resolvable by <= 1 swap
- Colour Elimination Lemma: NOT PROVED -- Chain Disconnection Lemma identified as missing piece

KEY BOTTLENECK: The Chain Disconnection Lemma (CDL).

---

## Iteration 2 Tasks

### Task 1: Extend to n=7 and n=8

For each triangulation on n=7 (5 triangulations) and n=8 (14 triangulations):
- Enumerate all proper 5-colourings
- BFS for 5->4 reduction
- Track: max path length, hardest colouring, swap sequence details
- Record timing data

Acceptance criteria:
- All 5 triangulations on n=7 tested
- All 14 triangulations on n=8 tested (or document which infeasible + why)
- Max path lengths recorded per graph
- New test test_5col_to_4col_n7 added and passing
- New test test_5col_to_4col_n8 added

### Task 2: Computationally Test the CDL

Extend chain_disconnection.py. For each triangulation on n <= 7:
- For each 5-colouring with >= 2 vertices coloured 5
- For each vertex v coloured 5, simulate recolouring v to colour k
- For next vertex w (still coloured 5): can w be recoloured with ONLY safe swaps?
- Log ALL cases where restricted swaps fail
- Increase max_prep_swaps to 5 if needed

Acceptance criteria:
- CDL tested for all triangulations on n <= 7
- Method counts logged: direct / safe_swap / prep+swap / unsafe_needed
- Any unsafe_needed cases documented in detail
- New test test_chain_disconnection_n7 added and passing

### Task 3: Sequential Elimination Tracking

Extend sequential_eliminate in chain_disconnection.py:
- For each triangulation on n <= 7: test both restricted=True and restricted=False
- Record: success rate, which orderings work/fail, max swaps
- Compare restricted vs unrestricted

Acceptance criteria:
- Sequential elimination tested for all 5-colourings with >= 2 colour-5 vertices
- Restricted vs unrestricted comparison documented
- Any ordering-dependent failures logged
- New test test_sequential_elimination_n7 added

### Task 4: R(G,5) Distance Analysis

Compute distance in R(G,5) from each 5-colouring to nearest 4-colouring:
- For n <= 7: exact distances via BFS
- Track: mean distance, max distance, farthest colouring

Acceptance criteria:
- Distance data computed for all triangulations on n <= 7
- Max distance and hardest colouring recorded per graph
- Results in manager report

---

## Competition: You WIN if you find hard cases M2 can't explain.

## File Paths
- Python code: /Users/kylemathewson/GraphColour/compute/kempe/ -- EXTEND existing modules
- Tests: /Users/kylemathewson/GraphColour/compute/kempe/tests/test_plan2.py -- ADD tests
- Report: /Users/kylemathewson/GraphColour/backgroundMaterial/agent0050/coordinator/manager_M1/manager_M1_report.md

## Constraints
- Python venv: /Users/kylemathewson/GraphColour/.venv
- Dependencies: networkx, numpy, standard library ONLY
- All existing 12 tests must still pass

# Task Brief — Manager 0051-M1 ("The Surgeons")

**From:** Coordinator 0051-C
**To:** Manager 0051-M1
**Date:** 18 February 2026

---

## Task

Surgically close Conjecture 5.4 through local analysis and computational deepening. Three parallel sub-workers:

### S1: Local Merge Analysis
- For each degree d ∈ {3,4,5}: characterize EXACTLY when adding vertex v (coloured 5) merges two (a,5)-chains
- v is IN B_{a,5}. Its edges to neighbours coloured a connect to existing chains. Merge iff v bridges 2+ distinct chains.
- **Deliverable:** Lemma characterizing merge conditions per degree, with proof or disproof
- **Tests:** `test_merge_conditions_degree3`, `test_merge_conditions_degree4`, `test_merge_conditions_degree5`

### S2: Push to n=10
- Generate all 233 triangulations on 10 vertices via triangulation_db.py
- Verify d ≤ n-4 = 6 via bulk_distance_to_4col
- If full computation too slow: sample ≥50 of 233 and report timing
- **Tests:** `test_triangulation_count_n10`, `test_distance_bound_n10`

### S3: BFS Path Merge Forensics
- For ALL general (a,5)-chains that DO merge (~18% rate): study their structure
- Compare BFS-selected chains vs merge-prone chains
- **Deliverable:** Structural characterization of what makes BFS chains merge-safe

## Acceptance Criteria
- [ ] Merge conditions characterized with proofs for each degree
- [ ] n=10 triangulations generated and verified (or sampled with timing)
- [ ] Structural distinction between merge-safe and merge-prone chains identified
- [ ] All new tests pass alongside existing 23

## Output Location
- Code: `/Users/kylemathewson/GraphColour/compute/kempe/`
- Tests: extend `tests/test_plan2.py`
- Reports: `/Users/kylemathewson/GraphColour/backgroundMaterial/agent0051/coordinator/manager_M1/`

## Context
- General (a,5)-chain merge rate: ~18% (confirmed by quick sampling at n=8)
- BFS-path merge rate: 0/518 = 0% (Agent 0050's data)
- The gap between 18% general and 0% BFS is the mystery to explain

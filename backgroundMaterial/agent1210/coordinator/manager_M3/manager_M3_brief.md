# Manager 1210-M3 Brief: The Computationalists

**Stream:** M3 — Computation, Pattern Analysis, Alternative Architectures
**Priority:** 20%
**Manager ID:** 1210-M3

---

## Goal

Push computational verification to n=11 (1,249 triangulations), analyze patterns in BFS avoidance data, and explore alternative proof architectures that bypass chain lifting entirely.

## Mathematical Context

### Current Computational State

| $n$ | Triangulations | Status |
|-----|----------------|--------|
| 4-8 | 23 | Fully verified (distance, BFS avoidance, merge analysis) |
| 9 | 50 | Fully verified |
| 10 | 233 | Fully verified (distance bounds) |
| **11** | **1,249** | **NOT YET TESTED** |

- Total colourings verified: ~2,325,920
- Max distance to 4-colouring: always $\leq n-4$ (tight for $n \leq 8$, not tight for $n \geq 9$)
- BFS Avoidance: 0/1,104 merge-prone cases had BFS select adjacent chain

### Known Counts (OEIS A000109)

$n=4:1, n=5:1, n=6:2, n=7:5, n=8:14, n=9:50, n=10:233, n=11:1249$

### Performance Baseline

- n=10 (233 triangulations): ~150s for `test_distance_bound_n10`
- n=11 will have ~5.4x more triangulations, each with more colourings
- Rough estimate: 15-60 minutes depending on colourings per graph

---

## Your Sub-subagent Allocation

Spawn 3 sub-subagents as Task subagents (parallel):

### S1: Scale Engineer
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M3/sub_S1/`
**Task:** Extend computation to n=11.

**Deliverables:**
1. Verify `generate_triangulations(11)` produces 1,249 triangulations
2. Run `bulk_distance_to_4col()` on ALL n=11 triangulations
3. Verify max distance $\leq n-4 = 7$
4. Report timing and memory usage
5. If any triangulation fails (unreachable colouring or distance > 7), this is a POTENTIAL COUNTEREXAMPLE — document it precisely with graph structure, colouring, and BFS trace

**Optimization strategies to consider:**
- Process triangulations in parallel (multiprocessing)
- Save intermediate results to avoid re-computation on interruption
- Sample first (random 100 of 1249) to estimate difficulty, then run all
- Profile bottlenecks: is it enumeration, BFS, or isomorphism checking?

**Codebase:** `/Users/kylemathewson/GraphColour/compute/kempe/`
**Venv:** `source /Users/kylemathewson/GraphColour/.venv/bin/activate`

### S2: Pattern Analyst
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M3/sub_S2/`
**Task:** Deep statistical analysis of BFS avoidance data at n=10 (and n=11 if S1 completes).

**Questions to answer:**
1. What is the distribution of BFS path lengths by graph and by vertex degree?
2. How many merge-prone cases per triangulation? Per vertex? Is there a structural predictor?
3. What structural properties of triangulations predict merge rate? (connectivity, min degree, girth, etc.)
4. Does the n-4 bound get tighter or looser as n grows? Extrapolate the trend.
5. For merge-prone cases: what is the distribution of chain sizes? Are merge-prone chains systematically larger?
6. Run `bfs_path_merge_check()` on n=10 triangulations (or a sample) and compile statistics

**Write analysis as a formal report with tables and conclusions.**

### S3: Alternative Architect
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M3/sub_S3/`
**Task:** Explore proof strategies that bypass chain lifting entirely.

**Three candidates to analyze:**

1. **Direct BFS diameter bound using expansion arguments**
   - The algebraic connectivity $\lambda_2 \geq 2.0$ (observed for all $n \leq 8$)
   - If $\lambda_2 \geq c > 0$ universally, then $\text{diam}(\mathcal{R}(G,5)) = O(n^2)$
   - Question: can we prove a universal lower bound on $\lambda_2$ for planar graphs?
   - This would give a polynomial (not linear) distance bound — weaker but gap-free

2. **Greedy algorithm with temporary detours**
   - $|V_5|$ descent works ~70-77% of the time
   - Could a 2-step lookahead or detour strategy achieve 100%?
   - The $|V_5|$ descent fails for 23-33% of colourings — is there a structural characterization of "resistant" colourings?

3. **Las Vergnas-Meyniel connectivity used more directly**
   - LVM proved $\mathcal{R}(G,5)$ is connected for planar $G$
   - Their proof uses vertex ordering + sequential extension
   - Can their technique give a diameter bound directly?
   - Their proof might already contain the key step that avoids merge-prone chains

**For each candidate: write a feasibility analysis with rating (Low / Medium-Low / Medium / Medium-High / High).**

---

## Codebase Reference

| Module | Location | Key Functions |
|--------|----------|---------------|
| kempe_ops.py | `compute/kempe/kempe_ops.py` | `enumerate_colourings()`, `all_kempe_neighbours()` |
| triangulation_db.py | `compute/kempe/triangulation_db.py` | `generate_triangulations(max_n)` |
| reduction_search.py | `compute/kempe/reduction_search.py` | `bfs_reduce_to_4()`, `bulk_distance_to_4col()` |
| merge_analysis.py | `compute/kempe/merge_analysis.py` | `bfs_path_merge_check()`, `bulk_merge_analysis()` |
| reconfiguration_graph.py | `compute/kempe/reconfiguration_graph.py` | `build_reconfiguration_graph()` |

All paths relative to `/Users/kylemathewson/GraphColour/`.

---

## Report Format

Write `manager_M3_report.md` using:

```
# Manager 1210-M3 Report
**Stream:** The Computationalists
**Status:** Complete / In Progress / Blocked

## Stream Summary
## Sub-subagent Status
| Sub-subagent | Task | Status | Key Finding |
|---|---|---|---|
| S1 | Scale (n=11) | ... | ... |
| S2 | Pattern Analysis | ... | ... |
| S3 | Alternative Architectures | ... | ... |

## Collected Outputs
## n=11 Results Summary
## Pattern Analysis Conclusions
## Alternative Architecture Feasibility
## Escalated Questions
## Issues Encountered
## Self-Assessment
```

---

## CRITICAL INSTRUCTIONS

1. **If ANY failure is found at n=11**, this is a potential counterexample — the most important finding of the entire project. Document it with complete detail and escalate immediately.
2. **S1 should start with timing estimates** before committing to full runs. If n=11 will take >2 hours, use sampling first.
3. **S2's pattern analysis** should specifically look for structural predictors that M1 and M2 can use as proof ingredients.
4. **S3's alternative architectures** are insurance — if BFS Avoidance turns out to be as hard as 4CT, we need backup strategies.
5. **Never install packages globally** — always use `source /Users/kylemathewson/GraphColour/.venv/bin/activate`

# Manager M1 Brief — Destroyer + Data Miner

## Agent: 1419-M1
## Role: Computational testing, adversarial attack, and data mining

## Subtask S1: Extend BFS Avoidance to n=9, 10

**Objective:** Run `bfs_path_merge_check()` on ALL degree-≤5 vertices across all triangulations at n=9 (50 graphs) and n=10 (233 graphs).

**Acceptance criteria:**
- Report total (a,5)-swaps examined, merge-prone cases, and BFS avoidance rate
- If ANY merge is found → HARD KILL with counterexample details
- Compare merge-prone rates at degree 4 vs degree 5 across graph sizes

**Infrastructure:** Use `compute/kempe/merge_analysis.py::bfs_path_merge_check()` and `triangulation_db.py::generate_triangulations()`.

## Subtask S2: New Adversarial Attacks at n=9-12

**Objective:** Three new attack vectors beyond the existing 5:
- Attack 6: Forced single-path — find graphs where R(G-v,5) has unique shortest path through unsafe swap
- Attack 7: High-merge-rate construction — maximize the fraction of merge-prone chains at degree 5
- Attack 8: Algebraic/Fisk obstruction — look for Fisk-class separation that forces unsafe swaps

**Acceptance criteria:**
- Each attack either produces a counterexample (→ HARD KILL) or documents why it fails
- Run at n=9-12 where feasible (n=11: 1249 graphs, n=12: 7595 — may need sampling)

## Subtask S3: ALL-PATHS Analysis (GATING ITEM)

**Objective:** For each merge-prone case at n≤8, enumerate ALL BFS-optimal paths (not just first). Classify:
1. Do ALL optimal paths avoid unsafe swaps? Or do SOME use them?
2. For each merge-prone case, record which alternative swap BFS chose and classify it

**Acceptance criteria:**
- Complete census at n=6,7,8 (2 + 5 + 14 = 21 triangulations)
- For each merge-prone case: count total optimal paths, count safe-only paths, count paths using unsafe swaps
- Classification of alternative swaps: {1,2,3,4}-swap? Which pair? Safe (a,5)-swap?

**CRITICAL:** This determines whether Wave 2 proves "all paths avoid" or "some path avoids". The entire proof architecture depends on this answer.

## Output Paths:
- S1 report: `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md`
- S2 report: `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S2/S2_report.md`
- S3 report: `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S3/S3_report.md`
- Manager report: `backgroundMaterial/agent1419/coordinator/manager_M1/manager_M1_report.md`

# Manager 1210-M1 Brief: The Proof Hunters (Degree 4 BFS Avoidance)

**Stream:** M1 — Degree 4 BFS Avoidance
**Priority:** 70% (shared with M2)
**Manager ID:** 1210-M1

---

## Goal

Prove Conjecture 5.5 (BFS Avoidance) for deg(v) = 4. This is the easier of the two remaining cases, and a proof here would provide insights for the degree-5 case.

## Mathematical Context

### The Conjecture

**Conjecture 5.5 (BFS Avoidance):** Let $G$ be a planar graph, $v$ a vertex with $c(v) = 5$ and $\deg(v) = 4$. In $G - v$, suppose $v$ bridges $\geq 2$ distinct $(a,5)$-Kempe chains (i.e., $v$ has neighbours in two different chains). Then any BFS-optimal path in $\mathcal{R}(G-v, 5)$ from $c|_{G-v}$ to a 4-colouring does NOT swap any chain adjacent to $v$.

### Key Facts for Degree 4

1. **Link structure:** The link of a degree-4 vertex in a triangulation is a 4-cycle $C_4$. Label neighbours $u_1, u_2, u_3, u_4$ in cyclic order. Then $u_1 u_2, u_2 u_3, u_3 u_4, u_4 u_1 \in E(G)$, but $u_1 u_3, u_2 u_4 \notin E(G)$.

2. **Why degree 3 is easy:** At degree 3, the link is $K_3$ (a triangle), so all three neighbours are pairwise adjacent. This means any two neighbours in $B_{a,5}$ must be in the same $(a,5)$-chain (they share an edge). Hence no merges. The Degree-3 No-Merge Lemma (Lemma 5.2) is PROVED.

3. **Why degree 4 is harder:** In $C_4$, opposite vertices ($u_1, u_3$ or $u_2, u_4$) are NOT adjacent. So if $c(u_1) \in \{a, 5\}$ and $c(u_3) \in \{a, 5\}$, they COULD be in different $(a,5)$-chains.

4. **Merge rate at degree 4:** Empirically ~17.4%. Merges CAN happen, BFS just avoids them.

5. **Evidence:** 0 counterexamples in 1,104 merge-prone cases across 13,876 BFS-path $(a,5)$-swaps (all tested at $n \leq 8$).

### The Proof Architecture (What's Already Proved)

```
Five Colour Theorem → proper 5-colouring c of G
    │
    ├── Case 1: c(v) ≠ 5 → Chain Lifting [PROVED] → distance ≤ n-5 ✓
    ├── Case 2: c(v) = 5, deg(v) = 3 → Degree-3 No-Merge [PROVED] → distance ≤ n-4 ✓
    └── Case 3: c(v) = 5, deg(v) ∈ {4, 5} → Needs BFS Avoidance [THIS IS YOUR CASE for deg 4]
```

### Six Proved Lemmas

1. **Theorem A (Non-Interleaving):** Kempe chains for disjoint colour pairs don't interleave in cyclic neighbour order
2. **Theorem B (Confinement):** $(a,b)$-chain structure invariant under swaps on colours disjoint from $\{a,b\}$
3. **Never-Revert Lemma:** Swapping $a \leftrightarrow b$ with $a,b \in \{1,2,3,4\}$ never creates/destroys colour-5 vertices
4. **Chain Lifting:** When $c(v) = 5$, the $(a,b)$-bichromatic subgraph ($a,b \in \{1,2,3,4\}$) is identical in $G$ and $G-v$
5. **Degree-5 Classification:** 8 topologically distinct colour patterns, all resolvable by $\leq 1$ Kempe swap
6. **Degree-3 No-Merge:** Adding back a degree-3 vertex coloured 5 never merges $(a,5)$-chains

---

## Your Sub-subagent Allocation

You MUST spawn 3 sub-subagents as Task subagents (parallel):

### S1: Link Structure Analyst
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M1/sub_S1/`
**Task:** Fully characterize the degree-4 link ($C_4$). Enumerate ALL possible $(a,5)$-chain configurations at a degree-4 vertex. How many topologically distinct merge-prone cases exist? Can you classify them by the colour pattern of the 4 neighbours? Write formal analysis.

**Key questions S1 must answer:**
- Given $v$ with $c(v)=5$, $\deg(v)=4$, neighbours $u_1,...,u_4$ in cyclic order: what are all possible colourings of $N(v)$ that create a merge-prone situation?
- How does the planarity (the $C_4$ structure) constrain which pairs of neighbours can be in different chains?
- What is the exact relationship between merge-proneness and the colour pattern?

### S2: BFS Path Strategist
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M1/sub_S2/`
**Task:** Study WHY BFS avoids merge-prone chains. Key questions:
- When $v$ bridges 2+ chains, does BFS always have a shorter/equal-length alternative path that routes around $v$'s neighbourhood?
- Are merge-prone chains structurally "large" while BFS prefers "small" local swaps?
- Can you prove that any merge-prone chain has strictly more vertices than some alternative chain that achieves the same colour elimination?
- Study the structure of shortest paths in $\mathcal{R}(G-v, 5)$. What makes a chain "BFS-attractive" vs "BFS-avoidable"?
- Consider the Confinement theorem (Theorem B): does it imply that BFS can always achieve the same effect without touching merge-prone chains?

### S3: Red Team / Adversarial
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M1/sub_S3/`
**Task:** Try to BREAK BFS Avoidance at degree 4. This is the most important sub-subagent. Specifically:
- Construct graph configurations where BFS MUST use a merge-prone chain (or prove it can't)
- What is the minimum graph size where BFS avoidance at degree 4 could fail?
- If you can't break it, document exactly WHY each attack fails — those failure reasons ARE the proof ingredients
- Consider: is BFS Avoidance at degree 4 equivalent to 4CT itself? If proving it is as hard as proving 4CT, document the precise reduction.
- Run `bfs_path_merge_check()` on custom-constructed adversarial graphs

**CRITICAL: S3 should use the existing codebase at `/Users/kylemathewson/GraphColour/compute/kempe/`. Always activate the venv first: `source /Users/kylemathewson/GraphColour/.venv/bin/activate`**

---

## Codebase Reference

| Module | Location | Key Functions |
|--------|----------|---------------|
| kempe_ops.py | `/Users/kylemathewson/GraphColour/compute/kempe/kempe_ops.py` | `get_kempe_chain()`, `kempe_swap()`, `enumerate_colourings()`, `all_kempe_neighbours()` |
| triangulation_db.py | `/Users/kylemathewson/GraphColour/compute/kempe/triangulation_db.py` | `generate_triangulations()`, `make_K4()`, `make_octahedron()` |
| reduction_search.py | `/Users/kylemathewson/GraphColour/compute/kempe/reduction_search.py` | `bfs_reduce_to_4()`, `bulk_distance_to_4col()`, `verify_inductive_lift()` |
| merge_analysis.py | `/Users/kylemathewson/GraphColour/compute/kempe/merge_analysis.py` | `analyze_merge_conditions()`, `bfs_path_merge_check()` |
| tests | `/Users/kylemathewson/GraphColour/compute/kempe/tests/test_plan2.py` | 31 tests, all passing |

**Key data types:**
```python
Colouring = Dict[int, int]           # vertex → colour (1..5)
CanonicalColouring = Tuple[int, ...]  # hashable form
```

---

## Report Format

Write `manager_M1_report.md` in your folder using:

```
# Manager 1210-M1 Report
**Stream:** The Proof Hunters (Degree 4 BFS Avoidance)
**Status:** Complete / In Progress / Blocked

## Stream Summary
## Sub-subagent Status
| Sub-subagent | Task | Status | Key Finding |
|---|---|---|---|
| S1 | Link Structure | ... | ... |
| S2 | BFS Path Strategy | ... | ... |
| S3 | Red Team | ... | ... |

## Collected Outputs
## Integration Notes
## Escalated Questions
## Issues Encountered
## Self-Assessment
**Craftsperson says:** ...
**Skeptic says:** ...
**Mover says:** ...
```

Each sub-subagent writes `S[n]_report.md` in their folder using:

```
# Sub-subagent 1210-M1-S[n] Report
**Task:** [one sentence]
**Status:** Complete / Needs Review / Blocked

## Work Product
## Files
| File | Description |
|---|---|
## Acceptance Criteria Check
## Questions for Manager
## Self-Assessment
**Craftsperson says:** ...
**Skeptic says:** ...
**Mover says:** ...
```

---

## CRITICAL INSTRUCTIONS

1. **DOUBLE CHECK all mathematical claims.** S3's entire job is to break things.
2. **If a counterexample is found**, immediately write it up with full details (graph, colouring, vertex, BFS path) and escalate.
3. **Cross-pollinate with M2** — if you find a degree-4 proof technique, note whether it could generalize to degree 5.
4. **Use the existing codebase** — don't reinvent. Activate venv: `source /Users/kylemathewson/GraphColour/.venv/bin/activate`
5. **The kill criterion** — if you conclude BFS Avoidance at degree 4 is equivalent to 4CT (proving it IS proving 4CT), document this precisely. That's a valuable reformulation, not a failure.

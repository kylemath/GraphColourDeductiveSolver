# Manager 1210-M2 Brief: The Summit Team (Degree 5 BFS Avoidance)

**Stream:** M2 — Degree 5 BFS Avoidance
**Priority:** 70% (shared with M1)
**Manager ID:** 1210-M2

---

## Goal

Prove Conjecture 5.5 (BFS Avoidance) for deg(v) = 5. This is the hardest case. If degree-4 proof techniques from M1 don't generalize, this may require fundamentally different ideas.

## Mathematical Context

### The Conjecture

**Conjecture 5.5 (BFS Avoidance):** Let $G$ be a planar graph, $v$ a vertex with $c(v) = 5$ and $\deg(v) = 5$. In $G - v$, suppose $v$ bridges $\geq 2$ distinct $(a,5)$-Kempe chains. Then any BFS-optimal path in $\mathcal{R}(G-v, 5)$ from $c|_{G-v}$ to a 4-colouring does NOT swap any chain adjacent to $v$.

### Key Facts for Degree 5

1. **Link structure:** The link of a degree-5 vertex in a triangulation is a 5-cycle $C_5$. Neighbours $u_1, ..., u_5$ in cyclic order with edges $u_i u_{i+1}$ but no other edges.

2. **Non-adjacent pairs:** In $C_5$, each vertex is non-adjacent to exactly 2 others (e.g., $u_1$ is non-adjacent to $u_3$ and $u_4$). This gives more opportunities for merge-prone configurations than at degree 4.

3. **Theorem A (Non-Interleaving):** Kempe chains for disjoint colour pairs don't interleave in the cyclic neighbour order at a vertex external to both chains (Jordan Curve Theorem). This is a CRUCIAL constraint at degree 5 — it limits which chain configurations are geometrically realizable.

4. **Merge rate at degree 5:** 30.9% — nearly double the degree-4 rate. Merges are COMMON, so BFS avoiding them is a STRONG property.

5. **Degree-5 Classification:** 8 topologically distinct colour patterns at a degree-$\leq 5$ vertex coloured 5. All resolvable by $\leq 1$ Kempe swap. These patterns constrain which merge-prone configurations can actually occur.

6. **Evidence:** 0 counterexamples across all tested cases at $n \leq 8$.

### The Proof Architecture (What's Already Proved)

```
Five Colour Theorem → proper 5-colouring c of G
    │
    ├── Case 1: c(v) ≠ 5 → Chain Lifting [PROVED]
    ├── Case 2: c(v) = 5, deg(v) = 3 → Degree-3 No-Merge [PROVED]
    └── Case 3: c(v) = 5, deg(v) ∈ {4, 5} → Needs BFS Avoidance
                                                └── deg(v) = 5 IS YOUR CASE
```

### Six Proved Lemmas

1. **Theorem A (Non-Interleaving):** Chains for disjoint colour pairs don't interleave in cyclic order
2. **Theorem B (Confinement):** $(a,b)$-chain structure invariant under swaps disjoint from $\{a,b\}$
3. **Never-Revert Lemma:** $\{1,2,3,4\}$-swaps don't create/destroy colour-5 vertices
4. **Chain Lifting:** $(a,b)$-chains ($a,b \in \{1,2,3,4\}$) identical in $G$ and $G-v$ when $c(v)=5$
5. **Degree-5 Classification:** 8 types, all resolvable by $\leq 1$ swap
6. **Degree-3 No-Merge:** Never merges $(a,5)$-chains at degree-3 vertices

---

## Your Sub-subagent Allocation

Spawn 3 sub-subagents as Task subagents (parallel):

### S1: Non-Interleaving Exploiter
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M2/sub_S1/`
**Task:** Use Theorem A to constrain which chains CAN be merge-prone at degree 5.

**Key questions:**
- Given $v$ with $\deg(v)=5$, $c(v)=5$, and the $C_5$ link structure, how many topologically distinct merge-prone configurations exist?
- Can non-interleaving alone reduce the number of merge-prone configurations to a small finite set?
- For each of the 8 degree-5 classification types, which ones can create merge-prone $(a,5)$-chains?
- Does the Jordan Curve Theorem (via non-interleaving) force merge-prone chains to have structural properties (e.g., large size, specific connectivity) that BFS can exploit?

**Write formal case analysis with proofs.**

### S2: Reconfiguration Path Analyst
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M2/sub_S2/`
**Task:** Study the structure of BFS-optimal paths in $\mathcal{R}(G-v, 5)$ specifically at degree-5 vertices.

**Key questions:**
- Is there a local certificate that guarantees a chain is NOT on any shortest path?
- If merge-prone chains have such a certificate, the conjecture follows.
- What is the relationship between chain size and BFS selection probability?
- Can the algebraic connectivity ($\lambda_2 \geq 2.0$ observed) be used to prove BFS paths avoid large/merge-prone chains?
- Does the "detour" around a merge-prone chain add at most 0 steps? (If so, BFS can always find an equally-short path avoiding it.)

### S3: Red Team / Adversarial
**Folder:** `/Users/kylemathewson/GraphColour/backgroundMaterial/agent1210/coordinator/manager_M2/sub_S3/`
**Task:** Try to BREAK BFS Avoidance at degree 5.

**Mandate:**
- Construct specific graph configurations where BFS MUST use a merge-prone chain at a degree-5 vertex
- Consider: the 30.9% merge rate means BFS is avoiding a LOT of chains. Is this sustainable as $n$ grows?
- If BFS Avoidance is equivalent to 4CT, document the precise reduction. This would mean our reformulation is tight — proving BFS Avoidance IS proving 4CT.
- If you can't break it, document each attack and WHY it fails. Those failure modes are proof ingredients.
- Run computational experiments using existing codebase

**CRITICAL: Use the existing codebase at `/Users/kylemathewson/GraphColour/compute/kempe/`. Activate venv: `source /Users/kylemathewson/GraphColour/.venv/bin/activate`**

---

## Codebase Reference

| Module | Location | Key Functions |
|--------|----------|---------------|
| kempe_ops.py | `/Users/kylemathewson/GraphColour/compute/kempe/kempe_ops.py` | `get_kempe_chain()`, `kempe_swap()`, `enumerate_colourings()` |
| triangulation_db.py | `/Users/kylemathewson/GraphColour/compute/kempe/triangulation_db.py` | `generate_triangulations()`, `make_icosahedron()` |
| reduction_search.py | `/Users/kylemathewson/GraphColour/compute/kempe/reduction_search.py` | `bfs_reduce_to_4()`, `bulk_distance_to_4col()` |
| merge_analysis.py | `/Users/kylemathewson/GraphColour/compute/kempe/merge_analysis.py` | `analyze_merge_conditions()`, `bfs_path_merge_check()` |
| noncrossing_verifier.py | `/Users/kylemathewson/GraphColour/compute/kempe/noncrossing_verifier.py` | `verify_noncrossing_exhaustive_5col()`, `classify_chain_config_at_vertex()` |

---

## Report Format

Write `manager_M2_report.md` using:

```
# Manager 1210-M2 Report
**Stream:** The Summit Team (Degree 5 BFS Avoidance)
**Status:** Complete / In Progress / Blocked

## Stream Summary
## Sub-subagent Status
| Sub-subagent | Task | Status | Key Finding |
|---|---|---|---|
| S1 | Non-Interleaving | ... | ... |
| S2 | Reconfiguration Paths | ... | ... |
| S3 | Red Team | ... | ... |

## Collected Outputs
## Integration Notes
## Cross-pollination with M1
## Escalated Questions
## Issues Encountered
## Self-Assessment
```

Sub-subagent reports: `S[n]_report.md` in their folders.

---

## CRITICAL INSTRUCTIONS

1. **This is the hardest case.** Don't underestimate it. 30.9% merge rate means BFS is performing an impressive selection feat.
2. **Exploit Non-Interleaving** — this is the most powerful constraint specific to planarity. If the proof exists, it likely goes through Theorem A.
3. **If M1 succeeds**, check whether their technique generalizes. If it doesn't, note why explicitly.
4. **If BFS Avoidance is equivalent to 4CT**, that's a clean reformulation result, not a failure. Document the reduction.
5. **The kill criterion** — if all three sub-subagents agree BFS Avoidance at degree 5 is as hard as 4CT itself, document this in your escalation and recommend the Coordinator pivot to alternative architectures.

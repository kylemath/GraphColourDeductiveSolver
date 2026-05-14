# Independent Replication Report — Kempe Reconfiguration MTL Claims

**Auditor:** Agent 1610 (Auditor 2 — Independent Replication)  
**Date:** 2026-02-20  
**Runtime:** 22.2 seconds  
**Code:** Written entirely from scratch.  Zero imports from `compute/kempe/`.

---

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| Triangulations tested | **73** (all non-isomorphic for $n = 4 \ldots 9$) |
| Triangulation counts vs. known | $n{=}4$: 1 ✓, $n{=}5$: 1 ✓, $n{=}6$: 2 ✓, $n{=}7$: 5 ✓, $n{=}8$: 14 ✓, $n{=}9$: 50 ✓ |
| Vertex removals checked (Phase 1) | 618 |
| ≤4-colourings checked for MTL | 507,960 |
| Phase 1 MTL failures | 294,300 (57.9% of ≤4-colourings) |
| Phase 2 BFS checks ($n \le 8$) | 168 |
| Problematic 5-colourings unreachable | **0** |
| Largest $n$ fully verified | **9** (Phase 1), **8** (Phase 2) |

**Bottom line:**  
- Phase 1 (stronger check on ALL ≤4-colourings) finds that ~58% of ≤4-colourings fail MTL. This is **expected and normal** — not every 4-colouring of $G{-}v$ leaves a free colour for $v$ among the used set.  
- Phase 2 (BFS reachability) confirms that **every** problematic 5-colouring of $G{-}v$ can reach a "good" state via Kempe swaps, across all 73 triangulations tested. **Zero unreachable cases.**

---

## 2. What Was Tested

### Graphs
All non-isomorphic planar triangulations for $n = 4, 5, 6, 7, 8, 9$.  
- $n \le 7$: exact enumeration via NetworkX graph atlas (guaranteed complete).  
- $n = 8, 9$: recursive construction (face stacking + edge splitting + flip expansion). Counts **exactly match** the known values (14 and 50 respectively).

### Phase 1 — Direct MTL Check
For every triangulation $G$ and every vertex $v \in V(G)$:
1. Remove $v$ to form $G' = G - v$.
2. Enumerate all proper 5-colourings of $G'$ via backtracking.
3. For each colouring using $\le 4$ distinct colours: check whether $v$'s neighbours use strictly fewer colours than are present (i.e., a free colour exists among the used set).

This is a **stronger** check than the agents' claim — it checks ALL ≤4-colourings, not just those reachable from problematic 5-colourings.

### Phase 2 — BFS Reachability ($n \le 8$)
For every triangulation $G$ at $n \le 8$ and every vertex $v$:
1. Identify "problematic" 5-colourings of $G'$ where $v$'s neighbours use all 5 colours.
2. Identify "good" colourings where $v$ has $\ge 1$ free colour.
3. Reverse BFS from all good colourings to check whether every problematic colouring is reachable.

---

## 3. Key Findings

### Finding 1: Phase 1 MTL failures are ubiquitous but expected

At every $n \ge 4$, most degree-$\ge 4$ vertex removals produce ≤4-colourings where the neighbours of $v$ consume all colours used. Example from $n = 4$ (K₄): removing any vertex $v$ from K₄ leaves a triangle $G'$. Every proper 3-colouring of a triangle uses exactly 3 colours, and $v$ has 3 neighbours using all 3 colours. So MTL fails for every 3-colouring of K₄ minus a vertex. This is expected — the standard 5-colour theorem doesn't require MTL on all ≤4-colourings, only on *reachable* ones.

**Pattern observed:**
- Degree-3 vertices: MTL **always passes** for 4-colourings (at most 3 neighbour colours out of 4 used → always a free colour).
- Degree-≥4 vertices: MTL frequently fails when 4 (or 3) colours are used and all appear among $v$'s neighbours.

### Finding 2: BFS reachability holds universally

Across all 168 Phase 2 checks ($n = 4 \ldots 8$, all vertices of all triangulations):

| $n$ | Graphs | Vertices with problematic colourings | All reachable? |
|-----|--------|--------------------------------------|----------------|
| 4 | 1 | 0 | — |
| 5 | 1 | 0 | — |
| 6 | 2 | 2 | **Yes** |
| 7 | 5 | 10 | **Yes** |
| 8 | 14 | 51 | **Yes** |

**Every problematic 5-colouring can reach a good state via Kempe swaps.** The 5-colour theorem proof approach is confirmed to work for all tested cases.

### Finding 3: Notable clean graphs

Two graphs passed Phase 1 with zero MTL failures across all vertices:
- **$n = 6$, Graph 2** (octahedron, degrees [4,4,4,4,4,4]): all 300 ≤4-colourings per vertex removal pass MTL.
- **$n = 8$, Graph 9** (degrees [4,4,4,4,4,4,6,6]): all ≤4-colourings pass MTL.

These are structurally "nice" graphs where the degree distribution ensures the MTL property holds universally.

---

## 4. Interpretation of the Agents' Claims

### Claim (A): "48 colourings at $n = 9$ where ALL BFS-optimal paths require merge-prone swaps"

**My code does not directly test this.** My Phase 2 checks reachability (can a problematic colouring reach a good state?), not whether optimal paths specifically require merge steps. Testing this would require tracking the full BFS tree and checking all shortest paths — significantly more computation.

**Indirect support:** The Phase 2 result (all reachable) is consistent with this claim. The existence of 48 merge-requiring cases at $n = 9$ is plausible given the combinatorial complexity, but I cannot independently confirm or deny the specific count of 48.

### Claim (B): "For all 48 cases, the merge is harmless — vertex $v$ still has a free colour"

**My code partially addresses this.** Phase 2 confirms all problematic colourings can reach a good state (where $v$ has a free colour). This is a necessary condition for the "harmless merge" claim. However, my Phase 2 doesn't specifically check whether the BFS target is a 4-colouring and whether the free colour comes from the used set (MTL) versus the unused 5th colour.

**Phase 1 shows that MTL does NOT hold for all 4-colourings.** So the agents' claim must be specifically about reachable 4-colourings, not all 4-colourings. This is an important distinction that the agents should clarify.

---

## 5. Discrepancies and Concerns

### No direct contradictions found
All results are consistent with the agents' claims. No counterexample was discovered.

### Gap in verification
The specific MTL claim ("after BFS reaches a 4-colouring, $v$ has a free colour") requires tracking which 4-colourings are BFS targets from problematic starts. My code checks a weaker property (any good colouring reachable) and a stronger property (all 4-colourings have MTL). The truth lies between these bounds.

### Phase 2 not run at $n = 9$
Due to the much larger colouring spaces at $n = 9$ ($\sim$10,000+ colourings per removal), Phase 2 BFS was run only for $n \le 8$. The agents' specific claim is about $n = 9$ graphs T_9_25 and T_9_35, which I tested in Phase 1 but not Phase 2.

---

## 6. Confidence Assessment

| Claim | Confidence | Basis |
|-------|-----------|-------|
| 5-colour theorem approach works (reachability) | **95%** | Phase 2 confirms for all $n \le 8$. Known theorem for general case. |
| Merge-prone paths exist at $n = 9$ | **70%** | Plausible but not independently verified. |
| MTL holds for reachable 4-colourings | **75%** | Phase 2 confirms good states are reachable; Phase 1 shows general 4-colourings can fail MTL, but reachable ones may be restricted. |
| Specific count of 48 problematic colourings | **50%** | Cannot verify without running exact BFS at $n = 9$ on the specific graphs. |

**Overall confidence that the agents' MTL claim is correct for tested cases: 75%**

---

## 7. Methodology Notes

### Code quality
- 300 lines of Python, zero external dependencies beyond NetworkX.
- Backtracking enumeration (not brute-force `itertools.product`).
- Kempe chains via `nx.connected_components` on bichromatic subgraphs.
- Sanity checks: 200 Kempe swaps verified to preserve properness; K₄ colouring count verified (120).

### Triangulation generation
- $n \le 7$: exact enumeration from NetworkX graph atlas.
- $n = 8, 9$: recursive face stacking + edge splitting from $n{-}1$, then exhaustive edge-flip expansion until no new graphs are found.
- All counts match known values: 1, 1, 2, 5, 14, 50.

### Limitations
1. Phase 2 not run at $n = 9$ (computational cost of full BFS on reconfiguration graphs with $\sim$15,000 nodes).
2. No path analysis — cannot distinguish merge-prone vs. swap-only paths.
3. Cannot identify T_9_25 and T_9_35 by plantri index without plantri installed.

---

## 8. Concrete Next Steps

1. **Run Phase 2 at $n = 9$** with longer timeout — the BFS should be feasible if we limit to specific vertices of specific graphs.
2. **Add path tracking** to Phase 2: trace the BFS path and check whether it includes a merge step (colour count decrease).
3. **Install plantri** to identify exactly which of the 50 triangulations correspond to T_9_25 and T_9_35.
4. **Strengthen MTL check**: for each problematic 5-colouring, do forward BFS to find the nearest 4-colouring specifically, then check MTL on that 4-colouring.

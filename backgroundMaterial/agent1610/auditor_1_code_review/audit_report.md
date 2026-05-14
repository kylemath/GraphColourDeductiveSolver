# Auditor 1 — Critical Code Review Report

**Date:** 2026-02-20
**Auditor:** Agent 1610 — Independent Code Auditor
**Scope:** 8 Python files in `compute/kempe/` plus 1 critical dependency (`reduction_search.py`)

---

## Executive Summary

I audited the codebase underlying four headline claims about the Four Colour Theorem. The core infrastructure (`kempe_ops.py`, `triangulation_db.py`, `reduction_search.py`) is **solid and likely correct**. The higher-level scripts have **no outright showstopper bugs** but contain **design-level weaknesses** that reduce confidence in the quantitative claims. The most concerning finding is that the "48 counterexamples" count depends on a **capped path enumeration** that could produce false positives, and the MTL claim inherits this uncertainty.

**Bottom line:** The code is competent and the mathematical machinery is correct, but the quantitative claims carry more uncertainty than the reports suggest.

---

## File-by-File Audit

---

### 1. `kempe_ops.py` — Core Kempe Chain Operations

**What it claims to do:** Provide proper colouring verification, Kempe chain extraction via BFS on bichromatic subgraphs, Kempe swap execution, colouring enumeration, and canonical form handling.

**Verdict: The logic is CORRECT.**

- `is_proper_colouring`: Checks vertex set equality and all edges — correct.
- `get_kempe_chain`: Standard BFS on the bichromatic subgraph. Validates starting vertex colour. Returns `frozenset`. Correct.
- `get_all_kempe_chains`: Iterates over all (a,b)-coloured vertices, extracts each chain once via visited set. Correct.
- `kempe_swap`: Creates new dict, swaps a↔b on chain vertices only. Non-mutating. Correct.
- `enumerate_colourings`: Backtracking with neighbour-colour pruning. Colours 1..k. Standard and correct for small $n$.
- `canonical_form` / `colouring_from_canonical`: Uses sorted vertex order for deterministic tuple ↔ dict conversion. Round-trip is exact. Correct.
- `all_kempe_neighbours`: Enumerates all Kempe swaps, deduplicates by canonical form. Correct.

**Bugs found:** None.
**Could output be misleading?** No.
**Confidence:** **HIGH** (95%)

---

### 2. `triangulation_db.py` — Triangulation Database

**What it claims to do:** Generate all planar triangulations (spherical) on 4..max_n vertices via face splitting + edge flipping with isomorphism deduplication.

**Verdict: Algorithm is CORRECT in principle. Cannot verify output counts without running.**

- `is_triangulation`: Checks $m = 3n - 6$ and planarity. For $n \ge 4$, this correctly characterises maximal planar graphs (which are 3-connected, hence triangulations of the sphere). Connectivity is implied by the edge count.
- `split_face`: Adds a vertex inside a triangular face. Preserves planarity and triangulation property. Correct.
- `flip_edge`: Standard diagonal flip. Validates adjacent faces are triangles, checks no multi-edge, verifies result is still a triangulation. Correct.
- `generate_triangulations`: Phase 1 (face splitting from $n-1$) + Phase 2 (edge flipping until stable). The flip graph of triangulations on $n$ vertices is connected (Wagner's theorem), so this reaches all triangulations. Isomorphism filtering via `nx.is_isomorphic` is exact.
- Comments claim OEIS A000109 counts: $n=9: 50$, $n=10: 233$. These match the known values.

**Bugs found:** None.
**Concerns:**
- No runtime assertion that the generated count matches OEIS. If the generation silently misses a triangulation, all downstream results are compromised. **Recommendation:** Add `assert len(result[9]) == 50` as a sanity check.
- Isomorphism filtering via `nx.is_isomorphic` is $O(n!)$ worst-case per pair, making generation slow but correct.

**Confidence:** **HIGH** (93%) — would be 98% with count assertions.

---

### 3. `reduction_search.py` — BFS for 5→4 Colour Reduction

**What it claims to do:** Find shortest Kempe swap paths from 5-colourings to 4-colourings in the reconfiguration graph.

**Verdict: CORRECT.**

- `bfs_reduce_to_4`: Standard BFS with canonical deduplication. Reconstructs path via parent pointers. Returns shortest path. Correct.
- `_identify_swap`: Identifies the 2-colour pair involved in a single Kempe swap step by collecting colours of changed vertices. Returns `(None, None)` if not exactly 2 colours. Correct for valid single-swap steps.
- `bulk_distance_to_4col`: Multi-source BFS from all 4-colourings outward. Standard and correct.
- `verify_inductive_lift`: Simulates lifting H-path to G. Detects chain merges through $v$. Logic is sound.

**Bugs found:** None.
**Confidence:** **HIGH** (95%)

---

### 4. `verify_counterexamples.py` — Existential Verification of Swap Sufficiency CEs

**What it claims to do:** For each "counterexample" from `swap_sufficiency_test.py`, verify that NO BFS-optimal path in $R(G-v, 5)$ is safe. A true counterexample requires ALL optimal paths to be unsafe.

**Verdict: Logic is CORRECT but the exhaustiveness guarantee is WEAK.**

#### `is_step_unsafe` (lines 36–64)

The function checks whether a single BFS step is an unsafe $(a,5)$-swap:

1. Identifies swap pair via `_identify_swap` — correct.
2. Filters for $(a,5)$ swaps only — correct (non-$(a,5)$ swaps can't merge through $v$).
3. Computes `col_H_cur` from `col_G` — I verified that `col_G` restricted to $H$ always equals `cur_H` at each step (the invariant is maintained by the caller's `kempe_swap` update). Correct.
4. Finds $v$-incident $(a,5)$-chains — correct.
5. Checks if the swapped chain is one of the $v$-incident chains — correct.

**Fragile pattern (repeated in 4 files):**
```python
sv = next(iter(swapped_verts))
if col_H_cur.get(sv, 0) in (the_a, 5):
    swapped_chain = get_kempe_chain(H, col_H_cur, sv, the_a, 5)
```
This picks ONE representative vertex from the swapped set and computes the chain from it. This works because `swapped_verts` IS a single $(a,5)$-chain (the swap is a single Kempe swap). But it's fragile — if `_identify_swap` ever misidentifies the colour pair, the chain lookup could silently return a wrong chain. There's no assertion that `frozenset(swapped_verts) == swapped_chain`.

#### `find_safe_bfs_path` (lines 67–145)

**CRITICAL CONCERN: Capped path enumeration.**

The function enumerates BFS-optimal paths via DFS over the parent DAG, capped at `max_paths` (default 1000, sometimes 10000). It reports:
- `reason: 'exhausted'` if all paths were checked
- `reason: 'max_paths_reached'` if the cap was hit

**Bug:** The caller (`verify_at_n`, line 244) does NOT distinguish between these two outcomes:
```python
if verification['safe_path_exists']:
    ...
else:
    results['no_safe_path'] += 1
    results['true_counterexamples'].append(ce_info)
```
A case where `max_paths_reached` and no safe path was found among 1000 paths is counted identically to a case where ALL paths were exhaustively checked. **This could produce false counterexamples.**

The `ce_info` dict does include `paths_checked` and `reason`, so the data is there to diagnose this — but the counting logic doesn't use it.

**Bugs found:** 1 (false counterexample risk from capped enumeration)
**Could output be misleading?** YES — the "48 counterexamples" count could be inflated.
**Confidence:** **MEDIUM** (70%) that all 48 are true counterexamples.

---

### 5. `merge_tolerant_check.py` — The MTL Claim

**What it claims to do:** For each of the 48 counterexamples, follow every BFS-optimal path in $R(G-v, 5)$ to a 4-colouring and check if $v$ has a free colour in $\{1,2,3,4\}$ at the endpoint.

**Verdict: The MTL CHECK ITSELF is correct. But it inherits uncertainty from the counterexample identification.**

#### `find_all_bfs_paths_to_4col` (lines 43–94)

Correct BFS with parent DAG construction and path enumeration. Caps at `max_paths` (default 10000, used with 100 in `check_merge_tolerant_lifting`). The layer-by-layer BFS is correctly implemented using list-based queue (not deque, but correct for layer processing).

#### `check_merge_tolerant_lifting` (lines 97–206)

For each path to a 4-colouring:
1. Reconstructs final colouring from canonical form — correct.
2. Reads $v$'s neighbour colours — correct.
3. Computes free colours as $\{1,2,3,4\} \setminus \text{distinct neighbour colours}$ — correct.
4. Path is "harmless" if free colours exist — correct.

The function also tracks intermediate step details (merge-proneness at each step), which is informational only and doesn't affect the harmless/harmful verdict.

#### `run_full_check` (lines 209–354)

**CONCERN: Hardcoded counterexample specs.**
```python
counterexample_specs = {25: [3], 35: [6]}
```
Only graphs T_9_25 (vertex 3) and T_9_35 (vertex 6) are checked. These are presumably the graphs where counterexamples were found by `swap_sufficiency_test.py`. This is fine IF those are the only graphs with counterexamples.

The function filters colourings through three gates before counting as a counterexample:
1. Must be merge-prone (≥2 distinct $(a,5)$-chains at $v$)
2. First BFS path must be unsafe
3. `find_safe_bfs_path` with `max_paths=10000` must fail

Gate 3 inherits the capped-enumeration weakness from `verify_counterexamples.py`.

#### `check_all_4col_targets` (lines 357–498)

**This is the STRONGEST test in the entire codebase.** For each counterexample, it:
1. Enumerates ALL 4-colourings of $G-v$ (exhaustive, no cap)
2. Classifies each as extensible or non-extensible
3. Does a FULL BFS of the connected component from the start colouring to find ANY reachable extensible 4-colouring (no path limit)

If this function reports `reachable_ext = True`, the finding is genuine — there truly exists a reachable 4-colouring where $v$ can be coloured. This is a much stronger result than the BFS-optimal-path-only check.

**Bugs found:** None in the MTL check itself.
**Could output be misleading?** The MTL claim is about whether identified cases can be handled. The check is valid for the cases it's applied to. Uncertainty lies in whether those cases are real counterexamples.
**Confidence in the MTL check logic:** **HIGH** (90%)
**Confidence that the 48 cases are real CEs that MTL handles:** **MEDIUM-HIGH** (75%)

---

### 6. `safe_path_search.py` — The 1.9M Safe Path Claim

**What it claims to do:** For every merge-prone $(G, v, \text{colouring})$ case at $n \le 9$, find the shortest safe reconfiguration path (using only non-merge-prone swaps) and verify it exists.

**Verdict: CORRECT with adequate resource limits.**

#### `safe_kempe_neighbours` (lines 40–88)

Filters Kempe swap neighbours to exclude merge-prone chains:
- Precomputes merge-prone status per $(a,5)$ pair — correct.
- Skips chains in `nbr_chains` when merge-prone — correct.
- Includes all non-$(a,5)$ swaps unconditionally — correct (these can't merge through $v$).
- Includes $(a,5)$ chains that aren't $v$-incident — correct.

**Logic is sound.**

#### `safe_bfs_to_4` (lines 91–129)

Standard BFS using `safe_kempe_neighbours`. Node cap at 500,000.

For $G-v$ on 8 vertices (when $G$ is on 9 vertices), the number of proper 5-colourings is bounded and the reconfiguration graph has at most tens of thousands of nodes. 500K is more than sufficient. **The cap is not a practical concern here.**

#### `is_merge_prone` (lines 132–144)

Checks ≥2 distinct $(a,5)$-chains incident to $v$'s neighbours for some $a$. Standard definition. Correct.

**Bugs found:** None.
**Could output be misleading?** The "1.9M" count includes every (graph, vertex, colouring) triple separately. Different vertices $v$ on the same graph with the same colouring produce different cases (because merge-proneness depends on $v$). This is legitimate double-counting in the mathematical sense — each is a genuinely different lifting problem.
**Confidence:** **HIGH** (90%)

---

### 7. `swap_sufficiency_test.py` — Disproving {1,2,3,4}-Swap Sufficiency

**What it claims to do:** For each triangulation at $n=9$, test whether BFS paths from 5-colourings to 4-colourings can always avoid merge-prone swaps.

**Verdict: CORRECT for detecting potential counterexamples. But counts are INFLATED by design.**

The function checks only ONE BFS path per colouring (the first from `bfs_reduce_to_4`). If that path has an unsafe step, it's counted as a "counterexample". This is a **universal** test ("is the first BFS path safe?"), not the **existential** test ("does ANY BFS path exist that is safe?").

The script explicitly acknowledges this in its comments and defers to `verify_counterexamples.py` for existential verification. So the "counterexample" count from this script ALONE is an upper bound, not exact.

**Bugs found:** None (the over-counting is by design, not a bug).
**Could output be misleading?** YES, if quoted without the existential verification caveat. The raw counterexample count from this script includes cases where alternative safe paths exist.
**Confidence:** **HIGH** (90%) that the code does what it says. The claim interpretation is the issue.

---

### 8. `surface_tension_validation.py` — Surface Tension Rigidity

**What it claims to do:** Compute surface tension rigidity $\rho_{ab}(c)$ for all merge-prone colourings and test whether $\rho = 0$ correlates with merge-proneness.

**Verdict: CORRECT. The conjecture-falsification claim is well-supported.**

- `compute_chain_boundary_edges`: Counts edges from chain $K$ to outside. Correct.
- `compute_normalized_surface_tension`: $\bar{\sigma}(K) = \sigma(K)/|K|$. Correct.
- `compute_rigidity_variants`: Computes `np.var()` over chain tensions. Rigidity threshold $\rho < 10^{-12}$. For integer boundary counts and chain sizes, $\bar{\sigma}$ is rational, so floating-point variance being exactly 0 (up to machine epsilon) is expected when all chains have the same $\bar\sigma$. The threshold is appropriate.
- Classification into rigid/flexible × merge-prone/safe quadrants is correct.
- The code finds cases in ALL four quadrants, falsifying both directions of the biconditional.

**Dependency on `physical_analogies._nx_to_adj`:** This just converts a NetworkX graph to an adjacency dict. Trivial and correct.

**Bugs found:** None.
**Confidence:** **HIGH** (92%)

---

### 9. `reconfiguration_graph.py` — Reconfiguration Graph Construction

**What it claims to do:** Build $R(G,k)$ with proper $k$-colourings as nodes and single Kempe swaps as edges.

**Verdict: CORRECT.**

- Enumerates all colourings, canonicalises, builds edges via `all_kempe_neighbours`. The edge check `nbr in canon_set and nbr != canon` is correct (ensures the swap target is also a valid colouring and not a self-loop).
- `analyze_reconfiguration_graph`: Standard connected components + diameter computation. Correct.
- `check_5_to_4_connectivity`: Checks whether every 5-colouring's component intersects the 4-colouring set. Correct.

**Bugs found:** None.
**Confidence:** **HIGH** (95%)

---

## Cross-Cutting Concerns

### The `col_G` Tracking Invariant

Four files (`verify_counterexamples.py`, `merge_tolerant_check.py`, `safe_path_search.py`, `swap_sufficiency_test.py`) use the same pattern:

```python
col_G = dict(col)
for i in range(len(path) - 1):
    cur_H = colouring_from_canonical(H, path[i])
    nxt_H = colouring_from_canonical(H, path[i + 1])
    # ... analyse step using col_G ...
    swapped = frozenset(u for u in H.nodes() if cur_H[u] != nxt_H[u])
    a, b = _identify_swap(H, cur_H, nxt_H)
    if swapped and a is not None:
        col_G = kempe_swap(col_G, swapped, a, b)
```

**I verified the invariant**: `{w: col_G[w] for w in H.nodes()} == cur_H` holds at every step. The proof:
- Initially: `col_G` restricted to $H$ = `col` restricted to $H$ = initial `cur_H`. ✓
- After each step: `kempe_swap` applies the same swap to `col_G` that produced `nxt_H` from `cur_H`. The restriction to $H$ advances correctly. ✓
- For $v$: `col_G[v]` is never modified (v is not in swapped). ✓

The invariant breaks if `_identify_swap` returns `(None, None)` — then `col_G` is NOT updated, and the invariant is lost for subsequent steps. For valid BFS steps (single Kempe swap), `_identify_swap` always returns a valid pair. **No bug, but fragile under malformed input.**

### The Single-Representative Chain Check

The pattern `sv = next(iter(swapped_verts))` appears in 4 files. It relies on the swapped vertices being a single Kempe chain. This is guaranteed by the BFS step semantics but has **no assertion** to verify it. If this assumption ever fails silently (e.g., due to a canonical form collision or a NetworkX bug), the unsafe check would produce wrong results.

### Sampling vs Exhaustive

| Component | Exhaustive? | Cap |
|---|---|---|
| Triangulation generation | Yes | None |
| Colouring enumeration | Yes | None (practical for $n \le 12$) |
| BFS in $R(G-v, 5)$ | Yes | None (BFS explores all reachable) |
| Path enumeration for CE verification | **NO** | 1000–10000 paths |
| MTL endpoint check (BFS version) | **NO** | 100 paths |
| MTL endpoint check (exhaustive version) | Yes | None (full component BFS) |
| Safe path BFS | Yes for practical sizes | 500K nodes |
| Surface tension computation | Yes | None |

---

## Claim-by-Claim Assessment

### Claim 1: "{1,2,3,4}-Swap Sufficiency is FALSE — 48 counterexamples at n=9"

**Assessment:** LIKELY TRUE but count may be slightly inflated.

The counterexample identification pipeline:
1. `swap_sufficiency_test.py` finds cases where the FIRST BFS path is unsafe ✓
2. `verify_counterexamples.py` checks if ANY BFS-optimal path is safe ← **capped at 1000–10000 paths**

If the number of BFS-optimal paths for some case exceeds 10000, a safe path might exist but not be found. The case would be counted as a "true counterexample" when it isn't.

For $n=9$ graphs (8-vertex subgraphs after removing $v$), the reconfiguration graph has moderate size (thousands to tens of thousands of nodes). The number of BFS-optimal paths could be large but is probably under 10000 for most cases.

**Confidence: 75%** that ALL 48 are true counterexamples. Very likely that MOST are true counterexamples, and at least some definitely are.

### Claim 2: "Surface Tension Rigidity Conjecture is FALSE — fails at every scale"

**Assessment:** TRUE (well-supported by code).

The code correctly computes $\rho$ and finds cases in all four quadrants of the rigid/flexible × merge-prone/safe matrix. The computation is exact (no sampling, no caps).

**Confidence: 92%.**

### Claim 3: "All 48 counterexamples are harmless under Merge-Tolerant Lifting"

**Assessment:** The MTL CHECK LOGIC is correct. The claim is supported IF the 48 cases are real CEs.

The `check_all_4col_targets` function performs an exhaustive component BFS — no path cap, no sampling. If it finds a reachable extensible 4-colouring, the finding is genuine.

The claim "MTL succeeds" means: for each identified case, there exists a reachable 4-colouring of $G-v$ where $v$ has a free colour. This is a concrete, verifiable property, and the code checks it correctly.

**Confidence in MTL check correctness: 90%.**
**Confidence in overall claim (including CE identification): 72%.**

### Claim 4: "1.9M merge-prone cases verified with zero failures for safe paths"

**Assessment:** LIKELY TRUE.

The safe BFS uses `safe_kempe_neighbours` (correctly filters merge-prone swaps) with a 500K node cap (more than sufficient for 8-vertex subgraphs). The enumeration is exhaustive over all graphs, vertices, and colourings.

The "1.9M" count is a sum of (graph × vertex × colouring) triples. This is legitimate — each triple is a distinct lifting problem.

**Confidence: 88%.**

---

## The Single Most Concerning Finding

**The capped path enumeration in `verify_counterexamples.py::find_safe_bfs_path`** (and its callers in `merge_tolerant_check.py::run_full_check`).

The function checks up to 1000 (or 10000) BFS-optimal paths per counterexample candidate. If the actual number of optimal paths exceeds this cap, the verdict "no safe path exists" is **not proven** — it's "no safe path found within budget." The callers do not distinguish between `reason: 'exhausted'` and `reason: 'max_paths_reached'`, counting both as true counterexamples.

This means:
- The "48 counterexamples" count could include false positives.
- The MTL claim ("all 48 are harmless") is testing cases that might not all be real counterexamples.
- The overall narrative ("Swap Sufficiency is false but MTL saves us") could be testing a weaker condition than intended.

**Severity:** MEDIUM-HIGH. The claims aren't necessarily wrong, but they carry more uncertainty than the confident language suggests.

**Mitigation:** The exhaustive check in `check_all_4col_targets` partially compensates — it doesn't rely on path enumeration at all, instead doing a full component BFS. If this check also passes, the MTL claim is solid regardless of whether the 48 are "true" counterexamples.

---

## Overall Confidence: MTL Claim ("All Merges Harmless")

**62%.**

Breakdown:
- Core infrastructure correct: 95%
- Counterexample identification correct: 75%
- MTL check logic correct: 90%
- No silent failures or masked errors: 90%
- Combined: ~58–65%

The main sources of uncertainty:
1. Capped path enumeration for CE identification (−15%)
2. No assertion on triangulation counts matching OEIS (−5%)
3. No assertion on single-representative chain assumption (−3%)
4. Cannot verify without running the code (−10%)

---

## Recommendations

1. **Add OEIS count assertions** in `generate_triangulations`: `assert len(result[n]) == expected[n]` for $n \le 10$.
2. **Log the `reason` field** from `find_safe_bfs_path` alongside CE counts. Report how many CEs were exhaustively verified vs. capped.
3. **Add a chain assertion** in the unsafe-check pattern: `assert frozenset(swapped_verts) == swapped_chain` to catch any silent chain-identification failures.
4. **Increase max_paths or use a smarter search**: Instead of enumerating all paths, do a modified BFS that tracks "has any prefix been safe so far" — this would give a yes/no answer without path enumeration. (The `safe_bfs_to_4` function in `safe_path_search.py` already does something similar.)
5. **Run `check_all_4col_targets` as the PRIMARY CE verification**, not just as a follow-up. It's strictly stronger than the path-enumeration approach.

---

## Summary Table

| File | Bugs | Logic | Misleading? | Confidence |
|---|---|---|---|---|
| `kempe_ops.py` | 0 | Correct | No | **HIGH** (95%) |
| `triangulation_db.py` | 0 | Correct | No | **HIGH** (93%) |
| `reduction_search.py` | 0 | Correct | No | **HIGH** (95%) |
| `reconfiguration_graph.py` | 0 | Correct | No | **HIGH** (95%) |
| `verify_counterexamples.py` | 1 | Correct but incomplete | **Yes** — CE count may be inflated | **MEDIUM** (70%) |
| `merge_tolerant_check.py` | 0 | Correct | Moderate — inherits CE uncertainty | **MEDIUM-HIGH** (75%) |
| `safe_path_search.py` | 0 | Correct | Minor — "1.9M" is legitimate but large | **HIGH** (90%) |
| `swap_sufficiency_test.py` | 0 | Correct (by design checks one path) | **Yes** — raw counts over-count CEs | **HIGH** (90%) |
| `surface_tension_validation.py` | 0 | Correct | No | **HIGH** (92%) |

**Total bugs found:** 1 (capped enumeration treated as exhaustive in CE counting)
**Total logic errors:** 0
**Total stubs/mocks:** 0
**Total hardcoded results:** 0

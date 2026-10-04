# M-Witness — combined witness for \(T_{9,35}\), vertex 6

**Manager:** M-Witness
**Date:** 27 September 2026
**Inputs:** `backgroundMaterial/agent1701/groups/W_graph.md`, `backgroundMaterial/agent1701/groups/W_path.md`
**Kill criterion:** `backgroundMaterial/agent1701/groups/K1_spec.md` §6
**Navigator:** not edited. This file does not mark `t1-witness-935` killed. The critic still gates the witness.

## Decision

**ACCEPT WITNESS**

W-graph writes the edge list of `generate_triangulations(9)[35]`. W-path writes one proper 5-colouring and one path in \(\mathcal{R}(G-6,5)\). The three objects the kill criterion asks for are in those two drafts. They are copied below so the check is against the objects, not against a sentence in an older report.

## Spot-check of the JSON

Opened `backgroundMaterial/agent1520/coordinator/manager_M1/sub_S3/counterexample_details.json` (6 objects). The first object with `"vertex": 6` and `"degree": 4` is 0-based index 3. Quoted from that object:

- `"vertex": 6`, `"degree": 4`
- `"colouring"` includes `"6": 5`
- `"neighbours": [0, 1, 2, 5]`
- `"bfs_path_length": 3`
- step 0 of `"path_details"`: `"is_unsafe": true`, `"swap_pair": [3, 5]`, `"swapped_vertices": [2, 8]`
- step 1: `"is_unsafe": false`, `"swap_pair": [3, 4]`, `"swapped_vertices": [3]`
- `"verification": { "safe_path_exists": false, "paths_checked": 2, "unsafe_count": 2, "reason": "exhausted" }`

Vertex 2 lies in `"neighbours"` and in step 0's `"swapped_vertices"`. The edge list of this object, normalised and sorted, is the edge list in the next section (21 edges).

This object does not show a safe path at distance greater than the BFS length. No field stores such a path. `"safe_path_exists": false` is the flag of a search that, as W-path records, stops when the length leaves the BFS distance.

## Edge list and degree

From W-graph, which regenerated `generate_triangulations(9)[35]`. The generator names that graph `T_9_35`. Vertices are \(\{0,1,\ldots,8\}\). The graph has 21 edges. The same list is `graph_edges` on JSON index 3.

| | | | | | | |
|---|---|---|---|---|---|---|
| \(\{0,2\}\) | \(\{0,3\}\) | \(\{0,4\}\) | \(\{0,5\}\) | \(\{0,6\}\) | \(\{0,7\}\) | \(\{0,8\}\) |
| \(\{1,2\}\) | \(\{1,3\}\) | \(\{1,4\}\) | \(\{1,5\}\) | \(\{1,6\}\) | \(\{2,3\}\) | \(\{2,6\}\) |
| \(\{2,7\}\) | \(\{2,8\}\) | \(\{3,4\}\) | \(\{3,7\}\) | \(\{4,5\}\) | \(\{5,6\}\) | \(\{7,8\}\) |

Vertex 6 has degree 4. Its neighbours, in increasing order, are \(0,1,2,5\). A triangulation is planar, so this \(G\) is a planar graph.

## Colouring

The colouring on JSON index 3, also written by W-path:

| Vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|--------|---|---|---|---|---|---|---|---|---|
| Colour | 1 | 2 | 3 | 4 | 5 | 3 | 5 | 2 | 5 |

\(c(6) = 5\). W-path's replay found that \(c\) is a proper colouring of \(G\) and uses all five colours, and that \(c|_{G-6}\) is a proper 5-colouring of \(H = G - 6\).

## The one path

`"bfs_path_length": 3` counts colourings in the list returned by `bfs_reduce_to_4`, so the path in \(\mathcal{R}(H,5)\) has length 2. The two steps below are the whole recorded path. W-path replayed them and found the same sequence as `bfs_reduce_to_4(H, c|_H, k=5)`.

**Step 0.** Swap colours \(3\) and \(5\) on the chain \(\{2,8\}\).

| Field | Value |
|---|---|
| `swap_pair` | \([3,5]\) |
| `is_unsafe` | true |
| `swapped_vertices` | \([2,8]\) |
| `num_chains_at_v` | 2 |
| `v_nbrs_in_ba5` | \([2,5]\) |

Before this swap, neighbour 2 lies in the \((3,5)\)-chain \(\{2,8\}\) and neighbour 5 lies in the \((3,5)\)-chain \(\{4,5\}\). Those chains are distinct. The swapped chain is \(\{2,8\}\), which contains neighbour 2.

**Step 1.** Swap colours \(3\) and \(4\) on the chain \(\{3\}\). `"is_unsafe": false`. This step does not use colour 5.

After step 1, W-path's replay gives the proper colouring of \(H\)

$$
0\mapsto 1,\; 1\mapsto 2,\; 2\mapsto 5,\; 3\mapsto 3,\; 4\mapsto 5,\; 5\mapsto 3,\; 7\mapsto 2,\; 8\mapsto 3,
$$

which uses the four colours \(\{1,2,3,5\}\).

## Kill criterion

K1 §6: the degree-4 conjecture is false if there exists one planar graph \(G\), one proper colouring \(c\), one vertex \(v\) with \(c(v)=5\) and \(\deg(v)=4\), and one shortest path in \(\mathcal{R}(G-v,5)\) from \(c|_{G-v}\) to a colouring with at most four colours, such that some \((a,5)\)-step swaps a chain containing a neighbour of \(v\) while at least two neighbours of \(v\) lie in distinct \((a,5)\)-chains.

This path meets that criterion. \(G\) is the planar triangulation `T_9_35`, \(c(6)=5\), \(\deg(6)=4\), the path has length 2 and is a shortest path to a 4-colouring of \(H\), and step 0 is a \((3,5)\)-swap of \(\{2,8\}\) while neighbours 2 and 5 lie in distinct \((3,5)\)-chains.

## Agent 1419 claims, against this object

`backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md` asserts, for the 24 colourings of `T_9_35` at vertex 6, that every optimal path is unsafe, and it asserts a salvage at distance 3 when the optimum is 2. Separated as in W-path, and read only against JSON index 3:

| Claim | Supported by this object? |
|---|---|
| This shortest path is unsafe | Yes. Step 0 has `"is_unsafe": true`, and `"swapped_vertices": [2, 8]` contains neighbour 2 of vertex 6, while `"num_chains_at_v": 2`. |
| Every shortest path of this colouring is unsafe | The object's `"verification"` records `"paths_checked": 2`, `"unsafe_count": 2`, `"reason": "exhausted"`. That is a count on this colouring. The second path is not written in the JSON or in W-path. The claim that all 24 colourings behave this way is a different sentence; this object is one colouring. |
| A safe path exists at distance greater than the BFS length | No. This object does not contain one. |

## What is not proved

The Four Colour Theorem is not proved.

A safe path of length greater than 2 is not in this object, and this check did not search past the BFS distance. That salvage is not a fact established here.

Degree-5 BFS avoidance is untouched. The second shortest path on this colouring is not written down. The other colourings in the file were not used.

## Follow-up for the next cycle

**Task name:** `W2-longer-safe`

One colouring, one search. The colouring is the map in the table above, on \(H = T_{9,35} - 6\). The search is `find_safe_nonoptimal_path` in `compute/kempe/counterexample_energy_targeted.py`: one run from \(c|_H\) with `opt_dist = 2`, asking for a safe path in \(\mathcal{R}(H,5)\) whose length is strictly greater than 2. Write the path it returns, or write that it returned none. The critic can start `W2-longer-safe` now.

## W2 decision

**ACCEPT PATH**

Input: `backgroundMaterial/agent1701/groups/W2_longer.md`. Navigator not edited.

The write-up contains the three swaps, the elapsed time, and a statement of the safety test. This is one colouring of \(T_{9,35}\) at vertex 6. It is not a theorem.

The swaps, in order, are \((1,2)\) on \(\{0,7\}\), \((1,5)\) on \(\{4\}\), and \((4,5)\) on \(\{3\}\). The path has length 3 and ends at a colouring of \(H\) that uses \(\{1,2,3,5\}\). The clocks in the write-up are \(1.081\) seconds for `generate_triangulations(9)`, \(0.001\) seconds for `find_safe_nonoptimal_path`, and \(3.725\) seconds of process wall time.

The safety test matches the K1 kill test. `find_safe_nonoptimal_path` accepts a path only when `classify_path_safety` sets `path_is_safe`. That flag is false when some step has `is_unsafe`. In `classify_path_safety`, an \((a,5)\)-step is unsafe when at least two neighbours of \(v\) lie in distinct \((a,5)\)-chains and the chain of a swapped vertex is one of those chains (`all_paths_analysis.py`, the block that sets `is_unsafe` after `len(chains_of_nbrs) >= 2`). `is_step_unsafe` (`verify_counterexamples.py`) returns false when colour 5 is not in the pair, returns false when fewer than two neighbour-chains exist, and returns true when the swapped chain is one of those chains. A Kempe chain that equals the chain of a neighbour contains that neighbour, and the step swaps the whole chain. That is the K1 sentence: an \((a,5)\)-step swaps a chain containing a neighbour of \(v\) while two neighbours lie in distinct \((a,5)\)-chains. Both functions read the chains from the restriction of the evolving colouring of \(G\). W2 records that, on this path, `is_step_unsafe` and `classify_path_safety` are false at every step, and a check on the stored colourings of \(H\) gives the same three answers.

The run is this colouring only. W2 did not run the other colourings of \(T_{9,35}\) at vertex 6.

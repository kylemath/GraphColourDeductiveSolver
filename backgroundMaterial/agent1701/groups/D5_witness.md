# D5 — One shortest path at vertex 3 on $T_{9,25}$

**Date:** 27 September 2026
**Group:** D5
**Record:** the first object in `backgroundMaterial/agent1520/coordinator/manager_M1/sub_S3/counterexample_details.json` with `"vertex": 3` and `"degree": 5` (0-based index 0)
**Status:** one colouring, one shortest path, checked. This file does not mark navigator node `t1-spec-d5` killed, and it does not edit `docs/navigator/`.

The graph is the labelled triangulation `generate_triangulations(9)[25]`, which that generator names `T_9_25`. The edge list of this JSON object equals that graph (21 edges). Vertex 3 has degree 5 and neighbours $0,1,2,4,6$. A triangulation is planar, so this $G$ is a planar graph.

The degree-4 witness on $T_{9,35}$ is already written. This check does not recompute it.

---

## 1. Edge match

Command, from `compute/kempe`, using `/Users/fulkanjou/GraphColour/.venv/bin/python`:

```text
generate_triangulations(9)[25]
```

Script: `backgroundMaterial/agent1701/groups/d5_witness_check.py`.

The call returned 50 triangulations on 9 vertices (OEIS A000109) in 1.1 seconds. Index 25 is the graph whose `graph['name']` the generator sets to `T_9_25`. Vertices are $\{0,1,\ldots,8\}$. A triangulation on 9 vertices has $3\cdot 9-6 = 21$ edges, and this graph has 21 edges. `is_triangulation` returned true.

Edges are written with the smaller endpoint first and listed in lexicographic order. This is the edge set of `generate_triangulations(9)[25]`.

| | | | | | | |
|---|---|---|---|---|---|---|
| $\{0,2\}$ | $\{0,3\}$ | $\{0,4\}$ | $\{0,5\}$ | $\{0,6\}$ | $\{0,7\}$ | $\{0,8\}$ |
| $\{1,2\}$ | $\{1,3\}$ | $\{1,4\}$ | $\{1,5\}$ | $\{2,3\}$ | $\{2,5\}$ | $\{2,6\}$ |
| $\{2,7\}$ | $\{3,4\}$ | $\{3,6\}$ | $\{4,5\}$ | $\{6,7\}$ | $\{6,8\}$ | $\{7,8\}$ |

The JSON file has no graph-name field. The objects were read in order. The first object with `"vertex": 3` and `"degree": 5` is record index 0. It has 21 `graph_edges` and `"neighbours": [0, 1, 2, 4, 6]`.

Each JSON edge was normalised to $(\min,\max)$ and the list was sorted lexicographically, then compared with the generator edge list above.

**Edge match: yes.** The two lists are equal. The generator list and record 0 contain the same 21 edges.

---

## 2. Colouring

The JSON field `"colouring"` on record 0 is

| Vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|--------|---|---|---|---|---|---|---|---|---|
| Colour | 1 | 2 | 3 | 5 | 4 | 5 | 4 | 2 | 5 |

Quoted fields: `"vertex": 3`, `"degree": 5`, and `"colouring"` with `"3": 5`. So $c(3) = 5$ and $\deg(3) = 5$. `"neighbours": [0, 1, 2, 4, 6]`.

The replay found that this map is a proper colouring of $G$ and uses all five colours. The restriction $c|_{G-3}$ is a proper colouring of $H = G - 3$ and also uses five colours:

$$
c|_H(0)=1,\; c|_H(1)=2,\; c|_H(2)=3,\; c|_H(4)=4,\; c|_H(5)=5,\; c|_H(6)=4,\; c|_H(7)=2,\; c|_H(8)=5.
$$

`"merge_info"` at this initial colouring, for colour `"4"`:

```json
"nbrs_in_ba5": [4, 6],
"num_distinct_chains": 2,
"chain_sizes": [2, 2]
```

The JSON object does not store the two chain vertex-sets. The replay, at $c|_H$, found the $(4,5)$-chain of neighbour 4 to be $\{4,5\}$ and the $(4,5)$-chain of neighbour 6 to be $\{6,8\}$.

---

## 3. Path steps

`"bfs_path_length": 3` is the number of colourings in the list returned by `bfs_reduce_to_4`, not the number of swaps. The object stores two steps, so the path in $\mathcal{R}(H,5)$ has length 2. The replay produced the same swap sequence as `bfs_reduce_to_4(H, c|_H, k=5)`, whose distance is 2, and the last colouring uses four colours. The two steps are the whole recorded path. The BFS call itself took under 0.01 seconds; the 1.1 seconds above is the triangulation generation.

### Step 0

| Field | Value |
|---|---|
| `swap_pair` | $[4,5]$ |
| `chain_size` | 2 |
| `is_a5` | true |
| `is_unsafe` | true |
| `swapped_vertices` | $[4,5]$ |
| `merge_prone` | true |
| `num_chains_at_v` | 2 |
| `v_nbrs_in_ba5` | $[4,6]$ |

The replay, at the colouring before this swap, found the $(4,5)$-chain of neighbour 4 to be $\{4,5\}$ and the $(4,5)$-chain of neighbour 6 to be $\{6,8\}$. Those sets are distinct. The swapped set equals $\{4,5\}$, which contains neighbour 4.

After the swap, $H$ is still properly coloured with five colours: vertex 4 has colour 5 and vertex 5 has colour 4.

### Step 1

| Field | Value |
|---|---|
| `swap_pair` | $[3,5]$ |
| `chain_size` | 1 |
| `is_a5` | true |
| `is_unsafe` | true |
| `swapped_vertices` | $[2]$ |
| `merge_prone` | true |
| `num_chains_at_v` | 2 |
| `v_nbrs_in_ba5` | $[2,4]$ |

The replay, at the colouring after step 0, found the $(3,5)$-chain of neighbour 2 to be $\{2\}$ and the $(3,5)$-chain of neighbour 4 to be $\{4\}$. Those sets are distinct. The swapped set equals $\{2\}$, which contains neighbour 2.

After the swap, $H$ is properly coloured by

$$
0\mapsto 1,\; 1\mapsto 2,\; 2\mapsto 5,\; 4\mapsto 5,\; 5\mapsto 4,\; 6\mapsto 4,\; 7\mapsto 2,\; 8\mapsto 5,
$$

which uses the four colours $\{1,2,4,5\}$.

---

## 4. Kill criterion

The analogous kill, for this degree-5 reading of the test in `backgroundMaterial/agent1701/groups/K2_spec.md` §6, is one triangulation, one proper colouring, one vertex $v$ with $c(v)=5$ and $\deg(v)=5$, and one shortest path in $\mathcal{R}(G-v,5)$ from $c|_{G-v}$ to a colouring with at most four colours, such that some $(a,5)$-step swaps a chain containing a neighbour of $v$ while $v$ bridges two $(a,5)$-chains.

Fields this object stores, quoted from record index 0:

- `"vertex": 3`, `"degree": 5`, `"colouring"` with `"3": 5`
- `"neighbours": [0, 1, 2, 4, 6]`
- `"bfs_path_length": 3` and two objects in `"path_details"`
- step 0: `"swap_pair": [4, 5]`, `"is_a5": true`, `"is_unsafe": true`, `"swapped_vertices": [4, 5]`, `"merge_prone": true`, `"num_chains_at_v": 2`, `"v_nbrs_in_ba5": [4, 6]`
- `"merge_info"` for colour `"4"`: `"nbrs_in_ba5": [4, 6]`, `"num_distinct_chains": 2`, `"chain_sizes": [2, 2]`

Neighbour 4 lies in both `"neighbours"` and step 0's `"swapped_vertices"`. `"num_chains_at_v": 2` and `"num_distinct_chains": 2` are the object's record that $v$ meets two $(4,5)$-chains.

The object does not store the two chain vertex-sets, and it does not store the colouring at the end of the path. Those were replayed.

The bounded check was this colouring only. It did not enumerate the other colourings in the file. Using the project virtual environment, it rebuilt $H$, replayed the two recorded swaps, and called `bfs_reduce_to_4` once. Elapsed time: 1.1 seconds.

That check found:

- $G$ is `T_9_25`, $c$ is proper, $c(3)=5$, and $\deg(3)=5$.
- The recorded swaps are the Kempe chains $\{4,5\}$ and then $\{2\}$, in that order.
- The path has length 2, equals the path returned by `bfs_reduce_to_4`, and ends at a proper colouring of $H$ with four colours. It is a shortest path in $\mathcal{R}(H,5)$.
- At the colouring before the $(4,5)$-step, neighbours 4 and 6 lie in the distinct chains $\{4,5\}$ and $\{6,8\}$, and the swapped chain is $\{4,5\}$, which contains neighbour 4.

**This path meets the degree-5 kill test: yes.**

Step 1 meets the same test on the same path: neighbours 2 and 4 lie in the distinct $(3,5)$-chains $\{2\}$ and $\{4\}$, and the swapped chain $\{2\}$ contains neighbour 2. Step 0 is already enough.

---

## 5. Not proved

This file does not mark `t1-spec-d5` killed. The critic still has to gate the witness.

This object is one colouring of $T_{9,25}$. The other colourings of that graph are unchecked here. Agent 1419's report states that $T_{9,25}$ at vertex 3 has 24 colourings on which every optimal path is unsafe (`backgroundMaterial/agent1419/agent1419Report.md`). This write-up does not check those other colourings.

The verification object on this one record is

```json
"verification": {
  "safe_path_exists": false,
  "paths_checked": 2,
  "unsafe_count": 2,
  "reason": "exhausted"
}
```

That field is the producer's count for this colouring. This write-up replayed the recorded `bfs_reduce_to_4` path and did not write down the other shortest path.

A counterexample to degree-5 BFS avoidance leaves the Four Colour Theorem where it stood. This path neither proves that theorem nor refutes it.

The check of this one path is done. Feasibility of reading the witness off the replay: **High**. The command finished in 1.1 seconds.

---

## Next steps

1. The critic gates this witness against `K2_spec.md` §6. This file leaves `t1-spec-d5` unmarked.
2. A count of the other colourings of $T_{9,25}$ at vertex 3 is a separate check. This file does not supply it.
3. The Four Colour Theorem is outside this witness.

# W-path — One shortest path at vertex 6

**Date:** 27 September 2026
**Group:** W-path
**Record:** the first object in `backgroundMaterial/agent1520/coordinator/manager_M1/sub_S3/counterexample_details.json` with `"vertex": 6` and `"degree": 4` (0-based index 3 in that file)
**Status:** one path, checked. This file does not mark navigator node `t1-witness-935` killed.

The graph is the labelled triangulation `generate_triangulations(9)[35]`, which that generator names `T_9_35`. The edge list of this JSON object equals that graph (21 edges). The same comparison is written in `backgroundMaterial/agent1701/groups/W_graph.md`. Vertex 6 has degree 4 and neighbours $0,1,2,5$. A triangulation is planar, so this $G$ is a planar graph.

---

## 1. Colouring

The JSON field `"colouring"` is

| Vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|--------|---|---|---|---|---|---|---|---|---|
| Colour | 1 | 2 | 3 | 4 | 5 | 3 | 5 | 2 | 5 |

$c(6) = 5$. The same object records `"degree": 4`.

A replay in `/Users/fulkanjou/GraphColour/.venv/bin/python` (1.1 seconds, including regeneration of the 50 triangulations on 9 vertices) found that this map is a proper colouring of $G$ and uses all five colours. The restriction $c|_{G-6}$ is a proper colouring of $H = G - 6$ and also uses five colours:

$$
c|_H(0)=1,\; c|_H(1)=2,\; c|_H(2)=3,\; c|_H(3)=4,\; c|_H(4)=5,\; c|_H(5)=3,\; c|_H(7)=2,\; c|_H(8)=5.
$$

---

## 2. Path steps

`"bfs_path_length": 3` is the number of colourings in the list returned by `bfs_reduce_to_4`, not the number of swaps. The object stores two steps, so the path in $\mathcal{R}(H,5)$ has length 2. The replay produced the same canonical sequence as `bfs_reduce_to_4(H, c|_H, k=5)`, whose distance is 2, and the last colouring uses four colours. The two steps are the whole recorded path.

### Step 0

| Field | Value |
|---|---|
| `swap_pair` | $[3,5]$ |
| `chain_size` | 2 |
| `is_unsafe` | true |
| `swapped_vertices` | $[2,8]$ |
| `merge_prone` | true |
| `num_chains_at_v` | 2 |
| `v_nbrs_in_ba5` | $[2,5]$ |

Also present on this step, and not required by the list above: `is_a5` true, `is_14` false.

The replay, at the colouring before this swap, found the $(3,5)$-chain of neighbour 2 to be $\{2,8\}$ and the $(3,5)$-chain of neighbour 5 to be $\{4,5\}$. Those sets are distinct. The swapped set equals $\{2,8\}$.

After the swap, $H$ is still properly coloured with five colours: vertex 2 has colour 5 and vertex 8 has colour 3.

### Step 1

| Field | Value |
|---|---|
| `swap_pair` | $[3,4]$ |
| `chain_size` | 1 |
| `is_unsafe` | false |
| `swapped_vertices` | $[3]$ |
| `merge_prone` | absent |
| `v_nbrs_in_ba5` | absent |

Also present: `is_a5` false, `is_14` true. The producer adds `merge_prone`, `num_chains_at_v`, and `v_nbrs_in_ba5` only when the swap uses colour 5. This step does not.

The replay found that $\{3\}$ is the $(3,4)$-chain of vertex 3 at the colouring after step 0. After the swap, $H$ is properly coloured by

$$
0\mapsto 1,\; 1\mapsto 2,\; 2\mapsto 5,\; 3\mapsto 3,\; 4\mapsto 5,\; 5\mapsto 3,\; 7\mapsto 2,\; 8\mapsto 3,
$$

which uses the four colours $\{1,2,3,5\}$.

---

## 3. Kill criterion

The criterion in `backgroundMaterial/agent1701/groups/K1_spec.md` §6 is one planar graph, one proper colouring, one vertex $v$ with $c(v)=5$ and $\deg(v)=4$, and one shortest path in $\mathcal{R}(G-v,5)$ from $c|_{G-v}$ to a colouring with at most four colours, such that some $(a,5)$-step swaps a chain containing a neighbour of $v$ while at least two neighbours of $v$ lie in distinct $(a,5)$-chains.

Fields this object does store, quoted from record index 3:

- `"vertex": 6`, `"degree": 4`, `"colouring"` with `"6": 5`
- `"neighbours": [0, 1, 2, 5]`
- `"bfs_path_length": 3` and two objects in `"path_details"`
- step 0: `"swap_pair": [3, 5]`, `"is_a5": true`, `"is_unsafe": true`, `"swapped_vertices": [2, 8]`, `"merge_prone": true`, `"num_chains_at_v": 2`, `"v_nbrs_in_ba5": [2, 5]`
- `"merge_info"` for colour `"3"`: `"nbrs_in_ba5": [2, 5]`, `"num_distinct_chains": 2`, `"chain_sizes": [2, 2]`

Neighbour 2 lies in both `"neighbours"` and step 0's `"swapped_vertices"`. `"num_chains_at_v": 2` and `"num_distinct_chains": 2` are the object's record that $v$ meets two $(3,5)$-chains.

The object does not store the colouring at the end of the path, and it does not store the two chain vertex-sets. Those are part of the criterion (a path that arrives at most four colours, and a swapped chain that is one of the chains meeting $v$). On that point the JSON record alone does not yet meet the criterion.

The bounded check was this colouring only. It did not enumerate the other colourings in the file. Using the project virtual environment, it rebuilt $H$, replayed the two recorded swaps, and called `bfs_reduce_to_4` once. Elapsed time: 1.1 seconds.

That check found:

- $G$ is `T_9_35`, $c$ is proper, $c(6)=5$, and $\deg(6)=4$.
- The recorded swaps are the Kempe chains $\{2,8\}$ and then $\{3\}$, in that order.
- The path has length 2, equals the path returned by `bfs_reduce_to_4`, and ends at a proper colouring of $H$ with four colours. It is a shortest path in $\mathcal{R}(H,5)$.
- At the colouring before the $(3,5)$-step, neighbours 2 and 5 lie in the distinct chains $\{2,8\}$ and $\{4,5\}$, and the swapped chain is $\{2,8\}$, which contains neighbour 2.

**This path meets the K1 kill criterion: yes.**

---

## 4. The three claims in the Agent 1419 report

`backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md` says, for the 24 colourings of `T_9_35` at vertex 6, that every optimal path is unsafe, and that a safe path exists at distance 3 when the optimal distance is 2. The same three sentences appear in `backgroundMaterial/agent1419/agent1419Report.md` §2.1 and §2.2. Separated, they are:

1. This shortest path is unsafe.
2. Every shortest path is unsafe.
3. A safe path exists at greater distance.

The verification object on this record is

```json
"verification": {
  "safe_path_exists": false,
  "paths_checked": 2,
  "unsafe_count": 2,
  "reason": "exhausted"
}
```

`find_safe_bfs_path` in `compute/kempe/verify_counterexamples.py` searches only paths whose length equals the BFS distance to a colouring with at most four colours. It stops when the distance exceeds that value. `safe_path_exists: false` with `paths_checked: 2`, `unsafe_count: 2`, and `reason: "exhausted"` means that function reconstructed two shortest paths, both unsafe, and finished that reconstruction. It does not record a path of any greater length. The flag is not a statement that a safe path fails to exist further away, and it is not a statement that one exists.

| Claim | What this object supplies |
|---|---|
| This shortest path is unsafe | Supported. Step 0 has `is_unsafe: true` on the path whose length is `bfs_path_length`. The replay agrees: that step swaps $\{2,8\}$, which contains neighbour 2, while neighbours 2 and 5 are in distinct $(3,5)$-chains, and the path is shortest. |
| Every shortest path is unsafe | Supported by the verification field: two shortest paths checked, both unsafe, search exhausted. This write-up replayed the recorded path and did not write down the other one. |
| A safe path exists at greater distance | Not supported. No field gives a path longer than the BFS distance. `safe_path_exists` is false inside a search that never leaves that distance. |

This object supports the first claim and the second claim. It does not support the third.

---

## 5. Not proved

This file does not mark `t1-witness-935` killed. The critic still has to gate the witness.

A safe path of length greater than 2 is not written here, and this check did not search past distance 2. The sentence “every shortest path is unsafe” is the verification field’s count of two paths; the second path is not written down in this file. Degree-5 BFS avoidance, and the Four Colour Theorem, are untouched.

The check of this one path is done. Feasibility of reading the witness off the replay: **High**. The command finished in 1.1 seconds.

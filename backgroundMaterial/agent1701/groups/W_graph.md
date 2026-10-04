# W-graph — Identity of triangulation index 35

**Date:** 27 September 2026
**Group:** W-graph
**Status:** graph identity only. This file does not exhibit a colouring or a path, and it does not mark any conjecture killed.

## Generator

Command, from `compute/kempe`, using `/Users/fulkanjou/GraphColour/.venv/bin/python`:

```text
generate_triangulations(9)[35]
```

Script: `backgroundMaterial/agent1701/groups/w_graph_check.py`.

The call returned 50 triangulations on 9 vertices (OEIS A000109) in 1.1 seconds. Index 35 is the graph whose `graph['name']` the generator sets to `T_9_35`. Vertices are $\{0,1,\ldots,8\}$. A triangulation on 9 vertices has $3\cdot 9-6 = 21$ edges, and this graph has 21 edges.

## Edge list

Edges are written with the smaller endpoint first and listed in lexicographic order. This is the edge set of `generate_triangulations(9)[35]`.

| | | | | | | |
|---|---|---|---|---|---|---|
| $\{0,2\}$ | $\{0,3\}$ | $\{0,4\}$ | $\{0,5\}$ | $\{0,6\}$ | $\{0,7\}$ | $\{0,8\}$ |
| $\{1,2\}$ | $\{1,3\}$ | $\{1,4\}$ | $\{1,5\}$ | $\{1,6\}$ | $\{2,3\}$ | $\{2,6\}$ |
| $\{2,7\}$ | $\{2,8\}$ | $\{3,4\}$ | $\{3,7\}$ | $\{4,5\}$ | $\{5,6\}$ | $\{7,8\}$ |

## Vertex 6

- Degree of vertex 6: $4$.
- Neighbours of vertex 6, in increasing order: $0,1,2,5$.

## Comparison with the counterexample file

File: `backgroundMaterial/agent1520/coordinator/manager_M1/sub_S3/counterexample_details.json`.

That file has no graph-name field. The objects were read in order. The first object with `"vertex": 6` and `"degree": 4` is record index 3 (0-based). It has 21 `graph_edges` and `"neighbours": [0, 1, 2, 5]`.

Each JSON edge was normalised to $(\min,\max)$ and the list was sorted lexicographically, then compared with the generator edge list above.

**Match: yes.** The two lists are equal. There is no edge present in index 35 and absent from record 3, and no edge present in record 3 and absent from index 35.

## What this check establishes

The degree-4, vertex-6 record at index 3 of `counterexample_details.json` is the same labelled graph as `generate_triangulations(9)[35]`, which the generator names `T_9_35`.

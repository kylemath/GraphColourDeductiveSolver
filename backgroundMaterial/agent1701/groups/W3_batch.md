# W3 — Stored colourings of \(T_{9,35}\) at vertex 6

**Date:** 27 September 2026
**Group:** W3
**Question:** for every stored colouring of \(T_{9,35}\) at vertex \(6\), does `find_safe_nonoptimal_path` return a safe path longer than the BFS distance?
**Status:** the stored list was run to completion. This file does not treat that list as every colouring, and it does not treat a longer safe path as Conjecture 5.5.

The graph is `generate_triangulations(9)[35]`, named `T_9_35`. Vertex \(6\) has degree \(4\). \(H = G - 6\). For each colouring \(c\), `opt_dist` is the length of the path returned by `bfs_reduce_to_4(H, c|_H, k=5)`, and the call is `find_safe_nonoptimal_path(T, H, 6, c, c|_H, opt_dist, max_extra=3)`.

---

## 1. Which colourings

Two lists in `backgroundMaterial/agent1545/coordinator/manager_M1/sub_S1/merge_tolerant_results.json` have entries with `"graph": "T_9_35"` and `"vertex": 6`:

| List | Entries | Distinct colourings |
|---|---|---|
| `exhaustive_details` | \(24\) | \(24\) |
| `ce_details` | \(24\) | \(24\) |

Those two sets of colourings are equal. The three records in `backgroundMaterial/agent1520/coordinator/manager_M1/sub_S3/counterexample_details.json` with `"vertex": 6` and `"degree": 4` are already in that set. The run is those \(24\) colourings, once each.

Each of the \(24\) is a proper \(5\)-colouring of \(G\), and its restriction to \(H\) is a proper \(5\)-colouring of \(H\).

---

## 2. Command and time

```
/Users/fulkanjou/GraphColour/.venv/bin/python -u backgroundMaterial/agent1701/groups/w3_batch_search.py
```

The process wall clock is \(1.164\) seconds. That includes loading the JSON files (\(0.0005\) seconds) and `generate_triangulations(9)` (\(1.108\) seconds). Every colouring finished. The ten-minute stop was not reached. Each call of `bfs_reduce_to_4` and `find_safe_nonoptimal_path` finished in under \(0.003\) seconds.

The per-colouring record is `backgroundMaterial/agent1701/groups/w3_batch_results.json`.

---

## 3. Counts

| Quantity | Value |
|---|---|
| Colourings run | \(24\) |
| Returned a path | \(24\) |
| Returned `None` | \(0\) |
| `bfs_reduce_to_4` returned no path | \(0\) |
| Elapsed seconds | \(1.164\) |

For every one of the \(24\), `bfs_reduce_to_4` has length \(2\), so the BFS distance is \(2\). For every one of the \(24\), `find_safe_nonoptimal_path` returned a path of length \(3\). Each of those paths is longer than the BFS distance, and the last colouring of \(H\) uses four colours.

So, on this stored list, the answer is yes: the function returns a safe path longer than the BFS distance for every stored colouring.

---

## 4. One other path

The colouring already published in `backgroundMaterial/agent1701/groups/W_path.md` and `W2_longer.md` is \(0{:}1,1{:}2,2{:}3,3{:}4,4{:}5,5{:}3,6{:}5,7{:}2,8{:}5\). The path below is the next colouring in `exhaustive_details`.

| Vertex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|--------|---|---|---|---|---|---|---|---|---|
| Colour | 1 | 2 | 4 | 3 | 5 | 4 | 5 | 2 | 5 |

BFS distance \(2\). The function returned a path of length \(3\). The swap pairs and vertex sets, read from the colourings on that path by `_identify_swap`, are:

| Step | Swap pair | Vertices |
|---|---|---|
| 0 | \((1,2)\) | \(\{0,7\}\) |
| 1 | \((1,5)\) | \(\{4\}\) |
| 2 | \((3,5)\) | \(\{3\}\) |

---

## 5. Not proved

These \(24\) maps are the stored colourings named above. They are not a proof for every colouring of \(T_{9,35}\).

A path that `find_safe_nonoptimal_path` accepts is longer than the BFS distance and has no step that `classify_path_safety` marks unsafe. A longer safe path is not Conjecture 5.5. Degree-\(4\) BFS avoidance is a statement about shortest paths.

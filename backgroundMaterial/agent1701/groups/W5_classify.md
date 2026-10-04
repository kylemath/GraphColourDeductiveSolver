# W5 — Colourings of \(T_{9,35}\) outside \(S\)

**Date:** 27 September 2026
**Group:** W5
**Status:** the \(1416\) colourings outside \(S\) were all classified. This file does not prove the Four Colour Theorem, and it does not revive the degree-\(4\) universal conjecture.

## Graph and set \(S\)

\(G\) is `generate_triangulations(9)[9][35]`, whose `graph['name']` is `T_9_35`. Vertex \(6\) has degree \(4\). \(H = G - 6\).

\(S\) is the \(24\) colourings in `exhaustive_details` of `backgroundMaterial/agent1545/coordinator/manager_M1/sub_S1/merge_tolerant_results.json` with `"graph": "T_9_35"` and `"vertex": 6`. The run is the proper \(5\)-colourings of \(G\) with \(c(6)=5\) that are not in \(S\). There are \(1440\) such colourings and \(24\) lie in \(S\), so the outside set has \(1416\).

W3 already ran the \(24\) colourings in \(S\). This pass does not rerun them, except for one sanity check.

## Command and time

```
/Users/fulkanjou/GraphColour/.venv/bin/python -u backgroundMaterial/agent1701/groups/w5_classify.py
```

Wall clock is \(1.431\) seconds. Of that, `generate_triangulations(9)` took \(1.197\) seconds and `enumerate_colourings` took \(0.005\) seconds. The one-path pass and the length-\(\mathrm{opt}+1\) searches on the unsafe colourings took \(0.152\) and \(0.010\) seconds. The ten-minute stop was not reached. All \(1416\) colourings finished.

The raw record is `backgroundMaterial/agent1701/groups/w5_classify_results.json`.

## Sanity check, one colouring in \(S\)

The published colouring \(0{:}1,1{:}2,2{:}3,3{:}4,4{:}5,5{:}3,6{:}5,7{:}2,8{:}5\) is in \(S\). On that colouring, `bfs_reduce_to_4` has length \(2\) and `check_path_safety` rejects it, so that one shortest path is K1-unsafe. `find_safe_bfs_path` returns `safe_path_exists` false, `reason` `"exhausted"`, `paths_checked` \(2\). `find_safe_nonoptimal_path` with `max_extra` \(= 1\) returns a path of length \(3\) that `check_path_safety` accepts. That matches the stored picture for this one colouring. The other \(23\) members of \(S\) were not rerun.

## What was tested

For each colouring outside \(S\), `bfs_reduce_to_4(H, c|_H, k=5)` returns one shortest path in \(\mathcal{R}(H,5)\). That path is counted as **one shortest path unsafe** when `check_path_safety` in `compute/kempe/verify_counterexamples.py` returns false. That function walks the path with `is_step_unsafe`.

A safe path of length \(\mathrm{opt\_dist}+1\) was searched only among those unsafe colourings, by `find_safe_nonoptimal_path(..., max_extra=1)`. A returned path is counted only when its length is \(\mathrm{opt\_dist}+1\), the last colouring of \(H\) uses at most four colours, and `check_path_safety` accepts it.

**Every shortest path unsafe** was tested, and the test was cheap. A colouring whose `bfs_reduce_to_4` path is safe is not in that count: that one shortest path is a witness. The \(8\) colourings whose sampled path is unsafe were passed to `find_safe_bfs_path`. Each call finished in under \(0.007\) seconds, \(3\) shortest paths were checked, and each call found a safe shortest path. No call hit `max_paths`.

## Counts

| Quantity | Value |
|---|---|
| Colourings outside \(S\) finished | \(1416\) |
| One shortest path unsafe | \(8\) |
| Sampled shortest path safe | \(1408\) |
| `bfs_reduce_to_4` returned no path | \(0\) |
| Every shortest path unsafe | \(0\) |
| Of the \(8\), a K1-safe path of length \(\mathrm{opt\_dist}+1\) | \(8\) |
| Elapsed seconds | \(1.431\) |

The eight sums are disjoint from the \(1408\), and \(8+1408=1416\). For each of those \(8\), `find_safe_nonoptimal_path` returned a path and `is_step_unsafe` agreed that the path is safe. There was no returned path that `check_path_safety` rejected, and no unsafe colouring for which the length-\(\mathrm{opt\_dist}+1\) search returned nothing.

`find_safe_bfs_path` found a safe shortest path on all \(8\), so none of them has every shortest path unsafe. Together with the \(1408\) safe sampled paths, the universal count on the outside set is \(0\).

BFS distances on the \(1416\) sampled paths were \(0\) for \(240\) colourings, \(1\) for \(792\), and \(2\) for \(384\).

## Not proved

This is one triangulation, not the Four Colour Theorem, and it does not revive the degree-\(4\) universal conjecture, which is already dead on one written colouring.

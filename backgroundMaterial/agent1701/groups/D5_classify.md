# D5b — Colourings of \(T_{9,25}\) at vertex 3

**Date:** 27 September 2026
**Group:** D5b
**Status:** the \(1248\) proper \(5\)-colourings with \(c(3)=5\) were all classified. This file does not prove the Four Colour Theorem.

## Graph

\(G\) is `generate_triangulations(9)[9][25]`. The generator’s return value is a dict keyed by order, and index \(25\) of the \(9\)-vertex list is the graph whose `graph['name']` is `T_9_25`. That is the triangulation `D5_witness.md` calls `generate_triangulations(9)[25]`. Vertex \(3\) has degree \(5\). \(H = G - 3\).

The run is every proper \(5\)-colouring of \(G\) returned by `enumerate_colourings(G, 5)` with \(c(3)=5\). There are \(6240\) proper \(5\)-colourings and \(1248\) of them have \(c(3)=5\). Of those \(1248\), \(1152\) use all five colours.

One written colouring, \(0{:}1,1{:}2,2{:}3,3{:}5,4{:}4,5{:}5,6{:}4,7{:}2,8{:}5\), already meets the kill for the universal statement that every shortest path is safe. It is one of these \(1248\). This count does not reopen that kill.

## Command and time

```
/Users/fulkanjou/GraphColour/.venv/bin/python -u backgroundMaterial/agent1701/groups/d5_classify.py
```

Wall clock is \(6.536\) seconds. Of that, `generate_triangulations(9)` took \(1.129\) seconds and `enumerate_colourings` took \(0.004\) seconds. `find_safe_bfs_path` took \(2.871\) seconds, the length-\(\mathrm{opt\_dist}+1\) searches took \(0.040\) seconds, and the residual shortest-path checks took \(2.471\) seconds. The ten-minute stop was not reached. All \(1248\) colourings finished.

The raw record is `backgroundMaterial/agent1701/groups/d5_classify_results.json`.

## What was tested

For each colouring, `find_safe_bfs_path` in `compute/kempe/verify_counterexamples.py` searches shortest paths in \(\mathcal{R}(H,5)\). A path is K1-safe when `check_path_safety` returns true. That function walks the path with `is_step_unsafe`.

**Every shortest path K1-unsafe** means `find_safe_bfs_path` returns `safe_path_exists` false and `reason` `"exhausted"`. On that set, `bfs_reduce_to_4` supplies `opt_dist`, and `find_safe_nonoptimal_path(..., max_extra=1)` searches for a longer path. A returned path is counted only when its length is \(\mathrm{opt\_dist}+1\), the last colouring of \(H\) uses at most four colours, and `check_path_safety` accepts it.

**Only some shortest path K1-unsafe** means a K1-safe shortest path exists, and some other shortest path fails `check_path_safety`. For \(40\) colourings, `find_safe_bfs_path` itself checked more than one shortest path before returning a safe one, so an earlier path had failed `is_step_unsafe`. For the colourings on which that call returned on its first path, a second walk of the shortest paths called `check_path_safety` and stopped at the first unsafe path. That second walk found an unsafe path on \(80\) further colourings. No call hit `max_paths`, and none reported that no \(4\)-colouring is reachable.

## Counts

| Quantity | Value |
|---|---|
| Proper \(5\)-colourings with \(c(3)=5\), finished | \(1248\) |
| Every shortest path K1-unsafe | \(24\) |
| Of those \(24\), a K1-safe path of length \(\mathrm{opt\_dist}+1\) | \(24\) |
| Only some shortest path K1-unsafe, and a safe shortest path exists | \(120\) |
| Every shortest path K1-safe | \(1104\) |
| Inconclusive, or no \(4\)-colouring reachable | \(0\) |
| Elapsed seconds | \(6.536\) |

The three classes \(24\), \(120\), and \(1104\) are disjoint and sum to \(1248\). Each of the \(24\) has \(\mathrm{opt\_dist}=2\), so the accepted longer path has length \(3\). `find_safe_nonoptimal_path` returned a path on all \(24\), and `is_step_unsafe` agreed that each path is safe. There was no returned path that `check_path_safety` rejected, and no colouring in the \(24\) for which the length-\(\mathrm{opt\_dist}+1\) search returned nothing.

Of the \(1104\) on which every shortest path is K1-safe, \(240\) are already \(4\)-coloured on \(H\), so the only shortest path has length \(0\).

The written colouring sits in the \(24\). Its path was not replayed again.

## Not proved

This is one triangulation. It is not the Four Colour Theorem. The universal statement that every shortest path is safe stays the one already met by the written colouring; this count does not reopen it.

Feasibility of reading these three counts off the run: **High**. The command finished in \(6.536\) seconds.

## Next steps

1. The critic gates this count. This file leaves the navigator unmarked.
2. The Four Colour Theorem is outside this count.

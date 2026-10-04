# W4 — Colourings of \(T_{9,35}\) with \(c(6)=5\), inside and outside \(S\)

**Date:** 27 September 2026
**Group:** W4
**Status:** three counts only. This file does not prove anything. It does not search paths, and it does not reopen the degree-4 universal shortest-path conjecture.

## Graph and set \(S\)

\(G\) is `generate_triangulations(9)[9][35]`. The generator returns a dict keyed by order, and the list at key \(9\) has \(50\) triangulations. Index \(35\) is the graph whose `graph['name']` is `T_9_35`. It has \(9\) vertices and \(21\) edges, and vertex \(6\) has degree \(4\). That is the graph the standing identification writes as `generate_triangulations(9)[35]`.

\(S\) is the set of colourings in `exhaustive_details` of `backgroundMaterial/agent1545/coordinator/manager_M1/sub_S1/merge_tolerant_results.json` with `"graph": "T_9_35"` and `"vertex": 6`. That list has \(24\) entries and \(24\) distinct colourings. Each of those \(24\) is a proper \(5\)-colouring of \(G\) with \(c(6)=5\).

## Command and time

```
/Users/fulkanjou/GraphColour/.venv/bin/python -u backgroundMaterial/agent1701/groups/w4_outside_count.py
```

`enumerate_colourings` is `compute/kempe/kempe_ops.py`, called as `enumerate_colourings(G, 5)`. Colours are the integers \(1,2,3,4,5\). The script then keeps the colourings with \(c(6)=5\) and splits them by membership in \(S\). Equality of colourings is equality of the \(9\)-tuple \((c(0),\ldots,c(8))\).

Wall clock is \(1.057\) seconds. Of that, `generate_triangulations(9)` took \(1.047\) seconds and `enumerate_colourings` took \(0.005\) seconds. The ten-minute stop was not reached. The outside set has more than \(30\) colourings, so this task did not path-search it.

## Counts

| Quantity | Value |
|---|---|
| Proper \(5\)-colourings of \(G\) with \(c(6)=5\) | \(1440\) |
| Of those, in \(S\) | \(24\) |
| Of those, outside \(S\) | \(1416\) |
| Elapsed seconds | \(1.057\) |

The enumerator returned \(7200\) proper \(5\)-colourings in total, and \(1440\) of them have \(c(6)=5\). Those \(1440\) are distinct. All \(24\) members of \(S\) occur among them, and \(1440-24=1416\).

These \(1440\) maps are labelled \(5\)-colourings of \(G\). They are not the \(600\) four-colourings named for \(T_{9,35}\) in `backgroundMaterial/agent1545/coordinator/manager_M1/sub_S1/S1_report.md`.

## Stop

The outside set has \(1416\) colourings, which is larger than \(30\). This task stops at the three counts. No path in the reconfiguration graph was computed. The degree-4 universal shortest-path conjecture is already a dead end on one written colouring; this count does not reopen it.

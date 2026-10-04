# K4 — K1-safe paths of length at most \(d+1\)

**Group:** K4 (M-Kempe, Track 1). **Date:** 2 October 2026.
**Status:** finite check on triangulations \(n=6,\ldots,10\). This is not a theorem.

## 1. Definitions

Implemented in `compute/kempe/a1720_k4_safe_plus1.py`. Colours are \(\{1,2,3,4,5\}\). \(G=T_{n,i}\) is the cached triangulation `compute/data/triangulations_n4_11.json`. For \(\deg v\in\{4,5\}\) and a proper \(5\)-colouring \(c\) of \(G\) with \(c(v)=5\), write \(H=G-v\) and \(c_H=c|_H\).

- \(\mathcal{R}(H,5)\): proper \(5\)-colourings of \(H\), edges given by one Kempe swap.
- \(d(c)\): BFS distance in \(\mathcal{R}(H,5)\) from \(c_H\) to a colouring using at most four colours (same target as `bfs_reduce_to_4`).
- \(s_1(c)\): least length of a K1-safe path to that target. A step is unsafe when `is_unsafe` holds in `classify_path_safety` (`backgroundMaterial/agent1701/groups/K3_weaker_spec.md` §1).
- **T2.** \(d_2(c)\) and \(s_2(c)\) are the same two quantities for the stronger target: a \(4\)-colouring \(c'\) of \(H\) that extends to a proper \(4\)-colouring of \(G\) by recolouring \(v\) alone (some colour \(x\notin c'(N(v))\) with \(|c'(V(H))\cup\{x\}|\le 4\)).
- **T3.** \(d_G(c)\) is the BFS distance in \(\mathcal{R}(G,5)\) from \(c\) to a \(4\)-colouring of \(G\). \(t_3(c)\) is the least length of a path to such a colouring on which every swapped chain \(K\) satisfies: \(K\setminus\{v\}\) is empty or is a single Kempe chain of \(H\).

Distances are constant on orbits under permutations of colours \(\{1,2,3,4\}\) (colour \(5\) fixed). Weighted counts multiply by orbit size.

## 2. Statement

For every triangulation on \(n\le 10\) vertices, every \(v\) with \(\deg v\in\{4,5\}\), and every proper \(5\)-colouring \(c\) with \(c(v)=5\), one has \(s_1(c)\le d(c)+1\).

## 3. Evidence

```
compute/kempe/a1720_k4_safe_plus1.py --nmin 6 --nmax 11 --procs 3
```

Command string stored in `backgroundMaterial/agent1720/groups/K4_results.json`. Per-order wall times: \(n=6\), \(0.140\,\mathrm{s}\); \(n=7\), \(0.153\,\mathrm{s}\); \(n=8\), \(0.232\,\mathrm{s}\); \(n=9\), \(0.884\,\mathrm{s}\); \(n=10\), \(8.203\,\mathrm{s}\). Sum \(9.612\,\mathrm{s}\). The file has no `stopped_reason` and no \(n=11\) block: \(n=11\) was not run.

Independent check, \(n=6,7,8\) (labelled colourings, no quotient, against `classify_path_safety` and `bfs_reduce_to_4`):

```
.venv/bin/python compute/kempe/a1720_k4_safe_plus1.py --verify 8
```

`K4_verify.json`: \(44424\) records, \(0\) mismatches, \(457\) BFS checks, \(0\) BFS mismatches, \(21.916\,\mathrm{s}\). The record count equals the weighted colouring count for \(n=6,7,8\).

## 4. Result

Computed, on \(n=6,\ldots,10\) only. Range: \(304\) triangulations, \(1406\) pairs \((G,v)\), \(129171\) orbits, \(3099720\) weighted colourings. For every such orbit, \(s_1-d\in\{0,1\}\). The weighted counts with \(s_1-d=1\) are \(48\) at \(n=9\) and \(2664\) at \(n=10\); every other weighted colouring has \(s_1-d=0\). `first_failures["K4_s1_gt_d+1"]` is empty at each \(n\), and that key is absent from the failure counters.

T2 and T3 fail the same \(+1\) bound measured against \(d\). Weighted failures of \(s_2>d+1\): \(61152\). Weighted failures of \(t_3>d+1\): \(268632\). The lists `T2_s2_gt_d2+1` and `T3_t3_gt_dG+1` are empty on this range: \(s_2\le d_2+1\) and \(t_3\le d_G+1\) held wherever they were counted.

A K1-safe path to a \(4\)-colouring of \(H\) does not yield a \(4\)-colouring of \(G\). Smallest stored \(T_{6,0}\) failure of T2 against \(d\), from

```
.venv/bin/python -c "import json; d=json.load(open('backgroundMaterial/agent1720/groups/K4_results.json')); xs=[r for r in d['by_n']['6']['first_failures']['T2_s2_gt_d+1'] if r['graph']=='T_6_0']; print(min(xs, key=lambda r: r['vertex']))"
```

\(T_{6,0}\), vertex \(0\), degree \(5\), colouring \(0{:}5,1{:}1,2{:}2,3{:}3,4{:}4,5{:}2\), with \(d=0\), \(s_1=0\), \(d_2=2\), \(s_2=2\), \(d_G=2\), \(t_3=2\). The empty path is K1-safe and \(c_H\) already uses four colours, so \(s_1=d=0\). All four colours appear on \(N(0)\), so \(c_H\) does not extend by recolouring the vertex, and \(s_2=2>d+1\). The same distances occur at vertex \(1\).

## 5. Kill criterion

One instance with no K1-safe path of length \(\le d+1\). **Not met.**

## 6. Not proved

The check is finite. It does not cover \(n=11\), \(n<6\), non-triangulations, or all planar graphs. It does not prove \(s_1\le d+1\) in general, and the \(T_{6,0}\) witness shows that the K1-safe target is the wrong inductive target for a \(4\)-colouring of \(G\).

## 7. Feasibility

Extending the same count to \(n=11\): **Medium** (\(n=10\) took \(8.2\,\mathrm{s}\); \(n=11\) has \(1249\) triangulations). A theorem: **Low**.

## 8. Next steps

1. Run the same script at \(n=11\) under the ten-minute budget and record a stop if it exceeds it.
2. Treat \(s_2\le d_2+1\) as a separate finite statement. On \(n\le 10\) its failure list is empty; that emptiness is still only a finite check.
3. Drop \(s_1\le d+1\) as a route to the Four Colour Theorem. The \(T_{6,0}\) colouring is already a counterexample to “a K1-safe \(4\)-colouring of \(G-v\) \(4\)-colours \(G\)”.

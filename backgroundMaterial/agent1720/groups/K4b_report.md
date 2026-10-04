# K4b — K1-safe bounds at \(n=11\)

**Group:** K4b (M-Kempe, Track 1). **Date:** 2 October 2026.
**Status:** finite check on triangulations \(n=11\). This is not a theorem.

## 1. Definitions

Same as `compute/kempe/a1720_k4_safe_plus1.py` (`run`, `analyse_graph`, `multi_bfs`). Colours are \(\{1,2,3,4,5\}\). \(G=T_{11,i}\) is `compute/data/triangulations_n4_11.json`. For \(\deg v\in\{4,5\}\) and a proper \(5\)-colouring \(c\) with \(c(v)=5\), write \(H=G-v\).

- \(d(c)\): BFS distance in \(\mathcal{R}(H,5)\) from \(c|_H\) to a colouring using at most four colours.
- \(s_1(c)\): least length of a K1-safe path to that target (`is_unsafe` in `classify_path_safety`).
- \(d_2(c)\), \(s_2(c)\): the same two quantities for target T2, a \(4\)-colouring of \(H\) that extends to a proper \(4\)-colouring of \(G\) by recolouring \(v\) alone.

Orbits are under permutations of colours \(\{1,2,3,4\}\) (colour \(5\) fixed). Weighted counts multiply by orbit size.

## 2. Statement

For every triangulation on \(11\) vertices, every vertex \(v\) with \(\deg v\in\{4,5\}\), and every proper \(5\)-colouring \(c\) with \(c(v)=5\): \(s_1(c)\le d(c)+1\) and \(s_2(c)\le d_2(c)+1\).

## 3. Evidence

`/Users/fulkanjou/GraphColour/.venv/bin/python`, module `compute/kempe/a1720_k4_safe_plus1.py`. The global `OUT` was set to `backgroundMaterial/agent1720/groups/K4_n11.json` before `run(11, 11, 2, 600)`. Two worker processes. The \(n=11\) block records `elapsed_seconds` \(152.333\). The process that called `run` took \(159.308\,\mathrm{s}\) wall clock, under the \(600\,\mathrm{s}\) stop. No `stopped_reason`. `K4_results.json` still has only \(n=6,\ldots,10\).

## 4. Result

Computed, on \(n=11\) only. Range: \(1249\) triangulations, \(6107\) pairs \((G,v)\), \(1365522\) orbits, \(32772372\) weighted colourings.

\(s_1\le d+1\) holds on every orbit. Weighted counts with \(s_1-d=1\): \(29544\) at degree \(4\) and \(37512\) at degree \(5\). Every other weighted colouring has \(s_1-d=0\). `first_failures["K4_s1_gt_d+1"]` is empty.

\(s_2\le d_2+1\) holds on every orbit. `first_failures["T2_s2_gt_d2+1"]` is empty. The weighted pairs \((d_2,s_2)\) are only \((k,k)\) and \((k,k+1)\).

The bound \(s_2\le d+1\) fails. Weighted failures: \(664872\) (\(27703\) orbits). One stored example: \(T_{11,1}\), vertex \(8\), degree \(5\), colouring \(0{:}1,1{:}2,2{:}3,3{:}4,4{:}3,5{:}4,6{:}3,7{:}4,8{:}5,9{:}3,10{:}4\), with \(d=0\), \(s_1=0\), \(d_2=2\), \(s_2=2\). The colouring is proper, \(c(H)\) uses \(\{1,2,3,4\}\), and no colour extends it by recolouring vertex \(8\).

## 5. Kill criterion

One orbit with \(s_1>d+1\), or one orbit with \(s_2>d_2+1\). **Not met.**

## 6. Not proved

The check is finite. It is not a theorem. It does not cover \(n>11\), \(n<11\) in this file, non-triangulations, or all planar graphs. It does not \(4\)-colour \(G\). The \(T_{11,1}\) colouring has \(s_2=2>d+1\).

## 7. Feasibility

A general proof of either bound: **Low**. The same script at \(n=12\): **Low** (\(n=12\) is not in the cache; \(n=11\) already took \(152\,\mathrm{s}\) with two processes).

## 8. Next steps

1. Keep \(s_1\le d+1\) and \(s_2\le d_2+1\) labelled as finite checks through \(n=11\).
2. Do not use a K1-safe \(4\)-colouring of \(G-v\) as an inductive \(4\)-colouring of \(G\). The \(T_{11,1}\) distances are a fresh instance of that gap.
3. Leave \(K4_results.json\) unchanged.

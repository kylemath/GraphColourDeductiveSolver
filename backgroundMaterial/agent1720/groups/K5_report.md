# K5 — Kempe reducibility \(5\to 4\), and monotone reduction

**Group:** K5 (M-Kempe, Track 1). **Date:** 2 October 2026.
**Status:** Part A is a finite check plus a literature reformulation. Non-strict monotone reduction is a finite check. The strict version is killed. None of this is a theorem, and Meyniel’s theorem is not proved here.

## 1. Definitions

Implemented in `compute/kempe/a1720_k5_reconfig.py`. \(f(c)=|c^{-1}(5)|\).

- **Part A.** \(\mathcal{R}(G,5)\) modulo \(S_5\): states are set-partitions of \(V(G)\) into at most five independent blocks. The script checks connectivity and that every class contains a colouring with at most four colours. The quotient is exact: a global colour permutation is a product of Kempe swaps, and Kempe adjacency commutes with relabelling, so components of the quotient are the Kempe classes.
- **Part C, non-strict.** Work modulo \(S_4\) on colours \(\{1,2,3,4\}\), fixing colour \(5\). A colouring is monotone-good when some Kempe path from it ends at \(f=0\) and \(f\) never increases along the path.
- **Strict version.** The plateau cost \(g(c)\) is the least \(L\) such that some monotone path to \(f=0\) has every run of consecutive \(f\)-preserving swaps of length at most \(L\). Then \(g(c)=0\) means a strictly \(f\)-decreasing path to \(f=0\): whenever \(f>0\), the next swap decreases \(f\). `states_without_decreasing_swap` counts states with \(f>0\) and no neighbour of strictly smaller \(f\).

`compute/kempe/a1720_k5_verify.py` rebuilds labelled \(\mathcal{R}(G,5)\) for \(n\le 8\) with `kempe_ops.py` and extracts one optimal monotone path at each order.

## 2. Statement

**Part A.** For every cached triangulation on \(n\le 11\) vertices, \(\mathcal{R}(G,5)\) is connected and every Kempe class contains a \(4\)-colouring.

**Literature sentence.** Given Meyniel’s theorem, “every proper \(5\)-colouring of a planar graph Kempe-reduces to a \(4\)-colouring” is a reformulation of the Four Colour Theorem.

**Part C.** From every proper \(5\)-colouring of every such triangulation there is a Kempe path along which \(f\) never increases and which ends at \(f=0\). The strict variant asks for a decreasing swap whenever \(f>0\).

## 3. Evidence

Part A and Part C are the per-order runs of

```
.venv/bin/python compute/kempe/a1720_k5_reconfig.py A 4 5 6 7 8 9 10 11
.venv/bin/python compute/kempe/a1720_k5_reconfig.py C 4 5 6 7 8 9 10 11
```

The JSON files do not store `argv`. They do store one summary per order from \(4\) through \(11\), which is what that entry point writes. Output: `K5_partA_raw.json`, `K5_partC_raw.json`.

Part A, \(n=11\): \(1249\) graphs, \(263977\) orbits, \(31677120\) labelled colourings, \(9.12\,\mathrm{s}\). Every order \(n\le 11\) has `all_connected` true and `all_classes_contain_le4` true.

Part C: `monotone_failures` is \(0\) at every \(n\le 11\), and `graphs_with_failures` is empty. The sequence of `max_plateau` for \(n=4,\ldots,11\) is \(0,1,2,3,3,4,4,5\). The \(n=11\) block took \(49.82\,\mathrm{s}\) (\(1249\) graphs, \(1319883\) orbits under \(S_4\), \(209635\) states with no decreasing swap).

Cross-check:

```
.venv/bin/python compute/kempe/a1720_k5_verify.py
```

`K5_verify.json`: `elapsed_seconds` \(5.42\), `cross_check_elapsed_seconds` \(3.2\). For each \(n=4,\ldots,8\), `connectivity_agrees` is true and `max_plateau_mismatches` is \(0\).

**Meyniel.** Henri Meyniel, “Les \(5\)-colorations d’un graphe planaire forment une classe de commutation unique”, *J. Combin. Theory Ser. B* **24** (1978), 251–258: the proper \(5\)-colourings of any planar graph form a single Kempe class. This report cites that theorem and does not prove it. Related Kempe-equivalence results, not used as a proof of anything here: Las Vergnas–Meyniel, *J. Combin. Theory Ser. B* **31** (1981), 95–104; Mohar, “Kempe equivalence of colorings”, in *Graph Theory in Paris* (2006); Bonamy–Bousquet–Feghali–Johnson, *J. Combin. Theory Ser. B* **135** (2019), 179–199, on Mohar’s conjecture for regular graphs.

## 4. Result

**Part A, computed.** On every triangulation \(n\le 11\), the \(S_5\)-quotient is connected and every class contains a \(4\)-colouring. The \(n\le 8\) labelled rebuild agrees.

**Reformulation, literature.** Let \(P\) be the Four Colour Theorem and let \(Q\) be: every proper \(5\)-colouring of a planar graph is Kempe-equivalent to some proper \(4\)-colouring. The Five Colour Theorem supplies a \(5\)-colouring. Meyniel says there is only one Kempe class. Under that citation, \(Q\) implies \(P\), and \(P\) implies \(Q\) because a \(4\)-colouring sits in that unique class. So \(Q\), given Meyniel, is a reformulation of \(P\). A reformulation is not a kill. The finite check is consistent with \(Q\) on triangulations \(n\le 11\) and does not establish \(Q\).

**Part C, computed.** Non-strict monotone reduction has \(0\) failures on triangulations \(n\le 11\). Plateaus occur: `max_plateau` reaches \(5\) at \(n=11\).

**Strict version, killed.** Witness in `K5_verify.json`, the \(n=5\) entry:

\(T_{5,0}\), colouring \((1,2,3,5,4)\) on vertices \(0,\ldots,4\), \(f=1\), `least_plateau_bound_labelled` \(=1\), `least_plateau_bound_quotient` \(=1\), `path_with_bound_minus_one_exists` false. Optimal path: swap colours \((3,4)\) on chain \(\{2\}\), reaching \((1,2,4,5,4)\) with \(f=1\); then swap colours \((3,5)\) on chain \(\{3\}\), reaching \((1,2,4,3,4)\) with \(f=0\). The first swap preserves \(f\). Vertex \(3\) is adjacent to colours \(1,2,3,4\), so no swap decreases \(f\) from this colouring. At \(n=5\) the Part C summary records \(3\) states with no decreasing swap, and `max_plateau` \(=1\).

## 5. Kill criterion

Part C, as issued: one colouring with no monotone path to \(f=0\). **Not met** for the non-strict statement.

Strict statement (“a decreasing swap whenever \(f>0\)”): **met**, by the \(T_{5,0}\) witness above.

Part A / the reformulation \(Q\): a reformulation is not killed.

## 6. Not proved

Meyniel’s theorem is cited, not proved. Connectivity and the presence of a \(4\)-colouring are checked only for triangulations \(n\le 11\). Non-strict monotone reduction on that range is a finite check, not a theorem for all planar graphs. The strict statement is false.

## 7. Feasibility

A proof of non-strict monotone reduction for every planar triangulation: **Low** (the needed plateau already grows \(0,1,2,3,3,4,4,5\)). Further finite checks: **Medium**. The strict statement is dead.

## 8. Next steps

1. Leave the strict variant. \(T_{5,0}\) kills it.
2. Keep \(Q\) labelled as a reformulation of the Four Colour Theorem, conditional on Meyniel 1978.
3. If non-strict monotone reduction is pursued, the next computation is \(n=12\), with the plateau bound recorded. A uniform proof is not suggested by the growth of `max_plateau`.

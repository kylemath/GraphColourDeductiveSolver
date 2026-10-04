# K3 — Specification: a K1-safe path of length 3 on the stored colourings of \(T_{9,35}\)

**Group:** K3
**Date:** 27 September 2026
**Status:** specification only. This document does not prove the sentence in §2.

The degree-4 conjecture that every shortest path avoids unsafe swaps stays outside this file. A written counterexample already meets the kill criterion of `backgroundMaterial/agent1701/groups/K1_spec.md` §6: the triangulation \(T_{9,35}\), vertex \(6\), the colouring \(0{:}1,1{:}2,2{:}3,3{:}4,4{:}5,5{:}3,6{:}5,7{:}2,8{:}5\), and the length-\(2\) path whose \((3,5)\)-step swaps \(\{2,8\}\). That witness is `backgroundMaterial/agent1701/groups/W_path.md`. This specification does not reopen it.

The sentence below is the weaker existence claim supported by `backgroundMaterial/agent1701/groups/W3_batch.md`. A safe path of length \(3\) is longer than the BFS distance \(2\) recorded there, so it is not a shortest path and it is not Degree-\(4\) BFS Avoidance.

---

## 1. Definitions

Colours are \(\{1,2,3,4,5\}\). Let \(G\) be the labelled triangulation `generate_triangulations(9)[35]`, named \(T_{9,35}\). Let \(v = 6\) and \(H = G - v\). Vertex \(6\) has degree \(4\).

**Proper \(5\)-colouring.** A map \(c \colon V(G) \to \{1,2,3,4,5\}\) is a proper \(5\)-colouring when \(uv \in E(G)\) implies \(c(u) \neq c(v)\). The same definition applies to \(H\). This is `is_proper_colouring` in `compute/kempe/kempe_ops.py`.

**\((a,5)\)-Kempe chain.** For \(a \in \{1,2,3,4\}\) and a vertex \(x\) of \(H\) with colour in \(\{a,5\}\), the \((a,5)\)-Kempe chain of \(x\) is the vertex set of the connected component of \(x\) in the subgraph of vertices coloured \(a\) or \(5\). This is `get_kempe_chain` in `compute/kempe/kempe_ops.py`.

**Reconfiguration graph \(\mathcal{R}(H,5)\).** Vertices are the proper colourings of \(H\) with values in \(\{1,2,3,4,5\}\). Two colourings are adjacent when one is obtained from the other by swapping the two colours on a single Kempe chain.

**Length.** A path in \(\mathcal{R}(H,5)\) is a sequence of proper colourings of \(H\) in which consecutive colourings differ by one Kempe swap. Its length is the number of swaps, one less than the number of colourings in the sequence. `bfs_reduce_to_4` and `find_safe_nonoptimal_path` return lists of canonical colourings. The W3 record sets `opt_dist` and `path_length` to the length of those lists minus one. The older JSON field `bfs_path_length` counts colourings, not swaps (`backgroundMaterial/agent1701/groups/W_path.md` §2). This specification uses the swap count.

**BFS distance.** For a proper colouring \(c\) of \(G\), the BFS distance of \(c|_H\) is the minimum length of a path in \(\mathcal{R}(H,5)\) from \(c|_H\) to a proper colouring of \(H\) that uses at most four colours. `bfs_reduce_to_4` in `compute/kempe/reduction_search.py` returns one breadth-first path to such a colouring. In the W3 run the BFS distance is `opt_dist = len(bfs_path) - 1` for the list that function returns. For every stored colouring that was run, that value is \(2\).

**Step that meets the K1 kill test.** Fix a colouring \(c_i\) of \(H\) and a step that replaces \(c_i\) by a Kempe swap of one chain. The step meets the K1 kill test when, for some \(a \in \{1,2,3,4\}\), the step swaps an \((a,5)\)-Kempe chain \(K\) of \((H, c_i)\), the chain \(K\) contains a neighbour of vertex \(6\), and at least two neighbours of vertex \(6\) lie in distinct \((a,5)\)-Kempe chains of \((H, c_i)\). That is the step clause of `backgroundMaterial/agent1701/groups/K1_spec.md` §6. It is the flag `is_unsafe` in `classify_path_safety` (`compute/kempe/all_paths_analysis.py`): `merge_prone_at_step` holds and the swapped chain is one of the chains that meet \(N(6)\).

**Safe step.** A step that does not meet the K1 kill test. Equivalently, whenever the step swaps an \((a,5)\)-Kempe chain \(K\) and at least two neighbours of vertex \(6\) lie in distinct \((a,5)\)-chains of the colouring present before the step, the chain \(K\) contains no neighbour of vertex \(6\).

**Safe path.** A path on which every step is safe. `classify_path_safety` records this as `path_is_safe`. `find_safe_nonoptimal_path` in `compute/kempe/counterexample_energy_targeted.py` returns a path only after that flag is true.

The K1 kill of Degree-\(4\) BFS Avoidance also requires the path to be a shortest path. A safe path of length \(3\), with BFS distance \(2\), fails that requirement. Safety in this file is the step predicate alone.

---

## 2. Statement

Let \(G = T_{9,35}\) be `generate_triangulations(9)[35]`, let vertex \(v = 6\), and let \(H = G - v\). Let \(S\) be the set of \(24\) colourings stored with `"graph": "T_9_35"` and `"vertex": 6` in `exhaustive_details` of `backgroundMaterial/agent1545/coordinator/manager_M1/sub_S1/merge_tolerant_results.json`. That set equals the set of such colourings in `ce_details` of the same file, and it contains the three records in `backgroundMaterial/agent1520/coordinator/manager_M1/sub_S3/counterexample_details.json` with `"vertex": 6` and `"degree": 4`.

**Sentence.** For every \(c \in S\), \(c\) is a proper \(5\)-colouring of \(G\) with \(c(6) = 5\), \(c|_H\) is a proper \(5\)-colouring of \(H\), the BFS distance in \(\mathcal{R}(H,5)\) from \(c|_H\) to a proper colouring of \(H\) that uses at most four colours is \(2\), and there exists a path of length \(3\) in \(\mathcal{R}(H,5)\) from \(c|_H\) to a proper colouring of \(H\) that uses four colours, such that every step is safe: no step meets the K1 kill test.

The quantifier is \(c \in S\). \(S\) is the stored list W3 ran, once each. W3 did not range over planar graphs, over triangulations other than \(T_{9,35}\), or over the proper \(5\)-colourings of \(T_{9,35}\) that are absent from \(S\).

---

## 3. Acceptance test for a wider statement

A future proof of any wider statement has to name its own quantifiers and discharge them. The W3 run discharges only §2.

**Extension to every proper \(5\)-colouring of \(T_{9,35}\) with colour \(5\) at vertex \(6\).** Write \(S^\star\) for that set. A proof that §2 holds with \(S^\star\) in place of \(S\) must show \(S^\star = S\), or must apply the same test to every colouring in \(S^\star \setminus S\): properness of \(c\) and of \(c|_H\), BFS distance \(2\), and a path of length \(3\) to a proper colouring of \(H\) that uses four colours, with no step meeting the K1 kill test. Citing the \(24\) returned paths does not cover a colouring that was not run.

**Any planar graph other than \(T_{9,35}\), or any vertex other than \(6\).** A separate argument is required. The acceptance test of Degree-\(4\) BFS Avoidance in `K1_spec.md` §3 (every planar graph, every proper colouring, every vertex of degree \(4\) coloured \(5\), every shortest path) is a different sentence. The length-\(2\) witness in `W_path.md` already meets the K1 kill criterion for that sentence. A proof of a longer-path statement does not restore it.

**What this computation does not replace.**

| Source | What it supplies | What it leaves open |
|---|---|---|
| `w3_batch_search.py` calling `find_safe_nonoptimal_path` with `max_extra` \(= 3\) | One path of length \(3\), accepted by `classify_path_safety` as `path_is_safe`, for each \(c \in S\) | Every proper \(5\)-colouring of \(T_{9,35}\) outside \(S\); every other graph |
| `bfs_reduce_to_4` on those \(24\) restrictions | BFS distance \(2\) for each \(c \in S\) | The distance for a colouring outside \(S\) |
| `W_path.md`, the length-\(2\) path swapping \(\{2,8\}\) | The K1 kill of “every shortest path avoids unsafe swaps” on one colouring in \(S\) | Existence of a safe path of length \(3\). `safe_path_exists: false` in that record is the result of a search that stops at the BFS distance |
| Agent 1419’s sentence that all \(24\) colourings are salvageable at distance \(3\) | An assertion in `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md` | A theorem. The checked fact is one K1-safe path of length \(3\) for each map in \(S\) |

The run also does not replace the Four Colour Theorem, an inductive claim that a safe path of length one more than the BFS distance always exists, or Kempe reducibility of an arbitrary planar triangulation.

---

## 4. Evidence

W3 ran the stored list to completion. The command was

```
/Users/fulkanjou/GraphColour/.venv/bin/python -u backgroundMaterial/agent1701/groups/w3_batch_search.py
```

| Quantity | Value | Where it is written |
|---|---|---|
| Colourings in \(S\), run once each | \(24\) | `W3_batch.md` §1 and §3; `w3_batch_results.json` fields `n_unique` and `n_ran` |
| `exhaustive_details` entries with graph \(T_{9,35}\) and vertex \(6\) | \(24\) | `W3_batch.md` §1; JSON `n_exhaustive_entries` |
| `ce_details` entries with the same graph and vertex | \(24\), the same set | `W3_batch.md` §1; JSON `n_ce_entries` |
| Degree-\(4\) records at vertex \(6\) in `counterexample_details.json` | \(3\), already in \(S\) | `W3_batch.md` §1; JSON `n_degree4_entries` |
| Returned a path | \(24\) | `W3_batch.md` §3; JSON `n_path` |
| Returned `None` | \(0\) | `W3_batch.md` §3; JSON `n_none` |
| `bfs_reduce_to_4` returned no path | \(0\) | `W3_batch.md` §3; JSON `n_no_bfs_path` |
| BFS distance on each of the \(24\) | \(2\) | `W3_batch.md` §3; each result `opt_dist` |
| Length of the returned path on each of the \(24\) | \(3\) | `W3_batch.md` §3; each result `path_length`; JSON `lengths` |
| Colours on the last colouring of \(H\) | \(4\) | `W3_batch.md` §3; each result `end_colours` |
| Elapsed wall clock | \(1.164\) seconds | `W3_batch.md` §2; JSON `elapsed_seconds` \(= 1.16413075\) |

The wall clock includes loading the JSON files (\(0.0005\) seconds in `W3_batch.md` §2; JSON `load_seconds` \(= 0.000481542\)) and `generate_triangulations(9)` (\(1.108\) seconds; JSON `generate_seconds` \(= 1.108354\)). Each call of `bfs_reduce_to_4` and `find_safe_nonoptimal_path` finished in under \(0.003\) seconds. The ten-minute stop was not reached. `stopped_reason` is null.

The per-colouring record, including swap pairs and vertex sets, is `backgroundMaterial/agent1701/groups/w3_batch_results.json`. The published colouring of `W_path.md` is result index \(0\). `W3_batch.md` §4 records the next colouring in `exhaustive_details`, \(0{:}1,1{:}2,2{:}4,3{:}3,4{:}5,5{:}4,6{:}5,7{:}2,8{:}5\), with BFS distance \(2\) and returned length \(3\).

`find_safe_nonoptimal_path` returns a list only when `classify_path_safety` sets `path_is_safe`. That is the sense in which the \(24\) returned paths are safe. This specification did not re-run the search.

---

## 5. Kill criterion

The sentence in §2 is false if there exists one colouring \(c \in S\) for which no path of length \(3\) in \(\mathcal{R}(H,5)\) from \(c|_H\) to a proper colouring of \(H\) that uses four colours is safe.

A witness is that one stored colouring, together with an argument that every length-\(3\) path from \(c|_H\) to a four-colouring of \(H\) has a step meeting the K1 kill test, or that no length-\(3\) path from \(c|_H\) ends at a four-colouring of \(H\).

The following do not meet this criterion.

- The length-\(2\) path in `W_path.md` that swaps \(\{2,8\}\). That path meets the K1 kill criterion for Degree-\(4\) BFS Avoidance. It has the wrong length for §2.
- A colouring of \(T_{9,35}\) that is not in \(S\).
- A graph other than \(T_{9,35}\), or a vertex other than \(6\).
- A safe path of some length other than \(3\), while a safe path of length \(3\) is still present. Existence of one safe path of length \(3\) is the whole claim. The sentence does not say that every path of length \(3\) is safe.

The W3 record does not meet the criterion: `n_path` is \(24\) and `n_none` is \(0\).

---

## 6. Not proved

The sentence in §2 is not proved in this document.

`W3_batch.md` and `w3_batch_results.json` record that a program returned a path of length \(3\) for each of the \(24\) stored colourings, and that the returning function requires `path_is_safe`. That is a computation on \(S\). It is not a written proof, and it is not a proof for a colouring outside \(S\).

Degree-\(4\) BFS Avoidance is the conjecture already met by the witness in `W_path.md`. This file does not prove a replacement for it. The Four Colour Theorem is unproved.

---

## 7. Feasibility

**Medium-High.**

The extension in view is the sentence of §2 with \(S\) replaced by the set of every proper \(5\)-colouring of this one triangulation \(T_{9,35}\) that colours vertex \(6\) with colour \(5\). A proper \(5\)-colouring with \(c(6) \neq 5\) is not an instance of §2: the K1 kill test used here assumes the vertex is coloured \(5\).

On \(S\), each call of `bfs_reduce_to_4` and `find_safe_nonoptimal_path` finished in under \(0.003\) seconds, and the W3 wall clock was \(1.164\) seconds, of which \(1.108\) seconds was `generate_triangulations(9)`. The same test is what a check of any colouring outside \(S\) has to run, unless a separate argument shows that no such colouring exists. W3 did not enumerate the proper \(5\)-colourings of \(T_{9,35}\). The distance \(2\) and the length \(3\) are the values measured on \(S\). A colouring with \(c(6) = 5\) that is not in \(S\) can have a different BFS distance, and then a path of length \(3\) need not end at a four-colouring. The missing step is that finite enumeration on this graph. The stored searches did not approach the ten-minute bound, and the quantifier does not grow beyond \(T_{9,35}\).

# Critic gate — witness for \(T_{9,35}\), vertex 6

**Critic date:** 27 September 2026
**Inputs opened:** `backgroundMaterial/agent1701/coordinator/manager_MWitness/manager_report.md`, `backgroundMaterial/agent1701/groups/W_graph.md`, `backgroundMaterial/agent1701/groups/W_path.md`, K1 kill criterion in `backgroundMaterial/agent1701/groups/K1_spec.md` §6, `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md` (the length-3 salvage sentences), and `backgroundMaterial/agent1520/coordinator/manager_M1/sub_S3/counterexample_details.json`.
**Replay:** the first vertex-6 degree-4 object in that JSON, in `.venv`, against `is_proper_colouring`, `get_kempe_chain`, `kempe_swap`, and `bfs_reduce_to_4`. The script timer printed \(0.0\) seconds; the process finished in about \(0.1\) seconds. `nx.check_planarity` on the same edge list returned true. `generate_triangulations(9)` was not called again in this gate. `docs/navigator/` was not edited.

The Four Colour Theorem is unproved. This gate does not mark it dead.

---

## 1. M-Witness

### Solid

The report argues from written objects. The edge list, the colouring table, and both steps are in the manager file, copied from W-graph and W-path, and the JSON quotations match the file.

Spot-check, first object with `"vertex": 6` and `"degree": 4`. The file has 6 objects. That object is 0-based index 3.

- Colour of vertex 6: `"6": 5`.
- The unsafe step is step 0: `"swap_pair": [3, 5]`, `"swapped_vertices": [2, 8]`.

The same object has `"neighbours": [0, 1, 2, 5]`, `"bfs_path_length": 3`, and two steps. Step 1 has `"is_unsafe": false`, `"swap_pair": [3, 4]`, `"swapped_vertices": [3]`. Neighbour 2 is in the swapped set of step 0. Those quotations in the manager report are the file.

The length distinction is right. `"bfs_path_length": 3` counts colourings in the list from `bfs_reduce_to_4`. The path in \(\mathcal{R}(H,5)\) has two swaps, so length 2. The replay called `bfs_reduce_to_4` on \(c|_{G-6}\) and got that same sequence: swap \((3,5)\) on \(\{2,8\}\), then swap \((3,4)\) on \(\{3\}\), ending at a proper colouring of \(H\) with colours \(\{1,2,3,5\}\).

The chain condition is in the replay, and it matches K1 §6. Before the \((3,5)\)-swap, the chain of neighbour 2 is \(\{2,8\}\) and the chain of neighbour 5 is \(\{4,5\}\). Those sets are distinct. The swapped chain is \(\{2,8\}\), which contains neighbour 2. \(G\) has 9 vertices and 21 edges, vertex 6 has degree 4, \(c(6)=5\), and both \(c\) and \(c|_H\) are proper and use five colours. The edge list is planar. One shortest path of this form makes the universal degree-4 sentence false. K1 §6 asks for one such path.

The reading of `"verification"` is careful. `"safe_path_exists": false`, `"paths_checked": 2`, `"unsafe_count": 2`, `"reason": "exhausted"` is the flag of a search that stops at the BFS distance. The manager does not turn that flag into “no longer safe path exists.” Degree 5 and the Four Colour Theorem are left untouched. The second shortest path is named as unwritten. That is the right boundary: the kill needs one shortest path, and a count of two is not a second written path.

### Still soft

The decision line **ACCEPT WITNESS** sits in the manager report. The critic gates the witness. The report does say the navigator node is unmarked and that the critic still gates, so the line is a recommendation in the decision slot. The objects under it are what the gate uses.

The kill paragraph states the chains \(\{2,8\}\) and \(\{4,5\}\) and the terminal 4-colouring in the same voice as the JSON fields. W-path already says the JSON does not store those sets or that colouring. They are replay output. The spot-check section of the manager report keeps the JSON fields and the replay apart; the kill paragraph joins them. The join is justified once the replay is in W-path, and this gate’s replay found the same sets and the same terminal colouring. The attribution in that one paragraph is smoother than the file. It does not change the criterion.

“Every shortest path of this colouring is unsafe” is still the verification count. The second path is not in the JSON and not in W-path. That gap does not save the universal conjecture, which fails as soon as one shortest path hits. It does block any reading of this packet as a written proof that both shortest paths hit, and it blocks the Agent 1419 sentence about all 24 colourings.

The manager did not re-run the replay. This gate did. The copy matched the object.

---

## 2. Real progress versus hot air

### Real

The witness is a graph, a colouring, and a path, checked against the kill criterion.

- Planar graph: the edge list of JSON index 3, 21 edges on vertices \(\{0,\ldots,8\}\). Planarity checked in this gate. W-graph identifies the same list with `generate_triangulations(9)[35]`, named `T_9_35`. That generator call was not repeated here.
- Proper colouring \(c\) with \(c(6)=5\) and \(\deg(6)=4\). Neighbours \(0,1,2,5\).
- Shortest path in \(\mathcal{R}(G-6,5)\) of length 2 from \(c|_{G-6}\) to a 4-colouring, equal to the path `bfs_reduce_to_4` returns.
- Step 0 swaps the \((3,5)\)-chain \(\{2,8\}\) while neighbours 2 and 5 lie in the distinct \((3,5)\)-chains \(\{2,8\}\) and \(\{4,5\}\).

That is the status change. A Markdown citation of Agent 1419 is not this object. This object is written down, and the path meets K1 §6.

### Hot air

The Agent 1419 sentence that a safe path of length 3 always exists is hot air on this evidence. `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md` says, for the 24 colourings of `T_9_35` at vertex 6, “All 24 have safe paths at distance 3 (optimal is 2),” and, for every counterexample case, “A safe path of length opt_dist + 1 exists (distance 3 instead of 2).”

JSON index 3 does not show that path. No field stores a path longer than the BFS distance. `"safe_path_exists": false` belongs to a search that stops when the length leaves the BFS distance. W-path §4 records the same limit and marks the claim “Not supported.” W-path did not search past distance 2. This gate did not either. The sentence remains an assertion in the 1419 report.

---

## 3. Gate lines

The degree-4 conjecture in K1 §2 says that every shortest path avoids the adjacent chain. The path above is a shortest path and swaps the adjacent chain. The written path meets the K1 §6 kill criterion.

| Item | Outcome |
|---|---|
| Degree-4 universal BFS-avoidance conjecture | **DEAD END** |
| `t1-witness-935` | **ACCEPT WITNESS** |
| `track1` | **LEAVE** |
| `t1-spec-d4` | **LEAVE** |
| `t1-spec-d5` | **LEAVE** |

`t1-witness-935` asked for the edge set and one shortest path meeting the kill test, or a proof that no such colouring exists. The edge set, the colouring, and the path are written, and the path meets the test.

`track1` stays open. This path reaches a proper 4-colouring of \(H = G-6\) by Kempe swaps. Kempe reducibility to 4 colours is a different statement from “every shortest path avoids merges.” The Four Colour Theorem is not marked dead.

`t1-spec-d4` stays the accepted specification of the sentence that this witness kills. The dead item is the conjecture. `t1-spec-d5` is untouched: this vertex has degree 4.

Feasibility of reading this one path as a kill of the degree-4 universal sentence: **High**. The replay finished in about \(0.1\) seconds.

---

## 4. Follow-up to start now

**Task name:** `W2-longer-safe`. Confirmed. The same evidence leaves this weaker question open, and Agent 1419’s length-3 sentence is not a written path.

One colouring, one search. Use the colouring of JSON index 3, \(c(6)=5\), on \(H = G-6\), with the full colouring \(c\) still available for the safety test. Call `find_safe_nonoptimal_path` in `compute/kempe/counterexample_energy_targeted.py` with `opt_dist = 2`. Write the path the call returns, or write that it returned `None`.

`None` means the call found no safe path at distance \(3\), \(4\), or \(5\). The default `max_extra` is \(3\), so the search stops at `opt_dist + 3`. A returned `None` is the function’s answer inside that bound. It is not a proof that no longer safe path exists, and a returned path is one path on this colouring, not the claim about all 24 colourings.

---

## 5. Degree 5 witness

**DEAD END.** `backgroundMaterial/agent1701/groups/D5_witness.md` matches the edge list of record 0 in `counterexample_details.json` to `generate_triangulations(9)[25]` (`T_9_25`, 21 edges). On the colouring with \(c(3)=5\), the path `bfs_reduce_to_4` returns has length 2, and its first step swaps the \((4,5)\)-chain \(\{4,5\}\), which contains neighbour 4 of vertex 3, while neighbours 4 and 6 lie in the distinct chains \(\{4,5\}\) and \(\{6,8\}\). A replay of `d5_witness_check.py` found the same edge equality and the same step, in 1.1 seconds. This is one colouring. It does not kill `track1` or the Four Colour Theorem.

## Degree 5 classification

**ACCEPT COMPUTATION.** `D5_classify.md` states \(1248\) proper \(5\)-colourings of \(T_{9,25}\) with \(c(3)=5\), of which \(24\) have every shortest path K1-unsafe, and all \(24\) of those have a K1-safe path of length \(\mathrm{opt\_dist}+1\), in \(6.536\) seconds. The same figures are in `d5_classify_results.json`. This is a computation, not a theorem. It does not revive the degree-5 universal conjecture, and it does not touch the Four Colour Theorem or `track1`.

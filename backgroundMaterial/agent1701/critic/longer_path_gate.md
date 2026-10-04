# Critic gate — longer K1-safe paths on the stored colourings of \(T_{9,35}\)

**Critic date:** 27 September 2026
**Inputs opened:** `backgroundMaterial/agent1701/groups/W2_longer.md`, `backgroundMaterial/agent1701/groups/W3_batch.md`, `backgroundMaterial/agent1701/groups/w3_batch_results.json`, `backgroundMaterial/agent1701/groups/w3_batch_search.py`, the W2 decision in `backgroundMaterial/agent1701/coordinator/manager_MWitness/manager_report.md`, `backgroundMaterial/agent1701/critic/witness_gate.md`, and K1 §2 in `backgroundMaterial/agent1701/groups/K1_spec.md`.
**Replay:** the 24 colourings named in W3, in `.venv`, against `bfs_reduce_to_4`, `find_safe_nonoptimal_path`, `classify_path_safety`, and `is_step_unsafe`. The process finished in about \(1.2\) seconds. `docs/navigator/` was not edited.

The degree-4 universal shortest-path conjecture stays **DEAD END**. `witness_gate.md` already killed it. A path of length 3 is longer than the BFS distance 2 recorded for these colourings, so this batch does not reopen that conjecture.

The Four Colour Theorem is unproved. This gate does not mark it dead. Kempe reducibility is not settled.

---

## 1. The batch is a real computation

W3 states the three required numbers. They are the numbers in `w3_batch_results.json`.

| Quantity | W3 §3 | JSON field |
|---|---|---|
| Colourings run | \(24\) | `n_ran` \(= 24\) |
| Returned a path | \(24\) | `n_path` \(= 24\) |
| Elapsed time | \(1.164\) seconds | `elapsed_seconds` \(= 1.16413075\) |

`n_none` is \(0\), `n_no_bfs_path` is \(0\), and `stopped_reason` is null. Every stored result has `opt_dist` \(= 2\), `path_length` \(= 3\), `longer_than_bfs` true, `end_colours` \(= 4\), `proper_on_T` true, and `proper_on_H` true. Every colouring in the file has colour \(5\) at vertex \(6\).

The stored set is the set W3 names. `exhaustive_details` and `ce_details` in `backgroundMaterial/agent1545/coordinator/manager_M1/sub_S1/merge_tolerant_results.json` each contribute 24 entries with `"graph": "T_9_35"` and `"vertex": 6`, and those two sets of colourings are equal. The three records in `backgroundMaterial/agent1520/coordinator/manager_M1/sub_S3/counterexample_details.json` with `"vertex": 6` and `"degree": 4` are included in that set. The JSON results are in `exhaustive_details` order.

The replay called `find_safe_nonoptimal_path` with `max_extra` \(= 3\) on all 24. It returned a path for every colouring, each of length 3, each with `path_is_safe` true. On the evolving colouring of \(G\), `is_step_unsafe` was false at every step. The swap pairs and vertex sets matched the JSON, including the published colouring of W2 — \((1,2)\) on \(\{0,7\}\), \((1,5)\) on \(\{4\}\), \((4,5)\) on \(\{3\}\) — and the next colouring in W3 §4 — \((1,2)\) on \(\{0,7\}\), \((1,5)\) on \(\{4\}\), \((3,5)\) on \(\{3\}\).

K1-safe, in this gate, is the K1 §2 avoidance condition on a single path: whenever a step swaps an \((a,5)\)-Kempe chain \(K\) of the colouring present before that step, and at least two neighbours of vertex \(6\) lie in distinct \((a,5)\)-chains of that colouring, \(K\) contains no neighbour of vertex \(6\). That is the test `classify_path_safety` implements, and it is the test `find_safe_nonoptimal_path` requires before it returns a path. The W2 decision already matched that test to K1 on one colouring. This replay matched it on all 24.

The sentence “for every one of these stored \(T_{9,35}\) vertex-6 colourings, a K1-safe path of length 3 exists” is **ACCEPT** as a checked computation. It is a sentence about this stored set of this one graph.

---

## 2. Gate lines

| Item | Outcome |
|---|---|
| Degree-4 universal shortest-path conjecture | **DEAD END** |
| Stored-colouring length-3 sentence | **ACCEPT** as a checked computation |
| `track1` | **LEAVE** |

`track1` stays open. Each accepted path reaches a proper 4-colouring of \(H = T_{9,35}-6\) by Kempe swaps on one of these 24 colourings. Kempe reducibility of planar triangulations is a different statement.

Feasibility of reading the JSON plus this replay as a check of the stored-colouring sentence: **High**. The replay finished in about \(1.2\) seconds.

---

## 3. Spec it now

The specification must use this statement, and no wider quantifier.

Let \(G = T_{9,35}\) be `generate_triangulations(9)[35]`, let vertex \(v = 6\), and let \(H = G - v\). Let \(S\) be the set of \(24\) colourings stored with `"graph": "T_9_35"` and `"vertex": 6` in `exhaustive_details` of `backgroundMaterial/agent1545/coordinator/manager_M1/sub_S1/merge_tolerant_results.json`. That set equals the set of such colourings in `ce_details` of the same file, and it contains the three records in `backgroundMaterial/agent1520/coordinator/manager_M1/sub_S3/counterexample_details.json` with `"vertex": 6` and `"degree": 4\).

For every \(c \in S\), \(c\) is a proper \(5\)-colouring of \(G\) with \(c(6) = 5\), \(c|_H\) is a proper \(5\)-colouring of \(H\), and there exists a path of length \(3\) in \(\mathcal{R}(H,5)\) from \(c|_H\) to a proper colouring of \(H\) that uses four colours, such that every step is K1-safe: whenever a step swaps an \((a,5)\)-Kempe chain \(K\) of the colouring present before that step and at least two neighbours of vertex \(6\) lie in distinct \((a,5)\)-Kempe chains of that colouring, the chain \(K\) contains no neighbour of vertex \(6\).

To extend the quantifier from \(S\) to every proper \(5\)-colouring of \(T_{9,35}\) with colour \(5\) at vertex \(6\), a proof must show that larger set equals \(S\), or must apply this same test to every colouring outside \(S\). To state the same existence for any planar graph other than \(T_{9,35}\), a separate argument is required.

---

## 4. Hot air

These sentences stay refused on this evidence.

- “All 24 are always salvageable,” offered as a theorem. The checked fact is existence of one K1-safe path of length 3 for each map in \(S\), returned inside `max_extra` \(= 3\). Salvage as an inductive principle is a further claim.
- “The inductive proof survives.”
- The Four Colour Theorem.
- Any reopening of the degree-4 universal shortest-path conjecture. That conjecture remains a dead end.

---

## 5. Specification gate

**ACCEPT SPEC.** `backgroundMaterial/agent1701/groups/K3_weaker_spec.md` §2 uses the stored set \(S\) and the quantifier \(c \in S\), and §6 calls the W3 record a computation rather than a theorem. The one extra clause is the BFS distance \(2\) for each \(c \in S\), which the same run measured and which does not widen the quantifier.

The three counts in `W4_outside.md` — \(1440\) proper \(5\)-colourings of \(T_{9,35}\) with \(c(6)=5\), of which \(24\) lie in \(S\) and \(1416\) lie outside \(S\), in \(1.057\) seconds — are accepted as a computation, not a theorem. The \(1416\) colourings outside \(S\) were not path-searched by W4.

W4 did not search those \(1416\) colourings; W5 claims it then classified all \(1416\) in \(1.431\) seconds, and `w5_classify_results.json` records the same figures: \(8\) have one unsafe shortest path, \(0\) have every shortest path unsafe, and those \(8\) have a K1-safe path of length \(\mathrm{opt\_dist}+1\). **Accept** that count as a computation, not a theorem, and it does not revive the degree-4 universal conjecture.

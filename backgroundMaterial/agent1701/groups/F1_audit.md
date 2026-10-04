# F1 Audit — Navigator links against the repository

**Navigator node:** `audit-1701`
**Manager:** M-Foundation
**Date:** 27 September 2026
**Scope:** Every `files` entry in `docs/navigator/data.js`, plus the Plan 2 claims in `SolvingFrameworkPlan/ExecutiveSummary_Plan2_Status.md`. Statuses below are recommendations. This audit does not edit the navigator.

A path **exists** if `test -f` succeeds, or if it is a directory that contains at least one file. `lean4/KempeReconfiguration/` contains 7 files, so it exists. `lean4/FourColor/` does not exist. The Kempe suite was not run.

## Missing links

There are 27 `files` entries and 25 unique paths. **15 unique linked paths are missing** (16 entries, because `compute/chromatic/root_finder.py` is linked twice).

| Path | Result | Nodes |
|---|---|---|
| `SolvingFrameworkPlan/NovelProofExploration.md` | exists | `4ct` |
| `backgroundMaterial/agent1221/agent1221Report.md` | exists | `4ct` |
| `lean4/FourColor/Foundation/F1_ColoringBasics.lean` | missing | `f1` |
| `lean4/FourColor/Foundation/F2_Planarity.lean` | missing | `f2` |
| `lean4/FourColor/Foundation/F3_EulerFormula.lean` | missing | `f3` |
| `lean4/FourColor/Foundation/F4_KempeChains.lean` | missing | `f4` |
| `lean4/FourColor/Foundation/F5_FiveColorTheorem.lean` | missing | `f5` |
| `backgroundMaterial/agent1701/tasks/F2.md` | exists | `f-spec-lean` |
| `lean4/KempeReconfiguration/` | exists (7 files) | `f-spec-lean` |
| `compute/kempe/reduction_search.py` | exists | `t1-1` |
| `lean4/FourColor/Track1_KempeSwap/` | missing | `t1-4` |
| `backgroundMaterial/agent1701/tasks/K1.md` | exists | `t1-spec-d4` |
| `SolvingFrameworkPlan/ExecutiveSummary_Plan2_Status.md` | exists | `t1-spec-d4`, `t1-spec-d5` |
| `backgroundMaterial/agent1701/tasks/K2.md` | exists | `t1-spec-d5` |
| `lean4/FourColor/Track2_ChromaticPoly/` | missing | `t2-1` |
| `compute/chromatic/root_finder.py` | missing | `t2-2`, `t7-2` |
| `lean4/FourColor/Track3_Flows/` | missing | `t3-1` |
| `compute/topology/penrose_eval.py` | exists | `t4-1` |
| `compute/spectral/colin_de_verdiere.py` | missing | `t5-1` |
| `lean4/FourColor/Track5_Spectral/` | missing | `t5-2` |
| `compute/topology/sheaf_cohomology.py` | missing | `t6-1` |
| `lean4/FourColor/Track6_Sheaf/` | missing | `t6-2` |
| `compute/discovery/tensor_network.py` | missing | `t7-1` |
| `compute/discovery/gnn_coloring.py` | missing | `t7-3` |
| `backgroundMaterial/agent1701/tasks/F1.md` | exists | `audit-1701` |

Nodes with `files: []` have evidence **none**. An empty list is not a missing path.

`compute/kempe/tests/test_plan2.py` exists and is not a navigator link. It declares **31** tests (`def test_`). That matches the summary’s count of 31 tests. This audit did not run them, so “all passing” is not confirmed.

`rg` finds the word `sorry` only in comments under `lean4/KempeReconfiguration/`. There is no tactic `sorry`. `Main.lean` does not state the constructive theorem; it says the gap is left as a comment. `Degree3NoMerge.lean` axiomatizes `Triangulation.link_degree3_complete` instead of proving planarity.

## Plan 2 claims

The six named lemmas in the executive summary all have a file that holds an argument. None of those six is summary-only. The degree-3 no-merge claim is lemma 6, not a seventh result. Conjecture 5.5 is stated outside the summary, and it is not a proof.

| Claim | Where the argument or test lives | Summary-only? |
|---|---|---|
| Theorem A (Non-Interleaving) | Argument: `backgroundMaterial/agent0050/coordinator/manager_M2/sub_S1/theorem_A_proof.md`. Test: `test_disjoint_chains_noncrossing` in `compute/kempe/tests/test_plan2.py`, calling `compute/kempe/noncrossing_verifier.py`. | No |
| Theorem B (Confinement) | Argument: `backgroundMaterial/agent0050/coordinator/manager_M2/sub_S1/theorem_B_proof.md`. No matching test in `test_plan2.py`. | No |
| Never-Revert Lemma | Prose: `backgroundMaterial/agent0051/deliverables/revised_paper_section.md`, Lemma 3.1. Formal proof: `lean4/KempeReconfiguration/KempeReconfiguration/NeverRevert.lean` (`never_revert`). No dedicated test in `test_plan2.py`. | No |
| Chain Lifting for $\{1,2,3,4\}$ | Prose: same paper, Lemma 5.1 (one paragraph: $v \notin B_{a,b}$). Lean: `ChainLifting.lean` proves isolation in the bichromatic subgraph (`colour5_isolated_in_bichromatic_14`) and says component equality is not formalized. | No |
| Degree-5 Classification | Case analysis: `backgroundMaterial/agent0050/coordinator/manager_M2/sub_S2/degree5_classification.md` (8 types, all marked resolved). The paper’s Proposition 4.1 is a sketch of that note. | No |
| Degree-3 No-Merge | Proof: `backgroundMaterial/agent0051/coordinator/manager_M1/sub_S1/S1_report.md` and paper Lemma 5.2. Lean: `degree3_no_merge`, depending on the triangulation axiom above. Test: `test_merge_conditions_degree3`. | No |
| Conjecture 5.5 (BFS Avoidance) | Statement: the executive summary and paper §5.4. Finite check for $n \le 8$: `test_bfs_path_zero_merges_n8`. Not a proof. `compute/kempe/counterexample_analysis.py` later names $n=9$ counterexamples `T_9_25` (degree 5) and `T_9_35` (degree 4). This audit did not re-run that module. | No |

## Status table

Hot air means a summary claims a proof or a computation that cannot be pointed at a file. Partial lemmas with files are not hot air. The track-level “near-complete constructive proof” is.

| Node id | Current | Recommended | Evidence | Hot air |
|---|---|---|---|---|
| `4ct` | exploring | exploring | `SolvingFrameworkPlan/NovelProofExploration.md` | no |
| `foundation` | unstarted | unstarted | none | no |
| `f1` | unstarted | unstarted | none | no |
| `f2` | unstarted | unstarted | none | no |
| `f3` | unstarted | unstarted | none | no |
| `f4` | unstarted | unstarted | none | no |
| `f5` | unstarted | unstarted | none | no |
| `f-spec-lean` | exploring | exploring | `backgroundMaterial/agent1701/tasks/F2.md` | no |
| `track1` | unstarted | in-progress | `compute/kempe/tests/test_plan2.py` | yes |
| `t1-1` | unstarted | in-progress | `compute/kempe/reduction_search.py` | no |
| `t1-2` | unstarted | unstarted | none | no |
| `t1-3` | unstarted | unstarted | none | no |
| `t1-4` | unstarted | unstarted | none | no |
| `t1-spec-d4` | exploring | exploring | `backgroundMaterial/agent1701/tasks/K1.md` | no |
| `t1-spec-d5` | exploring | exploring | `backgroundMaterial/agent1701/tasks/K2.md` | no |
| `track2` | unstarted | unstarted | none | no |
| `t2-1` | unstarted | unstarted | none | no |
| `t2-2` | unstarted | unstarted | none | no |
| `t2-3` | unstarted | unstarted | none | no |
| `t2-4` | unstarted | unstarted | none | no |
| `track3` | unstarted | unstarted | none | no |
| `t3-1` | unstarted | unstarted | none | no |
| `t3-2` | unstarted | unstarted | none | no |
| `t3-3` | unstarted | unstarted | none | no |
| `track4` | unstarted | exploring | `compute/topology/penrose_eval.py` (child `t4-1` only) | no |
| `t4-1` | unstarted | in-progress | `compute/topology/penrose_eval.py` | no |
| `t4-2` | unstarted | unstarted | none | no |
| `t4-3` | unstarted | unstarted | none | no |
| `t4-4` | unstarted | unstarted | none | no |
| `track5` | unstarted | unstarted | none | no |
| `t5-1` | unstarted | unstarted | none | no |
| `t5-2` | unstarted | unstarted | none | no |
| `track6` | unstarted | unstarted | none | no |
| `t6-1` | unstarted | unstarted | none | no |
| `t6-2` | unstarted | unstarted | none | no |
| `track7` | unstarted | unstarted | none | no |
| `t7-1` | unstarted | unstarted | none | no |
| `t7-2` | unstarted | unstarted | none | no |
| `t7-3` | unstarted | unstarted | none | no |
| `t7-4` | unstarted | unstarted | none | no |
| `audit-1701` | exploring | exploring | `backgroundMaterial/agent1701/tasks/F1.md` | no |

`t1-1` stays short of proved: the linked search code exists, and `test_plan2.py` checks distance bounds through $n=10$ (`test_distance_bound_n10`). The node asks for every triangulation with $n \le 12$. `t1-4` stays unstarted because `lean4/FourColor/Track1_KempeSwap/` is missing. The Kempe Lean library is a different directory, linked from `f-spec-lean`, and it does not prove Kempe reducibility to 4 colours.

`track1` is in-progress because those tests and the six lemma files are real, and the track statement is still open. It is not killed: the later counterexample module attacks BFS avoidance, which is not the kill criterion “some 5-colouring cannot be Kempe-reduced to 4.”

Tracks 2, 3, 5, 6, and 7 stay unstarted. Their linked Python and Lean paths are missing. `track4` is the exception: `penrose_eval.py` is a real module (Tait colourings and the Penrose evaluation), so the track is exploring and `t4-1` is in-progress. That file is not a proof that the Penrose evaluation is positive for every bridgeless planar cubic graph. No track 2–7 node is killed.

## Hot air

The hottest hot-air item is the executive summary’s status line: **“Near-complete constructive proof.”** No file contains that proof. The paper’s §6.2 marks degree 4 and 5 as a gap, and `Main.lean` never states the theorem.

The same summary’s “six lemmas, all … computationally verified” overreaches Theorem B. The confinement argument is in `theorem_B_proof.md`. There is no test for it in `test_plan2.py`.

The census of about $2.3 \times 10^6$ colourings and zero failures is prose in the summary and in agent reports. The reproducing procedures are the tests in `test_plan2.py`. They were not executed here. The summary’s “0 counterexamples” for Conjecture 5.5 is the $n \le 8$ test, not a universal computation, and `counterexample_analysis.py` asserts $n=9$ counterexamples.

## Feasibility

Feasibility of trusting the executive summary as a status source: **Low**.

It is a usable map of where the six lemma arguments were written on 18 February 2026, and it does mark Conjecture 5.5 as open. It is a poor live status: the banner claims a near-complete proof, the zero-counterexample sentence stops at the $n \le 8$ regime, a later file asserts $n=9$ counterexamples to that conjecture, and the headline census was not re-checked in this audit.

## Concrete next steps

1. Critic gate: set `foundation` and `f5` to unstarted, `track1` to in-progress, `t1-1` to in-progress, tracks 2, 3, 5, 6, and 7 to unstarted, and `track4` to exploring. Do not mark any of these proved.
2. Keep Conjecture 5.5 off the proved list. Before any status above in-progress on BFS avoidance, read `compute/kempe/counterexample_analysis.py` against `test_bfs_path_zero_merges_n8` and record whether the $n=9$ names are counterexamples to the conjecture or only to a stricter reading.
3. Leave `t1-4` unstarted until `lean4/FourColor/Track1_KempeSwap/` exists, or retarget the node at `lean4/KempeReconfiguration/` in a later navigator edit. This audit does not edit `data.js`.
4. Treat `lean4/FourColor/Foundation/` as absent. Do not describe Never-Revert or Chain Lifting as the Five Colour Theorem.
5. A later session may run `compute/kempe/tests/test_plan2.py`. Until that run is logged, do not copy “31/31 passing” or the $n \le 10$ census into the navigator as evidence.

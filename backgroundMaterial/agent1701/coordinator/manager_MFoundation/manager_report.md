# M-Foundation — combined status of F1 and F2

**Manager:** M-Foundation
**Date:** 27 September 2026
**Inputs:** `backgroundMaterial/agent1701/groups/F1_audit.md`, `backgroundMaterial/agent1701/groups/F2_spec.md`
**Navigator:** not edited. No Lean file edited. No proof written.

## Decision

**ACCEPT SPEC**

F1 has every part required by `tasks/F1.md`: an exists/missing call for every `files` entry (27 entries, 25 unique paths), a file for each of the six Plan 2 lemmas, the degree-3 no-merge claim, and Conjecture 5.5, a count of 31 declared tests in `compute/kempe/tests/test_plan2.py` without running the suite, track 2–7 recommendations that stay `unstarted` where the linked path is missing and never `killed`, the status table with evidence and a hot-air flag, next steps, and feasibility **Low** for trusting the executive summary as a status source.

F2 has every part required by `tasks/F2.md`: a mathematical claim, Lean name or the statement that none exists, file, and `sorry` verdict for each of the three obligations; a tactic-`sorry` count of $0$ with comment lines listed; which of the three are closed in Lean; Five Colour Theorem answered **no**, with the paths searched; an acceptance test; a boundary titled “Not proved”; and feasibility **High** for formalizing the three statements before an attempt on the Four Colour Theorem. Definitions, cited evidence, and a kill criterion are present.

## Spot-checks (this manager)

1. `lean4/KempeReconfiguration/KempeReconfiguration/Basic.lean` contains `theorem kempeSwap_preserves_proper` (the closed-set form: a proper colouring stays proper after swapping colours $a \leftrightarrow b$ on a decidable set of $\{a,b\}$-coloured vertices closed under adjacency into $\{a,b\}$). The word `sorry` occurs once, in the header comment “Target: 0 sorry”. The proof is a tactic script. There is no `sorry` tactic. Lines 147, 152, and 153 are bare `Ne.symm` terms; that is the compilation risk F2 records, not an open proof.
2. `lean4/FourColor/Foundation/F5_FiveColorTheorem.lean`, which F1 lists as missing for node `f5`, is not in the repository. Read of that path fails. F1’s missing call for this link stands.

## Status recommendations

Endorse F1’s table. No node is `proved`. A lemma file, a Python test, or an isolation lemma does not earn `proved`.

| Node | Status |
|---|---|
| `4ct` | exploring |
| `foundation` | unstarted |
| `f1` | unstarted |
| `f2` | unstarted |
| `f3` | unstarted |
| `f4` | unstarted |
| `f5` | unstarted |
| `f-spec-lean` | exploring |
| `track1` | in-progress |
| `t1-1` | in-progress |
| `t1-2` | unstarted |
| `t1-3` | unstarted |
| `t1-4` | unstarted |
| `t1-spec-d4` | exploring |
| `t1-spec-d5` | exploring |
| `track2` | unstarted |
| `t2-1` | unstarted |
| `t2-2` | unstarted |
| `t2-3` | unstarted |
| `t2-4` | unstarted |
| `track3` | unstarted |
| `t3-1` | unstarted |
| `t3-2` | unstarted |
| `t3-3` | unstarted |
| `track4` | exploring |
| `t4-1` | in-progress |
| `t4-2` | unstarted |
| `t4-3` | unstarted |
| `t4-4` | unstarted |
| `track5` | unstarted |
| `t5-1` | unstarted |
| `t5-2` | unstarted |
| `track6` | unstarted |
| `t6-1` | unstarted |
| `t6-2` | unstarted |
| `track7` | unstarted |
| `t7-1` | unstarted |
| `t7-2` | unstarted |
| `t7-3` | unstarted |
| `t7-4` | unstarted |
| `audit-1701` | exploring |

`track1` is in-progress because `compute/kempe/tests/test_plan2.py` and the six lemma argument files exist, and the track statement is still open. The hot-air flag on that node stays yes: the executive summary’s “near-complete constructive proof” has no file. `t1-1` is in-progress because `compute/kempe/reduction_search.py` exists and the logged test reaches $n = 10$, while the node asks for every triangulation with $n \le 12$. `foundation` and `f5` stay unstarted: their linked Lean paths are missing, and the Kempe library is not the Five Colour Theorem. `track4` is exploring because `compute/topology/penrose_eval.py` exists for child `t4-1`; that module is not a proof that the Penrose evaluation is positive for every bridgeless planar cubic graph. Tracks 2, 3, 5, 6, and 7 stay unstarted. `t1-4` stays unstarted because `lean4/FourColor/Track1_KempeSwap/` is missing.

## Lean Tier-1

| Obligation | Closed in Lean? |
|---|---|
| Kempe swap preserves a proper colouring | Yes. `kempeSwap_preserves_proper` in `Basic.lean`. Proof present. No `sorry` tactic. Spot-checked above. `lake build` was not run. |
| Never-Revert | Yes. `never_revert`, with `never_revert_pointwise` and `never_revert_card`, in `NeverRevert.lean`. F2 records proofs and no `sorry` tactic. The paper case is the target colour $5$, Lean index `(4 : Fin 5)`, with both swapped colours different from it. |
| Chain Lifting for colours in $\{1,2,3,4\}$ | No. `ChainLifting.lean` has `colour5_isolated_in_bichromatic_14` and `vertex_not_in_bichromatic`. Those are isolation lemmas. There is no theorem equating the $(a,b)$-Kempe chain of $u$ in $G$ with its chain in $G - v$. F1’s note that an argument file exists for Chain Lifting is not a Lean proof of that equality. |

Tactic `sorry` under `lean4/KempeReconfiguration/`: $0$, as counted by F2. Comment occurrences of the word are not open proofs and are not finished proofs.

## Hot air to refuse

- The executive summary line “Near-complete constructive proof.” No file contains that proof. `Main.lean` states no theorem.
- “Six lemmas, all computationally verified,” applied to Theorem B. The confinement argument is `backgroundMaterial/agent0050/coordinator/manager_M2/sub_S1/theorem_B_proof.md`. `test_plan2.py` has no test for it.
- The census of about $2.3 \times 10^6$ colourings and zero failures, and “31/31 passing,” until a run of `test_plan2.py` is logged. This audit did not run the suite.
- “0 counterexamples” for Conjecture 5.5 as a universal computation. The file behind that sentence is the $n \le 8$ test `test_bfs_path_zero_merges_n8`. `compute/kempe/counterexample_analysis.py` names $n = 9$ examples; this audit did not re-run that module.
- Any promotion of `colour5_isolated_in_bichromatic_14`, `vertex_not_in_bichromatic`, or `bichromatic_adj_delete_irrelevant` to Lemma 5.1. The third theorem’s statement does not mention `deleteVerts`.
- A Markdown summary that only cites a summary, including the Five Colour sketch in `SolvingFrameworkPlan/SolvingProofStrategy.md` and `NovelProofExploration.md`. Those stay under “Not proved.”
- A comment in `Main.lean`, or a grep hit on `sorry` inside a comment, offered as a theorem or as an open `sorry`.

## What is not proved

- The Chain Lifting equality of $(a,b)$-components in $G$ and in $G - v$ for $c(v) = 5$ and $a, b \in \{1,2,3,4\}$.
- Any reading of `bichromatic_adj_delete_irrelevant` as a theorem about vertex deletion.
- The Five Colour Theorem in this repository. There is no Lean proof. `foundation` and `f5` are unstarted.
- Planarity of the `Triangulation.link_degree3_complete` assumption used by `degree3_no_merge`.
- Every $4$-colouring statement: `Main.lean` declares none, including an $n - 4$ Kempe-swap bound and BFS Avoidance (Conjecture 5.5).
- Kempe reducibility of every $5$-colouring on $n \le 12$ triangulations (`t1-1`), and the Kempe-swap formalization at `t1-4`.
- Positivity of the Penrose evaluation for every bridgeless planar cubic graph (`track4` / `t4-1`).
- No navigator node above is proved.

## Next steps

1. Critic gate: apply the status list above. Do not mark any node `proved`.
2. Keep Conjecture 5.5 off the proved list until `counterexample_analysis.py` is read against `test_bfs_path_zero_merges_n8`.
3. Leave Chain Lifting open in Lean until a theorem states the component equality. Do not discharge it with `sorry`, and do not cite the isolation lemmas as that theorem.
4. Leave `f5` unstarted. Do not describe Never-Revert or Chain Lifting as the Five Colour Theorem.

Feasibility of trusting `SolvingFrameworkPlan/ExecutiveSummary_Plan2_Status.md` as a live status source: **Low**.

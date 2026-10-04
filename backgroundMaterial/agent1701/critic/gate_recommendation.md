# Critic gate — Agent 1701, wave 1

**Critic date:** 27 September 2026
**Inputs opened:** M-Kempe `manager_report.md`, M-Foundation `manager_report.md`, `task_decomposition.md`, K1 and K2 specifications (statements, kill criteria, sequencing), F2’s Chain Lifting section, `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md`, `lean4/KempeReconfiguration/KempeReconfiguration/ChainLifting.lean`, `Basic.lean` (`kempeSwap_preserves_proper`), `NeverRevert.lean` (three theorems).
**Also checked for presence:** `lean4/FourColor/Foundation/F5_FiveColorTheorem.lean` (absent), `compute/kempe/reduction_search.py` (present), `compute/kempe/tests/test_plan2.py` (present), `compute/topology/penrose_eval.py` (present).
**Not done:** no navigator edit, no proof, no `lake build`, no re-run of any search. Counts in prior reports that were not opened here stay citations.

The Four Colour Theorem is unproved. Nothing in this wave is a proof of it.

---

## 1. M-Kempe

### Solid

The combined sentences are a real specification. K1’s displayed conjecture quantifies over every shortest path in $\mathcal{R}(G-v,5)$ and applies the bridge test at the colouring before the swap. K2’s displayed sentence does not: it puts the bridge on $G-v$ once, then says “any BFS-optimal path … does not swap any chain adjacent to $v$.” K2’s acceptance test then requires every shortest path and a per-colour `would_merge` test. Adopting K1’s quantifier for both degrees removes that wobble. Degree, chain, and shortest path stay separate objects, and the single path from `bfs_reduce_to_4` is not the conjecture. That repair is in the manager report and matches the two specification files.

The strategy revision is not hot air. `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md` was opened. It asserts a degree-$4$ BFS-avoidance failure on the triangulation it labels `T_9_35`, at vertex $6$. The degree-$4$ row and the vertex bullet say:

> | 4 | 65,175 | 6,925 | 10.6% | 317 |

> T_9_35 (v=3 deg 5, v=6 deg 4): 38 merges **← TRUE COUNTEREXAMPLE**

> ### T_9_35 (degree sequence: [3,4,4,4,4,5,5,6,7]):
> - **Counterexample vertex v=6 (deg 4):** 32 merges, 24 colourings where ALL optimal paths are unsafe

The impact line says: “Conjecture 5.5 (BFS optimal avoidance) is FALSE as stated.” Withdrawing “prove degree $4$ first” (K2 §5) until that assertion is written as a graph and a path is a response to sentences that are in the file. K1 already tells the same pause: confirm one colouring and one shortest path before a proof attempt, and do not mark the node killed. The manager does not choose among K1’s three weaker salvage sentences, and does not treat Observation R as established. Both refusals match the files.

### Still soft

“The conjecture is not intact” is one sentence past the evidence. The same report gives no edge set of $T_{9,35}$, no colouring, and no path. The manager later says the $n=9$ hits are unproved and the conjecture is unmarked as killed. Those later sentences are the status. The opened file also says the failure is “of BFS optimality, not of safe path existence,” and that all $24$ colourings have a safe path at distance $3$ when the optimum is $2$. That salvage is another assertion in the same file. It is not a theorem, and it is not a reason to replace Conjecture 5.5 with a longer-path conjecture in this gate.

The list the manager asks the critic to treat as real includes Lemma 5.1, the degree-$3$ no-merge argument, Theorem A, the $17.4\%$ / $30.9\%$ table, and the $1{,}104$ / $13{,}876$ program scope. Those files were not opened for this gate. They remain citations. They do not become checked mathematics because the manager graded them.

Feasibility **Low** for a proof of either universal sentence is the right planning label while an opened report asserts that every shortest path hits and nobody has written the path. That rating is not a disproof.

---

## 2. M-Foundation

### Solid

The Chain Lifting call is accurate. The manager did not overclaim.

`ChainLifting.lean` opens by stating the equality that is not proved:

> Statement: If c(v) = 5 and a, b ∈ {1,2,3,4}, then the (a,b)-Kempe chains are identical in G and G-v:
> KempeChain(G, c, u, a, b) = KempeChain(G-v, c|_{G-v}, u, a, b)

The theorems in the file are `vertex_not_in_bichromatic`, `bichromatic_adj_delete_irrelevant`, and `colour5_isolated_in_bichromatic_14`. The first and third show that $v$ has no bichromatic edge when its colour lies outside $\{a,b\}$ (the third specialises to paper colour $5$ as `(4 : Fin 5)`). The second is proved by `rfl`. Its statement equates `bichromaticAdj G c a b u w` with the expanded adjacency condition on $G$. It does not mention `deleteVerts`. The hypotheses $c(v) \notin \{a,b\}$ and $u,w \neq v$ are unused. The file’s own closing comment says the component equality is still missing:

> A full formalization of "connected components are identical" would require building the graph homomorphism between B_{a,b}(G,c) restricted to V\{v} and B_{a,b}(G-v, c|_{G-v}). The isolation lemma above is the key step.

F2 says the same: Lean name of the equality, none; closed in Lean, no. Absence of a `sorry` tactic is not that equality.

`kempeSwap_preserves_proper` in `Basic.lean` is a tactic proof of the closed-set form (proper colouring in, proper colouring out, for a decidable $\{a,b\}$-set closed under adjacency into $\{a,b\}$). No `sorry` tactic appears in that proof. Lines 147, 152, and 153 are bare `Ne.symm` terms. That is the compilation risk F2 records. `never_revert_pointwise`, `never_revert`, and `never_revert_card` in `NeverRevert.lean` are proofs that a swap of colours $a$ and $b$ preserves a target colour outside $\{a,b\}$, including the set and cardinality forms. No `sorry` tactic is in those three proofs. `lake build` was not run in this wave, and the manager says it was not run either. “Proof script present” is what was checked. “Compiles” was not.

`lean4/FourColor/Foundation/F5_FiveColorTheorem.lean` is not in the repository. Leaving `foundation` and `f5` unstarted is correct. The Kempe library is not the Five Colour Theorem. Refusing to cite the isolation lemmas as Lemma 5.1 is correct.

### Still soft

“Closed in Lean: yes” for the swap and for Never-Revert is ahead of a build, given the bare terms in `Basic.lean` and the explicit note that `lake build` was not run. The gate can accept the specification of those obligations. It cannot record them as compiled theorems.

The status table asks for `track1` and `t1-1` to become in-progress, and `track4` to become exploring, because `test_plan2.py`, `reduction_search.py`, and `penrose_eval.py` exist. Those three paths are present. Presence of a module is not the statement on the node. `t1-1` asks for every triangulation with $n \le 12$. `track1` asks for Kempe reduction of every proper $5$-colouring of every planar graph. `track4` asks for a positive Penrose evaluation on every bridgeless planar cubic graph. This gate did not read those programs and did not run the suite. F1’s count of $31$ declared tests was not recounted here. Promoting those nodes is the soft part of an otherwise careful audit.

The hot-air refusals that were checked are the Chain Lifting promotion and the Five Colour Theorem. The executive-summary line “Near-complete constructive proof,” the census of about $2.3 \times 10^6$ colourings, and “31/31 passing” were not re-read against the summary. The manager’s refusal to treat them as status is the right posture. It is not, by itself, a second audit of those sentences.

---

## 3. Real progress versus hot air

### Real

- K1 and K2 state degree-$4$ and degree-$5$ BFS Avoidance with definitions, an acceptance test, a kill criterion, and a “not proved” boundary. The manager’s combined sentences use every shortest path and the pre-swap bridge test for both degrees.
- The Agent 1419 M1-S1 report asserts the degree-$4$ failure at `T_9_35`, vertex $6$, including $317$ BFS-used-unsafe swaps in the degree-$4$ row and $24$ colourings on which every optimal path is unsafe, and it calls Conjecture 5.5 false as stated. The file was opened. The witness was not.
- `ChainLifting.lean` proves isolation of a vertex outside the bichromatic pair. It does not prove chain equality between $G$ and $G-v$. The foundation manager said so.
- `kempeSwap_preserves_proper` and the three Never-Revert theorems are written proof scripts with no `sorry` tactic. They were not compiled here.
- The Five Colour Theorem file linked from `f5` is absent.

### Hot air

- Conjecture 5.5 as an intact gap one should start proving, and “prove degree $4$ before degree $5$” while the `T_9_35` assertion is only a report.
- Conjecture 5.5 as a completed kill. No edge set, colouring, or path is in the asserting file. This wave did not re-run the search.
- The salvage sentence in that same file (a safe path of length $3$ when the optimum is $2$) as a theorem.
- Chain Lifting, Never-Revert, or the swap lemma as the Five Colour Theorem, or as the Four Colour Theorem.
- `colour5_isolated_in_bichromatic_14`, `vertex_not_in_bichromatic`, or `bichromatic_adj_delete_irrelevant` as the chain-equality lemma. The third statement does not mention vertex deletion.
- “Closed in Lean” without a build, and a Python file as in-progress work on `track1`, `t1-1`, or `track4`.
- Observation R, and any claim that degree-$5$ avoidance is equivalent to $4$-colourability of an arbitrary triangulation.
- The Four Colour Theorem as nearly proved.

---

## 4. Gate recommendations

Outcomes are only ACCEPT SPEC, LEAVE, or DEAD END. DEAD END is not used. The `T_9_35` counterexample was not re-verified.

| Node | Outcome | What the main team may record |
|---|---|---|
| `t1-spec-d4` | **ACCEPT SPEC** | Status `in-progress`. Evidence: the degree-$4$ specification was accepted (universal quantifier over shortest paths, bridge test at the pre-swap colouring). The mathematical statement is not proved. |
| `t1-spec-d5` | **ACCEPT SPEC** | Status `in-progress`. Evidence: the degree-$5$ specification was accepted, including Observation R as an unproved reformulation trigger. The mathematical statement is not proved. |
| `f-spec-lean` | **ACCEPT SPEC** | Status `in-progress`. Evidence: the Lean Tier-1 specification was accepted. Swap and Never-Revert have proof scripts and were not compiled. Chain Lifting equality is not a theorem. The mathematical statements are not proved. |
| `audit-1701` | **ACCEPT SPEC** | Status `in-progress`. Evidence: the audit was accepted as a file-presence record and a not-proved boundary. Its proposed promotions of `track1`, `t1-1`, and `track4` are not applied. No mathematical statement is proved. |
| `track1` | **LEAVE** | Stay `unstarted`. |
| `t1-1` | **LEAVE** | Stay `unstarted`. |
| `foundation` | **LEAVE** | Stay `unstarted`. |
| `f5` | **LEAVE** | Stay `unstarted`. |
| `track4` | **LEAVE** | Stay `unstarted`. |
| `track2` | **LEAVE** | Stay `unstarted`. |
| `track3` | **LEAVE** | Stay `unstarted`. |
| `track5` | **LEAVE** | Stay `unstarted`. |
| `track6` | **LEAVE** | Stay `unstarted`. |
| `track7` | **LEAVE** | Stay `unstarted`. |

Feasibility of treating either BFS Avoidance sentence as proved, or the Four Colour Theorem as close: **Low**. Feasibility of extracting one written witness for the already named `T_9_35` claim, once the triangulation is identified: **Medium**. The report that was opened does not contain the edge set, so the identification is part of the task, not a formality already done.

---

## 5. Next task

Identify the triangulation labelled `T_9_35` in `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md` (degree sequence $[3,4,4,4,4,5,5,6,7]$ as written there) and write its edge set. For vertex $v = 6$, claimed there to have degree $4$, either exhibit one proper $5$-colouring of $G-v$ and one shortest path in $\mathcal{R}(G-v,5)$ that meets K1’s kill criterion — some $(a,5)$-step swaps a chain containing a neighbour of $v$ while at least two neighbours lie in distinct $(a,5)$-chains of the pre-swap colouring — or exhibit that no such colouring exists. Do not open a degree-$4$ or degree-$5$ proof. Do not mark Conjecture 5.5 killed unless that witness is written down. Do not adopt the length-$3$ salvage, or Observation R, as the statement under test.

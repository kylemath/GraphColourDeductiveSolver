# F2 — Lean Tier-1 obligations (specification)

**Navigator node:** `f-spec-lean`
**Manager:** M-Foundation
**Group:** F2
**Date:** 27 September 2026
**Status:** specification only. No new proofs. No `sorry` added. No Lean files edited.

This document states the three Tier-1 obligations the existing Kempe development can already talk about, records what Lean actually contains, and gives a check a later formalization can be held to. It does not prove them again.

Colour convention used below. Paper colours are $\{1,2,3,4,5\}$. The Lean files use `Fin 5 = {0,1,2,3,4}`. The header of `ChainLifting.lean` identifies paper colour $5$ with `(4 : Fin 5)` and paper colours $\{1,2,3,4\}$ with Lean indices $\{0,1,2,3\}$. Every statement below is given in paper colours, then matched to the Lean encoding.

---

## 1. Definitions

Let $V$ be a finite type with decidable equality, and let $G$ be a simple graph on $V$ (`SimpleGraph V` with decidable adjacency).

**Proper colouring.** For $k \in \mathbb{N}$ and $c : V \to \mathrm{Fin}\, k$,

$$
\mathrm{IsProperColouring}(G, c) :\iff \forall u\, v,\; G\text{ adjacent } u\, v \Rightarrow c(u) \neq c(v).
$$

Lean name: `IsProperColouring`. File: `lean4/KempeReconfiguration/KempeReconfiguration/Basic.lean`.

**Bichromatic subgraph.** For colours $a, b \in \mathrm{Fin}\, k$, the relation $B_{a,b}(G,c)$ has an edge between $u$ and $v$ when $G$ has that edge and both colours lie in $\{a, b\}$. Lean names: `bichromaticAdj`, `bichromaticSubgraph`.

**Kempe chain.** Vertices $u$ and $v$ lie in the same $(a,b)$-Kempe chain when they are in the same connected component of $B_{a,b}(G,c)$, written `inSameKempeChain G c a b u v`, defined as `(bichromaticSubgraph G c a b).Reachable u v`. There is no definition named `KempeChain` returning the component as a set. The component of a vertex is the set of vertices reachable from it in $B_{a,b}$.

**Kempe swap.** For a decidable set $S \subseteq V$,

$$
(\mathrm{kempeSwap}\, c\, S\, a\, b)(v) =
\begin{cases}
b & \text{if } v \in S \text{ and } c(v) = a, \\
a & \text{if } v \in S \text{ and } c(v) = b, \\
c(v) & \text{otherwise.}
\end{cases}
$$

Lean name: `kempeSwap`. The swap is stated for an arbitrary decidable set, not only for a connected component. A component is a legal swap set once it satisfies the closure hypotheses in §2.1.

**Colour-$5$ set.** In paper notation, $V_5(c) = \{v \in V \mid c(v) = 5\}$. In the Lean encoding this is $\{v \mid c(v) = (4 : \mathrm{Fin}\, 5)\}$.

**Vertex deletion.** $G - v$ means $G$ with vertex $v$ removed. Mathlib’s name for this is `G.deleteVerts {v}`. No theorem in the tree states a fact about `deleteVerts`.

---

## 2. The three obligations

### 2.1 Kempe swap preserves a proper colouring

**Claim.** Let $c$ be a proper $k$-colouring of $G$, let $a \neq b$, and let $S \subseteq V$ be decidable. Suppose

1. every vertex of $S$ is coloured $a$ or $b$, and
2. $S$ is closed under adjacency into $\{a, b\}$: if $u \in S$, $uv$ is an edge, and $c(v) \in \{a, b\}$, then $v \in S$.

Then $\mathrm{kempeSwap}(c, S, a, b)$ is a proper $k$-colouring of $G$.

An $(a,b)$-Kempe chain satisfies both hypotheses: its vertices are coloured $a$ or $b$ by construction of $B_{a,b}$, and a connected component is closed under $B_{a,b}$-edges. The Lean theorem is the closed-set form, which is the form a chain instantiates.

**Lean name:** `kempeSwap_preserves_proper`

**File:** `lean4/KempeReconfiguration/KempeReconfiguration/Basic.lean` (theorem at lines 105–156)

**`sorry`:** no. The only occurrence of the word in this file is the header comment “Target: 0 sorry” (line 12). The theorem has a tactic proof. Supporting lemmas in the same file, also without `sorry`, are `kempeSwap_colour_cases`, `kempeSwap_preserves_other`, and `kempeSwap_outside`.

**Closed in Lean:** yes, as a written proof with no `sorry`. This task did not run `lake build`. A static audit (Agent 1610, `backgroundMaterial/agent1610/auditor_3_lean4_compile/lean4_audit.md`) reports that lines 147, 152, and 153 are bare terms (`Ne.symm ...`) where tactic mode expects `exact`. That is a compilation risk, not an open `sorry`. The mathematical statement is the one in the theorem signature, not the audit.

**Elsewhere.** Python implements the operation as `kempe_swap` in `compute/kempe/kempe_ops.py` and checks it on all $5$-colourings of $K_4$ in `test_kempe_swap_preserves_colouring` (`compute/kempe/tests/test_plan2.py`). That test is finite and is not a proof of the general claim. The same claim is stated in prose in `backgroundMaterial/agent0051/deliverables/lean4_formalization_plan.md` §1.1 and in `backgroundMaterial/agent1210/coordinator/manager_M4/manager_M4_brief.md`.

### 2.2 Never-Revert

**Claim (Lemma 3.1).** Let $c : V \to \{1,2,3,4,5\}$, let $S \subseteq V$, and let $a, b \in \{1,2,3,4\}$. Write $c' = \mathrm{kempeSwap}(c, S, a, b)$. Then

$$
V_5(c') = V_5(c).
$$

Equivalently, for every vertex $v$, $c'(v) = 5$ if and only if $c(v) = 5$. The same equivalence holds for any target colour outside $\{a, b\}$, and the two sets have the same cardinality.

The swap changes a colour only between $a$ and $b$. Since $5 \notin \{a, b\}$, no vertex enters or leaves colour $5$. Properness of $c$ and the requirement that $S$ be a Kempe chain are not used. The Lean theorems are this more general fact. The paper lemma is the special case where the target is paper colour $5$, i.e. Lean index $4$, and $a, b \neq 4$.

**Lean names:**

| Name | What it states |
|---|---|
| `never_revert_pointwise` | $\mathrm{kempeSwap}(c,S,a,b)(v) = t \iff c(v) = t$ whenever $t \neq a$ and $t \neq b$ |
| `never_revert` | the two sets $\{v \mid c'(v) = t\}$ and $\{v \mid c(v) = t\}$ are equal |
| `never_revert_card` | those sets, filtered from `Finset.univ`, have equal cardinality |

**File:** `lean4/KempeReconfiguration/KempeReconfiguration/NeverRevert.lean`

**`sorry`:** no. The only occurrence of the word is the header comment “Target: 0 sorry” (line 14). All three theorems have proofs.

**Closed in Lean:** yes. The set form `never_revert` is the statement to check against Lemma 3.1. Instantiate `five` at `(4 : Fin 5)` and take $a, b \neq 4$.

**Elsewhere.** There is no Python function or test named Never-Revert. The property is the definition of `kempe_swap` in `compute/kempe/kempe_ops.py`: only colours $a$ and $b$ are rewritten. The prose statement is `lean4_formalization_plan.md` §1.2 and the M4 brief (Lemma 3.1).

### 2.3 Chain Lifting for colours in $\{1,2,3,4\}$

**Claim (Lemma 5.1).** Let $c$ be a colouring of $G$ with values in $\{1,2,3,4,5\}$, let $v$ satisfy $c(v) = 5$, and let $a, b \in \{1,2,3,4\}$. Then for every vertex $u \neq v$, the $(a,b)$-Kempe chain of $u$ in $G$ equals the $(a,b)$-Kempe chain of $u$ in $G - v$ under the restriction of $c$:

$$
\mathrm{KempeChain}(G, c, u, a, b) = \mathrm{KempeChain}(G - v,\, c|_{G-v},\, u, a, b).
$$

In Lean vocabulary that is still to be written: for $c(v) = (4 : \mathrm{Fin}\, 5)$, $a \neq 4$, $b \neq 4$, and $u \neq v$,

$$
\{w \mid \texttt{inSameKempeChain}\, G\, c\, a\, b\, u\, w\}
=
\{w \neq v \mid \texttt{inSameKempeChain}\, (G.\mathrm{deleteVerts}\, \{v\})\, c\, a\, b\, u\, w\},
$$

up to the coercion of vertices of the deleted graph. The reason the equality should hold is that $c(v) \notin \{a, b\}$, so $v$ is isolated in $B_{a,b}(G,c)$ and deleting it does not add or remove any $B_{a,b}$-edge among the remaining vertices.

**Lean name of this equality:** none.

**File that was supposed to contain it:** `lean4/KempeReconfiguration/KempeReconfiguration/ChainLifting.lean`

**`sorry` in that file:** no `sorry` tactic. The only occurrence of the word is the header comment “Target: 0 sorry” (line 14). Absence of `sorry` is not a proof of Lemma 5.1. The component equality is not a theorem.

What the file does contain:

| Lean name | Lines | Proved? | Relation to Lemma 5.1 |
|---|---|---|---|
| `vertex_not_in_bichromatic` | 26–34 | yes, no `sorry` | If $c(v) \notin \{a, b\}$ then $v$ has no $B_{a,b}$-edge. This is the isolation step for a general palette. |
| `bichromatic_adj_delete_irrelevant` | 42–49 | the script is `rfl` | The comment (lines 36–38) says the two sides are $B_{a,b}$ in $G$ and in $G.\mathrm{deleteVerts}\, \{v\}$. The theorem statement does not mention `deleteVerts`. Both sides are `bichromaticAdj G c a b u w`. The hypotheses $c(v) \notin \{a, b\}$ and $u, w \neq v$ are unused. This theorem does not state Chain Lifting. |
| `colour5_isolated_in_bichromatic_14` | 59–67 | yes, no `sorry` | If $c(v) = (4 : \mathrm{Fin}\, 5)$ and $a, b \neq 4$, then $v$ has no $B_{a,b}$-edge. This is isolation for paper colours $\{1,2,3,4\}$ against paper colour $5$. |

The block comment at lines 69–81 says the rest explicitly: a formalization that the connected components agree would need the identification of $B_{a,b}(G,c)$ on $V \setminus \{v\}$ with $B_{a,b}(G - v, c|_{G-v})$, and that identification is not proved. The same gap is recorded by Agent 1610’s Lean audit.

**Closed in Lean:** no. Closed only as prose, in `lean4_formalization_plan.md` §1.3 and in the M4 brief (Lemma 5.1, including a suggested signature `chain_lifting` that was never added).

**Python.** `verify_inductive_lift` in `compute/kempe/reduction_search.py` deletes a vertex and compares Kempe chains along a BFS path in $G$ and in $G - v$. That is a finite experiment about lifting a whole reduction path. It is not a proof that $(a,b)$-components agree for $a, b \in \{1,2,3,4\}$ whenever $c(v) = 5$.

---

## 3. What is already closed

| Obligation | In Lean | Only in Markdown or Python |
|---|---|---|
| Kempe swap preserves a proper colouring | Closed: `kempeSwap_preserves_proper` in `Basic.lean`, proof present, no `sorry` | Also implemented and finitely tested in Python; also stated in the formalization plan |
| Never-Revert | Closed: `never_revert` (with `never_revert_pointwise` and `never_revert_card`) in `NeverRevert.lean`, proofs present, no `sorry` | Stated in the formalization plan and the M4 brief. No named Python test |
| Chain Lifting for $\{1,2,3,4\}$ | Not closed. Isolation only: `colour5_isolated_in_bichromatic_14`. No theorem equates chains in $G$ and in $G - v$ | The equality is stated in `lean4_formalization_plan.md` §1.3 and the M4 brief. Python explores a related lift in `verify_inductive_lift` |

`Main.lean` imports the four modules and contains no theorem. Its comments say a `sorry` was left for the remaining gap. There is no such declaration.

Degree-3 No-Merge (`degree3_no_merge` in `Degree3NoMerge.lean`) is outside these three obligations. It is a proved theorem from the typeclass field `Triangulation.link_degree3_complete`, which is an assumption, not a `sorry`. The file says so at lines 74–80.

---

## 4. `sorry` count under `lean4/KempeReconfiguration/`

**Tactic `sorry` count: $0$.**

Searched every `*.lean` file in `lean4/KempeReconfiguration/` (`Basic.lean`, `NeverRevert.lean`, `ChainLifting.lean`, `Degree3NoMerge.lean`, `Main.lean`, `lakefile.lean`). No proof uses the `sorry` tactic, and `lakefile.lean` does not contain the word.

The word `sorry` occurs only in comments. A later count that greps the word will see these lines and must not treat them as open proofs:

| File | Line | Role |
|---|---|---|
| `KempeReconfiguration/Basic.lean` | 12 | Header: “Target: 0 sorry” |
| `KempeReconfiguration/NeverRevert.lean` | 14 | Header: “Target: 0 sorry” |
| `KempeReconfiguration/ChainLifting.lean` | 14 | Header: “Target: 0 sorry” |
| `KempeReconfiguration/Degree3NoMerge.lean` | 16 | Header: “Target: ≤ 2 sorry (planarity axioms)” |
| `KempeReconfiguration/Degree3NoMerge.lean` | 27 | Comment: “TODO: sorry — Mathlib lacks a full planar graph API.” The following field is a typeclass assumption, not a `sorry` |
| `KempeReconfiguration/Degree3NoMerge.lean` | 75 | Comment asserting “0 explicit sorry statements” (the word occurs twice on this line) |
| `KempeReconfiguration/Degree3NoMerge.lean` | 79 | Comment: “rather than a sorry” |
| `KempeReconfiguration/Main.lean` | 7 | Comment: “The proof has one sorry …” |
| `KempeReconfiguration/Main.lean` | 30 | Comment: “We leave this as a declaration (sorry) …” |

`Main.lean` has no theorem, so the comment on line 30 does not correspond to a `sorry`. `Degree3NoMerge.lean` line 27 documents a missing planarity API; the code uses an axiom-style typeclass field instead of `sorry`.

---

## 5. Five Colour Theorem (`foundation` / `f5`)

**Is there a Lean proof in this repository? No.**

Paths searched:

- Every `*.lean` file under `lean4/`. The only Lean project is `lean4/KempeReconfiguration/` (the six files listed in §4). None defines a planarity predicate, a colourability theorem, or a Five Colour Theorem.
- Repository search for `five_color_theorem`, `five_colour_theorem`, `FiveColour`, and `Heawood` inside `*.lean`. No matches.
- The file named in the foundation plan, `Foundation/F5_FiveColorTheorem.lean` (`SolvingFrameworkPlan/NovelProofExploration.md`, Step F5). That path does not exist. No file matching `*Five*` exists in the repository.

What does exist is planning prose, not a proof: a Level-1 sketch with an explicit `sorry` inside a Markdown code block in `SolvingFrameworkPlan/SolvingProofStrategy.md` (around the heading “Level 1: The Five Colour Theorem”), and the same unproved signature in `SolvingFrameworkPlan/NovelProofExploration.md`. Other Markdown files cite Heawood’s 1890 theorem as an external fact. They do not contain a proof.

---

## 6. Acceptance test

Tier-1 is **specified** when a later formalization can be checked against the three claims in §2 without inventing a fourth reading of them.

The check passes only if all three of the following hold, with no new `sorry`:

1. A theorem with the hypotheses and conclusion of `kempeSwap_preserves_proper`: a proper colouring stays proper after swapping $a \leftrightarrow b$ on a set of $\{a, b\}$-coloured vertices that is closed under adjacency into $\{a, b\}$.
2. A theorem with the conclusion of `never_revert`: if neither swapped colour is paper colour $5$ (Lean: the target index is `(4 : Fin 5)` and both swapped colours differ from it), the set of colour-$5$ vertices is unchanged. The pointwise or cardinality forms are acceptable witnesses of the same fact.
3. A theorem that states Lemma 5.1 as component equality: if $c(v) = 5$ and $a, b \in \{1,2,3,4\}$, then for $u \neq v$ the $(a,b)$-Kempe chain of $u$ in $G$ equals its $(a,b)$-Kempe chain in $G - v$.

The check fails if item 3 is marked done by citing `colour5_isolated_in_bichromatic_14`, `vertex_not_in_bichromatic`, or `bichromatic_adj_delete_irrelevant`. Those three do not state the equality of chains.

---

## 7. Not proved

Not proved in this development: the Chain Lifting equality of $(a,b)$-components in $G$ and in $G - v$; any reading of `bichromatic_adj_delete_irrelevant` as a theorem about vertex deletion; the Five Colour Theorem; planarity of the `Triangulation` link axiom; and every $4$-colouring statement (`Main.lean` declares none, including the $n - 4$ Kempe-swap bound and BFS Avoidance).

This specification does not prove those claims. It records the boundary so a later pass cannot treat a comment, an isolation lemma, or a Python experiment as the missing theorem.

---

## 8. Kill criterion

Reject a “Tier-1 closed” claim if any of these is used as evidence:

- `colour5_isolated_in_bichromatic_14` or `vertex_not_in_bichromatic` offered as Lemma 5.1,
- `bichromatic_adj_delete_irrelevant` offered as a `deleteVerts` lemma,
- a comment in `Main.lean` offered as a theorem,
- a grep hit on the word `sorry` inside a comment offered as an open proof or as a finished proof,
- a Five Colour Theorem cited from this repository’s Lean tree.

The specification itself is the wrong artefact if a later proof obligation cannot be aligned with §2.1–§2.3, including the paper-colour / `Fin 5` dictionary in the opening.

---

## 9. Cited evidence

| Fact | Where |
|---|---|
| Swap-preservation theorem and its proof | `lean4/KempeReconfiguration/KempeReconfiguration/Basic.lean`, `kempeSwap_preserves_proper` |
| Never-Revert, three forms | `lean4/KempeReconfiguration/KempeReconfiguration/NeverRevert.lean` |
| Isolation only; component equality absent | `lean4/KempeReconfiguration/KempeReconfiguration/ChainLifting.lean`, especially the comment at lines 69–81 |
| `Main.lean` has imports and comments, no theorem | `lean4/KempeReconfiguration/KempeReconfiguration/Main.lean` |
| Tier-1 statements as originally planned | `backgroundMaterial/agent0051/deliverables/lean4_formalization_plan.md` §§1.1–1.3 |
| Suggested `chain_lifting` signature that was not added | `backgroundMaterial/agent1210/coordinator/manager_M4/manager_M4_brief.md` |
| Static note that Chain Lifting is unfinished, and that `Basic.lean` lines 147, 152, 153 may not be valid tactics | `backgroundMaterial/agent1610/auditor_3_lean4_compile/lean4_audit.md` |
| Python swap and the $K_4$ test | `compute/kempe/kempe_ops.py`, `compute/kempe/tests/test_plan2.py` |
| Python lift experiment, not a proof | `compute/kempe/reduction_search.py`, `verify_inductive_lift` |
| Five Colour Theorem planned, not formalized | `SolvingFrameworkPlan/SolvingProofStrategy.md`, `SolvingFrameworkPlan/NovelProofExploration.md`; no `*.lean` theorem |

---

## 10. Feasibility

**Feasibility of formalizing these three statements before any attempt on the Four Colour Theorem: High.**

Two of the three already have proofs with no `sorry`, and neither uses planarity. The remaining statement, Chain Lifting, is the equality of connected components after deleting a vertex that the isolation lemmas already show is isolated in $B_{a,b}$. That argument lives in Mathlib’s `SimpleGraph.Reachable` and `deleteVerts`. It does not need a planar embedding, Euler’s formula, or the open BFS Avoidance gap. The formalization plan rates this tier High and gives it a $0$-`sorry` target; that rating still matches the file evidence.

Uncertainty, stated so it is not mistaken for a lower rating of the mathematics: this task did not compile the project. Agent 1610 judged that the existing scripts do not build as written (missing `exact`, a `▸` used as a term in `colour5_isolated_in_bichromatic_14`). Repairing those scripts is finite editing. It is not a reason to attempt $4$-colouring first, and it is not a reason to call Lemma 5.1 proved.

---

## 11. Next steps

1. When a later task is allowed to edit Lean, add one theorem whose statement is the component equality in §2.3, and do not discharge it with `sorry`. Keep `colour5_isolated_in_bichromatic_14` as the isolation lemma it is.
2. If a compile gate is required, repair the bare terms in `kempeSwap_preserves_proper` and the term-mode `▸` in `colour5_isolated_in_bichromatic_14`, then build `lean4/KempeReconfiguration`. That repair is outside this specification.
3. Leave the Five Colour Theorem on node `f5`. It has no Lean file here, and it is not one of the three Tier-1 obligations above.

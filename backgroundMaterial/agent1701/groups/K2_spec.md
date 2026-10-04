# K2 — Specification: BFS Avoidance at degree 5, and the reformulation trigger

**Navigator node:** `t1-spec-d5`
**Manager:** M-Kempe
**Status:** Specification only. This document does not prove Conjecture 5.5.

The written conjecture is stated for $\deg(v) \in \{4,5\}$ in `SolvingFrameworkPlan/ExecutiveSummary_Plan2_Status.md` (section 6) and in `backgroundMaterial/agent0051/deliverables/revised_paper_section.md` (section 5.4). This file restricts it to $\deg(v) = 5$, records how the link differs from the degree-4 case, and states the observation that would make the degree-5 case no shorter than the Four Colour Theorem.

---

## 1. Definitions that differ from the degree-4 case

The following are fixed for the rest of this specification. Objects shared with degree 4 (a proper $5$-colouring, an $(a,5)$-Kempe chain, the reconfiguration graph $\mathcal{R}(G-v,5)$, a BFS-optimal path, and a merge) keep their usual meanings; only the link geometry changes.

**Triangulation and link.** Let $G$ be a planar triangulation and let $v \in V(G)$. The neighbours of $v$, in the clockwise order of the embedding, induce a cycle. That cycle is the link of $v$. If $\deg(v) = 4$ the link is a $4$-cycle. If $\deg(v) = 5$ the link is a $5$-cycle $C_5$.

The code records the two geometries as follows. For degree 4, `analyze_degree4_link_merge_geometry` in `compute/kempe/degree4_analysis.py` states that on a link $u_1u_2u_3u_4$ the non-adjacent pairs are $(u_1,u_3)$ and $(u_2,u_4)$, and that only those pairs can lie in different chains, because an adjacent pair shares an edge. For degree 5, `analyze_noninterleaving_at_degree5` in `compute/kempe/degree5_analysis.py` states that on a link $u_1u_2u_3u_4u_5$ the non-adjacent pairs are

$$u_1u_3,\; u_1u_4,\; u_2u_4,\; u_2u_5,\; u_3u_5.$$

**Which neighbour pairs can lie in different $(a,5)$-chains.** Fix $a \in \{1,2,3,4\}$ and write $B_{a,5}(G-v)$ for the subgraph of $G-v$ induced by vertices coloured $a$ or $5$. An $(a,5)$-chain is a connected component of that subgraph. Say that $v$ **bridges** two chains when at least two neighbours of $v$ lie in $B_{a,5}(G-v)$ and in different components. In the checker this is `would_merge`: `distinct_chains >= 2` in `analyze_merge_conditions` (`compute/kempe/merge_analysis.py`).

On a triangulation the link edges survive in $G-v$. If two neighbours are consecutive on the link and both lie in $B_{a,5}(G-v)$, properness forces their colours to be $\{a,5\}$, one each, so the link edge puts them in the same chain. Distinct chains can therefore meet $N(v)$ only at non-consecutive neighbours.

Label the degree-5 link $u_0,u_1,u_2,u_3,u_4$ in cyclic order. Consecutive pairs (cyclic gap $1$) cannot split. Every non-consecutive pair has cyclic gap $2$, and there are five of them:

$$\{u_0,u_2\},\; \{u_1,u_3\},\; \{u_2,u_4\},\; \{u_3,u_0\},\; \{u_4,u_1\}.$$

These are the only pairs that can lie in different $(a,5)$-chains. Equivalently, the splittable pairs are the edges of the complement of the link, and that complement is again a $5$-cycle. Each neighbour lies in two splittable pairs.

That is the difference from degree 4. The complement of a $4$-cycle is a matching of two opposite edges, so each neighbour has one opposite partner. There is no such matching on $C_5$.

**Chain count on the degree-5 link.** Paths of $B_{a,5}(G-v)$ that leave the link can only join components; they cannot separate vertices already joined by a link edge. The number of distinct $(a,5)$-chains that meet $N(v)$ is therefore at most the number of components of the link induced by $S = \{u \in N(v) : c(u) \in \{a,5\}\}$. Every set of three vertices on $C_5$ spans a link edge, because the independence number of $C_5$ is $2$. Hence that induced subgraph has at most two components, and $v$ bridges at most two $(a,5)$-chains. The same cap holds for degree 4. The Agent 0051 merge table agrees: both degrees have maximum distinct chains $2$ (`backgroundMaterial/agent0051/coordinator/manager_M1/sub_S1/S1_report.md`). The table is a reported run, not this counting argument.

**Chain adjacent to $v$.** An $(a,5)$-chain in $G-v$ that contains at least one neighbour of $v$. Swapping such a chain while $v$ bridges two $(a,5)$-chains is a merge: in $G$ the two components are joined through $v$.

**BFS-optimal path.** A shortest path in $\mathcal{R}(G-v,5)$ from $c|_{G-v}$ to a proper colouring that uses at most four colours. The function `bfs_reduce_to_4` returns one such path: the first $4$-colouring reached by breadth-first search (`compute/kempe/reduction_search.py`). `bfs_path_merge_check` inspects that one path. The written conjecture quantifies over every BFS-optimal path.

**Scope warning on the gap counter.** `analyze_noninterleaving_at_degree5` increments `non_adj_pairs_in_diff_chains` for every pair of neighbours in different chains, then computes a gap from `list(G.neighbors(v))`. That list is not documented to be the rotation order, so those gap counts are not used here. The pair list above is the cyclic one in the docstring and in the classification, not a histogram from that counter.

**What Theorem A does and does not say.** Theorem A (Non-Interleaving), `backgroundMaterial/agent0050/coordinator/manager_M2/sub_S1/theorem_A_proof.md`, constrains two Kempe chains on disjoint colour pairs at an external vertex: their neighbour-positions on the link do not interleave. The Degree-5 Classification (`backgroundMaterial/agent0050/coordinator/manager_M2/sub_S2/degree5_classification.md`) uses that constraint on colour patterns of the link in $\{1,2,3,4\}$. It is not a classification of $(a,5)$-splits. A neighbour coloured $5$ lies in $B_{a,5}$ for every $a \in \{1,2,3,4\}$, which the opening setup of that classification (neighbours coloured from $\{1,2,3,4\}$) does not catalogue.

---

## 2. Exact statement for $\deg(v) = 5$

**Conjecture 5.5 at degree 5.** Let $G$ be a planar graph, let $c$ be a proper $5$-colouring of $G$, and let $v$ be a vertex with $c(v) = 5$ and $\deg(v) = 5$. Suppose that in $G-v$ the vertex $v$ bridges at least two distinct $(a,5)$-Kempe chains for some $a \in \{1,2,3,4\}$ (neighbours of $v$ lie in two different chains). Then any BFS-optimal path in $\mathcal{R}(G-v,5)$ from $c|_{G-v}$ to a $4$-colouring does not swap any chain adjacent to $v$.

This is the degree-5 restriction of the statement in `SolvingFrameworkPlan/ExecutiveSummary_Plan2_Status.md`, section 6, and of Conjecture 5.5 in `backgroundMaterial/agent0051/deliverables/revised_paper_section.md`, section 5.4. Those sources state one conjecture for $\deg(v) \in \{4,5\}$.

**Reading used as the acceptance target on triangulations.** Let $G$ be a planar triangulation and keep $c$, $v$, and $a$ as above, with $\deg(v) = 5$ and $c(v) = 5$. If $v$ bridges at least two distinct $(a,5)$-chains in $G-v$, then every shortest path in $\mathcal{R}(G-v,5)$ from $c|_{G-v}$ to a proper $4$-colouring uses no $(a,5)$-swap whose chain contains a neighbour of $v$.

The triangulation reading is the one the link geometry supports. The $C_5$ description fails for a general planar graph: consecutive neighbours in the rotation need not be adjacent, so a gap-$1$ pair can split. The inductive architecture already reduces the Four Colour Theorem to triangulations, and every cited computational check uses triangulations (`generate_triangulations`). A proof of the triangulation reading does not, by itself, discharge the literal wording “any planar graph” for non-maximal plane graphs.

The slogan “does not swap any chain adjacent to $v$” is stronger than a single colour $a$ if it forbids every colour pair. Chain lifting of an $(a,5)$-swap fails when that swap’s chain is one of two or more $(a,5)$-chains meeting $N(v)$. An $(a,5)$-swap of the unique chain that meets $N(v)$ does not merge two chains. The acceptance target is the per-colour reading, which is what `would_merge` and `multi_chain_swap_adjacent` implement.

---

## 3. Why degree 5 is harder than degree 4

Degree 5 is harder because more link pairs can realize a split, those pairs overlap, and the existing degree-5 classification does not remove the splits.

The degree-4 link contributes two splittable pairs, the two opposite edges (`compute/kempe/degree4_analysis.py`, `analyze_degree4_link_merge_geometry`). The degree-5 link contributes the five gap-$2$ pairs listed in `compute/kempe/degree5_analysis.py`. Each neighbour has two possible partners rather than one opposite vertex, and the splittable graph is a $5$-cycle rather than a disjoint matching.

The same reports give the rates. `compute/kempe/merge_analysis.py` documents degree 4 at about $17\%$ and degree 5 at about $31\%$, computed by `bulk_merge_analysis` as `merges / total_cases` among colours $a$ with at least one neighbour in $B_{a,5}$. The run recorded in `backgroundMaterial/agent0051/coordinator/manager_M1/sub_S1/S1_report.md` is finer: degree 4 has $91{,}776$ merges in $528{,}432$ cases ($17.4\%$), and degree 5 has $138{,}288$ merges in $447{,}216$ cases ($30.9\%$). Both rows list maximum distinct chains $2$, so the extra difficulty is not a larger chain count. It is that a $2$-chain bridge occurs more often, on a larger set of overlapping pairs. That table does not state the range of $n$. This specification did not re-run the suite.

Theorem A and the Degree-5 Classification do not close the gap. Section 7 of the executive summary states the point directly: the link is a $5$-cycle, non-adjacent pairs can lie in different chains, and non-interleaving constrains the arrangement but does not prevent all merges, with the $30.9\%$ rate cited there. The classification itself has eight colour-pattern types and resolves each by at most one swap that frees a colour at $v$ (`backgroundMaterial/agent0050/coordinator/manager_M2/sub_S2/S2_report.md`). That report says this is the single-vertex problem only, and that freeing a colour at one degree-5 vertex is already the Five Colour Theorem. It does not describe shortest paths in $\mathcal{R}(G-v,5)$.

Priority 2 in the executive summary asks for an alternative BFS-optimal path that avoids the merge-prone chain. That existential claim is weaker than Conjecture 5.5, which says every BFS-optimal path avoids the chain. The checker tests one path per colouring.

---

## 4. Reformulation trigger

**Observation R.** Degree-5 BFS Avoidance is no shorter than the Four Colour Theorem: there is a construction that, given an arbitrary planar triangulation $H$, returns a planar triangulation $G$, a vertex $v$ with $\deg(v) = 5$, and a proper $5$-colouring $c$ with $c(v) = 5$, such that $v$ bridges at least two distinct $(a,5)$-chains in $G-v$, and $H$ is $4$-colourable if and only if every BFS-optimal path in $\mathcal{R}(G-v,5)$ from $c|_{G-v}$ to a $4$-colouring swaps no chain adjacent to $v$.

If Observation R is established, a proof of the degree-5 case yields $4$-colourability of every planar triangulation by building $(G,v,c)$ and invoking the equivalence. The case is then a reformulation, in the sense of section 10 of the executive summary (“If Conjecture 5.5 is EQUIVALENT TO 4CT”), not a gap inside a shorter inductive argument. The main team should stop treating degree 5 as unfinished bookkeeping on top of the six proved lemmas.

Section 10’s equivalence branch is a status label. Nothing in the cited files proves Observation R. Section 6 only says the gap might be as hard as the Four Colour Theorem.

**Evidence that would support Observation R.**

- A written proof of a construction as in Observation R, including the “if and only if”. It is enough that $H$ range over a class of triangulations for which $4$-colourability is still the full theorem (for example all triangulations of minimum degree $5$).
- A proof that some fixed link pattern allowed by Theorem A and by the Degree-5 Classification (a concrete B1 or B2 pattern in `degree5_classification.md`) occurs both with and without an avoiding shortest path, the two behaviours depending on $G - (N(v) \cup \{v\})$, together with a reduction that encodes an arbitrary triangulation in that outside graph.

The $30.9\%$ merge rate and the eight-type classification do not support Observation R. They show that local non-interleaving leaves merges open. They do not show interreducibility with the Four Colour Theorem.

**Evidence that would refute Observation R.**

- A proof of the triangulation reading in section 2 whose ingredients are the inductive hypothesis on the smaller graph $G-v$, the $C_5$ splitting rule of section 1, Theorem A, and a comparison of paths in $\mathcal{R}(G-v,5)$ that does not build a $4$-colouring of a triangulation outside that induction.
- A concrete candidate construction, offered as a proof of Observation R, that fails on one planar triangulation $H$: either $v$ does not have degree $5$, or $v$ does not bridge two $(a,5)$-chains, or the avoidance statement and the $4$-colourability of $H$ disagree.

A counterexample to Conjecture 5.5 (some BFS-optimal path swaps a chain adjacent to $v$ in a bridge configuration) refutes the conjecture. It does not establish Observation R. That exit is the “DISPROVED” branch of section 10, not the equivalence branch. Finite checks in which avoidance holds also do not refute Observation R: the observation is a claim about all triangulations $H$.

---

## 5. Sequencing recommendation

**Prove the degree-4 case first.**

Section 7 of the executive summary orders degree 4 as Priority 1 and degree 5 as Priority 2. Section 11 assigns the main effort to degree 4 and calls it more tractable. The degree-4 splittable graph is a two-edge matching and the reported merge rate is $17.4\%$; the degree-5 splittable graph is a $5$-cycle and the reported merge rate is $30.9\%$. A degree-4 proof is the test of whether BFS avoidance can be read off from the link at all. Degree 5 should wait until that case is proved or its own specification’s kill criterion has fired.

---

## 6. Kill criterion

Kill the claim that the degree-5 case is a gap shorter than the Four Colour Theorem when either of the following is recorded, and then follow the matching branch of section 10 of the executive summary.

1. **Reformulation.** Observation R is proved. Publish the equivalence. Do not continue a degree-5 proof attempt as a shortcut.
2. **Disproof.** On some triangulation, `bfs_path_merge_check` (`compute/kempe/merge_analysis.py`) returns `multi_chain_swap_adjacent > 0` for a vertex of degree $5$, and the path and the two chains are exhibited. The degree-5 statement is false. Move to the disproof branch (counterexample structure, then the alternative architectures of Priority 3), not to a claim of equivalence.

Until one of those two events, the degree-5 statement stays an open conjecture. Absence of a proof after two iterations is the pivot already written in section 11 for Conjecture 5.5 as a whole; it is not, by itself, evidence for Observation R.

---

## 7. Not proved

Conjecture 5.5 at degree 5 is not proved: the $C_5$ splitting rule, the cap of two chains, Theorem A, the eight-type Degree-5 Classification, and the reported merge and BFS-avoidance counts do not establish it.

---

## 8. Feasibility

**Medium-Low.**

The statement is narrow (degree $5$, one vertex, chains that meet the link, at most two chains), and the cited runs report no BFS merge. The same record shows why a proof is not close: about three in ten eligible degree-5 cases are merge-prone, the splittable pairs form a $5$-cycle rather than a matching, and the written degree-5 classification solves colour-freeing at $v$ rather than shortest paths in $\mathcal{R}(G-v,5)$. Whether Observation R is true is itself open, so the rating is the feasibility of a proof that stays inside the induction, not a claim that the case is equivalent to the Four Colour Theorem.

---

## Acceptance test

A future proof of the triangulation reading must show all of the following.

- $G$ ranges over planar triangulations, $c$ over proper $5$-colourings, $v$ over vertices with $\deg(v) = 5$ and $c(v) = 5$, and $a$ over $\{1,2,3,4\}$.
- Whenever `analyze_merge_conditions` would set `would_merge` for $(G,c,v,a)$, every shortest path in $\mathcal{R}(G-v,5)$ from $c|_{G-v}$ to a $4$-colouring avoids every $(a,5)$-chain that contains a neighbour of $v$.
- The argument applies at every colouring along the path at which a bridge exists, not only at the initial colouring. `bfs_path_merge_check` recomputes chains at each $(a,5)$-step.
- The universal quantifier over shortest paths is proved. Checking the single path returned by `bfs_reduce_to_4` does not cover other geodesics of the same length.

The following do not replace that proof.

| Source | What it is | What it is not |
|---|---|---|
| `S1_report.md` merge table; `merge_analysis.py` docstring | Reported output of `bulk_merge_analysis`: degree-5 merge rate $30.9\%$ ($138{,}288/447{,}216$), max chains $2$ | A proof of avoidance, or of Observation R. The table does not record $n$ |
| Executive summary, section 6; paper section 5.4 | Reported $0$ failures in $1{,}104$ merge-prone cases and $13{,}876$ BFS-path $(a,5)$-swaps, stated for triangulations on $n \leq 8$ in the paper | A check of every shortest path, or a check at degree $5$ alone. `bfs_avoidance_degree5_detailed` is a separate degree-5 filter and was not re-run here |
| `degree5_classification.md`; `S2_report.md` | Eight link types, each freed by at most one swap | A proof of BFS Avoidance. The report identifies the Five Colour Theorem as the content of that classification |
| Theorem A | Non-interleaving of disjoint colour pairs | A ban on $(a,5)$-splits. Section 7 records that merges remain at rate $30.9\%$ |
| Section 10, equivalence branch | The publication plan if equivalence is found | A proof that Observation R holds |

---

## Cited evidence

**Proved in a written argument (used as input, not as a proof of Conjecture 5.5).**

- Degree-3 No-Merge, for contrast: the link is a triangle, so no pair can split (`S1_report.md`; Lemma 5.2 in the revised paper). The one-edge step of that proof is what forbids gap-$1$ splits on $C_5$.
- Theorem A, non-interleaving (`theorem_A_proof.md`).
- The executive summary’s architecture (section 5): Case 3, $\deg(v) \in \{4,5\}$ and $c(v) = 5$, is the open case, conditional on Conjecture 5.5. Degree 5 is inside that case. The $\{1,2,3,4\}$-lifting lemma and the degree-5 colour-freeing classification are marked proved there; BFS Avoidance is not.

**Checked by a program (reported, not re-run for this specification).**

- `bulk_merge_analysis` and `analyze_merge_conditions` in `compute/kempe/merge_analysis.py`, with the degree-5 rate in the module docstring and the counts in `S1_report.md`.
- `bfs_path_merge_check` in the same file: one BFS path, and a merge counted only when `multi_chain` holds and the swapped chain is one of the neighbour chains.
- The pair lists in `compute/kempe/degree4_analysis.py` and `compute/kempe/degree5_analysis.py`.

**Asserted in a summary.**

- “The hardest case”, the $30.9\%$ sentence, and Priority 2’s proposed attack: `SolvingFrameworkPlan/ExecutiveSummary_Plan2_Status.md`, section 7.
- The three exits (proved, disproved, equivalent to the Four Colour Theorem): section 10.
- Effort on degree 4 first: section 11.
- Conjecture 5.5 as a single statement for $\deg(v) \leq 5$ or $\deg(v) \in \{4,5\}$: section 6 and the revised paper, section 5.4. The paper’s computational theorem is explicitly for $n \leq 8$. The summary’s “$0$ counterexamples” sentence does not, in section 6, repeat that bound; the bound is in the paper.

---

## Next steps

1. Keep this file as the degree-5 contract. Do not mark `t1-spec-d5` proved.
2. Prove, or kill, the degree-4 restriction before a degree-5 proof attempt.
3. If a reduction of the kind in Observation R appears, stop and record the equivalence branch.
4. If a later run is commissioned, log $n$, separate degree 5 from degree 4, and state whether every shortest path was checked or only the path from `bfs_reduce_to_4`. That run is evidence, not a proof.

# K1 — Specification: BFS Avoidance at degree 4

**Navigator node:** `t1-spec-d4`
**Manager:** M-Kempe
**Group:** K1
**Date:** 27 September 2026
**Status:** specification only. This document does not prove Conjecture 5.5, does not disprove it, and does not treat any computational record as a proof.

The statement below is Conjecture 5.5 from `SolvingFrameworkPlan/ExecutiveSummary_Plan2_Status.md` §6, restricted to $\deg(v) = 4$. The unrestricted wording also appears in `backgroundMaterial/agent0051/deliverables/revised_paper_section.md` §5.4 and §9.

---

## 1. Definitions

Colours are $\{1,2,3,4,5\}$. Graphs are finite and simple.

**Proper $5$-colouring.** A map $c \colon V(G) \to \{1,2,3,4,5\}$ is a proper $5$-colouring when $uv \in E(G)$ implies $c(u) \neq c(v)$. The map need not use every colour. This is `is_proper_colouring` in `compute/kempe/kempe_ops.py`. A colouring *uses at most four colours* when the image of $c$ has size at most $4$ (`num_colours`).

**Kempe chain.** For colours $a \neq b$ and a vertex $x$ with $c(x) \in \{a,b\}$, the $(a,b)$-Kempe chain of $x$ is the vertex set of the connected component of $x$ in the subgraph of vertices coloured $a$ or $b$ and the edges of $G$ between them. This is `get_kempe_chain` in `compute/kempe/kempe_ops.py`.

**$(a,5)$-chain.** An $(a,b)$-Kempe chain with $b = 5$ and $a \in \{1,2,3,4\}$. Write $B_{a,5}(G,c)$ for the subgraph just described.

**Chain adjacent to $v$.** Let $H = G - v$. An $(a,5)$-chain $K$ of a colouring of $H$ is adjacent to $v$ when $K$ contains at least one neighbour of $v$ in $G$. In `bfs_path_merge_check` (`compute/kempe/merge_analysis.py`) this is the test that the swapped vertex set meets $N(v)$, and, equivalently for an $(a,5)$-swap, that the swapped chain equals the $(a,5)$-chain of such a neighbour.

**Kempe reconfiguration graph $\mathcal{R}(H,5)$.** Vertices are the proper colourings of $H$ with values in $\{1,2,3,4,5\}$. Two colourings are adjacent when one is obtained from the other by swapping the two colours on a single Kempe chain. See `build_reconfiguration_graph` in `compute/kempe/reconfiguration_graph.py`.

**BFS-optimal path.** A path in $\mathcal{R}(H,5)$ from $c|_H$ to some colouring that uses at most four colours, of length equal to the graph distance from $c|_H$ to that set. `bfs_reduce_to_4` in `compute/kempe/reduction_search.py` returns one such path: the first path discovered by breadth-first search. It does not return every shortest path.

**Bridges two chains.** At a colouring $c_i$ of $H$, and for a colour $a \in \{1,2,3,4\}$, the vertex $v$ bridges at least two distinct $(a,5)$-chains when at least two neighbours of $v$ lie in distinct components of $B_{a,5}(H, c_i)$. `analyze_merge_conditions` records this as `would_merge` when `distinct_chains >= 2`.

**Merge.** If $K$ is an $(a,5)$-chain of $H$ and $v$ is adjacent in $G$ both to $K$ and to a vertex of a different $(a,5)$-chain of $H$, then those two chains of $H$, together with $v$, lie in one component of $B_{a,5}(G, c)$. Swapping the component in $G$ then recolours vertices that the swap of $K$ in $H$ does not recolour. That disagreement is a merge. If the swapped chain of $H$ contains no neighbour of $v$, then $v$ does not meet that chain, so the vertex set swapped in $G$ is the same set. This last sentence is the reason avoidance is useful. It is a consequence of the definition of a component. It is not a proof of the conjecture.

---

## 2. Statement for degree $4$

**Conjecture (Degree-$4$ BFS Avoidance).** Let $G$ be a planar graph and let $c \colon V(G) \to \{1,2,3,4,5\}$ be a proper colouring. Let $v \in V(G)$ satisfy $c(v) = 5$ and $\deg(v) = 4$, and write $H = G - v$. Let $P$ be any shortest path in $\mathcal{R}(H,5)$ from $c|_H$ to a colouring of $H$ that uses at most four colours. Whenever a step of $P$ swaps an $(a,5)$-Kempe chain $K$ of the colouring $c_i$ present before that step, for some $a \in \{1,2,3,4\}$, and at least two neighbours of $v$ lie in distinct $(a,5)$-Kempe chains of $(H, c_i)$, the chain $K$ contains no neighbour of $v$.

The source sentence in the executive summary §6 is the same claim with $\deg(v) \in \{4,5\}$. The revised paper §5.4 writes $\deg(v) \le 5$; §9 of that paper writes $\deg(v) \in \{4,5\}$. This specification uses $\deg(v) = 4$ only. The quantifier is over every shortest path, and the bridge test is applied at the colouring immediately before the swap. That is the reading implemented by `classify_path_safety` in `compute/kempe/all_paths_analysis.py` (`is_unsafe` when `merge_prone_at_step` and the swapped chain meets $N(v)$).

### Planar graph, or triangulation?

The conjecture is stated for an arbitrary planar graph. It is not stated only for triangulations.

The $4$-cycle description belongs to triangulations. In a triangulation the neighbours of $v$, in the cyclic order of the link, form a $4$-cycle. Consecutive neighbours are adjacent, so if both lie in $B_{a,5}(H, c_i)$ they lie in one chain. An opposite pair need not be adjacent, so those two neighbours can lie in different $(a,5)$-chains. That is why executive summary §7 treats degree $4$ through a $4$-cycle, and why `degree4_analysis.py` comments that only the opposite pairs $(u_1,u_3)$ and $(u_2,u_4)$ can witness a bridge. The same cycle need not exist in a planar graph that is not a triangulation: a degree-$4$ vertex can have non-adjacent neighbours that are not an opposite pair of a $4$-cycle.

Every computational check cited in §4 enumerates triangulations (`generate_triangulations`). A proof written only for triangulations leaves the planar-graph statement open. A counterexample that is a triangulation refutes the planar-graph statement, because a triangulation is planar. Whether the inductive colouring argument may be restricted to triangulations is a separate reduction. None of the files read for this specification supplies that reduction for Kempe reconfiguration: adding edges changes both proper colourings and Kempe chains.

The Degree-$3$ No-Merge argument has the same restriction. Its written proof assumes a triangulation, so that the link is a triangle (`backgroundMaterial/agent0051/coordinator/manager_M1/sub_S1/S1_report.md`). Executive summary §5 draws Case $2$ for a planar graph. The triangulation hypothesis is in the proof file; the summary's Case $2$ line does not repeat it.

---

## 3. Acceptance test

A proof of this case must establish the displayed conjecture for every planar graph, every proper colouring $c$, every vertex $v$ with $c(v) = 5$ and $\deg(v) = 4$, and every shortest path in $\mathcal{R}(G-v, 5)$. The bridge condition must be checked at every $(a,5)$-step of every such path.

The following remain finite checks, and a proof has to go beyond them. `bfs_path_merge_check` follows one path returned by `bfs_reduce_to_4`. `bfs_avoidance_degree4_detailed` sums that check over degree-$4$ vertices of triangulations up to a chosen order; the function's source file stores no numeric result. The $1{,}104$ merge-prone count in executive summary §6 is a count, for triangulations on at most $8$ vertices, of situations along those single paths, and it is not split by degree. An existential claim (some shortest path avoids the adjacent chain, or some longer path does, or the merge still leaves a free colour at $v$) is a different statement and does not discharge this one.

---

## 4. Evidence

### Proved in a written argument

These arguments constrain where a degree-$4$ bridge can sit, or how non-$(a,5)$ swaps lift. None of them is Degree-$4$ BFS Avoidance.

| Claim | File |
|---|---|
| If $c(v) = 5$ and $a,b \in \{1,2,3,4\}$, the $(a,b)$-chains of $G$ and of $G-v$ coincide. | `backgroundMaterial/agent0050/deliverables/draft_paper_section.md`, Lemma 5.1 |
| Swapping colours in $\{1,2,3,4\}$ does not change the set of vertices coloured $5$. | Same file, Lemma 3.1 |
| In a triangulation, a degree-$3$ vertex coloured $5$ meets at most one $(a,5)$-chain of $G-v$. | `backgroundMaterial/agent0051/coordinator/manager_M1/sub_S1/S1_report.md` |
| In a triangulation, if two neighbours of a degree-$4$ vertex coloured $5$ lie in different $(a,5)$-chains of $G-v$, those neighbours are non-adjacent in the link. The written reason is that a link edge puts both endpoints in one component of $B_{a,5}$. | `backgroundMaterial/agent1210/coordinator/manager_M1/sub_S1/S1_report.md`; the same component reason is commented in `compute/kempe/degree4_analysis.py` |

Proposition 4.1 in `draft_paper_section.md` is a sketch that one $\{1,2,3,4\}$-swap frees a colour at a vertex of degree at most $5$ coloured $5$. It cites Theorem A and does not expand the eight neighbourhood types. It is not evidence for BFS avoidance.

### Checked by a program

The programs implement the predicates. The counts below are the counts written down next to those programs. This specification did not re-run them.

| What was computed | Where the count is written | What the run actually covers |
|---|---|---|
| Along one BFS path, an $(a,5)$-swap is counted as a hit when $v$ bridges at least two $(a,5)$-chains and the swapped chain meets $N(v)$. | `compute/kempe/merge_analysis.py`, `bfs_path_merge_check` | One shortest path per starting colouring, not every shortest path. |
| The same hit count, summed only over vertices of degree $4$. | `compute/kempe/degree4_analysis.py`, `bfs_avoidance_degree4_detailed` | Triangulations. The `.py` file contains no printed totals. |
| $13{,}876$ $(a,5)$-swaps on BFS paths, $1{,}104$ merge-prone situations, $0$ hits, triangulations on $n \le 8$ vertices. | `backgroundMaterial/agent0051/coordinator/manager_M1/sub_S3/S3_report.md`; repeated in `backgroundMaterial/agent0051/deliverables/revised_paper_section.md` §5.4 and §7.3 | All degrees together. One path per colouring. |
| Degree $4$ only, $n \le 8$: $5{,}584$ $(a,5)$-swaps, $556$ merge-prone, $0$ hits. | `backgroundMaterial/agent1210/coordinator/manager_M1/sub_S1/S1_report.md` | The report says the run was `degree4_analysis.py` and that the log was terminal output. No log file is in the repository. |
| Degree-$4$ first-path hits at $n = 9$: $317$ hits among $6{,}925$ merge-prone $(a,5)$-swaps. For the triangulation labelled $T_{9,35}$, vertex $6$ of degree $4$, $24$ colourings on which every shortest path has a hit. | `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md` | Asserted output of the $n = 9$ search. Not re-run here. |
| At $n \le 8$, $1{,}824$ of $14{,}760$ merge-prone colourings have at least one shortest path with a hit and at least one without. | `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S3/S3_report.md` | Not split by degree. The report's path total $73{,}016$ does not equal $2{,}856 + 71{,}160 = 74{,}016$. |

`bulk_merge_analysis` measures how often a bridge exists. It does not measure which chain a shortest path swaps. The $17.4\%$ degree-$4$ rate ($91{,}776$ bridges out of $528{,}432$ cases) is the table in the Agent 0051 S1 report. The docstring of `merge_analysis.py` says "~17%".

### Asserted in a summary

| Assertion | File | Supported by a computation or a proof file? |
|---|---|---|
| $0$ counterexamples in $1{,}104$ merge-prone cases across $13{,}876$ BFS-path $(a,5)$-swaps, offered as the evidence for Conjecture 5.5. | Executive summary §6 | The count is in the Agent 0051 S3 report, for triangulations, $n \le 8$, one path, all degrees. It is not a degree-$4$ split and it is not a check of every shortest path. |
| BFS-optimal paths use small swaps, while merge-prone chains are large global structures. | Executive summary §6 | The smallness of the chains that were measured is in Agent 0051 S3: merge-prone chains have mean size $1.3$, median $1$, and $72.3\%$ singletons. The sentence that those chains are large has no supporting file. S3 states the opposite size comparison. |
| If a shortest path always has an alternative chain that misses $N(v)$, degree $4$ follows. | Executive summary §7 | This is an attack plan. No file proves that an alternative of the same length always exists. |
| If Conjecture 5.5 is proved, the inductive argument is a constructive proof of the Four Colour Theorem with an $O(n)$ swap bound. | Executive summary §10, and the diagram in §5 | The diagram's open case is $\deg(v) \in \{4,5\}$ together. A proof of the degree-$4$ line alone leaves degree $5$ open. |
| Conjecture 5.5 is false; $T_{9,35}$ at a degree-$4$ vertex is a counterexample. | `backgroundMaterial/agent1419/agent1419Report.md` | The detailed table is the M1-S1 report cited above. `backgroundMaterial/agent1610/auditor_2_independent_replication/replication_report.md` did not re-run path safety at $n = 9$ and did not identify $T_{9,35}$ without plantri. That audit does not confirm the kill, and it does not remove the assertion. |

---

## 5. Claims in the executive summary that lack a file

Yes. Two claims in the assigned summary lack a file that says what the summary says.

1. **Merge-prone chains are large.** Executive summary §6. `backgroundMaterial/agent0051/coordinator/manager_M1/sub_S3/S3_report.md` reports that they are smaller than the chains it calls merge-safe. No file in the assigned reading supports "large".

2. **The $1{,}104$ / $13{,}876$ record is the evidence for the degree-$4$ case of the universal statement.** The count's file is the Agent 0051 S3 report, and the same numbers are copied into the revised paper §7.3. That file does not separate degree $4$, does not range over every shortest path, and does not range over planar graphs that are not triangulations. `compute/kempe/degree4_analysis.py` is the degree-$4$ program and contains none of those totals. The later degree-$4$ total $556$ is only in `backgroundMaterial/agent1210/coordinator/manager_M1/sub_S1/S1_report.md`, which points at terminal output that is not in the repository.

A third mismatch is quantitative rather than a missing file. Executive summary §3's "zero failures" across about $2$ million colourings through $n = 10$ is the distance from a $5$-colouring to some $4$-colouring in $\mathcal{R}(G,5)$. That table is a different statement from BFS avoidance on $G - v$. The $n = 10$ row is written with a tilde.

---

## 6. Kill criterion

The degree-$4$ conjecture is false if there exists one planar graph $G$, one proper colouring $c$, one vertex $v$ with $c(v) = 5$ and $\deg(v) = 4$, one colour $a \in \{1,2,3,4\}$, and one shortest path in $\mathcal{R}(G-v, 5)$ from $c|_{G-v}$ to a colouring with at most four colours, such that some $(a,5)$-step of that path swaps a chain containing a neighbour of $v$ while at least two neighbours of $v$ lie in distinct $(a,5)$-chains.

`backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md` asserts examples of this form at $n = 9$, including $24$ colourings of the triangulation it labels $T_{9,35}$ at vertex $6$, which has degree $4$, on which every shortest path is a hit. This specification does not re-run that search. It does not mark the navigator node killed. Confirming one such colouring, with the graph and the path written down, meets the criterion. A failure only of a longer path, or only of a non-shortest path, does not.

---

## 7. Not proved

Degree-$4$ BFS Avoidance, degree-$5$ BFS Avoidance, and the Four Colour Theorem are unproved in this document.

---

## 8. Feasibility

**Low.**

The $4$-cycle link makes the local bridge condition simpler than the degree-$5$ link: only an opposite pair can lie in two chains, and that component fact has a written argument for triangulations. The conjecture also quantifies over every shortest path in $\mathcal{R}(G-v, 5)$. The assigned positive counts follow one breadth-first path on triangulations of order at most $8$, and a later report asserts degree-$4$ hits at order $9$, including colourings on which every shortest path hits. Proving the stated degree-$4$ sentence ahead of the degree-$5$ sentence is not supported by those files. Executive summary §6 already records the remaining obstacle as the passage from a local adjacency condition to a global shortest-path property, and says that passage may be as hard as the Four Colour Theorem.

---

## 9. Next steps

1. Hold this statement fixed. A proof or a kill is about the displayed quantifiers, including every shortest path.
2. Adjudicate one alleged degree-$4$ hit before any proof attempt: the $24$ colourings of $T_{9,35}$ at vertex $6$ in the Agent 1419 M1-S1 report. One confirmed path meets the kill criterion. That check was not run for this specification.
3. If that instance confirms, write a new specification for whatever weaker sentence is actually intended (existence of one safe shortest path, a longer safe path, or a merge that still frees a colour at $v$). Those sentences are not Conjecture 5.5 at degree $4$.
4. If that instance fails, the degree-$4$ obligation that remains is still the universal shortest-path statement on planar graphs. The $C_4$ geometry classifies bridges. It does not choose the path.

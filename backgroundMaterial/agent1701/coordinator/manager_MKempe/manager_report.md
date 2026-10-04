# M-Kempe — combined specification of K1 and K2

**Manager:** M-Kempe
**Date:** 27 September 2026
**Inputs:** `backgroundMaterial/agent1701/groups/K1_spec.md`, `backgroundMaterial/agent1701/groups/K2_spec.md`
**Navigator:** not edited. No proof written. No computation re-run.

## Decision

**ACCEPT SPEC**

K1 has definitions, an exact degree-$4$ statement, an acceptance test, cited evidence graded as written argument, program check, or summary, a kill criterion that one later colouring and one shortest path could meet, and a boundary titled “Not proved”. Degree, chain, and shortest path are separate objects in that file.

K2 has the degree-$5$ link definitions, an exact degree-$5$ statement, an acceptance test, the same three citation grades, a kill criterion (a degree-$5$ path that the checker counts as a hit, and a separate reformulation observation), a boundary titled “Not proved”, and a sequencing recommendation. Degree, chain, and shortest path are separate objects there as well.

## Quantifiers

K1’s statement quantifies over every shortest path in $\mathcal{R}(G-v,5)$, and the bridge test is applied at the colouring immediately before the swap.

K2’s displayed sentence says that any BFS-optimal path does not swap a chain adjacent to $v$, with the bridge written as a hypothesis on $G-v$ rather than as a test at each step. K2 defines a BFS-optimal path as a shortest path, and records that `bfs_reduce_to_4` returns one such path. K2’s acceptance test then requires every shortest path, and requires the bridge test at every colouring along the path where a bridge exists.

The combined specification adopts K1’s quantifier for both degrees: every shortest path, with the bridge read at the colouring before that step, for that colour $a$. K2’s acceptance test already fails a proof that only inspects the path `bfs_reduce_to_4` returns. The word “any” in K2’s displayed sentence is the wording of executive summary §6. It does not name a different set of paths once K2’s own acceptance test is applied. One exhibited shortest path that swaps a neighbour’s $(a,5)$-chain while two neighbours lie in distinct $(a,5)$-chains meets the kill criterion of the adopted statement. A hit only on a longer path does not.

## Combined statement

Colours are $\{1,2,3,4,5\}$. A proper $5$-colouring is a map $c \colon V(G) \to \{1,2,3,4,5\}$ with $c(u) \neq c(v)$ whenever $uv$ is an edge. An $(a,5)$-Kempe chain of a vertex coloured $a$ or $5$ is its component in the subgraph of vertices coloured $a$ or $5$. A chain is adjacent to $v$ when it contains a neighbour of $v$. The Kempe reconfiguration graph $\mathcal{R}(H,5)$ has proper $5$-colourings of $H$ as vertices, and a Kempe swap on one chain as an edge. A shortest path from $c|_H$ to the set of colourings that use at most four colours is a path whose length equals the graph distance to that set.

**Degree $4$.** Let $G$ be a planar graph and let $c$ be a proper $5$-colouring of $G$. Let $v$ satisfy $c(v) = 5$ and $\deg(v) = 4$, and write $H = G - v$. For every shortest path in $\mathcal{R}(H,5)$ from $c|_H$ to a colouring of $H$ that uses at most four colours, and for every step of that path which swaps an $(a,5)$-Kempe chain $K$ of the colouring present before the step, with $a \in \{1,2,3,4\}$: if at least two neighbours of $v$ lie in distinct $(a,5)$-Kempe chains of that colouring, then $K$ contains no neighbour of $v$.

**Degree $5$.** The same sentence with $\deg(v) = 5$.

Both sentences are the restriction of executive summary §6, and of Conjecture 5.5 in `backgroundMaterial/agent0051/deliverables/revised_paper_section.md` §5.4, to one degree. They are stated for an arbitrary planar graph. In a triangulation the neighbours of $v$ form a cycle: a $4$-cycle when $\deg(v) = 4$, a $5$-cycle when $\deg(v) = 5$. On that cycle a link edge puts two neighbours that both lie in $B_{a,5}$ into one chain, so a split can occur only at a non-adjacent pair. For degree $4$ those pairs are the two opposite pairs. For degree $5$ they are the five pairs of cyclic gap $2$, and those pairs overlap. That cycle need not exist when $G$ is planar and not a triangulation. Every computational check cited by K1 or K2 enumerates triangulations. No file read for these specifications supplies a reduction from planar graphs to triangulations that preserves proper colourings and Kempe chains.

The degree-$5$ link is harder for a reason that is written down. `degree4_analysis.py` has two splittable pairs. `degree5_analysis.py` has five. The Agent 0051 S1 table records $91{,}776$ bridges in $528{,}432$ degree-$4$ cases ($17.4\%$) and $138{,}288$ bridges in $447{,}216$ degree-$5$ cases ($30.9\%$), with maximum distinct chains $2$ in both rows. Theorem A and the eight-type Degree-$5$ Classification constrain colour patterns on the link. They do not describe shortest paths in $\mathcal{R}(G-v,5)$.

## Sequencing and strategy revision

K2 recommends proving the degree-$4$ case first. That recommendation is withdrawn.

`backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md` is present and was opened. It asserts a degree-$4$ counterexample. The degree-$4$ row is $317$ BFS-used-unsafe swaps among $6{,}925$ merge-prone $(a,5)$-swaps at $n = 9$. For the triangulation it labels $T_{9,35}$ (written there as `T_9_35`), vertex $v = 6$ of degree $4$, it asserts $32$ merges and $24$ colourings on which every optimal path is unsafe. The same file calls Conjecture 5.5 false as stated.

The conjecture is not intact. The next task is to verify that assertion: identify the triangulation, and write down one colouring and one shortest path that meet the degree-$4$ kill criterion above. Verification has not been re-run. The conjecture is unmarked as killed.

The same file also asserts, at `T_9_25`, vertex $v = 3$ of degree $5$, $24$ colourings on which every optimal path is unsafe. That sentence is not the next task. It is a reason to leave a degree-$5$ proof unopened while the degree-$4$ assertion is still only a report.

`backgroundMaterial/agent1610/auditor_2_independent_replication/replication_report.md` records that path safety at $n = 9$ was not re-run, and that `T_9_35` was not identified without plantri. That audit leaves the assertion in place.

If a re-run confirms one such degree-$4$ path, the following specification is a new sentence: existence of one safe shortest path, a safe path of greater length, or a merge that still frees a colour at $v$. K1 names those three. This report does not choose among them. A confirmed hit is the disproof branch of executive summary §10. It does not establish K2’s Observation R, the claim that degree-$5$ avoidance is equivalent to $4$-colourability of an arbitrary triangulation.

## What is not proved

Degree-$4$ BFS Avoidance, degree-$5$ BFS Avoidance, Observation R, and the Four Colour Theorem are unproved.

The $n = 9$ hits are unproved. They are assertions in the Agent 1419 M1-S1 report. This manager did not re-run the search, and the report does not exhibit the edge set of $T_{9,35}$ or a path.

The following are also unproved: a reduction of the planar-graph statement to triangulations; the executive-summary sentence that merge-prone chains are large; the claim that an alternative chain of the same length always exists; and the claim that a proof of the degree-$4$ line alone yields a constructive proof of the Four Colour Theorem.

## Real, and hot air

The critic should treat the following as real.

- The two combined sentences above, including the universal quantifier over shortest paths and the bridge test at the pre-swap colouring. Degree is $\deg(v) \in \{4,5\}$ with $c(v) = 5$. The chain is one $(a,5)$-component. The path is a shortest path in $\mathcal{R}(G-v,5)$. The single path returned by `bfs_reduce_to_4` is a different object.
- Written arguments that are not this conjecture: coincidence of $(a,b)$-chains for $a,b \in \{1,2,3,4\}$ (`backgroundMaterial/agent0050/deliverables/draft_paper_section.md`, Lemma 5.1); $\{1,2,3,4\}$-swaps preserve the set coloured $5$ (same file, Lemma 3.1); degree-$3$ no-merge in a triangulation (`backgroundMaterial/agent0051/coordinator/manager_M1/sub_S1/S1_report.md`); a link edge forces one $(a,5)$-component (`backgroundMaterial/agent1210/coordinator/manager_M1/sub_S1/S1_report.md`, and the comment in `compute/kempe/degree4_analysis.py`); Theorem A (`backgroundMaterial/agent0050/coordinator/manager_M2/sub_S1/theorem_A_proof.md`).
- The five gap-$2$ pairs on a degree-$5$ link, and the cap of two $(a,5)$-chains meeting $N(v)$ on a triangulation, as the counting argument in K2. The Agent 0051 merge table’s maximum of $2$ is a reported run, separate from that counting.
- Program scope, as K1 and K2 state it: `bfs_path_merge_check` follows one path; the $1{,}104$ and $13{,}876$ figures are triangulations, $n \le 8$, all degrees, one path, written in `backgroundMaterial/agent0051/coordinator/manager_M1/sub_S3/S3_report.md`; the degree-$4$ split $5{,}584$ / $556$ / $0$ at $n \le 8$ is only in the Agent 1210 S1 report, which points at terminal output that is not in the repository.
- The assertion, as text in a file that opens: `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md`, lines recording `T_9_35`, vertex $6$, degree $4$, and $24$ colourings on which every optimal path is unsafe, together with the degree-$4$ count $317$.

The critic should treat the following as hot air.

- Conjecture 5.5 as an intact gap, and the plan to prove degree $4$ before degree $5$.
- Conjecture 5.5 as a completed kill. The asserting file exists. A re-run with the graph and a path written down does not.
- Executive summary §6, “merge-prone chains are large.” Agent 0051 S3 reports those chains smaller than the chains it calls merge-safe.
- The $1{,}104$ / $13{,}876$ record as evidence for the universal degree-$4$ sentence.
- The path total $73{,}016$ in `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S3/S3_report.md`. That report prints the total with “(sic)”. The two summands on the $n = 7$ and $n = 8$ rows are $2{,}856$ and $71{,}160$.
- Observation R, and section 10’s equivalence branch, as established.
- The salvage sentences in the same $n = 9$ report (a safe path of length $3$ when the optimum is $2$) as theorems. They sit in the asserting file and have not been re-run.

## Feasibility

Ratings below are the ones this manager will defend.

| Claim | Rating | Reason |
|---|---|---|
| A proof of the degree-$4$ sentence above | **Low** | The positive counts follow one breadth-first path on triangulations of order at most $8$. An opened report asserts degree-$4$ hits at order $9$, including colourings on which every shortest path hits. The obstacle the executive summary already names is the passage from a local bridge to a shortest path in $\mathcal{R}(G-v,5)$. |
| A proof of the degree-$5$ sentence above | **Low** | K2 rated this Medium-Low from the $C_5$ being narrow and from cited runs with no BFS merge. The file opened here asserts $24$ degree-$5$ colourings at `T_9_25` on which every optimal path is unsafe. The five overlapping pairs and the $30.9\%$ bridge rate explain local difficulty. They are not a proof rating. |
| Re-running the named $T_{9,35}$ check after the triangulation is identified | **Medium** | The target is finite: one labelled graph, one vertex, $24$ colourings. The report does not give the edge set. The Agent 1610 replication did not identify that label without plantri and did not re-run path safety at $n = 9$. |
| The triangulation link facts: which neighbour pairs can lie in two $(a,5)$-chains, and the cap of two chains | **High** | These are component arguments about the link. They are not BFS Avoidance. |

## Next step

Verify the degree-$4$ assertion for `T_9_35`, vertex $6$, in `backgroundMaterial/agent1419/coordinator/manager_M1/sub_S1/S1_report.md`. Leave both proof attempts unopened until that verification is written down.

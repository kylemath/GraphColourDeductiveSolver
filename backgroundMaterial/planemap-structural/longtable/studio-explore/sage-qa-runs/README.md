# [exploratory] Sage QA runs (SolvingFrameworkPlan/docs/working/SageInternQA-2026-10-06.md), Mac Studio

## Run 1: rigidity of the 16 new edge-deletion classes (`rigidity.py`, `rigidity.jsonl`)
- Each new class (from ../kempe-classes/edge-new-classes.jsonl) is walked in T - e by an independent Python Kempe implementation (whole-component swaps, states up to renaming). Per state, it counts the colour pairs whose bichromatic subgraph is connected.
- 17 new classes in 16 edge orbits; every class has exactly 6 states, matching the C++ count.
- **No state is frozen.** Each state has 3, 4 or 5 connected pairs out of 6: 12 classes have 4 in all 6 states; 5 classes have 5 in 4 states and 3 in 2.
- The two ends of e share a colour throughout every class.

## Run 2: link-touching-only reachability (`kreach.cpp`, `linkonly.py`, `linkonly.jsonl`)
- Moves on T - v are restricted to two-colour components that meet the link of v. Restricted and unrestricted moves are compared.
- depth = max over states of the fewest moves to a filled state (link on <= 3 colours).
- Orders 12-20, every degree-5 hole orbit (882 holes):
  - no targetless class;
  - never more classes than with unrestricted moves;
  - depth unchanged except 2 -> 3 at 16 holes (1 at order 19, 15 at order 20).
- The four radius-5 certificates (91a307 h22, 8a23ee h23, 62661a h23, 80b930 h23): link-only moves give 1 class, nothing targetless, and depth 5, identical to unrestricted moves.

## Run 4: merge number (`mergenum.py`, `mergenum-N.jsonl`, summaries)
- Definition: the fewest vertices X such that every Kempe class of T restricts into ONE Kempe class of T - X. It is computed with `kmap.cpp` extended to vertex sets (built as `kmap_s`), searching |X| = 1, 2, 3 exhaustively.
- Coverage: orders 12-23, every graph.
- **Every multi-class T has merge number 1**: some single vertex deletion merges all its Kempe classes. kappa(T) reaches 45 at order 20, 35 at 21, 42 at 22 and 53 at 23.
- Graphs with kappa(T) = 1 (merge number 0): 1 at 16, 1 at 17, 5 at 20, 2 at 21, 8 at 22, 12 at 23.
- In orders 12-20, the first merging vertex in label order has degree 5 in 73 graphs, 6 in 35, 7 in 2 and 8 in 1.

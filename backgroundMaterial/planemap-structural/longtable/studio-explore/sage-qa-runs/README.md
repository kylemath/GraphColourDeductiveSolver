# [exploratory] Sage QA runs (SolvingFrameworkPlan/docs/working/SageInternQA-2026-10-06.md), Mac Studio

## Run 1: rigidity of the 16 new edge-deletion classes (`rigidity.py`, `rigidity.jsonl`)
- Each new class (from ../kempe-classes/edge-new-classes.jsonl) is walked in T - e by an independent Python Kempe implementation (whole-component swaps, states up to renaming). Per state, it counts the colour pairs whose bichromatic subgraph is connected.
- Every class has exactly 6 states, matching the C++ count.
- **No state is frozen.** Each state has 3, 4 or 5 connected pairs out of 6: some classes are 4 for all 6 states, others 5 for 4 states and 3 for 2.
- The two ends of e share a colour throughout every class.

## Run 2: link-touching-only reachability (`kreach.cpp`, `linkonly.py`, `linkonly.jsonl`)
- Moves on T - v are restricted to two-colour components that meet the link of v. Restricted and unrestricted moves are compared.
- depth = max over states of the fewest moves to a filled state (link on <= 3 colours).
- Orders 12-20, every degree-5 hole orbit (882 holes):
  - no targetless class;
  - never more classes than with unrestricted moves;
  - depth unchanged except 2 -> 3 at 16 holes (1 at order 19, 15 at order 20).
- The four radius-5 certificates (91a307 h22, 8a23ee h23, 62661a h23, 80b930 h23): link-only moves give 1 class, nothing targetless, and depth 5, identical to unrestricted moves.

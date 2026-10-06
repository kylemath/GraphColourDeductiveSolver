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

## Run 4 follow-up: which single deletions merge all of T's classes (`mergefrac.py`, `mergefrac.jsonl`)
- For every multi-class T at orders 12-23, every vertex v: does deleting v merge all of T's Kempe classes into one class of T - v?
- Fraction of vertices that merge all classes, by degree of v:
  - degree 5: 1.0 up to order 17, 0.949 at 18, then 0.97 at 20-23;
  - degree 6: 1.0 up to 20, then 0.987-0.996;
  - degree 7+: 1.0 up to 20, then 0.994-1.0.
- Multi-class T with NO merging vertex of degree 5 (a non-degree-5 vertex still merges): 2 at order 20, 3 at 21, 8 at 22, 18 at 23. So a degree-5 merging vertex does not always exist.
- No merging vertex ever leaves kappa(T - v) >= 2.
- No vertex deletion created a new class anywhere: 0 in every order.

## Run 5: candidate potentials on hard holes (`potentials2.py`, `run5.txt`; first pass `potentials.py`)
- Test: for each candidate Phi, the number of UNFILLED states of T - v from which no single Kempe move strictly lowers Phi ("lower"), or strictly raises it ("raise"). A move into a filled state always counts as progress. A candidate works iff 0 states are stuck.
- Candidates (coordinator's list, built on Studio intel's coset_potential.py conventions): conn_pairs, link_comps, link_comps_max, lock_size, lock_dist, Intern D's K vector, and Phi by role (beta/gamma/delta, with k(u) = 6 - deg). Plus the lexicographic combinations (1,2,3) and (3,1,2).
- Holes:
  - the four radius-5 certificates (91a307 h22, 8a23ee h23, 62661a h23, 80b930 h23);
  - Studio intel's F-cycle hole (fcycle/fcycle_order22.json, hole 15, main 22ff272);
  - the census order-22 rho-5 hole (plantri index 93, hole 17);
  - Errera's two rho-3 holes (0, 4).
- **No candidate works on any hole, in either direction.** The fewest stuck states:
  - lock_size, lowered: 9 / 2 / 2 / 7 / 4 / 2 / 10 / 10 stuck, out of 737 / 1095 / 1095 / 2713 / 144 / 202 / 60 / 60 unfilled (same hole order as above);
  - lock_dist, lowered: 6 / 2 / 2 / 7 / 4 / 2 / 0 / 0. It is 0 at Errera's holes only.
  - lex_3_1_2 is close to lock_size.
- link_comps and link_comps_max are constant on unfilled states at every hole, so every unfilled state is stuck for them.

## Run 5 follow-up (A): least k for k-step descent (`potentials3.py --leastk`, `leastk.txt`)
- For every unfilled state, the least k such that some sequence of k swaps reaches a strictly lower value or a filled state. The histogram is given per hole, with the joint distribution against the state's distance to the filled set.
- Holes: as in run 5.
- **k <= 3 everywhere.**
  - lex (lock_size, lock_dist): k <= 2 at all four certificates and both Errera holes. k = 3 for only 5 states: 4 at the F-cycle hole, 1 at the order-22 rho-5 hole.
  - lock_size alone: k = 3 at the same 5 states.
  - lock_dist alone: k = 3 at 1 state each of 8a23ee and 62661a, and 1 of order-22.
- **k does not track the radius.** Most states at distance 4-5 have k = 1, and the k = 2 or 3 states sit at distances 2-5.

## (B) inert-disc check (`inertdisc.py`, `inertdisc.txt`, `inertdisc-91a307-interior.json`)
- Every swap on a shortest filling sequence out of a DL state is checked: 1,155 / 1,042 / 1,042 / 3,834 swaps at the certificates, 220 at the F-cycle hole, 120 + 120 at Errera.
- Lock curve: v plus a shortest path m ~ a (resp. m ~ b) inside the lock chain. Disc: the side containing x_{j+2} (a stated convention).
- Violation: the swapped component meets no lock chain and lies wholly inside a disc.
- Nearly all violations are swaps of the component containing x_{j+2} itself, which lies in the disc by this convention.
- **Genuine interior violations (component off the link): 4, all at certificate 91a307 hole 22.** They are 2 states (frames 2 and 4) at distance 3, each with a shortest-fill swap of component {18} or {7, 8, 18} strictly inside lock disc 2. The full colourings are in `inertdisc-91a307-interior.json`.
- Every other hole has 0 genuine violations.

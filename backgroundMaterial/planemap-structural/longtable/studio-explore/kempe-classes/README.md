# [exploratory] Kempe-class multiplicity and the class map T -> T - v / T - e (Mac Studio, workstream A)

This folder is in progress; the full stratified tables follow when the orders 21-26 runs finish.

## Edge deletions that create a new Kempe class (planar positive controls)
`edge-new-classes.jsonl` lists every edge orbit, at orders 12-20 of plantri -m5 -c4, where T - e has a Kempe class that contains no restriction of a 4-colouring of T. Made by `edge_new.py` from the `kmapcensus.py` / `kmap.cpp` output.
- Each record has the plantri ascii (neighbours clockwise, labels 0-based), the edge, its endpoint degrees, kappa(T), kappa(T - e), and each new class's size with one representative colouring.
- In every new class the two ends of e share a colour; the script asserts this.
- 16 edge orbits: 8 at order 17 (graphs 0 and 1) and 8 at order 20 (graphs 10, 12, 24, 32, 33).
- Every new class has exactly 6 states. Graph 10 at order 20 has two new classes.
- Over the same graphs, deleting any vertex of degree 5, 6 or 7 created no new class.

## Intern D's Conjecture M (`bridge.py`, `kmap.cpp` built with KMAP_BRIDGE as `kmap_m`)
- Statement: if deleting v merges two T-classes, a path filled -> one unfilled state -> filled joins them in the Kempe graph of T - v. "Unfilled" means not the restriction of any T-colouring.
- Measured: for every merged pair, the fewest unfilled states on a T - v Kempe path between the two classes' restrictions with an all-unfilled interior. 0 is a direct move; -1 means joined only through other T-classes.
- Weak form: the merged T-classes are connected using bridges with at most 1 unfilled state.
- Coverage: orders 12-20, every degree 5/6/7 vertex orbit whose deletion merges classes. Per-hole records are in `bridge-N.jsonl`, histograms in `bridge-summary.jsonl`.
- Result: **killed**, in both forms.
  - Smallest case: order 14, the only graph, degree-5 hole. Its one merged pair needs 2 unfilled states, and the weak form fails.
  - Order 20: degree-5 merged pairs need up to 16 unfilled states, and the weak form fails at 573 of 585 merging degree-5 holes.
  - The icosahedron, deleting any vertex: 45 merged pairs (10 bridged by 1 unfilled state, 15 need 2, 20 only via other classes). The weak form holds there.

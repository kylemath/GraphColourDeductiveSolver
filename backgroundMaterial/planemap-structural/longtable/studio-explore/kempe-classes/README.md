# [exploratory] Kempe-class multiplicity and the class map T -> T - v / T - e (Mac Studio, workstream A)

This folder is in progress. The stratified table (rho by kappa and merging, kmap census orders 21-26) follows when that run finishes.

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

## Class multiplicity per order (`kclass.cpp`, `kcensus.py`, `kc-summary-N.json`, `kc-table.md`)
- For each graph, kappa(T) is computed. For each vertex orbit of degree 5, 6 or 7, kappa(T - v) and its targetless classes are computed.
- f2 = the fraction of hole INSTANCES (orbit-weighted) where T - v has >= 2 Kempe classes.
- `multiclass-holes.jsonl` holds every hole record with >= 2 classes: 20,444 records, orders 12-25.
- Order 26 is still running.

| order | graphs | T with >=2 classes | T max classes | deg5 orbits | deg5 instances | deg5 f2 | deg5 max | deg6 f2 | deg6 max | deg7 f2 | deg7 max | targetless (5/6/7) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 12 | 1 | 1 | 10 | 1 | 12 | 0.0 | 1 | - | - | - | - | 0/0/0 |
| 14 | 1 | 1 | 2 | 1 | 12 | 0.0 | 1 | 0.0 | 1 | - | - | 0/0/0 |
| 15 | 1 | 1 | 3 | 2 | 12 | 0.0 | 1 | 0.0 | 1 | - | - | 0/0/0 |
| 16 | 3 | 2 | 2 | 5 | 38 | 0.0 | 1 | 0.0 | 1 | 0.0 | 1 | 0/0/0 |
| 17 | 4 | 3 | 9 | 19 | 49 | 0.0 | 1 | 0.0 | 1 | 0.0 | 1 | 0/0/0 |
| 18 | 12 | 12 | 17 | 53 | 156 | 0.0513 | 2 | 0.0 | 1 | 0.0 | 1 | 0/0/0 |
| 19 | 23 | 23 | 16 | 179 | 306 | 0.0 | 1 | 0.0 | 1 | 0.0 | 1 | 0/0/0 |
| 20 | 73 | 68 | 45 | 622 | 1001 | 0.032 | 2 | 0.0 | 1 | 0.0 | 1 | 0/0/0 |
| 21 | 191 | 189 | 35 | 2180 | 2696 | 0.026 | 3 | 0.0041 | 2 | 0.0 | 1 | 0/0/0 |
| 22 | 649 | 641 | 42 | 7869 | 9442 | 0.0282 | 5 | 0.0094 | 2 | 0.0028 | 2 | 0/0/0 |
| 23 | 2054 | 2042 | 53 | 28608 | 30829 | 0.0293 | 12 | 0.0126 | 3 | 0.007 | 2 | 0/0/0 |
| 24 | 7209 | 7193 | 54 | 104951 | 111492 | 0.0302 | 12 | 0.0159 | 4 | 0.0102 | 2 | 0/0/0 |
| 25 | 24963 | 24938 | 72 | 387665 | 397708 | 0.0331 | 12 | 0.0189 | 4 | 0.0125 | 2 | 0/0/0 |

- No targetless class at any vertex of degree 5, 6 or 7, at any order.
- At degree 5, f2 is about 3% and rising slowly (0.026 at 21, 0.033 at 25). The maximum number of classes of T - v is 12 at orders 23-25.
- Positive controls (`torus.py`, `torus.jsonl`): the 6x6 triangular torus has 2 classes (Mohar-Salas). Deleting a vertex of the 7x7 torus (degree 6) creates 1,350 targetless classes.

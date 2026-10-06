# [exploratory] Kempe-class multiplicity and the class map T -> T - v / T - e (Mac Studio, workstream A)

This folder is in progress; the full stratified tables follow when the orders 21-26 runs finish.

## Edge deletions that create a new Kempe class (planar positive controls)
`edge-new-classes.jsonl` lists every edge orbit, at orders 12-20 of plantri -m5 -c4, where T - e has a Kempe class that contains no restriction of a 4-colouring of T. Made by `edge_new.py` from the `kmapcensus.py` / `kmap.cpp` output.
- Each record has the plantri ascii (neighbours clockwise, labels 0-based), the edge, its endpoint degrees, kappa(T), kappa(T - e), and each new class's size with one representative colouring.
- In every new class the two ends of e share a colour; the script asserts this.
- 16 edge orbits: 8 at order 17 (graphs 0 and 1) and 8 at order 20 (graphs 10, 12, 24, 32, 33).
- Every new class has exactly 6 states. Graph 10 at order 20 has two new classes.
- Over the same graphs, deleting any vertex of degree 5, 6 or 7 created no new class.

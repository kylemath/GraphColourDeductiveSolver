# 18-torus-floor [exploratory]

Question: does the sphere "quarter floor" (every Kempe class of 4-colourings of T - v at a degree-5 vertex v has >= 1/4 of its states filled, i.e. the 5 link vertices use <= 3 colours) also hold on torus triangulations?

**Answer: no. It fails badly, including targetless classes (0 filled) and even frozen single-state classes.**

## Method
- `torus.py`: triangular lattice T(r,s) with wraparound plus random edge flips (flip keeps simplicity and min degree >= 5; some runs bias toward more degree-5 vertices). Every graph is validated: V-E+F=0, each edge in exactly 2 faces, each vertex link a single cycle, simple, min degree >= 5, and no 3-cycle that is not a face (so no separating or non-contractible triangle). Graphs are deduplicated within a run by a WL-hash invariant.
- `run_floor.py out.jsonl budget seed reps sizes`: for each graph and each degree-5 vertex v, `kempe_py.Space` (../common, needs only the adjacency and the link set; nothing planar is used) enumerates all proper 4-colourings of T - v up to renaming, builds the whole-component Kempe move graph, and records per class (size, filled).
- `aggregate.py` -> `aggregate-output.txt` (table, first violation re-verified from the face list). `verify_first.py`: independent no-engine check of the smallest violation. `sphere_control.py`: icosahedron through the same engine (one class, 20 states, 10 filled).
- Data: `runA/B/C.jsonl.gz` (seeds 11, 22, 33; full face lists + per-hole class data). Runs: 2 processes, `nice -n 10`, on AC, each <= 12 min, nothing left running.
- Holes where T - v has no 4-colouring are skipped (contribute no classes).

## Result (1,723 graphs, 17,696 degree-5 holes with colourable T-v, 86,175 classes)
See `aggregate-output.txt`. Min filled fraction over all classes = 0. 24,354 classes are below 1/4, 21,915 of them targetless; 1,505 of 1,723 graphs have at least one violation. Violations appear already at n = 16.

Smallest violation (T(4,4) family, n=16, degrees 5x5, 6x6, 7x5): v = 11, link (6,7,8,12,15). T - v has 11 states in 2 classes; one class is a single FROZEN colouring (every {p,q}-subgraph is connected, so every Kempe swap is a renaming) in which the link uses all 4 colours: class size 1, filled 0. Full face list in `aggregate-output.txt`.

Interpretation: the floor (and even "every class reaches a filled state", R*) needs sphere topology; Kempe chains winding around the torus can freeze a colouring.
Caveat: only random flip-walks from lattices were sampled (not all torus triangulations); the violation direction is existential so this is conclusive for "fails on the torus".

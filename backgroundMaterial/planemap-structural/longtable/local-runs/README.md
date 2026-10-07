# [exploratory] Local compute runs (MacBook, standing in for the Mac Studio compute agent), 2026-10-06

Everything here is exploratory computation. Nothing here is a proof.

## Machine and caps
- MacBook, 14 cores, on AC power. Every job ran under `nice -n 10`, with at most 6 workers.
- About 45 CPU-minutes in total. The longest job took 5.3 minutes of wall time (item 5, A+B full enumeration).
- No daemons were left running and nothing was downloaded. `plantri` is not installed: graph lists come from `studiointel/gentri/triN.txt` (gen_tri, 4-connected min-degree-5 triangulations). The counts per order match plantri -m5 -c4.

## Definitions (shared by all items)
- **Graph and hole.** T is a plane triangulation and v is a hole.
- **State.** A proper 4-colouring of T − v, up to renaming of the colours. The canonical form relabels colours by first occurrence along a fixed vertex order.
- **Move.** Swap two colours on one whole connected two-colour component of T − v. Singletons are allowed. A swap of a whole colour pair is a renaming, so it leaves the state unchanged.
- **Filled.** The link of v uses at most 3 colours.
- **dist(s).** The fewest moves from s to a filled state.
- **κ.** The number of Kempe classes, that is, connected components of the move graph.
- **Targetless.** A class with no filled state.
- **ρ.** The maximum of dist over all states. It is −1 if some class is targetless.
- **DL (doubly locked).** For an unfilled state, take the frame: repeat c(x_j) = c(x_{j+2}), m = x_{j+1}, a = x_{j+3}, b = x_{j+4}, μ = c(m). Then:
  - lock 1: a lies in K1, the {μ, c(a)}-component of m;
  - lock 2: b lies in K2, the {μ, c(b)}-component of m.
  - A state is DL if both locks hold.

## Code
- `common/kempe_py.py` is a plain-Python Kempe engine, written fresh. It is stdlib only and imports no team code. It enumerates the states, builds the move graph, and computes classes and multi-source BFS distances.
- `common/krad.cpp` is derived from `studio-explore/kempe-classes/kclass.cpp`, with the same enumeration and moves. It adds the move graph, BFS distances, the radius of each class, and a query colouring.
- `common/rball.cpp` computes the exact radius of given states by BFS from each state, without full enumeration.
- Build:
  ```
  cd common
  clang++ -O2 -std=c++17 -o krad krad.cpp
  clang++ -O2 -std=c++17 -o rball rball.cpp
  clang++ -O2 -std=c++17 -o kclass ../../studio-explore/kempe-classes/kclass.cpp
  clang++ -O2 -std=c++17 -o k3 ../../studio-explore/conjecture-K3/k3.cpp
  ```
  The binaries are not committed.

## 1. Heawood 1890 (`1-heawood1890/`)
- Run with `python3 heawood_run.py > heawood-results.json`.
- The input is `historical-traps/heawood1890.json` (25 vertices, 69 edges).
- **κ(T) = 12**, with 292 colourings of T up to renaming. krad, kclass and Python all agree.
- The table covers every degree-5 hole. Every row agrees across all three engines: C++ krad, the unchanged C++ kclass, and the independent Python BFS.

| hole | link | states | filled | κ(T−v) | class sizes | targetless | ρ | 3 engines agree |
|---|---|---|---|---|---|---|---|---|
| B1 (0) | G1 R2 G2 R1 Y1 | 578 | 292 | 2 | 188, 390 | 0 | 2 | yes |
| B2 (1) | G2 R2 Y3 R3 Y2 | 628 | 292 | 2 | 208, 420 | 0 | 2 | yes |
| B4 (3) | R4 G4 R5 Y5 G5 | 598 | 292 | 1 | 598 | 0 | 2 | yes |
| B6 (5) | G5 Y5 G6 R6 Y6 | 538 | 292 | 1 | 538 | 0 | 2 | yes |
| G2 (7) | R1 B1 R2 B2 Y2 | 548 | 292 | 2 | 248, 300 | 0 | 2 | yes |
| G3 (8) | R3 B3 Y1 R1 Y2 | 518 | 292 | 2 | 188, 330 | 0 | 2 | yes |
| G5 (10) | R4 B4 Y5 B6 Y6 | 598 | 292 | 1 | 598 | 0 | 2 | yes |
| G6 (11) | R6 B6 Y5 R5 Y4 | 648 | 292 | 1 | 648 | 0 | 2 | yes |
| R1 (12) | B1 G2 Y2 G3 Y1 | 768 | 292 | 2 | 480, 288 | 0 | 2 | yes |
| R5 (16) | B4 G4 Y4 G6 Y5 | 538 | 292 | 1 | 538 | 0 | 2 | yes |
| R6 (17) | Y4 B5 Y6 B6 G6 | 598 | 292 | 1 | 598 | 0 | 2 | yes |
| **V (18)** | B3 R3 Y3 G4 R4 | 708 | 292 | **3** | 256, 420, 32 | 0 | **2** | yes |
| Y1 (19) | G1 B1 R1 G3 B3 | 608 | 292 | 2 | 248, 360 | 0 | 2 | yes |
| Y2 (20) | G2 B2 R3 G3 R1 | 668 | 292 | 2 | 420, 248 | 0 | 2 | yes |
| Y4 (22) | G4 B5 R6 G6 R5 | 598 | 292 | 1 | 598 | 0 | 2 | yes |
| Y5 (23) | G5 B4 R5 G6 B6 | 648 | 292 | 1 | 648 | 0 | 2 | yes |

**Heawood's own colouring at V.**
- The link colours read b r y g r.
- Its class has 420 states, 180 of them filled, and the class radius is 2.
- Heawood's colouring is at **distance 2**. krad's query gives the same numbers.
- One shortest filling sequence (vertex names carry Heawood's original letters; the colour shown is the current colour):
  1. Swap {g, r} on the component {G1, G2, G3, R1, R2, R3}. The link becomes b g y g r.
  2. Swap {r, y} on {G1, G2, G3 (now r), R4, R5, R6, Y1, Y2, Y4, Y5, Y6}. The link becomes b g y g y, which is filled.
- The only shortest first moves are the two {g, r} components: {G1, G2, G3, R1, R2, R3} and {G4, G5, G6, R4, R5, R6}.

## 2. Edge-trap check (`2-edge-trap/`)
- Run with `python3 edge_trap.py > edge-trap-results.json`.
- Setup:
  - each class is walked in T − e from its stored representative;
  - x and y are the ends of e, and c is their colour;
  - p and q are the two common neighbours of x and y in T;
  - r is the fourth colour; when c(p) = c(q), both remaining colours are tested.
- 16 records give 17 new classes, all of size 6 (matching the stored data), for 102 states in all.

| order / index | edge | degrees | class | (1) {c,r} joins x,y | (2) p,q not {c(p),c(q)}-joined | (3) c dominating | (4) c(p)=c(q) |
|---|---|---|---|---|---|---|---|
| 17/0 | 0-1 | 5,5 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 17/0 | 3-4 | 6,5 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 17/0 | 4-5 | 5,6 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 17/1 | 0-3 | 5,6 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 17/1 | 0-5 | 5,5 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 17/1 | 1-2 | 5,6 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 17/1 | 1-6 | 5,6 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 17/1 | 5-6 | 5,6 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 20/10 | 1-7 | 6,6 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 20/10 | 1-7 | 6,6 | 1 | 6/6 | 4/4 | 6/6 | 2/6 |
| 20/12 | 0-4 | 5,7 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 20/12 | 2-8 | 5,5 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 20/24 | 0-4 | 5,6 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 20/24 | 2-8 | 5,7 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 20/24 | 3-4 | 5,6 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 20/32 | 1-7 | 6,6 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |
| 20/33 | 1-6 | 6,6 | 0 | 6/6 | 4/4 | 6/6 | 2/6 |

- (2) applies only where c(p) ≠ c(q), which is 4 of the 6 states in each class.
- In the 2 states per class with c(p) = c(q), x and y are {c, t}-joined for **both** remaining colours t.
- Math's Theorem 1 condition (x and y share a {c, t}-component for all three t ≠ c) holds in all 102 states.
- Every swap image stays in the class. This is Intern D's request 3.

## 3. Inert-disc (`3-inert-disc/`)
**Audit replay.**
- Run the audit's script unchanged (SHA-256 `3ea38284…be6b` verified):
  ```
  python3 ../../audit/inertdisc-replay/replay_inertdisc.py ../../studio-explore/sage-qa-runs/inertdisc-first-instance.json > inertdisc-replay-out.json
  ```
- Output: `pass: true`, radius 3, and the {11}-swap image is DL with radius 2. There are 2 shortest lock-1 paths, the lock-1 chain is not a tree, and {11} lies in D1 for path A and not for path B. Everything matches the audit's expectations.

**Independent replay.**
- Run `qall_scan.py --plantri LINE 1 --colouring JSON`, which writes `replay-20-51-1-local.json`.
- The state has dist 3. Lock 1 has exactly 2 SIMPLE paths, both shortest, and lock 2 has 1.
- {11} ({0,3}) is inside D1 for path A only. So it counts under Q∃ and not under Q∀.
- Intern A's Y = {9, 10} ({0,2}) is also a shortest-fill first move. 10 lies in K1, so it fails the chain-disjoint form.

**Scan.**
- Run `python3 qall_scan.py --orders 17 18 19 20 > qall-scan-17-20.jsonl` (9 s).
- What is scanned:
  - every degree-5 hole orbit (automorphism orbits from canonical BFS codes, both orientations);
  - every first move of a shortest filling sequence out of a DL state, where the component K contains no link vertex.
- Disc sides are computed geometrically from the rotation system, so chords are handled.
- The quantifiers:
  - **Qall** (coordinator): K is disjoint from K1 ∪ K2, and lies inside D_i(P) for EVERY simple lock-i path P (i = 1 or 2).
  - **QallA**: Intern A's cycle-6 form, "K disjoint from P and inside D_i(P) for every simple P". It does not require K to avoid the other chain.
  - **Qchain**: K is disjoint from K_i and lies in the component of T − v − K_i that holds the reference vertex.
  - **Qex / QexS**: K is disjoint from K1 ∪ K2, and lies inside the disc for SOME simple path / SOME shortest path.

| order | graphs | deg-5 hole orbits | DL states | moves checked | off-link | Qex | QexS | **Qall** | QallA | Qchain |
|---|---|---|---|---|---|---|---|---|---|---|
| 17 | 4 | 19 | 292 | 1368 | 278 | 0 | 0 | **0** | 15 | 13 |
| 18 | 12 | 53 | 473 | 2702 | 583 | 0 | 0 | **0** | 15 | 12 |
| 19 | 23 | 179 | 2093 | 12315 | 2816 | 0 | 0 | **0** | 122 | 80 |
| 20 | 73 | 622 | 11828 | 65179 | 15087 | 1 | 1 | **0** | 823 | 648 |

- The moves-checked total is 81,564, which equals the Studio's count exactly. The orbit counts match the kc table.
- The single Qex instance is the 20/51/1 graph and hole: gentri index 48, isomorphic, same hole orbit.
- **Under Qall, the count is 0 at orders 17–20, so there is no first instance.**
- Every QallA and Qchain hit touches the other lock's chain (otherwise it would be a Qall hit).
- QallA hits at state distance 3: 46 in all (24 with lock 1). An example is in `qallA-dist3-order17-example.json`: component {0, 1}, with 1 on the lock-2 path.
- Simple-path enumeration never hit its cap.

## 4. K3 depth (`4-k3-depth/`)
- Run with `python3 k3_depth.py > k3-depth-results.json`. Every sequence of length 1 to 3 is in `k3-depth-sequences-1to3.jsonl`.
- The state (order 26, plantri index 5401, hole 13) has Φ = (24, 10) and dist 5. The hole has 980 states.
- Every sequence of non-trivial swaps was enumerated:

| depth | sequences | lowering (first time) | filled ends | min lock_size at the end | end-Φ values |
|---|---|---|---|---|---|
| 1 | 6 | 0 | 0 | 24 | (24,14) ×2, (25,14) ×2, (25,16) ×2 |
| 2 | 28 | 0 | 0 | 24 | (24,10) ×12, (25,14), (25,16), (26,20), (27,24) ×4 each |
| 3 | 152 | 0 | 0 | 24 | (24,14) 40, (25,14) 32, (25,16) 40, (26,12) 16, (26,18) 8, (27,14) 16 |
| 4 | 808 | 80 | 0 | 8 | includes (8,0), (14,0), (16,7), (20,5), (21,12), (23,5) |

- Depth 1 matches Intern B's hand table exactly.
- **The least k is 4**, and k3.cpp (unchanged) agrees.
- One lowering sequence of 4 swaps, written as colour pair : component:
  1. {1,3} : {1, 7}, giving (25,14);
  2. {0,1} : {0, 4, 11, 20}, giving (26,20);
  3. {0,2} : {2, 8, 14, 19, 20, 22}, giving (25,16);
  4. {0,1} : {0, 2, 4, 9, 11, 17, 19, 25}, giving **(8,0)**, a state at dist 1.

## 5. Run 3: gluing the radius-5 certificates (`5-glue-radius5/`)
**Gluing.**
- The two certificates are glued as a connected sum along vertex links: delete w ∈ X and w′ ∈ Y of equal degree k, then identify the two link cycles in all 2k ways.
- w and w′ are at distance ≥ 2 from the certificate holes.
- Every glued graph is checked to be in the core class (E = 3n−6, #triangles = 2n−4, min degree 5). All 6,644 pass.

**Results.**
- **Extension test** (`glue.py --ext-cap 64`):
  - the certificate states of A = 91a307d1 h22 and B = 80b930d1 h23 are extended across the glued side, with up to 64 extensions each;
  - the exact radius of each state is computed with rball;
  - 334,074 states give radius histogram 1: 87,093, 2: 159,953, 3: 68,566, 4: 15,557, 5: 2,905. **The maximum is 5.**
- **Full enumeration with Errera** (`glue.py --full-errera`):
  - all 4,140 A+Errera and B+Errera gluings (37–42 vertices), with exact ρ over all states at the certificate hole;
  - ρ is 3, 4 or 5 (360 of them have ρ = 5);
  - κ = 1 everywhere, with no targetless class. **No ρ = 6.**
- **Full enumeration, A+B** (`glue.py --full-ab`):
  - the 658 (graph, hole) pairs of A+B gluings (52–53 vertices, up to 1.87M states) where an extension kept radius 5;
  - **ρ = 5 exactly in all 658**, with no targetless class.
  - The other A+B pairs were not fully enumerated, because of the CPU cap.

## 6. The 1/4 floor on the filled fraction of a Kempe class (`6-quarter-floor/`)
This item is exploratory and exhaustive over the stored gentri lists. Every hole of degree 5, 6 and 7 is scanned at orders 12, 14 and 16–24 (all vertices, not orbits). It used about 27 CPU-minutes, with at most 6 workers under nice 10.

**Definitions.**
- The filled fraction of a class C is #filled(C) / |C|, counting states up to renaming. Filled means the link uses at most 3 colours.
- The labelled ratio of a hole is #filled labelled colourings / #labelled colourings of T − v. Every state uses at least 3 colours, so each state stands for exactly 24 labelled colourings, and the ratio equals n_filled / n_states.
- P(T,4)/P(T − v,4) = states(T) / states(T − v).

**Commands.**
```
cd common && clang++ -O2 -std=c++17 -o krad krad.cpp && cd ../6-quarter-floor
python3 floor_scan.py --orders 12 14 16 17 18 19 20 --degrees 5 6 7 > holes-12-20.jsonl
python3 floor_scan.py --orders 21 22 --degrees 5 6 7 > holes-21-22.jsonl
python3 floor_scan.py --orders 23 24 --degrees 5 6 7 > holes-23-24.jsonl     # committed gzipped; gunzip -k before reuse
python3 aggregate.py holes-12-20.jsonl holes-21-22.jsonl holes-23-24.jsonl > summary.json
python3 quarter_struct.py --orders 12 14 16 17 18 19 20 --degrees 5 6 7 > raw-12-20.jsonl   # (6) raw labelled, all classes
python3 quarter_struct.py --quarter holes-12-20.jsonl holes-21-22.jsonl holes-23-24.jsonl > quarter-classes.jsonl  # (4)(6)(7)
python3 blocks.py > blocks-deg5.jsonl     # link-pattern blocks of the degree-5 1/4 classes
```

**Results.**

*Raw versus quotient (6).*
- The floor is not an artefact of counting up to renaming.
- For every class examined, the renaming stabiliser is all of S4. That covers all 2,274 classes at orders 12–20 (degrees 5, 6 and 7) and all 1,169 classes in the holes that contain a 1/4 class (orders 17–24).
- So each class lifts to ONE labelled Kempe class of 24|C| colourings, and its raw fraction equals its quotient fraction.
- An explicit labelled BFS, with no renaming at all, confirms size and #filled for every one of those classes, with 0 mismatches.
- Hand reason: swapping every {p,q}-component one after another applies the transposition (p q). So every transposition stabilises the labelled class, and the stabiliser is S4.

*Degree 5 (1).*
- 156,033 holes give 160,979 classes. The minimum fraction is **exactly 1/4**, and **no class falls below it**.
- 419 classes sit exactly at 1/4:
  - by order: 17: 2, 21: 2, 22: 11, 23: 129, 24: 275;
  - by size: 4: 319, 8: 22, 16: 9, 32: 1, 48: 4, 64: 10, 96: 25, 144: 8, 192: 18, 240: 2, 384: 1.
- Fractions in [1/4, 3/10]: 1/4 ×419, 16/59 ×4, 12/43 ×8, 11/39 ×1, 19/66 ×1, 9/31 ×6, 8/27 ×8. **Nothing lies strictly between 1/4 and 16/59 ≈ 0.271.**
- No class is targetless.

*Degrees 6 and 7 (2).* There is **no 1/4 floor**.
- Degree 6: 2/11 already at order 17 (10 classes below 1/4). Over orders 12–24 the minimum is **1/8**, at order 24 (gentri 71, hole 12, class 192 with 24 filled). 3,340 classes are below 1/4 and 197 are at exactly 1/4.
- Degree 7: 8/43 at order 17 and 1/6 at order 18. The minimum is **2/17**, at order 23 (gentri 189, hole 14, class 816 with 96 filled). 16,086 classes are below 1/4.

*Labelled ratio (3).*
- Degree 5: the minimum is **1/4** (order 17, gentri 1, hole 0, κ(T − v) = 1, class 64 with 16 filled). P(T,4)/P(T − v,4) equals n_filled / n_states at all 156,033 degree-5 holes, as unique extension predicts.
- Degree 6: the minimum labelled ratio and the minimum P(T)/P(T − v) are both 11/63 (order 23, gentri 153, hole 21).
- Degree 7: both minima are 49/414 (order 23, gentri 910, hole 11).

*Structure of the degree-5 1/4 classes (4).*
- **405 of the 419 classes split into 4 equal link-pattern blocks of size F = #filled:**
  - the filled block: every filled state has the same link pattern, with the singleton colour at one fixed position i;
  - three unfilled blocks, given by repeat pairs relative to i:
    - {i+1, i+3}: all non-DL;
    - {i+2, i+4}: all non-DL;
    - {i+1, i+4}, the two link neighbours of the singleton: all DL.
- Example (size 48, order 22, gentri 19, hole 12): filled ababc ×12; unfilled abacd ×12, abcad ×12, abcbd ×12.
- The other 14 classes are mixed blocks that still total 1/4: the two size-64 κ = 1 holes at order 17, plus sizes 96–384. In those, the filled states use several singleton positions, unevenly in 12 classes and evenly in 2.

*Bipartite filled–unfilled graph under single-link-vertex swaps (7).*
- At degree 5, every filled↔unfilled move has a component that meets the link in exactly one vertex.
- **The strict decomposition into 4-sets {1 filled + 3 unfilled neighbours} never exists** (0 of 658 classes at 1/4, all degrees). The reason: DL states have no filled neighbour by definition, and they make up exactly a quarter of each 4-block class.
- In 365 of the 405 4-block classes, the graph is a disjoint union of paths u–f–u′: each filled state has degree 2 (one neighbour in each non-DL block), each non-DL state has degree 1, and each DL state has degree 0.
- Examples:
  - size 4 (order 22, gentri 159, hole 19): the filled state has degree 2; the unfilled degrees are {0: 1, 1: 2}.
  - size 384 (order 24, gentri 160, hole 16): filled degrees {2: 20, 3: 60, 4: 16}; unfilled degrees {0: 112, 1: 84, 2: 76, 3: 16}.
  - size 192 (order 23, gentri 212, hole 16): filled degrees {2: 8, 3: 32, 4: 8}; unfilled degrees {0: 56, 1: 40, 2: 40, 3: 8}.

*Edge-deletion control (5).* All 17 new edge classes (102 states) have c(x) = c(y) in every state (asserted in item 2). So "filled = x, y differ" gives fraction **0**.

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

## 7. Link-position counts and the inequality behind the 1/4 floor (`7-offset-ineq/`)
This item is exploratory. It covers every degree-5 class at orders 12, 14 and 16–24: 160,979 classes in 156,033 holes. It used about 13 CPU-minutes.

**Counts per class** (link in rotation order):
- F_i = filled states whose singleton colour is at position i;
- U_j = unfilled states with c(x_j) = c(x_{j+2});
- D_j = the doubly-locked part of U_j.
- They come from `krad5.cpp`, which is `krad.cpp` plus these counts. Class sizes and #filled agree with item 6 at every hole.

**Commands.**
```
clang++ -O2 -std=c++17 -o krad5 krad5.cpp
python3 counts_scan.py --orders 12 14 16 17 18 19 20 21 22 > counts-12-22.jsonl
python3 counts_scan.py --orders 23 24 > counts-23-24.jsonl          # committed gzipped
python3 ineq.py counts-12-22.jsonl counts-23-24.jsonl > ineq-results.json
python3 inj.py --orders 12 14 16 17 18 19 20 21 > inj-12-21.jsonl
python3 inj.py --floor ../6-quarter-floor/blocks-deg5.jsonl > inj-floor.jsonl
```

**Families tested.** Every family U_j ≤ Σ_{a∈A} F_{j+a}, for every nonempty A ⊆ Z5, all j at once, offsets taken relative to j. The coordinator's F_i ≥ U_j is the case A = {i − j}. The same families were also tested with U_j replaced by U_j − D_j (non-DL) and by D_j (DL).

**Results.**
- **No single-term family F_i ≥ U_j holds.** Each of the 5 offsets fails in 149,706 to 158,818 classes.
- **No two-term family holds.** The best ones fail in 20,090 classes.
- **Exactly one family of size ≤ 3 holds in every class:**

  **U_j ≤ F_{j+1} + F_{j+3} + F_{j+4}**

  The three positions on the right are the link positions outside the repeat pair {j, j+2}. The family is mirror-symmetric (a ↦ 2 − a).
  - Equality occurs in 1,281 (class, j) cases with U_j > 0.
  - It is **tight for all j in exactly the 419 floor classes**.
  - Summed over j it gives ΣU ≤ 3ΣF, which is the 1/4 floor. Every other valid family contains one of size 4.
- **The non-DL part holds alone:** (U_j − D_j) ≤ F_{j+3} + F_{j+4} in every class. It has the most equality cases: 1,481, and it is tight for all j in 409 classes.
- **The DL part:** the minimal valid families are 6 three-term families, among them D_j ≤ F_{j+1} + F_{j+3} + F_{j+4}. No one- or two-term family holds.

**The injection behind the non-DL part (`inj.py`).**
- Setup: take an unfilled state s with repeat α at {j, j+2}, m = x_{j+1} (colour μ), a = x_{j+3} (colour A), b = x_{j+4} (colour B).
- If lock 1 fails, let φ(s) be the swap of the {μ,A}-component of a. The link becomes α μ α μ B, which is filled with the singleton at j+4.
- Otherwise lock 2 fails, and φ(s) is the swap of the {μ,B}-component of b. The image is filled with the singleton at j+3.
- **Computed:** the image is always filled, with the predicted singleton, in the same class, and φ is injective (0 collisions). This holds for:
  - all 353,812 non-DL unfilled states at every degree-5 hole of orders 12–21 (4,270 holes);
  - all 61,026 non-DL states in the 340 holes that contain a floor class.
- **Hand reason (unreviewed).** The swapped component K is still a whole {μ,A}-component after the swap. So s is recovered by swapping the {μ,A}-component of x_{j+3} in φ(s), and A is the one colour missing from φ(s)'s link.
- **The DL part needs ≥ 2 swaps,** since DL means no single swap fills.
  - In 417 of the 419 floor classes, every DL state fills in 2 swaps. The exceptions are the two order-17 classes of size 64, gentri 1, holes 0 and 2.
  - In 409 of the 419, the DL states reach at least as many distinct filled states in 2 swaps as there are DL states.
- **Three floor classes, in detail:**
  - size 4 (order 22, gentri 159, hole 19): F = 1, DL = 1, and the DL state fills in 2 swaps.
  - size 48 (order 22, gentri 19, hole 12): F = 12, DL = 12; the 12 DL states reach exactly the 12 filled states in 2 swaps.
  - size 192 (order 23, gentri 212, hole 16): F = 48, DL = 56 (a mixed-block class); they reach all 48 filled states.
  - In all three holes, φ is injective on every non-DL state.

## 8. Checks of MathQuarterFloorBijections.md: C1, C2, C3, C5, C7, global collisions, R_F/R_B (`8-quarter-identities/`)
This item is exploratory. It used about 22 CPU-minutes. Definitions are in the docstring of `qf.py`, following Math's §0–§5. All maps act on states up to renaming; each commutes with renaming.

**Coverage.** Every degree-5 hole at orders 12, 14 and 16–23 (45,904 classes), plus the 230 order-24 holes that contain a floor class (584 classes).

**Commands.**
```
python3 qf.py --orders 12 14 16 17 18 19 20 > qf-12-20.jsonl
python3 qf.py --orders 21 22 > qf-21-22.jsonl                 # committed gzipped
python3 qf.py --orders 23 > qf-23.jsonl                       # committed gzipped
python3 qf.py --floor-holes 24 > qf-24-floorholes.jsonl
python3 agg.py qf-12-20.jsonl qf-21-22.jsonl qf-23.jsonl qf-24-floorholes.jsonl > summary.json   # gunzip -k first
python3 qf.py --detail 17 1 0 > detail-17-1-0.jsonl
python3 internC_collision.py > internC-collision.json
```

**(0) Collisions of Lemma A's φ.**
- **Correction:** my item-7 count "0 collisions in 353,812" was keyed by (j, image). It was a per-j count, covering both cases, and **not** across j.
- Recounted across j at orders 12–21 (4,270 holes, 353,812 non-DL states):
  - **81,571 filled states have two φ-preimages, always with different j;**
  - 0 same-j collisions;
  - at most 2 preimages per filled state, as in Math's Remark 1.
- At orders 12–23 the cross-j total is 1,541,320.

**Intern C's construction is verified** (`internC-collision.json`):
- the graph is a triangulation (E = 45, 30 triangles = 30 faces), with degrees 5^12 6^5;
- it is isomorphic to gentri order 17, index 3;
- the colouring is proper, and s1 and s2 are proper and lie in t's class;
- s1 has j = 1 (lock 1 fails, Case 1) and s2 has j = 2 (lock 2 fails, Case 2), and φ sends both to t.

**C1. Identities.**
- **Class identity** 3F − U = 2N₀ + 1.5·L_F + Σ_P (1 − d(P)) − D_cyc: **0 mismatches** in all 46,488 classes.
- **Per-j identity** F_{j+1} + F_{j+3} + F_{j+4} − U_j = L_j + |U_j^ff| + |U_{j+3}^ff| + |E_j| − |DD_j|: **0 mismatches** in all 232,440 (class, j) cases.
- Every walk along Γ from a path start ends at a lock-1-only endpoint (0 bad paths).

**C2. Dichotomies.** 0 violations of any of the following:
- M3 and M2, each XOR its alternative condition;
- R+3 misses x_j ⇔ lock 2, and R+2 misses x_{j+2} ⇔ lock 1;
- R+3 lands in U_{j+3} with lock 1, and R+2 inverts it.

**C3. Where the compensation lives.**

d(P) histogram (paths):

| orders | 0 | 1 | 2 | 3 | 4 | 5 | 6+ | max |
|---|---|---|---|---|---|---|---|---|
| 12–20 | 9,847 | 15,964 | 1,566 | 640 | 305 | 204 | 72 | 15 |
| 21–22 | 144,518 | 247,174 | 22,502 | 10,795 | 4,031 | 2,984 | 984 | 17 |
| 23 | 519,725 | 852,423 | 87,548 | 41,291 | 15,344 | 8,425 | 2,007 | 31 |

- **D_cyc > 0 in 6 classes** (2 at orders ≤ 20, 3 at 21–22, 1 at 23), with D_cyc = 20 each time. None is a floor class.
- The largest DD_j is 8 at orders ≤ 20, 12 at 21–22 and 21 at 23. The largest DD_j ∩ DD′_j is 6, 12 and 17.
- **max over (class, j) of |DD_j| − room is 0**, so the room always suffices. This is the per-j form of the valid inequality of item 7.

**Floor classes (419 = 2 + 13 + 129 + 275):**
- **U_j = F_{j+1} + F_{j+3} + F_{j+4} with equality for every j in all 419.** That includes the order-17 class (Intern B's 10 cases).
- 405 classes have every term zero (N₀ = L_F = D_cyc = 0, all d(P) = 1).
- **All 14 non-block floor classes have F at more than one position i**, and every one has L_F = 0 and D_cyc = 0. They fall into three kinds:
  - 2 are unions of quartets, with every term zero: order 24, gentri 18 hole 14 and gentri 165 hole 14;
  - 2 are compensated by d = 0 paths against d = 2 paths, with N₀ = 0: order 24, gentri 830 hole 14 and gentri 1055 hole 14;
  - 10 are compensated by N₀ > 0 against long chains d ≥ 2: the two order-17 classes (N₀ = 6, d = 1 ×8, 5, 9); order 23, gentri 212 hole 16; and order 24, gentri 160/16, 165/16, 1055/16 and 1411 holes 13, 17, 20, 22.

**C5. ψ = φ_B⁻¹ R+3 R+3 φ_A on filled states with both bits short.**
- ψ is **not** the identity.
- In the floor classes it is defined on 2,295 states: it returns to f 931 times and reaches another filled state 1,364 times.
- In the size-48 class (order 22, gentri 19, hole 12) it is defined on all 12 filled states and returns to f in none.
- Over all classes at orders 12–23: defined 799,028 times, returning to f 298,285 times.

**C7. Distance from DL states to the nearest filled state.**

| orders | dist 2 | 3 | 4 | 5 |
|---|---|---|---|---|
| 12–20 | 23,249 | 509 | 44 | 0 |
| 21–22 | 356,824 | 5,883 | 226 | 1 |
| 23 | 1,254,513 | 13,533 | 430 | 1 |

- **Floor classes:** every DL state is at distance exactly 2 in 417 of the 419. The exceptions are order 17, gentri 1, holes 0 and 2.
- That class has 22 DL states (Intern B's request):
  - distances: 17 at 2, 3 at 3, 2 at 4;
  - R+3 d is DL for 12 of them, and R+2 d is DL for 12;
  - all five DL states at distance 3–4 have both R+3 d and R+2 d DL.
  - Per state, by (distance, R+3 DL, R+2 DL): (2,F,F) ×8, (2,T,T) ×5, (3,T,T) ×3, (2,T,F) ×2, (4,T,T) ×2, (2,F,T) ×2.
  - Per-j accounting: DD = [2, 2, 2, 3, 3], each equal to its room |U_j^ff| + |U_{j+3}^ff|.
- Full list: `detail-17-1-0.jsonl`.

**R_F = φ∘R+3 (Math's ρ) and R_B = φ∘R+2 on DL states (Intern A).**
- Each is injective per j (0 collisions), and each lands in F_{j+1} (0 bad images).

| orders | both defined, equal | both defined, differ | only R_F | only R_B (covers DD_j) | neither (DD ∩ DD′) | collisions of "R_F, else R_B" |
|---|---|---|---|---|---|---|
| 12–20 | 8,522 | 7,442 | 2,787 | 2,787 | 2,264 | 143 |
| 21–22 | 122,143 | 125,031 | 41,296 | 41,296 | 33,168 | 2,954 |
| 23 | 382,390 | 470,033 | 154,615 | 154,615 | 106,824 | 10,501 |

- So R_B covers part of DD_j, but the combined rule "R_F, else R_B" is not injective.
- **Size-48 class (order 22, gentri 19, hole 12):** R_F and R_B are both defined on all 12 DL states and **differ on all 12**. Each alone is a bijection onto the 12 filled states, and the combined rule has 0 collisions.

## 9. Locality of the DD_j room (`9-dd-locality/`), from Math's 1828 message, item 3
This item is exploratory. It used about 21 CPU-minutes.

**What is measured.**
- A DD state is a DL state whose R+3 image is also DL.
- For each DD state, measure the Kempe distance to the nearest compensating unit, using swaps of any kind within the class. A unit is any one of:
  - E: a Γ-path start with d = 0 (lock 1 fails, lock 2 holds, R+3 not DL);
  - U^ff: a state where both locks fail, i.e. N₀;
  - a filled state that carries a long M2 or M3 bit.
- The distance is a multi-source BFS in the class's move graph.
- The code is the `DDloc` block in `../8-quarter-identities/qf.py`. That block was added afterwards; nothing else in that file changed.

**Commands.**
```
cd ../8-quarter-identities
python3 qf.py --orders 12 14 16 17 18 19 20 21 22 > ../9-dd-locality/ddloc-12-22.jsonl   # committed gzipped
python3 qf.py --orders 23 > ../9-dd-locality/ddloc-23.jsonl                               # committed gzipped
cd ../9-dd-locality
python3 agg_dd.py ddloc-12-22.jsonl ddloc-23.jsonl > ddloc-summary.json
python3 a7_cycle.py 22 > a7-hole22.json
```

**Distance histogram by order** (DD states; every degree-5 hole at orders 12–23):

| order | classes with DD | 1 | 2 | 3 | 4 | 5 | max |
|---|---|---|---|---|---|---|---|
| 16 | 20 | 32 | 4 | 0 | 0 | 0 | 2 |
| 17 | 42 | 59 | 129 | 108 | 44 | 0 | 4 |
| 18 | 57 | 79 | 92 | 7 | 0 | 0 | 3 |
| 19 | 179 | 306 | 248 | 21 | 0 | 0 | 3 |
| 20 | 719 | 1,959 | 1,710 | 240 | 13 | 0 | 4 |
| 21 | 2,148 | 6,590 | 5,957 | 850 | 80 | 0 | 4 |
| 22 | 7,895 | 32,094 | 25,548 | 3,166 | 178 | 1 | 5 |
| 23 | 27,193 | 149,302 | 102,943 | 8,706 | 464 | 24 | 5 |

**By d(P).**
- The maximum distance is 4 or 5 for every d from 3 to 11, and at most 4 for d = 2, 8, 10, 12, 15, 28 and 31.
- For d = 13, 14, 16 and 17 it is at most 3.
- DL-cycle states (cyc) are at distance 1–3.
- **The distance does not grow with d(P).** The full table is in `ddloc-summary.json`.
- Every DD state reaches some unit. "Unreachable" counts are 0 except per kind: some classes have no E unit at all, but they always have U^ff or long-bit units.

**The 6 census classes with DL cycles (D_cyc = 20).** All have L_F > 0 and N₀ > 0. Room parts are summed over j; each U^ff state counts twice, once as U_j^ff and once as U_{j+3}^ff.

| class | size | F | U | N₀ | L_F | room L_j | room U^ff | room E | DD | room per j | max distance |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 17/3 h0, h16 | 100 | 40 | 60 | 10 | 40 | 60 | 20 | 0 | 4 per j | 16 per j | 2 |
| 22/417 h21 | 252 | 108 | 144 | 36 | 88 | 132 | 72 | 8 | 8,4,8,6,6 | 44,40,44,42,42 | 3 |
| 22/648 h0, h21 | 520 | 200 | 320 | 80 | 80 | 120 | 160 | 20 | 4 per j | 60 per j | 1 |
| 23/1108 h19 | 476 | 244 | 232 | 70 | 264 | 396 | 140 | 4 | 14,4,6,10,6 | 114,104,106,110,106 | 3 |

**Local intel's 800-cycle** (`best-A7_exc.json`, n = 37, hole 22, 25,326 states).
- My code reproduces Local intel's numbers: class 21,078 with F = 8,922, D_cyc = 840, DD = (690, 624, 726, 642, 648) and room = (3,612, 3,546, 3,648, 3,564, 3,570). The identities give 0 mismatches.
- Room parts, summed over j: L_j 12,834; U^ff 4,992 (N₀ = 2,496); E 114. Long bits (L_F = 8,556) supply about 72% of the room.
- d(P) reaches 81. **The maximum distance from a DD state to a unit is 3**, and DL-cycle states are at distance 1 or 2.
- The hole's two other cycle classes (size 2,124, D_cyc = 160 each) have maximum distance 2.

## 10. Is there a local injection of DD_j into room_j? (`10-local-injection/`)
This item is exploratory. It used about 22 CPU-minutes.

**What is tested.**
- For every degree-5 class with DD_j > 0, and each j, build a bipartite graph from the DD_j states to the units of room_j.
- The units, each with capacity 1, are exactly the terms of Math's per-j room:
  - F_{j+4} with M3 long;
  - F_{j+3} with M2 long;
  - F_{j+1} with M2 long;
  - U^ff_j and U^ff_{j+3};
  - E_j.
- A DD state is joined to a unit when their Kempe distance within the class is at most k.
- The maximum matching is computed for k = 1..8, by Kuhn's algorithm, augmented as k grows. k_min is the least k at which all of DD_j is matched.
- The unit counts equal room_j and the DD_j counts equal Math's DD_j in every case (0 mismatches against the `perj` field).
- The code is the `DDmatch` block of `../8-quarter-identities/qf.py`, enabled by `--match`.

**Commands.**
```
cd ../8-quarter-identities
python3 qf.py --orders 12 14 16 17 18 19 20 --match > ../10-local-injection/match-12-20.jsonl
python3 qf.py --orders 21 22 --match > ../10-local-injection/match-21-22.jsonl     # committed gzipped
python3 qf.py --orders 23 --match > ../10-local-injection/match-23.jsonl           # committed gzipped
cd ../9-dd-locality && python3 a7_cycle.py 22 > ../10-local-injection/a7-hole22-match.json
cd ../10-local-injection && python3 agg_match.py match-12-20.jsonl match-21-22.jsonl match-23.jsonl > match-summary.json
```

**k_min histogram over (class, j) with DD_j > 0:**

| order | pairs | 1 | 2 | 3 | 4 | 5 | 6 | max k_min |
|---|---|---|---|---|---|---|---|---|
| 16 | 36 | 32 | 4 | | | | | 2 |
| 17 | 158 | 16 | 42 | 48 | 32 | 20 | | 5 |
| 18 | 112 | 37 | 67 | 6 | 2 | | | 4 |
| 19 | 397 | 177 | 175 | 45 | | | | 3 |
| 20 | 2,158 | 757 | 992 | 354 | 50 | 5 | | 5 |
| 21 | 6,227 | 2,198 | 2,858 | 1,007 | 122 | 40 | 2 | 6 |
| 22 | 24,864 | 8,811 | 11,610 | 3,842 | 504 | 94 | 3 | 6 |
| 23 | 91,272 | 32,517 | 45,706 | 11,795 | 1,024 | 223 | 7 | 6 |

**Saturation.**
- **Every (class, j) saturates by k = 6.**
- The fraction saturated by k = 3 is 98.6% at order 23 (90,018 of 91,272).
- Witnesses with k_min = 6:
  - order 21: gentri 50, hole 11 (class 196, j = 0, DD_j = 2, room 14);
  - order 22: gentri 244, hole 17 (class 277, j = 2, DD_j = 3, room 34);
  - order 23: gentri 153, hole 18 (class 297, j = 0, DD_j = 5, room 16).
- In the tight cases (room_j = DD_j), k_min is at most 4: 10 at order 17, with k_min 3 or 4, and 4 at order 23, with k_min 1 or 2.

**Local intel's 800-cycle class** (A7, hole 22, size 21,078, DD_j up to 726, room about 3,600).
- **k_min = 2, 2, 3, 3, 2** for j = 0..4.
- The two size-2,124 cycle classes at that hole have k_min of 2 or 3.

## 11. Local-injection test at order 24 (`11-order24-injection/`)
This item is exploratory. It is the same test as §10, run on **all 111,492 degree-5 holes at order 24**: 362,572 (class, j) pairs with DD_j > 0. It used 82 CPU-minutes and 13.6 minutes of wall time, with 6 workers under nice 10.

**Commands.**
```
cd ../8-quarter-identities
python3 qf.py --orders 24 --match | gzip > ../11-order24-injection/match-24.jsonl.gz
cd ../11-order24-injection
python3 ../10-local-injection/agg_match.py match-24.jsonl.gz > match-24-summary.json
python3 check_k7.py > check-k7.json
```

**Results.**
- **k_min histogram:** 1: 116,109; 2: 181,204; 3: 58,272; 4: 5,801; 5: 1,164; 6: 21; **7: 1**.
- **The first case needing k = 7:** order 24, gentri 1460, hole 19.
  - The class has 544 states (F = 216, N₀ = 72, L_F = 128, D_cyc = 0).
  - At j = 4, DD_4 = 6 and room_4 = 70.
  - Two DD_4 states have a room_4 unit at distance 1. The other four have their nearest room_4 unit at distance **7**, although some unit of another j lies within 5.
  - An independent recomputation (`check_k7.py`, plain kempe_py, no qf code) gives the same nearest distances: [1, 1, 7, 7, 7, 7].
- **Tight cases** (room_j = DD_j): there are 26, and all have k_min ≤ 3.
- **Pairs needing k ≥ 6:** 22, listed in `kmin-ge6-24.json`.
- The identities give 0 mismatches at all 111,492 holes.
- `check-k7.json` contains two JSON documents: the qf view of the class, then the independent check.

## 12. Pooled (class-level) local injection (`12-pooled-injection/`)
This item is exploratory. It used about 38 CPU-minutes.

**What is tested.**
- Per class, ALL DD states (any j) are matched to ALL room units (any j) within Kempe distance k.
- A unit's capacity is the number of j whose room_j contains it, so the total capacity is Σ_j room_j. This is the class-level form, which is all the 1/4 floor needs.
- Capacity and DD totals agree with Math's per-j terms in every class.
- The matching is capacity-aware Kuhn, augmented as k grows. The code is the `DDpool` block of `../8-quarter-identities/qf.py` (`--pool`).

**Coverage.**
- Orders 16–23: all degree-5 holes.
- Order 24: 5,656 holes. These are every hole that has a class with per-j k_min ≥ 4, the 500 holes with the largest total DD, and gentri 1460 hole 19.
- Any pooling of the per-j matchings is itself a pooled matching, so pooled k_min ≤ the per-j maximum (confirmed in every class where both were computed). The order-24 counts for pooled k_min ≥ 4 are therefore exhaustive.

**Commands.**
```
cd ../8-quarter-identities
python3 qf.py --orders 16 17 18 19 20 --pool --match > ../12-pooled-injection/pool-16-20.jsonl
python3 qf.py --orders 21 22 --pool > ../12-pooled-injection/pool-21-22.jsonl                 # committed gzipped
python3 qf.py --orders 23 --pool | gzip > ../12-pooled-injection/pool-23.jsonl.gz
python3 qf.py --holes-file ../12-pooled-injection/holes24.txt --pool --match | gzip > ../12-pooled-injection/pool-24-subset.jsonl.gz
cd ../12-pooled-injection && python3 agg_pool.py pool-16-20.jsonl pool-21-22.jsonl.gz pool-23.jsonl.gz pool-24-subset.jsonl.gz > pool-summary.json
```

**Pooled k_min histogram (classes with DD > 0):**

| order | 1 | 2 | 3 | 4 | 5 | 6 | max pooled | max per-j (§10–11) |
|---|---|---|---|---|---|---|---|---|
| 16 | 16 | 4 | | | | | 2 | 2 |
| 17 | 1 | 17 | 2 | 22 | | | 4 | 5 |
| 18 | 9 | 43 | 5 | | | | 3 | 4 |
| 19 | 55 | 104 | 20 | | | | 3 | 3 |
| 20 | 131 | 424 | 155 | 9 | | | 4 | 5 |
| 21 | 441 | 1,292 | 365 | 48 | 2 | | 5 | 6 |
| 22 | 1,383 | 5,049 | 1,346 | 116 | 1 | | 5 | 6 |
| 23 | 3,845 | 18,982 | 4,096 | 260 | 10 | | 5 | 6 |
| 24 (subset) | 3* | 390* | 3,926* | 1,325 | 21 | 1 | 6 | 7 |

\* The order-24 counts at k_min 1–3 are partial, because only a subset of holes was scanned.

**Gentri 24 #1460, hole 19.**
- The whole class has DD = 44 and capacity 364.
- Pooled matching covers 22, 26, 28, 36, 40 and 44 DD states at k = 1..6, so **pooled k_min = 6**, against a per-j k_min of 7.
- It is the only order-24 class with pooled k_min = 6.

**Witnesses for pooled k_min = 5:**
- order 21: gentri 50, hole 11;
- order 22: gentri 307, hole 19;
- order 23: gentri 1186, hole 19.

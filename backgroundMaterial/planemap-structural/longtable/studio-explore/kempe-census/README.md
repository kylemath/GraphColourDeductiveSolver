# [exploratory] Kempe-radius census of min-degree-5 triangulations without separating triangles (Mac Studio)

## Method
- Graphs: plantri 5.8 (official tarball, sha256 e78a944116fec9f2c9f5e484206276cc2b0043bae803e9815f4b2683614629b8), `plantri -m5 -c4 N -a`. Check: `plantri -m5 17 -a` is byte-identical to longtable/wp20/input-m5-17.txt.
- Holes: the degree-5 vertices of each graph, grouped into orbits under the full automorphism group of the embedding (rotations and reflections). One hole per orbit; `orbit_size` and `n_aut` are recorded. Icosahedron check: 120 automorphisms, one orbit.
- Engine: Studio intel's `fast/kempe.cpp` (commit 85529ac, sha256 1a9770dadec064dd20df9c9f44d04ebfd863b549f6b862b270597557dbe995d0), compiled with `clang++ -O3 -march=native`.
  - It enumerates all proper 4-colourings of T - v. A state is "DL" when its link uses 4 colours and is doubly locked.
  - rho = 1 + the swap-distance from a DL state to the nearest non-DL state, maximised over DL states. rho = null would mean a DL state that can never leave DL, a targetless class, which would refute R* at that hole.
- Driver: `census.py`, run by `run_census.sh` with 8 workers at nice 10.
- Files:
  - `summary-N.json`: per-order histogram.
  - `rho-ge4-N.jsonl`: every hole class with rho >= 4, with the plantri graph line and the engine's witness state.
  - The full per-class files stay on the Studio (order 25 alone is 52 MB).

## Results, orders 12-25 (order 26 running, order 27 queued)
No order has a rho = null (targetless) class. The max-rho columns come from `analyse.py`, which uses its own diamond test.

| order | graphs | hole classes | rho=1 | rho=2 | rho=3 | rho=4 | rho=5 | rho=6 | rho=7 | null | max rho | max-rho holes in a diamond | max-rho graphs with a diamond |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 12 | 1 | 1 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| 13 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | - | - |
| 14 | 1 | 1 | 0 | 1 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | - | - |
| 15 | 1 | 2 | 2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | - | - |
| 16 | 3 | 5 | 1 | 4 | 0 | 0 | 0 | 0 | 0 | 0 | 2 | - | - |
| 17 | 4 | 19 | 0 | 9 | 3 | 7 | 0 | 0 | 0 | 0 | 4 | 4/7 | 7/7 |
| 18 | 12 | 53 | 3 | 46 | 4 | 0 | 0 | 0 | 0 | 0 | 3 | - | - |
| 19 | 23 | 179 | 4 | 155 | 20 | 0 | 0 | 0 | 0 | 0 | 3 | - | - |
| 20 | 73 | 622 | 1 | 467 | 150 | 4 | 0 | 0 | 0 | 0 | 4 | 4/4 | 4/4 |
| 21 | 191 | 2180 | 4 | 1708 | 438 | 30 | 0 | 0 | 0 | 0 | 4 | 13/30 | 27/30 |
| 22 | 649 | 7869 | 7 | 5969 | 1806 | 86 | 1 | 0 | 0 | 0 | 5 | 0/1 | 1/1 |
| 23 | 2054 | 28608 | 8 | 22233 | 6138 | 228 | 1 | 0 | 0 | 0 | 5 | 0/1 | 1/1 |
| 24 | 7209 | 104951 | 40 | 75841 | 27993 | 1071 | 6 | 0 | 0 | 0 | 5 | 3/6 | 6/6 |
| 25 | 24963 | 387665 | 106 | 269972 | 113764 | 3814 | 9 | 0 | 0 | 0 | 5 | 2/9 | 8/9 |

The table's diamond test (`analyse.py`, own code) and `rsst_check.py` (Studio intel's `rsst_contain.py`, commit 7f99280, unchanged, plus a hole-pinned copy of its search) agree on every rho-5 record.

## Birkhoff diamond (RSST 0.7322) and RSST 2.122 at the hole
- `rsst-rho4plus.jsonl`: every rho >= 4 record.
- `baseline-25.jsonl`: a random sample of 4000 order-25 records of all radii (seed 1), with graphs regenerated from plantri by index.

| order 25 | n | diamond at hole | 2.122 at hole | either at hole |
|---|---|---|---|---|
| rho 2 (sample) | 2756 | 63% | 62% | 94% |
| rho 3 (sample) | 1211 | 43% | 68% | 89% |
| rho 4 (all) | 3814 | 40% | 85% | 96% |
| rho 5 (all) | 9 | 2/9 | 5/9 | 7/9 |

Across orders 17-25, every rho >= 4 graph except a few contains a diamond somewhere, and almost every one contains 2.122. The hole lies in a diamond less often as rho grows.

## Graphs containing neither the diamond nor 2.122 (`neither.py`, `neither.jsonl`)
Graph-level containment was tested on every graph of each order (Studio intel's rsst_contain.py, commit 7f99280).

| order | graphs | graphs with neither | rho histogram over their hole classes | max rho |
|---|---|---|---|---|
| 12-21 | all | 0 | - | - |
| 22 | 649 | 1 | rho2: 1 | 2 |
| 23 | 2054 | 1 | rho2: 1 | 2 |
| 24 | 7209 | 4 | rho2: 11, rho3: 1 | 3 |
| 25 | 24963 | 2 | rho2: 6, rho3: 4 | 3 |

No graph with neither configuration has a rho >= 4 hole, up to order 25. Among the rho-5 classes, the one graph without a diamond (order 25, index 4830) contains 2.122. The one without 2.122 (order 24, index 7192) contains a diamond.

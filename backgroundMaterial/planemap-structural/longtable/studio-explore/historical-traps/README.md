# [exploratory] Run 6: the historical traps through the standard pipeline (Mac Studio)

- Edge lists come from Sage's `src/sage/graphs/generators/smallgraphs.py` (develop branch, sha256 9f9b34048e99ec9e85d3dffde4e76a6f7ea533c8c2f518efaa807363d0e4cdd9), parsed as data; Sage code was not executed.
- Faces are the non-separating triangles. The script checks that each graph is a triangulation (E = 3V - 6, F = 2V - 4, every edge in exactly 2 faces) and orients the faces consistently.
- At every degree-5 vertex v the pipeline runs:
  - `kmap`: kappa(T), kappa(T - v), new classes;
  - `kreach`: targetless classes, depth to a filled state;
  - Studio intel's `kempe.cpp` (85529ac): rho.
- Script: `traps.py`; per-graph JSON with oriented faces and per-hole records.

| graph | V | E | triangulation | min degree | separating triangles | core class | degree-5 holes | kappa(T) | kappa(T - v) | targetless | new classes | rho (count) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Errera (1921) | 17 | 45 | yes | 5 | 0 | **yes** | 12 | 1 | 1 at all 12 | 0 | 0 | 2 (10), 3 (2) |
| Kittell (1935) | 23 | 63 | yes | 5 | 0 | **yes** | 15 | 6 | 1 at all 15 | 0 | 0 | 2 (7), 3 (6), 4 (2) |
| Poussin | 15 | 39 | yes | **4** | 0 | no (min degree 4) | 8 | 3 | 1 at all 8 | 0 | 0 | 1 (1), 2 (7) |

`kreach` depth equals `kempe.cpp` rho at every hole. Errera's graph has twelve vertices of degree 5 and five of degree 6, so it is an order-17 fullerene dual and lies in the plantri -m5 -c4 census at order 17.

Not yet run: Heawood's 1890 map (25 vertices, 69 edges). No machine-readable source has been found yet: Sage's `HeawoodGraph` is the 14-vertex cage, and MathWorld's page gives no data.

## HoG 1152 (Saaty-type Kempe counterexample), added
- Input: Long Table's `longtable/historical-traps/hog1152-heawood-four-color-graph.json` (main 2e709d8). House of Graphs 1152, probably Saaty's 1972 25-vertex version. It is NOT Heawood's 1890 map: degrees 5x17, 6x3, 7x5, where the 1890 map has 5x16, 6x5, 7x4.
- Independent re-check here: 25 vertices, 69 edges, 46 faces, consistently oriented, 0 separating triangles, min degree 5. **Core class.**
- Pipeline at all 17 degree-5 holes (`HoG1152.json`):
  - **kappa(T) = 37**, and **kappa(T - v) = 3 at 16 holes and 4 at 1**, so every hole is multi-class.
  - 0 new classes and 0 targetless classes, so **R\* holds at all 17 holes**.
  - rho = 2 at every hole; kreach depth equals rho.
- This is the first historical trap where the test is informative (T - v has more than one class), and it passes.

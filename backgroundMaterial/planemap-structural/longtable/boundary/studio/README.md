# Boundary solvability at scale (Studio Job 7, 14 Oct 2026) [exploratory, data]

## Statement under test

Plan item A2. At a degree-5 hole h, every unfilled state of T − h can reach a filled state using only Kempe swaps
whose chain meets a chosen far region R. Webs are excluded, as in HoleGame.

## Engines

- **`bnd.cpp` (C++).** The same game as `~/4square/kempe_engine.HoleGame`. Restricted moves are swaps whose chain
  meets R. Moves are involutions, so the restricted distance dR is a BFS from the filled states.
  - Regions per hole (d = BFS distance from h; a face's distance is the minimum over its vertices):
    - `faceMax`: each face at maximal face distance, separately;
    - `face3`: each other face at distance ≥ 3, separately;
    - `shell1` = {d = dmax}; `shell2` = {d ≥ dmax − 1}; `dist3` = {d ≥ 3};
    - with `--distscan`, `ge<r>_<|R|>` = {d ≥ r} for every r.
  - Per kind: [regions, failing regions, worst number of failing states, max dR, max extra par dR − dF].
  - `faceMaxRim` (Long Table's leverage question): [states with dR > 0, dR-lowering R-moves, of them meeting the link,
    states whose every lowering R-move misses the link, all R-moves from unfilled states, of them meeting the link],
    summed over faceMax regions.
- **`ref_check.py`.** The Python reference: HoleGame plus the `ring_levels.py` logic with the same regions. It agrees
  with `bnd` on every field at all 790 holes of orders 22–27 plus 10 order-28 graphs, and on `faceMaxRim` at 177 holes.
- **`local_check.py`.** A third, local engine: no global enumeration and no shared code. From a witness state it
  computes the R-restricted closure and the unrestricted distance to a fill.

## 1. Census, frame class, orders 22–33 (1,337,323 holes; `out/census_summary.txt`, `out/census-failing-holes.jsonl.gz`, `out/census-fail-examples.jsonl.gz`)

| R | holes with a failing region | max failing states | max extra par (solvable) |
|---|---|---|---|
| faceMax | **67,882** (from order 25; 5.4% at order 33) | 288 | 17 |
| face3 | 140,399 / 1,314,441 | 348 | 16 |
| shell1 | 402,705 | 4,495 | 105 |
| shell2 | **776** (from order 30) | 40 | 8 |
| dist3 | **0** | – | 5 |

- Every unfilled state reaches a fill without restriction.
- **dist3 region size:** |R|/n at the minimum is 0.32–0.39 per order, and the mean rises from 0.36 to 0.53
  (`out/census_dist3_ratio.txt`).
- **Rim statistic (faceMax):**
  - 77.6% of dR-lowering R-moves also meet the link;
  - 11.5% of (state, face) pairs with dR > 0 have no rim-touching lowering move;
  - 61.9% of all R-moves from unfilled states meet the link.

**Counterexamples.** Each is confirmed by `bnd`, HoleGame and `local_check.py`.
- **Far face.** p25#2111 h1, R = face {12, 21, 22}, state `0.12123132030302101213123`: dF = 2, R-closure of 12 states,
  none filled. Independently confirmed on the MacBook.
- **Outer two shells.** p30.r29#66366 h18, R = {4, 12, 13, 22, 23, 24, 25}, state `213010202012123031.32320131210`:
  dF = 2, R-closure of 4 states.

## 2. Far-threshold scan (`--distscan`; `out/farscan_summary.txt`, `out/extra_summary.txt`)

Here rmax is the largest r with {d ≥ r} solving every unfilled state. Solvability was monotone in r at every hole.

| family | holes (skipped: > 1M states) | n | dmax | dmax − rmax distribution | min |R|/n solving | far face fails | shell2 fails | dist3 fails |
|---|---|---|---|---|---|---|---|---|---|
| fullerene duals C20–C46 (all) | 4,104 | 12–25 | 3–5 | 0, 1 only | 0.040 | 32 | 0 | 0 |
| Goldberg C20, C60, C80 | 36 (48 > 64 vertices) | 12–42 | 3–6 | 0, 1 | 0.083 | 0 | 0 | 0 |
| IPR duals | 4,125 (11,079) | 32–50 | 5–6 | 0: 1,517, 1: 2,607, **2: 1** | 0.041 | 521 | 1 | 0 |
| Job 2 glued (300 sampled graphs; all aimpos holes skipped) | 4,220 (3,617) | 42–52 | 4–7 | 0: 2,173, 1: 1,920, 2: 116, **3: 10, 4: 1** | 0.040 | 1,706 | 127 | 0 |

Witnesses (`local_check.py` confirms both):
- **IPR.** ipr#243 h20 (n = 49, dmax 6). {d ≥ 5} (9 vertices) fails 4 states; {d ≥ 4} (20 vertices) solves.
  State `31012102031203130231.2032102131203210313210313202`: dF = 2, R-closure of 4 states.
- **Glued.** gglue4_1754 = `p26#78654@21-22+p26#5298@9-10/q0`, a separating 4-cycle gluing, h44 (n = 48, dmax 7).
  {d ≥ 4} (25 of 48 vertices) fails 24 states; only {d ≥ 3} (32 vertices) solves.
  State `21310303202031213213200301023123032031202312.031`: dF = 1, R-closure of 6 states, none filled.

## Reading

- **Strong forms are false.** The single far face and the outer two shells both fail on census frame graphs.
- **Far-field form, internally 6-connected maps.** On census, fullerene and IPR maps, a region of the last one or two
  shells solves every hole (once more on IPR), sometimes with as little as 4% of the vertices.
- **Far-field form, glued maps.** On maps with separating 4- and 5-cycles (Job 2) it fails: the solving region must
  start up to 4 shells inside the far end, and at gglue4_1754 h44 even the far half of the map is not enough.
- **Only dist3 survives everywhere** (0 failures in 1.35M holes). At these sizes it is a third to two thirds of the
  map, so it is not a far-field statement.
- **Rim.** About 12% of restricted shortest-path states need a far-only chain, so the outer chains are not just "the
  giant chains that also reach the hole".

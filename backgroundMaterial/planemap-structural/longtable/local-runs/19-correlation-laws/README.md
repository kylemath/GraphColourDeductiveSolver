# [exploratory] Item 19: correlation laws (U <= sum of F) at degrees 5, 6, 7

Exploratory computation, not a proof. MacBook, AC power, 3 workers, `nice -n 10`, every job under 2 minutes of wall time, nothing left running, no downloads.

## Definitions
- Link word: the colour sequence c(x_0)..c(x_{d-1}) of a state at a degree-d hole, in rotation order, relabelled by first occurrence. There are 10, 31 and 91 such words at d = 5, 6, 7, and 5/11/21 of them are filled (at most 3 colours).
- A class vector counts, for every link word, the states of the class with that word. Position = the dihedral image of a word (rotation of x_0, mirror image). Class data are closed under the dihedral group (a mirrored or relabelled hole is a hole of another triangulation), so a family only has to be tested at one representative unfilled word per orbit.
- Family: `U(u) <= sum_{t in S} F(t)` with u an unfilled word and S a set of filled words, all conjugates by D_d included. A family is valid when it holds in every class of the data. Minimal = no proper subset of S is valid.
- At d = 5 the words are exactly U_j (repeat at {j, j+2}) and F_i (singleton at i).

## Files
- `kpat.cpp` (build: `clang++ -O2 -std=c++17 -o kpat kpat.cpp`) and `scan.py`: the common/krad.cpp enumeration and Kempe moves, extended to print per class the count of states per link word, for every hole of degree 5, 6, 7. `common/kempe_py.py` supplies `gentri_rotation`. `scan.py --orders 12 14 ...` was run for orders 12-24. Check: the d = 5 counts reproduce `7-offset-ineq/counts-12-22.jsonl` exactly for all 13712 holes.
- `patterns-12-17.jsonl`, `patterns-18-20.jsonl`: raw per-hole, per-class link-word counts. Orders 21-24 (80 MB) are not committed; regenerate with `python3 scan.py --orders 21 22 23 24` (70 s on 3 cores).
- `lib.py`, `build.py` (dedupes class vectors, observed floors), `laws.py` + `minsets.cpp` (all minimal valid S up to size 5/8/8 at d = 5/6/7, every unfilled orbit), `simplex.py` + `lp.py` (exact rational LP), `swaps.py`, `pattern.py`, `pattern2.py` (swap neighbourhoods).
- Results: `laws-12-24.json` (the minimal families), `lp-*.json`, `pattern-12-24.json`, `pattern2-12-24.json`, `classes-*-12-20.json`, logs. The big derived files for other order ranges are regenerable (`build.py`, then `laws.py TAG`, `lp.py TAG`).

## Findings (orders 12-24, 150340 / 58204 / 19385 distinct class vectors at d = 5 / 6 / 7)
Observed floors reproduced: 1/4, 1/8 (order 24, gentri 71, hole 12), 2/17 (order 23, gentri 189, hole 14). At orders 12-20 only the floors are 1/4, 2/11, 9/74.

1. Degree 5: exactly one valid family, U_j <= F_{j+1} + F_{j+3} + F_{j+4} (the known one; no other subset of any size is valid).
2. Degree 6: five unfilled orbits (words 010123, 010203, 010213, 010232, 012013). Each has a valid family; the smallest S has size 5 (of 11 filled words), with 21, 6, 4, 20, 4 minimal sets of size at most 8 (see `laws-12-24.json`).
3. Degree 7: seven unfilled orbits. Smallest S has size 5 or 6 (of 21 filled words); there are hundreds to thousands of minimal sets of size at most 8, so the minimal family is not pinned down.
4. The families are not saturated: the smallest valid S grows as larger orders are added (d = 6: 4, 4, 5, 5 for orders up to 20, 22, 23, 24; d = 7: 4, 5, 5, 5-6). At 12-20 the d = 6, 7 data are too small to say anything. A cap of 8 on the search size was used at d = 6, 7 (it never bound at d = 6).
5. LP (maximise U/F, implied floor 1/(1+U/F)): d = 5 gives exactly 1/4. d = 6 gives 1/12 at orders up to 24 (1/8 observed); d = 7 gives 4/85 (2/17 observed). The implied floors fall as data are added (d = 6: 9/89, 17/180, 1/12 for orders up to 22, 23, 24; d = 7: 3/52, 4/77, 4/85), so the single-U 0/1 families do NOT explain the floors at d = 6, 7. The LP optima put all the filled mass on one or a few words (d = 6: ABCABC), which no real class does, so joint (multi-U or weighted) laws are needed there.
6. Swap pattern (`pattern*.json`; abstract swap = flip p<->q on a union of link arcs alternating p,q, a superset of what a real state can do): the smallest valid S always contains every filled word one swap away from u (all one-swap neighbours N1, 1-3 words at d = 6, 1-2 at d = 7, 2 at d = 5), plus extra words. Number of extras |S| - |N1|: d = 5: 1; d = 6: 2-4; d = 7: 3-5. The extras are mostly at abstract swap distance 2 (sometimes 3). So the degree-5 rule "N1 plus one more" does not carry over literally: the extra count grows with d. At d = 5 the extra is F_{j+1}, the singleton on the vertex between the repeated pair, two swaps from u.

Caveat: validity is relative to orders 12-24 only; larger orders may kill more d = 6, 7 families (the trend above says they will).

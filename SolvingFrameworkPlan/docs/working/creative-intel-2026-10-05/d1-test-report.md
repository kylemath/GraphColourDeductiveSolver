# D1-test report (Long Table, 2026-10-05) — EXPLORATORY, post hoc

All numbers below are finite computer data from unreviewed scripts. SEP and D1 are conjectures; nothing here proves them.

## Results

SEP-bad state = unfilled state with no separable admitting legal fan. Max depth is the separation depth (pure Kempe swaps, hole fixed) of SEP-bad states; "-" means no bad state. "Graphs" counts all plantri graphs; deg-5 vertices are only in graphs that have one.

| family | order | graphs | deg-5 vertices | states | SEP-bad | max depth | source |
|---|---|---|---|---|---|---|---|
| c4m4 | 12 | 80 (87 listed incl. no deg-5) | 322 | 4185 | 0 | - | prior |
| c4m4 | 13 | 301 of 313 with deg-5 vertex | 1199 | 22491 | 0 | - | prior |
| c4m4 | 14 | 1323 of 1357 | 5506 | 145337 | 0 | - | prior |
| c4m4 | **15** | 6244 (6161 with a deg-5 vertex) | 26654 | 983192 | 0 | - | this run (all graphs) |
| c4m4 | **16** | 30926 (30672 with deg-5 vertex) | 138627 | 7072063 | 0 | - | this run (all graphs, no subsample) |
| m5 | 12/14/15 | 1/1/1 | 12/12/12 | 120/240/192 | 0 | - | prior |
| m5 | 16 | 3 | 38 | 1116 | 0 | - (depth rerun: none) | prior SEP; depth rerun now |
| m5 | 17 | 4 | 49 | 2146 | 8 (graphs 17:0 and 17:1, 4 each) | 1 | prior SEP; depth rerun now |
| m5 | 18 | 12 | 156 | 7900 | 0 | - (depth rerun: none) | prior SEP; depth rerun now |

Order 15 took about 1 minute wall time, order 16 about 12 minutes (with other jobs sharing the machine), so no subsample was needed.
Prior rows are taken from the existing `sep-c4-12..14.json` and `sep-m5-*.json`; I did not re-run them.
(Order 12 shows "87 listed" only in my diamond split; the 80 is graphs with a deg-5 vertex among the 87. Same reading for 13, 14.)

### Task 2a: Birkhoff diamond split of the c4m4 family (`d1_diamond.py`)

Diamond: degree-5 a,b,c,d, b~d, a and c both adjacent to b and d, a not adjacent to c.

| order | diamond graphs | diamond deg-5 v | diamond states | diamond bad | no-diamond graphs | no-diamond deg-5 v | no-diamond states | no-diamond bad |
|---|---|---|---|---|---|---|---|---|
| 12 | 13 | 83 | 1062 | 0 | 74 | 239 | 3123 | 0 |
| 13 | 38 | 233 | 4311 | 0 | 275 | 966 | 18180 | 0 |
| 14 | 153 | 984 | 25146 | 0 | 1204 | 4522 | 120191 | 0 |
| 15 | 650 | 4306 | 152131 | 0 | 5594 | 22348 | 831061 | 0 |
| 16 | 3065 | 20961 | 1015248 | 0 | 27861 | 117666 | 6056815 | 0 |

No SEP failure in either part, so there is nothing to compare for depth. The two classes behave the same in this data (both 0 bad).

### Task 2b: flips of 17:0 and 17:1 (`d1_flips.py`)

Only edges whose two ends both have degree at least 6 can be flipped without dropping below minimum degree 5; the flip also needs the new chord to be absent. From the four `-m5 17` graphs (degree-5 counts 12, 12, 13, 12) there are 12 such flips; every one is 4-connected (no separating triangle) and min degree 5. Each result was matched, by a canonical rotation-system code (both orientations), to a graph in the `plantri -m5 17` list, so each is legal and none is new:
- 17:0 flips only to 17:1 (2 flips); 17:1 flips to 17:0 (2 flips) and to 17:3 (1 flip).
- 17:2 flips only to itself (2 flips); 17:3 flips only to 17:1 (5 flips).
- SEP per graph (deg-5 vertices, states, bad): 17:0 (12, 496, 4); 17:1 (12, 522, 4); 17:2 (13, 608, 0); 17:3 (12, 520, 0).

Conclusion on this data: no new locked or SEP-failing graph appears among these neighbours. This is a weak statement, since the flip neighbourhood stays inside a 4-graph list by construction.

### Task 3

No state with separation depth 2 or more was found. D1 survives all runs here. No counterexample file was written. D1 itself was not specifically computed for c4m4 15/16 beyond SEP (there was nothing to extend, since SEP held everywhere).

## Commands (run in `backgroundMaterial/planemap-structural/longtable/explore-vhphi/`, P = plantri 5.8 path)

```
$P -c4m4 15 -a | python3 sep_any.py 15 sep-c4-15.json 13        # log run-d1-c4-15.log
$P -c4m4 16 -a | python3 sep_any.py 16 sep-c4-16.json 13        # log run-d1-c4-16.log
python3 d1_diamond.py $P d1-diamond-split.json 12 13 14 15 16   # log run-d1-diamond.log
python3 d1_flips.py $P d1-flips-m5-17.json                      # log run-d1-flips.log
python3 sep_depth.py $P 16 "-m5"  > run-d1-depth-m5-16.log
python3 sep_depth.py $P 18 "-m5"  > run-d1-depth-m5-18.log
python3 sep_depth.py $P 17 "-m5"  > run-d1-depth-m5-17.log
```
P = /private/tmp/claude-501/-Users-fulkanjou-GraphColour/28402cc5-3e09-4c31-94e9-5ae923a5533c/scratchpad/plantri58/plantri

## SHA-256 (shasum -a 256, no git)

```
b90ed43a2cb847b65452bafaccacbd3fbfc5387da22ba16eac6b464920423354  sep-c4-15.json
805ec8f55398e07247883cc7a4ec1b4b2d468801e295fad74567878244a3507d  sep-c4-16.json
3e404d80c92e67391d0d134d371455e50c44b78ba286e8708eef770887d0c5e0  d1-diamond-split.json
ce03ce09050079c5996528f9664241a7287514c9fc19205a518fb66d196e482e  d1-flips-m5-17.json
896ad0fbf8949798c82a867653160428180b485b19a75b5609b5b9e1d85b48be  run-d1-c4-15.log
babdb2a9f4e8ffa7d00841711a16164765a24c0751d25aae9b07c7c0874c9291  run-d1-c4-16.log
fd4a55a5219434c57c25ec556b25d2f78d32e689d878fd2a43824b89e05d4f2d  run-d1-depth-m5-16.log
1dbbee44060fabda7c431fd0b10801bd5b24a8ea235717713852b2291686bc70  run-d1-depth-m5-17.log
e4d60b34fe28f3a736dd828cf9efd331c00c6a9e3d32c66342e0bd02b76f7248  run-d1-depth-m5-18.log
dd95295c1f2e03fffdd6e9d08868eb0370659af8265b1014fc49efdd30fdf40a  run-d1-diamond.log
2c860e52b89d01c6962c250d1e59d85d5a04ac6adfcb1ddb6f1ed4e95bd9ce75  run-d1-flips.log
a8f5e1f155f59141573f5bbf491aac1820a8329982ac73a358c7d8524b7737e9  d1_diamond.py
912f4daeaf231fe5457d89160fd5cbc320e3d9a0e07bf5f13243382023e02061  d1_flips.py
```

## What was NOT tested

- Any triangulation of order above 18 (19-24 are spent holdouts); c4m4 orders 17 and 18 were not re-run here (earlier files exist but are not part of this report).
- Min-degree-4 triangulations that are not 4-connected, and graphs with separating triangles or degree-3 vertices.
- SEP-bad state depth for c4m4 15/16 (no bad states, so none needed); depth was run only on the `-m5` families 16-18.
- Flip neighbours with min degree 4 or 3, flips of the order-18 `-m5` graphs, and multi-step flip paths; flips of 17:0/17:1 were checked only one step deep.
- Diamond subset comparison for depth (no failures, so nothing to compare); diamonds at orders 17-18.
- Fans that are not legal, and filled states (SEP covers unfilled states only); Kempe-chain "separability" is exactly the sep_any.py definition and was not independently re-implemented. The separate independent-verification script of task 3 was not needed and not written.
- The new d1_*.py scripts and `canon_code` in d1_flips.py were checked only by internal asserts (triangulation edge/face counts, orientation, match to plantri list), not by a second implementation.

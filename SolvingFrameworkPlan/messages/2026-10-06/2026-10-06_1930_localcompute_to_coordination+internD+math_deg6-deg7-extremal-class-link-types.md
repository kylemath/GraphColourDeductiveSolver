# [exploratory] Intern D's requests: the degree-6 class at 1/8 has no ABABAB and no (2,2,2) filled states (all 24 are (3,2,1)); its rotation graph has 6 components of 28 nodes and is not a tree; at degree 7 the rotation graph is one 720-node component

- **From:** Studio compute (local), on the MacBook
- **To:** coordination session; Intern D; Math
- **Sent:** 2026-10-06 19:30 MDT
- **Replies to:** `interns-2026-10-06/intern-D-cycle6.md`, "Studio requests" (10d5c01), as relayed by the coordinator
- **Asks for:** nothing

Everything below is exploratory computation, with nothing proved. The data are in `backgroundMaterial/planemap-structural/longtable/local-runs/13-deg67-extremal/`, with README §13. Intern D's colouring counts on C6 are reproduced exactly: 12, 144, 96, 144, 72, 144, 72 and 48.

## Degree 6: order 24, gentri 71, hole 12 (class 192, 24 filled)
- **No ABABAB, and no (2,2,2) filled states.** All 24 filled states are (3,2,1).
- Unfilled states (fill moves = distinct filled neighbours; rotation degree = neighbours along pattern-changing swaps between unfilled states):

  | type | count | fill moves | rotation degree |
  |---|---|---|---|
  | T1 | 48 | 1 | 3 |
  | T2 | 48 | 0 | 3 |
  | T4 | 24 | 1 | 3 |
  | T5 | 24 | 0 | 3 |
  | (3,1,1,1) | 24 | 2 | 2 |

- **The rotation graph** has 6 components of 28 nodes each. Each component has 24 nodes of degree 3, 4 of degree 2, and 40 edges, so it is **not a tree** (cycle rank 13). 16 nodes per component carry a fill move.
- So U/F = 7 comes from cyclic degree-3 structure. It does not come from ABABAB states or from 5-ary nodes of degree above 3.

## Degree 7: order 23, gentri 189, hole 14 (class 816, 96 filled)
- Filled states: tait (3,3,1) with counts (3,2,2): 84; tait (5,1,1) with counts (3,3,1): 12.
- Unfilled states:
  - (3,3,1)/(2,2,2,1): 420;
  - (3,3,1)/(3,2,1,1): 264;
  - (5,1,1)/(3,2,1,1): 24;
  - (5,1,1)/(2,2,2,1): 12.
- **The rotation graph** is one component of 720 nodes, with degrees 3–7. 396 nodes carry a fill move.

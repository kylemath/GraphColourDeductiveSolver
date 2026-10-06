# Kill test of Theorem R5³ (three consecutive degree-5 neighbours): 0 violations on 6,256 holes and 264,947 doubly locked states

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Navigator; Math; Audit
- **Sent:** 2026-10-06 15:21 MDT
- **Replies to:** the coordinator's kill-test request for `MathRstar55566.md` (940336c); the Navigator's request for a citable file
- **Asks for:** nothing

**Label: [computed, exploratory].** Code commit `c5d0954` on `studio-intel`: `backgroundMaterial/planemap-structural/studiointel/r55566_test.py` (written from the theorem's statement only); `r55566_violations.json` (empty list); graphs in `gentri/`.

**Statement tested** (MathRstar55566.md item 1):
- T has no separating triangle.
- v has degree 5, with link y₀..y₄ in rotation order, where y₀, y₁, y₂ have degree 5.
- Claim: every doubly locked state has radius ≤ 7, and ≤ 6 when the repeat pair is {y₃,y₀} or {y₂,y₄}.
- Every frame is tested: each run of three consecutive 5s, in both rotation senses.

**Method:** the exact radius of every doubly locked state, by BFS over whole-component swaps of T − v (same definitions as `radius.py`).

**Graphs:**
- T4, the order-28 (6⁵) graph, the Phase B best graphs B2 and B3, and the 100 radius-5 certificate graphs from Phases C, D and E6;
- **every** 4-connected minimum-degree-5 triangulation of orders 12, 14 and 16–22, from Math's `MathRadiusCensus/gen_tri.cpp` (sha256 in `gentri/SOURCE.txt`). Counts: 1, 1, 3, 4, 12, 23, 73, 191, 649.

**Result:**
- 6,256 holes tested, 264,947 doubly locked states, **0 violations**.
- No targetless class.
- Not tested: the proof-internal confinement assertions (spec item (c)).

**Maximum radius by link-degree class** (sorted multiset of the five link degrees):

| Class | Max radius | Class | Max radius |
|---|---|---|---|
| (5,5,5,5,5) | 3 | (5,5,5,6,6) | 5 |
| (5,5,5,5,6) | 5 | (5,5,5,6,7) | 5 |
| (5,5,5,5,7) | 5 | (5,5,5,6,8) | 5 |
| (5,5,5,5,8) | 5 | (5,5,5,6,9) | 2 |
| (5,5,5,5,9) | 3 | (5,5,5,7,7) | 4 |
| (5,5,5,5,10) | 2 | (5,5,5,7,8) | 5 |
| | | (5,5,5,7,9) | 2 |
| | | (5,5,5,8,8) | 2 |

Radius 5 is the largest seen in any class. The bound 7 is never reached, and neither is 6.

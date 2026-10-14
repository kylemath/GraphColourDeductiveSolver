# Boundary solvability: Kempe's problem from the outside (exploratory)

Long Table, 13 Oct 2026. This is plan item A2 (CoordinatorPlan, "Overall plan to the deadline").

**Statement under test.** At a degree-5 hole of a planar triangulation, take any unfilled state. A fill can be
reached using only Kempe chains that meet a chosen far region R, where R is:
- the 3 outer-face tiles;
- the outermost one or two BFS shells from the hole; or
- all tiles at distance ≥ 3.

Webs (the only chain of its colour pair) are excluded, as in the game engine.

**Data so far** (`ring_levels.py` on the 36 non-onboarding 4square levels, 31 maps; `levels-ring.jsonl`).
Each table cell gives: restricted distance from the level start (X = unreachable) / |R| / the fraction of all
unfilled states that can still reach a fill.

| R | levels solvable from their start | par vs unrestricted | every unfilled state solvable on every map? |
|---|---|---|---|
| outer face ("border3", 3 tiles) | 36/36 | equal on 35; 7.3 quiet-way-out 2 → 3 | yes |
| outermost two shells | 36/36 | equal on 35; kempes-double same | yes |
| distance ≥ 3 | 34/36 | equal | mostly |
| farthest shell only | 28/36 | sometimes +1 | no (fails when the shell is a single tile) |

**Why it is plausible.**
- The 3 outer-face tiles use 3 different colours, so every colour pair has a chain through the outer face.
- Swapping a pocket chain (one that misses R) is the same, up to renaming, as swapping all the other chains of
  that pair at once. That is not one move, so the statement is not trivial.

**Next (Studio).** Test every census hole at orders 22–33, and glued and fullerene graphs. Any counterexample kills
the statement (falsification-first rule).

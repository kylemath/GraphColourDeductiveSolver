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
| outer face ("border3", 3 tiles) | 36/36 | equal on 33; +1 on 0.3 archipelago (1 → 2), 2 open-doors (1 → 2), 7.3 quiet-way-out (2 → 3) | yes |
| outermost two shells | 36/36 | equal on 34; +1 on 0.3 and 2 | yes |
| distance ≥ 3 | 34/36 (unsolvable from start: 0.1, 0.2) | equal on 32; +1 on 0.3 and 2 | mostly |
| farthest shell only | 28/36 | equal on 23; +1 on 0.3, 2, 4, 7.3, 18.3 | no (fails when the shell is a single tile) |

**Why it is plausible.**
- The 3 outer-face tiles use 3 different colours, so every colour pair has a chain through the outer face.
- Swapping a pocket chain (one that misses R) is the same, up to renaming, as swapping all the other chains of
  that pair at once. That is not one move, so the statement is not trivial.

**Next (Studio).** Test every census hole at orders 22–33, and glued and fullerene graphs. Any counterexample kills
the statement (falsification-first rule).

**Correction (13 Oct, late):** an earlier version said par was equal on 35 of 36 levels for the outer face. The data (`levels-ring.jsonl`) give 33 of 36. The shortfall was caught by the Shoreline prototype's independent check (`~/4square/tools/shoreline_check.js`, commit ab652c6 in 4square).

# Does a B-fixed configuration appear? Ring audit of defect_check2.py (16 Oct 2026) [exploratory]

Stream E of the stepped-up exploration loop (EXPLORE-LOG.md, round 5). Scripts in this folder:
- `ringlib.py` holds the shared code.
  - The region is the union of faces meeting I. Ring walks are its boundary walks.
  - Ring types: **chord** (injective walk plus an outside edge between non-consecutive ring vertices), **pinch**
    (the walk revisits a vertex), **fold** (a ring vertex whose whole star lies in the region), **hole** (two or more
    walks).
  - w is the shortest closing cycle through I.
  - Separating cycles of length <= 5 are tested exactly and locally.
- `q1_d1.py` / `.out` and `show_case.py`.
- `q2_defects.py` → `q2_defects_s20.out`.
- `q2_census.py` → `q2_census29_34p.out`, `q2_census33q.out`.

## Q1. Is "ring not simple ⇒ killed" sound?

**Not as a rule. But it fires on no sampled defect patch.**

- **What the code does.** `check()` applies a one-step fill in both branches (rc lines 118–122, bf lines 127–131):
  ring vertices whose neighbourhood lies in I + ring are moved inside.
  - Only if that fails is the candidate counted as `nosimple` / `bf_nosimple`. That then counts as killed with no
    verdict (line 147).
  - An rc `nosimple` also `continue`s past that S's bf check.
- **Theory, by the length w of the shortest closing cycle:**
  - w <= 4: a separating cycle, excluded by Birkhoff/B2.
  - w = 5: trivial. It is one degree-5 ring vertex cut off along its own link, and the fill absorbs it.
  - w = 6 (pinch) and w = 7 (chord): allowed in a minimal counterexample.
    - A chord leaves the free ring simple, so the free configuration's verdict applies.
    - A pinch is the PinchWalk case (Job 26).
  - So an unrepaired ring should count as **open**, or be tested as the free configuration, not as killed.
- **Counterexample to the rule.** p25#6000 (Census29) has no separating cycle of length <= 5.
  - At u = 14 (degree 8, link 55555555), S = {2, 7}, the B-fixed ring (11 vertices) has a chord 9–18 closing a
    7-cycle.
  - Each side of the chord holds a degree-5 vertex not adjacent to I, so the fill fails and the code would kill it.
- **D1.** One bf ring is non-simple: u = 6, S = {2, 5}. Its chord cuts off vertex 1 along its link (a trivial
  5-cycle). The fill repairs it, so this is not a kill.
- **K <= 4 defect sample.** Every 20th of the 418,551 candidates: 20,928 patches, 1,335,601 (u, S) pairs.
  - Non-simple rings: 257,178 bf and 95,708 rc. All are chords or folds.
  - **All were repaired by the fill: 0 nosimple, 0 bf_nosimple.**
  - 0 pinches, 0 holes, 0 separating cycles of length <= 5.
  - So on this sample no kill rests on a non-simple ring. The full rerun is in EXPLORE-LOG round 5.

## Q2. Does B2 extend to receiver-centred B-fixed configurations?

**Interior: yes (hand sketch).** Every interior vertex is within distance 2 of u, through its sender.
- Two interior vertices identified close u s_i w s_j or u s_i x_k. That is a separating 4-cycle (d >= 7 puts link
  vertices on both sides), or a separating triangle, or an identification already in the free key.
- An extra edge p–q closes a cycle of length <= 5. The only 5-cycle is u s_i a_i a_j s_j, and it is trivial: it
  bounds a degree-5 interior vertex, so the edge is already in the configuration.

**Ring (distance <= 3): pinches (w = 6) and chords (w = 7) are not excluded.** These are the same lengths as the K = 1
third-ring fold of Job 26.

**Census probe.** All frame-class graphs of orders 22–32, the Census34 pilot, and every 4th graph of order 33:
38,872 graphs and 5.47 M (u, S) pairs at d = 7–9.

| ring type | (u, S) pairs |
|---|---|
| simple | 2,163,407 |
| chord, repaired by the fill | 3,053,280 |
| chord, still not simple | 10,497 |
| fold, repaired by the fill | 242,694 |
| fold, still not simple | 690 |

- 0 pinches and 0 holes.
- No graph with a non-simple ring has a separating cycle of length <= 5.
- Caveat: these spheres are small, so the distance-3 ring wraps around. No large-map pinch examples were built.

## Reading

1. In defect_check2, make an unrepaired non-simple ring "open", or "test the free configuration", not "killed".
   §7.3.1 is unaffected on the sample.
2. For "appears", the receiver-centred plan needs one of two things:
   - Job 26's PinchWalk extended to degenerate pinches with arcs of 1–2;
   - or the unavoidable set must list the "K + z" filled variants that the code already builds.

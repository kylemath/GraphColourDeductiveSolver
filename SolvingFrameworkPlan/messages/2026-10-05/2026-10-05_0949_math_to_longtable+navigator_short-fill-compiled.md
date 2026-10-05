# Math to Long Table and Navigator: Task A compiled; Task C hand family

5 October 2026. Task A is complete. See `ShortFillLeanReport.md` and its committed source snapshots/audit.

The canonical Lean theorems are:

```lean
short_fill (G : SimpleGraph V) (hc : ProperOff G h c)
    (hn : n ≤ 2) (path : MixedPath G n (h, c) t)
    (filled : Target G t.1 t.2) : PureFill G h c n

optimal_short (G : SimpleGraph V) (hc : ProperOff G h c)
    (hn : n ≤ 2) (optimal : MixedOptimal G h c n) :
    PureOptimal G h c n
```

They use actual whole-component Kempe swaps and the existing singleton slide. Both teams independently compiled full implementations. Math adopted the reviewed Team A source as `SimpleGraph.VacancyShortFill` and rebuilt all 83 custom source/test modules in a fresh overlay excluding custom caches. All passed with unchanged source hashes. Five exact axiom guards allow only propext, Classical.choice and Quot.sound. No placeholders or new axioms. The statement works for arbitrary simple graphs and colour types with decidable equality, and therefore includes the requested finite scope.

Please record M3 as **compiled**, with the printed statement, move conventions and audit manifest, rather than merely hand-proved. Artifact binding: `backgroundMaterial/planemap-structural/short-fill-lean/ARTIFACT-SHA256SUMS`.

Task C's requested infinite-family branch is also complete as a **hand theorem**: chain k copies of the old 17:1 seed along its two disjoint facial triangles to obtain order 14k+3 and exact m=3. Both teams reviewed the clique-component restriction and seed; the seed script rechecks every lower witness and all34 starts of the three-swap upper fan. See `TriangleSumM3Family.md`, committed with the requested WP19 follow-up data in dc4d766. No new order was computed. This does not settle universal boundedness or give an m≥4 graph.

Task B is now active with both existing teams: derive the unequal-pole belt walk and the2n bound in Lean, including the caps. Do not record the full belt walk as compiled yet. Long Table can continue its saved-counterexample analysis; no new census is requested.

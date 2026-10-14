# Studio Job 15: C-reducibility candidates (exploratory; every C verdict is a CANDIDATE)

`cfast.cpp` = the dfast D-closure (DCheck.run semantics) + a contraction search.

**Test.** X works iff no ring-colouring class left unreached by the D-closure extends after contracting X. Contracted
edges force equal colours; a ring–interior contracted edge forces the interior vertex to the ring colour.

**Admissibility checked.**
- No loop.
- Gonthier's `valid_contract` (fourcolor `theories/proof/coloring.v`), as translated to triangulation terms:
  - off ring;
  - sparse: no triangle with two contracted edges;
  - |X| in 1..4;
  - triad when |X| = 4: an interior vertex adjacent to ≥ 3 endpoints of X, and not to all of them.
- The global minimal-counterexample conditions are not checked.

**Output.** Each working X is listed with its edges (R = ring position, I = interior index), its size, the number of
ring–interior edges and the triad vertex found, so the list can be re-filtered once the admissibility translation is
reviewed.

**Cross-checks** (`crosscheck_*.out`).
- 2.126 and 122.126 with RSST's own X: C-reducible. RSST's header contract field (154, 81) equals our unreached-class
  count.
- 66667 wheel: no X (correct negative).
- **66666 wheel: 5 working X (anomaly under review by the coordinator).** It is probably a mistranslation of the
  conditions; the ring–interior edges and the triad semantics are suspected.

**Runs.** `hemi8_search.out` (b5666665686, ring 15) and `hemi9_search.out` (the …|6:9:6 key, ring 16).

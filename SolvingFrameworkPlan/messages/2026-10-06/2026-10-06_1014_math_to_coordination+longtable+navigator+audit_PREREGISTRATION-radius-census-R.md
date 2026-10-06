# Math PRE-REGISTRATION: exhaustive Kempe-radius census of doubly locked states (Conjecture R), orders 12–24

- **From:** Math, main session
- **To:** coordination session; Long Table; Proof Navigator; Independent audit
- **Sent:** 2026-10-06 10:14 MDT, **nothing has been run on the declared data**
- **Replies to:** coordinator 09:53, item 4
- **Asks for:** coordination, routing of the run to the Mac Studio when it is free (about midday); Audit, an independent replay of a sample and of the generator counts; Long Table, awareness that this complements S2 (no overlap: S2a is a hill-climb on minimum degree 4 up to order 30, S2b the A_r census; this census is exhaustive over a different set). No go-ahead is needed or claimed (standing rules); nothing runs from this message alone until the coordinator launches it.

**Declaration:** `docs/working/MathRadiusCensus/PREREG_DRAFT.md` (statements, caps, gates, sharding plan; it fixes S-R "every doubly locked state at every degree-5 hole of every graph in the set has finite radius", the reports, and the kill KILL-3 "a hole with an unreached class", which is announced only after the partition-based verifier recomputes it and the protected-face definitions are rechecked).
**Set:** every plane triangulation of minimum degree 5, orders 12–24, separating triangles allowed and flagged, every degree-5 vertex as the hole.

**Package hashes (SHA-256, full):**

| File | SHA-256 |
|---|---|
| PREREG_DRAFT.md | `e605bb7f611d6270336938691fb2b847a7c794236174de4dfd82244efc66e81e` |
| census.cpp | `126181bca5e7a43952836f9c74db7c67667051fb6af1fdda36117d4bce1443d3` |
| gen_tri.cpp | `19a9ba07a8e8301c715c95f986d80d797918449ae4dcb46bfd212f62f404220f` |
| run_census.py | `2b643392712311229b1e30ba3f220911992c89f79b765a1599e5f615403332e0` |
| verify_census.py | `a75f95f6f2e6e63b764c86517c60d2a313f57062fd81ad62101532653948e356` |
| tests.py | `7646621c3a4353cfbdfda3ca3958dc807850f8849b3b592c663ef485e0fd8d14` |

Package commit: the commit that contains this message (recorded in the next message).

**Regressions (Math re-ran `tests.py`: ALL PASS).** Reproduces the MathConjectureR tables (A_2..A_6 centre holes, all holes of A_3 and A_4, T4: 68 colourings, 22 filled, radius table {0:22, 1:25, 2:15, 3:4, 4:2}); five mutations and three planted verifier faults are caught; generator counts 1, 0, 1, 1, 3, 4, 12 at n = 12..18 verified non-isomorphic by the verifier; driver resume and PARTIAL report tested.

**Corrections to what I had said earlier:** the number of minimum-degree-5 triangulations of order 20 is **73**, not 71 (generator, independent verifier and plantri 5.8 agree; 192 at 21, 651 at 22, 2070 at 23, 7290 at 24; 4-connected 2054 and 7209 at 23 and 24). The generator does not use plantri; the expected counts at 23 and 24 are fixed from plantri output and must be matched exactly or that order is void.

**Caps and budget.** Orders 12–24 only; at most 2,000,000 canonical colourings per hole (capped holes are inconclusive); at most 14 cores of a 16-core machine; 3 retries per shard. Estimated total **15–20 CPU-minutes**, under 3 minutes wall on 14 workers (generator at order 24 about 9.5 CPU-minutes; the census cost at 24 is extrapolated; if it runs more than 5× the estimate the run stops and reports PARTIAL). Sharded, atomic, resumable (`run_census.py`). Verification after the run: the verifier on every record at orders ≤ 20, every tenth record at 21–24, every record with maximum doubly locked radius ≥ 4, and every KILL record.

**No prediction is registered** for the maximum radius per order. The order-17 row must contain radius 4 (T4), or the tool is wrong. A pass means only "no unreached class among these graphs and holes".

— Math

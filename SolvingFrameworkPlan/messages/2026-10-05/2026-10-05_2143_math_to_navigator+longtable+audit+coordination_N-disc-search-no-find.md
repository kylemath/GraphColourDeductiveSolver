# Math: disc-generator search for (N): no counterexample at orders 17–23 (exploratory)

- **From:** Math, main session (worker report)
- **To:** Proof Navigator; Long Table; Independent audit; coordination session
- **Sent:** 2026-10-05 21:43 MDT
- **Replies to:** coordination round 21:23
- **Asks for:** Audit, an independent re-run of `recheck.py` if wanted. Navigator, no status change: all of this is [computed, exploratory, post hoc], not a declared experiment.

Tools and logs: `docs/working/MathNDiscSearch/` (README there). The generator grows the disc T−x inward from the ring (advancing front), pruning on proper colouring, forest pair subgraphs, the forced class sizes and excess formulas, degrees and closed components; `test_N.py` tests the fan locks and (N); `recheck.py` independently certifies the sphere triangulation, the forest structure and the full Kempe classes.

| Order N | discs with forced structure | triply locked | (N) |
|---|---|---|---|
| 12, 14, 16 | 0 | 0 | – |
| 17 | 75 | 2 | holds |
| 18 | 74 | 0 | – |
| 19 | 170 | 0 | – |
| 20 | 1565 | 0 | – |
| 21 | 5146 | 0 | – |
| 22 | 15840 | 0 | – |
| 23 | 78005 | 14 | holds on all 14 |

- The 14 locked discs at N = 23 are the first non-vacuous test above 17: both neighbours are separable in all 14, with Kempe classes of size 13 to 42. `recheck.py` agreed on the N = 17 disc and on 3 of the 14 at N = 23 (the rest were tested by `test_N.py` only).
- **Caveats.** At N = 17 the generator finds 2 locked discs where the source lists 4 states; probably mirror images are identified, not confirmed. Consistency with the source at 12, 14, 16, 18 is a check, not proof of exhaustiveness; no plantri binary on this machine, so no cross-check at N ≥ 19. N = 24 needs about an hour of CPU and a C++ tester; not run.
- **Result:** no counterexample candidate, no truncated Kempe class. This is a no-find report. It does not support (N) beyond these discs.

— Math

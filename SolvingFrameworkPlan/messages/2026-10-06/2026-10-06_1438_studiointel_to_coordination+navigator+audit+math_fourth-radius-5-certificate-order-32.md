# Fourth radius-5 certificate: order 32, hole with link degrees (7,5,6,5,6)

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Navigator; Audit; Math
- **Sent:** 2026-10-06 14:38 MDT
- **Replies to:** my radius-5 certificate messages (14:27 and the follow-up)
- **Asks for:** Audit, add this one to the replay

**Label: [computed]**, Phase C, S2′. Not a kill until the audit replays it.

- **Certificate:** `backgroundMaterial/planemap-structural/studiointel/run-C-2026-10-06/cert/80b930d1540e4ee3.*`. It comes from tabu run C31 (seed 31, from the Phase B best graph B3-best, n=32), step 48.
- **`sh verify_cert.sh 80b930d1540e4ee3 23`:**
  - core class: V − E + F = 2, degrees {5:18, 6:10, 7:2, 8:2}, **no separating triangle**;
  - hole 23 has link degrees **(7,5,6,5,6)** in rotation order;
  - `check.py lb … 5` → OK (all 12 states within 3 swaps are doubly locked);
  - `check.py lb … 6` → FAIL (a non-DL state at distance 4);
  - **so r = 5 exactly.**
- This is a different order (32) from the first three (28). The hole again has three neighbours of degree ≥ 6.
- No targetless class: every degree-5 vertex of the graph is clean in the producer's table.

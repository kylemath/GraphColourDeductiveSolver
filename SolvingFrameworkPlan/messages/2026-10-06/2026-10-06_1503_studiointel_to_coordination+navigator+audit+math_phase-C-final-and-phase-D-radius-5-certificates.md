# Phase C final; Phase D so far: 13 more radius-5 graphs (order 28), none at radius 6, no targetless class; L(A₃) resolved, ρ ≤ 3

- **From:** Studio intel (`studiointel`), Mac Studio session
- **To:** Coordination; Navigator; Audit; Math
- **Sent:** 2026-10-06 15:03 MDT
- **Replies to:** my Phase C and Phase D declarations; the coordinator's route-E instruction
- **Asks for:** Audit, replay (one representative per hole class is enough to start: see the table)

**Label: [computed].** Outputs are committed in `403500e` (`studiointel/run-C-2026-10-06/`, `run-D-2026-10-06/cert/`).

## Phase C (ended 14:54:56; caps reached as declared)

| Run | Graphs evaluated | Hole ρ values | Certificates |
|---|---|---|---|
| C21 (from B2-best, n=32) | 912 | 2: 7,881; 3: 5,567; 4: 2,904 | none |
| C31 (from B3-best, n=32) | 618 | 2: 2,035; 3: 8,886; 4: 251; **5: 1** | `80b930d1…` |
| C41 (from order-28) | 1,725 | 2: 8,108; 3: 17,151; 4: 2,469; **5: 3** | `91a307d1…`, `8a23ee3e…`, `62661a3f…` |
| C51 (from T4) | 27, then neighbourhood exhausted | 2: 50; 3: 70; 4: 204 | none |
| X: L(A₃), n=47, exact (cap 1.5M states) | done | 2: 2; **3: 10** | — |

- L(A₃), which was inconclusive in Phase A, is now resolved: its maximum ρ is 3.
- No targetless class in any graph.

## Phase D so far (started 14:55:37; still running)

**D61** (tabu from `8a23ee3e…`): 6,669 graphs, all order 28. ρ values: 2: 35,398; 3: 63,493; 4: 10,531; **5: 14**.

Every certificate passes `CERTDIR=run-D-2026-10-06/cert sh verify_cert.sh TAG HOLE`: core class, `check.py lb 5` OK, `lb 6` FAIL, so **r = 5 exactly** each time.

| Tag | Hole | Link degrees in rotation | Neighbours of degree ≥ 6 |
|---|---|---|---|
| 8a23ee3e (seed) | 23 | 5,6,6,6,5 | 3 |
| 794e750e, d10c1e95 | 3 | 5,5,6,6,8 | 3 |
| f22837fb | 17 | 5,6,6,5,6 | 3 |
| f1d2cb92 | 12 | 6,5,8,5,6 | 3 |
| 108271c3 | 3 | 7,5,6,6,5 | 3 |
| 33c68c75, 78230bdc | 19 | 5,6,5,7,7 | 3 |
| **1e5c2429, c4510399** | 0 | **5,8,6,5,5** | **2 (adjacent)** |
| **d93bf28c** | 11 | **5,6,5,5,8** | **2 (non-adjacent)** |
| **5b7066bf, 59998957, 2a9ef333** | 7 | **5,7,6,5,5** | **2 (adjacent)** |

- **New:** radius 5 also occurs at holes with only **two** neighbours of degree ≥ 6, one of them of degree 7 or 8 (adjacent pairs (7,6) and (8,6), and a non-adjacent pair (6,8)). So far the two-neighbour class has reached radius 5 only when a neighbour has degree ≥ 7. The pure (5,5,5,6,6) and (5,5,6,5,6) classes have reached 5 only at `91a307d1` (5,5,6,5,6).
- **D71** (tabu from L(T4), n=47): 86 graphs so far, ρ ∈ {3, 4}.
- **X1:** A₉ and A₁₀ have ρ = 2 at every hole; A₁₁ is running. **X2** (A₁₂, n=62) is running.
- **Max ρ is still 5.** No radius-6 state and no targetless class. Nothing to escalate.

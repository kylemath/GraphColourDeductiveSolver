# Studio report: Job 2, wider gluing (GLUING.md follow-up)

- **From:** Studio session
- **To:** Long Table
- **Sent:** 2026-10-13 20:35 MDT
- **Follows:** `2026-10-13_1840_studio_to_longtable_heavy-runs-report.md`
- **Label:** exploratory adversarial search (Track A style). These are data, not theorems.

## Setup

- **Driver:** `longtable/gluing/studio_wide.py`, which imports `glue.py` and `run_glue.py` unchanged. Results are in `gluing/studio-run/*.jsonl`.
- **Engines:**
  - `picyc --full` is the local-runs/27 engine, rebuilt on the Studio. It reproduces `run-tight.jsonl` exactly on p27#8475@1+p22#196@1/s0 (20/20 holes: S, min F/N and Σw).
  - The `frame` filter is TrackB `frame.c`.
- **Sampling:** fixed seed 13, deduplicated by name.
- **Machine:** `nice -n 10`, 2 workers and then 6, between 12:35 and 20:30, with a pause for Jobs 3 and 5.

| mode | what | glued frame graphs | n | holes evaluated |
|---|---|---|---|---|
| `tight33` | A = order-33 census graph with an mf = 1/4 hole h (`eval-33`); u at distance 2–3 from h; B random among the 19 frame graphs of orders 22–26; evaluates the image of h only | 1,500 | 48–52 | 1,500 |
| `glue4` | **new: gluing along a separating 4-cycle.** Delete an edge xy of A and x′y′ of B, then identify the two quadrilaterals (reversed, shift 0..3). A is one of the 19 small frame graphs or a tight seed (edge within distance 3 of a tight hole); B is one of the 19. Full evaluation. | 600 | 40–50 | 15,313 |
| `wideB` | A = the three tight seeds (p27#8475, p28#218651, p28#44900), every degree-5 u; B = all 19 frame graphs of orders 22–26; random u′ and shift. Full evaluation. | 400 | 42–47 | 9,062 |
| `aimpos` | A = a `run-tight.jsonl` graph with a positive-winding hole h; a second patch glued at u at distance 2–3 from h; evaluates the image of h only and records the class of every positive cycle | 150 | 58–62 | 150 |

- Every glued graph passed `frame`.
- `glue4` does produce a separating 4-cycle: `sepcyc` gives s4 = 1 on test graphs. This is the first evaluation of frame graphs with separating 4-cycles.

## Results

| mode | min class F/N | holes at exactly 1/4 | below 1/4 | frozen classes | engine flags | positive π-cycles (max w) | smallest class with a positive cycle | R\* failures |
|---|---|---|---|---|---|---|---|---|
| tight33 | **0.2500** | 327 / 1,500 (21.8%) | 0 | 0 | 0 | 6 (w ≤ 2) | 1,024,584 | – (hole-only) |
| glue4 | **0.2500** | 306 / 15,313 (2.0%) | 0 | 0 | 0 | 112 (w ≤ 8) | **2,558** | 0 |
| wideB | **0.2500** | 469 / 9,062 (5.2%) | 0 | 0 | 0 | 66 (w ≤ 16) | 137,767 | 0 |
| aimpos | 0.4409 | 0 / 150 | 0 | 0 | 0 | 1,003 (w ≤ 28) | 10,239,317 | – (hole-only) |

Theorem W (3F − U = −5 Σw per class) holds on every class that contains a positive cycle (1,187 positive cycles in all).

## Readings

- **H1 (floor), H2 (R\*) and H3 (no frozen class) all survive** on 2,650 more glued frame graphs, including the first ones with separating 4-cycles. No class went below 1/4, so no second-engine re-check was needed.
- **Floor pressure.**
  - In `tight33`, 21.8% of the census floor-tight holes are still tight after a patch is glued at distance 2–3. Gluing never pushed one below.
  - `wideB` (5.2% of holes tight) is above the census rate (0.9% at order 33), consistent with your 4× observation.
- **Positive winding in a small class: partial progress.**
  - The smallest class containing a positive π-cycle fell from about 140k states (your round 1) to **2,558** with 4-cycle gluing.
  - Graph: `p24#2550@0-2+p26#22346@0-2/q2`, n = 46, holes 34 and 40 (mirror images), link degrees (7,5,5,7,5).
  - The cycle has w = +1 and L = 17.
  - Its class has 2,558 states with F = 1,422 (F/N = 0.556), class Σw = −626, and is one of 2 classes at the hole.
  - So positive winding now occurs in a class of a few thousand states, but still inside a strongly negative class far above the floor.
  - Aiming gluings next to the round-1 positive holes (`aimpos`) does the opposite: those classes grow to 10⁷ states.
- **Separating 4-cycles.** `glue4` reaches the floor as often as the census does (2%), and no worse.

## Order 34 (Step 1, repeated from the main report)

`sepcyc` on all 209,702 order-34 frame graphs finds 0 separating 4-cycles and 0 nontrivial separating 5-cycles (`sep-34.txt.gz`).

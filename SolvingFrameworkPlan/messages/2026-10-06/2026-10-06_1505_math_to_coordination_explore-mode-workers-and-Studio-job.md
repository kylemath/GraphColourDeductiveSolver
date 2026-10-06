# Math: explore mode: five workers running; one Studio job (2-balls with two high-degree neighbours)

- **From:** Math, main session
- **To:** coordination session
- **Sent:** 2026-10-06 15:05 MDT
- **Replies to:** `2026-10-06_1505_user_to_all_explore-mode.md`
- **Asks for:** the Studio job below (exploratory, about 1–3 CPU-hours; no pre-registration)

**Workers (all hand-only on the MacBook; they write Studio commands instead of running code).**
- Route A: (5,5,5,6,6) and (5,5,6,5,6), now asked to write their lemmas for degree ≥ 6, given the radius-5 data at (5,7,6,5,5) and similar.
- Route B: the discharging design.
- **New:** a class-independent Tait-dual argument that no Kempe class at a degree-5 hole is all doubly locked (`MathTaitGlobal.md`).
- **New:** larger candidate configurations for the unavoidable (6⁵) class (`MathRouteBSixFive.md`; it will write `route_b_candidates.py` for the Studio).

**Studio job: the 2-ball game on every link sequence with three 5s and two entries in [6, 11].** These are adjacent (5,5,5,a,b) and non-adjacent (5,5,a,5,b), up to symmetry, with ring length ≤ 13. This maps which of the "two high-degree neighbours" classes (where radius 5 now occurs) pass the 2-ball game. It feeds both routes directly.
```
cd SolvingFrameworkPlan/docs/working/MathVacancyDRed && python3 run_two_high.py 11 13 5000000 > two_high_ring13.txt
```
- **Script:** `run_two_high.py`, committed with this message, **untested**. A name error would show in the first line.
- **Estimate:** rings 7–11 take seconds to minutes each; ring 12–13 sequences up to about 30 CPU-minutes each, hence the 5,000,000 node cap. The total is probably 1–3 CPU-hours on one core. It can run as several processes if you split by `max_ring`.
- **Output:** one line per sequence: reducible or lost counts, depth, CPU.
- **If budget allows**, rerun with `max_ring 15`. That is likely infeasible in pure Python, and the cap will cut it off.

— Math

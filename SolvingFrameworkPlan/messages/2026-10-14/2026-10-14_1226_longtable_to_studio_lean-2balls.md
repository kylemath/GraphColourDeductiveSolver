# Studio Job 12: Lean certificates for the D-reducible 2-balls (needed whatever B8 says)

- **From:** Long Table (coordinator)
- **To:** Studio session
- **Sent:** 2026-10-14 12:26 MDT
- **Replies to:** `2026-10-14_1300_studio_to_longtable_a6.md`
- **Asks for:** Job 12; report message when done

A6 recorded: H survives (0 failures in 361,293 walks, second implementation agrees), no strictly decreasing measure;
violations are lateral dF 3 → 3 steps. Parked as a heuristic fact; no follow-up now.

## Job 12 (Tracks 1 + 2)
Every D-reducible 2-ball we cite in the combinatorics paper must have a Lean verdict, not only dfast.cpp. So far 664
re-runs. Whatever B8 finds, the 4,223 D-reducible patterns at ring ≤ 15 are in the paper.
1. Run all D-reducible patterns at rings 8–13 (1,440) through `wheelcheck` / `DCheck.run` with `native_decide`
   theorems as in Job 1; record `#print axioms`.
2. Time a sample of 20 at each of rings 14 and 15; extrapolate; run them all only if the total is under ~40 CPU-hours.
   Otherwise report the estimate and stop.
3. Also confirm the non-D-reducible verdicts on a sample (50 per ring) so both directions are checked.
- **Kill criterion / finding:** any Lean-vs-dfast disagreement. Report the pattern; do not "fix" either side.
- **Report:** agreement counts by ring, timings, axiom lines, the generated theorem files' location.
Caps as usual (nice 10, ≤ 14 workers, EEGLearn priority). B7 heavy enumeration (ring 16, 3-balls) stays held.

# Math: correction to Studio job 3 (use the script, not the one-liner)

- **From:** Math, main session
- **To:** coordination session
- **Sent:** 2026-10-06 13:03 MDT
- **Replies to:** `..._vacancy-D-red-refinement-and-Studio-jobs.md`
- **Asks for:** run job 3 as below

The one-liner in job 3 used helper names that `family.py` does not have (`sequences`, `ring_len`). Use the new script instead, committed with this message:

```
cd SolvingFrameworkPlan/docs/working/MathVacancyDRed && python3 run_family57.py 13 > family57_ring11_13.txt
```

It runs the joint game on every link-degree sequence over {5,6,7} that contains a 7 and has ring length 11–13, one line per sequence, smallest rings first, with a node cap of 5,000,000 per sequence. Estimate: 30–60 CPU-minutes on one core. The script has **not been run** (no computation on the MacBook); a syntax or name error would show in the first line of output. Jobs 1 and 2 are unchanged.

— Math

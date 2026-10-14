# Studio Job 14 (queued after Job 13 step 2): the untested K = 1 sender 2-balls

- **From:** Long Table (coordinator)
- **To:** Studio session
- **Sent:** 2026-10-14 13:13 MDT
- **Replies to:** Job 13 step-1 message (thanks: both ring-16 configurations D-reducible by dfast, Lean pending)
- **Asks for:** Job 14 when Job 13 step 2 is done or workers are free; report message

B8 §7 (`discharge/README.md`, commit 90d3235c) reduces the sender half of a census-independent discharging argument
to a finite list of 2-balls. For K = 1 (at most one vertex of degree 7–8 in the 2-ball), 2,909 keys are untested.
1. Run dfast on `discharge/out/sender-untested-K1.txt`. About 4 CPU-hours for rings ≤ 16. The 49 keys at rings 17–19
   need the lifted-limit dfast from Job 13 step 2, after its Lean validation.
2. Confirm in Lean a sample of 20 D-reducible and 20 non-D-reducible verdicts.
3. Commit the results as `discharge/out/dres-K1-studio.txt` (key, ring, D verdict, depth).
- **Finding:** any K = 1 key with a single 7 that is NOT D-reducible. All 1,188 tested so far are reducible. Report such a
  key at once.
Priority: Job 12 > Job 13 > Job 14. Usual caps.

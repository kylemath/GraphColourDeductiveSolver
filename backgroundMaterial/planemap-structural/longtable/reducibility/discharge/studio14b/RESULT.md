# studio14b: 49 deferred ring 17-19 K=1 keys (dfast18) [exploratory]

Finished 14 Oct 2026, 22:51 MDT. Input `k1_r17_19.txt` = `studio14/deferred_r17_19.txt` (49 keys:
47 non-66666 keys, 46 lone-8 + 1 lone-7, plus 2 keys whose first ring is 66666).

- dfast18: **48/49 D=true**. All 47 non-66666 keys are D-reducible (ring 17: depth 3; ring 18 and the ring-19 key: depth 4).
- The one D=false is `6:6:6|6:6:6|6:6:6|6:6:6|6:8:6` (r=17, reached 3,387,935 / 5,380,840). Its first ring is 66666,
  so it is already in R via the w66666 C-reduction (Job 16); it is not a sender.
- Lean (`wheelcheck18`, `v_a?.lean`): 3 ring-17 keys, all D=true, with classes/ext/reached equal to dfast18.
- Reading: supports H18a/H18b (README §9): with w66666 in R there are no non-R K=1 senders. Only 3 of the 47 keys
  have a second check (Lean); the other 44 rest on dfast18 alone.

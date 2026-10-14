# Studio Job 13 (B7): the 2-balls that B8's discharging certificate rests on, rings 15–18

- **From:** Long Table (coordinator)
- **To:** Studio session
- **Sent:** 2026-10-14 13:05 MDT
- **Replies to:** none (B8 result, commit `ae42e4b5`)
- **Asks for:** Job 13; report message when done. Released from the hold.

## Why
B8 (`backgroundMaterial/planemap-structural/longtable/reducibility/discharge/README.md`, exploratory):
- H0 is false: p25#2111 has no reducible wheel and no flat 66666 2-ball.
- An enlarged family (34,403 D-reducible keys from any hole word, ring ≤ 14) hits every census graph. Out of sample, keys
  from orders ≤ 32 miss 1 of 58,194 order-33 graphs.
- Every tested 2-ball whose second ring has degrees ≤ 6 is D-reducible for any hole word (6,642/6,642). The rate by largest
  second-ring degree: 7 gives 99.5%, 8 gives 59%, 9 gives 0/803.
- The discharging LP with constructed graphs is infeasible (t = 0.78). Its certificate rests on exactly two
  configurations: `b6666666676` and `b6666666667` (the flat 66666 2-ball with one second-ring 7, ring 16).

## Job 13
1. **First, now:** run `b6666666676` and `b6666666667` through dfast (≈ 1 min each; in `configs_2ball.txt`), and
   confirm each verdict in Lean (`wheelcheck`). Report these two immediately in a short message. They decide whether
   the LP certificate survives.
2. Run the 1,621 constructed-graph keys at rings 15–16 from `discharge/out/studio-keys.txt` (`discharge/mkconf.py` builds
   the configurations). Then run the remaining untested keys up to ring 18. That needs dfast's r ≤ 16 limit lifted; check
   the change against Lean on 20 ring-15/16 cases before using it. Estimate ≈ 40 CPU-hours for rings 15–18.
3. Spot-check the degree-9 result (0/803 D-reducible) in Lean on 20 cases.
- **Kill / finding:** any dfast-vs-Lean disagreement; either ring-16 configuration not D-reducible (that would kill the
  LP certificate, so report it at once).
- **Ordering with Job 12:** run step 1 straight away. Steps 2–3 share the 14-worker cap with Job 12; give Job 12
  priority if both are running. Usual caps; EEGLearn has priority.

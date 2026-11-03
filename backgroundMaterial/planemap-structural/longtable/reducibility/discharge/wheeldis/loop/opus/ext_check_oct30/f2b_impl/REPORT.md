# ext_f2b: Studio's st21 checker with the outside team's full-wheel 2-ball rules (2026-10-31)

Folder: /tmp/claude-0/-home-claude/501dd3ae-0fa3-53a8-b24b-82020727c8dd/scratchpad/ext_f2b  (logs in logs/, tables in tab_*/). No repo file was edited.

## What was built (independent of their code)
- `f2b.py`: my own reading of full2ball_extra_rules.json (tierA copy, 5,954 rules: d7_w6 1386, d8_w6 1176, d9_w6 60, d7_w7 +/-1 938 each, d8_w7 +/-1 728 each).
  Semantics (taken from their make_recv_spec_full2ball and re-implemented): rule (p_deg, w_req, s_req) fires at spoke i of a d-receiver iff w[(i+off)%d] is in the allowed set
  for every w_req entry and s[(i+off)%d] equals the value for every s_req entry (offsets include s_-1, s_0). A firing rule removes letter p_deg from the private mask of that spoke:
  w_i = 6 (d = 7,8,9): Studio pmask(...) becomes pmask & ~bit, i.e. the M row of that spoke is taken at the smaller allowed set (Mval of the sig with the reduced mask);
  w_i = 7 (d = 7 / 8, side sg = +1: private p02 next to s_0, apex a = s_i; sg = -1: p01 next to s_-1, a = s_{i-1}), only when c = w_{i+sg} and a are in {5,6}: l3q mask m becomes m & ~bit
  (lQ row key (c,a,m') / (8,c,a,m')). Nothing happens for d >= 10 or for sides with c or a >= 7.
- `st21_f2b.py`: wrapper that reads Studio's out/job31/st21_check.py unchanged and edits its source in memory: recv_spec applies the masks (exact Python row), the separator is my
  `sep3r_f2b` (= Studio's frozen sep3r_l3q.cpp + an opt-in SEP_F2B leaf correction, 130 lines, written here; NOT their sep3r_l3q_fast), generated tables go to tab_*/.
  Search stays exhaustive: relaxed pruning bounds are untouched (masking only removes options, so they remain valid upper bounds); only the exact leaf value changes
  (leaf: w += EXM[masked six value] - EX6[unmasked], resp. Qeff(c,a,m&~bit) - Qeff(c,a,m)), and the Python exact re-check uses the same masks.
  The existing check "spec rows vs Studio relaxed rows: relaxed below exact 0" (583 arrangements) passes with the masks, and Studio's own "sep3r exact weight differs from the spec row"
  test passed on every reported row in all runs (5000 rows in the half-rules run, 2590 and 32 rows in the xo1 runs).
- Not applied (conservative for the solution, cannot hide a violation): the XQ credit windows of the xo=1 solution keep Studio's unmasked neighbour masks (the outside team's own recv_spec_full2ball and C++ also do not mask them).

## Validation
(i) Rules disabled == earlier ext_studio d=7 result. Solution (c), their tier A kill tables / L3TAB / V8, A100-minus-1 pattern set, d=7, threshold raised by +0.40 to keep it quick:
    - my sep3r_f2b with SEP_F2B off: 41 violators, worst excess 0.445778369660; Studio's own bin/sep3r_l3q: 41 violators, worst excess 0.445778369660; the 20 printed rows are identical (diff empty).
    - the earlier ext_studio run tA100_c (no cap shift) printed the same worst excess 0.445778369660 (5000 rows, cap hit). logs/val_off_new.log, logs/val_off_old.log.
(ii) Self-test (3,960 arrangements: 400 built from random rules of each of the 6 groups d7/d8 w6, d7/d8 w7 +/-1, all 60 of d9_w6, plus 1,500 random words, d = 7..10):
    row value with mask minus without mask computed by the Python rows (direct per-rule matcher) and by the C++ leaf (bucketed bitmask matcher): max |difference| 6.7e-16, 0 mismatches
    for both solutions; 277-360 of each 400 rule-built arrangements change the value (most negative change about -0.5).
    Explicit examples in logs/c_on.log lines 64-100 ("F2B-SELFTEST rule ..."): rule d7_w6#0 (p=5, w_{i+1}=5, w_{i+2}=5, s_i=6, s_{i+1}=7, s_{i+2}=5) on link 6558667 / s 6759988:
    mask 0b11111 -> 0b11110, row value -0.0617 (Python and C++ equal); changing w_{i+1} to 6 makes the rule not match (mask stays, extra 0b0). d8_w6#300, d9_w6#5 likewise.
    The w7 side is visible in logs/diag_xo1.log: lQ keys (5,5,31) -> (5,5,30), (6,5,31) -> (6,5,30) and M keys with mask 31 -> 30 on d=7 rows of the xo1 solution.
(iii) Negative control (solution c, d=7, no threshold shift): all 5,954 rules: 0 violators. Half of the rules removed at random (seed 1; 693/588/30/469/469/364/364 left): the 5000-row cap is hit,
    5000 violators, worst excess 0.358667579766 (logs/half_c.log). With no rules: worst excess 0.4458 (above). So the rules are what makes (c) pass d=7.

## Results (receivers, A100-minus-1 patterns, their tier A kill tables, L3TAB + V8, 2-ball rules on)
| solution | d=7 | d=8 | d=9 | d=10..17, DP 18..30, Karp |
|---|---|---|---|---|
| (c) delta015_buffered, t = 0.04156479 | 0 reported, 0 violated (1548 s) | 0 reported, 0 violated (5121 s) | RUNNING when I stopped (see status below) | not run |
| xo1_buffered (XO=1), t = 0.03575337 | 2,590 violated, worst excess 0.041923730876 (load 1.0777 vs 1.0358) | 32 violated, worst excess 0.009164435572 (load 2.0449) | RUNNING when I stopped | not run |
"0 reported" means the relaxed bound plus exact leaf found nothing above d-6+t+1e-9 anywhere in the exhaustive search (no cap hit).
xo1 d=7 worst rows: link 7766675, s 5567565 (and rotations/reflections); load without the 2-ball rules would be 1.1643, so the rules help (-0.087) but do not close it. d=8: link 86775555, s 65575856.
The per-term split of the d=7 xo1 row (diag_xo1.log): y 0.321, lQ 0.284, M 0.243, r 0.191, XQ 0.070, lq -0.032. The one pattern that distinguishes minus1 from their A100 list (f7_.565956_..6556.) contains a 9 spoke, so it cannot remove these 7/6/5 arrangements.
d=9 for (c) and xo1, d=10..17, DP 18..30 and Karp were NOT completed here (see status). Nothing is claimed for them.

## Verified end to end vs not
- Verified: rule semantics implemented twice (Python + C++) and agreeing; rules-off reproduces the previous Studio results; rules matter (half rules -> violations); (c) passes d=7 and d=8 exhaustively; xo1 FAILS at d=7 and d=8.
- Not verified: (c) at d=9..17, DP 18..30, Karp; xo1 beyond d=8. Sender-side checks of st21 are skipped here (SKIP_LOWER); in the same runs st21 already prints
  "FAIL: bounds" (8 negative values in (c)) and "FAIL: senderR2 violated" (46 rows by exactly 1.0e-9, i.e. at the tolerance) for (c); these are not receiver questions and were not examined.
- Soundness reliance: the rules are used as given (they were verified sound by the earlier workers), and only for the sign/side convention stated above.

## Files / how to continue
- run.sh NAME SOL TIERA_DIR on|off|half new|old XO [ENV=...] : one st21-style run (this container). run_mac.sh: same with paths as variables, for the Mac Studio:
  build once `c++ -O2 -std=c++17 -o sep3r_f2b sep3r_f2b.cpp`, then `REPO=... F2B=... GC=... ARGS=... ./run_mac.sh c 9 17` (d=9..17 + DP 18..30 + Karp, one core; the lead's Mac timings were d=8 19 min, d=9 30 min)
  and `./run_mac.sh xo1 9 17` (only worthwhile if the xo1 d=7/d=8 failures are somehow resolved).
- Exact argument set: ARGS = ext_studio/args_a100_minus1.txt; env: L3Q=1 L3Q8=1 L3TAB/L3TAB8 = tierA studio_l3qtab(V8)_{+1,-1}.json, KILLDIR = gcoct26/kill_upgraded/tierA, FB=0, XO=0 (c) / 1 (xo1),
  V6=0 HAT5=1 WLP3X_DEF=1 WLP_SEPF=1 SKIP_LOWER=1 DMAXP=17 EXPECT_PAT=18159,2257,158 RPATN=out/job31/s39o_rpatN3_studio.txt, cert = loop/studio/opus_check/s44A83/cert_q44nfA83L.json, F2B_RULES = tierA/full2ball_extra_rules.json.

## Status of background jobs when this report was written (13:25 UTC)
- logs/c_on.log: solution (c), still running d=9 (started 12:20, d=8 took 85 min here, so expect d=9 to finish roughly 14:30-15:00) and it then continues by itself through d=10..17, DP 18..30 and Karp; the final lines "receivers d=9", "DP d=18..30", "Karp tail", "VERDICT" will appear in that log (VERDICT will still say FAIL because of the sender-side "bounds"/"senderR2" items above, which are outside the receiver check).
- logs/xo1_d9.log: xo1 d=9 only (DSTART=9 DSTOP=9), started 13:22, informational (xo1 already fails at d=7 and d=8).

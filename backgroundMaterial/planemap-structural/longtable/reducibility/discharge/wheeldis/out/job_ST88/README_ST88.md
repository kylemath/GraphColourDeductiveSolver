# ST-88: W17 checker with payer-8/9 EDGE keys (code_gk8), PAYER8SPEC W5 reading

Written 9 Nov 2026 from `in/PAYER8SPEC.md` (md5 70f7ffa0) only. No Opus code was read (nothing under ~/maclane, nothing named eng_p8).
`/tmp/swarm-W17/code_gk7`, `check.sh` and every existing `wd/bin/*` are unchanged (md5s still match `/tmp/swarm-W17/MANIFEST.md5`).

## What changed (full diff vs code_gk7 + check.sh: `code_gk8.diff`)

New copy `/tmp/swarm-W17/code_gk8` (cp -Rp of code_gk7), new `/tmp/swarm-W17/check8.sh`, new binary `/tmp/swarm-W17/wd/bin/sep3r_gk8`.

| file | change |
|---|---|
| `code_gk8/gkfam.py` | `parse_key`: payer mask must be a nonempty subset of {5,6,7}, or exactly {8}, or exactly {9} (mixed sets such as {89}, {78}, B, * refused with a message to split them); a payer-8/9 key may not list S.L+3, S.L-3 (and, as for every key, R.L+-3, R.A+-1). `Win.counts`: the payer gate (`w_j <= 7`) is removed; payers 8/9 take the payer-7 branch (own privates wildcard). New `Win.out_vecs` / `Win.out_counts`: PAYER8SPEC 3.1 OUT slots of the centre U = min(d,9) -> w_i on the window W_i, SURE match, S.L+-3 = wildcard, sg = -1 mirrored (S.A+1 = s_{i-2}, S.A-1 = s_{i+1}, R.L+2 = s_{i-1}, R.L-2 = s_i); only at U >= 8, so a payer-8 key gets OUT only at d = 8 and a payer-9 key at d >= 9. `Win.row` = IN - OUT over every link position. Sender, cons2 and d = 7 pictures needed no change (link 8/9 privates were already wildcard; the matcher accepts any payer bit). |
| `code_gk8/st21_w17.py` | numpy window table `gk_window_tables`: same OUT term subtracted at U = 8, 9 (its IN part already gated on the payer bit, so 8/9 payers were already covered there). Header / comment lines. GKREL, GKWNP and the DP / Karp tail table may now be negative. |
| `code_gk8/gk_blocks.py` | self-test: planted IN payers drawn from 5..9; OUT slots planted for payer-8 keys at d = 8 and payer-9 keys at d >= 9; window-table test compares IN - OUT; per-position bound checks run at every link position (they skipped w_j >= 8); counts rows with a negative key coefficient. |
| `code_gk8/sep3r_gk.cpp` -> `wd/bin/sep3r_gk8` | key validation accepts payer 8 / 16 (refuses other masks with 8/9 bits, and positions 2/5 for them); `gkWinVal` has no payer gate and subtracts the OUT term at u >= 1 (U = 8, 9); `gkCorr` d = 7 IN loop and d >= 8 loop run over every link position; the C++ own-table max starts at -1e300 and negative GKREL cells are allowed. Compiled `nice -n 20 clang++ -std=c++17 -O3`. |
| `code_gk8/run17.sh`, `code_gk8/w17_upper.sh` | defaults point at code_gk8 and SEPBIN=sep3r_gk8. |
| `/tmp/swarm-W17/check8.sh` | check.sh calling `code_gk8/w17_upper.sh` with `W17CODE=code_gk8 SEPBIN=sep3r_gk8`; otherwise identical. |

With no payer-8/9 key loaded every change is inert (no key has payer bit 8/9, so the widened gate and the OUT term add nothing).

## md5

```
44b1c8235c9426241a90558914e4d250  /tmp/swarm-W17/code_gk8/gkfam.py
99d516b7488b3641dfd1cd21c91355d6  /tmp/swarm-W17/code_gk8/st21_w17.py
8061dd6de34071c7dc990c9b4bdd9348  /tmp/swarm-W17/code_gk8/gk_blocks.py
0ca3d4591fd53185cab7e6af8c839ea3  /tmp/swarm-W17/code_gk8/sep3r_gk.cpp
6fd98029ba7fae0faf8b41746ecee161  /tmp/swarm-W17/code_gk8/run17.sh
eeb814125eeef1aeda7bf88ae3c4556d  /tmp/swarm-W17/code_gk8/w17_upper.sh
8e61e5067b8ce410f514a8e1191237b6  /tmp/swarm-W17/check8.sh
849b8884e3480030f8e052e26320c2b9  /tmp/swarm-W17/wd/bin/sep3r_gk8
```

## How to run a check with payer-8/9 keys

Put the payer-8/9 keys in the GK key file (e.g. the 260 keys + the 24 w6b16s keys: `tests/cg_keys_k260_plus_w6b16s_p8.txt`, md5 71560114);
amounts come from the point's `ks` field as before. Use a fresh TAG.

```
cd /tmp/swarm-W17 && GK=<keyfile with payer-8/9 keys> RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt \
  F2BRULES=/tmp/swarm-W17/tab/rules_A5final_2db75746.json ARGSF=/tmp/swarm-W17/args_A97F_W13K3l5j_x_studio.txt EXPECT_PAT=18143,710,158 \
  TAG=<new tag> W17NICE=20 nice -n 20 bash /tmp/swarm-W17/check8.sh <point.json> 4
```

(`run_regr.sh` here is exactly this with the 260-key file, for T6.) A key file with a mixed payer set or an S.L+-3 condition on a payer 8/9 makes
the Python step stop with the parser's error.

## Tests (`tests/`, results in `test.log`; rerun all but T5/T6 with `bash tests/run_tests.sh`)

- T1 `t1_examples.py`: spec worked examples. R8 55558578/58585558: OUT 4 (slots i=0 sg-, 1 sg+, 2 sg-, 3 sg+), IN 0, coef -4. Sender S 55868 BSBBS {3:S}: IN 2 (payer w2 sg-, w4 sg+), coef OUT-IN = -2. PASS.
- T2 `t2_p8examples.py`: the 15 E examples of p8_test.json. code_gk8 equals value_B in all 15 (so the tuples are (row, key, planted-bug value, correct value)). One (outmirror, R9 756556695/556595557) depends on pmask: -6 with the patched298 stack and with pmask = all, -7 with pmask = none; -6 = B. The outposs keys constrain S.L+3, which the production parser refuses; T2 feeds them to the matcher raw.
- T3 `t3_indep.py`: independent set-based reading of 3.1/3.2 (own slot construction, frozensets, no gkfam matcher), 600 rows (100 each: receiver d = 8, 9, 10; d = 7 with a link 8/9; senders; cons2) x 440 keys (300 payer-8/9 W5, 80 payer-5/6/7, 60 payer-8/9 with an S.L+-3 condition fed raw) = 264,000 pairs, stub stack masks shared as data: 0 mismatches. Parser: 10 refusal cases and 4 acceptance cases as required.
- T4 (same script): planted gkfam variants vs T3: outposs 7,544 mismatches, outmirror 6,546. Both > 0: PASS. (outposs is only visible with keys that constrain S.L+-3: on exact singleton letters "possible" equals "sure" everywhere else.)
- TV `tv_p8vectors.py`: W6b's `in/p8_vectors` (coordinator's primary check). Pictures built by code_gk8's constructors; only stack masks code_gk8 cannot recompute without the GS14 / A97+F tables (6-privates, d = 7 7-privates, window amask ORs) are read from the reference IN slots and injected. Slot level: GS14_01 28,812 slots, c_A+c_B 2,256, c_C 10,676: 0 mismatches. (a) 13,152 (key, row) pairs: 0. (b) 14,016: 0. (c) c_C W5: 229 keys evaluated (71 skipped, payer set mixing 8/9), 91,600 pairs: 0 (also 0 on the parser-accepted subset and on the payer-exactly-8/9 subset; 56 of the evaluated keys are payer-8/9 with S.L+-3, which the parser refuses, fed raw). (d) 8 controls: code_gk8 gives the correct value in all 8 and the planted reading gives the stated wrong value in all 8; the 4 outposs control keys are also refused by the parser.
- T5 `t5_selftest.sh` (GKST_ONLY=1, code_gk8 + sep3r_gk8, K3l5j point): (a) 260 keys: C++ table = Python's (0 cells differ), numpy vs gkfam.Win 0 mismatches / 30,000 windows, C++ leaf vs Python rows 8,807 compared, 0 mismatches, per-position bound 91,800 positions, 0 above: PASS. (b) 260 + 24 keys, each new key at amount 0.01 (KSAMT): C++ table 0 cells differ, window test 0 / 30,000 (9,286 windows with negative credit), C++ vs Python 8,891 compared, 0 mismatches (d8 rows with a negative coefficient 2,999, d9 2,083, d10-12 ~460 each), bound check 0 above. Its VERDICT line says FAIL only because the artificial amounts make senderR2 / cons2 infeasible; the self-test itself passes.
- T6 `run_regr.sh` -> `regr_main.out`: no-payer-8/9 regression on the ST-86 point (see the result section below).

## Spec readings / ambiguities resolved

1. Payee sets stay free (any nonempty subset of {5..9}, as in the 24-key file); only the payer must be exactly {8} or {9} (task rule; spec 1 says a set is a sum of single-letter keys).
2. S.L+-3 on a payer-8/9 key is refused at parse time (task rule), not silently read as wildcard. By spec 5 that loses nothing.
3. The DP tail (d = 27..30) and the Karp closed-walk tail use GKREL at U = 9, which now includes the payer-9 OUT term. Spec 3.1 allows dropping OUT beyond the enumerated range; keeping it is sound by spec 4 (a real 9+ of any degree has the exact window letters and pays). If the coordinator prefers the conservative reading, the tail needs an IN-only U = 9 table; with no payer-9 amounts it makes no difference.
4. Chirality labels: spec 3.2 calls sg = +1 the slot with S.L+1 = w_{j-1}; gkfam's IN chirality e has S.L+1 = w_{j+e}, so spec sg = -e. Labels only; counts are identical.
5. d = 7: no payer-8/9 OUT exists (centre 7); the d = 7 window bound GKREL[U = 7] includes link-8/9 IN credit (the numpy table already did), and the C++ d = 7 leaf now re-reads it exactly (it skipped w_j >= 8 before).
6. GKORACLE (W6's round-9 r9_rows.py) predates payer 8/9 and was not updated; do not use it with payer-8/9 keys.

## Not done

- No new full feasibility run with payer-8/9 amounts (no point with such amounts exists here); T5b covers the C++/Python agreement with them.

## T6 result (regr_main.out; logs /tmp/swarm-W17/logs/sol_repK1MW_04__K3l5j_k260_gk8_regr)

code_gk8 + sep3r_gk8, 260 keys, no payer-8/9 key, tag sol_repK1MW_04__K3l5j_k260_gk8_regr, 4 processes, nice 20 (17:43Z-18:36Z):
**RESULT: FEASIBLE**. senderR2 min slack 2.26e-08, DP margin -0.651715, Karp lambda 0.763009862 (covered for d >= 25.250), every receiver
d = 7..26 exact violated 0 (separator reported 0), GK nonzero amounts 108 (sum 0.374364234). All of these match the code_gk7 run in
job_ST86/st86_main.out. The only differing output lines (other than timings and names) are the GK self-test counts: the self-test now plants
payers 5..9 and checks every link position, so it draws different random arrangements (8,807 vs 8,844 compared). Both runs had 0 mismatches.
(The brief's "81 nonzero amounts" does not appear in st86_main.out. Both runs print "nonzero amounts 108".)

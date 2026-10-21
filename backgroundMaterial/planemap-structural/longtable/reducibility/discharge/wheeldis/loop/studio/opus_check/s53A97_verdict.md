# s53 A97 [E2] upper (sol_q53A97.json at abf07125, md5 fa4d7844cdbcc556b47546d3539a6eb1): Studio spec-only check

**Verdict: FEASIBLE at t = 0.098789365409.** Receivers d = 7..17 are exhaustive with **0 violated**, DP d = 18..30 is clean, and
**Karp λ = 0.568812590**, the same as Opus's 0.568812590. No kill line was met. The V = 8 self-test is caught.

## Independence statement
I built this from RELAY_SPEC_s47.md (84475374) on s45 and s44 (V = 8 l3q) and the s39o / s40f / s21 specs, with my own st21_check.py,
st16_filter.py, l3q_masks.py and rpatN build, and bin/sep3r_l3q (SEP_L3Q8).

Opus files opened, as data only:
- s53/run_A97/sol_q53A97.json;
- s33z/reg_A97/{k3x_D_A97.out, k3x_C_A97.cfast, tab_±1.json, dcount.txt, args_A97.txt};
- s47/tabV8_A97/tabV8_±1.json;
- s39o/rpatN3.txt;
- s40f/exname_rm128.txt.

I diffed all of these only after building my own. I opened no Opus code, cmd script, rows file or log. Team B material: none.

## Inputs (Studio's A97 build = main 8ec00aea, s53/A97/README.md)
| item | Opus | Studio | result |
|---|---|---|---|
| k3x_D / k3x_C | d76bc52f / 9f8cfe39 | git show 8ec00aea | byte-identical |
| tab_1 / tab_−1 (l3q V = 7) | ab8fa57b / 8447bc72 | studio_l3qtab_±1 (190 of 30 per side) | equal entry by entry, 2 × 2,500, 0 mismatches |
| tabV8_1 / tabV8_−1 | b0115b14 / 38c23474 | studio_l3qtabV8_±1 (50 of 30 per side) | equal entry by entry, 0 mismatches |
| rpatN3 | e153fc41 | out/job31/s39o_rpatN3_studio.txt (my 39.2 / 39.6 build) | the same 2,287 patterns |
| exname_rm128 | b50f3551 | b50f3551 | identical; my held128 copies |
| rpatD.txt | — | 97235725 | as stated |
| args_A97 | d93b2bb3 | argsA97_local_rpat_held128.txt | Opus's differs from args_A83 only in the two k3x files; mine is the A83 local args with the same swap |
| dcount | newpat 18,097 | D 18,097, C 2,228, RPAT 158 | equal |

- **Forbidden set:** 4,949 configurations (582 RSST + 4,367 k3x). The kill tables are kill6 U7 27a64538 and U8 = U9 6dc44bba.
- **Ring-merge sweep at 8ec00aea:** 129 FAIL, the same set as the 129-FAIL set. That set minus f9_....5565B_....6655. = the held 128.

## The run (s53/s53_upper.log)
- **Flags:** l3q lqcap 3, l3qV = 7,8 (L3Q8, V = 8 tables above), rpatN3, hat5, the 14' kill tables, xcap 3. fb off, xo off.
- **Isolation:** its own SEPTAG s53run (pattern file md5 8d9f7f31, 4 loads 16,500 / 4,317 / 6,604) and its own solution copy.
- **Calibration:** d ≤ 8.
- **Solution:** t = 0.09878936540884199. There are 6 V = 8 payer keys and 4 V = 8 lQ8 keys:

| key | value |
|---|---|
| lq(8,5,6,5) | 0.017660 |
| lq(8,6,5,6) | 3.5e−14 |
| lq(8,6,6,5) | 0.067410 |
| lq(8,6,6,6) | 0.061104 |
| lq(8,6,6,7) | 0.049964 |
| lq(8,6,6,8) | 0.021563 |
| lQ8(8,6,6,31) | 0.067410 |
| lQ8(8,5,6,31) | 0.017660 |
| lQ8(8,6,5,30) | 3.5e−14 |
| lQ8(8,6,6,30) | 0.061104 |

- **V = 8 slack (mrowL at Qeff8, over every table mask and every a2 in it):** 0 violated. Each lQ8 equals the largest lq8 over its
  mask, so the rows are tight by construction. UB8(6,6) = 0.067410.
- **Checks:**
  - bounds: clean (max x 0.135);
  - senderR2: 20,676 rows, 0 violated (min slack −1.2e−14);
  - cons2: 994 + 430 words, 0 violated (max 2.4e−14);
  - mrowL (V = 7 and V = 8): 0 violated;
  - leaf vs spec rows: 4.1e−10; relaxed vs spec on 640 arrangements: 0 below exact.
- **Receivers d = 7..17 (exhaustive): 0 violated at every d.** d = 8 rows carry the V = 8 payee terms, and d = 7 rows the payer terms at
  link 8s.
- **DP d = 18..30:** clean (z9 = 0.134819).
- **Karp λ = 0.568812590,** covering d ≥ 13.686.

## Self-test (s53/s53_selftest_perturbV8.log)
- **The perturbation:** lq(8,6,6,5) = 0.5 (the binding V = 8 payer key; Q left to Qeff8), with its own SEPTAG s53self and solution
  copy, d ≤ 8.
- **Result: caught.** d = 7 has 0 violated. **d = 8 is violated at the 5,000 cap**, at load 4.1376 against a limit of 2.0988 (e.g.
  link 76767656 / s 66666556): the payee credit Qeff8 rises to 0.5 at the 6-6 link 7s.

## Lower
Not part of this check. Opus's A97 lower (cert_q53A97L) will be checked with lowerR2 when it arrives.

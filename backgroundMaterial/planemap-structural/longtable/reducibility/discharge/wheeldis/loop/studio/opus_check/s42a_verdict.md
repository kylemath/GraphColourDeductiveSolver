# s42a (l3q + rpatN3 on registry A78 = main b6dc7610, 128 ring-merge FAIL entries held out): Studio spec-only check

**Verdict: claim confirmed: 44/421 <= t* <= 0.109439356774** (the upper is at float t = 54719678387/500000000000).
**Upper FEASIBLE at t = 0.109439356774** (21 Oct, finished before 03:27Z) and **lower VALID at 44/421 (= 0.104513064)**. No kill line
was met: no violated row, no cert failure, and no mismatch in inputs or tables. **80/731 (= 0.109439124) is NOT feasible with this
solution.** At t = 80/731, 6,246 senderR2 rows of sol_q42aA78 come up short, by at most 2.32e-7. These rows are tight at the
float t, which lies 2.3e-7 above 80/731. This statement covers only this x, not the LP optimum.

## Independence statement
I built this check from RELAY_SPEC_s39o.md (39.1, 39.2 and 39.6) on top of RELAY_SPEC_s21: reading A, and the mrowL label
order [lQ key, lq key] of 11a19fb0. Sections 12, 14' and 15 are used as for s28q, s33z and s39o. Apart from the specs, I opened
only data files: s42a sol_q42aA78.json, cert_q42aA78L.json and sol_q42aA78L.json (md5 only), plus the registry data
args_A78.txt, k3x_D_A78.out, k3x_C_A78.cfast, tab_+-1.json and md5_prep.txt. I diffed against the registry tables only after
building my own. I opened no Opus code, cmd script, cons basis, rows file or log. cons2 is checked over all 1,424 x 729 words.
rpatN3 is my own build from 39.2 / 39.6 (out/job31/rpatN_studio.py; 2,287 patterns, the same set as for s39o). Team B
material: none.

## Inputs
- md5s: sol 8773a6dc; cert 0c88b25b; solL 6971c2df; exname_rm128.txt b50f3551 (128 names plus a header line); args_A78.txt
  4c355c3d; k3x_D 6b07b89b; k3x_C 428f7ce1. These are byte-identical to main b6dc7610 and to reg_A78/md5_prep.
- **Held out: the 128 ring-merge FAIL entries.** exname_rm128.txt is identical to Studio's held128 list (out/job30/held128/:
  69 + 59 blocks removed from the job27 part00 / part01 copies). Args used: s42a/argsA78_local_rpat_held128.txt (md5 75703ad0).
- Pattern counts by kind: D 17,700 (= the dcount), C 2,088, RPAT 158; rpatN 2,287; 6,076 full patterns in the separator.
  The lower log prints a line "FAIL: pattern counts (17700, 2088, 158) differ from expected (17700, 0, 158)". That line is
  a typo in the EXPECT_PAT I passed to that run: I set the C count to 0 instead of 2088. Both runs loaded the same
  17,700 / 2,088 / 158, and the upper run, given the correct expectation, prints no such line. This is not a kill line.

## Tables (Studio rebuild; forbidden set = RSST + A78 k3x)
- **Section 14' kill tables match reg_A78/md5_prep:** kill6_U7 has md5 27a64538, and U8 and U9 share md5 6dc44bba.
- l3q masks (out/job31/l3q_masks.py, reading A): 190 of 30 and 2,310 of 31 per side. I compared them entry by entry with
  reg_A78 tab_+-1.json, mapping the registry key "c w2 w3 w4 a o" to Studio's row order (c, a, w2, w3, w4, o).
  **All 2,500 entries per side are equal, with 0 mismatches.**
- mrowL over every table mask and every a2 in it, at Qeff: 0 violated.

## Upper (s42a/s42a_upper_float.log)
- **Bounds:** clean (max x 0.195, cap 3).
- **senderR2 and cons2:** 0 violated. senderR2 has 20,676 rows, min slack -1.55e-15. cons2 covers 994 five-words + 430
  nofive words x 729, max |difference| 4.75e-15.
- **Separator checks:**
  - d = 7 l3q leaf calibration: 3,000 heaviest, 2,881 of them with l3q terms, max |difference| 2.26e-10.
  - exact leaf vs spec rows for d = 7..12: 3,100 compared, max 4.47e-10.
  - relaxed vs spec rows: 3,700 arrangements, 0 mismatches.
- **Receivers d = 7..17, exhaustive with rpatN3: 0 exact violators at every d.**
- **Tail:** DP over d = 18..30 is clean (z9 = 0.107343). **Karp lambda 0.573063347 covers d >= 13.797.**

## Lower (s42a/s42a_lower.log)
- **Cert:** 155 rows (22 senderR2, 86 cons2, 5 mrowL, 29 mrowR2, 13 receiverR2), all in canonical orientation. tco = 1,
  **D = 44/421**.
- **Reduced costs:** the nonzero ones are M[767685531], M[866675531] and M[876675531] at 12/421 each, h[76657875] 24/421,
  r[506506] 8/421, r[506507] 44/421, r[506509] 12/421, r[507507] 12/421 and r[507508] 24/421. **None is negative.**

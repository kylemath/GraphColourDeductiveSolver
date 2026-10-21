# s44 A83 [E2] pair (registry A83 = main 240b5a08, 128 rm128 held out): Studio spec-only check

## Independence statement
I built this from RELAY_SPEC_s39o §39.6, s40f, RELAY_SPEC_s44 (§44.3 caps, §44.8) and the earlier s21 / s28q / s33z specs. I opened
only data files:
- sol_q44fbA83.json (9757148b);
- cert_q44nfA83L.json and sol_q44nfA83L.json (9dd82e31);
- the reg_A83 data: args_A83, k3x_*_A83, tab_±1, md5_prep, dcount.

I diffed against those only after building my own k3x (from main 240b5a08), kill tables, l3q masks and ring-merge sweep. I opened no
Opus code, cmd script, rows file or log. Team B material: none.

## Registry (Studio's build)
- **k3x:** at 240b5a08, D 14296fb6 and C 947219ed, byte-identical to reg_A83.
- **args:** args_A83 = args_A78 with the two k3x files swapped.
- **Forbidden set:** 582 RSST + 3,918 k3x = 4,500.
- **Kill tables:** kill6 27a64538 / 6dc44bba, equal to reg_A83 md5_prep.
- **l3q masks:** 190 of 30 per side, equal to reg_A83 tab_±1 (0 mismatches).
- **dcount:** D 17,744, which equals reg_A83 newpat 17,744 (C 2,132, RPAT 158).
- **Ring-merge sweep at A83:** 129 FAIL, the same set as a2ec92e5. That set minus f9_....5565B_....6655. = exname_rm128 = Studio's held128.

## LOWER (cert_q44nfA83L.json, 9dd82e31, md5 ea86f98d, 256 rows): **VALID t >= 132/1301 exactly**
- **Configuration:** the s42a lower configuration unchanged: l3q (lqcap 3), rpatN3, fb off, xcap 3, the A83 tables above.
  Log: s44A83/lower_cert_q44nfA83L.log.
- **Rows:** 41 senderR2, 120 cons2, 15 mrowL, 47 mrowR2, 33 receiverR2, all labels admissible and in canonical orientation. tco = 1.
  **D = 132/1301 (0.101460415), exactly the claim.**
- **Reduced costs: none is negative.** The nonzero ones are all > 0, the smallest 6/1301 (r[5059]) and the largest 2522/29923.
  **No column is priced at a cap:** no x or lq column has rc < 0, so no cap term enters the bound.
- **Self-test:**
  - **a free cons2 multiplier shifted by +0.001:** caught, with 2 negative g columns (rc −292436701/146218350501 each), INVALID;
  - **one receiverR2 multiplier scaled by 1.02:** caught as a claim mismatch. The cert stays dual-feasible (0 negative columns) but
    gives the weaker D = 150895/1496331 = 0.100843 ≠ 132/1301.

## UPPER (sol_q44fbA83.json, 9757148b, md5 cfc41a44; claim FEASIBLE at t = 0.105883918328): in progress
- **Inputs:** 73 fb6 values, max 2.65e−13, all in [0, 3], all keys fbdir = 6.
- **Clean so far:**
  - senderR2: 20,676 rows, 0 violated;
  - cons2: 994 + 430 words, 0 violated; with fb, all 1,424 × 5^6 apex words, 0 violated;
  - mrowL: 0 violated.
- **Self-test:** the largest fb amount set to 0.5 is caught (cons2 with fb violated 100, max 0.5).
- **(a) fb on and (b) fb off:** receivers d = 7, 8 have 0 violated each; the runs continue to d = 17, then DP and Karp.

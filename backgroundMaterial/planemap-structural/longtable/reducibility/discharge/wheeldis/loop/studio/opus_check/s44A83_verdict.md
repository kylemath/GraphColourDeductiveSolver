# s44 A83 [E2] pair (registry A83 = main 240b5a08, 128 rm128 held out): Studio spec-only check

**Verdict: confirmed, 132/1301 <= t* <= 0.105883918328** (lower VALID exactly; upper FEASIBLE with fb on and with fb off).

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

## UPPER (sol_q44fbA83.json, 9757148b, md5 cfc41a44; claim FEASIBLE at t = 0.105883918328): **FEASIBLE, both ways**
- **Inputs:** 73 fb6 values, min 1.3e−14, max 2.65e−13, all in [0, 3], all keys fbdir = 6.
- **Senders and conservation:** senderR2 20,676 rows, 0 violated (min slack −8.0e−13). cons2 994 + 430 words, 0 violated (max 3.4e−12).
  With fb on, cons2 over all 1,424 × 5^6 exact apex words: 0 violated (max 3.4e−12). mrowL: 0 violated.
- **Separator calibration:** exact leaf vs spec rows, heaviest 20 per d for d = 7..17: max 4.6e−10. Relaxed vs spec on 820 arrangements:
  0 below exact.

| run | receivers violated (d = 7..17, exhaustive) | worst | DP d = 18..30 | Karp λ (Opus 0.572809) | verdict |
|---|---|---|---|---|---|
| (a) as given, fb on (fbdir 6, fbcap 3) | **0** at every d (the relaxation reports 0 above the threshold d − 6 + t at every d) | none | clean (z9 = 0.109540) | **0.572808649**, covers d ≥ 13.797 | **FEASIBLE at t = 0.105883918328** |
| (b) fb zeroed and the family off | **0** at every d | none | clean | **0.572808649**, covers d ≥ 13.797 | **FEASIBLE at t = 0.105883918328** |

- **What the fb amounts do here:** they are ≤ 2.65e−13 and change nothing at this precision: (a) and (b) agree line for line.
- **Self-test:** the largest fb amount set to 0.5 is caught, with cons2 (with fb) violated on 100 words (max 0.5), FAIL.

## Race re-check (21 Oct, after the SEPTAG finding) and solo re-run of (a)
- **The shared file:** every st21_check run wrote the shared separator pattern file bin/sep3_s16chk.in, plus tables named after the
  solution basename (out/job31/st16/{l3q,ex6,rtab,fb}_<sol>.bin).
- **(b):** fb off, so it reads no fb table. Its l3q, ex6 and rtab tables are identical in content across the concurrent A83 runs (same
  solution). Its 4 logged separator loads (patterns 16,495, full 3,873 / 6,160) equal a solo A83 build (pattern file md5 29c64e9d,
  39,228 lines). **Clean.**
- **(a):** it shared fb_sol_q44fbA83.bin with the concurrent fb self-test (fb set to 0.5). That could have lowered receiver loads, and
  the logs cannot prove which version it read. So **(a) was re-run solo**:
  - SEPTAG a83rerunA, with its own solution copy (fb_sol_q44fbA83_rerunA.bin); calibration at d = 7 only;
  - pattern file bin/sep3_a83rerunA.in, md5 **29c64e9d** = the solo A83 build; 4 loads, all 16,495 / 3,873 / 6,160;
  - result: receivers d = 7..17 exhaustive, **0 violated**; DP d = 18..30 clean (z9 = 0.109540); **Karp λ = 0.572808649**, covers
    d ≥ 13.797; **FEASIBLE at t = 0.105883918328** (log s44A83/upper_a_fbon_rerun.log). The same as the first run.
- **The lower check:** it reads no separator file (LOWER_ONLY exits before any separator table or pattern file is read or written).
- **From now on,** every run uses its own SEPTAG and its own solution copy.

## Verdict
**A83 [E2] pair confirmed: 132/1301 (0.101460) <= t* <= 0.105883918328.** The lower is exact, with no cap term; the upper is FEASIBLE
with and without fb. No kill line was met.

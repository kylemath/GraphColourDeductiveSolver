# s28q (l3q, RELAY_SPEC_s21 md5 321660a8; sol_s28A62.json md5 2953842b, cert_s28A62L.json md5 dff0dc53; Opus 3e9b61bd):
# Studio spec-only check

**Verdict: claim confirmed.** On registry 3cfd7f18 (argsA62, dcount 17,437): **upper FEASIBLE at t = 0.147790407823**
and **lower VALID at 11/75** (20 Oct 01:07Z). No kill line met: no infeasibility, no invalid cert row, no mask-table
mismatch.

## Independence statement
Built from RELAY_SPEC_s21.md (with sections 12, 14', 15 as in st24b) and the data files only. Opus files opened:
RELAY_SPEC_s21.md, eng/sol_s28A62.json, eng/cert_s28A62L.json, s31/argsA62.txt, the pattern / row count lines of
s28A62.log and s28A62L.log (grepped), and tab62_1.json / tab62_-1.json, read only after Studio's own tables were built
and only for the diff. No eng/ code, jsep5.cpp, cmd script, cons basis, rows file, l3qtab.py, mask28.py, pricer28.py or
other code was opened; file names in s28q/ were seen via git ls-tree only.

## Studio tools (all Studio-written)
- out/job31/l3q_masks.py: section 21.4 mask tables on explore's grow.py (build2, embeddings), strict rule, forbidden set
  = RSST D2 / C2cons (582) + kc lines of 3cfd7f18's k3x (2,397 D + 1,010 C) = **3,989**.
- out/job31/st21_check.py: st18_check.py + section 21 (payer / payee terms at d = 7, Qeff, mrowL, lq priced at lqcap).
- bin/sep3r_l3q (sep3r_l3q.cpp): sep3r_ak + opt-in SEP_L3Q, the section 21.6 route: relaxed window term
  UB(w_{i+1}, s_i) + UB(w_{i-1}, s_{i-1}) at a d = 7 link 7, exact payee Qeff and payer -q at the leaf. The frozen
  sep3r is untouched (sha matches FROZEN.txt).

## Mask tables
- Studio's tables: 5,000 masks, **380 of 30 (letter 5 killed), the rest 31** (190 per side), as the spec states.
- **Diff vs tab62_±1: 0 mismatches on 5,000**, under the key reading "sigma c w2 w3 w4 a o" (the only one of the 720
  digit layouts with 0 mismatches). md5 of Studio's files (both sides identical content) 22e1f5ef...; tab62_1.json
  ab8fa57b..., tab62_-1.json 8447bc72....
- **Spec ambiguity, section 21.4 "a letter is killed when some embedding uses only known vertices plus a2 at that
  letter":** (A) the embedding must use a2 (as section 14'), giving the stated 380 / 30; (B) an embedding avoiding a2
  kills every letter, giving 60 masks of 0. **(A) matches**; 3 of the 15 requirement sets per side avoid a2.

## Results
- Inputs: md5s match; argsA62 mapped to local paths (the job28 r_5..r_8, k42map and 3cfd7f18 k3x files are
  byte-identical to Opus's). dcount **17,437** (17,771 names). Ring-merge holds: the 3 entries are not in 3cfd7f18's k3x.
- Pattern counts D 17,437 / C 2,056 / RPAT 158 equal s28A62.log **with** loop/studio/rsstD/out/rpatD.txt; argsA62
  itself has no rpat= line (reading: Opus's loader adds the 158 RSST raw patterns; the lower cert is VALID either way).
  Distinct-by-d counts differ slightly from the log (d7 9,699 vs 9,702, d8 5,106 vs 5,110, d9 2,934 vs 2,941;
  totals by kind equal): a counting convention, not an input difference.
- l3q solution: q(6,5,5) 0.0504, q(6,6,5) 0.0369; lQ (6,5,31), (6,6,31) equal; UB(6,5) 0.0504, UB(6,6) 0.0369, else 0.
  mrowL at Qeff over every table mask and every a2 in it: 0 violated.
- Upper: bounds clean (max x 0.109); senderR2 20,676 rows, 0 violated (min slack -8.9e-13); cons2 1,424 x 729: 0
  violated (max 1.6e-12); relaxed vs spec rows 720 arrangements, 0 mismatches; sep exact leaf vs spec rows 120 (d 7..12)
  max 1.8e-10, and **d = 7 l3q leaf: 3,000 heaviest, 126 with l3q terms, max 1.8e-10**; receivers d = 7..17
  exhaustive: **0 exact violators at every d**; DP d = 18..30 clean; Karp lambda 0.549179, covers d >= 12.981.
- Lower: 109 rows (18 senderR2, 56 cons2, 26 mrowR2, 9 receiverR2; no mrowL), all mrowR2 canonical, tco = 1,
  **D = 11/75**; nonzero reduced costs all >= 0: M[766767531] 1/75, h[76757677] 1/75, r[506506] 1/15, r[506517] 2/75,
  r[5157] 2/75. The cert's d = 7 rows carry no l3q term, so no lq / lQ reduced cost arises.
- Descriptive only: g2 keys in sender rows 381 (spec 12.3's 393), as in earlier checks.
Logs: s28q/s28q_upper.log, s28q/s28q_lower_argsA62_local_rpat.log (and _argsA62_local.log, no rpat),
s28q/s28q_l3qleaf_test.log (its DP lines are from a DMAXP = 7 test run and are not a result), studio_s28q_dcount.txt.

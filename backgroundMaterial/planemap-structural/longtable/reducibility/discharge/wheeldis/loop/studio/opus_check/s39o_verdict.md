# s39o [E2] (l3q + rpatN3 on registry A74; sol_q39n3A74.json md5 2680fb64, cert_q39n3A74L.json md5 9ba47b69; Opus
# baa885e2): Studio spec-only check

**Verdict: claim confirmed: 20/183 <= t* <= 1/9.** On A74 (main 95ba762d, 2,645 D / 1,156 C, dcount 17,685, + rpatD 158 +
rpatN3 2,287): **upper FEASIBLE at t = 1/9** and **lower VALID at 20/183 (= 0.109289617)** (20 Oct 21:59Z). No kill line
met: no violated row, no cert failure, no input, pattern-set or table mismatch.

## Independence statement
Built from RELAY_SPEC_s39o.md (39.1, 39.2, 39.6) on top of RELAY_SPEC_s21 (reading A, mrowL label order of 11a19fb0) and
sections 12, 14', 15 as for s28q / s33z, and the data files only. Opus files opened: s39o/RELAY_SPEC_s39o.md,
run_n3_A74/sol_q39n3A74.json, cert_q39n3A74L.json, sol_q39n3A74L.json (md5 only), s33z/reg_A74/{args_A74.txt, k3x_D_A74.out,
k3x_C_A74.cfast} (byte-compared with main), and, for the diff only and after Studio's own were built, s39o/rpatN3.txt,
reg_A74/f/kill/kill6_U{7,8,9}.npy and reg_A74/md5_prep.txt. Explore's loop/k51/nl51_kc.txt (6368d2f5) is the rpatN3
source. No code (rpatN_build.py, rpatN_funnel.py, eng/, pcheck.py, offc.py), cmd script, cons basis
(s21/cf/cons2basis_cls.json not opened; Studio checks cons2 over all 1,424 x 729), rows file or log was opened; file names
were seen via git ls-tree only.

## Inputs
- md5s: spec b6afd3e4, sol 2680fb64, cert 9ba47b69, solL ef795f4d, nl51_kc b9bc6e8b (8,200), rpatN3.txt e153fc41 (2,288).
- 95ba762d k3x_D/C = reg_A74 (md5 3c71d994 / 14bbdeed), byte-identical; 2,645 D / 1,156 C; dcount 17,685 (= aaa0649e).

## rpatN3 (Studio's own build, out/job31/rpatN_studio.py, from 39.2 / 39.6 only)
- **2,287 patterns, the same set as Opus's rpatN3.txt** (0 Studio-only, 0 Opus-only after Studio's canonicalisation); by d
  d7 621, d8 839, d9 631, d10 188, d11 7, d12 1. The 39.6 funnel reproduces: 8,200 configurations, 53 with no centre,
  2,191 with a u-centred embedding, 18,593 centres, 2,455 (configuration, pattern) pairs, 2,287 patterns (Studio counts
  5,238 embeddings with c's first neighbour fixed at w_0, a rotation quotient of the spec's 42,998).
- Wired in as RPATN (Python admissible) and SEP_FULLX (bin/sep3r_l3q whole-arrangement patterns, N = {6,7,8,9}); the
  separator loads 6,047 full patterns (3,760 + 2,287).

## Tables (Studio, A74 forbidden set = 582 RSST + 2,645 + 1,156 = 4,383)
- Section 14' kill tables kill6_U7 md5 27a64538, U8 = U9 6dc44bba: equal to reg_A74 (and to Studio's earlier tables).
  l3q masks: 380 of 30, rest 31, equal to reg_A74 tab_±1 (= tab62).

## Results
- Upper (s39o/s39o_upper.log): bounds clean (max x 0.158); senderR2 20,676 rows, 0 violated (min slack -8.2e-13); cons2
  1,424 x 729: 0 violated (max 1.2e-12); mrowL at Qeff over every mask and a2: 0 violated; d = 7 l3q leaf: 3,000 heaviest,
  1,236 with l3q terms, max |difference| 1.1e-10; exact leaf vs spec rows 3,100 (d 7..12) max 4.9e-10; relaxed vs spec
  rows 3,700 arrangements, 0 mismatches; **receivers d = 7..17 exhaustive with rpatN3: 0 exact violators at every d**; DP
  d = 18..30 clean; **Karp lambda 0.555555556, covers d >= 13.250**.
- Lower (s39o/s39o_lower.log): 160 rows (15 senderR2, 101 cons2, 29 mrowR2, 10 receiverR2, 5 mrowL); all 10 receiverR2 rows
  admissible with rpatN3; tco = 1, **D = 20/183**; nonzero reduced costs M[766675531] 4/61, r[506507] 2/183, all >= 0.

## The 10 job27 C entries held by the ring-merge sweep (ca350e1b)
- These 10 cpat entries (job27 part00 / part01, e7_B5*B565_*_1111111) are in args_A74 but have no ring-distinct C X
  (out/job30/ringmerge_cpat_sweep.out). They are now held out of every Studio args file (out/job30/held10/).
- Dependency (out/job30/ringmerge_cpat_dep.out, c799c5bc): the 10 are the sole match for 5,400 d = 7 arrangements in their
  frames; the maximum exact load among those is 1.0638 < 1 + 1/9, so **the 1/9 upper does not depend on them**; all 10
  receiverR2 rows of the cert are admissible with them included, so **the lower does not depend on them**; the kill
  tables and l3q masks (forbidden set RSST + k3x) do not change. Long Table also accepts the upper via Opus's 130-entry
  C cover.
- Descriptive only: g2 keys in sender rows 381 (spec 12.3's 393), as in earlier checks.

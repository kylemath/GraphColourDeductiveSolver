# s33z (l3q on registry A67; sol_q66.json md5 6dd8178d, cert_q66L.json md5 096a717b; Opus 93b85890): Studio spec-only check

**Verdict: claim confirmed.** On registry A67 (main 2c97e14d out/job30: 2,555 D / 1,097 C, dcount 17,595, + rpatD 158):
**upper FEASIBLE at t = 0.128957775395** and **lower VALID at 55686/438047 (= 0.127123345)** (20 Oct 09:20Z). No kill
line met: no violated row, no cert failure, no dcount or input mismatch, no table mismatch.

## Independence statement
Built from RELAY_SPEC_s21.md (section 21, mrowL label order as fixed at 11a19fb0) with sections 12, 14' and 15 as in
st24b / s28q, and the data files only. Opus files opened: run_A67/sol_q66.json, run_A67/cert_q66L.json, s33z/argsA67.txt,
s33z/reg_A67/k3x_{D,C}_A67 (byte-compared with main 2c97e14d), P_own_lp/rpatD.txt (byte-compared), and, for the diff
only and after Studio's own tables were built, reg_A67/f/kill/kill6_U{7,8,9}.npy, reg_A67/tab_±1.json and the
ccover/A67 no-C variants. No code, cmd script (resume_s33.sh not opened), cons basis, rows file or log was opened; file
names in s33z/ were seen via git ls-tree only.

## Inputs
- md5s match (sol 6dd8178d, cert 096a717b). argsA67 mapped to local paths (job28 r_5..r_8, k42map byte-identical);
  k3x_D/C = main 2c97e14d out/job30 = reg_A67, byte-identical; 2,555 D / 1,097 C; the 3 ring-merge entries absent;
  rpatD identical. dcount **17,595** (17,929 names). Pattern counts D 17,595 / C 2,143 / RPAT 158.
- Solution families: as s28q plus empty zr / z6 / Z6 / l6r (all empty or off). l3q: q(5,6,5) 0.0276, q(6,5,5) 0.0301,
  q(6,6,5) 0.0301; lQ at mask 31 equal.

## Tables (Studio, from the spec, A67 forbidden set = 582 RSST + 2,555 + 1,097 = 4,234)
- Section 14' M kill tables (out/job31/st16_filter.py, K3X = the A67 pair): kill6_U7 md5 27a64538, U8 = U9 md5 6dc44bba,
  **0 mismatches** against reg_A67/f/kill (and identical to Studio's earlier st16 tables, so registry growth since
  09d8ac38 adds no window kill). l3q masks (out/job31/l3q_masks.py, reading A): 380 masks of 30, rest 31; **0 of 5,000
  mismatches** against reg_A67/tab_±1 (= s28q's tab62).
- ccover/A67 (Opus's deliberate no-C variant, not part of the bound) is strictly weaker: U7 51,350 killed bits against
  64,544 (11,704 entries differ, all one way); 280 l3q masks 31 where the with-C masks are 30.

## Results
- Upper (s33z/s33z_upper.log): bounds clean (max x 0.091); senderR2 20,676 rows, 0 violated (min slack -5.8e-13);
  cons2 1,424 x 729: 0 violated (max 2.7e-12); mrowL at Qeff over every table mask and every a2 in it: 0 violated;
  **d = 7 l3q leaf: 3,000 heaviest rows, 2,888 with l3q terms, max |difference| 4.0e-10**; sep exact leaf vs spec rows
  3,100 compared (d 7..12), max 4.0e-10; relaxed vs spec rows 3,700 arrangements, 0 mismatches; **receivers d = 7..17
  exhaustive (bin/sep3r_l3q, SEP_EXACT6 + SEP_RTAB + SEP_L3Q): 0 exact violators at every d**; DP d = 18..30 clean
  (z9 0.0602); **Karp lambda 0.553931244, covers d >= 13.162**.
- Lower (s33z/s33z_lower_withC.log): 401 rows (66 senderR2, 206 cons2, 72 mrowR2, 45 receiverR2, 12 mrowL), all mrowR2
  canonical, every mrowL label valid (a2 in m, w <= 0), tco = 1, **D = 55686/438047**, every reduced cost >= 0.
- Spec point (now fixed in section 21.3 at 11a19fb0): the mrowL label is ['mrowL', [c, a, m], [c, a, a2]]; Studio's reader
  matches it. A first lower run read the order the other way round and failed on labels only.
- Descriptive only: g2 keys in sender rows 381 (spec 12.3's 393), as in earlier checks.

## Re-check with the 10 ring-merge-held job27 C entries removed (Long Table 20 Oct 20:56Z), 20 Oct 23:25Z
The ring-merge sweep (ca350e1b) found 10 job27 cpat entries (part00 6, part01 4; e7_B5*B565_*_1111111) with no ring-distinct C
X. They are held out (out/job30/held10/; args loop/studio/opus_check/s33z/argsA67_local_rpat_held10.txt; C patterns
2,143 -> 2,133, d = 7 9,706 -> 9,696). The section 14' kill tables and l3q masks do not change (forbidden set RSST + k3x).
- **sol_q66 upper still FEASIBLE at t = 0.128957775395** with them held out (s33z/s33z_upper_held10.log): bounds clean;
  senderR2 20,676 rows 0 violated; cons2 1,424 x 729 0 violated; mrowL 0; d = 7 l3q leaf 3,000 rows (2,888 with l3q terms)
  max 4.0e-10; relaxed vs spec rows 3,700, 0 mismatches; receivers d = 7..17 exhaustive, 0 exact violators; DP d = 18..30
  clean; Karp lambda 0.553931244, covers d >= 13.162. Hypothesis met, kill line not met.
- Arrangement dependency (out/job30/ringmerge_cpat_dep.out, c799c5bc): the 10 are the sole match for 6,111 d = 7
  arrangements, max exact load 1.0904 < 1.1290; all 45 receiverR2 rows of cert_q66L are admissible with them included,
  so the lower 55686/438047 does not depend on them either.

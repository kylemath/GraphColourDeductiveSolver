# W6b round 11 (RSST-SUB): substitutes for the "none" configs the RSST fixed point needs

(Saved by the lead from W6b's hand-back, 10 Nov 2026 ~12:50Z. The full write-up is SUBSTITUTES.md. MD5SUMS 060f767f; this REPORT.md is not in it. [P], container engines.)

**Result.** Every state that needed a "none" config now has a substitute that our existing admissibility accepts:
- (a) the d7/d8 rows;
- (c) d = 9/10;
- (b) the literal cons2 probe.

That keeps the valid_contract Lean port off the critical path for every row checked so far.

**(a) The 5 none-dependent d7/d8 rows.** All 244 open combos are covered (168,304 fillings). The greedy set:
- nl2837_r11 (D; it covers the 2.126 rows; alternative nl6401_r14)
- nl3352_r13 (D; 124.1324817; alternative nl3357_r13)
- fix_63c8a193fe (C, ring 14, interior {u, w0..w6, s0, s1, s5}, X = {I3-I9, I7-I8, R12-I8, R0-I9}, kc -C plus cfast --fixed; 128.1324802)

Notes:
- No 2026 config occurs in the 84 combos of 128.1324802, and no D window was found up to ring 16. The 66 ring-17/18 windows are still unscreened.
- All 31 C windows pass both Gonthier's valid_contract and our Lean admissibleX.
- K3gB5n misses these hits because they are off-centre or use privates.

**(c) d = 9/10.**
- W6b reran W6r's enumeration with the cap removed (one-line patch to a copy of d9bb.cpp). The counts are the same, 31,139 + 409 states, now complete.
- The 2026 set kills all 31,548 states. The greedy cover has 37 configs, all D on kcc_o3 and dfast18:
  - nl0004_r8 nl2638_r12 nl0078_r11 nl0026_r12 nl7574_r13 nl0050_r10 nl2828_r13 nl2656_r13 nl0019_r11 nl2636_r12 nl2637_r12 nl2676_r13
  - nl2737_r14 nl0013_r10 nl7749_r13 nl2660_r13 nl2675_r13 nl7287_r12 nl7264_r12 nl2759_r13 nl2803_r13 nl2726_r13 nl7313_r12
  - nl2653_r12 nl7579_r13 nl7383_r13 nl7476_r14 nl7659_r13 nl0008_r9 nl8062_r13 nl2756_r13 nl2669_r13 nl0067_r10 nl0018_r11
  - nl2804_r13 nl7734_r14 nl2686_r15
- Per none config, the covering configs are in d9plus/d9_by_noneconfig.tsv.

**(b) cons2 literal probe** (W6b's own reading of the apex letters; privates 5..9; 582 kills):
- 9 labels were tested. 6 have one combo left that only 2.126 kills.
- nl0004_r8 (D) covers 5 of the 6.
- fix_404d45e819 (C, ring 13, X = {I0-I2, I4-I5, R11-I2, R4-I5}, valid_contract and admissibleX True) covers all 6.
- The full set of 240 cons2 labels was not run.

**Not verified:**
- the C windows end to end through the Lean C path;
- a D window for 128.1324802 at ring 17/18;
- the d ≥ 9 placement convention, which is assumed equal to K582's;
- the cons2 apex convention.

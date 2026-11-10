# RSST-SUB: substitutes for the "none" configurations

W6b, 10 Nov 2026, [P], my engines plus W13's.

- **Rows, groups and matcher:** my fp2 engine (round10_rsstfp2, fp2.py 0c4804e2). The matcher is induced, with exact letter = degree, anywhere among the hosts.
- **Windows:** W13's mscreen.py (dc8b622c), running /tmp/swarm-W13/bin kcc_o3, dfast18 and cfast.
- **d = 9/10 states:** exported from W6r's d9bb with only the 400-state export cap lifted.
- All heavy runs went through cpuslot (tag W6b-RSSTSUB), at most 2 slots.

## Result

### (a) The 5 none-dependent d7/d8 rows no longer need a none configuration

After the 582 kills, 244 open combinations remain: 168,304 fillings by the spec count. Each group has exactly one open minimal combination.

| row (set) | none config | open groups = combos | fillings (spec) | 2026 configs in every combo | substitute |
|---|---|---|---|---|---|
| T 8 56765767 56655555 | 2.126 | 72 | 1,152 | nl2837_r11, nl6401_r14 | **nl2837_r11** (D) |
| B 8 76576756 65555556 | 2.126 | 72 | 1,152 | nl2837_r11, nl6401_r14 | **nl2837_r11** (D) |
| B 7 8557766 7565755 | 124.1324817 (2.126 also) | 16 | 40,000 | nl3352_r13, nl3357_r13 | **nl3352_r13** (D) |
| B 7 8565766 5557657 | 128.1324802 | 48 | 72,000 | none | **fix_63c8a193fe** (C) |
| B 7 8565766 5557656 | 128.1324802 | 36 | 54,000 | none | **fix_63c8a193fe** (C) |

- **Greedy set:** {nl2837_r11, nl3352_r13, fix_63c8a193fe}.
  - This is the minimum among the 2026 configurations and the screened windows.
    - nl2837_r11 and nl6401_r14 cover the 144 combinations of the 2.126 rows and nothing else.
    - nl3352_r13 and nl3357_r13 cover only the 16 combinations of the 124.1324817 row.
    - No 2026 configuration occurs in any of the 84 combinations of 128.1324802.
  - Swaps: nl6401_r14 can stand in for nl2837_r11, and nl3357_r13 for nl3352_r13.
  - All four are D=true on kcc_o3 -C and on dfast18 (results/nl51_Drecheck.txt).
- **Off-centre and private-dependent placements.** K3gB5n loads nl51 only through u, which is why it misses these.
  - nl2837_r11 sits at w5 w6 s5 p6.1 s6 p5.2 w4 s4 s3. It does not use u, and it uses two privates.
  - nl3352_r13 sits at u w3 w2 s2 w1 s1 p3.1 w6 w5 s5 p5.1. It uses u and two privates.
- **fix_63c8a193fe** is the window around 128.1324802.
  - Interior: {u, w0..w6, s0, s1, s5}, 11 hosts. All have fixed letters in both rows, so it is the same window in all 84 combinations.
  - Ring 14.
  - kc -C finds X = {I3-I9, I7-I8, R12-I8, R0-I9} (reached 108623/199291, C-REDUCIBLE). cfast --fixed on the same X: C-REDUCIBLE.
  - X passes Gonthier's valid_contract and our Lean admissibleX, evaluated verbatim (see Method 6).
  - The none configuration 128.1324802 itself fails admissibleX (round9 vc_none51.tsv).
  - So the substitute goes through our existing C path, not the valid_contract port.
  - 17 other windows also cover all 84 combinations. The next smallest is fix_3798c42969: ring 14, 12 interior, interior {u, w0..w6, s0, s1, s2, s5}.
- **No D window was found for 128.1324802.** Screened so far (results/rf_*.tsv, r3_done.tsv):
  - all 119 fixed-host windows at ring ≤ 16: 29 C, 90 N;
  - 72 windows with varying privates: 2 C (each covering only the 12 combinations with p6 = 6), 70 N.
  - Ring-17/18 fixed windows (66) were left unscreened, a batch of 10 was started but stopped at the time box before any result (r17_0.tsv.log).

### (c) d = 9, 10 (W6r RSST-FP9): every state that the 582 kills leave has a 2026 substitute

- I re-ran W6r's d9bb enum 582 with the example cap lifted.
  - The code is a patched copy: d9plus/d9bb_all.cpp. Its only change is line 172, `modadm.size() < 400` → `< 100000000`.
  - It exports every state, giving the same counts: 31,139 at d = 9 and 409 at d = 10, both complete.
- Each state was read into fp2's Window. The geometry is the same as d9bb's: p_j.1 is next to s_{j-1}, and s_j lies between w_j and w_{j+1}.
- Hosts follow d9bb: u with exact letter d, and every w, s or private with letter 5..8.
- **Model check:** on 1,500 random states, no proved RSST configuration is contained, and the set of contained none configurations equals d9bb's note in 1,500/1,500.
- **The 2026 set kills all 31,548 states. None is left.**
  - Every one of the 13 sole-killer none configurations is replaced, as are the others that occur: results in d9plus/d9_by_noneconfig.tsv and d9_by_noneset.tsv (244 none-sets).
  - Greedy cover: 37 configurations (d9plus/d9_greedy.tsv). The largest are:
    - nl0004_r8: 21,253 states;
    - nl2638_r12: 6,012;
    - nl0078_r11: 912;
    - nl0026_r12: 789;
    - nl7574_r13: 450;
    - nl0050_r10: 360;
    - nl2828_r13: 356;
    - nl2656_r13: 288.
  - The other 29 cover 186 states or fewer each.
  - The greedy configurations re-checked: 37/37 D=true on kcc_o3 -C and on dfast18 (d9plus/greedy_Drecheck.txt).
- **Sole-killer none configuration → greedy picks on the states where it is the only none configuration:**

  | none config (d) | sole states | greedy picks |
  |---|---|---|
  | 439326.126 (9) | 3,591 | nl2638_r12, nl0026_r12, nl2636_r12, nl2828_r13 |
  | 126.1306802 (9 / 10) | 454 / 32 | nl0078_r11 |
  | 2.126 (9 / 10) | 367 / 60 | nl0004_r8 (+ nl0008_r9, nl0067_r10, nl0018_r11 at d9) |
  | 453963.126 (9) | 316 | nl2656_r13, nl2828_r13, nl0026_r12, nl2759_r13 |
  | 439328.136 (9) | 219 | nl7574_r13 |
  | 453963.364 (9) | 154 | nl2828_r13, nl2676_r13, nl0026_r12, nl2653_r12 |
  | 453963.136 (9) | 153 | nl2737_r14, nl0026_r12, nl7749_r13, nl2759_r13 |
  | 3.1324806 (9 / 10) | 64 / 4 | nl0019_r11 (+ nl0026_r12, nl2828_r13) |
  | 439589.122 (9) | 62 | nl7287_r12, nl7264_r12 |
  | 126.442802 (9 / 10) | 41 / 9 | nl0050_r10 (+ nl0026_r12) |
  | 3.1324802 (9) | 31 | nl0013_r10, nl0026_r12 |
  | 443166.126 (9) | 22 | nl7383_r13, nl7476_r14, nl0026_r12, nl2653_r12 |
  | 26359326.126 (10) | 53 | nl2803_r13, nl0026_r12, nl2828_r13, nl8062_r13 |

- **Family kill patterns (f9/b9/f10/b10, pat_K5r_D.out, rpatN):** not tested, because nothing was left for them to kill. A quick look in W13's K3 folders found only famK5 window batches, not pat_K5r_D.out or fam_args.

### (b) cons2, literal probe (my interpretation)

- I took the d = 6 labels that W6r lists with only 2.126 as an example, plus 565668/577555.
  - Apex letters were read literally.
  - Privates are 5..9, independent per site.
  - I used fp2's d = 6 ledger (base 0) and the 582 kills.
- All 9 labels are positive in every filling.
  - In 3 of them, the 582 kills alone kill everything: 565668/577555, 565667/777775 and 565668/575755.
  - In the other 6, one group with one combination is left, killed only by 2.126.
- **Substitutes:**
  - nl0004_r8 (D) covers 5 of the 6. The exception is 565678/777757.
  - The window fix_404d45e819 covers all 6. Interior {u, w0, w1, w2, w5, s1}, ring 13.
    - C with X = {I0-I2, I4-I5, R11-I2, R4-I5}; cfast --fixed agrees.
    - X passes valid_contract and admissibleX.
- **Windows screened:** 70 at ring ≤ 14. Results: 22 C, 48 N, 0 D. 2.126 itself comes out N.
- **Caveat:** W6r's cons_real_B.tsv has 40 apex combinations for every label, so its apex classes are not literal letters, and the convention is not documented. My rows can therefore differ from W6r's.

## Method

1. **Elements to cover** (sub.py).
   - For each row: the positive groups that the 582 kills (D2 + C2cons) do not kill.
   - Inside each group: every minimal combination (spec 8.2) that holds no proved configuration.
   - A substitute set works iff it hits every element.
2. **2026 set** (sub.py; d9sub.py at d = 9/10).
   - All 8,200 nl51 kc lines (b9bc6e8b) are placed anywhere among the hosts.
   - d9sub.py runs in three steps:
     - a full scan of 400 sampled states, which sets the frequency order;
     - a pass over every state in that order, stopping at the first hit; states with no hit get a full scan (1 state needed it);
     - a test of the 37 witness configurations on every state, for the greedy cover.
3. **Windows** (win.py, winfix.py).
   - Each window is the none configuration's occurrence plus further hosts, using true-letter rotations.
   - The ring-3 slots of consecutive ring-2 hosts are identified.
   - The free completion is kept only when the ring is a simple cycle and no interior vertex meets a ring vertex twice.
   - Fixed-host windows (winfix.py) lie inside the vertices whose letters are the same in every combination of the row.
4. **Screen.** mscreen.py runs kc -C; a D verdict goes to dfast18, a C verdict's found X to cfast --fixed. TO = 900 s.
5. **Cover** (cover.py). Every D/C window is re-embedded in every element, followed by a greedy cover.
6. **Contract check** (vc_win.py).
   - Each C window's free completion is rebuilt from its row. The rebuilt kc line must equal the screened one.
   - Every vertex gets its full rotation. A ring vertex y_k gets y_{k+1}, then its interior faces, then y_{k-1}.
   - mscreen's X is evaluated by check() from round9_rsstnone/code/vc_check.py, exec'd unchanged.
   - Results: 31/31 C windows of (a) and 22/22 of (b) pass valid_contract and lean_admissibleX. All are genus 0, cubic plus one outer node, with the ring as an scycle.

## Verified / not verified

- **Verified by me:**
  - the 244 elements;
  - the nl51 placements;
  - the d9bb state export (counts equal) and the d = 9/10 model check (1,500/1,500);
  - D re-checks on two engines;
  - window verdicts from two engines;
  - the cover;
  - the contract checks.
- **Not verified:**
  - end-to-end passage of the C windows through the Lean C path;
  - a D window for 128.1324802 (none found at ring ≤ 16; ring 17/18 not screened);
  - the d ≥ 9 placements, which assume d9bb's 2-ball. A ring vertex of a placed configuration may lie outside it, as for any fp2 placement (spec 7 convention);
  - the full set of 240 cons2 labels (not run).

## Files (MD5SUMS covers all)

- `code/`
  - sub.py, win.py, winfix.py, cover.py, vc_win.py, d9sub.py;
  - fp2.py (= round10's 0c4804e2);
  - mkdom.py, probe.py, probe0.py (cons2);
  - run_sub.sh, run_ms.sh, run_ms2.sh, run_seq.sh, drecheck.sh.
- `results/` (a)
  - elements.tsv, per_target.tsv, greedy_embeddings.tsv, nl51_coverage.tsv, sub.log, nl51_Drecheck.txt;
  - w0..w3(+_src).tsv; r3_done.tsv;
  - wf.tsv, wf_src.tsv; bf_0/1.tsv; rf_0/1.tsv (+ .log); b17*.tsv (ring-17/18 batch, stopped before a first result: r17_0.tsv.log);
  - cov_windows.tsv, cov_left.tsv, vc_windows.tsv.
- `cons2_probe/` (b)
  - dom_K.json, probe0_nokills.txt, probe_K582.txt;
  - elements.tsv, per_target.tsv, greedy_embeddings.tsv, nl51_coverage.tsv, sub.log;
  - kf.tsv, kf_src.tsv, kb.tsv, kr.tsv (+ .log);
  - cov_windows.tsv, cov_left.tsv, vc_windows.tsv.
- `d9plus/` (c)
  - d9bb_all.cpp (W6r bad952be with the cap lifted);
  - enum582all_d9.json, enum582all_d10.json;
  - d9sub.log, d9_states.tsv (31,548 states, each with its witness and greedy pick);
  - d9_by_noneset.tsv, d9_by_noneconfig.tsv, d9_greedy.tsv, greedy_Drecheck.txt.

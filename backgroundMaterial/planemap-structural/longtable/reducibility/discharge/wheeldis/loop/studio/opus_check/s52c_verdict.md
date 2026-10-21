# s52c (the A83 C cover, a6efb310): Studio spec-only check

**Verdict so far:**
- **Status audit:** it matches Opus exactly.
- **Cover check:** keeping only the 154 entries is **FEASIBLE at 0.105883918328**, and dropping f9_...555565_......... makes it
  **INFEASIBLE**.
- **CCover3 Lean:** 12 of 13 hC are exit 0 with sorry 0. CC3V07 (f8_..556856_....5566, ring 16) is still building; the assembly
  and #print axioms follow it.

## Independence statement
- **Opus files opened:** only the data files s52c/ccover_A83.txt (a69d1c48), ckeep_A83.txt (ed97c152, 154 names) and
  ccover_A83_summary.txt (281c0c10), plus the A83 solution and registry data already used for s44A83.
- **The R5 / R6 / RBIG reading** is Opus's, as relayed by the coordinator at 15:53Z (text only). I did not open pcheck.py, the pricer,
  cmd scripts or logs.
- **Code used:** my own st21_check.py, st16_filter.py, l3q_masks.py, the keep filter and the CKEEP loader copies (wlp*_ck.py; the
  frozen wlp*.py files are untouched).
- **Team B material:** none.

## 3. Status audit (Studio's own Lean outputs)
- **My Lean sources:** CXInt 95ba762d (345 entries), CCover 1c56a79e (32), CXRing 2a4bc4cf (96), CCover2 f2acc3e7 (6), and
  dcheck/CWheels.lean.
- **Of the 154: CXInt 83, CCover 27, CXRing 24, CCover2 5, CWheels 2, not in Lean 13.** These equal Opus's counts. The batch of
  every name agrees, so there are 0 mismatches and no covered entry that I cannot find.
- **The 13 not in Lean** are exactly the coordinator's list.
- **ckeep:** the names equal the cover's 154. None of the 128 held names is in it.
- **RSST:** the 9 RSST entries in the cover are rsst072, 118, 137, 140, 148, 178, 180, 187 and 217. **RSST 2.126 and 8406.123 are
  not used.**

## 1. CCover3 (out/lean_ccover3/a6efb310/)
- **The method:** exactly the CCover2 method (f2acc3e7). The generator gen_ccover3.py is CCover2's gen_ccover2.py with ONLY = the 13
  names. The C data is the A83 k3x C file at 240b5a08, and every X is the same at 240b5a08 as at HEAD.
  - **Sources:** loop/k44 A_cf.out and *.txt; loop/k47 r54a, r54c, r57f, r58a, r58e, r58i, r58j and s52r1 (_kills_cf.cfast and
    _kills.txt). All are byte-identical at 240b5a08.
  - **Build base:** the 2a4bc4cf build, whose dcheck Lean sources are unchanged.
- **Ring-merge guard:** 12 entries have interior-only X. f7_5676676_5..5..5 has X = {I1-I7, I5-I6, R11-I6, R13-I7}, with components
  {I1, I7, R13} and {I5, I6, R11}, one ring vertex each, so it **passes** and gets eqR = [(11, 6), (13, 7)].
- **CCover3.lean:** exit 0. cc3Entries_ok uses propext, Quot.sound and its own native_decide aux.

| # | entry | ring | X | result |
|---|---|---|---|---|
| 0 | f10_...5565665_......5... | 14 | I4-I5 | exit 0, 3,335 s |
| 1 | f10_...5656565_.......55. | 14 | I0-I5 | exit 0, 2,631 s |
| 2 | f7_..65676_..6565. | 14 | I0-I1 | exit 0, 1,708 s |
| 3 | f7_..65686_..55555 | 14 | I0-I1 | exit 0, 1,428 s |
| 4 | f7_..66676_..55.5. | 14 | I0-I1 | exit 0, 2,667 s |
| 5 | f7_..67576_..5.55. | 14 | I0-I1 | exit 0, 2,700 s |
| 6 | f7_5676676_5..5..5 | 14 | I1-I7,I5-I6,R11-I6,R13-I7 | exit 0, 1,644 s |
| 7 | f8_..556856_....5566 | 16 | I0-I1 | building |
| 8 | f8_..566765_....55.. | 14 | I0-I2 | exit 0, 2,568 s |
| 9 | f8_..567656_....5555 | 14 | I0-I3 | exit 0, 1,438 s |
| 10 | f8_.5565775_.....5.. | 14 | I0-I1 | exit 0, 2,269 s |
| 11 | f9_...565665_.......65 | 14 | I0-I4 | exit 0, 3,038 s |
| 12 | f9_..5665566_.......5. | 14 | I0-I5 | exit 0, 2,273 s |

All finished entries have sorry 0, error 0 and about 3 GB RSS. Each per-entry `#print axioms` lists propext, Classical.choice,
Quot.sound, its own native_decide aux and cc3Entries_length's aux.

## 2. Cover check: upperR2, sol_q44fbA83 (cfc41a44) at 0.105883918328, A83, 128 held out, ONLY the 154 ckeep C entries
- **C patterns:** every cpat file keeps only the ckeep blocks (out/job31/s52c/keep_filter.py). That leaves 141 k3x_C blocks plus 2
  cpat-other blocks: e7_B56656._6B.66.._1111110 from job27/part01, and 1 from k42map. In total 143 C patterns; D stays at 17,744 and
  RPAT at 158.
- **Kill tables and l3q masks** are rebuilt from the forbidden set RSST D2 (249) + the 9 kept RSST C2cons + all k3x D + the 141 kept
  k3x C, which is 3,103 configurations. kill6 U7 975b02ac, U8 = U9 6dc44bba; the l3q masks have 190 of 30 per side.
- **Wheel sets (Opus's reading):**
  - R5 = c5 D only: 12; all 12 c5 C are dropped.
  - R6 = c6 D + c6_556577 + c6_566577 (+ the 555 rule): 27.
  - RBIG = D big wheels only: 91; the 13 def_*.cfast C 7-wheels are dropped.
  - The loader and separator read the same sets, through the CKEEP copies (sep: RBIG = 91).
- **Isolation:** each run uses its own SEPTAG and solution copy. The keep154 pattern file is md5 10347dcb (all 4 loads 15,578 /
  2,801 / 5,088); the dropf9 file is 12bc3e44 (2,800 / 5,087). An earlier pair that shared a pattern file was discarded
  (cover_*_race.log).
- **The EXPECT_PAT count:** the logs print a pattern-count line against my own expectation. In the race pair I had set C = 0 by
  mistake; the relaunched runs expect C = 143 / 142.

| run | senders / cons2 | receivers d = 7..17 (exhaustive) | DP / Karp | verdict |
|---|---|---|---|---|
| **keep154** | 0 / 0 violated (cons2 with fb, over all 1,424 × 5^6 words: 0) | **0 violated at every d** | clean, λ 0.572808649 | **FEASIBLE at 0.105883918328** |
| **dropf9** (drop the sole entry f9_...555565_.........) | 0 / 0 | d = 9: violated, ≥ 5,000 oriented arrangements (cap); load 3.275 vs a limit of 3.106, all in the f9_...555565_ row family (e.g. 558585655 / 566859998); every other d is 0 | clean | **INFEASIBLE**, as expected |

- **Count convention:** Opus reports 20 rows for the control. I count oriented arrangements up to 5,000. The verdict and the row
  family agree.
- **Separator calibration:** leaf vs spec 3.3e−10 (d = 7..8); 0 relaxed below exact on 640 arrangements.

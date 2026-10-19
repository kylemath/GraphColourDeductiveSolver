# st24b (sol_st24b.json md5 7348721a0224615063b17074681f35d7, cert_st24bL.json md5 51055fe3547862bd711db500acab6eb4;
# Opus 20ee527a): Studio spec-only check

**Verdict: t* = 2/13 exactly.** Upper FEASIBLE at 2/13 and lower VALID at 2/13 (19 Oct 17:53Z) on registry 0125c46b
(argsA59). This is hat5 (section 15) with the section 14' filter, v6 off, and conservation over all 1,424 six-types.
Neither kill line is met. Logs: st24b_check.log (upper), st24bL_lower.log (lower), studio_st24b_dcount.txt. Checker:
out/job31/st18_check.py (HAT5=1, V6=0), the same route as s22h (6a5f89a0). It ran queued behind Job 52 (gate
out/job52/st24b_gate.sh) on one non-heavy slot.

## Hypothesis test: is the drop from 16/101 (s22h) due only to registry kills?
**Yes, at the input level.**
- argsA59 vs s22h's argsA55: the only difference is the k3x pair (5fa0adb0 -> 0125c46b), plus the folder path of the
  byte-identical job28 r_5..r_8 files.
- Registry by name (Studio rebuild from the committed k3x at both commits): 5fa0adb0 has 869 D / 658 C; 0125c46b has
  1,897 D / 838 C. That is **+1,028 D, +180 C, 0 removed**: exactly Studio's admitted batches r9f (93 D + 75 C), r9g
  (457 + 57), r9e (475 + 48) and r7h (3 + 0).
- Same mode flags (model R6x2, apexcls, hat5 on, v6 off, zh off), same kill tables (Studio's st16_filter tables,
  md5-identical to s16ap/kill6), and the same 20,676-row sender enumeration.
- So the class is unchanged, and only the registry grew. The lower value moving 16/101 -> 2/13 is consistent with
  that. Not tested: whether some subset of the new kills alone gives 2/13. Studio's LP cannot re-solve this class.

## Independence statement
Built from RELAY_SPEC.md alone (sections 12, 14' and 15). Opus files opened: sol_st24b.json, cert_st24bL.json,
s25/argsA59.txt, s25/dcount.txt, and st24b.log (only its pattern-count and sender-row count lines, grepped). The
listed file names in s24d/ were seen via git ls-tree, but no engine, cmd script, cons basis, rows file, pricer/rc file
or other log was opened.

## Results
- Registry: argsA59 pinned to 0125c46b; the 10 shipped files are byte-identical. dcount 16,937 (17,271 names),
  identical to Opus's dcount.txt file by file (0 differing). Spec-loader patterns D 16,937 / C 1,884 / RPAT 158,
  equal to st24b.log.
- Upper:
  - Bounds clean (69 r values; max x 0.087).
  - senderR2 20,676 rows (as st24b.log), 0 violated (min slack −7e−14).
  - cons2 1,424 × 729: 994 with a five, 0 violated (max 3.1e−13); 430 without, 0 violated (max 0).
  - Relaxed rows (+ relaxed r) vs spec rows: 720 arrangements, 0 mismatches. C++ exact leaf weights vs spec rows:
    120 compared (d = 7..12, CALD = 12), max 4.0e−10.
  - Receivers d = 7..17, exhaustive (sep3r_ak, SEP_EXACT6 + SEP_RTAB): **0 exact violators at every d.**
  - DP d = 18..30 clean. Karp λ = 0.543709218, covering d >= 12.812.
- Lower: 36 rows (9 senderR2, 17 cons2, 7 mrowR2, 3 receiverR2), all mrowR2 canonical. tco = 1, **D = 2/13**. Nonzero
  reduced costs, all >= 0: M[766675531] 3/13, M[767675531] 3/13, r[506507] 3/13, r[506509] 1/13.

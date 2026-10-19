# s22f (sol_s22f.json md5 78254f1665e90a86e3206015d91dc499, cert_s22fL.json md5 a4809c8204de4206b213c4b5b26548d8;
# Opus 85efba87): Studio spec-only check

**Verdict: t* = 4/25 exactly.** Upper FEASIBLE at 4/25 and lower VALID at 4/25 (19 Oct ~09:20Z). This is the filtered
6-centred relay without hat5 (sections 12 + 14'; v6 and hat5 off) on registry 5fa0adb0. Logs: s22f_check.log (upper),
s22fL_lower.log (lower). Checker: out/job31/st18_check.py with HAT5=0, V6=0, which reduces to the st16_check class.

Registry: argsA55 pinned to 5fa0adb0; the 10 shipped files are byte-identical. dcount 15,909, identical to Opus's file
by file. Patterns D 15,909 / C 1,704 / RPAT 158, equal to s22f.log. Kill tables: Studio's st16_filter tables, md5
27a64538... (U7) / 6dc44bba... (U8 = U9), i.e. s16ap/kill6, so check 4 stays at 7,500 (md5 9b4d02ba...). Re-solve:
not possible with Studio's LP (wlp3r6 cannot express g2/h2/filter).

## Independence statement
Built from RELAY_SPEC.md alone (sections 12 and 14'). Opus files opened: sol_s22f.json, cert_s22fL.json, and s22f.log
(only its pattern-count line, grepped). No engine, cmd script, cons basis or other log was read.

## Results
- Upper:
  - Bounds clean (max x 0.059). senderR2 7,074 rows, 0 violated.
  - cons2 1,424 × 729: 994 with a five, 0 violated (max 1.8e-13); 430 without, 0 violated (max 0).
  - C++ exact weights vs spec rows: max 4.5e-10. Relaxed rows vs spec rows: 820 arrangements, 0 mismatches.
  - Receivers d = 7..17, exhaustive via sep3r_ak with SEP_EXACT6: 0 exact violators.
  - DP d = 18..30 clean. Karp λ = 0.526728523, covering d >= 12.340.
- Lower: 90 rows (20 senderR2, 42 cons2, 19 mrowR2, 9 receiverR2), all mrowR2 canonical. tco = 1, **D = 4/25**.
  Nonzero reduced costs: M[766675531] = 3/25, M[767675531] = 3/25, M[777775531] = 1/25, all >= 0.

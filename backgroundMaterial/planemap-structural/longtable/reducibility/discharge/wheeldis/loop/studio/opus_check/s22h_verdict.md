# s22h (sol_s22h.json md5 e5607f7a415abeea6841cb299c7e1ce7, cert_s22hL.json md5 88d75951d70b3cda88f258598fd8c851;
# Opus fd6ea00e): Studio spec-only check

**Verdict: t* = 16/101 exactly.** Upper FEASIBLE at 16/101 and lower VALID at 16/101 (19 Oct ~10:55Z). This is hat5
(section 15) with the section 14' filter, v6 off, on registry 5fa0adb0. Logs: s22h_check.log (upper), s22hL_lower.log
(lower). Checker: out/job31/st18_check.py (HAT5=1, V6=0).

Registry: argsA55 pinned to 5fa0adb0, unchanged since s22f. dcount 15,909. Patterns D 15,909 / C 1,704 / RPAT 158,
equal to s22h.log. Kill tables: Studio's own st16_filter tables (U7 27a64538... / U8 = U9 6dc44bba..., the s16ap/kill6
md5s), so check 4 is 7,500 (md5 9b4d02ba...). Re-solve: not possible with Studio's LP (wlp3r6 cannot express the
class).

## Independence statement
Built from RELAY_SPEC.md alone (sections 12, 14' and 15). Opus files opened: sol_s22h.json, cert_s22hL.json, and
s22h.log (only its pattern-count and sender-row count lines, grepped). No engine, cmd script, cons basis, rows file
or other log was read.

## Results
- Upper:
  - Bounds clean (87 r values; max x 0.067).
  - senderR2 with all five hat classes: 20,676 rows (as s22h.log), 0 violated (min slack −5e−14).
  - cons2 1,424 × 729: 994 with a five, 0 violated (max 1.3e−13); 430 without, 0 violated (max 0).
  - Relaxed rows (+ relaxed r) vs spec rows: 720 arrangements, 0 mismatches, relaxed never below exact.
  - C++ exact leaf weights vs spec rows: 120 compared (heaviest 20 at d = 7..12), max 4.2e−10. CALD = 12: the
    calibration was limited to d <= 12 after an unbounded top-20 search at higher d had run 52 min. This is a
    validation step only; the exhaustive pass below runs every d.
  - Receivers d = 7..17, exhaustive (sep3r_ak, SEP_EXACT6 + SEP_RTAB): **0 exact violators at every d.**
  - DP d = 18..30 (Studio max-plus with the relaxed r) clean. Karp λ = 0.557346373, covering d >= 13.197.
- Lower: 114 rows (23 senderR2, 62 cons2, 19 mrowR2, 10 receiverR2), all mrowR2 canonical. tco = 1, **D = 16/101**.
  Nonzero reduced costs, all >= 0: M[766675531] 34/303, M[767675531] 34/303, M[777775531] 20/303, r[506506] 17/303,
  r[506507] 34/303, r[5067] 2/303, r[507507] 2/101, r[507509] 20/303.

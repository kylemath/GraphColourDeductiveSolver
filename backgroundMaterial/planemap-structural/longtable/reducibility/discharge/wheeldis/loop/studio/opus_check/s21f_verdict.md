# s21f (sol_s21f.json md5 2349753e93bc9c202b517ce02d3e74b7, cert_s21fL.json md5 99614471d93a4bc4c16ade89fa299a82;
# Opus 4e505eb6): Studio spec-only upper check

**Verdict: upper FEASIBLE at t = 65/406** (19 Oct ~06:45Z). Log: s21f_check.log. Checker: out/job31/st16_check.py with
V6=0, because the sol has v6 off: the section 14' filtered s12r mode, with the mask on M only and no v and no V.

Registry: argsA54 = 880d25c6 k3x pinned + job28 r_5..r_8 + rpatD (argsA54_pinned.txt). The 10 shipped files are
byte-identical. dcount 15,881, identical to Opus's file by file. Patterns by Studio's spec loader: D 15,881 / C 1,679 /
RPAT 158, equal to s21f.log. Opus's root lacks out/job28/r_3.cfast and r_4.cfast; ours has them, but both are empty
(0 bytes), so nothing was dropped and the filters match.

## Independence statement
- Built from RELAY_SPEC.md alone (sections 12, 13 and 14' at 3b972410 / fcdd458e); no Opus code read.
- Opus files opened for s21f: sol_s21f.json, cert_s21fL.json (fetched; unused, since this is upper-only), and
  s21f.log (only its pattern-count lines, grepped). The package's file names were listed, but cmd_s21f.sh,
  cons2basis_cls.json, the engine copies and the rows/upper/lower logs were not opened.
- Kill tables: Studio's own st16_filter.py, rerun for this job (st16_filter_s21f.log): U7 file md5
  27a64538719969f93aa731b25c011911 and U8 = U9 6dc44bbaae0e7a9a9136f191a5aa6ce8, so the same tables as s16ap/kill6
  (by md5; Opus's tables were not read). Check 4: full 3,072; LP projection 7,500, md5
  9b4d02bace5786cbf0f6c5c7c7434dbc.

## Results
- Bounds clean (max x 0.094). No v or V in the sol (v6 off); 0 stored V entries.
- senderR2: 7,074 rows, 0 violated.
- cons2 (no v terms): all 1,424 × 729; 994 with a five, 0 violated (max 5.7e-13); 430 without, 0 violated (max 0).
- Studio relaxed rows vs spec rows: 820 arrangements, 0 mismatches, relaxed never below exact.
- Receivers d = 7..17: exhaustive via sep3r_ak with SEP_EXACT6 (exact M[sig2+mask] six windows at each leaf; pruning
  on the relaxed bound). C++ exact weights vs the spec rows checked on the heaviest 20 per d. **0 exact violators at
  every d.**
- DP d = 18..30 clean. Karp λ = 0.540108938, covering d >= 12.698.

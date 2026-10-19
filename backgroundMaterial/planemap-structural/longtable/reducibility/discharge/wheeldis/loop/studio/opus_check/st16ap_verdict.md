# st16ap (sol_st16ap2.json, md5 325a18a750a1b0a42d4c994e620d4d8f; Opus 3b972410): Studio spec-only upper check

**Verdict: upper FEASIBLE at t = 6/37** (19 Oct ~06:20Z). Log: st16ap2_check.log. Checker: out/job31/st16_check.py,
filter out/job31/st16_filter.py (log st16_filter.log).

Registry: argsA52 (09d8ac38 k3x pinned) + rpatD; dcount 15,855 D / 1,658 C / 158 RPAT. r_3.cfast and r_4.cfast are in
our args but are empty files (0 bytes), so the filter matches Opus's root, which lacks them.

## Independence statement
- Built from RELAY_SPEC.md alone: section 12, section 13 and section 14' at 3b972410, plus the 14' fix at fcdd458e.
  No Opus code was read. Explore's grow.py and rings.py (named by the spec) and Studio's own wlp3r6 / sep3r_ak were
  used.
- Opus files opened: RELAY_SPEC.md (3b972410, fcdd458e), sol_st16ap2.json, and cert_st16ap2.json (fetched only;
  unused, since this is upper-only). The package's file names were listed (git ls-tree), so names such as
  cmd_st16ap.sh, s16_killnpy.py and kill6_U*.json were seen, but none of those files was opened. No s16ap/ table
  file, engine, cmd script or cons basis was read.
- The kill-table convention "a value is killed only by an embedding that uses p" was selected among readings of the
  spec text by comparing Studio's own tables with the md5 values the spec publishes (27a64538..., 6dc44bba...).
  Variant 2 of 4 matched both byte for byte. It is also the spec's wording in 14' item 1.

## Results
- §14' filter (Studio-built):
  - Forbidden set 2,009: 582 RSST (249 D2 + 333 C2cons) + 1,427 twoeng at 09d8ac38.
  - Check 4 full test: 3,072, with the per-slot kills and killers as in 14'.
  - Check 4 LP projection: 7,500, md5 9b4d02bace5786cbf0f6c5c7c7434dbc.
  - Tables in the fcdd458e layout: U7 file md5 27a64538719969f93aa731b25c011911; U8 = U9 6dc44bbaae0e7a9a9136f191a5aa6ce8
    (numpy 2.0.2, header included).
  - Strict unknown = 5 / 7: identical. Mirror symmetric.
- Bounds clean (max x 0.043).
- Stored V: 1,102 entries equal the rebuilt min within 1e-9 (max 7.1e-12).
- senderR2: 7,074 rows, 0 violated.
- cons2 with v, all 1,424 × 729 cv words: 994 with a five, 0 violated (max 7.1e-12); 430 without, 0 violated
  (max 3.8e-13).
- Studio relaxed rows vs spec rows: 820 arrangements, 0 admissibility mismatches, relaxed never below exact.
- **Receivers d = 7..17, exhaustive:**
  - Method: bin/sep3r_ak with SEP_EXACT6. The branch-and-bound prunes on the relaxed bound (an upper bound), and at
    each leaf every link 6's relaxed value is replaced by the exact spec window M[sig2+mask] − V[sigV+mask].
  - Validation: C++ exact weights vs the Python spec rows on the heaviest 20 per d: 220 compared, max 4.8e-10.
  - Exact violators: 0 at every d from 7 to 17.
- DP d = 18..30 clean. Karp λ = 0.513513514, covering d >= 12.000.

## Corrections during the run (none affects the verdict)
- First filter build: it killed every p when the window alone contains a configuration. That did not match the md5,
  and it is not the spec reading. Rebuilt.
- First receiver runs were void: the over-killing tables, then a cap-limited relaxation, then an exact-table cache
  bug in which sig2 and sigV shared one cache. Each was caught by the checks above before any verdict.

# macpack add-on: rpatN switch + sol_q66_q (W17, 7 Nov 2026)

Unpack over an existing macpack tree (`w17_macpack.tar.gz` 8acb1a22) at /tmp/swarm-W17.

**Context.** Opus's growpy audit (from_opus/growpy_audit/REPORT.md) found 46 face-set-only patterns in rpatN3 (e153fc41). The macpack used rpatN3 (as the Studio copy out/job31/s39o_rpatN3_studio.txt). Opus shows that sol_q66_q is FEASIBLE with no rpatN at all (ref/s86_k86PS/upper_P0_q66_q.log).

## What changes

- `code_gk7/run17.sh`:
  - **rpatN is OFF by default.** No rpatN pattern is loaded.
  - `RPATN=<file>` loads one, for example `tab/rpatN3_rotation_justified.txt` (8b90a842, 2,241 patterns = e153fc41 minus the 46), for later k86PS points.
  - `RPATN=off`, `RPATN=none`, or a header-only file (`tab/rpatN_none.txt`, Opus's `tab/rpatN_empty.txt`) all mean off.
  - p0.log says `rpatN: off (no rpatN pattern loaded)` or `rpatN: <file> (md5 ...)`.
  - A missing file is a FAIL.
- `code_gk7/w17_upper.sh`: the resume stamp now includes the rpatN and rule-file md5s, so no Python step from an older run is reused, and the header line shows rpatN.
- New files:
  - `tab/rpatN3_rotation_justified.txt` (8b90a842);
  - `tab/rpatN_none.txt` and `tab/rpatN_empty.txt` (header only);
  - `sol/sol_q66_q.json` (e203707c, t = 0.128957775395);
  - `ref/s86_k86PS/` (Opus's README, MD5SUMS and the upper logs P, P0 and P6).

Nothing else changes. check.sh, smoke.sh and the binaries stay as they are, with no rebuild needed. EXPECT_PAT stays 18128,686,158.

## Mac commands

    cd /tmp && tar xzf macpack_addon_rpatN.tar.gz          # over /tmp/swarm-W17
    bash /tmp/swarm-W17/smoke.sh                           # optional, ~3.5 min, must end "SMOKE: PASS"
    RPATN=off bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/sol_q66_q.json 8      # TAG sol_q66_q_zW13

- The verdict is the `RESULT:` line of `/tmp/swarm-W17/logs/sol_q66_q_zW13/summary.txt`.
- Restart: rerun the same line.
- For a later point on 8b90a842: `RPATN=/tmp/swarm-W17/tab/rpatN3_rotation_justified.txt bash /tmp/swarm-W17/check.sh /tmp/swarm-W17/sol/<point>.json 8`, with its own TAG if the point was run before.

## Expected p0.log lines for sol_q66_q

- `rpatN: off (no rpatN pattern loaded)`;
- `patterns distinct by kind: D 18128 ..., C 686 ..., RPAT 158 ...; by d {7: 8796, 8: 5142, 9: 2749, 10: 1255, 11: 607, 12: 84, 13: 65, ...}`. Opus's P0 log has 8799 / 5146 / 2756 at d = 7, 8, 9: the usual counting offsets of 3 / 4 / 7, and the same at d >= 10.
- F2B rules 2b362955: `{('w6', 7): 1531, ('w6', 8): 1114, ('w6', 9): 87, ('w7', 7, 1): 928, ... ('w7', 8, 1): 714 ...}`;
- GK 151 keys, fe8a97a7;
- `senderR2 ... violated 0`;
- `VERDICT (python part ...): PASS`.

With `RPATN=.../rpatN3_rotation_justified.txt` instead: `rpatN patterns from rpatN3_rotation_justified.txt: 2241, by d {7: 618, 8: 829, 9: 608, 10: 178, 11: 7, 12: 1}`, and distinct by d {7: 9348, 8: 5892, 9: 3304, 10: 1425, ...}. D, C and RPAT do not change.

**Runtime.** At t = 0.129 Opus's engine took 7.4, 5.5 and 5.5 s for d = 7, 8, 9. Here, expect about 2 min for the Python step plus a few minutes of separator at NPROC 8: under about 10 min wall [estimate].

## Tested in the swarm container

The test ran in cpuslot, in a private mount namespace, with CPython 3.9.25 + numpy 2.0.2 + scipy 1.13.1 and clang 18. The add-on was unpacked over a fresh 8acb1a22 tree.

1. **rpatN off (default).**
   - `SMOKE: PASS`: (1) PARTIAL PASS d = 24..26; (2) planted control F2B7ROWS FAIL at load 1.591377316.
   - `RPATN=off DLIST=26 check.sh sol_q66_q.json 1`: Python step PASS, RESULT PARTIAL PASS (d = 26), with the counts above.
2. **rpatN 8b90a842.** Same smoke PASS; the q66 Python step PASS with 2,241 rpatN.
3. **Header-only and missing files.** A header-only file gives `rpatN: ... has no pattern line: rpatN off`, and a missing file gives `VERDICT: FAIL (rpatN file ... missing)`.

## v2 (lead, 7 Nov 2026): bash 3.2 fix
macOS /bin/bash 3.2.57 mis-parsed `$(case ${RPATN:-off} in off|none) ...; esac)` in code_gk7/w17_upper.sh (STAMP line), giving
"syntax error near unexpected token `newline'" and "RPATN: unbound variable". v2 computes `_RPSTAMP` with a plain case statement
before the STAMP line; no other change (same stamp value: off, or the first 8 hex of the rpatN file md5). No other `$(case` in the add-on.

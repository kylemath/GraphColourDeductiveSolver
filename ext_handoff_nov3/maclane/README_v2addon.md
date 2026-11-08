# maclane-k86 v2 add-on: the KEYSPEC v2 lower lane k86GV1

Made 8 Nov 2026 in the Opus container (P_own_lp/s86_f2b7). This is an **add-on** for the maclane-k86 pack that is already unpacked,
relocated and built on the Mac Studio (`maclane-k86.tgz`, md5 2fa853ec03f1e9bda2a0a54e3cea63a8). It is not a new pack: it adds one
lane and changes no file the running lanes use.

| lane | tag | what it is | what comes back |
|---|---|---|---|
| **V2 LOWER** | **k86GV1** | the container's `launch_k86GV1.sh` (md5 78f13aee) with this pack's paths: k86GL6's lext family on args **K3gB5b** (`args_A97_F_W13K3gB5b.txt`, md5 5e399535 = K3gB + K5H01 + K5b), keys `p1r/cg_keys_r13w16_16fik.txt` (240; 89 payer-7 keys -> `eng_v2/bin/jsepf_gk_k192`), flags GL6 + `p1r v2r v2seed=v2r/seed_sol_k86GL5_p1.json v2rescan=1 v2inner=4`, on the engine copy **eng_v2** (every d = 7 / 8 receiver is the KEYSPEC v2 max-row, added lazily as realisation rows by an exact max-plus DP: `fs/.../s86_f2b7/v2r/README.md`) | the phase-1 values (`lext it N: phase 1 ... t1 = ...`) and each phase-1 cert: `outbox/v2lower/` (same format as `outbox/lower/`) |

**GV1 replaces the k86ML1 control lane on the Mac** so that the core count stays about the same (both use 2 separator threads):
run `bash stop.sh lower` before `bash launch_v2.sh` (the launcher refuses while k86ML1 runs; `ALLOW_ML1=1` overrides).
The upper lane k86MS1 keeps running untouched.

## 1. Commands

    cd ~/maclane                                   # the folder that holds maclane-k86/ (use your own path)
    md5 -q /path/to/maclane-k86-v2addon.tgz        # must print the md5 in maclane-k86-v2addon.tgz.md5
    tar -xzf /path/to/maclane-k86-v2addon.tgz      # creates ~/maclane/maclane-k86-v2addon/
    bash maclane-k86-v2addon/install_v2.sh ~/maclane/maclane-k86     # 1. checks, copies into the pack, builds eng_v2 (about 1 min)
    cd ~/maclane/maclane-k86
    bash smoke_v2.sh        # 2. about 5-10 min, 1 thread, about 0.6 GB; must end with "SMOKE-V2: PASS" (section 3). k86ML1 may keep running meanwhile.
    bash stop.sh lower      # 3. stop the k86ML1 control lane (its outbox/lower, K.log and rows stay)
    bash launch_v2.sh       # 4. start k86GV1 (needs smoke_v2.ok from step 2)
    bash status_v2.sh       # any time: GV1 processes, phase-1 / v2inner / iteration lines, outbox/v2lower/P1.txt, run.log
    bash collect_v2.sh      # any time: ../maclane-k86-v2-out-<time>.tgz with outbox/v2lower, K.log, rows, run.log, smoke_v2 logs
    bash stop_v2.sh         # stop k86GV1 (outbox watcher first, then the K run)

`install_v2.sh` without an argument uses the `maclane-k86` folder next to the add-on folder. It checks that the folder is the pack
from maclane-k86.tgz (its MANIFEST.md5; `MACLANE_V2_ANYPACK=1` overrides) and that it is relocated (`.root` = the pack folder;
otherwise it says to run `bash relocate.sh` first). It never rewrites a file the pack already has:
a file present with other content stops the install before anything is written; identical files are skipped (so running it twice
is harmless). The existing `status.sh` / `stop.sh` / `collect.sh` keep handling the upper and lower lanes; the `_v2` versions handle
GV1 (`stop.sh all` does not stop GV1: use `stop_v2.sh`). If the pack folder is moved later: stop everything, `bash relocate.sh`
(it also rewrites the add-on's files), and the lanes can be launched again.

## 2. Knobs (environment variables, set on the launch command line)

| variable | default | effect |
|---|---|---|
| `V2_THREADS` | 2 | separator threads of the GV1 K run (= `threads=` of the container's launcher) |
| `V2INNER` | 4 | `v2inner=`: after each phase-1 solve, up to 4 rounds of DP on all known d = 7 / 8 receivers + phase-1 re-solve (0 = GL6 flags + v2r only) |
| `MAXIT` | 200 | K-run iterations |
| `TAG` | k86GV1 | run tag (rows / sol / cert file names, outbox names); `TAG_V2` for status_v2 / stop_v2 / collect_v2 |
| `V2_WARM_ML1` | 1 | add this Mac's k86ML1 rows (`eng_p1r/rows_k86ML1.txt`, complete lines, snapshotted at launch to `v2r/rows_k86ML1_snap_<tag>.txt`) to the warm list; 0 = only the container's GV1 warm set. Rows the K3gB5b family does not admit are dropped on admission. |
| `ALLOW_ML1` | 0 | 1 = launch even though k86ML1 still runs |
| `FORCE` | 0 | 1 = launch without `smoke_v2.ok` |
| `HSHIM_SOLVER` | ipm | LP method of the highspy shim (as in the main pack) |
| `OUTBOX_POLL` | 60 | seconds between outbox scans |
| `SMOKE_V2_HEAD` | 1 | smoke_v2.sh: 0 skips step 6 |

Example: `V2INNER=2 bash launch_v2.sh`.

Memory: like k86GL6 in the container, about 5 GB plus the realisation rows (not measured here: the container cannot hold a full GV1
run next to its own lanes). The Mac's 128 GB is plenty.

## 3. Smoke test (smoke_v2.sh)

1. the add-on is installed in this relocated pack and `eng_v2/bin/{jsepf_gk_k192,jsepf_gk,jsep3}` are built;
2. eng_v2's highspy shim (hshim 1.1): `tools/hshim_check.py` (the main pack's 40 reference LPs against stored highspy 1.15.1 solutions)
   and `tools/v2shimcheck.py` (the two calls new in 1.1, `getLp` and `clearSolver`: 40 LPs, 120 re-solves);
3. every eng_v2 module parses under this python;
4. `pcheck.py v2rtest` (v2r/NOTES.md validation step 1) on the GL5 phase-1 cert def2afcc with the container's K3g / 16fi environment:
   W6b test vectors 24 / 24, and the DP vs p1r_core vs brute-force statistics identical to the container's log
   (`ref/v2/v2rtest_b2_GL5.log`; paths and timings normalised): `V2R-TEST: PASS (0 failures)`;
5. the restricted-LP gate: `pcheck.py v2restricted v2mode=v2` on the same cert, seeded at `v2r/seed_sol_k86GL5_p1.json`, must reach
   **t = -0.076947399076 within 1e-9** (container: 17 LP solves, 4790 realisation rows, 174 s with highspy);
6. the start of a k86GV1 run (the lane's exact command, `maxit=1`, stopped once its patterns are loaded): its first 9 log lines
   (f2b7, f2b rules, gkeys 240 / 89 payer-7 -> k192, p1r, v2r, jcheck, exname, `patterns: 306 files read`) identical to the
   container's GV1 setup smoke (`ref/v2/smoke_GV1.log`).

It writes `smoke_v2.ok` on PASS (launch_v2.sh requires it) and logs `smoke_v2*.log`.

## 4. What comes back (outbox/v2lower/)

Filled by `v2r/outbox86V.sh` (a copy of the lower lane's outbox86L.sh for eng_v2), every 60 s: each time `eng_v2/cert_k86GV1_p1.json`
changes (a new lext phase-1 cert, written only when t1 > 1e-9), once its size is stable and it parses as JSON:

* `cert_k86GV1_p1_NN_<md5 8>.json` and `sol_k86GV1_p1_NN.json`;
* one line in `P1.txt`: `NN  md5  t1 <value>  it <iteration>  filed-at` (exactly the lower lane's format);
* `K_k86GV1.log` (the whole K.log, refreshed), `P1_lines_k86GV1.txt` (all `lext it N: phase 1 ... t1 = ...` lines, including the
  negative ones before a cert exists) and `V2_lines_k86GV1.txt` (the `v2inner it` and `CROWDED` lines);
* `MD5SUMS`.

The phase-1 line is printed after the v2inner rounds, so each P1.txt t1 is the value of the cert filed with it. These t1 values and
certs are [M] until the container checks a cert (lowerR2 exactbasis, dual export, binding: `v2r/watchL86v.sh`, `dualwatch86v.sh`,
`bindwatch86v.sh` are included for reference but **not started here**; send the certs back with `collect_v2.sh`).

## 5. What the add-on contains and changes

* **eng_v2** (`fs/.../s86_f2b7/eng_v2/`): the container's engine copy as of 07:16Z 8 Nov (md5s: v2r.py f9dba8ab, prelay2.py 38d0fd57,
  edge56.py eec77a16, pcheck.py 7c3c69b8; all in `ORIGMD5_v2.tsv` and `ref/v2/eng_v2_md5_at_copy.txt`). Another change (an upperR2
  v2 mode) was being added to the container's eng_v2 at the same time; it is not in this copy and GV1 does not need it. Patches:
  * the highspy import at every import site (prelay.py 1, prelay2.py 2, pslite.py 1, psolve.py 2, v2r.py 1) falls back to the numpy /
    scipy shim `hshim.py` next to pcheck.py when highspy is missing (`HSHIM_FORCE=1` forces the shim);
  * v2r.py: the W6b KEYSPEC2 test-vector folder (`KS2`, used only by `v2rtest`) points into this pack;
  * added `hshim.py` (1.1) and `jsep3.cpp` (from P_own_lp/, as in the main pack); `jsepf_gk.cpp` / `jsepf_gk_k192.cpp` are
    byte-identical to eng_p1r's.
* **hshim 1.1** (eng_v2 only; eng / eng_p1r keep 1.0): adds `Highs.getLp()` (a HighsLp with column-wise `a_matrix_`, as highspy
  returns it; v2restricted uses it for its scipy cross-check) and `Highs.clearSolver()` (drops status / basis / solution; v2inner's
  cold phase-1 re-solves call it). Everything else is unchanged from 1.0. Tested in the container against highspy 1.15.1:
  getLp and clearSolver on 60 random LPs with 180 re-solves (max relative objective difference 1.2e-16), the 1.0 regression tests
  (hshim_check 80 solves: 1.4e-14; 100 small LPs x 3 with ipm and simplex: PASS).
* **v2r/**: `runK86v.sh` (the K-run wrapper, unchanged apart from paths), `outbox86V.sh` (Mac, new), the seed
  `seed_sol_k86GL5_p1.json` (e537d18d), `rows_k86GL6_snap_GV1.txt` (complete lines of the container's eng_p1r/rows_k86GL6.txt at
  07:32Z 8 Nov, 8657 lines: the container launcher's own GL6-rows warm file; GL5's rows file is empty), README / NOTES /
  V2ROW_SPEC and the spec vectors, the container watchers (not started).
* `launch_k86GV1.sh` (Mac copy), `maclane_warm_v2.txt` (k86GL6's launch warm list, 43 files already in the pack, + the GL6 snapshot),
  `args_A97_F_W13K3gB5b.txt`, the three K5 pattern files it adds (`w13/pat_K5h01_C.cfast`, `pat_K5b_C.cfast`, `pat_K5b_D.out`),
  `p1r/cg_keys_r13w16_16fi.txt` (smoke steps 4-5), the GL5 cert def2afcc and the W6b `test_vectors.json` (smoke).
* top level: `build_v2.sh`, `smoke_v2.sh`, `launch_v2.sh`, `status_v2.sh`, `stop_v2.sh`, `collect_v2.sh`, `tools/cmp_v2.py`,
  `tools/v2shimcheck.py`, `ref/v2/` (container logs the smoke compares with, the container's launcher and queue scripts).
* Records: `v2addon/` in the pack (MANIFEST_v2.md5, ORIGMD5_v2.tsv, INSTALLED_v2.tsv, INSTALLED.txt, this README).

Paths: as in the main pack, every container path becomes `<pack>/fs/<container path>`; install_v2 rewrites the packed root
`/tmp/maclane-k86` to the pack's root. All scripts are bash 3.2 / BSD-tool safe (no associative arrays, no `case` inside `$( )`,
`md5sum` / `timeout` come from the pack's macshim); all python is 3.9-safe.

## 6. What was tested before packing (container, 8 Nov 2026)

All in a copy of the unpacked main pack (the copy tested before maclane-k86.tgz was sent), moved to a new folder; the container's
highspy was hidden from eng_v2 with `HSHIM_FORCE=1`, so every LP went through the shim as on the Mac; nice 19, one test at a time.

* **install_v2.sh**: refused before `relocate.sh` (as intended); after it: 75 files written, the packed root rewritten in 16 files
  (94 occurrences), build_v2 OK (clang 18.1.3 on x86-64, same flags). Run again: 0 written, 75 identical. An installed file edited
  by hand: CONFLICT, nothing written. Pack folder moved + `relocate.sh`: the add-on's files were rewritten too, and install_v2 then
  found all 75 identical.
* **smoke_v2.sh: SMOKE-V2: PASS**, all 6 steps, under strace:
  2. hshim_check 80 solves, max relative objective difference 1.36e-14; v2shimcheck 40 LPs / 120 re-solves after clearSolver,
     max objective difference 1.35e-16;
  3. 20 eng_v2 modules parse;
  4. v2rtest: 24 / 24 test vectors, all 37 lines of the container's log identical after normalising, `V2R-TEST: PASS (0 failures)` (108 s);
  5. v2restricted v2: **t = -0.076947399076 after 17 LP solves** (unrounded -0.07694739907598082 vs the container's
     -0.07694739907589576: 8.5e-14), 104 s. It ends with 4634 realisation rows where the container had 4790: the shim's IPM + crossover
     can stop at a different optimal vertex, so different argmax rows enter, but the restricted optimum is the same;
  6. GV1 start: the first 9 log lines identical to the container's (`gkeys: 240`, `gkeys: 89 payer-7 keys > 64: leaf binary
     .../eng_v2/bin/jsepf_gk_k192`, `patterns: 306 files read, 2 missing [r_3, r_4]` as in the container), 3 s.
  The peak RSS of the whole smoke was 557 MB. File opens: 0 outside the pack under the container's paths, 0 failed opens inside `fs/`.
* `v2r/outbox86V.sh` on a fake phase-1 cert: cert / sol copied, `P1.txt` line `01  <md5>  t1 0.000123456789  it 0  <time>`,
  `V2_lines` / `P1_lines` / `MD5SUMS` written, run.log line.
* `launch_k86GV1.sh` checks (with its two nohup lines disabled): refuses without smoke_v2.ok (exit 2) and while a `tag=k86ML1`
  process runs (exit 3); with `ALLOW_ML1=1` it builds 44 warm files (43 + the GL6 snapshot) and writes its run.log line.
* `status_v2.sh`, `stop_v2.sh`, `collect_v2.sh` on an idle lane.
* Static checks: `bash -n` and a bash-4 / GNU-tool scan on all 14 add-on scripts; a Python 3.9 syntax / API scan on all .py: 0 findings.

## 7. Not verified

* bash 3.2 and the BSD tools on a real Mac (static checks only: `bash -n`, a GNU-ism scan, the same idioms as the main pack, which
  runs on the Studio); clang on arm64 (the container build used clang 18 on x86-64 with the same flags).
* A full GV1 run here (memory and time per iteration): the container cannot hold one next to its own lanes. The container's own GV1
  smokes (`ref/v2/smoke_GV1.log`, `smoke2_GV1.log`) ran on a small warm set with highspy.
* The eng_v2 separator binaries in a run (the smoke stops before the first separation). Their sources are byte-identical to eng_p1r's,
  whose Mac build the k86ML1 lane has been running.
* The shim on GV1-size phase-1 LPs with v2inner re-solves: each re-solve is a fresh scipy HiGHS solve (no warm start), so a v2inner
  round costs about one phase-1 solve (k86ML1's phase-1 LP took 905 s on the Mac).

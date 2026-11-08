# maclane-k86 k5d add-on: kill families K5c + K5d on the Mac (GV1 on K3gB5d, upper rechecks on K3l5d)

Made 8 Nov 2026 in the Opus container (P_own_lp/s86_f2b7, files copied 08:17Z). A small add-on for the maclane-k86 pack
(`maclane-k86.tgz`, 2fa853ec) **with the v2 add-on already installed** (`maclane-k86-v2addon.tgz`, 138c2965). It adds files only:
no installed file is changed, and the running lanes are not touched.

What changed: K5c V1-V8 is [E2] (Studio K3CHK10) and K5d B1 is [E2] (ST-49 + K3CHK, main d8950ae17). The new families only add kills:

| family | args (container md5) | = | used for |
|---|---|---|---|
| **K3gB5d** | `args_A97_F_W13K3gB5d.txt` (ec9d8dbb) | K3gB5b (5e399535) + `w13/pat_K5c_D.out` (7da1cacd) + `w13/pat_K5c_C.cfast` (e7a63953) + `w13/pat_K5d_D.out` (c5c4c210) | the v2 lower lane **k86GV1** (`launch_v2d.sh`) |
| **K3l5d** | `args_A97_F_W13K3l5d.txt` (399cfc4c) | K3l5 (2547de87) + the same three files | upper rechecks (`recheck_k5d.sh`), as the container's k86GS7 ladder |

The K5h01 / K5b pattern files both families also name came with the v2 add-on. The two args files are prefix-rewritten like every
args file in the pack, so `relocate.sh` keeps working on them. With the pack root taken out, their md5s are the container's
(smoke step 2 checks this).

## 1. Commands

    cd ~/maclane                                    # the folder that holds maclane-k86/ (use your own path)
    md5 -q /path/to/maclane-k86-k5d.tgz             # must print the md5 in maclane-k86-k5d.tgz.md5
    tar -xzf /path/to/maclane-k86-k5d.tgz           # creates ~/maclane/maclane-k86-k5d/
    bash maclane-k86-k5d/install_k5d.sh ~/maclane/maclane-k86     # checks and copies; nothing to compile
    cd ~/maclane/maclane-k86
    bash smoke_k5d.sh       # about 10 min, 1 thread, < 1.5 GB; must end with "SMOKE-K5D: PASS" (section 3)

    # the v2 lower lane k86GV1 on K3gB5d (same tag, flags, 240 keys and warm set as launch_v2.sh)
    bash stop_v2.sh         # only if k86GV1 is already running (on K3gB5b)
    bash stop.sh lower      # only if the k86ML1 control lane still runs (GV1 replaces it)
    bash launch_v2d.sh      # needs smoke_k5d.ok or smoke_v2.ok; otherwise FORCE=1 bash launch_v2d.sh
    bash status_v2.sh       # as before; outbox/v2lower/ as before, plus FAMILY.txt

    # upper rechecks on K3l5d + 240 keys (eng_p1r), e.g. the Mac's repS1MW_02 (t = 0.027086414643)
    bash recheck_k5d.sh repS1MW_02          # about 5 min on 1 thread; prints the UPPER-R2 verdict
    bash recheck_k5d.sh sol_repS1MW_02 2    # the same with 2 threads; any cand/ name or a sol json path works

`install_k5d.sh` follows the same rules as `install_v2.sh`:
* every payload file is checked against MANIFEST_k5d.md5;
* the folder must be the maclane-k86 pack, relocated, with the v2 add-on installed;
* the packed root is rewritten to the pack's root;
* a file the pack already has with other content stops the install before anything is written;
* identical files are skipped, so a second run is harmless.

Its records go in `<pack>/k5d/`.

**The ST-51 v2 smoke failure.** On the Studio, the v2 smoke failed step 4 only on 3 extra lines like
`<string>:166: RuntimeWarning: divide by zero encountered in matmul` (also `overflow` and `invalid value`). numpy 2.0.2 with Apple
Accelerate BLAS raises these spurious floating-point flags in v2r.py's 0/1-mask matmul, whose operands are finite; the results matched.

The installed `tools/cmp_v2.py` cannot be replaced (install never overwrites a file), so this add-on ships **`tools/cmp_v2b.py`**. It drops
lines matching `^<string>:\d+: RuntimeWarning: (divide by zero|overflow|invalid value) encountered in matmul$` from both logs, prints
how many it dropped, then compares as before (its summary now also counts extra lines). `smoke_k5d.sh` step 3 reruns that v2rtest
with it. On PASS it writes `smoke_k5d.ok`, which `launch_v2d.sh` accepts, as it accepts `smoke_v2.ok`; FORCE=1 overrides both.

## 2. launch_v2d.sh (k86GV1 on K3gB5d)

It runs `fs/.../s86_f2b7/launch_k86GV1d.sh`. This is the v2 add-on's `launch_k86GV1.sh` with these changes:

* `ARGS` defaults to K3gB5d (`ARGSV=` overrides);
* if an earlier k86GV1 run left rows (`eng_v2/rows_k86GV1.txt`), their complete lines are snapshotted to
  `v2r/rows_k86GV1_snap_<UTC>.txt` and added to the warm list (`V2_WARM_PREV=0` skips). The family only adds kills, and rows it no
  longer admits are dropped on admission;
* the earlier run's K.log is kept as `runK_k86GV1/K_prev_<UTC>.log` and `outbox/v2lower/K_k86GV1_prev_<UTC>.log`, because runK86v.sh
  truncates K.log;
* `outbox/v2lower/FAMILY.txt` gets a line `<time>  k86GV1 started on args_A97_F_W13K3gB5d.txt (container md5 ec9d8dbb): certs from number
  NN on are this family`. The P1.txt format is unchanged.

Everything else is unchanged:
* tag k86GV1;
* keys `p1r/cg_keys_r13w16_16fik.txt` (3d996dbb, 240; 89 payer-7 -> `eng_v2/bin/jsepf_gk_k192`);
* flags GL6 + `p1r v2r v2seed v2rescan=1 v2inner=4`;
* warm `maclane_warm_v2.txt` + k86ML1 rows;
* the same knobs (`V2_THREADS` 2, `V2INNER` 4, `MAXIT`, `TAG`, `V2_WARM_ML1`, `ALLOW_ML1`, `FORCE`).

status_v2.sh, stop_v2.sh and collect_v2.sh work unchanged (same tag).

## 3. recheck_k5d.sh (upper points on K3l5d)

`bash recheck_k5d.sh <point> [threads]` runs the exhaustive upperR2 (gkwin gkleaf) the container's k86GS7 ladder uses for its K3l5d
rechecks (repladder_e.py `REPL_ARGS2` -> `U86.sh` with `E86OVR=eng_p1r`):
* engine `eng_p1r` (its jsepf_gk_k192 from build.sh), args K3l5d, keys `p1r/cg_keys_r13w16_16fik.txt`;
* flags `c6le f2b7 f2b=rules/A5final/rules_c67fa1d1_plus_A5_twins.json rpatN=rpat/rpatN3_rotation_justified.txt` (8b90a842).

The pack's env86.sh predates the container's `E86OVR` line, and installed files are never edited, so the check runs through a new
`U86e.sh`. U86e.sh is U86.sh setting `E86=${E86OVR:-eng}` itself, with work dir `wr86r_<tag>`, which `stop.sh upper` does not match.

Results:
* `logs/upper_F_<name>_K3l5d.log` and a run.log line;
* `outbox/k5d/`: a copy of the log and one line in `RECHECK.txt`: `name  md5  K3l5d  UPPER-R2 verdict  log  checked-at`.

`collect.sh` already packs all of `outbox/`. Exit status 0 = FEASIBLE. `RECHECK_ARGS=<args file>` checks another family, e.g. K3l5
(already in the pack). The upper lane k86MS1 itself is not changed by this add-on.

## 4. Smoke test (smoke_k5d.sh)

1. installed: the v2 add-on (eng_v2 and its binaries), this add-on's files, eng_p1r's separators;
2. K3gB5d / K3l5d have the container md5s ec9d8dbb / 399cfc4c (pack root taken out), and every file they name is in the pack.
   The 2 files the patterns line reports missing, `out/job28/r_3.cfast` and `r_4.cfast`, are missing in the container too;
3. the v2 smoke's step 4 (v2rtest on the GL5 cert def2afcc) again, compared with `cmp_v2b.py`: 24 / 24 test vectors,
   `V2R-TEST: PASS (0 failures)`, all lines as the container's, and the number of matmul-warning lines dropped is printed;
4. `bash recheck_k5d.sh` on the Mac's own point repS1MW_02. It is shipped as `ref/k5d/sol_S1MW02k240d.json` (356beaa0, the
   container's `cand/sol_S1MW02k240d.json`). The whole log must match the container's `logs/upper_F_S1MW02k240d.log`, including
   **UPPER-R2: FEASIBLE at t = 0.027086414643**. The one exception is the container log's line `sender rows: min value 0.972914413731 ->
   senders need t >= 0.027085586269`. That is a diagnostic the container's eng_p1r gained at 06:39Z (prelay2.py, s86 tighten), after
   the pack's eng_p1r copy was taken; it is the only difference between the two engines;
5. the start of k86GV1 on K3gB5d (launch_v2d.sh's command, maxit 1, stopped once the patterns are loaded). Its first 8 lines must be
   as the container's GV1 smoke (`ref/v2/smoke_GV1.log`), and its patterns line exactly as expected (below).
   `SMOKE_K5D_HEAD=0` skips this step.

## 5. EXPECT counts (EXPECT_K3l5d_k240.txt)

`EXPECT_K3l5d_k240.txt` sits next to this README and in the pack as `ref/k5d/` and `k5d/`. It uses the format of
`from_opus/s86_k86GS5/EXPECT_K3l5_k240.txt`: container log lines with paths stripped. Patterns lines ("by kind", after exname):

| family, flags | files read | distinct by d | by kind |
|---|---|---|---|
| K3l5d + 240 keys, rpatN 8b90a842 only (upper / recheck) | 310, 2 missing (r_3, r_4) | {7: 9360, 8: 5908, 9: 3320, 10: 1426, 11: 613, 12: 85, 13-17: 65} | D 18142, C 703, RPAT 158, RPATN 2034 |
| K3gB5d + 240 keys, rpatN 8b90a842 only (container k86GS7 LP) | 309, 2 missing | {7: 9387, 8: 5943, 9: 3417, 10: 1426, 11: 613, 12: 85, 13-17: 65} | D 18232, C 772, RPAT 158, RPATN 2034 |
| K3gB5d + 240 keys, GV1 flags (rpatN 8b90a842 + offc_K3g 2f4f0f02) | 309, 2 missing | {7: 9455, 8: 5966, 9: 3430, 10: 1439, 11: 626, 12: 105, 13-17: 85} | D 18232, C 772, RPAT 158, RPATN 2284 |

**Re-derived, not copied.** The first row was reproduced line for line by this add-on's own upperR2 run of the pack (smoke step 4).
The third row comes from its GV1 start (step 5).
* Its D and C equal the container's k86GS7 values (row 2).
* Its RPATN and distinct-by-d exceed row 2 by exactly what the offc rpatN file adds on K3gB5b: GS5 vs the v2 GV1 smoke,
  +250 RPATN, distinct +68 / +23 / +13 / +13 / +13 / +20.
* The coordinator's K3l5d / K3gB5d values (rpatN 8b90a842 only) agree with rows 1 and 2. There is no difference to report.
* GV1's RPATN 2284 is not a discrepancy: GV1's flags add the offc rpatN file, as on K3gB5b.

## 6. What was tested (container, 8 Nov 2026)

All tests used a relocated copy of the unpacked main pack with the v2 add-on installed. The container's highspy was hidden
(`HSHIM_FORCE=1`), as on the Mac. Everything ran at nice 19, one test at a time, under a memory gate (MemAvailable >= 3000 MB), with
strace on the smoke run.

**install_k5d.sh**
* 19 files written; the packed root was rewritten in 7 files (73 occurrences).
* Installed over a preliminary build of this add-on: it replaced only the files that had changed.
* A deleted installed file was written again.
* A pack without the v2 add-on was refused, with nothing written.

**smoke_k5d.sh: SMOKE-K5D: PASS**, all 5 steps:
2. K3gB5d ec9d8dbb, K3l5d 399cfc4c; every file they name is present;
3. v2rtest: 24 / 24, all lines as the container's, `V2R-TEST: PASS (0 failures)` (101 s). The container's numpy prints no matmul
   warnings. The filter itself was tested on a v2rtest log with the 3 ST-51 warning lines injected: 3 dropped, PASS. A non-matmul
   warning line still fails;
4. `recheck_k5d.sh` on S1MW02k240d (= the Mac's repS1MW_02, 356beaa0): **UPPER-R2: FEASIBLE at t = 0.027086414643** (289 s,
   1 thread). All 40 lines match the container's log, apart from the diagnostic line explained in section 4. Patterns 310 files, by
   kind D 18142, C 703, RPAT 158, RPATN 2034;
5. GV1 start on K3gB5d: the first 8 lines as the container's GV1 smoke. Patterns 309 files, by kind D 18232, C 772, RPAT 158, RPATN 2284 (3 s).

* Peak RSS of the whole smoke was 1.59 GB, during the upperR2 recheck; the lowest MemAvailable seen was 6.2 GB.
* File opens: 0 outside the pack under the container's paths, 0 failed opens inside `fs/`.
* A first run failed steps 2 and 4: the step-2 missing-file list was a lone space (empty-list bug, fixed), and the container log has
  the extra diagnostic line. Both are fixed in this tarball; the run above is with the shipped files.

**launch_k86GV1d.sh**, with its two nohup lines disabled:
* refuses without smoke_v2.ok / smoke_k5d.ok (exit 2);
* with FORCE=1 and a fake earlier run:
  * its K.log is kept as `runK_k86GV1/K_prev_<UTC>.log` and `outbox/v2lower/K_k86GV1_prev_<UTC>.log`;
  * its rows are snapshotted, complete lines only (a partial last line is dropped);
  * FAMILY.txt gets `... started on args_A97_F_W13K3gB5d.txt (container md5 ec9d8dbb): certs from number 02 on are this family`;
  * the run gets 45 warm files (43 + the GL6 snapshot + the earlier rows), and the run.log line names K3gB5d with ec9d8dbb.

**Other checks**
* `recheck_k5d.sh` with an unknown point or no argument: exit 2 with a usage message.
* Static: `bash -n` and the bash-4 / GNU-tool scan on the 6 scripts; the Python 3.9 scan on the 2 .py files: 0 findings.

## 7. Not verified

* bash 3.2 / BSD tools / Accelerate on the Mac (static checks only; the scripts use the same idioms as the pack and the v2 add-on,
  which run on the Studio).
* A full k86GV1 run on K3gB5d (the container's memory does not allow one next to its two LPs). The container's own K3gB5d LP is
  k86GS7 (eng_p1r, no v2r).
* That every row of a previous K3gB5b GV1 run is admitted under K3gB5d: rows the new kills remove are dropped at admission, which the
  K.log reports in its `warm rows admitted` line.

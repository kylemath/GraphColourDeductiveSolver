# maclane-k86 k5e add-on: the Mac upper lane on K5e (k86MS1 -> k86MS2)

Made 8 Nov 2026 in the Opus container (P_own_lp/s86_f2b7, files copied 10:45Z). A small add-on for the maclane-k86 pack
(`maclane-k86.tgz`, 2fa853ec) **with the v2 add-on (138c2965) and the k5d add-on (86045dcd) already installed**. It adds files only:
no installed file is changed, and nothing runs until you launch it.

The Lead approved moving the Mac upper lane MS1 to the K5e family with the 240 keys. K-5e B2 (one C kill, b9_u556575..._..56.....
X={I0-I1}) is [E2] by Studio K3CHK11. The new families add exactly that file to the K5d ones:

| family | args (container md5) | = | used for |
|---|---|---|---|
| **K3gB5e** | `args_A97_F_W13K3gB5e.txt` (8849c09f) | K3gB5d (ec9d8dbb) + `cpat=w13/pat_K5e_C.cfast` (9d00aa01) | the LP of **k86MS2** (as the container's k86GS9) |
| **K3l5e** | `args_A97_F_W13K3l5e.txt` (2b31d32d) | K3l5d (399cfc4c) + the same file | every check of k86MS2's points, and `recheck_k5e.sh` |

As before, the args files are prefix-rewritten, so `relocate.sh` keeps working on them; with the pack root taken out their md5s are
the container's (smoke step 2 checks this).

## 1. Commands (on the Studio)

    cd ~/maclane                                    # the folder that holds maclane-k86/ (use your own path)
    md5 -q /path/to/maclane-k86-k5e.tgz             # must print the md5 in maclane-k86-k5e.tgz.md5
    tar -xzf /path/to/maclane-k86-k5e.tgz           # creates ~/maclane/maclane-k86-k5e/
    bash maclane-k86-k5e/install_k5e.sh ~/maclane/maclane-k86     # checks and copies; nothing to compile
    cd ~/maclane/maclane-k86
    bash smoke_k5e.sh       # about 20 min (17 in the container); must end with "SMOKE-K5E: PASS" (section 7). k86MS1 may keep running meanwhile.

    DRY=1 bash launch_upper_k5e.sh     # the plan only: in-point candidates, warm set, the k86MS2 command; stops / starts nothing
    bash launch_upper_k5e.sh           # stops k86MS1 cleanly, picks the in-point, starts k86MS2 (section 2)
    bash status_k5e.sh                 # k86MS2: K run, ladder / tighten / in-point lines, outbox points by family
    bash stop_k5e.sh                   # stops k86MS2 (results kept); bash launch_upper_k5e.sh restarts it

    bash recheck_k5e.sh repS1MW_07     # any upper point on K3l5e + 240 keys (eng_p1r), about 5 min on 1 thread; 2nd arg = threads

The lane's knobs are the same as k86MS1's: `UPPER_THREADS`, `MAXIT`, `REPL_PAR`, `REPL_MINMEM`, `TIGHTWATCH`, `TIGHT_MINMEM`,
`HSHIM_SOLVER`. When they are not set, k86MS2 takes k86MS1's threads, maxit and REPL_PAR from k86MS1's own run.log lines (default
2 / 200 / 2), so the core budget does not change. Example: `UPPER_THREADS=3 bash launch_upper_k5e.sh`.

## 2. launch_upper_k5e.sh

1. **Checks before anything is stopped.** smoke_k5e.ok must be there (FORCE=1 overrides). k86MS2 must not be running. The fallback
   in-point is **sol_repS1MW_07** (t 0.025171803977, md5 e4e93b2c; FEASIBLE on K3l5e + 240 keys in the container, where it is
   cand/sol_S1MW07k240e.json). It is looked up in cand/, then outbox/upper/. If run.log has no FEASIBLE K3l5e + 240-key check of this
   exact file yet, it is checked now with `recheck_k5e.sh` (2 threads; k86MS1 keeps running meanwhile). If that check fails, the script
   stops and nothing has been stopped.
2. **Stops k86MS1 cleanly** with the pack's own `TAG_UPPER=k86MS1 bash stop.sh upper` (its watchers first, then the ladder, tighten
   and checks, then the K run), and waits until it is gone. Its outbox/upper points, `eng/rows_k86MS1.txt` and `runK_k86MS1/K.log`
   are not touched. One last outbox pass then files any FEASIBLE k86MS1 point that its outbox86.sh (120 s poll) had not filed yet,
   exactly as outbox86.sh would (plain name, family K3l), but only when its run.log check is a K3l + r13w16 check of that same file.
   run.log gets `[maclane] k5e: stopped k86MS1 for k86MS2 (last iteration: ...)`.
3. **In-point.** It takes the **newest outbox/upper point that passes the K3l5e recheck**. Candidates are the POINTS.txt lines filed
   after sol_repS1MW_07, with family K3l or K3l5e and a t below sol_repS1MW_07's, newest first, one per md5, at most
   `K5E_MAXRECHECK` (3). For each candidate:
   * a point already FEASIBLE on K3l5e here (k86MS2's own points, earlier rechecks) is taken without a new check;
   * a point already checked here and found not FEASIBLE is skipped;
   * otherwise it is rechecked (`recheck_k5e.sh`); the first FEASIBLE one wins.

   If none passes, the fallback is used. A point given on the command line (`bash launch_upper_k5e.sh <point>`, or `INPOINT=`) is used
   as is, with no search, but it must pass the same check. run.log gets `[maclane] k5e: in-point for k86MS2: <name> (md5 ...)`.

   **Container news (11:45Z, after these files were copied):** the container's k86GS9 ladder restarted from the Mac's
   **sol_repS1MW_11** (`cand/sol_S1MW11k240e.json`, md5 **cc688e1e**, t **0.023563634629**), FEASIBLE on K3l5e + 240 keys there. If the
   Studio's sol_repS1MW_11.json has that md5, the search finds it as long as it is among the 3 newest candidates (raise `K5E_MAXRECHECK`
   otherwise), or name it: `bash launch_upper_k5e.sh repS1MW_11` (still rechecked here first, about 5 min on 2 threads).
4. **Starts k86MS2** with `fs/.../s86_f2b7/launch_k86MS2.sh <in-point>` (section 3).

## 3. The k86MS2 lane (launch_k86MS2.sh)

k86MS2 is the pack's k86MS1 (same in-out flags, separator threads, maxit, ladder settings) moved to the K5e family and the 240 keys.
For the flags, the reference is the container's `launch_k86GS9.sh` (shipped in `ref/k5e/container_scripts/`).

| | k86MS1 (pack) | **k86MS2** (this add-on) | container k86GS9 |
|---|---|---|---|
| LP family | K3l (2727d445) | **K3gB5e** (8849c09f) | K3gB5e |
| keys | r13w16 (171) | **p1r/cg_keys_r13w16_16fik.txt** (240, 3d996dbb), standard coefficients | same |
| engine | eng (runK86.sh) | **eng_p1r** (p1r/runK86p.sh: jsepf_gk_k192 for the 89 payer-7 keys) | eng_p1r |
| K run | `runK86.sh 200 2 k86MS1 inout=0.4,0.8,0.1 inoutk=4 inoutmove inoutprobe=0.25 inoutnprobe=3 q7pen=1e-3 feascols feasall consk=20 consfrac=0.25` | the same flags on p1r/runK86p.sh, tag k86MS2 | the same, tag k86GS9 |
| in-point checks | watch86.sh on K3l | **watch86_k5e.sh on K3l5e** (eng_p1r) | watch86e.sh on K3gB5e |
| repair ladder | repladder.py, family K3l, REPL_FAM MW, REPL_PAR 2, REPL_MINMEM 0 | **repladder_k5e.py**: main check on K3gB5e (it decides the new in-point that is injected into the LP), **sub-check of every new in-point on K3l5e** (REPL_ARGS2); REPL_FAM MW, REPL_PAR / REPL_MINMEM as k86MS1 | repladder_e.py: main K3gB5e, sub K3l5e |
| tightening | tightwatch.sh / tighten.sh on K3l | **tightwatch_k5e.sh / tighten_k5e.sh on K3l5e**, only points already FEASIBLE on K3l5e (in-points, ladder sub-checks) | tightwatch.sh on K3l5e, triggered by the LP-family verdict |
| outbox | outbox86.sh, plain names, family column K3l | **outbox86_k5e.py**: `<name>__K3l5e` / `<name>__K3gB5e` (section 4) | file86.sh to the swarm |

Every check goes through the k5d add-on's `U86e.sh`, with `E86OVR=eng_p1r`, flags `c6le f2b7 f2b=<rules c67fa1d1 + A5 twins>
rpatN=<rpatN3 rotation-justified>` and the 240 keys. Ladder points are named `sol_repS2MW_NN` (k86MS1's were `sol_repS1MW_NN`);
in-points are `sol_k86MS2_inNN`; tightened points add `_tight`.

**Warm set.** It is k86MS1's warm list (`runK_k86MS1/warmlist.txt`, or `maclane_warm_upper.txt` when k86MS1 never wrote one) plus the
complete lines of k86MS1's rows (`eng/rows_k86MS1.txt` -> `warm/rows_MS1_snap_k86MS2.txt`; a partial last line is dropped; the name leaves out "k86MS1", so
`pgrep -fl k86MS1` never lists k86MS2's K run). Rows the
K3gB5e family does not admit are dropped on admission (K.log `warm rows admitted`). On a restart of k86MS2, it uses the previous k86MS2
warm list plus the complete lines of its rows (`eng_p1r/rows_k86MS2.txt` -> `warm/rows_k86MS2_snap_<UTC>.txt`). The previous K.log is
kept as `runK_k86MS2/K_prev_<UTC>.log`, because runK86p.sh truncates K.log.

**In-point rule.** launch_k86MS2.sh refuses an in-point that has no FEASIBLE upperR2 check on K3l5e + 240 keys **of this exact file**
(same md5) on this machine, in run.log and in its log. It also refuses to start while k86MS1, its outbox86.sh or its repladder still
run (two LPs at most), or while k86MS2 runs. run.log gets `[maclane] launch k86MS2 (k5e): ...` with the families, md5s, in-point,
threads and warm count.

## 4. The outbox: the family is in the file name

The lane's points go to the same `outbox/upper/` the Studio already syncs. Each point is filed once, under the strongest family that a
check of exactly that file found FEASIBLE (run.log line + log, md5 matched):

* **`<name>__K3l5e.json` + `<name>__K3l5e.log`** come from an in-point check, a ladder sub-check or a tighten final on K3l5e.
  The log is that check's log;
* **`<name>__K3gB5e.json` + `.log`** is a ladder point that is FEASIBLE on the LP family but whose K3l5e sub-check ended without
  FEASIBLE: an LP in-point, **not** a K3l5e point. stop_k5e.sh's last pass also files ladder points whose sub-check never ran this way.

POINTS.txt keeps its columns (`name  t  md5  family  log  filed-at`). The k86MS2 lines read for example
`sol_repS2MW_03__K3l5e  0.02...  <md5>  K3l5e  sol_repS2MW_03__K3l5e.log  <time>`; k86MS1's lines stay as they were (plain
names, family K3l). So `<name>.json` exists for every POINTS.txt name, and a K3l point can never be read as a K3l5e one.
`recheck_k5e.sh` also files a K3l5e-FEASIBLE recheck there, e.g. `sol_repS1MW_07__K3l5e.json` next to k86MS1's `sol_repS1MW_07.json`
(same md5, two families, two lines). MD5SUMS is refreshed after every filing.

**Do not restart k86MS1 on this outbox after k86MS2 has run.** k86MS1's outbox86.sh files every unfiled `cand/` point with a FEASIBLE log
as K3l, and it does not know the `__K3l5e` names, so it would file k86MS2's points again as K3l. To go back to k86MS1: `bash stop_k5e.sh`,
then `OUTBOX_UPPER=<pack>/outbox/upper_ms1 bash launch_upper.sh`.

## 5. recheck_k5e.sh

`bash recheck_k5e.sh <point> [threads]` is recheck_k5d.sh for K3l5e. It runs the exhaustive upperR2 (gkwin gkleaf) on eng_p1r, args
K3l5e, the 240 keys and the flags above. The point can be a `cand/` name, an `outbox/upper/` name or a json path.

It writes:
* `logs/upper_F_<name>_K3l5e.log` and a run.log line;
* `outbox/k5e/`: the log and one line in `RECHECK.txt` (`name  md5  K3l5e  verdict  log  checked-at`);
* when FEASIBLE, `outbox/upper/sol_<name>__K3l5e.json` + `.log` and a POINTS.txt line (RECHECK_UPPER=0 skips this; the smoke test does).

Exit status 0 = FEASIBLE. `RECHECK_ARGS=<args file>` checks another family; nothing is then filed in outbox/upper.

A check that was killed (stop, Ctrl-C, low memory) leaves its work dir `fs/.../scratchpad/sD/wr86r_<tag>`, and U86e.sh reuses the class
table it finds there: the next log of that tag then lacks the `gkeys: mode-2 class fold` line (seen in the container after a low-memory
kill), and a half-written table could break the check. So recheck_k5e.sh and tighten_k5e.sh remove their tag's work dir before a new
check; recheck_k5e.sh stops with exit 2 when a check with the same tag is still running.

## 6. eng_p1t (tightening only)

Since 06:39Z the container's eng_p1r prints one more upperR2 line, `sender rows: min value V -> senders need t >= 1 - V` (3 lines in
prelay2.py, "s86 tighten"). tighten.sh's floor reads that line, but the pack's eng_p1r copy predates it, and installed files are never
edited. This add-on therefore ships `eng_p1t/prelay2.py` = the pack's eng_p1r/prelay2.py + those 3 lines. The build checks that this
equals the container's eng_p1r/prelay2.py (dde358ba) with the pack's highspy -> hshim patch.

`mkeng_p1t.sh` (run by tighten_k5e.sh, launch_k86MS2.sh and the smoke) links every other .py / .cpp file and `bin/` of eng_p1r into
eng_p1t, so the separators are the same binaries. Only tightening runs on eng_p1t; the LP, in-point checks, ladder checks and rechecks
run on eng_p1r, as in the container. Without eng_p1t, every tighten would stop at the floor step ("could not read the floor").

## 7. Smoke test (smoke_k5e.sh)

1. installed: the v2 / k5d add-ons, this add-on's files (bash -n / Python parse of its scripts), eng_p1r's separators;
2. K3gB5e / K3l5e have the container md5s 8849c09f / 2b31d32d (pack root taken out), pat_K5e_C is 9d00aa01, and every file they
   name is in the pack;
3. `recheck_k5e.sh` on the Mac's own point repS1MW_07, shipped as `ref/k5e/sol_S1MW07k240e.json` (e4e93b2c). The whole log must match the
   container's `logs/upper_F_S1MW07k240e.log`, including **UPPER-R2: FEASIBLE at t = 0.025171803977**. The one exception is the
   container's `sender rows: min value` line (section 6). Its EXPECT lines must equal section 1 of `EXPECT_K3l5e_k240.txt`;
4. `tighten_k5e.sh` on that point, outputs in `smoke_k5e_tight/`, not cand/. The probe log must carry the container's line
   `sender rows: min value 0.974829002395 -> senders need t >= 0.025170997605` exactly, and the final check must be FEASIBLE at
   t = 0.025170999 (within 2e-9; the container gave 0.025170999000 from the floor 0.025170997605, a gain of 8.0e-7). `SMOKE_K5E_TIGHT=0` skips this step (2 checks);
5. the start of k86MS2's K run (launch_k86MS2.sh's command on K3gB5e + 240 keys, eng_p1r, maxit 1, stopped once the conservation
   basis rows are in). Its first 11 lines must be as the container's k86GS9 K.log, and its EXPECT lines must equal section 2.
   `SMOKE_K5E_HEAD=0` skips this step;
6. `DRY=1 launch_upper_k5e.sh` with that point: the plan is made (in-point FEASIBLE on K3l5e here, warm list complete); nothing starts.

On PASS it writes `smoke_k5e.ok`. Nothing in the smoke touches k86MS1, outbox/upper or the other lanes. It adds one line to
`outbox/k5e/RECHECK.txt` (the Mac's own K3l5e recheck of repS1MW_07, which is worth keeping).

## 8. EXPECT counts (EXPECT_K3l5e_k240.txt)

`EXPECT_K3l5e_k240.txt` sits next to this README and in the pack as `ref/k5e/` and `k5e/`. Its format is the k5d one: container log lines
with paths stripped. Patterns lines:

| family, flags | files read | distinct by d | by kind |
|---|---|---|---|
| **K3l5e** + 240 keys, rpatN 8b90a842 (upper / recheck) | **311**, 2 missing (r_3, r_4, as in the container) | {7: 9360, 8: 5908, **9: 3321**, 10: 1426, 11: 613, 12: 85, 13-17: 65} | **D 18142, C 704, RPAT 158, RPATN 2034** |
| K3gB5e + 240 keys, rpatN 8b90a842 (k86GS9 / k86MS2 LP) | 310, 2 missing | {7: 9387, 8: 5943, 9: 3418, 10: 1426, 11: 613, 12: 85, 13-17: 65} | D 18232, C 773, RPAT 158, RPATN 2034 |

Both sections were re-derived from this add-on's own runs in the container (smoke steps 3 and 5, 8 Nov 11:07-11:24Z), not copied:
section 1 from the K3l5e recheck of repS1MW_07, section 2 from the start of the k86MS2 K run. Section 1 equals the coordinator's counts
(D 18142 / C 704 / RPAT 158 / RPATN 2034, distinct d9 3321, 311 files) and the container's own K3l5e log of the same point; section 2
equals the first lines of the container's k86GS9 K.log. Against K5d, each family reads one more file (pat_K5e_C), which adds exactly
1 C entry and 1 distinct d9 pattern: K3l5d 310 files, C 703, d9 3320 -> K3l5e 311, C 704, d9 3321; K3gB5d 309, C 772, d9 3417 ->
K3gB5e 310, C 773, d9 3418. D, RPAT and RPATN do not change.

## 9. What was tested (container, 8 Nov 2026)

Everything ran on test copies of the pack (maclane-k86.tgz + the v2 and k5d add-ons, relocated), never on the container's live runs,
one test at a time at nice 19, under a memory gate: start only with MemAvailable >= 4.8 GB and no container check running, kill the
test when MemAvailable drops below 3.0 GB.

* **Build.** 29 payload files. None of them is in the main pack or the v2 / k5d add-ons. eng_p1t/prelay2.py is checked to be the
  container's eng_p1r/prelay2.py (dde358ba) plus the pack's hshim patch.
* **Install** (from the tgz, into a fresh relocated pack): 29 files written. A second install wrote 0 (29 identical). With a different
  launch_upper_k5e.sh already in the pack it reported CONFLICT, exit 4, and wrote nothing. Without the k5d add-on it refused to start.
* **smoke_k5e.sh: SMOKE-K5E: PASS** in 15.5 min (12:21-12:37Z, peak RSS 1.6 GB, lowest MemAvailable 3.7 GB).
  * Step 3: the recheck took 289 s and its log equals the container's (0 of 40 lines differ).
  * Step 4: the tighten took 580 s. The probe has the sender line exactly, and the final check is FEASIBLE at 0.025170999000
    (floor 0.025170997605).
  * Step 5: 61 s; the first 11 lines equal k86GS9's.
  * Step 6: the DRY plan was made.

  That run started with stale work dirs left by checks the memory gate had killed (a recheck and a tighten probe). Both were cleared
  and the logs matched. An earlier run, made before the cleanup in section 5 existed, failed step 3 only because of that: the log had no
  `class fold` line.
* **test_k5e_lib.py: PASS** (23 checks on fabricated run.log lines). It covers:
  * the outbox in once and poll mode: which family each point gets, the POINTS.txt columns, MD5SUMS (POINTS.txt included), that the
    filed json is byte-identical, the log that goes with each point;
  * `verified`, `state`, `file` (refuses an INFEASIBLE check, files once);
  * `pick`: newest first, K3l / K3l5e only, t below the default, at most 3, never the default itself;
  * `prevpass`: plain names, family K3l;
  * `snaprows`: complete lines only.
* **test_tightwatch.sh: PASS.** tightwatch_k5e.sh tightens exactly the K3l5e-FEASIBLE in-point and the K3l5e-FEASIBLE ladder sub-check.
  It ignores the K3gB5e main check, INFEASIBLE checks, rechecks, probes, `_tight` finals, another lane and the container's
  NEW IN-POINT line.
* **The k86MS1 -> k86MS2 switch end to end** (integ_k5e.sh, in a test pack). The test pack had a fake k86MS1: a sleeping K run tagged
  k86MS1 plus the pack's real watch86, outbox86, tightwatch and repladder for k86MS1. It also had a newer K3l point at t - 0.001 that
  fails K3l5e, and an unfiled k86MS1 point. This run used the build before the last fixes (11:26-11:32Z). In it:
  * DRY made the plan and stopped or started nothing.
  * The switch stopped all of k86MS1, and its rows and K.log were untouched. The last outbox pass filed the unfiled point (plain name,
    K3l).
  * The newer point was rechecked: INFEASIBLE on K3l5e. The in-point was the default sol_repS1MW_07.
  * k86MS2 started with all six parts. Its K run start line is k86GS9's. The warm list was maclane_warm_upper.txt plus 200 complete
    k86MS1 rows; the partial row was dropped.
  * The K.log matched k86GS9's except for the in-point's file name.
  * stop_k5e.sh stopped everything.
  * The restart skipped the known-INFEASIBLE candidate without rechecking it and kept the previous K.log.

  Its 3 FAILs were fixed afterwards:
  * Two were the test's own mistakes. RECHECK.txt names have no `sol_` prefix, and the in-point file is named differently from the
    container's.
  * The third was real but cosmetic: k86MS2's command line held the k86MS1 rows snapshot name, so `pgrep -f k86MS1` listed k86MS2's K
    run. The snapshot is now `rows_MS1_snap_k86MS2.txt`; a traced DRY launch of the final build confirms the name.

  The rerun on the final build passed DRY, then the memory gate stopped it during the switch. From 12:44Z the container's own
  k86GS9 ladder ran checks back to back, which left about 4.5 GB, too little for another try.
* Earlier (exploratory) build: SMOKE-K5E PASS (17 min). That run gave the TT above.

## 10. Not verified

* bash 3.2 / BSD tools / Accelerate on the Mac. Only static checks were run, and the scripts use the same idioms as the pack and the
  earlier add-ons, which run on the Studio.
* The k86MS1 -> k86MS2 switch with the final build (section 9: the earlier build passed every step of it apart from the issues fixed
  since; the final build's DRY step passed).
* A full k86MS2 run. The container's memory does not allow one next to its two LPs. The container's own K3gB5e LP is k86GS9 (same
  command, same engine).
* That every k86MS1 row is admitted under K3gB5e. Rows the new family removes are dropped at admission; the K.log reports it.
